"""Rastreo propio (gratuito) de las URLs del sitemap de physioactiva.ch.
Extrae status, title, meta description, H1-H3, canonical, robots, schema y nº de palabras.
Salida: data/site/paginas.json y data/site/html/<slug>.html
"""
import json, re, subprocess, pathlib, html as H
from concurrent.futures import ThreadPoolExecutor

BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "data/site"
(OUT / "html").mkdir(parents=True, exist_ok=True)


def fetch(url):
    r = subprocess.run(["curl", "-sS", "-L", "-A", "Mozilla/5.0 (physioactiva-seo-audit)",
                        "-w", "\n__STATUS__%{http_code}__%{url_effective}__%{num_redirects}", url],
                       capture_output=True, text=True, timeout=60)
    body, _, tail = r.stdout.rpartition("\n__STATUS__")
    code, eff, nred = tail.strip("_").split("__")[:3]
    return body, int(code), eff, int(nred)


def txt(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", H.unescape(s)).strip()


def meta(body, name):
    m = re.search(r'<meta[^>]+(?:name|property)=["\']%s["\'][^>]*content=["\']([^"\']*)' % re.escape(name), body, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+(?:name|property)=["\']%s["\']' % re.escape(name), body, re.I)
    return H.unescape(m.group(1)).strip() if m else ""


def parse(url):
    body, code, eff, nred = fetch(url)
    slug = url.rstrip("/").split("/")[-1] or "home"
    (OUT / "html" / f"{slug}.html").write_text(body)
    main = re.sub(r"<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>", " ", body, flags=re.S | re.I)
    hs = {f"h{i}": [txt(x) for x in re.findall(rf"<h{i}[^>]*>(.*?)</h{i}>", main, re.S | re.I)] for i in (1, 2, 3)}
    can = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', body, re.I)
    ld = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', body, re.S | re.I)
    types = set()
    for blk in ld:
        types.update(re.findall(r'"@type"\s*:\s*"([^"]+)"', blk))
    lang = re.search(r'<html[^>]+lang=["\']([^"\']+)', body, re.I)
    words = len(txt(main).split())
    links = re.findall(r'href=["\'](https?://physioactiva\.ch[^"\'#?]*)', main)
    return {
        "url": url, "slug": slug, "status": code, "url_final": eff, "redirecciones": nred,
        "title": H.unescape(re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I).group(1)).strip() if "<title" in body else "",
        "meta_description": meta(body, "description"), "robots": meta(body, "robots"),
        "canonical": can.group(1) if can else "", "lang": lang.group(1) if lang else "",
        **hs, "schema_types": sorted(types), "palabras": words,
        "enlaces_internos": sorted(set(l.rstrip("/") + "/" for l in links)),
        "tel_whatsapp_onedoc": {"tel": "tel:" in body, "whatsapp": "wa.me" in body or "whatsapp" in body.lower(),
                                "onedoc": "onedoc" in body.lower()},
    }


if __name__ == "__main__":
    urls = [u.strip() for u in (OUT / "urls.txt").read_text().split() if u.strip()]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(parse, urls))
    (OUT / "paginas.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    for p in res:
        print(p["status"], p["slug"][:38].ljust(38), "| H1:", (p["h1"] or ["—"])[0][:50], "| W", p["palabras"])
