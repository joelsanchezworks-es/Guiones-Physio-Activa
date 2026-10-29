# Generador de hooks y guiones · Physio Activa

Este repositorio es un sistema para generar hooks y guiones de vídeo (test, orgánico y ads de Meta) para Physio Activa, clínica de fisioterapia en Ins (Suiza).

Se usa solo con **Claude Code** (claude.ai/code, la app o la terminal), con el plan de la persona que lo abre. No hay API ni claves: no añadas código que llame a la API de Claude ni pidas una `ANTHROPIC_API_KEY`.
Formato: **solo Reels 9:16** (orgánico y Meta Ads). Sin Stories, sin versión de 15 s y sin TikTok.

## Antes de generar cualquier cosa
1. Lee `prompts/sistema.md`: rol, ángulos (A–F), tipos de hook, las tres capas de un hook, duraciones, formato, idiomas y reglas de cumplimiento. Síguelo siempre.
2. Lee todos los archivos de `contexto/`: es la única fuente de datos del cliente. No inventes cifras, precios, testimonios ni promesas. Si falta algo, escribe `[POR CONFIRMAR]`.
3. Cuenta de Meta Ads: `act_1583510023185138` (ver `contexto/cuenta-meta-ads.md`). Si el conector de Meta Ads está disponible, úsalo solo en lectura.
4. No uses nunca physiodom.ch.

## Dónde guardar
- Guarda cada resultado en `salidas/AAAA-MM-DD/` con un nombre descriptivo, por ejemplo `salidas/2026-10-30/hooks-A-C.md`.
- No sobrescribas resultados anteriores: crea archivos nuevos.
- El primer paquete completo (60 hooks, test, 8 orgánicos, 7 ads, plan y calendario) está en `salidas/2026-10-29/`. Revisa su `01-banco-de-hooks.csv` antes de crear hooks nuevos para no repetirlos.
- Para una hoja imprimible A4 de una carpeta de salidas, ejecuta `python3 tools/build_entregables.py salidas/AAAA-MM-DD`: regenera `01-banco-de-hooks.md` desde `01-banco-de-hooks.csv` (si existe) y crea `guiones-grabacion.html`.
- Los hooks que el equipo apruebe van a `salidas/aprobados.md`; los ganadores de test, con sus métricas, a `salidas/ganadores.md`. Consulta estos dos archivos antes de generar algo nuevo para no repetir y partir de lo que funcionó.

## Comandos disponibles
**`/guion [tema]`** (el principal: tema → guion completo), `/hooks`, `/test-hooks`, `/ads`, `/organico`, `/plan-grabacion`, `/ganadores`. Acepta indicaciones libres después del comando (ángulos, idioma, cantidad, notas).

## Al terminar cada tarea
1. Haz commit de los archivos nuevos y súbelos (push) a la rama de trabajo, para que queden guardados en GitHub: la sesión en la nube se borra al cerrarse.
2. Resume en 3–5 líneas qué generaste, dónde lo guardaste y qué queda `[POR CONFIRMAR]`.

## Petición libre
Si el usuario escribe un tema sin comando (por ejemplo "guion sobre dolor de espalda en oficinistas"), trátalo como `/guion` con ese tema.
