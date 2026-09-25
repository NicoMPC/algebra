# Complément banque d'entraînement — NC

Cible : `cibles_complement.json` (comp `NC.*`), 120 items `usage: ["train"]`, ids `<COMP>-tNN`,
ajoutés en fin de `NC.<THEME>.json` (items existants non modifiés). Auteur : agent `concepteur-items`
(25/09/2026). **À relire par `relecteur`.** Contrôles passés à chaque compétence : `check_banque.py NC`,
`validate_exos.py`, KaTeX, simulation `_matchFillQ` (bonne réponse + alt acceptées, toutes les clés `err` refusées).

## Fait (120 / 120 items)

| Compétence | Items | lvl 1/2/3 | fill/qcm/vf |
|---|---|---|---|
| NC.ARITH.03 | 9 | 3/4/2 | 5/4/0 |
| NC.ENT.01 | 12 | 5/5/2 | 8/3/1 |
| NC.ENT.02 | 12 | 5/5/2 | 7/4/1 |
| NC.ENT.03 | 12 | 5/5/2 | 8/3/1 |
| NC.FRAC.01 | 4 | 2/2/0 | 2/1/1 |
| NC.FRAC.02 | 6 | 2/3/1 | 3/2/1 |
| NC.FRAC.07 | 11 | 5/4/2 | 2/8/1 |
| NC.LIT.01 | 7 | 3/3/1 | 2/5/0 |
| NC.LIT.03 | 2 | 1/1/0 | 1/1/0 |
| NC.LIT.06 | 4 | 1/2/1 | 2/2/0 |
| NC.LIT.07 | 3 | 1/1/1 | 2/1/0 |
| NC.PRIO.01 | 6 | 2/3/1 | 5/1/0 |
| NC.PUIS.01 | 2 | 1/0/1 | 2/0/0 |
| NC.PUIS.02 | 3 | 1/2/0 | 2/1/0 |
| NC.RAC.01 | 11 | 4/5/2 | 7/3/1 |
| NC.REL.01 | 9 | 3/4/2 | 5/3/1 |
| NC.REL.03 | 7 | 3/3/1 | 5/1/1 |

## Restant

Rien : cible atteinte.

## Points pour le relecteur

- **Peu de fill en NC.FRAC.07 (2/11) et NC.LIT.01 (2/7), c'est voulu.** `_toNum` rend égales toutes les écritures d'un même nombre (`3/4` = `0,75`, `8%` = `0,08`). Dans un fill de conversion, l'élève qui recopie la donnée serait donc compté juste. Et le serveur (`mxEgal`) n'applique pas la règle « ___ % ». Les fill gardés portent sur un numérateur manquant (`\frac{\text{___}}{100}`).
- **Même piège en NC.FRAC.02** (fraction irréductible) : un fill à réponse fraction accepterait une simplification incomplète. On demande donc un numérateur manquant ou le diviseur à utiliser.
- **Fill à réponse littérale** (`LIT.01-t03`, `t06`, `LIT.03-t02`, `LIT.07-t03`) : `alt` couvre l'ordre inverse des termes et `×`. Simulation faite : `4*x-9`, `-9+4x` et `6x − 3` sont acceptés ; `4x+9` et `6x+3` sont refusés.
- **Sans clé `err`** : `NC.FRAC.07-t04` (`3/4 = ___/100`). Aucune erreur type du référentiel ne prédit une mauvaise réponse précise.
- **Erreurs de prérequis utilisées (§9)** : `NC.PUIS.01#carre_decimal` (RAC.01), `NC.ENT.02#plus_de_chiffres` (REL.01), `NC.ARITH.02#*` (ARITH.03), `NC.FRAC.01#pas_quotient` et `NC.ENT.01#nb_rangs` (FRAC.07), `NC.REL.02#mauvais_signe` (LIT.03), `NC.LIT.06#signes` (LIT.07), `NC.PUIS.01#base_fois_exposant` (PUIS.02).
- La bonne réponse des QCM est répartie sur toutes les positions.
- ⚠️ `*.json` est dans `.gitignore` : la banque n'est pas versionnée.
