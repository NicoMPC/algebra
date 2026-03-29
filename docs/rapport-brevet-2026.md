# Rapport — Ce qu'un 3ème attend en arrivant sur Matheux

> Analyse de ~40 sujets de brevet/brevet blanc (2023-2025) + sujets zéro 2026 + programme officiel.
> Objectif : comprendre les patterns, la présentation, les attentes, pour que Matheux colle à la réalité du brevet.

---

## 1. Le Brevet 2026 — ce qui change

### Nouvelle structure (BO 4 sept 2025)

| Partie | Durée | Points | Calculatrice | Ce qu'on évalue |
|---|---|---|---|---|
| **Automatismes** | 20 min | 6 pts | ❌ Interdite | Réflexes, calcul mental, bases |
| **Raisonnement** | 1h40 | 14 pts (dont 2 rédaction) | ✅ Autorisée | Méthode, justification, problèmes |

**Total** : 2h, noté sur 20 (coeff 2). Date : 30 juin 2026.

### Ce qui est NOUVEAU vs 2024-2025
- La partie **Automatismes sans calculatrice** est formalisée (avant c'était implicite)
- **2 points dédiés** à la qualité de rédaction et clarté
- Les démarches non abouties sont valorisées (l'élève peut grappiller des points même sans finir)
- Le sujet complet est distribué dès le début, la copie automatismes est ramassée après 20 min
- L'élève peut commencer la partie 2 avant la fin des 20 min

---

## 2. Les Automatismes — liste complète officielle

### Nombres et calculs
- Écriture décimale des fractions simples (1/2, 1/4, 3/4, 1/10...)
- Comparer et calculer avec des décimaux (y compris négatifs)
- Simplifier, comparer, opérer sur les fractions
- Fractions d'un nombre (tiers de 18, quart de 12)
- Pourcentages usuels (100%, 50%, 25%, 10%, 1%)
- Formes multiples d'un nombre (1,2 = 12/10 = 6/5)
- Notation décimale → scientifique
- Carrés de 1 à 12 par coeur
- Critères de divisibilité (2, 3, 5, 9)

### Géométrie
- Coordonnées dans un repère orthogonal
- Identifier triangles/quadrilatères via codage
- Nommer les angles (plat, nul, opposés, adjacents, supplémentaires, aigus, obtus)
- Angle manquant d'un triangle (somme = 180°)
- Pythagore et Thalès (cas simples, sans justification)
- Conversions : longueurs, surfaces, volumes, masses, capacités, temps
- Reconnaître les solides (cube, pavé, prisme, cylindre, pyramide, cône)

### Stats & Probas
- Probabilité simple (équiprobabilité)
- Fréquence
- Moyenne

### Proportionnalité & Fonctions
- Identifier une situation proportionnelle
- Procédures : linéarité, retour à l'unité

### Algorithmique
- Interpréter une suite d'instructions (programme de calcul, déplacement, construction)

### Format des questions automatismes
- **Réponse directe** (juste le résultat, pas de justification)
- **QCM** (1 seule bonne réponse)
- **Vrai/Faux**
- Notées sur 0,5 ou 1 point chacune

---

## 3. Structure type d'un sujet de brevet (analyse 2023-2025)

### Constantes observées sur ~40 sujets

| Caractéristique | Observation |
|---|---|
| **Nombre d'exercices** | 5 (parfois 6-7 en brevet blanc) |
| **Points par exercice** | 18-22 pts chacun (sur 100 total ancien format) |
| **Durée** | 2h |
| **Exercice QCM** | Présent dans 90%+ des sujets (4-5 affirmations multi-thèmes) |
| **Exercice Scratch/algo** | Présent dans 100% des sujets (programme de calcul ou script Scratch) |
| **Exercice géométrie avec figure** | Présent dans 100% des sujets |
| **Problème contextualisé** | Présent dans 80%+ (situation réelle : construction, voyage, recette...) |

### Structure type reconstituée

```
Exercice 1 — QCM ou Vrai/Faux (multi-thèmes)
  → 4-5 affirmations touchant : médiane, probabilités, puissances, transformations
  → Format : "Quelle affirmation est correcte ?" ou "Pour chaque affirmation, dire si elle est vraie ou fausse"

Exercice 2 — Programme de calcul / Scratch
  → "On considère le programme de calcul suivant..."
  → Tester avec un nombre, puis prouver avec le calcul littéral
  → Parfois : script Scratch à interpréter

Exercice 3 — Géométrie raisonnée (le plus gros, 20-22 pts)
  → Figure fournie avec des mesures
  → Enchaîne Pythagore → Thalès → trigo → aire/volume
  → Justification obligatoire : "En utilisant le théorème de Pythagore..."

Exercice 4 — Problème contextualisé
  → Situation réelle (construction piscine, cocktail, circuit sportif, chapeau Halloween...)
  → Mélange proportionnalité + volumes + conversions + pourcentages
  → Souvent avec un tableau ou un graphique à lire

Exercice 5 — Arithmétique / Fonctions
  → PGCD, décomposition en facteurs premiers
  → OU fonctions affines : lecture graphique + calcul d'image/antécédent
  → OU statistiques : moyenne, médiane, étendue
```

### Thèmes par fréquence (analyse 2021-2025)

| Fréquence | Thèmes |
|---|---|
| **5/5 ans** | Calcul littéral, Géométrie (Pythagore/Thalès), Algorithmique/Scratch |
| **4-5/5 ans** | Probabilités, Fonctions (affines/linéaires) |
| **3-4/5 ans** | Statistiques (médiane, moyenne), Trigonométrie |
| **3/5 ans** | Arithmétique (PGCD, premiers), Volumes, Transformations |
| **2/5 ans** | Puissances/notation scientifique, Inéquations |

---

## 4. Patterns de présentation — comment c'est présenté

### Ce que l'élève voit dans un vrai sujet

1. **Contexte réel systématique** — jamais "calcule 3x + 5". Toujours "Marie veut construire une piscine de 8m..." ou "Un cocktail contient 1/3 de jus de mangue..."

2. **Figures géométriques** — schéma fourni avec mesures partielles, l'élève doit trouver les mesures manquantes. Les figures ne sont PAS à l'échelle (c'est écrit).

3. **Tableaux de données** — fréquents dans les exos stats/probas. L'élève lit et interprète.

4. **Graphiques** — courbes de fonctions, diagrammes. L'élève fait des lectures graphiques puis justifie par le calcul.

5. **Scripts Scratch** — captures d'écran du programme, l'élève doit dire ce que fait le script ou le modifier.

6. **Progression dans l'exercice** — chaque exercice a 3-5 questions qui montent en difficulté. La première est accessible (lecture, calcul simple), la dernière demande du raisonnement.

7. **Formulation** — vouvoiement ("Justifiez votre réponse", "Déterminez la longueur..."). Questions structurées : "1.a) ... 1.b) ... 2.a) ..."

### Ce qui fait la différence pour l'élève

| Ce qui rapporte des points | Ce qui en fait perdre |
|---|---|
| Citer le théorème utilisé | Donner le résultat sans justifier |
| Montrer les étapes de calcul | Sauter des étapes |
| Conclure par une phrase | Laisser un nombre sans unité |
| Tenter même sans finir (2026 : valorisé) | Laisser blanc |
| Unités correctes | Oublier les unités (cm², m³...) |

---

## 5. Implications pour Matheux

### Ce qu'on fait BIEN (déjà en place)
- ✅ Les 22 chapitres Brevet couvrent tous les thèmes fréquents
- ✅ 4 chapitres Automatismes dédiés (Auto_Calcul, Auto_Géométrie, Auto_Littéral, Auto_Stats_Probas)
- ✅ Timer 30s sur automatismes (réflexes)
- ✅ Mix types : QCM + V/F + Fill (trou à compléter)
- ✅ Figures SVG sur Pythagore, Thalès, Trigo
- ✅ 3 types d'exercices correspondent au format brevet (QCM = choix, V/F = affirmations, Fill = réponse directe)

### Ce qu'on pourrait améliorer

| Gap | Détail | Priorité |
|---|---|---|
| **Contextes réels** | Nos exos sont parfois abstraits ("Simplifie √72"). Le brevet contextualise TOUT ("La diagonale d'un écran mesure..."). Plus de situations concrètes. | 🔴 |
| **Exercices multi-étapes** | Le brevet enchaîne 3-5 questions progressives dans un même exercice. Nos exos sont isolés (1 question = 1 exo). Pas bloquant mais différent du format réel. | 🟡 |
| **Rédaction / justification** | Le brevet 2026 donne 2 pts pour la rédaction. Nos exos ne demandent jamais de justifier — c'est du QCM/Fill. Possible coach tip "Au brevet, tu devras écrire : D'après le théorème de Pythagore..." | 🟡 |
| **Scratch / algo visuel** | Le brevet montre des captures Scratch. Nos exos Scratch sont textuels. Ajouter des images de blocs Scratch serait plus réaliste. | 🟡 |
| **Tableaux et graphiques** | Fréquents au brevet (stats, fonctions). Nos exos n'en ont pas (limitation HTML/SVG). | 🔵 |
| **Mode "Brevet Blanc"** | Simuler un vrai brevet : 5 exos, 2h chrono, partie 1 sans calc + partie 2. Existe en squelette mais pas peuplé avec le nouveau format 2026. | 🟡 |

### Format automatismes vs Matheux

| Brevet 2026 | Matheux |
|---|---|
| Réponse directe, pas de justification | ✅ Fill = réponse directe |
| QCM 1 seule réponse | ✅ QCM standard |
| Vrai/Faux | ✅ Type V/F |
| 0,5 ou 1 pt par question | Pas de scoring partiel (EASY/HARD) |
| Sans calculatrice, 20 min | ✅ Timer 30s par exo, pas de calculatrice native |

**Bonne nouvelle** : notre format d'exercices (QCM, V/F, Fill) correspond exactement aux 3 formats de la partie Automatismes du brevet 2026. C'est un argument marketing fort : "Entraîne-toi dans les mêmes conditions que le brevet."

---

## 6. Sujets analysés (sources)

### Sujets officiels 2024
- Métropole (1er juillet) — 5 exos : probas, programme calcul, géométrie Thalès/Pythagore/aires, QCM multi-thèmes, arithmétique/volumes
- Amérique du Nord (29 mai) — 5 exos : QCM médiane/vitesse/probas/homothétie, programme calcul/équations, fonctions affines, Pythagore/volumes, programme calcul
- Centres étrangers (10 juin) — 5 exos : QCM calcul/probas/stats, circuit vitesse/proportionnalité, programme calcul littéral, géométrie Thalès/Pythagore/trigo/homothétie, cône/patron/angles
- Polynésie (27 juin) — 5 exos : QCM triangle/fonction affine/transformation, cocktail proportionnalité, centre aquatique Pythagore/Thalès
- Asie (18 juin) — 5 exos : nombres premiers/patron cube/factorisation/ratio/médiane, Thalès/expériences aléatoires, Pythagore/trigo/aire disque

### Sujets zéro 2026
- Série générale Sujet A et Sujet B (eduscol.education.fr)
- Série professionnelle Sujet A et Sujet B
- Format : partie 1 automatismes (6 pts) + partie 2 raisonnement (14 pts)

### Sources principales
- [APMEP — Brevet 2024](https://www.apmep.fr/Brevet-2024)
- [Math93 — Annales 2024](https://math93.com/annales-du-brevet/1144-annales-du-brevet-de-maths-2024-sujets-et-corriges-de-mathematiques.html)
- [Académie Normandie — DNB 2026](https://mathematiques.ac-normandie.fr/DNB-2026)
- [Nomad Education — Sujets zéro 2026](https://www.nomadeducation.fr/blog/articles/2026-01-15/brevet-2026-les-sujets-0-de-lepreuve-de-mathematiques)
- [Nomad Education — Sujets probables 2026](https://www.nomadeducation.fr/blog/articles/2026-02-27/brevet-2026-sujets-probables-maths)
- [DigiSchool — Automatismes brevet 2026](https://www.digischool.fr/articles/college/brevet/automatisme-mathematiques-brevet/)
- [ProfPower — Automatismes 2026](https://profpower.lelivrescolaire.fr/automatismes-maths-brevet-2026-tout-comprendre-a-la-nouvelle-epreuve/)
- [Eduscol — Liste automatismes (PDF)](https://eduscol.education.fr/document/67781/download)
- [Eduscol — Sujet zéro A (PDF)](https://eduscol.education.fr/document/69067/download)
- [Académie Aix-Marseille — Exercices par thèmes](https://www.pedagogie.ac-aix-marseille.fr/jcms/c_160741/fr/exercices-extraits-des-annales-de-brevet-classes-par-themes)
- [Mathovore — Brevets blancs](https://mathovore.fr/brevet-blanc-de-maths-2025-avec-sujet-et-corrige)
- [Au fil des Maths — Brevets blancs](https://aufildesmaths.fr/diplome-national-du-brevetbrevets-blancs.html)
- [Calcul-brevet.fr — Barème 2026](https://www.calcul-brevet.fr/epreuves-dnb-2026/)
- [pi.ac3j.fr — Tous les brevets corrigés](https://pi.ac3j.fr/brevet/)
