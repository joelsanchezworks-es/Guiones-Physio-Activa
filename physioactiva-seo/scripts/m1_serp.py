"""Módulo 1 · SERP orgánica (Google CH, fr) centrada en Ins + repeticiones locales en Murten, Neuchâtel y Avenches.
Salida: data/m1_serp.json {keyword: {...}} y data/m1_serp_local.json
"""
import json, sys, pathlib, re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
COORD = {"Ins": "47.0058,7.1063,10000", "Murten": "46.9283,7.1176,10000",
         "Neuchâtel": "46.9920,6.9310,10000", "Avenches": "46.8803,7.0408,10000"}
T = json.loads((BASE / "data/m1_tabla.json").read_text())
LOC = json.loads((BASE / "data/m1_local.json").read_text())


def vol(r):
    return r["vol_ch_gads"] if r["vol_ch_gads"] is not None else (r["vol_ch_labs"] or 0)


sel = [r["keyword"] for r in T if "competidor" not in r["origen"] and (vol(r) >= 40 or "documento" in r["origen"])]
sel += [k for k, v in LOC.items() if (v.get("fr", {}).get("vol") or 0) > 0 and not k.startswith(("massage", "kiné"))]
sel += ["physio ins", "physio anet", "physio morat", "physio murten", "physio kerzers", "physio sugiez", "physio avenches",
        "physio fribourg", "physio bienne", "physio neuchâtel", "physiothérapie ins", "physio près de moi",
        "physiothérapeute à domicile", "physio à domicile", "massage thérapeutique ins", "massage murten", "massage biel"]
sel = sorted(set(sel))

PORTALES = re.compile(r"(planetesante|rts\.ch|hug\.ch|chuv\.ch|doctissimo|passeportsante|ameli|vidal|wikipedia|santemagazine|"
                      r"hopital|hospital|insel|unisante|msdmanuals|elle\.fr|topsante|journaldesfemmes|sante\.fr|youtube|"
                      r"ligues?|rheumaliga|physioswiss|mayoclinic|medecin|medical-|creapharma|futura|hirslanden|swissmedical|"
                      r"cleveland|healthline|sciencedirect|pubmed|ncbi|cairn|inserm|has-sante|vulgaris|lemonde|20min|"
                      r"letemps|24heures|lematin|tdg\.ch|arcinfo|laliberte|amazon|decathlon|galaxus|digitec)", re.I)
CLINICA = re.compile(r"(physio|kine|reeduc|therap|cabinet|praxis|rehab|fisio|mtt|massage|ergo|sport)", re.I)


def clasifica(dom, title):
    if PORTALES.search(dom):
        return "portal/medio/institución"
    if CLINICA.search(dom) or CLINICA.search(title or ""):
        return "clínica/physio"
    return "otro"


def desde_breadcrumb(it):
    """Google devuelve enlaces google.com/goto: el dominio y la ruta se toman del breadcrumb visible."""
    dom = (it.get("domain") or "").replace("www.", "")
    bc = it.get("breadcrumb") or ""
    if dom in ("", "google.com") and bc:
        partes = [x.strip() for x in bc.split("›")]
        dom = urlparse(partes[0] if "://" in partes[0] else "https://" + partes[0]).netloc.replace("www.", "")
        ruta = "/".join(x for x in partes[1:] if x and "..." not in x and "…" not in x)
        return dom, dom + ("/" + ruta if ruta else "/")
    u = urlparse(it.get("url", ""))
    return dom, dom + (u.path or "/")


def parse(d):
    out = {"organic": [], "local_pack": [], "paa": [], "ai_overview": False, "ai_citas": [], "featured": None,
           "tipos": [], "physioactiva_pos": None}
    for res in dfs.results(d):
        if "__error__" in res:
            out["error"] = res["__error__"]; continue
        out["tipos"] = res.get("item_types") or []
        for it in res.get("items") or []:
            t = it.get("type")
            if t == "organic":
                dom, ukey = desde_breadcrumb(it)
                out["organic"].append({"pos": it.get("rank_group"), "url": ukey, "domain": dom,
                                       "sitio": it.get("website_name"),
                                       "title": it.get("title"), "clase": clasifica(dom, it.get("title"))})
                if "physioactiva.ch" in dom and out["physioactiva_pos"] is None:
                    out["physioactiva_pos"] = it.get("rank_group")
            elif t == "local_pack":
                out["local_pack"].append({"title": it.get("title"), "domain": it.get("domain"),
                                          "rating": (it.get("rating") or {}).get("value"),
                                          "votes": (it.get("rating") or {}).get("votes_count")})
            elif t == "people_also_ask":
                for q in it.get("items") or []:
                    out["paa"].append(q.get("title"))
            elif t == "ai_overview":
                out["ai_overview"] = True
                for ref in it.get("references") or []:
                    out["ai_citas"].append(ref.get("domain") or ref.get("source") or ref.get("title"))
            elif t == "featured_snippet":
                out["featured"] = it.get("domain")
    out["organic"] = out["organic"][:10]
    return out


def serp(args):
    kw, lugar = args
    d = dfs.call("serp/google/organic/live/advanced",
                 [{"keyword": kw, "location_coordinate": COORD[lugar], "language_code": "fr", "device": "desktop",
                   "depth": 10}], estimate=0.004)
    return kw, lugar, parse(d)


if __name__ == "__main__":
    res = {}
    with ThreadPoolExecutor(10) as ex:
        for kw, lugar, p in ex.map(serp, [(k, "Ins") for k in sel]):
            res[kw] = p
    (BASE / "data/m1_serp.json").write_text(json.dumps(res, ensure_ascii=False))
    loc_kws = ["physio", "physiothérapeute", "physiothérapie à domicile", "physio près de moi", "physio sport", "massage thérapeutique"]
    rl = {}
    with ThreadPoolExecutor(10) as ex:
        for kw, lugar, p in ex.map(serp, [(k, l) for k in loc_kws for l in COORD]):
            rl.setdefault(kw, {})[lugar] = p
    (BASE / "data/m1_serp_local.json").write_text(json.dumps(rl, ensure_ascii=False))
    err = [k for k, v in res.items() if v.get("error")]
    print("serp", len(res), "errores", len(err), err[:5], "physioactiva en top10:",
          sorted((v["physioactiva_pos"], k) for k, v in res.items() if v["physioactiva_pos"]))
    print("gasto", round(dfs.gasto_ejecucion(dfs.RUN_ID), 3))
