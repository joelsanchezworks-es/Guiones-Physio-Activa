# Checklist — /physio-a-morat/

- Lote: B · Plantilla: lombaire · Validación: OK
- Indexación: NOINDEX hasta la confirmación del cliente

## Marcadores [À CONFIRMER] (4)

- [À CONFIRMER : déplacements à Morat] — «Vous habitez Morat et vous cherchez un physiothérapeute qui vous reçoit en français ? Le cabinet Physio Activa se trouve à Ins, à environ 8,7 km en ligne droite de la vieille ville, et des séances à domicile sont possibles selon les disponibilités [À CONFIRMER»
- [À CONFIRMER : localités desservies et jours de passage] — «Dans ce cas, nous pouvons envisager de venir chez vous à Morat, mais aussi à Meyriez, Muntelier, Greng, Courgevaux ou Galmiz [À CONFIRMER : localités desservies et jours de passage].»
- [À CONFIRMER : domicile à Morat et délai pour une première séance] — «Oui, dès que vous avez une ordonnance de physiothérapie, nous pouvons prendre le relais au cabinet ou, si c'est nécessaire, à domicile [À CONFIRMER : domicile à Morat et délai pour une première séance].»
- [À CONFIRMER : liste définitive des localités et jours de passage] — «Ces localités voisines de Morat font partie de la zone que nous envisageons de couvrir à domicile [À CONFIRMER : liste définitive des localités et jours de passage].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/physio-a-morat/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`. Avanzado → noindex.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Physio à Morat (Murten) : au cabinet d'Ins ou à domicile |
| 4 H3 de valor bajo el hero | no | omitida |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | sí |  |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | sí |  |
| FAQ (8-10) | no | 4 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | no | omitida |

- receta: ciudad en 4 H2 · FAQ 4 · CTA reserva 3 / tel 2 / WhatsApp 2 · palabras visibles 705
