// ════════════════════════════════════════════════════════════
//  Matheux — serveur de dev local (un seul process, un seul port)
//   http://localhost:8787/            → landing (index.html, ou landing/index.html s'il existe)
//   http://localhost:8787/app.html    → l'app (app.html bascule sur /api en localhost)
//   POST /api                         → supabase/functions/api/index.ts NON MODIFIÉ
//   /dev/…                            → outils de dev (pay, time, outbox, db, reset)
//  Supabase = faux PostgREST/GoTrue en mémoire (dev/fake_supabase.ts), persisté dans dev/data/db.json.
//  Tout fetch sortant d'index.ts est intercepté : Resend → dev/data/outbox/*.html, le reste est bloqué.
//
//  Usage : deno run -A dev/server.ts [serve|reset] [--port 8787]
// ════════════════════════════════════════════════════════════
import { loadSchema } from "./schema.ts";
import { FakeSupabase, signJwt } from "./fake_supabase.ts";
import { installClock, setOffsetDays, getOffsetDays } from "./clock.ts";

const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");
const DATA = Deno.env.get("DEV_DATA_DIR") || `${ROOT}/dev/data`;
const args = Deno.args;
const cmd = args.find((a) => !a.startsWith("--")) || "serve";
const portArg = args.indexOf("--port");
const PORT = Number(portArg >= 0 ? args[portArg + 1] : Deno.env.get("DEV_PORT") || 8787);
const PUBLIC = `http://localhost:${PORT}`;

// Secrets de DEV uniquement (jamais ceux de la prod — on ne les a pas et on n'en veut pas)
const FAKE_ORIGIN = "http://supabase.dev.invalid";
const JWT_SECRET = "matheux-dev-jwt-secret-local-uniquement";
export const STRIPE_DEV_SECRET = "whsec_matheux_dev_local";

Deno.mkdirSync(`${DATA}/outbox`, { recursive: true });
installClock();

const schema = await loadSchema(ROOT);
const SERVICE_KEY = await signJwt({ role: "service_role", iss: "supabase-dev", iat: 1758700000, exp: 4102444800 }, JWT_SECRET);
export const fake = new FakeSupabase(schema, `${DATA}/db.json`, JWT_SECRET, SERVICE_KEY, PUBLIC);

// ── Outbox emails ──
let mailSeq = 0;
async function writeMail(to: string, subject: string, html: string) {
  const ts = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  const slug = subject.normalize("NFD").replace(/[^\w]+/g, "_").slice(0, 50);
  const name = `${ts}_${String(++mailSeq).padStart(3, "0")}_${to.replace(/[^\w@.-]/g, "_")}_${slug}.html`;
  const head = `<!-- DEV OUTBOX --><div style="font:13px/1.5 monospace;background:#fff8d6;border-bottom:1px solid #e0c96a;padding:10px 14px">` +
    `<b>À :</b> ${to}<br><b>Objet :</b> ${subject.replace(/</g, "&lt;")}<br><b>Heure (horloge dev) :</b> ${new Date().toISOString()}</div>`;
  await Deno.writeTextFile(`${DATA}/outbox/${name}`, `<!doctype html><meta charset="utf-8"><title>${subject.replace(/</g, "&lt;")}</title>${head}${html}`);
  console.log(`[dev] ✉  email → ${to} « ${subject} » (dev/data/outbox/${name})`);
}
fake.onEmail = writeMail;

// ── Interception des fetch sortants ──
const realFetch = globalThis.fetch;
globalThis.fetch = async (input: Request | URL | string, init?: RequestInit) => {
  const req = input instanceof Request && !init ? input : new Request(input, init);
  const url = new URL(req.url);
  if (url.origin === FAKE_ORIGIN) return fake.handle(req);
  if (url.hostname === "api.resend.com") {
    const b = await req.json().catch(() => ({}));
    const to = Array.isArray(b.to) ? b.to.join(", ") : String(b.to || "?");
    await writeMail(to, String(b.subject || "(sans objet)"), String(b.html || b.text || ""));
    return new Response(JSON.stringify({ id: "dev-" + crypto.randomUUID() }), { status: 200, headers: { "Content-Type": "application/json" } });
  }
  if (url.hostname === "script.google.com") {
    console.log("[dev] appel GAS bloqué (legacy) :", url.pathname.slice(0, 40));
    return new Response(JSON.stringify({ status: "success", dev: "GAS non appelé en local" }), { headers: { "Content-Type": "application/json" } });
  }
  console.warn("[dev] ⛔ fetch externe bloqué :", req.method, url.href);
  return new Response(JSON.stringify({ error: "[dev] appel externe bloqué en local : " + url.host }), { status: 503, headers: { "Content-Type": "application/json" } });
};
void realFetch;

// ── Import de index.ts non modifié : Deno.serve est remplacé le temps de l'import pour capturer le handler ──
Deno.env.set("SUPABASE_URL", FAKE_ORIGIN);
Deno.env.set("SUPABASE_SERVICE_ROLE_KEY", SERVICE_KEY);
Deno.env.set("RESEND_API_KEY", "re_dev_local");
Deno.env.set("STRIPE_WEBHOOK_SECRET", STRIPE_DEV_SECRET);
type Handler = (req: Request) => Response | Promise<Response>;
let apiHandler: Handler | null = null;
const origServe = Object.getOwnPropertyDescriptor(Deno, "serve")!;
Object.defineProperty(Deno, "serve", {
  configurable: true,
  value: (a: unknown, b?: unknown) => {
    apiHandler = (typeof a === "function" ? a : b) as Handler;
    return { finished: Promise.resolve(), shutdown: async () => {}, ref() {}, unref() {}, addr: { hostname: "localhost", port: PORT, transport: "tcp" } };
  },
});
await import(`${ROOT}/supabase/functions/api/index.ts`);
Object.defineProperty(Deno, "serve", origServe);
if (!apiHandler) throw new Error("index.ts n'a pas appelé Deno.serve");
export const api: Handler = apiHandler;

/** Appel direct d'une action (utilisé par le seed et /dev/pay). */
export async function callApi(p: Record<string, unknown>, headers: Record<string, string> = {}): Promise<Record<string, unknown>> {
  const r = await api(new Request(`${PUBLIC}/api`, { method: "POST", body: JSON.stringify(p), headers }));
  return await r.json();
}

// ── Paiement simulé (webhook Stripe signé avec le secret de dev) ──
export async function simulerPaiement(code: string, produitIn: string) {
  const prof = fake.rows("profiles").find((r) => r.code === code);
  if (!prof) return { status: "error", message: "Code élève inconnu : " + code };
  const dejaDiag = fake.rows("achats").some((a) => (a.code === code || a.email === prof.email) && a.produit === "diagnostic_complet");
  let produit = produitIn === "diagnostic_complet" ? "diag_complet" : produitIn;
  if (produit === "programme_brevet" && dejaDiag) produit = "programme_upgrade";
  const montants: Record<string, number> = { diag_complet: 1900, programme_brevet: 4900, programme_upgrade: 3000 };
  if (!(produit in montants)) return { status: "error", message: "produit ∈ diag_complet | programme_brevet" };
  const event = {
    id: "evt_dev_" + crypto.randomUUID().slice(0, 8), type: "checkout.session.completed",
    data: { object: {
      id: "cs_dev_" + crypto.randomUUID().replace(/-/g, "").slice(0, 20), object: "checkout.session",
      customer_details: { email: String(prof.email) }, client_reference_id: code, amount_total: montants[produit],
      metadata: { produit, niveau: String(prof.niveau || "3EME"), offre_version: "dev" },
    } },
  };
  const raw = JSON.stringify(event);
  const t = Math.floor(Date.now() / 1000);
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(STRIPE_DEV_SECRET), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = Array.from(new Uint8Array(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`${t}.${raw}`))))
    .map((x) => x.toString(16).padStart(2, "0")).join("");
  const r = await api(new Request(`${PUBLIC}/api`, { method: "POST", body: raw, headers: { "stripe-signature": `t=${t},v1=${sig}` } }));
  const webhook = await r.json();
  const acces = await callApi({ action: "get_acces", code, access_token: await fake.tokenFor(String(prof.id)) });
  return { status: webhook.status, produit, montant_cents: montants[produit], webhook, droits: acces.droits };
}

// ── Reset / seed ──
async function reset() {
  const { seed } = await import("./seed.ts");
  for await (const e of Deno.readDir(`${DATA}/outbox`)) await Deno.remove(`${DATA}/outbox/${e.name}`);
  fake.resetEmpty();
  setOffsetDays(0);
  await seed({ fake, callApi, simulerPaiement, setOffsetDays, root: ROOT });
  setOffsetDays(0);
  fake.saveNow();
}

if (cmd === "reset") {
  await reset();
  console.log("[dev] base réinitialisée →", `${DATA}/db.json`);
  Deno.exit(0);
}

if (!fake.load()) {
  console.log("[dev] pas de base locale : seed initial…");
  await reset();
}

// ── Fichiers statiques ──
const MIME: Record<string, string> = {
  html: "text/html; charset=utf-8", js: "text/javascript; charset=utf-8", mjs: "text/javascript; charset=utf-8", css: "text/css; charset=utf-8",
  json: "application/json", png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", svg: "image/svg+xml", ico: "image/x-icon",
  webp: "image/webp", woff2: "font/woff2", woff: "font/woff", txt: "text/plain; charset=utf-8", xml: "application/xml", pdf: "application/pdf", webmanifest: "application/manifest+json",
};
const INTERDIT = [/^\/\./, /^\/dev\/data\//, /^\/supabase\//, /\.env/, /^\/node_modules\//];
function exists(p: string) { try { return Deno.statSync(p).isFile; } catch { return false; } }

const INJECT = `\n<script src="/dev/inject.js"></script>\n`;

async function serveStatic(pathname: string): Promise<Response> {
  let p = decodeURIComponent(pathname);
  if (p.includes("..") || INTERDIT.some((re) => re.test(p))) return new Response("Interdit", { status: 403 });
  if (p === "/sw.js") {
    // Service worker neutralisé en dev : évite qu'un cache garde une vieille version de l'app.
    return new Response("self.addEventListener('install',()=>self.skipWaiting());self.addEventListener('activate',e=>e.waitUntil(self.registration.unregister()));",
      { headers: { "Content-Type": MIME.js, "Cache-Control": "no-store" } });
  }
  let file: string | null = null;
  if (p === "/" || p === "/index.html") file = exists(`${ROOT}/landing/index.html`) ? `${ROOT}/landing/index.html` : `${ROOT}/index.html`;
  else if (p.startsWith("/b/")) file = exists(`${ROOT}/bilan.html`) ? `${ROOT}/bilan.html` : null;
  else {
    const cands = [`${ROOT}${p}`, `${ROOT}${p}.html`, `${ROOT}${p.replace(/\/$/, "")}/index.html`, `${ROOT}/landing${p}`];
    file = cands.find(exists) || null;
  }
  if (!file) {
    const nf = exists(`${ROOT}/404.html`) ? await Deno.readTextFile(`${ROOT}/404.html`) : "404";
    return new Response(nf, { status: 404, headers: { "Content-Type": MIME.html } });
  }
  const ext = file.split(".").pop()!.toLowerCase();
  const headers = { "Content-Type": MIME[ext] || "application/octet-stream", "Cache-Control": "no-store" };
  if (ext === "html") {
    let html = await Deno.readTextFile(file);
    html = html.includes("</body>") ? html.replace(/<\/body>(?![\s\S]*<\/body>)/, INJECT + "</body>") : html + INJECT;
    return new Response(html, { headers });
  }
  return new Response(await Deno.readFile(file), { headers });
}

// Script injecté dans les pages HTML servies en dev (pas dans les fichiers) :
// badge « DEV », et les liens Stripe (buy.stripe.com) sont redirigés vers le paiement simulé.
const INJECT_JS = `(function(){
  try{var b=document.createElement('div');b.textContent='DEV local';b.title='Backend en mémoire — rien ne part en prod. Emails : /dev/outbox';
  b.style.cssText='position:fixed;left:8px;bottom:8px;z-index:2147483647;background:#b91c1c;color:#fff;font:700 11px/1 system-ui;padding:5px 8px;border-radius:6px;opacity:.85;pointer-events:auto;cursor:pointer';
  b.onclick=function(){window.open('/dev/outbox','_blank')};(document.body||document.documentElement).appendChild(b);}catch(e){}
  function payer(url){
    var u; try{u=new URL(url,location.href)}catch(e){return false}
    if(!/(^|\\.)stripe\\.com$/.test(u.hostname))return false;
    var code=u.searchParams.get('client_reference_id')||'';
    try{if(!code){var s=JSON.parse(localStorage.getItem('boost_v23')||'{}');code=s.code||(s.prof&&s.prof.code)||''}}catch(e){}
    code=prompt('[DEV] Paiement Stripe simulé — code élève :',code);if(!code)return true;
    var produit=prompt('[DEV] Produit : diag_complet ou programme_brevet','diag_complet');if(!produit)return true;
    fetch('/dev/pay?code='+encodeURIComponent(code)+'&produit='+encodeURIComponent(produit),{method:'POST'}).then(function(r){return r.json()}).then(function(j){
      alert('[DEV] Paiement simulé : '+j.status+(j.droits?' — accès : '+j.droits.acces:'')+(j.message?' — '+j.message:''));location.reload();});
    return true;
  }
  document.addEventListener('click',function(e){var a=e.target&&e.target.closest&&e.target.closest('a[href]');if(a&&payer(a.href)){e.preventDefault();e.stopPropagation();}},true);
  var wo=window.open;window.open=function(url){if(url&&payer(String(url)))return null;return wo.apply(window,arguments)};
})();`;

async function outboxPage(): Promise<Response> {
  const list: string[] = [];
  for await (const e of Deno.readDir(`${DATA}/outbox`)) if (e.name.endsWith(".html")) list.push(e.name);
  list.sort().reverse();
  const li = list.map((n) => `<li><a href="/dev/outbox/${encodeURIComponent(n)}" target="mail">${n.replace(/</g, "&lt;")}</a></li>`).join("");
  return new Response(`<!doctype html><meta charset="utf-8"><title>Outbox dev</title><body style="font:14px system-ui;margin:0;display:flex;height:100vh">
<div style="width:40%;overflow:auto;padding:12px;border-right:1px solid #ddd"><h2>Emails (${list.length})</h2><p>Aucun email ne part : ils sont écrits dans <code>dev/data/outbox/</code>.</p><ol>${li}</ol></div>
<iframe name="mail" style="flex:1;border:0"></iframe></body>`, { headers: { "Content-Type": MIME.html } });
}

function j(o: unknown, status = 200) { return new Response(JSON.stringify(o, null, 2), { status, headers: { "Content-Type": "application/json; charset=utf-8" } }); }

async function devRoute(req: Request, url: URL): Promise<Response> {
  const p = url.pathname;
  if (p === "/dev/inject.js") return new Response(INJECT_JS, { headers: { "Content-Type": MIME.js, "Cache-Control": "no-store" } });
  if (p === "/dev/health") return j({ status: "ok", offset_jours: getOffsetDays(), tables: Object.fromEntries(Object.entries(fake.state.tables).map(([k, v]) => [k, v.length])) });
  if (p === "/dev/outbox") return await outboxPage();
  if (p.startsWith("/dev/outbox/")) {
    const n = decodeURIComponent(p.slice("/dev/outbox/".length));
    if (n.includes("/") || n.includes("..")) return new Response("Interdit", { status: 403 });
    try { return new Response(await Deno.readFile(`${DATA}/outbox/${n}`), { headers: { "Content-Type": MIME.html } }); } catch { return new Response("introuvable", { status: 404 }); }
  }
  if (p === "/dev/pay") {
    const code = String(url.searchParams.get("code") || "").toUpperCase();
    const produit = String(url.searchParams.get("produit") || "");
    const res = await simulerPaiement(code, produit);
    if (url.searchParams.get("redirect")) return Response.redirect(`${PUBLIC}/app.html`, 303);
    return j(res, res.status === "success" ? 200 : 400);
  }
  if (p === "/dev/time") {
    if (url.searchParams.has("reset")) setOffsetDays(0);
    if (url.searchParams.has("jours")) setOffsetDays(getOffsetDays() + Number(url.searchParams.get("jours")));
    return j({ offset_jours: getOffsetDays(), maintenant: new Date().toISOString(), aujourdhui_paris: new Date().toLocaleDateString("sv-SE", { timeZone: "Europe/Paris" }) });
  }
  if (p === "/dev/reset" && req.method === "POST") { await reset(); return j({ status: "success", message: "base réinitialisée" }); }
  if (p.startsWith("/dev/db/")) {
    const t = p.slice("/dev/db/".length);
    if (!fake.state.tables[t]) return j({ error: "table inconnue", tables: Object.keys(fake.state.tables) }, 404);
    let rows = fake.state.tables[t];
    for (const [k, v] of url.searchParams) if (k !== "limit") rows = rows.filter((r) => String(r[k]) === v);
    return j(rows.slice(-Number(url.searchParams.get("limit") || 200)));
  }
  if (p === "/dev" || p === "/dev/") {
    return new Response(`<!doctype html><meta charset="utf-8"><title>Matheux dev</title><body style="font:15px system-ui;max-width:720px;margin:30px auto">
<h1>Matheux — outils de dev</h1><ul>
<li><a href="/">Landing</a> · <a href="/app.html">App</a></li>
<li><a href="/dev/outbox">Emails (outbox)</a></li>
<li><a href="/dev/health">État de la base</a> · tables : ${Object.keys(fake.state.tables).map((t) => `<a href="/dev/db/${t}">${t}</a>`).join(", ")}</li>
<li>Paiement simulé : <code>curl -X POST 'localhost:${PORT}/dev/pay?code=LINA3E&amp;produit=diag_complet'</code></li>
<li>Horloge : <a href="/dev/time?jours=1">+1 jour</a> · <a href="/dev/time?reset">remettre à aujourd'hui</a> (${getOffsetDays()} j)</li>
<li><form method="post" action="/dev/reset" onsubmit="return confirm('Remettre la base à l\\'état initial ?')"><button>Reset de la base</button></form></li></ul>`,
      { headers: { "Content-Type": MIME.html } });
  }
  return j({ error: "route dev inconnue" }, 404);
}

Deno.serve({ port: PORT, hostname: "127.0.0.1", onListen: () => {
  console.log(`\n  Matheux (dev local) → ${PUBLIC}\n  App : ${PUBLIC}/app.html · Outils : ${PUBLIC}/dev · Emails : ${PUBLIC}/dev/outbox\n  Base : ${DATA}/db.json · Ctrl+C pour arrêter\n`);
} }, async (req) => {
  const url = new URL(req.url);
  try {
    if (url.pathname === "/api" || url.pathname === "/api/") {
      const t0 = performance.now();
      const clone = req.clone();
      const res = await api(req);
      let action = "?";
      try { const b = JSON.parse(await clone.text()); action = b.action || b.type || "?"; } catch { /* */ }
      if (Deno.env.get("DEV_QUIET") !== "1") console.log(`[api] ${action} → ${res.status} (${Math.round(performance.now() - t0)} ms)`);
      return res;
    }
    if (url.pathname.startsWith("/dev")) return await devRoute(req, url);
    return await serveStatic(url.pathname);
  } catch (e) {
    console.error("[dev] erreur", e);
    return j({ status: "error", message: String(e) }, 500);
  }
});

globalThis.addEventListener("unload", () => fake.saveNow());
Deno.addSignalListener("SIGINT", () => { fake.saveNow(); Deno.exit(0); });
Deno.addSignalListener("SIGTERM", () => { fake.saveNow(); Deno.exit(0); });
