# Relecture du complément 2 — NC + DF (items `-u`)

Relecteur : agent `relecteur`, 25-26/09/2026. Périmètre : les 102 items d'entraînement dont l'id contient `-u`,
dans `NC.ARITH`, `NC.LIT`, `NC.EQUA`, `DF.PROP`, `DF.FONC`, `DF.AFF`, `DF.STAT` et `DF.PROB`. Les items n'ont pas
été modifiés : les verdicts sont dans `<DOM>.<THEME>.u-review.json`, à appliquer avec `apply_reviews.py`.

## Bilan

| Fichier | Items | ok | corrigé | rejet |
|---|---|---|---|---|
| NC.ARITH | 4 | 4 | 0 | 0 |
| NC.LIT | 12 | 11 | 1 | 0 |
| NC.EQUA | 16 | 16 | 0 | 0 |
| DF.PROP | 11 | 11 | 0 | 0 |
| DF.FONC | 9 | 8 | 1 | 0 |
| DF.AFF | 19 | 19 | 0 | 0 |
| DF.STAT | 10 | 10 | 0 | 0 |
| DF.PROB | 21 | 19 | 2 | 0 |
| **Total** | **102** | **98** | **4** | **0** |

## Méthode

- Chaque calcul a été refait à la main, distracteurs compris : pour chaque clé `err`, j'ai recalculé le chemin
  d'erreur annoncé.
- Contrôle automatique sur les 102 items :
  - la compétence existe et l'id lui correspond ;
  - chaque id d'erreur existe dans le référentiel et appartient à `comp` ou à un **prérequis direct** (§9) ;
  - chaque distracteur de QCM a une clé `err` ;
  - `a` fait partie des options ;
  - `usage` vaut `["train"]`.
- Pour les fill, tests de saisie avec `_matchFillQ` (extrait d'`app.html`) **et** `mxEgal` (porté depuis `index.ts`) :
  - `a` et chaque `alt` sont acceptés ;
  - aucune clé `err` n'est acceptée ;
  - aucun nombre recopié de l'énoncé n'est accepté ;
  - des variantes de saisie sont testées (`x=`, `−` Unicode, unité, fraction ou décimal équivalent, `%`).
- Rendu KaTeX (strict) des corrections proposées : 30 formules, 0 erreur.
- Doublons : comparaison des énoncés avec les autres items de la même compétence. On trouve des variantes de gabarit,
  avec d'autres nombres (normal pour de l'entraînement), mais aucun doublon.

## Corrections

1. **NC.LIT.10-u04**. La réponse `n + 2` était écrite dans l'énoncé : c'était le 3e des cinq entiers listés, donc
   on pouvait la recopier. Nouvel énoncé : « on appelle $n$ le plus petit des cinq », sans lister les entiers ; les
   steps sont adaptés.
2. **DF.FONC.03-u03**. Le step 2 (« Sur chacun des trois segments… ? », réponse « oui » partout) donnait la réponse 3.
   Il est reformulé pour faire compter les passages à la hauteur 5.
3. **DF.PROB.04-u01**. Avec 5 stylos bleus sur 16, P(bleu) = 5/16 = la bonne réponse : un élève qui lit la mauvaise
   couleur est compté juste. Nouvelle composition : 4 bleus et 7 verts. Le total reste 16 et les `err` ne changent pas.
4. **DF.PROB.06-u01**. Le distracteur « probabilité de 6/7 » ne correspondait à aucune fréquence observée, alors que
   6 rouges sur 6 tours donne 1. Il est remplacé par « probabilité de $1$, puisqu'il est sorti à chaque fois »
   (`frequence_egale_proba`).

## Points de l'auteur vérifiés

- **Recopies assumées** : ARITH.02-u01, EQUA.06-u03, FONC.03-u01 et FONC.05-u02 sont acceptées telles quelles.
  Le « 5 » signalé sur FONC.03-u06 vient du LaTeX de `0{,}5` : il n'est pas recopiable.
- **Tags des prérequis** : les tags §9 annoncés sont tous des prérequis directs, et les chemins sont recalculés et
  conformes. En particulier :
  - AFF.03-u05 → `REL.02#soustraire_negatif` donne bien $-10x - 13$ ;
  - STAT.05-u02 → `STAT.01#valeurs_effectifs` donne « 3 » ;
  - AFF.04-u01 et AFF.04-u06 → `EG.REP.01#quadrant` : acceptable, faute d'erreur « signe de b » propre à AFF.04.
- **Pas de fill « ___ % »**, ce qui est cohérent avec la limite de `mxEgal` : les taux de DF.PROP.05 sont en QCM et
  tous justes.
- **Fills littéraux** (LIT.05, LIT.08, LIT.10) : l'ordre inverse et `×x` sont acceptés, et les erreurs prévisibles
  refusées, dans l'app comme sur le serveur.

## Remarques mineures (sans correction)

- **Rattachements un peu lâches mais admissibles** :
  - STAT.07-u02, « plus grand score » → `STAT.06#max_seul` ;
  - PROB.05-u02, $\frac{5}{9}$ → `branche_additionnee` : c'est plutôt une somme directe, mais FRAC.03 n'est pas
    prérequis direct de PROB.05 ;
  - PROB.01-u07 : le calcul relève aussi de PROB.02.
- **Mauvaises réponses prévisibles sans clé** (aucun id adapté dans le référentiel) :
  - STAT.06-u05 : « 135 », l'ancienne étendue ;
  - EQUA.03-u01 : « 3 », pour $7x = 21$ ;
  - PROP.08-u07 : « 16 », le nombre de filles.
- `f` est vide sur 34 items, comme dans une bonne partie de la banque existante : ce n'est pas bloquant.
