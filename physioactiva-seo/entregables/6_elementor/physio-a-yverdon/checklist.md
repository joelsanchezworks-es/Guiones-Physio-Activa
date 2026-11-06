# Checklist — /physio-a-yverdon/

- Lote: B · Plantilla: lombaire · Validación: OK
- Indexación: NOINDEX hasta la confirmación del cliente

## Marcadores [À CONFIRMER] (4)

- [À CONFIRMER : déplacements à Yverdon-les-Bains possibles ou non] — «Notre unique adresse se trouve à Ins (Rämismatte 21), à environ 43 km en ligne droite, et les visites à domicile à Yverdon sont [À CONFIRMER : déplacements à Yverdon-les-Bains possibles ou non].»
- [À CONFIRMER : couverture de ces localités, jours de passage et délai du premier rendez-vous] — «Une physiothérapie à Yverdon même ou dans les communes voisines, comme Grandson, Montagny-près-Yverdon, Cheseaux-Noréaz ou Treycovagnes, reste donc [À CONFIRMER : couverture de ces localités, jours de passage et délai du premier rendez-vous].»
- [À CONFIRMER : drainage à domicile dans la région d'Yverdon] — «Comme les séances peuvent être rapprochées, les 43 km jusqu'à Ins pèsent lourd : nous vous dirons franchement si un suivi est réaliste [À CONFIRMER : drainage à domicile dans la région d'Yverdon].»
- [À CONFIRMER : déplacements dans la région d'Yverdon et conditions] — «La réponse est [À CONFIRMER : déplacements dans la région d'Yverdon et conditions].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/physio-a-yverdon/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`. Avanzado → noindex.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Physio à Yverdon-les-Bains : au cabinet d'Ins ou à domicile |
| 4 H3 de valor bajo el hero | no | omitida |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | sí |  |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | sí |  |
| FAQ (8-10) | no | 4 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | no | omitida |

- receta: ciudad en 3 H2 · FAQ 4 · CTA reserva 3 / tel 2 / WhatsApp 2 · palabras visibles 875
