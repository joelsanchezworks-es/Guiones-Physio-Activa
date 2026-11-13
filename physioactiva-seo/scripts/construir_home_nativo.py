"""Home de physioactiva.ch en widgets NATIVOS de Elementor (cada bloque editable), mismo sistema que las ciudades.
Uso: python3 scripts/construir_home_nativo.py
Salida: entregables/13_home_nativo/{accueil.json, accueil.zip, preview.html, yoast.txt}
Cambios SEO frente a la home anterior (auditoría 2026-11-13): H1 sin promesa «dès cette semaine», bloque de texto
«Votre cabinet de physiothérapie à Ins», 12 soins con enlaces (fitness → /fitness-medical/, périnée → plancher pelvien),
14 zonas enlazadas, FAQ con «FAQ Schema» de Elementor, schema Physiotherapy con el @id de Yoast (#organization).
"""
import json, sys, pathlib, zipfile
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from construir_nativo import B, pad, icon, link, CSS, estilos_nativos, preview, imgs_alt, UP, SITE, ONEDOC, CLI  # noqa: E402

BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "entregables/13_home_nativo"
VIDEO = UP + "2026/06/Physioactiva.mp4"
CTA_BG = UP + "2026/11/Centerbild_IMG_9184-scaled-1.jpg"
GBP = "https://www.google.com/maps?cid=17004812906479027083"
WA = CLI["whatsapp_href"] + "?text=" + quote("Bonjour, je souhaite prendre rendez-vous chez Physio Activa à Ins.")
NAVY, AZURE, AZURE_D = "#0E2C4F", "#29A9E0", "#1E8AC0"

TITLE = "Physio à Ins (Anet) et à domicile | Physio Activa"
META = ("Physio à Ins (Anet) : cabinet de physiothérapie et soins à domicile dans le Seeland et les Trois-Lacs. "
        "Ouvert jusqu'à 20h. Prenez rendez-vous.")

CSS_HOME = """
/* ===== Home (complementos del diseño pa-lp) ===== */
.pa-lp.pa-home-hero{background-color:#0E2C4F !important}
.pa-lp .pa-rating .elementor-heading-title a,.pa-lp .pa-rating .elementor-heading-title{color:#fff !important;font-size:14px !important;font-weight:600 !important}
.pa-lp .pa-rating .elementor-heading-title{display:inline-block;background:rgba(0,0,0,.32);border:1px solid rgba(255,255,255,.22);padding:8px 16px;border-radius:40px}
.pa-lp .pa-grid .elementor-widget-wrap{padding:0 9px !important}
.pa-lp .pa-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px 22px;margin-bottom:18px !important;transition:transform .25s,box-shadow .25s,border-color .25s;height:auto}
.pa-lp .pa-card:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(14,44,79,.10);border-color:transparent}
.pa-lp .pa-card .elementor-icon-box-wrapper{text-align:left !important}
.pa-lp .pa-card .elementor-icon-box-icon{margin:0 0 12px !important;display:block}
.pa-lp .pa-card .elementor-icon{width:46px;height:46px;border-radius:12px;background:var(--tint);color:var(--azure) !important;fill:var(--azure) !important;display:flex !important;align-items:center;justify-content:center;font-size:19px !important;padding:0 !important;border:none !important}
.pa-lp .pa-card .elementor-icon svg{width:19px;height:19px}
.pa-lp .pa-card .elementor-icon-box-title,.pa-lp .pa-card .elementor-icon-box-title a{font-family:'Poppins',sans-serif !important;font-size:17px !important;color:var(--navy) !important;font-weight:600 !important;line-height:1.3 !important;margin:0 0 6px !important}
.pa-lp .pa-card .elementor-icon-box-description{color:var(--muted) !important;font-size:14.5px !important;line-height:1.6 !important;margin:0 !important}
.pa-lp .pa-card a{color:inherit}
.pa-lp.pa-stats{background-color:#0E2C4F !important}
.pa-lp .pa-stat .elementor-icon-box-title,.pa-lp .pa-stat .elementor-icon-box-title span{font-family:'Poppins',sans-serif !important;color:#fff !important;font-size:30px !important;font-weight:700 !important;margin:6px 0 2px !important}
.pa-lp .pa-stat .elementor-icon-box-description{color:#DCE9F4 !important;font-size:14.5px !important;margin:0 !important}
.pa-lp .pa-stat .elementor-icon{color:#29A9E0 !important;fill:#29A9E0 !important;font-size:24px !important}
.pa-lp .pa-stat .elementor-icon-box-wrapper{text-align:center !important}
.pa-lp .pa-member-name .elementor-heading-title{font-family:'Poppins',sans-serif !important;color:#29A9E0 !important;font-size:22px !important;font-weight:600 !important}
.pa-lp .pa-team .pa-img img{aspect-ratio:1/1;object-fit:cover;object-position:center top;border-radius:18px}
.pa-lp .pa-gallery .pa-img img{aspect-ratio:4/3;object-fit:cover;border-radius:14px}
.pa-lp .pa-gallery .pa-img{margin-bottom:16px !important}
.pa-lp .zones{list-style:none !important;display:flex;flex-wrap:wrap;gap:10px;justify-content:center;max-width:920px;margin:6px auto 0 !important;padding:0 !important}
.pa-lp .zones li{margin:0 !important;list-style:none !important}
.pa-lp .zones a{display:inline-block;background:#fff;border:1px solid var(--line) !important;border-radius:30px;padding:9px 18px;font-size:14.5px;font-weight:500;color:var(--navy) !important;transition:.2s}
.pa-lp .zones a:hover{border-color:var(--azure) !important;color:var(--azure-d) !important}
.pa-lp .pa-intro p{font-size:17px !important;line-height:1.8 !important;color:var(--body) !important;margin:0 0 14px !important}
.pa-lp .pa-intro a{color:var(--azure-d) !important;font-weight:600}
.pa-lp.pa-cta{background-image:url('""" + CTA_BG + """');background-size:cover;background-position:center center}
.pa-lp .pa-mini{padding:18px 18px !important;margin-bottom:12px !important}
.pa-lp .pa-mini .elementor-icon-box-wrapper{display:flex !important;gap:14px;align-items:flex-start;text-align:left !important}
.pa-lp .pa-mini .elementor-icon-box-icon{margin:0 !important;flex:0 0 auto}
.pa-lp .pa-mini .elementor-icon-box-title{font-size:16px !important;margin:2px 0 2px !important}
.pa-lp .pa-mini .elementor-icon-box-description{font-size:14px !important}
.pa-lp:not(.pa-intro-sec) .pa-title,.pa-lp:not(.pa-intro-sec) .pa-title .elementor-heading-title,.pa-lp:not(.pa-intro-sec) .pa-eyebrow{text-align:center !important}
.pa-lp .pa-sub a{color:var(--azure-d) !important;font-weight:600}
.pa-lp.pa-stats .pa-grid{width:100%}
.pa-lp.pa-stats .pa-btn{margin-top:18px !important}
@media(max-width:767px){.pa-lp .pa-stat .elementor-icon-box-title{font-size:26px !important}}
"""


def card_style(dark=False):
    return {"primary_color": AZURE, "title_color": "#FFFFFF" if dark else NAVY, "description_color": "#DCE9F4" if dark else "#5C7186"}


def build():
    b = B("accueil")
    W = b.w

    def btn(text, href, ic, kind="", ext=True, lib="fa-solid"):
        return W("button", {"text": text, "link": link(href, ext), "selected_icon": icon(ic, lib), "icon_indent": {"unit": "px", "size": 8},
                            "_element_width": "auto", "_element_width_mobile": "inherit"}, ("pa-btn " + kind).strip())

    def eyebrow(t, center=True):
        return W("heading", {"title": t, "header_size": "p", "align": "center" if center else "left"}, "pa-eyebrow")

    def title(t):
        return W("heading", {"title": t, "header_size": "h2", "align": "center"}, "pa-title")

    def sub(t):
        return W("text-editor", {"editor": f"<p>{t}</p>", "align": "center"}, "pa-sub")

    def card(ic, t, d, href=None, tag="h3", cls="pa-card", pos="top"):
        s = {"selected_icon": icon(ic), "title_text": t, "description_text": d, "title_size": tag, "position": pos, "text_align": "left"} | card_style()
        if href:
            s["link"] = link(href)
        return W("icon-box", s, cls)

    def grid(items, cols):
        """Reparte los widgets en `cols` columnas de una sección interior (orden de lectura correcto en móvil)."""
        per = -(-len(items) // cols)
        size = {2: 50, 3: 33, 4: 25}[cols]
        return b.sec([b.col(items[i * per:(i + 1) * per], size, inner=True) for i in range(cols)], "pa-grid", inner=True, gap="no",
                     content_width={"unit": "px", "size": 1140})

    def seccion(widgets, cls="", **st):
        base = dict(padding=pad(72, 24, 72, 24), padding_mobile=pad(54, 16, 54, 16))
        return b.sec([b.col(widgets)], ("pa-lp " + cls).strip(), **(base | st))

    S = []
    # 0 · estilos
    S.append(b.sec([b.col([W("html", {"html": "<style>\n" + CSS + CSS_HOME + "\n</style>"}, "pa-styles")])], "pa-lp pa-styles-sec"))
    # 1 · hero con vídeo de fondo (enlace de vídeo: no se importa a la biblioteca)
    S.append(b.sec([b.col([
        eyebrow("Physiothérapie à Ins (Anet) · Seeland"),
        W("heading", {"title": "Physio à Ins : cabinet de physiothérapie et soins à domicile", "header_size": "h1", "align": "center"}, "pa-h1"),
        W("heading", {"title": "Rämismatte 21, 3232 Ins · au cabinet ou à domicile · du lundi au vendredi jusqu'à 20h", "header_size": "div", "align": "center"}, "pa-ameta"),
        btn("Prendre rendez-vous", ONEDOC, "fas fa-calendar-check"),
        btn("WhatsApp", WA, "fab fa-whatsapp", "wa", lib="fa-brands"),
        W("heading", {"title": "★★★★★ 5,0 sur Google", "header_size": "div", "align": "center", "link": link(GBP, True)}, "pa-rating"),
    ], css="pa-center")], "pa-lp pa-hero pa-home-hero", layout="full_width", stretch_section="section-stretched",
        background_background="video", background_video_link=VIDEO, background_play_on_mobile="yes", background_color=NAVY,
        background_overlay_background="classic", background_overlay_color="#000000", background_overlay_opacity={"unit": "px", "size": 0.5},
        padding=pad(130, 24, 120, 24), padding_mobile=pad(90, 18, 80, 18)))
    # 2 · confianza (6 tarjetas)
    trust = [card("fas fa-calendar-check", "Rendez-vous rapide", "Dans la semaine dans la plupart des cas.", tag="div", cls="pa-card pa-mini", pos="left"),
             card("fas fa-clock", "Ouvert jusqu'à 20h", "Du lundi au vendredi, venez après le travail.", tag="div", cls="pa-card pa-mini", pos="left"),
             card("fas fa-shield-heart", "Toutes les assurances", "Cabinet reconnu par toutes les compagnies d'assurance maladie en Suisse.", tag="div", cls="pa-card pa-mini", pos="left"),
             card("fas fa-comments", "Équipe multilingue", "Français, allemand, anglais, espagnol et portugais.", tag="div", cls="pa-card pa-mini", pos="left"),
             card("fas fa-house-medical", "Au cabinet ou à domicile", "À Ins et dans toute la région des Trois-Lacs.", tag="div", cls="pa-card pa-mini", pos="left"),
             card("fas fa-dumbbell", "Fitness médical sur place", "Rééducation active sur les appareils de l'InsGym.", tag="div", cls="pa-card pa-mini", pos="left")]
    S.append(seccion([grid(trust, 3)], "pa-soft", padding=pad(48, 24, 36, 24), padding_mobile=pad(40, 16, 28, 16)))
    # 3 · texto SEO: el cabinet de Ins
    intro = ("<p>Physio Activa est votre <strong>cabinet de physiothérapie à Ins (Anet)</strong>, dans le Seeland, entre le lac de Morat, le lac de Neuchâtel et le lac de Bienne. "
             "Nos physiothérapeutes vous reçoivent à la Rämismatte 21, au 1er étage du bâtiment Lidl, dans les locaux de l'InsGym, avec un parking juste devant l'entrée.</p>"
             "<p>Vous cherchez un physio à Ins pour un mal de dos, une nuque raide, une épaule qui bloque, un genou opéré ou une entorse qui traîne ? "
             "Chaque prise en charge commence par un bilan, puis associe thérapie manuelle, exercices et, quand c'est utile, entraînement sur appareils "
             "(<a href=\"/fitness-medical/\">fitness médical</a>). Si vous ne pouvez pas vous déplacer, un physiothérapeute vient chez vous : "
             "<a href=\"/physiotherapeute-a-domicile/\">physiothérapie à domicile</a> à Ins, Morat, dans le Vully, à Chiètres, La Neuveville, Avenches, Bienne et Lyss.</p>"
             "<p>La physiothérapie à Ins se fait chez nous en français, en allemand, en anglais, en espagnol ou en portugais, du lundi au vendredi jusqu'à 20h. "
             "Découvrez <a href=\"/a-propos-de-nous/\">notre équipe</a> ou <a href=\"/nous-trouver/\">comment venir au cabinet</a>.</p>")
    S.append(seccion([eyebrow("Votre cabinet"), title("Votre cabinet de physiothérapie à Ins (Anet)"),
                      W("text-editor", {"editor": intro}, "pa-intro")], "pa-intro-sec", content_width={"unit": "px", "size": 860}))
    # 4 · soins (12, todos enlazados)
    soins = [("fas fa-hand-holding-medical", "Physiothérapie générale", "Douleurs, raideurs, suites d'accident : bilan, thérapie manuelle et exercices.", "/physio-generale/"),
             ("fas fa-house-medical", "Physio à domicile", "Vos séances chez vous, à Ins et dans la région des Trois-Lacs.", "/physiotherapeute-a-domicile/"),
             ("fas fa-dumbbell", "Fitness médical (MTT)", "Entraînement thérapeutique encadré pour retrouver force et confiance.", "/fitness-medical/"),
             ("fas fa-droplet", "Drainage lymphatique", "Technique manuelle douce en cas d'œdème ou de jambes lourdes.", "/drainage-lymphatique/"),
             ("fas fa-hands", "Massage thérapeutique", "Contractures, nuque, dos et récupération sportive.", "/massage-therapeutique/"),
             ("fas fa-person-running", "Physio du sport", "Blessure, tendinite et retour progressif à l'entraînement.", "/physio-du-sport/"),
             ("fas fa-bed-pulse", "Rééducation post-opératoire", "Après une prothèse de hanche ou de genou, une opération de l'épaule ou du genou.", "/physiotherapie-post-operatoire/"),
             ("fas fa-hand", "Thérapie manuelle", "Mobilisations articulaires et techniques des tissus mous, avec exercices.", "/therapie-manuelle/"),
             ("fas fa-syringe", "Dry needling", "Aiguille fine sans injection pour relâcher les points de tension.", "/physioactiva-puncture-seche/"),
             ("fas fa-brain", "Physio neurologique", "Rééducation après un AVC ou en cas de maladie neurologique.", "/physiotherapie-neurologique/"),
             ("fas fa-lungs", "Physio respiratoire", "Rééducation respiratoire et reprise progressive de l'effort.", "/physiotherapie-cardiorespiratoire/"),
             ("fas fa-person-pregnant", "Rééducation du périnée", "Grossesse, post-partum, incontinence, douleurs pelviennes.", "/physiotherapie-du-plancher-pelvien/")]
    S.append(seccion([eyebrow("Nos soins"), title("Nos soins de physiothérapie à Ins"),
                      sub("Une prise en charge complète, du cabinet à la salle de fitness, ou à domicile. Douleurs de la mâchoire : voir la <a href=\"/physiotemporo-mandibulaire-atm/\">physiothérapie ATM</a>."),
                      grid([card(*s) for s in soins], 3)], "pa-soft"))
    # 5 · ¿dónde le duele?
    dolor = [("fas fa-person-walking", "Mal de dos et lombalgie", "Lumbago, douleur lombaire aiguë ou qui dure.", "/mal-de-dos-lombaire/"),
             ("fas fa-bolt", "Sciatique et hernie discale", "Douleur qui descend dans la jambe.", "/mal-de-dos-lombaire/"),
             ("fas fa-user", "Douleur cervicale", "Nuque raide, torticolis, coup du lapin.", "/douleur-cervicale-au-cou/"),
             ("fas fa-hand-fist", "Douleur de l'épaule", "Coiffe des rotateurs, tendinite, capsulite.", "/lesions-de-lepaule/"),
             ("fas fa-bone", "Douleur du genou", "Ménisque, ligament croisé, arthrose, prothèse.", "/douleur-du-genou-lesions-de-la-cheville/"),
             ("fas fa-shoe-prints", "Pied et cheville", "Entorse, instabilité, tendinite d'Achille.", "/douleur-du-genou-lesions-de-la-cheville/")]
    S.append(seccion([eyebrow("Vos douleurs"), title("Où avez-vous mal ?"),
                      sub("Choisissez la zone douloureuse ou consultez notre <a href=\"/pour-les-patients/\">guide des pathologies traitées</a>."),
                      grid([card(*d, tag="div") for d in dolor], 3)], ""))
    # 6 · por qué (4 tarjetas, H3)
    why = [("fas fa-calendar-check", "Un rendez-vous rapide à Ins", "Quand on a mal, on ne veut pas attendre trois semaines. Dans la plupart des cas, nous vous proposons un créneau dans la semaine, et nos horaires jusqu'à 20h vous permettent de venir après le travail."),
           ("fas fa-dumbbell", "Une rééducation active", "Votre récupération ne s'arrête pas sur la table de traitement : nous vous guidons dans des exercices de renforcement, dans une salle spacieuse et équipée, pour traiter le problème à la source."),
           ("fas fa-house-medical", "Au cabinet ou à domicile", "Après une opération, une hospitalisation ou quand se déplacer est difficile, nos physiothérapeutes viennent chez vous à Ins et dans la région des Trois-Lacs."),
           ("fas fa-people-group", "Une équipe proche et multilingue", "Des physiothérapeutes diplômés, une prise en charge personnalisée dans un cadre calme, en français, en allemand, en anglais, en espagnol et en portugais.")]
    S.append(seccion([eyebrow("Notre approche"), title("Plus qu'un massage : un vrai plan de récupération"),
                      grid([card(*w) for w in why], 2), btn("Prendre rendez-vous", ONEDOC, "fas fa-calendar-check")], "pa-soft pa-center"))
    # 7 · galería (imágenes vacías: se eligen en Elementor)
    gal = [W("image", {"image": {"url": "", "id": "", "alt": a}, "image_size": "large"}, "pa-img") for a in
           ["Salle de traitement du cabinet Physio Activa à Ins", "Physiothérapeute de Physio Activa en séance à Ins",
            "Espace de fitness médical (MTT) à l'InsGym, Ins", "Entrée du cabinet Physio Activa, Rämismatte 21 à Ins"]]
    S.append(seccion([eyebrow("Le cabinet"), title("Un espace de soins et de mouvement à Ins"),
                      sub("Des salles de traitement modernes, une salle de fitness complète et un parking à disposition, à la Rämismatte 21."),
                      grid(gal, 2)], "pa-gallery", content_width={"unit": "px", "size": 980}))
    # 8 · equipo
    def miembro(nombre, rol, bio, alt):
        return [W("image", {"image": {"url": "", "id": "", "alt": alt}, "image_size": "large"}, "pa-img"),
                W("heading", {"title": nombre, "header_size": "h3"}, "pa-member-name"),
                W("text-editor", {"editor": f"<p><em>{rol}</em></p><p>{bio}</p>"}, "pa-text"),
                btn("Prendre rendez-vous", ONEDOC, "fas fa-calendar-check", "outline")]
    team = b.sec([b.col(miembro("Lucile Combes", "Physiothérapeute diplômée", "Une prise en charge complète et personnalisée, dans un cadre apaisant et à l'écoute.",
                                "Lucile Combes, physiothérapeute diplômée chez Physio Activa à Ins"), 50, inner=True),
                  b.col(miembro("Francisco Díaz", "Physiothérapeute diplômé", "Rigueur, écoute et empathie pour favoriser des progrès durables.",
                                "Francisco Díaz, physiothérapeute diplômé chez Physio Activa à Ins"), 50, inner=True)],
                 "pa-grid pa-team", inner=True, gap="extended", content_width={"unit": "px", "size": 860})
    S.append(seccion([eyebrow("Notre équipe"), title("Vos physiothérapeutes à Ins"),
                      sub("Découvrez leur parcours sur la page <a href=\"/a-propos-de-nous/\">À propos de nous</a>."), team], "pa-soft"))
    # 9 · cifras (banda azul marino)
    def stat(ic, big, lab, lib="fa-solid"):
        return W("icon-box", {"selected_icon": icon(ic, lib), "title_text": big, "description_text": lab, "title_size": "div", "position": "top",
                              "text_align": "center", "primary_color": AZURE, "title_color": "#FFFFFF", "description_color": "#DCE9F4"}, "pa-stat")
    S.append(seccion([grid([stat("fas fa-star", "5,0 ★", "Note moyenne sur Google"), stat("fas fa-language", "5 langues", "parlées au cabinet"),
                            stat("fas fa-clock", "20h", "ouvert en semaine"), stat("fas fa-house-medical", "Domicile", "dans les Trois-Lacs")], 4),
                      btn("Lire les avis sur Google", GBP, "fab fa-google", "ghost", lib="fa-brands")],
                     "pa-stats pa-center", background_background="classic", background_color=NAVY, padding=pad(56, 24, 56, 24)))
    # 10 · zonas (14 ciudades enlazadas)
    zonas = [("/physio-a-sugiez/", "Sugiez (Mont-Vully)"), ("/physio-a-la-neuveville/", "La Neuveville"), ("/physio-a-kerzers/", "Kerzers (Chiètres)"),
             ("/physio-a-morat/", "Morat (Murten)"), ("/physio-a-neuchatel/", "Neuchâtel"), ("/physio-a-avenches/", "Avenches"), ("/physio-a-lyss/", "Lyss"),
             ("/physio-a-bienne/", "Bienne (Biel)"), ("/physio-a-fribourg/", "Fribourg"), ("/physio-a-payerne/", "Payerne"),
             ("/physio-a-estavayer/", "Estavayer-le-Lac"), ("/physio-a-yvonand/", "Yvonand"), ("/physio-a-yverdon/", "Yverdon-les-Bains"), ("/physio-a-lausanne/", "Lausanne")]
    chips = '<ul class="zones">' + "".join(f'<li><a href="{u}">Physio à {n}</a></li>' for u, n in zonas) + "</ul>"
    S.append(seccion([eyebrow("Nos zones"), title("Votre physio dans le Seeland et les Trois-Lacs"),
                      sub("Un seul cabinet, à Ins (Anet), et des soins à domicile dans la région. Distance, accès et informations locales :"),
                      W("text-editor", {"editor": chips}, "pa-text")], ""))
    # 11 · seguros (frase aprobada por el cliente)
    S.append(seccion([eyebrow("Assurances"), title("Reconnus par toutes les assurances"),
                      sub("Notre cabinet est reconnu par toutes les compagnies d'assurance maladie en Suisse. Nous disposons de toutes les autorisations sanitaires nécessaires et accueillons les patients quel que soit leur canton de résidence.")],
                     "pa-soft", padding=pad(56, 24, 56, 24)))
    # 12 · FAQ (acordeón + FAQ Schema de Elementor)
    faq = [("Quand dois-je consulter un physiothérapeute ?", "Lorsqu'une douleur dure plus d'une semaine, limite vos mouvements, perturbe votre sommeil ou revient régulièrement, ou après un accident ou une opération. Plus on la prend en charge tôt, plus la récupération est simple. En cas de douleur très intense, de fièvre ou de perte de force, consultez d'abord un médecin."),
           ("Physio Activa travaille-t-il avec toutes les compagnies d'assurance ?", "Oui. Notre cabinet est reconnu par toutes les compagnies d'assurance maladie en Suisse. Nous disposons de toutes les autorisations sanitaires nécessaires et accueillons les patients quel que soit leur canton de résidence."),
           ("Combien de séances me faut-il ?", "La durée du traitement varie selon votre situation : une douleur récente évolue souvent plus vite qu'un problème installé depuis longtemps. Lors de la première visite, nous établissons avec vous une estimation adaptée à votre cas."),
           ("Où se trouve votre cabinet à Ins et y a-t-il un parking ?", "Notre cabinet se trouve à la Rämismatte 21, 3232 Ins (Anet), au 1er étage du bâtiment Lidl, au sein de l'InsGym. Un parking est à disposition devant le bâtiment."),
           ("Combien de temps faut-il pour obtenir un rendez-vous ?", "Dans la plupart des cas, dans la semaine. Nous recevons du lundi au vendredi jusqu'à 20h, pour que vous puissiez venir après le travail."),
           ("Proposez-vous des soins à domicile ?", "Oui, à Ins et dans la région des Trois-Lacs, notamment à Morat, dans le Vully, à Chiètres, La Neuveville, Avenches, Bienne et Lyss. Pour les autres localités, contactez-nous pour vérifier votre adresse."),
           ("Dans quelles langues pouvez-vous me recevoir ?", "Notre équipe vous reçoit en français, en allemand, en anglais, en espagnol et en portugais."),
           ("Quelle est la différence entre un kiné et un physiothérapeute ?", "C'est la même profession de santé. En France et en Belgique, on parle de kinésithérapeute ; en Suisse, le terme officiel est physiothérapeute."),
           ("Comment se passe une séance de physiothérapie ?", "La première séance commence par un entretien et un bilan (mobilité, force, posture). Nous définissons ensuite avec vous des objectifs et un plan de traitement, qui associe techniques manuelles et exercices que vous pourrez poursuivre chez vous."),
           ("Est-ce normal d'avoir plus mal après une séance ?", "Une sensation de courbature ou de fatigue musculaire passagère peut apparaître après des exercices nouveaux. Si la douleur est forte, inhabituelle ou dure plusieurs jours, signalez-le à votre physiothérapeute.")]
    from construir_nativo import eid
    tabs = [{"tab_title": q, "tab_content": f"<p>{a}</p>", "_id": eid("accueil", "faq", str(i))} for i, (q, a) in enumerate(faq)]
    S.append(seccion([eyebrow("Questions fréquentes"), title("Questions fréquentes sur la physio à Ins"),
                      W("accordion", {"tabs": tabs, "faq_schema": "yes", "title_html_tag": "h3", "icon_align": "right",
                                      "selected_icon": icon("fas fa-plus"), "selected_active_icon": icon("fas fa-minus")}, "pa-faq")],
                     "pa-faq-sec", content_width={"unit": "px", "size": 868}))
    # 13 · CTA con imagen de fondo (por CSS: sin duplicados en la biblioteca)
    S.append(b.sec([b.col([
        W("heading", {"title": "Besoin d'un physio à Ins ou dans les environs ?", "header_size": "h2", "align": "center"}, "pa-cta-title"),
        W("text-editor", {"editor": "<p>Au cabinet d'Ins ou à domicile, du lundi au vendredi jusqu'à 20h. Dans la plupart des cas, nous vous proposons un rendez-vous dans la semaine.</p>", "align": "center"}, "pa-cta-sub"),
        btn("Prendre rendez-vous", ONEDOC, "fas fa-calendar-check"), btn("WhatsApp", WA, "fab fa-whatsapp", "wa", lib="fa-brands"),
        btn("Appelez-nous · 076 627 38 38", "tel:+41766273838", "fas fa-phone", "ghost", ext=False),
    ], css="pa-center")], "pa-lp pa-cta", layout="full_width", stretch_section="section-stretched",
        background_background="classic", background_color=NAVY, background_position="center center", background_size="cover",
        background_overlay_background="classic", background_overlay_color=NAVY, background_overlay_opacity={"unit": "px", "size": 0.86},
        padding=pad(88, 24, 88, 24), padding_mobile=pad(64, 16, 64, 16)))
    # 14 · mapa
    S.append(b.sec([b.col([W("google_maps", {"address": "Physio Activa, Rämismatte 21, 3232 Ins", "zoom": {"unit": "px", "size": 16},
                                             "height": {"unit": "px", "size": 480}, "height_mobile": {"unit": "px", "size": 380}}, "pa-map")])],
                   "pa-lp pa-map-sec", layout="full_width", stretch_section="section-stretched"))
    # 15 · botón WhatsApp + schema local con el MISMO @id que la Organization de Yoast (Google une ambos nodos)
    ld = {"@context": "https://schema.org", "@graph": [{
        "@type": "Physiotherapy", "@id": SITE + "/#organization", "name": "Physio Activa", "url": SITE + "/",
        "logo": UP + "2026/06/Physio-Activa-Logo00001.png", "image": UP + "2025/06/Centerbild_IMG_9184-scaled-1.jpg",
        "description": "Cabinet de physiothérapie à Ins (Anet), Seeland : soins au cabinet et à domicile dans la région des Trois-Lacs.",
        "telephone": "+41 76 627 38 38", "email": "physio@physioactiva.ch",
        "address": {"@type": "PostalAddress", "streetAddress": "Rämismatte 21", "postalCode": "3232", "addressLocality": "Ins", "addressRegion": "BE", "addressCountry": "CH"},
        "geo": {"@type": "GeoCoordinates", "latitude": CLI["geo"]["lat"], "longitude": CLI["geo"]["lng"]}, "hasMap": GBP,
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:30", "closes": "20:00"}],
        "availableLanguage": ["fr", "de", "en", "es", "pt"],
        "areaServed": [{"@type": "Place", "name": n} for n in ["Ins", "Seeland", "Morat", "Mont-Vully", "Kerzers", "La Neuveville", "Neuchâtel", "Avenches", "Lyss", "Bienne"]],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1], "url": SITE + s[3]}} for s in soins],
        "sameAs": ["https://www.instagram.com/physio_activa_/", "https://www.facebook.com/profile.php?id=100094154144954", GBP]}]}
    tail = (f'<a class="pa-wafab" href="{WA}" target="_blank" rel="noopener" aria-label="Contacter Physio Activa sur WhatsApp"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i></a>\n'
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    S.append(b.sec([b.col([W("html", {"html": tail}, "pa-tail")])], "pa-lp pa-tail-sec"))

    tpl = {"content": S, "page_settings": {"hide_title": "yes"}, "version": "0.4", "title": "Physio Activa · Accueil", "type": "page"}
    estilos_nativos(tpl)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "accueil.json").write_text(json.dumps(tpl, ensure_ascii=False, indent=1))
    with zipfile.ZipFile(OUT / "accueil.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(OUT / "accueil.json", "accueil.json")
    (OUT / "yoast.txt").write_text(
        f"Página: Accueil (portada; slug interno «accueil», URL pública https://physioactiva.ch/)\n"
        f"SEO title ({len(TITLE)}/60): {TITLE}\nMeta description ({len(META)}/155): {META}\nFocus keyphrase: physio Ins\n"
        f"Indexación: index, follow\nImportante: en el campo de título de Yoast, borra las variables «Séparateur» y «Titre du site».\n\n"
        "IMÁGENES (la plantilla se importa SIN imágenes para no duplicarlas; elígelas en Elementor):\n"
        + "".join(f"- {n}: {a}\n" for n, a in imgs_alt(tpl) if not n.startswith("Fondo"))
        + f"- Vídeo del hero: ya enlazado ({VIDEO}); no se importa a la biblioteca.\n"
          f"- Fondo del CTA final: {CTA_BG} (por CSS).\n- Imagen destacada / Open Graph de Yoast: foto del cabinet.\n")
    html = preview(tpl, {"title": TITLE, "meta": META}).replace(
        "</style>", ".elementor-col-33{width:33.333%}.elementor-col-25{width:25%}@media(max-width:767px){.elementor-col-33,.elementor-col-25{width:100%!important}}</style>", 1)
    (OUT / "preview.html").write_text(html)
    return tpl


if __name__ == "__main__":
    t = build()
    print("secciones", len(t["content"]))
