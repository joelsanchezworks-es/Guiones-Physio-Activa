# Checklist — /physio-a-bienne/

- Lote: A · Plantilla: lombaire · Validación: ERRORES: receta: ciudad nunca en un H3
- Indexación: index, follow

## Marcadores [À CONFIRMER] (5)

- [À CONFIRMER : domicile à Bienne] — «Selon votre situation, une prise en charge à domicile peut aussi être organisée [À CONFIRMER : domicile à Bienne].»
- [À CONFIRMER : localités desservies, jours de passage et délai du premier rendez-vous] — «Autour de la ville, Nidau, Brügg, Port, Ipsach et Evilard sont des communes voisines que nous pourrions inclure dans nos tournées [À CONFIRMER : localités desservies, jours de passage et délai du premier rendez-vous].»
- [À CONFIRMER : drainage à domicile à Bienne] — «Sur prescription médicale, il fait partie d'un traitement de physiothérapie, au cabinet d'Ins ou à votre domicile biennois [À CONFIRMER : drainage à domicile à Bienne].»
- [À CONFIRMER : localités desservies] — «Ces communes voisines de Bienne peuvent entrer dans nos déplacements à domicile [À CONFIRMER : localités desservies].»
- [À CONFIRMER : délai du premier rendez-vous] — «Le délai pour la première séance dépend de nos disponibilités [À CONFIRMER : délai du premier rendez-vous].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/physio-a-bienne/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Physio à Bienne (Biel) : au cabinet d'Ins ou à domicile |
| 4 H3 de valor bajo el hero | no | omitida |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | sí |  |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | sí |  |
| FAQ (8-10) | no | 4 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | no | omitida |

- receta: ciudad en 5 H2 · FAQ 4 · CTA reserva 3 / tel 2 / WhatsApp 2 · palabras visibles 777
