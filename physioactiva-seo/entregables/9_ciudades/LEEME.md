# Páginas de ciudad (diseño pa-lp) · cómo montarlas

Cada carpeta `physio-a-<ciudad>/` tiene:
- `elementor.json`: **el único archivo que se importa**. Lleva el CSS, el HTML, el JS y el schema JSON-LD dentro de un solo widget HTML.
- `yoast.txt`: título SEO, meta descripción, slug, palabra clave principal e imagen OG.
- `preview.html`: vista previa local (no se sube).

## Montaje
1. WordPress › Plantillas › Importar `elementor.json`.
2. Crea la página con el slug exacto `/physio-a-<ciudad>/`, inserta la plantilla y publica.
3. Rellena Yoast con lo que indica `yoast.txt` (indexar: sí).

## Imagen de fondo del hero (la cambias tú)
Neuchâtel ya usa su imagen (`Neuchatel-physio.jpg`). Las otras 13 llevan de momento la foto del cabinet, que se ve bien, para que la página no salga rota.

Para poner la de la ciudad:
1. Súbela a la biblioteca de medios. Nombre recomendado: `physio-<ciudad>.jpg`, unos 1920 px de ancho, menos de 300 KB, con texto alternativo «Physio à <Ciudad>».
2. Copia su URL.
3. En el widget HTML, busca `Centerbild_IMG_9184-scaled-1.jpg` (aparece en el `background-image` del hero y en `primaryImageOfPage` del schema) y reemplaza la URL completa en los dos sitios.
4. Cámbiala también en la imagen OG de Yoast.

### Fotos libres sugeridas (Wikimedia Commons)
Si usas una foto CC BY o CC BY-SA, hay que citar al autor y la licencia.

| Ciudad | Archivo en Commons | Licencia · autor |
|---|---|---|
| Sugiez | Murtensee Sugiez.jpg | CC0 · Hadi |
| La Neuveville | La Neuveville BE vom Schiff aus (2017).jpg | CC BY-SA 4.0 · JoachimKohler-HB |
| Chiètres | Kerzers - panoramio.jpg | CC BY-SA 3.0 · Francois Polito |
| Morat | Blick von der Stadtmauer auf Murten mit Schloss und Murtensee (2008).jpg | CC BY-SA 4.0 · JoachimKohler-HB |
| Avenches | Avenches vue du Château.JPG | CC BY-SA 3.0 · Nyro Xeo |
| Lyss | Lyss in winter.JPG (1000 px, algo pequeña) | CC BY-SA 3.0 · Hawkeye29 |
| Bienne | Vue panoramique de Bienne sur le lac et le Jura.jpg | CC0 · Juan-Luis Konitzer |
| Fribourg | Fribourg - Brücken über Saane und Galtera.jpg | CC BY-SA 4.0 · JoachimKohler-HB |
| Payerne | Abbatiale de Payerne - 1.jpg | CC BY-SA 2.5 · Twen |
| Estavayer-le-Lac | Estavayer-le-Lac, Switzerland (Unsplash peOp2E3Zukk).jpg | CC0 · Camille (kmile_ch) |
| Yvonand | Yvonand.JPG | CC0 · Christophe Badoux |
| Yverdon-les-Bains | Château d'Yverdon les Bains.jpg | CC BY-SA 3.0 · Olivier Anh |
| Lausanne | Lausanne-Lac-Léman-2022-04-23.jpg | CC BY-SA 4.0 · Zikai Liu |

Para buscar cada archivo: `https://commons.wikimedia.org/wiki/File:<nombre>`.

## Validación
Ver `validacion.md`. Las 14 páginas pasan:
- sin marcadores y sin receta ni seguro;
- un solo H1, sin saltos de encabezado;
- la FAQ visible coincide con el JSON-LD;
- enlaces internos válidos;
- cada variante (physio / physiothérapeute / physiothérapie + ciudad) aparece al menos 2 veces;
- similitud máxima entre ciudades: 30,5 %.
