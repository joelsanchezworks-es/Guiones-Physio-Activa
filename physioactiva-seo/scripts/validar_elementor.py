"""Valida cada elementor.json del lote (sección 6 del encargo) y escribe entregables/6_elementor/validacion.md."""
import json, re, sys, pathlib, collections, yaml
from html.parser import HTMLParser
from bs4 import BeautifulSoup
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from construir_pagina import PAGINAS, OUT, STYLE_HOME, STYLE_LOMB, T_HOME, T_LOMB, REDIRIGIDAS, CLI
import similitud_zonas

BASE = pathlib.Path(__file__).resolve().parent.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
URLS_OK = {u.strip().replace("https://physioactiva.ch", "") or "/" for u in (BASE / "data/site/urls.txt").read_text().split()}
URLS_OK |= {p[1] for p in PAGINAS} | {"/nous-trouver/", "/contact/", "/physiotherapeute-a-domicile/"}
URLS_OK -= REDIRIGIDAS
CLASES_OK = set(re.findall(r"\.([a-zA-Z][\w-]*)", STYLE_HOME + STYLE_LOMB))
for t in (T_HOME, T_LOMB):
    h = t["content"][0]["elements"][0]["elements"][0]["settings"]["html"]
    for c in re.findall(r'class="([^"]+)"', h.split("<style>")[0]):
        CLASES_OK |= set(c.split())
TXT_PLANTILLA = set()
for t in (T_HOME, T_LOMB):
    s = BeautifulSoup(t["content"][0]["elements"][0]["elements"][0]["settings"]["html"].split("<style>")[0], "html.parser")
    TXT_PLANTILLA |= {x.strip() for x in s.find_all(string=True) if len(x.strip()) > 30}
ESPANOL = re.compile(r"\b(POR CONFIRMAR|para el|de la página|también|usted|teléfono de|¿|está|según el cliente|pendiente)\b", re.I)


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(); self.st, self.err = [], []

    def handle_starttag(self, t, a):
        if t not in VOID:
            self.st.append(t)

    def handle_endtag(self, t):
        if t in VOID:
            return
        if self.st and self.st[-1] == t:
            self.st.pop()
        else:
            self.err.append(f"cierre </{t}> inesperado (abierto: {self.st[-1] if self.st else '—'})")


IDS = collections.Counter()
filas, detalle = [], []
sim = similitud_zonas.calcular()
for p in PAGINAS:
    slug, url, plantilla, lote = p[0], p[1], p[2], p[3]
    f = OUT / slug / "elementor.json"
    checks, notas = {}, []
    try:
        j = json.loads(f.read_text()); checks["JSON válido"] = True
    except Exception as e:
        filas.append((slug, False, {"JSON válido": False}, [str(e)])); continue
    tpl = T_HOME if plantilla == "home" else T_LOMB
    checks["estructura raíz"] = list(j.keys()) == list(tpl.keys()) and j["version"] == tpl["version"] and j["type"] == tpl["type"]
    ids = []
    def walk(es):
        for e in es:
            ids.append(e["id"]); walk(e.get("elements", []))
    walk(j["content"])
    IDS.update(ids)
    checks["IDs 7 hex únicos en el archivo"] = len(ids) == len(set(ids)) and all(re.fullmatch(r"[0-9a-f]{7}", i) for i in ids)
    h = j["content"][0]["elements"][0]["elements"][0]["settings"]["html"]
    b = Balance(); b.feed(h); b.close()
    checks["HTML bien cerrado"] = not b.err and not b.st
    if b.err or b.st:
        notas += b.err[:3] + ([f"sin cerrar: {b.st[-3:]}"] if b.st else [])
    style = re.search(r"<style>.*?</style>", h, re.S)
    checks["<style> idéntico a la plantilla"] = bool(style) and style.group(0) == (STYLE_HOME if plantilla == "home" else STYLE_LOMB)
    markup = h.split("<style>")[0]
    soup = BeautifulSoup(markup, "html.parser")
    checks["sin href=\"#\""] = 'href="#"' not in h
    markup = h.split("<style>")[0]
    checks["sin data-i18n"] = "data-i18n" not in markup and "I18N" not in h
    usadas = {c for el in soup.find_all(True) for c in (el.get("class") or [])}
    raras = sorted(c for c in usadas if c not in CLASES_OK and not c.startswith("fa-"))
    checks["solo clases de la plantilla"] = not raras
    if raras: notas.append("clases nuevas: " + ", ".join(raras))
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S).group(1).replace("<\\/", "</"))
    g = {x["@type"]: x for x in ld["@graph"]}
    faq_vis = [(x.select_one(".faq-q").get_text(" ", strip=True), " ".join(x.select_one(".ans").get_text(" ", strip=True).split()))
               for x in soup.select(".faq")]
    faq_ld = [(q["name"], " ".join(q["acceptedAnswer"]["text"].split())) for q in g.get("FAQPage", {}).get("mainEntity", [])]
    norm_ = lambda s: re.sub(r"\s+([,.;:!?»)])", r"\1", s)
    checks["FAQ visible = JSON-LD"] = [(a, norm_(b_)) for a, b_ in faq_vis] == [(a, norm_(b_)) for a, b_ in faq_ld] and len(faq_vis) > 0
    if not checks["FAQ visible = JSON-LD"]:
        notas.append(f"FAQ: {len(faq_vis)} visibles / {len(faq_ld)} JSON-LD")
    hs = [int(x.name[1]) for x in soup.find_all(re.compile(r"^h[1-6]$"))]
    saltos = [f"h{a}→h{b_}" for a, b_ in zip(hs, hs[1:]) if b_ > a + 1]
    checks["un solo H1 y sin saltos"] = hs.count(1) == 1 and hs and hs[0] == 1 and not saltos
    if saltos: notas.append("saltos: " + ", ".join(sorted(set(saltos))))
    malos = []
    for a in soup.select("a[href]"):
        u = a["href"]
        if u.startswith("/") and u.split("#")[0] not in URLS_OK:
            malos.append(u)
        if u in REDIRIGIDAS:
            malos.append(u)
    urls_b = {z["url"] for z in __import__("construir_pagina").ZON.values() if z["lote"] == "B"}
    if lote != "B":
        malos += [u for u in (a["href"] for a in soup.select("a[href]")) if u in urls_b]
    checks["enlaces internos a URL final (sin 301/404 ni a borradores B)"] = not malos
    if malos: notas.append("enlaces: " + ", ".join(sorted(set(malos))))
    vis = soup.get_text(" ", strip=True)
    restos = [t for t in TXT_PLANTILLA if t in vis]
    checks["sin texto de la plantilla original"] = not restos
    if restos: notas.append("texto de plantilla: " + restos[0][:60])
    esp = ESPANOL.findall(vis)
    checks["sin lorem/TODO/español"] = not re.search(r"lorem|TODO", vis, re.I) and not esp
    if esp: notas.append("posible español: " + ", ".join(sorted(set(esp))[:5]))
    neg = g.get("Physiotherapy", {})
    checks["JSON-LD y NAP = cliente.yml"] = neg.get("telephone") == CLI["telephone_e164"] and neg.get("address", {}).get("streetAddress") == CLI["rue"] \
        and CLI["telephone"] in vis
    y = (OUT / slug / "yoast.txt").read_text()
    tl = int(re.search(r"SEO title \((\d+)/60\)", y).group(1)); ml = int(re.search(r"Meta description \((\d+)/155\)", y).group(1))
    checks["title ≤ 60 y meta ≤ 155"] = tl <= 60 and ml <= 155
    sub = soup.select_one(".hero .sub").get_text(" ", strip=True)
    ref = 300 if plantilla == "home" else 433
    notas.append(f"hero sub {len(sub)} car. (plantilla {ref}; ±20 % = {int(ref*.8)}–{int(ref*1.2)})")
    if slug.startswith("physio-a-"):
        z = sim[slug]
        checks["zona: similitud < 40 % y ≥ 4 datos"] = z["ok"]
        notas.append(f"similitud máx. {z['similitud_max']} % (con {z['con']}); datos propios: {', '.join(z['datos_propios'])}")
    n_conf = vis.count("[À CONFIRMER")
    ok = all(checks.values())
    filas.append((slug, ok, checks, notas, lote, url, plantilla, n_conf))

dup = [i for i, n in IDS.items() if n > 1]
lineas = ["# Validación de los JSON de Elementor", "", f"- Páginas: {len(filas)} · correctas: {sum(1 for f in filas if f[1])}",
          f"- IDs duplicados en el lote: {len(dup)}", "- Comprobaciones: estructura raíz, IDs, HTML cerrado, <style> idéntico, sin href=\"#\" ni data-i18n, solo clases de la plantilla, FAQ = JSON-LD, un H1 sin saltos, enlaces finales, sin texto de la plantilla, sin español, NAP, title/meta y, en zonas, similitud y datos propios.", ""]
for slug, ok, checks, notas, *rest in filas:
    lote, url, plantilla, n_conf = rest
    lineas += [f"## {'✅' if ok else '❌'} {slug} ({url}) · lote {lote} · plantilla {plantilla} · [À CONFIRMER]: {n_conf}", ""]
    lineas += [f"- {'✔' if v else '✘'} {k}" for k, v in checks.items()] + [f"- ℹ {n}" for n in notas] + [""]
(OUT / "validacion.md").write_text("\n".join(lineas))
(OUT / "_validacion.json").write_text(json.dumps([{"slug": f[0], "ok": f[1], "a_confirmer": f[7], "fallos": [k for k, v in f[2].items() if not v], "notas": f[3]} for f in filas], ensure_ascii=False, indent=1))
for f in filas:
    print("OK " if f[1] else "ERR", f[0], f[7], [k for k, v in f[2].items() if not v], [n for n in f[3] if not n.startswith(("hero", "similitud"))][:3])
print("IDs duplicados:", dup)
