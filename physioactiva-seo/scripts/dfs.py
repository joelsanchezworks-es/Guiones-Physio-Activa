"""Cliente DataForSEO v3 con caché, registro de costes y techo de gasto.
Credenciales: en la nube las inyecta el proxy; en local, variables DATAFORSEO_LOGIN/DATAFORSEO_USERNAME y
DATAFORSEO_PASSWORD (o .env). Nunca se imprimen.
"""
import json, os, hashlib, datetime, pathlib, csv, base64, urllib.request, yaml, threading

BASE = pathlib.Path(__file__).resolve().parent.parent
HOY = datetime.date.today().isoformat()
_lock = threading.Lock()
LIM = yaml.safe_load((BASE / "config/limites.yml").read_text())
UMB = yaml.safe_load((BASE / "config/umbrales.yml").read_text())
COSTES = BASE / "data/costes.csv"


def _env():
    envf = BASE / ".env"
    if envf.exists():
        for line in envf.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    u = os.environ.get("DATAFORSEO_LOGIN") or os.environ.get("DATAFORSEO_USERNAME")
    p = os.environ.get("DATAFORSEO_PASSWORD")
    return (u, p) if u and p else None


def gasto_ejecucion(run_id):
    if not COSTES.exists():
        return 0.0
    with COSTES.open() as f:
        return sum(float(r["coste_usd"]) for r in csv.DictReader(f) if r["ejecucion"] == run_id)


def _ttl(endpoint):
    fam = endpoint.split("/")[0]
    return UMB["cache_ttl_dias"].get(fam, 7)


def _cache_lookup(endpoint, h):
    ttl = _ttl(endpoint)
    if ttl <= 0:
        return None
    for d in sorted((BASE / "data/cache").glob("*"), reverse=True):
        try:
            age = (datetime.date.today() - datetime.date.fromisoformat(d.name)).days
        except ValueError:
            continue
        if age > ttl:
            continue
        f = d / endpoint.replace("/", "__") / f"{h}.json"
        if f.exists():
            return json.loads(f.read_text())
    return None


RUN_ID = os.environ.get("SEO_RUN_ID", HOY)


def call(endpoint, payload, method="POST", estimate=0.05):
    """endpoint sin /v3/, payload = lista de tareas. Devuelve el JSON completo."""
    body = json.dumps(payload, sort_keys=True, ensure_ascii=False) if payload is not None else ""
    h = hashlib.sha1((method + endpoint + body).encode()).hexdigest()[:16]
    hit = _cache_lookup(endpoint, h)
    if hit is not None:
        return hit
    with _lock:
        g = gasto_ejecucion(RUN_ID)
        if g + estimate > LIM["techo_usd_ejecucion"]:
            raise SystemExit(f"TECHO DE GASTO: acumulado {g:.3f} + estimado {estimate:.3f} > {LIM['techo_usd_ejecucion']} USD")
    req = urllib.request.Request("https://api.dataforseo.com/v3/" + endpoint, method=method,
                                 data=body.encode() if method == "POST" else None,
                                 headers={"Content-Type": "application/json"})
    cred = _env()
    if cred:
        req.add_header("Authorization", "Basic " + base64.b64encode(f"{cred[0]}:{cred[1]}".encode()).decode())
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    cost = float(data.get("cost") or 0)
    with _lock:
        new = not COSTES.exists()
        with COSTES.open("a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["fecha", "ejecucion", "endpoint", "hash", "coste_usd", "status", "tareas"])
            w.writerow([datetime.datetime.now().isoformat(timespec="seconds"), RUN_ID, endpoint, h, f"{cost:.5f}",
                        data.get("status_code"), len(payload or [])])
    d = BASE / "data/cache" / HOY / endpoint.replace("/", "__")
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{h}.json").write_text(json.dumps(data, ensure_ascii=False))
    raw = BASE / "data/raw" / HOY
    raw.mkdir(parents=True, exist_ok=True)
    (raw / f"{endpoint.replace('/', '__')}__{h}.json").write_text(json.dumps(data, ensure_ascii=False))
    return data


def results(data):
    out = []
    for t in data.get("tasks") or []:
        if t.get("status_code") != 20000:
            out.append({"__error__": t.get("status_message"), "__data__": t.get("data")})
            continue
        out.extend(t.get("result") or [])
    return out
