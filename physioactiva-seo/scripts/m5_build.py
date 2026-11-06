"""Módulo 5 · de fr.md a fr.html, fr-ascii.html, yoast.txt y schema.json (+ validación)."""
import json, re, sys, pathlib, yaml, markdown, html as H
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
SITE = "https://physioactiva.ch"
NEGOCIO = {
    "@type": "Physiotherapy", "@id": SITE + "/#physiotherapy", "name": "Physio Activa", "url": SITE + "/",
    "telephone": "+41766273838",
    "address": {"@type": "PostalAddress", "streetAddress": "Rämismatte 21", "postalCode": "3232", "addressLocality": "Ins",
                "addressRegion": "BE", "addressCountry": "CH"},
    "geo": {"@type": "GeoCoordinates", "latitude": 47.0058, "longitude": 7.1063},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                    "opens": "08:30", "closes": "19:30"}],
    "areaServed": [{"@type": "City", "name": n} for n in ["Ins", "Anet", "Sugiez", "Mont-Vully", "Murten / Morat", "Kerzers / Chiètres",
                                                         "Avenches", "La Neuveville", "Neuchâtel", "Biel/Bienne", "Lyss"]],
    "availableLanguage": ["fr", "es"], "priceRange": "[POR CONFIRMAR]",
}


def split(md):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.S)
    return yaml.safe_load(m.group(1)), m.group(2)


def faq(body):
    m = re.search(r"^## Questions fr[ée]quentes.*?$(.*?)(?=^## |\Z)", body, re.S | re.M)
    if not m:
        return []
    out = []
    for q, a in re.findall(r"^### (.+?)\n(.*?)(?=^### |\Z)", m.group(1), re.S | re.M):
        a = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", " ".join(a.split()))
        out.append({"@type": "Question", "name": q.strip(), "acceptedAnswer": {"@type": "Answer", "text": a.strip()}})
    return out


def ascii_html(s):
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in s)


informe = []
for d in sorted((BASE / "entregables/5_paginas").iterdir()):
    f = d / "fr.md"
    if not f.exists():
        continue
    meta, body = split(f.read_text())
    cuerpo = re.split(r"^## Notes pour l'équipe \(ES\)", body, flags=re.M)[0].strip()
    notas = body[len(cuerpo):].strip()
    html = markdown.markdown(cuerpo, extensions=["extra", "sane_lists"])
    (d / "fr.html").write_text(html + "\n")
    (d / "fr-ascii.html").write_text(ascii_html(html) + "\n")
    h1 = re.search(r"^# (.+)$", cuerpo, re.M)
    t, m = meta["title"], meta["meta"]
    errores = []
    if len(t) > 60: errores.append(f"title {len(t)} > 60")
    if len(m) > 155: errores.append(f"meta {len(m)} > 155")
    if len(m) < 110: errores.append(f"meta {len(m)} < 110")
    if not h1: errores.append("sin H1")
    if re.search(r"\b(guérir|guérison garantie|garanti|100 ?%)\b", cuerpo, re.I): errores.append("posible promesa de resultado")
    (d / "yoast.txt").write_text(
        f"SEO title ({len(t)}/60): {t}\nMeta description ({len(m)}/155): {m}\nSlug: {meta['slug']}\nFocus keyphrase: {meta['keyword_principal']}\n"
        f"H1: {h1.group(1) if h1 else ''}\n")
    url = SITE + meta["slug"]
    graph = [NEGOCIO]
    page = {"@type": "MedicalWebPage" if meta["tipo"] == "patologia" else "WebPage", "@id": url + "#webpage", "url": url,
            "name": t, "description": m, "inLanguage": "fr-CH", "isPartOf": {"@id": SITE + "/#website"},
            "about": {"@id": SITE + "/#physiotherapy"}, "lastReviewed": dfs.HOY,
            "reviewedBy": {"@type": "Person", "name": "[POR CONFIRMAR: physiothérapeute qui valide la page]"}}
    if meta["tipo"] == "patologia":
        page["about"] = {"@type": "MedicalCondition", "name": meta.get("condicion") or meta["keyword_principal"]}
        page["provider"] = {"@id": SITE + "/#physiotherapy"}
    graph.append(page)
    q = faq(cuerpo)
    if q:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": q})
    (d / "schema.json").write_text(json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1))
    palabras = len(re.sub(r"[#*\[\]()>|`-]", " ", re.sub(r"\]\([^)]+\)", "]", cuerpo)).split())
    informe.append({"slug": d.name, "url": meta["slug"], "tipo": meta["tipo"], "title": t, "len_title": len(t), "meta": m, "len_meta": len(m),
                    "h1": h1.group(1) if h1 else "", "palabras": palabras, "faq": len(q), "por_confirmar": cuerpo.count("[POR CONFIRMAR"),
                    "errores": errores, "keyword_principal": meta["keyword_principal"], "notas_es": notas})
(BASE / "data/m5_paginas.json").write_text(json.dumps(informe, ensure_ascii=False, indent=1))
for i in informe:
    print(i["slug"], i["len_title"], i["len_meta"], i["palabras"], "faq", i["faq"], "PC", i["por_confirmar"], i["errores"])
