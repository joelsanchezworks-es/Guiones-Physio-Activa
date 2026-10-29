# Guiones · Physio Activa

Sistema para generar hooks y guiones de **Reels 9:16** (test de hooks, orgánico y Meta Ads) para Physio Activa, en francés y alemán, y verlos en un visor web.

## Cómo funciona

```
Claude Code  ──►  GitHub  ──►  Cloudflare Pages
/guion [tema]     JSON en       npm run build → visor web estático
                  salidas/      https://physioactiva-guiones.pages.dev
```

1. En **Claude Code** (claude.ai/code, la app del móvil o la terminal) escribes `/guion [tema]`.
2. Claude genera el guion, lo guarda como JSON en `salidas/AAAA-MM-DD/`, lo valida con `npm run build` y hace **push** a GitHub.
3. **Cloudflare Pages** detecta el push, ejecuta `npm run build` y publica el visor. En un minuto el guion está en `https://physioactiva-guiones.pages.dev/#/[id]`.

El consumo de Claude va contra el plan de quien usa Claude Code (por ejemplo, tu Max). **No hay API, ni claves, ni Functions**: la web es 100 % estática y Cloudflare Pages es gratis.

## Puesta en marcha en Cloudflare (una sola vez)

1. Cloudflare → **Workers & Pages → Create → Pages → Connect to Git** → elige este repositorio.
2. Configuración de build:
   - **Production branch:** la rama en la que trabaja Claude Code (o `main` si fusionas ahí).
   - **Framework preset:** None
   - **Build command:** `npm run build`
   - **Build output directory:** `public`
   - **Variables de entorno:** ninguna.
3. **Save and Deploy.** Tendrás `https://[nombre-del-proyecto].pages.dev`. Si el nombre no es `physioactiva-guiones`, cambia la línea `VISOR_URL:` de `CLAUDE.md`. En *Custom domains* puedes ponerle un subdominio propio.

### Proteger el visor con Cloudflare Access (gratis, por email)

El visor contiene información interna del cliente, así que conviene cerrarlo:

1. Cloudflare → **Zero Trust** (la primera vez te pide elegir un nombre de equipo y el plan **Free**).
2. **Access → Applications → Add an application → Self-hosted.** Como dominio, pon el del visor: `physioactiva-guiones.pages.dev` (y, si quieres cubrir también las vistas previas, añade `*.physioactiva-guiones.pages.dev`).
3. Crea una política **Allow** con **Include → Emails** y añade los correos del equipo (o **Emails ending in** `@tudominio.com`). Método de acceso: **One-time PIN**.
4. Al abrir el visor, Cloudflare pide el email y envía un código de un solo uso. El plan gratuito de Zero Trust cubre hasta 50 usuarios.

> El interruptor *Settings → General → Access policy* del proyecto de Pages solo protege las vistas previas, no la URL principal. Por eso se usa Zero Trust. Los nombres de los menús de Cloudflare cambian a veces: si no encuentras uno, busca «Access» o «Applications» en el panel.

## Uso diario

```
/guion dolor de espalda en personas que trabajan en oficina
```

```
/guion orgánico 3 mitos sobre la rodilla, solo FR
```

```
/guion MTT gratis en Neuchâtel tras una operación de hombro
```

No hace falta el comando: «guion sobre recuperación tras prótesis de rodilla» funciona igual. Claude responde con el título, el ángulo, el hook recomendado y el **enlace al visor**.

En el visor:
- **FR / DE:** cambia todos los textos (recuerda tu elección).
- **Leer a cámara:** pantalla negra con letra grande y solo lo que se dice, con A− / A+ y Escape para cerrar. Al final salen los hooks alternativos.
- **Copiar guion**, **Copiar** en cada texto de Meta (con contador de caracteres) e **Imprimir / PDF**.
- Los documentos `.md` de `salidas/` (banco de hooks, test, plan de grabación…) también se ven en el visor, en «Documentos».

### Otros comandos

| Comando | Qué hace |
| --- | --- |
| `/guion [tema]` | **El principal.** Un guion completo (JSON + enlace al visor) |
| `/ads [ángulos]` | Varios guiones de ads (JSON + enlaces) |
| `/organico [formatos]` | Varios guiones orgánicos (JSON + enlaces) |
| `/hooks [ángulos, cantidad]` | Banco de hooks |
| `/test-hooks` | Test de cuerpo fijo: 3 cuerpos × 5 hooks, nombres de anuncio, métricas y reglas |
| `/plan-grabacion` | Plan de una jornada por localización + hoja imprimible A4 |
| `/ganadores [métricas o CSV de Meta]` | Calcula hook rate, hold rate, CTR y CPL y guarda los ganadores |

## Estructura

| Carpeta / archivo | Para qué sirve |
| --- | --- |
| `CLAUDE.md` | Instrucciones que Claude Code lee siempre (incluye `VISOR_URL`) |
| `.claude/commands/` | Los comandos `/guion`, `/ads`, etc. |
| `prompts/sistema.md` | Rol, ángulos A–F, tipos de hook, duraciones y reglas de cumplimiento |
| `prompts/formato-guion.md` | Formato JSON exacto de cada guion |
| `contexto/` | Datos del cliente (web, reunión del 28/10, cuenta de Meta Ads). Añade aquí más `.md` |
| `salidas/` | Todo lo generado, por fecha. `salidas/2026-10-29/` es el primer paquete completo |
| `tools/build-visor.mjs` | Valida los JSON y prepara `public/data/` (lo ejecuta `npm run build`) |
| `tools/build_entregables.py` | Hoja imprimible A4 de una carpeta, solo bajo petición |
| `public/index.html` | El visor (un solo archivo) |
| `docs/carga-inicial.md` | El prompt de la carga inicial (solo documentación) |

## Probar en local (opcional)

```bash
npm run dev
```

Abre la dirección que indica `serve` (normalmente http://localhost:3000).

## Seguridad

- Mantén el repositorio **privado** y el visor protegido con Cloudflare Access: `contexto/` y `salidas/` tienen información interna del cliente.
- No subas datos de pacientes ni fotos sin consentimiento.
