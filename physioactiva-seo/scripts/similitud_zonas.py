"""Regla antipuerta: similitud entre páginas de zona (shingles de 5 palabras) y nº de datos propios de zonas.yml.
Se excluyen el bloque común «Remboursement», el hero (pills y botones), la CTA y el mapa."""
import json, re, pathlib, itertools, sys, unicodedata, yaml
from bs4 import BeautifulSoup
BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "entregables/6_elementor"
ZON = yaml.safe_load((BASE / "config/zonas.yml").read_text())


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def texto_zona(slug):
    h = json.loads((OUT / slug / "elementor.json").read_text())["content"][0]["elements"][0]["elements"][0]["settings"]["html"]
    soup = BeautifulSoup(h.split("<style>")[0], "html.parser")
    for sec in soup.select("section"):
        cls = sec.get("class") or []
        t = sec.find("h2")
        if any(c in cls for c in ("cta-band", "map", "insurers")) or (t and re.match(r"Remboursement", t.get_text(strip=True))):
            sec.decompose()
    for el in soup.select(".hero-cta, .hero-pills"):
        el.decompose()
    return soup.get_text(" ", strip=True)


def shingles(t, n=5):
    w = re.findall(r"\w+", norm(t))
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def datos_propios(k, t):
    z, n = ZON[k], norm(t)
    hits = []
    if str(z["km_depuis_ins"]).replace(".", ",") in t or str(z["km_depuis_ins"]) in t or f"{round(z['km_depuis_ins'])} km" in t:
        hits.append("distancia")
    if any(w in n for w in ["germanophone", "francophone", "bilingue"]):
        hits.append("idioma")
    if norm(z["district"]) in n or norm(z["canton"]) in n:
        hits.append("distrito/cantón")
    hop = norm(z["hopital_reference"].split("–")[0].split("(")[0].strip())
    if hop[:10] in n:
        hits.append("hospital")
    v = [x for x in z["localites_voisines"] if norm(x.split(" (")[0]) in n]
    if len(v) >= 2:
        hits.append(f"localidades vecinas ({len(v)})")
    if any(norm(q)[:40] in n for q in z.get("faq_locales_serp") or []):
        hits.append("FAQ de la SERP local")
    return hits


def calcular():
    zonas = {f"physio-a-{k}": k for k in ZON if (OUT / f"physio-a-{k}" / "elementor.json").exists()}
    sh = {s: shingles(texto_zona(s)) for s in zonas}
    res = {}
    for a in zonas:
        best, contra = 0.0, None
        for b in zonas:
            if a == b:
                continue
            inter = len(sh[a] & sh[b])
            jac = inter / max(1, len(sh[a] | sh[b]))
            cont = inter / max(1, min(len(sh[a]), len(sh[b])))
            sim = max(jac, cont)
            if sim > best:
                best, contra = sim, b
        d = datos_propios(zonas[a], texto_zona(a))
        res[a] = {"similitud_max": round(100 * best, 1), "con": contra, "datos_propios": d, "n_datos": len(d),
                  "ok": best < 0.40 and len(d) >= 4}
    return res


if __name__ == "__main__":
    for k, v in calcular().items():
        print(k, v)
