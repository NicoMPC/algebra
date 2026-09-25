# 2e complément banque d'entraînement — GM, EG, AP

> Concepteur d'items · 25/09/2026 · branche `feat/diagnostic-3e`. Cibles : `cibles_complement2.json` (entrées `GM.*`, `EG.*`, `AP.*`), 127 items.
> Items `usage: ["train"]`, ids `<COMP>-uNN`, ajoutés en fin de `<DOM>.<THEME>.json`. Aucun item existant modifié (vérifié par comparaison JSON avec une copie d'avant, ordre compris). À faire relire par le `relecteur`.

## Faites — 127 / 127 items (chaque compétence ciblée atteint 10 items)

| Compétence | Cible | Produits | lvl 1/2/3 |
|---|---|---|---|
| GM.CONV.02 | 5 | 5 | 2/2/1 |
| GM.CONV.03 | 7 | 7 | 3/3/1 |
| GM.AIRE.03 | 7 | 7 | 3/3/1 |
| GM.VOL.01 | 6 | 6 | 2/3/1 |
| GM.VOL.04 | 5 | 5 | 2/2/1 |
| GM.VOL.05 | 5 | 5 | 2/2/1 |
| GM.VIT.02 | 7 | 7 | 3/3/1 |
| GM.AGR.01 | 4 | 4 | 2/1/1 |
| GM.AGR.02 | 4 | 4 | 1/2/1 |
| EG.REP.03 | 7 | 7 | 3/3/1 |
| EG.ANG.02 | 5 | 5 | 2/2/1 |
| EG.THAL.03 | 3 | 3 | 1/1/1 |
| EG.SEMB.01 | 6 | 6 | 2/3/1 |
| EG.TRIG.01 | 6 | 6 | 2/3/1 |
| EG.TRANS.01 | 7 | 7 | 3/3/1 |
| EG.TRANS.02 | 2 | 2 | 1/1/0 |
| EG.TRANS.03 | 1 | 1 | 0/1/0 |
| EG.TRANS.04 | 2 | 2 | 1/1/0 |
| EG.TRANS.05 | 3 | 3 | 1/1/1 |
| EG.ESP.01 | 5 | 5 | 2/2/1 |
| EG.ESP.02 | 6 | 6 | 2/3/1 |
| AP.PROG.02 | 4 | 4 | 2/1/1 |
| AP.PROG.04 | 6 | 6 | 2/3/1 |
| AP.PROG.05 | 7 | 7 | 3/3/1 |
| AP.PROG.06 | 7 | 7 | 3/3/1 |

Total : lvl 1 = 50, lvl 2 = 55, lvl 3 = 22 ; fill 88, qcm 39, vf 0. Bonne réponse QCM répartie sur toutes les positions.

## Restantes — 0

## Contrôles (25/09)

- `check_banque.py GM EG AP` : ✅ OK. Seul warning : `NC.LIT.10-u04` (fichier NC, autre agent).
- `validate_exos.py` sur les 13 fichiers touchés : ✅, uniquement des warnings non bloquants (lvl 3, taille de lot, faux « prénoms répétés » sur des mots de Scratch).
- KaTeX 0.16.22 `strict:'error'` sur tous les `$…$` des 127 items (`\text{___}` substitué) : 1125 segments, 0 erreur.
- Simulation des 88 fill avec `_matchFillQ` (extrait d'`app.html`) **et** `mxEgal` (extrait de `supabase/functions/api/index.ts`) : `a` et chaque `alt` acceptés, ainsi que les variantes de saisie (espaces, moins Unicode, `[AC]`, `√2`, `5/8`…). Chaque clé `err` est refusée et retrouvée par `_errDe`. 2 à 4 mauvaises réponses prévisibles non taguées par item sont refusées aussi. 0 problème. `fill_match_node.js` : all ok.
- Les 24 scripts AP ont été exécutés pas à pas (simulateur Python : déplacements, variables, conditions, boucles), avec toutes les valeurs `err` (branche inversée, deux branches, ±1 tour, valeur initiale oubliée, mettre/ajouter).
- Tous les calculs ont été refaits (π à la calculatrice pour AIRE.03, VOL.04 et VOL.05 ; arrondis vérifiés loin d'un « ,5 » pile).

## Points d'attention pour le relecteur

- **`err` rattachés à un prérequis direct (§9)** : `GM.CONV.01#rapport_unites`/`#mauvais_sens` (CONV.02-u03), `NC.PUIS.01#carre_double` (AGR.01-u01/u02), `GM.AGR.01#rapport_inverse` (AGR.02-u02), `GM.VOL.03#oubli_tiers` (VOL.05-u03), `GM.VOL.04#r_carre` (VOL.05-u04), `EG.THAL.01#segment_partiel`/`#rapports_croises` (THAL.03-u01/u02), `EG.ANG.01#somme_360` (SEMB.01-u05), `EG.PYTH.01#hypotenuse_mal_identifiee` (TRIG.01-u01/u04), `EG.TRANS.04#longueur_negative` (TRANS.05-u03), `EG.REP.01#xy_inverses` (AP.PROG.02-u04), `AP.PROG.02#instruction_sautee` (AP.PROG.05-u05), `AP.PROG.03#*` (AP.PROG.04-u05/u06).
- **Erreurs indiscernables, laissées sans étiquette** :
  - VOL.05-u05 (gourde) : la valeur 509 correspond aussi bien à l'oubli du ÷ 3 qu'à un cylindre unique de 18 cm. C'est vrai pour tout solide cylindre + cône : π r² (h₁ + h₂) = π r² H. On la garde en mauvaise réponse non taguée.
  - VOL.05-u03 : 720 est tagué `oubli_tiers`. Le même nombre sort d'un pavé de 9 m de haut, mais la hauteur totale n'est pas donnée dans l'énoncé, donc c'est peu probable.
  - AP.PROG.04-u03/u04 : la valeur commune à `valeur_initiale` et à `mettre_ajouter` n'est pas taguée.
- **Réponse égale à une donnée, par construction** : EG.REP.03-u01 (lire une coordonnée), EG.ESP.01-u04 (la génératrice est le rayon du secteur ; le distracteur `patron_cone` = 3 est tagué), AP.PROG.05-u07 (le tarif affiché est une des valeurs du script). Le fait de recopier ne correspond à aucune erreur type.
- AP.PROG.05-u07 : `10` est tagué `deux_branches`. C'est la valeur finale si l'élève exécute toutes les branches, puisque la dernière affectation l'emporte.
- VIT.02-u07 et GM.AIRE.03-u04 : l'arrondi est demandé, mais la valeur non arrondie est acceptée en `alt` (même choix que les relectures précédentes). Les QCM à 3 options, quand il n'existe que 3 choix naturels (côtés, axes, branches), sont assumés.
- Scratch : blocs du Brevet (« mettre … à », « ajouter … à », « répéter … fois », « si … alors / sinon », « demander », « s'orienter à », « tourner à droite/gauche de … degrés »). On a ajouté les lignes « Fin répéter » et « Fin si », et rappelé la convention d'orientation dans les énoncés de déplacement. Les champs `f` d'AP.PROG.02/04/05 sont vides (convention AP).
- `validate_exos.py` écrit un log par exécution dans `docs/logs/` (fichiers `validate-2026-09-25-22*.md`, non suivis).
