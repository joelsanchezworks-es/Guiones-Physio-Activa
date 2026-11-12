"""Genera los entregables HTML (sin JS, sin dependencias) y el Excel a partir de los datos calculados."""
import json, csv, sys, pathlib, re, html, statistics, collections, unicodedata, yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
E = BASE / "entregables"
HOY = dfs.HOY
R = json.loads((BASE / "data/m1_rows.json").read_text())
C = json.loads((BASE / "data/clusters.json").read_text())
A = json.loads((BASE / "data/arquitectura.json").read_text())
ZON = json.loads((BASE / "data/zonas.json").read_text())
HAL = json.loads((BASE / "data/hallazgos.json").read_text())
D = json.loads((BASE / "data/m2_dominios.json").read_text())
L = json.loads((BASE / "data/m2_local.json").read_text())
S = json.loads((BASE / "data/m1_serp.json").read_text())
PG = json.loads((BASE / "data/m5_paginas.json").read_text())
SEM = yaml.safe_load((BASE / "config/semillas.yml").read_text())
MAPA = yaml.safe_load((BASE / "config/mapa_urls.yml").read_text())
COST = list(csv.DictReader((BASE / "data/costes.csv").open()))
GASTO = round(sum(float(c["coste_usd"]) for c in COST), 2)
e = lambda x: html.escape("" if x is None else str(x))


def vol(r):
    return r["vol_ch_gads"] if r["vol_ch_gads"] is not None else r["vol_ch_labs"]


def n(x):
    return "sin dato" if x is None else f"{x:,}".replace(",", ".") if isinstance(x, int) else str(x)


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return " ".join("".join(c for c in s if not unicodedata.combining(c)).split())


CSS = """
:root{--bg:#fff;--fg:#1b1f23;--mut:#5b6670;--line:#e3e7ea;--soft:#f5f7f8;--acc:#0b7a75;--alta:#b42318;--media:#b54708;--baja:#4b5563}
@media (prefers-color-scheme:dark){:root{--bg:#0f1214;--fg:#e8eaec;--mut:#9aa4ad;--line:#2a3136;--soft:#171c1f;--acc:#3cc4bc;--alta:#f97066;--media:#fdb022;--baja:#9ca3af}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:1180px;margin:0 auto;padding:40px 20px 80px}
h1,h2,h3{font-family:"Arial Narrow","Roboto Condensed","Helvetica Neue",Arial,sans-serif;font-stretch:condensed;letter-spacing:-.01em;line-height:1.15}
h1{font-size:2.3rem;margin:.2em 0 .3em}h2{font-size:1.55rem;margin:2.2em 0 .6em;padding-top:.6em;border-top:2px solid var(--acc)}h3{font-size:1.15rem;margin:1.6em 0 .4em}
.kicker{color:var(--acc);font-weight:700;text-transform:uppercase;letter-spacing:.08em;font-size:.8rem}
.lead{font-size:1.1rem;color:var(--mut);max-width:820px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:18px 0}
.card{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card b{display:block;font-size:1.6rem;font-family:"Arial Narrow",Arial,sans-serif;color:var(--acc)}
.card span{color:var(--mut);font-size:.88rem}
.tw{overflow-x:auto;margin:10px 0 4px}
table{border-collapse:collapse;width:100%;font-size:.88rem}th,td{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}
th{background:var(--soft);font-weight:600;white-space:nowrap}td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.src{color:var(--mut);font-size:.78rem;margin:2px 0 14px}
.tag{display:inline-block;padding:1px 8px;border-radius:99px;font-size:.75rem;font-weight:700;border:1px solid currentColor}
.alta{color:var(--alta)}.media{color:var(--media)}.baja,.info{color:var(--baja)}
ul.tight li{margin:.2em 0}code{background:var(--soft);padding:1px 5px;border-radius:4px;font-size:.85em}
pre.tree{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:16px;overflow-x:auto;font-size:.85rem;line-height:1.45}
nav.top{display:flex;gap:14px;flex-wrap:wrap;font-size:.85rem;margin-bottom:18px}nav.top a{color:var(--acc);text-decoration:none}
.warn{color:var(--media);font-weight:700}
"""
NAV = '<nav class="top"><a href="index.html">Índice</a><a href="1_investigacion_keywords.html">1 · Keywords</a><a href="2_auditoria_tecnica_local.html">2 · Auditoría</a><a href="3_arquitectura.html">3 · Arquitectura</a><a href="4_estrategia_roadmap.html">4 · Roadmap</a><a href="5_paginas/index.html">5 · Páginas</a></nav>'


def page(nombre, titulo, kicker, cuerpo):
    (E / nombre).write_text(f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titulo)}</title><style>{CSS}</style></head><body><main>{NAV}<div class="kicker">{e(kicker)}</div><h1>{e(titulo)}</h1>{cuerpo}
<p class="src" style="margin-top:50px">physioactiva.ch · investigación SEO FR · generado el {HOY} a partir de DataForSEO (API v3) y del rastreo del sitio. Gasto DataForSEO de la ejecución: {GASTO} USD.</p></main></body></html>""")


def table(cols, rows, src=None, num=()):
    h = "".join(f"<th>{e(c)}</th>" for c in cols)
    b = "".join("<tr>" + "".join(f'<td class="{"n" if i in num else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>' + (f'<p class="src">Fuente: {e(src)}</p>' if src else "")


def cards(items):
    return '<div class="grid">' + "".join(f'<div class="card"><b>{e(v)}</b><span>{e(t)}</span></div>' for v, t in items) + "</div>"


# ---------- datos comunes ----------
def ro(dom, lang="fr"):
    v = D["rank_overview"].get(f"{dom}|{lang}")
    try:
        o = v[0]["items"][0]["metrics"]["organic"]
        return o
    except Exception:
        return {}


def bls(dom, k):
    v = D["bl_summary"].get(dom)
    return v[0].get(k) if isinstance(v, list) and v else None


lp = [k for k, v in S.items() if any("Physio Activa" in (l.get("title") or "") for l in v.get("local_pack", []))]
nkw = len(R)
gads_ok = sum(1 for r in R.values() if r["vol_ch_gads"] is not None)
aio = sum(1 for v in S.values() if v.get("ai_overview"))

# ---------- tabla de contraste ----------
def contraste():
    out = []
    keys = {norm(k): k for k in R}
    rk = {}
    for key in ("physioactiva.ch|fr", "physioactiva.ch|de"):
        for it in (D["ranked"][key][0].get("items") or []):
            kk = norm(it["keyword_data"]["keyword"]); pos_ = it["ranked_serp_element"]["serp_item"]["rank_group"]
            if kk not in rk or pos_ < rk[kk][1]:
                rk[kk] = (it["keyword_data"]["keyword_info"]["search_volume"], pos_)
    for d in SEM["documento"]:
        r = R.get(d["kw"]) or R.get(keys.get(norm(d["kw"]), ""))
        if r and r.get("duplicado_de") and vol(r) is None:
            r = R.get(r["duplicado_de"]) or r
        v = vol(r) if r else None
        pos = r.get("pos_actual") if r else None
        if norm(d["kw"]) in rk:
            v = v if v is not None else rk[norm(d["kw"])][0]
            pos = pos or rk[norm(d["kw"])][1]
        ref = d["ref"]
        if v is None or v < 10:
            ver = "sin volumen → sección o blog"
        elif ref.isdigit():
            ver = "confirmada" if abs(v - int(ref)) <= 0.3 * int(ref) else "corregida"
        else:
            nivel = "Alta" if v >= 500 else "Media" if v >= 50 else "Baja"
            ver = "confirmada" if nivel == ref else f"corregida (los datos dicen {nivel})"
        out.append([e(d["kw"]), e(ref), n(v), n(pos) if pos else "—", e(ver)])
    return out


CONTRASTE = contraste()

# ---------- patologías ⚠ ----------
evid = {}
for t in ["sciatique", "lombalgie", "cervicalgie", "epaule", "coude_main", "genou_lca", "hanche", "cheville_pied", "plancher_pelvien", "atm",
          "vertiges", "neuro", "fibromyalgie", "arthrose", "post_op"]:
    pass
EVID = {"lombalgie": "página propia", "cervicalgie": "página propia", "epaule": "página propia", "genou_lca": "página propia",
        "plancher_pelvien": "página propia", "atm": "página propia", "neuro": "página propia", "post_op": "página propia",
        "sciatique": "mencionada en /mal-de-dos-lombaire/", "cheville_pied": "fasciite y Achille en /physioactiva-ondes-de-choc/; entorse en la página de rodilla",
        "hanche": "mencionada en ondes de choc, Tecar y gériatrique", "arthrose": "mencionada en rodilla, cervical y gériatrique",
        "coude_main": None, "vertiges": None, "fibromyalgie": None}

# ================= 1. KEYWORDS =================
top_cl = [c for c in C if c["tema"] != "marca_competidor"][:45]
TEMAS = yaml.safe_load((BASE / "config/temas.yml").read_text())["temas"]
pat_rows = []
for a in sorted(A["temas"], key=lambda a: -a["volumen_tema"]):
    if a["tipo"] != "patologia":
        continue
    ev = EVID.get(a["tema"])
    pat_rows.append([e(a["nombre"]), n(a["volumen_tema"]), e(a["kw_principal"]), e(a["serp_tipo"]), "sí" if a["ai_overview"] else "no",
                     e("página propia" if a["volumen_tema"] >= 150 else "sección / blog"),
                     e(ev) if ev else '<span class="warn">⚠ el sitio no lo menciona: confirmar con el cliente</span>'])
loc_rows = []
LOCV = json.loads((BASE / "data/m1_local.json").read_text())
for k, v in sorted(LOCV.items(), key=lambda x: -(x[1].get("fr", {}).get("vol") or 0)):
    fr = v.get("fr", {})
    if (fr.get("vol") or 0) > 0:
        loc_rows.append([e(k), n(fr.get("vol")), e(fr.get("cpc")), e(fr.get("comp"))])
top_kw = sorted([r for r in R.values() if r["tema"] != "marca_competidor"], key=lambda r: -(vol(r) or 0))[:120]
cuerpo = f"""<p class="lead">Qué se busca en francés en Suiza (y en la zona de Ins, Seeland y Trois-Lacs) sobre fisioterapia y patologías, cuánto y quién gana hoy cada búsqueda. Keywords en francés; análisis en español.</p>
{cards([(n(nkw), "keywords relevantes tras filtrar 5.792 candidatas"), (n(gads_ok), "con volumen medido en Google Ads (CH-FR)"), (n(len(S)), "SERP analizadas desde Ins"), (n(len(C)), "clústeres por SERP"), (n(len(lp)), "búsquedas donde Physio Activa sale en el mapa (local pack)"), (n(aio), "SERP con AI Overview")])}
<h2>Lo esencial</h2><ul class="tight">
<li><b>La demanda local existe, pero es pequeña:</b> «physio ins» 140/mes, «physio vully» 110, «physio aarberg» 140, «physiothérapie avenches» 50. «physio murten», «physio kerzers» y «physio sugiez» no tienen volumen medible en francés (Google Ads devuelve nulo). Las ciudades grandes del menú sí lo tienen: Biel/Bienne, Lyss, Payerne, Fribourg, Yverdon y Lausanne.</li>
<li><b>El gran volumen está en las patologías y las técnicas:</b> drainage lymphatique (5.400), dry needling (4.400), fasciite plantaire (2.400), kinesio taping (1.900), ménisque (1.600), MTT (1.600), périostite (1.300), lombalgie y douleur en bas du dos (880 cada una).</li>
<li><b>Las búsquedas de patología las dominan los portales médicos</b> y muestran AI Overview: se ganan con páginas realmente informativas, una respuesta directa, FAQ y una llamada a la acción local.</li>
<li><b>Fortaleza clara:</b> Physio Activa aparece en el local pack de {len(lp)} búsquedas desde Ins (physio, physiothérapeute, physio près de moi, physio à domicile…). En orgánico, en cambio, solo entra en el top 10 en una («physiothérapeute à anet», pos. 4).</li>
<li><b>«Physio» (12.100/mes) es un término nacional y bilingüe:</b> el filtro de idioma de Google Ads no separa francés y alemán en Suiza. Se trabaja como «physio à Ins» en la home y se gana desde el mapa.</li></ul>
<h2>Contraste con la auditoría anterior</h2>
<p>Una fila por keyword del documento. Las etiquetas Alta/Media/Baja se comparan con el volumen medido (Alta ≥ 500, Media 50–499, Baja &lt; 50).</p>
{table(["Keyword (documento)", "Valor del documento", "Volumen DataForSEO CH-FR", "Posición actual physioactiva.ch", "Veredicto"], CONTRASTE, f"DataForSEO google_ads/search_volume (2756, fr) y Labs ranked_keywords, {HOY}", num=(2, 3))}
<p class="src">Nota: «physio» pasa de 1.238 a 12.100 porque el dato anterior era probablemente regional; «physiothérapeute» (260 → 6.600) incluye la variante «physiothérapie», que Google Ads agrupa. «MTT» tiene volumen nacional alto (1.600), pero mezcla búsquedas en alemán («MTT-Verordnung», «MTT Therapie»).</p>
<h2>Patologías: viabilidad y confirmación del cliente</h2>
{table(["Patología / tema", "Volumen agregado", "Keyword principal", "Quién gana la SERP", "AI Overview", "Formato", "¿La trata Physioactiva?"], pat_rows, f"DataForSEO + rastreo de physioactiva.ch, {HOY}", num=(1,))}
<p>No se redacta ninguna página marcada con ⚠ hasta que el cliente confirme que trata esa patología.</p>
<h2>Clústeres (top 45 por volumen)</h2>
<p>Dos keywords van a la misma página si comparten ≥ 4 URLs en el top 10 de Google desde Ins. Las variantes sin SERP propia se asignan por léxico al clúster de su tema.</p>
{table(["Clúster (keyword principal)", "Tema", "Nº kw", "Vol. agregado", "Intención", "Gana", "Clínicas/portales en top 10", "Local pack", "AI Overview", "Top 3", "Decisión"],
       [[e(c["cluster"]), e(TEMAS[c["tema"]]["nombre"]), n(c["n_keywords"]), n(c["volumen_agregado"]), e(c["intencion_dominante"]), e(c["tipo_pagina_gana"]),
         f'{c["top10_clinicas"]} / {c["top10_portales"]}', ("sí" + (" (con Physio Activa)" if c["physioactiva_en_local_pack"] else "")) if c["local_pack"] else "no",
         "sí" if c["ai_overview"] else "no", e(", ".join(c["top3"])), e(c["decision"])] for c in top_cl],
       f"DataForSEO serp/google/organic/live/advanced (Ins, fr) + google_ads/search_volume, {HOY}", num=(2, 3))}
<h2>Búsquedas locales (genérica × localidad)</h2>
{table(["Keyword", "Volumen/mes", "CPC USD", "Competencia Ads"], loc_rows, f"DataForSEO google_ads/search_volume (2756, fr), {HOY}. Las combinaciones sin volumen no aparecen.", num=(1,))}
<h2>Top 120 keywords</h2>
{table(["Keyword", "Tema", "Vol. CH", "BE", "FR", "NE", "VD", "Tend. 12 m", "Intención", "KD", "CPC USD", "Pos. actual"],
       [[e(r["keyword"]), e(TEMAS[r["tema"]]["nombre"]), n(vol(r)), n(r["vol_be"]), n(r["vol_fr"]), n(r["vol_ne"]), n(r["vol_vd"]),
         "" if r["tendencia_12m_pct"] is None else f'{r["tendencia_12m_pct"]} %', e(r["intencion"]), "" if r["kd"] is None else r["kd"], "" if r["cpc_usd"] is None else r["cpc_usd"],
         r["pos_actual"] or ""] for r in top_kw],
       f"DataForSEO google_ads/search_volume (CH 2756 y cantones BE 20129, FR 20132, NE 20138, VD 20148; fr) + Labs (KD, intención), {HOY}. Vacío = sin dato.", num=(2, 3, 4, 5, 6, 7, 9, 10, 11))}
<p>Listado completo ({n(nkw)} keywords) en <code>data/keywords.csv</code> y en el Excel. Las descartadas, con su motivo, en <code>data/m1_descartadas.csv</code>.</p>
<h2>Método en una línea</h2><p>Semillas del documento + genéricas × 20 localidades + 45 patologías × 8 modificadores → ampliación con <code>keyword_suggestions</code> e <code>keyword_ideas</code> (Labs, CH-FR) → filtro determinista (oficios, Francia, alemán, otras ciudades, marcas) → volumen Google Ads (CH y 4 cantones) → intención y KD → SERP desde Ins → clústeres. Umbrales en <code>config/umbrales.yml</code>; decisiones en <code>decisiones.md</code>.</p>
"""
page("1_investigacion_keywords.html", "Investigación de keywords FR · physioactiva.ch", "Módulo 1", cuerpo)

# ================= 2. AUDITORÍA =================
doms = ["physioactiva.ch", "physiodulac-physioduparc.ch", "physioptima.ch", "physiotherapie-kerzers.ch", "physiomurten.ch", "physioplus-avenches.com", "physio-7.ch", "physio-clinics.ch", "therapie-ins-seeland.ch"]
aut = []
for d in doms:
    o, od = ro(d, "fr"), ro(d, "de")
    t3 = lambda o: None if not o else (o.get("pos_1") or 0) + (o.get("pos_2_3") or 0)
    aut.append([f"<b>{e(d)}</b>" if d == "physioactiva.ch" else e(d), n(t3(o)), n((t3(o) or 0) + (o.get("pos_4_10") or 0) if o else None), n(o.get("pos_11_20")), n(o.get("count")),
                n(round(o["etv"], 1) if o.get("etv") is not None else None), n(od.get("count")), n(bls(d, "rank")), n(bls(d, "referring_domains")), n(bls(d, "backlinks_spam_score"))])
hist = D["historical"]["physioactiva.ch"][0]["items"]
blh = D["bl_history"]["physioactiva.ch"][0]["items"]
rev = []
for k, v in L["reviews"].items():
    it = v["items"]
    ult12 = sum(1 for i in it if i["date"] and i["date"][:7] >= "2025-11")
    rev.append([e(k), n(v["reviews_count"]), n(v["rating"]["value"]), f'{sum(i["respondida"] for i in it)} / {len(it)}', n(ult12), e(it[0]["date"][:10] if it else "")])
mrows = [[e(z["ciudad"]), n(z["km_linea_recta_desde_ins"]), n(z["maps_physio_pos_physioactiva"]) if z["maps_physio_pos_physioactiva"] else "fuera del top 20",
          n(z["maps_domicile_pos_physioactiva"]) if z["maps_domicile_pos_physioactiva"] else "fuera del top 20", e(", ".join(z["maps_top3"]))] for z in ZON]
hal_rows = [[f'<span class="tag {h["severidad"]}">{e(h["severidad"])}</span>', e(h["bloque"]), f'<b>{e(h["titulo"])}</b><br><span class="src">{e(", ".join(h["urls"][:8]))}{" …" if len(h["urls"]) > 8 else ""}</span>',
             e(h["evidencia"]), e(h["accion"]), n(h["esfuerzo_h"]), e(h["estado_vs_auditoria_previa"]), e(h["fuente"])] for h in HAL]
sev = collections.Counter(h["severidad"] for h in HAL)
cuerpo = f"""<p class="lead">Lo que frena hoy a physioactiva.ch en Google, medido. Cada hallazgo lleva evidencia, fuente y acción.</p>
{cards([(sev["alta"], "hallazgos de severidad alta"), (sev["media"], "de severidad media"), (n(L["on_page"]["summary"]["crawl_status"]["pages_crawled"]), "URLs rastreadas por DataForSEO (FR + /de/)"), (A["indice_autoridad"], "índice de autoridad (rank propio / mediana de los locales)")])}
<h2>Hallazgos</h2>
{table(["Severidad", "Bloque", "Hallazgo y URLs", "Evidencia", "Acción", "Horas", "Frente a la auditoría previa", "Fuente"], hal_rows)}
<h2>Autoridad: physioactiva.ch frente a la competencia</h2>
{table(["Dominio", "Top 3 (FR)", "Top 10 (FR)", "Pos. 11-20 (FR)", "Keywords posicionadas (FR)", "Tráfico estimado FR*", "Keywords posicionadas (DE)", "Rank enlaces", "Dominios de referencia", "Spam score"], aut,
       f"DataForSEO dataforseo_labs/google/domain_rank_overview (2756) y backlinks/summary, {HOY}. *Estimación de DataForSEO, no tráfico real (el real sale de GSC/GA4, no disponibles en esta ejecución). therapie-ins-seeland.ch no tiene datos en DataForSEO.", num=tuple(range(1, 10)))}
<p><b>Lectura:</b> los competidores locales (Physio du Lac, PhysiOptima, Kerzers, Physio Murten, Physio Plus Avenches) también son débiles en orgánico: ninguno tiene más de 5 keywords en francés. Las cadenas (physio-7.ch, physio-clinics.ch) sí dominan las búsquedas genéricas. El hueco orgánico local está libre, y el índice de autoridad de {A["indice_autoridad"]} aconseja empezar por clústeres con SERP local y KD bajo antes que por los términos genéricos.</p>
<h3>Evolución de physioactiva.ch</h3>
{table(["Mes", "Keywords posicionadas (FR)", "Tráfico estimado"], [[f'{i["year"]}-{i["month"]:02d}', n(i["metrics"]["organic"].get("count")), n(round(i["metrics"]["organic"].get("etv") or 0, 1))] for i in hist],
       f"DataForSEO historical_rank_overview (2756, fr), {HOY}", num=(1, 2))}
{table(["Mes", "Dominios de referencia", "Nuevos", "Perdidos"], [[e(i["date"][:7]), n(i.get("referring_domains")), n(i.get("new_referring_domains")), n(i.get("lost_referring_domains"))] for i in blh],
       f"DataForSEO backlinks/history, {HOY}", num=(1, 2, 3))}
<h2>Reseñas de Google</h2>
{table(["Ficha", "Reseñas", "Nota", "Respondidas (muestra)", "Reseñas en los últimos 12 meses (muestra)", "Última"], rev,
       f"DataForSEO business_data/google/reviews (muestra: hasta 50 más recientes), {HOY}", num=(1, 2, 4))}
<h2>Google Maps por localidad («physio» y «physiothérapie à domicile»)</h2>
{table(["Localidad", "km desde Ins (línea recta)", "Pos. Physio Activa «physio»", "Pos. «à domicile»", "Top 3 en Maps («physio»)"], mrows,
       f"DataForSEO serp/google/maps/live/advanced (centro aproximado de cada localidad, zoom 13, top 20), {HOY}", num=(1,))}
<h2>Bloques no disponibles en esta ejecución</h2><ul class="tight"><li><b>Search Console y GA4:</b> sin acceso. Hace falta un export de GSC (consultas y páginas, 16 meses) y acceso de lectura a GA4 (eventos de WhatsApp, OneDoc y teléfono).</li>
<li><b>Core Web Vitals reales:</b> PageSpeed Insights / CrUX no consultados; on_page solo detecta recursos que bloquean el renderizado.</li>
<li><b>physiodom.ch:</b> no se consulta (regla del repositorio). Hay que comprobar a mano que su 301 apunta a https://physioactiva.ch/ página a página.</li>
<li><b>NAP en directorios</b> (local.ch, search.ch, Apple, Bing): requiere revisión manual.</li></ul>
"""
page("2_auditoria_tecnica_local.html", "Auditoría técnica y local · physioactiva.ch", "Módulo 2", cuerpo)

# ================= 3. ARQUITECTURA =================
T = A["temas"]
byt = {a["tema"]: a for a in T}
def li(t, extra=""):
    a = byt.get(t)
    return f"{a['url']}  — {a['nombre']} · {n(a['volumen_tema'])}/mes · {a['accion']}{extra}" if a else ""
tree = f"""Accueil  /  — « Physio à Ins (Anet) · à domicile dans le Seeland et les Trois-Lacs »  ({n(byt['home']['volumen_tema'])}/mes genéricas + local pack)
├── Pathologies traitées (hub)  /pour-les-patients/  — se reutiliza, sin 301
│   ├── Dos & colonne
│   │   ├── {li('lombalgie')}
│   │   ├── {li('sciatique')}
│   │   └── {li('cervicalgie')}
│   ├── {li('epaule')}
│   ├── {li('genou_lca')}   (se centra en rodilla)
│   ├── {li('cheville_pied')}
│   ├── {li('hanche')}
│   ├── {li('plancher_pelvien')}
│   ├── {li('atm')}
│   └── ⚠ pendientes de confirmación: épicondylite / canal carpien ({n(byt['coude_main']['volumen_tema'])}/mes) · vertiges ({n(byt['vertiges']['volumen_tema'])}) · fibromyalgie ({n(byt['fibromyalgie']['volumen_tema'])})
├── Traitements & techniques (hub)  /physio/  — reconvertir (hoy duplica el H1 de MTT)
│   ├── {li('lymph')}
│   ├── {li('dry_needling')}
│   ├── {li('taping')}
│   ├── {li('mtt')}   ← fusionar /fitness-medical/ (301)
│   ├── {li('massage')}
│   ├── {li('sport')}
│   ├── {li('tecar')}
│   ├── {li('ondes_choc')}
│   ├── {li('post_op')}
│   └── thérapie manuelle, neurologique, gériatrique, cardiorespiratoire, uro-gynécologie (se mantienen, fuera del foco SEO)
├── {li('domicile')}   (página fuerte, transaccional)
├── Zones  (solo las que pasan la regla antipuerta: ver tabla)
├── À propos · Contact · Nous trouver
└── Prendre rendez-vous  /reservation-en-ligne/  (UNA URL canónica)"""
arq_rows = [[n(a["prioridad"]), e(a["url"]), e(a["nombre"]), e(a["accion"]), e(a["kw_principal"]), n(a["vol_kw_principal"]), n(a["volumen_tema"]), e(a["intencion"]),
             e(a["serp_tipo"]), e(" · ".join(a["secciones_h2"][:5])), e(" · ".join(a["candidatas_fase2"][:4]))] for a in T]
redir = [[e(u), e(MAPA["reserva"]["canonica"]), "duplicado de reserva"] for u in MAPA["reserva"]["redirigir"]]
redir += [["/online-termin-buchen/", "/de/ (versión alemana) o " + MAPA["reserva"]["canonica"], "H1 en alemán: decide el cliente"],
          ["/fitness-medical/", "/medical-training-therapy-mtt/", "canibalización MTT / fitness médical"],
          ["/douleurs-cervicales", "/douleur-cervicale-au-cou/", "404 enlazada desde el hub"], ["/douleurs-genou", "/douleur-du-genou-lesions-de-la-cheville/", "404 enlazada desde el hub"],
          ["/lesions-cheville", "/douleur-pied-cheville-fasciite-plantaire/", "404 enlazada desde el hub"], ["/lesions-epaule", "/lesions-de-lepaule/", "404 enlazada desde el hub"],
          ["/mtt-fitness-medical", "/medical-training-therapy-mtt/", "404 enlazada desde post-opératoire"],
          ["/physio-en-uro-gynecologie/", "/physiotherapie-du-plancher-pelvien/ (solo si se fusiona)", "pendiente de validación"]]
noidx = [[e(u), "noindex + fuera del sitemap"] for u in MAPA["noindex"]]
links = [["Patología → técnicas", "lombalgie → thérapie manuelle, MTT, puncture sèche, Tecar · sciatique → lombalgie, MTT · épaule → ondes de choc, post-op · genou → post-op, MTT, sport, taping · pied/cheville → ondes de choc, taping, sport · hanche → post-op, MTT, gériatrique"],
         ["Patología → conversión", "todas → /physiotherapeute-a-domicile/ y /reservation-en-ligne/ (CTA teléfono, WhatsApp, OneDoc)"],
         ["Técnica → patologías", "ondes de choc → épaule, pied/cheville · puncture sèche → lombalgie, cervicalgie · MTT → genou, hanche, lombalgie · taping → genou, pied/cheville · Tecar → lombalgie, sciatique"],
         ["Zona → patologías", "cada zona → las 3-5 patologías con más volumen (lombalgie, pied/cheville, genou, épaule, sciatique)"],
         ["Accueil →", "hub de patologías + top 6 patologías + domicile + reserva"],
         ["Anchors", "descriptivos («physio pour une sciatique à Ins»), nunca «cliquez ici»"]]
zrows = [[e(z["ciudad"]), n(z["km_linea_recta_desde_ins"]), n(z["volumen_total"]), e(", ".join(f"{k} ({v})" for k, v in z["keywords_con_volumen"].items()) or "—"),
          n(z["maps_physio_pos_physioactiva"]) if z["maps_physio_pos_physioactiva"] else "—", e(z["url_existente"] or "—"), e(z["decision"])] for z in ZON]
cuerpo = f"""<p class="lead">El árbol final del sitio, construido a partir de los clústeres: qué página ataca cada búsqueda, qué se crea, qué se optimiza y qué se redirige.</p>
<h2>Árbol</h2><pre class="tree">{e(tree)}</pre>
<p class="src">Volúmenes: DataForSEO google_ads/search_volume (CH-FR), {HOY}. «Volumen del tema» = suma de los clústeres asignados, sin contar dos veces las variantes que Google Ads agrupa.</p>
<h2>URL ↔ clúster ↔ keyword principal ↔ acción</h2>
{table(["Prioridad", "URL", "Página", "Acción", "Keyword principal", "Vol. kw", "Vol. tema", "Intención", "SERP", "Secciones H2 (clústeres secundarios)", "Candidatas a página propia (fase 2)"], arq_rows,
       f"Cálculo propio sobre datos de DataForSEO, {HOY}. Prioridad = impacto × confianza / esfuerzo (sección 9, pesos en config/umbrales.yml).", num=(0, 5, 6))}
<h2>Plan de redirecciones 301</h2>{table(["Origen", "Destino", "Motivo"], redir)}
<h2>Noindex</h2>{table(["URL", "Acción"], noidx)}
<h2>Matriz de enlazado interno</h2>{table(["Regla", "Enlaces"], links)}
<h2>Zonas: regla antipuerta</h2>
<p>Una sola dirección física: una página de zona solo se publica si aporta información real y propia de esa zona (desplazamiento, si hay atención a domicilio allí, médicos u hospitales cercanos, preguntas locales y datos de su local pack). Si solo cambia el nombre de la ciudad, no se publica.</p>
{table(["Localidad", "km desde Ins", "Vol. local (FR)", "Keywords con volumen", "Pos. en Maps («physio»)", "URL actual", "Decisión"], zrows,
       f"DataForSEO google_ads/search_volume y serp/google/maps, {HOY}. Distancia en línea recta desde el centro de Ins (aproximada).", num=(1, 2, 4))}
<p>Murten/Morat y Kerzers/Chiètres no tienen volumen medible en francés (son localidades germanófonas o bilingües): sus páginas valen para la fase DE o si el cliente confirma que tiene pacientes a domicilio allí.</p>
"""
page("3_arquitectura.html", "Arquitectura del sitio · physioactiva.ch", "Módulo 3", cuerpo)

# ================= 4. ESTRATEGIA =================
o = ro("physioactiva.ch", "fr")
top10_now = (o.get("pos_1") or 0) + (o.get("pos_2_3") or 0) + (o.get("pos_4_10") or 0)
set_obj = [a["kw_principal"] for a in T]
fases = [
    ("Mes 1 · Técnica (bloquea todo lo demás)", [h for h in HAL if h["severidad"] == "alta" and h["bloque"] in ("Indexación", "On-page", "Técnica", "Local")]),
]
prio_rows = [[n(a["prioridad"]), e(a["nombre"]), e(a["url"]), e(a["accion"]), n(a["impacto"]), n(a["confianza"]), n(a["esfuerzo_h"])] for a in T]
road = [
    ["Mes 1", "Técnica + local", "Reserva canónica y 301 · /merci/ y archivos en noindex · arreglar los 404 del hub y los enlaces del menú · lang fr-CH · schema Physiotherapy · confirmar dirección (21 o 31) y corregir la URL de la ficha · restaurar o despublicar los 4 posts duplicados · reseñas: QR + WhatsApp", "≈ 10 h", "—"],
    ["Mes 1-2", "Home + hub + 4 patologías existentes", "Publicar los textos del módulo 5: accueil, /pour-les-patients/, lombalgie, cervicalgie, épaule y genou (yoast.txt + schema.json)", "≈ 14 h", "Mes 1"],
    ["Mes 2-3", "Patologías nuevas", "Publicar /sciatique-hernie-discale/, /douleur-pied-cheville-fasciite-plantaire/ y /douleur-de-hanche-protheses/ tras la revisión clínica; enlazarlas desde la home, el hub y las técnicas", "≈ 15 h", "Mes 1-2"],
    ["Mes 3-4", "Técnicas con más volumen", "Optimizar drainage lymphatique, dry needling, taping, MTT (+ fusión de fitness-medical), massage thérapeutique y physio du sport con la misma plantilla", "≈ 14 h", "Mes 1"],
    ["Mes 4-5", "Zonas", "Sugiez y Neuchâtel (existentes) con datos reales; nuevas: La Neuveville, Avenches, Lyss, Biel/Bienne, Payerne y Fribourg, solo con contenido propio (regla 8.2)", "≈ 4-6 h/zona", "Mes 2-3 + datos del cliente"],
    ["Mes 5-6", "Autoridad", "Altas en directorios (physio-verzeichnis.ch, regionalinfo-schweiz.ch, better-search.ch, local.ch, search.ch), physioswiss, InsGym, clubes y comuna; vigilancia de enlaces spam", "≈ 6 h", "—"],
    ["Mes 6-12", "Fase 2", "Clústeres candidatos a página propia (ménisque, périostite, coiffe des rotateurs, prothèse genou…), patologías ⚠ confirmadas, blog que enlace a patologías y versión DE", "según datos de GSC", "Mes 3"],
]
cuerpo = f"""<p class="lead">Situación en una página, objetivos medibles y plan mes a mes. La prioridad sale de una fórmula, no de una opinión.</p>
<h2>Situación</h2>
{cards([(n(o.get("count")), "keywords FR donde physioactiva.ch está en el top 100"), (n(top10_now), "keywords FR en el top 10 (Labs)"), (n(len(lp)), "búsquedas desde Ins con Physio Activa en el local pack"), (f'{L["reviews"]["Physio Activa Ins"]["reviews_count"]} · {L["reviews"]["Physio Activa Ins"]["rating"]["value"]}', "reseñas · nota en Google"), (n(bls("physioactiva.ch", "referring_domains")), "dominios de referencia (muchos de spam)")])}
<ul class="tight"><li><b>Lo que funciona:</b> la ficha de Google (nota 5, todas las reseñas respondidas) y el local pack en Ins.</li>
<li><b>Lo que frena:</b> titles genéricos, 6 URLs de reserva, enlaces rotos en el hub, posts duplicados, ausencia de páginas para las patologías con más búsqueda y poca autoridad de enlaces.</li>
<li><b>La oportunidad:</b> los competidores locales apenas existen en orgánico; las patologías tienen volumen, y el AI Overview recompensa las páginas claras con FAQ.</li></ul>
<h2>Objetivos (parten del valor medido hoy)</h2>
{table(["Indicador", "Hoy", "3 meses", "6 meses", "12 meses", "Cómo se mide"], [
    ["Keywords del set objetivo en el top 10 (FR, CH)", n(top10_now), "3", "8", "15", "DataForSEO ranked_keywords (mismo set, mensual)"],
    ["Keywords del set objetivo en el top 3", "0", "1", "3", "6", "DataForSEO ranked_keywords"],
    ["Búsquedas con Physio Activa en el local pack (SERP desde Ins)", n(len(lp)), f"≥ {len(lp)}", f"≥ {len(lp) + 5}", f"≥ {len(lp) + 10}", "DataForSEO SERP Ins (mismo set)"],
    ["Reseñas en Google", n(L["reviews"]["Physio Activa Ins"]["reviews_count"]), "[POR CONFIRMAR]", "[POR CONFIRMAR]", "[POR CONFIRMAR]", "business_data/google/reviews"],
    ["Clics orgánicos / impresiones", "no disponible", "base + objetivo tras export GSC", "", "", "Search Console"],
    ["Conversiones orgánicas (WhatsApp, OneDoc, teléfono)", "no disponible", "configurar eventos", "", "", "GA4"]],
    "Objetivos propuestos sobre el valor actual medido. Los de GSC/GA4 se fijan cuando haya datos.", num=(1,))}
<h2>Prioridad calculada</h2>
{table(["Prioridad", "Página", "URL", "Acción", "Impacto (1-5)", "Confianza (1-3)", "Esfuerzo (h)"], prio_rows,
       "prioridad = impacto × confianza / esfuerzo. Impacto = volumen normalizado (log) × factor de intención × ganabilidad × ajuste de autoridad. Detalle en decisiones.md.", num=(0, 4, 5, 6))}
<p>Las dependencias mandan sobre la fórmula: primero la técnica, después la home y las 4 patologías existentes, luego las patologías nuevas y al final las zonas.</p>
<h2>Roadmap</h2>{table(["Cuándo", "Bloque", "Tareas", "Esfuerzo", "Depende de"], road)}
<h2>Aprobaciones del cliente (bloquean)</h2><ul class="tight">
<li>Patologías que tratan de verdad: épicondylite / canal carpien, vertiges, fibromyalgie (⚠).</li>
<li>URL de reserva canónica (propuesta: /reservation-en-ligne/) y destino de /online-termin-buchen/.</li>
<li>Dirección: Rämismatte 21 (sitio y ficha) o 31 (encargo).</li>
<li>Zonas lejanas (Lausanne, Yverdon, Yvonand; también Estavayer, a más de 25 km) como zonas reales de servicio.</li>
<li>Nombres, titulaciones y foto de Francisco Díaz y Lucile Combes para la autoría (E-E-A-T); horario (la ficha dice lunes a viernes de 8:30 a 19:30 y el sitio, «jusqu'à 20h»).</li>
<li>Revisión clínica de cada página de patología antes de publicarla.</li></ul>
"""
page("4_estrategia_roadmap.html", "Estrategia y roadmap · physioactiva.ch", "Módulo 4", cuerpo)

# ================= 5. índice de páginas =================
prow = [[f'<a href="{e(p["slug"])}/fr.html">{e(p["slug"])}</a>', e(p["url"]), e(p["tipo"]), e(p["keyword_principal"]), f'{e(p["title"])} <span class="src">({p["len_title"]})</span>',
         f'{e(p["meta"])} <span class="src">({p["len_meta"]})</span>', n(p["palabras"]), n(p["faq"]), n(p["por_confirmar"])] for p in PG]
(E / "5_paginas").mkdir(exist_ok=True)
(E / "5_paginas/index.html").write_text(f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Páginas del primer lote · physioactiva.ch</title><style>{CSS}</style></head><body><main>
{NAV.replace('href="', 'href="../').replace('href="../5_paginas/index.html"', 'href="index.html"')}<div class="kicker">Módulo 5</div><h1>Páginas del primer lote (copy en francés)</h1>
<p class="lead">Cada carpeta contiene <code>brief.md</code>, <code>fr.md</code>, <code>fr.html</code>, <code>fr-ascii.html</code>, <code>yoast.txt</code> y <code>schema.json</code>. El <code>elementor.json</code> queda pendiente: falta el JSON de referencia de la plantilla (<code>lombaire-elementor.json</code>).</p>
{table(["Carpeta", "URL", "Tipo", "Keyword principal", "SEO title", "Meta description", "Palabras", "FAQ", "[POR CONFIRMAR]"], prow, "Textos redactados a partir de los briefs; title ≤ 60 y meta ≤ 155 validados por script.", num=(6, 7, 8))}
<p><b>Antes de publicar:</b> revisión clínica de cada patología y resolver los [POR CONFIRMAR]. «Épicondylite / canal carpien» no se ha redactado (⚠ falta la confirmación del cliente).</p></main></body></html>""")

# ================= índice =================
idx = f"""<p class="lead">Investigación SEO en francés de physioactiva.ch: physio y patologías en Ins, el Seeland y los Trois-Lacs. Informe en español; keywords y textos de la web en francés de Suiza.</p>
{cards([(n(nkw), "keywords analizadas"), (n(len(C)), "clústeres"), (len(HAL), "hallazgos"), (len(PG), "páginas redactadas en francés"), (f"{GASTO} USD", "gasto DataForSEO")])}
<h2>Entregables</h2><ul class="tight"><li><a href="1_investigacion_keywords.html">1 · Investigación de keywords</a></li><li><a href="2_auditoria_tecnica_local.html">2 · Auditoría técnica y local</a></li>
<li><a href="3_arquitectura.html">3 · Arquitectura</a></li><li><a href="4_estrategia_roadmap.html">4 · Estrategia y roadmap</a></li><li><a href="5_paginas/index.html">5 · Páginas del primer lote (FR)</a></li>
<li>Excel con todo: <code>entregables/physioactiva-seo.xlsx</code></li></ul>"""
page("index.html", "SEO physioactiva.ch · FR", "Índice", idx)

# ================= Excel =================
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
wb = Workbook()
def hoja(nombre, cols, filas, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = nombre
    ws.append(cols)
    for f in filas:
        ws.append(["" if x is None else x for x in f])
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="0B7A75"); c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
    for i, col in enumerate(cols, 1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = min(60, max(10, len(str(col)) + 2))
kcols = ["keyword", "tema", "cluster", "ciudad", "vol_ch_gads", "vol_ch_labs", "vol_be", "vol_fr", "vol_ne", "vol_vd", "tendencia_12m_pct", "serie_12m", "intencion", "kd", "cpc_usd", "competencia_ads", "pos_actual", "url_actual", "local_pack_physioactiva", "origen", "fuente"]
hoja("Keywords", kcols, [[r.get(c) for c in kcols] for r in sorted(R.values(), key=lambda r: -(vol(r) or 0))], first=True)
hoja("Clusters", ["cluster", "tema", "n_keywords", "volumen_agregado", "intencion", "tipo_pagina_gana", "clinicas_top10", "portales_top10", "local_pack", "physioactiva_en_local_pack", "ai_overview", "top3", "paa", "decision", "keywords"],
     [[c["cluster"], c["tema"], c["n_keywords"], c["volumen_agregado"], c["intencion_dominante"], c["tipo_pagina_gana"], c["top10_clinicas"], c["top10_portales"], c["local_pack"], c["physioactiva_en_local_pack"], c["ai_overview"], " | ".join(c["top3"]), " | ".join(c["paa"]), c["decision"], " | ".join(c["keywords"])] for c in C])
hoja("Contraste", ["keyword", "valor_documento", "volumen_dataforseo", "posicion_actual", "veredicto"], [[re.sub("<[^>]+>", "", html.unescape(str(x))) for x in r] for r in CONTRASTE])
hoja("Arquitectura", ["prioridad", "url", "pagina", "accion", "kw_principal", "vol_kw", "vol_tema", "intencion", "serp", "impacto", "confianza", "esfuerzo_h", "secciones_h2", "fase2"],
     [[a["prioridad"], a["url"], a["nombre"], a["accion"], a["kw_principal"], a["vol_kw_principal"], a["volumen_tema"], a["intencion"], a["serp_tipo"], a["impacto"], a["confianza"], a["esfuerzo_h"], " | ".join(a["secciones_h2"]), " | ".join(a["candidatas_fase2"])] for a in T])
hoja("Zonas", ["ciudad", "km_desde_ins", "volumen_total", "keywords", "maps_pos_physio", "maps_pos_domicile", "maps_top3", "url_existente", "decision"],
     [[z["ciudad"], z["km_linea_recta_desde_ins"], z["volumen_total"], " | ".join(f"{k} ({v})" for k, v in z["keywords_con_volumen"].items()), z["maps_physio_pos_physioactiva"], z["maps_domicile_pos_physioactiva"], " | ".join(z["maps_top3"]), z["url_existente"], z["decision"]] for z in ZON])
hoja("Hallazgos", ["id", "severidad", "bloque", "titulo", "urls", "evidencia", "accion", "esfuerzo_h", "estado_vs_previa", "fuente"],
     [[h["id"], h["severidad"], h["bloque"], h["titulo"], " | ".join(h["urls"]), h["evidencia"], h["accion"], h["esfuerzo_h"], h["estado_vs_auditoria_previa"], h["fuente"]] for h in HAL])
hoja("Paginas FR", ["carpeta", "url", "tipo", "keyword_principal", "title", "len_title", "meta", "len_meta", "h1", "palabras", "faq", "por_confirmar"],
     [[p["slug"], p["url"], p["tipo"], p["keyword_principal"], p["title"], p["len_title"], p["meta"], p["len_meta"], p["h1"], p["palabras"], p["faq"], p["por_confirmar"]] for p in PG])
hoja("Costes", ["fecha", "ejecucion", "endpoint", "coste_usd", "status", "tareas"], [[c["fecha"], c["ejecucion"], c["endpoint"], float(c["coste_usd"]), c["status"], c["tareas"]] for c in COST])
wb.save(E / "physioactiva-seo.xlsx")
print("ok", GASTO)
