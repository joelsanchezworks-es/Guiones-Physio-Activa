# Checklist — /physio-a-estavayer/

- Lote: B · Plantilla: lombaire · Validación: ERRORES: receta: ciudad nunca en un H3
- Indexación: NOINDEX hasta la confirmación del cliente

## Marcadores [À CONFIRMER] (6)

- [À CONFIRMER : domicile à Estavayer] — «Physio Activa vous accueille au cabinet d'Ins et étudie la possibilité de séances à domicile dans la Broye [À CONFIRMER : domicile à Estavayer].»
- [À CONFIRMER : couverture de ces localités et jours de passage] — «Pour Estavayer, cela pourrait concerner aussi Font, Cheyres-Châbles, Sévaz et Les Montets [À CONFIRMER : couverture de ces localités et jours de passage].»
- [À CONFIRMER : drainage à domicile dans la Broye fribourgeoise] — «Vu les 26,4 km qui séparent Estavayer du cabinet, il se fera en principe à Ins, le domicile restant [À CONFIRMER : drainage à domicile dans la Broye fribourgeoise].»
- [À CONFIRMER : domicile à Estavayer] — «Si ce n'est pas le cas, le domicile peut être une option [À CONFIRMER : domicile à Estavayer].»
- [À CONFIRMER : délai pour une première séance] — «Avec l'ordonnance de physiothérapie remise par le médecin, nous pouvons organiser la suite de votre rééducation [À CONFIRMER : délai pour une première séance].»
- [À CONFIRMER : localités desservies et jours de passage] — «Ces villages proches d'Estavayer pourraient être regroupés avec les visites à domicile du secteur [À CONFIRMER : localités desservies et jours de passage].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/physio-a-estavayer/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`. Avanzado → noindex.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Physio à Estavayer-le-Lac : au cabinet d'Ins ou à domicile |
| 4 H3 de valor bajo el hero | no | omitida |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | sí |  |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | sí |  |
| FAQ (8-10) | no | 4 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | no | omitida |

- receta: ciudad en 4 H2 · FAQ 4 · CTA reserva 3 / tel 2 / WhatsApp 2 · palabras visibles 781
