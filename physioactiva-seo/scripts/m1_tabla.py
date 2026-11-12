"""Módulo 1 · paso 4: tabla única de keywords con todas las métricas (sin estimar nada que falte)."""
import json, sys, pathlib, statistics
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
K = json.loads((BASE / "data/m1_filtradas.json").read_text())
M = json.loads((BASE / "data/m1_metricas.json").read_text())


def tendencia(monthly):
    """% de cambio entre la media de los 3 últimos meses y la de los 3 primeros de los 12 últimos."""
    m = sorted([x for x in monthly if x[2] is not None], key=lambda x: (x[0], x[1]))[-12:]
    if len(m) < 12:
        return None
    a, b = statistics.mean(x[2] for x in m[:3]), statistics.mean(x[2] for x in m[-3:])
    if a == 0:
        return None
    return round(100 * (b - a) / a)


INT_ES = {"commercial": "comercial", "informational": "informacional", "navigational": "navegacional",
          "transactional": "transaccional"}
rows = []
for kw, v in K.items():
    L = v["labs"] or {}
    G = M["gads"].get(kw, {})
    ch = G.get("CH", {})
    monthly = ch.get("monthly") or L.get("monthly") or []
    intent = L.get("intent") or M["intent"].get(kw)
    kd = L.get("kd") if L.get("kd") is not None else M["kd"].get(kw)
    rows.append({
        "keyword": kw, "origen": ",".join(v["origen"]), "variantes": " | ".join(v.get("variantes", [])),
        "duplicado_de": v.get("duplicado_de", ""),
        "vol_ch_gads": ch.get("vol"), "vol_ch_labs": L.get("vol"),
        "vol_be": G.get("BE", {}).get("vol"), "vol_fr": G.get("FR", {}).get("vol"),
        "vol_ne": G.get("NE", {}).get("vol"), "vol_vd": G.get("VD", {}).get("vol"),
        "cpc_usd": ch.get("cpc") if ch.get("cpc") is not None else L.get("cpc"),
        "competencia_ads": ch.get("comp") or L.get("comp_level"),
        "kd": kd, "intencion": INT_ES.get(intent, intent),
        "tendencia_12m_pct": tendencia(monthly),
        "serie_12m": ";".join(str(x[2]) for x in sorted(monthly, key=lambda x: (x[0], x[1]))[-12:]),
        "fuente": f"DataForSEO google_ads/search_volume + dataforseo_labs (CH, fr) {M['fecha']}",
    })


def vol(r):
    return r["vol_ch_gads"] if r["vol_ch_gads"] is not None else (r["vol_ch_labs"] or 0)


rows.sort(key=lambda r: (-vol(r), r["keyword"]))
(BASE / "data/m1_tabla.json").write_text(json.dumps(rows, ensure_ascii=False, indent=0))
print(len(rows), "con gads", sum(r["vol_ch_gads"] is not None for r in rows), "kd", sum(r["kd"] is not None for r in rows),
      "intent", sum(bool(r["intencion"]) for r in rows))
for r in rows[:40]:
    print(r["keyword"], r["vol_ch_gads"], r["vol_ch_labs"], r["vol_be"], r["vol_fr"], r["vol_ne"], r["vol_vd"], r["cpc_usd"], r["kd"], r["intencion"], r["tendencia_12m_pct"])
