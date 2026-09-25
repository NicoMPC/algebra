// ════════════════════════════════════════════════════════════
//  Tests unitaires des fonctions pures ajoutées pour les « Besoins API » (41-integration-log.md) :
//  mxErrLibelles (n°2), mxMaitriseDepuisObs (n°1, rejeu invité), mxPourquoi / mxFocusTitres (n°4).
//  Même extraction du bloc MOTEUR_PUR que moteur_test.ts. Les parcours HTTP bout en bout
//  (invité, jetons, attaques) sont dans dev/smoke_test.ts (./matheux.sh test).
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

// Mini-référentiel : REL.01 (5e) → FRAC.03 (5e) → EQUA.02 (3e)
const comps = [
  { id: "NC.REL.01", domaine: "NC", titre: "Additionner des relatifs", titre_eleve: "Ajouter des nombres négatifs", niveau_origine: "5EME", prerequis: [], poids_brevet: 3,
    erreurs: [{ id: "NC.REL.01#signe", libelle: "Oublie le signe moins" }] },
  { id: "NC.FRAC.03", domaine: "NC", titre: "Additionner des fractions", titre_eleve: "Additionner des fractions", niveau_origine: "5EME", prerequis: ["NC.REL.01"], poids_brevet: 2,
    erreurs: [{ id: "NC.FRAC.03#somme_directe", libelle: "Additionne numérateurs et dénominateurs (1/3+1/4=2/7)" }] },
  { id: "NC.EQUA.02", domaine: "NC", titre: "Résoudre ax+b=c", titre_eleve: "Résoudre une équation", niveau_origine: "3EME", prerequis: ["NC.FRAC.03"], poids_brevet: 3, erreurs: [] },
];
const items = comps.flatMap((c) => [0, 1, 2, 3].map((k) => ({ id: `${c.id}-${k}`, comp: c.id, q: "?", a: "1", type: "fill", lvl: 1, usage: ["diag", "train"] })));
const ref = M.mxIndexer(comps, items);
const D = "2026-10-01";

Deno.test("err_libelles : libellé depuis la compétence de l'erreur (y compris prérequis direct)", () => {
  const it = { err: { "2/7": "NC.FRAC.03#somme_directe", "-3": "NC.REL.01#signe", "9": "NC.X#inconnue" } };
  const lib = M.mxErrLibelles(ref, it);
  assert(lib["NC.FRAC.03#somme_directe"]?.startsWith("Additionne"), "libellé de l'erreur de la compétence");
  assert(lib["NC.REL.01#signe"] === "Oublie le signe moins", "libellé d'une erreur de prérequis");
  assert(!("NC.X#inconnue" in lib), "id inconnu ignoré");
  assert(Object.keys(M.mxErrLibelles(ref, {})).length === 0, "item sans err → {}");
});

Deno.test("rejeu invité : maîtrise reconstruite = application réponse par réponse", () => {
  const obs = [
    { item_id: "NC.FRAC.03-0", comp: "NC.FRAC.03", ok: false, w: 1, err: null, date: D },
    { item_id: "NC.FRAC.03-0", comp: "NC.REL.01", ok: false, w: 1, err: "NC.REL.01#signe", date: D, imputee: true },
    { item_id: "NC.FRAC.03-1", comp: "NC.FRAC.03", ok: true, w: 0.67, err: null, date: D },
    { item_id: "NC.EQUA.02-0", comp: "NC.EQUA.02", ok: true, w: 1, err: null, date: D, graine: true }, // graine : ignorée
  ];
  const mt = M.mxMaitriseDepuisObs(obs, D);
  let m: any = null;
  m = M.mxMajMaitrise(m, "NC.FRAC.03", false, 1, null, D);
  m = M.mxMajMaitrise(m, "NC.FRAC.03", true, 0.67, null, D);
  assert(JSON.stringify(mt["NC.FRAC.03"]) === JSON.stringify(m), "même maîtrise que 2 mises à jour successives");
  assert(mt["NC.REL.01"].erreurs_vues["NC.REL.01#signe"] === 1 && mt["NC.REL.01"].n_obs === 1, "observation imputée au prérequis rejouée");
  assert(!mt["NC.EQUA.02"], "les graines ne sont pas rejouées");
});

Deno.test("pourquoi : cause racine > erreur vue > statut, + révision ; jamais « prof »", () => {
  let mt: Record<string, any> = {};
  const obs = (comp: string, ok: boolean, n: number, err: string | null = null) => {
    for (let i = 0; i < n; i++) mt[comp] = M.mxMajMaitrise(mt[comp], comp, ok, 1, err, D);
  };
  obs("NC.REL.01", false, 3); obs("NC.FRAC.03", false, 3); obs("NC.EQUA.02", true, 3);
  const p1 = M.mxPourquoi(ref, mt, ["NC.REL.01", "NC.FRAC.03"], [{ comp: "NC.EQUA.02", role: "revision" }]);
  assert(/On attaque « Ajouter des nombres négatifs »/.test(p1) && /notion de 5e/.test(p1) && /1 autre point/.test(p1), "cause racine : " + p1);
  assert(/Puis « Additionner des fractions »/.test(p1) && /révision de « Résoudre une équation »/.test(p1), "2e focus + révision : " + p1);
  mt = {};
  obs("NC.FRAC.03", false, 2, "NC.FRAC.03#somme_directe"); obs("NC.FRAC.03", true, 1);
  const p2 = M.mxPourquoi(ref, mt, ["NC.FRAC.03"], []);
  assert(/erreur classique « Additionne numérateurs/.test(p2), "erreur vue : " + p2);
  const p3 = M.mxPourquoi(ref, {}, ["NC.EQUA.02"], []);
  assert(/découvre/.test(p3), "non évalué : " + p3);
  const p4 = M.mxPourquoi(ref, {}, [], [], true);
  assert(/zone de travail est acquise/.test(p4), "zone maîtrisée : " + p4);
  for (const p of [p1, p2, p3, p4]) assert(!/prof|Nicolas/i.test(p), "aucune mention d'un humain : " + p);
  assert(M.mxPourquoi(ref, mt, ["NC.FRAC.03"], []) === p2, "déterministe");
  const ft = M.mxFocusTitres(ref, ["NC.FRAC.03", "INCONNU"]);
  assert(ft.length === 1 && ft[0].titre_eleve === "Additionner des fractions" && ft[0].niveau_origine === "5EME", "focus_titres");
});
