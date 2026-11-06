#!/usr/bin/env bash
# Ejecuta el pipeline completo. Con la caché del día no vuelve a gastar en DataForSEO.
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/rastreo.py > /dev/null          # gratis: rastreo propio del sitio
python3 scripts/m1_expandir.py                  # Labs (caché 30 días)
python3 scripts/m1_filtrar.py
python3 scripts/m1_metricas.py
python3 scripts/m1_local.py > /dev/null
python3 scripts/m1_tabla.py > /dev/null
python3 scripts/m1_serp.py > /dev/null          # SERP (caché 7 días)
python3 scripts/m2_datos.py > /dev/null
[ -f data/m2_local.json ] || python3 scripts/m2_local.py
python3 scripts/m1_cluster.py > /dev/null
python3 scripts/m2_auditoria.py
python3 scripts/m3_m4.py > /dev/null
python3 scripts/m5_briefs.py > /dev/null
python3 scripts/m5_build.py > /dev/null
python3 scripts/m6_informes.py
