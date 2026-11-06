"""2.5.1 · Extrae el patrón de estructura SEO local de activaglobals.com (4 páginas guardadas en referencias/activa_html/).
Salida: referencias/activa_patron.md (por página: title, H1, H2/H3 en orden, palabras, FAQ, CTA, enlaces internos y ciudad en encabezados)."""
import re, pathlib, json, collections
from bs4 import BeautifulSoup

BASE = pathlib.Path(__file__).resolve().parent.parent
D = BASE / "referencias/activa_html"
CIUDAD = re.compile(r"sabadell", re.I)
out = ["# Patrón de estructura: activaglobals.com", "", "Rastreo propio del 2026-11-06 (HTML servido, sin JavaScript). Se copia la **estructura**, no el contenido ni el tono.", ""]
resumen = {}
for f in ["home", "instalacion-electrica-sabadell", "acometida-electrica-sabadell", "cuadro-electrico-sabadell"]:
    soup = BeautifulSoup((D / f"{f}.html").read_text(errors="ignore"), "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    for t in soup.select("header, footer, nav"):
        t.decompose()
    main = soup.select_one("main") or soup.body
    hs = [(h.name, " ".join(h.get_text(" ", strip=True).split())) for h in main.find_all(re.compile(r"^h[1-4]$"))]
    words = len(main.get_text(" ", strip=True).split())
    faq_q = []
    h2f = next((x for x in main.find_all("h2") if re.search(r"frecuentes", x.get_text(), re.I)), None)
    if h2f:
        for el in h2f.find_all_next(string=True):
            if el.parent.name == "h2" and el.parent is not h2f:
                break
            t = el.strip()
            if t.endswith("?") and 15 < len(t) < 160 and t not in faq_q:
                faq_q.append(t)
    details = []
    links = []
    for a in main.select("a[href]"):
        h = a["href"]
        if "activaglobals.com" in h or h.startswith("/"):
            txt = " ".join(a.get_text(" ", strip=True).split())
            if txt:
                links.append((txt[:60], h.replace("https://activaglobals.com", "")))
    ctas = collections.Counter()
    for a in main.select("a[href]"):
        h = a["href"]
        if h.startswith("tel:"): ctas["teléfono"] += 1
        elif "wa.me" in h or "whatsapp" in h: ctas["WhatsApp" + (" (con mensaje)" if "text=" in h else "")] += 1
        elif "contact" in h or "presupuesto" in h: ctas["formulario/presupuesto"] += 1
        elif h == "#": ctas["enlace #"] += 1
    ld = len(re.findall(r"application/ld\+json", (D / f"{f}.html").read_text(errors="ignore")))
    ciudad_en = [f"{n.upper()}: {t}" for n, t in hs if CIUDAD.search(t)]
    resumen[f] = {"h2": sum(1 for n, _ in hs if n == "h2"), "h3": sum(1 for n, _ in hs if n == "h3"), "palabras": words,
                  "faq": max(len(faq_q), len(details)), "ciudad_h2": sum(1 for n, t in hs if n == "h2" and CIUDAD.search(t)),
                  "ciudad_h3": sum(1 for n, t in hs if n == "h3" and CIUDAD.search(t))}
    out += [f"## /{'' if f == 'home' else f + '/'}", "", f"- **Title:** {title}", f"- **Palabras (cuerpo, sin header/footer):** {words}",
            f"- **Preguntas de FAQ detectadas:** {resumen[f]['faq']}", f"- **CTA:** {dict(ctas) or '—'}",
            f"- **JSON-LD:** {ld} bloque(s)", f"- **FAQ:** " + " · ".join(faq_q[:12]), f"- **Ciudad en encabezados:** {len(ciudad_en)} → " + ("; ".join(ciudad_en) or "—"), "",
            "### Encabezados en orden", ""] + [f"{'  ' * (int(n[1]) - 1)}- {n.upper()} {t}" for n, t in hs] + ["",
            "### Enlaces internos del cuerpo (anchor → URL)", ""] + [f"- {t} → `{u}`" for t, u in list(dict.fromkeys(links))[:30]] + [""]
out += ["## Receta común deducida", "",
        "| Página | H2 | H3 | Palabras | FAQ | Ciudad en H2 | Ciudad en H3 |", "|---|---|---|---|---|---|---|"]
out += [f"| {k} | {v['h2']} | {v['h3']} | {v['palabras']} | {v['faq']} | {v['ciudad_h2']} | {v['ciudad_h3']} |" for k, v in resumen.items()]
out += ["", "### Receta (lo que se copia, verificado en el rastreo)", "",
        "1. **H1 corto «Servicio en Ciudad»** (home: «Electricista en Sabadell»).",
        "2. **4 H3 de valor justo debajo del hero.** La referencia salta de H1 a H3; en Physioactiva se pone un H2 corto encima para no romper la jerarquía.",
        "3. **Servicio:** qué es y cuándo hace falta (H2) → qué tipo necesita tu caso (H2 + un H3 por subtipo) → proceso en 3-5 pasos (H2 + H3 por paso) → cuánto cuesta / qué lo determina (H2 con la ciudad + H3) → FAQ de 10 preguntas (H2 con la ciudad) → CTA final en pregunta (H2 con la ciudad + «o alrededores»).",
        "4. **Home:** H1 → 4 H3 de valor → quiénes somos (H2 con la ciudad) → trabajos/galería (H2) → servicios (H2 con la ciudad + un H3 por servicio) → proceso en 3 pasos (H2 + 3 H3) → FAQ de 10 (H2 con la ciudad) → CTA final en pregunta (H2 con la ciudad).",
        "5. **Ciudad en el title, el H1 y 2-4 H2**; nunca en un H3.",
        "6. **CTA repetidos:** hero, tras el proceso y al final; teléfono ×4 por página y WhatsApp con mensaje rellenado (`wa.me/…?text=`).",
        "7. **Enlaces internos en el cuerpo** hacia otros servicios con anchor descriptivo («cambio de cuadro eléctrico en Sabadell», «acometida eléctrica»).",
        "8. **No se copia:** precios, «+30 años», galería antes/después, enlaces `#` del menú, contadores a 0, CTA a formulario."]
(BASE / "referencias/activa_patron.md").write_text("\n".join(out) + "\n")
print(json.dumps(resumen, indent=1))
