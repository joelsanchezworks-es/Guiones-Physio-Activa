# Ajuste v3 (2026-11-09) — seguros, receta, horario y FAQ estándar

Petición del cliente: alinear los textos con la web actual (https://physioactiva.ch) y **no tratar el tema de la receta médica ni el detalle del seguro**, que considera delicado.

## 1. Quitar
- Toda mención a **ordonnance / prescription médicale / médecin prescripteur / carte d'assuré**, a **LAMal, LAA, AI, AM**, **franchise, quote-part, remboursement, tarif, structure tarifaire, prix, coût**. Reformula la frase sin ese contenido (no la sustituyas por lo contrario: nunca escribas que no hace falta receta ni que todo está pagado).
- Los marcadores `[À CONFIRMER …]` / `[POR CONFIRMAR]` que solo existían por esos temas o por el horario.
- **Sí se mantienen** las señales de alarma médicas («consultez d'abord un médecin», «appelez le 144»): son seguridad del paciente, no seguro.

## 2. Usar en su lugar (copy de la web y del cliente)
- Seguros, una sola formulación: « Notre cabinet est reconnu par toutes les compagnies d'assurance maladie en Suisse. Nous disposons de toutes les autorisations sanitaires nécessaires et accueillons les patients quel que soit leur canton de résidence. » (se puede acortar a « reconnu par toutes les assurances maladie en Suisse »).
- Horario (web): « du lundi au vendredi, jusqu'à 20h ». Sin marcador.
- Reserva: en ligne, par téléphone (076 627 38 38) ou WhatsApp (+41 76 627 38 38).

## 3. Sección de reembolso
La H2 «Remboursement…» (y sus H3 sobre LAMal, accidentes, coste) se sustituye por **una sección corta**:
- Zonas: `## Assurances et horaires : physio à [Ville]` (mantiene la ciudad en este H2), 2-4 frases: reconocido por todas las aseguradoras, cualquier cantón, jusqu'à 20h, cómo reservar.
- Resto de páginas: `## Assurances et horaires` con el mismo contenido (sin ciudad).

## 4. FAQ estándar (base de la web, página /douleur-cervicale-au-cou/)
La FAQ de cada página empieza por estas 3 preguntas, adaptadas al tema de la página, seguidas de las preguntas que ya tenía y que no traten de receta, reembolso ni precio (total 8-10; si se quitan preguntas, completa con otras de `data/paa_banco.json` o del `brief.json` de la página que no toquen esos temas):
1. **« Quand dois-je consulter un physiothérapeute pour [motif / une douleur] ? »** — p. ej. si la douleur dure plus d'une semaine, limite la mobilité, perturbe le sommeil… ; plus on la traite tôt, plus c'est simple. (Adaptar al tema; en zonas: « … pour une douleur ? »).
2. **« Physio Activa travaille-t-il avec toutes les compagnies d'assurance ? »** — « Oui. Notre cabinet est reconnu par toutes les compagnies d'assurance maladie en Suisse. Nous disposons de toutes les autorisations sanitaires nécessaires et accueillons les patients quel que soit leur canton de résidence. » (idéntica en todas las páginas).
3. **« Combien de séances me faut-il [pour …] ? »** — « La durée du traitement varie selon votre situation… Lors de la première visite, nous établissons une estimation adaptée à votre cas. » (sin cifras).

Preguntas que se **eliminan o sustituyen**: las de ordonnance/prescription, remboursement, LAMal, tarif/prix/coût, « faut-il une ordonnance », « combien coûte », etc.

## 5. Otras reglas
- No cambies el resto del texto más de lo necesario; mantén slugs, front matter (ajusta `meta` si mencionaba reembolso/LAMal: 120-155 caracteres), estructura, enlaces y longitud aproximada.
- La ciudad sigue sin aparecer en ningún H3. Sin promesas de resultado.
- Las páginas de ciudad **no** llevan sección de equipo (va en À propos y en la home).
- Añade en `## Notes pour l'équipe (ES)` una viñeta: «Ajuste v3: sin receta ni detalle de seguro; FAQ estándar; horario hasta las 20h».
