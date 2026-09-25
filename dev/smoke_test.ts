// ════════════════════════════════════════════════════════════
//  Matheux — smoke test du backend de dev (HTTP, bout en bout)
//  Démarre un serveur ISOLÉ (port 8799, base temporaire : ne touche pas dev/data/), le seed,
//  puis déroule le parcours : inscription → login → diagnostic express (15 q) → carte →
//  entraînement + save_score → partage parent → paiement simulé → droits premium.
//  Usage : deno run -A dev/smoke_test.ts   (ou ./matheux.sh test)
// ════════════════════════════════════════════════════════════
const ADMIN_EMAIL = "admin@dev.matheux.local", ADMIN_CODE = "ADMDEV"; // admin fictif de dev/seed.ts
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
  check("register renvoie access_token + refresh_token", !!reg.access_token && !!reg.refresh_token, reg);
  const lg = await api({ action: "login", email, password: h });
  check("login", lg.status === "success" && lg.profile?.code === code && !!lg.access_token && !!lg.refresh_token, lg);
  const tok = lg.access_token as string;
  const A = { code, email, access_token: tok }; // identité élève = code + jeton de session
  check("login mauvais mot de passe refusé", (await api({ action: "login", email, password: "x".repeat(64) })).status === "error");
  // régression : après un login, le client admin ne doit pas rester « connecté » en tant qu'élève
  const tomTok = (await api({ action: "login", email: "tom@exemple.fr", password: await hashApp("tom@exemple.fr", "matheux-dev") })).access_token;
  const autre = await api({ action: "get_carte", code: codes.Tom, access_token: tomTok });
  check("après login d'un élève, un autre élève reste lisible (client admin non contaminé)", autre.status === "success", autre);
  check("pas de mail J+0 au register sans diagnostic (P-X0 part à la fin du diag)", ![...Deno.readDirSync(`${DATA}/outbox`)].some((e) => e.name.includes(email)));

  console.log("▶ auto-login par jeton (Besoin API n°9)");
  const lt = await api({ action: "login_token", access_token: tok });
  check("login_token {access_token} → même profil", lt.status === "success" && lt.profile?.code === code && lt.access_token === tok, lt.message);
  const lt2 = await api({ action: "login_token", access_token: "jeton.expire.bidon", refresh_token: lg.refresh_token });
  check("login_token jeton expiré + refresh_token → session renouvelée", lt2.status === "success" && lt2.profile?.code === code && !!lt2.access_token && lt2.access_token !== tok, lt2.message);
  check("jeton renouvelé utilisable", (await api({ action: "get_acces", code, access_token: lt2.access_token })).status === "success");
  const rs = await api({ action: "refresh_session", refresh_token: lt2.refresh_token });
  check("refresh_session", rs.status === "success" && !!rs.access_token && rs.code === code, rs);
  check("login_token sans jeton valide → auth_requise", (await api({ action: "login_token", access_token: "x" })).auth_requise === true);

  console.log("▶ diagnostic express");
  let r = await api({ action: "start_diagnostic", ...A, type: "express" });
  check("start_diagnostic express", r.status === "success" && r.question?.id, r);
  check("question publique sans réponse ni erreurs types", r.question && !("a" in r.question) && !("err" in r.question) && !("steps" in r.question));
  check("question : domaine + niveau_origine (Besoin n°11)", /^(NC|DF|GM|EG|AP)$/.test(r.question?.domaine) && /^[3-6]EME$/.test(r.question?.niveau_origine), r.question);
  const did = r.diagnostic_id;
  let n = 0;
  while (r.question && n < 40) {
    const q = r.question;
    const rep = n % 3 === 0 ? "" : (q.options?.[0] ?? "12"); // mélange de « je ne sais pas » et de réponses
    r = await api({ action: "answer_diagnostic", ...A, diagnostic_id: did, item_id: q.id, reponse: rep, temps: 25 });
    if (r.status !== "success") break;
    n++;
  }
  check("answer_diagnostic ×15 puis terminé", r.status === "success" && r.termine && n === 15, { n, r });
  check("carte express masquée (gratuit)", r.carte?.type === "express" && r.carte?.masque === true, r.carte);
  check("récap des corrections à la fin", Array.isArray(r.corrections) && r.corrections.length === 15);
  const carte = await api({ action: "get_carte", ...A });
  check("get_carte", carte.status === "success" && carte.carte?.domaines?.length > 0 && carte.droits?.acces === "free", carte);
  const cm = (carte.carte?.competences || []) as any[]; // deno-lint-ignore no-explicit-any
  check("carte masquée : titre_eleve + niveau_origine sur TOUTES les compétences (Besoin n°3)", cm.length > 1 && cm.every((c) => c.titre_eleve && c.niveau_origine), cm.slice(0, 3));
  check("carte masquée : résultats détaillés seulement sur le point faible", cm.filter((c) => !c.masque).length === 1 && cm.filter((c) => c.masque).every((c) => !("erreurs" in c) && !("maitrise" in c)), cm.filter((c) => !c.masque).map((c) => c.id));
  check("carte : non_mesurees (compétences de 3e pas encore mesurées, avec titres)", Array.isArray(carte.carte?.non_mesurees) && carte.carte.non_mesurees.length > 0 && carte.carte.non_mesurees.every((c: any) => c.titre_eleve), carte.carte?.non_mesurees?.slice(0, 2)); // deno-lint-ignore no-explicit-any
  const mailsPx0 = () => [...Deno.readDirSync(`${DATA}/outbox`)].filter((e) => e.name.includes(email) && e.name.includes("bilan_maths")).map((e) => Deno.readTextFileSync(`${DATA}/outbox/${e.name}`));
  check("P-X0 : bilan express envoyé au parent à la fin du diag (Besoin n°7)", mailsPx0().length === 1 && /vous/.test(mailsPx0()[0]) && mailsPx0()[0].includes("/b/"), mailsPx0().length);
  const px0Tok = (mailsPx0()[0]?.match(/\/b\/([0-9a-f]{48})\?confirmer=1/) || [])[1];
  check("P-X0 : lien de confirmation parentale", !!px0Tok);

  console.log("▶ entraînement");
  const tr = await api({ action: "get_training", ...A });
  const exos = tr.boost?.exos || [];
  // 5 exos visés ; moins si la banque est trop mince sur la zone gratuite (drapeau banque_insuffisante, voulu par le moteur)
  check("get_training : exos avec item_id + comp (5, ou banque_insuffisante signalée)", tr.status === "success" && exos.length >= 1 &&
    (exos.length === 5 || tr.boost?.banque_insuffisante === true) && exos.every((e: any) => e.item_id && e.comp), tr); // deno-lint-ignore no-explicit-any
  if (exos.length < 5) console.log(`     ℹ️  ${exos.length} exo(s) seulement : banque trop mince sur la zone ${JSON.stringify(tr.boost?.zone)}`);
  check("exos[].err_libelles (Besoin n°2)", exos.every((e: any) => e.err_libelles && typeof e.err_libelles === "object") && // deno-lint-ignore no-explicit-any
    exos.some((e: any) => Object.keys(e.err_libelles).length > 0), exos.map((e: any) => e.err_libelles)); // deno-lint-ignore no-explicit-any
  check("boost.focus_titres + boost.pourquoi (Besoin n°4)", Array.isArray(tr.boost?.focus_titres) && tr.boost.focus_titres.every((f: any) => f.titre_eleve) && // deno-lint-ignore no-explicit-any
    typeof tr.boost?.pourquoi === "string" && tr.boost.pourquoi.length > 10 && !/prof/i.test(tr.boost.pourquoi), { f: tr.boost?.focus_titres, p: tr.boost?.pourquoi });
  console.log("     ℹ️  pourquoi : " + tr.boost?.pourquoi);
  for (const [i, e] of exos.entries()) {
    const s = await api({ action: "save_score", ...A, name: "Zoé", level: "3EME", categorie: e.categorie, exercice_idx: e.num,
      resultat: i % 2 ? "EASY" : "HARD", source: "BOOST", item_id: e.item_id, comp: e.comp, q: e.q, reponse: i % 2 ? e.a : "", time: 40 });
    if (s.status !== "success") check("save_score " + i, false, s);
  }
  const tr2 = await api({ action: "get_training", ...A });
  check("get_training idempotent, exos_done = nb d'exos faits", tr2.deja === true && tr2.exos_done === exos.length, tr2);
  const scores = JSON.parse((await get(`/dev/db/scores?code=${code}`)).body);
  check("1 ligne scores par exo (upsert dédup)", scores.length === exos.length, scores.length);
  const rep = JSON.parse((await get(`/dev/db/reponses_items?code=${code}&contexte=train`)).body);
  check("1 réponse d'entraînement journalisée par exo", rep.length === exos.length, rep.length);
  const bis = await api({ action: "save_score", ...A, name: "Zoé", level: "3EME", categorie: exos[0].categorie, exercice_idx: exos[0].num, resultat: "EASY", source: "BOOST", q: exos[0].q });
  const scores2 = JSON.parse((await get(`/dev/db/scores?code=${code}`)).body);
  check("save_score rejoué le même jour : dédupliqué", bis.status === "success" && scores2.length === exos.length, scores2.length);

  console.log("▶ partage parent");
  const sh = await api({ action: "create_share", ...A, canal: "email_parent" });
  check("create_share", sh.status === "success" && /^[0-9a-f]{48}$/.test(sh.token), sh);
  const bp = await api({ action: "get_bilan_partage", token: sh.token });
  check("get_bilan_partage (public)", bp.status === "success" && bp.carte?.domaines && bp.acces === "free" && !JSON.stringify(bp).includes(email), bp);
  check("get_bilan_partage jeton bidon → expiré", (await api({ action: "get_bilan_partage", token: "0".repeat(48) })).expire === true);
  const cpart = await api({ action: "get_carte", ...A });
  check("get_carte.partages[] : lien actif avec vues (Besoin n°14)", Array.isArray(cpart.partages) && cpart.partages.some((x: any) => x.token === sh.token && x.vues === 1), cpart.partages); // deno-lint-ignore no-explicit-any
  check("create_share canal email_parent forcé en « app »", cpart.partages.find((x: any) => x.token === sh.token)?.canal === "app"); // deno-lint-ignore no-explicit-any
  check("confirm_parent avec un lien créé depuis l'app → refusé (canal email_parent réservé au mail)", (await api({ action: "confirm_parent", token: sh.token })).status === "error");
  const cp = await api({ action: "confirm_parent", token: px0Tok, optin_marketing: true });
  const profZ = JSON.parse((await get(`/dev/db/profiles?code=${code}`)).body)[0];
  check("confirm_parent (lien du mail P-X0) → consentement + opt-in enregistrés", cp.status === "success" && !!profZ?.consentement_parent_at && profZ?.optin_marketing === true, { cp, c: profZ?.consentement_parent_at });
  check("log_consent depuis la page parent (jeton de partage, sans session)", (await api({ action: "log_consent", token: sh.token, produit: "diag_complet", texte_version: "v1", texte_hash: "abc", cases: ["cgv"] })).status === "success");

  console.log("▶ prix (Besoin n°6)");
  const ac = await api({ action: "get_acces", ...A });
  check("get_acces.produits : 1900 / 4900 / 3000 centimes", ac.produits?.diagnostic_complet?.prix_cents === 1900 && ac.produits?.programme_brevet?.prix_cents === 4900 &&
    ac.produits?.programme_upgrade?.prix_cents === 3000 && ac.produits?.programme_upgrade?.offre === "programme_upgrade", ac.produits);
  const libreFree = await api({ action: "get_training", ...A, comp: exos[0]?.comp });
  check("entraînement libre refusé en gratuit (paywall programme)", libreFree.status === "error" && libreFree.paywall === "programme_brevet", libreFree);

  console.log("▶ paiement simulé (webhook Stripe signé)");
  const faux = await fetch(`${BASE}/api`, { method: "POST", headers: { "stripe-signature": "t=1,v1=00" },
    body: JSON.stringify({ type: "checkout.session.completed", data: { object: { customer_details: { email }, client_reference_id: code, metadata: { produit: "programme_brevet" } } } }) });
  check("webhook non signé rejeté", faux.status === 400);
  const p1 = JSON.parse((await get(`/dev/pay?code=${code}&produit=diag_complet`, "POST")).body);
  check("/dev/pay diag_complet → accès diagnostic_complet", p1.status === "success" && p1.droits?.acces === "diagnostic_complet" && p1.droits?.pdf === true, p1);
  check("prix du programme = 49 € − 19 €", p1.droits?.prix_cents?.programme_brevet === 3000, p1.droits);
  const sc = await api({ action: "start_diagnostic", ...A, type: "complet" });
  check("diagnostic complet débloqué (graines express reprises)", sc.status === "success" && sc.question?.id, sc);
  const cartePaye = await api({ action: "get_carte", ...A });
  check("carte non masquée après achat", cartePaye.carte && !cartePaye.carte.masque, cartePaye.carte?.masque);
  const p2 = JSON.parse((await get(`/dev/pay?code=${code}&produit=programme_brevet`, "POST")).body);
  check("/dev/pay programme_brevet → upgrade 30 € → accès programme_brevet", p2.status === "success" && p2.produit === "programme_upgrade" && p2.droits?.acces === "programme_brevet" && p2.droits?.entrainement_complet, p2);

  console.log("▶ entraînement libre Programme (Besoin n°5)");
  const boostsAvant = JSON.parse((await get(`/dev/db/daily_boosts?code=${code}`)).body);
  const compLibre = String(exos[0]?.comp || "");
  const lib = await api({ action: "get_training", ...A, comp: compLibre });
  const lexos = (lib.boost?.exos || []) as any[]; // deno-lint-ignore no-explicit-any
  check("get_training {comp} → exos sur cette seule compétence", lib.status === "success" && lib.libre === true && lexos.length >= 1 && lexos.every((e) => e.comp === compLibre && e.err_libelles), lib);
  check("entraînement libre : aucun exo de la séance du jour", !lexos.some((e) => exos.some((x: any) => x.item_id === e.item_id))); // deno-lint-ignore no-explicit-any
  const sl = await api({ action: "save_score", ...A, name: "Zoé", level: "3EME", categorie: lexos[0]?.categorie, exercice_idx: lexos[0]?.num, resultat: "EASY", source: "LIBRE", item_id: lexos[0]?.item_id, q: lexos[0]?.q, reponse: lexos[0]?.a });
  const boostsApres = JSON.parse((await get(`/dev/db/daily_boosts?code=${code}`)).body);
  check("save_score source LIBRE accepté, daily_boosts inchangé (hors quota)", sl.status === "success" && JSON.stringify(boostsApres) === JSON.stringify(boostsAvant), sl);
  const lib2 = await api({ action: "get_training", ...A, comp: compLibre });
  check("2e série libre : l'item répondu n'est pas resservi en premier (sauf banque d'1 item)", lib2.status === "success" && (lexos.length < 2 || lib2.boost?.exos?.[0]?.item_id !== lexos[0]?.item_id), { avant: lexos.map((e: any) => e.item_id), apres: lib2.boost?.exos?.map((e: any) => e.item_id), sl }); // deno-lint-ignore no-explicit-any

  console.log("▶ comptes seedés");
  const adm = await api({ action: "login", email: ADMIN_EMAIL, password: await hashApp(ADMIN_EMAIL, "matheux-dev") });
  check("login admin de dev", adm.status === "success" && adm.profile?.isAdmin === true && adm.profile?.code === ADMIN_CODE, adm.message);
  const ov = await api({ action: "get_admin_overview", access_token: adm.access_token });
  check("get_admin_overview avec jeton de session admin", ov.status === "success");
  check("get_admin_overview : diagnostics + stats, invités, achats, funnel agrégé (Besoin n°10)", Array.isArray(ov.diagnostics) && ov.diagnostics.length > 0 &&
    ov.diagnostics_stats?.express?.termine >= 1 && ov.invites?.rattache >= 1 && Array.isArray(ov.achats) && ov.achats.length >= 1 && ov.ca_cents > 0 &&
    ov.funnel?.diag_express_done?.total >= 1, { s: ov.diagnostics_stats, i: ov.invites, f: Object.keys(ov.funnel || {}), ca: ov.ca_cents });

  console.log("▶ sécurité (failles corrigées le 24/09)");
  check("get_admin_overview avec le seul code admin → refusé", (await api({ action: "get_admin_overview", code: ADMIN_CODE })).status === "error");
  check("publish_admin_boost sans jeton → refusé", (await api({ action: "publish_admin_boost", code: codes.Lina, boost: { exos: [] } })).status === "error");
  check("stripe_webhook via action → inconnue", /inconnue/i.test(String((await api({ action: "stripe_webhook", email, premium_end: "2099-01-01" })).message)));
  const nouveauMdp = await hashApp(email, "nouveau-mdp-dev");
  check("reset_password sans jeton → refusé", (await api({ action: "reset_password", email, password: nouveauMdp })).status === "error");
  const eleveTok = (await api({ action: "login", email: ADMIN_EMAIL, password: await hashApp(ADMIN_EMAIL, "matheux-dev") })).access_token;
  check("reset_password avec le jeton d'un autre compte → refusé", (await api({ action: "reset_password", email, access_token: eleveTok, password: nouveauMdp })).status === "error");
  check("forgot_password", (await api({ action: "forgot_password", email })).status === "success");
  const mails = [...Deno.readDirSync(`${DATA}/outbox`)].filter((e) => e.name.includes(email)).map((e) => Deno.readTextFileSync(`${DATA}/outbox/${e.name}`));
  const recTok = mails.map((m) => (m.match(/access_token=([A-Za-z0-9._-]+)/) || [])[1]).filter(Boolean).pop();
  check("lien de récupération dans l'outbox", !!recTok);
  check("reset_password avec le jeton de récupération → OK", (await api({ action: "reset_password", email, access_token: recTok, password: nouveauMdp })).status === "success");
  check("login avec le nouveau mot de passe", (await api({ action: "login", email, password: nouveauMdp })).status === "success");
  const tokDe = async (e: string) => (await api({ action: "login", email: e, password: await hashApp(e, "matheux-dev") })).access_token;
  const linaTok = await tokDe("lina@exemple.fr"), sarahTok = await tokDe("sarah@exemple.fr");
  const lina = await api({ action: "get_training", code: codes.Lina, access_token: linaTok });
  check("Lina (neuve) : diagnostic requis", lina.diagnostic_requis === true, lina);
  const tom = await api({ action: "get_carte", code: codes.Tom, access_token: tomTok });
  check("Tom (diag express invité rattaché au register) : carte express, accès gratuit", tom.carte?.type === "express" && tom.droits?.acces === "free", tom.carte?.type);
  const sarah = await api({ action: "get_carte", code: codes.Sarah, access_token: sarahTok });
  check("Sarah : carte complète, Programme Brevet, streak ≥ 10", sarah.carte?.type === "complet" && sarah.droits?.acces === "programme_brevet" && sarah.streak?.streak >= 10, { t: sarah.carte?.type, a: sarah.droits?.acces, s: sarah.streak });

  console.log("▶ sécurité des actions élève (Besoin n°8) : code seul / jeton d'un autre élève");
  const ACTIONS_ELEVE: Record<string, Record<string, unknown>> = {
    get_carte: {}, get_training: {}, get_acces: {}, start_diagnostic: { type: "express" }, answer_diagnostic: { diagnostic_id: did, item_id: "x", reponse: "1" },
    create_share: {}, revoke_share: {}, set_preferences: { optin_marketing: true }, log_consent: { produit: "compte", texte_version: "v", texte_hash: "h" },
    save_score: { name: "X", level: "3EME", categorie: "Fractions_Brevet", exercice_idx: 1, resultat: "EASY" },
    save_scores_batch: { scores: [{ categorie: "Fractions_Brevet", exercice_idx: 1, resultat: "EASY" }] },
    save_boost: { boost: { exos: [] } }, save_calibration_batch: { scores: [] }, get_progress: {}, check_trial_status: {},
    generate_adaptive_boost: {}, save_brevet_result: {},
  };
  const refusCode = Object.entries(ACTIONS_ELEVE).filter(([a, x]) => { void a; void x; return true; });
  const failles1: string[] = [], failles2: string[] = [];
  for (const [action, extra] of refusCode) {
    const r1 = await api({ action, code: codes.Lina, email: "lina@exemple.fr", ...extra });
    if (r1.status !== "error" || !r1.auth_requise) failles1.push(action + " → " + JSON.stringify(r1).slice(0, 80));
    const r2 = await api({ action, code: codes.Lina, email: "lina@exemple.fr", access_token: tomTok, ...extra });
    if (r2.status !== "error" || !r2.auth_requise) failles2.push(action + " → " + JSON.stringify(r2).slice(0, 80));
  }
  check(`${refusCode.length} actions élève avec le code seul → refusées`, failles1.length === 0, failles1);
  check(`${refusCode.length} actions élève avec le jeton d'un AUTRE élève → refusées`, failles2.length === 0, failles2);
  check("jeton bidon → refusé", (await api({ action: "get_carte", code: codes.Lina, access_token: "abc.def.ghi" })).auth_requise === true);
  check("admin : lecture de la carte d'un élève autorisée (monitoring)", (await api({ action: "get_carte", code: codes.Tom, access_token: adm.access_token })).status === "success");
  check("admin : get_training d'un élève refusé (A6, admin read-only)", (await api({ action: "get_training", code: codes.Tom, access_token: adm.access_token })).auth_requise === true);
  check("admin : save_score au nom d'un élève refusé", (await api({ action: "save_score", code: codes.Tom, access_token: adm.access_token, ...ACTIONS_ELEVE.save_score })).auth_requise === true);
  // ADMIN_ONLY (hotfix prod 4fc6123) + cron : ni sans jeton, ni avec le code admin public, ni avec un jeton élève
  const ADMIN_ACTIONS = ["get_admin_overview", "publish_admin_boost", "publish_admin_chapter", "get_cours_admin", "save_cours",
    "send_admin_email", "send_test_email", "send_marketing_email", "log_manual_email", "send_weekly_report", "send_custom_email",
    "send_session_rapport", "cron_send_emails"];
  const piege = { targetEmail: "victime@exemple.fr", to: "victime@exemple.fr", subject: "x", html: "<p>x</p>", email: "victime@exemple.fr",
    name: "X", day: 0, niveau: "3EME", categorie: "X", targetCode: codes.Lina, boost: { exos: [] }, chapter: { exos: [] } };
  const nMails0 = [...Deno.readDirSync(`${DATA}/outbox`)].filter((e) => e.name.includes("victime")).length;
  const f3: string[] = [];
  for (const a of ADMIN_ACTIONS) {
    for (const [nom, cred] of [["sans jeton", {}], ["code admin seul", { code: ADMIN_CODE, adminCode: ADMIN_CODE }], ["jeton élève", { access_token: tomTok, code: codes.Tom }]] as [string, Record<string, unknown>][]) {
      const r = await api({ action: a, ...piege, ...cred });
      if (r.status !== "error") f3.push(`${a} (${nom}) → ${JSON.stringify(r).slice(0, 60)}`);
    }
  }
  check(`${ADMIN_ACTIONS.length} actions admin / envoi d'email × 3 attaques → toutes refusées`, f3.length === 0, f3);
  check("aucun mail parti vers la victime pendant les attaques", [...Deno.readDirSync(`${DATA}/outbox`)].filter((e) => e.name.includes("victime")).length === nMails0);
  check("cron_send_emails avec un faux cron_secret → refusé", (await api({ action: "cron_send_emails", cron_secret: "0".repeat(64) })).status === "error");
  const sae = await api({ action: "send_admin_email", access_token: adm.access_token, to: "parent-test@exemple.fr", subject: "Test admin", html: "<p>ok</p>" });
  check("send_admin_email avec jeton admin → envoyé (outbox)", sae.status === "success" && [...Deno.readDirSync(`${DATA}/outbox`)].some((e) => e.name.includes("parent-test@")), sae);
  check("register : prénom avec balise HTML refusé (XSS stockée, audit 04/11)", (await api({ action: "register", name: "<img src=x onerror=alert(1)>", email: `xss${Date.now()}@exemple.fr`, level: "3EME", password: "x".repeat(64) })).status === "error");
  check("cron_send_emails avec jeton élève → refusé", (await api({ action: "cron_send_emails", access_token: tomTok })).status === "error");
  check("cron_send_emails avec jeton admin → OK", (await api({ action: "cron_send_emails", access_token: adm.access_token })).status === "success");
  const ev0 = JSON.parse((await get(`/dev/db/funnel_events?event=paywall_view`)).body).length;
  await api({ action: "log_funnel_event", event: "paywall_view", code: codes.Lina });
  const evs = JSON.parse((await get(`/dev/db/funnel_events?event=paywall_view`)).body);
  check("log_funnel_event : code non prouvé → événement anonyme", evs.length === ev0 + 1 && evs[evs.length - 1].code === null, evs.slice(-1));

  console.log("▶ diagnostic express INVITÉ, sans compte (Besoin n°1)");
  let g = await api({ action: "start_diagnostic", type: "express", prenom: "Inès" });
  check("start_diagnostic sans code → diagnostic_id + guest_token + question", g.status === "success" && g.invite === true && /^[0-9a-f]{48}$/.test(g.guest_token) && g.question?.id && !("a" in g.question), g);
  const inv = { diagnostic_id: g.diagnostic_id, guest_token: g.guest_token };
  check("start_diagnostic invité : complet refusé (compte requis)", (await api({ action: "start_diagnostic", type: "complet" })).status === "error");
  const autreInv = await api({ action: "start_diagnostic", type: "express" });
  check("mauvais guest_token → refusé", (await api({ action: "answer_diagnostic", diagnostic_id: g.diagnostic_id, guest_token: autreInv.guest_token, item_id: g.question.id, reponse: "1" })).status === "error");
  check("guest_token d'un autre diagnostic → refusé", (await api({ action: "answer_diagnostic", diagnostic_id: autreInv.diagnostic_id, guest_token: g.guest_token, item_id: autreInv.question.id, reponse: "1" })).status === "error");
  const reprise = await api({ action: "start_diagnostic", ...inv });
  check("reprise invité : même question en attente, pas de nouveau jeton", reprise.status === "success" && reprise.question?.id === g.question.id && !reprise.guest_token, reprise);
  let ng = 0;
  while (g.question && ng < 40) {
    const q = g.question;
    g = await api({ action: "answer_diagnostic", ...inv, item_id: q.id, reponse: ng % 4 === 0 ? "" : (q.options?.[1] ?? "7"), temps: 30 });
    if (g.status !== "success") break;
    ng++;
  }
  check("invité : 15 réponses puis carte express masquée (free) + corrections", g.status === "success" && g.termine && ng === 15 && g.carte?.masque === true && g.carte?.eleve?.prenom === "Inès" && g.corrections?.length === 15, { ng, g });
  check("invité : rien écrit dans maitrise / reponses_items avant le compte", JSON.parse((await get(`/dev/db/reponses_items?diagnostic_id=${inv.diagnostic_id}`)).body).length === 0);
  const emailG = `invite${Date.now()}@exemple.fr`;
  const regG = await api({ action: "register", name: "Inès", email: emailG, level: "3EME", password: await hashApp(emailG, "mdp-invite"), ...inv });
  check("register {diagnostic_id, guest_token} → diagnostic rattaché", regG.status === "success" && regG.diagnostic_rattache === true && !!regG.diagnostic_id && regG.carte?.type === "express" && !!regG.access_token, regG);
  const codeG = regG.profile?.code;
  const repG = JSON.parse((await get(`/dev/db/reponses_items?code=${codeG}&contexte=diag`)).body);
  const mtG = JSON.parse((await get(`/dev/db/maitrise?code=${codeG}`)).body);
  check("register : observations rejouées (reponses_items + maitrise)", repG.length === 15 && mtG.length >= 5, { rep: repG.length, mt: mtG.length });
  const cG = await api({ action: "get_carte", code: codeG, access_token: regG.access_token });
  check("carte du compte = carte invitée (mêmes domaines, même point faible)", cG.carte?.point_faible === g.carte?.point_faible &&
    JSON.stringify(cG.carte?.domaines) === JSON.stringify(g.carte?.domaines), { a: cG.carte?.point_faible, b: g.carte?.point_faible });
  check("P-X0 envoyé au parent au register (diag invité terminé)", [...Deno.readDirSync(`${DATA}/outbox`)].some((e) => e.name.includes(emailG) && e.name.includes("bilan_maths")));
  const trG = await api({ action: "get_training", code: codeG, access_token: regG.access_token });
  check("compte issu d'un diag invité : entraînement disponible", trG.status === "success" && trG.boost?.exos?.length >= 1, trG.message);
  const emailG2 = `invite2${Date.now()}@exemple.fr`;
  const regG2 = await api({ action: "register", name: "Pirate", email: emailG2, level: "3EME", password: await hashApp(emailG2, "x-mdp-x"), ...inv });
  check("même guest_token réutilisé → compte créé mais rien rattaché", regG2.status === "success" && regG2.diagnostic_rattache === false && !!regG2.rattachement_erreur, regG2);
  // Besoin n°12 : diag invité passé par quelqu'un qui a déjà un compte → rattaché au login
  let g3 = await api({ action: "start_diagnostic", type: "express" });
  const inv3 = { diagnostic_id: g3.diagnostic_id, guest_token: g3.guest_token };
  for (let k = 0; g3.question && k < 40; k++) g3 = await api({ action: "answer_diagnostic", ...inv3, item_id: g3.question.id, reponse: "", temps: 30 });
  const lgInv = await api({ action: "login", email: emailG, password: await hashApp(emailG, "mdp-invite"), ...inv3 });
  check("login {…, diagnostic_id, guest_token} → diag invité rattaché au compte existant", lgInv.status === "success" && lgInv.diagnostic_rattache === true && !!lgInv.diagnostic_id, { s: lgInv.status, r: lgInv.diagnostic_rattache, m: lgInv.message });
  const nDiagG = JSON.parse((await get(`/dev/db/diagnostics?code=${codeG}`)).body).length;
  check("le compte a maintenant 2 diagnostics express", nDiagG === 2, nDiagG);
  await get("/dev/time?jours=3");
  check("guest_token expiré (+3 j) → refusé", (await api({ action: "answer_diagnostic", diagnostic_id: autreInv.diagnostic_id, guest_token: autreInv.guest_token, item_id: autreInv.question.id, reponse: "1" })).invite_expire === true);
  await get("/dev/time?reset");

  console.log("▶ horloge de dev");
  const t1 = JSON.parse((await get("/dev/time?jours=1")).body);
  const tr3 = await api({ action: "get_training", ...A });
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
