// ════════════════════════════════════════════════════════════
//  Tests du moteur « Diagnostic 3e » : logique pure, sans Supabase.
//  Lancer : deno test --allow-read --allow-write supabase/tests/moteur_test.ts
//
//  Le bloc MOTEUR_PUR_DEBUT…MOTEUR_PUR_FIN de supabase/functions/api/index.ts est
//  extrait tel quel dans un module temporaire : on teste le vrai code, pas une copie.
//
//  Méthode : le moteur est déterministe, l'élève simulé est aléatoire. On lance donc des
//  CAMPAGNES (N graines par profil) :
//    - invariants durs : vérifiés sur CHAQUE exécution (jamais conclure sur 1 réponse, budget,
//      5 exos/jour, prérequis en lacune jamais sautés, zone gratuite respectée…) ;
//    - résultats pédagogiques : vérifiés en TAUX (ex. « la cause racine est trouvée dans ≥ 90 %
//      des cas »), parce qu'un élève simulé peut deviner juste ou faire une étourderie.
//  Référentiels : fixtures/competences_mini.json (19 compétences) ET le référentiel réel
//  data/referentiel_3eme/competences.json (121 compétences), banques synthétiques générées ici.
// ════════════════════════════════════════════════════════════

// deno-lint-ignore-file no-explicit-any
const ICI = new URL(".", import.meta.url);
const src = await Deno.readTextFile(new URL("../functions/api/index.ts", ICI));
const debut = src.lastIndexOf("\n", src.indexOf("MOTEUR_PUR_DEBUT"));
const fin = src.indexOf("MOTEUR_PUR_FIN");
if (debut < 0 || fin < 0) throw new Error("Marqueurs MOTEUR_PUR introuvables dans index.ts");
const bloc = src.slice(debut, fin);
const noms = [...bloc.matchAll(/^(?:function|const) ([mM][xX][A-Za-z0-9_]*)/gm)].map((m) => m[1]);
const tmp = await Deno.makeTempFile({ suffix: ".ts" });
await Deno.writeTextFile(tmp, bloc + "\nexport { " + [...new Set(noms)].join(", ") + " };\n");
const M: any = await import("file://" + tmp);

// ── Outils ──────────────────────────────────────────────────
function assert(cond: unknown, msg: string): asserts cond {
  if (!cond) throw new Error("ÉCHEC : " + msg);
}
function taux(nom: string, oks: boolean[], min: number) {
  const t = oks.filter(Boolean).length / oks.length;
  console.log(`    ${t >= min ? "✓" : "✗"} ${nom} : ${Math.round(t * 100)} % (seuil ${Math.round(min * 100)} %)`);
  assert(t >= min, `${nom} : ${Math.round(t * 100)} % < ${Math.round(min * 100)} %`);
}
function mulberry32(seed: number) {
  return () => {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const clone = <T>(x: T): T => JSON.parse(JSON.stringify(x)); // = aller-retour en base (etat_json)
const DATE0 = "2026-10-01";

// ── Banque synthétique : 24 items / compétence (8 QCM, 12 fill, 4 VF ; niveaux 1-3 mélangés) ──
function genererBanque(comps: any[]) {
  const items: any[] = [];
  for (const c of comps) {
    const errId = (c.erreurs && c.erreurs[0]?.id) || null;
    for (let k = 0; k < 24; k++) {
      const id = `${c.id}-${String(k).padStart(3, "0")}`;
      const lvl = 1 + (Math.floor(k / 2) % 3);
      const usage = k < 10 ? ["diag", "train"] : ["train"]; // y compris hors programme : le moteur doit les écarter du diag
      const depend = k === 23 ? { depend_question_precedente: true } : {};
      const t = k % 6;
      if (t === 0 || t === 3) {
        items.push({ id, comp: c.id, q: `QCM ${id}`, a: `R${k}`, type: "qcm", options: [`R${k}`, `E${k}`, `Z${k}`],
          err: errId ? { [`E${k}`]: errId } : {}, steps: ["?"], f: "", lvl, usage });
      } else if (t === 5) {
        items.push({ id, comp: c.id, q: `VF ${id}`, a: "Vrai", type: "vf", options: ["Vrai", "Faux"], err: {}, steps: [], f: "", lvl, usage });
      } else {
        items.push({ id, comp: c.id, q: `Calcule ${id} ___`, a: `${k + 10}/7`, type: "fill", options: [],
          err: errId ? { [`${k + 3}/9`]: errId } : {}, steps: ["?"], f: "", lvl, usage, ...depend });
      }
    }
  }
  return items;
}
function charger(chemin: URL) {
  const comps = JSON.parse(Deno.readTextFileSync(chemin));
  return { comps, ref: M.mxIndexer(comps, genererBanque(comps)) };
}
const MINI = charger(new URL("fixtures/competences_mini.json", ICI));
const REEL = charger(new URL("../../data/referentiel_3eme/competences.json", ICI));

// ── Élève simulé ────────────────────────────────────────────
type Eleve = { nom: string; p: Record<string, number>; hasard?: boolean; rng: () => number };
function eleve(comps: any[], nom: string, base: (c: any) => number, special: Record<string, number>, seed: number, hasard = false): Eleve {
  const p: Record<string, number> = {};
  for (const c of comps) p[c.id] = special[c.id] ?? base(c);
  return { nom, p, hasard, rng: mulberry32(seed) };
}
function repondre(e: Eleve, it: any): { reponse: string; temps: number } {
  const r = e.rng;
  if (e.hasard) {
    const opts = it.options || [];
    return { reponse: opts.length ? opts[Math.floor(r() * opts.length)] : "42", temps: 2 + r() * 1.5 };
  }
  const temps = 15 + r() * 45;
  if (r() < e.p[it.comp]) return { reponse: it.a, temps };
  const errKeys = Object.keys(it.err || {});
  if (it.type === "fill") {
    if (r() < 0.2) return { reponse: "", temps }; // « je ne sais pas »
    return { reponse: errKeys.length && r() < 0.6 ? errKeys[0] : "???", temps };
  }
  if (errKeys.length && r() < 0.7) return { reponse: errKeys[0], temps };
  const opts = it.options || [];
  return { reponse: opts[Math.floor(r() * opts.length)], temps }; // devine
}

function simulerDiag(R: any, e: Eleve, type: string, mt: Record<string, any>, graines?: any[]) {
  let etat = M.mxDemarrerDiag(R.ref, type, "SIM" + e.nom.slice(0, 3).toUpperCase(), { graines, maitrise: mt });
  let finsModule = 0, poses = 0;
  const dejaVus: string[] = [];
  for (let garde = 0; garde < 500; garde++) {
    etat = clone(etat);
    const q = M.mxProchaineQuestion(etat, R.ref, dejaVus);
    if ("fin" in q) break;
    if ("fin_module" in q) { finsModule++; continue; }
    etat = clone(etat); // reprise possible entre la question et la réponse
    const { reponse, temps } = repondre(e, q.item);
    const res = M.mxEnregistrerReponse(etat, R.ref, q.item.id, reponse, temps, DATE0);
    assert(!("error" in res), "réponse refusée : " + JSON.stringify(res));
    const o = res.obs;
    mt[o.comp] = M.mxMajMaitrise(mt[o.comp], o.comp, o.ok, o.w, o.err, DATE0);
    dejaVus.push(o.item_id);
    poses++;
  }
  const carte = M.mxCalculerCarte(R.ref, mt, { type, eleve: { prenom: e.nom, niveau: "3EME" }, date: DATE0, obs: etat.obs });
  return { etat, carte, poses, finsModule, mt };
}

function simulerEntrainement(R: any, e: Eleve, mt: Record<string, any>, zone: string[] | null, jours = 30) {
  const historique: any[] = [];
  const journal: any[] = [];
  for (let j = 0; j < jours; j++) {
    const date = M.mxAjoutJours(DATE0, j + 1);
    const avant = clone(mt);
    const sel = M.mxChoisirEntrainement(R.ref, mt, { code: "SIM" + e.nom, date, zone, historique });
    journal.push({ date, sel, mtAvant: avant });
    for (const x of sel.exos) {
      const { reponse } = repondre(e, x.item);
      const { ok } = M.mxCorriger(x.item, reponse);
      const err = ok ? null : M.mxErreurType(x.item, reponse);
      mt[x.item.comp] = M.mxMajMaitrise(mt[x.item.comp], x.item.comp, ok, M.mxPoidsSucces(x.item), err, date);
      historique.push({ item_id: x.item.id, date, ok, contexte: "train" });
      // Apprentissage simulé : progrès seulement si les prérequis directs sont là.
      const c = R.ref.comps[x.item.comp];
      const pret = c.prerequis.every((pq: string) => (e.p[pq] ?? 1) >= 0.7);
      e.p[c.id] = Math.min(0.95, e.p[c.id] + (pret ? 0.07 : 0.005));
    }
  }
  return journal;
}

const parId = (carte: any) => Object.fromEntries(carte.competences.map((c: any) => [c.id, c]));

// Invariants durs, vérifiés sur chaque exécution
function invariantsCarte(R: any, nom: string, carte: any) {
  const S = parId(carte);
  for (const c of carte.competences) {
    if (c.statut !== "non_evalue") assert(c.n_obs >= 2, `${nom} : ${c.id} conclu sur ${c.n_obs} obs`);
    if (c.cause_racine) {
      assert(c.statut === "lacune", `${nom} : cause racine ${c.id} non lacune`);
      assert(R.ref.desc2[c.id].some((d: string) => S[d]?.statut === "lacune"), `${nom} : cause racine ${c.id} sans lacune à distance ≤ 2`);
    }
    for (const e of c.erreurs) assert("libelle_parent" in e && "remediation" in e, `${nom} : erreur ${e.id} sans libelle_parent/remediation`);
    assert(c.niveau_origine && c.titre, `${nom} : ${c.id} sans niveau_origine/titre`);
  }
  if (carte.type !== "mensuel") for (const id of M.MX_HORS_DIAG) assert(!(id in S), `${nom} : ${id} (hors programme) évalué en diagnostic`);
  assert(carte.plan_4_semaines.length === 4, `${nom} : plan ≠ 4 semaines`);
  assert(typeof carte.phrase_cle === "string" && carte.phrase_cle.length > 20, `${nom} : phrase_cle absente`);
  carte.priorites.forEach((id: string, i: number) => {
    for (const a of R.ref.anc2[id]) {
      if (S[a]?.statut !== "lacune") continue;
      const j = carte.priorites.indexOf(a);
      assert(j < 0 || j < i, `${nom} : priorité ${id} avant son prérequis en lacune ${a}`);
    }
  });
  assert(!/\bprof\b|Nicolas|prépare/i.test(carte.message_parent + " " + carte.phrase_cle), `${nom} : texte laissant croire à une intervention humaine`);
}
function invariantsEntrainement(R: any, nom: string, journal: any[], zone: string[] | null) {
  const vuLe: Record<string, string> = {};
  journal.forEach((j: any, idx: number) => {
    assert(j.sel.exos.length === 5, `${nom} J${idx + 1} : ${j.sel.exos.length} exos`);
    assert(new Set(j.sel.exos.map((x: any) => x.item.id)).size === 5, `${nom} J${idx + 1} : doublon dans la journée`);
    for (const x of j.sel.exos) {
      assert(!x.item.depend_question_precedente, `${nom} : sous-question dépendante servie seule`);
      if (zone) assert(zone.includes(x.item.comp), `${nom} : ${x.item.comp} hors zone gratuite`);
      if (x.role === "travail") {
        const bloque = R.ref.anc2[x.item.comp].some((a: string) => M.mxStatut(j.mtAvant[a]) === "lacune" && (!zone || zone.includes(a)));
        assert(!bloque, `${nom} J${idx + 1} : travail sur ${x.item.comp} alors qu'un prérequis proche est en lacune`);
      }
      const prev = vuLe[x.item.id];
      assert(!prev || M.mxJoursEntre(prev, j.date) >= 3, `${nom} : item ${x.item.id} resservi trop tôt (${prev} → ${j.date})`);
      vuLe[x.item.id] = j.date;
    }
  });
}

// Campagne pour un profil : express → complet (graines de l'express) → 30 j d'entraînement (programme)
function campagne(R: any, fabrique: (seed: number) => Eleve, n: number, opts: { gratuit?: boolean } = {}) {
  const out: any[] = [];
  for (let s = 1; s <= n; s++) {
    const exp = simulerDiag(R, fabrique(s), "express", {});
    assert(exp.poses <= 15, `express ${exp.poses} q > 15`);
    invariantsCarte(R, "express", exp.carte);
    const mtC: Record<string, any> = {};
    for (const o of exp.etat.obs) mtC[o.comp] = M.mxMajMaitrise(mtC[o.comp], o.comp, o.ok, o.w, o.err, DATE0);
    const comp = simulerDiag(R, fabrique(s + 1000), "complet", mtC, exp.etat.obs);
    assert(comp.poses <= 64, `complet ${comp.poses} q > 64`);
    assert(comp.finsModule === 2, `complet : ${comp.finsModule} pauses entre modules (attendu 2)`);
    invariantsCarte(R, "complet", comp.carte);
    const e = fabrique(s + 2000);
    const mtT = clone(comp.mt);
    const journal = simulerEntrainement(R, e, mtT, null);
    invariantsEntrainement(R, "programme", journal, null);
    let gratuit: any = null;
    if (opts.gratuit) {
      const mtG: Record<string, any> = {};
      for (const o of exp.etat.obs) mtG[o.comp] = M.mxMajMaitrise(mtG[o.comp], o.comp, o.ok, o.w, o.err, DATE0);
      const zone = M.mxZoneGratuite(exp.carte);
      assert(zone && zone.includes(exp.carte.point_faible), "zone gratuite sans le point faible");
      const jg = simulerEntrainement(R, fabrique(s + 3000), mtG, zone);
      invariantsEntrainement(R, "gratuit", jg, zone);
      gratuit = { zone, mt: mtG, pf: exp.carte.point_faible };
    }
    out.push({ exp, comp, journal, mtFin: mtT, gratuit });
  }
  return out;
}

// ════════════════════════════════════════════════════════════
Deno.test("unitaire : correction, poids QCM, erreurs types, statut, droits, streak", () => {
  const it = { id: "x", comp: "NC.FRAC.03", q: "", a: "7/12", type: "fill", err: { "2/7": "NC.FRAC.03#somme_directe" } };
  assert(M.mxCorriger(it, "$\\frac{7}{12}$").ok, "fraction LaTeX acceptée");
  assert(M.mxCorriger(it, "14/24").ok, "égalité numérique acceptée");
  const c = M.mxCorriger(it, "2/7");
  assert(!c.ok && c.err === "NC.FRAC.03#somme_directe", "erreur type reconnue");
  assert(!M.mxCorriger(it, "").ok, "« je ne sais pas » = échec");
  // comparaison stricte (correctif « 4x+3 » d'app.html), alt, unités, erreurs types brutes
  assert(!M.mxEgal("4x+3", "4x+12") && !M.mxEgal("4x+3", "4"), "pas de parseFloat sur une entrée libre");
  assert(M.mxEgal("12 cm", "12") && M.mxEgal("2,5", "2.5") && M.mxEgal("0,25", "25%") && M.mxEgal("1/4", "0.25"), "équivalences numériques");
  assert(!M.mxEgal("1.2.3", "1.2") && M.mxNum("3/0") === null, "nombres mal formés refusés");
  const pc = { id: "p", comp: "X", q: "", a: "0,25", alt: ["25%"], type: "fill", err: { "2,50": "X#virgule", "\\sqrt{10}": "X#racine" } };
  assert(M.mxCorriger(pc, "25 %").ok, "alt pourcentage accepté");
  assert(M.mxCorriger(pc, "2.5").err === "X#virgule", "clé err brute « 2,50 » normalisée");
  assert(M.mxCorriger(pc, "sqrt(10)").err === "X#racine", "clé err LaTeX \\sqrt{10} normalisée");
  assert(M.mxPoidsSucces({ type: "qcm", options: ["a", "b", "c"] }) < 0.7, "QCM 3 options pondéré");
  assert(M.mxPoidsSucces({ type: "vf" }) === 0.5, "VF = 0.5");
  let m = M.mxMajMaitrise(null, "X", true, 1, null, DATE0);
  assert(M.mxStatut(m) === "non_evalue", "1 obs → non évalué");
  m = M.mxMajMaitrise(m, "X", true, 1, null, DATE0);
  assert(M.mxStatut(m) === "acquis", "2 succès ouverts → acquis");
  assert(m.prochaine_revision && m.prochaine_revision > DATE0, "révision espacée planifiée");
  let q = M.mxMajMaitrise(null, "X", true, 2 / 3, null, DATE0);
  q = M.mxMajMaitrise(q, "X", true, 2 / 3, null, DATE0);
  assert(M.mxStatut(q) !== "acquis", "2 succès QCM ne suffisent pas à conclure « acquis »");
  let l = M.mxMajMaitrise(null, "X", false, 1, "e1", DATE0);
  l = M.mxMajMaitrise(l, "X", false, 1, "e1", DATE0);
  assert(M.mxStatut(l) === "lacune" && l.erreurs_vues.e1 === 2, "2 échecs → lacune + erreurs comptées");
  assert(M.mxCycles(MINI.ref).length === 0 && M.mxCycles(REEL.ref).length === 0, "référentiels acycliques");
  const t = "2026-10-01";
  assert(M.mxDroits({}, [], t).acces === "free", "free par défaut");
  const d = M.mxDroits({}, [{ produit: "diagnostic_complet" }], t);
  assert(d.acces === "diagnostic_complet" && !d.entrainement_complet && d.prix_cents.programme_brevet === 3000, "diag complet : 19 € déduits");
  assert(M.mxDroits({ premium: true }, [], t).acces === "programme_brevet", "premium legacy = programme");
  assert(M.mxDroits({ premium: true, premium_end: "2026-06-30" }, [], t).acces === "free", "premium expiré");
  assert(M.mxStreak(["2026-10-01", "2026-10-02", "2026-10-03"], "2026-10-03").streak === 3, "streak 3 jours");
  assert(M.mxStreak(["2026-10-01", "2026-10-02"], "2026-10-03").streak === 2, "streak conservé tant qu'aujourd'hui n'est pas fini");
  assert(M.mxStreak(["2026-10-01", "2026-10-02", "2026-10-04"], "2026-10-04").streak === 3, "gel 1 jour (G3)");
  assert(M.mxStreak(["2026-10-01"], "2026-10-05").streak === 0, "streak perdu");
});

Deno.test("mini-référentiel : 4 profils × 20 graines", () => {
  const C = MINI.comps;
  const DEP_REL = ["NC.LIT.01", "NC.LIT.03", "NC.EQUA.02", "NC.EQUA.04", "DF.FONC.02", "AP.SCR.02"];
  const rel = campagne(MINI, (s) => eleve(C, "Rel", () => 0.92, { "NC.REL.01": 0.1, "NC.REL.02": 0.1, "NC.LIT.01": 0.15,
    "NC.LIT.03": 0.1, "NC.EQUA.02": 0.15, "NC.EQUA.04": 0.1, "DF.FONC.02": 0.15, "AP.SCR.02": 0.2 }, 1100 + s), 20, { gratuit: true });
  const bon = campagne(MINI, (s) => eleve(C, "Bon", () => 0.95, { "NC.FRAC.03": 0.05, "DF.PROB.02": 0.15 }, 2200 + s), 20);
  const has = campagne(MINI, (s) => eleve(C, "Has", () => 0, {}, 3300 + s, true), 20);
  const moy = campagne(MINI, (s) => eleve(C, "Moy", (c) =>
    c.niveau_origine === "6EME" || c.niveau_origine === "5EME" ? 0.9 : c.niveau_origine === "4EME" ? 0.6 : 0.4, {}, 4400 + s), 20);

  console.log("  1. cause racine sur les relatifs");
  taux("express : point faible = relatifs", rel.map((r) => String(r.exp.carte.point_faible).startsWith("NC.REL.")), 0.9);
  taux("complet : priorité n°1 = relatifs", rel.map((r) => r.comp.carte.priorites[0]?.startsWith("NC.REL.")), 0.95);
  taux("complet : une cause racine relatifs identifiée", rel.map((r) => ["NC.REL.01", "NC.REL.02"].some((id) => parId(r.comp.carte)[id]?.cause_racine)), 0.9);
  taux("complet : la géométrie ressort en point fort", rel.map((r) => r.comp.carte.points_forts.some((id: string) => id.startsWith("EG."))), 0.9);
  taux("complet : erreur type nommée avec exemple", rel.map((r) => r.comp.carte.competences.some((c: any) => c.erreurs.some((x: any) => x.exemple && x.libelle !== x.id))), 0.9);
  taux("J1-5 : ≥ 60 % du travail sur les relatifs", rel.map((r) => {
    const t = r.journal.slice(0, 5).flatMap((j: any) => j.sel.exos.filter((x: any) => x.role === "travail"));
    return t.filter((x: any) => x.item.comp.startsWith("NC.REL.")).length / t.length >= 0.6;
  }), 0.9);
  taux("J30 : REL.01 et REL.02 acquis", rel.map((r) => M.mxStatut(r.mtFin["NC.REL.01"]) === "acquis" && M.mxStatut(r.mtFin["NC.REL.02"]) === "acquis"), 0.9);
  taux("J30 : ≥ 3 compétences dépendantes sorties de la lacune", rel.map((r) => DEP_REL.filter((c) => M.mxStatut(r.mtFin[c]) !== "lacune").length >= 3), 0.8);
  taux("J30 : révisions espacées présentes", rel.map((r) => r.journal.some((j: any) => j.sel.exos.some((x: any) => x.role === "revision"))), 1);
  taux("gratuit J30 : point faible acquis", rel.map((r) => M.mxStatut(r.gratuit.mt[r.gratuit.pf]) === "acquis"), 0.85);

  console.log("  2. bon élève avec 1 trou (FRAC.03)");
  taux("complet : priorité n°1 = FRAC.03", bon.map((r) => r.comp.carte.priorites[0] === "NC.FRAC.03"), 0.85);
  taux("complet : FRAC.03 en lacune et bloque PROB.02", bon.map((r) => parId(r.comp.carte)["NC.FRAC.03"]?.statut === "lacune" && parId(r.comp.carte)["NC.FRAC.03"].bloque.includes("DF.PROB.02")), 0.85);
  taux("complet : ≤ 2 lacunes", bon.map((r) => r.comp.carte.competences.filter((c: any) => c.statut === "lacune").length <= 2), 0.9);
  taux("complet : score ≥ 70", bon.map((r) => r.comp.carte.score_global >= 70), 0.9);
  taux("J1-5 : ≥ 60 % du travail sur FRAC.03", bon.map((r) => {
    const t = r.journal.slice(0, 5).flatMap((j: any) => j.sel.exos.filter((x: any) => x.role === "travail"));
    return t.filter((x: any) => x.item.comp === "NC.FRAC.03").length / Math.max(1, t.length) >= 0.6;
  }), 0.8);
  taux("J30 : FRAC.03 acquis", bon.map((r) => M.mxStatut(r.mtFin["NC.FRAC.03"]) === "acquis"), 0.9);

  console.log("  3. élève qui répond au hasard");
  taux("express : fiabilité « faible » + alerte", has.map((r) => r.exp.carte.fiabilite.niveau === "faible" && !!r.exp.carte.alerte), 1);
  taux("complet : fiabilité « faible » + alerte", has.map((r) => r.comp.carte.fiabilite.niveau === "faible" && !!r.comp.carte.alerte), 1);
  taux("complet : score < 40", has.map((r) => r.comp.carte.score_global < 40), 0.95);
  taux("complet : ≤ 2 « acquis » par chance", has.map((r) => r.comp.carte.competences.filter((c: any) => c.statut === "acquis").length <= 2), 0.9);

  console.log("  4. élève moyen (bases OK, programme 4e/3e fragile)");
  taux("complet : priorité n°1 sur le programme 4e/3e", moy.map((r) => ["3EME", "4EME"].includes(MINI.ref.comps[r.comp.carte.priorites[0]]?.niveau_origine)), 0.85);
  taux("complet : carte contrastée", moy.map((r) => r.comp.carte.competences.some((c: any) => c.statut === "acquis") &&
    r.comp.carte.competences.some((c: any) => c.statut !== "acquis" && c.statut !== "non_evalue")), 0.95);
  taux("complet : fiabilité non « faible »", moy.map((r) => r.comp.carte.fiabilite.niveau !== "faible"), 0.95);
  taux("J30 : lacunes en baisse", moy.map((r) => {
    const l0 = Object.keys(r.comp.mt).filter((c) => M.mxStatut(r.comp.mt[c]) === "lacune").length;
    const l1 = Object.keys(r.mtFin).filter((c) => M.mxStatut(r.mtFin[c]) === "lacune").length;
    return l1 < l0 || l0 === 0;
  }), 0.9);
  const moyQ = (l: any[], k: string) => Math.round(l.reduce((s, r) => s + r[k].poses, 0) / l.length);
  console.log(`  questions moyennes express/complet : relatifs ${moyQ(rel, "exp")}/${moyQ(rel, "comp")} · bon ${moyQ(bon, "exp")}/${moyQ(bon, "comp")} · hasard ${moyQ(has, "exp")}/${moyQ(has, "comp")} · moyen ${moyQ(moy, "exp")}/${moyQ(moy, "comp")}`);
});

Deno.test("référentiel réel (121 compétences) : 4 profils × 10 graines", () => {
  const C = REEL.comps, ref = REEL.ref;
  const baisse = (racine: string, pRacine: number, pDep: number) => {
    const sp: Record<string, number> = { [racine]: pRacine };
    for (const d of ref.desc2[racine]) sp[d] = pDep;
    return sp;
  };
  const rel = campagne(REEL, (s) => eleve(C, "Rel", () => 0.92, baisse("NC.REL.02", 0.1, 0.15), 5500 + s), 10, { gratuit: true });
  const bon = campagne(REEL, (s) => eleve(C, "Bon", () => 0.95, baisse("NC.FRAC.02", 0.05, 0.2), 6600 + s), 10);
  const has = campagne(REEL, (s) => eleve(C, "Has", () => 0, {}, 7700 + s, true), 10);
  const moy = campagne(REEL, (s) => eleve(C, "Moy", (c) =>
    c.niveau_origine === "6EME" || c.niveau_origine === "5EME" ? 0.9 : c.niveau_origine === "4EME" ? 0.6 : 0.4, {}, 8800 + s), 10);

  const n3e = ref.ordre.filter((id: string) => ref.comps[id].niveau_origine === "3EME").length;
  const cov = (l: any[]) => Math.round(l.reduce((s, r) => s + r.comp.carte.competences.filter((c: any) => c.statut !== "non_evalue").length, 0) / l.length);
  const q = (l: any[], k: string) => Math.round(l.reduce((s, r) => s + r[k].poses, 0) / l.length);
  console.log(`  couverture complet (compétences conclues / 121, dont ${n3e} de 3e) : relatifs ${cov(rel)} · bon ${cov(bon)} · hasard ${cov(has)} · moyen ${cov(moy)}`);
  console.log(`  questions express/complet : relatifs ${q(rel, "exp")}/${q(rel, "comp")} · bon ${q(bon, "exp")}/${q(bon, "comp")} · hasard ${q(has, "exp")}/${q(has, "comp")} · moyen ${q(moy, "exp")}/${q(moy, "comp")}`);
  const ex = rel[0].comp.carte;
  console.log(`  exemple relatifs : priorités ${ex.priorites.slice(0, 4).join(", ")} · causes racines ${ex.competences.filter((c: any) => c.cause_racine).map((c: any) => c.id).join(", ")}`);
  console.log(`  phrase_cle : ${ex.phrase_cle}`);

  taux("express : 5 domaines colorés", [...rel, ...bon, ...moy].map((r) => r.exp.carte.domaines.filter((d: any) => d.statut !== "non_evalue").length === 5), 1);
  taux("relatifs : NC.REL.02 dans les 3 premières priorités", rel.map((r) => r.comp.carte.priorites.slice(0, 3).includes("NC.REL.02")), 0.8);
  taux("relatifs : NC.REL.02 cause racine", rel.map((r) => !!parId(r.comp.carte)["NC.REL.02"]?.cause_racine), 0.8);
  taux("relatifs J30 : NC.REL.02 acquis", rel.map((r) => M.mxStatut(r.mtFin["NC.REL.02"]) === "acquis"), 0.8);
  taux("bon : NC.FRAC.02 identifiée (lacune)", bon.map((r) => parId(r.comp.carte)["NC.FRAC.02"]?.statut === "lacune"), 0.8);
  taux("bon : score ≥ 70", bon.map((r) => r.comp.carte.score_global >= 70), 0.8);
  taux("hasard : fiabilité « faible »", has.map((r) => r.comp.carte.fiabilite.niveau === "faible"), 1);
  taux("moyen : priorité n°1 en 4e/3e", moy.map((r) => ["3EME", "4EME"].includes(ref.comps[r.comp.carte.priorites[0]]?.niveau_origine)), 0.8);
});

Deno.test("re-diagnostic mensuel : évolution de la carte", () => {
  const C = MINI.comps;
  const fab = (s: number) => eleve(C, "Rel", () => 0.92, { "NC.REL.01": 0.1, "NC.REL.02": 0.1, "NC.LIT.01": 0.15, "NC.LIT.03": 0.1,
    "NC.EQUA.02": 0.15, "NC.EQUA.04": 0.1, "DF.FONC.02": 0.15, "AP.SCR.02": 0.2 }, s);
  const oks: boolean[] = [];
  for (let s = 1; s <= 10; s++) {
    const base = simulerDiag(MINI, fab(9900 + s), "complet", {});
    const mt = clone(base.mt);
    const e = fab(9950 + s);
    simulerEntrainement(MINI, e, mt, null);
    const r = simulerDiag(MINI, e, "mensuel", mt);
    assert(r.poses <= 20, "mensuel ≤ 20 q");
    invariantsCarte(MINI, "mensuel", r.carte);
    const evo = M.mxComparerCartes(base.carte, r.carte);
    oks.push(!!evo && evo.score_apres > evo.score_avant && evo.changements.some((c: any) => c.id.startsWith("NC.REL.") && c.apres !== "lacune"));
  }
  taux("mensuel : score en hausse et relatifs sortis de la lacune", oks, 0.9);
  assert(M.mxRediagDu("2026-10-01", "2026-10-31", "programme_brevet") && !M.mxRediagDu("2026-10-01", "2026-10-31", "free"), "rediag dû à J+30 (programme)");
});

Deno.test("déterminisme : mêmes entrées, même carte, même séance", () => {
  const f = () => eleve(MINI.comps, "Moy", () => 0.6, {}, 42);
  const a = simulerDiag(MINI, f(), "express", {}), b = simulerDiag(MINI, f(), "express", {});
  assert(JSON.stringify(a.carte) === JSON.stringify(b.carte), "carte non déterministe");
  const s1 = M.mxChoisirEntrainement(MINI.ref, a.mt, { code: "X", date: "2026-10-02", zone: null, historique: [] });
  const s2 = M.mxChoisirEntrainement(MINI.ref, a.mt, { code: "X", date: "2026-10-02", zone: null, historique: [] });
  assert(JSON.stringify(s1) === JSON.stringify(s2), "séance non déterministe");
});

// Cartes exemples (référentiel réel) écrites pour le test PDF (carte_pdf_test.ts) et pour les autres agents.
Deno.test("export des cartes exemples (fixtures)", () => {
  const C = REEL.comps, ref = REEL.ref;
  const sp: Record<string, number> = { "NC.REL.02": 0.1 };
  for (const d of ref.desc2["NC.REL.02"]) sp[d] = 0.15;
  const exp = simulerDiag(REEL, eleve(C, "Léa", () => 0.9, sp, 77), "express", {});
  const mt: Record<string, any> = {};
  for (const o of exp.etat.obs) mt[o.comp] = M.mxMajMaitrise(mt[o.comp], o.comp, o.ok, o.w, o.err, DATE0);
  const r = simulerDiag(REEL, eleve(C, "Léa", () => 0.9, sp, 78), "complet", mt, exp.etat.obs);
  Deno.writeTextFileSync(new URL("fixtures/carte_exemple_complet.json", ICI), JSON.stringify(r.carte, null, 1) + "\n");
  Deno.writeTextFileSync(new URL("fixtures/carte_exemple_express.json", ICI), JSON.stringify(exp.carte, null, 1) + "\n");
});
