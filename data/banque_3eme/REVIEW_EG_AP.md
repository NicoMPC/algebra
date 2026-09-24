# Relecture diagnostic : EG + AP (90 items)

Relecteur, 24/09/2026. Branche `feat/diagnostic-3e`. Aucun item modifié : les verdicts et les corrections complètes sont dans les `*.review.json`.

## Méthode
- Tous les calculs refaits à la main. Trigo : valeurs recalculées en degrés, en radians et en grades, avec leurs arrondis.
- `_normFill`, `_toNum` et `_matchFill` (version stricte du 24/09) extraits d'`app.html` et simulés en Node. Pour chaque fill, on a testé `a`, `alt`, les variantes raisonnables (virgule/point, unité en fin, fraction, casse, crochets) et chaque clé `err`. **Aucune clé `err` ni réponse fausse testée n'est acceptée.**
- LaTeX de tous les champs passé dans KaTeX 0.16.9 en `strict:'error'`, après la substitution `\text{___}`. 0 erreur.
- Tous les ids `err` existent dans `competences.json`.
- Scripts Scratch et robot exécutés pas à pas.

## Bilan

| Fichier | ok | corrige | rejet |
|---|---|---|---|
| EG.ANG | 9 | 0 | 0 |
| EG.ESP | 6 | 0 | 0 |
| EG.PYTH | 7 | 2 | 0 |
| EG.REP | 6 | 3 | 0 |
| EG.SEMB | 3 | 0 | 0 |
| EG.THAL | 8 | 1 | 0 |
| EG.TRANS | 10 | 5 | 0 |
| EG.TRIG | 11 | 1 | 0 |
| AP.PROG | 12 | 6 | 0 |
| **Total** | **72** | **18** | **0** |

**Aucune réponse `a` fausse ni ambiguë** sur les 90 items. Les 18 corrections portent sur quatre points : des clés `err` qui étiquetteraient mal l'élève dans le bilan parent, la validité de l'item (notation ou indentation), le périmètre du programme, ou la formulation.

## Corrections importantes (elles changent ce que dit le bilan)
1. **EG.TRANS.02-d02** (point signalé, confirmé) : `soustrait_vecteur` (C − v) et `vecteur_inverse` (C + (A − B)) donnent **toujours** le même point sur un item en coordonnées : les deux erreurs sont indiscernables. De plus, `(3 ; −2)` ne correspond pas à `soustrait_vecteur`. Correction proposée : `(−3 ; −2)` → `soustrait_vecteur`, et `(4 ; 2)` (C + B) à la place de `(3 ; −2)`, avec un **id à créer** `EG.TRANS.02#ajoute_coordonnees_image`. Reco didacticien : fusionner `vecteur_inverse` dans `soustrait_vecteur`.
2. **EG.TRANS.03-d01** : la clé `"0"` → `mauvais_centre` n'a aucune justification. Elle ferait écrire à tort « tourne autour du mauvais point ». Clé à retirer.
3. **EG.TRANS.05-d02** : `−24` est une longueur négative. Il faut le rattacher à `EG.TRANS.04#longueur_negative`, pas à `homothetie_conserve`.
4. **AP.PROG.03-d01/02/03** : même avec les retours à la ligne, **si l'indentation est perdue le corps de la boucle devient ambigu** et la bonne réponse change (6↔4, 9↔12…). Correction : ajouter une ligne `Fin répéter`. À intégrer à la convention Scratch, tout comme un `Fin si` facultatif pour les « si/sinon ». En l'état, AP.PROG.05 et AP.PROG.06 ne sont pas ambigus : rien ne suit le bloc, ou le résultat est le même quelle que soit la lecture.
5. **AP.PROG.04-d01/02/03** : la notation `n ← n + 4` n'est pas celle du collège ni du Brevet, qui utilisent les blocs Scratch « mettre n à », « ajouter 4 à n ». L'élève échouerait sur la notation et non sur la compétence. Réécriture proposée en blocs Scratch, avec un err `21` ajouté sur d01.
6. **EG.REP.02-d01/02/03** (point signalé) : la mathématique est juste, mais la compétence est hors programme du cycle 4. Le contrat commun §8 impose `usage: ["train"]` uniquement. Retrait du diagnostic.

## Corrections mineures
- EG.PYTH.02-d01 et d03 : ajout des mauvaises réponses prévisibles `64` et `576` (oubli de la racine carrée).
- EG.TRANS.04-d03 : ajout de `6` (3 × ΩA sans repartir du centre).
- EG.TRIG.04-d02 : ajout d'une 4e option `30°` (sinus au lieu du cosinus).
- EG.THAL.01-d02 : « On peut écrire » devient « On peut en déduire que ». Un bon élève pouvait contester la formulation d'origine.
- EG.TRANS.04-d01 : l'énoncé « de longueur ? ___ » devient « de quelle longueur ? ___ ».

## Points signalés par l'auteur
- **EG.TRIG.03 et EG.TRIG.04** : toutes les valeurs `mode_calculatrice` et `pas_arccos` ont été vérifiées et sont exactes. Radians : −9,52 / −6,30 / −39,5. Grades : 5,88 / 10,21 / 18,2. cos(0,5°) ≈ 1 et cos(0,5 rad) ≈ 0,88. Verdict ok.
- **EG.THAL.03-d01** : juste, verdict ok. Faiblesses de forme, non bloquantes : le distracteur « inférieur à 1 » est peu crédible, et la bonne réponse est la plus longue.
- **QCM à 3 options** (19 items) : acceptables quand il n'existe que 3 choix possibles (3 côtés, 3 égalités de Pythagore, 3 formes). Une seule 4e option est proposée, là où un distracteur naturel existe (TRIG.04-d02).
- **Blocs ajoutés à la convention (AP.PROG.05/06)** : corrects, conformes aux libellés Scratch français. Il faut juste ajouter les marqueurs de fin de bloc (voir point 4).

## Hors items (pour dev-ux)
- `_normFill` ne normalise pas le moins Unicode `−` (U+2212, clavier iOS ou copier-coller) : « −5 » est refusé pour « -5 ». Cela touche toutes les réponses négatives. Reco : `replace(/[−–]/g,'-')` dans `_normFill` et `_toNum`.

## ❓ Questions pour Nicolas
1. Le diagnostic se fait-il **avec calculatrice** ? Les items TRIG.03 et TRIG.04 le supposent, car cos 60° n'est pas exigible de mémoire. Reco : oui, et l'écrire dans la consigne du diagnostic.
2. Faut-il créer l'id `EG.TRANS.02#ajoute_coordonnees_image` et fusionner `vecteur_inverse` dans `soustrait_vecteur` ? Reco : oui (décision du didacticien).
3. EG.REP.02 : faut-il le garder dans le référentiel en « train » seul, sans aucun item de diagnostic ? Reco : oui, en poids 1.
