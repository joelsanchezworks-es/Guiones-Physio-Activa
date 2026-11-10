"""Valida las plantillas nativas de entregables/10_nativo (H1 único, términos prohibidos, enlaces, keywords, FAQ)."""
import json, re, sys, pathlib, unicodedata
from bs4 import BeautifulSoup
BASE = pathlib.Path(__file__).resolve().parent.parent
PROHIB = re.compile(r"ordonnance|prescri\w*|LAMal|\bLAA\b|franchise|quote-part|rembours\w*|CONFIRM|tarif|\bprix\b|\bCHF\b|gratuit", re.I)
URLS = {u.strip().replace("https://physioactiva.ch", "") or "/" for u in (BASE / "data/site/urls.txt").read_text().split()}
URLS |= {f"/physio-a-{k}/" for k in ["ins", "sugiez", "neuchatel", "la-neuveville", "avenches", "lyss", "bienne", "fribourg", "payerne", "morat", "kerzers", "estavayer", "yvonand", "yverdon", "lausanne"]}
URLS |= {"/", "/sciatique-hernie-discale/", "/douleur-pied-cheville-fasciite-plantaire/", "/douleur-de-hanche-protheses/", "/reservation-en-ligne/"}
norm = lambda s: "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))
for slug, city in [a.split(":") for a in sys.argv[1:]]:
    t = json.loads((BASE / f"entregables/10_nativo/{slug}/{slug}.json").read_text())
    ws = []
    def walk(e):
        if e["elType"] == "widget": ws.append(e)
        for x in e["elements"]: walk(x)
    for s in t["content"]: walk(s)
    txt, html, h1 = [], [], 0
    for w in ws:
        s = w["settings"]
        if w["widgetType"] == "heading": txt.append(s["title"]); h1 += s["header_size"] == "h1"
        elif w["widgetType"] == "text-editor": html.append(s["editor"])
        elif w["widgetType"] == "button": txt.append(s["text"])
        elif w["widgetType"] == "icon-box": txt += [s["title_text"], s["description_text"]]
        elif w["widgetType"] == "accordion": faq = s["tabs"]; txt += [x["tab_title"] for x in faq]; html += [x["tab_content"] for x in faq]
        elif w["widgetType"] == "html" and "fiche" in s["html"]: html.append(s["html"])
    soup = BeautifulSoup(" ".join(html), "html.parser")
    vis = " ".join(txt) + " " + soup.get_text(" ")
    n, v = norm(vis), norm(city)
    links = [a["href"] for a in soup.find_all("a") if a["href"].startswith("/")]
    kw = {k: len(re.findall(rf"\b{k} (?:a |de |d'|pres de |pour )?{v}\b", n)) for k in ["physio", "physiotherapeute", "physiotherapie"]}
    res = {"H1 único": h1 == 1, "sin términos prohibidos": not PROHIB.search(vis), "enlaces válidos": all(l in URLS for l in links),
           "FAQ 8-10 + schema": 8 <= len(faq) <= 10 and any(w["widgetType"] == "accordion" and w["settings"].get("faq_schema") == "yes" for w in ws),
           "keywords ≥2": all(x >= 2 for x in kw.values()), "IDs únicos": len({w["id"] for w in ws}) == len(ws)}
    print(slug, "OK" if all(res.values()) else "ERR", [k for k, x in res.items() if not x], kw, "FAQ", len(faq), "palabras", len(vis.split()),
          "malos:", [l for l in links if l not in URLS], "título plantilla:", t["title"])
