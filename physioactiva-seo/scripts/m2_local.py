"""Módulo 2 · local: fichas de Google (propia + competidores), reseñas, Google Maps por ciudad y rastreo on_page.
Coordenadas: centro aproximado de cada localidad (decisiones.md).
"""
import json, sys, pathlib, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
CIUDADES = {
    "Ins": (47.0058, 7.1063), "Neuchâtel": (46.9920, 6.9310), "Biel/Bienne": (47.1368, 7.2468),
    "Murten/Morat": (46.9283, 7.1176), "Kerzers/Chiètres": (46.9750, 7.1960), "Sugiez": (46.9622, 7.1136),
    "Lyss": (47.0742, 7.3069), "Fribourg": (46.8065, 7.1620), "Payerne": (46.8220, 6.9380),
    "Estavayer": (46.8490, 6.8460), "Yverdon-les-Bains": (46.7785, 6.6410), "Yvonand": (46.8000, 6.7420),
    "Lausanne": (46.5197, 6.6323), "La Neuveville": (47.0650, 7.0970), "Avenches": (46.8803, 7.0408),
}
FICHAS = ["Physio Activa Ins", "Physiotherapie André van den Heuvel Ins", "Physio du Lac Sugiez", "PhysiOptima Murten",
          "Physiotherapie Kerzers", "Physio Plus Avenches", "Physio Vully"]


def maps(args):
    ciudad, kw = args
    lat, lng = CIUDADES[ciudad]
    d = dfs.call("serp/google/maps/live/advanced", [{"keyword": kw, "location_coordinate": f"{lat},{lng},13z",
                                                     "language_code": "fr", "depth": 20}], estimate=0.004)
    items = []
    for r in dfs.results(d):
        for it in r.get("items") or []:
            items.append({"pos": it.get("rank_group"), "title": it.get("title"), "domain": it.get("domain"),
                          "rating": (it.get("rating") or {}).get("value"), "votes": (it.get("rating") or {}).get("votes_count"),
                          "category": it.get("category"), "address": it.get("address")})
    return ciudad, kw, items


def ficha(kw):
    d = dfs.call("business_data/google/my_business_info/live", [{"keyword": kw, "location_coordinate": "47.0058,7.1063,10",
                                                                  "language_code": "fr"}], estimate=0.006)
    r = dfs.results(d)
    it = ((r[0].get("items") or [None])[0]) if r and "items" in r[0] else None
    return kw, it


out = {"maps": {}, "fichas": {}, "reviews": {}, "on_page": {}}
with ThreadPoolExecutor(10) as ex:
    for ciudad, kw, items in ex.map(maps, [(c, k) for c in CIUDADES for k in ("physio", "physiothérapie à domicile")]):
        out["maps"].setdefault(ciudad, {})[kw] = items
    for kw, it in ex.map(ficha, FICHAS):
        out["fichas"][kw] = it

# Reseñas (asíncrono): task_post → tasks_ready → task_get
ids = {}
for kw, it in out["fichas"].items():
    if not it or not it.get("cid"):
        continue
    d = dfs.call("business_data/google/reviews/task_post", [{"cid": it["cid"], "location_coordinate": "47.0058,7.1063,10",
                                                              "language_code": "fr", "depth": 50, "sort_by": "newest"}], estimate=0.01)
    t = d["tasks"][0]
    if t.get("id"):
        ids[kw] = t["id"]

# on_page: rastreo de physioactiva.ch (asíncrono)
d = dfs.call("on_page/task_post", [{"target": "physioactiva.ch", "max_crawl_pages": 120, "load_resources": True,
                                     "enable_javascript": False, "check_spell": False, "validate_micromarkup": True,
                                     "calculate_keyword_density": False}], estimate=0.03)
op_id = d["tasks"][0].get("id")


def get(ep):
    req = __import__("urllib.request").request.Request("https://api.dataforseo.com/v3/" + ep)
    with __import__("urllib.request").request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


for _ in range(60):
    pend = [k for k in ids if k not in out["reviews"]]
    for kw in pend:
        r = get(f"business_data/google/reviews/task_get/{ids[kw]}")
        t = r["tasks"][0]
        if t["status_code"] == 20000 and t.get("result"):
            res = t["result"][0]
            out["reviews"][kw] = {"rating": res.get("rating"), "reviews_count": res.get("reviews_count"),
                                  "items": [{"date": i.get("timestamp"), "rating": (i.get("rating") or {}).get("value"),
                                             "respondida": bool(i.get("owner_answer"))} for i in (res.get("items") or [])]}
    s = ((get(f"on_page/summary/{op_id}")["tasks"][0].get("result")) or [{}])[0]
    if not [k for k in ids if k not in out["reviews"]] and s.get("crawl_progress") == "finished":
        break
    time.sleep(20)
out["on_page"]["task_id"] = op_id
out["on_page"]["summary"] = ((get(f"on_page/summary/{op_id}")["tasks"][0].get("result")) or [{}])[0]


def post(ep, t):
    req = __import__("urllib.request").request.Request("https://api.dataforseo.com/v3/" + ep, method="POST",
                                                        data=json.dumps([t]).encode(), headers={"Content-Type": "application/json"})
    with __import__("urllib.request").request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


for ep in ("pages", "duplicate_tags", "non_indexable", "redirect_chains", "links", "microdata"):
    try:
        if ep == "duplicate_tags":
            res = {tt: post(f"on_page/{ep}", {"id": op_id, "type": tt, "limit": 100})["tasks"][0].get("result")
                   for tt in ("duplicate_title", "duplicate_description")}
        elif ep == "microdata":
            res = None
        else:
            res = post(f"on_page/{ep}", {"id": op_id, "limit": 1000})["tasks"][0].get("result")
        out["on_page"][ep] = res
    except Exception as e:
        out["on_page"][ep] = {"no_disponible": str(e)[:200]}
(BASE / "data/m2_local.json").write_text(json.dumps(out, ensure_ascii=False))
print("maps", {c: [i["title"] for i in v["physio"][:5]] for c, v in out["maps"].items()})
print("fichas", {k: (v or {}).get("title") for k, v in out["fichas"].items()}, "reviews", list(out["reviews"]))
print("on_page", out["on_page"]["summary"].get("crawl_progress"), (out["on_page"]["summary"].get("crawl_status") or {}))
print("gasto registrado", round(dfs.gasto_ejecucion(dfs.RUN_ID), 3))
