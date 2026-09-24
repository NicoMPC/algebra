// ════════════════════════════════════════════════════════════
//  Matheux — smoke test du backend de dev (HTTP, bout en bout)
//  Démarre un serveur ISOLÉ (port 8799, base temporaire : ne touche pas dev/data/), le seed,
//  puis déroule le parcours : inscription → login → diagnostic express (15 q) → carte →
//  entraînement + save_score → partage parent → paiement simulé → droits premium.
//  Usage : deno run -A dev/smoke_test.ts   (ou ./matheux.sh test)
// ════════════════════════════════════════════════════════════
const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");
const PORT = Number(Deno.env.get("SMOKE_PORT") || 8799);
const BASE = `http://localhost:${PORT}`;
const DATA = await Deno.makeTempDir({ prefix: "matheux-smoke-" });
const DENO = Deno.execPath();
const FLAGS = ["run", "--allow-net", "--allow-read", "--allow-write", "--allow-env", "--allow-run=python3", "--allow-sys", "--no-prompt"];
const env = { DEV_DATA_DIR: DATA, DEV_PORT: String(PORT), DEV_QUIET: "1" };

let ok = 0, ko = 0;
function check(nom: string, cond: unknown, info?: unknown) {
  if (cond) { ok++; console.log("  ✅", nom); }
  else { ko++; console.log("  ❌", nom, info !== undefined ? JSON.stringify(info).slice(0, 400) : ""); }
}
async function api(p: Record<string, unknown>) {
  const r = await fetch(`${BASE}/api`, { method: "POST", body: JSON.stringify(p) });
  return await r.json() as Record<string, any>; // deno-lint-ignore no-explicit-any
}
async function get(path: string, method = "GET") { const r = await fetch(BASE + path, { method }); return { status: r.status, body: await r.text() }; }
async function hashApp(email: string, mdp: string) {
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(email.toLowerCase() + "::" + mdp + "::AB22"));
  return Array.from(new Uint8Array(h)).map((x) => x.toString(16).padStart(2, "0")).join("");
}

console.log("▶ seed (base temporaire " + DATA + ")");
const seed = await new Deno.Command(DENO, { args: [...FLAGS, `${ROOT}/dev/server.ts`, "reset"], env, stdout: "piped", stderr: "piped" }).output();
const seedOut = new TextDecoder().decode(seed.stdout);
check("seed OK", seed.success, new TextDecoder().decode(seed.stderr).slice(-800));
const codes = Object.fromEntries([...seedOut.matchAll(/(Lina|Tom|Sarah) ([A-Z0-9]{6})/g)].map((m) => [m[1], m[2]]));

const srv = new Deno.Command(DENO, { args: [...FLAGS, `${ROOT}/dev/server.ts`, "serve", "--port", String(PORT)], env, stdout: "piped", stderr: "piped" }).spawn();
let logs = "";
(async () => { for await (const c of srv.stdout.pipeThrough(new TextDecoderStream())) logs += c; })();
(async () => { for await (const c of srv.stderr.pipeThrough(new TextDecoderStream())) logs += c; })();
for (let i = 0; i < 60; i++) { try { if ((await fetch(`${BASE}/dev/health`)).ok) break; } catch { /* pas prêt */ } await new Promise((r) => setTimeout(r, 250)); }

try {
  console.log("▶ statique");
  check("GET / (landing) 200", (await get("/")).status === 200);
  const app = await get("/app.html");
  check("GET /app.html 200 + script dev injecté", app.status === 200 && app.body.includes("/dev/inject.js"));

  console.log("▶ inscription / login");
  const email = `smoke${Date.now()}@exemple.fr`, mdp = "motdepasse-smoke";
  const h = await hashApp(email, mdp);
  const reg = await api({ action: "register", name: "Zoé", email, level: "3EME", password: h, objectif: "brevet" });
  check("register", reg.status === "success" && reg.profile?.code?.length === 6, reg);
  const code = reg.profile?.code;
  check("register en double refusé", (await api({ action: "register", name: "Zoé", email, level: "3EME", password: h })).status === "error");
  const lg = await api({ action: "login", email, password: h });
  check("login", lg.status === "success" && lg.profile?.code === code, lg);
  check("login mauvais mot de passe refusé", (await api({ action: "login", email, password: "x".repeat(64) })).status === "error");
  // régression : après un login, le client admin ne doit pas rester « connecté » en tant qu'élève
  const autre = await api({ action: "get_carte", code: codes.Tom });
  check("après login d'un élève, un autre élève reste lisible (client admin non contaminé)", autre.status === "success", autre);
  check("email de bienvenue dans l'outbox", [...Deno.readDirSync(`${DATA}/outbox`)].some((e) => e.name.includes(email)));

  console.log("▶ diagnostic express");
  let r = await api({ action: "start_diagnostic", code, email, type: "express" });
  check("start_diagnostic express", r.status === "success" && r.question?.id, r);
  check("question publique sans réponse ni erreurs types", r.question && !("a" in r.question) && !("err" in r.question) && !("steps" in r.question));
  const did = r.diagnostic_id;
  let n = 0;
  while (r.question && n < 40) {
    const q = r.question;
    const rep = n % 3 === 0 ? "" : (q.options?.[0] ?? "12"); // mélange de « je ne sais pas » et de réponses
    r = await api({ action: "answer_diagnostic", code, email, diagnostic_id: did, item_id: q.id, reponse: rep, temps: 25 });
    if (r.status !== "success") break;
    n++;
  }
  check("answer_diagnostic ×15 puis terminé", r.status === "success" && r.termine && n === 15, { n, r });
  check("carte express masquée (gratuit)", r.carte?.type === "express" && r.carte?.masque === true, r.carte);
  check("récap des corrections à la fin", Array.isArray(r.corrections) && r.corrections.length === 15);
  const carte = await api({ action: "get_carte", code, email });
  check("get_carte", carte.status === "success" && carte.carte?.domaines?.length > 0 && carte.droits?.acces === "free", carte);

  console.log("▶ entraînement");
  const tr = await api({ action: "get_training", code, email });
  const exos = tr.boost?.exos || [];
  // 5 exos visés ; moins si la banque est trop mince sur la zone gratuite (drapeau banque_insuffisante, voulu par le moteur)
  check("get_training : exos avec item_id + comp (5, ou banque_insuffisante signalée)", tr.status === "success" && exos.length >= 1 &&
    (exos.length === 5 || tr.boost?.banque_insuffisante === true) && exos.every((e: any) => e.item_id && e.comp), tr); // deno-lint-ignore no-explicit-any
  if (exos.length < 5) console.log(`     ℹ️  ${exos.length} exo(s) seulement : banque trop mince sur la zone ${JSON.stringify(tr.boost?.zone)}`);
  for (const [i, e] of exos.entries()) {
    const s = await api({ action: "save_score", code, email, name: "Zoé", level: "3EME", categorie: e.categorie, exercice_idx: e.num,
      resultat: i % 2 ? "EASY" : "HARD", source: "BOOST", item_id: e.item_id, comp: e.comp, q: e.q, reponse: i % 2 ? e.a : "", time: 40 });
    if (s.status !== "success") check("save_score " + i, false, s);
  }
  const tr2 = await api({ action: "get_training", code, email });
  check("get_training idempotent, exos_done = nb d'exos faits", tr2.deja === true && tr2.exos_done === exos.length, tr2);
  const scores = JSON.parse((await get(`/dev/db/scores?code=${code}`)).body);
  check("1 ligne scores par exo (upsert dédup)", scores.length === exos.length, scores.length);
  const rep = JSON.parse((await get(`/dev/db/reponses_items?code=${code}&contexte=train`)).body);
  check("1 réponse d'entraînement journalisée par exo", rep.length === exos.length, rep.length);
  const bis = await api({ action: "save_score", code, email, name: "Zoé", level: "3EME", categorie: exos[0].categorie, exercice_idx: exos[0].num, resultat: "EASY", source: "BOOST", q: exos[0].q });
  const scores2 = JSON.parse((await get(`/dev/db/scores?code=${code}`)).body);
  check("save_score rejoué le même jour : dédupliqué", bis.status === "success" && scores2.length === exos.length, scores2.length);

  console.log("▶ partage parent");
  const sh = await api({ action: "create_share", code, email });
  check("create_share", sh.status === "success" && /^[0-9a-f]{48}$/.test(sh.token), sh);
  const bp = await api({ action: "get_bilan_partage", token: sh.token });
  check("get_bilan_partage (public)", bp.status === "success" && bp.carte?.domaines && bp.acces === "free" && !JSON.stringify(bp).includes(email), bp);
  check("get_bilan_partage jeton bidon → expiré", (await api({ action: "get_bilan_partage", token: "0".repeat(48) })).expire === true);

  console.log("▶ paiement simulé (webhook Stripe signé)");
  const faux = await fetch(`${BASE}/api`, { method: "POST", headers: { "stripe-signature": "t=1,v1=00" },
    body: JSON.stringify({ type: "checkout.session.completed", data: { object: { customer_details: { email }, client_reference_id: code, metadata: { produit: "programme_brevet" } } } }) });
  check("webhook non signé rejeté", faux.status === 400);
  const p1 = JSON.parse((await get(`/dev/pay?code=${code}&produit=diag_complet`, "POST")).body);
  check("/dev/pay diag_complet → accès diagnostic_complet", p1.status === "success" && p1.droits?.acces === "diagnostic_complet" && p1.droits?.pdf === true, p1);
  check("prix du programme = 49 € − 19 €", p1.droits?.prix_cents?.programme_brevet === 3000, p1.droits);
  const sc = await api({ action: "start_diagnostic", code, email, type: "complet" });
  check("diagnostic complet débloqué (graines express reprises)", sc.status === "success" && sc.question?.id, sc);
  const cartePaye = await api({ action: "get_carte", code, email });
  check("carte non masquée après achat", cartePaye.carte && !cartePaye.carte.masque, cartePaye.carte?.masque);
  const p2 = JSON.parse((await get(`/dev/pay?code=${code}&produit=programme_brevet`, "POST")).body);
  check("/dev/pay programme_brevet → upgrade 30 € → accès programme_brevet", p2.status === "success" && p2.produit === "programme_upgrade" && p2.droits?.acces === "programme_brevet" && p2.droits?.entrainement_complet, p2);

  console.log("▶ comptes seedés");
  const adm = await api({ action: "login", email: "nicolas.follezou@hotmail.fr", password: await hashApp("nicolas.follezou@hotmail.fr", "matheux-dev") });
  check("login admin KN6CFG", adm.status === "success" && adm.profile?.isAdmin === true && adm.profile?.code === "KN6CFG", adm.message);
  check("get_admin_overview avec jeton de session admin", (await api({ action: "get_admin_overview", access_token: adm.access_token })).status === "success");

  console.log("▶ sécurité (failles corrigées le 24/09)");
  check("get_admin_overview avec le seul code admin → refusé", (await api({ action: "get_admin_overview", code: "KN6CFG" })).status === "error");
  check("publish_admin_boost sans jeton → refusé", (await api({ action: "publish_admin_boost", code: codes.Lina, boost: { exos: [] } })).status === "error");
  check("stripe_webhook via action → inconnue", /inconnue/i.test(String((await api({ action: "stripe_webhook", email, premium_end: "2099-01-01" })).message)));
  const nouveauMdp = await hashApp(email, "nouveau-mdp-dev");
  check("reset_password sans jeton → refusé", (await api({ action: "reset_password", email, password: nouveauMdp })).status === "error");
  const eleveTok = (await api({ action: "login", email: "nicolas.follezou@hotmail.fr", password: await hashApp("nicolas.follezou@hotmail.fr", "matheux-dev") })).access_token;
  check("reset_password avec le jeton d'un autre compte → refusé", (await api({ action: "reset_password", email, access_token: eleveTok, password: nouveauMdp })).status === "error");
  check("forgot_password", (await api({ action: "forgot_password", email })).status === "success");
  const mails = [...Deno.readDirSync(`${DATA}/outbox`)].filter((e) => e.name.includes(email)).map((e) => Deno.readTextFileSync(`${DATA}/outbox/${e.name}`));
  const recTok = mails.map((m) => (m.match(/access_token=([A-Za-z0-9._-]+)/) || [])[1]).filter(Boolean).pop();
  check("lien de récupération dans l'outbox", !!recTok);
  check("reset_password avec le jeton de récupération → OK", (await api({ action: "reset_password", email, access_token: recTok, password: nouveauMdp })).status === "success");
  check("login avec le nouveau mot de passe", (await api({ action: "login", email, password: nouveauMdp })).status === "success");
  const lina = await api({ action: "get_training", code: codes.Lina });
  check("Lina (neuve) : diagnostic requis", lina.diagnostic_requis === true, lina);
  const tom = await api({ action: "get_carte", code: codes.Tom });
  check("Tom : carte express, accès gratuit", tom.carte?.type === "express" && tom.droits?.acces === "free", tom.carte?.type);
  const sarah = await api({ action: "get_carte", code: codes.Sarah });
  check("Sarah : carte complète, Programme Brevet, streak ≥ 10", sarah.carte?.type === "complet" && sarah.droits?.acces === "programme_brevet" && sarah.streak?.streak >= 10, { t: sarah.carte?.type, a: sarah.droits?.acces, s: sarah.streak });

  console.log("▶ horloge de dev");
  const t1 = JSON.parse((await get("/dev/time?jours=1")).body);
  const tr3 = await api({ action: "get_training", code, email });
  check("/dev/time +1 j → nouvel entraînement du jour", t1.offset_jours === 1 && tr3.status === "success" && tr3.deja === false, tr3);
  await get("/dev/time?reset");

  check("aucun fetch externe bloqué pendant le test", !logs.includes("fetch externe bloqué"), logs.match(/fetch externe bloqué.*/)?.[0]);
} finally {
  srv.kill("SIGTERM");
  await srv.status;
  await Deno.remove(DATA, { recursive: true }).catch(() => {});
}
console.log(`\n${ko === 0 ? "✅" : "❌"} smoke test : ${ok} OK, ${ko} KO`);
Deno.exit(ko === 0 ? 0 : 1);
