# Relecture DF + GM — 24/09/2026

Relecteur indépendant. 10 fichiers, **138 items** (qcm 55, vf 13, fill 70). Chaque calcul a été refait à la main. `_normFill` / `_toNum` / `_matchFill` ont été extraits d'`app.html` (version corrigée du 24/09) et exécutés sous Node sur `a`, `alt`, toutes les clés `err` et des variantes prévisibles (unité, `%`, virgule/point, `x=`, `kπ`, décimal équivalent).

## Bilan

| Fichier | ok | corrige | rejet |
|---|---|---|---|
| DF.PROP | 23 | 1 | 0 |
| DF.FONC | 10 | 5 | 0 |
| DF.AFF | 11 | 4 | 0 |
| DF.PROB | 17 | 1 | 0 |
| DF.STAT | 21 | 0 | 0 |
| GM.CONV | 8 | 1 | 0 |
| GM.AIRE | 7 | 2 | 0 |
| GM.VOL | 8 | 7 | 0 |
| GM.VIT | 6 | 0 | 0 |
| GM.AGR | 6 | 0 | 0 |
| **Total** | **117** | **21** | **0** |

- **Aucune réponse `a` fausse.** Aucune clé `err` n'est égale à `a` ou à un `alt`, et aucune n'est acceptée par `_matchFill`. Toutes les réponses `a` passent.
- Banque corrigée (les 21 corrections appliquées sur une copie) : `check_banque.py DF GM` renvoie ✅ OK.
- Détail item par item, avec l'item corrigé complet : `<DOMAINE>.<THEME>.review.json`.

## Corrections de fond (le diagnostic serait faux)

| Item | Problème | Correction |
|---|---|---|
| DF.PROP.07-d01 | Réponse 4,5 = donnée 4,5 cm (échelle 1/100, cm→m) : recopier la donnée compte comme juste | échelle 1/50, 9 cm → 4,5 m |
| GM.CONV.02-d02 | Réponse 54 = donnée 54 dm³ : recopier la donnée compte comme juste | 18 000 cm³ → 18 L |
| GM.VOL.02-d02 | Triangle 3-4-5 : périmètre = 2 × aire, donc 120 veut dire aussi bien « périmètre × h » qu'« oubli du ÷2 » | triangle 9-12-15 → 540 |
| GM.AIRE.03-d03 | 3,14 × 225 = 706,5 pile : la réponse dépend de la convention d'arrondi | r = 12 → 452 (même arrondi avec π calculatrice), valeurs non arrondies en `alt` |
| DF.PROB.01-d03 | Deux pièces : prérequis caché DF.PROB.05 (3e) sur une compétence 5e | une seule épreuve (billes numérotées) |
| DF.FONC.04-d02 | x² = 9 repose sur NC.EQUA.06, qui n'est **pas** prérequis de DF.FONC.04 | item inchangé ; **ajouter NC.EQUA.06 aux prérequis de DF.FONC.04** (didacticien) |

## Étiquettes `err` fausses (le bilan afficherait la mauvaise erreur)

- DF.FONC.01-d03 : la clé `6` (erreur de colonne) est retirée.
- DF.FONC.05-d02 : « Il est à l'arrêt » ne correspond pas à `variations_valeurs`. Remplacé par « Il accélère » (le palier est la vitesse maximale).
- DF.AFF.02-d01 : la clé `5` (= C(1)) est retirée.
- DF.AFF.02-d02 : la clé `775` (= V(1)) est remplacée par `-25`.
- DF.AFF.02-d03 : « 75 € par heure » (a + b) n'a aucune erreur au référentiel. Passé en fill sur b. Autre option : créer `DF.AFF.02#somme_a_b` et garder le QCM.
- GM.VOL.01-d01 : la clé `24` (aucune somme de dimensions ne donne 24) est retirée.

## Bonnes réponses refusées par `_matchFill` (ajout d'`alt`)

- Items « k π » (GM.AIRE.03-d02, GM.VOL.02-d03, 03-d03, 04-d02, 05-d02, 05-d03) : « 9π » est refusé. Ajout de `kπ`, `kpi`, `k\pi`.
- `a=3` (DF.AFF.03-d01), `x=4` et `x=9` (DF.FONC.04-d01/d03).

## Points prioritaires signalés par l'auteur

- **DF.FONC.05-d02** : corrigé (étiquette, voir plus haut).
- **DF.PROP.03-d02** : ok. 210 est juste. `35` tagué `soustrait_taux` colle au titre du libellé mais pas à son exemple ; acceptable.
- **DF.PROB.01-d03** : le lvl 2 n'est pas le problème, c'est le prérequis caché. Corrigé.
- **GM.AIRE.03-d03** : corrigé (valeur à 0,5 pile).
- **DF.FONC.04-d02** : acceptable seulement si le référentiel relie DF.FONC.04 à NC.EQUA.06. On ne peut pas simplement le retirer du diag : DF.FONC.04 tomberait à 2 items et à 1 seule erreur type (check bloquant).
- **DF.AFF.02** : les 3 items corrigés (étiquettes).
- **DF.PROP.06** : les 3 items sont ok (72 ; 400 avec 375 = inverse par le même taux ; 100 → 110 → 99).
- **Items graphes** DF.FONC.02/03/05, DF.AFF.04, DF.STAT.01-d02 : descriptions non ambiguës, réponse unique. Limite assumée : quand l'énoncé rappelle l'échelle, l'erreur de graduation devient moins probable. L'item sous-détecte l'erreur, mais ne produit pas de faux diagnostic.

## Hors items : à traiter dans le code

1. **`_matchFill` et `%`** : un `alt` « 25% » a `_toNum` = 0,25, donc « 0,25 » ou « 1/4 » tapés dans une case « ___ % » sont acceptés. Concerne DF.PROP.05-d01, DF.STAT.02-d01, DF.STAT.02-d03, DF.PROB.03-d03. Ça ne se corrige pas dans l'item (sans cet `alt`, « 25 % » serait refusé). Correctif proposé : à l'étape 4, ne comparer numériquement un `alt` en `%` qu'avec une saisie qui contient elle aussi `%`.
2. **Préfixe `x=` / `a=`** : une règle générale dans `_normFill` (retirer `^[a-z]=`) éviterait d'avoir à ajouter un `alt` item par item.
3. **Correspondance `err` ↔ saisie** : si le moteur cherche la saisie brute dans les clés `err`, « 3/5 » ne sera pas reconnu pour la clé `6/10` (DF.PROB.02-d02). Il vaut mieux normaliser la saisie via `_normFill`/`_toNum` avant la recherche.
4. **Rendu des `table`** : seul le rendu d'exercice (`app.html` ~l. 9320) dessine `table`. La vue rétro `_renderRetroExo` ne le fait pas. Le futur écran de diagnostic devra le faire, sinon 9 items DF deviennent insolubles.
