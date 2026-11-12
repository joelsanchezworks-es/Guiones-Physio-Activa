# Guía SEO para el montaje de physioactiva.ch

Prácticas para dejar el sitio optimizado al montarlo y mantenerlo después. Está adaptada a este sitio: WordPress + Elementor (páginas importadas desde `6_elementor/`) + Yoast SEO, ficha de Google en Ins y 8 zonas publicables. Complementa a `PUBLICAR.md`, que dice qué página montar, en qué orden y cómo; esta guía cubre lo que hay alrededor para que posicione.

Las prioridades salen de la auditoría del 06.11.2026 (`../2_auditoria_tecnica_local.html`). Ningún objetivo numérico de esta guía es una promesa: se mide con Search Console, GA4 y DataForSEO.

---

## 0. Antes de tocar nada (día 0)

- [ ] **Copia de seguridad completa** del sitio (archivos y base de datos) con el plugin de copias o desde el hosting. Guárdala fuera del servidor.
- [ ] Si el hosting lo permite, **monta primero en un entorno de staging** y pasa a producción cuando esté revisado. Si no, usa los borradores `-v2` de `PUBLICAR.md`.
- [ ] **Google Search Console:** verifica la propiedad de dominio `physioactiva.ch` (registro DNS). Exporta antes del cambio el informe de rendimiento de los últimos 16 meses: es la línea base para medir la mejora.
- [ ] **Bing Webmaster Tools:** importa la propiedad desde Search Console (2 minutos).
- [ ] **GA4:** comprueba que la etiqueta carga en todas las páginas (Tag Assistant).
- [ ] Anota la posición actual de las 10 búsquedas clave (sección 9) para compararla después.

## 1. Ajustes de WordPress y Yoast (una vez)

### WordPress
- [ ] Ajustes → Generales → **Idioma del sitio: «Français (Suisse)»**, para que el sitio declare `lang="fr-CH"` y no `fr-FR`.
- [ ] Ajustes → Enlaces permanentes: **«Nombre de la entrada»** (`/%postname%/`). No lo cambies después: rompería todas las URL.
- [ ] Ajustes → Lectura: **desmarca** «Disuadir a los motores de búsqueda…» en producción.
- [ ] Borra plugins y temas que no se usen y actualiza los que quedan.

### Yoast SEO
- [ ] **Tipos de contenido:** Páginas y Entradas indexables; plantilla de título `%%title%% %%sep%% %%sitename%%`. En las páginas nuevas el title se escribe a mano desde `yoast.txt`.
- [ ] **Archivos de autor:** desactivados (hoy `/author/joel/` muestra «Joel Nova Agency»: no aporta nada y no es un fisioterapeuta).
- [ ] **Categorías y etiquetas:** noindex mientras el blog tenga pocos artículos.
- [ ] **Páginas de adjuntos (medios):** redirigir al archivo (opción por defecto de Yoast; compruébala).
- [ ] **`/merci/`:** noindex y fuera del sitemap (Avanzado → «¿Permitir que los motores muestren esta página?» = No).
- [ ] **Organización:** nombre «Physio Activa», logo cuadrado (≥ 112 × 112 px) y perfiles sociales reales (Google Business Profile, Facebook o Instagram si existen).
- [ ] **Schema:** las páginas importadas ya llevan su propio JSON-LD (clínica `Physiotherapy` con dirección, horario y zonas atendidas, `MedicalWebPage` o `WebPage`, `FAQPage`, `Service` en las zonas y `AboutPage` + `Person` en À propos). Yoast añade Organización, WebSite, WebPage y BreadcrumbList; no se pisan. **No añadas otro bloque de FAQ** con un plugin ni con el widget FAQ de Elementor: duplicaría la FAQ.
- [ ] Tras publicar cada plantilla, pasa una URL de muestra por la **prueba de resultados enriquecidos** (search.google.com/test/rich-results) y por validator.schema.org: no debe haber errores.

### Elementor
- [ ] Elementor → Ajustes → Funciones: activa **«Carga mejorada de recursos»**, **«Iconos de fuente en línea»** y **«Rendimiento optimizado del DOM»** si tu versión las tiene.
- [ ] Cada página: plantilla **«Elementor Canvas»** (o «Pleine largeur» si el header y el footer los pone el Theme Builder) y **título del tema oculto**, para que no salga un segundo H1.
- [ ] Botones del header y del footer: nunca `#`. Reserva → `/reservation-en-ligne/`, teléfono → `tel:+41766273838`, WhatsApp → `https://wa.me/41766273838`.

## 2. Indexación y arquitectura

- [ ] **Una sola página de reserva:** `/reservation-en-ligne/`. Importa `redirecciones.csv` en el plugin Redirection **después** de publicar las páginas de destino.
- [ ] **Menú y pie con URLs finales** (ver `menu.md`): con barra final y sin redirecciones. Hoy el menú enlaza a `/mal-de-dos`, `/fitness-medica/`… que redirigen.
- [ ] **Hub de patologías** `/pour-les-patients/` en el menú: hoy enlaza a 5 URL que dan 404. Al importar su JSON se arregla.
- [ ] **Zonas del lote B** (Morat, Chiètres, Estavayer, Yvonand, Yverdon, Lausanne): en borrador o noindex y fuera del menú hasta que el cliente confirme que atiende allí.
- [ ] **Versión `/de/`:** hoy tiene títulos y metas en francés y duplica la versión FR. Hasta que se traduzca de verdad, pon noindex en `/de/` (o tradúcela: es la fase siguiente). El hreflang debe declarar `fr-CH` y `de-CH`.
- [ ] **Blog:** los 4 artículos muestran el mismo contenido (el de drenaje linfático). Recupera el contenido propio de cada uno o despublícalos (con 301 a la página del tema).
- [ ] **Sitemap:** Yoast → `sitemap_index.xml`. Comprueba que solo contiene páginas indexables (sin `/merci/`, autor, categorías ni lote B). Envíalo en Search Console y en Bing.
- [ ] Después de publicar, **Inspección de URLs → Solicitar indexación** para la home, el hub, las 7 patologías y las 8 zonas del lote A (como mucho unas 10-15 al día).

## 3. Contenido y on-page en cada página

Las páginas importadas ya cumplen esto (lo comprueba `validar_elementor.py`). Para cualquier página nueva o editada después:

- [ ] **Un solo H1**, con la búsqueda principal y la localidad («Physio à Lyss : …»). Después H2 → H3, sin saltos de nivel.
- [ ] **Title ≤ 60 caracteres** con keyword + localidad + «Physio Activa»; **meta 120-155** con localidad, servicio y una llamada a la acción (`yoast.txt`).
- [ ] **Respuesta directa en las 2-3 primeras líneas**: es lo que leen Google y las respuestas de IA (AI Overview).
- [ ] **La ciudad en el title, el H1 y 2-4 H2, nunca en los H3.** Sin repetirla de forma artificial.
- [ ] **FAQ de 8-10 preguntas reales**, sacadas de las «Autres questions posées» de Google (`data/paa_banco.json`), con las 3 preguntas estándar al principio.
- [ ] **Enlaces internos con anchor descriptivo** («physio pour une sciatique», no «cliquez ici»):
  - patología → técnicas que usa, domicilio y reserva;
  - zona → zonas vecinas y patologías;
  - home → hub, patologías y zonas.
- [ ] **CTA en tres puntos** (hero, tras el proceso y al final) con reserva, teléfono y WhatsApp.
- [ ] **Imágenes:** nombre de archivo descriptivo en francés (`physiotherapie-genou-ins.jpg`), `alt` que describa la imagen, formato WebP, ancho máximo 1.600 px y menos de 200 KB. Nada de fotos de banco presentadas como el cabinet (ver `pendientes_imagenes.md`).
- [ ] **Publicidad sanitaria suiza:** sin testimonios, sin promesas de resultado, sin cifras de éxito, sin comparaciones con otros profesionales. Señales de alarma → médico o 144.
- [ ] **E-E-A-T:** nombre y titulación de quien revisa cada página de patología («Revu par …, physiothérapeute») cuando el cliente los confirme, y fecha de revisión visible.

## 4. Rendimiento (Core Web Vitals)

Objetivos de Google, medidos en móvil: **LCP < 2,5 s · INP < 200 ms · CLS < 0,1**.

- [ ] **Plugin de caché** según el hosting: LiteSpeed Cache (servidores LiteSpeed) o WP Rocket. Activa:
  - caché de página;
  - minificación y combinación de CSS/JS;
  - diferido de JS;
  - lazy load de imágenes e iframes (el mapa ya va en `loading="lazy"`).
- [ ] **Versión ligera de las páginas** (recomendada cuando todo funcione):
  1. Carga `global/pa-styles.css` en todo el sitio (Elementor → Ajustes del sitio → CSS personalizado, o WPCode).
  2. Carga las fuentes y Font Awesome con `<link>` + `preconnect` en el `<head>`.
  3. Carga `global/pa-scripts.js` en el pie.
  4. Importa `elementor-css-global.json` en lugar de `elementor.json`.

  Así cada página deja de repetir ~20 KB de CSS y JS (detalle en `PUBLICAR.md`).
- [ ] **Fuentes:** Poppins e Inter con `display=swap` (ya lo llevan). Mejor aún, alójalas en local (Elementor → Ajustes → «Cargar fuentes de Google localmente», o el plugin OMGF).
- [ ] **Vídeo de la home:** comprímelo (720p, ≤ 2-3 MB, H.264). Ya tiene `poster` y `preload="metadata"`.
- [ ] **Imágenes del hero:** no las pongas en lazy load (son el LCP).
- [ ] Mide **cada plantilla** (home, una patología, una zona) en PageSpeed Insights antes y después, y guarda las capturas.

## 5. SEO local: ficha de Google (el canal que hoy funciona mejor)

Physio Activa ya sale en el local pack de 33 búsquedas desde Ins. Cuidarlo es la acción con más retorno.

- [ ] **Coherencia de datos (NAP):** el mismo nombre, dirección y teléfono que la web:
  - Nombre: «Physio Activa».
  - Dirección: «Rämismatte 21, 3232 Ins». Confirmar con el cliente: el encargo decía 31.
  - Teléfono: 076 627 38 38.
- [ ] **Horario:** la ficha dice lunes a viernes de 8:30 a 19:30 y la web «jusqu'à 20h». **Iguálalos** en la ficha y en la web.
- [ ] **Web de la ficha:** `https://physioactiva.ch/?utm_source=google&utm_medium=organic&utm_campaign=gbp` (hoy apunta a `http://www…`).
- [ ] **Categorías:** principal «Physiothérapeute»; secundaria «Centre de rééducation» (ya está). No añadas categorías de servicios que no prestas.
- [ ] **Servicios:** da de alta en la ficha los mismos servicios que tienen página (physio à domicile, drainage lymphatique, MTT, thérapie manuelle, physio du sport…), con una descripción breve y sin promesas.
- [ ] **Zona de servicio:** las localidades donde se va a domicilio de verdad (solo las confirmadas).
- [ ] **Botón de reserva:** enlace a OneDoc.
- [ ] **Fotos reales:** cabinet, InsGym, equipo y atención a domicilio con permiso. Sube 2-4 al mes.
- [ ] **Publicaciones:** 1 cada 1-2 semanas (consejo útil + enlace a la página correspondiente).
- [ ] **Reseñas:**
  - pide la reseña al terminar el tratamiento, con un QR en el cabinet y un enlace por WhatsApp;
  - sin incentivos y sin filtrar quién la deja;
  - responde a todas (hoy 19 de 19 respondidas: mantenlo);
  - no copies reseñas en la web como testimonios.
- [ ] **Directorios con el mismo NAP:** local.ch, search.ch, OneDoc, Apple Business Connect (Apple Maps), Bing Places, physioswiss (si sois miembros), Moneyhouse (datos de la empresa). Además, los que enlazan a la competencia y no a Physio Activa: physio-verzeichnis.ch, regionalinfo-schweiz.ch, better-search.ch y oeffnungszeitenbuch.de.

## 6. Autoridad y enlaces

- [ ] Enlaces locales reales:
  - InsGym (página de partners o servicios);
  - clubes deportivos de Ins y del Seeland;
  - comuna de Ins (listado de salud);
  - asociaciones de pacientes y de personas mayores;
  - prensa local (Bieler Tagblatt, Murtenbieter, La Liberté).
- [ ] **No compres enlaces.** El sitio ya recibe enlaces spam tipo «PBN / backlinks»: vigílalos en Search Console → Enlaces. Usa el archivo disavow solo si aparece una acción manual.
- [ ] Cada enlace nuevo debe apuntar a la página más relevante (por ejemplo, un club de running → `/douleur-pied-cheville-fasciite-plantaire/` o `/physio-du-sport/`), no siempre a la home.

## 7. Medición (sin esto no se sabe qué funciona)

- [ ] **Eventos en GA4** (con Google Tag Manager o el plugin de GA4), marcados como conversiones clave:
  - `click_whatsapp` (enlaces `wa.me`);
  - `click_telefono` (enlaces `tel:`);
  - `click_onedoc` (enlaces a onedoc.ch);
  - `click_reserva` (enlaces a `/reservation-en-ligne/`).
- [ ] **UTM** en la ficha de Google (sección 5) y en las publicaciones de redes sociales.
- [ ] **Search Console:** revisa cada semana Indexación de páginas, Experiencia y Rendimiento; filtra por las páginas nuevas.
- [ ] **Informe mensual:**
  - clics e impresiones (Search Console);
  - conversiones (GA4);
  - posición de las búsquedas clave;
  - reseñas nuevas.

  Las búsquedas clave y su volumen están en `../1_investigacion_keywords.html`. Cuando quieras, vuelvo a medir las posiciones con DataForSEO y lo comparo con la línea base del 06.11.2026.

## 8. Mantenimiento y crecimiento (meses 2-12)

- [ ] **Resolver `PREGUNTAS_CLIENTE.md`** (domicilio por localidad, titulaciones, duración de la sesión…), regenerar las páginas y publicar las zonas del lote B que se confirmen. Los enlaces entre zonas aparecen solos al regenerar.
- [ ] **Actualizar cada página de patología** una vez al año como mínimo: revisión clínica, fecha y FAQ con las preguntas nuevas que muestre Google.
- [ ] **Nuevas páginas por orden de prioridad** (`../4_estrategia_roadmap.html`): técnicas con mucho volumen (drainage lymphatique, dry needling, taping, MTT) con la misma receta, y después los clústeres candidatos (ménisque, périostite, coiffe des rotateurs, prothèse du genou). Las patologías marcadas ⚠ (épicondylite / canal carpien, vertiges, fibromyalgie) solo si el cliente las trata.
- [ ] **Blog:** 1-2 artículos al mes que respondan preguntas reales («Est-ce normal d'avoir plus mal après une séance ?», «Comment choisir son physiothérapeute ?»…) y enlacen a la página de patología o de zona.
- [ ] **Versión alemana (fase 2):** traducción real (no automática) de las páginas clave con hreflang `fr-CH` / `de-CH`. Prioridades: Hausbesuch, Kreuzschmerzen, Beckenboden y Physiotherapie Murten/Kerzers/Lyss/Biel. Morat y Chiètres tienen demanda en alemán, no en francés.

## 9. Comprobación después del montaje

**Día 1 (cada URL publicada):**
- [ ] responde 200;
- [ ] un solo H1;
- [ ] ningún botón en `#`;
- [ ] título del tema oculto;
- [ ] FAQ que abre y cierra;
- [ ] mapa visible;
- [ ] schema sin errores;
- [ ] noindex solo en el lote B.

**Semana 1:**
- [ ] redirecciones activas y sin cadenas (`/reserver-maintenant/` → `/reservation-en-ligne/` en un solo salto);
- [ ] sitemap enviado;
- [ ] indexación solicitada;
- [ ] PageSpeed medido;
- [ ] ficha de Google corregida (horario, URL con UTM, servicios).

**Semana 2:** pídeme la **verificación por rastreo** con la lista de URLs del final de `PUBLICAR.md`. Compruebo estado, H1, enlaces, botones, schema, noindex y redirecciones en todo el sitio.

**Mes 1-3:** en Search Console, las páginas nuevas deben pasar a «Indexadas» y empezar a tener impresiones en sus búsquedas (patologías y zonas). Si alguna sigue en «Descubierta: actualmente sin indexar», revisa sus enlaces internos y vuelve a solicitar la indexación.

### Búsquedas clave para seguir (volumen mensual en Suiza, DataForSEO, 06.11.2026)

| Búsqueda | Volumen | Página |
|---|---|---|
| physio ins | 140 | `/` |
| physio biel / physiothérapeute bienne | 720 / 320 | `/physio-a-bienne/` |
| physio neuchatel / physiothérapie neuchatel | 590 / 390 | `/physio-a-neuchatel/` |
| physio lyss | 390 | `/physio-a-lyss/` |
| physio payerne | 320 | `/physio-a-payerne/` |
| physiothérapie fribourg | 260 | `/physio-a-fribourg/` |
| physio vully | 110 | `/physio-a-sugiez/` |
| lombalgie / douleur en bas du dos | 880 / 880 | `/mal-de-dos-lombaire/` |
| fasciite plantaire | 2.400 | `/douleur-pied-cheville-fasciite-plantaire/` |
| ménisque | 1.600 | `/douleur-du-genou-lesions-de-la-cheville/` |
| drainage lymphatique | 5.400 | `/drainage-lymphatique/` (optimizar en la fase siguiente) |
