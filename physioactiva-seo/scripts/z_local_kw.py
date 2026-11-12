"""Fase SEO local: demanda por ciudad objetivo.
a) Google Ads search_volume (CH, sin filtro de idioma) para la matriz servicio × ciudad (nombres FR y DE).
b) Labs keyword_ideas con las semillas «physio/physiothérapie + ciudad» (1 llamada) y keyword_suggestions de «physio <ciudad>».
Salida: data/z_local_kw.json"""
import json, sys, pathlib, itertools, os
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault("SEO_RUN_ID", "local-2026-11-06")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
CIU = {"sugiez": ["sugiez", "vully", "mont-vully"], "neuchatel": ["neuchâtel", "neuchatel"], "la-neuveville": ["la neuveville"],
       "avenches": ["avenches"], "lyss": ["lyss"], "bienne": ["bienne", "biel"], "fribourg": ["fribourg", "freiburg"],
       "payerne": ["payerne"], "morat": ["morat", "murten"], "chietres": ["chiètres", "kerzers"], "estavayer": ["estavayer", "estavayer-le-lac"],
       "yvonand": ["yvonand"], "yverdon": ["yverdon", "yverdon-les-bains"], "lausanne": ["lausanne"], "ins": ["ins", "anet"]}
PRE_FR = ["physio", "physiothérapie", "physiothérapeute", "physio à domicile", "physiothérapie à domicile", "physiothérapeute à domicile",
          "drainage lymphatique", "massage thérapeutique", "dry needling", "physio sport", "rééducation", "cabinet de physiothérapie",
          "centre de physiothérapie", "fitness médical", "mtt", "ostéopathe", "kiné", "mal de dos", "physio dos", "physio genou", "physio épaule"]
PRE_DE = ["physiotherapie", "physiotherapeut", "physio hausbesuch", "lymphdrainage", "medizinische massage", "dry needling"]
kws = set()
for k, alias in CIU.items():
    for a in alias:
        for p in PRE_FR:
            kws.add(f"{p} {a}")
        for p in PRE_DE:
            kws.add(f"{p} {a}")
kws = sorted(k.replace("/", " ") for k in kws)
out = {"gads": {}, "labs": {}}
for i in range(0, len(kws), 1000):
    d = dfs.call("keywords_data/google_ads/search_volume/live", [{"keywords": kws[i:i + 1000], "location_code": 2756}], estimate=0.09)
    for r in dfs.results(d):
        if "keyword" in r:
            out["gads"][r["keyword"]] = {"vol": r.get("search_volume"), "cpc": r.get("cpc"), "comp": r.get("competition")}
seeds = sorted({f"{p} {a}" for alias in CIU.values() for a in alias for p in ("physio", "physiothérapie", "physiothérapeute")})
d = dfs.call("dataforseo_labs/google/keyword_ideas/live", [{"keywords": seeds[:200], "location_code": 2756, "language_code": "fr", "limit": 700}], estimate=0.1)
for r in dfs.results(d):
    for it in r.get("items") or []:
        ki = it.get("keyword_info") or {}
        out["labs"][it["keyword"]] = {"vol": ki.get("search_volume"), "src": "keyword_ideas"}


def sug(a):
    d = dfs.call("dataforseo_labs/google/keyword_suggestions/live", [{"keyword": f"physio {a}", "location_code": 2756, "language_code": "fr",
                                                                     "limit": 50, "include_seed_keyword": True}], estimate=0.02)
    res = []
    for r in dfs.results(d):
        for it in (r.get("items") or []):
            res.append((it["keyword"], (it.get("keyword_info") or {}).get("search_volume")))
    return res


with ThreadPoolExecutor(8) as ex:
    for res in ex.map(sug, [al[0] if k != "bienne" else "biel" for k, al in CIU.items()]):
        for k, v in res:
            out["labs"].setdefault(k, {"vol": v, "src": "keyword_suggestions"})
(BASE / "data/z_local_kw.json").write_text(json.dumps(out, ensure_ascii=False, indent=0))
con = sorted([(v["vol"], k) for k, v in out["gads"].items() if v["vol"]], reverse=True)
print("gads con volumen:", len(con)); print(con[:120])
print("gasto fase", round(dfs.gasto_ejecucion(dfs.RUN_ID), 3))
