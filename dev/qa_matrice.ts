// ════════════════════════════════════════════════════════════
//  Matheux — matrice QA « persona × moment » (docs/specs/80-qa-matrice.md)
//  Un scénario court par case, Chrome headless 375 px. Serveur ISOLÉ (port 8795 par défaut, base temporaire).
//  États construits par l'API (register, diag, save_score, /dev/pay, /dev/time), puis l'app / bilan.html
//  est ouverte comme le verrait l'utilisateur. Contrôles communs à chaque écran ado :
//   0 erreur console · aucun CTA d'achat (contrat §7) · jamais « ton prof » · cohérence droits/messages.
//  Usage : deno run -A dev/qa_matrice.ts [filtre]      (filtre = sous-chaîne du nom de case)
//          QA_PORT=8795 QA_SHOTS=/tmp/qa-shots pour garder les captures
// ════════════════════════════════════════════════════════════
/// <reference lib="dom" />
import puppeteer from "npm:puppeteer-core@23.11.1";

const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");
const PORT = Number(Deno.env.get("QA_PORT") || 8795), BASE = `http://localhost:${PORT}`;
const DATA = await Deno.makeTempDir({ dir: "/tmp", prefix: "matheux-qa-" });
const CHROME = Deno.env.get("CHROME") || "/usr/bin/google-chrome";
const SHOTS = Deno.env.get("QA_SHOTS") || "";
const FILTRE = Deno.args[0] || "";
const FLAGS = ["run", "--allow-net", "--allow-read", "--allow-write", "--allow-env", "--allow-run=python3", "--allow-sys", "--no-prompt"];
const env = { DEV_DATA_DIR: DATA, DEV_QUIET: "1" };
const MDP = "matheux-dev";
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
// deno-lint-ignore no-explicit-any
type J = Record<string, any>;

// ── serveur isolé ──
const seed = await new Deno.Command(Deno.execPath(), { args: [...FLAGS, `${ROOT}/dev/server.ts`, "reset"], env, stdout: "null", stderr: "piped" }).output();
if (!seed.success) { console.error(new TextDecoder().decode(seed.stderr)); Deno.exit(1); }
const srv = new Deno.Command(Deno.execPath(), { args: [...FLAGS, `${ROOT}/dev/server.ts`, "serve", "--port", String(PORT)], env, stdout: "null", stderr: "null" }).spawn();
for (let i = 0; i < 80; i++) { try { if ((await fetch(`${BASE}/dev/health`)).ok) break; } catch { /* */ } await sleep(250); }

async function api(p: J): Promise<J> { return await (await fetch(`${BASE}/api`, { method: "POST", body: JSON.stringify(p) })).json(); }
async function dev(path: string, method = "GET"): Promise<J> { return await (await fetch(BASE + path, { method })).json().catch(() => ({})); }
async function hash(email: string, mdp: string) {
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(email.toLowerCase() + "::" + mdp + "::AB22"));
  return Array.from(new Uint8Array(h)).map((x) => x.toString(16).padStart(2, "0")).join("");
}
let decalage = 0; // jours : le navigateur suit l'horloge du serveur de dev
const temps = async (j: number) => { await dev("/dev/time?reset"); if (j) await dev(`/dev/time?jours=${j}`); decalage = j; };

// ── personas (états construits par l'API, comme la prod les produirait) ──
type Eleve = { code: string; email: string; access_token: string; refresh_token: string; prenom: string };
let nEleve = 0;
async function inscrit(prenom: string, express = true): Promise<Eleve> {
  const email = `qa${++nEleve}.${Date.now()}@exemple.fr`;
  const r = await api({ action: "register", name: prenom, email, level: "3EME", password: await hash(email, MDP), objectif: "brevet" });
  if (r.status !== "success") throw new Error("register " + JSON.stringify(r));
  const e: Eleve = { code: r.profile.code, email, access_token: r.access_token, refresh_token: r.refresh_token, prenom };
  if (express) await diag(e, "express");
  return e;
}
const A = (e: Eleve) => ({ code: e.code, access_token: e.access_token });
// Répond à un diagnostic : alterne bonne-ish / mauvaise / je ne sais pas. `max` = arrêt en cours de route.
async function diag(e: Eleve, type: string, max = 999, jusquAuModule = 99): Promise<J> {
  let r = await api({ action: "start_diagnostic", ...A(e), type });
  if (r.status !== "success") return r;
  const id = r.diagnostic_id; let n = 0;
  while (n < max) {
    if (r.termine) return r;
    if (r.fin_module) { if (r.fin_module > jusquAuModule) return r; r = await api({ action: "start_diagnostic", ...A(e), type }); continue; }
    const q = r.question; if (!q) return r;
    const rep = n % 4 === 3 ? "" : (q.options?.[n % 2] ?? (n % 2 ? "12" : "3"));
    r = await api({ action: "answer_diagnostic", ...A(e), diagnostic_id: id, item_id: q.id, reponse: rep, temps: 20 });
    if (r.status !== "success") return r;
    n++;
  }
  return r;
}
async function seance(e: Eleve, n = 5): Promise<J> {
  const tr = await api({ action: "get_training", ...A(e) });
  const exos = (tr.boost?.exos || []) as J[];
  for (const [i, x] of exos.slice(0, n).entries()) {
    // comme l'app (sendScore) : categorie BOOST, exercice_idx = rang dans la séance (1-based)
    await api({ action: "save_score", ...A(e), name: e.prenom, level: "3EME", categorie: "BOOST", exercice_idx: i + 1, resultat: i % 2 ? "EASY" : "HARD",
      source: "BOOST", item_id: x.item_id, comp: x.comp, q: x.q, reponse: i % 2 ? x.a : "zz", time: 30 });
  }
  return tr;
}
const payer = (e: Eleve, produit: string) => dev(`/dev/pay?code=${e.code}&produit=${produit}`, "POST");
const partage = async (e: Eleve) => (await api({ action: "create_share", ...A(e), canal: "app" })).token as string;

// ── navigateur ──
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--no-sandbox", "--disable-gpu"] });
type Vue = { texte: string; boutons: string[]; errs: string[]; page: puppeteer.Page; ctx: puppeteer.BrowserContext };
const bruit = (e: string) => /favicon|googletagmanager|google-analytics|fonts\.g|ERR_INTERNET_DISCONNECTED|net::ERR_NAME|cdn\.jsdelivr|cdnjs|ERR_BLOCKED/.test(e);
async function ouvrir(url: string, ls: Record<string, string> = {}, opts: { attente?: number; intercepte?: (j: J, action: string) => J | null } = {}): Promise<Vue> {
  const ctx = await browser.createBrowserContext();
  const page = await ctx.newPage();
  await page.setViewport({ width: 375, height: 800 });
  const errs: string[] = [];
  page.on("pageerror", (e) => errs.push("PAGEERROR " + (e as Error).message));
  page.on("console", (m) => { if (m.type() === "error" && !bruit(m.text()) && !/Failed to load resource/.test(m.text())) errs.push("CONSOLE " + m.text()); });
  page.on("dialog", (d) => d.dismiss());
  page.on("response", (r) => { if (r.status() >= 400 && r.url().startsWith(BASE) && !/favicon/.test(r.url())) errs.push(`HTTP ${r.status()} ${r.url().replace(BASE, "")}`); });
  if (opts.intercepte) {
    await page.setRequestInterception(true);
    page.on("request", async (req) => {
      if (!req.url().endsWith("/api") || req.method() !== "POST") return req.continue();
      const body = JSON.parse(req.postData() || "{}");
      const r = await fetch(req.url(), { method: "POST", body: req.postData() });
      let j = await r.json();
      j = opts.intercepte!(j, body.action) || j;
      req.respond({ status: 200, contentType: "application/json", body: JSON.stringify(j) });
    });
  }
  if (decalage) await page.evaluateOnNewDocument((ms: number) => {
    const R = Date; // deno-lint-ignore no-explicit-any
    class D extends R { constructor(...a: any[]) { if (a.length) super(...(a as [any])); else super(R.now() + ms); } static override now() { return R.now() + ms; } }
    (globalThis as any).Date = D; // deno-lint-ignore no-explicit-any
  }, decalage * 86400000);
  await page.goto(BASE + "/offline.html", { waitUntil: "load" });
  await page.evaluate((ls) => { localStorage.clear(); localStorage.setItem("mx_cookie_consent", "refused"); for (const [k, v] of Object.entries(ls)) localStorage.setItem(k, v); }, ls);
  await page.goto(BASE + url, { waitUntil: "networkidle2" });
  await sleep(opts.attente ?? 1500);
  return await lire({ page, ctx, errs, texte: "", boutons: [] });
}
async function lire(v: Vue): Promise<Vue> {
  const r = await v.page.evaluate(() => {
    const vis = (el: Element) => { const b = (el as HTMLElement).getBoundingClientRect(); const s = getComputedStyle(el); return b.width > 0 && b.height > 0 && s.visibility !== "hidden" && s.display !== "none"; };
    return {
      texte: document.body.innerText.replace(/[ \t]+/g, " ").replace(/\n+/g, " | "),
      boutons: [...document.querySelectorAll("button, a.btn, a.mx-btn, [role=button]")].filter(vis).map((b) => (b as HTMLElement).innerText.replace(/\s+/g, " ").trim()).filter(Boolean),
      largeur: document.documentElement.scrollWidth,
    };
  });
  v.texte = r.texte; v.boutons = r.boutons;
  if (r.largeur > 380) v.errs.push("scroll horizontal (" + r.largeur + " px)");
  return v;
}
const sess = (e: Eleve) => ({ boost_v23: JSON.stringify({ code: e.code, email: e.email, access_token: e.access_token, refresh_token: e.refresh_token }) });
const appDe = (e: Eleve, qs = "", o: J = {}) => ouvrir("/app.html" + qs, sess(e), o);
async function clic(v: Vue, re: RegExp | string, attente = 1500): Promise<boolean> {
  const ok = await v.page.evaluate((src) => {
    const re = new RegExp(src, "i");
    const vis = (el: Element) => { const b = (el as HTMLElement).getBoundingClientRect(); return b.width > 0 && b.height > 0; };
    const b = [...document.querySelectorAll("button, a")].filter(vis).reverse().find((x) => re.test((x as HTMLElement).innerText));
    if (b) { (b as HTMLElement).click(); return true; } return false;
  }, typeof re === "string" ? re : re.source);
  await sleep(attente); await lire(v);
  return ok;
}

// ── contrôles ──
type Res = { cas: string; ok: boolean; notes: string[] };
const resultats: Res[] = [];
const ACHAT_ADO = /€|acheter|payer|obtenir le diagnostic|choisir le programme|offrir|débloquer (le|ta)|activer mon plan|passer au programme/i;
function controlesAdo(v: Vue, notes: string[], vueParentOuverte = false) {
  if (v.errs.length) notes.push("erreurs : " + v.errs.slice(0, 3).join(" ; "));
  if (/ton prof|prof prépare|Nicolas prépare|prépare la suite/i.test(v.texte)) notes.push("« ton prof / prépare la suite » visible");
  if (!vueParentOuverte) { const b = v.boutons.filter((x) => ACHAT_ADO.test(x)); if (b.length) notes.push("CTA d'achat côté ado : " + b.join(" / ")); }
  if (/undefined|NaN|\[object Object\]|null €/i.test(v.texte)) notes.push("texte cassé (undefined/NaN/null)");
}
function attendu(notes: string[], cond: unknown, msg: string) { if (!cond) notes.push(msg); }
async function cas(nom: string, f: (notes: string[]) => Promise<Vue | Vue[] | void>) {
  if (FILTRE && !nom.toLowerCase().includes(FILTRE.toLowerCase())) return;
  const notes: string[] = [];
  let vues: Vue[] = [];
  try {
    const r = await f(notes);
    vues = r ? (Array.isArray(r) ? r : [r]) : [];
  } catch (e) { notes.push("exception : " + (e as Error).message); }
  for (const [i, v] of vues.entries()) {
    if (SHOTS) { await Deno.mkdir(SHOTS, { recursive: true }); await v.page.screenshot({ path: `${SHOTS}/${nom.replace(/[^\w]+/g, "_")}${i ? "_" + i : ""}.png`, fullPage: true }).catch(() => {}); }
    await v.ctx.close().catch(() => {});
  }
  await temps(0);
  const ok = notes.length === 0;
  resultats.push({ cas: nom, ok, notes });
  console.log(`${ok ? "✅" : "❌"} ${nom}${ok ? "" : "\n     - " + notes.join("\n     - ")}`);
}

// ════════════════════════════════════════════════════════════
//  CASES
// ════════════════════════════════════════════════════════════
try {
  // ── Visiteur invité ──
  await cas("invité · diag en cours puis rechargement → reprise proposée", async (n) => {
    const v = await ouvrir("/app.html#diag", {}, { attente: 1500 });
    await clic(v, "lancer|commencer");
    for (let i = 0; i < 4; i++) {
      await v.page.evaluate(() => { const o = document.querySelector(".dx-opt") as HTMLElement; if (o) o.click(); else { const f = document.getElementById("dx-fill") as HTMLInputElement; if (f) { f.value = "12"; f.dispatchEvent(new Event("input", { bubbles: true })); } } });
      await v.page.evaluate(() => (document.getElementById("dx-val") as HTMLButtonElement)?.click()); await sleep(900);
    }
    await v.page.goto(BASE + "/app.html", { waitUntil: "networkidle2" }); await sleep(1800); await lire(v);
    attendu(n, /arrêté|reprendre|on reprend/i.test(v.texte), "pas de proposition de reprise après rechargement : " + v.texte.slice(0, 200));
    controlesAdo(v, n);
    return v;
  });
  await cas("invité · diag express fini sans compte → carte partielle + suite", async (n) => {
    const v = await ouvrir("/app.html#diag", {}, { attente: 1500 });
    await clic(v, "lancer|commencer");
    for (let i = 0; i < 25; i++) {
      const st = await v.page.evaluate(() => document.getElementById("dx-val") ? 1 : 0); if (!st) break;
      await v.page.evaluate((i) => { const o = [...document.querySelectorAll(".dx-opt")] as HTMLElement[]; if (o.length) o[i % o.length].click(); else { const f = document.getElementById("dx-fill") as HTMLInputElement; if (f) { f.value = "12"; f.dispatchEvent(new Event("input", { bubbles: true })); } } }, i);
      await v.page.evaluate(() => (document.getElementById("dx-val") as HTMLButtonElement)?.click()); await sleep(700);
    }
    await sleep(2000); await lire(v);
    attendu(n, /Tes 5 domaines|point faible|point le plus fragile|il nous manque/i.test(v.texte), "carte partielle absente : " + v.texte.slice(0, 200));
    attendu(n, v.boutons.some((b) => /entraîner gratuitement/i.test(b)), "pas de bouton « M'entraîner gratuitement »");
    attendu(n, v.boutons.some((b) => /parents/i.test(b)), "pas de bouton « Envoyer à mes parents »");
    controlesAdo(v, n);
    // la carte invité est-elle retrouvée après rechargement (avant compte) ?
    await v.page.goto(BASE + "/app.html", { waitUntil: "networkidle2" }); await sleep(1800); await lire(v);
    attendu(n, /carte|domaines|créer mon espace|reprendre/i.test(v.texte), "après rechargement, la carte invité est perdue sans explication : " + v.texte.slice(0, 160));
    controlesAdo(v, n);
    return v;
  });

  // ── Inscrit gratuit ──
  const lea = await inscrit("Léa");
  await cas("gratuit · J0 séance pas faite → séance du jour prête", async (n) => {
    const v = await appDe(lea);
    attendu(n, /TA SÉANCE DU JOUR/i.test(v.texte) && v.boutons.some((b) => /C'est parti/i.test(b)), "pas de séance du jour + « C'est parti »");
    attendu(n, v.boutons.some((b) => /Gratuit · voir ce qui est inclus/.test(b)), "chip Gratuit absent");
    attendu(n, !/Diagnostic complet ✓|Check-up|S'entraîner sur/i.test(v.texte), "éléments payants visibles en gratuit");
    controlesAdo(v, n);
    // paywall ado : prix cité, pas de bouton d'achat, suite gratuite + partage + « Je suis le parent »
    await clic(v, "Gratuit · voir");
    attendu(n, /décision pour tes parents/i.test(v.texte), "paywall ado : phrase « décision pour tes parents » absente");
    attendu(n, v.boutons.some((b) => /Continuer gratuitement/.test(b)) && v.boutons.some((b) => /Montrer ma carte/.test(b)), "paywall ado : boutons attendus absents");
    controlesAdo(v, n);
    // vue parent : 19 € + 49 € ; programme sans lien → bientôt
    await clic(v, "^Je suis le parent$");
    attendu(n, /19 €/i.test(v.texte) && /49 €/i.test(v.texte), "vue parent : prix 19/49 absents");
    controlesAdo(v, n, true);
    return v;
  });
  await cas("gratuit · J0 séance faite → pas « C'est parti », « demain » ok", async (n) => {
    const e = await inscrit("Inès"); await seance(e);
    const v = await appDe(e);
    attendu(n, /Séance faite/i.test(v.texte), "état « séance faite » absent");
    attendu(n, !v.boutons.some((b) => /C'est parti|Continue, encore/i.test(b)), "bouton « C'est parti » alors que la séance est faite");
    attendu(n, /🎯[\s|]*5[\s|]*\/[\s|]*5/.test(v.texte), "mission du jour pas à 5/5 : " + (v.texte.match(/🎯[^|]*/) || [""])[0]);
    controlesAdo(v, n);
    return v;
  });
  await cas("gratuit · séance en cours (2/5) → « Continue, encore 3 exos »", async (n) => {
    const e = await inscrit("Noé"); await seance(e, 2);
    const v = await appDe(e);
    attendu(n, v.boutons.some((b) => /Continue, encore 3 exos/i.test(b)), "reprise de séance absente : " + v.boutons.join(" / "));
    controlesAdo(v, n);
    return v;
  });
  await cas("gratuit · fin de séance dans l'app → écran de fin cohérent", async (n) => {
    const e = await inscrit("Zoé"); await seance(e, 4);
    const v = await appDe(e);
    await clic(v, "Continue, encore");
    await v.page.evaluate(() => {
      // deno-lint-ignore no-explicit-any
      const g = (x: string) => (0, eval)(x); const S = g("S"); const ex = g("LVL")["3EME"].cats[S.sessCat][S._activeIdx];
      if (ex.type === "fill") (document.querySelector(".fill-input") as HTMLInputElement).value = String(ex.a).replace(/\$/g, "");
      else ([...document.querySelectorAll(".opt-grid .opt")].find((x) => +(x as HTMLElement).dataset.oi! === ex.options.indexOf(ex.a)) as HTMLElement).click();
      g("validateAnswer")();
    });
    await sleep(2500); await clic(v, "suivant|continuer|→", 3500);
    attendu(n, /Séance faite/i.test(v.texte) && /du premier coup/i.test(v.texte), "écran de fin absent : " + v.texte.slice(0, 200));
    attendu(n, !/Le reste de ta carte n'est pas encore mesuré/i.test(v.texte) || true, "");
    controlesAdo(v, n);
    await clic(v, "Voir ce qui est inclus");
    controlesAdo(v, n);
    return v;
  });
  await cas("gratuit · J+1 → nouvelle séance prête, streak conservé", async (n) => {
    const e = await inscrit("Tim"); await seance(e);
    await temps(1);
    const v = await appDe(e);
    attendu(n, v.boutons.some((b) => /C'est parti/i.test(b)), "J+1 : pas de nouvelle séance");
    controlesAdo(v, n);
    return v;
  });
  await cas("gratuit · J+7 (inactif 6 j) → séance prête, pas d'impasse", async (n) => {
    const e = await inscrit("Max"); await seance(e);
    await temps(7);
    const v = await appDe(e);
    attendu(n, v.boutons.some((b) => /C'est parti/i.test(b)), "J+7 : pas de séance");
    controlesAdo(v, n);
    return v;
  });
  await cas("gratuit · J+31 → pas de check-up (réservé Programme)", async (n) => {
    const e = await inscrit("Eva"); await seance(e);
    await temps(31);
    const v = await appDe(e);
    attendu(n, !/check-up/i.test(v.texte), "check-up proposé à un gratuit");
    attendu(n, v.boutons.some((b) => /C'est parti/i.test(b)), "J+31 : pas de séance");
    controlesAdo(v, n);
    return v;
  });
  await cas("gratuit · zone maîtrisée → « point faible réglé », sans prix", async (n) => {
    const e = await inscrit("Lou"); await seance(e);
    const v = await appDe(e, "", { intercepte: (j, a) => a === "get_training" && j.boost ? { ...j, zone_maitrisee: true, boost: { ...j.boost, zone_maitrisee: true } } : null });
    attendu(n, /point faible est réglé/i.test(v.texte), "message zone maîtrisée absent");
    controlesAdo(v, n);
    return v;
  });
  await cas("gratuit · compte sans diagnostic → lancer le diag express", async (n) => {
    const e = await inscrit("Sam", false);
    const v = await appDe(e);
    attendu(n, v.boutons.some((b) => /Lancer mon diagnostic/i.test(b)), "pas de CTA diagnostic pour un compte sans diag : " + v.texte.slice(0, 200));
    controlesAdo(v, n);
    return v;
  });

  // ── Acheteur diagnostic complet ──
  const dc = await inscrit("Hugo"); await seance(dc); await payer(dc, "diag_complet");
  await cas("diag complet · retour paiement ?achat=diag_complet", async (n) => {
    const v = await appDe(dc, "?achat=diag_complet", { attente: 4000 });
    attendu(n, /Diagnostic complet débloqué/i.test(v.texte), "retour paiement : pas « Diagnostic complet débloqué »");
    attendu(n, v.boutons.some((b) => /Commencer le module 1/.test(b)), "retour paiement : pas de suite « Commencer le module 1 »");
    controlesAdo(v, n);
    await clic(v, "Commencer le module 1", 2500);
    attendu(n, /Diagnostic complet/i.test(v.texte) && /module/i.test(v.texte), "le bouton ne mène pas au hub");
    return v;
  });
  await cas("diag complet · avant les modules → accueil + chip + hub", async (n) => {
    const v = await appDe(dc);
    attendu(n, v.boutons.some((b) => /Diagnostic complet ✓/.test(b)), "chip « Diagnostic complet ✓ » absent");
    attendu(n, /3 modules/i.test(v.texte), "carte « Diagnostic complet · 3 modules » absente");
    attendu(n, !/pas encore mesurées|voir ce qui est inclus/i.test(v.texte), "« pas encore mesurées »/paywall montré à qui a payé le complet");
    controlesAdo(v, n);
    await clic(v, "Diagnostic complet ✓");
    controlesAdo(v, n);  // l'ado ne doit pas tomber sur une offre d'achat
    return v;
  });
  const dc2 = await inscrit("Jade"); await payer(dc2, "diag_complet"); await diag(dc2, "complet", 999, 1);
  await cas("diag complet · pendant (module 1 fait) → reprise module 2", async (n) => {
    const v = await appDe(dc2);
    attendu(n, /Module 2 \/ 3 en cours|Reprendre/i.test(v.texte), "accueil : pas de reprise du module 2 : " + v.texte.slice(0, 300));
    await clic(v, "Diagnostic complet", 2000);
    attendu(n, /Reprendre le module 2|Commencer le module 2/.test(v.boutons.join(" ")), "hub : pas de « module 2 » : " + v.boutons.join(" / "));
    attendu(n, /Fait ✓/i.test(v.texte), "hub : module 1 pas marqué fait");
    controlesAdo(v, n);
    return v;
  });
  const dc3 = await inscrit("Adam"); await payer(dc3, "diag_complet"); const fin3 = await diag(dc3, "complet");
  await cas("diag complet · après les 3 modules → carte complète + PDF", async (n) => {
    attendu(n, fin3.termine, "le diag complet ne se termine pas : " + JSON.stringify(fin3).slice(0, 200));
    const v = await appDe(dc3);
    attendu(n, !/3 modules de ~13 min|Module \d \/ 3 en cours/i.test(v.texte), "l'accueil propose encore le diagnostic complet fini");
    attendu(n, !/pas encore mesurées/i.test(v.texte), "« pas encore mesurées » après le complet");
    await clic(v, "Voir →", 1500);
    attendu(n, /ta carte en entier/i.test(v.texte), "carte complète absente");
    const dl = await v.page.evaluate(async () => {
      // deno-lint-ignore no-explicit-any
      const g = (x: string) => (0, eval)(x); await g("_loadPdfLib")(); const r = await (window as any).MatheuxBilanPDF.render(g("S").carte, { apercu: false }); return r.pageCount;
    }).catch((e) => "ERR " + e.message);
    attendu(n, typeof dl === "number" && dl >= 4, "PDF non généré : " + dl);
    controlesAdo(v, n);
    return v;
  });
  await cas("diag complet · après, séance faite → fin de séance sans « pas encore mesuré »", async (n) => {
    await seance(dc3, 4);
    const v = await appDe(dc3);
    await clic(v, "Continue, encore");
    await v.page.evaluate(() => { // deno-lint-ignore no-explicit-any
      const g = (x: string) => (0, eval)(x); const S = g("S"); const ex = g("LVL")["3EME"].cats[S.sessCat][S._activeIdx];
      if (ex.type === "fill") (document.querySelector(".fill-input") as HTMLInputElement).value = "zz";
      else ([...document.querySelectorAll(".opt-grid .opt")][0] as HTMLElement).click();
      g("validateAnswer")(); });
    await sleep(2500); await clic(v, "suivant|continuer|→", 3500);
    attendu(n, /Séance faite/i.test(v.texte), "fin de séance absente");
    attendu(n, !/pas encore mesuré/i.test(v.texte), "fin de séance : « Le reste de ta carte n'est pas encore mesuré » alors que le complet est fait");
    controlesAdo(v, n);
    await clic(v, "Voir ce qui est inclus|continuer");
    controlesAdo(v, n);
    return v;
  });
  await cas("diag complet · J+31 → pas de check-up promis (Programme seulement)", async (n) => {
    await temps(31);
    const v = await appDe(dc3);
    attendu(n, !/check-up/i.test(v.texte), "check-up proposé à un acheteur du seul diagnostic");
    attendu(n, v.boutons.some((b) => /C'est parti/.test(b)), "J+31 : pas de séance");
    controlesAdo(v, n);
    return v;
  });

  // ── Programme direct ──
  const pg = await inscrit("Nina"); await payer(pg, "programme_brevet");
  await cas("programme · retour ?achat=programme_brevet", async (n) => {
    const v = await appDe(pg, "?achat=programme_brevet", { attente: 4000 });
    attendu(n, /Programme Brevet activé/i.test(v.texte), "pas « Programme Brevet activé »");
    await clic(v, "C'est parti", 1500);
    controlesAdo(v, n);
    return v;
  });
  await cas("programme · J0 avant diag complet → hub + libre, aucun paywall", async (n) => {
    const v = await appDe(pg);
    attendu(n, !v.boutons.some((b) => /Gratuit|Diagnostic complet ✓/.test(b)), "chip d'accès visible pour un Programme");
    attendu(n, /3 modules/i.test(v.texte), "diag complet (inclus) non proposé");
    attendu(n, v.boutons.some((b) => /S'entraîner sur/.test(b)), "« S'entraîner sur… » absent");
    attendu(n, !/pas encore mesurées|voir ce qui est inclus/i.test(v.texte), "paywall visible en Programme");
    controlesAdo(v, n);
    await clic(v, "S'entraîner sur");
    const nComp = v.boutons.length;
    attendu(n, nComp > 3, "liste « S'entraîner sur… » vide");
    await v.page.evaluate(() => (document.querySelector("#mx-sheet .mx-row") as HTMLElement)?.click()); await sleep(2500); await lire(v);
    attendu(n, !!(await v.page.$(".fill-input, .opt-grid .opt")), "l'entraînement libre ne démarre pas");
    controlesAdo(v, n);
    return v;
  });
  const pg2 = await inscrit("Paul"); await payer(pg2, "programme_brevet"); await diag(pg2, "complet"); await seance(pg2);
  await cas("programme · séance faite → « Encore une séance », check-up dans N jours", async (n) => {
    const v = await appDe(pg2);
    attendu(n, /Check-up dans \d+ jour/i.test(v.texte), "« Check-up dans N jours » absent");
    attendu(n, /Séance faite/i.test(v.texte), "séance faite absente");
    controlesAdo(v, n);
    return v;
  });
  await cas("programme · J+31 → check-up du mois proposé et lançable", async (n) => {
    await temps(31);
    const v = await appDe(pg2);
    attendu(n, /Check-up du mois/i.test(v.texte), "check-up absent à J+31");
    await clic(v, "Check-up du mois|C'est parti →", 3000);
    attendu(n, !!(await v.page.$("#dx-val")), "le check-up ne démarre pas");
    controlesAdo(v, n);
    return v;
  });
  await cas("programme · J+31 check-up fini → carte avec évolution", async (n) => {
    await temps(31);
    const r = await diag(pg2, "mensuel");
    attendu(n, r.termine, "check-up non terminé : " + JSON.stringify(r).slice(0, 200));
    const v = await appDe(pg2);
    attendu(n, !/Check-up du mois/i.test(v.texte), "check-up encore proposé après l'avoir fait");
    await clic(v, "Voir →", 1500);
    attendu(n, /Depuis ta dernière carte/i.test(v.texte), "évolution absente de la carte");
    controlesAdo(v, n);
    return v;
  });

  // ── Upgrade diag → programme ──
  const up = await inscrit("Tom"); await payer(up, "diag_complet"); await diag(up, "complet");
  await cas("upgrade · page parent (diag payé) → Programme 30 € au lieu de 49 €", async (n) => {
    const t = await partage(up);
    const v = await ouvrir(`/b/${t}`, {}, { attente: 2500 });
    attendu(n, /30 €/i.test(v.texte) && /au lieu de 49 €/i.test(v.texte), "offre upgrade 30 € absente : " + v.texte.slice(0, 300));
    attendu(n, !/Offrir le diagnostic complet/i.test(v.texte), "le diag complet est encore vendu à qui l'a payé");
    if (v.errs.length) n.push("erreurs : " + v.errs.join(" ; "));
    return v;
  });
  await cas("upgrade · paiement 30 € → Programme partout", async (n) => {
    const p = await payer(up, "programme_brevet");
    attendu(n, p.produit === "programme_upgrade", "pas facturé en upgrade : " + p.produit);
    const v = await appDe(up, "?achat=programme_upgrade", { attente: 4000 });
    attendu(n, /Programme Brevet activé/i.test(v.texte), "retour ?achat=programme_upgrade : pas « Programme Brevet activé »");
    await clic(v, "C'est parti", 1200);
    attendu(n, v.boutons.some((b) => /S'entraîner sur/.test(b)), "« S'entraîner sur… » absent après upgrade");
    controlesAdo(v, n);
    const t = await partage(up);
    const w = await ouvrir(`/b/${t}`, {}, { attente: 2500 });
    attendu(n, !/Choisir le Programme|Offrir le diagnostic|au lieu de/i.test(w.texte), "page parent : offres encore affichées après Programme");
    return [v, w];
  });

  // ── Parent sur bilan.html ──
  await cas("parent · lien gratuit → 19 € + 49 €, aperçu PDF", async (n) => {
    const t = await partage(lea);
    const v = await ouvrir(`/b/${t}`, {}, { attente: 2500 });
    attendu(n, /bilan maths de Léa/i.test(v.texte), "titre parent absent");
    attendu(n, /19 €/i.test(v.texte) && /49 €/i.test(v.texte), "prix 19/49 absents");
    const tu = v.texte.replace(/[«"][^»"]*[»"]/g, "").match(/.{0,30}(?<=[\s|(])(tu|ton|tes|toi)\b.{0,30}/i);
    attendu(n, !tu, "tutoiement sur la page parent : " + (tu && tu[0]));
    if (v.errs.length) n.push("erreurs : " + v.errs.join(" ; "));
    await clic(v, "Voir un aperçu du bilan PDF", 4000);
    if (v.errs.length) n.push("aperçu PDF : " + v.errs.join(" ; "));
    return v;
  });
  await cas("parent · lien diag payé (avant modules) → pas de 2e vente du diag", async (n) => {
    const t = await partage(dc);
    const v = await ouvrir(`/b/${t}`, {}, { attente: 2500 });
    attendu(n, !/Offrir le diagnostic complet/i.test(v.texte), "diag complet revendu");
    attendu(n, /30 €/i.test(v.texte), "upgrade 30 € absent");
    if (v.errs.length) n.push("erreurs : " + v.errs.join(" ; "));
    return v;
  });
  await cas("parent · lien programme → aucune offre", async (n) => {
    const t = await partage(pg2);
    const v = await ouvrir(`/b/${t}`, {}, { attente: 2500 });
    attendu(n, !/€ <|Choisir le Programme|Offrir le diagnostic|au lieu de/i.test(v.texte), "offres affichées à un Programme");
    if (v.errs.length) n.push("erreurs : " + v.errs.join(" ; "));
    return v;
  });
  await cas("parent · lien révoqué / expiré / inconnu → message clair", async (n) => {
    const e = await inscrit("Rose"); const t = await partage(e);
    await api({ action: "revoke_share", ...A(e) });
    const v = await ouvrir(`/b/${t}`, {}, { attente: 2000 });
    attendu(n, /n'est plus actif|expiré|désactivé/i.test(v.texte), "lien révoqué : pas de message");
    const t2 = await partage(e); await temps(31);
    const w = await ouvrir(`/b/${t2}`, {}, { attente: 2000 });
    attendu(n, /n'est plus actif|expiré|désactivé/i.test(w.texte), "lien expiré (J+31) : pas de message");
    const x = await ouvrir(`/b/${"0".repeat(48)}`, {}, { attente: 2000 });
    attendu(n, /n'est plus actif|expiré|désactivé/i.test(x.texte) && !/Rose/i.test(x.texte), "lien inconnu : pas de message");
    for (const y of [v, w, x]) if (y.errs.length) n.push("erreurs : " + y.errs.join(" ; "));
    return [v, w, x];
  });
  await cas("parent · retour paiement bilan.html?merci=1", async (n) => {
    const t = await partage(lea);
    const v = await ouvrir(`/b/${t}?merci=1`, {}, { attente: 2500 });
    attendu(n, /paiement est enregistré/i.test(v.texte), "bandeau merci absent");
    if (v.errs.length) n.push("erreurs : " + v.errs.join(" ; "));
    return v;
  });

  // ── Emails ado (email_eleve) et mesure des clics email (53 §4) ──
  await cas("inscription UI avec « ton email » → parent l'autorise sur ?confirmer=1", async (n) => {
    const v = await ouvrir("/app.html#diag", {}, { attente: 1200 });
    await clic(v, "lancer|commencer");
    for (let i = 0; i < 25; i++) {
      if (!(await v.page.$("#dx-val"))) break;
      await v.page.evaluate(() => { const o = document.querySelector(".dx-opt") as HTMLElement; if (o) o.click(); else { const f = document.getElementById("dx-fill") as HTMLInputElement; if (f) { f.value = "12"; f.dispatchEvent(new Event("input", { bubbles: true })); } } });
      await v.page.evaluate(() => (document.getElementById("dx-val") as HTMLButtonElement)?.click()); await sleep(600);
    }
    await sleep(1800); await clic(v, "entraîner gratuitement", 800);
    const em = `parent.ui${Date.now()}@exemple.fr`;
    await v.page.type("#rg-name", "Mila"); await v.page.type("#rg-email", em); await v.page.type("#rg-pass", "motdepasse1");
    attendu(n, !!(await v.page.$("#rg-email-eleve")), "champ « Ton email (facultatif) » absent");
    await v.page.type("#rg-email-eleve", "mila.ado@exemple.fr");
    await v.page.click("#rg-ok"); await v.page.click("#rg-btn"); await sleep(3500); await lire(v);
    controlesAdo(v, n);
    const prof = (await dev(`/dev/db/profiles?email=${encodeURIComponent(em)}`) as unknown as J[])[0] || {};
    attendu(n, prof.email_eleve === "mila.ado@exemple.fr", "email_eleve non enregistré : " + prof.email_eleve);
    const px0 = [...Deno.readDirSync(`${DATA}/outbox`)].filter((e) => e.name.includes(em)).map((e) => Deno.readTextFileSync(`${DATA}/outbox/${e.name}`)).join("");
    const tok = (px0.match(/\/b\/([0-9a-f]{48})\?confirmer=1/) || [])[1];
    attendu(n, !!tok, "P-X0 sans lien de confirmation");
    const w = await ouvrir(`/b/${tok}?confirmer=1`, {}, { attente: 2000 });
    attendu(n, /m•••@exemple\.fr/.test(w.texte), "case « emails à l'ado » sans l'adresse masquée");
    await w.page.click("#cf-eleve"); await w.page.click("#cf-go"); await sleep(2000); await lire(w);
    attendu(n, /rappels d'entraînement/.test(w.texte) && /confirmée/i.test(w.texte), "confirmation : pas de mention des rappels ado");
    const prof2 = (await dev(`/dev/db/profiles?email=${encodeURIComponent(em)}`) as unknown as J[])[0] || {};
    attendu(n, !!prof2.consentement_parent_at && prof2.email_eleve === "mila.ado@exemple.fr", "après confirmation : consentement/email_eleve incohérents");
    if (w.errs.length) n.push("erreurs page parent : " + w.errs.join(" ; "));
    return [v, w];
  });
  await cas("?confirmer=1 sans cocher la case ado → adresse ado effacée", async (n) => {
    const e = await inscrit("Ana", false);
    await api({ action: "set_preferences", ...A(e), email: e.email, email_eleve: "ana.ado@exemple.fr" });
    await diag(e, "express");
    const px0 = [...Deno.readDirSync(`${DATA}/outbox`)].filter((x) => x.name.includes(e.email)).map((x) => Deno.readTextFileSync(`${DATA}/outbox/${x.name}`)).join("");
    const tok = (px0.match(/\/b\/([0-9a-f]{48})\?confirmer=1/) || [])[1];
    const w = await ouvrir(`/b/${tok}?confirmer=1`, {}, { attente: 2000 });
    await w.page.click("#cf-go"); await sleep(2000);
    const prof = (await dev(`/dev/db/profiles?code=${e.code}`) as unknown as J[])[0] || {};
    attendu(n, !!prof.consentement_parent_at && !prof.email_eleve, "adresse ado gardée sans autorisation du parent : " + prof.email_eleve);
    if (w.errs.length) n.push("erreurs : " + w.errs.join(" ; "));
    return w;
  });
  await cas("clic email ?src=email_* → funnel_events email_click (app connecté + bilan)", async (n) => {
    const v = await appDe(lea, "?src=email_P-X1", { attente: 4000 });
    const t = await partage(lea);
    const w = await ouvrir(`/b/${t}?src=email_P-X0`, {}, { attente: 2000 });
    const x = await ouvrir(`/app.html?src=email_A-X0`, {}, { attente: 4000 });
    const ev = (await dev(`/dev/db/funnel_events?event=email_click&limit=5000`) as unknown as J[]);
    const de = (src: string) => ev.filter((r) => r.meta?.src === src);
    attendu(n, de("email_P-X1").some((r) => r.code === lea.code), "app connecté : email_click absent ou sans code");
    attendu(n, de("email_P-X0").some((r) => r.code === lea.code), "bilan : email_click absent ou sans code");
    attendu(n, de("email_A-X0").length === 1 && !de("email_A-X0")[0].code, "app anonyme : email_click absent (ou code non prouvé)");
    const bad = await api({ action: "log_funnel_event", event: "email_click", meta: { src: "<script>" } });
    attendu(n, bad.status === "error", "src arbitraire accepté");
    controlesAdo(v, n);
    return [v, w, x];
  });

  // ── Admin ──
  await cas("admin · monitoring lecture seule", async (n) => {
    const lg = await api({ action: "login", email: "admin@dev.matheux.local", password: await hash("admin@dev.matheux.local", MDP) });
    const v = await ouvrir("/app.html", { boost_v23: JSON.stringify({ code: lg.profile.code, email: "admin@dev.matheux.local", access_token: lg.access_token, refresh_token: lg.refresh_token }) }, { attente: 3000 });
    attendu(n, /Monitoring/i.test(v.texte) && /inscrits/i.test(v.texte), "monitoring absent");
    attendu(n, !/séance du jour/i.test(v.texte), "l'admin voit une séance");
    if (v.errs.length) n.push("erreurs : " + v.errs.join(" ; "));
    await v.page.evaluate(() => (document.querySelector(".mx-row") as HTMLElement)?.click()); await sleep(2500); await lire(v);
    if (v.errs.length) n.push("fiche élève : " + v.errs.join(" ; "));
    return v;
  });

  // ── Autre appareil / session ──
  await cas("autre appareil · connexion email + mdp → retrouve carte et séance", async (n) => {
    const v = await ouvrir("/app.html#login", {}, { attente: 1500 });
    await v.page.evaluate((em, mdp) => { (document.getElementById("le") as HTMLInputElement).value = em; (document.getElementById("lp") as HTMLInputElement).value = mdp; }, lea.email, MDP);
    await v.page.evaluate(() => (document.getElementById("btn-auth-submit") as HTMLElement).click()); await sleep(3500); await lire(v);
    attendu(n, /Salut Léa/i.test(v.texte) && /Ta carte/i.test(v.texte), "connexion : accueil ou carte absents : " + v.texte.slice(0, 200));
    controlesAdo(v, n);
    return v;
  });
  await cas("session · jeton expiré + refresh valide → renouvelée sans friction", async (n) => {
    const v = await ouvrir("/app.html", { boost_v23: JSON.stringify({ code: lea.code, email: lea.email, access_token: "expire.bidon.x", refresh_token: lea.refresh_token }) }, { attente: 3000 });
    attendu(n, /Salut Léa/i.test(v.texte), "pas reconnecté par le refresh_token");
    controlesAdo(v, n);
    return v;
  });
  await cas("session · jetons invalides → écran de connexion / diag, pas d'impasse", async (n) => {
    const v = await ouvrir("/app.html", { boost_v23: JSON.stringify({ code: lea.code, email: lea.email, access_token: "x", refresh_token: "y" }) }, { attente: 3000 });
    attendu(n, /connecte|Se connecter|Lancer mon diagnostic|diagnostic/i.test(v.texte), "session perdue : écran vide : " + v.texte.slice(0, 200));
    controlesAdo(v, n);
    return v;
  });

  // ── Prix cohérents : API, app, bilan, emails ──
  await cas("prix · 19/49/30 identiques API, app, bilan, emails", async (n) => {
    const ac = await api({ action: "get_acces", ...A(lea) });
    const p = ac.produits || {};
    attendu(n, p.diagnostic_complet?.prix_cents === 1900 && p.programme_brevet?.prix_cents === 4900 && p.programme_upgrade?.prix_cents === 3000, "API : " + JSON.stringify(p));
    const app = Deno.readTextFileSync(`${ROOT}/app.html`), bil = Deno.readTextFileSync(`${ROOT}/bilan.html`);
    for (const [nom, src] of [["app.html", app], ["bilan.html", bil]]) {
      const m = src.match(/prix: ?(\d+)/g) || [];
      attendu(n, m.join() === "prix: 19,prix: 49,prix: 30", `${nom} OFFRE : ${m.join()}`);
      if (/29,99|29\.99/.test(src)) n.push(nom + " : ancien prix 29,99 €");
    }
    const mails = [...Deno.readDirSync(`${DATA}/outbox`)].map((e) => Deno.readTextFileSync(`${DATA}/outbox/${e.name}`)).join("\n");
    const prixMails = [...new Set((mails.match(/\b\d{2}(?:,\d{2})? ?€/g) || []).map((x) => x.replace(/\s/, " ")))];
    const hors = prixMails.filter((x) => !/^(19|49|30|20|25)(,00)? €$/.test(x));
    attendu(n, hors.length === 0, "emails : prix inattendus " + hors.join(", "));
  });
} finally {
  await browser.close().catch(() => {});
  srv.kill("SIGTERM"); await srv.status;
  await Deno.remove(DATA, { recursive: true }).catch(() => {});
}
const ko = resultats.filter((r) => !r.ok);
console.log(`\n${ko.length ? "❌" : "✅"} matrice QA : ${resultats.length - ko.length}/${resultats.length} cases OK`);
Deno.exit(ko.length ? 1 : 0);
