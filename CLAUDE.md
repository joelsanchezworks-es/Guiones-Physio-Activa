# Generador de hooks y guiones · Physio Activa

VISOR_URL: https://physioactiva-guiones.pages.dev

Este repositorio genera hooks y guiones de **Reels 9:16** (test, orgánico y Meta Ads) para Physio Activa, clínica de fisioterapia en Ins (Suiza). Cada guion se guarda como JSON en `salidas/`, se sube a GitHub y Cloudflare Pages lo publica en el visor web (`public/index.html`, 100 % estático).

Se usa solo con **Claude Code**, con el plan de la persona que lo abre. No hay API ni claves: no añadas código que llame a la API de Claude ni Cloudflare Functions, y no pidas una `ANTHROPIC_API_KEY`. Sin Stories, sin versión de 15 s y sin TikTok.

## Uso diario
- Cualquier tema que escriba el usuario, con o sin `/guion`, se trata como `/guion` (ver `.claude/commands/guion.md`).
- No generes HTML, PDF ni paquetes completos salvo que el usuario lo pida explícitamente.
- `docs/carga-inicial.md` es documentación de la carga inicial: no se ejecuta.

## Antes de generar
1. Lee `prompts/sistema.md` (rol, ángulos A–F, tipos de hook, tres capas, duraciones, idiomas y reglas de cumplimiento) y todos los archivos de `contexto/`.
2. No inventes cifras, precios, testimonios ni promesas. Si falta algo, escribe `[POR CONFIRMAR]`.
3. Consulta `salidas/` (los guiones `.json`, `salidas/2026-10-29/01-banco-de-hooks.csv`, `salidas/aprobados.md` y `salidas/ganadores.md`) para no repetir hooks y partir de lo que funcionó.
4. Cuenta de Meta Ads `act_1583510023185138` (ver `contexto/cuenta-meta-ads.md`): solo en lectura, si el conector está disponible.
5. No uses nunca physiodom.ch.

## Guardar
- Guiones: JSON en `salidas/AAAA-MM-DD/guion-[tema-corto].json`, siguiendo **exactamente** `prompts/formato-guion.md`. No sobrescribas guiones anteriores. Cada texto lleva también su traducción al español en la clave `es` (solo para que el equipo lo entienda; no se graba ni se publica).
- Otros documentos (planes, tests, notas): `.md` que empiece por `# Título`.
- Después: `npm run build` (valida los JSON; si avisa de uno no válido, corrígelo), commit y push. **El push es obligatorio**, porque la sesión en la nube se borra al cerrarse.
- **Publicar en `main`:** Cloudflare Pages publica la rama `main`. Después del push a la rama de trabajo, súbelo también a `main` sin pedir permiso: `git fetch origin main`; si `main` tiene commits que tu rama no tiene, `git merge origin/main` (sin reescribir historia) y vuelve a ejecutar `npm run build`; después `git push origin HEAD:main`. Si hay un conflicto que no se resuelve de forma obvia, no fuerces nada: avisa al usuario.

## Respuesta en el chat
Breve: título, ángulo, hook recomendado (FR) y el enlace `VISOR_URL/#/[id]`. No pegues el guion entero.

## Comandos disponibles
**`/guion [tema]`** (el principal), `/hooks`, `/test-hooks`, `/ads`, `/organico`, `/plan-grabacion`, `/ganadores` y `/eliminar [id…]` (borra guiones o documentos de `salidas/`; el visor copia el comando desde el botón «Eliminar» o el modo «Depurar»). Aceptan indicaciones libres después del comando (ángulos, idioma, cantidad, notas).
La hoja imprimible A4 de una carpeta (`python3 tools/build_entregables.py salidas/AAAA-MM-DD`) solo se genera con `/plan-grabacion` o si el usuario la pide.
