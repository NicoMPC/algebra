# Complément 2 banque d'entraînement — NC + DF

Cible : `cibles_complement2.json` (comp `NC.*` et `DF.*`), 102 items `usage: ["train"]`, ids `<COMP>-uNN`,
ajoutés en fin de `<DOM>.<THEME>.json` (items existants non modifiés). Auteur : agent `concepteur-items`
(25/09/2026). **À relire par `relecteur`.**

Contrôles à chaque compétence : `check_banque.py NC DF` ✅, `validate_exos.py` (0 bloquant), KaTeX (strict),
simulation `_matchFillQ` (app.html) **et** `mxEgal` (index.ts) : `a`, `alt` et variantes de saisie
(`x=`, `×`/`*`, `−` Unicode, unité) acceptées ; clés `err` et mauvaises réponses prévisibles refusées ;
recopie des nombres de l'énoncé testée.

## Fait

| Compétence | Items | lvl 1/2/3 | fill/qcm/vf |
|---|---|---|---|
| NC.ARITH.02 | 4 | 2/1/1 | 2/2/0 |
| NC.LIT.05 | 5 | 2/2/1 | 5/0/0 |
| NC.LIT.08 | 2 | 1/1/0 | 1/1/0 |
| NC.LIT.09 | 1 | 1/0/0 | 0/1/0 |
| NC.LIT.10 | 4 | 1/2/1 | 3/1/0 |
| NC.EQUA.01 | 5 | 2/2/1 | 1/3/1 |
| NC.EQUA.03 | 2 | 0/1/1 | 1/1/0 |
| NC.EQUA.05 | 2 | 0/1/1 | 1/1/0 |
| NC.EQUA.06 | 7 | 3/3/1 | 5/2/0 |
| DF.PROP.01 | 1 | 0/1/0 | 0/1/0 |
| DF.PROP.05 | 3 | 1/1/1 | 0/3/0 |
| DF.PROP.08 | 7 | 3/3/1 | 5/2/0 |
| DF.FONC.03 | 6 | 2/3/1 | 4/2/0 |
| DF.FONC.05 | 3 | 1/1/1 | 1/2/0 |
| DF.AFF.01 | 7 | 3/3/1 | 2/5/0 |
| DF.AFF.03 | 5 | 2/2/1 | 3/2/0 |
| DF.AFF.04 | 7 | 3/3/1 | 3/4/0 |
| DF.STAT.02 | 1 | 0/1/0 | 0/1/0 |
| DF.STAT.05 | 2 | 0/1/1 | 1/1/0 |
| DF.STAT.06 | 5 | 2/2/1 | 3/2/0 |
| DF.STAT.07 | 2 | 0/1/1 | 0/2/0 |
| DF.PROB.01 | 7 | 3/3/1 | 4/2/1 |
| DF.PROB.03 | 3 | 1/1/1 | 2/1/0 |
| DF.PROB.04 | 4 | 2/1/1 | 2/2/0 |
| DF.PROB.05 | 3 | 1/1/1 | 2/1/0 |
| DF.PROB.06 | 4 | 2/1/1 | 1/3/0 |
| **Total** | **102** | **38/42/22** | **52/48/2** |

## Restant

Rien : cible atteinte (102/102). Dernière vérification : `check_banque.py NC DF` ✅, `_legacy/check_legacy.py` ✅
(pas de collision d'id), `validate_exos.py` sur les 8 fichiers touchés ✅ (0 bloquant), `fill_match_node.js` ✅.

## Points pour le relecteur

- **Pas de fill « ___ % »** : `mxEgal` (serveur) n'applique pas la règle `_matchFillQ` sur le « % » ; un `alt`
  « 25% » y ferait accepter « 0,25 ». Les taux d'évolution (DF.PROP.05) sont donc tous en QCM.
- **Fills littéraux** (LIT.05-u01…u05, LIT.08-u02, LIT.10-u01/u02/u04) : `alt` couvre l'ordre inverse des termes
  et `×x` (`_normFill` ne transforme pas `2*x` en `2x`). Simulé : `2*x-7`, `6 − x`, `10(2*x+3)` acceptés ;
  `2x+7`, `14-x`, `3x-6`, `2x+35`, `2(10x+15)` refusés (app et serveur).
- **Recopies acceptées, voulues** : ARITH.02-u01 (« 2 » dans la liste d'entiers), FONC.03-u01 et FONC.05-u02
  (l'abscisse du point à lire figure dans la description de la courbe : c'est la lecture attendue),
  EQUA.06-u03 (« 2 » = exposant de $x^2$). Partout ailleurs, aucune donnée de l'énoncé recopiée n'est acceptée.
- **QCM à 3 options** (pas de 4e distracteur honnête dans le référentiel) : EQUA.01-u05, FONC.05-u01/u03,
  AFF.01-u03/u05/u06, STAT.07-u01, PROB.01-u02/u05, PROB.06-u03/u04.
- **Sans clé `err`** : LIT.10-u04 (`5(n + 2)`) — la mauvaise réponse prévisible `n + 10` relève de LIT.04/LIT.08,
  qui ne sont pas prérequis directs de LIT.10.
- **Erreurs de prérequis (§9)**, toutes directes : ARITH.01→ARITH.02 ; LIT.04→LIT.05 ; RAC.01→LIT.09 ;
  LIT.01/LIT.05→LIT.10 ; LIT.02→EQUA.01 ; EQUA.02→EQUA.03/05/06 ; RAC.01→EQUA.06 ; FRAC.07→PROP.05 ;
  PROP.02/FRAC.04→PROP.08 ; FONC.02→FONC.03/05 ; PROP.01/FONC.01→AFF.01 ; AFF.02/REL.02→AFF.03 ;
  AFF.02/REP.01→AFF.04 ; FRAC.07→STAT.02 ; STAT.01→STAT.05/06 ; STAT.05/06→STAT.07 ; PROB.02→PROB.03/04 ;
  FRAC.03→PROB.04 ; FRAC.05→PROB.05 ; STAT.02→PROB.06.
- Tags à regarder : `EG.REP.01#quadrant` pour la réponse « 4 » au lieu de « −4 » (AFF.04-u01) et « −3 » au lieu
  de « 3 » (AFF.04-u06) ; `DF.STAT.01#valeurs_effectifs` pour « 3 » (effectif de la colonne du milieu,
  STAT.05-u02) ; `NC.REL.02#soustraire_negatif` pour $3 - (-2) = 1$ (AFF.03-u05).
- Graphiques décrits en texte (points reliés par des segments), conformément au §8.
