// ════════════════════════════════════════════════════════════
//  Matheux — test navigateur minimal (Chrome headless via puppeteer-core, cache Deno hors repo)
//  landing → clic « Faire le diagnostic gratuit » → l'app affiche la 1re question du diagnostic,
//  sans erreur console ni erreur JS. Serveur isolé (port 8798, base temporaire).
//  Usage : deno run -A dev/browser_test.ts   (CHROME=/chemin/chrome pour changer de navigateur)
//  Capture : /tmp/matheux-browser-test.png (ou $BROWSER_SHOT)
// ════════════════════════════════════════════════════════════
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
} finally {
  await browser.close();
  srv.kill("SIGTERM"); await srv.status;
  await Deno.remove(DATA, { recursive: true }).catch(() => {});
}
const bruit = (e: string) => /favicon|googletagmanager|google-analytics|fonts\.g/.test(e);
const vraies = erreurs.filter((e) => !bruit(e));
console.log(ok ? "  ✅ 1re question du diagnostic affichée" : "  ❌ aucune question du diagnostic affichée (questions reçues : " + questions.length + ")");
console.log(vraies.length ? "  ❌ erreurs :\n     " + vraies.join("\n     ") : "  ✅ aucune erreur console / JS");
console.log("  capture : " + SHOT);
Deno.exit(ok && !vraies.length ? 0 : 1);
