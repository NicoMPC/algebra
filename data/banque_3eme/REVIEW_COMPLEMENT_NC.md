# Relecture du complément NC : items d'entraînement (`-tNN`)

Relecteur : agent `relecteur`, 25/09/2026, branche `feat/diagnostic-3e`. Items non modifiés.
Détail par item : `NC.<THEME>.train-review.json`. Chaque item `corrige` y porte l'item complet (`correction`).

## Bilan

| Fichier | Items `-t` | ok | corrigé | rejet |
|---|---|---|---|---|
| NC.ENT | 36 | 35 | 1 | 0 |
| NC.RAC | 11 | 11 | 0 | 0 |
| NC.FRAC | 21 | 20 | 1 | 0 |
| NC.REL | 16 | 15 | 1 | 0 |
| NC.ARITH | 9 | 9 | 0 | 0 |
| NC.LIT | 16 | 11 | 5 | 0 |
| NC.PRIO | 6 | 6 | 0 | 0 |
| NC.PUIS | 5 | 5 | 0 | 0 |
| **Total** | **120** | **112** | **8** | **0** |

**Ce que j'ai vérifié :**
- J'ai refait tous les calculs. Aucune réponse `a` n'est fausse, et chaque réponse est unique.
- J'ai simulé les fills dans Node avec `_matchFillQ` / `_matchFill` / `_toNum` extraits d'`app.html`, et avec `mxEgal` / `mxNorm` / `mxNum` extraits d'`index.ts`. Pour chaque item :
  - `a` et chaque `alt` sont acceptés ;
  - chaque clé `err` est refusée ;
  - les nombres de l'énoncé recopiés tels quels sont testés.
- Les seules recopies acceptées sont celles des items « choisis parmi les valeurs données » (ENT.02-t01/t04/t09/t11, REL.01-t01/t06). C'est le principe même de ces items. Aucun fill de conversion n'accepte une recopie : FRAC.07-t04/t08 refusent `3`, `0,75` et `0,08`.
- KaTeX : tous les segments `$…$` (énoncés, options, steps, `f`, alt, corrections) se rendent sans erreur, `\text{___}` compris une fois remplacé par `\boxed{\phantom{xx}}`. Le test a tourné avec KaTeX 0.16.22 (seule version locale), pas 0.16.9. Les macros utilisées sont basiques.
- Les erreurs de prérequis (§9) sont toutes des prérequis directs de `comp` : PUIS.01→RAC.01, ENT.02→REL.01, ARITH.02→ARITH.03, FRAC.01/ENT.01→FRAC.07, REL.02→LIT.03, LIT.06→LIT.07, PUIS.01→PUIS.02.
- Doublons : aucun avec les items `-d` de la même compétence. Quelques items ont la même forme avec d'autres valeurs (ENT.01-t11 / d03, RAC.01-t06 / d02) : ce ne sont pas des doublons.
- `check_banque.py` repasse ✅ sur la banque NC avec les corrections appliquées (copie dans le scratchpad). Le seul avertissement, déjà connu, est FRAC.07-t04 sans `err`, que j'accepte.

## Corrections

1. **Tag faux sur `LIT.01-t04`.**
   - L'énoncé dit « 3 ans **de plus** ». Le distracteur `n + 3` applique la relation à la mauvaise personne : ce n'est pas `#de_moins_plus`, et aucune erreur du référentiel ne décrit ce cas.
   - Je reformule en « 3 € de moins que » dans un contexte de tarifs, pour ne pas doubler LIT.01-d02 qui porte sur des âges.
2. **Tag ambigu sur `REL.01-t09`.**
   - `−4,09 < −4,1` est aussi produit par `#distance_zero` seul.
   - Avec deux négatifs, toute comparaison fausse devient « vraie » sous `#distance_zero` : on ne peut donc pas isoler `NC.ENT.02#plus_de_chiffres` ici. Je ramène le tag à `#distance_zero`.
3. **Clé err non prédite sur `ENT.02-t11`.**
   - La clé `52,4` (`#plus_de_chiffres`) ne correspond à aucune règle erronée. Je la retire.
4. **Indice qui donne la réponse (`FRAC.07-t01`).**
   - L'indice « 1/5 = 2/10, combien de dixièmes ? » donne la réponse. Je le reformule : l'élève doit trouver lui-même la fraction de dénominateur 10.
5. **Faux négatifs de saisie** (app et serveur, `alt` ajoutés ; la simulation confirme qu'aucune mauvaise réponse ne passe) :
   - `LIT.03-t02` et `LIT.07-t03` : `6*x-3` et `6×x+9` étaient refusés. La note de l'auteur annonçait pourtant que `×` était couvert : c'est vrai seulement pour LIT.01.
   - `LIT.06-t02` et `LIT.07-t01` : la case est suivie de « x », et l'élève qui tape `-2x` ou `12x` était refusé.

## Points signalés par l'auteur

| Point | Verdict |
|---|---|
| Peu de fills en FRAC.07 / LIT.01 / FRAC.02 (piège de conversion `_toNum`) | Ok, justifié. Les fills gardés (numérateur manquant, diviseur) n'acceptent aucune recopie. |
| FRAC.07-t04 sans `err` | Ok |
| Fills littéraux | LIT.01-t03/t06 ok. LIT.03-t02 et LIT.07-t03 corrigés (× manquant). |
| Erreurs de prérequis | Ok : toutes directes. Seul le tag REL.01-t09 est ramené à la compétence (ambiguïté). |

## Remarques sans correction

- **Items de comparaison à deux valeurs** (ENT.02-t01/t02/t04/t05/t09) : l'une des deux règles erronées donne forcément la bonne réponse, et l'item n'en teste que l'autre. C'est acceptable en entraînement, puisqu'une seule erreur est taguée.
- **`LIT.01-t03`/`t06`** : `4(x−9)` et `18(r−7)` sont des parenthèses **en trop**, taguées `#parentheses_oubliees`. Je les tolère : c'est la même famille d'erreur, la structure du programme mal traduite.
- **Arrondis** : `5` pour 5,0 (ENT.03-t06) et `10` pour 10,00 (ENT.03-t12) sont acceptés par égalité numérique. Je le tolère.

## Problèmes transversaux (code, pour le dev)

- `mxNorm` (serveur) ne retire pas le `+` de tête, alors que `_normFill` le fait. Aucun impact sur ces 120 items, mais le portage n'est plus fidèle.
- `_errDe` / `mxErreurType` ne retrouvent pas une clé `err` quand l'élève tape la lettre avec le coefficient. Exemple : `6x` au lieu de la clé `6` dans LIT.07-t01. L'erreur type est alors perdue, sans conséquence sur la correction.

## ❓ Questions pour Nicolas

1. Faut-il ajouter au référentiel une erreur `NC.LIT.01#relation_inversee` (« 3 ans de plus que son frère » → `n + 3` pour le frère) et `#parentheses_superflues` ? Ma reco : oui, via le didacticien. Les deux reviennent souvent en traduction.
