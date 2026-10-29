# Prompt para Claude Code — Hooks y guiones de vídeo Physio Activa (test, orgánico y ads)

> Descomprime `physioactiva-guiones.zip`, abre Claude Code dentro de la carpeta `physioactiva-guiones/` y pega todo lo que hay debajo de la línea. La carpeta `contexto/` ya trae la información del cliente.

---

Actúa como estratega creativo y guionista senior de vídeo corto en formato Reels (orgánico y Meta Ads) experto en clínicas de fisioterapia: conoces a fondo cómo piensa un paciente con dolor, qué le frena a pedir cita y qué mensajes le hacen reservar. Tu prioridad número uno son los **hooks**: los primeros 3 segundos que deciden si alguien deja de hacer scroll. A partir de los mejores hooks construirás guiones para tres usos: **contenido de prueba (test de hooks)**, **contenido orgánico** y **anuncios (ads)**, que el equipo grabará con el móvil la próxima semana.

## 1. Antes de empezar

1. **Lee primero todos los archivos de `contexto/`** — son la fuente principal y prevalecen sobre cualquier otra:
   - `contexto/web-physioactiva.md`: datos, servicios, cobertura, MTT, testimonios y tono, extraídos de la web.
   - `contexto/transcripcion-reunion.md`: reunión del 28/10 con los objetivos y el problema de cierre de leads.
   - `contexto/cuenta-meta-ads.md`: cuenta publicitaria y reglas de la cuenta.
   - Cualquier otro archivo que encuentres ahí (reseñas, anuncios anteriores, competencia).
2. Si necesitas confirmar algo más, consulta https://physioactiva.ch/ y https://physioactiva.ch/de/. **No uses physiodom.ch** (se va a redirigir). Usa solo datos que aparezcan en `contexto/`, en la web o en este prompt; no inventes cifras, precios ni promesas.
3. **Cuenta publicitaria de Meta:** Physio Activa Publicité 2 · ID `act_1583510023185138` (CHF). Si tienes el conector de Meta Ads disponible, sigue las instrucciones de `contexto/cuenta-meta-ads.md` para leer el rendimiento de los anuncios actuales (solo lectura) antes de escribir los hooks. Si no lo tienes, continúa sin ello.
4. Si falta un dato marcado como `[POR CONFIRMAR]`, déjalo como marcador visible y añádelo a `00-pendientes.md`. No te detengas por ello.
5. Muéstrame primero un índice de lo que vas a crear y continúa sin esperar respuesta.

## 2. Contexto del cliente

- **Negocio:** Physio Activa, clínica de fisioterapia en **Ins (Anet), cantón de Berna**, 1.ª planta del edificio Lidl, dentro de InsGym. También atiende **a domicilio** en la región de los Tres Lagos (Morat, Neuchâtel, Bienne).
- **Equipo:** Lucile Combes y Francisco Díaz, fisioterapeutas diplomados. Atienden en francés, alemán, inglés, español y portugués.
- **Propuesta de valor (confirmada en la web):**
  - Cita **en la misma semana**, sin listas de espera. En la zona la competencia tiene listas de espera de unos 3 meses.
  - Abierto **hasta las 20 h**, de lunes a viernes.
  - **Cubierto por el seguro** (LAMal, LAA, AI, AM) con prescripción médica.
  - Sala de fitness completa para **MTT (Medical Training Therapy)**: recuperación activa, no solo masaje.
  - Valoración media de 4,9 en Google y un 74 % de pacientes que llegan por recomendación.
- **Novedad:** convenio con un gimnasio de **Neuchâtel** para ofrecer **MTT gratuita a pacientes con prescripción**. Nombre del gimnasio y condiciones: `[POR CONFIRMAR]`.
- **Contacto y CTA:** WhatsApp +41 76 627 38 38 · reserva online en OneDoc · formulario de Meta (Lead Ads).
- **Problema de negocio:** hay volumen de leads, pero el cierre es bajo. Los ads deben atraer leads con **intención real de reservar** (dolor concreto, prescripción en mano, urgencia), no curiosos.

## 3. Público, idiomas y zonas

- **Públicos:** adultos de 30 a 70 años con dolor (espalda, cervical, hombro, rodilla o tobillo); personas en postoperatorio; mayores que necesitan fisio a domicilio y sus hijos o familiares; personas que trabajan y no tienen tiempo; deportistas.
- **Francés** (idioma principal): Neuchâtel, Fribourg, Payerne, Estavayer, Yverdon-les-Bains, Yvonand, Lausanne, Sugiez, La Neuveville, Avenches.
- **Alemán:** Ins, Murten, Kerzers, Lyss. Biel/Bienne es bilingüe.
- Todo se escribe en **francés** con su **adaptación al alemán** (natural, no literal). Tratamiento de "vous" en francés y "Sie" en alemán.

## 4. PARTE 1 — Banco de hooks (lo más importante)

Crea un banco de **60 hooks** (30 en francés y sus 30 adaptaciones al alemán), repartidos entre los 6 ángulos de la tabla y los 10 tipos de hook. Cada hook tiene **tres capas**, que deben funcionar juntas y por separado (mucha gente ve el vídeo sin sonido):

1. **Hook verbal:** la frase que se dice a cámara. 12 palabras o menos.
2. **Hook visual:** qué se ve en el primer segundo (acción, plano, objeto, movimiento). Debe ser grabable con un móvil.
3. **Texto en pantalla:** 6 palabras o menos.

**Ángulos:**

| Ángulo | Idea central |
| --- | --- |
| A. Sin espera | Cita esta semana frente a 3 meses de espera |
| B. Sin tiempo | Hasta las 20 h, ven después del trabajo |
| C. Dolor concreto | Espalda, cervical, hombro, rodilla |
| D. Más que un masaje | Plan de recuperación activo + MTT |
| E. A domicilio | Para mayores o tras una hospitalización (habla al familiar) |
| F. Cubierto por el seguro / MTT gratis en Neuchâtel | Elimina la objeción del precio |

**Tipos de hook (usa todos):** pregunta directa al dolor · error común ("deja de hacer esto si…") · dato o contraste (3 meses frente a esta semana) · contraintuitivo o mito ("el reposo no siempre cura…") · POV o situación reconocible · demostración visual (ejercicio o test de movilidad en 3 s) · "si te pasa esto…" (autoidentificación) · historia en primera persona del fisio · lista o número ("3 señales de que…") · llamada local (nombrar la zona: "Si vives cerca de Morat…").

Para cada hook indica: ID (por ejemplo `A-03-FR`), ángulo, tipo, público, uso recomendado (test, orgánico o ads) y una **hipótesis** de por qué debería funcionar, en una línea.

Al final, marca tus **10 hooks favoritos para testear primero** y explica la elección en una línea por hook.

## 5. PARTE 2 — Contenido de prueba (test de hooks)

Diseña un **test de hooks con cuerpo fijo**: el mismo cuerpo de vídeo y el mismo CTA, cambiando solo los primeros 3 segundos. Así se graba poco y se aprende rápido.

- Crea **3 cuerpos base** de 20–30 s (por ejemplo, ángulos A, C y D).
- Asigna a cada cuerpo **5 hooks distintos** del banco → 15 variantes.
- Para cada variante: ID, hook (verbal + visual + texto), cuerpo base que usa, nombre del archivo de vídeo sugerido (`TEST_A_H1_FR.mp4`) y nombre del anuncio para la cuenta `act_1583510023185138` (formato `PA_TEST_[ángulo]_[hook]_[idioma]_[fecha]`).
- Ajusta presupuestos y reglas de decisión a las reglas de `contexto/cuenta-meta-ads.md` (tests a 16–20 CHF/día, pausar sin lead a ~17 CHF, mínimo 2 anuncios activos, CPL objetivo ~4 CHF).
- Incluye las **métricas para decidir el ganador** en Meta, con criterio de paso: hook rate (reproducciones de 3 s / impresiones), hold rate (ThruPlays / reproducciones de 3 s), CTR, CPL y calidad del lead. Incluye también una regla simple de decisión (por ejemplo, gasto mínimo por variante antes de juzgar; los ganadores pasan a ads).

## 6. PARTE 3 — Guiones orgánicos (Reels)

Escribe **8 guiones orgánicos** de 20–45 s que eduquen, generen confianza y conecten. No son anuncios: venden poco y aportan mucho. Mezcla estos formatos:

- Educativo: "3 ejercicios para…" o "por qué te duele…"
- Mito frente a realidad
- Detrás de cámaras: la clínica, la sala de fitness, un día con el fisio
- Presentación del equipo (Lucile, Francisco) e idiomas
- Preguntas frecuentes: "¿necesito prescripción?", "¿lo cubre el seguro?"
- Contenido local: la zona de los Tres Lagos, el gimnasio de Neuchâtel

Cada guion abre con un hook del banco (indica su ID) y cierra con un CTA suave: guardar, compartir, seguir o "escríbenos".

## 7. PARTE 4 — Guiones de ads (respuesta directa)

Escribe **7 guiones de ads** en formato Reels de 20–30 s (máximo 40 s), uno por ángulo (el de MTT gratis en el gimnasio de Neuchâtel es obligatorio y va aparte del de seguro):

- **Gancho (0–3 s):** 3 variantes de hook del banco (indica sus IDs).
- **Problema (3–10 s):** el dolor o la situación del paciente, en sus palabras.
- **Solución y prueba (10–25 s):** cita esta semana, hasta las 20 h, seguro, MTT, equipo, 4,9 en Google.
- **CTA (últimos 5 s):** una sola acción ("Escríbenos por WhatsApp" o "Reserva tu cita esta semana") con un **filtro de intención** ("Si tienes prescripción, te vemos esta semana").
- **Copy para Meta** en francés y alemán: texto principal corto (125 caracteres o menos) y largo, titular (40 caracteres o menos) y descripción.

## 8. Formato de todos los guiones

- Vertical 9:16, grabable con móvil por el equipo (Francisco, Lucile, Paul y el equipo) en la clínica, en la sala de fitness, en un domicilio o en el gimnasio de Neuchâtel.
- Tabla de dos columnas: *Lo que se ve / se graba* | *Lo que se dice*, con los textos en pantalla y la duración de cada bloque.
- Frases cortas, fáciles de decir por alguien que no es actor. Unas 2,5 palabras por segundo como máximo.
- Indicaciones de edición: subtítulos siempre activos, cortes cada 2–3 s y música sugerida (tipo, no canción concreta).

## 9. Reglas de cumplimiento (publicidad sanitaria en Suiza y políticas de Meta)

- No prometer curas ni resultados garantizados ("eliminamos tu dolor" no vale; "te ayudamos a recuperar el movimiento" sí).
- No usar lenguaje que señale condiciones personales ("¿Tienes artrosis?" no vale; "Si el dolor de rodilla no te deja caminar…" sí). Aplica esta regla en los ads; en orgánico puede ser algo más flexible, pero sin diagnósticos.
- Nada de antes/después, testimonios inventados ni caras o datos de pacientes sin consentimiento.
- Las cifras (4,9 en Google, 74 %) solo pueden aparecer tal como están en la web.

## 10. Archivos que debes generar

```
00-pendientes.md               ← datos [POR CONFIRMAR] y preguntas para el cliente
01-banco-de-hooks.csv          ← los 60 hooks con todas sus columnas
01-banco-de-hooks.md           ← el mismo banco agrupado por ángulo + top 10 para testear
02-test-de-hooks.md            ← 3 cuerpos base, 15 variantes, métricas y reglas de decisión
03-guiones-organico/           ← 8 archivos .md, uno por guion
04-guiones-ads/                ← 7 archivos .md, uno por guion (con copy de Meta)
05-plan-de-grabacion.md        ← todas las tomas agrupadas por localización, quién sale, material; los hooks se graban en bloque para hacerlo todo en una jornada
06-calendario-publicacion.md   ← 4 semanas: qué orgánico se publica cada día y qué test/ads se lanzan cada semana
guiones-grabacion.html         ← todo en una página imprimible (A4) para llevar el día de la grabación, con los hooks primero
```

## 11. Control de calidad antes de terminar

- Ningún hook verbal supera las 12 palabras y todos tienen capa visual y texto en pantalla.
- No hay dos hooks que digan lo mismo con otras palabras.
- Las versiones en alemán suenan naturales y no queda texto en español dentro de los guiones.
- Todos los datos usados están en `contexto/`, en la web o en este prompt.
- Abre `guiones-grabacion.html` y confirma que se ve bien al imprimir.
- Termina con un resumen de 5 líneas: qué se ha generado, cuáles son los 3 hooks más fuertes, qué queda `[POR CONFIRMAR]` y qué grabar primero.
