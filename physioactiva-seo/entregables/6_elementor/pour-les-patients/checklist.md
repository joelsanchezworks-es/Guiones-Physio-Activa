# Checklist — /pour-les-patients/

- Lote: C · Plantilla: lombaire · Validación: OK
- Indexación: index, follow

## Marcadores [À CONFIRMER] (0)


## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/pour-les-patients/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Pathologies traitées en physiothérapie : où avez-vous mal ? |
| 4 H3 de valor bajo el hero | sí |  |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | no | no aplica a esta página |
| Proceso en pasos (H2 + H3) + CTA intermedio | sí |  |
| Reembolso y coste | no | omitida |
| FAQ (8-10) | no | 5 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | sí |  |

- receta: ciudad en 2 H2 · FAQ 5 · CTA reserva 3 / tel 3 / WhatsApp 3 · palabras visibles 835
