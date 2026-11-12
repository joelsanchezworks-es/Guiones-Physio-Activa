"""Separa cada plantilla Elementor en markup / <style> / <script> y guarda cada <section> como componente,
con un resumen .md (clases, campos de texto y su longitud, iconos, enlaces, imágenes).
Salida: plantillas/_componentes/<plantilla>__NN-<nombre>.html|.md, plantillas/_partes/<plantilla>.{style.css,script.js,markup.html}
"""
import json, re, pathlib, sys
from bs4 import BeautifulSoup

BASE = pathlib.Path(__file__).resolve().parent.parent
P = BASE / "plantillas"
OUT, PARTES = P / "_componentes", P / "_partes"
OUT.mkdir(exist_ok=True); PARTES.mkdir(exist_ok=True)


def partes(nombre):
    d = json.loads((P / f"{nombre}.json").read_text())
    html = d["content"][0]["elements"][0]["elements"][0]["settings"]["html"]
    style = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    script = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    markup = html[: html.find("<style>")].strip()
    return d, markup, style, script


def nombre_seccion(s):
    cls = " ".join(s.get("class") or [])
    if cls:
        return cls.split()[0]
    for c in ("faq-list", "team-grid", "serv-grid"):
        if s.select_one("." + c):
            return c
    return "texte"


if __name__ == "__main__":
    for nombre in ("home-design-elementor", "lombaire-elementor"):
        d, markup, style, script = partes(nombre)
        corto = nombre.split("-")[0]
        (PARTES / f"{corto}.style.css").write_text(style)
        (PARTES / f"{corto}.script.js").write_text(script)
        (PARTES / f"{corto}.markup.html").write_text(markup)
        soup = BeautifulSoup(markup, "html.parser")
        for i, s in enumerate(soup.select("div.pa-home > section"), 1):
            n = nombre_seccion(s)
            (OUT / f"{corto}__{i:02d}-{n}.html").write_text(str(s))
            textos = []
            for el in s.find_all(["span", "h1", "h2", "h3", "h4", "p", "a", "button", "div"]):
                t = el.find(string=True, recursive=False)
                if t and t.strip():
                    textos.append(f"- `{el.name}.{'.'.join(el.get('class') or [])}` ({len(el.get_text(' ', strip=True))} car.): {el.get_text(' ', strip=True)[:90]}")
            clases = sorted({c for el in s.find_all(True) for c in (el.get("class") or [])})
            iconos = sorted({c for el in s.select("i") for c in el.get("class") if c.startswith("fa-") and c not in ("fa-solid", "fa-brands", "fa-regular")})
            enlaces = [a.get("href") for a in s.select("a[href]")]
            imgs = [im.get("src") for im in s.select("img")] + [so.get("src") for so in s.select("source")]
            md = [f"# Componente {corto} #{i}: {n}", "", f"- Clases: {', '.join(clases)}", f"- Iconos: {', '.join(iconos) or '—'}",
                  f"- Enlaces: {', '.join(enlaces) or '—'}", f"- Imágenes/vídeo: {', '.join(imgs) or '—'}",
                  f"- data-i18n: {len(s.select('[data-i18n]'))}", "", "## Campos de texto", ""] + textos[:60]
            (OUT / f"{corto}__{i:02d}-{n}.md").write_text("\n".join(md) + "\n")
            print(corto, i, n, len(str(s)), "car.")
        print(corto, "style", len(style), "script", len(script), "href=#:", markup.count('href="#"'))
