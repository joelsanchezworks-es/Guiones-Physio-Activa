Genera un guion de vídeo completo a partir de un tema, siguiendo CLAUDE.md y prompts/sistema.md.

Tema e indicaciones del usuario: $ARGUMENTS

Si el usuario no da tema, pregúntale solo el tema en una línea y espera. Si da tema, no hagas más preguntas: decide tú lo que falte y dilo en una línea al principio.

Valores por defecto (el usuario puede cambiarlos en el mismo mensaje):
- Uso: ads (si dice "orgánico", es orgánico). Formato siempre Reels 9:16.
- Idioma: francés + adaptación al alemán (si dice "solo FR" o "solo DE", respétalo).
- Ángulo: elige el que mejor encaje con el tema (A–F) e indica cuál.

Entrega, en este orden:
1. **Ficha**: tema, ángulo, uso, público, duración, idioma, localización y quién sale.
2. **5 hooks** de tres capas (verbal ≤12 palabras, visual, texto en pantalla ≤6 palabras), cada uno de un tipo distinto, con una hipótesis en español. Marca el recomendado.
3. **Guion del Reel** (ads: 20–30 s; orgánico: 20–45 s) con el hook recomendado, en tabla de dos columnas "Lo que se ve / se graba" | "Lo que se dice", con texto en pantalla y duración por bloque. Ads: gancho, problema, solución y prueba, CTA con filtro de intención. Orgánico: gancho, valor, CTA suave.
4. **Versión en alemán** del guion (adaptación natural), si aplica.
5. **Copy**: ads → texto principal corto (≤125 caracteres), texto largo, titular (≤40 caracteres) y descripción, en cada idioma. Orgánico → texto del post y 5 hashtags.
6. **Notas de grabación y edición**: tomas, material, música (tipo), subtítulos.
7. **Pendientes**: los [POR CONFIRMAR], si hay.

Guarda el resultado en salidas/AAAA-MM-DD/guion-[tema-en-pocas-palabras].md y muéstralo también en la respuesta.
