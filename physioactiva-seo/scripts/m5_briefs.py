"""Módulo 5 · briefs del primer lote (datos calculados; el texto lo redacta después el modelo).
Salida: entregables/5_paginas/<slug>/brief.md y brief.json
"""
import json, re, sys, pathlib, html as H, collections
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
A = json.loads((BASE / "data/arquitectura.json").read_text())["temas"]
C = json.loads((BASE / "data/clusters.json").read_text())
R = json.loads((BASE / "data/m1_rows.json").read_text())
PAG = {p["url"].replace("https://physioactiva.ch", ""): p for p in json.loads((BASE / "data/site/paginas.json").read_text())}

ENLACES_TEMA = {  # 8.1: patología → técnicas que se usan (solo páginas existentes)
    "lombalgie": ["/therapie-manuelle/", "/medical-training-therapy-mtt/", "/physioactiva-puncture-seche/", "/tecar-therapie/"],
    "sciatique": ["/therapie-manuelle/", "/medical-training-therapy-mtt/", "/tecar-therapie/", "/mal-de-dos-lombaire/"],
    "cervicalgie": ["/therapie-manuelle/", "/physioactiva-puncture-seche/", "/massage-therapeutique/", "/physiotemporo-mandibulaire-atm/"],
    "epaule": ["/physioactiva-ondes-de-choc/", "/therapie-manuelle/", "/physiotherapie-post-operatoire/", "/medical-training-therapy-mtt/"],
    "genou_lca": ["/physiotherapie-post-operatoire/", "/medical-training-therapy-mtt/", "/physio-du-sport/", "/physioactiva-bandage-neuromusculaire/"],
    "cheville_pied": ["/physioactiva-ondes-de-choc/", "/physioactiva-bandage-neuromusculaire/", "/physio-du-sport/", "/physioactiva-puncture-seche/"],
    "hanche": ["/physiotherapie-post-operatoire/", "/medical-training-therapy-mtt/", "/physiotherapie-geriatrique/", "/therapie-manuelle/"],
}
LOTE = [
    ("accueil", "home", "/"),
    ("pour-les-patients", "hub", "/pour-les-patients/"),
    ("mal-de-dos-lombaire", "lombalgie", "/mal-de-dos-lombaire/"),
    ("douleur-cervicale-au-cou", "cervicalgie", "/douleur-cervicale-au-cou/"),
    ("lesions-de-lepaule", "epaule", "/lesions-de-lepaule/"),
    ("douleur-du-genou-lesions-de-la-cheville", "genou_lca", "/douleur-du-genou-lesions-de-la-cheville/"),
    ("sciatique-hernie-discale", "sciatique", "/sciatique-hernie-discale/"),
    ("douleur-pied-cheville-fasciite-plantaire", "cheville_pied", "/douleur-pied-cheville-fasciite-plantaire/"),
    ("douleur-de-hanche-protheses", "hanche", "/douleur-de-hanche-protheses/"),
    ("reservation-en-ligne", "reserva", "/reservation-en-ligne/"),
]


def vol(r):
    return r["vol_ch_gads"] if r["vol_ch_gads"] is not None else (r["vol_ch_labs"] or 0)


def texto_actual(url):
    p = PAG.get(url)
    if not p:
        return None
    f = BASE / "data/site/html" / f"{p['slug']}.html"
    s = f.read_text()
    s = re.sub(r"<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>|<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<(h[1-3])[^>]*>", lambda m: "\n## " if m.group(1) != "h1" else "\n# ", s)
    s = re.sub(r"<(p|li|br)[^>]*>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = H.unescape(s)
    s = "\n".join(" ".join(l.split()) for l in s.splitlines())
    s = re.sub(r"\n{2,}", "\n", s).strip()
    return {"title": p["title"], "meta": p["meta_description"], "h1": p["h1"], "h2": p["h2"], "palabras": p["palabras"], "texto": s[:6000]}


for slug, tema, url in LOTE:
    d = BASE / "entregables/5_paginas" / slug
    d.mkdir(parents=True, exist_ok=True)
    a = next((x for x in A if x["tema"] == tema), None)
    if tema == "hub":
        a = {"nombre": "Hub « Pathologies traitées »", "kw_principal": "pathologies physiothérapie", "intencion": "informacional",
             "serp_tipo": None, "paa": [], "top3": []}
    if tema == "reserva":
        a = {"nombre": "Prendre rendez-vous (URL canónica de reserva)", "kw_principal": "rendez-vous physio ins",
             "intencion": "transaccional", "serp_tipo": None, "paa": [], "top3": []}
    kws, paa = [], []
    if tema not in ("hub", "reserva"):
        cl = [c for c in C if (c["tema"] == tema or (tema == "home" and c["tema"] == "local_generico"))]
        for c in cl:
            for k in c["keywords"]:
                r = R[k]
                if tema == "home" and r["ciudad"] not in ("", "ins", "anet", "seeland", "vully"):
                    continue
                kws.append((k, vol(r), r["intencion"], r["kd"], r["cpc_usd"], r["tendencia_12m_pct"], c["cluster"]))
            for q in c["paa"]:
                if q not in paa:
                    paa.append(q)
        kws = sorted(set(kws), key=lambda x: (-(x[1] or 0), x[0]))[:30]
    brief = {"slug": slug, "url": url, "tema": tema, "nombre": a["nombre"], "kw_principal": a["kw_principal"],
             "intencion": a["intencion"], "serp_tipo": a.get("serp_tipo"), "ai_overview": a.get("ai_overview"),
             "top3": a.get("top3"), "paa": paa[:10], "secciones_sugeridas": a.get("secciones_h2", []),
             "keywords": [{"kw": k, "vol": v, "intencion": i, "kd": kd, "cpc_usd": cpc, "tendencia_12m_pct": t, "cluster": cl}
                          for k, v, i, kd, cpc, t, cl in kws],
             "enlaces_internos": ENLACES_TEMA.get(tema, []) + (["/physiotherapeute-a-domicile/", "/reservation-en-ligne/"] if tema not in ("reserva",) else []),
             "actual": texto_actual(url), "fuente": f"DataForSEO (google_ads/search_volume, Labs, SERP Ins) {dfs.HOY}"}
    (d / "brief.json").write_text(json.dumps(brief, ensure_ascii=False, indent=1))
    md = [f"# Brief — {brief['nombre']}", "", f"- **URL:** `{url}` ({'existe: optimizar' if brief['actual'] else 'nueva: crear'})",
          f"- **Intención dominante:** {brief['intencion']} · **SERP:** {brief['serp_tipo'] or '—'} · **AI Overview:** {'sí' if brief['ai_overview'] else 'no'}",
          f"- **Keyword principal:** {brief['kw_principal']}", f"- **Top 3 actual (SERP desde Ins):** {', '.join(brief['top3'] or []) or '—'}",
          f"- Fuente: {brief['fuente']}", "", "## Keywords (volumen mensual CH-FR)", "", "| Keyword | Vol. | Intención | KD | CPC USD | Tend. 12 m |", "|---|---|---|---|---|---|"]
    md += [f"| {k['kw']} | {k['vol'] if k['vol'] is not None else 'sin dato'} | {k['intencion'] or ''} | {k['kd'] if k['kd'] is not None else ''} | {k['cpc_usd'] or ''} | {'' if k['tendencia_12m_pct'] is None else str(k['tendencia_12m_pct']) + ' %'} |" for k in brief["keywords"]]
    md += ["", "## Preguntas reales («Autres questions posées»)", ""] + [f"- {q}" for q in brief["paa"]] + ["", "## Enlaces internos", ""] + [f"- {u}" for u in brief["enlaces_internos"]]
    (d / "brief.md").write_text("\n".join(md) + "\n")
    print(slug, len(brief["keywords"]), "kws", len(brief["paa"]), "paa", "actual" if brief["actual"] else "nueva")
