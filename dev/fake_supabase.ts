// ════════════════════════════════════════════════════════════
//  Matheux — faux Supabase en mémoire (PostgREST + GoTrue minimal) pour le dev local
//  Couvre EXACTEMENT le sous-ensemble utilisé par supabase/functions/api/index.ts :
//   REST  : GET/HEAD (select colonnes, filtres eq/neq/gt/gte/lt/lte/is/like/ilike/in/not/or,
//           order, limit, offset, count=exact, single/maybeSingle), POST insert/upsert
//           (on_conflict, merge/ignore-duplicates, return=representation), PATCH, DELETE.
//   AUTH  : admin listUsers/createUser/updateUserById, token?grant_type=password|refresh_token,
//           recover (mail de réinitialisation → outbox), user, logout.
//  Fidélité volontaire (pour attraper les bugs avant la prod) : colonne inconnue → erreur
//  PGRST204/42703, NOT NULL → 23502, doublon → 23505, on_conflict sans contrainte unique
//  correspondante → 42P10, requête REST portant le JWT d'un élève → 401 DEV_RLS.
//  Données persistées dans dev/data/db.json.
// ════════════════════════════════════════════════════════════
import type { Schema, Table, Col } from "./schema.ts";

type Row = Record<string, unknown>;
export type AuthUser = { id: string; email: string; pwd: string; created_at: string; email_confirmed_at: string | null };
export type DbState = { tables: Record<string, Row[]>; seq: Record<string, number>; users: AuthUser[] };

const enc = new TextEncoder();
const b64url = (b: Uint8Array | string) => {
  const bytes = typeof b === "string" ? enc.encode(b) : b;
  let s = ""; for (const x of bytes) s += String.fromCharCode(x);
  return btoa(s).replace(/=+$/, "").replace(/\+/g, "-").replace(/\//g, "_");
};
async function sha256hex(s: string) {
  const h = await crypto.subtle.digest("SHA-256", enc.encode(s));
  return Array.from(new Uint8Array(h)).map((x) => x.toString(16).padStart(2, "0")).join("");
}
export async function signJwt(payload: Record<string, unknown>, secret: string) {
  const head = b64url(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const body = b64url(JSON.stringify(payload));
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = new Uint8Array(await crypto.subtle.sign("HMAC", key, enc.encode(head + "." + body)));
  return head + "." + body + "." + b64url(sig);
}
function jwtPayload(tok: string): Record<string, unknown> | null {
  try { return JSON.parse(atob(tok.split(".")[1].replace(/-/g, "+").replace(/_/g, "/"))); } catch { return null; }
}

function todayParis() { return new Date().toLocaleDateString("sv-SE", { timeZone: "Europe/Paris" }); }
function pgNow() { return new Date().toISOString().replace("Z", "+00:00"); }

function jres(body: unknown, status = 200, headers: Record<string, string> = {}) {
  return new Response(body === null ? null : JSON.stringify(body), { status, headers: { "Content-Type": "application/json", ...headers } });
}
function pgErr(status: number, code: string, message: string, details: string | null = null, hint: string | null = null) {
  return jres({ code, details, hint, message }, status);
}
class PgError extends Error { constructor(public status: number, public code: string, msg: string, public details: string | null = null) { super(msg); } }

// ── Types ──
const INT = new Set(["bigint", "integer", "smallint"]);
const NUM = new Set(["real", "numeric", "double precision"]);
function coerce(col: Col, v: unknown): unknown {
  if (v === null || v === undefined) return null;
  const t = col.type;
  if (INT.has(t) || NUM.has(t)) {
    const n = typeof v === "number" ? v : Number(v);
    if (!Number.isFinite(n)) throw new PgError(400, "22P02", `invalid input syntax for type ${t}: "${v}"`);
    return INT.has(t) ? Math.trunc(n) : n;
  }
  if (t === "boolean") {
    if (typeof v === "boolean") return v;
    if (v === "true" || v === "t") return true;
    if (v === "false" || v === "f") return false;
    throw new PgError(400, "22P02", `invalid input syntax for type boolean: "${v}"`);
  }
  if (t === "date") {
    const s = String(v);
    if (!/^\d{4}-\d{2}-\d{2}/.test(s)) throw new PgError(400, "22007", `invalid input syntax for type date: "${s}"`);
    return s.slice(0, 10);
  }
  if (t === "timestamptz" || t === "timestamp") {
    const d = new Date(String(v));
    if (isNaN(d.getTime())) throw new PgError(400, "22007", `invalid input syntax for type timestamp with time zone: "${v}"`);
    return d.toISOString().replace("Z", "+00:00");
  }
  if (t === "jsonb" || t === "json") return typeof v === "string" ? (() => { try { return JSON.parse(v); } catch { return v; } })() : v;
  if (t === "text[]") {
    if (Array.isArray(v)) return v.map(String);
    throw new PgError(400, "22P02", `malformed array literal: "${v}"`);
  }
  if (typeof v === "object") return JSON.stringify(v);
  return String(v);
}

function evalDefault(col: Col, seqNext: () => number): unknown {
  if (col.identity) return seqNext();
  const d = col.def;
  if (d === null) return null;
  const s = d.trim().toLowerCase();
  if (s === "now()") return pgNow();
  if (s === "current_date") return todayParis();
  if (s === "gen_random_uuid()") return crypto.randomUUID();
  const iv = s.match(/^now\(\)\s*\+\s*interval\s*'(\d+)\s*days?'$/);
  if (iv) return new Date(Date.now() + Number(iv[1]) * 86400000).toISOString().replace("Z", "+00:00");
  if (s === "true" || s === "false") return s === "true";
  if (/^-?\d+(\.\d+)?$/.test(s)) return Number(s);
  const q = d.trim().match(/^'(.*)'(::\w+)?$/s);
  if (q) {
    const inner = q[1];
    if (col.type === "text[]") return inner.replace(/^\{|\}$/g, "").split(",").filter(Boolean);
    if (col.type === "jsonb") return JSON.parse(inner);
    return inner;
  }
  return null;
}

// ── Comparaison ──
function cmpVal(col: Col | undefined, a: unknown, b: unknown): number {
  if (a === null || a === undefined) return b === null || b === undefined ? 0 : 1; // NULL = +∞ (comme Postgres)
  if (b === null || b === undefined) return -1;
  if (col && (INT.has(col.type) || NUM.has(col.type))) return Number(a) - Number(b);
  if (col && (col.type === "timestamptz" || col.type === "timestamp")) return new Date(String(a)).getTime() - new Date(String(b)).getTime();
  if (col && col.type === "boolean") return Number(a) - Number(b);
  const x = String(a), y = String(b);
  return x < y ? -1 : x > y ? 1 : 0;
}

function unquote(s: string) {
  s = s.trim();
  if (s.length >= 2 && s.startsWith('"') && s.endsWith('"')) return s.slice(1, -1).replace(/\\(.)/g, "$1");
  return s;
}
function splitList(s: string): string[] {
  const out: string[] = []; let depth = 0, q = false, cur = "";
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (ch === "\\" && q) { cur += ch + (s[i + 1] ?? ""); i++; continue; }
    if (ch === '"') q = !q;
    if (!q && ch === "(") depth++;
    if (!q && ch === ")") depth--;
    if (!q && depth === 0 && ch === ",") { out.push(cur); cur = ""; continue; }
    cur += ch;
  }
  if (cur !== "") out.push(cur);
  return out;
}

type Pred = (r: Row) => boolean;

function likeRe(pat: string, ci: boolean) {
  const esc = pat.replace(/[.+?^${}()|[\]\\]/g, "\\$&").replace(/[*%]/g, ".*").replace(/_/g, ".");
  return new RegExp("^" + esc + "$", ci ? "is" : "s");
}

function opPred(t: Table, colName: string, expr: string): Pred {
  const col = t.cols[colName];
  if (!col) throw new PgError(400, "42703", `column ${t.name}.${colName} does not exist`);
  let neg = false;
  if (expr.startsWith("not.")) { neg = true; expr = expr.slice(4); }
  const dot = expr.indexOf(".");
  if (dot < 0) throw new PgError(400, "PGRST100", `"failed to parse filter (${expr})"`);
  const op = expr.slice(0, dot), rawV = expr.slice(dot + 1);
  let p: Pred;
  if (op === "is") {
    const v = rawV.toLowerCase();
    p = v === "null" ? (r) => r[colName] === null || r[colName] === undefined
      : v === "true" ? (r) => r[colName] === true : v === "false" ? (r) => r[colName] === false
      : (() => { throw new PgError(400, "PGRST100", `invalid is value ${rawV}`); })();
  } else if (op === "in") {
    const inner = rawV.replace(/^\(/, "").replace(/\)$/, "");
    const vals = splitList(inner).map(unquote).map((v) => coerce(col, v));
    p = (r) => vals.some((v) => r[colName] !== null && r[colName] !== undefined && cmpVal(col, r[colName], v) === 0);
  } else if (op === "like" || op === "ilike") {
    const re = likeRe(unquote(rawV), op === "ilike");
    p = (r) => r[colName] !== null && r[colName] !== undefined && re.test(String(r[colName]));
  } else {
    const v = coerce(col, unquote(rawV));
    const nn = (r: Row) => r[colName] !== null && r[colName] !== undefined;
    const c = (r: Row) => cmpVal(col, r[colName], v);
    const ops: Record<string, Pred> = {
      eq: (r) => nn(r) && c(r) === 0, neq: (r) => nn(r) && c(r) !== 0,
      gt: (r) => nn(r) && c(r) > 0, gte: (r) => nn(r) && c(r) >= 0,
      lt: (r) => nn(r) && c(r) < 0, lte: (r) => nn(r) && c(r) <= 0,
    };
    if (!ops[op]) throw new PgError(400, "PGRST100", `opérateur non géré par le faux PostgREST : ${op}`);
    p = ops[op];
  }
  return neg ? (r) => !p(r) : p;
}

function logicPred(t: Table, kind: "or" | "and", inner: string): Pred {
  const parts = splitList(inner.replace(/^\(/, "").replace(/\)$/, "")).map((s) => s.trim());
  const preds = parts.map((part): Pred => {
    let neg = false, s = part;
    if (s.startsWith("not.")) { neg = true; s = s.slice(4); }
    const m = s.match(/^(and|or)(\(.*\))$/s);
    let p: Pred;
    if (m) p = logicPred(t, m[1] as "or" | "and", m[2]);
    else { const d = s.indexOf("."); p = opPred(t, s.slice(0, d), s.slice(d + 1)); }
    return neg ? (r) => !p(r) : p;
  });
  return kind === "or" ? (r) => preds.some((p) => p(r)) : (r) => preds.every((p) => p(r));
}

const RESERVED = new Set(["select", "order", "limit", "offset", "on_conflict", "columns"]);
function buildFilter(t: Table, params: URLSearchParams): Pred {
  const preds: Pred[] = [];
  for (const [k, v] of params) {
    if (RESERVED.has(k)) continue;
    if (k === "or" || k === "and") preds.push(logicPred(t, k, v));
    else if (k === "not.or" || k === "not.and") { const p = logicPred(t, k.slice(4) as "or", v); preds.push((r) => !p(r)); }
    else preds.push(opPred(t, k, v));
  }
  return (r) => preds.every((p) => p(r));
}

function project(t: Table, rows: Row[], select: string | null): Row[] {
  const sel = (select ?? "*").trim();
  if (sel === "*" || sel === "") return rows.map((r) => { const o: Row = {}; for (const c of t.order) o[c] = r[c] ?? null; return o; });
  const fields = splitList(sel).map((f) => {
    if (f.includes("(")) throw new PgError(400, "PGRST200", `ressources imbriquées non gérées par le faux PostgREST : ${f}`);
    let alias: string | null = null, name = f;
    const ci = f.indexOf(":");
    if (ci > 0 && f[ci + 1] !== ":") { alias = f.slice(0, ci); name = f.slice(ci + 1); }
    name = name.split("::")[0];
    if (name !== "*" && !t.cols[name]) throw new PgError(400, "42703", `column ${t.name}.${name} does not exist`);
    return { name, alias: alias || name };
  });
  return rows.map((r) => {
    const o: Row = {};
    for (const f of fields) {
      if (f.name === "*") for (const c of t.order) o[c] = r[c] ?? null;
      else o[f.alias] = r[f.name] ?? null;
    }
    return o;
  });
}

function sortRows(t: Table, rows: Row[], order: string | null) {
  if (!order) return rows;
  const keys = order.split(",").map((s) => {
    const [c, ...mods] = s.split(".");
    if (!t.cols[c]) throw new PgError(400, "42703", `column ${t.name}.${c} does not exist`);
    const desc = mods.includes("desc");
    const nullsFirst = mods.includes("nullsfirst") ? true : mods.includes("nullslast") ? false : desc;
    return { c, desc, nullsFirst };
  });
  return rows.slice().sort((a, b) => {
    for (const k of keys) {
      const an = a[k.c] === null || a[k.c] === undefined, bn = b[k.c] === null || b[k.c] === undefined;
      if (an || bn) { if (an && bn) continue; return (an ? -1 : 1) * (k.nullsFirst ? 1 : -1); }
      const d = cmpVal(t.cols[k.c], a[k.c], b[k.c]);
      if (d !== 0) return k.desc ? -d : d;
    }
    return 0;
  });
}

// ════════════════════════════════════════════════════════════
export class FakeSupabase {
  state: DbState = { tables: {}, seq: {}, users: [] };
  userTokens = new Set<string>();
  private saveTimer: number | null = null;
  log: (m: string) => void = (m) => console.log(m);
  onEmail: (to: string, subject: string, html: string) => Promise<void> = async () => {};

  constructor(public schema: Schema, public file: string | null, public jwtSecret: string, public serviceKey: string, public publicUrl: string) {
    for (const t of Object.keys(schema)) this.state.tables[t] = [];
  }

  load(): boolean {
    if (!this.file) return false;
    try {
      const s = JSON.parse(Deno.readTextFileSync(this.file)) as DbState;
      this.state = { tables: s.tables || {}, seq: s.seq || {}, users: s.users || [] };
      for (const t of Object.keys(this.schema)) this.state.tables[t] ||= [];
      return true;
    } catch { return false; }
  }
  resetEmpty() { this.state = { tables: {}, seq: {}, users: [] }; for (const t of Object.keys(this.schema)) this.state.tables[t] = []; this.userTokens.clear(); this.scheduleSave(); }
  scheduleSave() {
    if (!this.file) return;
    if (this.saveTimer !== null) return;
    this.saveTimer = setTimeout(() => { this.saveTimer = null; this.saveNow(); }, 300);
  }
  saveNow() {
    if (!this.file) return;
    if (this.saveTimer !== null) { clearTimeout(this.saveTimer); this.saveTimer = null; }
    const tmp = this.file + ".tmp";
    Deno.writeTextFileSync(tmp, JSON.stringify(this.state));
    Deno.renameSync(tmp, this.file);
  }
  rows(table: string): Row[] { return this.state.tables[table] || []; }
  private nextSeq(table: string) { this.state.seq[table] = (this.state.seq[table] || 0) + 1; return this.state.seq[table]; }

  async handle(req: Request): Promise<Response> {
    const url = new URL(req.url);
    try {
      if (url.pathname.startsWith("/rest/v1/")) return await this.rest(req, url);
      if (url.pathname.startsWith("/auth/v1/")) return await this.auth(req, url);
      return pgErr(404, "DEV404", "faux Supabase : route non gérée " + url.pathname);
    } catch (e) {
      if (e instanceof PgError) return pgErr(e.status, e.code, e.message, e.details);
      console.error("[fake-supabase]", e);
      return pgErr(500, "DEV500", String(e));
    }
  }

  // ── PostgREST ─────────────────────────────────────────────
  private checkKey(req: Request) {
    const bearer = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
    if (bearer && bearer !== this.serviceKey) {
      const p = jwtPayload(bearer);
      if (p && p.role === "authenticated")
        throw new PgError(401, "DEV_RLS", "[dev] requête PostgREST avec le JWT d'un élève (" + p.email + ") au lieu de la clé service_role : en prod, la RLS s'appliquerait. Le client admin a probablement été « connecté » par auth.signInWithPassword.");
      throw new PgError(401, "PGRST301", "JWT invalide");
    }
  }

  private async rest(req: Request, url: URL): Promise<Response> {
    this.checkKey(req);
    const name = url.pathname.slice("/rest/v1/".length);
    if (name.startsWith("rpc/")) throw new PgError(404, "PGRST202", "faux PostgREST : aucune fonction rpc définie (" + name + ")");
    const t = this.schema[name];
    if (!t) throw new PgError(404, "PGRST205", `Could not find the table 'public.${name}' in the schema cache`);
    const prefer = (req.headers.get("prefer") || "").split(",").map((s) => s.trim());
    const params = url.searchParams;
    const accept = req.headers.get("accept") || "";
    const wantsObject = accept.includes("vnd.pgrst.object");
    const repr = prefer.includes("return=representation");
    const all = this.rows(name);

    const finish = (rows: Row[], status: number, total?: number) => {
      const headers: Record<string, string> = {};
      if (prefer.some((p) => p.startsWith("count="))) {
        const n = total ?? rows.length;
        headers["Content-Range"] = rows.length ? `0-${rows.length - 1}/${n}` : `*/${n}`;
      }
      if (wantsObject) {
        if (rows.length !== 1) return jres({ code: "PGRST116", details: `The result contains ${rows.length} rows`, hint: null, message: "JSON object requested, multiple (or no) rows returned" }, 406);
        return jres(rows[0], status === 201 ? 201 : 200, headers);
      }
      return jres(rows, status, headers);
    };

    if (req.method === "GET" || req.method === "HEAD") {
      const pred = buildFilter(t, params);
      let rows = sortRows(t, all.filter(pred), params.get("order"));
      const total = rows.length;
      const off = Number(params.get("offset") || 0);
      const lim = params.get("limit") !== null ? Number(params.get("limit")) : Infinity;
      rows = rows.slice(off, off + lim);
      const out = project(t, rows, params.get("select"));
      if (req.method === "HEAD") {
        const r = finish(out, 200, total);
        return new Response(null, { status: r.status, headers: r.headers });
      }
      return finish(out, 200, total);
    }

    if (req.method === "POST") {
      const body = await req.json();
      const list: Row[] = Array.isArray(body) ? body : [body];
      const isArr = Array.isArray(body);
      const colsParam = params.get("columns");
      const colList = colsParam ? colsParam.split(",").map(unquote) : null;
      const resolution = prefer.find((p) => p.startsWith("resolution="))?.split("=")[1] || null;
      const missingDefault = prefer.includes("missing=default");
      let target: string[] | null = null;
      if (resolution) {
        target = (params.get("on_conflict") || t.pk.join(",")).split(",").map((s) => s.trim());
        const cands = [t.pk, ...t.uniques].filter((u) => u.length);
        const ok = cands.some((u) => u.length === target!.length && u.every((c) => target!.includes(c)));
        if (!ok) throw new PgError(400, "42P10", "there is no unique or exclusion constraint matching the ON CONFLICT specification",
          `[dev] table ${name} : on_conflict=${target.join(",")} ; contraintes uniques connues : ${cands.map((u) => "(" + u.join(",") + ")").join(" ")}`);
      }
      // validation + construction (toute la requête échoue si une ligne échoue, comme en SQL)
      const staged: { row: Row; keys: string[] }[] = [];
      for (const src of list) {
        const keys = isArr && colList ? colList : Object.keys(src);
        for (const k of keys) if (!t.cols[k]) throw new PgError(400, "PGRST204", `Could not find the '${k}' column of '${name}' in the schema cache`);
        staged.push({ row: src, keys });
      }
      const results: Row[] = [];
      const snapshot = JSON.stringify(all);
      try {
        for (const { row: src, keys } of staged) {
          const row: Row = {};
          for (const c of t.order) {
            const col = t.cols[c];
            if (keys.includes(c) && !(src[c] === undefined && (missingDefault || !isArr))) {
              if (col.identity && src[c] !== undefined && src[c] !== null) throw new PgError(400, "428C9", `cannot insert a non-DEFAULT value into column "${c}"`);
              row[c] = coerce(col, src[c] === undefined ? null : src[c]);
            } else row[c] = evalDefault(col, () => this.nextSeq(name));
          }
          if (target) {
            const ex = all.find((r) => target!.every((c) => r[c] !== null && r[c] !== undefined && cmpVal(t.cols[c], r[c], row[c]) === 0));
            if (ex) {
              if (resolution === "ignore-duplicates") continue;
              const upd: Row = {};
              for (const k of keys) if (!t.cols[k].identity) upd[k] = row[k];
              if (t.updatedAtTrigger && t.cols.updated_at) upd.updated_at = pgNow();
              this.checkUnique(t, all, { ...ex, ...upd }, ex);
              this.checkNotNull(t, { ...ex, ...upd });
              Object.assign(ex, upd);
              results.push(ex);
              continue;
            }
          }
          this.checkNotNull(t, row);
          this.checkUnique(t, all, row, null);
          all.push(row);
          results.push(row);
        }
      } catch (e) {
        this.state.tables[name] = JSON.parse(snapshot);
        throw e;
      }
      this.scheduleSave();
      if (!repr) return new Response(null, { status: 201 });
      return finish(project(t, results, params.get("select")), 201);
    }

    if (req.method === "PATCH") {
      const body = await req.json() as Row;
      for (const k of Object.keys(body)) if (!t.cols[k]) throw new PgError(400, "PGRST204", `Could not find the '${k}' column of '${name}' in the schema cache`);
      const upd: Row = {};
      for (const k of Object.keys(body)) upd[k] = coerce(t.cols[k], body[k]);
      if (t.updatedAtTrigger && t.cols.updated_at && !("updated_at" in upd)) upd.updated_at = pgNow();
      const pred = buildFilter(t, params);
      const hits = all.filter(pred);
      for (const r of hits) { this.checkNotNull(t, { ...r, ...upd }); this.checkUnique(t, all, { ...r, ...upd }, r); }
      for (const r of hits) Object.assign(r, upd);
      this.scheduleSave();
      if (!repr) return new Response(null, { status: 204 });
      return finish(project(t, hits, params.get("select")), 200);
    }

    if (req.method === "DELETE") {
      const pred = buildFilter(t, params);
      const hits = all.filter(pred);
      this.state.tables[name] = all.filter((r) => !pred(r));
      this.scheduleSave();
      if (!repr) return new Response(null, { status: 204 });
      return finish(project(t, hits, params.get("select")), 200);
    }
    throw new PgError(405, "DEV405", "méthode non gérée " + req.method);
  }

  private checkNotNull(t: Table, row: Row) {
    for (const c of t.order) if (t.cols[c].notNull && (row[c] === null || row[c] === undefined))
      throw new PgError(400, "23502", `null value in column "${c}" of relation "${t.name}" violates not-null constraint`);
  }
  private checkUnique(t: Table, all: Row[], row: Row, self: Row | null) {
    for (const u of [t.pk, ...t.uniques].filter((u) => u.length)) {
      if (u.some((c) => row[c] === null || row[c] === undefined)) continue;
      const dup = all.find((r) => r !== self && u.every((c) => cmpVal(t.cols[c], r[c], row[c]) === 0));
      if (dup) throw new PgError(409, "23505", `duplicate key value violates unique constraint "${t.name}_${u.join("_")}_key"`, `Key (${u.join(", ")})=(${u.map((c) => row[c]).join(", ")}) already exists.`);
    }
  }

  // ── GoTrue ────────────────────────────────────────────────
  private authErr(status: number, error_code: string, msg: string) { return jres({ code: status, error_code, msg }, status); }
  private publicUser(u: AuthUser) {
    return { id: u.id, aud: "authenticated", role: "authenticated", email: u.email, email_confirmed_at: u.email_confirmed_at,
      phone: "", app_metadata: { provider: "email", providers: ["email"] }, user_metadata: {}, identities: [],
      created_at: u.created_at, updated_at: u.created_at, is_anonymous: false };
  }
  async createUser(email: string, password: string, id?: string): Promise<AuthUser> {
    const u: AuthUser = { id: id || crypto.randomUUID(), email: email.toLowerCase(), pwd: await sha256hex(password), created_at: pgNow(), email_confirmed_at: pgNow() };
    this.state.users.push(u);
    this.scheduleSave();
    return u;
  }
  private async session(u: AuthUser) {
    const exp = Math.floor(Date.now() / 1000) + 3600;
    const access_token = await signJwt({ sub: u.id, email: u.email, role: "authenticated", aud: "authenticated", exp, iat: exp - 3600, session_id: crypto.randomUUID() }, this.jwtSecret);
    this.userTokens.add(access_token);
    return { access_token, token_type: "bearer", expires_in: 3600, expires_at: exp, refresh_token: "dev-refresh-" + u.id + "-" + crypto.randomUUID(), user: this.publicUser(u) };
  }

  /** Jeton de session d'un utilisateur (outils de dev : /dev/pay lit les droits comme l'app le ferait). */
  async tokenFor(userId: string): Promise<string | null> {
    const u = this.state.users.find((x) => x.id === userId);
    return u ? (await this.session(u)).access_token : null;
  }

  private async auth(req: Request, url: URL): Promise<Response> {
    const path = url.pathname.slice("/auth/v1".length);
    const isService = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "") === this.serviceKey;
    const body = req.method === "GET" || req.method === "DELETE" ? {} : await req.json().catch(() => ({})) as Record<string, unknown>;

    if (path.startsWith("/admin/")) {
      if (!isService) return this.authErr(403, "not_admin", "User not allowed");
      if (path === "/admin/users" && req.method === "GET") {
        const page = Math.max(1, Number(url.searchParams.get("page") || 1));
        const per = Math.max(1, Number(url.searchParams.get("per_page") || 50));
        const users = this.state.users.slice((page - 1) * per, page * per).map((u) => this.publicUser(u));
        return jres({ users, aud: "authenticated" }, 200, { "x-total-count": String(this.state.users.length) });
      }
      if (path === "/admin/users" && req.method === "POST") {
        const email = String(body.email || "").trim().toLowerCase();
        if (!email) return this.authErr(400, "validation_failed", "Unable to validate email address: invalid format");
        if (this.state.users.some((u) => u.email === email)) return this.authErr(422, "email_exists", "A user with this email address has already been registered");
        if (String(body.password || "").length < 6) return this.authErr(422, "weak_password", "Password should be at least 6 characters.");
        const u = await this.createUser(email, String(body.password));
        return jres(this.publicUser(u));
      }
      const m = path.match(/^\/admin\/users\/([^/]+)$/);
      if (m) {
        const u = this.state.users.find((x) => x.id === m[1]);
        if (!u) return this.authErr(404, "user_not_found", "User not found");
        if (req.method === "PUT") {
          if (body.password) u.pwd = await sha256hex(String(body.password));
          if (body.email) u.email = String(body.email).toLowerCase();
          this.scheduleSave();
          return jres(this.publicUser(u));
        }
        if (req.method === "GET") return jres(this.publicUser(u));
        if (req.method === "DELETE") { this.state.users = this.state.users.filter((x) => x !== u); this.scheduleSave(); return jres(this.publicUser(u)); }
      }
      return this.authErr(404, "not_found", "faux GoTrue : route admin non gérée " + path);
    }
    if (path === "/token") {
      const gt = url.searchParams.get("grant_type");
      if (gt === "password") {
        const email = String(body.email || "").trim().toLowerCase();
        const u = this.state.users.find((x) => x.email === email);
        if (!u || u.pwd !== await sha256hex(String(body.password || ""))) return this.authErr(400, "invalid_credentials", "Invalid login credentials");
        return jres(await this.session(u));
      }
      if (gt === "refresh_token") {
        const id = String(body.refresh_token || "").replace(/^dev-refresh-/, "").slice(0, 36);
        const u = this.state.users.find((x) => x.id === id);
        if (!u) return this.authErr(400, "refresh_token_not_found", "Invalid Refresh Token");
        return jres(await this.session(u));
      }
      return this.authErr(400, "unsupported_grant_type", "grant_type non géré");
    }
    if (path === "/recover" && req.method === "POST") {
      const email = String(body.email || "").trim().toLowerCase();
      const u = this.state.users.find((x) => x.email === email);
      if (u) {
        const s = await this.session(u);
        const redirect = (url.searchParams.get("redirect_to") || this.publicUrl + "/app.html#reset").replace("https://matheux.fr", this.publicUrl);
        const link = redirect + (redirect.includes("#") ? "&" : "#") + "access_token=" + s.access_token + "&type=recovery";
        await this.onEmail(email, "[GoTrue] Réinitialisation du mot de passe", `<p>Lien de réinitialisation (dev) :</p><p><a href="${link}">${link}</a></p>`);
      }
      return jres({});
    }
    if (path === "/user") {
      const tok = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
      const p = jwtPayload(tok);
      const u = p && this.userTokens.has(tok) ? this.state.users.find((x) => x.id === p.sub) : null;
      if (!u) return this.authErr(401, "bad_jwt", "invalid JWT");
      return jres(this.publicUser(u));
    }
    if (path === "/logout") return new Response(null, { status: 204 });
    return this.authErr(404, "not_found", "faux GoTrue : route non gérée " + path);
  }
}
