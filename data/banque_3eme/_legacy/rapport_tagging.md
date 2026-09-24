# Banque legacy taggée — rapport de conversion

> Concepteur d'items · 24/09/2026 · branche `feat/diagnostic-3e`. Conversion **sans génération** de la banque existante
> au format item atomique (contrat §3), `usage: ["train"]`. Rien n'est importé en base.
> Vérification : `python3 data/banque_3eme/_legacy/check_legacy.py` (comp, ids d'erreur, appartenance erreur↔compétence, unicité des ids, y compris contre les fichiers `<DOM>.<THEME>.json`) → ✅.
> `validate_exos.py` : 32 fichiers sur 39 passent. Les 7 bloqués (Arithmetique, Auto_Stats_Probas, Calcul_Litteral, Pythagore, Racines_Carrees, Transformations, diagnostic_3eme) le sont par des erreurs **héritées des sources, à l'identique** (Unicode mêlé au LaTeX, un step jugé générique, un `\times` hors `$`), listées en § LaTeX. Non corrigées, conformément à la consigne.

## Chiffres clés

| | Valeur |
|---|---|
| Questions lues | 814 (440 v4 + 54 diagnostic + 320 banques 6e/5e/4e) |
| Items convertis | **779** |
| Items écartés | 35 (voir § Items écartés) |
| Compétences couvertes | 106 / 121 |
| Rattachements `err` | 448 |
| Distracteurs QCM rattachés à une erreur type | **176 / 634 = 28 %** (317 QCM) |
| VF dont la mauvaise réponse est rattachée | 33 / 152 = 22 % |
| Fill avec au moins une mauvaise réponse prévisible rattachée | 184 / 310 = 59 % |
| Items préfixés par le contexte du parapluie (`contexte: true`) | 215 |
| Items marqués `depend_question_precedente: true` | 8 |

Le taux de rattachement est volontairement bas : un distracteur n'est rattaché que si l'erreur type est **évidente** et appartient à la compétence de l'item. Les distracteurs « au hasard » (ex. 16 et 20 pour 18) ou relevant d'une autre compétence (ex. `x(x+8) = 52` dans une mise en équation → confusion périmètre/aire, `GM.AIRE.01`) restent sans `err`. Conséquence : sur ces items, une mauvaise réponse compte comme échec sans nommer d'erreur.

## Fichiers

Un fichier par source, même nom, sous `data/banque_3eme/_legacy/` (les banques par niveau gardent leur sous-dossier : `bank_6eme/`, `bank_5eme/`, `bank_4eme/`).

| Source | Lues | Converties |
|---|---|---|
| `Arithmetique_Brevet_v4.json` | 20 | 19 |
| `Calcul_Litteral_Brevet_v4.json` | 20 | 20 |
| `Equations_Brevet_v4.json` | 20 | 20 |
| `Fonctions_Affines_Brevet_v4.json` | 20 | 20 |
| `Fonctions_Brevet_v4.json` | 20 | 19 |
| `Fractions_Brevet_v4.json` | 20 | 20 |
| `Geometrie_Espace_Brevet_v4.json` | 20 | 19 |
| `Inequations_Brevet_v4.json` | 20 | 19 |
| `Probabilites_Brevet_v4.json` | 20 | 20 |
| `Proportionnalite_Brevet_v4.json` | 20 | 20 |
| `Puissances_Brevet_v4.json` | 20 | 20 |
| `Pythagore_Brevet_v4.json` | 20 | 20 |
| `Racines_Carrees_Brevet_v4.json` | 20 | 19 |
| `Scratch_Brevet_v4.json` | 20 | 18 |
| `Statistiques_Brevet_v4.json` | 20 | 20 |
| `Thales_Brevet_v4.json` | 20 | 20 |
| `Transformations_Brevet_v4.json` | 20 | 18 |
| `Trigonometrie_Brevet_v4.json` | 20 | 20 |
| `Auto_Calcul_v4.json` | 20 | 20 |
| `Auto_Geometrie_v4.json` | 20 | 20 |
| `Auto_Litteral_v4.json` | 20 | 20 |
| `Auto_Stats_Probas_v4.json` | 20 | 20 |
| `diagnostic_3eme.json` | 54 | 52 |
| `bank_4eme/Calcul_Littéral.json` | 20 | 19 |
| `bank_4eme/Fractions.json` | 20 | 20 |
| `bank_4eme/Proportionnalité.json` | 20 | 20 |
| `bank_4eme/Puissances.json` | 20 | 20 |
| `bank_4eme/Équations.json` | 20 | 20 |
| `bank_5eme/Calcul_Littéral.json` | 20 | 20 |
| `bank_5eme/Fractions.json` | 20 | 20 |
| `bank_5eme/Nombres_relatifs.json` | 20 | 20 |
| `bank_5eme/Proportionnalité.json` | 20 | 20 |
| `bank_5eme/Pythagore.json` | 20 | 20 |
| `bank_6eme/Angles.json` | 20 | 15 |
| `bank_6eme/Fractions.json` | 20 | 20 |
| `bank_6eme/Géométrie.json` | 20 | 2 |
| `bank_6eme/Nombres_entiers.json` | 20 | 20 |
| `bank_6eme/Proportionnalité.json` | 20 | 20 |
| `bank_6eme/Périmètres_Aires.json` | 20 | 20 |

### Format

- Champs du contrat : `id` (`<COMP>-L<nnn>`), `comp`, `q`, `a`, `type`, `options`, `err`, `steps`, `f`, `lvl`, `usage`, `contexte`.
- Conservés tels quels : `q`, `a`, `type`, `options`, `steps`, `f`, `f_disabled`, `lvl`, `table`, `draw`, `figure` (+ `figure_desc` du parapluie).
- Traçabilité : `source` (`<fichier>|<PARAPLUIE>.<num>`, ou `diagnostic_3eme|<index>`), `parapluie_id` + `num` (reconstitution des problèmes Brevet dans l'ordre), `comp_secondaires` (repris de `mapping_legacy.json`).
- `contexte: true` : `q` = contexte du parapluie + « » + question d'origine. Appliqué seulement quand la question est incompréhensible seule (données, fonction ou figure définies dans le contexte). Dans ce cas, le tableau du parapluie (ou celui d'une sous-question sœur) est recopié dans `table`.
- `depend_question_precedente: true` (champ ajouté, hors contrat) : la question utilise un résultat de la question précédente qui n'est ni dans son énoncé ni dans le contexte. **À ne servir qu'en problème complet**, jamais en item isolé. Le moteur doit filtrer ce champ.
- `err` des fill : clé = mauvaise réponse brute (même écriture que `a`, sans `$`). Le moteur doit la comparer après `_normFill()`, comme la bonne réponse.
- Normalisations de format (pas de changement de contenu) : `type: "qcm"` ajouté sur 5 questions du diagnostic qui n'avaient pas de `type` ; `options: ["Vrai", "Faux"]` ajouté sur 5 VF du diagnostic qui avaient `options: []` (index 17, 22, 26, 29, 34).

## Items par compétence

Colonnes : **N** items · **QCM distr.** = distracteurs rattachés / total · **VF** = VF rattachés / total · **Fill** = fill avec ≥ 1 `err` / total · **Erreurs vues** = erreurs types distinctes présentes / erreurs du référentiel.

| Compétence | Niv. | N | QCM distr. | VF | Fill | Erreurs vues |
|---|---|---|---|---|---|---|
| `NC.PRIO.01` Calculer une expression numérique en respectant les priorité | 5e | 6 | 2/6 | 1/1 | 2/2 | 1/3 |
| `NC.REL.01` Repérer, comparer et ranger des nombres relatifs | 5e | 3 | 2/4 | 1/1 | 0/0 | 1/2 |
| `NC.REL.02` Additionner et soustraire des nombres relatifs | 5e | 12 | 5/10 | 0/2 | 5/5 | 2/3 |
| `NC.REL.03` Multiplier et diviser des nombres relatifs | 4e | 5 | 1/2 | 0/1 | 0/3 | 1/2 |
| `NC.ARITH.01` Reconnaître multiples et diviseurs (critères de divisibilité | 5e | 22 | 0/14 | 0/7 | 3/8 | 1/3 |
| `NC.ARITH.02` Reconnaître un nombre premier | 5e | 3 | 2/4 | 1/1 | 0/0 | 2/3 |
| `NC.ARITH.03` Décomposer un entier en produit de facteurs premiers | 3e | 3 | 4/4 | 0/0 | 1/1 | 2/3 |
| `NC.ARITH.04` Utiliser les diviseurs communs (plus grand diviseur commun)  | 3e | 11 | 0/10 | 0/1 | 3/5 | 1/3 |
| `NC.FRAC.01` Comprendre une fraction comme partage et comme quotient | 6e | 11 | 0/10 | 0/3 | 0/3 | 0/2 |
| `NC.FRAC.02` Reconnaître des fractions égales, simplifier une fraction, l | 5e | 6 | 1/2 | 0/2 | 2/3 | 1/3 |
| `NC.FRAC.03` Additionner et soustraire des fractions (dénominateurs diffé | 4e | 23 | 8/20 | 1/3 | 8/10 | 1/3 |
| `NC.FRAC.04` Calculer une fraction d'une quantité | 6e | 21 | 5/16 | 0/2 | 5/11 | 2/2 |
| `NC.FRAC.05` Multiplier des fractions (y compris « fraction d'une fractio | 4e | 16 | 7/12 | 2/3 | 4/7 | 3/3 |
| `NC.FRAC.06` Diviser par une fraction | 4e | 9 | 2/8 | 2/2 | 3/3 | 1/3 |
| `NC.FRAC.07` Passer d'une écriture à une autre : fraction, décimal, pourc | 5e | 1 | 0/0 | 0/1 | 0/0 | 0/2 |
| `NC.PUIS.01` Calculer le carré, le cube ou une puissance d'un nombre (y c | 4e | 10 | 2/6 | 0/1 | 6/6 | 2/4 |
| `NC.PUIS.02` Comprendre les puissances de 10 d'exposant positif ou négati | 4e | 9 | 7/10 | 0/1 | 3/3 | 2/2 |
| `NC.PUIS.03` Utiliser les règles de calcul sur les puissances (produit, q | 3e | 17 | 4/14 | 1/4 | 4/6 | 3/4 |
| `NC.PUIS.04` Écrire un nombre en notation scientifique (et revenir à l'éc | 4e | 7 | 4/4 | 1/2 | 3/3 | 3/3 |
| `NC.PUIS.05` Calculer et comparer des nombres en notation scientifique | 3e | 9 | 3/10 | 1/1 | 0/3 | 3/3 |
| `NC.RAC.01` Connaître la racine carrée d'un nombre positif (carrés parfa | 4e | 1 | 0/0 | 0/0 | 1/1 | 1/3 |
| `NC.RAC.02` Calculer un produit ou un quotient de racines carrées (et sa | 3e | 8 | 0/2 | 2/4 | 3/3 | 3/3 |
| `NC.RAC.03` Simplifier une racine carrée (écrire sous la forme a√b) | 3e | 5 | 1/6 | 0/0 | 2/2 | 2/2 |
| `NC.RAC.04` Réduire ou développer une expression avec des racines carrée | 3e | 10 | 6/10 | 0/1 | 1/4 | 3/3 |
| `NC.LIT.01` Produire une expression littérale qui traduit une situation  | 5e | 5 | 1/4 | 0/0 | 0/3 | 1/3 |
| `NC.LIT.02` Calculer la valeur d'une expression littérale pour une valeu | 4e | 20 | 1/20 | 1/3 | 4/7 | 2/3 |
| `NC.LIT.03` Réduire une expression littérale | 4e | 10 | 6/6 | 1/2 | 4/5 | 3/3 |
| `NC.LIT.04` Développer avec la simple distributivité k(a + b) | 4e | 19 | 6/12 | 4/5 | 8/8 | 2/2 |
| `NC.LIT.05` Supprimer des parenthèses précédées d'un signe moins | 4e | 2 | 1/4 | 0/0 | 0/0 | 1/2 |
| `NC.LIT.06` Développer avec la double distributivité (a + b)(c + d) | 4e | 8 | 3/6 | 1/1 | 4/4 | 3/3 |
| `NC.LIT.07` Développer à l'aide des identités remarquables | 3e | 9 | 2/6 | 2/3 | 3/3 | 3/3 |
| `NC.LIT.08` Factoriser par un facteur commun | 3e | 5 | 2/6 | 0/0 | 2/2 | 1/3 |
| `NC.LIT.09` Factoriser à l'aide d'une identité remarquable (a² − b², a²  | 3e | 6 | 1/6 | 0/1 | 1/2 | 2/3 |
| `NC.LIT.10` Prouver un résultat général à l'aide du calcul littéral | 3e | 3 | 0/2 | 1/1 | 0/1 | 1/2 |
| `NC.EQUA.01` Tester si un nombre est solution d'une équation ou d'une iné | 4e | 2 | 0/0 | 0/2 | 0/0 | 0/2 |
| `NC.EQUA.02` Résoudre une équation du type ax + b = c | 4e | 19 | 5/20 | 1/2 | 7/7 | 4/4 |
| `NC.EQUA.03` Résoudre une équation du type ax + b = cx + d | 4e | 6 | 0/4 | 0/1 | 2/3 | 1/2 |
| `NC.EQUA.04` Mettre un problème en équation et interpréter la solution | 3e | 11 | 0/12 | 0/1 | 1/4 | 1/3 |
| `NC.EQUA.05` Résoudre une équation produit nul | 3e | 5 | 1/4 | 0/1 | 1/2 | 2/3 |
| `NC.INEQ.01` Résoudre une inéquation du premier degré | 3e | 7 | 0/8 | 0/2 | 0/1 | 0/3 |
| `NC.INEQ.02` Traduire une contrainte (budget, seuil) par une inéquation e | 3e | 15 | 1/14 | 0/3 | 2/5 | 1/2 |
| `DF.PROP.01` Reconnaître une situation de proportionnalité | 5e | 6 | 1/4 | 1/4 | 0/0 | 2/2 |
| `DF.PROP.02` Calculer une quatrième proportionnelle (retour à l'unité, co | 5e | 25 | 5/22 | 0/3 | 6/11 | 2/3 |
| `DF.PROP.03` Appliquer un pourcentage (calculer x % d'une quantité) | 5e | 5 | 0/2 | 0/1 | 3/3 | 2/2 |
| `DF.PROP.04` Appliquer une augmentation ou une réduction en pourcentage ( | 4e | 9 | 2/8 | 0/1 | 2/4 | 2/2 |
| `DF.PROP.05` Calculer un taux d'évolution en pourcentage | 3e | 4 | 3/6 | 0/1 | 0/0 | 2/2 |
| `DF.PROP.06` Enchaîner ou inverser des évolutions en pourcentage | 3e | 7 | 2/4 | 2/2 | 2/3 | 2/2 |
| `DF.PROP.07` Utiliser une échelle (plan, carte, maquette) | 5e | 20 | 1/14 | 0/4 | 8/9 | 2/2 |
| `DF.FONC.01` Calculer l'image d'un nombre par une fonction donnée par une | 3e | 13 | 0/6 | 0/0 | 0/10 | 0/2 |
| `DF.FONC.02` Lire une image sur une représentation graphique | 3e | 4 | 0/4 | 0/0 | 0/2 | 0/2 |
| `DF.FONC.03` Lire un ou des antécédents sur une représentation graphique | 3e | 1 | 0/0 | 0/0 | 0/1 | 0/2 |
| `DF.FONC.04` Déterminer un antécédent par le calcul (résoudre f(x) = k) | 3e | 8 | 0/4 | 0/4 | 1/2 | 1/2 |
| `DF.FONC.05` Interpréter une courbe : variations, maximum, intervalle où  | 3e | 4 | 0/2 | 0/2 | 0/1 | 0/3 |
| `DF.AFF.02` Interpréter les coefficients a et b d'une fonction affine da | 3e | 5 | 3/6 | 0/1 | 0/1 | 1/2 |
| `DF.AFF.03` Déterminer l'expression d'une fonction affine à partir de de | 3e | 2 | 0/2 | 0/0 | 1/1 | 1/3 |
| `DF.AFF.05` Comparer deux fonctions affines ou deux offres (point d'inte | 3e | 10 | 1/8 | 1/4 | 1/2 | 2/2 |
| `DF.STAT.01` Lire et exploiter un tableau ou un diagramme (effectifs, eff | 6e | 8 | 0/0 | 0/1 | 1/7 | 1/2 |
| `DF.STAT.02` Calculer une fréquence (fraction, décimal, pourcentage) | 5e | 6 | 2/6 | 0/2 | 1/1 | 1/2 |
| `DF.STAT.03` Calculer une moyenne simple | 5e | 4 | 0/8 | 0/0 | 0/0 | 0/3 |
| `DF.STAT.04` Calculer une moyenne pondérée (coefficients ou effectifs) | 4e | 8 | 1/6 | 0/1 | 2/4 | 1/2 |
| `DF.STAT.05` Déterminer une médiane | 4e | 5 | 1/4 | 0/2 | 0/1 | 1/4 |
| `DF.STAT.06` Calculer l'étendue d'une série | 4e | 2 | 0/2 | 0/0 | 1/1 | 2/2 |
| `DF.STAT.07` Comparer et interpréter des séries (indicateurs de position  | 3e | 5 | 1/4 | 1/1 | 0/2 | 2/3 |
| `DF.PROB.02` Calculer une probabilité dans une situation d'équiprobabilit | 4e | 13 | 5/10 | 0/4 | 3/4 | 3/3 |
| `DF.PROB.03` Utiliser l'événement contraire | 4e | 4 | 1/2 | 0/1 | 2/2 | 1/2 |
| `DF.PROB.04` Calculer la probabilité d'un événement formé de plusieurs is | 4e | 3 | 2/4 | 0/0 | 0/1 | 1/2 |
| `DF.PROB.05` Déterminer une probabilité dans une expérience à deux épreuv | 3e | 4 | 2/6 | 0/0 | 1/1 | 2/3 |
| `DF.PROB.06` Distinguer fréquence observée et probabilité (hasard sans mé | 3e | 3 | 1/2 | 0/0 | 1/2 | 2/2 |
| `GM.CONV.01` Convertir des longueurs, des masses et des contenances | 6e | 1 | 0/0 | 0/0 | 1/1 | 2/2 |
| `GM.CONV.02` Convertir des aires et des volumes (y compris 1 L = 1 dm³) | 5e | 2 | 0/2 | 0/0 | 1/1 | 1/2 |
| `GM.AIRE.01` Calculer le périmètre d'un polygone ou d'un cercle | 6e | 13 | 5/10 | 1/2 | 4/6 | 3/3 |
| `GM.AIRE.02` Calculer l'aire d'un rectangle, d'un triangle, d'une figure  | 6e | 16 | 1/10 | 0/2 | 6/9 | 1/3 |
| `GM.VOL.01` Calculer le volume d'un pavé droit | 6e | 1 | 1/2 | 0/0 | 0/0 | 1/2 |
| `GM.VOL.02` Calculer le volume d'un prisme droit ou d'un cylindre | 5e | 5 | 2/2 | 0/2 | 2/2 | 3/3 |
| `GM.VOL.03` Calculer le volume d'une pyramide ou d'un cône | 4e | 3 | 2/4 | 0/0 | 1/1 | 1/2 |
| `GM.VOL.04` Calculer le volume d'une boule | 3e | 2 | 1/2 | 0/0 | 1/1 | 2/2 |
| `GM.VOL.05` Calculer le volume d'un solide composé | 3e | 2 | 0/0 | 0/0 | 0/2 | 0/2 |
| `GM.VIT.01` Calculer une vitesse moyenne, une distance ou une durée | 4e | 14 | 0/12 | 0/3 | 3/5 | 2/3 |
| `GM.AGR.01` Utiliser l'effet d'un agrandissement ou d'une réduction sur  | 3e | 3 | 3/6 | 0/0 | 0/0 | 1/2 |
| `GM.AGR.02` Utiliser l'effet d'un agrandissement ou d'une réduction sur  | 3e | 3 | 0/2 | 1/1 | 1/1 | 2/2 |
| `EG.REP.01` Lire et placer des points dans un repère du plan (coordonnée | 5e | 2 | 0/2 | 0/0 | 1/1 | 1/2 |
| `EG.REP.02` Calculer les coordonnées du milieu d'un segment | 3e | 3 | 0/2 | 0/1 | 1/1 | 2/2 |
| `EG.ANG.01` Utiliser la somme des angles d'un triangle | 5e | 4 | 0/2 | 0/0 | 3/3 | 2/2 |
| `EG.ANG.02` Utiliser les propriétés des angles des triangles isocèles et | 5e | 2 | 1/2 | 0/0 | 0/1 | 1/2 |
| `EG.ANG.03` Utiliser les angles complémentaires, supplémentaires, opposé | 5e | 12 | 3/8 | 0/4 | 1/4 | 1/2 |
| `EG.PYTH.01` Calculer la longueur de l'hypoténuse avec le théorème de Pyt | 4e | 20 | 10/20 | 0/4 | 6/6 | 2/4 |
| `EG.PYTH.02` Calculer la longueur d'un côté de l'angle droit avec le théo | 4e | 13 | 3/10 | 0/2 | 6/6 | 1/2 |
| `EG.PYTH.03` Démontrer qu'un triangle est ou n'est pas rectangle (récipro | 4e | 10 | 0/8 | 0/5 | 0/1 | 0/3 |
| `EG.THAL.01` Reconnaître une configuration de Thalès et écrire l'égalité  | 4e | 3 | 2/2 | 0/0 | 0/2 | 2/3 |
| `EG.THAL.02` Calculer une longueur avec le théorème de Thalès (triangles  | 3e | 12 | 1/10 | 0/1 | 4/6 | 2/3 |
| `EG.THAL.03` Démontrer que deux droites sont ou ne sont pas parallèles (r | 3e | 4 | 0/4 | 0/2 | 0/0 | 0/3 |
| `EG.SEMB.01` Reconnaître et utiliser des triangles semblables | 3e | 1 | 0/0 | 0/1 | 0/0 | 0/2 |
| `EG.TRIG.01` Nommer le côté adjacent, le côté opposé et l'hypoténuse rela | 3e | 1 | 0/0 | 1/1 | 0/0 | 1/2 |
| `EG.TRIG.02` Choisir le rapport trigonométrique adapté (cosinus, sinus, t | 3e | 3 | 4/4 | 0/1 | 0/0 | 1/2 |
| `EG.TRIG.03` Calculer une longueur avec la trigonométrie | 3e | 10 | 1/6 | 0/1 | 3/6 | 1/2 |
| `EG.TRIG.04` Calculer la mesure d'un angle avec la trigonométrie | 3e | 8 | 0/8 | 1/1 | 0/3 | 1/2 |
| `EG.TRANS.02` Déterminer l'image d'un point ou d'une figure par une transl | 4e | 5 | 3/8 | 0/0 | 1/1 | 2/2 |
| `EG.TRANS.03` Déterminer l'image d'un point ou d'une figure par une rotati | 4e | 6 | 0/4 | 0/1 | 1/3 | 1/2 |
| `EG.TRANS.04` Déterminer l'image par une homothétie (rapport positif ou né | 3e | 5 | 0/4 | 0/0 | 1/3 | 1/3 |
| `EG.TRANS.05` Connaître les propriétés conservées par les transformations | 3e | 4 | 0/0 | 0/3 | 0/1 | 0/2 |
| `EG.ESP.01` Reconnaître un solide et son patron | 6e | 2 | 0/4 | 0/0 | 0/0 | 0/2 |
| `EG.ESP.02` Déterminer la nature d'une section plane (pavé, cylindre, cô | 3e | 1 | 0/0 | 0/1 | 0/0 | 0/2 |
| `AP.PROG.01` Exécuter un programme de calcul pour un nombre donné | 5e | 9 | 0/4 | 0/1 | 1/6 | 1/2 |
| `AP.PROG.02` Lire un script : suite d'instructions et déplacements (orien | 5e | 3 | 1/2 | 0/1 | 1/1 | 2/2 |
| `AP.PROG.03` Comprendre une boucle « répéter n fois » | 4e | 2 | 2/2 | 0/0 | 0/1 | 1/2 |
| `AP.PROG.04` Suivre l'évolution d'une variable dans un script | 4e | 1 | 0/2 | 0/0 | 0/0 | 0/2 |

**15 compétences sans aucun item legacy** : `NC.ENT.01`, `NC.ENT.02`, `NC.ENT.03`, `NC.EQUA.06`, `DF.PROP.08`, `DF.AFF.01`, `DF.AFF.04`, `DF.PROB.01`, `GM.CONV.03`, `GM.AIRE.03`, `GM.VIT.02`, `EG.REP.03`, `EG.TRANS.01`, `AP.PROG.05`, `AP.PROG.06`.

## Corrections du mapping didacticien

| Source | Mapping | Corrigé en | Pourquoi |
|---|---|---|---|
| `Equations_Brevet_v4|EQ_01.3` | `NC.EQUA.01` | `NC.EQUA.04` | Interpréter la solution (Noé = 2x = 20), pas tester une solution. |
| `Fonctions_Affines_Brevet_v4|FONC_AFF_02.2` | `DF.AFF.03` | `DF.AFF.02` | La question porte sur le sens du coefficient (débit vs volume initial), pas sur son calcul. |
| `Fonctions_Affines_Brevet_v4|FONC_AFF_03.2` | `DF.AFF.03` | `DF.AFF.02` | Idem : les distracteurs testent l'interprétation de a et b (commission prise pour a). |
| `Fonctions_Brevet_v4|FONC_03.1` | `DF.FONC.02` | `DF.FONC.01` | Lecture dans un tableau de valeurs (DF.FONC.01 couvre « formule ou tableau »), pas sur une courbe. |
| `Fonctions_Brevet_v4|FONC_03.2` | `DF.FONC.02` | `DF.FONC.01` | Idem : image lue dans un tableau. |
| `Inequations_Brevet_v4|INEQ_04.4` | `NC.INEQ.01` | `NC.INEQ.02` | Seuil en contexte avec solution entière (81,25 → 82) : c'est l'interprétation entière qui est évaluée. |
| `Scratch_Brevet_v4|SCRATCH_03.4` | `AP.PROG.04` | `AP.PROG.03` | n compte les tours de boucle : la question évalue le nombre de répétitions (distracteurs 3 et 5 = un tour de trop / de moins). |
| `Statistiques_Brevet_v4|STAT_04.1` | `DF.STAT.03` | `DF.STAT.04` | Moyenne à partir d'un tableau d'effectifs = moyenne pondérée par les effectifs. |
| `Statistiques_Brevet_v4|STAT_04.2` | `DF.STAT.03` | `DF.STAT.04` | Idem. |

Banques 6e/5e/4e (non mappées par le didacticien) : rattachement fait ici, question par question. Quelques choix à relire : les additions de fractions **de même dénominateur** (6e/5e) sont rangées en `NC.FRAC.03` (seule compétence d'addition, erreur `somme_directe` pertinente) ; « `2x` avec `x = 30` » et équivalents en `NC.LIT.02` ; « si je double x, le périmètre `2x + 10` double-t-il ? » en `DF.PROP.01#partie_fixe`.

## Items écartés

### Bugs bloquants (10) — écartés tant que non corrigés à la source

- `Arithmetique_Brevet_v4|ARITH_01.5` — Réponse non unique : 14, 21, 28, 42 et 84 divisent aussi 84 et dépassent 10 ; « la seule taille possible » = 12 est faux.
- `Fonctions_Brevet_v4|FONC_02.4` — Réponse douteuse : d'après les points de la figure, T ≥ 20 °C jusque vers 19 h 20, pas « de 12 h à 18 h ».
- `Geometrie_Espace_Brevet_v4|GEOESP_01.5` — Réponse fausse : des boules de rayon 3 cm (diamètre 6 cm) dans un cylindre de 12 cm de haut → 2 boules, pas 3.
- `Racines_Carrees_Brevet_v4|RAC_01.5` — Réponse fausse : √9 + √16 = 3 + 4 = 7 ≠ √25 = 5, la bonne réponse est « Faux » (le fichier dit « Vrai »). Écarté tant que non corrigé.
- `Scratch_Brevet_v4|SCRATCH_02.4` — Réponse incohérente : la question demande si le résultat est toujours impair, la réponse attendue est « 2x + 7 » alors que l'option « 2(x + 3) + 1 » est celle qui prouve l'imparité (et seulement pour x entier, non précisé).
- `Scratch_Brevet_v4|SCRATCH_04.4` — VF sans affirmation (« Développe l'expression… pour prouver la conjecture ») : « Vrai » n'a pas de sens.
- `Transformations_Brevet_v4|TRANSF_03.5` — Bonne réponse discutable : une homothétie de rapport négatif est une similitude directe (elle conserve l'orientation au sens mathématique) ; « Faux » n'est juste que si « orientation » veut dire « la figure n'est pas retournée ».
- `Transformations_Brevet_v4|TRANSF_04.5` — Fill à réponse textuelle libre (« L'homothétie de rapport k ≠ 1 ») non comparable par _normFill, question sans liste de choix, et réponse inexacte (k = −1 conserve les longueurs).
- `diagnostic_3eme|5` — Les deux distracteurs sont égaux à la bonne réponse ($\frac{21}{126} = \frac{7}{42} = \frac{1}{6}$) : un élève qui calcule juste sans simplifier est compté faux.
- `diagnostic_3eme|47` — Réponse fausse selon la convention française (Q1 = plus petite valeur couvrant 25 % des effectifs = 2e valeur = 6, pas 7) et quartiles hors programme collège.

### N'évaluent aucune compétence du référentiel (25)

- Addition triviale 350 + 200 (mappée NC.PRIO.01 sans priorité opératoire) : n'évalue aucune compétence du référentiel. (1) : `Inequations_Brevet_v4|INEQ_04.1`
- Affirmation d'opinion (« il est plus rapide d'utiliser l'expression réduite ») : n'évalue aucune compétence. (1) : `bank_4eme/Calcul_Littéral|CAL_04.4`
- Vocabulaire des angles (plat, aigu, obtus, moitié d'un droit) : aucune compétence du référentiel. (5) : `bank_6eme/Angles|ANG_01.1`, `bank_6eme/Angles|ANG_01.2`, `bank_6eme/Angles|ANG_01.3`, `bank_6eme/Angles|ANG_01.4`, `bank_6eme/Angles|ANG_01.5`
- Vocabulaire du cercle (rayon, diamètre) : aucune compétence du référentiel. (6) : `bank_6eme/Géométrie|GEOM_01.1`, `bank_6eme/Géométrie|GEOM_01.2`, `bank_6eme/Géométrie|GEOM_01.3`, `bank_6eme/Géométrie|GEOM_01.4`, `bank_6eme/Géométrie|GEOM_01.5`, `bank_6eme/Géométrie|GEOM_04.5`
- Propriétés/nature des triangles et quadrilatères usuels : aucune compétence du référentiel. (7) : `bank_6eme/Géométrie|GEOM_02.1`, `bank_6eme/Géométrie|GEOM_02.2`, `bank_6eme/Géométrie|GEOM_02.3`, `bank_6eme/Géométrie|GEOM_02.5`, `bank_6eme/Géométrie|GEOM_04.1`, `bank_6eme/Géométrie|GEOM_04.3`, `bank_6eme/Géométrie|GEOM_04.4`
- Droites parallèles/perpendiculaires : aucune compétence du référentiel. (5) : `bank_6eme/Géométrie|GEOM_03.1`, `bank_6eme/Géométrie|GEOM_03.2`, `bank_6eme/Géométrie|GEOM_03.3`, `bank_6eme/Géométrie|GEOM_03.4`, `bank_6eme/Géométrie|GEOM_03.5`

## Corrections appliquées dans `_legacy/` (décision du coordinateur, 24/09)

Les sources (`data/*.json`) ne sont **pas** modifiées. Les corrections sont faites directement dans les fichiers `_legacy/` (le script de conversion était temporaire et n'est pas conservé : ne pas régénérer ces fichiers depuis les sources, sinon les corrections sont perdues).

### Distracteurs égaux à la bonne réponse → remplacés par une erreur type taguée

| Item | Ancien distracteur (= bonne réponse) | Nouveau distracteur | `err` |
|---|---|---|---|
| `Probabilites_Brevet_v4|PROB_01.2` | $\frac{6}{12}$ | $6$ | `DF.PROB.02#superieure_a_1` | (step « Attention… » qui citait l'ancien distracteur retiré)
| `Probabilites_Brevet_v4|PROB_01.5` | $\frac{4}{12}$ | $\frac{4}{11}$ | `DF.PROB.02#favorables_sur_defavorables` |
| `Probabilites_Brevet_v4|PROB_02.2` | $\frac{12}{20}$ | $\frac{21}{4000}$ | `DF.PROB.04#multiplie_ou` | (step « Attention… » qui citait l'ancien distracteur retiré)
| `Probabilites_Brevet_v4|PROB_02.4` | $\frac{5}{20}$ | $\frac{3}{200}$ | `DF.PROB.04#multiplie_ou` |
| `Probabilites_Brevet_v4|PROB_03.5` | $\frac{2}{6}$ | $\frac{7}{6}$ | `DF.PROB.05#branche_additionnee` |
| `Probabilites_Brevet_v4|PROB_04.2` | $\frac{32}{50}$ | $32$ | `DF.STAT.02#effectif_pour_frequence` | (step « Attention… » qui citait l'ancien distracteur retiré)
| `Pythagore_Brevet_v4|PYT_02.5` | $\sqrt{6{,}25}$ m | $\sqrt{78{,}25}$ m | `EG.PYTH.02#additionne_au_lieu_soustraire` |
| `Pythagore_Brevet_v4|PYT_03.1` | $\sqrt{2500}$ m | $2500$ m | `EG.PYTH.01#oubli_racine` |
| `Pythagore_Brevet_v4|PYT_04.2` | $\sqrt{144}$ m | $\sqrt{194}$ m | `EG.PYTH.02#additionne_au_lieu_soustraire` |
| `Racines_Carrees_Brevet_v4|RAC_03.4` | $\dfrac{10\sqrt{50}}{50}$ | $\dfrac{1}{5}$ | `NC.RAC.04#rationalisation_partielle` |
| `Auto_Stats_Probas_v4|AUTSP_02.5` | $\frac{5}{50}$ | $\frac{1}{9}$ | `DF.PROB.02#favorables_sur_defavorables` |
| `diagnostic_3eme|36` | $90\pi$ cm³ | $1131$ cm³ | `GM.VOL.02#diametre` |
| `bank_4eme/Fractions|FRA_02.5` | $\frac{15}{60}$ | $\frac{25}{9}$ | `NC.FRAC.05#produit_en_croix` |

`PROB_01.5` (deux distracteurs égaux entre eux, 1/3 = 4/12) est corrigé dans la même passe. Le distracteur « favorables ÷ défavorables » de `PROB_02.2` (21/4000) et `PROB_02.4` (3/200) est moins naturel que les autres : il est choisi parce qu'il nomme `multiplie_ou`, seule erreur du référentiel qui s'applique ici.

### Tableaux de `STAT_04` rendus cohérents

Le tableau de `STAT_04.1` donnait à la classe C les notes de la classe A. Chaque item a maintenant le tableau dont il a besoin : `STAT_04.1` classe A seule, `STAT_04.2` et `STAT_04.4` classe C seule, `STAT_04.3` et `STAT_04.5` les deux classes (tableau à 4 lignes). Données de C reprises de `STAT_04.2`, cohérentes avec les steps de 04.3 à 04.5 (médianes 12 et 12, écarts interquartiles 4 et 8).

## Bugs repérés dans l'existant (non corrigés)

Les 10 items écartés pour bug (§ Items écartés) ne sont **pas** corrigés : décision du coordinateur, les anciens chapitres v4 seront retirés.

### Réponses fausses ou incohérentes

- `Arithmetique_Brevet_v4|ARITH_01.5` — Réponse non unique : les diviseurs de 84 supérieurs à 10 sont 12, 14, 21, 28, 42 et 84 ; « la seule taille possible » = 12 est faux.
- `Racines_Carrees_Brevet_v4|RAC_01.5` — RÉPONSE FAUSSE : a = « Vrai » pour « √9 + √16 = √25 » ; c'est Faux (7 ≠ 5). Enseigne exactement l'erreur type NC.RAC.02#somme_racines. Écarté de la banque.
- `Fonctions_Brevet_v4|FONC_02.4` — RÉPONSE DOUTEUSE : d'après les points de la figure, T(18) = 22 et T(20) = 19, donc T ≥ 20 jusqu'à environ 19 h 20, pas seulement « de 12 h à 18 h ».
- `Geometrie_Espace_Brevet_v4|GEOESP_01.5` — RÉPONSE FAUSSE : diamètre 6 cm, hauteur 12 cm → 2 boules empilées, le fichier dit 3 (la figure aussi). Écarté.
- `Scratch_Brevet_v4|SCRATCH_02.4` — RÉPONSE INCOHÉRENTE : a = « 2x + 7 » à la question « le résultat est-il toujours impair ? ». Écarté.
- `diagnostic_3eme|47` — RÉPONSE FAUSSE (convention française) : Q1 de 4, 6, …, 18 (8 valeurs) = 6 (rang 2), le fichier dit 7 (moyenne de la 2e et 3e valeur, convention anglo-saxonne). Écarté.

### Doublons

- `diagnostic_3eme|33` — Doublon quasi exact de Transformations_Brevet_v4|TRANSF_01.2 (même point, même vecteur, mêmes options).
- `diagnostic_3eme|51` — Doublon quasi exact de Scratch_Brevet_v4|SCRATCH_01.1 (×3 + 5 pour x = 4).

### Ambiguïtés, consignes, format

- `Arithmetique_Brevet_v4|ARITH_01.4` — QCM ambigu : le distracteur « Faux, car 84 est pair donc divisible par 4 » a une conclusion juste et une affirmation vraie (84 = 4 × 21) ; seul le « donc » est discutable.
- `Puissances_Brevet_v4|PUIS_01.5` — Ne discrimine pas l'erreur « compare seulement les premiers facteurs » : le rangement par mantisses donne le même ordre que le bon (1,5 < 3,2 < 5).
- `Puissances_Brevet_v4|PUIS_04.2` — La réponse attendue $0{,}78 \times 10^{8}$ n'est pas en notation scientifique (7,8 × 10⁷) : acceptable car la question ne l'exige pas, mais la question suivante (PUIS_04.3) l'écrit 7,8 × 10⁷.
- `Racines_Carrees_Brevet_v4|RAC_04.4` — Consigne « Factorise » pour une réduction ($5\sqrt{3} + \sqrt{75} = 10\sqrt{3}$) : vocabulaire impropre.
- `Calcul_Litteral_Brevet_v4|CALLIT_04.2` — Factoriser $x^2 + 4x + 3$ en $(x+1)(x+3)$ : ni facteur commun ni identité remarquable, hors programme 3e. Rattaché faute de mieux à NC.LIT.08 (mapping didacticien conservé).
- `Inequations_Brevet_v4|INEQ_02.5` — Ambigu : « minutes entières complètes » de t = 4 à t = 16 → 12 attendu, mais 13 (instants entiers 4…16) est défendable.
- `Fonctions_Brevet_v4|FONC_01.1` — Double consigne (expression de f(d) + prix pour 10 km) mais une seule réponse fill (15). Même problème sur FONC_01.3 (« Que représente cette valeur ? ») et FONC_04.1.
- `Statistiques_Brevet_v4|STAT_03.3` — Quartiles / écart interquartile : hors programme collège (cf. référentiel, poids 1). Idem STAT_03.4 et STAT_04.4.
- `Thales_Brevet_v4|THAL_02.4` — Unité non précisée : a = 160 (cm) ; « 1,6 » (m) serait compté faux par le fill.
- `Thales_Brevet_v4|THAL_03.3` — VF avec consigne « Justifie à l'aide de la réciproque » : la justification n'est pas évaluable en Vrai/Faux.
- `Geometrie_Espace_Brevet_v4|GEOESP_01.4` — Modèle discutable : on additionne le volume du cône plein et de la boule entière alors que la boule repose dans le cône (volumes qui se chevauchent).
- `Transformations_Brevet_v4|TRANSF_03.5` — Ambigu / discutable : « k = −1/2 conserve l'orientation » est mathématiquement vrai (similitude directe). Écarté.
- `Transformations_Brevet_v4|TRANSF_04.5` — Fill à réponse texte libre, sans liste, réponse inexacte (k = −1). Écarté.
- `Scratch_Brevet_v4|SCRATCH_04.4` — VF sans affirmation. Écarté.
- `Scratch_Brevet_v4|SCRATCH_03.4` — Double question (valeur de n + figure tracée) pour une seule réponse (4).
- `Auto_Stats_Probas_v4|AUTSP_04.1` — Ambigu : si les 4 joueurs s'affrontent entre eux, chaque match est compté deux fois (40 participations ≠ 40 matchs).
- `Auto_Stats_Probas_v4|AUTSP_03.3` — Ne discrimine pas l'erreur « (min + max)/2 » : (8 + 16)/2 = 12 = la vraie moyenne.
- `diagnostic_3eme|5` — Les 2 distracteurs valent la bonne réponse (21/126 = 7/42 = 1/6). Écarté.
- `diagnostic_3eme|45` — Champ `type` absent sur 6 questions QCM (45, 47, 48, 50, 52, 53) : rendu par défaut en QCM, `type: "qcm"` ajouté à la conversion. Et 5 VF (17, 22, 26, 29, 34) ont `options: []` (bloquant pour validate_exos) : `["Vrai", "Faux"]` ajouté.
- `bank_6eme/Fractions|FRAC_03.4` — Fill à réponse non simplifiée ($\frac{4}{12}$) : $\frac{1}{3}$, juste, sera compté faux par `_normFill`. Même risque sur bank_6eme/Fractions FRAC_01.1/01.4 et FRAC_03.1 (fractions non irréductibles acceptées uniquement sous une forme).
- `bank_5eme/Pythagore|PYT5_03.4` — Distracteur « Non, car 7 + 9 ≠ 12 » : conclusion juste, justification fausse — ambigu en QCM.

### LaTeX / gate `validate_exos.py` (erreurs déjà présentes dans les fichiers source, identiques après conversion)

- `Arithmetique_Brevet_v4|ARITH_02.1` — LATEX BRUT dans a : commandes hors $...$ → \times, \times
- `Auto_Stats_Probas_v4|AUTSP_03.4` — UNICODE_MIX dans q
- `Calcul_Litteral_Brevet_v4|CALLIT_04.3` — UNICODE_MIX dans q
- `Calcul_Litteral_Brevet_v4|CALLIT_04.4` — UNICODE_MIX dans q
- `Pythagore_Brevet_v4|PYT_03.2` — UNICODE_MIX dans steps[1]
- `Pythagore_Brevet_v4|PYT_04.4` — UNICODE_MIX dans q
- `Pythagore_Brevet_v4|PYT_04.4` — UNICODE_MIX dans steps[1]
- `Racines_Carrees_Brevet_v4|RAC_01.4` — UNICODE_MIX dans q
- `Transformations_Brevet_v4|TRANSF_01.2` — Step 1 est générique/passe-partout : "On applique la formule pour chaque coordonnée : $x_{A'} = x_..."
- `diagnostic_3eme|36` — UNICODE_MIX dans a
- `diagnostic_3eme|36` — UNICODE_MIX dans options[0]
- `diagnostic_3eme|36` — UNICODE_MIX dans options[1]
- `diagnostic_3eme|36` — UNICODE_MIX dans options[2]
- `diagnostic_3eme|36` — UNICODE_MIX dans steps[2]

Les caractères Unicode signalés (`²`, `√`, `×`) sont hors `$…$` à côté de LaTeX : rendu KaTeX correct mais incohérent. `ARITH_02.1` a `a = "2 \times 3^2 \times 7"` sans `$` : la comparaison fill passe par `_normFill`, à tester.

## Pour le moteur et le relecteur

- Tous les items sont `usage: ["train"]`. Aucun n'est calibré pour le diagnostic.
- Ne pas servir seuls les items `depend_question_precedente: true` ; servir de préférence les parapluies complets dans l'ordre `num` pour les « problèmes Brevet ».
- Les notions hors programme (quartiles `DF.STAT.07`, simplification/rationalisation de racines `NC.RAC.03`/`.04`, factorisation de trinômes rangée en `NC.LIT.08`) restent en entraînement, conformément à la reco du didacticien.
- Le relecteur doit repasser en priorité : les rattachements `err` des fill (mauvaises réponses « prévisibles » déduites, non observées) et les items de § Bugs.

