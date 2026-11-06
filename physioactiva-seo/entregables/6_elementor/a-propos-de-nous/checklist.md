# Checklist — /a-propos-de-nous/

- Lote: A · Plantilla: lombaire · Validación: OK
- Indexación: index, follow

## Marcadores [À CONFIRMER] (9)

- [À CONFIRMER : titre et formation] — «[À CONFIRMER : titre et formation]»
- [À CONFIRMER : titre, formation et numéro d'enregistrement NAREG / RCC] — «Francisco est physiothérapeute [À CONFIRMER : titre, formation et numéro d'enregistrement NAREG / RCC].»
- [À CONFIRMER] — «Il parle français et espagnol, ainsi que portugais [À CONFIRMER].»
- [À CONFIRMER : titre et formation] — «[À CONFIRMER : titre et formation]»
- [À CONFIRMER : titre, formation et numéro d'enregistrement NAREG / RCC] — «Lucile est physiothérapeute [À CONFIRMER : titre, formation et numéro d'enregistrement NAREG / RCC].»
- [À CONFIRMER] — «Elle parle français et espagnol, ainsi que portugais [À CONFIRMER].»
- [À CONFIRMER : lun–ven 8h30–19h30 ou jusqu'à 20h] — «Horaires : [À CONFIRMER : lun–ven 8h30–19h30 ou jusqu'à 20h].»
- [À CONFIRMER : titres, formations, enregistrement professionnel] — «Leurs titres et formations sont précisés ici : [À CONFIRMER : titres, formations, enregistrement professionnel].»
- [À CONFIRMER] — «Le portugais est [À CONFIRMER].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/a-propos-de-nous/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Vos physiothérapeutes à Ins : l'équipe Physio Activa |
| 4 H3 de valor bajo el hero | no | omitida |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | sí |  |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | no | omitida |
| FAQ (8-10) | no | 4 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | no | omitida |

- receta: ciudad en 1 H2 · FAQ 4 · CTA reserva 5 / tel 2 / WhatsApp 2 · palabras visibles 784
