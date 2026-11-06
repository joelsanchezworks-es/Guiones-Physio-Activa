# Checklist — /physio-a-fribourg/

- Lote: A · Plantilla: lombaire · Validación: ERRORES: receta: ciudad nunca en un H3
- Indexación: index, follow

## Marcadores [À CONFIRMER] (6)

- [À CONFIRMER : domicile à Fribourg] — «Après une opération ou en cas de mobilité réduite, recevoir son physiothérapeute chez soi à Fribourg peut simplifier la rééducation [À CONFIRMER : domicile à Fribourg].»
- [À CONFIRMER : localités desservies et jours de passage] — «En plus de la ville, Villars-sur-Glâne, Marly, Givisiez et Granges-Paccot sont les localités voisines que nous pourrions couvrir [À CONFIRMER : localités desservies et jours de passage].»
- [À CONFIRMER : drainage à domicile à Fribourg] — «Sur ordonnance, le drainage s'intègre à votre traitement de physiothérapie, à Ins ou chez vous selon votre mobilité [À CONFIRMER : drainage à domicile à Fribourg].»
- [À CONFIRMER : dry needling aussi à domicile] — «Les séances ont lieu au cabinet d'Ins [À CONFIRMER : dry needling aussi à domicile].»
- [À CONFIRMER : localités desservies] — «Ces deux communes voisines de Fribourg font partie des zones envisagées pour les visites à domicile [À CONFIRMER : localités desservies].»
- [À CONFIRMER : délai du premier rendez-vous] — «Le délai pour la première séance est à vérifier avec nous [À CONFIRMER : délai du premier rendez-vous].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/physio-a-fribourg/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Physiothérapie à Fribourg : au cabinet d'Ins ou à domicile |
| 4 H3 de valor bajo el hero | no | omitida |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | sí |  |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | sí |  |
| FAQ (8-10) | no | 4 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | no | omitida |

- receta: ciudad en 4 H2 · FAQ 4 · CTA reserva 3 / tel 2 / WhatsApp 2 · palabras visibles 839
