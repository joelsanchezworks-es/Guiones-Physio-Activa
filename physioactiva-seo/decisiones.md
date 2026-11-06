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
