// ════════════════════════════════════════════════════════════
//  Matheux — dev local : lecture du schéma SQL documenté
//  Source : supabase/schema.sql, puis supabase/fix_schema.sql, puis supabase/migrations/*.sql
//  (ordre alphabétique). On n'exécute pas le SQL : on en extrait seulement ce dont le faux
//  PostgREST a besoin (colonnes, types, défauts, NOT NULL, clés primaires, contraintes uniques).
//  Le schéma documenté fait foi : une colonne utilisée par index.ts mais absente ici = écart à corriger.
// ════════════════════════════════════════════════════════════

export type Col = { name: string; type: string; notNull: boolean; def: string | null; identity: boolean };
export type Table = { name: string; cols: Record<string, Col>; order: string[]; pk: string[]; uniques: string[][]; updatedAtTrigger: boolean };
export type Schema = Record<string, Table>;

function splitTopLevel(s: string, sep = ","): string[] {
  const out: string[] = [];
  let depth = 0, cur = "", q = false;
  for (const ch of s) {
    if (ch === "'") q = !q;
    if (!q && ch === "(") depth++;
    if (!q && ch === ")") depth--;
    if (!q && depth === 0 && ch === sep) { out.push(cur); cur = ""; continue; }
    cur += ch;
  }
  if (cur.trim()) out.push(cur);
  return out;
}

function stripComments(sql: string): string {
  return sql.split("\n").map((l) => {
    let q = false;
    for (let i = 0; i < l.length - 1; i++) {
      if (l[i] === "'") q = !q;
      if (!q && l[i] === "-" && l[i + 1] === "-") return l.slice(0, i);
    }
    return l;
  }).join("\n");
}

const TYPE_RE = /^(bigint|integer|int|smallint|real|numeric(\([^)]*\))?|double precision|boolean|date|timestamptz|timestamp|uuid|jsonb|json|text\[\]|text|char\(\d+\)|varchar(\(\d+\))?)/i;

function parseColumn(def: string): Col | null {
  const m = def.trim().match(/^"?([a-z_][a-z0-9_]*)"?\s+(.*)$/is);
  if (!m) return null;
  const name = m[1].toLowerCase();
  if (["primary", "unique", "constraint", "check", "foreign"].includes(name)) return null;
  const rest = m[2];
  const tm = rest.match(TYPE_RE);
  const type = tm ? tm[1].toLowerCase().replace(/\(.*\)/, "") : "text";
  const identity = /generated\s+(always|by default)\s+as\s+identity/i.test(rest);
  const pk = /primary\s+key/i.test(rest);
  const notNull = /not\s+null/i.test(rest) || pk;
  // défaut : tout ce qui suit « default » jusqu'au prochain mot-clé de contrainte
  let d: string | null = null;
  const dm = rest.match(/\bdefault\s+(.+?)(\s+(not\s+null|null|primary\s+key|unique|check|references|constraint)\b|$)/is);
  if (dm) d = dm[1].trim();
  return { name, type: type === "int" ? "integer" : type, notNull, def: d, identity };
}

export function parseSchema(sqlTexts: string[]): Schema {
  const schema: Schema = {};
  for (const raw of sqlTexts) {
    const sql = stripComments(raw);
    // create table [if not exists] name ( ... );
    const reTable = /create\s+table\s+(?:if\s+not\s+exists\s+)?([a-z_][a-z0-9_]*)\s*\(([\s\S]*?)\);/gi;
    for (const m of sql.matchAll(reTable)) {
      const name = m[1].toLowerCase();
      if (schema[name]) continue; // « if not exists »
      const t: Table = { name, cols: {}, order: [], pk: [], uniques: [], updatedAtTrigger: false };
      for (const part of splitTopLevel(m[2])) {
        const p = part.trim();
        const tpk = p.match(/^primary\s+key\s*\(([^)]*)\)/i);
        if (tpk) { t.pk = tpk[1].split(",").map((x) => x.trim().toLowerCase()); continue; }
        const tun = p.match(/^(?:constraint\s+\w+\s+)?unique\s*\(([^)]*)\)/i);
        if (tun) { t.uniques.push(tun[1].split(",").map((x) => x.trim().toLowerCase())); continue; }
        const c = parseColumn(p);
        if (!c) continue;
        t.cols[c.name] = c;
        t.order.push(c.name);
        if (/primary\s+key/i.test(p)) t.pk = [c.name];
        else if (/\bunique\b/i.test(p)) t.uniques.push([c.name]);
      }
      schema[name] = t;
    }
    // alter table X add column [if not exists] c type ...;
    for (const m of sql.matchAll(/alter\s+table\s+([a-z_]+)\s+add\s+column\s+(?:if\s+not\s+exists\s+)?([^;]+);/gi)) {
      const t = schema[m[1].toLowerCase()];
      const c = parseColumn(m[2]);
      if (t && c && !t.cols[c.name]) { t.cols[c.name] = c; t.order.push(c.name); if (/\bunique\b/i.test(m[2])) t.uniques.push([c.name]); }
    }
    // alter table X rename column a to b;
    for (const m of sql.matchAll(/alter\s+table\s+([a-z_]+)\s+rename\s+column\s+([a-z_0-9]+)\s+to\s+([a-z_0-9]+)\s*;/gi)) {
      const t = schema[m[1].toLowerCase()];
      const a = m[2].toLowerCase(), b = m[3].toLowerCase();
      if (t && t.cols[a] && !t.cols[b]) { t.cols[b] = { ...t.cols[a], name: b }; delete t.cols[a]; t.order = t.order.map((x) => (x === a ? b : x)); }
    }
    // index uniques (drop puis create : on suit l'ordre des fichiers)
    for (const m of sql.matchAll(/(drop\s+index\s+(?:if\s+exists\s+)?([a-z_0-9]+)\s*;)|(create\s+unique\s+index\s+(?:if\s+not\s+exists\s+)?([a-z_0-9]+)\s+on\s+([a-z_]+)\s*\(([^)]*)\)([^;]*);)/gi)) {
      if (m[1]) {
        const idx = m[2].toLowerCase();
        for (const t of Object.values(schema)) t.uniques = t.uniques.filter((u) => (u as unknown as { idx?: string }).idx !== idx);
      } else {
        const t = schema[m[5].toLowerCase()];
        if (!t) continue;
        const cols = m[6].split(",").map((x) => x.trim().toLowerCase()) as string[] & { idx?: string };
        cols.idx = m[4].toLowerCase();
        if (/\bwhere\b/i.test(m[7])) continue; // index partiel : non utilisable comme cible ON CONFLICT simple
        t.uniques = t.uniques.filter((u) => (u as unknown as { idx?: string }).idx !== cols.idx);
        t.uniques.push(cols);
      }
    }
    for (const m of sql.matchAll(/create\s+trigger\s+\w+\s+before\s+update\s+on\s+([a-z_]+)[^;]*update_updated_at/gi)) {
      const t = schema[m[1].toLowerCase()];
      if (t) t.updatedAtTrigger = true;
    }
  }
  return schema;
}

export async function loadSchema(root: string): Promise<Schema> {
  const files = [`${root}/supabase/schema.sql`, `${root}/supabase/fix_schema.sql`];
  const migs: string[] = [];
  for await (const e of Deno.readDir(`${root}/supabase/migrations`)) if (e.name.endsWith(".sql")) migs.push(e.name);
  migs.sort();
  files.push(...migs.map((f) => `${root}/supabase/migrations/${f}`));
  const texts: string[] = [];
  for (const f of files) { try { texts.push(await Deno.readTextFile(f)); } catch { /* fichier absent */ } }
  return parseSchema(texts);
}
