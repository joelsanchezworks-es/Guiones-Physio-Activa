"""Módulos 3 y 4: arquitectura (tema → página), zonas (regla antipuerta), prioridad calculada y roadmap.
Salida: data/arquitectura.csv, data/arquitectura.json, data/zonas.json, data/roadmap.json
"""
import json, csv, math, sys, pathlib, statistics, yaml, collections
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
UMB = dfs.UMB
C = json.loads((BASE / "data/clusters.json").read_text())
R = json.loads((BASE / "data/m1_rows.json").read_text())
TEMAS = yaml.safe_load((BASE / "config/temas.yml").read_text())["temas"]
MAPA = yaml.safe_load((BASE / "config/mapa_urls.yml").read_text())
D = json.loads((BASE / "data/m2_dominios.json").read_text())
L = json.loads((BASE / "data/m2_local.json").read_text()) if (BASE / "data/m2_local.json").exists() else {}
P = UMB["prioridad"]

SLUG_NUEVO = {"sciatique": "/sciatique-hernie-discale/", "cheville_pied": "/douleur-pied-cheville-fasciite-plantaire/",
              "hanche": "/douleur-de-hanche-protheses/", "coude_main": "/epicondylite-canal-carpien/",
              "vertiges": "/vertiges-reeducation-vestibulaire/", "fibromyalgie": "/fibromyalgie-physiotherapie/",
              "arthrose": "/arthrose-physiotherapie/"}


def vol(r):
    return r["vol_ch_gads"] if r["vol_ch_gads"] is not None else (r["vol_ch_labs"] or 0)


# --- índice de autoridad ---
def bl_rank(d):
    v = D["bl_summary"].get(d)
    return v[0].get("rank") if isinstance(v, list) and v else None


LOCALES = ["physiodulac-physioduparc.ch", "physioptima.ch", "physiotherapie-kerzers.ch", "physiomurten.ch",
           "physioplus-avenches.com"]
ranks = [bl_rank(d) for d in LOCALES if bl_rank(d) is not None]
IDX_AUT = round(bl_rank("physioactiva.ch") / statistics.median(ranks), 2) if ranks else None

# --- temas ---
por_tema = collections.defaultdict(list)
for c in C:
    if c["tema"] != "marca_competidor":
        por_tema[c["tema"]].append(c)
existentes = {}
for url, v in MAPA["existentes"].items():
    if v.get("tema") and v["rol"] in ("patologia", "servicio", "home"):
        existentes.setdefault(v["tema"], url)
vmax = max(sum(c["volumen_agregado"] for c in cs) for t, cs in por_tema.items() if t != "local_generico")

arq = []
for t, cs in por_tema.items():
    if t in ("local_generico", "massage_bienestar"):
        continue
    cs = sorted(cs, key=lambda c: -c["volumen_agregado"])
    main = cs[0]
    vtot = sum(c["volumen_agregado"] for c in cs)
    ints = collections.Counter()
    for c in cs:
        for k in c["keywords"]:
            if R[k]["intencion"]:
                ints[R[k]["intencion"]] += vol(R[k]) or 0
    intent = ints.most_common(1)[0][0] if ints else "informacional"
    local = any(c["top10_clinicas"] >= 1 or c["local_pack"] for c in cs[:3])
    gan = P["factor_ganabilidad"]["clinicas_locales" if local else "solo_portales"]
    aj = 1.0 if local else (0.5 + 0.5 * min(1, IDX_AUT or 0))
    fi = P["factor_intencion"].get(intent, 0.6)
    impacto = round(5 * math.log10(vtot + 1) / math.log10(vmax + 1) * fi * gan * aj, 2)
    medido = vtot > 0
    serp = any(c["tipo_pagina_gana"] for c in cs)
    confianza = 3 if (medido and serp) else 2 if (medido or serp) else 1
    url = existentes.get(t)
    accion = "optimizar" if url else ("crear" if vtot >= UMB["viabilidad_pagina"]["volumen_cluster_min"] else "sección/blog")
    esfuerzo = P["esfuerzo_horas"]["optimizar" if accion == "optimizar" else "nueva" if accion == "crear" else "seccion"]
    secciones = [c["cluster"] for c in cs[1:8]]
    fase2 = [c["cluster"] for c in cs[1:] if c["volumen_agregado"] >= 300 and c["decision"].startswith("página")]
    tipo = TEMAS[t]["tipo"]
    arq.append({
        "tema": t, "nombre": TEMAS[t]["nombre"], "tipo": tipo, "url": url or SLUG_NUEVO.get(t, "/" + t.replace("_", "-") + "/"),
        "accion": accion, "kw_principal": main["cluster"], "vol_kw_principal": main["kw_principal_vol"],
        "volumen_tema": vtot, "n_clusters": len(cs), "n_keywords": sum(c["n_keywords"] for c in cs),
        "intencion": intent, "serp_tipo": main["tipo_pagina_gana"], "serp_local": local,
        "ai_overview": main["ai_overview"], "top3": main["top3"], "paa": main["paa"][:6],
        "secciones_h2": secciones, "candidatas_fase2": fase2,
        "kd_media": main["kd_media"], "cpc_max_usd": main["cpc_max_usd"],
        "impacto": impacto, "confianza": confianza, "esfuerzo_h": esfuerzo,
        "prioridad": round(impacto * confianza / esfuerzo, 2),
        "fuente": f"DataForSEO google_ads/search_volume + Labs + SERP Ins {dfs.HOY}",
    })

# --- home / genéricas ---
gen = [c for c in por_tema.get("local_generico", []) if not R[c["cluster"]]["ciudad"]]
vgen = sum(c["volumen_agregado"] for c in gen)
arq.append({"tema": "home", "nombre": "Accueil — physio Ins (Anet) + à domicile", "tipo": "home", "url": "/", "accion": "optimizar",
            "kw_principal": "physio", "vol_kw_principal": R["physio"]["vol_ch_gads"], "volumen_tema": vgen,
            "n_clusters": len(gen), "n_keywords": sum(c["n_keywords"] for c in gen), "intencion": "comercial",
            "serp_tipo": "clínica local", "serp_local": True, "ai_overview": False,
            "top3": next((c["top3"] for c in gen if c["cluster"] == "physio"), []), "paa": [],
            "secciones_h2": [c["cluster"] for c in gen[:8]], "candidatas_fase2": [], "kd_media": None, "cpc_max_usd": None,
            "impacto": 5.0, "confianza": 3, "esfuerzo_h": P["esfuerzo_horas"]["optimizar"],
            "prioridad": round(5.0 * 3 / P["esfuerzo_horas"]["optimizar"], 2),
            "fuente": f"DataForSEO google_ads + SERP Ins {dfs.HOY}"})
arq.sort(key=lambda a: (-a["prioridad"], a["tema"]))

# --- zonas ---
CIUDAD_KW = {"Ins": ["ins", "anet"], "Neuchâtel": ["neuchatel", "neuchâtel"], "Biel/Bienne": ["biel", "bienne", "biel bienne"],
             "Murten/Morat": ["murten", "morat"], "Kerzers/Chiètres": ["kerzers", "chiètres"], "Sugiez": ["sugiez", "vully", "mont-vully"],
             "Lyss": ["lyss"], "Fribourg": ["fribourg"], "Payerne": ["payerne"], "Estavayer": ["estavayer", "estavayer-le-lac"],
             "Yverdon-les-Bains": ["yverdon", "yverdon-les-bains"], "Yvonand": ["yvonand"], "Lausanne": ["lausanne"],
             "La Neuveville": ["la neuveville"], "Avenches": ["avenches"]}
LOCV = json.loads((BASE / "data/m1_local.json").read_text())
CO = {"Ins": (47.0058, 7.1063), "Neuchâtel": (46.9920, 6.9310), "Biel/Bienne": (47.1368, 7.2468), "Murten/Morat": (46.9283, 7.1176),
      "Kerzers/Chiètres": (46.9750, 7.1960), "Sugiez": (46.9622, 7.1136), "Lyss": (47.0742, 7.3069), "Fribourg": (46.8065, 7.1620),
      "Payerne": (46.8220, 6.9380), "Estavayer": (46.8490, 6.8460), "Yverdon-les-Bains": (46.7785, 6.6410), "Yvonand": (46.8000, 6.7420),
      "Lausanne": (46.5197, 6.6323), "La Neuveville": (47.0650, 7.0970), "Avenches": (46.8803, 7.0408)}


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return round(6371 * 2 * math.asin(math.sqrt(h)), 1)


zonas = []
for ciudad, alias in CIUDAD_KW.items():
    kws = {}
    for k, v in LOCV.items():
        if any(k.endswith(" " + a) or k.endswith(" à " + a) for a in alias) and not k.startswith(("massage", "kiné")):
            if (v.get("fr", {}).get("vol") or 0) > 0:
                kws[k] = v["fr"]["vol"]
    m = (L.get("maps") or {}).get(ciudad, {})
    mp = m.get("physio") or []
    pos_pa = next((i["pos"] for i in mp if "physio activa" in (i["title"] or "").lower()), None)
    mpd = m.get("physiothérapie à domicile") or []
    pos_pa_dom = next((i["pos"] for i in mpd if "physio activa" in (i["title"] or "").lower()), None)
    dist = km(CO["Ins"], CO[ciudad])
    existe = {"Neuchâtel": "/physio-a-neuchatel/", "Sugiez": "/physio-a-sugiez/", "Ins": "/"}.get(ciudad)
    lejana = ciudad in ("Lausanne", "Yverdon-les-Bains", "Yvonand")
    vtot = sum(kws.values())
    if ciudad == "Ins":
        dec = "home (no hace falta página de zona: Ins es la sede)"
    elif lejana:
        dec = "solo con confirmación del cliente (zona lejana)"
    elif dist <= 25 and (vtot > 0 or pos_pa):
        dec = "publicar con contenido propio (regla 8.2)"
    elif dist <= 25:
        dec = "publicar solo si el cliente aporta datos propios (sin volumen medido)"
    elif vtot > 0:
        dec = "solo con confirmación del cliente (> 25 km)"
    else:
        dec = "no publicar por ahora (lejos y sin señal)"
    zonas.append({"ciudad": ciudad, "km_linea_recta_desde_ins": dist, "keywords_con_volumen": kws, "volumen_total": vtot,
                  "maps_physio_pos_physioactiva": pos_pa, "maps_domicile_pos_physioactiva": pos_pa_dom,
                  "maps_top3": [i["title"] for i in mp[:3]], "url_existente": existe, "decision": dec})
zonas.sort(key=lambda z: (z["km_linea_recta_desde_ins"]))

(BASE / "data/arquitectura.json").write_text(json.dumps({"indice_autoridad": IDX_AUT, "temas": arq}, ensure_ascii=False, indent=1))
(BASE / "data/zonas.json").write_text(json.dumps(zonas, ensure_ascii=False, indent=1))
with (BASE / "data/arquitectura.csv").open("w", newline="") as f:
    cols = ["prioridad", "tema", "nombre", "url", "accion", "kw_principal", "vol_kw_principal", "volumen_tema", "intencion",
            "serp_tipo", "serp_local", "ai_overview", "impacto", "confianza", "esfuerzo_h", "secciones_h2", "candidatas_fase2", "fuente"]
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
    for a in arq:
        w.writerow({**a, "secciones_h2": " | ".join(a["secciones_h2"]), "candidatas_fase2": " | ".join(a["candidatas_fase2"])})
print("índice autoridad", IDX_AUT)
for a in arq:
    print(a["prioridad"], a["tema"], a["url"], a["accion"], a["volumen_tema"], a["intencion"], a["serp_tipo"], a["impacto"], a["confianza"])
for z in zonas:
    print(z["ciudad"], z["km_linea_recta_desde_ins"], z["volumen_total"], z["maps_physio_pos_physioactiva"], z["maps_domicile_pos_physioactiva"], z["decision"])
