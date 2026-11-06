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

## Publicación manual (nada se escribe en WordPress desde aquí)
La publicación se hace a mano. Orden: técnica → reserva → home → hub y patologías → À propos y zonas del lote A → lote B tras la confirmación. **Las 301 de `redirecciones.csv` se activan después de publicar las páginas de destino.**

# Checklist por URL (imprimible)

<div style="page-break-before:always"></div>

## 01. `/reservation-en-ligne/` — lote C

Archivo: `reservation-en-ligne/elementor.json` · Marcadores [À CONFIRMER]: 2 (ver `reservation-en-ligne/checklist.md`)

- [ ] **Copia de seguridad:** la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)
- [ ] **Borrador de prueba:** crear página `reservation-en-ligne-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página original (conserva URL e ID) y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (54/60): Rendez-vous physio à Ins : réservation | Physio Activa
Meta description (142/155): Prenez rendez-vous chez votre physio à Ins : réservation en ligne OneDoc, par téléphone ou WhatsApp. Au cabinet ou à domicile dans le Seeland.
Slug: /reservation-en-ligne/
Focus keyphrase: rendez-vous physio ins
H1: Prendre rendez-vous chez votre physio à Ins
Indexación: index, follow
Canonical: https://physioactiva.ch/reservation-en-ligne/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 02. `/` — lote A

Archivo: `accueil/elementor.json` · Marcadores [À CONFIRMER]: 6 (ver `accueil/checklist.md`)

- [ ] **Copia de seguridad:** la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)
- [ ] **Borrador de prueba:** crear página `accueil-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página original (conserva URL e ID) y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (49/60): Physio à Ins (Anet) et à domicile | Physio Activa
Meta description (141/155): Physio à Ins (Anet) et physiothérapie à domicile dans le Seeland et les Trois-Lacs. Remboursé sur ordonnance (LAMal, LAA). Réservez en ligne.
Slug: /
Focus keyphrase: physio à Ins
H1: Physio à Ins (Anet)
Indexación: index, follow
Canonical: https://physioactiva.ch/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 03. `/pour-les-patients/` — lote C

Archivo: `pour-les-patients/elementor.json` · Marcadores [À CONFIRMER]: 0 (ver `pour-les-patients/checklist.md`)

- [ ] **Copia de seguridad:** la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)
- [ ] **Borrador de prueba:** crear página `pour-les-patients-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página original (conserva URL e ID) y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (60/60): Pathologies traitées en physiothérapie à Ins | Physio Activa
Meta description (145/155): Pathologies traitées en physiothérapie à Ins : dos, sciatique, cou, épaule, genou, pied, hanche, plancher pelvien, ATM. Au cabinet ou à domicile.
Slug: /pour-les-patients/
Focus keyphrase: pathologies physiothérapie
H1: Pathologies traitées en physiothérapie : où avez-vous mal ?
Indexación: index, follow
Canonical: https://physioactiva.ch/pour-les-patients/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 04. `/mal-de-dos-lombaire/` — lote C

Archivo: `mal-de-dos-lombaire/elementor.json` · Marcadores [À CONFIRMER]: 1 (ver `mal-de-dos-lombaire/checklist.md`)

- [ ] **Copia de seguridad:** la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)
- [ ] **Borrador de prueba:** crear página `mal-de-dos-lombaire-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página original (conserva URL e ID) y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (54/60): Lombalgie et mal de dos : physio à Ins | Physio Activa
Meta description (142/155): Lombalgie, lumbago, douleur en bas du dos : causes, signes d'alarme et physiothérapie à Ins ou à domicile dans le Seeland. Prenez rendez-vous.
Slug: /mal-de-dos-lombaire/
Focus keyphrase: lombalgie
H1: Lombalgie et mal de dos : physio à Ins
Indexación: index, follow
Canonical: https://physioactiva.ch/mal-de-dos-lombaire/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 05. `/douleur-cervicale-au-cou/` — lote C

Archivo: `douleur-cervicale-au-cou/elementor.json` · Marcadores [À CONFIRMER]: 1 (ver `douleur-cervicale-au-cou/checklist.md`)

- [ ] **Copia de seguridad:** la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)
- [ ] **Borrador de prueba:** crear página `douleur-cervicale-au-cou-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página original (conserva URL e ID) y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (56/60): Cervicalgie : physio à Ins et à domicile | Physio Activa
Meta description (148/155): Cervicalgie, douleur de nuque, torticolis ou coup du lapin ? Physiothérapie à Ins et à domicile dans le Seeland, sur ordonnance. Prenez rendez-vous.
Slug: /douleur-cervicale-au-cou/
Focus keyphrase: cervicalgie
H1: Cervicalgie et douleur cervicale : physio à Ins
Indexación: index, follow
Canonical: https://physioactiva.ch/douleur-cervicale-au-cou/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 06. `/lesions-de-lepaule/` — lote C

Archivo: `lesions-de-lepaule/elementor.json` · Marcadores [À CONFIRMER]: 1 (ver `lesions-de-lepaule/checklist.md`)

- [ ] **Copia de seguridad:** la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)
- [ ] **Borrador de prueba:** crear página `lesions-de-lepaule-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página original (conserva URL e ID) y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (51/60): Coiffe des rotateurs : physio à Ins | Physio Activa
Meta description (137/155): Coiffe des rotateurs, tendinite ou épaule gelée ? Physiothérapie à Ins et à domicile dans le Seeland, sur ordonnance. Prenez rendez-vous.
Slug: /lesions-de-lepaule/
Focus keyphrase: coiffe des rotateurs
H1: Coiffe des rotateurs et douleur à l'épaule : physio à Ins
Indexación: index, follow
Canonical: https://physioactiva.ch/lesions-de-lepaule/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 07. `/douleur-du-genou-lesions-de-la-cheville/` — lote C

Archivo: `douleur-du-genou-lesions-de-la-cheville/elementor.json` · Marcadores [À CONFIRMER]: 0 (ver `douleur-du-genou-lesions-de-la-cheville/checklist.md`)

- [ ] **Copia de seguridad:** la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)
- [ ] **Borrador de prueba:** crear página `douleur-du-genou-lesions-de-la-cheville-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página original (conserva URL e ID) y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (59/60): Ménisque et douleur du genou : physio à Ins | Physio Activa
Meta description (148/155): Ménisque, ligament croisé, arthrose du genou ou prothèse : physiothérapie du genou à Ins et à domicile dans le Seeland. Prenez rendez-vous en ligne.
Slug: /douleur-du-genou-lesions-de-la-cheville/
Focus keyphrase: ménisque
H1: Douleur du genou et ménisque : physio à Ins
Indexación: index, follow
Canonical: https://physioactiva.ch/douleur-du-genou-lesions-de-la-cheville/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 08. `/sciatique-hernie-discale/` — lote C

Archivo: `sciatique-hernie-discale/elementor.json` · Marcadores [À CONFIRMER]: 1 (ver `sciatique-hernie-discale/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `sciatique-hernie-discale-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/sciatique-hernie-discale/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (58/60): Sciatique et hernie discale : physio à Ins | Physio Activa
Meta description (147/155): Sciatique, douleur du nerf sciatique, hernie discale L5-S1 : symptômes, signes d'urgence et physiothérapie à Ins ou à domicile. Prenez rendez-vous.
Slug: /sciatique-hernie-discale/
Focus keyphrase: sciatique
H1: Sciatique et hernie discale : physio à Ins
Indexación: index, follow
Canonical: https://physioactiva.ch/sciatique-hernie-discale/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 09. `/douleur-pied-cheville-fasciite-plantaire/` — lote C

Archivo: `douleur-pied-cheville-fasciite-plantaire/elementor.json` · Marcadores [À CONFIRMER]: 0 (ver `douleur-pied-cheville-fasciite-plantaire/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `douleur-pied-cheville-fasciite-plantaire-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/douleur-pied-cheville-fasciite-plantaire/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (53/60): Fasciite plantaire et douleur au talon : physio à Ins
Meta description (150/155): Fasciite plantaire, périostite, entorse de la cheville ou tendinite d'Achille : physiothérapie à Ins et à domicile dans le Seeland. Réservez en ligne.
Slug: /douleur-pied-cheville-fasciite-plantaire/
Focus keyphrase: fasciite plantaire
H1: Fasciite plantaire et douleur du pied : physio à Ins
Indexación: index, follow
Canonical: https://physioactiva.ch/douleur-pied-cheville-fasciite-plantaire/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 10. `/douleur-de-hanche-protheses/` — lote C

Archivo: `douleur-de-hanche-protheses/elementor.json` · Marcadores [À CONFIRMER]: 2 (ver `douleur-de-hanche-protheses/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `douleur-de-hanche-protheses-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/douleur-de-hanche-protheses/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (54/60): Prothèse de hanche : rééducation à Ins | Physio Activa
Meta description (149/155): Prothèse de hanche, arthrose ou douleur de hanche : rééducation en physiothérapie au cabinet à Ins ou à domicile dans le Seeland. Prenez rendez-vous.
Slug: /douleur-de-hanche-protheses/
Focus keyphrase: prothèse de hanche
H1: Prothèse de hanche et douleur de hanche : votre physio à Ins
Indexación: index, follow
Canonical: https://physioactiva.ch/douleur-de-hanche-protheses/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 11. `/a-propos-de-nous/` — lote A

Archivo: `a-propos-de-nous/elementor.json` · Marcadores [À CONFIRMER]: 9 (ver `a-propos-de-nous/checklist.md`)

- [ ] **Copia de seguridad:** la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)
- [ ] **Borrador de prueba:** crear página `a-propos-de-nous-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página original (conserva URL e ID) y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (54/60): Physiothérapeutes à Ins : notre équipe | Physio Activa
Meta description (147/155): Découvrez Physio Activa, physiothérapeutes à Ins (InsGym) : bilan, traitement actif, domicile dans le Seeland. Sur ordonnance LAMal, LAA. Réservez.
Slug: /a-propos-de-nous/
Focus keyphrase: physiothérapeutes à Ins
H1: Vos physiothérapeutes à Ins : l'équipe Physio Activa
Indexación: index, follow
Canonical: https://physioactiva.ch/a-propos-de-nous/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 12. `/physio-a-sugiez/` — lote A

Archivo: `physio-a-sugiez/elementor.json` · Marcadores [À CONFIRMER]: 4 (ver `physio-a-sugiez/checklist.md`)

- [ ] **Copia de seguridad:** la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)
- [ ] **Borrador de prueba:** crear página `physio-a-sugiez-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página original (conserva URL e ID) y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (58/60): Physio à Sugiez et Vully – domicile ou Ins | Physio Activa
Meta description (150/155): Physio dans le Vully, à Sugiez et alentour : au cabinet d'Ins ou à domicile, remboursé sur ordonnance (LAMal, LAA). Réservez en ligne ou par WhatsApp.
Slug: /physio-a-sugiez/
Focus keyphrase: physio vully
H1: Physio à Sugiez et dans le Vully : au cabinet d'Ins ou à domicile
Indexación: index, follow
Canonical: https://physioactiva.ch/physio-a-sugiez/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 13. `/physio-a-neuchatel/` — lote A

Archivo: `physio-a-neuchatel/elementor.json` · Marcadores [À CONFIRMER]: 5 (ver `physio-a-neuchatel/checklist.md`)

- [ ] **Copia de seguridad:** la página ya existe → Elementor → Guardar como plantilla → Exportar (guardar el .json con fecha)
- [ ] **Borrador de prueba:** crear página `physio-a-neuchatel-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página original (conserva URL e ID) y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (56/60): Physio à Neuchâtel – à domicile ou à Ins | Physio Activa
Meta description (151/155): Physio à Neuchâtel : physiothérapie à domicile ou au cabinet d'Ins, drainage lymphatique, remboursement sur ordonnance (LAMal, LAA). Réservez en ligne.
Slug: /physio-a-neuchatel/
Focus keyphrase: physio neuchâtel
H1: Physio à Neuchâtel : au cabinet d'Ins ou à domicile
Indexación: index, follow
Canonical: https://physioactiva.ch/physio-a-neuchatel/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 14. `/physio-a-la-neuveville/` — lote A

Archivo: `physio-a-la-neuveville/elementor.json` · Marcadores [À CONFIRMER]: 3 (ver `physio-a-la-neuveville/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-la-neuveville-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-la-neuveville/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (56/60): Physio à La Neuveville – domicile ou Ins | Physio Activa
Meta description (153/155): Physio pour La Neuveville et le Plateau de Diesse : séances à domicile ou au cabinet d'Ins, remboursées sur ordonnance. Rendez-vous en ligne ou WhatsApp.
Slug: /physio-a-la-neuveville/
Focus keyphrase: physio la neuveville
H1: Physio à La Neuveville : au cabinet d'Ins ou à domicile
Indexación: index, follow
Canonical: https://physioactiva.ch/physio-a-la-neuveville/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 15. `/physio-a-avenches/` — lote A

Archivo: `physio-a-avenches/elementor.json` · Marcadores [À CONFIRMER]: 3 (ver `physio-a-avenches/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-avenches-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-avenches/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (59/60): Physiothérapie à Avenches – domicile ou Ins | Physio Activa
Meta description (151/155): Physiothérapie à Avenches et dans la Broye-Vully : à domicile ou au cabinet d'Ins, remboursée sur ordonnance (LAMal, LAA). Prenez rendez-vous en ligne.
Slug: /physio-a-avenches/
Focus keyphrase: physiothérapie avenches
H1: Physiothérapie à Avenches : au cabinet d'Ins ou à domicile
Indexación: index, follow
Canonical: https://physioactiva.ch/physio-a-avenches/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 16. `/physio-a-lyss/` — lote A

Archivo: `physio-a-lyss/elementor.json` · Marcadores [À CONFIRMER]: 8 (ver `physio-a-lyss/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-lyss-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-lyss/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (51/60): Physio à Lyss – à domicile ou à Ins | Physio Activa
Meta description (137/155): Physio à Lyss : séances en français au cabinet d'Ins ou à domicile, remboursées sur prescription (LAMal, LAA, AI, AM). Réservez en ligne.
Slug: /physio-a-lyss/
Focus keyphrase: physio lyss
H1: Physio à Lyss : au cabinet d'Ins ou à domicile
Indexación: index, follow
Canonical: https://physioactiva.ch/physio-a-lyss/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 17. `/physio-a-bienne/` — lote A

Archivo: `physio-a-bienne/elementor.json` · Marcadores [À CONFIRMER]: 5 (ver `physio-a-bienne/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-bienne-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-bienne/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (60/60): Physio à Bienne (Biel) – à domicile ou à Ins | Physio Activa
Meta description (149/155): Physiothérapeute pour Bienne (Biel) et environs : cabinet à Ins ou séances à domicile, remboursées sur ordonnance. Réservez en ligne ou par WhatsApp.
Slug: /physio-a-bienne/
Focus keyphrase: physio biel
H1: Physio à Bienne (Biel) : au cabinet d'Ins ou à domicile
Indexación: index, follow
Canonical: https://physioactiva.ch/physio-a-bienne/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 18. `/physio-a-fribourg/` — lote A

Archivo: `physio-a-fribourg/elementor.json` · Marcadores [À CONFIRMER]: 6 (ver `physio-a-fribourg/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-fribourg-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-fribourg/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (59/60): Physiothérapie à Fribourg – domicile ou Ins | Physio Activa
Meta description (151/155): Physiothérapie à Fribourg : physio à domicile ou au cabinet d'Ins, drainage lymphatique, remboursée sur ordonnance (LAMal, LAA, AI). Réservez en ligne.
Slug: /physio-a-fribourg/
Focus keyphrase: physiothérapie fribourg
H1: Physiothérapie à Fribourg : au cabinet d'Ins ou à domicile
Indexación: index, follow
Canonical: https://physioactiva.ch/physio-a-fribourg/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 19. `/physio-a-payerne/` — lote A

Archivo: `physio-a-payerne/elementor.json` · Marcadores [À CONFIRMER]: 6 (ver `physio-a-payerne/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-payerne-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-payerne/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt`
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (54/60): Physio à Payerne – à domicile ou à Ins | Physio Activa
Meta description (151/155): Physio à Payerne et dans la Broye : à domicile ou au cabinet d'Ins, séances remboursées sur prescription médicale. Réservez votre rendez-vous en ligne.
Slug: /physio-a-payerne/
Focus keyphrase: physio payerne
H1: Physio à Payerne : au cabinet d'Ins ou à domicile
Indexación: index, follow
Canonical: https://physioactiva.ch/physio-a-payerne/
Estado: publicable tras revisión
```

<div style="page-break-before:always"></div>

## 20. `/physio-a-morat/` — lote B · BORRADOR (noindex hasta confirmación)

Archivo: `physio-a-morat/elementor.json` · Marcadores [À CONFIRMER]: 4 (ver `physio-a-morat/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-morat-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-morat/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt` · **Avanzado → noindex**
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (57/60): Physio à Morat (Murten) – domicile ou Ins | Physio Activa
Meta description (133/155): Physio à Morat (Murten) : séances en français au cabinet d'Ins, à 8,7 km, ou à domicile. Remboursé sur ordonnance. Réservez en ligne.
Slug: /physio-a-morat/
Focus keyphrase: physio morat
H1: Physio à Morat (Murten) : au cabinet d'Ins ou à domicile
Indexación: NOINDEX hasta la confirmación del cliente (Yoast → Avanzado → ¿Permitir que los motores muestren esta página? = No)
Canonical: https://physioactiva.ch/physio-a-morat/
Estado: borrador — noindex hasta confirmación
```

<div style="page-break-before:always"></div>

## 21. `/physio-a-chietres/` — lote B · BORRADOR (noindex hasta confirmación)

Archivo: `physio-a-chietres/elementor.json` · Marcadores [À CONFIRMER]: 5 (ver `physio-a-chietres/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-chietres-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-chietres/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt` · **Avanzado → noindex**
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (45/60): Physio à Chiètres (Kerzers) – domicile ou Ins
Meta description (137/155): Physio à Chiètres (Kerzers) : cabinet à Ins, à 7,6 km, ou séances à domicile, en français. Remboursé sur prescription. Réservez en ligne.
Slug: /physio-a-chietres/
Focus keyphrase: physio chiètres
H1: Physio à Chiètres (Kerzers) : au cabinet d'Ins ou à domicile
Indexación: NOINDEX hasta la confirmación del cliente (Yoast → Avanzado → ¿Permitir que los motores muestren esta página? = No)
Canonical: https://physioactiva.ch/physio-a-chietres/
Estado: borrador — noindex hasta confirmación
```

<div style="page-break-before:always"></div>

## 22. `/physio-a-estavayer/` — lote B · BORRADOR (noindex hasta confirmación)

Archivo: `physio-a-estavayer/elementor.json` · Marcadores [À CONFIRMER]: 6 (ver `physio-a-estavayer/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-estavayer-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-estavayer/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt` · **Avanzado → noindex**
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (43/60): Physio à Estavayer-le-Lac – domicile ou Ins
Meta description (139/155): Physio à Estavayer-le-Lac : cabinet à Ins (26,4 km) ou séances à domicile selon disponibilité. Remboursé sur ordonnance. Réservez en ligne.
Slug: /physio-a-estavayer/
Focus keyphrase: physio estavayer
H1: Physio à Estavayer-le-Lac : au cabinet d'Ins ou à domicile
Indexación: NOINDEX hasta la confirmación del cliente (Yoast → Avanzado → ¿Permitir que los motores muestren esta página? = No)
Canonical: https://physioactiva.ch/physio-a-estavayer/
Estado: borrador — noindex hasta confirmación
```

<div style="page-break-before:always"></div>

## 23. `/physio-a-yvonand/` — lote B · BORRADOR (noindex hasta confirmación)

Archivo: `physio-a-yvonand/elementor.json` · Marcadores [À CONFIRMER]: 4 (ver `physio-a-yvonand/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-yvonand-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-yvonand/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt` · **Avanzado → noindex**
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (54/60): Physio à Yvonand – à domicile ou à Ins | Physio Activa
Meta description (141/155): Physio à Yvonand (VD) : rééducation au cabinet d'Ins ou à domicile selon disponibilité. Remboursée sur prescription LAMal. Réservez en ligne.
Slug: /physio-a-yvonand/
Focus keyphrase: physio yvonand
H1: Physio à Yvonand : au cabinet d'Ins ou à domicile
Indexación: NOINDEX hasta la confirmación del cliente (Yoast → Avanzado → ¿Permitir que los motores muestren esta página? = No)
Canonical: https://physioactiva.ch/physio-a-yvonand/
Estado: borrador — noindex hasta confirmación
```

<div style="page-break-before:always"></div>

## 24. `/physio-a-yverdon/` — lote B · BORRADOR (noindex hasta confirmación)

Archivo: `physio-a-yverdon/elementor.json` · Marcadores [À CONFIRMER]: 4 (ver `physio-a-yverdon/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-yverdon-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-yverdon/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt` · **Avanzado → noindex**
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (54/60): Physio à Yverdon – à domicile ou à Ins | Physio Activa
Meta description (149/155): Physio à Yverdon : pas de cabinet sur place, nous recevons à Ins (43 km) ; domicile à confirmer. Remboursé sur ordonnance LAMal, LAA. Contactez-nous.
Slug: /physio-a-yverdon/
Focus keyphrase: physio yverdon
H1: Physio à Yverdon-les-Bains : au cabinet d'Ins ou à domicile
Indexación: NOINDEX hasta la confirmación del cliente (Yoast → Avanzado → ¿Permitir que los motores muestren esta página? = No)
Canonical: https://physioactiva.ch/physio-a-yverdon/
Estado: borrador — noindex hasta confirmación
```

<div style="page-break-before:always"></div>

## 25. `/physio-a-lausanne/` — lote B · BORRADOR (noindex hasta confirmación)

Archivo: `physio-a-lausanne/elementor.json` · Marcadores [À CONFIRMER]: 6 (ver `physio-a-lausanne/checklist.md`)

- [ ] **Copia de seguridad:** página nueva: no hace falta
- [ ] **Borrador de prueba:** crear página `physio-a-lausanne-v2` en borrador → Elementor → Plantillas → Importar `elementor.json` → Insertar
- [ ] Plantilla de página «Elementor Canvas» (o «Pleine largeur» si el header/footer vienen del Theme Builder) y **título del tema oculto**
- [ ] Revisar en **móvil y escritorio**: diseño de la plantilla, sin elementos rotos, FAQ abre y cierra, botones funcionan
- [ ] Sustituir el contenido de la página definitiva con el slug `/physio-a-lausanne/` y borrar el borrador `-v2`
- [ ] **Yoast:** pegar title, meta, slug y frase clave de `yoast.txt` · **Avanzado → noindex**
- [ ] Verificación tras publicar: **200** · **un solo H1** · **ningún botón en `#`** · **título del tema oculto** · schema válido en validator.schema.org

```
SEO title (55/60): Physio à Lausanne – à domicile ou à Ins | Physio Activa
Meta description (144/155): Physio à Lausanne ? Notre physiothérapeute vous reçoit à Ins, à 65 km ; domicile à confirmer. Remboursé sur ordonnance LAMal, LAA. Appelez-nous.
Slug: /physio-a-lausanne/
Focus keyphrase: physio lausanne
H1: Physio à Lausanne : au cabinet d'Ins ou à domicile
Indexación: NOINDEX hasta la confirmación del cliente (Yoast → Avanzado → ¿Permitir que los motores muestren esta página? = No)
Canonical: https://physioactiva.ch/physio-a-lausanne/
Estado: borrador — noindex hasta confirmación
```


<div style="page-break-before:always"></div>

## Lista de URLs para la verificación por rastreo

Cuando estén publicadas, pásame esta lista (o di «verifica el rastreo») y compruebo estado 200, H1, enlaces, botones, schema e indexación:

```
https://physioactiva.ch/reservation-en-ligne/
https://physioactiva.ch/
https://physioactiva.ch/pour-les-patients/
https://physioactiva.ch/mal-de-dos-lombaire/
https://physioactiva.ch/douleur-cervicale-au-cou/
https://physioactiva.ch/lesions-de-lepaule/
https://physioactiva.ch/douleur-du-genou-lesions-de-la-cheville/
https://physioactiva.ch/sciatique-hernie-discale/
https://physioactiva.ch/douleur-pied-cheville-fasciite-plantaire/
https://physioactiva.ch/douleur-de-hanche-protheses/
https://physioactiva.ch/a-propos-de-nous/
https://physioactiva.ch/physio-a-sugiez/
https://physioactiva.ch/physio-a-neuchatel/
https://physioactiva.ch/physio-a-la-neuveville/
https://physioactiva.ch/physio-a-avenches/
https://physioactiva.ch/physio-a-lyss/
https://physioactiva.ch/physio-a-bienne/
https://physioactiva.ch/physio-a-fribourg/
https://physioactiva.ch/physio-a-payerne/
https://physioactiva.ch/physio-a-morat/
https://physioactiva.ch/physio-a-chietres/
https://physioactiva.ch/physio-a-estavayer/
https://physioactiva.ch/physio-a-yvonand/
https://physioactiva.ch/physio-a-yverdon/
https://physioactiva.ch/physio-a-lausanne/
```
