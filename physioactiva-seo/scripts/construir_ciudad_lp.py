"""Páginas de ciudad con el diseño «pa-lp» del cliente (hero con foto de la ciudad, migas, ficha, artículo, pourquoi,
FAQ, CTA, mapa, botón flotante). Un único elementor.json por ciudad con CSS + HTML + JS + JSON-LD dentro.
Uso: python3 scripts/construir_ciudad_lp.py
Salida: entregables/9_ciudades/<slug>/{elementor.json, preview.html, yoast.txt}
"""
import json, re, sys, pathlib, hashlib, html as H, copy, yaml, markdown
from urllib.parse import quote
from bs4 import BeautifulSoup, Tag

BASE = pathlib.Path(__file__).resolve().parent.parent
PAG = BASE / "entregables/5_paginas"
OUT = BASE / "entregables/9_ciudades"
CSS = (BASE / "plantillas/pa-lp.css").read_text()
CLI = yaml.safe_load((BASE / "config/cliente.yml").read_text())
ZON = yaml.safe_load((BASE / "config/zonas.yml").read_text())
IMGS = {}
fimg = BASE / "data/imagenes_ciudades.json"
if fimg.exists():
    for x in json.loads(fimg.read_text()):
        IMGS[x["town"].lower()] = x
TPL = json.loads((BASE / "plantillas/lombaire-elementor.json").read_text())
SITE = "https://physioactiva.ch"
UP = "https://physioactiva.ch/wp-content/uploads/"
ONEDOC = CLI["onedoc_url"]
DOMICILE = {"sugiez", "la-neuveville", "chietres", "morat", "neuchatel", "avenches", "lyss", "bienne"}
TOWN_KEY = {"sugiez": "sugiez", "la-neuveville": "la neuveville", "chietres": "kerzers", "morat": "murten", "neuchatel": "neuchâtel",
            "avenches": "avenches", "lyss": "lyss", "bienne": "biel/bienne", "fribourg": "fribourg", "payerne": "payerne",
            "estavayer": "estavayer-le-lac", "yvonand": "yvonand", "yverdon": "yverdon-les-bains", "lausanne": "lausanne"}
ICON_WHY = ["fa-shield-heart", "fa-house-medical", "fa-clipboard-list", "fa-calendar-check"]
SOINS = [  # (url, título, descripción, claves de demanda local)
    ("/physio-generale/", "Physiothérapie générale", "Douleurs, raideurs et gênes du quotidien.", ""),
    ("/physiotherapeute-a-domicile/", "Physiothérapie à domicile", "Les séances chez vous quand se déplacer est difficile.", "domicile"),
    ("/drainage-lymphatique/", "Drainage lymphatique", "Œdèmes, jambes lourdes, suites opératoires.", "drainage"),
    ("/mal-de-dos-lombaire/", "Mal de dos et lombalgie", "Lumbago, douleurs en position assise, rechutes.", ""),
    ("/sciatique-hernie-discale/", "Sciatique et hernie discale", "Douleur qui descend dans la jambe.", ""),
    ("/douleur-cervicale-au-cou/", "Douleur cervicale", "Nuque raide, torticolis, travail de bureau.", ""),
    ("/lesions-de-lepaule/", "Douleur de l'épaule", "Coiffe des rotateurs, tendinite, capsulite.", ""),
    ("/douleur-du-genou-lesions-de-la-cheville/", "Genou", "Ménisque, ligament croisé, arthrose, prothèse.", ""),
    ("/physiotherapie-post-operatoire/", "Physiothérapie post-opératoire", "Rééducation après une prothèse ou une chirurgie.", ""),
    ("/physio-du-sport/", "Physiothérapie du sport", "Blessures, surcharge et retour à l'entraînement.", "sport"),
    ("/medical-training-therapy-mtt/", "Fitness médical (MTT)", "Entraînement thérapeutique encadré à l'InsGym.", ""),
    ("/massage-therapeutique/", "Massage thérapeutique", "Contractures et tensions musculaires.", "massage"),
]
esc = lambda s: H.escape(s, quote=True)


def texto(t):
    return " ".join(t.get_text(" ", strip=True).split())


def inline(tag):
    s = "".join(str(c) for c in tag.contents).strip()
    s = re.sub(r"</?code>", "", s)
    def fix(m):
        h = H.unescape(m.group(1))
        if h.startswith(SITE):
            h = h[len(SITE):] or "/"
        if h.startswith("/") and not h.endswith("/") and "." not in h.split("/")[-1]:
            h += "/"
        return f'<a class="inlink" href="{esc(h)}">'
    return re.sub(r'<a href="([^"]+)">', fix, s)


def parse(md):
    meta = yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", md, re.S).group(1))
    body = md[re.match(r"^---\n.*?\n---\n", md, re.S).end():]
    body = re.split(r"^## Notes pour l'équipe \(ES\)", body, flags=re.M)[0]
    body = re.sub(r"\s*`?\[(?:À CONFIRMER|POR CONFIRMAR)[^\]]*\]`?", "", body)  # seguridad: ningún marcador en la web
    soup = BeautifulSoup(markdown.markdown(body, extensions=["extra", "sane_lists"]), "html.parser")
    h1, intro, secs, cur = None, [], [], None
    for el in soup.children:
        if not isinstance(el, Tag):
            continue
        if el.name == "h1":
            h1 = el; continue
        if el.name == "h2":
            cur = {"h2": el, "b": []}; secs.append(cur); continue
        (cur["b"] if cur else intro).append(el)
    return meta, h1, intro, secs


def bloques_html(bl):
    out = []
    for b in bl:
        if b.name == "p":
            out.append(f"<p>{inline(b)}</p>")
        elif b.name in ("ul", "ol"):
            out.append('<ul class="plain">' + "".join(f"<li>{inline(li)}</li>" for li in b.find_all("li", recursive=False)) + "</ul>")
        elif b.name == "h3":
            out.append(f"<h3>{inline(b)}</h3>")
    return "\n   ".join(out)


def subs(bl):
    res, cur = [], None
    for b in bl:
        if b.name == "h3":
            cur = {"h3": b, "c": []}; res.append(cur)
        elif cur:
            cur["c"].append(b)
    return res


def eid(*p):
    return hashlib.sha1("|".join(p).encode()).hexdigest()[:7]


def build(key):
    z = ZON[key]
    slug = f"physio-a-{key}"
    url = z["url"]
    ville, vtitre = z["nom_fr"], z["nom_titre"]
    meta, h1, intro, secs = parse((PAG / slug / "fr.md").read_text())
    h1t = texto(h1)
    wa = CLI["whatsapp_href"] + "?text=" + quote(f"Bonjour, je souhaite prendre rendez-vous chez Physio Activa (physio à {ville}).")
    # imagen de la ciudad
    if key == "neuchatel":
        img = {"url": UP + "2026/09/Neuchatel-physio.jpg", "author": None}
    else:
        img = IMGS.get(TOWN_KEY[key]) or IMGS.get(ville.lower()) or {"url": UP + "2025/06/Centerbild_IMG_9184-scaled-1.jpg", "author": None}
    credit = ""
    if img.get("author"):
        credit = (f'<span class="photo-credit">Photo : {esc(img["author"])}, <a href="{esc(img["file_page"])}" target="_blank" rel="noopener nofollow">'
                  f'{esc(img["license"])}</a>, via Wikimedia Commons</span>')
    # secciones
    why = next((s for s in secs if re.search(r"essentiel", texto(s["h2"]), re.I)), None)
    faq = next((s for s in secs if re.match(r"questions fréquentes", texto(s["h2"]), re.I)), None)
    cta = secs[-1] if secs and secs[-1] is not faq else None
    cuerpo = [s for s in secs if s not in (why, faq, cta)]
    domicile = key in DOMICILE
    vois = z["localites_voisines"]
    km = str(z["km_depuis_ins"]).replace(".", ",")
    route = f"https://www.google.com/maps/dir/?api=1&origin={quote(ville + ', Suisse')}&destination={quote('Physio Activa, Rämismatte 21, 3232 Ins')}"
    intro_html = " ".join(inline(b) for b in intro if b.name == "p")
    fiche_rows = [
        ("Cabinet", "Rämismatte 21, 3232 Ins (1er étage du bâtiment Lidl, InsGym), parking à disposition"),
        (f"Depuis {ville}", f"Environ {km} km à vol d'oiseau jusqu'au cabinet d'Ins"),
        ("À domicile", (f"{ville} et environs ({', '.join(vois)})" if domicile else
                        f"Selon votre adresse ({', '.join(vois)}) : contactez-nous pour le vérifier")),
        ("Délai", "Rendez-vous dans la semaine dans la plupart des cas"),
        ("Horaires", "Du lundi au vendredi, jusqu'à 20h"),
        ("Langues", "Français, allemand, anglais, espagnol et portugais"),
        ("Assurances", "Cabinet reconnu par toutes les compagnies d'assurance maladie en Suisse"),
        ("Réservation", "En ligne (OneDoc), par WhatsApp ou au 076 627 38 38"),
    ]
    fiche = ('<div class="fiche">\n    <table>\n     <caption>' + esc(f"Physio Activa pour les patients de {ville}, en bref") + "</caption>\n     <tbody>\n"
             + "".join(f'      <tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td></tr>\n' for a, b in fiche_rows) + "     </tbody>\n    </table>\n   </div>")
    locales = {s[1].split(" ")[0] for s in []}
    brief = json.loads((BASE / "data/z_briefs_local.json").read_text()).get(key, {})
    demanda = " ".join(k for _, k, _ in brief.get("services_locaux", []))
    soins = sorted(SOINS, key=lambda s: (0 if (s[3] and s[3] in demanda) else 1, SOINS.index(s)))[:10]
    soins_html = ('<ul class="soins-list">' + "".join(f'<li><a href="{u}"><strong>{esc(t)}</strong><span>{esc(d)}</span></a></li>' for u, t, d, _ in soins) + "</ul>")
    art = []
    for i, s in enumerate(cuerpo):
        h2t = texto(s["h2"])
        art.append(f"<h2>{inline(s['h2'])}</h2>\n   " + bloques_html(s["b"]))
        if i == 0:
            art.append(f'<div class="inline-actions"><a class="btn outline" href="{esc(route)}" target="_blank" rel="noopener"><i class="fa-solid fa-route" aria-hidden="true"></i> <span>Itinéraire depuis {esc(ville)}</span></a></div>\n'
                       f'   <figure>\n    <img src="{UP}2025/04/Physio-Activa-00031.jpg" alt="{esc(f"Physiothérapeute de Physio Activa en séance, physio pour les patients de {ville}")}" width="1200" height="675" loading="lazy" decoding="async">\n   </figure>')
        if re.search(r"domicile", h2t, re.I):
            art.append(f"<h2>{esc(f'Nos soins de physiothérapie pour les patients de {ville}')}</h2>\n   <p>Vous avez accès à l'ensemble de nos soins, au cabinet d'Ins ou à domicile selon votre situation. Les plus demandés :</p>\n   {soins_html}")
            art.append(f'<div class="cta-inline">\n    <p>{esc(f"Vous habitez {ville} et vous avez mal ? Nous vous proposons un rendez-vous dans la semaine dans la plupart des cas, au cabinet d’Ins ou " + ("chez vous." if domicile else "à domicile selon votre adresse."))}</p>\n'
                       f'    <a class="btn" href="{ONEDOC}" target="_blank" rel="noopener"><i class="fa-solid fa-calendar-check" aria-hidden="true"></i> <span>Rendez-vous online</span></a>\n   </div>')
        if re.search(r"déroule", h2t, re.I):
            art.append(f'<figure>\n    <img src="{UP}2025/04/Physio-Activa-00036.jpg" alt="{esc(f"Salle de traitement du cabinet Physio Activa à Ins, proche de {ville}")}" width="1200" height="675" loading="lazy" decoding="async">\n   </figure>')
    why_cards = ""
    if why:
        for j, sb in enumerate(subs(why["b"])):
            why_cards += (f'<div class="wcard"><div class="wic" aria-hidden="true"><i class="fa-solid {ICON_WHY[j % 4]}"></i></div><h3>{inline(sb["h3"])}</h3>'
                          + "".join(f"<p>{inline(c)}</p>" for c in sb["c"] if c.name == "p") + "</div>")
    faqs = []
    if faq:
        for sb in subs(faq["b"]):
            a_html = " ".join(inline(c) for c in sb["c"] if c.name == "p")
            a_txt = " ".join(texto(c) for c in sb["c"] if c.name == "p")
            faqs.append((texto(sb["h3"]), a_html, a_txt))
    faq_html = "".join(
        f'<div class="faq{" open" if i == 0 else ""}"><h3><button type="button" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="faq-a{i+1}"><span class="faq-q">{esc(q)}</span>'
        f'<span class="q-ic" aria-hidden="true"><i class="fa-solid fa-plus"></i></span></button></h3><div class="ans" id="faq-a{i+1}"><p>{a}</p></div></div>'
        for i, (q, a, _) in enumerate(faqs))
    cta_h2 = texto(cta["h2"]) if cta else f"Besoin d'un physio à {ville} ou dans les environs ?"
    cta_s1 = " ".join(texto(b) for b in (cta["b"] if cta else []) if b.name == "p") or f"Au cabinet d'Ins ou à domicile. Du lundi au vendredi, jusqu'à 20h."
    full = SITE + url
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Physiotherapy", "@id": SITE + "/#physiotherapy", "name": "Physio Activa", "url": SITE + "/",
         "logo": UP + "2026/06/Physio-Activa-Logo00001.png", "image": UP + "2025/04/Physio-Activa-00031.jpg",
         "telephone": "+41 76 627 38 38", "email": "physio@physioactiva.ch",
         "address": {"@type": "PostalAddress", "streetAddress": "Rämismatte 21", "postalCode": "3232", "addressLocality": "Ins", "addressRegion": "BE", "addressCountry": "CH"},
         "geo": {"@type": "GeoCoordinates", "latitude": CLI["geo"]["lat"], "longitude": CLI["geo"]["lng"]},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:30", "closes": "20:00"}],
         "areaServed": [{"@type": "City", "name": z["commune"], "sameAs": z["source_publique"]}] + [{"@type": "Place", "name": v} for v in vois] + [{"@type": "Place", "name": "Ins"}],
         "availableLanguage": ["fr", "de", "en", "es", "pt"],
         "sameAs": ["https://www.instagram.com/physio_activa_/", "https://www.facebook.com/profile.php?id=100094154144954", "https://www.google.com/maps?cid=17004812906479027083"]},
        {"@type": "WebPage", "@id": full + "#webpage", "url": full, "name": meta["title"], "description": meta["meta"], "inLanguage": "fr-CH",
         "about": {"@id": full + "#service"}, "primaryImageOfPage": {"@type": "ImageObject", "url": img["url"]}},
        {"@type": "Service", "@id": full + "#service", "name": f"Physiothérapie à {ville}", "serviceType": "Physiothérapie au cabinet et à domicile",
         "provider": {"@id": SITE + "/#physiotherapy"},
         "areaServed": {"@type": "City", "name": z["commune"], "containedInPlace": {"@type": "AdministrativeArea", "name": f"Canton de {z['canton']}"}}},
        {"@type": "FAQPage", "@id": full + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, _, t in faqs]}]}
    ld_tag = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    markup = f"""<div class="pa-lp">

<!-- ===== HERO ===== -->
<section class="art-hero-sec" style="background-image:url('{img['url']}')">
  <div class="art-hero-overlay" aria-hidden="true"></div>
  <div class="art-hero">
    <span class="eyebrow">Physiothérapie · {esc(vtitre)}</span>
    <h1>{esc(h1t)}</h1>
    <div class="ameta">Par l'équipe Physio Activa · Physiothérapie à {esc(ville)}</div>
    <div class="hero-cta"><a class="btn" href="{ONEDOC}" target="_blank" rel="noopener"><i class="fa-solid fa-calendar-check" aria-hidden="true"></i> <span>Rendez-vous online</span></a><a class="btn wa" href="{esc(wa)}" target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i> <span>WhatsApp</span></a></div>
  </div>
  {credit}
</section>

<!-- ===== BREADCRUMB ===== -->
<nav class="crumbs" aria-label="Fil d'Ariane">
  <ol><li><a href="/">Accueil</a></li><li aria-current="page">Physiothérapie à {esc(ville)}</li></ol>
</nav>

<!-- ===== ARTICLE ===== -->
<section class="sec">
 <div class="wrap">
  <article class="article">
   <p class="lead-intro">{intro_html}</p>

   {fiche}

   {chr(10).join('   ' + a for a in art)}
  </article>
 </div>
</section>

<!-- ===== POURQUOI ===== -->
<section class="sec soft">
 <div class="wrap">
  <div class="sec-head reveal">
   <span class="eyebrow">Pourquoi Physio Activa</span>
   <h2 class="title">{esc(f"Pourquoi les patients de {ville} choisissent Physio Activa")}</h2>
   <p>Un cabinet de physiothérapie à Ins, des soins à domicile dans la région et une équipe qui vous reçoit en cinq langues.</p>
  </div>
  <div class="why-grid reveal">{why_cards}</div>
 </div>
</section>

<!-- ===== FAQ ===== -->
<section class="sec">
 <div class="wrap">
  <div class="sec-head">
   <span class="eyebrow">Questions fréquentes</span>
   <h2 class="title">{esc(texto(faq["h2"]) if faq else f"Questions fréquentes sur la physio à {ville}")}</h2>
  </div>
  <div class="faq-list" id="paFaq">{faq_html}</div>
 </div>
</section>

<!-- ===== CTA BAND ===== -->
<section class="cta-band">
 <div class="wrap reveal">
  <h2>{esc(cta_h2)}</h2>
  <p class="s1">{esc(cta_s1)}</p>
  <div class="cta-actions"><a class="btn" href="{ONEDOC}" target="_blank" rel="noopener"><i class="fa-solid fa-calendar-check" aria-hidden="true"></i> <span>Rendez-vous online</span></a><a class="btn wa" href="{esc(wa)}" target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i> <span>WhatsApp</span></a><a class="btn ghost" href="tel:+41766273838"><i class="fa-solid fa-phone" aria-hidden="true"></i> <span>Appelez-nous · 076 627 38 38</span></a></div>
 </div>
</section>

<!-- ===== MAP ===== -->
<section class="map">
 <iframe src="https://maps.google.com/maps?q=Physio%20Activa%2C%20R%C3%A4mismatte%2021%2C%203232%20Ins&amp;z=17&amp;hl=fr&amp;output=embed" title="Physio Activa — Rämismatte 21, 3232 Ins" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe>
</section>

<a class="pa-wafab" href="{esc(wa)}" target="_blank" rel="noopener" aria-label="Contacter Physio Activa sur WhatsApp"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i></a>

</div>"""
    script = """<script>
(function(){
  function safe(fn,n){try{fn()}catch(e){console.warn(n,e)}}
  function initReveal(){
    var els=document.querySelectorAll('.pa-lp .reveal');
    if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});return;}
    var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}})},{threshold:0.05});
    els.forEach(function(e){io.observe(e)});
    setTimeout(function(){els.forEach(function(e){e.classList.add('in')})},6000);
  }
  function initFAQ(){
    var l=document.getElementById('paFaq'); if(!l)return;
    var items=l.querySelectorAll('.faq');
    items.forEach(function(d){
      var btn=d.querySelector('button'),ans=d.querySelector('.ans');
      if(d.classList.contains('open'))ans.style.maxHeight=ans.scrollHeight+'px';
      btn.addEventListener('click',function(){
        var open=d.classList.contains('open');
        items.forEach(function(x){x.classList.remove('open');x.querySelector('.ans').style.maxHeight=null;x.querySelector('button').setAttribute('aria-expanded','false');});
        if(!open){d.classList.add('open');ans.style.maxHeight=ans.scrollHeight+'px';btn.setAttribute('aria-expanded','true');}
      });
    });
  }
  function boot(){var root=document.querySelector('.pa-lp'); if(root)root.classList.add('is-js');safe(initReveal,'reveal');safe(initFAQ,'faq');}
  if(document.readyState!=='loading'){boot();}else{document.addEventListener('DOMContentLoaded',boot);}
})();
</script>"""
    widget = "<style>\n" + CSS + "\n</style>\n\n" + markup + "\n\n" + script + "\n" + ld_tag + "\n"
    t = copy.deepcopy(TPL)
    sec = t["content"][0]; col = sec["elements"][0]; w = col["elements"][0]
    sec["id"], col["id"], w["id"] = eid(slug, "lp-section"), eid(slug, "lp-column"), eid(slug, "lp-widget")
    w["settings"]["html"] = widget
    t["title"] = h1t
    t["page_settings"] = {"hide_title": "yes"}
    d = OUT / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "elementor.json").write_text(json.dumps(t, ensure_ascii=False))
    (d / "yoast.txt").write_text(f"SEO title ({len(meta['title'])}/60): {meta['title']}\nMeta description ({len(meta['meta'])}/155): {meta['meta']}\n"
                                 f"Slug: {url}\nFocus keyphrase: {meta['keyword_principal']}\nH1: {h1t}\nIndexación: index, follow\n"
                                 f"Imagen destacada / Open Graph: {img['url']}\n")
    (d / "preview.html").write_text(f'<!doctype html><html lang="fr-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                                    f'<title>{esc(meta["title"])}</title><meta name="description" content="{esc(meta["meta"])}"></head><body style="margin:0">\n{widget}</body></html>')
    return {"slug": slug, "url": url, "title": meta["title"], "lt": len(meta["title"]), "lm": len(meta["meta"]), "faq": len(faqs),
            "img": img["url"], "palabras": len(BeautifulSoup(markup, "html.parser").get_text(" ").split())}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    res = [build(k) for k in ZON]
    (OUT / "_lote.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    for r in res:
        print(r["slug"], r["lt"], r["lm"], "faq", r["faq"], "palabras", r["palabras"], r["img"][-50:])
