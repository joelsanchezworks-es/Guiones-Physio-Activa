// Prepara public/data/ para el visor estático (public/index.html).
// - Copia cada guion JSON ("tipo": "guion") y cada documento .md de salidas/ a public/data/.
// - Escribe public/data/index.json con { items: [...] }, de más reciente a más antiguo.
// Sin dependencias: node tools/build-visor.mjs
import { readdirSync, readFileSync, writeFileSync, mkdirSync, rmSync, statSync, existsSync } from "node:fs";
import { join, relative, dirname, basename, extname, sep } from "node:path";
import { execSync } from "node:child_process";

const ROOT = process.cwd();
const SRC = join(ROOT, "salidas");
const OUT = join(ROOT, "public", "data");
const FECHA = /^\d{4}-\d{2}-\d{2}$/;
const ANGULOS = ["A", "B", "C", "D", "E", "F"];
const BLOQUES = { ads: ["Gancho", "Problema", "Solución", "Prueba", "CTA"], organico: ["Gancho", "Valor", "CTA"] };

const warn = (file, msg) => console.warn(`⚠️  ${file}: ${msg}`);
const words = (s) => String(s || "").split(/\s+/).filter((w) => /[\p{L}\p{N}]/u.test(w)).length;

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    if (name.startsWith(".")) continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}

// Devuelve la lista de errores (el guion se omite) y avisa de los límites (el guion se publica igual).
function validate(g, file) {
  const errors = [];
  const need = (cond, msg) => { if (!cond) errors.push(msg); };
  need(g && typeof g === "object", "no es un objeto");
  if (errors.length) return errors;
  for (const k of ["id", "fecha", "titulo", "tema", "angulo", "uso", "duracion", "publico", "localizacion", "quien_sale"])
    need(typeof g[k] === "string" && g[k].trim(), `falta "${k}"`);
  need(FECHA.test(g.fecha || ""), `"fecha" debe ser AAAA-MM-DD`);
  need(ANGULOS.includes(g.angulo), `"angulo" debe ser una letra de A a F`);
  need(["ads", "organico"].includes(g.uso), `"uso" debe ser "ads" u "organico"`);
  const langs = Array.isArray(g.idiomas) ? g.idiomas : [];
  need(langs.length > 0 && langs.every((l) => ["fr", "de"].includes(l)), `"idiomas" debe ser ["fr"], ["de"] o ["fr", "de"]`);
  const hasLangs = (obj, where) => {
    if (!obj || typeof obj !== "object") return errors.push(`${where}: falta`);
    for (const l of langs) if (typeof obj[l] !== "string" || !obj[l].trim()) errors.push(`${where}: falta "${l}"`);
  };

  need(Array.isArray(g.hooks) && g.hooks.length === 5, "tiene que haber exactamente 5 hooks");
  const hooks = Array.isArray(g.hooks) ? g.hooks : [];
  need(hooks.filter((h) => h && h.recomendado === true).length === 1, `exactamente un hook con "recomendado": true`);
  hooks.forEach((h, i) => {
    const w = `hooks[${i}]`;
    if (!h || typeof h !== "object") return errors.push(`${w}: no es un objeto`);
    for (const k of ["id", "tipo", "visual", "hipotesis"]) need(typeof h[k] === "string" && h[k].trim(), `${w}: falta "${k}"`);
    hasLangs(h.verbal, `${w}.verbal`);
    hasLangs(h.texto, `${w}.texto`);
    for (const l of langs) {
      if (words(h.verbal?.[l]) > 12) warn(file, `${h.id || w} verbal ${l.toUpperCase()} tiene ${words(h.verbal[l])} palabras (máx. 12)`);
      if (words(h.texto?.[l]) > 6) warn(file, `${h.id || w} texto ${l.toUpperCase()} tiene ${words(h.texto[l])} palabras (máx. 6)`);
    }
  });

  need(Array.isArray(g.guion) && g.guion.length > 0, `"guion" debe tener al menos un bloque`);
  (Array.isArray(g.guion) ? g.guion : []).forEach((b, i) => {
    const w = `guion[${i}]`;
    if (!b || typeof b !== "object") return errors.push(`${w}: no es un objeto`);
    for (const k of ["tiempo", "bloque", "visual"]) need(typeof b[k] === "string" && b[k].trim(), `${w}: falta "${k}"`);
    if (BLOQUES[g.uso] && b.bloque && !BLOQUES[g.uso].includes(b.bloque))
      errors.push(`${w}: "bloque" debe ser ${BLOQUES[g.uso].join(", ")}`);
    hasLangs(b.dice, `${w}.dice`);
    hasLangs(b.texto, `${w}.texto`);
  });

  if (!g.copy || typeof g.copy !== "object") errors.push(`falta "copy"`);
  else for (const l of langs) {
    const c = g.copy[l];
    if (!c || typeof c !== "object") { errors.push(`copy: falta "${l}"`); continue; }
    if (g.uso === "ads") {
      for (const k of ["corto", "largo", "titular", "descripcion"]) need(typeof c[k] === "string" && c[k].trim(), `copy.${l}: falta "${k}"`);
      if ((c.corto || "").length > 125) warn(file, `copy.${l}.corto tiene ${c.corto.length} caracteres (máx. 125)`);
      if ((c.titular || "").length > 40) warn(file, `copy.${l}.titular tiene ${c.titular.length} caracteres (máx. 40)`);
    } else {
      need(typeof c.post === "string" && c.post.trim(), `copy.${l}: falta "post"`);
      need(Array.isArray(c.hashtags), `copy.${l}: "hashtags" debe ser una lista`);
    }
  }
  // El español ("es") es una traducción de referencia para el equipo: opcional, pero recomendada.
  const sinEs = [
    ...hooks.flatMap((h, i) => [[h?.verbal, `hooks[${i}].verbal`], [h?.texto, `hooks[${i}].texto`]]),
    ...(Array.isArray(g.guion) ? g.guion : []).flatMap((b, i) => [[b?.dice, `guion[${i}].dice`], [b?.texto, `guion[${i}].texto`]]),
  ].filter(([o]) => o && typeof o === "object" && !(typeof o.es === "string" && o.es.trim())).map(([, w]) => w);
  if (sinEs.length) warn(file, `sin traducción "es" en ${sinEs.length} texto(s) (p. ej. ${sinEs[0]})`);
  if (g.copy && typeof g.copy === "object" && !g.copy.es) warn(file, `sin traducción "es" en "copy"`);

  need(Array.isArray(g.notas), `"notas" debe ser una lista`);
  need(Array.isArray(g.pendientes), `"pendientes" debe ser una lista`);
  return errors;
}

function folderDate(relPath) {
  const parts = relPath.split(sep);
  return parts.find((p) => FECHA.test(p)) || null;
}

// Repositorio y rama, para que el visor pueda abrir la pantalla de borrado de GitHub.
// Repo: campo "repository" de package.json. Rama: la que está publicando Cloudflare Pages
// (CF_PAGES_BRANCH) o, en local, la rama actual de git.
function config() {
  let repo = "", branch = process.env.CF_PAGES_BRANCH || "";
  try { repo = JSON.parse(readFileSync(join(ROOT, "package.json"), "utf8")).repository || ""; } catch {}
  repo = String(repo).replace(/^github:/, "").replace(/^https:\/\/github\.com\//, "").replace(/\.git$/, "");
  if (!branch) {
    try { branch = execSync("git rev-parse --abbrev-ref HEAD", { stdio: ["ignore", "pipe", "ignore"] }).toString().trim(); } catch {}
  }
  return { repo, branch: branch === "HEAD" ? "" : branch };
}

function main() {
  rmSync(OUT, { recursive: true, force: true });
  mkdirSync(OUT, { recursive: true });
  if (!existsSync(SRC)) {
    writeFileSync(join(OUT, "index.json"), JSON.stringify({ items: [] }));
    console.log("No existe salidas/: índice vacío.");
    return;
  }

  const files = walk(SRC);
  const jsonStems = new Set();
  const items = [];
  let omitted = 0;

  for (const abs of files.filter((f) => extname(f) === ".json")) {
    const rel = relative(SRC, abs);
    let g;
    try {
      g = JSON.parse(readFileSync(abs, "utf8"));
    } catch (e) {
      warn(rel, `JSON no válido (${e.message}). Se omite.`);
      omitted++;
      continue;
    }
    if (g?.tipo !== "guion") continue;
    const errors = validate(g, rel);
    if (errors.length) {
      warn(rel, `formato no válido, se omite:\n     - ${errors.join("\n     - ")}`);
      omitted++;
      continue;
    }
    if (items.some((it) => it.id === g.id)) {
      warn(rel, `id "${g.id}" repetido. Se omite.`);
      omitted++;
      continue;
    }
    const file = rel.split(sep).join("/");
    mkdirSync(dirname(join(OUT, rel)), { recursive: true });
    writeFileSync(join(OUT, rel), JSON.stringify(g));
    jsonStems.add(join(dirname(abs), basename(abs, ".json")));
    // Archivos del repo que forman este guion (el .json y, si existe, el .md con el mismo nombre).
    const twin = join(dirname(abs), basename(abs, ".json") + ".md");
    const repoFiles = [abs, ...(existsSync(twin) ? [twin] : [])].map((f) => relative(ROOT, f).split(sep).join("/"));
    items.push({
      kind: "guion", id: g.id, file, fecha: g.fecha, titulo: g.titulo, tema: g.tema,
      uso: g.uso, angulo: g.angulo, duracion: g.duracion, idiomas: g.idiomas, repoFiles,
    });
  }

  for (const abs of files.filter((f) => extname(f) === ".md")) {
    // Si el mismo guion existe ya como JSON, el .md no se lista para no duplicarlo.
    if (jsonStems.has(join(dirname(abs), basename(abs, ".md")))) continue;
    const rel = relative(SRC, abs);
    const text = readFileSync(abs, "utf8");
    const m = text.match(/^#\s+(.+)$/m);
    const file = rel.split(sep).join("/");
    mkdirSync(dirname(join(OUT, rel)), { recursive: true });
    writeFileSync(join(OUT, rel), text);
    items.push({
      kind: "doc", id: "doc/" + file.replace(/\.md$/, ""), file,
      fecha: folderDate(rel), titulo: m ? m[1].trim() : basename(abs, ".md"),
      repoFiles: [relative(ROOT, abs).split(sep).join("/")],
    });
  }

  items.sort((a, b) =>
    (b.fecha || "").localeCompare(a.fecha || "") ||
    (a.kind === b.kind ? 0 : a.kind === "guion" ? -1 : 1) ||
    a.file.localeCompare(b.file));
  writeFileSync(join(OUT, "index.json"), JSON.stringify({ generado: new Date().toISOString(), items }, null, 1));
  writeFileSync(join(OUT, "config.json"), JSON.stringify(config()));

  const n = items.filter((i) => i.kind === "guion").length;
  console.log(`Visor: ${n} guion(es) y ${items.length - n} documento(s) en public/data/index.json${omitted ? ` · ${omitted} omitido(s)` : ""}.`);
}

main();
