"""Entregables de cierre de la fase Elementor: checklist por página, PREGUNTAS_CLIENTE.md, menu.md, redirecciones.csv,
pendientes_imagenes.md, PUBLICAR.md e index.html."""
import json, re, pathlib, sys, html as H, collections, yaml
from bs4 import BeautifulSoup
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from construir_pagina import PAGINAS, OUT, CLI, ZON

V = {v["slug"]: v for v in json.loads((OUT / "_validacion.json").read_text())}
LOTE = {r["slug"]: r for r in json.loads((OUT / "_lote.json").read_text())}
TEMAS = [("Datos del cabinet y NAP", r"adresse|rämismatte|nap"), ("Horarios y plazos", r"horaire|heure|délai|semaine|rendez-vous|annulation|20h|19"),
         ("Atención a domicilio por localidad", r"domicile|déplac|passage|localités|villages|desservi"),
         ("Equipo, titulaciones e idiomas", r"titre|formation|diplôm|registre|nareg|rcc|langue|portugais|allemand|espagnol|grossesse|spécialis"),
         ("Tarifas y sesiones", r"tarif|prix|durée|séance|coût"), ("Otros", r".")]


def marcadores(slug):
    h = json.loads((OUT / slug / "elementor.json").read_text())["content"][0]["elements"][0]["elements"][0]["settings"]["html"]
    soup = BeautifulSoup(h.split("<style>")[0], "html.parser")
    out = []
    for el in soup.find_all(["p", "h3", "span", "div"]):
        t = el.get_text(" ", strip=True)
        if "[À CONFIRMER" in t and not any("[À CONFIRMER" in c.get_text(" ", strip=True) for c in el.find_all(["p", "h3", "span", "div"])):
            for m in re.finditer(r"\[À CONFIRMER[^\]]*\]", t):
                i = m.start()
                frase = t[max(0, t.rfind(".", 0, i) + 1):t.find(".", m.end()) + 1 if t.find(".", m.end()) > 0 else len(t)].strip()
                out.append((m.group(0), frase[:260]))
    return out


preg = collections.OrderedDict((t, []) for t, _ in TEMAS)
for p in PAGINAS:
    slug, url, plt, lote = p[:4]
    ms = marcadores(slug)
    for m, frase in ms:
        tema = next(t for t, rx in TEMAS if re.search(rx, (m + " " + frase).lower()))
        preg[tema].append((url, m, frase))
    r = LOTE[slug]
    receta_p = json.loads((OUT / slug / "receta.json").read_text())
    nota_receta = next((n for n in V[slug]["notas"] if n.startswith("receta:")), "")
    def tiene(pred):
        return any(pred(x) for x in receta_p)
    h2s = lambda x: re.sub("<[^>]+>", "", x.get("h2", "") or "")
    rec = [
        ("H1 «servicio + ciudad»", True, r["h1"]),
        ("4 H3 de valor bajo el hero", tiene(lambda x: x["tipo"] == "grid" and len(x.get("cards", [])) == 4 and re.search(r"essentiel|bref", h2s(x), re.I)), ""),
        ("Qué es / cuándo consultar (+ señales de alarma)", tiene(lambda x: re.search(r"qu'est-ce|quand consulter|urgence|médecin", h2s(x), re.I)), ""),
        ("Tipos según el caso (H2 + H3 por subtipo)", tiene(lambda x: x["tipo"] in ("grid", "serv") and re.search(r"selon|peut aider|traitement|prise en charge|traitons|soins", h2s(x), re.I)), ""),
        ("Proceso en pasos (H2 + H3) + CTA intermedio", tiene(lambda x: x.get("cta_mid")), ""),
        ("Reembolso y coste", tiene(lambda x: re.search(r"rembours", h2s(x), re.I)), ""),
        ("FAQ (8-10)", tiene(lambda x: x["tipo"] == "faq" and len(x["faq"]) >= 8), f"{next((len(x['faq']) for x in receta_p if x['tipo'] == 'faq'), 0)} preguntas"),
        ("CTA final en pregunta con la ciudad", tiene(lambda x: x["tipo"] == "cta" and x["h2"].endswith("?")), ""),
    ]
    motivo = {"FAQ (8-10)": "texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión",
              "Qué es / cuándo consultar (+ señales de alarma)": "página sin patología concreta (hub/reserva/home): no aplica",
              "Proceso en pasos (H2 + H3) + CTA intermedio": "no aplica a esta página",
              "Tipos según el caso (H2 + H3 por subtipo)": "no aplica a esta página"}
    ck_rec = ["", "## Receta activaglobals (2.5)", "", "| Sección | ¿Está? | Nota |", "|---|---|---|"] + [
        f"| {a} | {'sí' if b else 'no'} | {c if b or c else motivo.get(a, 'omitida')}{'' if b else (' — ' + motivo.get(a, '') if c else '')} |" for a, b, c in rec] + ["", f"- {nota_receta}"]
    ck = [f"# Checklist — {url}", "", f"- Lote: {lote} · Plantilla: {plt} · Validación: {'OK' if V[slug]['ok'] else 'ERRORES: ' + ', '.join(V[slug]['fallos'])}",
          f"- Indexación: {'NOINDEX hasta la confirmación del cliente' if lote == 'B' else 'index, follow'}", "",
          f"## Marcadores [À CONFIRMER] ({len(ms)})", ""] + [f"- {m} — «{f}»" for m, f in ms] + ["",
          "## Publicación", "", "1. WordPress → Páginas → abrir (o crear) la página con el slug `" + url + "`.",
          "2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.",
          "3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.",
          "4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`." + (" Avanzado → noindex." if lote == "B" else ""),
          "5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.",
          "6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md)."] + ck_rec
    (OUT / slug / "checklist.md").write_text("\n".join(ck) + "\n")

GLOBAL = [
    ("Datos del cabinet y NAP", "Dirección exacta: el sitio y la ficha de Google dicen «Rämismatte 21, 3232 Ins»; el encargo decía 31. ¿Cuál es la correcta?"),
    ("Horarios y plazos", "Horario real: la ficha de Google dice lunes a viernes de 8:30 a 19:30; el sitio actual, «jusqu'à 20h». ¿Y el plazo habitual para la primera cita?"),
    ("Equipo, titulaciones e idiomas", "Titulación, formación y número de registro profesional (NAREG / RCC) de Francisco Díaz y Lucile Combes, y foto actualizada para la autoría."),
    ("Equipo, titulaciones e idiomas", "Idiomas: el sitio actual cita francés, alemán, portugués y español; ¿cuáles se ofrecen de verdad en consulta?"),
    ("Equipo, titulaciones e idiomas", "Traductor del navegador (FR/DE/EN/PT/ES) retirado de la home: ¿quieren mantener versiones EN/PT/ES? La versión DE ya existe en /de/."),
    ("Atención a domicilio por localidad", "¿En qué localidades hacen visitas a domicilio, qué días y con qué plazo? (Las zonas del lote B — Morat, Chiètres, Estavayer, Yvonand, Yverdon y Lausanne — no se publican hasta confirmarlo.)"),
    ("Otros", "Reseñas: la home muestra la nota real de Google (5,0 · 19 reseñas, 06.11.2026) con enlace a la ficha. ¿Quieren un widget oficial de reseñas?"),
    ("Otros", "Logos de aseguradoras: la plantilla tenía nombres de ejemplo («Placeholders»); se ha quitado la sección. ¿Hay convenios o logos oficiales que mostrar?"),
    ("Otros", "Destino de /online-termin-buchen/ (H1 en alemán): ¿301 a /de/ o a /reservation-en-ligne/?"),
    ("Otros", "Fotos: ver pendientes_imagenes.md."),
]
md = ["# Preguntas para el cliente", "", "Todo lo marcado como [À CONFIRMER] en las páginas, agrupado por tema. Cuando se responda, se cambia en `config/cliente.yml` / `config/zonas.yml` o en el `fr.md` de la página y se vuelve a ejecutar `python3 scripts/construir_pagina.py`.", ""]
for tema, items in preg.items():
    g = [q for t, q in GLOBAL if t == tema]
    if not items and not g:
        continue
    md += [f"## {tema}", ""] + [f"- **{q}**" for q in g]
    for url, m, f in items:
        md.append(f"- `{url}` — {m} · «{f}»")
    md.append("")
(OUT / "PREGUNTAS_CLIENTE.md").write_text("\n".join(md))

zA = [(z["nom_titre"], z["url"]) for k, z in ZON.items() if z["lote"] == "A"]
zB = [(z["nom_titre"], z["url"]) for k, z in ZON.items() if z["lote"] == "B"]
menu = ["# Menú principal y pie (URLs finales)", "", "El header y el footer no se regeneran: solo hay que cambiar estos enlaces en el Theme Builder / menú de WordPress.", "",
        "## Menú principal", "", "1. Accueil → `/`", "2. Pathologies traitées → `/pour-les-patients/` (nuevo en el menú)", "3. À propos de nous → `/a-propos-de-nous/`",
        "4. Nos zones ▾", "   - Physio Ins → `/` (no hay página de zona de Ins: la home ya posiciona «physio ins»; una página aparte la canibalizaría)"]
menu += [f"   - Physio {n} → `{u}`" for n, u in zA]
menu += [f"   - Physio {n} → `{u}` *(añadir solo cuando el cliente confirme la zona; hasta entonces, noindex y fuera del menú)*" for n, u in zB]
menu += ["5. Contact → `/contact/`", "6. Nous trouver → `/nous-trouver/`", "7. Botón «Prendre rendez-vous» → `/reservation-en-ligne/`", "",
         "## Cambios respecto al menú actual", "", "- Sustituir los enlaces que redirigen (`/mal-de-dos`, `/fitness-medica/`, `/drainage-lymphatique` sin barra, `/physiotherapie-a-domicile`) por las URLs finales: `/mal-de-dos-lombaire/`, `/medical-training-therapy-mtt/`, `/drainage-lymphatique/`, `/physiotherapeute-a-domicile/`.",
         "- Todos los botones de reserva del header/footer → `/reservation-en-ligne/` (nunca a las 5 URLs antiguas).",
         "- Selector de idioma: enlace a `/de/` (versión alemana existente) en lugar del traductor por JavaScript.", "",
         "## Pie", "", f"- NAP: {CLI['nom']} · {CLI['adresse']} · {CLI['telephone']} · WhatsApp {CLI['whatsapp']} (debe coincidir con la ficha de Google).",
         "- Enlaces: Pathologies traitées, Physio à domicile, Réservation en ligne, Contact, Nous trouver, Politique de données."]
(OUT / "menu.md").write_text("\n".join(menu) + "\n")

red = [("/reserver-maintenant/", "/reservation-en-ligne/"), ("/rendez-vous-des-maintenant/", "/reservation-en-ligne/"), ("/reserve/", "/reservation-en-ligne/"),
       ("/rendez-vous-online/", "/reservation-en-ligne/"), ("/fitness-medical/", "/medical-training-therapy-mtt/"),
       ("/douleurs-cervicales", "/douleur-cervicale-au-cou/"), ("/douleurs-genou", "/douleur-du-genou-lesions-de-la-cheville/"),
       ("/lesions-cheville", "/douleur-pied-cheville-fasciite-plantaire/"), ("/lesions-epaule", "/lesions-de-lepaule/"),
       ("/mtt-fitness-medical", "/medical-training-therapy-mtt/"), ("/physio-a-ins/", "/")]
(OUT / "redirecciones.csv").write_text("source,target,regex,code\n" + "".join(f"{a},{b},0,301\n" for a, b in red))

(OUT / "pendientes_imagenes.md").write_text("""# Imágenes pendientes

Solo se han usado imágenes que ya existen en las plantillas (`/wp-content/uploads/…`), con `alt` nuevo en francés. Para no repetir la misma foto en zonas consecutivas, las 14 zonas rotan entre las 5 fotos disponibles. Fotos que mejorarían las páginas:

| Página | Foto actual | Foto que haría falta |
|---|---|---|
| Zonas (14) | rotación de 5 fotos genéricas | Una foto por zona: el physio llegando a un domicilio de la región o un paisaje reconocible (lago de Morat, Vully, casco antiguo de Bienne…) con permiso de uso |
| /douleur-cervicale-au-cou/ | salle de traitement | Tratamiento de la nuca / cervicales |
| /douleur-pied-cheville-fasciite-plantaire/ | salle de fitness | Tratamiento o vendaje del pie y del tobillo |
| /lesions-de-lepaule/, /mal-de-dos-lombaire/ | paciente con banda elástica | Foto propia del tratamiento (la actual parece de banco de imágenes) |
| /a-propos-de-nous/ | paciente con banda elástica + fotos del equipo | Foto del equipo en el cabinet (InsGym) |
| /physiotherapeute-a-domicile/ y zonas | — | Sesión a domicilio (con consentimiento del paciente) |
| Home (vídeo) | `Physioactiva.mp4` con póster `Physio-Activa-00036.jpg` | Versión comprimida del vídeo (≤ 2-3 MB, 720p) para mejorar la carga |
""")

ORDEN = (["reservation-en-ligne", "accueil", "pour-les-patients", "mal-de-dos-lombaire", "douleur-cervicale-au-cou", "lesions-de-lepaule",
          "douleur-du-genou-lesions-de-la-cheville", "sciatique-hernie-discale", "douleur-pied-cheville-fasciite-plantaire", "douleur-de-hanche-protheses",
          "a-propos-de-nous"] + [p[0] for p in PAGINAS if p[0].startswith("physio-a-") and p[3] == "A"] + [p[0] for p in PAGINAS if p[3] == "B"])
EXISTE = {"/", "/a-propos-de-nous/", "/physio-a-sugiez/", "/physio-a-neuchatel/", "/pour-les-patients/", "/mal-de-dos-lombaire/", "/douleur-cervicale-au-cou/",
          "/lesions-de-lepaule/", "/douleur-du-genou-lesions-de-la-cheville/", "/reservation-en-ligne/"}
fichas = []
for i, slug in enumerate(ORDEN, 1):
    p = next(x for x in PAGINAS if x[0] == slug)
    url, lote = p[1], p[3]
    y = (OUT / slug / "yoast.txt").read_text()
    existe = url in EXISTE
    fichas.append(f"""<div style="page-break-before:always"></div>

## {i:02d}. `{url}` — lote {lote}{' · BORRADOR (noindex hasta confirmación)' if lote == 'B' else ''}

Archivo: `{slug}/elementor.json` · Marcadores [À CONFIRMER]: {V[slug]['a_confirmer']} (ver `{slug}/checklist.md`)

- [ ] **Copia de seguridad:** {'la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)' if existe else 'página nueva: no hace falta'}
- [ ] **Borrador de prueba:** crear página `{url.strip('/') or 'accueil'}-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de {'la página original (conserva URL e ID)' if existe else 'la página definitiva con el slug `' + url + '`'} y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`{' · **Avanzado → noindex**' if lote == 'B' else ''}
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
{y.strip()}
```
""")
pub_fichas = "\n".join(fichas)
lista_urls = "\n".join("https://physioactiva.ch" + next(x for x in PAGINAS if x[0] == s_)[1] for s_ in ORDEN)
pub = f"""# Cómo publicar el sitio en Elementor

> Antes de empezar, lee `GUIA_SEO_MONTAJE.md`: ajustes de WordPress/Yoast/Elementor, rendimiento, ficha de Google, medición y comprobaciones después del montaje.

## 0. Antes de nada (prueba)
1. Crear una página de borrador, importar `accueil/elementor.json` y `mal-de-dos-lombaire/elementor.json` (Elementor → carpeta Mis plantillas → Importar → Insertar) y comprobar en móvil y escritorio que el diseño es el de la plantilla, sin elementos rotos.
2. Configurar las páginas con **«Elementor Canvas»** (si el header y el footer vienen del Theme Builder: «Elementor Pleine largeur») y **título del tema oculto**, para que no salga un segundo H1. Los JSON ya llevan `hide_title: yes`.

## 1. Técnica (antes de publicar contenido)
- Redirecciones: plugin Redirection → Importar `redirecciones.csv`.
- /merci/, /author/, /category/ → noindex en Yoast.
- Ajustes → General → idioma «Français (Suisse)» (lang fr-CH).
- Menú y pie: ver `menu.md`.

## 2. Reserva y home
1. `/reservation-en-ligne/` (canónica) → importar `reservation-en-ligne/elementor.json`.
2. Home `/` → importar `accueil/elementor.json` (plantilla home: hero con vídeo, servicios y FAQ en HTML estático; sin traductor por JavaScript).

## 3. Hub y patologías (lote C)
`/pour-les-patients/`, `/mal-de-dos-lombaire/`, `/douleur-cervicale-au-cou/`, `/lesions-de-lepaule/`, `/douleur-du-genou-lesions-de-la-cheville/` y las nuevas `/sciatique-hernie-discale/`, `/douleur-pied-cheville-fasciite-plantaire/` y `/douleur-de-hanche-protheses/` (crear la página con ese slug). **Revisión clínica** de cada patología antes de publicarla.

## 4. Zonas del lote A y «À propos»
`/a-propos-de-nous/`, `/physio-a-sugiez/`, `/physio-a-neuchatel/` (sustituyen a las actuales), `/physio-a-la-neuveville/`, `/physio-a-avenches/`, `/physio-a-lyss/`, `/physio-a-bienne/`, `/physio-a-fribourg/`, `/physio-a-payerne/`. Resolver antes sus [À CONFIRMER] (`PREGUNTAS_CLIENTE.md`).

## 5. Zonas del lote B (solo tras la confirmación del cliente)
`/physio-a-morat/`, `/physio-a-chietres/`, `/physio-a-estavayer/`, `/physio-a-yvonand/`, `/physio-a-yverdon/`, `/physio-a-lausanne/`. Mientras no se confirmen: borrador o noindex y fuera del menú.

## Yoast
En cada página, copiar de `yoast.txt`: SEO title, meta description, slug y frase clave. El schema (JSON-LD con `Physiotherapy`, `MedicalWebPage`/`WebPage`/`AboutPage`, `FAQPage`) ya va dentro del widget: Yoast no genera FAQPage en páginas de Elementor. Evitar duplicados: en Yoast → Apariencia en el buscador → mantener el schema de Organización/WebSite de Yoast (no se solapa) y no añadir otro bloque FAQ.

## Rendimiento (recomendado, no bloquea)
Cada página repite unos 20 KB de CSS y 1,4 KB de JS en línea y carga las fuentes y Font Awesome con `@import` (bloquea el renderizado). Para pasar a la versión ligera:
1. Cargar `global/pa-styles.css` en todo el sitio: Elementor → Ajustes del sitio → CSS personalizado (o WPCode, «CSS snippet», en todo el sitio).
2. Cargar las fuentes y Font Awesome con `<link rel="preconnect">` + `<link rel="stylesheet">` en el `<head>` (WPCode → Header): Google Fonts (Poppins 500/600/700, Inter 400/500/600, `display=swap`) y Font Awesome 6.5.1 (cdnjs).
3. Cargar `global/pa-scripts.js` en el pie (WPCode → Footer, `<script>…</script>`).
4. Importar en cada página `elementor-css-global.json` en lugar de `elementor.json` (la home conserva su CSS propio porque el hero con vídeo usa reglas distintas).
`global/pa-styles.css` corrige además una errata de la plantilla (`.faq . q-ic` → `.faq .q-ic`) que dejaba sin estilo el icono «+» de la FAQ.

## Publicación manual (nada se escribe en WordPress desde aquí)
La publicación se hace a mano. Orden: técnica → reserva → home → hub y patologías → À propos y zonas del lote A → lote B tras la confirmación. **Las 301 de `redirecciones.csv` se activan después de publicar las páginas de destino.**

# Checklist por URL (imprimible)

{pub_fichas}

<div style="page-break-before:always"></div>

## Lista de URLs para la verificación por rastreo

Cuando estén publicadas, pásame esta lista (o di «verifica el rastreo») y compruebo estado 200, H1, enlaces, botones, schema e indexación:

```
{lista_urls}
```
"""
(OUT / "PUBLICAR.md").write_text(pub)

E = lambda s: H.escape(str(s))
rows = ""
for p in PAGINAS:
    slug, url, plt, lote = p[:4]
    v, r = V[slug], LOTE[slug]
    estado = ("✅ válida" if v["ok"] else "❌ " + ", ".join(v["fallos"])) + (" · borrador noindex" if lote == "B" else "")
    rows += (f"<tr><td>{lote}</td><td><a href='{slug}/preview.html'>{E(url)}</a></td><td>{E(r['h1'])}</td><td>{plt}</td><td>{E(estado)}</td>"
             f"<td class=n>{v['a_confirmer']}</td><td><a href='{slug}/elementor.json'>JSON</a> · <a href='{slug}/yoast.txt'>Yoast</a> · <a href='{slug}/checklist.md'>checklist</a></td></tr>")
(OUT / "index.html").write_text(f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Páginas Elementor · physioactiva.ch</title>
<style>:root{{--bg:#fff;--fg:#12273F;--mut:#5C7186;--line:#E4EEF5;--soft:#F4F9FD;--acc:#29A9E0}}@media(prefers-color-scheme:dark){{:root{{--bg:#0f1214;--fg:#e8eaec;--mut:#9aa4ad;--line:#2a3136;--soft:#171c1f;--acc:#3cc4bc}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif}}main{{max-width:1180px;margin:0 auto;padding:32px 16px}}h1{{font-size:1.8rem}}.tw{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:.88rem}}
th,td{{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}}th{{background:var(--soft)}}td.n{{text-align:right}}a{{color:var(--acc)}}p{{color:var(--mut)}}</style></head><body><main>
<h1>Páginas Elementor de physioactiva.ch</h1><p>{len(PAGINAS)} JSON importables (16 del menú + 9 de patologías, hub y reserva). Cada fila enlaza a la previsualización. Lote A = publicable · B = zonas en borrador (noindex hasta confirmación) · C = páginas ya redactadas de más valor SEO.</p>
<div class="tw"><table><thead><tr><th>Lote</th><th>URL (previsualización)</th><th>H1</th><th>Plantilla</th><th>Estado</th><th>[À CONFIRMER]</th><th>Archivos</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>Documentos: <a href="GUIA_SEO_MONTAJE.md">GUIA_SEO_MONTAJE.md</a> · <a href="PUBLICAR.md">PUBLICAR.md</a> · <a href="PREGUNTAS_CLIENTE.md">PREGUNTAS_CLIENTE.md</a> · <a href="menu.md">menu.md</a> · <a href="redirecciones.csv">redirecciones.csv</a> · <a href="validacion.md">validacion.md</a> · <a href="pendientes_imagenes.md">pendientes_imagenes.md</a> · CSS/JS global en <code>global/</code>.</p>
</main></body></html>""")
print("preguntas:", {k: len(v) for k, v in preg.items()})
