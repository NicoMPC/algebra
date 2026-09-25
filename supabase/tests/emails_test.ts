// ════════════════════════════════════════════════════════════
//  Séquence emails « diagnostic 3e » (docs/specs/51-emails.md) : planificateur pur mxPlanEmails.
//  Simulation d'élèves fictifs jour par jour (sans base, sans envoi) : chaque email planifié est
//  « envoyé » (ajouté aux logs), puis on vérifie les invariants : plafonds, opt-in, arrêt après achat,
//  jamais de commercial à l'ado, rien le week-end, pause du 15 mai, dernier message de conversion.
//  Le parcours HTTP bout en bout (outbox, /dev/time) est dans dev/smoke_test.ts.
//  Usage : deno test -A supabase/tests/
// ════════════════════════════════════════════════════════════
// deno-lint-ignore-file no-explicit-any
const src = await Deno.readTextFile(new URL("../functions/api/index.ts", import.meta.url));
const bloc = src.slice(src.lastIndexOf("\n", src.indexOf("MOTEUR_PUR_DEBUT")), src.indexOf("MOTEUR_PUR_FIN"));
const noms = [...bloc.matchAll(/^(?:function|const) ([mM][xX][A-Za-z0-9_]*)/gm)].map((m) => m[1]);
const tmp = await Deno.makeTempFile({ suffix: ".ts" });
await Deno.writeTextFile(tmp, bloc + "\nexport { " + [...new Set(noms)].join(", ") + " };\n");
const M: any = await import("file://" + tmp);

function assert(c: unknown, msg: string): asserts c { if (!c) throw new Error("ÉCHEC : " + msg); }
const add = (d: string, n: number) => M.mxAjoutJours(d, n);
const jours = (a: string, b: string) => M.mxJoursEntre(a, b);
const dow = (d: string) => new Date(d + "T12:00:00Z").getUTCDay();

type Eleve = {
  debut: string; express?: number | null; achatDiag?: number | null; programme?: number | null; complet?: number | null;
  consent?: number | null; optin?: boolean; emailEleve?: boolean; pfFragile?: boolean; actifs?: number[]; rediag?: boolean;
};
// Simule `n` jours à partir de `debut` (J0 = inscription). Renvoie les emails envoyés, datés.
function simuler(e: Eleve, n = 35) {
  const logs: any[] = [];
  const jd = (k: number | null | undefined) => (k === null || k === undefined ? null : add(e.debut, k));
  if (e.express !== null && e.express !== undefined) logs.push({ type: "D3:P-X0", cat: "T", date: jd(e.express), dest: "parent" }); // P-X0 : envoyé à la fin du diag
  for (let k = 0; k <= n; k++) {
    const today = add(e.debut, k);
    const vu = (x: number | null | undefined) => x !== null && x !== undefined && x <= k;
    const etat = {
      today, inscription: e.debut,
      express_at: vu(e.express) ? jd(e.express) : null, complet_at: vu(e.complet) ? jd(e.complet) : null,
      achat_diag_at: vu(e.achatDiag) ? jd(e.achatDiag) : null, programme_at: vu(e.programme) ? jd(e.programme) : null,
      complet_modules_faits: 1, consentement: vu(e.consent), optin: !!e.optin && vu(e.consent), email_eleve: !!e.emailEleve,
      pf_fragile: e.pfFragile !== false, jours_actifs: (e.actifs || []).filter((a) => a <= k).map((a) => add(e.debut, a)),
      rediag_du: !!e.rediag, logs: logs.filter((l) => l.date <= today),
    };
    for (const p of M.mxPlanEmails(etat)) logs.push({ type: "D3:" + p.type, cat: p.cat, date: today, dest: p.dest, k });
  }
  return logs.filter((l) => l.type !== "D3:P-X0");
}
function invariants(nom: string, logs: any[], e: Eleve) {
  const parent = logs.filter((l) => l.dest === "parent"), ado = logs.filter((l) => l.dest === "ado");
  const dates = parent.map((l) => l.date);
  assert(new Set(dates).size === dates.length, nom + " : 2 emails au parent le même jour " + JSON.stringify(parent));
  const m = parent.filter((l) => l.cat === "M");
  for (let i = 1; i < m.length; i++) assert(jours(m[i - 1].date, m[i].date) >= 3, nom + " : 2 commerciaux à moins de 72 h");
  for (const l of m) assert(m.filter((x) => jours(x.date, l.date) >= 0 && jours(x.date, l.date) < 30).length <= 5, nom + " : plus de 5 commerciaux en 30 jours");
  if (!e.optin) assert(m.length === 0, nom + " : commercial sans opt-in " + JSON.stringify(m));
  assert(ado.every((l) => l.cat === "P"), nom + " : email non pédagogique à l'ado");
  if (!e.emailEleve || e.consent === null || e.consent === undefined) assert(ado.length === 0, nom + " : email ado sans adresse ou sans accord parental");
  for (const l of ado) assert(ado.filter((x) => jours(x.date, l.date) >= 0 && jours(x.date, l.date) < 7).length <= 3, nom + " : plus de 3 emails ado en 7 jours");
  for (const l of logs) {
    if (dow(l.date) === 6) assert(l.type.startsWith("D3:A-MENS"), nom + " : email un samedi " + l.type);
    if (dow(l.date) === 0) assert(l.type.startsWith("D3:P-HEBDO"), nom + " : email un dimanche " + l.type);
  }
  const achat = [e.achatDiag, e.programme].filter((x) => x !== null && x !== undefined) as number[];
  if (achat.length) {
    const kA = Math.min(...achat);
    assert(!logs.some((l) => /^D3:P-X[123]$/.test(l.type) && l.k >= kA), nom + " : relance de conversion après un achat");
  }
  const x3 = logs.find((l) => l.type === "D3:P-X3");
  if (x3) assert(!logs.some((l) => /^D3:P-X[12]$/.test(l.type) && l.k > x3.k), nom + " : relance de conversion après P-X3");
  const types = logs.map((l) => l.type);
  assert(new Set(types).size === types.length, nom + " : doublon " + types.join(","));
}
const types = (logs: any[]) => logs.map((l) => l.type.replace(/^D3:/, "") + "@J" + l.k).join(" ");

// Un lundi, pour que J+2 / J+6 / J+13 tombent en semaine (sauf quand on teste le week-end).
const LUNDI = "2026-10-05";

Deno.test("compte neuf sans diagnostic : P-X0N (confirmation) puis 2 rappels, rien d'autre", () => {
  const e: Eleve = { debut: LUNDI, express: null };
  const logs = simuler(e);
  invariants("neuf", logs, e);
  assert(types(logs) === "P-X0N@J1 P-X0R1@J4 P-X0R2@J21", "séquence : " + types(logs)); // J+19/J+20 = week-end → lundi J+21
});

Deno.test("express fait, pas de confirmation, inactif : rappels + relance d'usage, AUCUNE offre", () => {
  const e: Eleve = { debut: LUNDI, express: 0 };
  const logs = simuler(e);
  invariants("express inactif", logs, e);
  assert(!logs.some((l) => l.cat === "M"), "aucun commercial");
  assert(logs.some((l) => l.type === "D3:P-X0R1") && logs.some((l) => l.type === "D3:P-X2b"), "R1 + P-X2b : " + types(logs));
});

Deno.test("express + accord + opt-in + actif : P-X1, P-X2, P-X3 puis plus rien", () => {
  const e: Eleve = { debut: LUNDI, express: 0, consent: 0, optin: true, actifs: [0, 1, 2, 4] };
  const logs = simuler(e, 60);
  invariants("convertible", logs, e);
  assert(types(logs) === "P-X1@J2 P-X2@J7 P-X3@J14", "séquence : " + types(logs)); // J+6 et J+13 = dimanches → reportés au lundi
  assert(!logs.some((l) => l.cat === "M" && l.k > 20), "rien de commercial après la fenêtre P-X3");
});

Deno.test("opt-in mais tout vert (aucun point fragile) : pas de P-X1", () => {
  const e: Eleve = { debut: LUNDI, express: 0, consent: 0, optin: true, pfFragile: false, actifs: [1, 2, 3] };
  const logs = simuler(e);
  invariants("tout vert", logs, e);
  assert(!logs.some((l) => l.type === "D3:P-X1"), types(logs));
});

Deno.test("achat du diagnostic à J+4 : la conversion s'arrête, relances modules puis post-bilan", () => {
  const e: Eleve = { debut: LUNDI, express: 0, consent: 0, optin: true, actifs: [0, 1, 5, 6, 7, 8, 12, 13, 14, 15], achatDiag: 4, complet: 9, emailEleve: true };
  const logs = simuler(e, 40);
  invariants("acheteur diag", logs, e);
  assert(!logs.some((l) => /^D3:P-X[23]$/.test(l.type)), "pas de P-X2/P-X3 après l'achat : " + types(logs));
  assert(logs.some((l) => l.type === "D3:P-UP1") && logs.some((l) => l.type === "D3:P-UP2"), "P-UP1 + P-UP2 : " + types(logs));
  assert(logs.some((l) => l.type === "D3:A-X0") && logs.every((l) => l.dest !== "ado" || l.cat === "P"), "ado : A-X0, pédagogique");
});

Deno.test("diagnostic acheté mais jamais fini : A-MOD puis P-MOD, une seule fois chacun", () => {
  const e: Eleve = { debut: LUNDI, express: 0, consent: 0, achatDiag: 1, emailEleve: true };
  const logs = simuler(e);
  invariants("modules", logs, e);
  assert(logs.filter((l) => l.type === "D3:A-MOD").length === 1 && logs.filter((l) => l.type === "D3:P-MOD").length === 1, types(logs));
});

Deno.test("Programme Brevet : bilan du dimanche, suspendu après 2 semaines sans exo ; re-diagnostic le 1er samedi", () => {
  const e: Eleve = { debut: "2026-10-26", express: 0, consent: 0, optin: true, programme: 0, complet: 1, actifs: [1, 2, 3, 8, 9], emailEleve: true, rediag: true };
  const logs = simuler(e, 40);
  invariants("programme", logs, e);
  const hebdo = logs.filter((l) => l.type.startsWith("D3:P-HEBDO:"));
  assert(hebdo.length >= 2 && hebdo.every((l) => dow(l.date) === 0), "hebdo le dimanche : " + types(hebdo));
  assert(!hebdo.some((l) => l.k > 9 + 14), "suspendu après 2 semaines sans entraînement : " + types(hebdo));
  assert(logs.some((l) => l.type === "D3:A-MENS:2026-11" && l.date === "2026-11-07"), "A-MENS 1er samedi : " + types(logs));
  assert(!logs.some((l) => /^D3:P-(X[123]|UP[12])$/.test(l.type)), "aucune relance commerciale pour un client du programme");
});

Deno.test("aucun email commercial entre le 15 mai et le 31 août", () => {
  const e: Eleve = { debut: "2027-05-10", express: 0, consent: 0, optin: true, actifs: [0, 1, 2, 3] };
  const logs = simuler(e);
  invariants("mai", logs, e);
  assert(!logs.some((l) => l.cat === "M" && l.date >= "2027-05-15"), types(logs));
});

Deno.test("ado : 1 seul rappel (A-X1) si aucun exo, jamais le jour où il s'entraîne", () => {
  const e: Eleve = { debut: LUNDI, express: 0, consent: 0, emailEleve: true };
  const logs = simuler(e);
  invariants("ado", logs, e);
  assert(types(logs.filter((l) => l.dest === "ado")) === "A-X0@J0 A-X1@J1", types(logs));
  const actif: Eleve = { ...e, actifs: [1] };
  assert(!simuler(actif).some((l) => l.type === "D3:A-X1"), "pas de rappel si l'ado s'est entraîné");
});

Deno.test("fuzz : 300 élèves fictifs aléatoires, invariants toujours vrais", () => {
  let s = 12345;
  const r = () => { s = (s * 1103515245 + 12345) % 2147483648; return s / 2147483648; };
  const opt = (p: number, max: number) => (r() < p ? Math.floor(r() * max) : null);
  for (let i = 0; i < 300; i++) {
    const debut = add("2026-09-01", Math.floor(r() * 300));
    const express = opt(0.8, 5);
    const achatDiag = express !== null ? opt(0.3, 20) : null;
    const e: Eleve = {
      debut, express, consent: opt(0.6, 10), optin: r() < 0.5, emailEleve: r() < 0.5, pfFragile: r() < 0.8,
      achatDiag, programme: opt(0.15, 25), complet: achatDiag !== null ? (r() < 0.6 ? achatDiag + Math.floor(r() * 8) : null) : null,
      actifs: [...new Set(Array.from({ length: Math.floor(r() * 20) }, () => Math.floor(r() * 40)))].sort((a, b) => a - b), rediag: r() < 0.5,
    };
    invariants("fuzz#" + i + " " + JSON.stringify(e), simuler(e, 45), e);
  }
});
