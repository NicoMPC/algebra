# Audit Phase 3 Brevet -- 120 exercices

**Date** : 2026-03-28
**Auditeur** : Monsieur Exos
**Fichiers** : 6 fichiers, 120 exercices au total

---

## Synthese

| Fichier | Exos | Calculs OK | Erreurs bloquantes | Warnings |
|---|---|---|---|---|
| Fractions_Brevet | 20 | 20/20 | 0 | 3 |
| Trigonometrie_Brevet | 20 | 20/20 | 0 | 1 |
| Fonctions_Affines_Brevet | 20 | 20/20 | 0 | 1 |
| Statistiques_Brevet | 20 | 20/20 | 0 | 0 |
| Probabilites_Brevet | 20 | 19/20 | **1** | 0 |
| Auto_Stats_Probas | 20 | 20/20 | 0 | 0 |
| **TOTAL** | **120** | **119/120** | **1** | **5** |

---

## ERREURS BLOQUANTES (1)

### BUG #1 -- Probabilites_Brevet exo #9 : distracteur = reponse

**Exo :** "Noe tire 2 billes SANS remise... P(2 jaunes) ?"
**Reponse :** `$\frac{3}{10}$`
**Distracteur :** `$\frac{6}{20}$`

**Probleme :** 6/20 = 3/10. Le distracteur est mathematiquement egal a la bonne reponse. Un eleve qui choisit 6/20 sera marque HARD alors qu'il a raison.

**Fix :** Remplacer `$\frac{6}{20}$` par un vrai distracteur, par exemple `$\frac{6}{25}$` (erreur : garder le denominateur du cas avec remise 5x5=25 au lieu de 5x4=20) ou `$\frac{2}{5}$` (erreur : ne considerer que le 1er tirage).

---

## WARNINGS (5)

### W1 -- Fractions_Brevet exo #10 : enonce confus

**Exo :** "Nadia partage 5/6 d'un gateau entre 5/3 de part."
**Probleme :** "5/3 de part" n'a pas de sens concret pour un eleve de 3eme. Diviser par une fraction est un concept valide mais le contexte est artificiel et incomprehensible.
**Suggestion :** Reformuler avec un contexte clair, ex: "Nadia a 5/6 d'un gateau. Elle veut que chaque part fasse 5/3 fois la part habituelle. Combien de parts obtient-elle ?" -- ou simplement changer pour un contexte different.

### W2 -- Fractions_Brevet exo #15 : step donne la reponse

**Exo :** "Forme irreductible de 45/60 ?"
**Step 3 :** "Les distracteurs 9/12 et 15/20 sont egaux a 3/4 mais ne sont pas irreductibles."
**Probleme :** Ce step revele explicitement que la reponse est 3/4 et commente les distracteurs -- ce n'est pas le role d'un indice. Un indice doit guider, pas donner la reponse.
**Fix :** Remplacer step 3 par : "On verifie : PGCD(3, 4) = 1. La fraction obtenue est-elle irreductible ?"

### W3 -- Fractions_Brevet exos #16-20 : dependance entre exos

**Exos 16-20 :** Fil narratif "Ines et son gateau". L'exo 17 presuppose le resultat de l'exo 16, et l'exo 19 presuppose le resultat de l'exo 18.
**Probleme :** Si l'eleve rate l'exo 16, il n'a pas le resultat pour l'exo 17. De plus, en mode retro ou si les exos sont affiches isolement, le contexte est perdu.
**Impact :** Mineur -- dans le flux normal les exos sont sequentiels. Mais c'est une fragilite si l'ordre change.

### W4 -- Fonctions_Affines_Brevet exo #17 : exo trivial/auto-repondant

**Exo :** "Le volume est modelise par f(t) = -800t + 5000. Quelle est l'expression de f(t) ?"
**Probleme :** La reponse est littéralement dans l'enonce. Pedagogiquement inutile.
**Fix :** Reformuler : "Le volume est modelise par f(t) = at + b avec a = -800. Si f(0) = 5000 et f(2) = 3400, determine l'expression de f(t)." Ou mieux : demander f(4) ou le temps pour un volume donne.

### W5 -- Trigonometrie_Brevet exo #20 : arrondi intermediaire

**Exo :** Hauteur falaise = 30 x tan(60) + 1.7
**Step :** "30 x 1,732 = 52,0 m"
**Calcul exact :** 30 x 1.73205 = 51.96 m, pas 52.0 m.
**Impact :** L'arrondi final (53.7) reste correct car 51.96+1.7=53.66 arrondi a 53.7. Mais le calcul intermediaire dans le step est imprecis.
**Fix :** Ecrire "30 x 1,732 = 51,96 m" dans le step.

---

## CHECKS DE FORMAT

### validate_exos.py : 6/6 PASSES

Tous les fichiers passent le validateur. Aucun `$` impair, aucun LaTeX brut hors `$...$`, toutes les reponses `a` sont dans les options, V/F ont `type: "vf"`, fill ont `options: []`.

### Automatismes (Auto_Stats_Probas)

- `f: ""` sur tous les exos : OK
- 1 step max : OK (tous ont exactement 1 step)
- `timer: 30` present : OK

### Niveaux (lvl)

| Fichier | Repartition lvl 1 / lvl 2 |
|---|---|
| Fractions_Brevet | 10 / 10 |
| Trigonometrie_Brevet | 12 / 8 |
| Fonctions_Affines_Brevet | 12 / 8 |
| Statistiques_Brevet | 10 / 10 |
| Probabilites_Brevet | 10 / 10 |
| Auto_Stats_Probas | 13 / 7 |

### Types d'exercices

| Fichier | QCM | V/F | Fill |
|---|---|---|---|
| Fractions_Brevet | 5 | 3 | 12 |
| Trigonometrie_Brevet | 4 | 4 | 12 |
| Fonctions_Affines_Brevet | 3 | 5 | 12 |
| Statistiques_Brevet | 4 | 4 | 12 |
| Probabilites_Brevet | 5 | 5 | 10 |
| Auto_Stats_Probas | 2 | 4 | 14 |

Bonne variete de types sur tous les fichiers.

---

## DOUBLONS INTER-PHASES

Pas de fichiers Phase 1 ou Phase 2 dans `data/` portant sur les memes categories (Fractions, Trigo, Fonctions Affines, Stats, Probas pour le Brevet). Pas de risque de doublon inter-phases.

Auto_Stats_Probas vs Statistiques_Brevet / Probabilites_Brevet : quelques proximites thematiques (moyenne, proba de base) mais les valeurs numeriques sont toujours differentes et les automatismes sont volontairement plus courts (1 step, pas de formule). Acceptable.

---

## VERDICT

**1 erreur bloquante a corriger** (Probabilites exo #9 : distracteur = reponse).
**4 warnings a considerer** (enonce confus, step revelateur, exo trivial, arrondi intermediaire).

Qualite globale : **BONNE**. 119/120 calculs justes. Bon equilibre de types et niveaux. Steps pedagogiquement solides dans l'ensemble.
