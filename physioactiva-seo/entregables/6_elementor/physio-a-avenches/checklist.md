# Checklist — /physio-a-avenches/

- Lote: A · Plantilla: lombaire · Validación: OK
- Indexación: index, follow

## Marcadores [À CONFIRMER] (3)

- [À CONFIRMER : déplacements à Avenches] — «Selon votre situation, les séances de physio ont lieu au cabinet ou à votre domicile [À CONFIRMER : déplacements à Avenches].»
- [À CONFIRMER : villages desservis autour d'Avenches et jours de passage] — «Salavaux, au bord du lac de Morat, est aussi proche du Vully ; pour les autres villages, la possibilité d'un passage à domicile reste à confirmer [À CONFIRMER : villages desservis autour d'Avenches et jours de passage].»
- [À CONFIRMER : Faoug, Domdidier, Donatyre, Oleyres] — «Ces villages entourent Avenches, mais nous devons encore confirmer s'ils font partie de notre zone à domicile [À CONFIRMER : Faoug, Domdidier, Donatyre, Oleyres].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/physio-a-avenches/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Physiothérapie à Avenches : au cabinet d'Ins ou à domicile |
| 4 H3 de valor bajo el hero | no | omitida |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | sí |  |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | sí |  |
| FAQ (8-10) | no | 4 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | no | omitida |

- receta: ciudad en 3 H2 · FAQ 4 · CTA reserva 3 / tel 2 / WhatsApp 2 · palabras visibles 670
