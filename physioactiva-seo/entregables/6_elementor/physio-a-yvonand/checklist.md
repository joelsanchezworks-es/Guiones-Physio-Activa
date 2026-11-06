# Checklist — /physio-a-yvonand/

- Lote: B · Plantilla: lombaire · Validación: OK
- Indexación: NOINDEX hasta la confirmación del cliente

## Marcadores [À CONFIRMER] (4)

- [À CONFIRMER : domicile à Yvonand] — «Une ordonnance de physiothérapie en poche et un domicile à Yvonand ? Physio Activa travaille depuis Ins, à environ 35,9 km en ligne droite, et vous propose des séances au cabinet ; le déplacement à domicile reste à confirmer pour votre secteur [À CONFIRMER : d»
- [À CONFIRMER : localités desservies et jours de passage] — «Chêne-Pâquier, Démoret, Rovray et Cheyres-Châbles seraient alors concernés [À CONFIRMER : localités desservies et jours de passage].»
- [À CONFIRMER : délai pour une première séance et domicile possible à Yvonand] — «Oui, la rééducation peut commencer dès réception de l'ordonnance de physiothérapie [À CONFIRMER : délai pour une première séance et domicile possible à Yvonand].»
- [À CONFIRMER : localités et jours de passage] — «Ces communes voisines d'Yvonand seraient regroupées avec les visites du secteur si le domicile y est proposé [À CONFIRMER : localités et jours de passage].»

## Publicación

1. WordPress → Páginas → abrir (o crear) la página con el slug `/physio-a-yvonand/`.
2. Plantilla de página: «Elementor Canvas / Pleine largeur» si el header y el footer los pone el Theme Builder; si no, «Elementor Pleine largeur». Título del tema oculto.
3. Editar con Elementor → carpeta (Mis plantillas) → Importar `elementor.json` → Insertar.
4. Yoast: copiar title, meta, slug y keyword de `yoast.txt`. Avanzado → noindex.
5. Comprobar en móvil y escritorio; validar el schema en https://validator.schema.org con la URL publicada.
6. Si se usa el CSS global, importar `elementor-css-global.json` en su lugar (ver PUBLICAR.md).

## Receta activaglobals (2.5)

| Sección | ¿Está? | Nota |
|---|---|---|
| H1 «servicio + ciudad» | sí | Physio à Yvonand : au cabinet d'Ins ou à domicile |
| 4 H3 de valor bajo el hero | no | omitida |
| Qué es / cuándo consultar (+ señales de alarma) | no | página sin patología concreta (hub/reserva/home): no aplica |
| Tipos según el caso (H2 + H3 por subtipo) | sí |  |
| Proceso en pasos (H2 + H3) + CTA intermedio | no | no aplica a esta página |
| Reembolso y coste | sí |  |
| FAQ (8-10) | no | 4 preguntas — texto ya validado del módulo 5: no se reescribe (2.5.5); ampliar con preguntas de data/paa_banco.json en una revisión |
| CTA final en pregunta con la ciudad | sí |  |

- receta: ciudad en 3 H2 · FAQ 4 · CTA reserva 3 / tel 2 / WhatsApp 2 · palabras visibles 642
