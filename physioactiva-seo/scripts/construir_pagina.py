"""Construye los JSON de Elementor (y la previsualización) a partir de fr.md + componentes de las plantillas.

Uso: python3 scripts/construir_pagina.py [--css-global] [slug ...]
- Paso 1: fr.md → receta estructurada (entregables/6_elementor/<slug>/receta.json): lista ordenada de componentes y campos.
- Paso 2: receta → HTML con las clases de la plantilla (sin clases ni colores nuevos), dentro de <div class="pa-home">,
  + <style>/<script> de la plantilla sin cambios (o nada con --css-global) + JSON-LD.
- Paso 3: JSON con la estructura raíz de la plantilla e IDs nuevos (7 hex, únicos en el lote).
"""
import json, re, sys, pathlib, hashlib, html as H, copy, yaml, markdown
from bs4 import BeautifulSoup, NavigableString, Tag

BASE = pathlib.Path(__file__).resolve().parent.parent
PL = BASE / "plantillas"
OUT = BASE / "entregables/6_elementor"
PAG = BASE / "entregables/5_paginas"
CLI = yaml.safe_load((BASE / "config/cliente.yml").read_text())
ZON = yaml.safe_load((BASE / "config/zonas.yml").read_text())
CSS_GLOBAL = "--css-global" in sys.argv
SITE = "https://physioactiva.ch"
IMG = "https://physioactiva.ch/wp-content/uploads/"
FOTOS = {"jambe": IMG + "2025/04/Physio-Activa-00031.jpg", "senior": IMG + "2025/04/Physio-Activa-00032.jpg",
         "salle": IMG + "2025/04/Physio-Activa-00036.jpg", "fitness": IMG + "2025/06/Centerbild_IMG_9184-scaled-1.jpg",
         "insgym": IMG + "2025/06/fxbtrjhiol.jpg"}
VIDEO = IMG + "2026/06/Physioactiva.mp4"
GBP = "https://www.google.com/maps?cid=17004812906479027083"
REDIRIGIDAS = {"/reserver-maintenant/", "/rendez-vous-des-maintenant/", "/reserve/", "/rendez-vous-online/", "/online-termin-buchen/",
               "/fitness-medical/", "/mal-de-dos", "/fitness-medica/", "/drainage-lymphatique", "/physiotherapie-a-domicile",
               "/douleurs-cervicales", "/douleurs-genou", "/lesions-cheville", "/lesions-epaule", "/mtt-fitness-medical"}


def tpl(nombre):
    d = json.loads((PL / f"{nombre}.json").read_text())
    h = d["content"][0]["elements"][0]["elements"][0]["settings"]["html"]
    return d, re.search(r"<style>.*?</style>", h, re.S).group(0), re.search(r"<script>.*?</script>", h, re.S).group(0)


T_HOME, STYLE_HOME, _SCRIPT_HOME = tpl("home-design-elementor")
T_LOMB, STYLE_LOMB, SCRIPT_LOMB = tpl("lombaire-elementor")
# Home: el script original genera servicios/FAQ por JS y traduce con data-i18n. Con el contenido estático, solo hacen falta
# la animación de aparición (reveal) y el acordeón de la FAQ: son exactamente las dos funciones del script de lombaire.
SCRIPT_HOME = SCRIPT_LOMB

# ---------------------------------------------------------------- páginas del lote
PAGINAS = [  # slug, url, plantilla, lote, carpeta fr.md, foto hero, alt hero
    ("accueil", "/", "home", "A", "accueil", "salle", "Salle de traitement du cabinet de physiothérapie Physio Activa à Ins"),
    ("a-propos-de-nous", "/a-propos-de-nous/", "lombaire", "A", "a-propos-de-nous", "senior", "Physiothérapeute accompagnant un patient lors d'exercices avec bande élastique"),
] + [(f"physio-a-{k}", z["url"], "lombaire", z["lote"], f"physio-a-{k}", None, None) for k, z in ZON.items()] + [
    ("pour-les-patients", "/pour-les-patients/", "lombaire", "C", "pour-les-patients", "salle", "Cabinet de physiothérapie à Ins : table de traitement et matériel de rééducation"),
    ("mal-de-dos-lombaire", "/mal-de-dos-lombaire/", "lombaire", "C", "mal-de-dos-lombaire", "senior", "Exercice de renforcement accompagné par un physiothérapeute pour le mal de dos"),
    ("douleur-cervicale-au-cou", "/douleur-cervicale-au-cou/", "lombaire", "C", "douleur-cervicale-au-cou", "salle", "Salle de traitement pour la physiothérapie des douleurs cervicales à Ins"),
    ("lesions-de-lepaule", "/lesions-de-lepaule/", "lombaire", "C", "lesions-de-lepaule", "senior", "Rééducation de l'épaule avec bande élastique guidée par un physiothérapeute"),
    ("douleur-du-genou-lesions-de-la-cheville", "/douleur-du-genou-lesions-de-la-cheville/", "lombaire", "C", "douleur-du-genou-lesions-de-la-cheville", "jambe", "Physiothérapeute mobilisant le genou d'un patient allongé"),
    ("sciatique-hernie-discale", "/sciatique-hernie-discale/", "lombaire", "C", "sciatique-hernie-discale", "jambe", "Mobilisation de la jambe d'un patient souffrant de sciatique par un physiothérapeute"),
    ("douleur-pied-cheville-fasciite-plantaire", "/douleur-pied-cheville-fasciite-plantaire/", "lombaire", "C", "douleur-pied-cheville-fasciite-plantaire", "fitness", "Espace d'entraînement pour la rééducation du pied et de la cheville"),
    ("douleur-de-hanche-protheses", "/douleur-de-hanche-protheses/", "lombaire", "C", "douleur-de-hanche-protheses", "jambe", "Physiothérapeute mobilisant la hanche et la jambe d'un patient"),
    ("reservation-en-ligne", "/reservation-en-ligne/", "lombaire", "C", "reservation-en-ligne", "salle", "Cabinet Physio Activa à Ins prêt à accueillir les patients"),
]
FOTO_ZONA = ["insgym", "senior", "salle", "fitness", "jambe"]  # rotación: no repetir la misma foto en zonas consecutivas
ALT_ZONA = {"insgym": "Espace d'entraînement de l'InsGym, où se trouve le cabinet Physio Activa à Ins",
            "senior": "Physiothérapeute accompagnant un patient lors d'exercices à domicile ou au cabinet",
            "salle": "Salle de traitement du cabinet Physio Activa à Ins",
            "fitness": "Salle de fitness médical utilisée pour la rééducation à Ins",
            "jambe": "Physiothérapeute mobilisant la jambe d'un patient au cabinet d'Ins"}

ICONOS = [(r"urgence|alarme|médecin|144", "fa-triangle-exclamation"), (r"domicile|maison|chez vous", "fa-house-medical"),
          (r"cabinet|ins|venir|accès|trajet|km", "fa-location-dot"), (r"rembours|lamal|assurance|ordonnance|prescription", "fa-file-medical"),
          (r"exercice|renforc|mtt|fitness|entraîn", "fa-dumbbell"), (r"manuel|mobilis|massage|main", "fa-hand-holding-heart"),
          (r"sport|course|coureur", "fa-person-running"), (r"bilan|évaluation|examen|diagnostic|entretien", "fa-clipboard-list"),
          (r"opér|prothèse|chirurg|hôpital|hospital", "fa-hospital"), (r"langue|français|allemand|bilingue", "fa-language"),
          (r"douleur|aigu|lumbago|crise", "fa-bolt"), (r"nerf|sciatique|hernie|disque|vertèbre|dos|colonne", "fa-bone"),
          (r"équipe|physiothérapeute|thérapeute", "fa-user-doctor"), (r"rendez-vous|réserv|séance", "fa-calendar-check")]
CICLO = ["fa-circle-check", "fa-stethoscope", "fa-heart-pulse", "fa-person-walking", "fa-shield-heart", "fa-notes-medical"]
EYEBROW = [(r"urgence|médecin", "Signaux d'alarme"), (r"rembours", "Remboursement"), (r"domicile", "À domicile"),
           (r"venir|cabinet d'ins|accès", "Accès"), (r"déroulement|séance|se passe", "Vos séances"), (r"traitons|pathologies|traitées", "Ce que nous traitons"),
           (r"physiothérapie peut|traitement|prise en charge|aider|approche", "Notre approche"), (r"symptôme", "Symptômes"),
           (r"qu'est-ce|comprendre|définition|c'est quoi", "Comprendre"), (r"équipe", "Notre équipe"), (r"cause", "Causes"),
           (r"exercice|prévenir|prévention|conseils", "Conseils"), (r"réserver|rendez-vous|prendre", "Rendez-vous"), (r"assurance", "Assurances")]


def eid(*parts):
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:7]


def esc(s):
    return H.escape(s, quote=True)


def limpiar_md(md):
    md = re.split(r"^## Notes pour l'équipe \(ES\)", md, flags=re.M)[0]
    md = re.sub(r"`?\[([^\]\[]*?)\s*POR CONFIRMAR\s*:?\s*([^\]\[]*)\]`?",
                lambda m: "[À CONFIRMER" + (" : " + " ".join(x for x in (m.group(1).strip(), m.group(2).strip()) if x) if (m.group(1).strip() or m.group(2).strip()) else "") + "]", md)
    md = md.replace("`[À CONFIRMER", "[À CONFIRMER").replace("]`", "]")
    return md


def inline(tag):
    """HTML interior permitido de un bloque: a, strong, em; enlaces con URL final."""
    s = "".join(str(c) for c in tag.contents).strip()
    s = re.sub(r"</?code>", "", s)
    s = re.sub(r"<a href=\"([^\"]+)\">", lambda m: f'<a href="{fix_href(m.group(1))}" style="color:var(--azure);font-weight:600">', s)
    return s


def fix_href(h):
    h = H.unescape(h)
    if h.startswith("https://physioactiva.ch"):
        h = h[len("https://physioactiva.ch"):] or "/"
    if h.startswith("/") and not h.endswith("/") and "#" not in h and "." not in h.split("/")[-1]:
        h += "/"
    return esc(h)


def texto(tag):
    return " ".join(tag.get_text(" ", strip=True).split())


def parse_md(md):
    meta = yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", md, re.S).group(1))
    body = limpiar_md(md[re.match(r"^---\n.*?\n---\n", md, re.S).end():])
    soup = BeautifulSoup(markdown.markdown(body, extensions=["extra", "sane_lists"]), "html.parser")
    h1, intro, secciones, cur = None, [], [], None
    for el in soup.children:
        if not isinstance(el, Tag):
            continue
        if el.name == "h1":
            h1 = el; continue
        if el.name == "h2":
            cur = {"h2": el, "bloques": []}; secciones.append(cur); continue
        (cur["bloques"] if cur else intro).append(el)
    return meta, h1, intro, secciones


def estructura(bloques):
    """Divide los bloques de una sección en: intro (p antes del primer h3/lista), sub-secciones h3 y listas sueltas."""
    intro, subs, listas, cur = [], [], [], None
    for b in bloques:
        if b.name == "h3":
            cur = {"h3": b, "contenido": []}; subs.append(cur); continue
        if cur:
            cur["contenido"].append(b)
        elif b.name in ("ul", "ol"):
            listas.append(b)
        elif not listas:
            intro.append(b)
    return intro, subs, listas


def despues(bloques, intro_b):
    """Párrafos que van después de la primera lista (fuera de h3)."""
    out, vista = [], False
    for b in bloques:
        if b.name == "h3":
            break
        if b.name in ("ul", "ol"):
            vista = True; continue
        if vista and b.name == "p":
            out.append(inline(b))
    return out


def icono(texto_, i):
    t = texto_.lower()
    for rx, ic in ICONOS:
        if re.search(rx, t):
            return ic
    return CICLO[i % len(CICLO)]


def eyebrow(h2):
    t = h2.lower()
    for rx, e in EYEBROW:
        if re.search(rx, t):
            return e
    return "Physio Activa"


def item_card(li):
    """«**Titre** : texte» → (h3, p); si no, (None, p)."""
    strong = li.find("strong")
    raw = inline(li)
    if strong and raw.startswith("<strong>"):
        t = texto(strong).rstrip(" :")
        rest = re.sub(r"^<strong>.*?</strong>\s*[:–-]?\s*", "", raw)
        return t, rest
    return None, raw


def p_bloques(bloques):
    out = []
    for b in bloques:
        if b.name in ("ul", "ol"):
            out += [f"<p>– {inline(li)}</p>" for li in b.find_all("li", recursive=False)]
        elif b.name in ("p", "blockquote"):
            out.append(f"<p>{inline(b)}</p>")
    return espaciar("".join(out))


def espaciar(h):
    """Separación vertical entre párrafos consecutivos (el reset de la plantilla pone margin:0)."""
    partes = re.split(r"(?=<p>)", h)
    return "".join(x if i == 0 else x.replace("<p>", '<p style="margin-top:12px">', 1) for i, x in enumerate([y for y in partes if y]))


# ---------------------------------------------------------------- componentes (marcado de las plantillas)
def c_hero(r):
    pills = "".join(f'<span><i class="fa-solid fa-circle-check"></i> {esc(p)}</span>' for p in r["pills"])
    h1 = r["h1"]
    if " : " in h1:
        a, b = h1.split(" : ", 1)
        h1h = f"{esc(a)} : <span>{esc(b)}</span>"
    else:
        h1h = esc(h1)
    if r.get("video"):
        return f"""<section class="hero" style="padding:0">
  <video class="hero-video" autoplay muted loop playsinline preload="metadata" poster="{r['img']}" aria-label="{esc(r['alt'])}">
    <source src="{VIDEO}" type="video/mp4">
    {esc(r['alt'])}
  </video>
  <div class="wrap">
    <div class="reveal hero-content">
      <span class="eyebrow">{esc(r['eyebrow'])}</span>
      <h1>{h1h}</h1>
      <p class="sub">{r['sub']}</p>
      <div class="hero-cta">
        <a class="btn" href="{CLI['reservation']}"><i class="fa-solid fa-calendar-check"></i> <span>Réserver en ligne</span></a>
        <a class="btn ghost" href="{CLI['whatsapp_href']}"><i class="fa-brands fa-whatsapp"></i> <span>WhatsApp</span></a>
      </div>
      <div class="hero-pills">{pills}</div>
      <a class="hero-rating" href="{GBP}" target="_blank" rel="noopener"><span class="num">{CLI['avis_google']['note']}</span><span class="stars">★★★★★</span><span>{CLI['avis_google']['nombre']} avis Google</span></a>
    </div>
  </div>
</section>"""
    return f"""<section class="hero" style="padding:0">
  <div class="wrap">
    <div class="reveal">
      <span class="eyebrow">{esc(r['eyebrow'])}</span>
      <h1>{h1h}</h1>
      <p class="sub">{r['sub']}</p>
      <div class="hero-cta">
        <a class="btn" href="{r.get('cta_href', CLI['reservation'])}"><i class="fa-solid fa-calendar-check"></i> <span>{esc(r.get('cta', 'Prendre rendez-vous'))}</span></a>
        <a class="btn ghost" href="{CLI['whatsapp_href']}"><i class="fa-brands fa-whatsapp"></i> <span>WhatsApp</span></a>
      </div>
      <div class="hero-pills">{pills}</div>
    </div>
    <div class="hero-img reveal"><img src="{r['img']}" alt="{esc(r['alt'])}" width="1200" height="800" fetchpriority="high"></div>
  </div>
</section>"""


def cab(r, extra=""):
    lead = "".join(f'<p class="lead" style="margin-top:14px">{p}</p>' for p in r.get("lead", []))
    return f'<div class="wrap center"><span class="eyebrow center">{esc(r["eyebrow"])}</span><h2 class="title">{r["h2"]}</h2>{lead}{extra}</div>'


def c_grid(r):
    cards = ""
    for c in r["cards"]:
        h3 = f"<h3>{c['h3']}</h3>" if c.get("h3") else ""
        cards += f'<div class="wcard reveal"><div class="wic"><i class="fa-solid {c["icon"]}"></i></div>{h3}{c["html"]}</div>'
    bg = f' class="{r["bg"]}"' if r.get("bg") else ""
    return f'<section{bg}>\n  {cab(r)}\n  <div class="wrap"><div class="why-grid">{cards}</div></div>\n</section>'


def c_texte(r):
    bg = f' class="{r["bg"]}"' if r.get("bg") else ""
    return f'<section{bg}>\n  {cab(r)}\n  <div class="wrap"><div class="wcard reveal" style="max-width:820px;margin:40px auto 0">{r["html"]}</div></div>\n</section>'


def c_steps(r):
    steps = "".join(f'<li><span class="num">{i}</span><p>{s}</p></li>' for i, s in enumerate(r["steps"], 1))
    btn = f'<a class="btn outline" href="{CLI["reservation"]}"><i class="fa-solid fa-calendar-check"></i> {esc(r["btn"])}</a>' if r.get("btn") else ""
    after = "".join(f'<p class="lead" style="margin-top:14px">{p}</p>' for p in r.get("after", []))
    cls = r.get("bg") or "assur-sec"
    return f'<section class="{cls}">\n  {cab(r, f"<ol class=\"steps\">{steps}</ol>{after}{btn}")}\n</section>'


def c_serv(r):
    cards = ""
    for c in r["cards"]:
        sic = f'<img src="{c["icon_img"]}" alt="" width="40" height="40" loading="lazy">' if c.get("icon_img") else f'<i class="fa-solid {c["icon"]} fa-2x"></i>'
        cards += (f'<div class="scard reveal"><div class="sic">{sic}</div><h3>{esc(c["h3"])}</h3><p>{c["p"]}</p>'
                  f'<a class="more" href="{c["href"]}"><span>{esc(c.get("more", "En savoir plus"))}</span> <i class="fa-solid fa-arrow-right"></i></a></div>')
    bg = f' class="{r["bg"]}"' if r.get("bg") else ""
    return f'<section{bg}>\n  {cab(r)}\n  <div class="wrap"><div class="serv-grid">{cards}</div></div>\n</section>'


def c_team(r):
    ms = ""
    for m in r["membres"]:
        langs = "".join(f"<span>{l}</span>" for l in CLI["langues_codes"])
        ms += (f'<div class="member reveal"><div class="ph"><img src="{m["photo"]}" alt="{esc(m["nom"])}, physiothérapeute chez Physio Activa à Ins" loading="lazy" width="1024" height="1024"></div>'
               f'<div class="body"><h3 class="name">{esc(m["nom"])}</h3><div class="role">{esc(m["titre"])}</div><div class="langs">{langs}</div>'
               f'{m["html"]}<a class="btn outline" href="{CLI["reservation"]}">Prendre rendez-vous</a></div></div>')
    bg = f' class="{r["bg"]}"' if r.get("bg") else ""
    return f'<section{bg}>\n  {cab(r)}\n  <div class="wrap"><div class="team-grid">{ms}</div></div>\n</section>'


def c_gallery(r):
    a = "".join(f'<a{" class=\"big\"" if i == 0 else ""} href="{src}"><img src="{src}" alt="{esc(alt)}" loading="lazy"></a>' for i, (src, alt) in enumerate(r["imgs"]))
    return f'<section class="gallery">\n  {cab(r)}\n  <div class="wrap"><div class="gal-grid reveal">{a}</div></div>\n</section>'


def c_faq(r):
    items = ""
    for i, f in enumerate(r["faq"]):
        items += (f'<div class="faq{" open" if i == 0 else ""}"><button><span class="faq-q">{esc(f["q"])}</span><span class="q-ic"><i class="fa-solid fa-plus"></i></span></button>'
                  f'<div class="ans"><p>{f["a_html"]}</p></div></div>')
    return f'<section>\n  <div class="wrap center"><span class="eyebrow center">FAQ</span><h2 class="title">{esc(r["h2"])}</h2></div>\n  <div class="wrap"><div class="faq-list">{items}</div></div>\n</section>'


def c_cta(r):
    s2 = f'<p class="s2">{r["s2"]}</p>' if r.get("s2") else ""
    return f"""<section class="cta-band">
  <div class="wrap reveal">
    <h2>{esc(r['h2'])}</h2>
    <p class="s1">{r['s1']}</p>{s2}
    <div class="cta-actions">
      <a class="btn primary" href="{CLI['reservation']}"><i class="fa-solid fa-calendar-check"></i> <span>Prendre rendez-vous en ligne</span></a>
      <a class="btn ghost" href="{CLI['whatsapp_href']}"><i class="fa-brands fa-whatsapp"></i> <span>Contacter par WhatsApp</span></a>
      <a class="btn ghost" href="{CLI['tel_href']}"><i class="fa-solid fa-phone"></i> <span>{esc(CLI['telephone'])}</span></a>
    </div>
  </div>
</section>"""


def c_map(r):
    return f"""<section class="map" id="map">
  <a class="map-facade" href="{CLI['maps_url']}" target="_blank" rel="noopener" aria-label="{esc(CLI['map_title'])} — ouvrir dans Google Maps">
    <span class="map-facade-inner"><i class="fa-solid fa-location-dot"></i><strong>{esc(CLI['map_title'])}</strong><span>Ouvrir dans Google Maps</span></span>
  </a>
</section>"""


RENDER = {"hero": c_hero, "grid": c_grid, "texte": c_texte, "steps": c_steps, "serv": c_serv, "team": c_team,
          "gallery": c_gallery, "faq": c_faq, "cta": c_cta, "map": c_map}

# ---------------------------------------------------------------- fr.md → receta
DESC_PATO = {
    "/mal-de-dos-lombaire/": "Lumbago, douleur lombaire aiguë ou qui dure : bilan, thérapie manuelle et exercices.",
    "/sciatique-hernie-discale/": "Douleur qui descend dans la jambe : évaluation, soulagement et reprise du mouvement.",
    "/douleur-cervicale-au-cou/": "Nuque raide, torticolis, coup du lapin ou céphalée de tension.",
    "/lesions-de-lepaule/": "Coiffe des rotateurs, tendinite, capsulite rétractile ou rééducation après une opération.",
    "/douleur-du-genou-lesions-de-la-cheville/": "Ménisque, ligament croisé, arthrose ou rééducation après une prothèse du genou.",
    "/douleur-pied-cheville-fasciite-plantaire/": "Fasciite plantaire, entorse de la cheville, tendinite d'Achille ou périostite.",
    "/douleur-de-hanche-protheses/": "Arthrose de la hanche et rééducation après une prothèse de hanche.",
}
SERVICIOS_HOME = [  # iconos de servicio de la plantilla home (2025/05/N.png) → páginas de servicio existentes (200)
    (1, "Physiothérapie générale", "Douleurs, raideurs et rééducation de l'appareil locomoteur, sur prescription médicale.", "/physio-generale/"),
    (2, "Physiothérapie à domicile", "Les séances se déroulent chez vous lorsque vous ne pouvez pas vous déplacer.", "/physiotherapeute-a-domicile/"),
    (3, "Fitness médical (MTT)", "Entraînement thérapeutique encadré pour renforcer et reprendre confiance dans le mouvement.", "/medical-training-therapy-mtt/"),
    (4, "Drainage lymphatique", "Technique manuelle douce indiquée notamment en cas d'œdème, sur prescription.", "/drainage-lymphatique/"),
    (7, "Thérapie manuelle", "Techniques manuelles pour mobiliser les articulations et les tissus, associées à des exercices.", "/therapie-manuelle/"),
    (8, "Plancher pelvien et uro-gynécologie", "Rééducation du périnée, notamment en cas d'incontinence ou après une grossesse.", "/physiotherapie-du-plancher-pelvien/"),
    (9, "ATM et mâchoire", "Physiothérapie des troubles de l'articulation temporo-mandibulaire.", "/physiotemporo-mandibulaire-atm/"),
    (5, "Physiothérapie neurologique", "Rééducation après un AVC ou en cas de maladie neurologique, sur prescription.", "/physiotherapie-neurologique/"),
    (6, "Physiothérapie cardio-respiratoire", "Rééducation respiratoire et reprise de l'effort, sur prescription médicale.", "/physiotherapie-cardiorespiratoire/"),
]


def partir_sub(intro_html, maxc):
    txt = re.sub(r"<[^>]+>", "", intro_html)
    if len(txt) <= maxc:
        return intro_html, []
    frases = re.split(r"(?<=[.!?])\s+", intro_html)
    sub, resto = "", []
    for f in frases:
        if not resto and len(re.sub(r"<[^>]+>", "", sub + " " + f)) <= maxc:
            sub = (sub + " " + f).strip()
        else:
            resto.append(f)
    return sub, [" ".join(resto)] if resto else []


def receta(slug, url, plantilla, lote, carpeta, foto, alt, idx_zona=0):
    md = (PAG / carpeta / "fr.md").read_text()
    meta, h1, intro, secciones = parse_md(md)
    tipo = meta.get("tipo")
    zona = ZON.get(meta.get("zona", "")) if tipo == "zona" else None
    if tipo == "zona":
        foto = FOTO_ZONA[idx_zona % len(FOTO_ZONA)]
        alt = ALT_ZONA[foto]
    intro_p = [b for b in intro if b.name == "p" and not re.search(r"Téléphone\s*:|^\s*<a", inline(b)) and "reservation-en-ligne" not in inline(b)[:60]]
    intro_html = " ".join(inline(b) for b in intro_p)
    lim = 520 if plantilla == "lombaire" else 430   # plantilla: sub de lombaire ≈ 433 car. y de la home ≈ 300 (+20 % / +40 % home)
    sub, resto = partir_sub(intro_html, lim)
    if tipo == "zona":
        pills = [f"Cabinet à Ins, à {str(zona['km_depuis_ins']).replace('.', ',')} km", "Sur prescription médicale", "LAMal · LAA · AI · AM"]
        eyebrow_h = f"Physio · {zona['nom_titre']}"
    elif tipo == "home":
        pills = ["Au cabinet d'Ins ou à domicile", "Sur prescription médicale", "Remboursé LAMal / LAA"]
        eyebrow_h = "Physiothérapie à Ins (Anet)"
    elif tipo == "reserva":
        pills = ["En ligne, par téléphone ou WhatsApp", "Au cabinet d'Ins ou à domicile", "Sur prescription médicale"]
        eyebrow_h = "Rendez-vous"
    elif tipo == "hub":
        pills = ["Sur prescription médicale", "Au cabinet d'Ins ou à domicile", "Remboursé LAMal / LAA"]
        eyebrow_h = "Pathologies traitées"
    elif tipo == "apropos":
        pills = ["Physiothérapeutes à Ins", "Français et espagnol", "Au cabinet ou à domicile"]
        eyebrow_h = "Notre équipe"
    else:
        pills = ["Sur prescription médicale", "Au cabinet d'Ins ou à domicile", "Remboursé LAMal / LAA"]
        eyebrow_h = "Physiothérapie à Ins · cabinet et domicile"
    R = [{"tipo": "hero", "eyebrow": eyebrow_h, "h1": texto(h1), "sub": sub, "pills": pills, "img": FOTOS[foto], "alt": alt,
          "video": tipo == "home", "cta": "Réserver sur OneDoc" if tipo == "reserva" else "Prendre rendez-vous",
          **({"cta_href": CLI["onedoc_url"]} if tipo == "reserva" else {})}]
    pend_lead = resto
    faq, cta = None, None
    secs = [s for s in secciones]
    for s in secs:
        if re.match(r"questions fréquentes", texto(s["h2"]), re.I):
            faq = s
    cta = secs[-1] if secs and secs[-1] is not faq else None
    bg_toggle = False
    for s in secs:
        if s is faq or s is cta:
            continue
        h2t = texto(s["h2"])
        h2h = inline(s["h2"])
        intro_b, subs, listas = estructura(s["bloques"])
        overflow = pend_lead
        lead = pend_lead + [inline(b) for b in intro_b if b.name == "p"]
        pend_lead = []
        bg = "trust" if bg_toggle else None
        bg_toggle = not bg_toggle
        base = {"eyebrow": eyebrow(h2t), "h2": h2h, "lead": lead, "bg": bg}
        if tipo == "home" and re.search(r"équipe", h2t, re.I):
            membres = []
            for m in CLI["equipe"]:
                membres.append({**m, "html": f"<p>Physiothérapeute chez Physio Activa, au cabinet d'Ins et à domicile.</p>"})
            R.append({"tipo": "team", **base, "membres": membres})
            continue
        if tipo == "apropos" and subs and all(any(m["nom"] in texto(x["h3"]) for m in CLI["equipe"]) for x in subs):
            membres = []
            for x in subs:
                m = next(m for m in CLI["equipe"] if m["nom"] in texto(x["h3"]))
                membres.append({**m, "html": p_bloques(x["contenido"])})
            R.append({"tipo": "team", **base, "membres": membres})
            continue
        if tipo == "home" and re.search(r"ce que nous traitons", h2t, re.I):
            cards = []
            for li in (listas[0].find_all("li") if listas else []):
                a = li.find("a")
                if a:
                    nom = texto(a)
                    cards.append({"h3": nom[0].upper() + nom[1:], "p": esc(DESC_PATO.get(fix_href(a["href"]), "Bilan, traitement et exercices adaptés, au cabinet d'Ins ou à domicile.")),
                                  "href": fix_href(a["href"]), "icon": icono(nom, len(cards))})
            after = despues(s["bloques"], intro_b)
            R.append({"tipo": "serv", **base, "cards": cards})
            R.append({"tipo": "serv", "eyebrow": "Nos soins", "h2": "Nos soins de physiothérapie", "lead": after,
                      "bg": "trust" if bg_toggle else None,
                      "cards": [{"h3": t, "p": esc(p), "href": u, "icon_img": f"{IMG}2025/05/{'2-1' if n == 2 else n}.png"} for n, t, p, u in SERVICIOS_HOME]})
            bg_toggle = not bg_toggle
            continue
        # hub: tarjetas con enlace
        if tipo == "hub" and subs and all(x["contenido"] and any(c.find("a") for c in x["contenido"] if isinstance(c, Tag)) for x in subs):
            cards = []
            for x in subs:
                a = next(c.find("a") for c in x["contenido"] if isinstance(c, Tag) and c.find("a"))
                cards.append({"h3": texto(x["h3"]), "p": re.sub(r"</?p[^>]*>", " ", p_bloques(x["contenido"])).strip(),
                              "href": fix_href(a["href"]), "icon": icono(texto(x["h3"]), len(cards)), "more": "Lire la page"})
            R.append({"tipo": "serv", **base, "cards": cards})
            continue
        if re.search(r"rembours", h2t, re.I) and plantilla == "lombaire" and listas:
            R.append({"tipo": "steps", **base, "bg": "assur-sec", "steps": [inline(li) for li in listas[0].find_all("li", recursive=False)],
                      "after": [inline(b) for b in s["bloques"] if b.name == "p" and b not in intro_b], "btn": "Vous avez une prescription ? Prenez rendez-vous"})
            continue
        if re.search(r"déroulement|se passe|étapes|comment réserver|réserver", h2t, re.I) and listas and not subs and plantilla == "lombaire":
            R.append({"tipo": "steps", **base, "bg": "assur-sec", "steps": [inline(li) for li in listas[0].find_all("li", recursive=False)],
                      "after": [inline(b) for b in s["bloques"] if b.name == "p" and b not in intro_b]})
            continue
        if subs:
            cards = []
            alerta = re.search(r"urgence|médecin|alarme", h2t, re.I)
            for l in listas:
                for li in l.find_all("li", recursive=False):
                    t, p_ = item_card(li)
                    cards.append({"h3": esc(t) if t else None, "html": f"<p>{p_}</p>",
                                  "icon": "fa-triangle-exclamation" if alerta else icono(texto(li), len(cards))})
            if despues(s["bloques"], intro_b):
                cards.append({"h3": None, "html": espaciar("".join(f"<p>{a}</p>" for a in despues(s["bloques"], intro_b))), "icon": "fa-circle-info"})
            cards += [{"h3": inline(x["h3"]), "html": p_bloques(x["contenido"]), "icon": icono(texto(x["h3"]), len(cards) + i)} for i, x in enumerate(subs)]
            # listas o párrafos sueltos tras las h3 ya van dentro de la última tarjeta
            R.append({"tipo": "grid", **base, "cards": cards})
            continue
        if listas and sum(len(l.find_all("li", recursive=False)) for l in listas) >= 2:
            alerta = re.search(r"urgence|médecin|alarme", h2t, re.I)
            cards = []
            for l in listas:
                for li in l.find_all("li", recursive=False):
                    t, p = item_card(li)
                    cards.append({"h3": esc(t) if t else None, "html": f"<p>{p}</p>",
                                  "icon": "fa-triangle-exclamation" if alerta else icono(texto(li), len(cards))})
            after = despues(s["bloques"], intro_b)
            R.append({"tipo": "grid", **base, "cards": cards})
            if after:
                R[-1]["cards"].append({"h3": None, "html": espaciar("".join(f"<p>{a}</p>" for a in after)), "icon": "fa-circle-info" if not alerta else "fa-phone"})
            continue
        html_ = p_bloques(s["bloques"][len(intro_b):]) if False else p_bloques(s["bloques"])
        R.append({"tipo": "texte", **{**base, "lead": overflow}, "html": html_ or espaciar("".join(f"<p>{l}</p>" for l in lead))})
    if faq:
        _, subs, _ = estructura(faq["bloques"])
        R.append({"tipo": "faq", "h2": texto(faq["h2"]),
                  "faq": [{"q": texto(x["h3"]), "a_html": " ".join(inline(c) if c.name == "p" else " ".join(inline(li) for li in c.find_all("li")) for c in x["contenido"] if isinstance(c, Tag)),
                           "a_text": " ".join(texto(c) for c in x["contenido"] if isinstance(c, Tag))} for x in subs]})
    if cta:
        ps = [b for b in cta["bloques"] if b.name == "p"]
        R.append({"tipo": "cta", "h2": texto(cta["h2"]), "s1": inline(ps[0]) if ps else "Contactez-nous pour une séance au cabinet à Ins ou à domicile.",
                  "s2": inline(ps[1]) if len(ps) > 1 else None})
    R.append({"tipo": "map"})
    if tipo == "home":  # galería del cabinet (mismas fotos que la plantilla, alt descriptivos) antes de la FAQ
        gal = {"tipo": "gallery", "eyebrow": "Le cabinet", "h2": "Un espace de soins et de mouvement à Ins",
               "lead": ["Des salles de traitement et un espace d'entraînement au sein de l'InsGym, Rämismatte 21."],
               "imgs": [(FOTOS["insgym"], "Espace d'entraînement de l'InsGym à Ins"), (FOTOS["salle"], "Salle de traitement du cabinet Physio Activa"),
                        (FOTOS["jambe"], "Physiothérapeute mobilisant la jambe d'un patient"), (FOTOS["fitness"], "Salle de fitness médical (MTT)"),
                        (FOTOS["senior"], "Exercice de rééducation avec bande élastique")]}
        i = next(i for i, x in enumerate(R) if x["tipo"] == "faq")
        R.insert(i, gal)
    return meta, R


# ---------------------------------------------------------------- JSON-LD
def jsonld(slug, url, meta, R, plantilla):
    sch_f = PAG / slug / "schema.json"
    negocio = {
        "@type": "Physiotherapy", "@id": SITE + "/#physiotherapy", "name": CLI["nom"], "url": SITE + "/", "telephone": CLI["telephone_e164"],
        "address": {"@type": "PostalAddress", "streetAddress": CLI["rue"], "postalCode": CLI["npa"], "addressLocality": CLI["localite"],
                    "addressRegion": CLI["canton"], "addressCountry": "CH"},
        "geo": {"@type": "GeoCoordinates", "latitude": CLI["geo"]["lat"], "longitude": CLI["geo"]["lng"]},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": CLI["horaires_schema"]["jours"],
                                        "opens": CLI["horaires_schema"]["ouvre"], "closes": CLI["horaires_schema"]["ferme"]}],
        "areaServed": [{"@type": "City", "name": n} for n in ["Ins", "Anet", "Sugiez", "Mont-Vully", "Murten / Morat", "Kerzers / Chiètres",
                                                             "Avenches", "La Neuveville", "Neuchâtel", "Biel/Bienne", "Lyss"]],
        "availableLanguage": ["fr", "es"], "sameAs": [GBP]}
    full = SITE + url
    tipo = meta.get("tipo")
    page = {"@type": "MedicalWebPage" if tipo == "patologia" else "AboutPage" if tipo == "apropos" else "WebPage",
            "@id": full + "#webpage", "url": full, "name": meta["title"], "description": meta["meta"], "inLanguage": "fr-CH",
            "about": {"@id": SITE + "/#physiotherapy"}}
    if tipo == "patologia":
        page["about"] = {"@type": "MedicalCondition", "name": meta.get("condicion") or meta["keyword_principal"]}
        page["provider"] = {"@id": SITE + "/#physiotherapy"}
    graph = [negocio, page]
    if tipo == "apropos":
        for m in CLI["equipe"]:
            graph.append({"@type": "Person", "name": m["nom"], "jobTitle": "Physiothérapeute", "image": m["photo"],
                          "worksFor": {"@id": SITE + "/#physiotherapy"}, "knowsLanguage": ["fr", "es"]})
    f = next((x for x in R if x["tipo"] == "faq"), None)
    if f:
        graph.append({"@type": "FAQPage", "@id": full + "#faq", "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a_text"]}} for q in f["faq"]]})
    return {"@context": "https://schema.org", "@graph": graph}


# ---------------------------------------------------------------- ensamblado
USADOS = set()


def nuevo_id(*p):
    i, k = eid(*p), 0
    while i in USADOS:
        k += 1; i = eid(*p, str(k))
    USADOS.add(i)
    return i


def construir(pag, idx_zona=0):
    slug, url, plantilla, lote, carpeta, foto, alt = pag
    meta, R = receta(slug, url, plantilla, lote, carpeta, foto, alt, idx_zona)
    d = OUT / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "receta.json").write_text(json.dumps(R, ensure_ascii=False, indent=1))
    markup = '<div class="pa-home">\n\n' + "\n\n".join(RENDER[r["tipo"]](r) for r in R) + "\n\n</div>\n"
    ld = jsonld(carpeta, url, meta, R, plantilla)
    ld_tag = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"
    style, script = (STYLE_HOME, SCRIPT_HOME) if plantilla == "home" else (STYLE_LOMB, SCRIPT_LOMB)
    inline_assets = not CSS_GLOBAL or plantilla == "home"   # la home conserva su CSS propio (hero con vídeo)
    widget_html = markup + ("\n" + style + "\n\n" + script + "\n" if inline_assets else "") + ld_tag
    t = copy.deepcopy(T_HOME if plantilla == "home" else T_LOMB)
    sec = t["content"][0]; col = sec["elements"][0]; w = col["elements"][0]
    sec["id"], col["id"], w["id"] = nuevo_id(slug, "section"), nuevo_id(slug, "column"), nuevo_id(slug, "widget")
    w["settings"]["html"] = widget_html
    h1 = next(r["h1"] for r in R if r["tipo"] == "hero")
    t["title"] = h1
    t["page_settings"] = {"hide_title": "yes"}
    dest = d / ("elementor-css-global.json" if CSS_GLOBAL else "elementor.json")
    dest.write_text(json.dumps(t, ensure_ascii=False))
    if not CSS_GLOBAL:
        estado = "borrador — noindex hasta confirmación" if lote == "B" else "publicable tras revisión"
        (d / "yoast.txt").write_text(
            f"SEO title ({len(meta['title'])}/60): {meta['title']}\nMeta description ({len(meta['meta'])}/155): {meta['meta']}\n"
            f"Slug: {url}\nFocus keyphrase: {meta['keyword_principal']}\nH1: {h1}\n"
            f"Indexación: {'NOINDEX hasta la confirmación del cliente (Yoast → Avanzado → ¿Permitir que los motores muestren esta página? = No)' if lote == 'B' else 'index, follow'}\n"
            f"Canonical: https://physioactiva.ch{url}\nEstado: {estado}\n")
        prev = (f'<!doctype html><html lang="fr-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>{esc(meta["title"])}</title><meta name="description" content="{esc(meta["meta"])}">'
                f'{"<meta name=robots content=noindex>" if lote == "B" else ""}<style>body{{margin:0;background:#fff}}</style></head><body>\n'
                f'<!-- Vista previa: solo el cuerpo de la página (el header y el footer los pone el tema). -->\n{widget_html}</body></html>')
        (d / "preview.html").write_text(prev)
    return {"slug": slug, "url": url, "plantilla": plantilla, "lote": lote, "title": meta["title"], "meta": meta["meta"], "h1": h1,
            "tipo": meta.get("tipo"), "componentes": [r["tipo"] for r in R], "a_confirmer": widget_html.count("[À CONFIRMER")}


if __name__ == "__main__":
    pedir = [a for a in sys.argv[1:] if not a.startswith("--")]
    res, iz = [], 0
    for p in PAGINAS:
        if not (PAG / p[4] / "fr.md").exists():
            print("FALTA fr.md:", p[0]); continue
        es_zona = p[0].startswith("physio-a-")
        if not pedir or p[0] in pedir:
            res.append(construir(p, iz))
        iz += 1 if es_zona else 0
    OUT.mkdir(parents=True, exist_ok=True)
    if not CSS_GLOBAL:
        (OUT / "_lote.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    for r in res:
        print(r["lote"], r["slug"], r["plantilla"], len(r["title"]), len(r["meta"]), r["a_confirmer"], " ".join(r["componentes"]))
