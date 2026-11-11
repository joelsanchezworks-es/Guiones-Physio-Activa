"""Página de ciudad en widgets NATIVOS de Elementor (cada bloque editable desde el panel).
Diseño pa-lp: el CSS va en un widget HTML pequeño al inicio; textos en Encabezado / Editor de texto / Botón /
Cuadro de icono / Acordeón (con «FAQ Schema» de Elementor) / Google Maps; imágenes de fondo nativas.
Uso: python3 scripts/construir_nativo.py ins
Salida: entregables/10_nativo/physio-a-<key>/{physio-a-<key>.json, preview.html, yoast.txt} + .zip
"""
import json, re, sys, pathlib, hashlib, html as H, zipfile
from urllib.parse import quote
from bs4 import BeautifulSoup

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from construir_ciudad_lp import parse, inline, subs, texto, SOINS, CLI, UP, SITE, ONEDOC, esc, ZON, DOMICILE  # noqa: E402

BASE = pathlib.Path(__file__).resolve().parent.parent
PAG = BASE / "entregables/5_paginas"
OUT = BASE / "entregables/10_nativo"
CSS = (BASE / "plantillas/pa-lp-nativo.css").read_text()

FICHAS = {
    "ins": dict(ville="Ins", vtitre="Ins (Anet)", url="/physio-a-ins/", commune="Ins", canton="Berne",
                wiki="https://fr.wikipedia.org/wiki/Ins_(Berne)",
                voisines=["Gampelen", "Müntschemier", "Brüttelen", "Treiten", "Siselen", "Erlach", "Vinelz", "Lüscherz"],
                hero=UP + "2025/06/Centerbild_IMG_9184-scaled-1.jpg", cta=UP + "2025/04/Physio-Activa-00036.jpg",
                soins_first=["domicile", "sport"]),
}


SOINS_FIRST = {"chietres": ["massage", "domicile"], "lyss": ["domicile", "drainage", "massage"], "fribourg": ["drainage", "massage", "domicile"], "payerne": ["drainage", "domicile"], "estavayer": ["sport", "drainage", "domicile"], "yverdon": ["drainage", "sport", "domicile"], "yvonand": ["domicile"], "lausanne": ["domicile", "drainage", "massage", "sport"], "la-neuveville": ["domicile", "massage"], "avenches": ["domicile", "massage"]}  # demanda local medida (massage kerzers 90/mes)


def ficha(key):
    if key in FICHAS:
        return FICHAS[key]
    z = ZON[key]
    brief = json.loads((BASE / "data/z_briefs_local.json").read_text()).get(key, {})
    dem = " ".join(k for _, k, _ in brief.get("services_locaux", []))
    return dict(ville=z["nom_fr"], vtitre=z["nom_titre"], url=z["url"], commune=z["commune"], canton=z["canton"], wiki=z["source_publique"],
                voisines=z["localites_voisines"], km=str(z["km_depuis_ins"]).replace(".", ","), domicile=key in DOMICILE,
                hero=UP + ("2026/09/Neuchatel-physio.jpg" if key == "neuchatel" else "2025/06/Centerbild_IMG_9184-scaled-1.jpg"),
                cta=UP + "2025/04/Physio-Activa-00036.jpg",
                soins_first=SOINS_FIRST.get(key) or [k for k in ("domicile", "drainage", "massage", "sport") if k in dem] or ["domicile"])


VAR = {  # frases fijas del constructor que cambian por ciudad para que las páginas no se parezcan
    "morat": dict(
        ameta="Physio Activa · physiothérapie pour Morat (Murten) et le district du Lac",
        soins_h2="Physiothérapie à Morat : nos soins les plus demandés",
        soins_p="Au cabinet d'Ins ou chez vous à Morat, voici les prises en charge que nos patients du bord du lac nous demandent le plus :",
        cta_p="Une douleur qui ne passe pas, une sortie d'hôpital à préparer ? Écrivez-nous : un physiothérapeute vous propose un créneau, en général dans la semaine, à Ins ou à domicile à Morat.",
        why_eb="Physio Activa en bref", why_h2="Quatre raisons de choisir Physio Activa depuis Morat",
        why_p="Bilingue, ouvert jusqu'à 20h et à quelques minutes de Morat, avec un espace d'entraînement complet.",
        faq_eb="Vos questions"),
    "chietres": dict(
        ameta="Physio Activa · physiothérapie et massage pour Kerzers (Chiètres)",
        soins_h2="Physiothérapie à Kerzers : ce que nous proposons",
        soins_p="Du massage thérapeutique à la rééducation après une opération, au cabinet d'Ins ou chez vous à Kerzers :",
        cta_p="Le dos qui coince, une épaule qui ne suit plus ? Envoyez-nous un message en allemand ou en français : un physiothérapeute vous rappelle et vous propose un créneau, souvent dans la semaine.",
        why_eb="Ce qui change pour vous", why_h2="Physio Activa pour Kerzers, en quatre points",
        why_p="Germanophone et francophone, ouvert le soir, à quelques minutes de Kerzers, avec massage et entraînement sur place.",
        faq_eb="On nous demande souvent"),
    "lyss": dict(
        ameta="Physio Activa · physiothérapie à domicile à Lyss et dans le Seeland",
        soins_h2="Physiothérapie à Lyss : nos soins",
        soins_p="Tous nos soins sont possibles pour les patients de Lyss ; la plupart se font aussi à domicile :",
        cta_p="Vous ne pouvez pas faire la route jusqu'à Ins ? Pas de souci : nous venons chez vous à Lyss ou dans les communes voisines. Écrivez-nous en allemand ou en français.",
        why_eb="Pour les patients de Lyss", why_h2="Physio Activa à Lyss, en quatre points",
        why_p="Soins à domicile dans tout le secteur Lyss–Aarberg, drainage et massage, en allemand ou en français, jusqu'à 20h.",
        faq_eb="Questions des patients"),
    "fribourg": dict(
        ameta="Physio Activa · physiothérapie, drainage lymphatique et dry needling pour Fribourg",
        soins_h2="Physiothérapie à Fribourg : tous nos soins",
        soins_p="Au cabinet d'Ins, les patients de Fribourg ont accès à l'ensemble de nos soins, dont les plus demandés :",
        cta_p="Un œdème, une prothèse récente, une douleur qui revient ? Réservez un créneau, en soirée si besoin : le premier rendez-vous a lieu dans la semaine dans la plupart des cas.",
        why_eb="Pourquoi faire la route", why_h2="Pourquoi des patients de Fribourg viennent à Ins",
        why_p="Drainage lymphatique manuel, dry needling, entraînement sur appareils et créneaux jusqu'à 20h, en français ou en allemand.",
        faq_eb="Vos questions, nos réponses"),
    "payerne": dict(
        ameta="Physio Activa · physiothérapie pour Payerne et la Broye",
        soins_h2="Physiothérapie à Payerne : nos soins",
        soins_p="Les patients de Payerne et de la Broye ont accès à tous nos soins au cabinet d'Ins, notamment :",
        cta_p="Vous sortez de l'hôpital ou une douleur s'installe ? Réservez dès maintenant : le premier rendez-vous a lieu dans la semaine dans la plupart des cas, en soirée si besoin.",
        why_eb="L'essentiel pour vous", why_h2="Physio Activa pour les patients de la Broye",
        why_p="Suivi après l'hôpital, espace d'entraînement, créneaux jusqu'à 20h et équipe multilingue.",
        faq_eb="Ce que vous nous demandez"),
    "estavayer": dict(
        ameta="Physio Activa · physiothérapie pour Estavayer-le-Lac et la rive sud du lac",
        soins_h2="Physiothérapie pour Estavayer : nos soins",
        soins_p="Au cabinet d'Ins, et parfois à domicile selon l'adresse, les patients d'Estavayer bénéficient de tous nos soins :",
        cta_p="Blessure de sport, retour de l'hôpital ou douleur qui traîne ? Réservez : un premier rendez-vous est possible dans la semaine dans la plupart des cas, même en soirée.",
        why_eb="En quelques mots", why_h2="Physio Activa pour les patients d'Estavayer",
        why_p="Rééducation et reprise du sport, drainage lymphatique, appareils d'entraînement et créneaux jusqu'à 20h.",
        faq_eb="Questions d'Estavayer"),
    "yverdon": dict(
        ameta="Physio Activa · drainage lymphatique médical et fitness médical pour Yverdon-les-Bains",
        soins_h2="Physiothérapie pour Yverdon : nos soins",
        soins_p="Les patients d'Yverdon-les-Bains ont accès à l'ensemble de nos soins au cabinet d'Ins, en particulier :",
        cta_p="Un œdème après une opération, une blessure de sport, une rééducation à reprendre ? Réservez un créneau, y compris en soirée : premier rendez-vous dans la semaine dans la plupart des cas.",
        why_eb="Ce que nous apportons", why_h2="Pourquoi des patients d'Yverdon choisissent Physio Activa",
        why_p="Drainage lymphatique fait par un physiothérapeute, fitness médical encadré et créneaux jusqu'à 20h.",
        faq_eb="Questions des patients d'Yverdon"),
    "yvonand": dict(
        ameta="Physio Activa · votre physio pour Yvonand et le Nord vaudois",
        soins_h2="Physio à Yvonand : nos soins",
        soins_p="Les patients d'Yvonand ont accès à tous nos soins de physiothérapie au cabinet d'Ins :",
        cta_p="Une douleur qui traîne ou une rééducation à démarrer ? Votre physio vous propose un créneau, souvent dans la semaine et jusqu'à 20h.",
        why_eb="Votre physio en bref", why_h2="Physio Activa pour les patients d'Yvonand",
        why_p="Un physio qui explique, des appareils pour progresser et des rendez-vous le soir.",
        faq_eb="Vos questions au physio"),
    "lausanne": dict(
        ameta="Physio Activa · physio à domicile selon l'adresse et cabinet d'Ins, pour Lausanne",
        soins_h2="Physiothérapie pour Lausanne : nos soins",
        soins_p="Au cabinet d'Ins, les patients venus de Lausanne retrouvent tous nos soins, en particulier :",
        cta_p="Besoin d'un physio à domicile à Lausanne ? Écrivez-nous votre adresse : nous vérifions si un physiothérapeute peut venir, sinon nous vous proposons un créneau au cabinet d'Ins jusqu'à 20h.",
        why_eb="En résumé", why_h2="Ce que Physio Activa offre aux patients de Lausanne",
        why_p="Créneaux jusqu'à 20h, drainage lymphatique médical, dry needling et entraînement sur appareils, en cinq langues.",
        faq_eb="Questions de Lausannois"),
    "la-neuveville": dict(
        ameta="Physio Activa · physiothérapie à domicile à La Neuveville, au Landeron et sur le Plateau de Diesse",
        soins_h2="Physiothérapie à La Neuveville : nos soins",
        soins_p="À domicile à La Neuveville ou au Landeron, ou au cabinet d'Ins à quelques minutes, voici nos soins les plus demandés :",
        cta_p="Une douleur à La Neuveville ou au Landeron ? Nous venons chez vous ou vous recevons à Ins, en général dans la semaine et jusqu'à 20h.",
        why_eb="Pourquoi nous choisir", why_h2="Physio Activa pour La Neuveville et Le Landeron",
        why_p="Physiothérapie à domicile, massage thérapeutique, fitness médical et créneaux le soir, à quelques minutes de chez vous.",
        faq_eb="Vos questions"),
    "avenches": dict(
        ameta="Physio Activa · physiothérapie à domicile et fitness médical pour Avenches et la Broye-Vully",
        soins_h2="Physiothérapie à Avenches : nos soins",
        soins_p="À domicile à Avenches, Domdidier ou Salavaux, ou au cabinet d'Ins : voici nos soins les plus demandés.",
        cta_p="Une contracture, un dos qui coince, une prothèse récente ? Nous venons chez vous ou vous recevons à Ins, généralement dans la semaine, jusqu'à 20h.",
        why_eb="Les points forts", why_h2="Physio Activa pour Avenches et la Broye-Vully",
        why_p="Physiothérapie à domicile, massage thérapeutique et fitness médical encadré, avec des créneaux le soir.",
        faq_eb="Questions fréquentes"),
}


def var(key, k, default):
    return VAR.get(key, {}).get(k, default)


def de(v):
    return ("d'" if v[0].lower() in "aeiouyéèêiîh" else "de ") + v


def imgs_alt(tpl):
    """Huecos de imagen de la plantilla con su texto alternativo sugerido."""
    out = []
    def walk(e):
        s = e.get("settings", {})
        if e["elType"] == "section" and "pa-hero" in s.get("css_classes", ""):
            out.append(("Fondo del hero (sección › Estilo › Fondo)", "foto de la ciudad o del cabinet, 1920 px"))
        if e["elType"] == "section" and "pa-cta" in s.get("css_classes", ""):
            out.append(("Fondo del CTA final (sección › Estilo › Fondo)", "foto del cabinet; la capa azul oscura ya está puesta"))
        if e.get("widgetType") == "image":
            out.append((f"Imagen {sum(1 for x in out if x[0].startswith('Imagen')) + 1} del artículo", "alt: " + s["image"]["alt"]))
        for x in e.get("elements", []):
            walk(x)
    for s in tpl["content"]:
        walk(s)
    return out


def eid(*p):
    return hashlib.sha1("|".join(p).encode()).hexdigest()[:7]


class B:
    """Generador de elementos Elementor con IDs estables."""
    def __init__(s, slug):
        s.slug, s.n = slug, 0

    def _id(s):
        s.n += 1
        return eid(s.slug, "nat", str(s.n))

    def w(s, wtype, settings, css=""):
        if css:
            settings["_css_classes"] = css
        return {"id": s._id(), "elType": "widget", "widgetType": wtype, "settings": settings, "elements": [], "isInner": False}

    def col(s, widgets, size=100, css="", inner=False):
        st = {"_column_size": size, "_inline_size": None}
        if css:
            st["css_classes"] = css
        return {"id": s._id(), "elType": "column", "settings": st, "elements": widgets, "isInner": inner}

    def sec(s, cols, css="", inner=False, **st):
        settings = {"gap": "no"} | st
        if css:
            settings["css_classes"] = css
        return {"id": s._id(), "elType": "section", "settings": settings, "elements": cols, "isInner": inner}


def pad(t, r, b, l, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": False}


def icon(v, lib="fa-solid"):
    return {"value": v, "library": lib}


def link(u, ext=False):
    return {"url": u, "is_external": "on" if ext else "", "nofollow": "", "custom_attributes": ""}


def bloques(bl):
    out = []
    for b in bl:
        if b.name == "p":
            lang = ' lang="de"' if re.match(r"(Physiotherapie |Ja\.|Unser )", b.get_text()) else ""
            out.append(f"<p{lang}>{inline(b)}</p>")
        elif b.name in ("ul", "ol"):
            out.append('<ul class="plain">' + "".join(f"<li>{inline(li)}</li>" for li in b.find_all("li", recursive=False)) + "</ul>")
        elif b.name == "h3":
            out.append(f"<h3>{inline(b)}</h3>")
    return "\n".join(out)


def build(key):
    f = ficha(key)
    src = f"physio-a-{key}"                 # carpeta del texto fuente (5_paginas)
    slug = f["url"].strip("/")              # slug publicado = nombre de la plantilla y de los archivos
    ville, vtitre = f["ville"], f["vtitre"]
    es_ins = key == "ins"
    cab = "au cabinet d'Ins"
    if es_ins:
        f["domicile"] = True
    meta, h1, intro, secs = parse(re.sub(r"^((?!- )[^\n]+)\n(- )", r"\1\n\n\2", (PAG / src / "fr.md").read_text(), flags=re.M))  # lista sin línea en blanco
    h1t = texto(h1)
    b = B(slug)
    wa = CLI["whatsapp_href"] + "?text=" + quote(f"Bonjour, je souhaite prendre rendez-vous chez Physio Activa (physio à {ville}).")
    why = next(s for s in secs if re.search(r"essentiel", texto(s["h2"]), re.I))
    faq = next(s for s in secs if re.match(r"questions fréquentes", texto(s["h2"]), re.I))
    cta = secs[-1]
    cuerpo = [s for s in secs if s not in (why, faq, cta)]

    def btn(text, href, ic, kind="", ext=True, lib="fa-solid"):
        return b.w("button", {"text": text, "link": link(href, ext), "selected_icon": icon(ic, lib), "icon_indent": {"unit": "px", "size": 8},
                              "_element_width": "auto", "_element_width_mobile": "inherit"}, ("pa-btn " + kind).strip())

    btn_rdv = lambda: btn("Rendez-vous online", ONEDOC, "fas fa-calendar-check")
    btn_wa = lambda: btn("WhatsApp", wa, "fab fa-whatsapp", "wa", lib="fa-brands")

    secciones = []
    # 0 · estilos (no editar)
    secciones.append(b.sec([b.col([b.w("html", {"html": "<style>\n" + CSS + "\n</style>"}, "pa-styles")])], "pa-lp pa-styles-sec"))
    # 1 · hero
    secciones.append(b.sec([b.col([
        b.w("heading", {"title": f"Physiothérapie · {vtitre}", "header_size": "p", "align": "center"}, "pa-eyebrow"),
        b.w("heading", {"title": h1t, "header_size": "h1", "align": "center"}, "pa-h1"),
        b.w("heading", {"title": var(key, "ameta", f"Par l'équipe Physio Activa · Physiothérapie à {ville}"), "header_size": "div", "align": "center"}, "pa-ameta"),
        btn_rdv(), btn_wa(),
    ], css="pa-center")], "pa-lp pa-hero", layout="full_width", stretch_section="section-stretched",
        background_background="classic", background_color="#0E2C4F", background_position="center center",
        background_size="cover", background_overlay_background="classic", background_overlay_color="#000000",
        background_overlay_opacity={"unit": "px", "size": 0.45}, padding=pad(120, 24, 120, 24), padding_mobile=pad(84, 18, 76, 18)))
    # 2 · migas
    secciones.append(b.sec([b.col([b.w("text-editor", {"editor": f'<p><a href="/">Accueil</a> <span aria-hidden="true">›</span> Physiothérapie à {esc(ville)}</p>'}, "pa-crumbs")])],
                           "pa-lp pa-crumbs-sec", content_width={"unit": "px", "size": 828}))
    # 3 · artículo
    km_route = "https://www.google.com/maps/dir/?api=1" + ("" if es_ins else f"&origin={quote(ville + ', Suisse')}") + f"&destination={quote('Physio Activa, Rämismatte 21, 3232 Ins')}"
    fiche_rows = [("Cabinet", "Rämismatte 21, 3232 Ins (1er étage du bâtiment Lidl, InsGym), parking sur place")]
    if not es_ins:
        fiche_rows.append((f"Depuis {ville}", f"Environ {f['km']} km à vol d'oiseau jusqu'au cabinet d'Ins"))
    fiche_rows += [
        ("À domicile", f"{ville} et environs ({', '.join(f['voisines'])})" if f["domicile"] else f"Selon votre adresse ({', '.join(f['voisines'])}) : contactez-nous pour le vérifier"),
        ("Délai", "Rendez-vous dans la semaine dans la plupart des cas"),
        ("Horaires", "Du lundi au vendredi, jusqu'à 20h"),
        ("Langues", "Français, allemand, anglais, espagnol et portugais"),
        ("Assurances", "Cabinet reconnu par toutes les compagnies d'assurance maladie en Suisse"),
        ("Réservation", "En ligne (OneDoc), par WhatsApp ou au 076 627 38 38"),
    ]
    fiche = ('<div class="fiche"><table><caption>' + esc((f"Physio Activa à {ville}, en bref" if es_ins else f"Physio Activa pour les patients {de(ville)}, en bref")) + "</caption><tbody>"
             + "".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(c)}</td></tr>' for a, c in fiche_rows) + "</tbody></table></div>")
    soins = sorted(SOINS, key=lambda s: (f["soins_first"].index(s[3]) if s[3] in f["soins_first"] else 99, SOINS.index(s)))[:10]
    soins_html = '<ul class="soins-list">' + "".join(f'<li><a href="{u}"><strong>{esc(t)}</strong><span>{esc(d)}</span></a></li>' for u, t, d, _ in soins) + "</ul>"
    art = [b.w("text-editor", {"editor": "<p>" + " ".join(inline(x) for x in intro if x.name == "p") + "</p>"}, "pa-lead"),
           b.w("html", {"html": fiche}, "pa-fiche")]
    for i, s in enumerate(cuerpo):
        h2t = texto(s["h2"])
        art.append(b.w("heading", {"title": h2t, "header_size": "h2"}, "pa-h2"))
        art.append(b.w("text-editor", {"editor": bloques(s["b"])}, "pa-text"))
        if i == 0:
            art.append(btn("Itinéraire vers le cabinet" if es_ins else f"Itinéraire depuis {ville}", km_route, "fas fa-route", "outline"))
            art.append(b.w("image", {"image": {"url": "", "id": "", "alt": (f"Physiothérapeute de Physio Activa en séance au cabinet de physiothérapie à {ville}" if es_ins else f"Physiothérapeute de Physio Activa en séance, physio pour les patients {de(ville)}")},
                                     "image_size": "full"}, "pa-img"))
        if re.search(r"domicile", h2t, re.I):
            art.append(b.w("heading", {"title": var(key, "soins_h2", f"Nos soins de physiothérapie à {ville}" if es_ins else f"Nos soins de physiothérapie pour les patients {de(ville)}"), "header_size": "h2"}, "pa-h2"))
            art.append(b.w("text-editor", {"editor": "<p>" + var(key, "soins_p", f"Vous avez accès à l'ensemble de nos soins, {'au cabinet' if es_ins else cab} ou à domicile selon votre situation. Les plus demandés :") + f"</p>\n{soins_html}"}, "pa-text"))
            art.append(b.w("text-editor", {"editor": '<div class="cta-inline"><p>' + var(key, "cta_p", f"Vous habitez {esc(ville)} ou un village voisin et vous avez mal ? Nous vous proposons un rendez-vous dans la semaine dans la plupart des cas, " + ((("au cabinet" if es_ins else cab) + " ou chez vous.") if f["domicile"] else f"{cab} ou à domicile selon votre adresse.")) + '</p>'
                                                     f'<p><a class="btn" href="{ONEDOC}" target="_blank" rel="noopener">Rendez-vous online</a></p></div>'}, "pa-text"))
        if re.search(r"déroule|parcours|premier contact|étapes|pas à pas|quatre temps|première séance|votre suivi|quatre étapes|programme maison|vos séances", h2t, re.I):
            art.append(b.w("image", {"image": {"url": "", "id": "", "alt": (f"Salle de traitement du cabinet Physio Activa à {ville}" if es_ins else f"Salle de traitement du cabinet Physio Activa à Ins, proche {de(ville)}")},
                                     "image_size": "full"}, "pa-img"))
    secciones.append(b.sec([b.col(art, css="article")], "pa-lp pa-article", content_width={"unit": "px", "size": 828}, padding=pad(56, 0, 72, 0)))
    # 4 · pourquoi
    ICON = ["fas fa-shield-heart", "fas fa-house-medical", "fas fa-clipboard-list", "fas fa-calendar-check"]
    cards = [b.w("icon-box", {"selected_icon": icon(ICON[j]), "title_text": texto(sb["h3"]),
                              "description_text": " ".join(texto(c) for c in sb["c"] if c.name == "p"), "title_size": "h3", "position": "top", "text_align": "left"},
                 "pa-wcard") for j, sb in enumerate(subs(why["b"]))]
    grid = b.sec([b.col(cards[0:1] + cards[2:3], 50, inner=True), b.col(cards[1:2] + cards[3:4], 50, inner=True)], "pa-why-grid", inner=True,
                 gap="extended", content_width={"unit": "px", "size": 1000})
    secciones.append(b.sec([b.col([
        b.w("heading", {"title": var(key, "why_eb", "Pourquoi Physio Activa"), "header_size": "p", "align": "center"}, "pa-eyebrow"),
        b.w("heading", {"title": var(key, "why_h2", f"Pourquoi les patients {de(ville)} choisissent Physio Activa"), "header_size": "h2", "align": "center"}, "pa-title"),
        b.w("text-editor", {"editor": "<p>" + var(key, "why_p", "Un cabinet de physiothérapie à Ins, des soins à domicile dans la région et une équipe qui vous reçoit en cinq langues.") + "</p>", "align": "center"}, "pa-sub"),
        grid])], "pa-lp pa-soft", padding=pad(72, 24, 72, 24), padding_mobile=pad(54, 16, 54, 16)))
    # 5 · FAQ (acordeón nativo + FAQ Schema de Elementor)
    tabs = []
    for i, sb in enumerate(subs(faq["b"])):
        ans = "".join((f'<p lang="de">' if re.match(r"(Ja\.|Unser )", c.get_text()) else "<p>") + inline(c) + "</p>" for c in sb["c"] if c.name == "p")
        tabs.append({"tab_title": texto(sb["h3"]), "tab_content": ans, "_id": eid(slug, "faq", str(i))})
    secciones.append(b.sec([b.col([
        b.w("heading", {"title": var(key, "faq_eb", "Questions fréquentes"), "header_size": "p", "align": "center"}, "pa-eyebrow"),
        b.w("heading", {"title": texto(faq["h2"]), "header_size": "h2", "align": "center"}, "pa-title"),
        b.w("accordion", {"tabs": tabs, "faq_schema": "yes", "title_html_tag": "h3", "icon_align": "right",
                          "selected_icon": icon("fas fa-plus"), "selected_active_icon": icon("fas fa-minus")}, "pa-faq"),
    ])], "pa-lp pa-faq-sec", content_width={"unit": "px", "size": 868}, padding=pad(72, 24, 72, 24), padding_mobile=pad(54, 16, 54, 16)))
    # 6 · CTA con imagen de fondo oscurecida
    cta_p = " ".join(texto(x) for x in cta["b"] if x.name == "p")
    secciones.append(b.sec([b.col([
        b.w("heading", {"title": texto(cta["h2"]), "header_size": "h2", "align": "center"}, "pa-cta-title"),
        b.w("text-editor", {"editor": f"<p>{esc(cta_p)}</p>", "align": "center"}, "pa-cta-sub"),
        btn_rdv(), btn_wa(), btn("Appelez-nous · 076 627 38 38", "tel:+41766273838", "fas fa-phone", "ghost", ext=False),
    ], css="pa-center")], "pa-lp pa-cta", layout="full_width", stretch_section="section-stretched",
        background_background="classic", background_color="#0E2C4F", background_position="center center", background_size="cover",
        background_overlay_background="classic", background_overlay_color="#0E2C4F", background_overlay_opacity={"unit": "px", "size": 0.86},
        padding=pad(88, 24, 88, 24), padding_mobile=pad(64, 16, 64, 16)))
    # 7 · mapa
    secciones.append(b.sec([b.col([b.w("google_maps", {"address": "Physio Activa, Rämismatte 21, 3232 Ins", "zoom": {"unit": "px", "size": 16},
                                                         "height": {"unit": "px", "size": 480}, "height_mobile": {"unit": "px", "size": 380}}, "pa-map")])],
                           "pa-lp pa-map-sec", layout="full_width", stretch_section="section-stretched"))
    # 8 · botón flotante WhatsApp + schema local (no editar)
    full = SITE + f["url"]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Physiotherapy", "@id": SITE + "/#physiotherapy", "name": "Physio Activa", "url": SITE + "/",
         "logo": UP + "2026/06/Physio-Activa-Logo00001.png", "image": UP + "2025/04/Physio-Activa-00031.jpg",
         "telephone": "+41 76 627 38 38", "email": "physio@physioactiva.ch",
         "address": {"@type": "PostalAddress", "streetAddress": "Rämismatte 21", "postalCode": "3232", "addressLocality": "Ins", "addressRegion": "BE", "addressCountry": "CH"},
         "geo": {"@type": "GeoCoordinates", "latitude": CLI["geo"]["lat"], "longitude": CLI["geo"]["lng"]},
         "hasMap": "https://www.google.com/maps?cid=17004812906479027083",
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:30", "closes": "20:00"}],
         "areaServed": [{"@type": "City", "name": f["commune"], "sameAs": f["wiki"]}] + [{"@type": "Place", "name": v} for v in f["voisines"]] + ([] if es_ins else [{"@type": "Place", "name": "Ins"}]),
         "availableLanguage": ["fr", "de", "en", "es", "pt"],
         "sameAs": ["https://www.instagram.com/physio_activa_/", "https://www.facebook.com/profile.php?id=100094154144954", "https://www.google.com/maps?cid=17004812906479027083"]},
        {"@type": "WebPage", "@id": full + "#webpage", "url": full, "name": meta["title"], "description": meta["meta"], "inLanguage": "fr-CH",
         "about": {"@id": full + "#service"}, "primaryImageOfPage": {"@type": "ImageObject", "url": f["hero"]}},
        {"@type": "Service", "@id": full + "#service", "name": f"Physiothérapie à {ville}", "serviceType": "Physiothérapie au cabinet et à domicile",
         "provider": {"@id": SITE + "/#physiotherapy"},
         "areaServed": {"@type": "City", "name": f["commune"], "containedInPlace": {"@type": "AdministrativeArea", "name": f"Canton de {f['canton']}"}}}]}
    tail = (f'<a class="pa-wafab" href="{esc(wa)}" target="_blank" rel="noopener" aria-label="Contacter Physio Activa sur WhatsApp"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i></a>\n'
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    secciones.append(b.sec([b.col([b.w("html", {"html": tail}, "pa-tail")])], "pa-lp pa-tail-sec"))

    tpl = {"content": secciones, "page_settings": {"hide_title": "yes"}, "version": "0.4", "title": f"Physio à {ville}", "type": "page"}
    d = OUT / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{slug}.json").write_text(json.dumps(tpl, ensure_ascii=False, indent=1))
    with zipfile.ZipFile(d / f"{slug}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(d / f"{slug}.json", f"{slug}.json")
    (d / "yoast.txt").write_text(f"SEO title ({len(meta['title'])}/60): {meta['title']}\nMeta description ({len(meta['meta'])}/155): {meta['meta']}\n"
                                 f"Slug: {f['url']}\nFocus keyphrase: {meta['keyword_principal']}\nH1: {h1t}\nIndexación: index, follow\n"
                                 "\nIMÁGENES (la plantilla se importa SIN imágenes para no duplicarlas en la biblioteca; elígelas en Elementor):\n"
                                 + "".join(f"- {n}: {a}\n" for n, a in imgs_alt(tpl)) +
                                 "- Imagen destacada / Open Graph de Yoast: la misma del hero.\n")
    (d / "preview.html").write_text(preview(tpl, meta))
    return tpl, meta


# ---------- vista previa aproximada (imita el DOM de Elementor en el frontend) ----------
BASE_CSS = """body{margin:0;font-family:sans-serif}.elementor-section{position:relative}.elementor-section .elementor-container{display:flex;margin:0 auto;position:relative;max-width:1140px}
.elementor-section.elementor-section-full_width>.elementor-container{max-width:none}.elementor-column{position:relative;display:flex;min-height:1px;width:100%}
.elementor-col-50{width:50%}.elementor-widget-wrap{position:relative;width:100%;display:flex;flex-wrap:wrap;align-content:flex-start;padding:10px}
.elementor-section-gap-no .elementor-widget-wrap{padding:0}.elementor-widget{position:relative;width:100%}.elementor-widget:not(:last-child){margin-bottom:20px}
.elementor-widget__width-auto{width:auto;max-width:100%}.elementor-background-overlay{position:absolute;inset:0}
.elementor-button{display:inline-block;line-height:1;padding:12px 24px;background:#69727d;color:#fff;border-radius:3px}.elementor-button-content-wrapper{display:flex;justify-content:center;gap:8px}
.elementor-heading-title{margin:0;padding:0;line-height:1}.elementor-tab-content{display:none}.elementor-tab-content.elementor-active{display:block}
.elementor-icon{display:inline-block}.elementor-accordion-icon-right{float:right}.elementor-image img{max-width:100%;height:auto}
@media(max-width:767px){.elementor-column{width:100% !important}.elementor-container{flex-wrap:wrap}.elementor-widget-mobile__width-inherit{width:inherit;max-width:100%}}"""


def r_widget(w):
    s, t = w["settings"], w["widgetType"]
    if t == "html":
        inner = s["html"]
    elif t == "heading":
        tag = s["header_size"]
        inner = f'<{tag} class="elementor-heading-title elementor-size-default">{esc(s["title"])}</{tag}>'
    elif t == "text-editor":
        inner = s["editor"]
    elif t == "button":
        ic = s["selected_icon"]["value"].replace("fas ", "fa-solid ").replace("fab ", "fa-brands ")
        inner = (f'<div class="elementor-button-wrapper"><a class="elementor-button elementor-button-link elementor-size-sm" href="{esc(s["link"]["url"])}">'
                 f'<span class="elementor-button-content-wrapper"><span class="elementor-button-icon"><i class="{ic}"></i></span><span class="elementor-button-text">{esc(s["text"])}</span></span></a></div>')
    elif t == "image":
        inner = (f'<img src="{s["image"]["url"]}" alt="{esc(s["image"]["alt"])}" loading="lazy">' if s["image"]["url"] else
                 '<div style="aspect-ratio:16/9;border-radius:16px;background:#e3e8ee;display:flex;align-items:center;justify-content:center;color:#7a8794;font:14px sans-serif">Imagen: elígela en Elementor</div>')
    elif t == "icon-box":
        ic = s["selected_icon"]["value"].replace("fas ", "fa-solid ")
        inner = (f'<div class="elementor-icon-box-wrapper"><div class="elementor-icon-box-icon"><span class="elementor-icon"><i class="{ic}"></i></span></div>'
                 f'<div class="elementor-icon-box-content"><h3 class="elementor-icon-box-title"><span>{esc(s["title_text"])}</span></h3><p class="elementor-icon-box-description">{esc(s["description_text"])}</p></div></div>')
    elif t == "accordion":
        items = "".join(
            f'<div class="elementor-accordion-item"><h3 class="elementor-tab-title{" elementor-active" if i == 0 else ""}"><span class="elementor-accordion-icon elementor-accordion-icon-right">'
            f'<span class="elementor-accordion-icon-closed"><i class="fa-solid fa-plus"></i></span><span class="elementor-accordion-icon-opened"><i class="fa-solid fa-minus"></i></span></span>'
            f'<a class="elementor-accordion-title" href="">{esc(x["tab_title"])}</a></h3><div class="elementor-tab-content elementor-clearfix{" elementor-active" if i == 0 else ""}">{x["tab_content"]}</div></div>'
            for i, x in enumerate(s["tabs"]))
        inner = f'<div class="elementor-accordion">{items}</div>'
    elif t == "google_maps":
        inner = (f'<div class="elementor-custom-embed"><iframe loading="lazy" style="width:100%;height:{s["height"]["size"]}px;border:0" '
                 f'src="https://maps.google.com/maps?q={quote(s["address"])}&amp;t=m&amp;z=16&amp;output=embed&amp;iwloc=near" title="{esc(s["address"])}"></iframe></div>')
    elif t == "section":
        return r_section(w)
    cls = f'elementor-element elementor-widget elementor-widget-{t} {s.get("_css_classes", "")}'
    if s.get("_element_width") == "auto":
        cls += " elementor-widget__width-auto"
    if s.get("_element_width_mobile") == "inherit":
        cls += " elementor-widget-mobile__width-inherit"
    return f'<div class="{cls}"><div class="elementor-widget-container">{inner}</div></div>'


def r_section(sec):
    s = sec["settings"]
    cls = f'elementor-section elementor-element {"elementor-inner-section" if sec["isInner"] else "elementor-top-section"} elementor-section-{"full_width" if s.get("layout") == "full_width" else "boxed"} elementor-section-gap-{s.get("gap", "default")} {s.get("css_classes", "")}'
    style = ""
    if s.get("background_image"):
        style += f'background-image:url({s["background_image"]["url"]});background-size:cover;background-position:center;'
    p = s.get("padding")
    if p:
        style += f'padding:{p["top"]}px {p["right"]}px {p["bottom"]}px {p["left"]}px;'
    ov = ""
    if s.get("background_overlay_color"):
        ov = f'<div class="elementor-background-overlay" style="background:{s["background_overlay_color"]};opacity:{s["background_overlay_opacity"]["size"]}"></div>'
    cw = s.get("content_width", {}).get("size")
    cstyle = f' style="max-width:{cw}px"' if cw else ""
    cols = ""
    for c in sec["elements"]:
        cs = c["settings"]
        cols += (f'<div class="elementor-column elementor-col-{cs["_column_size"]} elementor-element {cs.get("css_classes", "")}"><div class="elementor-widget-wrap elementor-element-populated">'
                 + "".join(r_section(x) if x["elType"] == "section" else r_widget(x) for x in c["elements"]) + "</div></div>")
    return f'<section class="{cls}" style="{style}">{ov}<div class="elementor-container elementor-column-gap-{s.get("gap", "default")}"{cstyle}>{cols}</div></section>'


def preview(tpl, meta):
    body = "".join(r_section(s) for s in tpl["content"])
    return (f'<!doctype html><html lang="fr-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(meta["title"])}</title><meta name="description" content="{esc(meta["meta"])}"><style>{BASE_CSS}</style></head>'
            f'<body><div class="elementor elementor-page">{body}</div>'
            "<script>document.querySelectorAll('.elementor-tab-title').forEach(function(t){t.addEventListener('click',function(e){e.preventDefault();var c=t.nextElementSibling,o=t.classList.contains('elementor-active');"
            "t.closest('.elementor-accordion').querySelectorAll('.elementor-active').forEach(function(x){x.classList.remove('elementor-active')});if(!o){t.classList.add('elementor-active');c.classList.add('elementor-active')}})})</script>"
            "</body></html>")


if __name__ == "__main__":
    for k in sys.argv[1:]:
        tpl, meta = build(k)
        print(k, "secciones", len(tpl["content"]), meta["title"], len(meta["title"]), len(meta["meta"]))
