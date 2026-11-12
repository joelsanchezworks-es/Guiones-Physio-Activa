"""Módulo 1 · paso 3: volumen Google Ads (CH-FR y cantones), intención y KD para las keywords filtradas.
Solo se piden intención/KD a los endpoints dedicados cuando Labs no los trajo.
Salida: data/m1_metricas.json
"""
import json, re, sys, pathlib
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
K = json.loads((BASE / "data/m1_filtradas.json").read_text())
LOCS = {"CH": 2756, "BE": 20129, "FR": 20132, "NE": 20138, "VD": 20148}
ok_chars = re.compile(r"^[\w\sàâäéèêëîïôöùûüçœæ'’\-]+$", re.I)
kws = sorted(K)
gads_kws = [k for k in kws if ok_chars.match(k) and len(k) <= 80 and len(k.split()) <= 10]
canton_kws = [k for k in gads_kws if ((K[k]["labs"] or {}).get("vol") or 0) >= 20 or "documento" in K[k]["origen"]
              or "generica_ciudad" in K[k]["origen"]]


def sv(args):
    loc, lote = args
    d = dfs.call("keywords_data/google_ads/search_volume/live",
                 [{"keywords": lote, "location_code": LOCS[loc], "language_code": "fr"}], estimate=0.09)
    return loc, dfs.results(d)


jobs = [("CH", gads_kws[i:i + 1000]) for i in range(0, len(gads_kws), 1000)]
for loc in ("BE", "FR", "NE", "VD"):
    jobs += [(loc, canton_kws[i:i + 1000]) for i in range(0, len(canton_kws), 1000)]
gads = {}
with ThreadPoolExecutor(6) as ex:
    for loc, res in ex.map(sv, jobs):
        for r in res:
            if "__error__" in r:
                print("ERR", loc, r["__error__"]); continue
            g = gads.setdefault(r["keyword"].lower(), {})
            g[loc] = {"vol": r.get("search_volume"), "cpc": r.get("cpc"), "comp": r.get("competition"),
                      "comp_index": r.get("competition_index"),
                      "monthly": [(m["year"], m["month"], m["search_volume"]) for m in (r.get("monthly_searches") or [])]}

falta_int = [k for k in kws if not (K[k]["labs"] or {}).get("intent")]
falta_kd = [k for k in kws if (K[k]["labs"] or {}).get("kd") is None]
intent, kd = {}, {}
for i in range(0, len(falta_int), 1000):
    d = dfs.call("dataforseo_labs/google/search_intent/live",
                 [{"keywords": falta_int[i:i + 1000], "language_code": "fr"}], estimate=0.15)
    for r in dfs.results(d):
        for it in r.get("items") or []:
            intent[it["keyword"]] = (it.get("keyword_intent") or {}).get("label")
for i in range(0, len(falta_kd), 1000):
    d = dfs.call("dataforseo_labs/google/bulk_keyword_difficulty/live",
                 [{"keywords": falta_kd[i:i + 1000], "location_code": 2756, "language_code": "fr"}], estimate=0.15)
    for r in dfs.results(d):
        for it in r.get("items") or []:
            kd[it["keyword"]] = it.get("keyword_difficulty")
(BASE / "data/m1_metricas.json").write_text(json.dumps({"gads": gads, "intent": intent, "kd": kd,
                                                          "fecha": dfs.HOY}, ensure_ascii=False))
print("gads", len(gads), "intent pedidas", len(falta_int), "kd pedidas", len(falta_kd),
      "gasto", round(dfs.gasto_ejecucion(dfs.RUN_ID), 3))
