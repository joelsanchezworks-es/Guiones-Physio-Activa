#!/usr/bin/env python3
"""Genera, a partir de una carpeta de salidas:
  - 01-banco-de-hooks.md (desde 01-banco-de-hooks.csv, si existe)
  - guiones-grabacion.html (todo el paquete en una página imprimible A4, con los hooks primero)

Uso:  python3 tools/build_entregables.py salidas/2026-10-29
Sin dependencias externas (solo la librería estándar de Python).
"""
import csv
import html
import re
import sys
from pathlib import Path

ANGULOS = {
    "A": "A. Sin espera — cita esta semana frente a 3 meses de espera",
    "B": "B. Sin tiempo — hasta las 20 h, después del trabajo",
    "C": "C. Dolor concreto — espalda, cervical, hombro, rodilla",
    "D": "D. Más que un masaje — plan activo + MTT",
    "E": "E. A domicilio — para mayores o tras el hospital (habla al familiar)",
    "F": "F. Seguro / MTT gratis en Neuchâtel — elimina la objeción del precio",
}


# ---------------------------------------------------------------- banco de hooks
def load_hooks(folder: Path):
    path = folder / "01-banco-de-hooks.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pipe(s: str) -> str:
    return s.replace("|", "\\|")


def bank_markdown(rows) -> str:
    by_base = {}
    for r in rows:
        by_base.setdefault(r["id"].rsplit("-", 1)[0], {})[r["idioma"]] = r
    out = [
        "# 01 · Banco de hooks",
        "",
        f"{len(rows)} hooks ({sum(r['idioma'] == 'FR' for r in rows)} FR + {sum(r['idioma'] == 'DE' for r in rows)} DE). "
        "Cada hook tiene tres capas: **verbal** (≤12 palabras), **visual** (primer segundo, grabable con móvil) y **texto en pantalla** (≤6 palabras). "
        "La versión DE es una adaptación natural del mismo hook (mismo número, sufijo `-DE`). La fuente editable es `01-banco-de-hooks.csv`.",
        "",
    ]
    for letter, title in ANGULOS.items():
        bases = [b for b in by_base if b.startswith(letter)]
        if not bases:
            continue
        out += [f"## {title}", ""]
        out += ["| ID | Tipo | Hook verbal | Texto en pantalla | Hook visual | Público | Uso | Hipótesis |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for b in bases:
            fr, de = by_base[b].get("FR"), by_base[b].get("DE")
            for r in (fr, de):
                if not r:
                    continue
                star = " ⭐" if r.get("top10") else ""
                out.append(f"| **{r['id']}**{star} | {pipe(r['tipo'])} | {pipe(r['hook_verbal'])} | {pipe(r['texto_pantalla'])} | "
                           f"{pipe(r['hook_visual']) if r is fr else '= FR'} | {pipe(r['publico'])} | {pipe(r['uso'])} | "
                           f"{pipe(r['hipotesis']) if r is fr else '= FR'} |")
        out.append("")
    top = sorted((r for r in rows if r.get("top10")), key=lambda r: int(r["top10"]))
    if top:
        out += ["## ⭐ Top 10 para testear primero", "",
                "| # | Hook | Hook verbal (FR) | Por qué |", "| --- | --- | --- | --- |"]
        for r in top:
            out.append(f"| {r['top10']} | **{r['id']}** | {pipe(r['hook_verbal'])} | {pipe(r['motivo_top10'])} |")
        out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- markdown → html mínimo
def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = s.replace("&lt;br&gt;", "<br>")
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\s][^*]*)\*(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"\[(POR CONFIRMAR[^\]]*|NOMBRE POR CONFIRMAR|NOM DU FITNESS|NAME DES FITNESS)\]",
               r'<mark>[\1]</mark>', s)
    s = s.replace("\\|", "|")
    return s


def split_row(line: str):
    line = line.strip().strip("|")
    cells = re.split(r"(?<!\\)\|", line)
    return [c.strip() for c in cells]


def md_to_html(md: str, shift: int = 0) -> str:
    lines = md.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            lvl = min(len(m.group(1)) + shift, 6)
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue
        if line.strip() == "---":
            out.append("<hr>")
            i += 1
            continue
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            head = split_row(line)
            i += 2
            body = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                body.append(split_row(lines[i]))
                i += 1
            t = ["<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"]
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue
        if line.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").rstrip())
                i += 1
            out.append("<blockquote>" + "<br>".join(inline(b) for b in buf) + "</blockquote>")
            continue
        if re.match(r"^\s*[-*] ", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                txt = re.sub(r"^\s*[-*] ", "", lines[i])
                txt = re.sub(r"^\[ \] ", "☐ ", txt)
                items.append(f"<li>{inline(txt)}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if re.match(r"^\s*\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\. ", lines[i]):
                items.append(f"<li>{inline(re.sub(r'^\s*\d+\. ', '', lines[i]))}</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||>|\s*[-*] |\s*\d+\. |---)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        if not buf:  # línea que no encaja en nada: se pinta tal cual
            buf, i = [line.strip()], i + 1
        out.append("<p>" + "<br>".join(inline(b) for b in buf) + "</p>")
    return "\n".join(out)


# ---------------------------------------------------------------- hoja de rodaje
def hooks_sheet(rows) -> str:
    """Tabla compacta de hooks para el rodaje: FR y DE juntos, con casilla de toma."""
    by_base = {}
    for r in rows:
        by_base.setdefault(r["id"].rsplit("-", 1)[0], {})[r["idioma"]] = r
    out = []
    for letter, title in ANGULOS.items():
        bases = [b for b in by_base if b.startswith(letter)]
        if not bases:
            continue
        out.append(f"<h3>{html.escape(title)}</h3>")
        out.append('<table class="hooks"><thead><tr><th>ID</th><th>Visual (primer segundo)</th>'
                   "<th>FR · lo que se dice / texto</th><th>DE · was gesagt wird / Text</th><th>✓</th></tr></thead><tbody>")
        for b in bases:
            fr, de = by_base[b].get("FR", {}), by_base[b].get("DE", {})
            star = " ⭐" if fr.get("top10") else ""
            out.append(
                f"<tr><td><strong>{b}</strong>{star}<br><small>{html.escape(fr.get('tipo', ''))}</small></td>"
                f"<td>{html.escape(fr.get('hook_visual', ''))}</td>"
                f"<td>«{html.escape(fr.get('hook_verbal', ''))}»<br><span class='ost'>{html.escape(fr.get('texto_pantalla', ''))}</span></td>"
                f"<td>«{html.escape(de.get('hook_verbal', ''))}»<br><span class='ost'>{html.escape(de.get('texto_pantalla', ''))}</span></td>"
                "<td class='chk'>☐ FR<br>☐ DE</td></tr>")
        out.append("</tbody></table>")
    return "\n".join(out)


CSS = """
:root{--ink:#1d2421;--muted:#5d6762;--line:#d9d6cd;--accent:#1f7a5a;--soft:#e8f3ee;--mark:#fff1c2;--bg:#ffffff}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ink:#e9ece9;--muted:#a3ada8;--line:#34403b;--accent:#4cc095;--soft:#1f2d27;--mark:#5a4a12;--bg:#121614}}
:root[data-theme="dark"]{--ink:#e9ece9;--muted:#a3ada8;--line:#34403b;--accent:#4cc095;--soft:#1f2d27;--mark:#5a4a12;--bg:#121614}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:13px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1000px;margin:0 auto;padding:24px 16px 64px}
header.cover{border-bottom:3px solid var(--accent);padding-bottom:12px;margin-bottom:16px}
header.cover h1{margin:0;font-size:22px}
header.cover p{margin:4px 0 0;color:var(--muted)}
nav.toc{columns:2;column-gap:24px;font-size:12px;margin:12px 0 24px}
nav.toc a{color:var(--accent);text-decoration:none}
h1{font-size:20px;margin:28px 0 8px}
h2{font-size:17px;margin:22px 0 8px;color:var(--accent)}
h3{font-size:14px;margin:16px 0 6px}
h4,h5,h6{font-size:13px;margin:12px 0 4px}
table{border-collapse:collapse;width:100%;margin:8px 0 12px;font-size:12px}
th,td{border:1px solid var(--line);padding:5px 7px;vertical-align:top;text-align:left}
th{background:var(--soft)}
table.hooks td:nth-child(1){width:11%}
table.hooks td:nth-child(2){width:27%}
table.hooks td.chk{width:7%;white-space:nowrap;font-size:11px}
.ost{display:inline-block;margin-top:3px;padding:1px 5px;border-radius:4px;background:var(--soft);font-weight:600;font-size:11px}
code{font-size:11px;background:var(--soft);padding:0 3px;border-radius:3px}
td code{white-space:nowrap}
td:first-child,th:first-child{white-space:nowrap}
table.hooks td:first-child{white-space:normal}
mark{background:var(--mark);color:inherit;padding:0 2px}
blockquote{margin:8px 0;padding:6px 10px;border-left:3px solid var(--accent);background:var(--soft)}
section.doc{border-top:1px solid var(--line);margin-top:24px}
.wrap{overflow-wrap:anywhere}
@media (max-width:640px){nav.toc{columns:1}table{display:block;overflow-x:auto}}
@page{size:A4;margin:12mm 10mm}
@media print{
  :root{--ink:#000;--muted:#444;--line:#999;--accent:#1f5f47;--soft:#eef4f1;--mark:#fff1c2;--bg:#fff}
  body{font-size:9.5pt}
  .wrap{max-width:none;padding:0}
  nav.toc{display:none}
  section.doc{page-break-before:always;border:0;margin:0}
  section.doc:first-of-type{page-break-before:auto}
  td code{font-size:7pt}
  h1,h2,h3{page-break-after:avoid}
  tr,blockquote{page-break-inside:avoid}
  table{font-size:8.5pt}
  a{color:inherit;text-decoration:none}
}
"""


def build_html(folder: Path, rows) -> str:
    docs = []  # (id, título, html)
    if rows:
        top = sorted((r for r in rows if r.get("top10")), key=lambda r: int(r["top10"]))
        top_html = "<ol>" + "".join(
            f"<li><strong>{r['id']}</strong> — «{html.escape(r['hook_verbal'])}» <small>({html.escape(r['motivo_top10'])})</small></li>"
            for r in top) + "</ol>"
        docs.append(("hooks", "Hooks para grabar (FR + DE)",
                     "<p>⭐ = top 10 para testear primero. Grabar <strong>3 tomas por hook y por idioma</strong>, 1 s de silencio antes y después. "
                     "Hook verbal ≤12 palabras · texto en pantalla ≤6 palabras.</p>"
                     + "<h2>⭐ Top 10 para testear primero</h2>" + top_html + hooks_sheet(rows)))
    used = {"01-banco-de-hooks.md"}

    def add_file(names, did, title):
        for name in names:
            p = folder / name
            if p.exists():
                used.add(name)
                docs.append((did, title, md_to_html(p.read_text(encoding="utf-8"), shift=1)))
                return

    def add_dir(names, did, title):
        for name in names:
            d = folder / name
            if d.is_dir():
                parts = [md_to_html(f.read_text(encoding="utf-8"), shift=1) for f in sorted(d.glob("*.md"))]
                if parts:
                    docs.append((did, title, "<hr>".join(parts)))
                return

    # Nombres del paquete completo y de los comandos de .claude/commands.
    add_file(["02-test-de-hooks.md", "test-hooks.md"], "test", "Test de hooks (cuerpos base)")
    add_file(["05-plan-de-grabacion.md", "plan-grabacion.md"], "plan", "Plan de grabación")
    add_dir(["04-guiones-ads", "ads"], "ads", "Guiones de ads")
    add_dir(["03-guiones-organico", "organico"], "org", "Guiones orgánicos")
    rest = [f for f in sorted(folder.glob("*.md"))
            if f.name not in used | {"06-calendario-publicacion.md", "00-pendientes.md"}]
    for n, f in enumerate(rest):
        used.add(f.name)
        docs.append((f"otro{n}", f.stem, md_to_html(f.read_text(encoding="utf-8"), shift=1)))
    add_file(["06-calendario-publicacion.md"], "cal", "Calendario de publicación")
    add_file(["00-pendientes.md"], "pend", "Pendientes")
    docs[:] = [(d, f"{i} · {t}", h) for i, (d, t, h) in enumerate(docs, 1)]

    toc = "".join(f'<div><a href="#{d}">{html.escape(t)}</a></div>' for d, t, _ in docs)
    body = "".join(f'<section class="doc" id="{d}"><h1>{html.escape(t)}</h1>{h}</section>' for d, t, h in docs)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Guiones de grabación</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="cover">
  <h1>Physio Activa · Guiones de grabación</h1>
  <p>Paquete {html.escape(folder.name)} · Hooks, test, ads y orgánico en FR + DE · Imprimir en A4 (Ctrl/Cmd + P)</p>
</header>
<nav class="toc">{toc}</nav>
{body}
</div>
</body>
</html>
"""


def main():
    if len(sys.argv) != 2:
        sys.exit("Uso: python3 tools/build_entregables.py salidas/AAAA-MM-DD")
    folder = Path(sys.argv[1])
    if not folder.is_dir():
        sys.exit(f"No existe la carpeta {folder}")
    rows = load_hooks(folder)
    if rows:
        (folder / "01-banco-de-hooks.md").write_text(bank_markdown(rows), encoding="utf-8")
        print(f"01-banco-de-hooks.md: {len(rows)} hooks")
    (folder / "guiones-grabacion.html").write_text(build_html(folder, rows), encoding="utf-8")
    print(f"guiones-grabacion.html generado en {folder}")


if __name__ == "__main__":
    main()
