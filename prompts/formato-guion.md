# Formato de guardado de un guion (JSON)

Cada guion se guarda como **un archivo JSON** en:

```
salidas/AAAA-MM-DD/guion-[tema-corto].json
```

(fecha de hoy; tema en minúsculas, sin acentos y con guiones, por ejemplo `guion-dolor-espalda-oficina.json`).

El visor web (`public/index.html`) solo muestra los JSON que siguen **exactamente** esta estructura. Después de guardar, ejecuta `npm run build`: si avisa de un JSON no válido, corrígelo antes de hacer commit.

## Estructura

```json
{
  "tipo": "guion",
  "id": "2026-10-29-domicilio",
  "fecha": "2026-10-29",
  "titulo": "Fisio a domicilio tras el hospital",
  "tema": "domicilio",
  "angulo": "E",
  "uso": "ads",
  "duracion": "28 s",
  "idiomas": ["fr", "de"],
  "publico": "Hijos y familiares de personas mayores tras una hospitalización o caída",
  "localizacion": "Un domicilio: puerta, salón y pasillo",
  "quien_sale": "Un fisio y un figurante con consentimiento firmado",
  "hooks": [
    {
      "id": "H1", "tipo": "POV / familiar", "recomendado": true,
      "verbal": { "fr": "Votre père sort de l'hôpital ? On vient chez lui.", "de": "Ihr Vater kommt aus dem Spital? Wir kommen zu ihm nach Hause.", "es": "¿Su padre sale del hospital? Vamos a su casa." },
      "visual": "El fisio llama al timbre con su bolsa",
      "texto": { "fr": "Physio à domicile, cette semaine", "de": "Physio zu Hause, diese Woche", "es": "Fisio a domicilio, esta semana" },
      "hipotesis": "Habla a quien decide justo cuando busca solución"
    }
  ],
  "guion": [
    {
      "tiempo": "0–3 s", "bloque": "Gancho",
      "visual": "El fisio llama al timbre con la bolsa",
      "dice": { "fr": "Votre père sort de l'hôpital ? On vient chez lui.", "de": "Ihr Vater kommt aus dem Spital? Wir kommen zu ihm nach Hause.", "es": "¿Su padre sale del hospital? Vamos a su casa." },
      "texto": { "fr": "Physio à domicile, cette semaine", "de": "Physio zu Hause, diese Woche", "es": "Fisio a domicilio, esta semana" }
    }
  ],
  "copy": {
    "fr": { "corto": "…", "largo": "…", "titular": "…", "descripcion": "…" },
    "de": { "corto": "…", "largo": "…", "titular": "…", "descripcion": "…" },
    "es": { "corto": "…", "largo": "…", "titular": "…", "descripcion": "…" }
  },
  "notas": ["…"],
  "pendientes": ["…"]
}
```

## Campos

| Campo | Contenido |
| --- | --- |
| `tipo` | Siempre `"guion"` |
| `id` | `AAAA-MM-DD-tema-corto`, igual que el nombre del archivo sin `guion-` ni `.json`. Único |
| `fecha` | `AAAA-MM-DD` (la de la carpeta) |
| `titulo` | Título corto en español |
| `tema` | El tema tal como lo escribió el usuario (corto) |
| `angulo` | Una letra: `A`–`G` (ver `prompts/sistema.md`) |
| `uso` | `"ads"` u `"organico"` |
| `duracion` | Por ejemplo `"28 s"` (ads 20–30 s; orgánico 20–45 s) |
| `idiomas` | `["fr", "de"]`, `["fr"]` o `["de"]` |
| `publico`, `localizacion`, `quien_sale` | Texto en español |
| `hooks` | Exactamente **5** hooks de tipos distintos |
| `guion` | Bloques en orden de tiempo |
| `copy` | Ver abajo |
| `notas` | Lista de notas de grabación y edición (tomas, material, música, subtítulos) |
| `pendientes` | Lista de `[POR CONFIRMAR]`; `[]` si no hay |

## Reglas

- **5 hooks**, exactamente uno con `"recomendado": true` (los demás con `false`). Cada hook tiene `id` (`H1`–`H5`), `tipo`, `verbal`, `visual`, `texto` e `hipotesis`.
  - Hook verbal (`verbal`): **12 palabras o menos** en cada idioma.
  - Texto en pantalla (`texto`): **6 palabras o menos** en cada idioma.
- `bloque`: `Gancho`, `Problema`, `Solución`, `Prueba` o `CTA` en ads; `Gancho`, `Valor` o `CTA` en orgánico. El primer bloque (`Gancho`) usa el hook recomendado.
- `copy`:
  - En **ads**: `corto` (**≤125 caracteres**), `largo`, `titular` (**≤40 caracteres**) y `descripcion`, por idioma. En `largo` los saltos de línea se escriben como `\n`.
  - En **orgánico**: `{ "fr": { "post": "…", "hashtags": ["#…"] } }` (y `de` si aplica), con 5 hashtags.
- Las claves de idioma (`fr`, `de`) son **solo** las de `idiomas`. Además, **todo** texto con idiomas (`verbal`, `texto`, `dice` y `copy`) lleva una clave **`es`**: la traducción al español para que el equipo entienda el guion. `es` **no** va en `idiomas`: no se graba ni se publica, solo se ve en el visor (botón ES y «Ver en español»). Es una traducción fiel del francés (o del alemán si el guion es solo DE), sin añadir nada. En `copy.es`, las mismas claves que en los demás idiomas.
- Lo que se ve (`visual`), las hipótesis, las notas y los pendientes van **en español**. Lo que se dice, el texto en pantalla y el copy van en el idioma de su clave. Nunca texto en español dentro de las claves `fr` o `de` de `dice`, `verbal`, `texto` o `copy`: el español va solo en la clave `es`.
- Los datos (cifras, seguros, horarios, zonas) salen solo de `contexto/`. Si falta algo: `[POR CONFIRMAR]` en el texto y una línea en `pendientes`.
- JSON válido: comillas dobles, sin comas finales, en UTF-8.

## Ejemplo completo

`salidas/2026-10-29/guion-domicilio.json`.
