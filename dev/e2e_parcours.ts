// Matheux — e2e « vrai visiteur » : landing → diag express invité → carte partielle → inscription →
// séance du jour → fin de séance. Vérifie surtout que la séance sert 5 exos quel que soit le point faible.
// Lancer (serveur de dev déjà démarré) : deno run -A dev/e2e_parcours.ts [BASE] [N]
//   BASE par défaut http://localhost:8787 · N = nombre de parcours (reset de la base entre chaque)
import puppeteer from "npm:puppeteer-core@23.11.1";

const BASE = Deno.args[0] || "http://localhost:8787";
const N = Number(Deno.args[1] || 3);
const CHROME = Deno.env.get("CHROME") || "/usr/bin/google-chrome";
const LENT = Number(Deno.env.get("E2E_LENT") || 1); // ×3 contre la prod (latence réseau)
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms * LENT));
let ko = 0;

for (let run = 1; run <= N; run++) {
  if (/localhost|127\.0\.0\.1/.test(BASE)) await fetch(BASE + "/dev/reset", { method: "POST" });
  const b = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--no-sandbox", "--disable-gpu"] });
  const p = await b.newPage();
  await p.setViewport({ width: 375, height: 800 });
  const errs: string[] = [];
  p.on("pageerror", (e) => errs.push("PAGEERROR " + (e as Error).message));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.text())) errs.push("CONSOLE " + m.text()); });
  const clic = (re: string) => p.evaluate((re) => {
    const b = [...document.querySelectorAll("button")].find((x) => new RegExp(re, "i").test((x as HTMLElement).innerText) && (x as HTMLElement).offsetParent);
    if (b) { (b as HTMLElement).click(); return true; } return false;
  }, re);
  try {
    await p.goto(BASE + "/", { waitUntil: "networkidle2" });
    await p.evaluate(() => { localStorage.clear(); localStorage.setItem("mx_cookie_consent", "refused"); });
    const href = await p.$eval('a[href*="#diag"]', (a) => a.getAttribute("href"));
    await p.goto(BASE + href, { waitUntil: "networkidle2" }); await sleep(1500);
    await clic("lancer|commencer"); await sleep(1500);
    let nq = 0;
    for (; nq < 25; nq++) {
      const st = await p.evaluate(() => {
        // deno-lint-ignore no-explicit-any
        const DX = (window as any).DX;
        return DX && DX.q && document.getElementById("dx-val") ? (DX.q.type === "fill" ? "fill" : "opt") : "none";
      });
      if (st === "none") break;
      if (st === "fill") await p.type("#dx-fill", nq % 3 === 0 ? "zz" : "12");
      else await p.evaluate((k) => { const o = [...document.querySelectorAll(".dx-opt")]; (o[k % o.length] as HTMLElement).click(); }, nq);
      await p.click("#dx-val"); await sleep(900);
    }
    await sleep(1200);
    await clic("entraîner gratuitement"); await sleep(800);
    await p.type("#rg-name", "Zoé"); await p.type("#rg-email", Deno.env.get("E2E_EMAIL") || `parent.run${run}@exemple.fr`); await p.type("#rg-pass", "motdepasse1");
    await p.click("#rg-ok"); await p.click("#rg-btn"); await sleep(3500);
    const accueil = await p.evaluate(() => document.body.innerText.replace(/\n+/g, " | "));
    const m = accueil.match(/TA SÉANCE DU JOUR \| ([^|]+)\| (\d+) exos?/);
    const annonce = m ? Number(m[2]) : 0;
    await clic("^C'est parti"); await sleep(1500);
    let faits = 0;
    for (; faits < 6; faits++) {
      const ok = await p.evaluate(() => !!document.querySelector(".fill-input, .opt-grid .opt"));
      if (!ok) break;
      await p.evaluate((right) => {
        // deno-lint-ignore no-explicit-any
        const g = (n: string) => (0, eval)(n); // LVL/S sont des globales lexicales (let), pas des propriétés de window
        const S = g("S"); const ex = g("LVL")["3EME"].cats[S.sessCat][S._activeIdx];
        if (ex.type === "fill") { (document.querySelector(".fill-input") as HTMLInputElement).value = right ? String(ex.a).replace(/\$/g, "") : "zz"; }
        else { const t = right ? ex.options.indexOf(ex.a) : (ex.options.indexOf(ex.a) + 1) % ex.options.length; ([...document.querySelectorAll(".opt-grid .opt")].find((x) => +(x as HTMLElement).dataset.oi! === t) as HTMLElement).click(); }
        g("validateAnswer")();
      }, faits % 2 === 0);
      await sleep(2200);
      await p.evaluate(() => { const b = [...document.querySelectorAll("button")].find((x) => /suivant|continuer|→/i.test((x as HTMLElement).innerText) && (x as HTMLElement).offsetParent && !/valider/i.test((x as HTMLElement).innerText)); if (b) (b as HTMLElement).click(); });
      await sleep(900);
    }
    const fin = await p.evaluate(() => /SÉANCE FAITE/i.test(document.body.innerText));
    const bon = annonce === 5 && faits === 5 && fin && errs.length === 0 && nq >= 10;
    if (!bon) ko++;
    console.log(`${bon ? "✅" : "❌"} parcours ${run} : ${nq} q de diag · point faible « ${m ? m[1].trim() : "?"} » · séance ${annonce} exos annoncés, ${faits} faits · fin ${fin ? "ok" : "absente"}${errs.length ? " · " + errs.slice(0, 2).join(" ; ") : ""}`);
  } catch (e) {
    ko++; console.log(`❌ parcours ${run} : ${(e as Error).message}`);
  } finally { await b.close(); }
}
console.log(ko ? `❌ ${ko}/${N} parcours KO` : `✅ ${N}/${N} parcours OK (5 exos par séance)`);
Deno.exit(ko ? 1 : 0);
