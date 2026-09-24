# Couverture de la banque existante par le référentiel 3e

> Généré par `data/referentiel_3eme/couverture.py` — ne pas éditer à la main.
> Mapping manuel question → compétence (approximation raisonnable), exporté dans `mapping_legacy.json`.

## Périmètre analysé

- **440 questions** des 22 chapitres v4 (`data/*_Brevet_v4.json`, `data/Auto_*_v4.json`, 4 parapluies × 5 sous-questions)
- **54 questions** de `data/diagnostic_3eme.json`
- `data/diag_*.json` : 54 questions, **toutes des copies** de `diagnostic_3eme.json` → comptées une seule fois
- Non inclus : `data/bank_6eme|5eme|4eme/` (320 items, format par niveau, pas encore en base) — réutilisables pour les prérequis 6e/5e/4e après mapping
- Total unique : **494 questions** → 121 compétences

**Constat structurel** : aucune question existante n'a de champ `err` (mauvaise réponse → erreur type). La banque actuelle permet donc de mesurer la réussite, **pas de diagnostiquer les erreurs types**. Les distracteurs QCM existants sont souvent réalistes : ils peuvent être rattachés aux erreurs du référentiel lors de la migration (travail de tagging, pas de génération).

Colonnes : **P** = questions dont c'est la compétence principale · **S** = mentions secondaires · **dont diag** = issues du diagnostic actuel · **Cible** = items atomiques visés (diag + entraînement) · **Manque** = Cible − P.

## NC — Nombres et calculs

| Compétence | Niv. | Poids | P | S | dont diag | Types (P) | Cible | Manque |
|---|---|---|---|---|---|---|---|---|
| `NC.ENT.01` Multiplier ou diviser un décimal par 10, 100, 1000, 0,1, 0,01 🔴 | 6e | 3 | 0 | 2 | 0 | — | 34 | 34 |
| `NC.ENT.02` Comparer et ranger des nombres décimaux 🔴 | 6e | 2 | 0 | 0 | 0 | — | 24 | 24 |
| `NC.ENT.03` Arrondir un nombre ou donner une valeur approchée à la précision demandée 🔴 | 6e | 3 | 0 | 0 | 0 | — | 34 | 34 |
| `NC.PRIO.01` Calculer une expression numérique en respectant les priorités opératoires 🟠 | 5e | 3 | 1 | 0 | 0 | fill:1 | 34 | 33 |
| `NC.REL.01` Repérer, comparer et ranger des nombres relatifs 🔴 | 5e | 2 | 0 | 0 | 0 | — | 24 | 24 |
| `NC.REL.02` Additionner et soustraire des nombres relatifs 🔴 | 5e | 3 | 0 | 0 | 0 | — | 34 | 34 |
| `NC.REL.03` Multiplier et diviser des nombres relatifs 🔴 | 4e | 3 | 0 | 0 | 0 | — | 34 | 34 |
| `NC.ARITH.01` Reconnaître multiples et diviseurs (critères de divisibilité, division euclidienne) | 5e | 2 | 9 | 1 | 0 | fill:3 qcm:2 vf:4 | 24 | 15 |
| `NC.ARITH.02` Reconnaître un nombre premier | 5e | 2 | 3 | 0 | 1 | qcm:2 vf:1 | 24 | 21 |
| `NC.ARITH.03` Décomposer un entier en produit de facteurs premiers | 3e | 2 | 3 | 1 | 0 | fill:1 qcm:2 | 26 | 23 |
| `NC.ARITH.04` Utiliser les diviseurs communs (plus grand diviseur commun) pour résoudre un problème de partage | 3e | 2 | 11 | 1 | 2 | fill:5 qcm:5 vf:1 | 26 | 15 |
| `NC.FRAC.01` Comprendre une fraction comme partage et comme quotient 🔴 | 6e | 2 | 0 | 0 | 0 | — | 24 | 24 |
| `NC.FRAC.02` Reconnaître des fractions égales, simplifier une fraction, la rendre irréductible | 5e | 3 | 3 | 0 | 0 | fill:2 qcm:1 | 34 | 31 |
| `NC.FRAC.03` Additionner et soustraire des fractions (dénominateurs différents) | 4e | 3 | 8 | 0 | 1 | fill:2 qcm:4 vf:2 | 34 | 26 |
| `NC.FRAC.04` Calculer une fraction d'une quantité | 6e | 3 | 8 | 0 | 1 | fill:6 qcm:2 | 34 | 26 |
| `NC.FRAC.05` Multiplier des fractions (y compris « fraction d'une fraction ») | 4e | 2 | 5 | 0 | 1 | fill:3 qcm:2 | 24 | 19 |
| `NC.FRAC.06` Diviser par une fraction | 4e | 2 | 3 | 1 | 0 | qcm:2 vf:1 | 24 | 21 |
| `NC.FRAC.07` Passer d'une écriture à une autre : fraction, décimal, pourcentage 🟠 | 5e | 2 | 1 | 2 | 0 | vf:1 | 24 | 23 |
| `NC.PUIS.01` Calculer le carré, le cube ou une puissance d'un nombre (y compris négatif ou décimal) | 4e | 3 | 3 | 0 | 0 | fill:2 qcm:1 | 34 | 31 |
| `NC.PUIS.02` Comprendre les puissances de 10 d'exposant positif ou négatif | 4e | 2 | 4 | 0 | 0 | fill:1 qcm:3 | 24 | 20 |
| `NC.PUIS.03` Utiliser les règles de calcul sur les puissances (produit, quotient, puissance de puissance) | 3e | 2 | 7 | 0 | 1 | fill:2 qcm:3 vf:2 | 26 | 19 |
| `NC.PUIS.04` Écrire un nombre en notation scientifique (et revenir à l'écriture décimale) | 4e | 2 | 7 | 0 | 1 | fill:3 qcm:2 vf:2 | 24 | 17 |
| `NC.PUIS.05` Calculer et comparer des nombres en notation scientifique | 3e | 2 | 9 | 0 | 1 | fill:3 qcm:5 vf:1 | 26 | 17 |
| `NC.RAC.01` Connaître la racine carrée d'un nombre positif (carrés parfaits, définition) 🟠 | 4e | 3 | 1 | 1 | 0 | fill:1 | 34 | 33 |
| `NC.RAC.02` Calculer un produit ou un quotient de racines carrées (et savoir que √ ne se distribue pas sur +) | 3e | 1 | 9 | 0 | 2 | fill:3 qcm:1 vf:5 | 16 | 7 |
| `NC.RAC.03` Simplifier une racine carrée (écrire sous la forme a√b) | 3e | 1 | 5 | 0 | 1 | fill:2 qcm:3 | 16 | 11 |
| `NC.RAC.04` Réduire ou développer une expression avec des racines carrées, rationaliser un dénominateur | 3e | 1 | 10 | 0 | 0 | fill:4 qcm:5 vf:1 | 16 | 6 |
| `NC.LIT.01` Produire une expression littérale qui traduit une situation ou un programme de calcul | 5e | 3 | 5 | 2 | 1 | fill:3 qcm:2 | 34 | 29 |
| `NC.LIT.02` Calculer la valeur d'une expression littérale pour une valeur donnée | 4e | 3 | 8 | 0 | 0 | fill:2 qcm:3 vf:3 | 34 | 26 |
| `NC.LIT.03` Réduire une expression littérale 🔴 | 4e | 3 | 0 | 1 | 0 | — | 34 | 34 |
| `NC.LIT.04` Développer avec la simple distributivité k(a + b) | 4e | 3 | 9 | 0 | 1 | fill:4 qcm:2 vf:3 | 34 | 25 |
| `NC.LIT.05` Supprimer des parenthèses précédées d'un signe moins 🟠 | 4e | 2 | 1 | 0 | 0 | qcm:1 | 24 | 23 |
| `NC.LIT.06` Développer avec la double distributivité (a + b)(c + d) | 4e | 3 | 3 | 1 | 0 | fill:2 qcm:1 | 34 | 31 |
| `NC.LIT.07` Développer à l'aide des identités remarquables | 3e | 2 | 9 | 3 | 1 | fill:3 qcm:3 vf:3 | 26 | 17 |
| `NC.LIT.08` Factoriser par un facteur commun | 3e | 2 | 5 | 0 | 1 | fill:2 qcm:3 | 26 | 21 |
| `NC.LIT.09` Factoriser à l'aide d'une identité remarquable (a² − b², a² ± 2ab + b²) | 3e | 2 | 6 | 0 | 0 | fill:2 qcm:3 vf:1 | 26 | 20 |
| `NC.LIT.10` Prouver un résultat général à l'aide du calcul littéral | 3e | 3 | 4 | 0 | 0 | fill:1 qcm:2 vf:1 | 36 | 32 |
| `NC.EQUA.01` Tester si un nombre est solution d'une équation ou d'une inéquation | 4e | 2 | 3 | 2 | 0 | vf:3 | 24 | 21 |
| `NC.EQUA.02` Résoudre une équation du type ax + b = c | 4e | 3 | 9 | 0 | 2 | fill:3 qcm:6 | 34 | 25 |
| `NC.EQUA.03` Résoudre une équation du type ax + b = cx + d 🟠 | 4e | 2 | 1 | 0 | 0 | qcm:1 | 24 | 23 |
| `NC.EQUA.04` Mettre un problème en équation et interpréter la solution | 3e | 3 | 5 | 1 | 0 | fill:3 qcm:2 | 36 | 31 |
| `NC.EQUA.05` Résoudre une équation produit nul | 3e | 2 | 5 | 0 | 1 | fill:2 qcm:2 vf:1 | 26 | 21 |
| `NC.EQUA.06` Résoudre une équation du type x² = a 🔴 | 3e | 2 | 0 | 0 | 0 | — | 26 | 26 |
| `NC.INEQ.01` Résoudre une inéquation du premier degré | 3e | 1 | 8 | 0 | 2 | fill:2 qcm:4 vf:2 | 16 | 8 |
| `NC.INEQ.02` Traduire une contrainte (budget, seuil) par une inéquation et interpréter la solution entière | 3e | 2 | 14 | 0 | 1 | fill:4 qcm:7 vf:3 | 26 | 12 |

## DF — Données, fonctions, proportionnalité

| Compétence | Niv. | Poids | P | S | dont diag | Types (P) | Cible | Manque |
|---|---|---|---|---|---|---|---|---|
| `DF.PROP.01` Reconnaître une situation de proportionnalité 🟠 | 5e | 2 | 1 | 0 | 0 | vf:1 | 24 | 23 |
| `DF.PROP.02` Calculer une quatrième proportionnelle (retour à l'unité, coefficient, produit en croix) | 5e | 3 | 7 | 2 | 1 | fill:2 qcm:4 vf:1 | 34 | 27 |
| `DF.PROP.03` Appliquer un pourcentage (calculer x % d'une quantité) 🟠 | 5e | 3 | 1 | 1 | 0 | fill:1 | 34 | 33 |
| `DF.PROP.04` Appliquer une augmentation ou une réduction en pourcentage (coefficient multiplicateur) | 4e | 3 | 5 | 1 | 1 | fill:2 qcm:2 vf:1 | 34 | 29 |
| `DF.PROP.05` Calculer un taux d'évolution en pourcentage | 3e | 2 | 3 | 0 | 1 | qcm:2 vf:1 | 26 | 23 |
| `DF.PROP.06` Enchaîner ou inverser des évolutions en pourcentage | 3e | 2 | 3 | 0 | 0 | fill:2 qcm:1 | 26 | 23 |
| `DF.PROP.07` Utiliser une échelle (plan, carte, maquette) | 5e | 2 | 5 | 0 | 0 | fill:3 qcm:1 vf:1 | 24 | 19 |
| `DF.PROP.08` Partager une quantité selon un ratio donné 🔴 | 3e | 1 | 0 | 0 | 0 | — | 16 | 16 |
| `DF.FONC.01` Calculer l'image d'un nombre par une fonction donnée par une formule ou un tableau | 3e | 3 | 11 | 0 | 2 | fill:9 qcm:2 | 36 | 25 |
| `DF.FONC.02` Lire une image sur une représentation graphique | 3e | 3 | 6 | 0 | 1 | fill:3 qcm:3 | 36 | 30 |
| `DF.FONC.03` Lire un ou des antécédents sur une représentation graphique 🟠 | 3e | 3 | 1 | 0 | 0 | fill:1 | 36 | 35 |
| `DF.FONC.04` Déterminer un antécédent par le calcul (résoudre f(x) = k) | 3e | 2 | 8 | 0 | 1 | fill:2 qcm:2 vf:4 | 26 | 18 |
| `DF.FONC.05` Interpréter une courbe : variations, maximum, intervalle où une condition est vérifiée | 3e | 2 | 5 | 0 | 0 | fill:1 qcm:2 vf:2 | 26 | 21 |
| `DF.AFF.01` Reconnaître une fonction linéaire ou affine (et le lien linéaire ↔ proportionnalité) 🔴 | 3e | 2 | 0 | 0 | 0 | — | 26 | 26 |
| `DF.AFF.02` Interpréter les coefficients a et b d'une fonction affine dans une situation | 3e | 3 | 3 | 0 | 0 | fill:1 qcm:1 vf:1 | 36 | 33 |
| `DF.AFF.03` Déterminer l'expression d'une fonction affine à partir de deux valeurs ou d'un graphique | 3e | 2 | 4 | 0 | 1 | fill:1 qcm:3 | 26 | 22 |
| `DF.AFF.04` Représenter graphiquement une fonction affine et lire a et b sur la droite 🔴 | 3e | 2 | 0 | 0 | 0 | — | 26 | 26 |
| `DF.AFF.05` Comparer deux fonctions affines ou deux offres (point d'intersection, résolution) | 3e | 3 | 9 | 0 | 1 | fill:2 qcm:4 vf:3 | 36 | 27 |
| `DF.STAT.01` Lire et exploiter un tableau ou un diagramme (effectifs, effectif total) | 6e | 3 | 8 | 0 | 0 | fill:7 vf:1 | 34 | 26 |
| `DF.STAT.02` Calculer une fréquence (fraction, décimal, pourcentage) | 5e | 2 | 6 | 0 | 0 | fill:1 qcm:3 vf:2 | 24 | 18 |
| `DF.STAT.03` Calculer une moyenne simple | 5e | 3 | 6 | 0 | 1 | fill:1 qcm:5 | 34 | 28 |
| `DF.STAT.04` Calculer une moyenne pondérée (coefficients ou effectifs) | 4e | 2 | 6 | 0 | 0 | fill:3 qcm:2 vf:1 | 24 | 18 |
| `DF.STAT.05` Déterminer une médiane | 4e | 3 | 5 | 0 | 1 | fill:1 qcm:2 vf:2 | 34 | 29 |
| `DF.STAT.06` Calculer l'étendue d'une série 🟠 | 4e | 2 | 2 | 0 | 0 | fill:1 qcm:1 | 24 | 22 |
| `DF.STAT.07` Comparer et interpréter des séries (indicateurs de position et de dispersion) | 3e | 2 | 6 | 0 | 1 | fill:2 qcm:3 vf:1 | 26 | 20 |
| `DF.PROB.01` Identifier les issues et les événements d'une expérience aléatoire 🔴 | 5e | 2 | 0 | 0 | 0 | — | 24 | 24 |
| `DF.PROB.02` Calculer une probabilité dans une situation d'équiprobabilité | 4e | 3 | 13 | 0 | 1 | fill:4 qcm:5 vf:4 | 34 | 21 |
| `DF.PROB.03` Utiliser l'événement contraire | 4e | 2 | 4 | 0 | 1 | fill:2 qcm:1 vf:1 | 24 | 20 |
| `DF.PROB.04` Calculer la probabilité d'un événement formé de plusieurs issues (« A ou B ») | 4e | 2 | 3 | 0 | 0 | fill:1 qcm:2 | 24 | 21 |
| `DF.PROB.05` Déterminer une probabilité dans une expérience à deux épreuves (arbre, tableau) | 3e | 2 | 4 | 0 | 1 | fill:1 qcm:3 | 26 | 22 |
| `DF.PROB.06` Distinguer fréquence observée et probabilité (hasard sans mémoire, loi des grands nombres) | 3e | 2 | 3 | 0 | 0 | fill:2 qcm:1 | 26 | 23 |

## GM — Grandeurs et mesures

| Compétence | Niv. | Poids | P | S | dont diag | Types (P) | Cible | Manque |
|---|---|---|---|---|---|---|---|---|
| `GM.CONV.01` Convertir des longueurs, des masses et des contenances 🟠 | 6e | 3 | 1 | 0 | 0 | fill:1 | 34 | 33 |
| `GM.CONV.02` Convertir des aires et des volumes (y compris 1 L = 1 dm³) 🟠 | 5e | 2 | 2 | 0 | 0 | fill:1 qcm:1 | 24 | 22 |
| `GM.CONV.03` Convertir des durées (heures-minutes ↔ écriture décimale) 🔴 | 6e | 2 | 0 | 1 | 0 | — | 24 | 24 |
| `GM.AIRE.01` Calculer le périmètre d'un polygone ou d'un cercle 🟠 | 6e | 2 | 2 | 1 | 0 | fill:1 qcm:1 | 24 | 22 |
| `GM.AIRE.02` Calculer l'aire d'un rectangle, d'un triangle, d'une figure composée ou d'une surface latérale | 6e | 3 | 4 | 2 | 0 | fill:3 qcm:1 | 34 | 30 |
| `GM.AIRE.03` Calculer l'aire d'un disque 🔴 | 5e | 2 | 0 | 1 | 0 | — | 24 | 24 |
| `GM.VOL.01` Calculer le volume d'un pavé droit 🟠 | 6e | 2 | 1 | 0 | 0 | qcm:1 | 24 | 23 |
| `GM.VOL.02` Calculer le volume d'un prisme droit ou d'un cylindre | 5e | 3 | 6 | 0 | 1 | fill:2 qcm:2 vf:2 | 34 | 28 |
| `GM.VOL.03` Calculer le volume d'une pyramide ou d'un cône | 4e | 3 | 3 | 0 | 0 | fill:1 qcm:2 | 34 | 31 |
| `GM.VOL.04` Calculer le volume d'une boule 🟠 | 3e | 2 | 2 | 0 | 0 | fill:1 qcm:1 | 26 | 24 |
| `GM.VOL.05` Calculer le volume d'un solide composé 🟠 | 3e | 2 | 2 | 0 | 0 | fill:2 | 26 | 24 |
| `GM.VIT.01` Calculer une vitesse moyenne, une distance ou une durée | 4e | 3 | 4 | 1 | 0 | fill:1 qcm:2 vf:1 | 34 | 30 |
| `GM.VIT.02` Convertir une grandeur composée (km/h ↔ m/s, débit…) 🔴 | 3e | 1 | 0 | 0 | 0 | — | 16 | 16 |
| `GM.AGR.01` Utiliser l'effet d'un agrandissement ou d'une réduction sur les longueurs et les aires (k, k²) | 3e | 2 | 3 | 0 | 0 | qcm:3 | 26 | 23 |
| `GM.AGR.02` Utiliser l'effet d'un agrandissement ou d'une réduction sur les volumes (k³) | 3e | 2 | 3 | 0 | 1 | fill:1 qcm:1 vf:1 | 26 | 23 |

## EG — Espace et géométrie

| Compétence | Niv. | Poids | P | S | dont diag | Types (P) | Cible | Manque |
|---|---|---|---|---|---|---|---|---|
| `EG.REP.01` Lire et placer des points dans un repère du plan (coordonnées relatives) 🟠 | 5e | 3 | 2 | 1 | 0 | fill:1 qcm:1 | 34 | 32 |
| `EG.REP.02` Calculer les coordonnées du milieu d'un segment | 3e | 1 | 3 | 0 | 0 | fill:1 qcm:1 vf:1 | 16 | 13 |
| `EG.REP.03` Se repérer dans un pavé droit ou sur une sphère (latitude, longitude) 🔴 | 3e | 1 | 0 | 0 | 0 | — | 16 | 16 |
| `EG.ANG.01` Utiliser la somme des angles d'un triangle 🟠 | 5e | 2 | 2 | 0 | 0 | fill:2 | 24 | 22 |
| `EG.ANG.02` Utiliser les propriétés des angles des triangles isocèles et équilatéraux 🟠 | 5e | 1 | 1 | 0 | 0 | qcm:1 | 14 | 13 |
| `EG.ANG.03` Utiliser les angles complémentaires, supplémentaires, opposés par le sommet, alternes-internes 🟠 | 5e | 1 | 2 | 0 | 0 | qcm:1 vf:1 | 14 | 12 |
| `EG.PYTH.01` Calculer la longueur de l'hypoténuse avec le théorème de Pythagore | 4e | 3 | 12 | 0 | 1 | fill:3 qcm:7 vf:2 | 34 | 22 |
| `EG.PYTH.02` Calculer la longueur d'un côté de l'angle droit avec le théorème de Pythagore | 4e | 3 | 8 | 0 | 1 | fill:4 qcm:3 vf:1 | 34 | 26 |
| `EG.PYTH.03` Démontrer qu'un triangle est ou n'est pas rectangle (réciproque et contraposée de Pythagore) | 4e | 3 | 6 | 0 | 1 | fill:1 qcm:1 vf:4 | 34 | 28 |
| `EG.THAL.01` Reconnaître une configuration de Thalès et écrire l'égalité des rapports | 4e | 3 | 3 | 0 | 0 | fill:2 qcm:1 | 34 | 31 |
| `EG.THAL.02` Calculer une longueur avec le théorème de Thalès (triangles emboîtés ou papillon) | 3e | 3 | 12 | 0 | 2 | fill:6 qcm:5 vf:1 | 36 | 24 |
| `EG.THAL.03` Démontrer que deux droites sont ou ne sont pas parallèles (réciproque de Thalès) | 3e | 2 | 4 | 0 | 1 | qcm:2 vf:2 | 26 | 22 |
| `EG.SEMB.01` Reconnaître et utiliser des triangles semblables 🟠 | 3e | 1 | 1 | 0 | 0 | vf:1 | 16 | 15 |
| `EG.TRIG.01` Nommer le côté adjacent, le côté opposé et l'hypoténuse relativement à un angle 🟠 | 3e | 3 | 1 | 0 | 0 | vf:1 | 36 | 35 |
| `EG.TRIG.02` Choisir le rapport trigonométrique adapté (cosinus, sinus, tangente) | 3e | 3 | 3 | 0 | 1 | qcm:2 vf:1 | 36 | 33 |
| `EG.TRIG.03` Calculer une longueur avec la trigonométrie | 3e | 3 | 10 | 0 | 1 | fill:6 qcm:3 vf:1 | 36 | 26 |
| `EG.TRIG.04` Calculer la mesure d'un angle avec la trigonométrie | 3e | 2 | 8 | 0 | 1 | fill:3 qcm:4 vf:1 | 26 | 18 |
| `EG.TRANS.01` Construire ou reconnaître l'image d'une figure par une symétrie axiale ou centrale 🔴 | 5e | 1 | 0 | 1 | 0 | — | 14 | 14 |
| `EG.TRANS.02` Déterminer l'image d'un point ou d'une figure par une translation | 4e | 2 | 5 | 0 | 1 | fill:1 qcm:4 | 24 | 19 |
| `EG.TRANS.03` Déterminer l'image d'un point ou d'une figure par une rotation | 4e | 2 | 6 | 0 | 0 | fill:3 qcm:2 vf:1 | 24 | 18 |
| `EG.TRANS.04` Déterminer l'image par une homothétie (rapport positif ou négatif) | 3e | 2 | 6 | 0 | 1 | fill:3 qcm:2 vf:1 | 26 | 20 |
| `EG.TRANS.05` Connaître les propriétés conservées par les transformations | 3e | 2 | 5 | 0 | 1 | fill:2 vf:3 | 26 | 21 |
| `EG.ESP.01` Reconnaître un solide et son patron 🟠 | 6e | 1 | 2 | 0 | 1 | qcm:2 | 14 | 12 |
| `EG.ESP.02` Déterminer la nature d'une section plane (pavé, cylindre, cône, sphère) 🟠 | 3e | 1 | 1 | 0 | 0 | vf:1 | 16 | 15 |

## AP — Algorithmique et programmation

| Compétence | Niv. | Poids | P | S | dont diag | Types (P) | Cible | Manque |
|---|---|---|---|---|---|---|---|---|
| `AP.PROG.01` Exécuter un programme de calcul pour un nombre donné | 5e | 3 | 9 | 0 | 1 | fill:6 qcm:2 vf:1 | 34 | 25 |
| `AP.PROG.02` Lire un script : suite d'instructions et déplacements (orientation, coordonnées) | 5e | 2 | 3 | 0 | 0 | fill:1 qcm:1 vf:1 | 24 | 21 |
| `AP.PROG.03` Comprendre une boucle « répéter n fois » 🟠 | 4e | 3 | 1 | 1 | 0 | fill:1 | 34 | 33 |
| `AP.PROG.04` Suivre l'évolution d'une variable dans un script 🟠 | 4e | 2 | 2 | 0 | 1 | qcm:2 | 24 | 22 |
| `AP.PROG.05` Comprendre une instruction conditionnelle (si… alors… sinon) 🔴 | 4e | 2 | 0 | 0 | 0 | — | 24 | 24 |
| `AP.PROG.06` Déterminer l'angle de rotation et le nombre de répétitions pour tracer un polygone régulier 🔴 | 4e | 2 | 0 | 0 | 0 | — | 24 | 24 |

## Synthèse par domaine

| Domaine | Compétences | Questions (P) | Compétences sans aucune question | Items manquants (cible) |
|---|---|---|---|---|
| NC | 45 | 205 | 9 | 1047 |
| DF | 31 | 138 | 4 | 748 |
| GM | 15 | 33 | 3 | 377 |
| EG | 24 | 103 | 2 | 507 |
| AP | 6 | 15 | 2 | 149 |
| **Total** | 121 | 494 | 20 | **2828** / 3322 |

## 🔴 Trous : compétences sans aucune question (principale)

- `NC.ENT.01` (6EME, poids 3) — Multiplier ou diviser un décimal par 10, 100, 1000, 0,1, 0,01 · 2 mention(s) secondaire(s)
- `NC.ENT.03` (6EME, poids 3) — Arrondir un nombre ou donner une valeur approchée à la précision demandée
- `NC.LIT.03` (4EME, poids 3) — Réduire une expression littérale · 1 mention(s) secondaire(s)
- `NC.REL.02` (5EME, poids 3) — Additionner et soustraire des nombres relatifs
- `NC.REL.03` (4EME, poids 3) — Multiplier et diviser des nombres relatifs
- `AP.PROG.05` (4EME, poids 2) — Comprendre une instruction conditionnelle (si… alors… sinon)
- `AP.PROG.06` (4EME, poids 2) — Déterminer l'angle de rotation et le nombre de répétitions pour tracer un polygone régulier
- `DF.AFF.01` (3EME, poids 2) — Reconnaître une fonction linéaire ou affine (et le lien linéaire ↔ proportionnalité)
- `DF.AFF.04` (3EME, poids 2) — Représenter graphiquement une fonction affine et lire a et b sur la droite
- `DF.PROB.01` (5EME, poids 2) — Identifier les issues et les événements d'une expérience aléatoire
- `GM.AIRE.03` (5EME, poids 2) — Calculer l'aire d'un disque · 1 mention(s) secondaire(s)
- `GM.CONV.03` (6EME, poids 2) — Convertir des durées (heures-minutes ↔ écriture décimale) · 1 mention(s) secondaire(s)
- `NC.ENT.02` (6EME, poids 2) — Comparer et ranger des nombres décimaux
- `NC.EQUA.06` (3EME, poids 2) — Résoudre une équation du type x² = a
- `NC.FRAC.01` (6EME, poids 2) — Comprendre une fraction comme partage et comme quotient
- `NC.REL.01` (5EME, poids 2) — Repérer, comparer et ranger des nombres relatifs
- `DF.PROP.08` (3EME, poids 1) — Partager une quantité selon un ratio donné
- `EG.REP.03` (3EME, poids 1) — Se repérer dans un pavé droit ou sur une sphère (latitude, longitude)
- `EG.TRANS.01` (5EME, poids 1) — Construire ou reconnaître l'image d'une figure par une symétrie axiale ou centrale · 1 mention(s) secondaire(s)
- `GM.VIT.02` (3EME, poids 1) — Convertir une grandeur composée (km/h ↔ m/s, débit…)

## 🟠 Couverture faible (1-2 questions)

- `AP.PROG.03` (4EME, poids 3) — Comprendre une boucle « répéter n fois » : 1
- `DF.FONC.03` (3EME, poids 3) — Lire un ou des antécédents sur une représentation graphique : 1
- `DF.PROP.03` (5EME, poids 3) — Appliquer un pourcentage (calculer x % d'une quantité) : 1
- `EG.REP.01` (5EME, poids 3) — Lire et placer des points dans un repère du plan (coordonnées relatives) : 2
- `EG.TRIG.01` (3EME, poids 3) — Nommer le côté adjacent, le côté opposé et l'hypoténuse relativement à un angle : 1
- `GM.CONV.01` (6EME, poids 3) — Convertir des longueurs, des masses et des contenances : 1
- `NC.PRIO.01` (5EME, poids 3) — Calculer une expression numérique en respectant les priorités opératoires : 1
- `NC.RAC.01` (4EME, poids 3) — Connaître la racine carrée d'un nombre positif (carrés parfaits, définition) : 1
- `AP.PROG.04` (4EME, poids 2) — Suivre l'évolution d'une variable dans un script : 2
- `DF.PROP.01` (5EME, poids 2) — Reconnaître une situation de proportionnalité : 1
- `DF.STAT.06` (4EME, poids 2) — Calculer l'étendue d'une série : 2
- `EG.ANG.01` (5EME, poids 2) — Utiliser la somme des angles d'un triangle : 2
- `GM.AIRE.01` (6EME, poids 2) — Calculer le périmètre d'un polygone ou d'un cercle : 2
- `GM.CONV.02` (5EME, poids 2) — Convertir des aires et des volumes (y compris 1 L = 1 dm³) : 2
- `GM.VOL.01` (6EME, poids 2) — Calculer le volume d'un pavé droit : 1
- `GM.VOL.04` (3EME, poids 2) — Calculer le volume d'une boule : 2
- `GM.VOL.05` (3EME, poids 2) — Calculer le volume d'un solide composé : 2
- `NC.EQUA.03` (4EME, poids 2) — Résoudre une équation du type ax + b = cx + d : 1
- `NC.FRAC.07` (5EME, poids 2) — Passer d'une écriture à une autre : fraction, décimal, pourcentage : 1
- `NC.LIT.05` (4EME, poids 2) — Supprimer des parenthèses précédées d'un signe moins : 1
- `EG.ANG.02` (5EME, poids 1) — Utiliser les propriétés des angles des triangles isocèles et équilatéraux : 1
- `EG.ANG.03` (5EME, poids 1) — Utiliser les angles complémentaires, supplémentaires, opposés par le sommet, alternes-internes : 2
- `EG.ESP.01` (6EME, poids 1) — Reconnaître un solide et son patron : 2
- `EG.ESP.02` (3EME, poids 1) — Déterminer la nature d'une section plane (pavé, cylindre, cône, sphère) : 1
- `EG.SEMB.01` (3EME, poids 1) — Reconnaître et utiliser des triangles semblables : 1

## Lecture pour le dimensionnement

- Les **37 compétences de socle 6e/5e** (celles qui portent la plupart des causes racines) ne totalisent que **101 questions** principales, et **10 n'en ont aucune** : la banque actuelle est construite par chapitre Brevet, elle mesure le symptôme mais ne permet pas de remonter à la cause. C'est le premier chantier de génération (items courts, `usage: ["diag"]`).
- **Diagnostic** : ≈ **582 items atomiques calibrés** à produire (49 compétences 3e × 6 + 72 prérequis × 4). Seules les 54 questions de `diagnostic_3eme.json` sont réutilisables telles quelles, après ajout de `comp` et `err`.
- Les questions v4 sont des sous-questions de problèmes contextualisés : elles restent précieuses comme **problèmes Brevet** (usage `train`), mais sont trop dépendantes du contexte pour le diagnostic (une erreur à la question 4 peut venir de la question 2).
- Volume cible total ≈ **3322 items**, dont **≈ 2828 à produire** (hypothèse : 6 items diag par compétence 3e, 4 par prérequis ; 30/20/10 items d'entraînement selon le poids).
- Priorité de génération suggérée : (1) items diag des prérequis à poids 3 (relatifs, priorités, fractions, carrés/racines, proportionnalité, conversions) ; (2) items diag des compétences 3e à poids 3 ; (3) tagging `err` des distracteurs existants ; (4) entraînement.
