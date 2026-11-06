# Cómo publicar el sitio en Elementor

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
