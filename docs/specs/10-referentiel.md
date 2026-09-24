# 10 — Référentiel de compétences 3e

> Livrable Didacticien · 24/09/2026 · branche `feat/diagnostic-3e`
> Contrat : [00-contrat-commun.md](00-contrat-commun.md) §2

## Fichiers

| Fichier | Rôle |
|---|---|
| `data/referentiel_3eme/competences.json` | Le référentiel (format contrat §2) : source de vérité |
| `data/referentiel_3eme/check_referentiel.py` | Vérification : JSON, IDs, prérequis résolus, graphe acyclique, erreurs types, aucun orphelin, chapitres legacy existants. **Passe ✅** |
| `data/referentiel_3eme/couverture.py` | Rattache les 494 questions existantes aux compétences, génère les deux fichiers ci-dessous |
| `data/referentiel_3eme/mapping_legacy.json` | Clé `Chapitre\|SLOT.num` → `comp` (+ secondaires). Sert à remplir le champ `comp` des sous-questions v4 (contrat §3) |
| `data/referentiel_3eme/couverture_existante.md` | Couverture par compétence, trous, volume à générer |

## Chiffres

**121 compétences · 297 erreurs types · 193 arcs de prérequis · chaîne la plus longue : 9 niveaux.**

| Domaine | Total | dont 6e | 5e | 4e | 3e | Poids 3 |
|---|---|---|---|---|---|---|
| NC — Nombres et calculs (+ littéral, équations) | 45 | 5 | 8 | 16 | 16 | 18 |
| DF — Données, fonctions, proportionnalité | 31 | 1 | 7 | 7 | 16 | 12 |
| GM — Grandeurs et mesures | 15 | 5 | 3 | 2 | 5 | 5 |
| EG — Espace et géométrie | 24 | 1 | 5 | 6 | 12 | 9 |
| AP — Algorithmique et programmation | 6 | 0 | 2 | 4 | 0 | 2 |
| **Total** | **121** | 12 | 25 | 35 | 49 | 46 |

Thèmes : `ENT PRIO REL ARITH FRAC PUIS RAC LIT EQUA INEQ` · `PROP FONC AFF STAT PROB` ·
`CONV AIRE VOL VIT AGR` · `REP ANG PYTH THAL SEMB TRIG TRANS ESP` · `PROG`.

## Principes retenus

1. **Atomique.** Une compétence = un geste évaluable en une question (« calculer un côté de
   l'angle droit » est séparé de « calculer l'hypoténuse » et de « prouver qu'un triangle est
   rectangle » : ce sont trois erreurs différentes).
2. **Niveau d'origine ≠ importance.** `niveau_origine` indique où la compétence s'apprend.
   Pythagore (4e) ou les relatifs (5e) sont des attendus de fin de 3e à part entière. Le
   Brevet évalue tout le cycle 4.
3. **Prérequis directs uniquement.** Chaque arc veut dire « si l'élève rate le prérequis,
   il rate très probablement la compétence ». Exemple : `EG.PYTH.02` → `EG.PYTH.01` →
   `NC.PUIS.01` (carrés) + `NC.RAC.01` (racines). Le graphe ne relie jamais deux
   compétences de même niveau « par proximité de chapitre ».
4. **Erreurs types réelles.** Ce sont des conceptions erronées classiques, documentées
   en didactique : modèle additif en proportionnalité, `(a+b)² = a²+b²`, carré pris pour
   un double, `1/3 + 1/4 = 2/7`, erreur du joueur, `1 h 30 = 1,30 h`, confusion
   image/antécédent, etc. Chacune a 3 formulations : élève (`libelle`), parent
   (`libelle_parent`, sans jargon), remédiation (geste concret).
5. **Poids Brevet** (1 rare / 2 fréquent / 3 incontournable). Il vient de l'analyse des
   ~40 sujets 2021-2025 et des sujets zéro 2026 (`docs/rapport-brevet-2026.md`) :
   calcul littéral, Pythagore/Thalès et Scratch tombent 5 ans sur 5 (poids 3). Probas et
   fonctions tombent 4 à 5 ans sur 5 (poids 2-3). Arithmétique, volumes, transformations et
   trigo : 3 ans sur 5 (poids 2). Puissances et inéquations : 2 ans sur 5 (poids 2 ou 1).
   Un prérequis mobilisé partout **sans être nommé** reçoit aussi 3 : relatifs, priorités,
   fractions, carrés, arrondis, conversions. Ils sont implicites dans presque tous les
   exercices et figurent dans la liste officielle des automatismes 2026.
6. **Automatismes 2026 couverts.** Chaque item de la liste officielle (fractions usuelles,
   pourcentages usuels, carrés de 1 à 12, critères de divisibilité, notation scientifique,
   repère, angle manquant, conversions y compris durées, solides, probabilité simple,
   fréquence, moyenne, proportionnalité, suite d'instructions) a sa compétence.
7. **Hors programme officiel, conservé à poids 1.** Ces notions ne sont plus au programme
   de collège depuis 2016 mais figurent dans les chapitres existants : simplification et
   rationalisation des racines (`NC.RAC.03`, `NC.RAC.04`), quartiles et boîtes (erreur
   `DF.STAT.07#boite_effectif`), coordonnées du milieu (`EG.REP.02`). Les inéquations
   (`NC.INEQ.01`) sont gardées à poids 1. Les problèmes de seuil (`NC.INEQ.02`, poids 2)
   restent fréquents même quand on les résout par une équation ou par des essais.

## Les 10 causes racines attendues chez un élève de 3e

On les classe par portée dans le graphe (nombre de compétences 3e qui en dépendent,
directement ou non) et par fréquence connue en didactique :

| # | Cause racine | Compétence(s) | Ce qu'elle fait rater en 3e |
|---|---|---|---|
| 1 | Règles des signes (addition vs produit) | `NC.REL.02`, `NC.REL.03` | Développements, équations, coefficient directeur, exposants négatifs, translations |
| 2 | Priorités opératoires | `NC.PRIO.01` | Substitution, programmes de calcul, moyennes, `3 × 2²` |
| 3 | Sens de la fraction et opérations | `NC.FRAC.01` à `.03` | Probabilités, Thalès (rapports), équations à coefficient fractionnaire |
| 4 | Carré confondu avec le double | `NC.PUIS.01` | Pythagore, identités remarquables, aire du disque, volumes |
| 5 | Racine carrée (oubli, √ distribuée sur +) | `NC.RAC.01` | Pythagore (réponse « 25 » au lieu de 5), `x² = a` |
| 6 | Modèle additif au lieu de multiplicatif | `DF.PROP.01`, `DF.PROP.02` | Pourcentages, échelles, Thalès, vitesses, fonctions linéaires, agrandissements |
| 7 | Statut de la lettre, réduction (`x + x = x²`) | `NC.LIT.01`, `NC.LIT.03` | Tout le calcul littéral, mise en équation, preuves « quel que soit x » |
| 8 | Numération décimale, puissances de 10 | `NC.ENT.01`, `NC.ENT.02`, `NC.PUIS.02` | Notation scientifique, conversions, comparaisons |
| 9 | Conversions (durées en base 60, aires ×100, volumes ×1000) | `GM.CONV.01` à `.03` | Vitesse moyenne, volumes en litres, échelles |
| 10 | Abscisse et ordonnée inversées, lecture d'axes | `EG.REP.01` | Lecture graphique d'images et d'antécédents, fonctions affines, Scratch (déplacements) |

**Note pour le moteur (20-moteur).** La fermeture transitive est large : `NC.ENT.02` atteint
66 compétences. Pour désigner une « cause racine », il vaut mieux s'en tenir aux
prérequis à distance 1 ou 2 d'une lacune, et exiger que le prérequis soit lui-même en
lacune (contrat §4). Sinon on accuse la numération de 6e de tout.

## Couverture de l'existant (résumé)

- 494 questions uniques rattachées (440 v4 + 54 diagnostic ; les `diag_*.json` sont des
  copies du diagnostic).
- **20 compétences sans aucune question**, dont 5 prérequis à poids 3 : `NC.REL.02`,
  `NC.REL.03`, `NC.ENT.01`, `NC.ENT.03`, `NC.LIT.03`. Les relatifs, cause n°1, ne sont
  jamais testés isolément.
- Les 37 compétences de socle 6e/5e totalisent 101 questions : l'existant mesure le
  symptôme (chapitre Brevet), pas la cause.
- **Aucune question n'a de champ `err`** : aujourd'hui, on ne peut détecter aucune erreur
  type. Les distracteurs QCM existants sont souvent réalistes et peuvent être tagués
  sans rien générer.
- Dimensionnement : ≈ 582 items de diagnostic à produire (6 par compétence 3e, 4 par
  prérequis). Avec l'entraînement (30/20/10 selon le poids), la cible est ≈ 3 300 items,
  dont ≈ 2 830 manquants. Détail dans `couverture_existante.md`.

## Note pour le chef de projet (contrat)

Le contrat §2 impose un `THEME` de 3 à 5 lettres, mais l'exemple §5 cite `NC.EQ.04`. J'ai
appliqué la règle : les équations sont `NC.EQUA.xx`. Il faut corriger l'exemple du contrat
(`NC.EQ.04` → `NC.EQUA.04`).

## ❓ Questions pour Nicolas

1. **Notions hors programme présentes dans les chapitres actuels** : simplifier ou
   rationaliser √, quartiles, milieu. Les garder ?
   → *Reco : oui dans le référentiel (poids 1), en entraînement seulement, jamais dans le
   diagnostic ni sur la carte du parent.*
2. **Profondeur du diagnostic sur les prérequis** : les tester seulement quand une
   compétence 3e est ratée (descente adaptative), ou systématiquement ?
   → *Reco : descente adaptative. C'est ce qui tient dans ~15 questions (express) et
   ~40 min (complet).*
3. **Banques `data/bank_6eme|5eme|4eme/`** (320 items déjà validés) : les rattacher aux
   compétences de prérequis ?
   → *Reco : oui. C'est la source la moins chère d'items pour les causes racines, à taguer
   `comp` + `err` avant toute génération.*
4. **Ordre de génération** : on commence par les ~582 items de diagnostic (et le tagging
   `err` des 494 existants) avant l'entraînement ?
   → *Reco : oui. Sans items de diagnostic tagués, la carte ne peut pas nommer d'erreur.*
