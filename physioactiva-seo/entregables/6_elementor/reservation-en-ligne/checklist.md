# Checklist — /reservation-en-ligne/

- Lote: C · Plantilla: lombaire · Validación: OK
- Indexación: index, follow

## Marcadores [À CONFIRMER] (3)

- [À CONFIRMER] — «Horaires : du lundi au vendredi, de 8 h 30 à 19 h 30 [À CONFIRMER].»
- [À CONFIRMER] — «Délai d'annulation : [À CONFIRMER].»
- [À CONFIRMER] — «Durée d'une séance : [À CONFIRMER].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/reservation-en-ligne/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Prendre rendez-vous chez votre physio à Ins |
| 4 H3 de valor bajo el hero | sí |  |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | no | no aplica a esta página |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | sí |  |
| FAQ (8-10) | sí | 8 preguntas |
| CTA final en pregunta con la ciudad | sí |  |

- receta: ciudad en 3 H2 · FAQ 8 · CTA reserva 3 / tel 2 / WhatsApp 2 · palabras visibles 767
