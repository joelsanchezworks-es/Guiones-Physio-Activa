Escribe guiones orgánicos (Reels 9:16) siguiendo CLAUDE.md y prompts/sistema.md.
Opciones del usuario: $ARGUMENTS
Si no indica nada: 4 guiones de 20–45 s, en francés + alemán, mezclando educativo, mito vs. realidad, detrás de cámaras y preguntas frecuentes.
Cada guion: 5 hooks de tipos distintos (tres capas, uno recomendado), bloques Gancho, Valor y CTA suave (guardar, compartir, seguir o «escríbenos»), texto del post y 5 hashtags por idioma, notas de grabación y pendientes. No repitas hooks de guiones anteriores de salidas/.

Pasos:
1. Guarda cada guion como un JSON con "uso": "organico" en salidas/AAAA-MM-DD/guion-[tema-corto].json siguiendo EXACTAMENTE prompts/formato-guion.md (copy: { "fr": { "post": "…", "hashtags": ["#…"] } }).
2. Ejecuta npm run build para validar; si avisa de JSON no válido, corrígelo.
3. Haz commit y push.
4. Responde en el chat SOLO con una línea por guion: título, ángulo, hook recomendado (FR) y el enlace VISOR_URL/#/[id].
