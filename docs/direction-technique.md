# Direction Technique — Matheux

> Le process complet : de l'analyse des données élève à la prescription d'exercices.
> Ce document garantit la "patte Matheux" — que ce soit Nicolas, l'IA, ou un futur automate.
>
> Complémentaire de `prompt-generation-exos.md` (fabrication des exos).
> Celui-ci couvre le POURQUOI et le QUOI. L'autre couvre le COMMENT.

---

## 0. Philosophie — ce qui fait la patte Matheux

1. **Chirurgical** — on ne refait jamais un chapitre entier "pour voir". On identifie le trou exact, on le comble
2. **Jamais culpabilisant** — "Commence par..." pas "Tu as des lacunes en..."
3. **Le score ne ment pas** — difficulté homogène entre slots, EASY = 1er essai sans aide
4. **L'élève progresse, il le voit** — sessions retro avec %, flèches tendance, pills colorées
5. **Pas de doublon** — un élève ne retombe JAMAIS sur un exercice identique (voir §4)

---

## 1. Analyse des données élève — les signaux à lire

### Source : onglet Scores

Pour chaque exercice fait par l'élève, on a :

| Signal | Colonne | Ce que ça révèle |
|---|---|---|
| **Résultat** | `EASY/MEDIUM/HARD` | EASY = maîtrisé. MEDIUM = compris avec aide. HARD = pas compris |
| **NbIndices** | `0-3` | 0 = autonome. 1-2 = besoin de guidage. 3 = bloqué sans aide complète |
| **FormuleVue** | `0/1` | 0 = sait la formule. 1 = a eu besoin du rappel théorique |
| **Temps(sec)** | nombre | <30s = automatisé. 30-120s = réfléchi. >120s = laborieux ou pause |
| **MauvaiseOption** | texte | L'erreur exacte choisie — révèle le raisonnement faux |
| **Source** | `BOOST/CALIBRAGE/""` | Distinguer les contextes (ne pas mélanger calibrage et curriculum) |

### Grille de lecture croisée

| Pattern | Signaux | Diagnostic | Prescription |
|---|---|---|---|
| **Formule-dépendant** | EASY mais FormuleVue=1 sur >50% des exos | Sait appliquer, ne possède pas encore la formule | Exos SANS formule. Fill et V/F qui forcent la restitution de mémoire |
| **Erreur de signe** | HARD + MauvaiseOption montre inversion ±  | Confusion sur le double produit, les négatifs | Exos ciblés sur les cas pièges : $(a-b)^2$, $(-x)^2$, développer avec négatifs |
| **Confusion conceptuelle** | HARD sur V/F, temps court (<30s) | Répond vite et faux = fausse certitude | V/F avec justification dans les steps. Exos "Où est l'erreur ?" |
| **Lent mais juste** | EASY mais Temps >200s | Comprend mais pas encore fluide | Exos de calcul direct, répétition avec variantes numériques |
| **Bloqué sans indices** | MEDIUM systématique, NbIndices ≥2 | Besoin du guidage étape par étape | Exos avec steps très décomposés. Commencer par des valeurs simples |
| **Lecture graphique** | HARD sur exos de graphique/tableau | Ne sait pas extraire l'info d'un support visuel | Exos contextualisés avec vocabulaire graphique explicite |
| **Calcul mental fragile** | HARD sur exos simples, temps long | Les bases numériques ne sont pas automatisées | Exos de calcul pur, valeurs entières, progression lente |

### Process d'analyse — checklist

1. **Filtrer** les scores hors CALIBRAGE (le calibrage est un snapshot, pas une mesure de progression)
2. **Séparer** par chapitre
3. **Pour chaque chapitre**, calculer :
   - Score P8 (EASY / total × 100)
   - Taux FormuleVue (combien ont eu besoin de la formule)
   - Taux Indices (combien ont utilisé ≥1 indice)
   - Temps moyen
   - Liste des HARD avec MauvaiseOption (les erreurs exactes)
4. **Identifier le pattern dominant** (tableau ci-dessus)
5. **Lire les MauvaiseOption** — c'est l'info la plus précieuse. L'erreur choisie révèle le raisonnement

---

## 2. De l'analyse à la prescription

### Étape 1 — Diagnostic en une phrase

Après analyse, formuler le diagnostic en UNE phrase qui dit exactement ce qui bloque.

**Exemples réels :**
- Charlie, Calcul Littéral : "Il sait factoriser $a^2-b^2$ avec la formule devant lui, mais confond $(2x)^2$ et $2x^2$ sans aide — il ne possède pas encore les identités remarquables par coeur"
- Charlie, Fonctions : "Les bases sont solides (93% EASY), mais la lecture graphique et les fonctions non-linéaires $x^2$ restent fragiles"

### Étape 2 — Prescription des 4 slots

Chaque slot de 5 exos doit cibler un aspect du diagnostic :

| Slot | Rôle dans la prescription |
|---|---|
| **Slot 1 (1-5)** | Remettre en confiance — reprendre la base acquise avec de nouvelles valeurs |
| **Slot 2 (6-10)** | Attaquer la faiblesse #1 — le pattern d'erreur le plus fréquent |
| **Slot 3 (11-15)** | Attaquer la faiblesse #2 — le deuxième pattern ou une variante plus dure du #1 |
| **Slot 4 (16-20)** | Synthèse — croiser les compétences, exos qui forcent à mobiliser tout |

### Étape 3 — Brief pour la génération

Rédiger un brief clair AVANT de générer les exos :

```
BRIEF — [Chapitre] V2 pour [Prénom] ([Niveau])

Diagnostic : [1 phrase]

Erreurs exactes observées :
- Exo #N : a répondu [X] au lieu de [Y] → [explication de l'erreur]
- Exo #N : ...

Prescription slots :
- Slot 1 : [sous-compétence] — confiance
- Slot 2 : [sous-compétence] — faiblesse #1
- Slot 3 : [sous-compétence] — faiblesse #2
- Slot 4 : [sous-compétence] — synthèse

Contraintes spécifiques :
- [ex: pas de formule affichée sur slots 2-3]
- [ex: inclure au moins 2 V/F pièges]
- [ex: varier les contextes vs le chapitre précédent]

Exercices déjà vus (NE PAS REPRODUIRE) :
- [liste des énoncés/types déjà faits — voir §4]
```

→ Puis passer à `prompt-generation-exos.md` pour la fabrication.

---

## 3. Ton et messages — invariants

### Message d'accueil du chapitre (insight)

| Situation | Formulation | Interdit |
|---|---|---|
| Nouveau chapitre assigné | "On commence par [X] — [raison positive]" | "Tu as des lacunes en..." |
| Chapitre V2 (re-travail) | "On reprend [X] avec de nouveaux exercices" | "Tu n'as pas compris..." |
| Boost ciblé | "Tes exos du jour ciblent [X et Y]" | "Tu as fait des erreurs sur..." |

### Steps (indices) — la patte Matheux

Les indices sont le coeur de l'expérience. Ils doivent :
1. **Guider sans donner** — step 1 = reformulation, step 2 = calcul intermédiaire, step 3 = conclusion
2. **Utiliser les valeurs de l'énoncé** — jamais de "applique la formule", toujours "ici, $a = 2x$ et $b = 3$, donc..."
3. **Être progressifs** — un élève qui lit le step 1 doit pouvoir re-tenter AVANT de lire le step 2
4. **Être cohérents entre chapitres** — même structure, même niveau de détail, même ton

### Adaptation au niveau (rappel)

| Niveau | Ton steps | Longueur | Formule |
|---|---|---|---|
| 6EME | "On commence par compter..." | Court, 1-2 phrases/step | Toujours affichée |
| 5EME-4EME | "Ici, on utilise..." | Moyen | Affichée sauf si test de restitution |
| 3EME | "On identifie..." | Précis | Parfois masquée (Brevet) |
| 1ERE | "On pose..." | Dense | Rarement affichée |

---

## 4. Règle anti-doublon — JAMAIS le même exo deux fois

### Principe

Un élève qui refait un chapitre (V2, V3...) ne doit JAMAIS retomber sur un exercice identique.
Le système `getSeenExoKeys()` du backend filtre les exos déjà vus dans les boosts.
Mais pour les chapitres injectés manuellement, c'est au prescripteur de garantir la nouveauté.

### Ce qui doit changer entre V1 et V2

| Element | Doit changer | Peut rester |
|---|---|---|
| **Valeurs numériques** | Oui, toujours | — |
| **Contexte / mise en situation** | Oui, varier les prénoms et situations | — |
| **Type de question** | Oui si possible (QCM → V/F → Fill) | Si le type est contraint par la compétence |
| **Sous-compétence testée** | Oui, cibler les faiblesses | Les bases acquises peuvent être re-testées |
| **Formule générale (f)** | — | Oui, la formule du chapitre reste la même |
| **Structure des steps** | — | Le schéma 3 étapes reste le même |
| **Wording énoncé** | Oui, reformuler | La question mathématique sous-jacente peut être similaire |

### Exemple concret

**V1 exo #4 (Charlie, Calcul Littéral) :**
> Factorise $4x^2-9$

**V2 — même compétence, exercice différent :**
> QCM → Fill : "Complète : $16x^2 - 25 = (\_\_\_ - 5)(\_\_\_ + 5)$"

Même compétence (différence de carrés), mais :
- Valeurs différentes ($16x^2$ au lieu de $4x^2$)
- Type différent (fill au lieu de QCM)
- L'élève doit reconnaître $(4x)^2$ — exactement son point faible

### Checklist avant injection

Avant d'injecter un chapitre V2, **toujours** :
1. Lister les énoncés du V1 (extraire de Scores via `Énoncé`)
2. Vérifier qu'aucun exo V2 n'a le même énoncé ou les mêmes valeurs
3. Si la même compétence est retestée, varier au minimum le type ET les valeurs

---

## 5. Boost personnalisé — le brief rapide

Pour les boosts quotidiens (5 exos), le process est allégé :

1. **Identifier les 2-3 erreurs récentes** (derniers Scores HARD)
2. **Mixer les chapitres** si les erreurs viennent de chapitres différents
3. **Structure fixe :**
   - Exo 1 : confiance — base acquise, valeurs simples
   - Exos 2-3 : ciblés sur les erreurs exactes, valeurs différentes
   - Exo 4 : variante du même type
   - Exo 5 : un cran au-dessus pour consolider
4. **Insight** : 1 phrase qui explique le ciblage ("Tes exos du jour ciblent les identités remarquables et la lecture de graphique")
5. **Anti-doublon** : vérifier BoostExos + Scores pour ne pas re-servir un exo vu

---

## 6. Cas d'usage — exemples réels

### Cas Charlie (3EME) — Mars 2026

**Données :**
- Calcul Littéral : 21 exos, 76% P8, FormuleVue sur 8/21, 6 HARD
- Fonctions : 15 exos, 93% P8, 1 HARD (lecture graphique)

**Analyse :**
- Pattern "formule-dépendant" sur Calcul Littéral (#1-6 tous EASY avec formule, #7-20 mix avec 6 HARD sans formule)
- Pattern "confusion conceptuelle" : $(3x)^2 = 3x^2$ (FAUX), $4x^2 = (4x)^2$ (FAUX)
- Fonctions : solide, seul trou = lecture graphique

**Prescription :**
- Calcul Littéral V2 : slot 1 = double distributivité sans identités, slot 2 = identités SANS formule, slot 3 = preuves/développements, slot 4 = V/F pièges
- Fonctions V2 : slot 1 = lecture graphique, slot 2 = sens de variation, slot 3 = déterminer $ax+b$, slot 4 = non-linéaire $x^2$
- Boost : mix des 2 chapitres, ciblé erreurs exactes

**Exercices déjà vus à ne pas reproduire :**
- Factorise $x^2-9$, $4x^2-9$, $25x^2-4$ (même pattern, changer les valeurs)
- Développe $(x+4)^2$, $(x-5)^2$, $(3x-1)^2$ (varier vers $(2x+3)^2$, $(4x-1)^2$)
- $f(x)=2x-3$ calcule $f(0)$, $f(4)$, $f(-1)$ (changer la fonction)

---

## 7. Vers l'automatisation

Ce process est aujourd'hui manuel (Nicolas + IA). Les étapes automatisables :

| Étape | Aujourd'hui | Automatisable ? |
|---|---|---|
| Lecture Scores | Script Python | Oui — déjà fait via `sheets.py` |
| Pattern matching | Analyse humaine | Oui — grille ci-dessus est algorithmique |
| Diagnostic 1 phrase | Rédaction humaine | Oui — templates par pattern |
| Brief prescription | Rédaction humaine | Partiellement — les slots sont standardisés |
| Génération exos | Claude via prompt | Oui — `prompt-generation-exos.md` |
| Anti-doublon | Vérification manuelle | Oui — `getSeenExoKeys()` + comparaison textuelle |
| Injection Sheet | Admin panel | Oui — script Python |

**Étapes d'automatisation (par priorité) :**

1. ✅ `direction-technique.md` — process documenté (fait 2026-03-23)
2. ✅ Boutons "Aperçu élève" + "Publier" dans l'admin pour chapitres ET boosts (fait 2026-03-23)
3. ✅ Explication "Pourquoi ces exos" visible dans la carte admin — chapitres ET boosts (fait 2026-03-23)
4. ✅ Pré-remplissage textarea admin depuis Suivi — le JSON injecté en amont remonte automatiquement dans l'admin avec diagnostic + aperçu prêts (fait 2026-03-23)
5. ✅ Action "📦 À VALIDER" dans l'admin — quand un chapitre/boost est pré-rempli dans Suivi, l'admin affiche une action dédiée (fait 2026-03-23)
6. 🔜 **`prescribe.py`** — script qui analyse automatiquement les Scores d'un élève quand un chapitre est terminé, génère le brief (diagnostic + slots + exos déjà vus), et le stocke comme draft dans l'admin. Nicolas n'a plus qu'à valider + aperçu + publier. L'objectif : réduire le workflow de 8 étapes à 3 (voir brief → aperçu → publier).
7. 🔜 Génération auto des exos depuis le brief (Claude API) — Nicolas valide toujours avant publish

---

## Historique

| Date | Changement |
|---|---|
| 2026-03-23 | Création — basé sur analyse réelle de Charlie (Calcul Littéral + Fonctions) |
