# Menú Physio Activa: cómo montarlo

Archivo: `menu-elementor.html` (HTML + CSS + JS en un solo bloque).

1. **Copia de seguridad del header actual:** Plantillas → Theme Builder → Header → … → Exportar.
2. Edita el header con Elementor y **borra los widgets actuales** del menú, el logo, la barra superior y el botón de WhatsApp (este bloque los sustituye a todos).
3. Añade **un widget HTML** a todo el ancho (sección o contenedor «Ancho completo», padding 0) y pega **todo** el contenido de `menu-elementor.html`.
4. En los ajustes de esa sección o contenedor: **padding 0, gap 0**. No hace falta activar «Sticky» de Elementor: el menú ya se queda fijo al hacer scroll.
5. Guarda, publica y comprueba en escritorio y móvil:
   - los 3 desplegables;
   - el panel móvil (☰ abre, ✕ cierra);
   - el botón de WhatsApp;
   - la página activa resaltada.
6. **Menú:** Accueil · À propos de nous · Nos Zones (submenú con las 15 localidades, con el título y el slug de la tabla) · Contact · Accès.
   - Las 6 zonas del lote B (Morat, Chiètres, Estavayer, Yvonand, Yverdon, Lausanne) están en el submenú. Para que sus enlaces no den 404, **publícalas** con **noindex** en Yoast (no las dejes como borrador). Si prefieres no mostrarlas hasta que el cliente confirme, borra sus 6 líneas `<li>` del submenú.
7. Las URLs del menú son las finales (ver `../6_elementor/menu.md`). Las páginas de patologías y de zonas tienen que existir con esos slugs; mientras no estén publicadas, esos enlaces darán 404.

Notas:
- Se ha quitado el selector de idioma por petición del cliente. Si más adelante se publica la versión alemana, se añade un enlace a `/de/`.
- TikTok no aparece porque no se encontró el perfil: pásanos el enlace y se añade.
- Si el tema muestra su propio menú además de este, desactiva el header del tema (Elementor → Theme Builder → Header aplicado a «Todo el sitio»).
