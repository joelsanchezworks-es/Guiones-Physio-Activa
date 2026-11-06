"""Comprueba que todo el texto de fr.md (sin notas) aparece en la página construida (cobertura de palabras)."""
import re, json, pathlib, collections, sys
from bs4 import BeautifulSoup
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from construir_pagina import PAGINAS, PAG, OUT, limpiar_md
import markdown


def palabras(t):
    return re.findall(r"[a-zàâäéèêëîïôöùûüçœ']{4,}", t.lower())


res = {}
for slug, url, plt, lote, carpeta, *_ in PAGINAS:
    md = (PAG / carpeta / "fr.md").read_text()
    body = limpiar_md(md[re.match(r"^---\n.*?\n---\n", md, re.S).end():])
    src = collections.Counter(palabras(BeautifulSoup(markdown.markdown(body), "html.parser").get_text(" ")))
    j = json.loads((OUT / slug / "elementor.json").read_text())
    h = j["content"][0]["elements"][0]["elements"][0]["settings"]["html"]
    vis = BeautifulSoup(h.split("<style>")[0], "html.parser").get_text(" ")
    dst = collections.Counter(palabras(vis))
    falt = sum((src - dst).values())
    res[slug] = round(100 * (1 - falt / max(1, sum(src.values()))), 1)
if __name__ == "__main__":
    print(res)
