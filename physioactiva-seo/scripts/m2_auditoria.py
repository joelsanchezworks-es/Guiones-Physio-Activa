"""Módulo 2 · reglas de auditoría → data/hallazgos.json (determinista: mismas entradas = mismos hallazgos)."""
import json, sys, pathlib, re, collections, statistics
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dfs
BASE = dfs.BASE
U = dfs.UMB["severidad"]
P = json.loads((BASE / "data/site/paginas.json").read_text())
L = json.loads((BASE / "data/m2_local.json").read_text())
D = json.loads((BASE / "data/m2_dominios.json").read_text())
S = json.loads((BASE / "data/m1_serp.json").read_text())
F = f"rastreo propio + DataForSEO on_page {dfs.HOY}"
path = lambda u: u.replace("https://physioactiva.ch", "") or "/"
H = []


def add(bloque, sev, titulo, urls, evidencia, accion, esfuerzo, fuente=F, previo="nuevo"):
    H.append({"id": f"H{len(H) + 1:02d}", "bloque": bloque, "severidad": sev, "titulo": titulo, "urls": urls,
              "evidencia": evidencia, "fuente": fuente, "accion": accion, "esfuerzo_h": esfuerzo, "estado_vs_auditoria_previa": previo})


pag = {path(p["url"]): p for p in P}
op = L["on_page"]
pm = op["summary"].get("page_metrics", {})
items = op["pages"][0]["items"]

# --- Indexación ---
reservas = ["/online-termin-buchen/", "/reservation-en-ligne/", "/reserver-maintenant/", "/rendez-vous-des-maintenant/", "/reserve/", "/rendez-vous-online/"]
add("Indexación", "alta", "6 URLs de reserva indexables que compiten entre sí", reservas,
    "Las 6 URLs responden 200, son indexables y están en el sitemap; 4 comparten H1 «Physiothérapie en cabinet et à domicile dès cette semaine» y la misma meta.",
    "Dejar /reservation-en-ligne/ como canónica (aprobación del cliente); 301 de /reserver-maintenant/, /rendez-vous-des-maintenant/, /reserve/ y /rendez-vous-online/ hacia ella; /online-termin-buchen/ (H1 en alemán) a la versión /de/ o 301; actualizar todos los botones.", 1.5, previo="pendiente (ya detectado)")
add("Indexación", "media", "/merci/ indexable y en el sitemap", ["/merci/"], f"robots: «{pag['/merci/']['robots'][:40]}…»; incluida en page-sitemap.xml.",
    "Yoast → «¿Permitir que los motores muestren esta página?» = No (noindex) y fuera del sitemap.", 0.25, previo="pendiente (ya detectado)")
add("Indexación", "baja", "Páginas de archivo de autor y categorías indexables", ["/author/joel/", "/category/domicile-sugiez/", "/category/nos-soins/"],
    "Indexables y sin meta description; la de autor muestra «Joel Nova Agency» (la agencia, no un fisioterapeuta).",
    "Yoast → noindex para archivos de autor y categorías; quitar los archivos de autor del sitemap.", 0.25)
rotos = [path(p["url"]) for p in items if p["status_code"] == 404]
add("Indexación", "alta", f"{len(rotos)} URLs internas devuelven 404 (enlaces rotos en el hub de patologías)", rotos,
    "El hub /pour-les-patients/ enlaza a /douleurs-cervicales, /douleurs-genou, /lesions-cheville y /lesions-epaule (404); /physiotherapie-post-operatoire/ enlaza a /mtt-fitness-medical (404). Las mismas en /de/.",
    "Corregir los enlaces hacia /douleur-cervicale-au-cou/, /douleur-du-genou-lesions-de-la-cheville/, /douleur-pied-cheville-fasciite-plantaire/, /lesions-de-lepaule/ y /medical-training-therapy-mtt/; añadir 301 de las URL rotas por si tienen enlaces externos.", 0.75)
red = [path(p["url"]) for p in items if p["status_code"] == 301]
add("Indexación", "media", "El menú enlaza a URLs que redirigen (301)", red,
    f"{pm.get('checks', {}).get('has_links_to_redirects')} páginas enlazan a /mal-de-dos, /fitness-medica, /drainage-lymphatique (sin barra) y /physiotherapie-a-domicile, que redirigen.",
    "Cambiar en el menú y en el pie las URLs por la versión final (con barra y slug real).", 0.5)
add("Indexación", "media", "Versión /de/ publicada con títulos y contenidos en francés", ["/de/"],
    "La versión /de/ (42 URLs rastreadas) tiene hreflang fr/de, pero títulos como «Accueil - Physio Activa» siguen en francés: on_page detecta 34 títulos y 20 metas duplicados entre /fr y /de.",
    "Fase posterior DE: traducir títulos/metas o poner noindex en /de/ hasta traducirla de verdad. Mientras tanto, evitar que compita con la versión FR.", 1)

# --- On-page ---
cortos = [u for u, p in pag.items() if len(p["title"]) < 35 and u not in ("/merci/",)]
add("On-page", "alta", "Titles genéricos sin keyword ni localidad", cortos[:20],
    "Patrón «[Nombre de página] - Physio Activa» (p. ej. home: «Accueil - Physio Activa», 23 caracteres; /physio/: «Physio - Physio Activa»). on_page: %s titles demasiado cortos." % pm.get("checks", {}).get("title_too_short"),
    "Reescribir con la plantilla «[keyword] à Ins | Physio Activa» (≤ 60 caracteres): ver yoast.txt de cada página del primer lote.", 2, previo="pendiente (ya detectado)")
largas = [u for u, p in pag.items() if len(p["meta_description"]) > U["meta_max"]]
add("On-page", "baja", "Metas de más de 155 caracteres (se cortan)", largas,
    "; ".join(f"{u}: {len(pag[u]['meta_description'])}" for u in largas), "Recortar a 120-155 caracteres con keyword + localidad + CTA.", 0.5)
add("On-page", "alta", "H1 incorrecto en /physio/", ["/physio/"], f"H1 actual: «{pag['/physio/']['h1'][0]}» (copiado de la página MTT).",
    "Convertir /physio/ en el hub «Traitements & techniques» con H1 propio, o redirigirla a la home si no se usa.", 0.5)
add("On-page", "alta", "Los 4 artículos del blog tienen el mismo H1 y el mismo contenido", [u for u in pag if u.startswith("/2026/")],
    "Los 4 posts muestran el H1 «Drainage lymphatique manuel : ce que c'est et à quoi ça sert» y los mismos H2: la plantilla del artículo de drainage se aplicó a todos. on_page: %s páginas con contenido duplicado." % pm.get("duplicate_content"),
    "Restaurar el contenido propio de cada post o despublicarlos; después reescribirlos como artículos que enlacen a las páginas de patología.", 2)
add("On-page", "media", "Canibalizaciones de servicios", ["/physio/", "/physio-generale/", "/medical-training-therapy-mtt/", "/fitness-medical/", "/physiotherapie-du-plancher-pelvien/", "/physio-en-uro-gynecologie/"],
    "/physio/ y /medical-training-therapy-mtt/ tienen el mismo H1; /fitness-medical/ y /medical-training-therapy-mtt/ atacan «MTT / fitness médical» (Labs: physioactiva.ch rankea con /fitness-medical/ en «fitness medical», pos. 18, y con /medical-training-therapy-mtt/ en «mtt», pos. 36).",
    "Fusionar /fitness-medical/ en /medical-training-therapy-mtt/ (301). Diferenciar uro-gynécologie (mujer, embarazo, posparto) de plancher pelvien o fusionarlas tras validarlo con el cliente.", 1.5, fuente=f"rastreo + DataForSEO Labs ranked_keywords {dfs.HOY}")
add("On-page", "media", "Imágenes sin texto alternativo", ["(todas las plantillas)"], f"on_page: {pm.get('checks', {}).get('no_image_alt')} páginas con imágenes sin alt.",
    "Añadir alt descriptivo en francés (qué muestra + contexto: «Physiothérapeute traitant une épaule au cabinet à Ins»).", 1.5)
add("On-page", "media", "Contenido escaso en páginas de servicio", [u for u, p in pag.items() if p["palabras"] < U["palabras_min_pagina_servicio"] and u.count("/") == 2 and u not in ("/merci/",) + tuple(reservas)],
    "Páginas con menos de %d palabras (rastreo propio)." % U["palabras_min_pagina_servicio"], "Ampliar con el formato del módulo 5 (qué es, para quién, cómo, reembolso, FAQ).", 3)

# --- Técnica ---
add("Técnica", "media", "lang=\"fr-FR\" en lugar de fr-CH", ["(todo el sitio)"], f"<html lang=\"{pag['/']['lang']}\"> en todas las URLs FR.",
    "Ajustes → General → Idioma del sitio: «Français (Suisse)», o filtro `language_attributes`. Comprobar el hreflang (fr-CH / de-CH).", 0.25, previo="la auditoría previa lo daba por corregido: sigue en fr-FR")
add("Técnica", "alta", "Falta schema de negocio sanitario en la home y en las páginas de servicio", ["/", "(servicios y patologías)"],
    "Solo /physio-a-neuchatel/ y /physio-a-sugiez/ declaran `Physiotherapy`; la home solo tiene Organization/WebSite (Yoast).",
    "Añadir `Physiotherapy` (MedicalBusiness) con dirección, teléfono, horario, `areaServed` y `sameAs` en todo el sitio; `MedicalWebPage` + `MedicalCondition` + `FAQPage` en patologías (ver schema.json del módulo 5).", 1.5, previo="pendiente (ya detectado)")
add("Técnica", "media", "Recursos que bloquean el renderizado y errores de microdatos", ["(todas las plantillas)"],
    f"on_page: {pm.get('checks', {}).get('has_render_blocking_resources')} páginas con recursos render-blocking y {pm.get('checks', {}).get('has_micromarkup_errors')} con errores de micromarcado. Core Web Vitals reales: no disponible (sin PageSpeed/CrUX en esta ejecución).",
    "Plugin de caché con CSS crítico y diferido de JS (p. ej. WP Rocket / LiteSpeed); validar el schema en validator.schema.org; medir CWV con PageSpeed Insights por plantilla.", 2)

# --- Local ---
f = L["fichas"]["Physio Activa Ins"]
add("Local", "alta", "Dirección: el encargo dice «Rämismatte 31», pero el sitio y la ficha de Google dicen «Rämismatte 21»", ["/", "/contact/", "/nous-trouver/", "Google Business Profile"],
    f"Ficha de Google: «{f['address']}»; el sitio repite «Rämismatte 21» 90 veces. El contexto del cliente indica 31.",
    "Confirmar la dirección correcta con el cliente y unificarla (NAP) en el sitio, la ficha, OneDoc, local.ch y search.ch.", 0.5, fuente=f"DataForSEO business_data/my_business_info {dfs.HOY} + rastreo")
add("Local", "media", "La ficha de Google enlaza a http://www.physioactiva.ch/", ["Google Business Profile"],
    f"URL de la ficha: {f['url']} (sin https y con www; el sitio canónico es https://physioactiva.ch/).",
    "Cambiar la web de la ficha a https://physioactiva.ch/ con UTM (utm_source=google&utm_medium=organic&utm_campaign=gbp) para medirla en GA4.", 0.25, fuente=f"DataForSEO business_data {dfs.HOY}")
R = L["reviews"]
comp = {k: v for k, v in R.items() if k != "Physio Activa Ins"}
add("Local", "media", "Pocas reseñas frente a los competidores", ["Google Business Profile"],
    "Physio Activa: %s reseñas (nota %s; %s de %s respondidas). " % (R["Physio Activa Ins"]["reviews_count"], R["Physio Activa Ins"]["rating"]["value"],
     sum(i["respondida"] for i in R["Physio Activa Ins"]["items"]), len(R["Physio Activa Ins"]["items"])) +
    "; ".join(f"{k.split(' ')[0]} {k.split(' ')[1] if len(k.split(' '))>1 else ''}: {v['reviews_count']} (nota {v['rating']['value']})" for k, v in comp.items()),
    "Pedir reseña tras la última sesión (QR en el cabinet y enlace por WhatsApp), sin incentivos y sin filtrar; seguir respondiendo todas. Objetivo de ritmo: [POR CONFIRMAR] reseñas/mes.", 1, fuente=f"DataForSEO business_data/google/reviews {dfs.HOY}")
add("Local", "media", "Categorías de la ficha", ["Google Business Profile"],
    f"Principal: «{f['category']}»; adicionales: {f.get('additional_categories')}. PhysiOptima usa 4 categorías.",
    "Mantener «Physiothérapeute» como principal; valorar añadir servicios a domicilio en «Servicios» y el área de servicio (Seeland / Trois-Lacs). No añadir categorías que no correspondan.", 0.25, fuente=f"DataForSEO business_data {dfs.HOY}")
maps = L["maps"]
pos_ins = next((i["pos"] for i in maps["Ins"]["physio"] if "physio activa" in (i["title"] or "").lower()), None)
fuera = [c for c, v in maps.items() if not any("physio activa" in (i["title"] or "").lower() for i in v.get("physio", []))]
add("Local", "alta", "En Google Maps solo aparece cerca de Ins", list(maps),
    f"«physio» en Maps desde el centro de Ins: posición {pos_ins}. No aparece en el top 20 de Maps en: {', '.join(fuera)}.",
    "Es normal (Maps depende de la distancia): el área a domicilio se gana con páginas de zona útiles, la ficha (área de servicio) y reseñas que mencionen la localidad, no con una dirección por ciudad.", 0, fuente=f"DataForSEO serp/google/maps {dfs.HOY}")
lp = [k for k, v in S.items() if any("Physio Activa" in (l.get("title") or "") for l in v.get("local_pack", []))]
add("Local", "info", f"Fortaleza: Physio Activa sale en el local pack de {len(lp)} búsquedas desde Ins", lp[:15],
    "Incluye physio, physiothérapeute, physiothérapie, physio ins, physio près de moi, physio à domicile, kiné…",
    "Proteger la ficha (reseñas, publicaciones, fotos) y alinear la home con esas búsquedas.", 0, fuente=f"DataForSEO SERP Ins {dfs.HOY}")
add("Local", "media", "Directorios (NAP)", ["local.ch", "search.ch", "OneDoc", "Apple Maps", "Bing Places"],
    "local.ch y search.ch aparecen en el top 10 de 18 y 39 SERP analizadas; onedoc.ch, en 84. La consistencia NAP en cada directorio no se puede verificar desde aquí: no disponible.",
    "Revisar a mano la ficha en local.ch, search.ch, OneDoc, Apple Business Connect y Bing Places con la misma dirección, teléfono y web.", 1)

# --- Autoridad ---
def blv(d, k):
    v = D["bl_summary"].get(d)
    return v[0].get(k) if isinstance(v, list) and v else None
loc = ["physiodulac-physioduparc.ch", "physioptima.ch", "physiotherapie-kerzers.ch", "physiomurten.ch", "physioplus-avenches.com"]
add("Autoridad", "media", "Autoridad de enlaces por debajo de los competidores locales", ["physioactiva.ch"],
    f"Rank DataForSEO: physioactiva.ch {blv('physioactiva.ch','rank')} frente a una mediana de {statistics.median([blv(d,'rank') for d in loc])} de los competidores locales; {blv('physioactiva.ch','referring_domains')} dominios de referencia; spam score {blv('physioactiva.ch','backlinks_spam_score')}.",
    "Plan de enlaces locales (ver huecos de enlaces en el informe): directorios suizos, asociaciones, clubes deportivos y gimnasios de la zona (InsGym).", 4, fuente=f"DataForSEO backlinks/summary {dfs.HOY}")

an = D["bl_anchors"]["physioactiva.ch"][0]["items"]
spam = [a for a in an if re.search(r"backlink|pbn|casino|poker|buy|cheap|pinterest", a["anchor"] or "", re.I)]
rd = D["bl_refdomains"]["physioactiva.ch"][0]["items"]
toxic = [r["domain"] for r in rd if (r.get("backlinks_spam_score") or 0) >= 50]
add("Autoridad", "media", "Enlaces spam apuntando a physioactiva.ch", toxic[:15],
    f"{len(toxic)} de {len(rd)} dominios de referencia con spam score ≥ 50; anchors como «{spam[0]['anchor'][:70]}…» ({spam[0]['backlinks']} enlaces)." if spam else f"{len(toxic)} dominios con spam score ≥ 50.",
    "No comprar enlaces. Google suele ignorar este tipo de enlaces: vigilarlos en Search Console y usar el archivo disavow solo si aparece una acción manual o una caída clara. Pedir a la agencia que confirme que no proceden de ninguna campaña contratada.", 0.5,
    fuente=f"DataForSEO backlinks/anchors + referring_domains {dfs.HOY}")
GAP = json.loads((BASE / "data/m2_bl_gap.json").read_text())
utiles = [k for k, v in GAP.items() if (v.get("spam") or 0) < 30]
add("Autoridad", "media", "Huecos de enlaces: directorios que enlazan a ≥ 2 competidores y no a physioactiva.ch", utiles,
    "; ".join(f"{k} ({len(GAP[k]['competidores'])} competidores)" for k in utiles),
    "Darse de alta en physio-verzeichnis.ch, regionalinfo-schweiz.ch, better-search.ch y oeffnungszeitenbuch.de; además, por criterio local: physioswiss (miembro), InsGym, clubes deportivos de Ins/Seeland, comuna de Ins (listado de salud) y prensa local (Bieler Tagblatt, Murtenbieter, La Liberté).", 2,
    fuente=f"DataForSEO backlinks/domain_intersection {dfs.HOY}")
GEO = [k for k, v in S.items() if v.get("ai_overview")]
add("GEO", "media", f"AI Overview en {len(GEO)} de {len(S)} SERP analizadas (sobre todo patologías)", GEO[:12],
    "Las búsquedas de patología muestran AI Overview y citan portales; las búsquedas locales («physio + ciudad») no.",
    "En cada página de patología: respuesta directa en las 2-3 primeras líneas, preguntas como H2/H3, FAQ marcada y autor con nombre (fisioterapeuta) y titulación.", 0, fuente=f"DataForSEO SERP Ins {dfs.HOY}")

orden = {"alta": 0, "media": 1, "baja": 2, "info": 3}
H.sort(key=lambda h: (orden[h["severidad"]], h["bloque"], h["id"]))
(BASE / "data/hallazgos.json").write_text(json.dumps(H, ensure_ascii=False, indent=1))
print(len(H), collections.Counter(h["severidad"] for h in H))
