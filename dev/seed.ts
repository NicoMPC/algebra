// ════════════════════════════════════════════════════════════
//  Matheux — seed de la base de dev
//  1. Référentiel + banque 3e : même mapping que supabase/import_referentiel_banque.py
//     (on appelle directement ses fonctions via python3 → aucune duplication de logique).
//  2. Chapitres legacy (curriculum 3e = data/*_v4.json, 6e/5e/4e = data/bank_*), diagnostic_exos.
//  3. Comptes : admin + 3 élèves à des stades différents, fabriqués EN PASSANT PAR L'API
//     (register, start/answer_diagnostic, webhook Stripe signé, get_training, save_score) avec
//     l'horloge de dev décalée dans le passé : l'état obtenu est celui que la prod produirait.
// ════════════════════════════════════════════════════════════
import type { FakeSupabase } from "./fake_supabase.ts";

type Api = (p: Record<string, unknown>) => Promise<Record<string, unknown>>;
type Deps = {
  fake: FakeSupabase; callApi: Api; root: string;
  simulerPaiement: (code: string, produit: string) => Promise<Record<string, unknown>>;
  setOffsetDays: (n: number) => void;
};

export const COMPTES = {
  admin: { code: "KN6CFG", prenom: "Nicolas", email: "nicolas.follezou@hotmail.fr", mdp: "matheux-dev" },
  neuf: { prenom: "Lina", email: "lina@exemple.fr", mdp: "matheux-dev" },
  express: { prenom: "Tom", email: "tom@exemple.fr", mdp: "matheux-dev" },
  programme: { prenom: "Sarah", email: "sarah@exemple.fr", mdp: "matheux-dev" },
};

// Même hash que app.html (_hashPw) : SHA-256(email + '::' + mdp + '::AB22') — l'app envoie ce hash comme mot de passe.
export async function hashApp(email: string, mdp: string) {
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(email.toLowerCase() + "::" + mdp + "::AB22"));
  return Array.from(new Uint8Array(h)).map((x) => x.toString(16).padStart(2, "0")).join("");
}

function hash01(s: string) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0) / 4294967296; }

async function importReferentiel(d: Deps) {
  const py = `
import sys, json, os
sys.path.insert(0, os.path.join(${JSON.stringify(d.root)}, "supabase"))
import import_referentiel_banque as m
err, av = [], []
comps = m.valider_referentiel(m.charger_json(os.path.join(m.RACINE, "data/referentiel_3eme/competences.json")), err)
fichiers, items = m.charger_items(os.path.join(m.RACINE, "data/banque_3eme"))
m.valider_items(items, comps, err, av)
print(json.dumps({"erreurs": err, "avert": len(av), "competences": m.lignes_competences(comps), "items": m.lignes_items(items)}, ensure_ascii=False))
`;
  const out = await new Deno.Command("python3", { args: ["-c", py], stdout: "piped", stderr: "piped" }).output();
  if (!out.success) throw new Error("import référentiel (python3) : " + new TextDecoder().decode(out.stderr));
  const r = JSON.parse(new TextDecoder().decode(out.stdout));
  if (r.erreurs.length) throw new Error("référentiel/banque invalides : " + r.erreurs.slice(0, 5).join(" | "));
  const now = new Date().toISOString().replace("Z", "+00:00");
  d.fake.state.tables.competences = r.competences.map((c: Record<string, unknown>) => ({ ...c, updated_at: now }));
  d.fake.state.tables.items = r.items.map((i: Record<string, unknown>) => ({ ...i, updated_at: now }));
  console.log(`[seed] référentiel : ${r.competences.length} compétences, ${r.items.length} items (${r.avert} avertissements, cf. --dry-run)`);
}

async function importLegacy(d: Deps) {
  const cur = d.fake.state.tables.curriculum = [] as Record<string, unknown>[];
  let id = 0;
  const add = (niveau: string, categorie: string, exos: unknown) => {
    const titre = categorie.replace(/_v4$/, "").replace(/_Brevet$/, "").replace(/^Auto_/, "Automatismes ").replace(/_/g, " ");
    cur.push({ id: ++id, niveau, categorie, titre, icone: null, exos_json: exos, timer: categorie.startsWith("Auto_") ? 30 : 60, ordered: false });
  };
  for await (const e of Deno.readDir(`${d.root}/data`)) {
    if (e.isFile && e.name.endsWith("_v4.json")) add("3EME", e.name.replace(/_v4\.json$/, ""), JSON.parse(await Deno.readTextFile(`${d.root}/data/${e.name}`)));
  }
  for (const n of ["6", "5", "4"]) {
    try {
      for await (const e of Deno.readDir(`${d.root}/data/bank_${n}eme`)) {
        if (e.isFile && e.name.endsWith(".json")) add(`${n}EME`, e.name.replace(/\.json$/, ""), JSON.parse(await Deno.readTextFile(`${d.root}/data/bank_${n}eme/${e.name}`)));
      }
    } catch { /* dossier absent */ }
  }
  d.fake.state.seq.curriculum = id;
  const diag = JSON.parse(await Deno.readTextFile(`${d.root}/data/diagnostic_3eme.json`)) as Record<string, unknown>[];
  const parCat: Record<string, unknown[]> = {};
  for (const x of diag) (parCat[String(x.categorie)] ||= []).push(x);
  d.fake.state.tables.diagnostic_exos = Object.entries(parCat).map(([categorie, exos], i) => ({ id: i + 1, niveau: "3EME", categorie, exos_json: exos }));
  d.fake.state.seq.diagnostic_exos = Object.keys(parCat).length;
  console.log(`[seed] legacy : ${cur.length} chapitres curriculum, ${Object.keys(parCat).length} catégories diagnostic_exos`);
}

// ── Élève simulé : répond selon un profil (compétences faibles), de façon déterministe ──
type Profil = { faibles: RegExp; pFort: number; pFaible: number; graine: string };
function repondre(d: Deps, itemId: string, prof: Profil, bonus = 0): { reponse: string; ok: boolean } {
  const row = d.fake.rows("items").find((r) => r.id === itemId);
  const it = (row?.item_json || {}) as Record<string, unknown>;
  const comp = String(it.comp || row?.comp || "");
  const p = Math.min(0.97, (prof.faibles.test(comp) ? prof.pFaible : prof.pFort) + bonus);
  const ok = hash01(prof.graine + "|" + itemId + "|" + bonus) < p;
  if (ok) return { reponse: String(it.a ?? ""), ok: true };
  const errs = Object.keys((it.err || {}) as Record<string, string>);
  if (errs.length) return { reponse: errs[Math.floor(hash01(prof.graine + itemId) * errs.length)], ok: false };
  const opts = ((it.options || []) as string[]).filter((o) => o !== it.a);
  return { reponse: opts[0] ?? "", ok: false }; // "" = je ne sais pas
}

async function inscrire(d: Deps, c: { prenom: string; email: string; mdp: string }) {
  const r = await d.callApi({ action: "register", name: c.prenom, email: c.email, level: "3EME", password: await hashApp(c.email, c.mdp), objectif: "brevet" });
  if (r.status !== "success") throw new Error("register " + c.email + " : " + r.message);
  return String((r.profile as Record<string, unknown>).code);
}

async function faireDiagnostic(d: Deps, code: string, type: string, prof: Profil) {
  let r = await d.callApi({ action: "start_diagnostic", code, type });
  if (r.status !== "success") throw new Error(`start_diagnostic ${type} ${code} : ${r.message}`);
  const id = r.diagnostic_id;
  let n = 0;
  while (r.question && n < 200) {
    const q = r.question as Record<string, unknown>;
    const { reponse } = repondre(d, String(q.id), prof);
    r = await d.callApi({ action: "answer_diagnostic", code, diagnostic_id: id, item_id: q.id, reponse, temps: 20 + Math.round(hash01(String(q.id)) * 40) });
    if (r.status !== "success") throw new Error(`answer_diagnostic ${code} : ${r.message}`);
    n++;
    if (!r.question && r.fin_module && !r.termine) r = await d.callApi({ action: "start_diagnostic", code, type }); // module suivant (reprise)
  }
  if (!r.termine) throw new Error(`diagnostic ${type} ${code} non terminé après ${n} questions`);
  return n;
}

async function faireEntrainement(d: Deps, code: string, prenom: string, prof: Profil, bonus: number, email: string) {
  const r = await d.callApi({ action: "get_training", code, email });
  if (r.status !== "success") throw new Error(`get_training ${code} : ${r.message}`);
  const exos = ((r.boost as Record<string, unknown>).exos || []) as Record<string, unknown>[];
  for (const e of exos) {
    const { reponse, ok } = repondre(d, String(e.item_id), prof, bonus);
    const s = await d.callApi({
      action: "save_score", code, email, name: prenom, level: "3EME", categorie: e.categorie, exercice_idx: e.num,
      resultat: ok ? "EASY" : "HARD", source: "BOOST", item_id: e.item_id, comp: e.comp, q: e.q, reponse, wrongOpt: ok ? "" : reponse,
      time: 30 + Math.round(hash01(String(e.item_id)) * 50), type: e.type, nbOptions: ((e.options || []) as unknown[]).length,
    });
    if (s.status !== "success") throw new Error(`save_score ${code} : ${s.message}`);
  }
  return exos.length;
}

export async function seed(d: Deps) {
  // Math.random déterministe pendant le seed → mêmes codes élèves à chaque reset
  const realRandom = Math.random;
  let st = 0x9e3779b9;
  Math.random = () => { st = (st + 0x6d2b79f5) | 0; let t = Math.imul(st ^ (st >>> 15), 1 | st); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  try { return await seedInner(d); } finally { Math.random = realRandom; }
}

async function seedInner(d: Deps) {
  await importReferentiel(d);
  await importLegacy(d);

  // Admin (compte existant en prod, recréé ici avec un mot de passe de DEV)
  const a = COMPTES.admin;
  d.setOffsetDays(-30);
  const au = await d.fake.createUser(a.email, await hashApp(a.email, a.mdp));
  const today = () => new Date().toLocaleDateString("sv-SE", { timeZone: "Europe/Paris" });
  const now = () => new Date().toISOString().replace("Z", "+00:00");
  d.fake.state.tables.profiles.push({
    id: au.id, code: a.code, prenom: a.prenom, niveau: "3EME", email: a.email, password_hash: null, date_inscription: today(),
    is_admin: true, premium: true, trial_start: today(), premium_end: null, free_chapter: null, is_test: true, pending_brevet: null,
    revision_chapters: null, objectif: null, created_at: now(), updated_at: now(), email_eleve: null, consentement_parent_at: null,
    optin_marketing: false, optin_marketing_at: null, date_brevet_blanc: null, premium_niveau: "3EME", mode: null,
  });

  // 1. Lina — compte neuf (inscrite aujourd'hui, rien fait)
  d.setOffsetDays(0);
  const lina = await inscrire(d, COMPTES.neuf);

  // 2. Tom — diagnostic express fait hier (fractions / relatifs fragiles)
  d.setOffsetDays(-1);
  const tom = await inscrire(d, COMPTES.express);
  const nTom = await faireDiagnostic(d, tom, "express", { faibles: /^NC\.(FRAC|REL|PUIS)/, pFort: 0.85, pFaible: 0.2, graine: "tom" });

  // 3. Sarah — express il y a 11 jours, Programme Brevet payé, diagnostic complet, puis 10 jours d'entraînement
  d.setOffsetDays(-11);
  const sarah = await inscrire(d, COMPTES.programme);
  const profS: Profil = { faibles: /^(NC\.(LIT|EQUA|FRAC)|DF\.(AFF|FONC))/, pFort: 0.8, pFaible: 0.3, graine: "sarah" };
  const nS1 = await faireDiagnostic(d, sarah, "express", profS);
  const pay = await d.simulerPaiement(sarah, "programme_brevet");
  if (pay.status !== "success") throw new Error("paiement Sarah : " + JSON.stringify(pay));
  const nS2 = await faireDiagnostic(d, sarah, "complet", profS);
  let nTrain = 0;
  for (let j = 10; j >= 1; j--) {
    d.setOffsetDays(-j);
    nTrain += await faireEntrainement(d, sarah, COMPTES.programme.prenom, profS, (10 - j) * 0.04, COMPTES.programme.email);
  }
  d.setOffsetDays(0);
  console.log(`[seed] comptes : admin ${a.code} · Lina ${lina} (neuve) · Tom ${tom} (express ${nTom} q) · Sarah ${sarah} (express ${nS1} q + complet ${nS2} q + ${nTrain} exos sur 10 j)`);
  return { lina, tom, sarah };
}
