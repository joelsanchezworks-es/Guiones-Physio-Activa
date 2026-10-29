Genera un guion de Reel completo a partir de un tema, siguiendo CLAUDE.md y prompts/sistema.md.

Tema e indicaciones del usuario: $ARGUMENTS

Reglas:
- Si no hay ningún tema, pregunta solo el tema en una línea y espera.
- Si el tema es ambiguo, **no preguntes**: elige tú ángulo, uso e idioma y dilo en una sola línea al principio (por ejemplo: «Ángulo C · ads · FR + DE»).
- Responde **directamente en el chat** con el guion completo en Markdown.
- No generes HTML ni PDF, no ejecutes `tools/build_entregables.py` y no regeneres el paquete completo ni ejecutes `PROMPT.md`.

Valores por defecto (el usuario puede cambiarlos en el mismo mensaje):
- Uso: ads (si dice «orgánico», es orgánico). Formato siempre Reels 9:16.
- Idioma: francés + adaptación al alemán (si dice «solo FR» o «solo DE», respétalo).
- Ángulo: el que mejor encaje con el tema (A–F).

Entrega, en este orden:
1. **Ficha**: tema, ángulo, uso, público, duración, idioma, localización y quién sale.
2. **5 hooks** de tres capas (verbal ≤12 palabras, visual, texto en pantalla ≤6 palabras), cada uno de un tipo distinto, con una hipótesis en español. Marca el recomendado. Que no repitan hooks de `salidas/2026-10-29/01-banco-de-hooks.csv` ni de `salidas/aprobados.md`.
3. **Guion del Reel** (ads: 20–30 s; orgánico: 20–45 s) con el hook recomendado, en tabla «Lo que se ve / se graba» | «Lo que se dice», con texto en pantalla y duración por bloque. Ads: gancho, problema, solución y prueba, CTA con filtro de intención. Orgánico: gancho, valor, CTA suave.
4. **Versión en alemán** del guion (adaptación natural), si aplica.
5. **Copy**: ads → texto principal corto (≤125 caracteres), texto largo, titular (≤40 caracteres) y descripción, en cada idioma. Orgánico → texto del post y 5 hashtags.
6. **Notas de grabación y edición**: tomas, material, música (tipo), subtítulos.
7. **Pendientes**: los [POR CONFIRMAR], si hay (una lista corta).

Al terminar:
- Guarda **solo** ese guion en `salidas/AAAA-MM-DD/guion-[tema-en-pocas-palabras].md` (fecha de hoy, tema en minúsculas y con guiones).
- Haz commit y push a la rama de trabajo **sin pedir permiso**.
- Cierra la respuesta con una sola línea con la ruta del archivo guardado.
