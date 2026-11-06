"""Módulo 1 · paso 5: tema léxico + clustering por SERP + métricas de clúster + viabilidad. Determinista.
Salida: data/keywords.csv, data/clusters.json
"""
import json, csv, re, sys, pathlib, yaml, collections
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
import unicodedata


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower().replace("œ", "oe").replace("’", "'"))
    return " ".join("".join(ch for ch in s if not unicodedata.combining(ch)).split())


def rx(terms):
    return re.compile(r"(?<![a-z])(" + "|".join(re.escape(norm(t)) for t in terms) + r")(?![a-z])")


R_CIU = rx(yaml.safe_load((dfs.BASE / "config/filtro.yml").read_text())["ciudades_zona"])
BASE = dfs.BASE
UMB = dfs.UMB
T = json.loads((BASE / "data/m1_tabla.json").read_text())
S = json.loads((BASE / "data/m1_serp.json").read_text())
LOC = json.loads((BASE / "data/m1_local.json").read_text())
TEMAS = yaml.safe_load((BASE / "config/temas.yml").read_text())["temas"]
D = json.loads((BASE / "data/m2_dominios.json").read_text())
R_TEMA = {k: rx(v["terminos"]) for k, v in TEMAS.items() if v["terminos"]}
N = UMB["clustering"]["urls_compartidas_top10"]

# filas de keywords: tabla + combinaciones locales con volumen que no estuvieran
rows = {r["keyword"]: r for r in T}
for k, v in LOC.items():
    fr = v.get("fr", {})
    if k not in rows and (fr.get("vol") or 0) > 0:
        rows[k] = {"keyword": k, "origen": "generica_ciudad", "variantes": "", "duplicado_de": "", "vol_ch_gads": fr.get("vol"),
                   "vol_ch_labs": None, "vol_be": None, "vol_fr": None, "vol_ne": None, "vol_vd": None,
                   "cpc_usd": fr.get("cpc"), "competencia_ads": fr.get("comp"), "kd": None, "intencion": None,
                   "tendencia_12m_pct": None, "serie_12m": ";".join(str(m[2]) for m in sorted(fr.get("monthly") or [])[-12:]),
                   "fuente": f"DataForSEO google_ads/search_volume (CH, fr) {dfs.HOY}"}


def vol(r):
    return r["vol_ch_gads"] if r["vol_ch_gads"] is not None else (r["vol_ch_labs"] or 0)


# posición actual de physioactiva.ch (Labs ranked_keywords CH fr/de) y SERP propia
pos = {}
for key in ("physioactiva.ch|fr", "physioactiva.ch|de"):
    res = D["ranked"].get(key)
    if isinstance(res, list) and res:
        for it in res[0].get("items") or []:
            k = it["keyword_data"]["keyword"]; s = it["ranked_serp_element"]["serp_item"]
            if k not in pos or s["rank_group"] < pos[k][0]:
                pos[k] = (s["rank_group"], s.get("url"))


def tema(kw, origen):
    if "competidor" in origen:
        return "marca_competidor"
    n = norm(kw)
    if re.search(r"(?<![a-z])massage", n) and R_CIU.search(n) and not re.search(r"therapeut|medical|sportif|physio", n):
        return "massage_bienestar"
    for k, r in R_TEMA.items():
        if r.search(n):
            return k
    return "local_generico"


for k, r in rows.items():
    r["tema"] = tema(k, r["origen"])
    m = R_CIU.findall(norm(k))
    r["ciudad"] = m[0] if m else ""
    sp = S.get(k)
    r["serp_ins"] = bool(sp and not sp.get("error"))
    r["pos_actual"] = pos.get(k, (None, None))[0]
    r["url_actual"] = pos.get(k, (None, None))[1]
    if r["pos_actual"] is None and sp and sp.get("physioactiva_pos"):
        r["pos_actual"], r["url_actual"] = sp["physioactiva_pos"], "(SERP Ins)"
    r["local_pack_physioactiva"] = bool(sp and any("Physio Activa" in (l.get("title") or "") for l in sp.get("local_pack", [])))

# clustering voraz por solapamiento de URLs (keywords con SERP), orden: volumen desc, keyword asc
con_serp = sorted([k for k in rows if rows[k]["serp_ins"] and rows[k]["tema"] != "marca_competidor"
                   and not rows[k].get("duplicado_de")],
                  key=lambda k: (-vol(rows[k]), k))
urls = {k: set(o["url"] for o in S[k]["organic"]) for k in con_serp}
asign, clusters = {}, collections.OrderedDict()
for h in con_serp:
    if h in asign:
        continue
    clusters[h] = [h]; asign[h] = h
    for k in con_serp:
        if k not in asign and len(urls[h] & urls[k]) >= N:
            clusters[h].append(k); asign[k] = h

# fusión: cabezas del mismo tema que Google Ads agrupa (mismo volumen y misma serie de 12 meses)
firma = {}
for h in list(clusters):
    sig = (rows[h]["tema"], vol(rows[h]), rows[h]["serie_12m"])
    if sig[1] and sig in firma:
        destino = firma[sig]
        for k in clusters.pop(h):
            clusters[destino].append(k); asign[k] = destino
    else:
        firma[sig] = h
for k in rows:  # duplicados declarados van con su original
    o = rows[k].get("duplicado_de")
    if o and o in asign and k not in asign:
        clusters[asign[o]].append(k); asign[k] = asign[o]

# keywords sin SERP: al clúster cuya cabeza esté contenida en la keyword (más larga gana); si no, al tema
def tokens(s):
    return set(w for w in re.split(r"[\s'\-:]+", norm(s)) if len(w) > 2)

cabezas = sorted(clusters, key=lambda h: (-len(tokens(h)), h))
for k in sorted(rows):
    if k in asign or rows[k]["tema"] == "marca_competidor":
        continue
    tk = tokens(k)
    for h in cabezas:
        if tokens(h) and tokens(h) <= tk and rows[h]["tema"] == rows[k]["tema"]:
            clusters[h].append(k); asign[k] = h; rows[k]["cluster_metodo"] = "léxico (sin SERP)"; break
for k in rows:
    rows[k]["cluster"] = asign.get(k, "")
    rows[k].setdefault("cluster_metodo", "SERP (≥%d URLs)" % N if k in asign else "")

FI = UMB["prioridad"]["factor_intencion"]
cl_out = []
for h, ms in clusters.items():
    seen, vtot = set(), 0
    for k in ms:  # no sumar dos veces variantes que Google Ads agrupa (misma serie)
        sig = (vol(rows[k]), rows[k]["serie_12m"])
        if sig in seen and sig[0]:
            continue
        seen.add(sig); vtot += vol(rows[k]) or 0
    sp = S[h]
    clases = collections.Counter(o["clase"] for o in sp["organic"])
    ints = collections.Counter(rows[k]["intencion"] for k in ms if rows[k]["intencion"])
    paa = []
    for k in ms:
        for q in (S.get(k) or {}).get("paa", []):
            if q and q not in paa:
                paa.append(q)
    temas = collections.Counter(rows[k]["tema"] for k in ms)
    lp = bool(sp["local_pack"])
    cl_out.append({
        "cluster": h, "tema": temas.most_common(1)[0][0], "n_keywords": len(ms), "keywords": ms,
        "volumen_agregado": vtot, "kw_principal_vol": vol(rows[h]), "intencion_dominante": ints.most_common(1)[0][0] if ints else None,
        "top10_clinicas": clases.get("clínica/physio", 0), "top10_portales": clases.get("portal/medio/institución", 0),
        "top10_otros": clases.get("otro", 0), "local_pack": lp,
        "physioactiva_en_local_pack": any("Physio Activa" in (l.get("title") or "") for l in sp["local_pack"]),
        "ai_overview": sp["ai_overview"], "ai_citas": sorted(set(x for x in sp["ai_citas"] if x))[:8],
        "paa": paa[:8], "top3": [f'{o["pos"]}. {o["domain"]}' for o in sp["organic"][:3]],
        "physioactiva_mejor_pos": min([rows[k]["pos_actual"] for k in ms if rows[k]["pos_actual"]] or [None], key=lambda x: x or 999),
        "kd_media": round(sum(rows[k]["kd"] for k in ms if rows[k]["kd"] is not None) / max(1, sum(1 for k in ms if rows[k]["kd"] is not None)), 1)
        if any(rows[k]["kd"] is not None for k in ms) else None,
        "cpc_max_usd": max([rows[k]["cpc_usd"] for k in ms if rows[k]["cpc_usd"]] or [None], key=lambda x: x or 0),
    })
    c = cl_out[-1]
    tipo = "clínica local" if c["top10_clinicas"] >= max(c["top10_portales"], 1) else ("portal médico" if c["top10_portales"] else "mixta/otros")
    c["tipo_pagina_gana"] = tipo
    c["viable_volumen"] = vtot >= UMB["viabilidad_pagina"]["volumen_cluster_min"]
    c["viable_serp_local"] = c["top10_clinicas"] >= UMB["viabilidad_pagina"]["clinicas_locales_top10_min"] or lp
    c["decision"] = ("página propia" if (c["viable_volumen"] and c["viable_serp_local"]) else
                     "página propia (enfoque informacional + CTA local)" if c["viable_volumen"] else
                     "sección / artículo de blog")
cl_out.sort(key=lambda c: (-c["volumen_agregado"], c["cluster"]))
(BASE / "data/clusters.json").write_text(json.dumps(cl_out, ensure_ascii=False, indent=1))

cols = ["keyword", "tema", "cluster", "cluster_metodo", "ciudad", "vol_ch_gads", "vol_ch_labs", "vol_be", "vol_fr", "vol_ne",
        "vol_vd", "tendencia_12m_pct", "serie_12m", "intencion", "kd", "cpc_usd", "competencia_ads", "pos_actual", "url_actual",
        "local_pack_physioactiva", "origen", "variantes", "duplicado_de", "fuente"]
with (BASE / "data/keywords.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
    for r in sorted(rows.values(), key=lambda r: (-vol(r), r["keyword"])):
        w.writerow(r)
(BASE / "data/m1_rows.json").write_text(json.dumps(rows, ensure_ascii=False))
print("keywords", len(rows), "clusters", len(cl_out), "páginas propias", sum(c["decision"].startswith("página") for c in cl_out))
for c in cl_out[:45]:
    print(c["volumen_agregado"], c["cluster"], "|", c["tema"], "|", c["n_keywords"], "|", c["tipo_pagina_gana"], c["top10_clinicas"], c["top10_portales"], "| LP", c["local_pack"], c["physioactiva_en_local_pack"], "| AIO", c["ai_overview"], "|", c["decision"])
