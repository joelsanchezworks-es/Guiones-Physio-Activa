"""Módulo 1 · paso 1: candidatos + ampliación con DataForSEO Labs (CH, fr).
Salida: data/m1_candidatos.json  {keyword: {origen: [...], labs: {...}}}
"""
import json, sys, pathlib, yaml, itertools
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs

BASE = dfs.BASE
S = yaml.safe_load((BASE / "config/semillas.yml").read_text())
LOC, LANG = 2756, "fr"

cand = {}


def add(kw, origen, labs=None):
    kw = " ".join(kw.lower().split())
    c = cand.setdefault(kw, {"origen": [], "labs": None})
    if origen not in c["origen"]:
        c["origen"].append(origen)
    if labs and not c["labs"]:
        c["labs"] = labs


for d in S["documento"]:
    add(d["kw"], "documento")
for g, c in itertools.product(S["genericas"], S["ciudades"]):
    if "près de moi" in g:
        continue
    add(f"{g} {c}", "generica_ciudad")
for g in S["genericas"]:
    add(g, "generica")
pats = [p for k, v in S["patologias"].items() for p in v]
for p in pats:
    add(p, "patologia")
    for m in S["modificadores"]:
        add(f"{m} {p}" if m in ("physio", "physiothérapie", "rééducation", "traitement", "exercices") else f"{p} {m}", "patologia_mod")


def labs_item(it):
    ki = it.get("keyword_info") or {}
    kp = it.get("keyword_properties") or {}
    si = it.get("search_intent_info") or {}
    return {"vol": ki.get("search_volume"), "cpc": ki.get("cpc"), "comp": ki.get("competition"),
            "comp_level": ki.get("competition_level"), "kd": kp.get("keyword_difficulty"),
            "intent": si.get("main_intent"), "intent_2": si.get("foreign_intent"),
            "monthly": [(m["year"], m["month"], m["search_volume"]) for m in (ki.get("monthly_searches") or [])],
            "updated": ki.get("last_updated_time")}


# keyword_suggestions: una semilla por tarea (genéricas + patologías + técnicas)
sug_seeds = sorted(set(S["genericas"] + pats + ["physiothérapeute", "physio", "rééducation", "kiné"]))


def sug(seed):
    d = dfs.call("dataforseo_labs/google/keyword_suggestions/live",
                 [{"keyword": seed, "location_code": LOC, "language_code": LANG, "limit": 100,
                   "include_seed_keyword": True, "include_serp_info": False}], estimate=0.03)
    return seed, dfs.results(d)


with ThreadPoolExecutor(8) as ex:
    for seed, res in ex.map(sug, sug_seeds):
        for r in res:
            if "__error__" in r:
                print("ERR sug", seed, r["__error__"]); continue
            if r.get("seed_keyword_data"):
                add(seed, "labs_seed", labs_item(r["seed_keyword_data"]))
            for it in r.get("items") or []:
                add(it["keyword"], "labs_suggestions", labs_item(it))

# keyword_ideas: semillas en lotes de 200
seeds_ideas = sorted(set([d["kw"] for d in S["documento"]] + pats + S["genericas"]))
for i in range(0, len(seeds_ideas), 200):
    d = dfs.call("dataforseo_labs/google/keyword_ideas/live",
                 [{"keywords": seeds_ideas[i:i + 200], "location_code": LOC, "language_code": LANG,
                   "limit": 1000, "include_serp_info": False}], estimate=0.15)
    for r in dfs.results(d):
        if "__error__" in r:
            print("ERR ideas", r["__error__"]); continue
        for it in r.get("items") or []:
            add(it["keyword"], "labs_ideas", labs_item(it))

(BASE / "data/m1_candidatos.json").write_text(json.dumps(cand, ensure_ascii=False, indent=0))
print("candidatos", len(cand), "con labs", sum(1 for c in cand.values() if c["labs"]),
      "gasto", round(dfs.gasto_ejecucion(dfs.RUN_ID), 3))
