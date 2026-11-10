# Páginas de ciudad con widgets editables de Elementor (Ins, Bienne…)

## Archivos
- `physio-a-ins/physio-a-ins.zip`, o el `.json` de dentro: se importan en **Plantillas › Plantillas guardadas › Importar plantillas**. Sirve el .zip o el .json.
- `physio-a-ins/yoast.txt`: título SEO, meta descripción, slug `/physio-a-ins/` y keyword principal «physio ins».
- `physio-a-ins/preview.html`: vista previa aproximada (no se sube).

## Imágenes: la plantilla se importa SIN fotos
Elementor descarga y vuelve a subir a la biblioteca cada imagen que encuentra en una plantilla importada, y por eso se creaban duplicados. Ahora la plantilla trae todos los huecos de imagen vacíos:
- **Hero:** fondo azul oscuro. Ve a la sección › Estilo › Fondo y elige la foto de la ciudad o del cabinet.
- **Imágenes 1 y 2 del artículo:** marcador gris. Elige la foto en el widget Imagen. El texto alternativo sugerido está en `yoast.txt`.
- **CTA final:** fondo azul oscuro con la capa ya puesta. Elige la foto en la sección › Estilo › Fondo.

Si ya importaste versiones anteriores, borra de la biblioteca de medios los duplicados que se crearon (los «Physio-Activa-00036», «-00031» y «Centerbild…» repetidos).

## Montaje
1. Importa el .zip.
2. Crea la página «Physio à Ins» con el slug `/physio-a-ins/`. Edita con Elementor › carpeta › «Mis plantillas» › Insertar.
3. Rellena Yoast según `yoast.txt` (indexar: sí).
4. El menú ya enlaza Ins a `/physio-a-ins/` (en `8_menu/menu-elementor.html`, sustituye el menú anterior).

## Qué se edita desde el panel (todo nativo)
| Bloque | Widget | Cómo editarlo |
|---|---|---|
| Hero | Sección con **imagen de fondo** y capa oscura + Encabezados (H1) + Botones | Sección › Estilo › Fondo (elige la foto de la biblioteca de medios) |
| Migas | Editor de texto | Texto |
| Intro y bloques del artículo | Encabezado (H2) + Editor de texto (párrafos, H3, enlaces) | Directamente en el editor visual |
| Imágenes | Imagen | Imagen y texto alternativo |
| «Pourquoi» (4 tarjetas) | Cuadro de icono | Icono, título y texto |
| FAQ | **Acordeón con «FAQ Schema» activado** | Preguntas y respuestas. Elementor genera el schema FAQPage solo |
| CTA final | Sección con imagen de fondo oscurecida + Botones | Fondo, título, texto y botones |
| Mapa | Google Maps | Dirección |

Solo hay tres widgets HTML, que no hace falta tocar:
- **Estilos**, el primero: el CSS del diseño pa-lp.
- **Ficha «en bref»**: una tabla, para que Google y las IA extraigan los datos.
- **Final**: el botón flotante de WhatsApp y el schema local (Physiotherapy, WebPage, Service).

**Importante:** no quites las **clases CSS** de las secciones y widgets (`pa-lp`, `pa-hero`, `pa-btn`, `pa-h2`, `pa-faq`…, en Avanzado › Clases CSS). De ellas depende el diseño.

## SEO
- Keywords (DataForSEO, Suiza): «physio ins» 140/mes y «physiotherapie ins» 50/mes.
  - El title, el H1, la primera frase y los H2 contienen «physio à Ins», «physiothérapeute à Ins» y «physiothérapie à Ins».
  - Hay una frase y una FAQ en alemán para captar «Physiotherapie Ins».
- Enlaces internos a 5 páginas de ciudad, a las pathologies, a domicilio y a MTT.
- Ningún precio, receta ni detalle de seguro: solo la frase aprobada del cliente.
- **Canibalización con la home:** enlaza desde la home a `/physio-a-ins/` con el anchor «physio à Ins». Deja la home para la marca y la región.
