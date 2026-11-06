# Checklist — /physio-a-sugiez/

- Lote: A · Plantilla: lombaire · Validación: OK
- Indexación: index, follow

## Marcadores [À CONFIRMER] (4)

- [À CONFIRMER : domicile toujours proposé à Sugiez] — «Vous pouvez venir au cabinet ou, sur ordonnance médicale, recevoir votre physio chez vous dans le Mont-Vully [À CONFIRMER : domicile toujours proposé à Sugiez].»
- [À CONFIRMER : liste des villages et jours de passage dans le Vully] — «Notre site mentionne déjà des visites à domicile à Sugiez, Praz, Môtier, Lugnorre et Guévaux ; pour Nant, Salavaux ou Cudrefin, demandez-nous simplement si votre adresse est desservie [À CONFIRMER : liste des villages et jours de passage dans le Vully].»
- [À CONFIRMER : arrêt et horaires à vérifier pour Sugiez] — «Notre site indique aussi un accès en train par la ligne Fribourg–Morat–Ins [À CONFIRMER : arrêt et horaires à vérifier pour Sugiez].»
- [À CONFIRMER : jours de passage dans le Mont-Vully] — «Les jours de passage restent à fixer avec vous [À CONFIRMER : jours de passage dans le Mont-Vully].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/physio-a-sugiez/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Physio à Sugiez et dans le Vully : au cabinet d'Ins ou à domicile |
| 4 H3 de valor bajo el hero | no | omitida |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | sí |  |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | sí |  |
| FAQ (8-10) | no | 3 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | no | omitida |

- receta: ciudad en 4 H2 · FAQ 3 · CTA reserva 3 / tel 2 / WhatsApp 2 · palabras visibles 722
