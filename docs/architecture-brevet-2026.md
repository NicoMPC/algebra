# Architecture Brevet 2026 — Matheux

> Document de reference pour la conception des exercices Brevet 2026.
> Couvre le programme complet cycle 4 + la nouveaute Partie 1 Automatismes.
> Cree le 2026-03-27.

---

## 1. TABLEAU MAITRE — Tous les chapitres Brevet

### Conventions

- **Priorite** : 1 = systematique aux annales (100%), 2 = tres frequent (>75%), 3 = regulier (>50%)
- **Volume** : 20 exos standard (4 slots de 5) sauf mention contraire
- **Existant** : chapitres deja dans Curriculum_Officiel 3EME (11 chapitres) ou BrevetExos (15 chapitres, 144 exos)

### Nombres et Calculs

| # | Chapitre Matheux | Priorite | Slots (sous-competences) | Couverture programme |
|---|---|---|---|---|
| N1 | `Fractions_Brevet` | 2 | S1: +/- denominateurs differents, S2: x/div, S3: fraction de fraction + irred., S4: problemes concrets (vitesse, partage) | Fractions completes |
| N2 | `Puissances_Brevet` | 3 | S1: regles a^n x a^m et (a^n)^m, S2: puissances de 10 + notation scientifique, S3: ordres de grandeur + conversions, S4: problemes (distances astro, tailles cellules) | Puissances + notation scientifique |
| N3 | `Racines_Carrees_Brevet` | 3 | S1: definition + sqrt(a^2)=|a|, S2: sqrt(axb)=sqrt(a)xsqrt(b) + simplification, S3: calculs avec radicaux, S4: Pythagore avec racines (lien geometrie) | Racines carrees |
| N4 | `Arithmetique_Brevet` | 3 | S1: nombres premiers + crible, S2: decomposition facteurs premiers, S3: PGCD + applications (partage, pave), S4: problemes croisant divisibilite + PGCD | Arithmetique |
| N5 | `Calcul_Litteral_Brevet` | 1 | S1: developpement simple + double distrib, S2: identites remarquables sens direct, S3: factorisation (facteur commun + IR), S4: programmes de calcul + preuves | Calcul litteral complet |
| N6 | `Equations_Brevet` | 1 | S1: equations 1er degre, S2: mise en equation de problemes, S3: equations produit (apres factorisation), S4: problemes multi-etapes | Equations |
| N7 | `Inequations_Brevet` | 3 | S1: resoudre une inequation, S2: representer sur droite graduee, S3: problemes avec contrainte, S4: lien avec fonctions (signe) | Inequations |

### Fonctions et Proportionnalite

| # | Chapitre Matheux | Priorite | Slots | Couverture |
|---|---|---|---|---|
| F1 | `Fonctions_Brevet` | 1 | S1: image/antecedent + notation, S2: lecture graphique (courbe), S3: tableau de valeurs + courbe, S4: problemes avec fonctions non-lineaires | Fonctions generales |
| F2 | `Fonctions_Affines_Brevet` | 2 | S1: f(x)=ax+b identifier a et b, S2: tracer/lire graphiquement, S3: determiner f(x) depuis 2 points, S4: systemes graphiques (intersection) | Lineaires + affines |
| F3 | `Proportionnalite_Brevet` | 3 | S1: tableaux + coefficient, S2: pourcentages (augmentation/reduction), S3: vitesse/distance/temps, S4: echelles + problemes croises | Proportionnalite + pourcentages |

### Geometrie

| # | Chapitre Matheux | Priorite | Slots | Couverture |
|---|---|---|---|---|
| G1 | `Pythagore_Brevet` | 1 | S1: calculer hypotenuse, S2: calculer un cote de l'angle droit, S3: reciproque (prouver angle droit), S4: problemes dans l'espace (diagonale pave, distance) | Pythagore direct + reciproque |
| G2 | `Thales_Brevet` | 1 | S1: calculer une longueur (config triangle), S2: calculer une longueur (config papillon), S3: reciproque (prouver parallelisme), S4: problemes concrets (ombre, maquette) | Thales direct + reciproque |
| G3 | `Trigonometrie_Brevet` | 2 | S1: calculer un cote (cos/sin/tan), S2: calculer un angle, S3: choisir le bon ratio, S4: problemes (hauteur arbre, angle elevation, pente) | Trigonometrie |
| G4 | `Geometrie_Espace_Brevet` | 3 | S1: volumes (cone, sphere, pyramide, cylindre), S2: sections planes, S3: patrons + aire laterale, S4: problemes croises (volume + Pythagore) | Geometrie espace |
| G5 | `Transformations_Brevet` | 3 | S1: homothetie (centre, rapport, image), S2: agrandissement/reduction (rapport k, aires, volumes), S3: rappels symetries + translation, S4: compositions | Transformations |

### Statistiques et Probabilites

| # | Chapitre Matheux | Priorite | Slots | Couverture |
|---|---|---|---|---|
| S1 | `Statistiques_Brevet` | 2 | S1: moyenne (simple + ponderee), S2: mediane + etendue, S3: quartiles + boite a moustaches, S4: lecture diagrammes + interpretation | Statistiques |
| S2 | `Probabilites_Brevet` | 2 | S1: vocabulaire + P(A) simple, S2: arbre a 2 epreuves, S3: tableau double entree, S4: problemes contexualises | Probabilites |

### Algorithmique

| # | Chapitre Matheux | Priorite | Slots | Couverture |
|---|---|---|---|---|
| A1 | `Scratch_Brevet` | 1 | S1: lire un script (predire resultat), S2: variables + boucles, S3: conditions (si/sinon), S4: modifier/completer un script | Scratch/Algo |

### Automatismes (NOUVEAU — Partie 1)

| # | Chapitre Matheux | Priorite | Slots | Couverture |
|---|---|---|---|---|
| AT1 | `Auto_Calcul` | 1 | S1: calcul mental (+/-/x entiers), S2: fractions simples, S3: puissances de 10 + ecriture scientifique, S4: racines carrees simples | Automatismes numeriques |
| AT2 | `Auto_Litteral` | 1 | S1: substitution rapide, S2: developper/factoriser mental, S3: identifier IR, S4: resoudre equation simple de tete | Automatismes algebriques |
| AT3 | `Auto_Geometrie` | 1 | S1: reconnaitre config Pythagore/Thales, S2: formules volumes/aires, S3: cos/sin/tan choix rapide, S4: lecture figure (angles, longueurs) | Automatismes geometriques |
| AT4 | `Auto_Stats_Probas` | 2 | S1: lire un graphique, S2: calculer moyenne/mediane rapide, S3: probabilite simple, S4: pourcentages de tete | Automatismes stats/probas |

**TOTAL : 22 chapitres = 440 exercices**

Couverture programme : 100% du cycle 4. Chaque notion du programme 3eme est couverte par au moins un chapitre.

---

## 2. MATRICE TYPES x CHAPITRES

| Chapitre | QCM | V/F | Fill | Justification |
|---|---|---|---|---|
| `Fractions_Brevet` | 8 | 4 | 8 | Fill pour calcul direct (resultat exact). V/F pour fausses regles ("on additionne les denominateurs"). QCM pour choix de methode |
| `Puissances_Brevet` | 8 | 6 | 6 | V/F ideal pour regles (a^0=1, a^-n=1/a^n — vrai ou faux ?). Fill pour notation scientifique (resultat exact) |
| `Racines_Carrees_Brevet` | 8 | 4 | 8 | Fill pour simplification (reponse exacte). V/F pour sqrt(a+b)=sqrt(a)+sqrt(b) (FAUX — piege classique) |
| `Arithmetique_Brevet` | 8 | 4 | 8 | Fill pour decomposition + PGCD (resultat unique). QCM pour identification nombres premiers |
| `Calcul_Litteral_Brevet` | 6 | 4 | 10 | Fill dominant : developper/factoriser = resultat exact a ecrire. V/F pour pieges IR |
| `Equations_Brevet` | 6 | 2 | 12 | Fill largement dominant : resoudre = trouver x. QCM pour mise en equation (choisir la bonne equation) |
| `Inequations_Brevet` | 8 | 4 | 8 | QCM pour representation graphique (choisir la bonne droite). Fill pour resolution |
| `Fonctions_Brevet` | 10 | 4 | 6 | QCM dominant : lecture graphique = choisir la bonne valeur. V/F pour proprietes (croissance, parite) |
| `Fonctions_Affines_Brevet` | 8 | 4 | 8 | Fill pour calculer a et b. QCM pour reconnaissance graphique. V/F pour "f est lineaire" |
| `Proportionnalite_Brevet` | 8 | 4 | 8 | Fill pour calcul pourcentage/coefficient. V/F pour "ce tableau est proportionnel". QCM pour methode |
| `Pythagore_Brevet` | 6 | 4 | 10 | Fill dominant : calculer = resultat numerique. V/F pour reciproque ("ce triangle est-il rectangle ?") |
| `Thales_Brevet` | 6 | 4 | 10 | Fill pour calcul longueur. V/F pour reciproque ("les droites sont-elles paralleles ?"). QCM config |
| `Trigonometrie_Brevet` | 8 | 4 | 8 | QCM pour choix du ratio (cos vs sin vs tan). Fill pour calcul. V/F pour pieges (cos(A)=adj/hyp) |
| `Geometrie_Espace_Brevet` | 10 | 4 | 6 | QCM pour choix formule volume. Fill pour calcul. V/F pour sections ("la section est un rectangle") |
| `Transformations_Brevet` | 10 | 6 | 4 | QCM dominant : identifier l'image, le rapport. V/F pour proprietes (conserve angles, aires x k^2) |
| `Statistiques_Brevet` | 8 | 4 | 8 | Fill pour moyenne/mediane (valeur exacte). QCM pour lecture diagramme. V/F pour interpretation |
| `Probabilites_Brevet` | 8 | 4 | 8 | Fill pour P(A) (fraction exacte). QCM pour arbre/tableau. V/F pour equiprobabilite |
| `Scratch_Brevet` | 12 | 4 | 4 | QCM ultra-dominant : "Que vaut x apres ce script ?" = choix parmi 3 resultats. V/F pour "la boucle s'arrete" |
| `Auto_Calcul` | 4 | 2 | 14 | Fill massif : automatismes = reponse directe, pas de choix. Le QCM donne la reponse |
| `Auto_Litteral` | 4 | 4 | 12 | Fill massif + V/F pour "cette egalite est-elle vraie ?" (rapidite de jugement) |
| `Auto_Geometrie` | 8 | 6 | 6 | V/F fort : "Ce triangle est rectangle" (Pythagore rapide). QCM pour formules volumes |
| `Auto_Stats_Probas` | 6 | 4 | 10 | Fill pour lecture rapide + calcul mental. QCM pour graphiques |

### Regles degagees

**QCM pertinent quand :**
- Reconnaissance visuelle (graphiques, figures, scripts Scratch)
- Choix entre methodes (cos vs sin, Pythagore vs Thales)
- L'erreur est dans le raisonnement, pas dans le calcul

**V/F pertinent quand :**
- Fausses croyances a debusquer (sqrt(a+b)=sqrt(a)+sqrt(b), on additionne les denominateurs)
- Reciproques (Pythagore, Thales)
- Proprietes (lineaire vs affine, proportionnel vs non)

**Fill pertinent quand :**
- Le resultat est un nombre ou une expression exacte
- L'exercice teste la fluence de calcul (automatismes)
- La reponse ne peut pas etre "devinee" parmi des options

**CONTRE-PRODUCTIF :**
- QCM sur les automatismes (donne la reponse, tue le but de la Partie 1)
- Fill sur Scratch (trop de reponses possibles, normalisation fragile)
- V/F sur les equations (pas de piege naturel en vrai/faux pour x=3)

---

## 3. GRILLE DECISIONNELLE STEPS / FORMULE / FIGURE

| Situation | Steps | Combien | Formule (f) | Figure (fig) |
|---|---|---|---|---|
| **Automatisme simple** (calcul mental) | 1 seul step | 1 | `""` (vide) — pas de formule, c'est le but | Non |
| **Automatisme avec methode** (identifier IR) | 1-2 steps | 1-2 | `""` | Non |
| **Calcul standard** (Pythagore, equation) | 3 steps classiques | 3 | Affichee | Oui si geometrie |
| **Reciproque** (Pythagore, Thales) | 3 steps avec conclusion | 3 | Affichee | Oui |
| **Probleme contextualise** | 3 steps : extraction, calcul, conclusion | 3 | Affichee | Si geometrie |
| **Lecture graphique** | 2 steps : reperer, lire | 2 | `""` | Non (pas de SVG graphique dispo) |
| **Scratch/Algo** | 2-3 steps : tracer l'execution | 2-3 | `""` | Non |
| **Identites remarquables** | 3 steps | 3 | Masquee (test restitution) sur S2-S3, affichee sur S1 | Non |
| **Statistiques** (moyenne, mediane) | 2-3 steps | 2-3 | Affichee | Non |
| **Probabilites** (arbre) | 3 steps | 3 | `$P(A) = \\frac{\\text{cas favorables}}{\\text{cas possibles}}$` | Non |

### Cas speciaux detailles

**Automatismes (AT1-AT4) :**
- 0 ou 1 step maximum. L'objectif est la rapidite, pas la methode.
- Step unique = reformulation minimale ("$7^2$ signifie $7 \\times 7$")
- Jamais de formule. Si l'eleve a besoin de la formule, ce n'est plus un automatisme.
- Timer fortement recommande (timer actif par defaut, 30s au lieu de 60s si possible via config future)

**Geometrie (G1-G5) :**
- Figure SVG systematique sauf si l'enonce est purement calculatoire
- Types disponibles : `tri_rect` (Pythagore), `tri_trigo` (Trigo), `thales` (Thales), `cube3d` (espace), `parallel` (paralleles)
- Toujours utiliser `"fig"` dans le JSON avec les parametres adaptes

**Identites remarquables :**
- Slot 1 : formule affichee (confiance)
- Slots 2-3 : formule masquee (`"f": ""`) pour tester la restitution — c'est un objectif Brevet
- Slot 4 : formule masquee aussi (synthese)

---

## 4. STRATEGIE MULTI-ETAPES

Le Brevet pose des exercices a 3-4 sous-questions guidees. Matheux ne supporte qu'une question par exercice. Deux techniques pour simuler l'experience.

### Technique 1 : Fil narratif

Meme contexte sur un slot entier. Chaque exo est une etape du meme probleme.

**Exemple — Pythagore dans un jardin (slot 4, exos 16-20) :**

- Exo 16 : "Lucas amenage un jardin rectangulaire ABCD de longueur $12$ m et largeur $5$ m. Calcule la diagonale $AC$." (Pythagore direct)
- Exo 17 : "Lucas veut placer une cloture le long de la diagonale. Il a $14$ m de grillage. Est-ce suffisant ?" (V/F, comparaison)
- Exo 18 : "Le triangle ABM, ou M est le milieu de [BC], est-il rectangle ?" (Reciproque, BM=2.5, AB=12, AM=?)
- Exo 19 : "Lucas decoupe un triangle rectangle dans un coin du jardin pour faire un potager. L'hypotenuse mesure $\\sqrt{50}$ m. Simplifie cette racine." (Lien racines carrees)
- Exo 20 : "L'aire du potager triangulaire est de $12{,}5$ m$^2$. Si un cote mesure $5$ m, quelle est la hauteur correspondante ?" (Synthese aire + contexte)

**Regle** : chaque exo est autonome (on peut repondre sans les precedents) mais le contexte cree une coherence narrative.

### Technique 2 : Zoom progressif

Meme notion, chaque exo ajoute une couche de difficulte.

**Exemple — Thales (slot 2, exos 6-10) :**

- Exo 6 : Config triangle simple, calculer une longueur. Valeurs entieres.
- Exo 7 : Config triangle, calculer une longueur. Valeurs fractionnaires.
- Exo 8 : Config papillon, calculer une longueur.
- Exo 9 : Config papillon, deux longueurs a trouver (une seule demandee, mais les donnees sont plus nombreuses).
- Exo 10 : Probleme concret (ombre d'un poteau) avec config Thales implicite.

**Regle** : la competence-coeur est la meme, mais la complexite technique monte graduellement.

### Quand utiliser quelle technique ?

| Technique | Quand | Chapitres concernes |
|---|---|---|
| Fil narratif | Slot 4 (synthese) de tout chapitre geometrique ou fonctions | G1-G5, F1-F2 |
| Zoom | Slots 1-3 de tout chapitre technique | Tous |
| Mix | Slot 4 de chapitres non-geometriques | N1-N7, S1-S2, A1 |

---

## 5. ARCHITECTURE MODE AUTOMATISMES

### Decision : chapitres dedies, pas integres

Les automatismes sont des chapitres a part (AT1-AT4), pas melanges dans les chapitres classiques. Raisons :

1. **Timer different** — les automatismes doivent etre rapides (objectif <30s/exo), les chapitres classiques tolerent 2min
2. **Pas de steps** — fondamentalement different du workflow "indices progressifs"
3. **Pas de formule** — le but est que l'eleve SACHE la formule, pas qu'on la lui donne
4. **Mode d'entrainement distinct** — un eleve peut faire des sessions "automatismes" de 5min le matin, independamment des chapitres

### Format recommande

```json
{
  "lvl": 1,
  "type": "fill",
  "q": "Calcule : $\\frac{3}{4} + \\frac{1}{6} = $ ___",
  "a": "11/12",
  "options": [],
  "steps": ["Denominateur commun : $12$. On obtient $\\frac{9}{12} + \\frac{2}{12} = $ ?"],
  "f": ""
}
```

Caracteristiques :
- **Fill dominant** (70%+) — pas de QCM qui donne la reponse
- **1 step max** — reformulation ou calcul intermediaire, jamais la reponse
- **f vide** — toujours
- **Enonce court** — 1 phrase, pas de contexte narratif (sauf AT4 lecture graphique)
- **Reponse normalisable** — nombres, fractions simples (`a/b`), expressions courtes

### Les 4 chapitres Automatismes detailles

**AT1 — Auto_Calcul (20 exos)**
- S1 : Calcul mental entiers (additions, multiplications, carres, cubes)
- S2 : Fractions simples (+ - x div, meme denominateur puis different)
- S3 : Puissances de 10 (3,5 x 10^4 = ?, ecriture scientifique)
- S4 : Racines carrees (sqrt(49), sqrt(12) simplifie, sqrt(a)xsqrt(b))

**AT2 — Auto_Litteral (20 exos)**
- S1 : Substitution (si x=3, que vaut 2x+5 ?)
- S2 : Developper/factoriser de tete (3(x+2), x^2-9)
- S3 : Identifier une IR ((x+3)^2 = ?, est-ce (a+b)^2 ?)
- S4 : Resoudre equation simple (2x+1=7, 3x=-12)

**AT3 — Auto_Geometrie (20 exos)**
- S1 : Reconnaitre si Pythagore applicable (triangle rectangle ?)
- S2 : Formules volumes/aires (V sphere = ?, A disque = ?)
- S3 : Cos, sin ou tan ? (quel ratio pour tel cote ?)
- S4 : Lecture figure (lire un angle, une longueur, identifier un triangle)

**AT4 — Auto_Stats_Probas (20 exos)**
- S1 : Lire un diagramme (baton, circulaire — "combien de ...")
- S2 : Moyenne rapide (3 valeurs, 5 valeurs)
- S3 : Probabilite simple (P = cas fav / cas total)
- S4 : Pourcentages (20% de 150, augmenter de 30%)

---

## 6. 10 EXERCICES EXEMPLES

### Calcul — Automatisme

```json
{
  "lvl": 1,
  "type": "fill",
  "q": "Ecris $0{,}00042$ en notation scientifique : ___",
  "a": "$4{,}2 \\times 10^{-4}$",
  "options": [],
  "steps": ["On deplace la virgule de $4$ rangs vers la droite pour obtenir $4{,}2$, donc l'exposant est $-4$."],
  "f": ""
}
```

### Calcul — Raisonnement

```json
{
  "lvl": 1,
  "q": "Lena veut simplifier $\\sqrt{75}$. Quel est le resultat ?",
  "a": "$5\\sqrt{3}$",
  "options": ["$5\\sqrt{3}$", "$3\\sqrt{5}$", "$25\\sqrt{3}$"],
  "steps": [
    "On cherche le plus grand carre parfait qui divise $75$ : $75 = 25 \\times 3$.",
    "$\\sqrt{75} = \\sqrt{25 \\times 3} = \\sqrt{25} \\times \\sqrt{3} = 5\\sqrt{3}$.",
    "Le resultat simplifie est $5\\sqrt{3}$."
  ],
  "f": "$\\sqrt{a \\times b} = \\sqrt{a} \\times \\sqrt{b}$"
}
```

### Geometrie — Automatisme

```json
{
  "lvl": 1,
  "type": "vf",
  "q": "Un triangle a pour cotes $6$ cm, $8$ cm et $10$ cm. Ce triangle est rectangle.",
  "a": "Vrai",
  "options": ["Vrai", "Faux"],
  "steps": ["$6^2 + 8^2 = 36 + 64 = 100$ et $10^2 = 100$. L'egalite de Pythagore est verifiee."],
  "f": ""
}
```

### Geometrie — Raisonnement

```json
{
  "lvl": 1,
  "q": "Dans un triangle $ABC$ rectangle en $A$, $AB = 7$ cm et $\\widehat{ABC} = 35°$. Calcule $AC$ (arrondi au dixieme).",
  "a": "$4{,}9$ cm",
  "options": ["$4{,}9$ cm", "$5{,}7$ cm", "$10{,}0$ cm"],
  "steps": [
    "On cherche le cote oppose ($AC$) a l'angle $\\widehat{ABC}$ en connaissant le cote adjacent ($AB$). On utilise $\\tan$.",
    "$\\tan(35°) = \\frac{AC}{AB} = \\frac{AC}{7}$, donc $AC = 7 \\times \\tan(35°)$.",
    "$AC = 7 \\times 0{,}7002 \\approx 4{,}9$ cm."
  ],
  "f": "$\\tan(\\alpha) = \\frac{\\text{oppose}}{\\text{adjacent}}$",
  "fig": {"t": "tri_trigo", "pts": ["A","B","C"], "sides": [7, null, null], "angles": [90, 35, 55], "unknown": "AC"}
}
```

### Fonctions — Automatisme

```json
{
  "lvl": 1,
  "type": "fill",
  "q": "Si $f(x) = 3x - 2$, alors $f(4) = $ ___",
  "a": "10",
  "options": [],
  "steps": ["$f(4) = 3 \\times 4 - 2 = 12 - 2 = $ ?"],
  "f": ""
}
```

### Fonctions — Raisonnement

```json
{
  "lvl": 2,
  "q": "La fonction $f$ est definie par $f(x) = -2x + 5$. Pour quelle valeur de $x$ a-t-on $f(x) = 0$ ?",
  "a": "$\\frac{5}{2}$",
  "options": ["$\\frac{5}{2}$", "$-\\frac{5}{2}$", "$\\frac{2}{5}$"],
  "steps": [
    "On cherche l'antecedent de $0$ : on resout $-2x + 5 = 0$.",
    "$-2x = -5$, donc $x = \\frac{-5}{-2} = \\frac{5}{2}$.",
    "$f\\left(\\frac{5}{2}\\right) = -2 \\times \\frac{5}{2} + 5 = -5 + 5 = 0$. Verifie."
  ],
  "f": "$f(x) = ax + b$"
}
```

### Stats/Probas — Automatisme

```json
{
  "lvl": 1,
  "type": "fill",
  "q": "On lance un de equilibre a $6$ faces. Quelle est la probabilite d'obtenir un nombre pair ? ___",
  "a": "1/2",
  "options": [],
  "steps": ["$3$ faces paires ($2, 4, 6$) sur $6$ faces au total : $P = \\frac{3}{6} = $ ?"],
  "f": ""
}
```

### Stats/Probas — Raisonnement

```json
{
  "lvl": 1,
  "q": "Dans une classe de $30$ eleves, la moyenne en maths est $12{,}5$. Les $18$ filles ont une moyenne de $13$. Quelle est la moyenne des garcons ?",
  "a": "$11{,}75$",
  "options": ["$11{,}75$", "$12$", "$11{,}5$"],
  "steps": [
    "Total points classe : $30 \\times 12{,}5 = 375$. Total points filles : $18 \\times 13 = 234$.",
    "Total points garcons : $375 - 234 = 141$. Il y a $30 - 18 = 12$ garcons.",
    "Moyenne garcons : $\\frac{141}{12} = 11{,}75$."
  ],
  "f": "$\\bar{x} = \\frac{\\sum x_i}{n}$"
}
```

### Algo — Automatisme

```json
{
  "lvl": 1,
  "q": "Un script Scratch initialise $x$ a $2$, puis repete $3$ fois : $x \\leftarrow x \\times 2 + 1$. Que vaut $x$ a la fin ?",
  "a": "$23$",
  "options": ["$23$", "$15$", "$21$"],
  "steps": [
    "Tour 1 : $x = 2 \\times 2 + 1 = 5$. Tour 2 : $x = 5 \\times 2 + 1 = 11$.",
    "Tour 3 : $x = 11 \\times 2 + 1 = 23$.",
    "$x = 23$ apres les $3$ repetitions."
  ],
  "f": ""
}
```

### Algo — Raisonnement

```json
{
  "lvl": 2,
  "q": "Un programme Scratch demande un nombre $n$, puis calcule $n^2 - 4n + 4$. Pour $n = 5$, Hugo dit que le programme affiche $9$ car c'est $(5-2)^2$. A-t-il raison ?",
  "a": "Vrai",
  "options": ["Vrai", "Faux"],
  "type": "vf",
  "steps": [
    "On calcule : $5^2 - 4 \\times 5 + 4 = 25 - 20 + 4 = 9$.",
    "On reconnait $n^2 - 4n + 4 = (n - 2)^2$. Pour $n = 5$ : $(5-2)^2 = 3^2 = 9$.",
    "Hugo a raison : le programme calcule $(n-2)^2$, ici $9$."
  ],
  "f": ""
}
```

---

## 7. RESUME EN CLAIR

1. **22 chapitres** couvrent 100% du programme Brevet 2026, avec 4 chapitres dedies aux automatismes (Partie 1, 6 points) qui sont le vrai differenciateur commercial de Matheux.

2. Les automatismes utilisent massivement le format **Fill sans formule et avec 1 step max** — l'objectif est la rapidite et la restitution, pas le guidage. C'est fondamentalement different des chapitres classiques.

3. Les exercices Brevet multi-etapes sont mappes sur des **slots a fil narratif** (meme contexte, 5 questions = 5 etapes) ou par **zoom progressif** (meme competence, difficulte croissante).

4. Le mix QCM/VF/Fill est adapte par chapitre : Fill dominant pour le calcul, QCM pour la reconnaissance/lecture, V/F pour debusquer les fausses croyances et tester les reciproques.

5. Les 18 chapitres classiques + 4 automatismes representent **440 exercices** a generer progressivement, en commencant par les priorite 1 (Pythagore, Thales, Calcul Litteral, Equations, Fonctions, Scratch, Auto_Calcul, Auto_Litteral, Auto_Geometrie).

---

## Historique

| Date | Changement |
|---|---|
| 2026-03-27 | Creation — architecture complete Brevet 2026 |
