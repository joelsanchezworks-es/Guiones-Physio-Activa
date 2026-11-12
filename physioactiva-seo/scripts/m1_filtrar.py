"""Módulo 1 · paso 2: normalizar, deduplicar y filtrar relevancia (determinista).
Entrada: data/m1_candidatos.json · Salida: data/m1_filtradas.json + data/m1_descartadas.csv
"""
import json, re, csv, sys, pathlib, unicodedata, yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs

BASE = dfs.BASE
F = yaml.safe_load((BASE / "config/filtro.yml").read_text())
UMB = dfs.UMB


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower().replace("œ", "oe").replace("’", "'"))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return " ".join(s.split())


def clave(s):
    """Clave de deduplicación: sin acentos, sin artículos/preposiciones, singular, palabras ordenadas."""
    stop = {"de", "du", "des", "la", "le", "les", "l", "d", "a", "au", "aux", "en", "et", "pour", "un", "une", "a"}
    w = re.split(r"[\s'\-]+", norm(s))
    w = [x[:-1] if len(x) > 3 and x.endswith(("s", "x")) else x for x in w if x and x not in stop]
    return " ".join(sorted(w))


def rx(terms):
    return re.compile(r"(?<![a-z])(" + "|".join(re.escape(norm(t)) for t in terms) + r")(?![a-z])")


R_NUC, R_MSK, R_EXC = rx(F["nucleo"]), rx(F["msk"]), rx(F["excluir"])
R_COND, R_MODC = rx(F["condicionales"]), rx(F["modificador_condicional"])
R_NUC_PREF = re.compile(r"(?<![a-z])(physio\w*|kine\w*|reeducation|rehabilitation)")


R_CIU, R_COMP = rx(F["ciudades_zona"]), rx(F["competidores"])
VOC = set(norm(x) for x in F["vocabulario_local_permitido"])


def relevante(kw):
    n = norm(kw)
    if R_COMP.search(n):
        return True, "competidor"
    if R_EXC.search(n):
        return False, "excluida: " + R_EXC.search(n).group(1)
    if R_MSK.search(n):
        return True, ""
    if R_NUC_PREF.search(n):
        resto = [w for w in re.split(r"[\s]+", n) if w and w not in VOC and not R_NUC_PREF.fullmatch(w)
                 and not R_CIU.fullmatch(w)]
        if not resto:
            return True, ""
        if R_CIU.search(n):
            return True, "competidor"  # marca de una clínica de la zona: dato de competencia, no objetivo
        return False, "navegacional de otra clínica / fuera de vocabulario: " + " ".join(resto)
    if R_COND.search(n):
        return (True, "") if R_MODC.search(n) else (False, "condicional sin modificador")
    return False, "sin término del sector"


cand = json.loads((BASE / "data/m1_candidatos.json").read_text())
grupos, desc = {}, []
for kw, v in sorted(cand.items()):
    ok, motivo = relevante(kw)
    if ok and motivo == "competidor":
        v["origen"] = v["origen"] + ["competidor"]
    vol = (v["labs"] or {}).get("vol")
    oblig = "documento" in v["origen"]
    if not ok and not oblig:
        desc.append([kw, vol, motivo]); continue
    if not oblig and (vol or 0) < UMB["filtro"]["volumen_min_sin_serp"]:
        desc.append([kw, vol, "volumen < umbral"]); continue
    grupos.setdefault(clave(kw), []).append((kw, v))

final = {}
for k, items in grupos.items():
    # representante: el de mayor volumen Labs; la semilla del documento siempre se conserva como fila propia
    items.sort(key=lambda x: (-(x[1]["labs"] or {}).get("vol", 0) if (x[1]["labs"] or {}).get("vol") else 0, x[0]))
    docs = [i for i in items if "documento" in i[1]["origen"]]
    rep = docs[0] if docs else items[0]
    items = [rep] + [i for i in items if i is not rep]
    final[rep[0]] = {**rep[1], "variantes": [i[0] for i in items[1:]]}
    for kw, v in items[1:]:
        if "documento" in v["origen"]:
            final[kw] = {**v, "variantes": [], "duplicado_de": rep[0]}
        else:
            desc.append([kw, (v["labs"] or {}).get("vol"), f"duplicado de «{rep[0]}»"])

(BASE / "data/m1_filtradas.json").write_text(json.dumps(final, ensure_ascii=False, indent=0))
with (BASE / "data/m1_descartadas.csv").open("w", newline="") as f:
    w = csv.writer(f); w.writerow(["keyword", "volumen_labs", "motivo"]); w.writerows(desc)
print("candidatas", len(cand), "→ filtradas", len(final), "descartadas", len(desc))
