"""Módulo 1 · volumen de las combinaciones genérica × ciudad (CH, fr y sin filtro de idioma)."""
import json, sys, pathlib, itertools, yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
S = yaml.safe_load((BASE / "config/semillas.yml").read_text())
gen = ["physio", "physiothérapeute", "physiothérapie", "physio à domicile", "physiothérapie à domicile", "kiné", "massage"]
ciu = S["ciudades"] + ["mont-vully", "estavayer-le-lac", "yverdon-les-bains", "biel/bienne", "erlach", "cerlier", "aarberg", "täuffelen", "seeland", "gampelen", "cudrefin", "salavaux"]
kws = sorted({f"{g} {c}" for g, c in itertools.product(gen, ciu)} | {f"{g} à {c}" for g, c in itertools.product(gen[:3], ciu)})
kws = [k.replace("/", " ") for k in kws]
out = {}
for lang in ("fr", None):
    for i in range(0, len(kws), 1000):
        t = {"keywords": kws[i:i + 1000], "location_code": 2756}
        if lang: t["language_code"] = lang
        d = dfs.call("keywords_data/google_ads/search_volume/live", [t], estimate=0.09)
        for r in dfs.results(d):
            if "keyword" in r:
                out.setdefault(r["keyword"], {})[lang or "todas"] = {"vol": r.get("search_volume"), "cpc": r.get("cpc"),
                    "comp": r.get("competition"), "monthly": [(m["year"], m["month"], m["search_volume"]) for m in (r.get("monthly_searches") or [])]}
(BASE / "data/m1_local.json").write_text(json.dumps(out, ensure_ascii=False))
con = sorted([(k, v.get("fr", {}).get("vol"), v.get("todas", {}).get("vol")) for k, v in out.items()
              if (v.get("fr", {}).get("vol") or 0) + (v.get("todas", {}).get("vol") or 0) > 0], key=lambda x: -(x[2] or 0))
print(len(kws), "con volumen", len(con)); print(con)
print("gasto", round(dfs.gasto_ejecucion(dfs.RUN_ID), 3))
