"""Fase Elementor · una SERP por zona y keyword («physio [ville]», «physiothérapeute [ville]») centrada en la localidad.
Solo para extraer «Autres questions posées» y la competencia local. Techo de la fase: 1 USD."""
import json, sys, pathlib
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import os; os.environ.setdefault("SEO_RUN_ID", "elementor-2026-11-06")
import dfs
from m1_serp import parse
BASE = dfs.BASE
Z = {"sugiez": ("Sugiez", 46.9622, 7.1136), "neuchatel": ("Neuchâtel", 46.9920, 6.9310), "la-neuveville": ("La Neuveville", 47.0650, 7.0970),
     "avenches": ("Avenches", 46.8803, 7.0408), "lyss": ("Lyss", 47.0742, 7.3069), "bienne": ("Bienne", 47.1368, 7.2468),
     "fribourg": ("Fribourg", 46.8065, 7.1620), "payerne": ("Payerne", 46.8220, 6.9380), "morat": ("Morat", 46.9283, 7.1176),
     "chietres": ("Chiètres", 46.9750, 7.1960), "estavayer": ("Estavayer", 46.8490, 6.8460), "yvonand": ("Yvonand", 46.8000, 6.7420),
     "yverdon": ("Yverdon", 46.7785, 6.6410), "lausanne": ("Lausanne", 46.5197, 6.6323)}


def one(a):
    z, kw = a
    nom, lat, lng = Z[z]
    d = dfs.call("serp/google/organic/live/advanced", [{"keyword": kw, "location_coordinate": f"{lat},{lng},10000",
                  "language_code": "fr", "device": "desktop", "depth": 10}], estimate=0.004)
    return z, kw, parse(d)


jobs = [(z, f"{p} {v[0].lower()}") for z, v in Z.items() for p in ("physio", "physiothérapeute")]
out = {}
with ThreadPoolExecutor(10) as ex:
    for z, kw, p in ex.map(one, jobs):
        out.setdefault(z, {})[kw] = {"paa": p["paa"], "top5": [f'{o["pos"]}. {o["domain"]}' for o in p["organic"][:5]],
                                     "local_pack": [l["title"] for l in p["local_pack"]], "ai_overview": p["ai_overview"]}
(BASE / "data/z_serp_zonas.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
for z, v in out.items():
    print(z, {k: (len(x["paa"]), x["local_pack"][:3]) for k, x in v.items()})
    for k, x in v.items():
        for q in x["paa"]: print("   ?", q)
print("gasto fase", round(dfs.gasto_ejecucion(dfs.RUN_ID), 3))
