#!/usr/bin/env python3
"""Mappe la banque existante (22 chapitres v4 + diagnostics) vers le référentiel 3e
et génère couverture_existante.md + mapping_legacy.json.

Usage : python3 data/referentiel_3eme/couverture.py

Mapping manuel (approximation raisonnable) : chaque question existante reçoit une
compétence principale (1re) et éventuellement des compétences secondaires.
Clés : "<Chapitre>|<ID_slot>.<num>" pour les v4, "diag|<index>" pour diagnostic_3eme.json.
Les fichiers diag_*.json sont des copies des questions de diagnostic_3eme.json :
ils sont rattachés par texte de question et ne sont comptés qu'une fois.
"""
import glob
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.dirname(HERE)

MAPPING_TXT = """
Arithmetique_Brevet|ARITH_01: NC.ARITH.01 ; NC.ARITH.01 ; NC.ARITH.01,NC.ARITH.03 ; NC.ARITH.02 ; NC.ARITH.01
Arithmetique_Brevet|ARITH_02: NC.ARITH.03 ; NC.ARITH.03 ; NC.ARITH.01 ; NC.ARITH.04 ; NC.ARITH.04
Arithmetique_Brevet|ARITH_03: NC.ARITH.01 ; NC.ARITH.04 ; NC.ARITH.04 ; NC.FRAC.02 ; NC.FRAC.02,NC.ARITH.04
Arithmetique_Brevet|ARITH_04: NC.ARITH.03 ; NC.ARITH.04 ; NC.ARITH.04 ; NC.ARITH.04 ; NC.ARITH.04,GM.AIRE.02
Auto_Calcul|ACALC_01: DF.PROP.04 ; NC.FRAC.04 ; DF.PROP.02 ; NC.FRAC.03 ; DF.PROP.04
Auto_Calcul|ACALC_02: NC.PUIS.01 ; NC.RAC.01 ; NC.PUIS.02 ; NC.RAC.02 ; NC.PUIS.04
Auto_Calcul|ACALC_03: NC.ARITH.01 ; NC.ARITH.01 ; NC.ARITH.01 ; NC.ARITH.02 ; NC.ARITH.04
Auto_Calcul|ACALC_04: NC.FRAC.04 ; NC.PUIS.02,NC.FRAC.07 ; NC.PUIS.04,NC.ENT.01 ; GM.CONV.01 ; NC.PUIS.01,NC.ARITH.01
Auto_Geometrie|AUTOGEO_01: EG.REP.01 ; EG.REP.01 ; EG.REP.02 ; EG.REP.02 ; EG.REP.02
Auto_Geometrie|AUTOGEO_02: EG.ANG.01 ; EG.ANG.01 ; EG.ANG.03 ; EG.ANG.03 ; EG.ANG.02
Auto_Geometrie|AUTOGEO_03: EG.PYTH.02 ; EG.PYTH.03 ; EG.THAL.02 ; EG.PYTH.01 ; EG.THAL.02
Auto_Geometrie|AUTOGEO_04: GM.CONV.02 ; GM.VOL.01 ; GM.VOL.02 ; GM.VOL.03 ; GM.VOL.04
Auto_Litteral|AUTO_LIT_01: NC.LIT.02,GM.VIT.01 ; NC.LIT.02 ; NC.LIT.02 ; NC.LIT.02 ; NC.LIT.02
Auto_Litteral|AUTO_LIT_02: NC.LIT.04 ; NC.LIT.04 ; NC.LIT.04 ; NC.LIT.08 ; NC.LIT.04
Auto_Litteral|AUTO_LIT_03: NC.LIT.07 ; NC.LIT.07 ; NC.LIT.07 ; NC.LIT.09 ; NC.LIT.07
Auto_Litteral|AUTO_LIT_04: NC.EQUA.02 ; NC.EQUA.02 ; NC.LIT.02 ; NC.LIT.06 ; NC.EQUA.03
Auto_Stats_Probas|AUTSP_01: DF.STAT.01 ; DF.PROB.02 ; DF.PROB.02 ; DF.PROB.02 ; DF.PROB.03
Auto_Stats_Probas|AUTSP_02: DF.STAT.01 ; DF.STAT.02 ; DF.STAT.02,NC.FRAC.07 ; DF.STAT.02 ; DF.PROB.02
Auto_Stats_Probas|AUTSP_03: DF.STAT.01 ; DF.STAT.06 ; DF.STAT.03 ; DF.STAT.01 ; DF.STAT.03
Auto_Stats_Probas|AUTSP_04: DF.STAT.01 ; DF.STAT.03 ; DF.PROB.02 ; DF.STAT.02 ; DF.STAT.02
Calcul_Litteral_Brevet|CALLIT_01: NC.LIT.04 ; NC.LIT.06 ; NC.LIT.04 ; NC.LIT.04,NC.LIT.03 ; NC.LIT.05,NC.LIT.06
Calcul_Litteral_Brevet|CALLIT_02: NC.LIT.08 ; NC.LIT.08 ; NC.LIT.09 ; NC.LIT.09 ; NC.LIT.09
Calcul_Litteral_Brevet|CALLIT_03: NC.LIT.07 ; NC.LIT.07 ; NC.LIT.07 ; NC.LIT.07 ; NC.LIT.09
Calcul_Litteral_Brevet|CALLIT_04: NC.LIT.06 ; NC.LIT.08 ; NC.LIT.02 ; NC.EQUA.05 ; NC.LIT.02
Equations_Brevet|EQ_01: NC.EQUA.04 ; NC.EQUA.02 ; NC.EQUA.01 ; NC.EQUA.04 ; NC.EQUA.04
Equations_Brevet|EQ_02: NC.EQUA.04 ; NC.EQUA.02,NC.FRAC.06 ; NC.LIT.04 ; NC.EQUA.02 ; NC.EQUA.02
Equations_Brevet|EQ_03: NC.LIT.01 ; NC.LIT.09 ; NC.EQUA.05 ; NC.EQUA.05 ; NC.EQUA.05
Equations_Brevet|EQ_04: NC.LIT.01 ; NC.EQUA.04 ; NC.EQUA.01 ; GM.AIRE.02 ; GM.AIRE.01
Fonctions_Affines_Brevet|FONC_AFF_01: DF.AFF.02 ; DF.FONC.01 ; DF.AFF.02 ; DF.FONC.04 ; DF.AFF.05
Fonctions_Affines_Brevet|FONC_AFF_02: DF.FONC.02 ; DF.AFF.03 ; DF.FONC.04 ; DF.FONC.04 ; DF.FONC.01,DF.PROP.03
Fonctions_Affines_Brevet|FONC_AFF_03: DF.FONC.01 ; DF.AFF.03 ; DF.FONC.04 ; DF.AFF.03 ; NC.INEQ.02
Fonctions_Affines_Brevet|FONC_AFF_04: DF.FONC.01 ; DF.AFF.05 ; DF.AFF.05 ; DF.AFF.05 ; DF.AFF.05
Fonctions_Brevet|FONC_01: DF.FONC.01,NC.LIT.01 ; DF.FONC.01 ; DF.AFF.02 ; DF.FONC.04 ; DF.AFF.05
Fonctions_Brevet|FONC_02: DF.FONC.02 ; DF.FONC.02 ; DF.FONC.03 ; DF.FONC.05 ; DF.FONC.05
Fonctions_Brevet|FONC_03: DF.FONC.02 ; DF.FONC.02 ; DF.FONC.05 ; DF.FONC.05 ; DF.FONC.05
Fonctions_Brevet|FONC_04: DF.FONC.01,NC.LIT.01 ; DF.FONC.04 ; DF.FONC.01 ; NC.INEQ.02 ; DF.FONC.04
Fractions_Brevet|FRAC_01: NC.FRAC.03 ; NC.FRAC.03 ; NC.FRAC.03 ; NC.FRAC.03 ; NC.FRAC.03
Fractions_Brevet|FRAC_02: NC.FRAC.05 ; NC.FRAC.04 ; NC.FRAC.05 ; NC.FRAC.06 ; NC.FRAC.06
Fractions_Brevet|FRAC_03: NC.FRAC.04 ; NC.FRAC.04 ; NC.FRAC.07,DF.PROP.04 ; DF.PROP.06 ; NC.FRAC.04
Fractions_Brevet|FRAC_04: NC.FRAC.05,DF.PROP.02 ; NC.FRAC.03,DF.PROP.02 ; DF.PROP.02 ; NC.FRAC.05 ; NC.FRAC.06
Geometrie_Espace_Brevet|GEOESP_01: GM.VOL.04 ; GM.VOL.03 ; GM.VOL.02 ; GM.VOL.05 ; GM.VOL.02
Geometrie_Espace_Brevet|GEOESP_02: GM.AIRE.01 ; EG.ESP.01 ; EG.ESP.02 ; GM.AIRE.02 ; GM.AIRE.02,GM.AIRE.03
Geometrie_Espace_Brevet|GEOESP_03: DF.PROP.07 ; DF.PROP.07 ; GM.AGR.02 ; GM.VOL.02 ; GM.AGR.02
Geometrie_Espace_Brevet|GEOESP_04: GM.VOL.02 ; GM.VOL.03 ; EG.PYTH.01 ; GM.VOL.05 ; GM.CONV.02
Inequations_Brevet|INEQ_01: NC.INEQ.02 ; NC.INEQ.01 ; NC.INEQ.02,NC.EQUA.01 ; NC.INEQ.02 ; NC.INEQ.02
Inequations_Brevet|INEQ_02: NC.LIT.01 ; NC.INEQ.02 ; NC.INEQ.01,NC.EQUA.01 ; NC.INEQ.01 ; NC.INEQ.02
Inequations_Brevet|INEQ_03: NC.INEQ.02 ; NC.INEQ.01 ; NC.FRAC.04 ; NC.INEQ.02 ; NC.INEQ.02
Inequations_Brevet|INEQ_04: NC.PRIO.01 ; NC.INEQ.01 ; NC.INEQ.02 ; NC.INEQ.01 ; NC.INEQ.02
Probabilites_Brevet|PROB_01: DF.STAT.01 ; DF.PROB.02 ; DF.PROB.02 ; DF.PROB.02 ; DF.PROB.02
Probabilites_Brevet|PROB_02: DF.PROB.02 ; DF.PROB.04 ; DF.PROB.03 ; DF.PROB.04 ; DF.PROB.06
Probabilites_Brevet|PROB_03: DF.PROB.05 ; DF.PROB.05 ; DF.PROB.02 ; DF.PROB.03 ; DF.PROB.05
Probabilites_Brevet|PROB_04: DF.PROB.04 ; DF.STAT.02 ; DF.PROB.02 ; DF.PROB.06 ; DF.PROB.06
Proportionnalite_Brevet|PROP_01: DF.PROP.02 ; DF.PROP.01 ; DF.PROP.02 ; DF.PROP.02 ; DF.PROP.02
Proportionnalite_Brevet|PROP_02: DF.PROP.03 ; DF.PROP.04 ; DF.PROP.05 ; DF.PROP.06 ; DF.PROP.06
Proportionnalite_Brevet|PROP_03: DF.PROP.07 ; GM.VIT.01 ; GM.VIT.01 ; GM.VIT.01 ; GM.VIT.01,GM.CONV.03
Proportionnalite_Brevet|PROP_04: DF.FONC.01 ; DF.AFF.05 ; DF.AFF.05 ; DF.PROP.04 ; DF.PROP.05
Puissances_Brevet|PUIS_01: NC.PUIS.04 ; NC.PUIS.02 ; NC.PUIS.04 ; NC.PUIS.05 ; NC.PUIS.05
Puissances_Brevet|PUIS_02: NC.PUIS.03 ; NC.PUIS.03 ; NC.PUIS.03 ; NC.PUIS.03 ; NC.PUIS.03
Puissances_Brevet|PUIS_03: NC.PUIS.02 ; NC.PUIS.04 ; NC.PUIS.03 ; NC.PUIS.05 ; NC.PUIS.05
Puissances_Brevet|PUIS_04: NC.PUIS.04,NC.ENT.01 ; NC.PUIS.05 ; NC.PUIS.05 ; NC.PUIS.05 ; NC.PUIS.05
Pythagore_Brevet|PYT_01: EG.PYTH.01 ; EG.PYTH.01 ; EG.PYTH.01 ; EG.PYTH.01 ; EG.PYTH.01,GM.AIRE.01
Pythagore_Brevet|PYT_02: EG.PYTH.02 ; EG.PYTH.02 ; EG.PYTH.02 ; EG.PYTH.02 ; EG.PYTH.02
Pythagore_Brevet|PYT_03: EG.PYTH.01 ; EG.PYTH.03,GM.AIRE.02 ; EG.PYTH.03 ; NC.PUIS.01 ; EG.PYTH.03
Pythagore_Brevet|PYT_04: EG.PYTH.01 ; EG.PYTH.02 ; EG.PYTH.03 ; GM.AIRE.02 ; EG.PYTH.01
Racines_Carrees_Brevet|RAC_01: NC.RAC.03 ; NC.RAC.03 ; NC.RAC.03 ; NC.RAC.03,NC.RAC.01 ; NC.RAC.02
Racines_Carrees_Brevet|RAC_02: NC.RAC.02 ; NC.RAC.02 ; NC.RAC.02 ; NC.RAC.04 ; NC.RAC.02
Racines_Carrees_Brevet|RAC_03: NC.RAC.04 ; NC.RAC.04 ; NC.RAC.04 ; NC.RAC.04 ; NC.RAC.02
Racines_Carrees_Brevet|RAC_04: NC.RAC.04 ; NC.RAC.04,NC.LIT.07 ; NC.RAC.04,NC.LIT.07 ; NC.RAC.04 ; NC.RAC.04,NC.LIT.07
Scratch_Brevet|SCRATCH_01: AP.PROG.01 ; AP.PROG.01 ; AP.PROG.01 ; AP.PROG.01 ; NC.EQUA.02
Scratch_Brevet|SCRATCH_02: AP.PROG.01 ; NC.LIT.01 ; NC.EQUA.01 ; NC.LIT.10 ; AP.PROG.01
Scratch_Brevet|SCRATCH_03: AP.PROG.02 ; AP.PROG.02 ; AP.PROG.02 ; AP.PROG.04,AP.PROG.03 ; AP.PROG.03
Scratch_Brevet|SCRATCH_04: AP.PROG.01 ; AP.PROG.01 ; NC.LIT.10 ; NC.LIT.10 ; NC.LIT.10
Statistiques_Brevet|STAT_01: DF.STAT.04 ; DF.STAT.04 ; DF.STAT.04 ; DF.STAT.04 ; DF.STAT.04
Statistiques_Brevet|STAT_02: DF.STAT.01 ; DF.STAT.06 ; DF.STAT.05 ; DF.STAT.04 ; DF.STAT.05
Statistiques_Brevet|STAT_03: DF.STAT.01 ; DF.STAT.05 ; DF.STAT.07 ; DF.STAT.07 ; DF.STAT.07
Statistiques_Brevet|STAT_04: DF.STAT.03 ; DF.STAT.03 ; DF.STAT.05 ; DF.STAT.07 ; DF.STAT.07
Thales_Brevet|THAL_01: NC.FRAC.02 ; EG.THAL.01 ; EG.THAL.02 ; EG.THAL.02 ; EG.THAL.02
Thales_Brevet|THAL_02: EG.THAL.02 ; EG.THAL.02 ; EG.SEMB.01 ; DF.PROP.07 ; GM.AGR.01
Thales_Brevet|THAL_03: EG.THAL.01 ; EG.THAL.03 ; EG.THAL.03 ; EG.THAL.03 ; EG.THAL.02
Thales_Brevet|THAL_04: EG.THAL.01 ; EG.THAL.02 ; DF.PROP.07 ; EG.THAL.02 ; GM.AGR.01
Transformations_Brevet|TRANSF_01: EG.TRANS.02 ; EG.TRANS.02 ; EG.TRANS.05 ; EG.TRANS.02 ; EG.TRANS.05
Transformations_Brevet|TRANSF_02: EG.TRANS.03 ; EG.TRANS.03 ; EG.TRANS.03 ; EG.TRANS.03 ; EG.TRANS.03,EG.REP.01
Transformations_Brevet|TRANSF_03: EG.TRANS.04 ; EG.TRANS.04 ; EG.TRANS.04 ; GM.AGR.01 ; EG.TRANS.04
Transformations_Brevet|TRANSF_04: EG.TRANS.02 ; EG.TRANS.03,EG.TRANS.01 ; EG.TRANS.05 ; EG.TRANS.04 ; EG.TRANS.05
Trigonometrie_Brevet|TRIGO_01: EG.TRIG.03 ; EG.TRIG.03 ; EG.TRIG.02 ; EG.TRIG.04 ; EG.TRIG.04
Trigonometrie_Brevet|TRIGO_02: EG.TRIG.04 ; EG.TRIG.04 ; EG.TRIG.03 ; EG.TRIG.03 ; EG.TRIG.01
Trigonometrie_Brevet|TRIGO_03: EG.TRIG.03 ; EG.TRIG.03 ; EG.TRIG.04 ; EG.TRIG.04 ; EG.TRIG.03
Trigonometrie_Brevet|TRIGO_04: EG.TRIG.03 ; EG.TRIG.03 ; EG.TRIG.04 ; EG.PYTH.01 ; EG.TRIG.02
diag|0-17: NC.ARITH.04 ; NC.ARITH.02 ; NC.ARITH.04 ; NC.FRAC.03 ; NC.FRAC.04 ; NC.FRAC.05 ; NC.PUIS.03 ; NC.PUIS.04 ; NC.PUIS.05 ; NC.RAC.03 ; NC.RAC.02 ; NC.RAC.02 ; DF.PROP.04 ; DF.PROP.02 ; DF.PROP.05 ; NC.LIT.04 ; NC.LIT.08 ; NC.LIT.07
diag|18-35: NC.EQUA.02 ; NC.EQUA.02,NC.EQUA.04 ; NC.EQUA.05 ; NC.INEQ.01 ; NC.INEQ.01 ; NC.INEQ.02 ; EG.PYTH.01 ; EG.PYTH.02 ; EG.PYTH.03 ; EG.THAL.02 ; EG.THAL.02 ; EG.THAL.03 ; EG.TRIG.02 ; EG.TRIG.03 ; EG.TRIG.04 ; EG.TRANS.02 ; EG.TRANS.05 ; EG.TRANS.04
diag|36-53: GM.VOL.02 ; EG.ESP.01 ; GM.AGR.02 ; DF.FONC.01 ; DF.FONC.02 ; DF.FONC.04 ; DF.FONC.01 ; DF.AFF.03 ; DF.AFF.05 ; DF.STAT.03 ; DF.STAT.05 ; DF.STAT.07 ; DF.PROB.02 ; DF.PROB.03 ; DF.PROB.05 ; AP.PROG.01 ; NC.LIT.01 ; AP.PROG.04
"""

# Cible de dimensionnement par compétence (items atomiques à terme, diag + train).
# Diagnostic : ≥ 6 items calibrés par compétence 3e (n_obs ≥ 2 sur plusieurs passages
# sans répétition), 4 pour un prérequis. Entraînement : selon le poids Brevet.
CIBLE_DIAG = {"3EME": 6, "autre": 4}
CIBLE_TRAIN = {3: 30, 2: 20, 1: 10}


def parse_mapping():
    m = {}
    for line in MAPPING_TXT.strip().splitlines():
        head, body = line.split(":", 1)
        comps = [[x.strip() for x in cell.split(",")] for cell in body.split(";")]
        chap, slot = head.split("|")
        if chap == "diag":
            a, b = (int(x) for x in slot.split("-"))
            assert len(comps) == b - a + 1, line
            for i, c in zip(range(a, b + 1), comps):
                m[f"diag|{i}"] = c
        else:
            assert len(comps) == 5, line
            for n, c in enumerate(comps, 1):
                m[f"{chap}|{slot}.{n}"] = c
    return m


def load_items():
    """Retourne [(clé, source, question dict)] pour les 22 chapitres v4 + diagnostic_3eme."""
    items = []
    for f in sorted(glob.glob(os.path.join(DATA, "*_v4.json"))):
        chap = os.path.basename(f)[:-8]
        for slot in json.load(open(f, encoding="utf-8")):
            for q in slot["questions"]:
                items.append((f"{chap}|{slot['id']}.{q.get('num')}", chap, q))
    for i, q in enumerate(json.load(open(os.path.join(DATA, "diagnostic_3eme.json"), encoding="utf-8"))):
        items.append((f"diag|{i}", "diagnostic_3eme", q))
    return items


def diag_copies(diag_texts):
    """Vérifie que les diag_*.json ne contiennent que des copies de diagnostic_3eme."""
    total, nouveaux = 0, []
    for f in sorted(glob.glob(os.path.join(DATA, "diag_*.json"))):
        for x in json.load(open(f, encoding="utf-8")):
            for q in (x["exos"] if "exos" in x else [x]):
                total += 1
                if q["q"] not in diag_texts:
                    nouveaux.append((os.path.basename(f), q["q"][:80]))
    return total, nouveaux


def main():
    ref = json.load(open(os.path.join(HERE, "competences.json"), encoding="utf-8"))
    by_id = {c["id"]: c for c in ref}
    mapping = parse_mapping()
    items = load_items()
    keys = {k for k, _, _ in items}
    missing = keys - set(mapping)
    extra = set(mapping) - keys
    bad = {c for cs in mapping.values() for c in cs if c not in by_id}
    assert not missing and not extra and not bad, (missing, extra, bad)

    diag_texts = {q["q"] for k, _, q in items if k.startswith("diag|")}
    n_copies, nouveaux = diag_copies(diag_texts)
    assert not nouveaux, nouveaux

    prim = defaultdict(int)
    sec = defaultdict(int)
    diag_n = defaultdict(int)
    types = defaultdict(lambda: defaultdict(int))
    for k, src, q in items:
        cs = mapping[k]
        prim[cs[0]] += 1
        types[cs[0]][q.get("type") or "qcm"] += 1
        if k.startswith("diag|"):
            diag_n[cs[0]] += 1
        for c in cs[1:]:
            sec[c] += 1

    # Export du mapping (utile pour tagger les sous-questions v4 avec "comp")
    with open(os.path.join(HERE, "mapping_legacy.json"), "w", encoding="utf-8") as f:
        json.dump({k: {"comp": v[0], "comp_secondaires": v[1:]} for k, v in sorted(mapping.items())},
                  f, ensure_ascii=False, indent=1)
        f.write("\n")

    # ---------- Rapport Markdown
    L = []
    w = L.append
    n_v4 = sum(1 for k in keys if not k.startswith("diag|"))
    n_d = len(keys) - n_v4
    w("# Couverture de la banque existante par le référentiel 3e")
    w("")
    w("> Généré par `data/referentiel_3eme/couverture.py` — ne pas éditer à la main.")
    w("> Mapping manuel question → compétence (approximation raisonnable), exporté dans `mapping_legacy.json`.")
    w("")
    w("## Périmètre analysé")
    w("")
    w(f"- **{n_v4} questions** des 22 chapitres v4 (`data/*_Brevet_v4.json`, `data/Auto_*_v4.json`, 4 parapluies × 5 sous-questions)")
    w(f"- **{n_d} questions** de `data/diagnostic_3eme.json`")
    w(f"- `data/diag_*.json` : {n_copies} questions, **toutes des copies** de `diagnostic_3eme.json` → comptées une seule fois")
    w("- Non inclus : `data/bank_6eme|5eme|4eme/` (320 items, format par niveau, pas encore en base) — "
      "réutilisables pour les prérequis 6e/5e/4e après mapping")
    w(f"- Total unique : **{len(keys)} questions** → {len(ref)} compétences")
    w("")
    w("**Constat structurel** : aucune question existante n'a de champ `err` (mauvaise réponse → erreur type). "
      "La banque actuelle permet donc de mesurer la réussite, **pas de diagnostiquer les erreurs types**. "
      "Les distracteurs QCM existants sont souvent réalistes : ils peuvent être rattachés aux erreurs du référentiel "
      "lors de la migration (travail de tagging, pas de génération).")
    w("")
    w("Colonnes : **P** = questions dont c'est la compétence principale · **S** = mentions secondaires · "
      "**dont diag** = issues du diagnostic actuel · **Cible** = items atomiques visés (diag + entraînement) · "
      "**Manque** = Cible − P.")
    w("")

    tot_cible = tot_manque = 0
    trous = []
    faibles = []
    dom_stats = defaultdict(lambda: [0, 0, 0, 0])
    DOMS = [("NC", "Nombres et calculs"), ("DF", "Données, fonctions, proportionnalité"),
            ("GM", "Grandeurs et mesures"), ("EG", "Espace et géométrie"), ("AP", "Algorithmique et programmation")]
    for code, lib in DOMS:
        w(f"## {code} — {lib}")
        w("")
        w("| Compétence | Niv. | Poids | P | S | dont diag | Types (P) | Cible | Manque |")
        w("|---|---|---|---|---|---|---|---|---|")
        for c in ref:
            if c["domaine"] != code:
                continue
            cid = c["id"]
            p, s = prim[cid], sec[cid]
            cible = CIBLE_DIAG["3EME" if c["niveau_origine"] == "3EME" else "autre"] + CIBLE_TRAIN[c["poids_brevet"]]
            manque = max(0, cible - p)
            tot_cible += cible
            tot_manque += manque
            ds = dom_stats[code]
            ds[0] += 1
            ds[1] += p
            ds[2] += 1 if p == 0 else 0
            ds[3] += manque
            ty = " ".join(f"{t}:{n}" for t, n in sorted(types[cid].items())) or "—"
            flag = " 🔴" if p == 0 else (" 🟠" if p < 3 else "")
            w(f"| `{cid}` {c['titre']}{flag} | {c['niveau_origine'][0]}e | {c['poids_brevet']} | {p} | {s} | "
              f"{diag_n[cid]} | {ty} | {cible} | {manque} |")
            if p == 0:
                trous.append(c)
            elif p < 3:
                faibles.append((c, p))
        w("")

    w("## Synthèse par domaine")
    w("")
    w("| Domaine | Compétences | Questions (P) | Compétences sans aucune question | Items manquants (cible) |")
    w("|---|---|---|---|---|")
    for code, lib in DOMS:
        n, p, z, m = dom_stats[code]
        w(f"| {code} | {n} | {p} | {z} | {m} |")
    w(f"| **Total** | {len(ref)} | {len(keys)} | {len(trous)} | **{tot_manque}** / {tot_cible} |")
    w("")

    w("## 🔴 Trous : compétences sans aucune question (principale)")
    w("")
    for c in sorted(trous, key=lambda c: (-c["poids_brevet"], c["id"])):
        s = sec[c["id"]]
        w(f"- `{c['id']}` ({c['niveau_origine']}, poids {c['poids_brevet']}) — {c['titre']}"
          + (f" · {s} mention(s) secondaire(s)" if s else ""))
    w("")
    w("## 🟠 Couverture faible (1-2 questions)")
    w("")
    for c, p in sorted(faibles, key=lambda t: (-t[0]["poids_brevet"], t[0]["id"])):
        w(f"- `{c['id']}` ({c['niveau_origine']}, poids {c['poids_brevet']}) — {c['titre']} : {p}")
    w("")

    # Prérequis : couverture globale
    socle = [c for c in ref if c["niveau_origine"] in ("6EME", "5EME")]
    socle_p = sum(prim[c["id"]] for c in socle)
    socle_zero = sum(1 for c in socle if prim[c["id"]] == 0)
    n3 = sum(1 for c in ref if c["niveau_origine"] == "3EME")
    diag_cible = n3 * CIBLE_DIAG["3EME"] + (len(ref) - n3) * CIBLE_DIAG["autre"]
    w("## Lecture pour le dimensionnement")
    w("")
    w(f"- Les **{len(socle)} compétences de socle 6e/5e** (celles qui portent la plupart des causes racines) "
      f"ne totalisent que **{socle_p} questions** principales, et **{socle_zero} n'en ont aucune** : la banque actuelle "
      "est construite par chapitre Brevet, elle mesure le symptôme mais ne permet pas de remonter à la cause. "
      "C'est le premier chantier de génération (items courts, `usage: [\"diag\"]`).")
    w(f"- **Diagnostic** : ≈ **{diag_cible} items atomiques calibrés** à produire ({n3} compétences 3e × "
      f"{CIBLE_DIAG['3EME']} + {len(ref) - n3} prérequis × {CIBLE_DIAG['autre']}). Seules les {n_d} questions de "
      "`diagnostic_3eme.json` sont réutilisables telles quelles, après ajout de `comp` et `err`.")
    w("- Les questions v4 sont des sous-questions de problèmes contextualisés : elles restent précieuses "
      "comme **problèmes Brevet** (usage `train`), mais sont trop dépendantes du contexte pour le diagnostic "
      "(une erreur à la question 4 peut venir de la question 2).")
    w(f"- Volume cible total ≈ **{tot_cible} items**, dont **≈ {tot_manque} à produire** "
      "(hypothèse : 6 items diag par compétence 3e, 4 par prérequis ; 30/20/10 items d'entraînement selon le poids).")
    w("- Priorité de génération suggérée : (1) items diag des prérequis à poids 3 (relatifs, priorités, fractions, "
      "carrés/racines, proportionnalité, conversions) ; (2) items diag des compétences 3e à poids 3 ; "
      "(3) tagging `err` des distracteurs existants ; (4) entraînement.")
    w("")
    with open(os.path.join(HERE, "couverture_existante.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"{len(keys)} questions mappées · {len(trous)} compétences sans question · "
          f"{tot_manque}/{tot_cible} items manquants")


if __name__ == "__main__":
    main()
