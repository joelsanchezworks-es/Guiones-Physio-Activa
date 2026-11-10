"""Valida los 14 elementor.json de ciudad (diseño pa-lp) y mide el uso de keywords locales."""
import json, re, sys, pathlib, unicodedata, yaml, itertools
from html.parser import HTMLParser
from bs4 import BeautifulSoup
BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "entregables/9_ciudades"
ZON = yaml.safe_load((BASE / "config/zonas.yml").read_text())
CSS = (BASE / "plantillas/pa-lp.css").read_text()
CLASES = set(re.findall(r"\.([a-zA-Z][\w-]*)", CSS)) | {"faq-q"}
URLS = {u.strip().replace("https://physioactiva.ch", "") or "/" for u in (BASE / "data/site/urls.txt").read_text().split()}
URLS |= {z["url"] for z in ZON.values()} | {"/", "/sciatique-hernie-discale/", "/douleur-pied-cheville-fasciite-plantaire/", "/douleur-de-hanche-protheses/", "/reservation-en-ligne/"}
PROHIB = re.compile(r"ordonnance|prescri\w*|LAMal|\bLAA\b|franchise|quote-part|rembours\w*|CONFIRM|tarif", re.I)
VOID = {"img", "br", "source", "meta", "link", "input", "hr"}


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))


class Bal(HTMLParser):
    def __init__(s):
        super().__init__(); s.st, s.err = [], []
    def handle_starttag(s, t, a):
        if t not in VOID: s.st.append(t)
    def handle_endtag(s, t):
        if t in VOID: return
        if s.st and s.st[-1] == t: s.st.pop()
        else: s.err.append(t)


lines, ok_all, textos = ["# Validación páginas de ciudad (diseño pa-lp)", ""], True, {}
ids = []
for k, z in ZON.items():
    slug = f"physio-a-{k}"
    j = json.loads((OUT / slug / "elementor.json").read_text())
    w = j["content"][0]["elements"][0]["elements"][0]
    ids += [j["content"][0]["id"], j["content"][0]["elements"][0]["id"], w["id"]]
    h = w["settings"]["html"]
    markup = h[h.index('<div class="pa-lp">'):h.index("<script>")]
    soup = BeautifulSoup(markup, "html.parser")
    vis = soup.get_text(" ", strip=True)
    textos[slug] = vis
    b = Bal(); b.feed(h); b.close()
    c = {}
    c["JSON y estructura raíz"] = list(j) == ["content", "page_settings", "version", "title", "type"]
    c["HTML bien cerrado"] = not b.err and not b.st
    c["un solo H1"] = len(soup.find_all("h1")) == 1
    hs = [int(x.name[1]) for x in soup.find_all(re.compile("^h[1-6]$"))]
    c["sin saltos de encabezado"] = all(bb <= a + 1 for a, bb in zip(hs, hs[1:]))
    c["sin href=#"] = 'href="#"' not in h
    raras = sorted({cl for el in soup.find_all(True) for cl in (el.get("class") or []) if cl not in CLASES and not cl.startswith("fa-")})
    c["solo clases del CSS"] = not raras
    c["sin marcadores, receta ni seguro"] = not PROHIB.search(vis)
    ld = json.loads(re.search(r'application/ld\+json">(.*?)</script>', h, re.S).group(1).replace("<\\/", "</"))
    fq = next(g for g in ld["@graph"] if g["@type"] == "FAQPage")["mainEntity"]
    vfaq = [(x.select_one(".faq-q").get_text(strip=True), " ".join(x.select_one(".ans").get_text(" ", strip=True).split())) for x in soup.select(".faq")]
    c["FAQ visible = JSON-LD"] = vfaq == [(q["name"], " ".join(q["acceptedAnswer"]["text"].split())) for q in fq] and 8 <= len(vfaq) <= 10
    malos = [a["href"] for a in soup.select("a[href^='/']") if a["href"] not in URLS]
    c["enlaces internos válidos"] = not malos
    v = norm(z["nom_fr"]).split("-les-")[0]
    n = norm(vis)
    kw = {f"physio {v}": len(re.findall(rf"physio (?:a |de |pres de |pour )?{re.escape(v)}", n)),
          f"physiotherapeute {v}": len(re.findall(rf"physiotherapeute[s]? (?:a |de |pres de |pour )?{re.escape(v)}|physiotherapeute[^.]{{0,40}}{re.escape(v)}", n)),
          f"physiotherapie {v}": len(re.findall(rf"physiotherapie (?:a |de |pres de |pour )?{re.escape(v)}|physiotherapie[^.]{{0,40}}{re.escape(v)}", n)),
          "menciones de la ciudad": n.count(v)}
    c["keywords locales (≥ 2 cada variante)"] = all(x >= 2 for x in list(kw.values())[:3])
    ok = all(c.values()); ok_all &= ok
    lines += [f"## {'✅' if ok else '❌'} {slug}", ""] + [f"- {'✔' if vv else '✘'} {kk}" for kk, vv in c.items()]
    lines += [f"- ℹ keywords: {kw}", f"- ℹ palabras visibles: {len(vis.split())} · FAQ: {len(vfaq)}"] + ([f"- ℹ clases nuevas: {raras}"] if raras else []) + ([f"- ℹ enlaces: {malos}"] if malos else []) + [""]
    print("OK " if ok else "ERR", slug, [kk for kk, vv in c.items() if not vv], kw)


def sh(t):
    w = re.findall(r"\w+", norm(t)); return {" ".join(w[i:i + 5]) for i in range(len(w) - 4)}
S = {k: sh(v) for k, v in textos.items()}
mx = max(len(S[a] & S[b]) / min(len(S[a]), len(S[b])) for a, b in itertools.combinations(S, 2))
lines.insert(2, f"- IDs únicos: {len(ids) == len(set(ids))} · similitud máxima entre ciudades (texto completo, incl. bloques comunes): {mx:.1%}")
(OUT / "validacion.md").write_text("\n".join(lines))
print("IDs únicos", len(ids) == len(set(ids)), "similitud máx", f"{mx:.1%}", "TODO OK" if ok_all else "HAY ERRORES")
