# Prompt v2 — Página de zona según la receta de activaglobals.com (fr-CH)

Sustituye a v1 para la estructura. Se mantienen todas las reglas de `prompts/redaccion-zona.md` (fuentes permitidas, prohibiciones, `[À CONFIRMER : …]`, nada de tiempos de trayecto, no nombrar competidores). El patrón de referencia está en `referencias/activa_patron.md`: se copia la **estructura**, no el tono ni el contenido.

Parte del `fr.md` actual de la zona (ya incluye las keywords locales con volumen de `data/z_briefs_local.json`): reutiliza sus datos y frases, reordénalos y amplíalos. **1.000-1.200 palabras de cuerpo** (sin notas).

## Reglas de la receta
- La **ciudad** aparece en el title, el H1 y **exactamente en estos H2**: «Venir au cabinet d'Ins depuis [Ville]», «Remboursement et coût de la physio à [Ville]», «Questions fréquentes sur la physio à [Ville]» y el CTA final. **Nunca en un H3** (tampoco «à [Ville]» al final de un H3 de servicio: «### Drainage lymphatique», no «### Drainage lymphatique à Fribourg»). En el texto, la ciudad con naturalidad, sin relleno.
- Encabezados que responden a búsquedas reales. FAQ de **8 a 10 preguntas**: elige las preguntas de `data/paa_banco.json` (preguntas reales de Google) que tengan sentido en Suiza (descarta «Sécurité sociale», salarios, formación, «MTT poker», inglés), y añade 2-3 preguntas locales que se respondan con la ficha (distancia, idioma, localidades vecinas, hospital de la región). Reformula ligeramente la pregunta si hace falta, sin cambiar su sentido. **Respuestas propias de cada ciudad** (2-4 frases) para que las páginas no se parezcan: usa datos de la ficha en las respuestas. Sin precios ni número de sesiones: para tarifas, explica que existe una estructura tarifaria nationale pour la physiothérapie convenue avec les assureurs y pon `[À CONFIRMER : tarif appliqué]`.
- **Varía** la selección de preguntas y el orden entre ciudades (similitud < 40 % con las otras zonas, medida sin la sección «Remboursement…»).

## Estructura obligatoria
```
---  (mismo YAML que ahora: title ≤ 60, meta 120-155, slug, keyword_principal, tipo: "zona", zona)
# Physio à [Ville] : au cabinet d'Ins ou à domicile
(Respuesta directa 2-3 frases: km en línea recta, modalidad, reembolso con prescripción, cómo reservar.)

## L'essentiel en bref
### Sur prescription, remboursé LAMal / LAA
### Au cabinet d'Ins ou à domicile
### Bilan et plan de traitement
### Rendez-vous en ligne, par téléphone ou WhatsApp
(1-2 frases cada uno, adaptadas a la ciudad en el texto, no en el H3. Si el domicilio en esa ciudad no está confirmado, dilo con [À CONFIRMER : …].)

## Quand consulter un physio, et quand voir d'abord un médecin ?
(Motivos frecuentes de consulta + señales de alarma → médecin / 144. Sin ciudad en el H2.)

## Quelle prise en charge selon votre situation ?
### … (un H3 por caso: p. ej. au cabinet d'Ins · à domicile et localités voisines · après une opération ou une hospitalisation · douleurs du dos, du genou, de l'épaule… con enlaces a las patologías · y un H3 por cada servicio local con volumen que ya tenga la página: drainage lymphatique, massage thérapeutique, dry needling, physio sport, enlazados a su página)

## Comment se déroule votre prise en charge ?
### Ordonnance
### Bilan
### Séances au cabinet ou à domicile
### Autonomie et prévention
(1-3 frases cada paso.)

## Venir au cabinet d'Ins depuis [Ville]
(km en línea recta, InsGym, enlace a /nous-trouver/, idioma de la localidad, hospital de la región como contexto.)

## Remboursement et coût de la physio à [Ville]
### Assurance de base (LAMal)
### Accident, AI et AM
### Ce qui détermine ce que vous payez
(franquicia, quote-part, estructura tarifaria nacional; sin cifras.)

## Questions fréquentes sur la physio à [Ville]
### … ? (8-10)

## Besoin d'un physio à [Ville] ou dans les environs ?
(1-2 frases + reserva en línea [/reservation-en-ligne/], 076 627 38 38 y WhatsApp.)

## Notes pour l'équipe (ES)
```
