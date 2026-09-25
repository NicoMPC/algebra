// ════════════════════════════════════════════════════════════
//  Matheux — test navigateur minimal (Chrome headless via puppeteer-core, cache Deno hors repo)
//  landing → clic « Faire le diagnostic gratuit » → l'app affiche la 1re question du diagnostic,
//  sans erreur console ni erreur JS. Serveur isolé (port 8798, base temporaire).
//  Usage : deno run -A dev/browser_test.ts   (CHROME=/chemin/chrome pour changer de navigateur)
//  Capture : /tmp/matheux-browser-test.png (ou $BROWSER_SHOT)
// ════════════════════════════════════════════════════════════
/// <reference lib="dom" />
import puppeteer from "npm:puppeteer-core@23.11.1";

const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");
const PORT = 8798, BASE = `http://localhost:${PORT}`;
const DATA = await Deno.makeTempDir({ dir: "/tmp", prefix: "matheux-browser-" }); // chemin court : Chrome limite la longueur du socket
const CHROME = Deno.env.get("CHROME") || "/usr/bin/google-chrome";
const FLAGS = ["run", "--allow-net", "--allow-read", "--allow-write", "--allow-env", "--allow-run=python3", "--allow-sys", "--no-prompt"];
const env = { DEV_DATA_DIR: DATA, DEV_QUIET: "1" };
const SHOT = Deno.env.get("BROWSER_SHOT") || "/tmp/matheux-browser-test.png";

const seed = await new Deno.Command(Deno.execPath(), { args: [...FLAGS, `${ROOT}/dev/server.ts`, "reset"], env, stdout: "null", stderr: "piped" }).output();
if (!seed.success) { console.error(new TextDecoder().decode(seed.stderr)); Deno.exit(1); }
const srv = new Deno.Command(Deno.execPath(), { args: [...FLAGS, `${ROOT}/dev/server.ts`, "serve", "--port", String(PORT)], env, stdout: "null", stderr: "null" }).spawn();
for (let i = 0; i < 60; i++) { try { if ((await fetch(`${BASE}/dev/health`)).ok) break; } catch { /* */ } await new Promise((r) => setTimeout(r, 250)); }

const erreurs: string[] = [];
const questions: string[] = [];
let ok = false;
// deno-lint-ignore no-explicit-any
let sw: any = null;
// deno-lint-ignore no-explicit-any
let confirmer: any = null;
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--no-sandbox", "--disable-gpu", `--user-data-dir=${DATA}/chrome`] });
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 844 });
  page.on("console", (m) => { if (m.type() === "error") erreurs.push("console: " + m.text()); });
  page.on("pageerror", (e) => erreurs.push("pageerror: " + String((e as Error).message || e)));
  page.on("requestfailed", (r) => { if (r.url().startsWith(BASE)) erreurs.push("requête échouée: " + r.url()); });
  page.on("response", async (r) => {
    if (!r.url().startsWith(BASE + "/api")) return;
    try {
      const j = await r.json();
      if (j?.question?.q) questions.push(String(j.question.q));
      for (const e of (j?.exos || [])) if (e?.q) questions.push(String(e.q)); // ancien flux generate_diagnostic
    } catch { /* */ }
  });

  await page.goto(BASE + "/", { waitUntil: "networkidle2" });
  const cta = await page.$('a[data-cta="hero"]') || await page.$('a[href*="#diag"]');
  if (!cta) throw new Error("CTA « Faire le diagnostic gratuit » introuvable sur la landing");
  await Promise.all([page.waitForNavigation({ waitUntil: "networkidle2" }), cta.click()]);
  console.log("  → " + page.url());

  // L'app peut demander d'abord un écran d'accueil (prénom, classe, « C'est parti ») : on avance
  // génériquement jusqu'à ce que le texte d'une question servie par l'API soit affiché.
  const extrait = (q: string) => q.replace(/\$[^$]*\$/g, " ").replace(/\\[a-z]+/g, " ").replace(/\s+/g, " ").trim().split(" ").filter((w) => w.length > 3).slice(0, 3).join(" ");
  for (let etape = 0; etape < 12 && !ok; etape++) {
    await new Promise((r) => setTimeout(r, 900));
    const texte: string = await page.evaluate(() => document.body.innerText.replace(/\s+/g, " "));
    // mots un par un : KaTeX intercale la formule rendue entre les mots (question différente à chaque run en invité)
    if (questions.some((q) => { const x = extrait(q); return x && x.split(" ").every((w) => texte.includes(w)); })) { ok = true; break; }
    await page.evaluate(() => {
      const vis = (el: Element) => { const r = (el as HTMLElement).getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== "hidden" && s.display !== "none"; };
      for (const i of Array.from(document.querySelectorAll('input[type="text"],input:not([type])'))) if (vis(i) && !(i as HTMLInputElement).value) { (i as HTMLInputElement).value = "Test"; i.dispatchEvent(new Event("input", { bubbles: true })); }
      const btns = Array.from(document.querySelectorAll("button, [role=button], .btn")).filter(vis) as HTMLElement[];
      const pref = btns.find((b) => /3e|3ème|3EME/i.test(b.innerText) && b.innerText.length < 20) ||
        btns.find((b) => /(commencer|c'est parti|démarrer|go|continuer|suivant|lancer)/i.test(b.innerText));
      pref?.click();
    });
  }
  await page.screenshot({ path: SHOT, fullPage: false });

  // ── Service worker réel (sw.js, servi par /sw.js?reel=1) : install OK, anciens caches supprimés,
  //    pages HTML en réseau d'abord (jamais une vieille landing servie depuis le cache).
  const p2 = await browser.newPage();
  await p2.goto(BASE + "/offline.html", { waitUntil: "load" });
  sw = await p2.evaluate(async () => {
    await caches.open("matheux-v13").then((c) => c.put("/", new Response("VIEILLE LANDING", { headers: { "Content-Type": "text/html" } })));
    const reg = await navigator.serviceWorker.register("/sw.js?reel=1", { scope: "/" });
    const w = reg.installing || reg.waiting || reg.active;
    const etat = await new Promise<string>((res) => {
      if (!w) return res("aucun worker");
      if (w.state === "activated") return res("activated");
      w.addEventListener("statechange", () => { if (w.state === "activated" || w.state === "redundant") res(w.state); });
      setTimeout(() => res("timeout:" + w.state), 10000);
    });
    const keys = await caches.keys();
    const n = keys.includes("matheux-v14") ? (await (await caches.open("matheux-v14")).keys()).length : 0;
    // piège : une vieille landing dans le cache courant ne doit PAS être servie (réseau d'abord)
    await (await caches.open("matheux-v14")).put("/", new Response("VIEILLE LANDING", { headers: { "Content-Type": "text/html" } }));
    return { etat, keys, n };
  });
  await p2.reload({ waitUntil: "load" }); // la page est maintenant contrôlée par le SW
  const controle = await p2.evaluate(() => !!navigator.serviceWorker.controller);
  const r = await p2.goto(BASE + "/", { waitUntil: "load" });
  const landing = await p2.evaluate(() => document.body.innerText.slice(0, 200));
  sw = { ...sw, controle, landingStatus: r?.status(), vieille: /VIEILLE LANDING/.test(landing) };

  // ── bilan.html?confirmer=1 : carte de confirmation (vouvoiement), clic → confirm_parent → confirmé ──
  const px0 = [...Deno.readDirSync(`${DATA}/outbox`)].filter((e) => e.name.includes("tom@exemple.fr") && e.name.includes("bilan_maths"))
    .map((e) => Deno.readTextFileSync(`${DATA}/outbox/${e.name}`))[0] || "";
  const tokC = (px0.match(/\/b\/([0-9a-f]{48})\?confirmer=1/) || [])[1];
  const p3 = await browser.newPage();
  p3.on("pageerror", (e) => erreurs.push("pageerror bilan: " + String((e as Error).message || e)));
  await p3.goto(`${BASE}/b/${tokC}?confirmer=1`, { waitUntil: "networkidle2" });
  const avantClic = await p3.evaluate(() => ({ form: !document.getElementById("cf-form")!.hidden, titre: document.getElementById("cf-t")!.textContent }));
  await p3.click("#cf-go");
  await p3.waitForFunction(() => !document.getElementById("cf-ok")!.hidden, { timeout: 8000 }).catch(() => {});
  const apres = await p3.evaluate(() => ({ ok: !document.getElementById("cf-ok")!.hidden, txt: document.getElementById("cf-ok")!.innerText, bilan: !document.getElementById("st-ok")!.hidden }));
  const p4 = await browser.newPage();
  await p4.goto(`${BASE}/b/${"0".repeat(48)}?confirmer=1`, { waitUntil: "networkidle2" });
  const expire = await p4.evaluate(() => !document.getElementById("cf-exp")!.hidden);
  confirmer = { tokC: !!tokC, avantClic, apres, expire };
} finally {
  await browser.close();
  srv.kill("SIGTERM"); await srv.status;
  await Deno.remove(DATA, { recursive: true }).catch(() => {});
}
const bruit = (e: string) => /favicon|googletagmanager|google-analytics|fonts\.g/.test(e);
const vraies = erreurs.filter((e) => !bruit(e));
console.log(ok ? "  ✅ 1re question du diagnostic affichée" : "  ❌ aucune question du diagnostic affichée (questions reçues : " + questions.length + ")");
console.log(vraies.length ? "  ❌ erreurs :\n     " + vraies.join("\n     ") : "  ✅ aucune erreur console / JS");
const swOk = sw && sw.etat === "activated" && !sw.keys.includes("matheux-v13") && sw.keys.includes("matheux-v14") && sw.n >= 6 && sw.controle && sw.landingStatus === 200 && !sw.vieille;
console.log(swOk ? `  ✅ sw.js : install + activation OK (${sw.n} ressources en cache), ancien cache v13 supprimé, landing servie par le réseau`
  : "  ❌ sw.js : " + JSON.stringify(sw));
const cfOk = confirmer && confirmer.tokC && confirmer.avantClic.form && /Tom/.test(confirmer.avantClic.titre) && confirmer.apres.ok && /confirmée/.test(confirmer.apres.txt) && confirmer.apres.bilan && confirmer.expire;
console.log(cfOk ? "  ✅ bilan.html?confirmer=1 : formulaire, clic → « inscription confirmée », bilan affiché ; lien invalide → message d'erreur"
  : "  ❌ bilan.html?confirmer=1 : " + JSON.stringify(confirmer));
console.log("  capture : " + SHOT);
Deno.exit(ok && !vraies.length && swOk && cfOk ? 0 : 1);
