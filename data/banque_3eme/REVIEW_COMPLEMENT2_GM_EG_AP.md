# Relecture — 2e complément d'entraînement GM, EG, AP (items `-uNN`)

> Relecteur · 26/09/2026 · branche `feat/diagnostic-3e`. Relu : les 127 items `-u` listés dans `COMPLEMENT2_GM_EG_AP.md`.
> Verdicts item par item dans `data/banque_3eme/<DOM>.<THEME>.u-review.json` (correction = item complet). Aucun item édité.

## Bilan : 124 ok · 3 corrige · 0 rejet

| Fichier | Items | ok | corrige | rejet |
|---|---|---|---|---|
| GM.CONV | 12 | 12 | 0 | 0 |
| GM.AIRE | 7 | 7 | 0 | 0 |
| GM.VOL (VOL.01/04/05) | 16 | 16 | 0 | 0 |
| GM.VIT | 7 | 7 | 0 | 0 |
| GM.AGR | 8 | 7 | 1 | 0 |
| EG.REP | 7 | 7 | 0 | 0 |
| EG.ANG | 5 | 5 | 0 | 0 |
| EG.THAL | 3 | 3 | 0 | 0 |
| EG.SEMB | 6 | 6 | 0 | 0 |
| EG.TRIG | 6 | 6 | 0 | 0 |
| EG.TRANS | 15 | 15 | 0 | 0 |
| EG.ESP | 11 | 10 | 1 | 0 |
| AP.PROG | 24 | 23 | 1 | 0 |

Aucune réponse `a` n'est fausse. Aucune clé `err` n'est acceptée comme bonne réponse, que ce soit par l'app ou par le serveur.

## Corrections proposées

- **AP.PROG.05-u07** (tarif de cinéma, âge 15) : la clé `10`, taguée `deux_branches`, est indiscernable. On obtient aussi 10 en inversant **seulement le second test** (lire « 15 < 18 » comme faux). Pour tout âge de la tranche du milieu, les deux erreurs donnent la même valeur. Correction : retirer la clé `10` et garder `5` → `condition_inversee`. C'est le même traitement que les autres cas indiscernables du lot.
- **EG.ESP.01-u05** (cube + pyramide, 9 faces) : l'énoncé dit « pyramide à base carrée » sans préciser « régulière ». Si le sommet de la pyramide est à l'aplomb d'un côté du carré collé, une face triangulaire devient coplanaire avec une face du cube. Les deux faces fusionnent et le solide n'a plus que 8 faces. Correction : écrire « pyramide régulière à base carrée ».
- **GM.AGR.02-u02** (maquette au 1/10) : le calcul est juste, mais le contexte est irréaliste. Le réservoir d'une vraie voiture ferait 3000 L (en réalité ≈ 50 L), et celui d'une maquette de 45 cm contiendrait 3 L. Un élève qui a le sens des grandeurs doutera de sa bonne réponse. Correction : garder le même calcul sur un camion-citerne (3 m³, plausible).

## Contrôles effectués

- **Calculs** : tous refaits. π à la calculatrice (AIRE.03, VOL.04, VOL.05 : 153,94 / 1,1310 / 33,51 / 268,08 / 523,6 / 433,54…), et chaque distracteur recalculé (par exemple 294,52 → 295, 150,80 → 151, 546,6 → 547, 180π = 565,5). Aucun arrondi ne tombe près d'un « ,5 ». Pour VIT.02-u07 : 100 / 9,58 × 3,6 = 37,58. Pour AGR.01-u04 : √2 = 1,414.
- **Scratch** : les 24 scripts AP ont été exécutés pas à pas, ainsi que chaque valeur `err`. Cela couvre les déplacements et l'orientation Scratch (tourner à droite = sens horaire), la suite de Fibonacci d'AP.PROG.04-u06 et les deux branches en séquence d'AP.PROG.05-u04 (3,5 puis 11,5).
- **Comparaison des réponses** : `_matchFillQ`/`_errDe` (app.html) et `mxEgal` (index.ts) ont été extraits et exécutés sous Node sur les 88 fill.
  - `a` et chaque `alt` sont acceptés.
  - Aucune clé `err` n'est acceptée, et chaque clé est retrouvée par `_errDe`.
  - Environ 150 variantes ont été testées en plus : unités, moins Unicode, `[AC]`, minuscules, `√2`, `5/8`, `12 h 30`, `(4 ; 0 ; 2)`, plus 2 à 5 mauvaises réponses prévisibles non taguées par item. Aucune mauvaise réponse n'est acceptée.
- **Clés `err`** : tous les ids existent dans `competences.json`. Chacun appartient à `comp` ou à un **prérequis direct** (§9), ce qui a été vérifié par script. Les rattachements listés par l'auteur sont tous corrects.
- **LaTeX** : KaTeX 0.16.22 en `strict:'error'` sur les items et les corrections, avec `\text{___}` substitué : 1239 segments, 0 erreur.
- **Doublons** : aucun énoncé identique. Certains items reprennent le gabarit d'un `-d` avec d'autres nombres (AIRE.03-u01/u02 et d02, TRIG.01-u02 et d01, ESP.02-u05 et d03, AP.PROG.06-u02 et u03…). C'est acceptable en entraînement.

## Points d'attention de l'auteur

- **Rattachements à un prérequis** : tous valides, y compris `EG.REP.01#xy_inverses` (AP.PROG.02-u04, (−30;10) exact) et `AP.PROG.02#instruction_sautee` (AP.PROG.05-u05, 40 = aucune branche exécutée).
- **Cas indiscernables laissés sans étiquette** (VOL.05-u05 : 509 ; AP.PROG.04-u03/u04) : d'accord. Pour VOL.05-u03, le 720 tagué `oubli_tiers` est d'accord aussi.
- **Réponses égales à une donnée** : EG.REP.03-u01 et EG.ESP.01-u04 sont acceptables, parce que l'élève doit choisir parmi plusieurs données (c'est la compétence). Pour AP.PROG.05-u07, c'est acceptable, mais la clé `10` est corrigée (voir plus haut).
- **`alt` non arrondis** (VIT.02-u07, AIRE.03-u04) : conformes à la convention. À l'inverse, une valeur plus précise que celle des `alt` est refusée (GM.VOL.05-u05 « 433,54 »). C'est cohérent avec « arrondi demandé ».

## Remarques non bloquantes

- **GM.AGR.01-u04** : la clé `4` (= 2², le rapport des aires élevé au carré) ne correspond qu'approximativement à `aire_fois_k`. Aucun id plus juste n'existe au référentiel.
- **EG.ANG.02-u05** : « 40 et 140 » vient d'un oubli du second angle à la base. Le rattacher à `pas_de_partage` est approximatif mais défendable.
- **EG.ESP.02-u03** : l'item mobilise Pythagore, qui n'est pas un prérequis déclaré d'EG.ESP.02. Il est en entraînement seulement et c'est un exercice classique de 3e : acceptable.
- **EG.SEMB.01-u04** : « 8-10-12 » est une erreur additive, taguée `a_l_oeil` faute de mieux.

## Hors items (pour dev-ux / ingénieur adaptatif)

1. **Unités composées** : `_toNum`/`mxNum` ne retirent pas `m/s`, `km/h`, `cL/s` ni `dm2` (sans exposant). Du coup, « 10 m/s » est refusé pour 10. L'unité est affichée après la case, donc l'impact est faible. Correctif possible : ajouter `(/(s|h|min))?` et `2|3` à la regex d'unité.
2. **Coordonnées** : « F(4;0;2) », avec une lettre devant la parenthèse, est refusé. Une virgule comme séparateur est acceptée seulement quand l'item a un `alt` dédié : oui pour EG.REP.03-u04 et AP.PROG.02-u01, non pour EG.TRANS.01-u03 ou EG.TRANS.03-u01. Les énoncés montrent tous le `;`. Reco : une règle générale dans `_normFill`/`mxNorm` (retirer `^[a-z]\(` → `(`), plutôt qu'un `alt` item par item.
3. **Le serveur n'applique pas la règle « ___ % »** de `_matchFillQ`. `mxEgal` n'a pas l'équivalent : un `alt` en `%` y reste converti. Aucun item de ce lot n'est concerné (il n'y a pas de case %), mais c'est à aligner.
