# Generador de hooks y guiones · Physio Activa

Este repositorio es un sistema para generar hooks y guiones de vídeo (test, orgánico y ads de Meta) para Physio Activa, clínica de fisioterapia en Ins (Suiza).

Se usa solo con **Claude Code** (claude.ai/code, la app o la terminal), con el plan de la persona que lo abre. No hay API ni claves: no añadas código que llame a la API de Claude ni pidas una `ANTHROPIC_API_KEY`.
Formato: **solo Reels 9:16** (orgánico y Meta Ads). Sin Stories, sin versión de 15 s y sin TikTok.

## Uso diario (lo normal)
Cuando el usuario escribe un tema, con `/guion` o sin comando (por ejemplo «guion sobre dolor de espalda en oficinistas»), sigue `.claude/commands/guion.md`:
1. Responde **directamente en el chat** con el guion completo en Markdown: ficha, 5 hooks con el recomendado marcado, guion del Reel en tabla, versión en alemán, copy de Meta y notas de grabación.
2. Si el tema es ambiguo, **no preguntes**: elige ángulo, uso (ads por defecto) e idioma (FR + DE) y dilo en una línea al principio.
3. Guarda **solo** el `.md` del guion en `salidas/AAAA-MM-DD/guion-[tema].md`.
4. Al final, haz commit y push **sin pedir permiso**.

## Lo que NO se hace salvo petición explícita
- **No** generes HTML ni PDF, y **no** ejecutes `tools/build_entregables.py`, salvo que el usuario lo pida explícitamente (por ejemplo «hazme la hoja imprimible») o use `/plan-grabacion`.
- **No** regeneres el paquete completo ni ejecutes `PROMPT.md`. `PROMPT.md` es solo documentación de la carga inicial (el paquete ya está en `salidas/2026-10-29/`).

## Antes de generar cualquier cosa
1. Lee `prompts/sistema.md`: rol, ángulos (A–F), tipos de hook, las tres capas de un hook, duraciones, formato, idiomas y reglas de cumplimiento. Síguelo siempre.
2. Lee todos los archivos de `contexto/`: es la única fuente de datos del cliente. No inventes cifras, precios, testimonios ni promesas. Si falta algo, escribe `[POR CONFIRMAR]`.
3. Cuenta de Meta Ads: `act_1583510023185138` (ver `contexto/cuenta-meta-ads.md`). Si el conector de Meta Ads está disponible, úsalo solo en lectura.
4. No uses nunca physiodom.ch.

## Dónde guardar
- Guarda cada resultado en `salidas/AAAA-MM-DD/` con un nombre descriptivo, por ejemplo `salidas/2026-10-30/guion-dolor-espalda-oficina.md`.
- No sobrescribas resultados anteriores: crea archivos nuevos.
- Para no repetir hooks, revisa `salidas/2026-10-29/01-banco-de-hooks.csv`, `salidas/aprobados.md` y `salidas/ganadores.md` (este último dice qué funcionó en los tests).
- Hoja imprimible A4 (solo si se pide): `python3 tools/build_entregables.py salidas/AAAA-MM-DD`.

## Comandos disponibles
**`/guion [tema]`** (el principal: tema → guion completo en el chat), `/hooks`, `/test-hooks`, `/ads`, `/organico`, `/plan-grabacion`, `/ganadores`. Acepta indicaciones libres después del comando (ángulos, idioma, cantidad, notas).

## Al terminar cada tarea
1. Haz commit de los archivos nuevos y súbelos (push) a la rama de trabajo sin pedir permiso: la sesión en la nube se borra al cerrarse.
2. Con `/guion`, el guion ya es la respuesta: termina con una sola línea con la ruta del archivo guardado. En las demás tareas, resume en 3–5 líneas qué generaste, dónde lo guardaste y qué queda `[POR CONFIRMAR]`.
