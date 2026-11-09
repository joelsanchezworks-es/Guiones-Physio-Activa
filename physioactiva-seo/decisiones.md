# Decisiones del proyecto SEO physioactiva.ch

Una línea por decisión. Fecha de la ejecución: 2026-11-06.

## Conexión y datos
- DataForSEO por API REST v3 (no hay MCP). En la nube las credenciales las inyecta el proxy para `api.dataforseo.com`; en local se leen de `.env` (`DATAFORSEO_LOGIN`/`DATAFORSEO_USERNAME`, `DATAFORSEO_PASSWORD`). Nunca se escriben en el código ni en los entregables.
- Volumen: `keywords_data/google_ads/search_volume/live` con `location_code` 2756 (Suiza) y `language_code` "fr". En Suiza el filtro de idioma casi no cambia los números (se comprobó con 320 combinaciones locales: mismo volumen con "fr" y sin idioma), así que el volumen de términos neutros como "physio" incluye búsquedas germanófonas.
- Cantones probados: Berna 20129, Friburgo 20132, Neuchâtel 20138, Vaud 20148. Solo se piden para keywords con volumen CH ≥ 20, semillas del documento y combinaciones locales.
- Google Ads agrupa variantes cercanas (p. ej. "physiothérapeute" y "physiothérapie" devuelven la misma cifra, 6.600). Al sumar volúmenes de un clúster no se cuentan dos veces las keywords con el mismo volumen y la misma serie de 12 meses.
- Intención y KD: se toman de DataForSEO Labs (`keyword_suggestions`/`keyword_ideas`); solo se llama a `search_intent` y `bulk_keyword_difficulty` para las que faltan. Si el KD no viene, se deja vacío (no se estima).
- La SERP orgánica se pide con `location_coordinate` centrada en Ins (47.0058, 7.1063, radio 10 km). Las coordenadas de las ciudades del mapa son el centro aproximado de cada localidad.
- Google ya no devuelve la URL directa (devuelve `google.com/goto?...`): el dominio y la ruta de cada resultado se toman del breadcrumb visible. El clustering usa ese «dominio + ruta» como identificador de URL.
- physiodom.ch no se consulta (regla del repositorio: no se usa nunca). La redirección 301 queda como decisión ya tomada por el cliente.

## Filtro y normalización (scripts/m1_filtrar.py, config/filtro.yml)
- Normalización: minúsculas, sin acentos, œ→oe. Clave de duplicado: sin artículos ni preposiciones, singular simple (-s/-x) y palabras ordenadas.
- Una keyword es relevante si contiene un término de fisioterapia o una patología/técnica musculoesquelética, y no contiene un término excluido (otros oficios, Francia/Bélgica, alemán, inglés, productos, lugares fuera de la zona).
- Patologías neurológicas o generales (AVC, Parkinson, vertiges, post-partum) solo cuentan si van con physio/rééducation/exercice/traitement.
- Las marcas de otras clínicas se marcan como «competidor»: sirven como dato de competencia, no como objetivo.
- Umbral de volumen: se descartan keywords con volumen CH < 10, salvo las semillas del documento anterior (se conservan siempre, con su dato aunque sea nulo).

## Clustering y viabilidad (config/umbrales.yml)
- Dos keywords van en la misma página si comparten ≥ 4 URLs de su top 10 (algoritmo voraz por volumen descendente: determinista).
- Las keywords sin SERP propia se asignan al clúster cuya keyword principal está contenida en ellas y es del mismo tema.
- Página propia: volumen agregado del clúster ≥ 150/mes (subido de 50 porque con 50 salían 215 páginas, inmanejable para una clínica de dos fisioterapeutas). Con volumen pero SERP dominada por portales → página con enfoque informacional y CTA local. Por debajo → sección de la página del tema o artículo de blog.
- Arquitectura: una página por tema (patología o técnica). Los clústeres secundarios del mismo tema son secciones H2; si un clúster secundario supera 300/mes con SERP distinta, queda como «candidata a página propia en fase 2».
- Clasificación de los resultados de la SERP: «portal/medio/institución» por lista de dominios (Planète Santé, HUG, CHUV, Doctissimo, Wikipedia, Ligue suisse contre le rhumatisme…), «clínica/physio» por léxico en dominio o título, y «otro» para el resto.

## Prioridad (sección 9)
- prioridad = impacto × confianza / esfuerzo.
- Impacto (1–5) = 5 × log10(volumen+1)/log10(volumen máximo+1) × factor de intención × factor de ganabilidad × ajuste de autoridad.
- Factor de intención: transaccional/local 1,0 · comercial 0,8 · informacional 0,6 · navegacional 0,3.
- Ganabilidad: 1,0 si hay clínicas en el top 10 o local pack; 0,5 si solo portales.
- Ajuste de autoridad: índice = rank de dominio de physioactiva.ch / mediana del de los competidores locales (backlinks/summary). En SERP de portales se aplica 0,5 + 0,5 × índice; en SERP locales no se aplica (el local pack depende de la ficha, no de los enlaces).
- Confianza: 3 = volumen medido y SERP analizada; 2 = solo uno de los dos; 1 = hipótesis.
- Esfuerzo: optimizar 2 h, página nueva 5 h, sección 1,5 h, tarea técnica 1 h.
- Dependencias: técnica → home y 4 patologías existentes → patologías nuevas → zonas.

## Caché y coste
- Caché `data/cache/AAAA-MM-DD/<endpoint>/<hash>.json`. TTL: Labs y volumen 30 días, SERP y mapa 7 días, ficha de Google 7 días, on_page en cada ejecución. El hash es el del cuerpo exacto de la petición, así que cambiar un parámetro invalida la entrada.
- Techo por ejecución: 15 USD (`config/limites.yml`). Cada llamada se registra en `data/costes.csv` con el coste que devuelve la API.
- `data/raw/` (copia idéntica de la caché) no se sube al repositorio para no duplicar 29 MB; la caché sí, para poder reproducir la ejecución.
- Al modelo no se le pasan respuestas crudas: solo tablas agregadas (`data/clusters.json`, top N por tema).
- Contradicción entre fuentes: GSC > SERP en vivo > Labs > volumen Google Ads > auditoría anterior. No hay acceso a GSC ni a GA4 en esta ejecución: esos bloques salen como «no disponible».

## Contenido
- Las páginas de patología no prometen curas ni resultados, no dan diagnósticos e incluyen señales de alarma que requieren médico. Sin testimonios.
- `[POR CONFIRMAR]` donde falte un dato del cliente (titulaciones, zonas lejanas, tarifas).
- Hub de patologías: se reutiliza `/pour-les-patients/` («Où avez-vous mal ?») en vez de crear una URL nueva; así no hace falta ninguna 301.
- Reserva: se propone `/reservation-en-ligne/` como canónica (slug en francés y descriptivo). Requiere aprobación del cliente.
- `elementor.json`: no se genera en esta ejecución porque no se recibió el JSON de referencia (`lombaire-elementor.json`). Queda pendiente; el resto de archivos por página sí se entregan.

## Fase Elementor (2026-11-06)
- 25 JSON: 16 del menú (home, à propos, 8 zonas del lote A y 6 del lote B en borrador) + 9 ya redactadas (hub, 7 patologías, reserva). No hay página de zona de Ins: «Physio Ins» del menú enlaza a `/` para no canibalizar la home.
- Plantillas: `home-design-elementor.json` solo para la home; `lombaire-elementor.json` para todas las demás. `<style>` de cada plantilla sin cambios en la versión por defecto.
- La receta de cada página (`receta.json`) la genera un script de forma determinista desde `fr.md` (reglas por tipo de sección): H2 con H3 → `why-grid`; listas → tarjetas `wcard` (con icono de alerta en «quand consulter»); procesos → `steps`; texto corrido → `wcard` centrada; hub y home → `serv-grid` con enlace; equipo → `team-grid`; FAQ → `faq-list` (la primera abierta); CTA → `cta-band`; mapa → `map-facade` (enlace a Google Maps, sin iframe).
- Estilos en línea mínimos solo de espaciado (`margin-top` entre párrafos, ancho máximo de la tarjeta de texto) y el color de los enlaces del texto (`var(--azure)`, variable de la plantilla): la plantilla pone `margin:0` y `color:inherit` a todo y, sin eso, los párrafos se pegaban y los enlaces no se distinguían. No se crea ninguna clase.
- Home: se quitan el traductor (`data-i18n` + diccionario FR/DE/EN/PT/ES), los servicios y la FAQ generados por JS (ahora HTML estático), las reseñas de ejemplo (`ph-flag`), las cifras sin fuente (`stats`: 4,9 · 74 % · <1 semaine · 20h) y la sección de aseguradoras de ejemplo. La nota real de Google (5,0 · 19 reseñas, DataForSEO 06.11.2026) va en el hero con enlace a la ficha. Su script pasa a ser el de lombaire (reveal + acordeón FAQ): `buildFAQ` de la home no añadía el acordeón a una FAQ estática.
- Vídeo del hero: `preload="metadata"`, `poster` (Physio-Activa-00036.jpg), `muted playsinline autoplay loop` y `aria-label`.
- Se elimina la sección `trust` de la plantilla home: sus títulos son `h4` y rompían la jerarquía (H1 → H4). Sus mensajes verificables pasan a las `hero-pills`.
- Botones: reserva → `/reservation-en-ligne/` (en esa página, el principal → OneDoc, enlace publicado en el sitio actual); teléfono → `tel:+41766273838`; WhatsApp → `https://wa.me/41766273838`. Ningún `href="#"`.
- IDs de Elementor: 7 hex derivados del slug (SHA-1), deterministas y únicos en el lote. `page_settings: {hide_title: yes}` en todas.
- Marcadores `[POR CONFIRMAR]` de los textos → `[À CONFIRMER : …]` al construir (ningún texto en español en las páginas).
- Zonas: datos públicos (comuna, distrito, idioma, hospital de la región, localidades vecinas) aportados con URL de fuente en `config/zonas.yml`, pero no verificados en línea en esta sesión (red restringida): revisarlos antes de publicar. Distancias = línea recta desde Ins; no se dan tiempos de trayecto.
- Regla antipuerta: similitud máxima entre zonas 8,9 % (shingles de 5 palabras, sin hero, Remboursement, enlaces a localidades, CTA ni mapa) y ≥ 4 datos propios en las 14.
- SERP por zona: 28 consultas (0,05 USD), registradas en `data/costes.csv` con la ejecución «elementor-2026-11-06».
- Modo `--css-global`: `global/pa-styles.css` (CSS de lombaire, con la errata `.faq . q-ic` corregida y los `@import` pasados a `<link>`) + `global/pa-scripts.js`; las páginas ligeras (`elementor-css-global.json`) no llevan `<style>` ni `<script>` en línea, salvo la home (hero con vídeo con reglas propias).

## Optimización SEO local (2026-11-06, segunda pasada)
- Demanda local medida con Google Ads (CH, sin filtro de idioma) para 15 localidades × 27 variantes (FR y DE) + Labs keyword_ideas/suggestions: 0,39 USD (ejecución «local-2026-11-06» en `data/costes.csv`). Resultado en `data/z_local_kw.json` y brief por ciudad en `data/z_briefs_local.json`.
- Google Ads separa las grafías con y sin acento («physio neuchatel» 590 frente a «physio neuchâtel» 50): el texto se escribe con acentos (Google los iguala al posicionar) y el volumen de la ciudad se lee sumando ambas.
- Las páginas de zona se reescriben para cubrir las variantes genéricas con volumen (physio / physiothérapeute / physiothérapie + ville) y, donde hay demanda ≥ 20/mes, una sección con un H3 por servicio local (drainage lymphatique, massage thérapeutique, dry needling, physio sport, à domicile) enlazado a la página del servicio.
- Enlazado interno local (componente `insurers`/`chip` de la plantilla, sin clases nuevas):
  - Home: cuadrícula «Nos zones» (`serv-grid`) con las 8 zonas publicables, ordenadas por distancia, con km, distrito y cantón.
  - Zonas: «Localités voisines» → home + las 4 zonas publicables más cercanas.
  - Patologías, hub, reserva y À propos: chips hacia la home y las 8 zonas publicables.
  - Las páginas publicables no enlazan a las zonas del lote B (borradores noindex). Cuando el cliente las confirme, se pasan a lote A en `config/zonas.yml` y se reconstruye: los enlaces aparecen solos.
- Schema local: `BreadcrumbList` en todas las páginas salvo la home; en las zonas, `Service` con `areaServed` = la comuna (con `sameAs` a su ficha pública y `containedInPlace` = cantón); `areaServed` del negocio = Ins, Anet y las comunas de las zonas publicables.
- Morat y Chiètres siguen sin volumen medible ni en francés ni en alemán (Google Ads devuelve nulo): se quedan en el lote B.

## Estructura según activaglobals.com (2.5, 2026-11-06)
- Red: se añadió `activaglobals.com` a la red permitida del entorno para rastrear `/`, `/instalacion-electrica-sabadell/`, `/acometida-electrica-sabadell/` y `/cuadro-electrico-sabadell/` (HTML guardado en `referencias/activa_html/`, patrón en `referencias/activa_patron.md`).
- Patrón verificado: H1 «Servicio en Ciudad» → 4 H3 de valor → qué es/cuándo → tipos (H3) → proceso (H3 por paso) → coste (H2 con ciudad) → FAQ de 10 (H2 con ciudad) → CTA final en pregunta (H2 con ciudad «o alrededores»); ciudad en 2-4 H2 y en ningún H3; teléfono ×4 y WhatsApp con mensaje rellenado.
- Diferencia deliberada: la referencia salta de H1 a H3 en los 4 puntos de valor; aquí llevan un H2 corto encima («L'essentiel en bref» / «L'essentiel avant de prendre rendez-vous») para no romper la jerarquía.
- Los 4 H3 de valor son verificables: «Sur prescription, remboursé LAMal / LAA», «Au cabinet ou à domicile», «Bilan et plan de traitement», «Rendez-vous en ligne, par téléphone ou WhatsApp». «Premier rendez-vous rapide» no se usa hasta que el cliente lo confirme. En la home, patologías, hub y reserva los inyecta el constructor; en zonas y À propos van en su `fr.md`.
- Proceso: 4 pasos (Ordonnance → Bilan → Séances au cabinet ou à domicile → Autonomie et prévention); en las patologías se añade a la sección «Déroulement des séances» sin tocar su texto. Tras el proceso, CTA intermedio con reserva, teléfono y WhatsApp.
- WhatsApp: enlace con mensaje rellenado por página (`wa.me/41766273838?text=Bonjour, je souhaite prendre rendez-vous chez Physio Activa (<página>).`). El hero lleva tres vías: reserva, WhatsApp y teléfono.
- Patologías (texto ya validado, no se reescribe): se reordena «Quand consulter un médecin» justo después de «Qu'est-ce que…», se añaden los 4 H3 de valor y los pasos, y se renombran tres H2 para llevar la ciudad: «Remboursement et coût de la physio à Ins», «Questions fréquentes sur <sujet> et la physio à Ins» y el CTA final en pregunta «<Motivo> : besoin d'un physio à Ins ou dans les environs ?». Se añaden preguntas reales («Autres questions posées» del brief) hasta 8 por página.
- Home: H1 corto «Physio à Ins (Anet)»; orden: valor → quiénes somos → equipo → galería → patologías → servicios → zonas → proceso en 3 pasos → domicilio → enfoque → reembolso → FAQ de 10 (5 nuevas de preguntas reales) → CTA final en pregunta.
- Zonas y À propos: reescritos con la receta completa (1.000-1.200 palabras, FAQ de 8-10 a partir de `data/paa_banco.json` + preguntas locales respondidas con la ficha), ciudad solo en title, H1 y 4 H2 («Venir au cabinet d'Ins depuis…», «Remboursement et coût…», «Questions fréquentes…», CTA final).
- Validador: nuevas comprobaciones «ciudad nunca en un H3» (en zonas, el nombre de esa localidad; en el resto, Ins/Anet) y «CTA repetidos» (reserva ≥ 3, teléfono ≥ 2, WhatsApp ≥ 2); el informe anota ciudad en H2, nº de FAQ y palabras.
- Publicación manual (7.5): nada se escribe en WordPress. `PUBLICAR.md` es una checklist imprimible con una ficha por URL (copia de seguridad, borrador `-v2`, Yoast, noindex del lote B, verificación 200/H1/botones/título) y la lista de URLs para la verificación por rastreo.

## Ajuste v3 (2026-11-09) — petición del cliente
- Seguros y receta: el cliente prefiere no tratar la receta médica ni el detalle del seguro. Se quitan de todas las páginas las menciones a ordonnance/prescription, LAMal/LAA/AI/AM, franchise, quote-part, remboursement y tarifas, sin afirmar lo contrario. Única formulación (del cliente): « Notre cabinet est reconnu par toutes les compagnies d'assurance maladie en Suisse. Nous disposons de toutes les autorisations sanitaires nécessaires et accueillons les patients quel que soit leur canton de résidence. » Se mantienen las señales de alarma médicas (seguridad del paciente).
- La sección «Remboursement…» pasa a «Assurances et horaires» (en zonas: «… : physio à [Ville]»), excluida de la medición de similitud como bloque común.
- FAQ: empieza por las 3 preguntas estándar de la web (/douleur-cervicale-au-cou/): cuándo consultar, «Physio Activa travaille-t-il avec toutes les compagnies d'assurance ?» y cuántas sesiones (sin cifras).
- Horario: «du lundi au vendredi, jusqu'à 20h» (web del cliente); schema `closes 20:00`, apertura 08:30 (ficha de Google).
- Puntos de valor: «Reconnu par toutes les assurances» sustituye a «Sur prescription, remboursé LAMal / LAA»; paso 1 del proceso: «Prise de rendez-vous» en lugar de «Ordonnance»; etiquetas del hero sin receta ni LAMal («Ouvert jusqu'à 20h»).
- Diseño pedido por el cliente: la CTA final (tras la FAQ) lleva foto de fondo de la plantilla (salle de traitement) con capa oscura y acciones al estilo de la referencia (botón «Réserver maintenant» · «ou» · WhatsApp redondo · «Appelez-nous directement» + teléfono grande). Estilos en línea con las variables de la plantilla, sin clases nuevas.
- Mapa: iframe de Google Maps embebido con la ficha del lugar (nombre, dirección, nota y «Ouvrir dans Maps»), `loading="lazy"`, en lugar de la fachada con enlace.
- Equipo: solo en la home y en À propos; las páginas de ciudad no lo llevan.
