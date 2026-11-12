# Ajuste v4 (2026-11-10) — páginas de ciudad para el diseño «pa-lp» del cliente

Se mantiene todo lo de `prompts/ajuste-seguros-faq.md` (sin receta ni detalle de seguro, horario «jusqu'à 20h», FAQ estándar) y la estructura de `prompts/redaccion-zona-v2.md`. Cambios:

## 1. Sin marcadores
Elimina **todos** los `[À CONFIRMER …]` / `[POR CONFIRMAR …]` y reescribe la frase para que sea correcta sin el dato pendiente:
- **Domicilio:**
  - **Zonas de la región que el cliente ya cubre en su web** (Seeland y Trois-Lacs): sugiez, la-neuveville, chietres, morat, neuchatel, avenches, lyss, bienne. Afirma con naturalidad: « Nos physiothérapeutes se déplacent à domicile à [Ville] et dans les environs (localités vecinas de la ficha) ».
  - **Resto** (fribourg, payerne, estavayer, yvonand, yverdon, lausanne): « Selon votre adresse, nous pouvons aussi venir à domicile : contactez-nous pour le vérifier. »
  - Nunca des días de paso.
- **Plazo del primer rendez-vous:** la web del cliente dice «rendez-vous dans la semaine dans la plupart des cas». Puedes usar exactamente esa formulación.
- **Idiomas** (web del cliente): français, allemand, anglais, espagnol et portugais.
- **Duración de la sesión, tarifas, titulaciones:** no los menciones.
- **MTT:** el cabinet lo ofrece (existe /medical-training-therapy-mtt/).

## 2. SEO local reforzado
Objetivo: que la página salga para «physio [ville]», «physiothérapeute [ville]» y «physiothérapie [ville]». Las búsquedas y su volumen están en `data/z_briefs_local.json`.
- **H1:** `Physio à [Ville] : au cabinet d'Ins ou à domicile` (ya está); el title igual o con la variante de más volumen.
- **Primera frase** del intro: contiene « physio à [Ville] » o « physiothérapeute à [Ville] ».
- Las tres variantes (physio / physiothérapeute / physiothérapie + ciudad) aparecen **al menos 2 veces cada una** en el cuerpo, de forma natural. Además, «près de [Ville]» y «à domicile à [Ville]» al menos una vez cada una. Sin relleno ni listas de keywords.
- **Ciudad en H2:** «Venir au cabinet d'Ins depuis [Ville]», «Assurances et horaires : physio à [Ville]», «Questions fréquentes sur la physio à [Ville]», CTA final, y además el H2 de domicilio «Physiothérapie à domicile à [Ville] et environs». **Nunca en un H3.**
- **Localidades vecinas** (ficha) nombradas en el texto de domicilio y en una pregunta de la FAQ.
- **Servicios con demanda local** (`services_locaux` ≥ 20): un H3 por servicio, con enlace, en la sección «Quelle prise en charge selon votre situation ?».
- **FAQ de 8-10:** primera pregunta « Où trouver un physiothérapeute près de [Ville] ? » (respuesta: cabinet d'Ins, Rämismatte 21, 1er étage du bâtiment Lidl, parking, distancia aproximada, domicilio según el punto anterior). Después, las 3 estándar y el resto, variadas.

## 3. Estructura (secciones H2, en este orden)
1. `# Physio à [Ville] : au cabinet d'Ins ou à domicile` + intro (2-3 frases).
2. `## L'essentiel en bref` + 4 `###` (Reconnu par toutes les assurances · Au cabinet ou à domicile · Bilan et plan de traitement · Rendez-vous en ligne, par téléphone ou WhatsApp).
3. `## Un physiothérapeute près de [Ville]` (párrafos: dónde está el cabinet, por qué venir, qué se trata).
4. `## Physiothérapie à domicile à [Ville] et environs`.
5. `## Quand consulter un physio, et quand voir d'abord un médecin ?`.
6. `## Quelle prise en charge selon votre situation ?` + `###`.
7. `## Comment se déroule votre prise en charge ?` + 4 `###` (Prise de rendez-vous · Bilan · Séances au cabinet ou à domicile · Autonomie et prévention).
8. `## Venir au cabinet d'Ins depuis [Ville]`.
9. `## Assurances et horaires : physio à [Ville]`.
10. `## Questions fréquentes sur la physio à [Ville]` + 8-10 `###`.
11. `## Besoin d'un physio à [Ville] ou dans les environs ?` + 1-2 frases.
12. `## Notes pour l'équipe (ES)`.

**Longitud:** 1.000-1.300 palabras de cuerpo. Páginas distintas entre sí (similitud < 40 %).
