# physioactiva-seo

Investigación SEO en francés de physioactiva.ch (physio + patologías · Ins / Seeland / Trois-Lacs) con DataForSEO.

- **Entregables:** `entregables/index.html` (abre sin conexión) y `entregables/physioactiva-seo.xlsx`.
- **Páginas en francés:** `entregables/5_paginas/<slug>/` (`fr.md`, `fr.html`, `fr-ascii.html`, `yoast.txt`, `schema.json`, `brief.md`).
- **Datos:** `data/keywords.csv`, `data/clusters.json`, `data/hallazgos.json`, `data/arquitectura.csv`, `data/costes.csv`.
- **Reproducir:** `./run_all.sh` (usa la caché de `data/cache/`; con la caché vigente no vuelve a gastar).
- **Decisiones y umbrales:** `decisiones.md`, `config/`.
- **Elementor:** `entregables/6_elementor/index.html` (25 páginas: `elementor.json`, `preview.html`, `yoast.txt`, `checklist.md`), `PUBLICAR.md`, `PREGUNTAS_CLIENTE.md`, `menu.md`, `redirecciones.csv`. Reconstruir: `python3 scripts/construir_pagina.py && python3 scripts/construir_pagina.py --css-global && python3 scripts/validar_elementor.py && python3 scripts/cierre_elementor.py`.
