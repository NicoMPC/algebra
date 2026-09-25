# Complément banque d'entraînement — DF, GM, EG, AP

> Concepteur d'items · 25/09/2026 · branche `feat/diagnostic-3e`. Cibles : `cibles_complement.json` (hors `NC.*`), 107 items.
> Items `usage: ["train"]`, ids `<COMP>-tNN`, ajoutés en fin de `<DOM>.<THEME>.json`. À faire relire par le `relecteur`.
> Contrôles par compétence : `check_banque.py`, `validate_exos.py`, simulation `_matchFillQ` (app.html) sur `a`/`alt` et sur chaque clé `err` + mauvaises réponses prévisibles.

## Faites — 107 / 107 items

| Compétence | Cible | Produits |
|---|---|---|
| EG.REP.01 | 10 | 10 |
| DF.STAT.01 | 4 | 4 |
| DF.FONC.02 | 8 | 8 |
| DF.AFF.02 | 7 | 7 |
| GM.CONV.01 | 11 | 11 |
| EG.THAL.01 | 9 | 9 |
| DF.PROP.03 | 7 | 7 |
| DF.STAT.03 | 8 | 8 |
| GM.VOL.02 | 7 | 7 |
| GM.VOL.03 | 9 | 9 |
| EG.TRIG.02 | 9 | 9 |
| AP.PROG.03 | 10 | 10 |
| EG.ANG.01 | 8 | 8 |

## Restantes — 0

Aucune.

## Contrôles finaux (25/09)

- `check_banque.py DF GM EG AP` : ✅ OK (580 items dans la banque). `validate_exos.py` sur les 11 fichiers touchés : ✅, uniquement des warnings non bloquants (lvl 3, taille de batch, faux « prénoms répétés »).
- Simulation `_matchFillQ` (extrait d'`app.html`) : pour chaque fill, `a` + `alt` acceptés ; chaque clé `err` + 2-3 mauvaises réponses prévisibles non taguées refusées. 0 problème.
- KaTeX 0.16 `strict:'error'` sur tous les `$…$` des nouveaux items (après substitution `\text{___}`) : 981 segments, 0 erreur.
- Répartition : lvl 1 = 44, lvl 2 = 41, lvl 3 = 22 ; fill 74, qcm 32, vf 1.
- Scratch (AP.PROG.03) : blocs du Brevet (« répéter n fois », « ajouter … à x », « mettre … à », « dire »), ligne « Fin répéter » systématique.
- Items « kπ » : `alt` `kπ` / `kpi` / `k\pi` ajoutés. Items trigo : calculatrice supposée (contrat §8).

## Points d'attention pour le relecteur

- `err` rattachés à un prérequis direct (§9) : `NC.REL.01#graduation` (EG.REP.01), `EG.REP.01#quadrant` (DF.FONC.02), `DF.AFF.01#affine_proportionnel` (DF.AFF.02), `NC.ENT.01#*` (GM.CONV.01), `NC.FRAC.07#pourcent_virgule` (DF.PROP.03), `NC.PRIO.01#trait_fraction` (DF.STAT.03), `GM.VOL.01#somme_dimensions` / `GM.VOL.02#*` (GM.VOL.02/03), `EG.TRIG.01#*` (EG.TRIG.02), `AP.PROG.02#instruction_sautee` (AP.PROG.03).
- GM.VOL.02-t05 (prisme à base triangulaire) : l'oubli du ÷ 2 (5,4) relève de `GM.AIRE.02#triangle_sans_moitie`, qui n'est pas un prérequis direct de GM.VOL.02 : laissé sans `err`. Idem pour DF.STAT.03-t08 (réponse « 13 »).
- GM.VOL.02-t07 accepte `2,83` en plus de l'arrondi au dixième `2,8` (même choix que la relecture DF/GM pour les arrondis).
- Les `*.json` de `data/banque_3eme/` sont couverts par `.gitignore` (`*.json`) : les ajouts ne sont pas visibles dans `git status`.
