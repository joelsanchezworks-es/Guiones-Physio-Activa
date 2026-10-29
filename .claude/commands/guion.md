Genera un guion de Reel completo a partir de un tema, siguiendo CLAUDE.md y prompts/sistema.md.

Tema e indicaciones del usuario: $ARGUMENTS

Si no hay tema, pregunta solo el tema en una línea. Si hay tema, no preguntes nada más: decide tú lo que falte.

Valores por defecto (el usuario puede cambiarlos en el mismo mensaje):
- Uso: ads (si dice "orgánico", es orgánico). Formato siempre Reel 9:16.
- Idioma: francés + alemán (si dice "solo FR" o "solo DE", respétalo).
- Ángulo: el que mejor encaje con el tema (A–G).

Contenido: ficha, 5 hooks de tipos distintos con tres capas y uno recomendado, guion por bloques (ads 20–30 s: gancho, problema, solución, prueba, CTA con filtro de intención; orgánico 20–45 s: gancho, valor, CTA suave), versión en cada idioma, copy, notas de grabación y pendientes. No repitas hooks de guiones anteriores de salidas/. Añade en cada texto (hooks, bloques y copy) la traducción al español en la clave "es", solo como referencia para el equipo.

Aplica contexto/aprendizajes-copys.md: un anuncio, una idea; hook de 12 palabras o menos; CTA concreto con filtro de intención; nada de afirmaciones marcadas como [POR CONFIRMAR].

Pasos:
1. Guarda el guion en salidas/AAAA-MM-DD/guion-[tema-corto].json siguiendo EXACTAMENTE prompts/formato-guion.md.
2. Ejecuta npm run build para validar; si avisa de JSON no válido, corrígelo.
3. Haz commit y push a la rama de trabajo y a `main` (ver «Publicar en main» en CLAUDE.md).
4. Responde en el chat SOLO con: título, ángulo elegido, hook recomendado (FR) y el enlace VISOR_URL/#/[id]. No pegues el guion entero ni generes HTML o PDF.
