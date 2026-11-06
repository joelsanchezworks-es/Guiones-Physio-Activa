# Checklist — /physio-a-chietres/

- Lote: B · Plantilla: lombaire · Validación: OK
- Indexación: NOINDEX hasta la confirmación del cliente

## Marcadores [À CONFIRMER] (5)

- [À CONFIRMER : visites à domicile à Chiètres] — «Nous vous recevons au cabinet et pouvons aussi nous déplacer chez vous [À CONFIRMER : visites à domicile à Chiètres].»
- [À CONFIRMER : localités couvertes et jours de passage] — «Autour de Chiètres, les localités concernées seraient Fräschels, Ried bei Kerzers, Galmiz et Agriswil [À CONFIRMER : localités couvertes et jours de passage].»
- [À CONFIRMER : séances possibles en allemand ?] — «Chez Physio Activa, les séances se déroulent en français ou en espagnol : une solution pratique pour les familles francophones ou hispanophones installées à Kerzers et dans les villages voisins [À CONFIRMER : séances possibles en allemand ?].»
- [À CONFIRMER : déplacements à Chiètres et délai pour un premier rendez-vous] — «C'est précisément le type de situation où le domicile est utile [À CONFIRMER : déplacements à Chiètres et délai pour un premier rendez-vous].»
- [À CONFIRMER : liste des localités et jours de passage] — «Ce sont des villages voisins de Chiètres que nous souhaitons inclure dans nos tournées [À CONFIRMER : liste des localités et jours de passage].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/physio-a-chietres/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`. Avanzado → noindex.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Physio à Chiètres (Kerzers) : au cabinet d'Ins ou à domicile |
| 4 H3 de valor bajo el hero | no | omitida |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | sí |  |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | sí |  |
| FAQ (8-10) | no | 4 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | no | omitida |

- receta: ciudad en 4 H2 · FAQ 4 · CTA reserva 3 / tel 2 / WhatsApp 2 · palabras visibles 659
