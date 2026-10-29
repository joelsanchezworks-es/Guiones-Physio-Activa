# Generador de hooks y guiones · Physio Activa

Sistema para generar hooks y guiones de **Reels 9:16** (test de hooks, orgánico y Meta Ads) para Physio Activa, en francés y alemán.

Funciona **solo con Claude Code** (en la web, en la app del móvil o en la terminal). El consumo va contra el plan de quien lo usa (por ejemplo, tu Max): **no hay API, ni claves, ni servidores que pagar**.

## Cómo se usa

1. Entra en **claude.ai/code** (o en la app de Claude → Code) y elige este repositorio.
2. Escribe lo que necesitas. Por ejemplo:

```
/guion dolor de espalda en personas que trabajan en oficina
```

No hace falta el comando: «guion sobre recuperación tras prótesis de rodilla» funciona igual.

3. Claude Code lee `CLAUDE.md`, `prompts/sistema.md` y `contexto/`, genera el resultado, lo guarda en `salidas/AAAA-MM-DD/` y lo sube a GitHub.

### Comandos

| Comando | Qué hace |
| --- | --- |
| `/guion [tema]` | **El principal.** Tema → ficha, 5 hooks, guion del Reel FR + DE, copy de Meta (o texto del post), notas de grabación y pendientes |
| `/hooks [ángulos, cantidad]` | Banco de hooks de tres capas (verbal, visual, texto en pantalla) |
| `/test-hooks` | Test de cuerpo fijo: 3 cuerpos × 5 hooks, nombres de archivo y de anuncio, métricas y reglas |
| `/ads [ángulos]` | Guiones de ads de 20–30 s con copy de Meta |
| `/organico [formatos]` | Guiones orgánicos de 20–45 s con texto del post y hashtags |
| `/plan-grabacion` | Plan de una jornada por localización + hoja imprimible A4 |
| `/ganadores [métricas o CSV de Meta]` | Calcula hook rate, hold rate, CTR y CPL, guarda los ganadores y propone hooks nuevos |

## Estructura

| Carpeta / archivo | Para qué sirve |
| --- | --- |
| `CLAUDE.md` | Instrucciones que Claude Code lee siempre al abrir el repo |
| `.claude/commands/` | Los comandos `/guion`, `/hooks`, etc. |
| `prompts/sistema.md` | Rol, ángulos A–F, tipos de hook, duraciones, formato y reglas de cumplimiento |
| `contexto/` | Datos del cliente (web, reunión del 28/10, cuenta de Meta Ads). Añade aquí más `.md` |
| `salidas/` | Todo lo generado, por fecha. `aprobados.md` y `ganadores.md` hacen de memoria del sistema |
| `salidas/2026-10-29/` | Primer paquete completo: 60 hooks, test de hooks, 8 orgánicos, 7 ads, plan de grabación, calendario y `guiones-grabacion.html` |
| `tools/build_entregables.py` | Genera la hoja imprimible A4: `python3 tools/build_entregables.py salidas/AAAA-MM-DD` |
| `PROMPT.md` | El prompt completo del primer paquete, por si quieres regenerarlo desde cero |

## Actualizar el contexto

Edita o añade archivos en `contexto/` directamente en GitHub (por ejemplo `gimnasio-neuchatel.md` cuando tengáis el nombre y las condiciones, o `rendimiento-anuncios.md` con los datos de Meta). La siguiente vez que uses Claude Code, ya lo tendrá en cuenta.

## Quién puede usarlo

- Cualquiera con su propia cuenta de Claude con Claude Code y acceso a este repositorio en GitHub. Lo que genere cada persona se descuenta de su propio plan.
- El cliente no necesita acceso: le pasas los `.md` o el `guiones-grabacion.html` impreso.

## Seguridad

- Mantén el repositorio **privado**: `contexto/` tiene información interna del cliente.
- No subas datos de pacientes ni fotos sin consentimiento.
