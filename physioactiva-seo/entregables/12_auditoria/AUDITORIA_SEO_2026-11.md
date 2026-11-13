# Auditoría SEO de physioactiva.ch · noviembre 2026

**Qué se ha revisado**
- Las 54 URL publicadas (sitemap de Yoast), una por una, el 13/11/2026.
- La ficha de Google (Perfil de Empresa), con datos de DataForSEO.
- Las búsquedas reales de Google para «physio ins».

**Contra qué se ha comparado**
- El ebook «Los 7 prompts de Claude para catapultar tu SEO en 2026» (8 pasos).
- El vídeo de Dani Llamazares «Cómo crear un negocio de una persona (con Claude)», sobre SEO local en Google Maps, analizado completo a partir de su transcripción.

Archivos que acompañan este informe:
- `auditoria-paginas.csv`: una fila por página con todos los datos.
- `yoast-propuestas.json`: títulos y metas listos para pegar en Yoast.
- `crawl-2026-11-13.json`: los datos en bruto del rastreo.

---

## 1. Resumen: lo que más pesa ahora

| # | Problema | Dónde | Impacto | Esfuerzo |
|---|---|---|---|---|
| 1 | **La home no tiene title de Yoast**: Google muestra «Physio Activa: Accueil». La meta habla de «ordonnance» y el H1 promete «dès cette semaine». | Home | Muy alto | 5 min |
| 2 | **Las 4 entradas del blog muestran el mismo artículo** (el del drenaje): la plantilla de entrada tiene el texto fijo, sin campos dinámicos. Son 4 páginas duplicadas. | Blog | Alto | 30 min |
| 3 | **La marca sale dos veces en el title** de las 14 ciudades («… \| Physio Activa - Physio Activa»). Los títulos se cortan en Google. | Ciudades | Alto | 15 min |
| 4 | **Canibalización**: tres páginas compiten por MTT/fitness médical, dos por suelo pélvico, cuatro de reserva son casi iguales, y la home compite con `/physio-a-ins/`. | Arquitectura | Alto | 1 h |
| 5 | **20 páginas de servicio flojas**: título genérico sin ciudad, 300-650 palabras, ningún enlace interno, la FAQ visible sin schema, y metas que mencionan LAMal, receta u «ordonnance» (va contra la línea del cliente). | Servicios | Alto | 1 día |
| 6 | **Ficha de Google**: dice que cierra a las 19:30 y la web dice «jusqu'à 20h». Las reseñas se han parado (15 en julio, 1 en septiembre, 0 desde entonces). La descripción es genérica y sin keywords. Solo tiene una categoría secundaria. | Google Maps | Muy alto | 2 h y después constancia |
| 6b | **3 páginas enlazadas dan error 404**: `/sciatique-hernie-discale/`, `/douleur-pied-cheville-fasciite-plantaire/` y `/douleur-de-hanche-protheses/`. Las enlazan la home actual y las 14 ciudades, así que hay enlaces rotos en todo el sitio. **Solución:** publicar esas 3 páginas (keywords sciatique, hanche/prothèse y fasciite) o cambiar los enlaces. | Todo el sitio | Alto | 1 h |
| 7 | Páginas que no deberían estar en Google: `/merci/`, `/reserve/`, `/reserver-maintenant/`, `/rendez-vous-online/` y la política de datos. | Indexación | Medio | 10 min |
| 8 | Dos «empresas» distintas en el schema: la Organization de Yoast (`#organization`) y nuestro Physiotherapy (`#physiotherapy`). Google no las une. | Schema | Medio | ya resuelto en las próximas plantillas |
| 9 | 1-2 imágenes sin texto alternativo en cada ciudad (las que subisteis después). | Ciudades | Bajo | 10 min |
| 10 | Algunas respuestas del servidor tardan entre 2 y 3,5 s (TTFB). Conviene caché y optimizar imágenes. | Rendimiento | Medio | técnico |

**La buena noticia:**
- En Google, **Physio Activa es la ficha nº 1 del mapa para «physio ins»**.
- En los resultados normales (orgánicos) de esa búsqueda no hay ningún competidor serio: el top 20 son directorios y páginas sin relación. La home tiene el camino libre para entrar.
- Las 14 páginas de ciudad, la home y «À propos» ya cumplen la mayoría de los pasos del ebook.

---

## 2. Los 8 pasos del ebook: qué cumplimos

| Paso del ebook | Estado | Detalle |
|---|---|---|
| 1. Público objetivo (avatar) | ⚠️ Parcial | Conocemos al paciente por la investigación (zonas, idiomas, postoperatorio, deportistas, mayores), pero no hay un documento de avatar formal. **Acción:** redactarlo (deseos, miedos, vocabulario FR y DE, motivos para elegir). |
| 2. Keywords | ✅ Cumple en ciudades / ⚠️ falta en servicios | Hay investigación DataForSEO por ciudad (volumen, CPC e intención), pero las páginas de servicio no usan sus keywords: drainage lymphatique (590 al mes solo en Lausana), massage, fitness, dry needling… |
| 3. Arquitectura sin canibalización | ❌ No cumple | Duplicados: MTT ×3 (`/physio/`, `/fitness-medical/`, `/medical-training-therapy-mtt/`), suelo pélvico ×2, reserva ×4 más la versión DE, y home contra `/physio-a-ins/`. Ver el apartado 5. |
| 4. Jerarquía H1-H2-H3 frente al top 3 | ✅ Ciudades y home / ⚠️ Servicios | Los servicios tienen H1 sin keyword ni ciudad («Une prise en charge spécialisée et personnalisée», «Retrouver confort et mobilité au quotidien»). Para «physio ins» no hay top 3 orgánico que imitar: la competencia está solo en el mapa. |
| 5. Contenido que posiciona | ✅ Ciudades (1.500-2.400 palabras) / ❌ Servicios (300-650) | Les falta el proceso paso a paso, las indicaciones, para quién es, los enlaces a ciudades y a dolencias, y el CTA. |
| 6. FAQ para los LLM | ✅ Home, ciudades y À propos (con FAQPage) / ⚠️ Servicios | Los servicios tienen FAQ visible pero no tienen schema FAQPage. |
| 7. Diseño que genera confianza | ✅ | Diseño pa-lp responsive. Pendiente: fotos reales en cada ciudad y medir Core Web Vitals. |
| 8. Schema LocalBusiness | ✅ Home y ciudades / ⚠️ Servicios | Physiotherapy + WebPage + Service + FAQPage. Falta unificar el `@id` con Yoast y añadir Service + FAQPage en los servicios. |

---

## 3. El vídeo (SEO local en Google Maps): la ficha de Physio Activa

Datos de la ficha (DataForSEO, 06/11/2026), comparados con la competencia:

| Palanca del vídeo | Physio Activa hoy | Competencia | Qué hacer |
|---|---|---|---|
| **Categoría principal** | Physiothérapeute ✅ | Igual en casi todos | Mantener. |
| **Categorías secundarias** (2-3 alineadas) | Solo «Centre de rééducation» | PhysiOptima tiene 3 | Añadir 1-2 alineadas con la principal, por ejemplo «Clinique de physiothérapie» y «Massothérapeute» (hay demanda de massage). Nada que se aleje del tema. |
| **Servicios** (keyword exacta) | No consta ninguno | — | Crear servicios personalizados: Physiothérapie à domicile · Drainage lymphatique manuel · Massage thérapeutique · Fitness médical (MTT) · Dry needling · Thérapie manuelle · Physio du sport · Rééducation post-opératoire · Ondes de choc · Tecar · Kinésiotaping · Rééducation du périnée · Physiothérapie neurologique · Physiothérapie respiratoire · ATM. |
| **Fotos reales** | 32 | Physio du Lac 23, PhysiOptima 51 | Subir fotos reales cada mes: equipo, sala, máquinas MTT, entrada del edificio Lidl, parking. Nada de stock ni imágenes de IA. |
| **Reseñas** | **19, todas de 5★, con el 100 % respondidas ✅** | Líder en Ins: 42 · Physio du Lac: 71 · PhysiOptima: 67 | **El ritmo se ha parado**: 15 en julio, 3 en agosto, 1 en septiembre y 0 en octubre y noviembre. Para Google pesan las reseñas recientes. **Sistema:** un QR en recepción y un WhatsApp con el enlace de reseña tras la 3.ª sesión. Objetivo: 4-6 al mes. Seguir respondiendo y mencionar con naturalidad el servicio y la ciudad. |
| **Datos completos** | Horario de lunes a viernes 8:30-19:30 ⚠️ · web `http://www.` ⚠️ | — | **Igualar el horario con la web** (la web y el schema dicen 20:00): hay que confirmar cuál es el real y ponerlo igual en todas partes. Web: `https://physioactiva.ch/?utm_source=gbp&utm_medium=organic`. Añadir el chat de WhatsApp y el enlace de cita de OneDoc. |
| **Descripción** | Genérica (DE + FR), sin zonas ni servicios | — | Reescribirla (borrador en el apartado 6). |
| **Publicaciones semanales** | — | — | 1 a la semana: consejo + servicio + ciudad, por ejemplo «Lumbago : que faire les premières 48 h» o «Physio à domicile à Morat». |
| **Citas en directorios** | OneDoc ✅ | — | Mismo nombre, dirección y teléfono (NAP) en local.ch, search.ch, el directorio de physioswiss, Moneyhouse y en la web de InsGym. |
| **Benchmark del top 3** | En Ins: **5.º para «physio»** y **3.º para «physiothérapie à domicile»**. En Sugiez/Vully: 8.º-9.º | Ins: André van den Heuvel (42 reseñas) | Las reseñas, los servicios y las categorías son lo que separa a Physio Activa del top 3 en su propio pueblo. |
| **Reporting mensual** | — | — | Un vídeo corto (Loom) de 5 minutos con el informe de rendimiento de la ficha (llamadas, rutas, clics en la web) y Search Console. |

**Sobre «mejorar la ficha de Google con Yoast»:**
- Yoast no cambia la ficha de Google: la ficha se edita en Google (Perfil de Empresa).
- Lo que Yoast sí hace es reforzarla desde la web:
  - **Ajustes de Yoast › Representación del sitio:** Organización «Physio Activa», logo cuadrado, y perfiles sociales Facebook e Instagram. El enlace de la ficha de Google ya va en nuestro schema.
  - **Título y meta de cada página**: apartado 4.
  - **Yoast Local SEO** (complemento de pago) no hace falta: el schema Physiotherapy con dirección, horario, coordenadas, zona servida y `sameAs` a la ficha ya va en la home y en las ciudades.

---

## 4. Títulos y metas para Yoast (listos para pegar)

En cada página: Editar › Yoast SEO › Título SEO y Meta descripción.

**Importante:** borra las variables «Séparateur» y «Titre du site» que Yoast añade solo. Si no, la marca sale dos veces (es lo que pasa hoy en las ciudades).

| Página | Título SEO (≤60) | Meta descripción (≤155) | Frase clave |
|---|---|---|---|
| `/` | Physio à Ins (Anet) et à domicile | Physio Activa | Physio à Ins (Anet) : cabinet de physiothérapie et soins à domicile dans le Seeland et les Trois-Lacs. Ouvert jusqu'à 20h. Prenez rendez-vous. | physio Ins |
| `/a-propos-de-nous/` | À propos : nos physiothérapeutes à Ins | Physio Activa | Physio Activa, cabinet de physiothérapie à Ins (Seeland) : notre équipe, notre approche, nos soins et nos zones. Au cabinet ou à domicile, jusqu'à 20h. | physiothérapeute Ins |
| `/physio-generale/` | Physiothérapie générale à Ins | Physio Activa | Physiothérapie générale à Ins (Anet) : douleurs, raideurs, rééducation après une blessure ou une opération. Au cabinet ou à domicile, jusqu'à 20h. | physiothérapie Ins |
| `/physiotherapeute-a-domicile/` | Physio à domicile : Ins, Morat, Vully | Physio Activa | Physio à domicile à Ins, Morat, Vully, Avenches, Bienne et Chiètres : rééducation chez vous après une opération ou une chute. Rendez-vous rapide. | physio à domicile |
| `/fitness-medical/` | Fitness médical (MTT) à Ins | Physio Activa | Fitness médical à Ins : entraînement sur appareils encadré par un physiothérapeute après une blessure, une opération ou un mal de dos. | fitness médical |
| `/drainage-lymphatique/` | Drainage lymphatique à Ins | Physio Activa | Drainage lymphatique manuel par un physiothérapeute à Ins : œdème après une opération, lymphœdème, jambes lourdes. Au cabinet ou à domicile. | drainage lymphatique |
| `/massage-therapeutique/` | Massage thérapeutique à Ins | Physio Activa | Massage thérapeutique à Ins par des physiothérapeutes : contractures, nuque, dos, récupération sportive. Au cabinet ou à domicile, jusqu'à 20h. | massage thérapeutique |
| `/physio-du-sport/` | Physio du sport à Ins | Physio Activa | Physiothérapie du sport à Ins : entorse, tendinite, ligament croisé et retour progressif à l'entraînement avec le fitness médical. Rendez-vous en ligne. | physio du sport |
| `/physiotherapie-post-operatoire/` | Rééducation post-opératoire à Ins | Physio Activa | Physiothérapie après une prothèse de hanche ou de genou, une ligamentoplastie ou une chirurgie de l'épaule, au cabinet d'Ins ou à domicile. | rééducation post-opératoire |
| `/therapie-manuelle/` | Thérapie manuelle à Ins | Physio Activa | Thérapie manuelle à Ins : techniques manuelles ciblées pour les douleurs de dos, de nuque et des articulations, associées à des exercices. | thérapie manuelle |
| `/physioactiva-puncture-seche/` | Dry needling (puncture sèche) à Ins | Physio Activa | Dry needling à Ins : aiguille fine sans injection pour relâcher les points gâchettes et les tensions musculaires, par un physiothérapeute. | dry needling |
| `/physioactiva-ondes-de-choc/` | Ondes de choc à Ins : tendinites | Physio Activa | Thérapie par ondes de choc à Ins pour les tendinopathies chroniques : épaule, coude, talon (fasciite plantaire) et tendon d'Achille. | ondes de choc |
| `/tecar-therapie/` | Tecar thérapie à Ins | Physio Activa | Tecar thérapie à Ins : la radiofréquence chauffe les tissus en profondeur pour soulager la douleur et accélérer la récupération. | tecar thérapie |
| `/physioactiva-bandage-neuromusculaire/` | Kinésiotaping à Ins | Physio Activa | Bandage neuromusculaire (kinésiotaping) à Ins : soutenir muscles et articulations sans bloquer le mouvement, en sport comme au quotidien. | kinésiotaping |
| `/physiotherapie-cardiorespiratoire/` | Physiothérapie respiratoire à Ins | Physio Activa | Physiothérapie cardiorespiratoire à Ins : BPCO, asthme, suites de COVID et réentraînement à l'effort après un problème cardiaque. | physiothérapie respiratoire |
| `/physiotherapie-neurologique/` | Physiothérapie neurologique à Ins | Physio Activa | Rééducation neurologique à Ins : AVC, Parkinson, sclérose en plaques. Équilibre, marche et autonomie, au cabinet ou à domicile. | physiothérapie neurologique |
| `/physiotherapie-du-plancher-pelvien/` | Rééducation du périnée à Ins | Physio Activa | Physiothérapie du plancher pelvien à Ins : incontinence, post-partum, douleurs pelviennes. Suivi discret en français, espagnol ou portugais. | rééducation périnée |
| `/physiotemporo-mandibulaire-atm/` | Physio de la mâchoire (ATM) à Ins | Physio Activa | Physiothérapie de la mâchoire (ATM) à Ins : bruxisme, blocage, claquements, douleur articulaire. Traitement manuel et exercices. | physiothérapie ATM |
| `/douleur-cervicale-au-cou/` | Douleur cervicale : physio à Ins | Physio Activa | Nuque raide, torticolis, cervicalgie : physiothérapie à Ins pour soulager la douleur au cou et retrouver la mobilité. Rendez-vous en ligne. | douleur cervicale |
| `/mal-de-dos-lombaire/` | Mal de dos et lombalgie : physio à Ins | Physio Activa | Lombalgie, lumbago, hernie discale : physiothérapie à Ins pour soulager le mal de dos et éviter les rechutes. Au cabinet ou à domicile. | mal de dos |
| `/lesions-de-lepaule/` | Douleur à l'épaule : physio à Ins | Physio Activa | Tendinite, coiffe des rotateurs, épaule gelée : physiothérapie à Ins pour retrouver la mobilité et la force de l'épaule. Rendez-vous rapide. | douleur épaule |
| `/douleur-du-genou-lesions-de-la-cheville/` | Genou et cheville : physio à Ins | Physio Activa | Entorse, ménisque, ligament croisé, arthrose du genou : physiothérapie à Ins pour retrouver la marche et le sport. Au cabinet ou à domicile. | douleur genou |
| `/pour-les-patients/` | Où avez-vous mal ? Guide physio à Ins | Physio Activa | Dos, nuque, épaule, genou, hanche, cheville : trouvez la page qui correspond à votre douleur et notre prise en charge à Ins. | physiothérapie douleur |
| `/reservation-en-ligne/` | Rendez-vous de physio à Ins en ligne | Physio Activa | Réservez en ligne votre rendez-vous de physiothérapie à Ins (Anet), au cabinet ou à domicile, du lundi au vendredi jusqu'à 20h. | rendez-vous physio |
| `/contact/` | Contact : physio à Ins | Physio Activa | Contactez Physio Activa à Ins (Seeland) : WhatsApp, téléphone, e-mail ou réservation en ligne. Réponse rapide, du lundi au vendredi. | contact physio Ins |
| `/nous-trouver/` | Accès au cabinet de physio à Ins | Physio Activa | Physio Activa, Rämismatte 21, 3232 Ins : 1er étage du bâtiment Lidl, parking sur place, plan d'accès et horaires du cabinet. | physio Ins adresse |

**Las 14 ciudades:** el título está bien. Solo hay que borrar `%%sep%% %%sitename%%` al final del campo de Yoast, para que quede, por ejemplo, «Physio Morat (Murten) : à domicile ou à Ins | Physio Activa».

**Páginas que no deben salir en Google** (Yoast › Avanzado › «¿Permitir que los buscadores muestren esta página?» › No):
- `/merci/`, `/reserve/`, `/reserver-maintenant/` y `/rendez-vous-online/` (son páginas para anuncios);
- `/politique-de-donnees/`.

---

## 5. Arquitectura: decisiones para quitar la canibalización

| Grupo | Páginas que compiten | Propuesta |
|---|---|---|
| Fitness médical / MTT | `/fitness-medical/`, `/medical-training-therapy-mtt/`, `/physio/` (su H1 es «MTT et fitness médical à Ins») | Una sola página: **`/fitness-medical/`** («fitness avenches» tiene 140 búsquedas al mes; «MTT» casi ninguna). Redirigir con 301 las otras dos (`/physio/` a `/physio-generale/` si se quiere usar como hub de servicios). Actualizar los enlaces de las ciudades. |
| Suelo pélvico | `/physiotherapie-du-plancher-pelvien/` y `/physio-en-uro-gynecologie/` | Fusionar en plancher pelvien y hacer 301 desde uro-gynécologie. |
| Reserva | `/reservation-en-ligne/` y 3 landings de anuncios | Indexar solo `/reservation-en-ligne/` y poner noindex a las landings. |
| «physio Ins» | Home (H1 «Physio à Ins…») y `/physio-a-ins/` | **Hay que decidir** (ver la pregunta al final). |
| Blog | 4 entradas con el mismo contenido | Arreglar la plantilla de entrada (Elementor › Theme Builder › Single post): usar los widgets dinámicos «Post title» y «Post content» en lugar de texto fijo. |

---

## 6. Borrador de descripción para la ficha de Google (FR + DE, 750 caracteres máximo)

> Physio Activa, cabinet de physiothérapie à Ins (Anet), Rämismatte 21, 1er étage du bâtiment Lidl, parking sur place. Physiothérapie générale et du sport, rééducation post-opératoire, drainage lymphatique, massage thérapeutique, dry needling et fitness médical (MTT). Séances au cabinet ou à domicile à Ins, Morat, Vully, Chiètres, La Neuveville, Avenches, Bienne et Lyss. Du lundi au vendredi, en français, allemand, anglais, espagnol et portugais. Rendez-vous en ligne ou par WhatsApp.
> Physiotherapie in Ins: Praxis und Hausbesuche im Seeland, auf Deutsch und Französisch.

(573 caracteres. El horario exacto se pone en su campo, una vez confirmado.)

---

## 7. Página por página

### Home y páginas clave
| Página | Palabras | H2 | FAQ | Schema propio | Prioridad | Qué falla |
|---|---|---|---|---|---|---|
| `/` | 2006 | 10 | 10 | FAQPage, Physiotherapy | CRÍTICA | title genérico (sin keyword ni ciudad); meta larga (189); meta menciona receta/LAMal/cobertura (política del cliente); promesa «cette semaine» (usar «dans la semaine dans la plupart des cas») |
| `/reservation-en-ligne/` | 297 | 3 | 2 | — | ALTA | title genérico (sin keyword ni ciudad); H1 sin ubicación; 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/nous-trouver/` | 334 | 3 | 0 | — | ALTA | title genérico (sin keyword ni ciudad) |
| `/contact/` | 577 | 5 | 0 | — | ALTA | title genérico (sin keyword ni ciudad) |
| `/pour-les-patients/` | 166 | 2 | 0 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta larga (169); meta menciona receta/LAMal/cobertura (política del cliente); H1 sin ubicación |
| `/a-propos-de-nous/` | 1544 | 9 | 5 | AboutPage, FAQPage, Physiotherapy | ALTA | title genérico (sin keyword ni ciudad); 10 imágenes sin alt |

### Servicios y dolencias
| Página | Palabras | H2 | FAQ | Schema propio | Prioridad | Qué falla |
|---|---|---|---|---|---|---|
| `/physio/` | 445 | 3 | 3 | — | ALTA | title genérico (sin keyword ni ciudad); contenido corto (445 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/physiotherapeute-a-domicile/` | 739 | 4 | 5 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta larga (184); meta menciona receta/LAMal/cobertura (política del cliente); H1 sin ubicación; 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/physioactiva-bandage-neuromusculaire/` | 379 | 3 | 4 | — | ALTA | title genérico (sin keyword ni ciudad); H1 sin ubicación; contenido corto (379 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/douleur-cervicale-au-cou/` | 578 | 4 | 4 | — | CRÍTICA | meta menciona receta/LAMal/cobertura (política del cliente); contenido corto (578 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/douleur-du-genou-lesions-de-la-cheville/` | 655 | 4 | 4 | — | ALTA | contenido corto (655 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/drainage-lymphatique/` | 388 | 4 | 0 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta menciona receta/LAMal/cobertura (política del cliente); contenido corto (388 palabras); 0 enlaces internos en el contenido |
| `/fitness-medical/` | 737 | 7 | 4 | — | ALTA | title genérico (sin keyword ni ciudad); H1 sin ubicación; 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/lesions-de-lepaule/` | 610 | 4 | 4 | — | ALTA | meta larga (178); H1 sin ubicación; contenido corto (610 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/mal-de-dos-lombaire/` | 633 | 4 | 4 | — | CRÍTICA | meta larga (172); meta menciona receta/LAMal/cobertura (política del cliente); contenido corto (633 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/massage-therapeutique/` | 351 | 4 | 3 | — | ALTA | title genérico (sin keyword ni ciudad); contenido corto (351 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/medical-training-therapy-mtt/` | 368 | 3 | 2 | — | ALTA | contenido corto (368 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/physioactiva-ondes-de-choc/` | 467 | 3 | 5 | — | ALTA | title genérico (sin keyword ni ciudad); H1 sin ubicación; contenido corto (467 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/physiotherapie-cardiorespiratoire/` | 545 | 4 | 4 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta menciona receta/LAMal/cobertura (política del cliente); contenido corto (545 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/physiotherapie-du-plancher-pelvien/` | 628 | 4 | 4 | — | CRÍTICA | meta larga (245); meta menciona receta/LAMal/cobertura (política del cliente); H1 sin ubicación; contenido corto (628 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage; respuesta lenta (3.53 s) |
| `/physio-du-sport/` | 442 | 4 | 3 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta menciona receta/LAMal/cobertura (política del cliente); contenido corto (442 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/physio-en-uro-gynecologie/` | 457 | 4 | 4 | — | ALTA | title genérico (sin keyword ni ciudad); contenido corto (457 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/physio-generale/` | 326 | 3 | 4 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta menciona receta/LAMal/cobertura (política del cliente); H1 sin ubicación; contenido corto (326 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/physiotherapie-neurologique/` | 546 | 4 | 4 | — | CRÍTICA | meta larga (176); meta menciona receta/LAMal/cobertura (política del cliente); H1 sin ubicación; contenido corto (546 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/therapie-manuelle/` | 386 | 3 | 4 | — | ALTA | title genérico (sin keyword ni ciudad); H1 sin ubicación; contenido corto (386 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/tecar-therapie/` | 431 | 3 | 5 | — | ALTA | title genérico (sin keyword ni ciudad); meta larga (201); H1 sin ubicación; contenido corto (431 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/physiotherapie-post-operatoire/` | 400 | 4 | 3 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta menciona receta/LAMal/cobertura (política del cliente); contenido corto (400 palabras); FAQ visible sin schema FAQPage |
| `/physioactiva-puncture-seche/` | 458 | 3 | 5 | — | ALTA | title genérico (sin keyword ni ciudad); H1 sin ubicación; contenido corto (458 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |
| `/physiotemporo-mandibulaire-atm/` | 532 | 4 | 3 | — | ALTA | H1 sin ubicación; contenido corto (532 palabras); 0 enlaces internos en el contenido; FAQ visible sin schema FAQPage |

### Páginas de ciudad
| Página | Palabras | H2 | FAQ | Schema propio | Prioridad | Qué falla |
|---|---|---|---|---|---|---|
| `/physio-a-neuchatel/` | 1596 | 11 | 9 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (72) |
| `/physio-a-ins/` | 2298 | 12 | 9 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (72); 2 imágenes sin alt |
| `/physio-a-bienne/` | 1573 | 11 | 10 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (76); 2 imágenes sin alt; respuesta lenta (3.04 s) |
| `/physio-a-sugiez/` | 2370 | 12 | 9 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (74); 1 imágenes sin alt |
| `/physio-a-morat/` | 2278 | 12 | 9 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (75); 2 imágenes sin alt |
| `/physio-a-kerzers/` | 2259 | 13 | 9 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (73) |
| `/physio-a-lyss/` | 2211 | 13 | 9 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (75); 1 imágenes sin alt |
| `/physio-a-fribourg/` | 2139 | 13 | 9 | FAQPage, Physiotherapy, Service | MEDIA | title largo (67) |
| `/physio-a-payerne/` | 2101 | 13 | 9 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (72); 2 imágenes sin alt |
| `/physio-a-yverdon/` | 2262 | 14 | 10 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (69); 2 imágenes sin alt |
| `/physio-a-lausanne/` | 2384 | 14 | 10 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (74); 2 imágenes sin alt |
| `/physio-a-la-neuveville/` | 2287 | 14 | 10 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (75); 2 imágenes sin alt |
| `/physio-a-avenches/` | 2306 | 15 | 10 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (74); 2 imágenes sin alt |
| `/physio-a-yvonand/` | 2020 | 13 | 9 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (65) |
| `/physio-a-estavayer/` | 2111 | 13 | 9 | FAQPage, Physiotherapy, Service | ALTA | marca duplicada en el title; title largo (66); 1 imágenes sin alt |

### Reserva, legales y blog
| Página | Palabras | H2 | FAQ | Schema propio | Prioridad | Qué falla |
|---|---|---|---|---|---|---|
| `/politique-de-donnees/` | 570 | 8 | 0 | — | CRÍTICA | title genérico (sin keyword ni ciudad); sin meta description; debería ser noindex |
| `/reserver-maintenant/` | 1319 | 8 | 12 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta menciona receta/LAMal/cobertura (política del cliente); promesa «cette semaine» (usar «dans la semaine dans la plupart des cas»); FAQ visible sin schema FAQPage; debería ser noindex |
| `/reserve/` | 491 | 4 | 0 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta menciona receta/LAMal/cobertura (política del cliente); promesa «cette semaine» (usar «dans la semaine dans la plupart des cas»); debería ser noindex |
| `/rendez-vous-online/` | 928 | 8 | 0 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta menciona receta/LAMal/cobertura (política del cliente); promesa «cette semaine» (usar «dans la semaine dans la plupart des cas»); debería ser noindex |
| `/merci/` | 43 | 0 | 0 | — | CRÍTICA | title genérico (sin keyword ni ciudad); sin meta description; debería ser noindex |
| `/online-termin-buchen/` | 1427 | 11 | 12 | — | CRÍTICA | title genérico (sin keyword ni ciudad); meta menciona receta/LAMal/cobertura (política del cliente); FAQ visible sin schema FAQPage |
| `/2026/06/27/perte-de-poids-et-sante-musculaire/` | 317 | 5 | 0 | Article, Person | CRÍTICA | title genérico (sin keyword ni ciudad); plantilla de entrada muestra el MISMO artículo (contenido duplicado) |
| `/2026/06/27/sante-musculo-squelettique/` | 317 | 5 | 0 | Article, Person | CRÍTICA | title genérico (sin keyword ni ciudad); plantilla de entrada muestra el MISMO artículo (contenido duplicado) |
| `/2026/06/27/physiotherapie-a-domicile/` | 317 | 5 | 0 | Article, Person | CRÍTICA | plantilla de entrada muestra el MISMO artículo (contenido duplicado) |
| `/2026/09/11/physiotherapie-a-sugiez/` | 317 | 5 | 0 | Article, Person | CRÍTICA | promesa «cette semaine» (usar «dans la semaine dans la plupart des cas»); plantilla de entrada muestra el MISMO artículo (contenido duplicado) |

---

## 8. Plan de trabajo propuesto

1. **Hoy, en 30 minutos:**
   - title y meta de la home;
   - borrar la marca duplicada en las 14 ciudades;
   - poner noindex a las 5 páginas indicadas;
   - corregir el horario de la ficha de Google.
2. **Esta semana:**
   - arreglar la plantilla del blog;
   - hacer las 301 de MTT y de suelo pélvico;
   - completar la ficha de Google (categorías, servicios, descripción, web con UTM, WhatsApp);
   - poner en marcha el sistema de reseñas.
3. **Home como plantilla de Elementor editable** (.zip con widgets nativos, como las ciudades), con el schema unificado con Yoast.
4. **Las 20 páginas de servicio**, una a una, con el método del ebook: keyword con datos, H1-H3, 900-1.200 palabras, enlaces a ciudades y dolencias, FAQ con schema, Service schema y plantilla editable. Primero las que tienen demanda: drainage lymphatique, massage, fitness médical, physio à domicile y physio du sport.
5. **Cada semana:** una publicación en la ficha de Google, fotos nuevas cada mes, 4-6 reseñas al mes y un informe mensual.
