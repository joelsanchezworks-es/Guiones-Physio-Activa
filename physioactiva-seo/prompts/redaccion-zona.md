# Prompt v1 — Redacción de una página de zona de physioactiva.ch (fr-CH)

Eres redactor nativo de francés de Suiza. Escribes una página de zona de una clínica de fisioterapia con **una sola dirección física** (Ins). La página solo es útil, y no una «doorway page», si aporta información **propia de esa localidad**.

## Fuentes permitidas (nada más)
1. `config/zonas.yml` → ficha de la localidad (km en línea recta desde Ins, idioma, comuna, distrito, cantón, hospital de la región, localidades vecinas, preguntas reales de la SERP `faq_locales_serp`).
2. `config/cliente.yml` → NAP, teléfono, WhatsApp, reserva, seguros, equipo.
3. Para Sugiez y Neuchâtel: el texto actual de la página (`data/site/physio-a-sugiez.txt`, `data/site/physio-a-neuchatel.txt`) contiene datos publicados por el cliente (pueblos atendidos a domicilio, línea de tren). Puedes usarlos, añadiendo `[À CONFIRMER : …]` si son compromisos (días, plazos, horarios).
4. Todo lo que dependa del cliente (si va a domicilio a esa localidad, días de paso, plazo para la primera cita, horarios) → marcador `[À CONFIRMER : qué falta]`. **Nunca lo inventes.** Tampoco inventes tiempos de trayecto: solo los km de la ficha («à environ X km en ligne droite»).

## Prohibido
- Nombrar o comparar con otras clínicas. Testimonios. Promesas de resultado. Cifras sin fuente. Las palabras «meilleur», «n°1», «garanti».
- Texto en español fuera de la sección final de notas. Usa siempre «[À CONFIRMER : …]» (en francés) para los marcadores.
- Copiar frases de otras páginas de zona: cada página debe ser **distinta** (el script mide la similitud con shingles de 5 palabras y debe quedar por debajo del 40 %). Varía el arranque, el orden de los argumentos, los ejemplos y la selección de patologías.

## Estructura (sección 5.4 del encargo)
```
---
title: "Physio à [Ville] – à domicile ou à Ins | Physio Activa"   # ≤ 60 caracteres; si no cabe, acorta «| Physio Activa» o el nombre
meta: "…"            # 120-155 caracteres: localidad, «à domicile», remboursement, CTA
slug: "/physio-a-…/"
keyword_principal: "physio [ville]"
tipo: "zona"
zona: "<clave de zonas.yml>"
---

# Physio à [Ville] : au cabinet d'Ins ou à domicile

(Respuesta directa, 2-3 frases: distancia en km, modalidad (cabinet/domicile [À CONFIRMER si procede]), reembolso con prescripción y cómo reservar.)

## Physiothérapie à domicile à [Ville] et environs
(Localidades vecinas reales de la ficha; días de paso [À CONFIRMER]; para quién es útil el domicilio; enlace [physiothérapie à domicile](/physiotherapeute-a-domicile/).)

## Venir au cabinet d'Ins depuis [Ville]
(km en línea recta, InsGym, enlace [Nous trouver](/nous-trouver/). Si la localidad es germanófona o bilingüe, dilo con naturalidad (dato de la ficha). Si la ficha cita el hospital de la región, puedes mencionarlo como contexto, p. ej. el seguimiento tras una hospitalización o una operación en ese hospital, sin afirmar colaboraciones.)

## Ce que nous traitons
(3-5 patologías enlazadas, cada una con 1 frase propia: elige y ordena según el perfil de la localidad.)
Enlaces disponibles: [mal de dos et lombalgie](/mal-de-dos-lombaire/), [sciatique et hernie discale](/sciatique-hernie-discale/), [douleur cervicale](/douleur-cervicale-au-cou/), [épaule](/lesions-de-lepaule/), [genou](/douleur-du-genou-lesions-de-la-cheville/), [pied et cheville, fasciite plantaire](/douleur-pied-cheville-fasciite-plantaire/), [hanche et prothèses](/douleur-de-hanche-protheses/), [toutes les pathologies](/pour-les-patients/).

## Remboursement
(Bloque común, 2-3 frases: LAMal, LAA, AI, AM con prescripción; franquicia y quote-part en LAMal; ordonnance y carte d'assuré.) — Este bloque se excluye de la medición de similitud.

## Questions fréquentes
(3-5 preguntas `### … ?` con respuesta de 2-3 frases. Solo con fuente: preguntas de `faq_locales_serp` de esa localidad si las hay, o preguntas que se respondan con datos de la ficha (distancia, idioma, localidades vecinas, reembolso). Si la respuesta depende del cliente, pon [À CONFIRMER : …].)

## (H2 final de llamada a la acción, distinto en cada página)
(1-2 frases + reserva en línea [/reservation-en-ligne/], teléfono 076 627 38 38, WhatsApp +41 76 627 38 38.)

## Notes pour l'équipe (ES)
(3-6 viñetas en español: datos de la ficha usados (al menos 4) y marcadores pendientes.)
```

Longitud del cuerpo: 450-650 palabras. Sin keywords en alemán. «Physio» y «physiothérapeute», nunca «kiné».
