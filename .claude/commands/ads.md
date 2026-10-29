Escribe guiones de anuncios de respuesta directa (Reels 9:16) siguiendo CLAUDE.md y prompts/sistema.md.
Opciones del usuario: $ARGUMENTS
Si no indica nada: 3 guiones (ángulos A, C y F), francés + alemán, partiendo de salidas/ganadores.md si existe.
Cada guion: 5 hooks de tipos distintos (tres capas, uno recomendado), Reel de 20–30 s por bloques (Gancho, Problema, Solución, Prueba, CTA con filtro de intención), copy de Meta por idioma (corto ≤125 caracteres, largo, titular ≤40 caracteres, descripción), notas de grabación y pendientes. No repitas hooks de guiones anteriores de salidas/.

Pasos:
1. Guarda cada guion como un JSON con "uso": "ads" en salidas/AAAA-MM-DD/guion-[tema-corto].json siguiendo EXACTAMENTE prompts/formato-guion.md (un archivo y un id distinto por guion).
2. Ejecuta npm run build para validar; si avisa de JSON no válido, corrígelo.
3. Haz commit y push.
4. Responde en el chat SOLO con una línea por guion: título, ángulo, hook recomendado (FR) y el enlace VISOR_URL/#/[id].
