"""Módulo 2 · datos de autoridad, competencia, backlinks, ficha de Google y rastreo on_page.
Salida: data/m2_*.json. Si un bloque falla, se guarda {"no_disponible": motivo}.
"""
import json, sys, pathlib, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
YO = "physioactiva.ch"
COMP = ["therapie-ins-seeland.ch", "physiodulac-physioduparc.ch", "physioptima.ch", "physiotherapie-kerzers.ch",
        "physiomurten.ch", "physio-7.ch", "physio-clinics.ch", "physioplus-avenches.com"]
COMP4 = COMP[:4]
LANGS = ["fr", "de"]


def safe(fn):
    try:
        return fn()
    except SystemExit:
        raise
    except Exception as e:  # el informe sale igual con el bloque marcado
        return {"no_disponible": str(e)[:300]}


def labs(ep, t, est=0.05):
    return dfs.results(dfs.call(f"dataforseo_labs/google/{ep}/live", [t], estimate=est))


def ranked(dom, lang, limit):
    return labs("ranked_keywords", {"target": dom, "location_code": 2756, "language_code": lang, "limit": limit,
                                    "order_by": ["ranked_serp_element.serp_item.rank_group,asc"]}, 0.012 + limit * 0.00012)


out = {}
jobs = {}
with ThreadPoolExecutor(10) as ex:
    for d in [YO] + COMP:
        for lang in LANGS:
            jobs[("ranked", d, lang)] = ex.submit(safe, lambda d=d, lang=lang: ranked(d, lang, 1000 if d == YO else 300))
            jobs[("rank_overview", d, lang)] = ex.submit(safe, lambda d=d, lang=lang: labs("domain_rank_overview", {
                "target": d, "location_code": 2756, "language_code": lang}, 0.013))
    for d in [YO] + COMP4:
        jobs[("historical", d)] = ex.submit(safe, lambda d=d: labs("historical_rank_overview", {
            "target": d, "location_code": 2756, "language_code": "fr"}, 0.14))
    jobs[("competitors_domain", YO)] = ex.submit(safe, lambda: labs("competitors_domain", {
        "target": YO, "location_code": 2756, "language_code": "fr", "limit": 50}, 0.02))
    for c in COMP4 + ["physiomurten.ch"]:
        jobs[("gap", c)] = ex.submit(safe, lambda c=c: labs("domain_intersection", {
            "target1": c, "target2": YO, "location_code": 2756, "language_code": "fr", "intersections": False,
            "limit": 300}, 0.05))

    def bl(ep, t, est=0.03):
        return dfs.results(dfs.call(f"backlinks/{ep}/live", [t], estimate=est))
    for d in [YO] + COMP:
        jobs[("bl_summary", d)] = ex.submit(safe, lambda d=d: bl("summary", {"target": d, "include_subdomains": True}))
    for d in [YO] + COMP4:
        jobs[("bl_history", d)] = ex.submit(safe, lambda d=d: bl("history", {"target": d, "date_from": "2025-11-01"}))
    jobs[("bl_refdomains", YO)] = ex.submit(safe, lambda: bl("referring_domains", {"target": YO, "limit": 200}))
    jobs[("bl_anchors", YO)] = ex.submit(safe, lambda: bl("anchors", {"target": YO, "limit": 50}))
    jobs[("bl_competitors", YO)] = ex.submit(safe, lambda: bl("competitors", {"target": YO, "limit": 50}))
    jobs[("bl_gap", "comp4")] = ex.submit(safe, lambda: bl("domain_intersection", {
        "targets": {str(i + 1): c for i, c in enumerate(COMP4)}, "exclude_targets": [YO], "limit": 300,
        "intersection_mode": "partial"} if False else {
        "targets": {str(i + 1): c for i, c in enumerate(COMP4)}, "exclude_targets": [YO], "limit": 300}, 0.05))
    jobs[("bl_bulk_ranks", "all")] = ex.submit(safe, lambda: bl("bulk_ranks", {"targets": [YO] + COMP}))
    for k, f in jobs.items():
        out.setdefault(k[0], {})["|".join(k[1:])] = f.result()

(BASE / "data/m2_dominios.json").write_text(json.dumps(out, ensure_ascii=False))
print({k: {kk: ("ERR " + vv["no_disponible"][:80]) if isinstance(vv, dict) and "no_disponible" in vv else len(vv)
           for kk, vv in v.items()} for k, v in out.items()})
print("gasto", round(dfs.gasto_ejecucion(dfs.RUN_ID), 3))
