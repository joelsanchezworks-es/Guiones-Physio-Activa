Elimina guiones o documentos de salidas/ para depurar el visor, siguiendo CLAUDE.md.

Qué eliminar: $ARGUMENTS

Si no se indica nada, pregunta en una línea qué quiere eliminar y espera.

Cómo identificar cada elemento (el visor copia el comando con los id):
- Guion: el "id" del JSON (por ejemplo `2026-10-29-domicilio`) → el .json de salidas/ con ese "id" y, si existe, el .md con el mismo nombre en la misma carpeta.
- Documento: `doc/[ruta sin .md]` (por ejemplo `doc/2026-10-29/02-test-de-hooks`) → `salidas/[ruta].md`.
- También se aceptan rutas de salidas/ o el título del guion. Si un título coincide con más de un elemento o no coincide con ninguno, no borres ese elemento: dilo y sigue con los demás.

Reglas:
- Borra solo dentro de salidas/. Nunca toques contexto/, prompts/, tools/, public/, docs/ ni .claude/.
- salidas/aprobados.md y salidas/ganadores.md solo se borran si el usuario los nombra por su ruta.
- No pidas confirmación: el comando ya es la confirmación. Lo borrado queda en el historial de Git.

Pasos:
1. Localiza los archivos y bórralos con `git rm`.
2. Ejecuta `npm run build` para comprobar que el visor sigue bien.
3. Haz commit («Elimina: [títulos]») y push a la rama de trabajo y a `main` (ver «Publicar en main» en CLAUDE.md).
4. Responde en el chat SOLO con la lista de lo eliminado (título y archivo), lo que no se pudo eliminar y por qué, y una línea final: «Se puede recuperar con git (commit [hash corto])».
