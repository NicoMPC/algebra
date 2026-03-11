# Brief Landing Page — Matheux
> Destiné à Claude Code pour coder `landing.html`. Fichier à lire en entier avant de coder. Chaque section est utilisable directement.

---

## Contexte projet

- **Produit :** Matheux — outil pédagogique maths collège (6ème→3ème), SPA vanilla JS
- **Fondateur :** Nicolas, prof de maths solo
- **Cible :** parents d'élèves 11-15 ans cherchant à améliorer les résultats en maths
- **Modèle :** freemium 7 jours → 9,99 €/mois
- **Stack existant :** vanilla JS, Tailwind CDN, CSS vars définis dans `index.html`, fonts Syne + DM Sans

---

## 1. Structure exacte de la page

La page se lit de haut en bas sans scrolljack ni parallax. Chaque section a un seul objectif.

---

### Section 1 — Hero (above the fold)

| Champ | Contenu |
|---|---|
| **Objectif** | Capter l'attention en moins de 3 secondes. Faire comprendre qui c'est, pour qui, et pourquoi agir maintenant. |
| **Titre** | Voir § Copywriting — Headline variante A ou B |
| **Sous-titre** | Voir § Copywriting — Sous-titre |
| **CTA principal** | Bouton unique, pleine largeur sur mobile. Voir § Copywriting — CTA |
| **Micro-copie sous CTA** | "7 jours offerts · Sans carte bancaire" |
| **Badge de confiance** | Pill en haut : point vert animé + "Assistant Mathématiques IA" |
| **Élément visuel** | Fond sombre (`#07090f`) avec overlay grille CSS (déjà dans index.html : `.lhero` + `.grid-ov`). Pas d'image. Pas d'illustration. |
| **Hauteur** | 100vh sur mobile. Le CTA doit être visible sans scroller. |

---

### Section 2 — Problème (douleur des parents)

| Champ | Contenu |
|---|---|
| **Objectif** | Nommer la frustration exacte du parent avant de proposer quoi que ce soit. |
| **Tag** | Pill indigo : "Le vrai problème" |
| **Titre** | "Ce n'est pas un problème de travail. C'est un problème de direction." |
| **Contenu** | Deux cartes côte à côte (stacked sur mobile) : "Sans Matheux" (3 points négatifs) vs "Avec Matheux" (3 points positifs). Utiliser les classes `.ccard.bad` et `.ccard.good` déjà définies. |
| **Points "Sans"** | ✕ Révise ce qu'il sait déjà / ✕ Oublie avant l'examen / ✕ Les lacunes s'accumulent en silence |
| **Points "Avec"** | ✓ Diagnostic précis par niveau et par chapitre / ✓ L'IA cible les vraies erreurs / ✓ Remédiation automatique le lendemain |
| **Élément visuel** | Fond blanc (`#fff`). Accent rouge sur la carte "Sans", accent vert sur "Avec". |

---

### Section 3 — Solution (comment Matheux résout le problème)

| Champ | Contenu |
|---|---|
| **Objectif** | Expliquer le mécanisme produit en une lecture de 15 secondes. Pas de jargon. |
| **Tag** | Pill indigo : "Comment ça marche" |
| **Titre** | "L'IA qui sait exactement où votre enfant est bloqué." |
| **Contenu** | 3 blocs en colonne (icône + titre + phrase). Voir détail ci-dessous. |
| **Bloc 1** | Icône : 🔍 / Titre : "Diagnostic de lacunes" / Texte : "En 8 questions, Matheux identifie précisément les notions non maîtrisées — pas juste le chapitre, mais le type d'erreur." |
| **Bloc 2** | Icône : ⚡ / Titre : "Boost quotidien ciblé" / Texte : "Chaque jour, 5 exercices calibrés sur les vraies difficultés du moment. 15 minutes suffisent." |
| **Bloc 3** | Icône : 📈 / Titre : "Rapport de progression" / Texte : "Le parent voit l'évolution réelle : score de confiance par chapitre, séries, notions maîtrisées." |
| **Élément visuel** | Fond légèrement teinté (`var(--bg)` = `#f7f8fc`). Icônes dans un carré arrondi indigo. |

---

### Section 4 — Demo / Screenshots

| Champ | Contenu |
|---|---|
| **Objectif** | Montrer le produit réel. Ancrer la confiance par la preuve visuelle. |
| **Tag** | Pill indigo : "Le produit" |
| **Titre** | "Voici ce que voit votre enfant chaque jour." |
| **Contenu** | 3 mockups en carrousel horizontal scrollable (mobile) ou 3 colonnes (desktop). |
| **Mockup 1** | Capture écran : vue chapitres avec anneaux de maîtrise (mastery ring SVG). Légende : "Tous les chapitres du programme collège" |
| **Mockup 2** | Capture écran : exercice QCM avec options colorées. Légende : "Exercices adaptés au niveau" |
| **Mockup 3** | Capture écran : vue Progression avec barre de confiance. Légende : "Progression visible en temps réel" |
| **Fallback si pas de captures** | 3 placeholders gris anthracite 320×580px avec légendes — les remplacer par de vraies captures dès que possible. |
| **Élément visuel** | Fond blanc. Mockups avec ombre douce (`box-shadow: 0 8px 40px rgba(0,0,0,.12)`). Bord arrondi 22px. |

---

### Section 5 — Fonctionnement en 3 étapes

| Champ | Contenu |
|---|---|
| **Objectif** | Rassurer sur la simplicité. Répondre à "oui mais comment on commence ?" |
| **Tag** | Pill indigo : "En 3 minutes" |
| **Titre** | "Prêt à démarrer. Vraiment." |
| **Étape 1** | Numéro "01" / Titre : "Je m'inscris" / Texte : "Prénom, email, niveau de classe. Aucune carte bancaire." |
| **Étape 2** | Numéro "02" / Titre : "Le diagnostic" / Texte : "8 questions pour cartographier les lacunes. Résultats immédiats." |
| **Étape 3** | Numéro "03" / Titre : "Je progresse" / Texte : "Boost quotidien de 15 minutes. L'IA adapte chaque jour." |
| **Connecteur** | Ligne verticale pointillée entre les étapes (CSS `border-left: 2px dashed var(--brd)`). |
| **CTA en bas** | Bouton secondaire : "Faire le diagnostic gratuit →" |
| **Élément visuel** | Fond blanc. Numéros en gros (Syne, couleur `var(--p)`). |

---

### Section 6 — Social proof

| Champ | Contenu |
|---|---|
| **Objectif** | Réduire le risque perçu. Montrer que d'autres ont essayé et que ça marche. |
| **Tag** | Pill indigo : "Ils l'ont testé" |
| **Titre** | "Les premiers retours." |
| **Chiffres** | 3 pills stat en ligne : "480 exercices dans la base" / "Créé par un prof de maths" / "7 jours gratuits" |
| **Témoignages** | 2 cartes témoignage (voir § Social proof — template). Placeholders prêts à remplir. |
| **Format carte** | Citation en italique + prénom + rôle (ex. "Mère de Lucas, 5ème") + étoiles (★★★★★). |
| **Élément visuel** | Fond `#f7f8fc`. Cartes blanches avec ombre légère. |

---

### Section 7 — Pricing

| Champ | Contenu |
|---|---|
| **Objectif** | Éliminer toute friction financière. Une seule offre, une seule décision. |
| **Tag** | Pill indigo : "Tarif" |
| **Titre** | "Un tarif. Aucune surprise." |
| **Carte unique** | Fond indigo sombre (`var(--pd)`). Texte blanc. |
| **Prix** | "9,99 € / mois" — grand, Syne, blanc |
| **Période d'essai** | Badge ambre en haut de carte : "7 jours gratuits — sans carte bancaire" |
| **Liste inclus** | ✓ Diagnostic de lacunes complet / ✓ Boost quotidien adaptatif / ✓ Suivi de progression / ✓ Remédiation automatique / ✓ Tous les niveaux 6ème → 3ème |
| **CTA dans la carte** | "Commencer gratuitement →" — bouton blanc, texte indigo |
| **Sous-carte** | "Annulation à tout moment. Aucun engagement." — petit, centré, gris clair |
| **Élément visuel** | Carte centrée, max-width 400px. Glow subtil indigo autour de la carte. |

---

### Section 8 — FAQ

| Champ | Contenu |
|---|---|
| **Objectif** | Lever les 5 objections les plus fréquentes avant qu'elles bloquent. |
| **Tag** | Pill indigo : "Questions fréquentes" |
| **Titre** | "On répond à vos questions." |
| **Format** | Accordéon (details/summary HTML natif). Une question à la fois ouverte. |
| **Élément visuel** | Fond blanc. Séparateurs fins (`var(--brd)`). |

**Questions et réponses :**

**Q1 : Est-ce adapté à tous les niveaux ?**
Oui. Matheux couvre les 4 niveaux du collège : 6ème, 5ème, 4ème et 3ème. Le diagnostic initial adapte automatiquement les exercices au niveau réel de votre enfant, pas seulement à sa classe.

**Q2 : Combien de temps faut-il y consacrer chaque jour ?**
15 minutes suffisent. Le boost quotidien est conçu pour tenir dans un trajet de bus ou une pause après l'école. L'application s'adapte à la disponibilité, pas l'inverse.

**Q3 : En quoi c'est différent d'une application de révision classique ?**
La plupart des applications proposent des exercices aléatoires. Matheux commence par un diagnostic pour identifier les lacunes précises, puis génère un parcours ciblé. Votre enfant ne révise que ce qu'il ne maîtrise pas encore.

**Q4 : Puis-je suivre la progression de mon enfant ?**
Oui. La vue Progression affiche le score de confiance par chapitre, la date de dernière pratique et le statut de maîtrise. Un rapport est généré chaque matin pour les élèves actifs.

**Q5 : Que se passe-t-il après les 7 jours gratuits ?**
Un email vous prévient avant la fin de la période d'essai. Vous pouvez continuer à 9,99 €/mois ou arrêter sans aucune démarche compliquée. Aucune carte bancaire n'est demandée à l'inscription.

---

### Section 9 — CTA final

| Champ | Contenu |
|---|---|
| **Objectif** | Dernière chance de convertir. Répéter la proposition de valeur + réduire l'hésitation. |
| **Fond** | Sombre (`var(--ink)`) avec overlay grille (même style que le Hero). |
| **Titre** | "Votre enfant peut progresser. Il manque juste le bon outil." |
| **Sous-titre** | "Diagnostic gratuit en 3 minutes. Sans carte bancaire." |
| **CTA** | Bouton gradient indigo pleine largeur (mobile) : "Démarrer le diagnostic gratuit →" |
| **Micro-copie** | "7 jours offerts · 9,99 €/mois ensuite · Annulable à tout moment" |
| **Élément visuel** | Même traitement que le Hero. Consistance visuelle volontaire. |

---

## 2. Copywriting prêt à l'emploi

### Headlines principales (test A/B)

**Variante A — angle frustration parent :**
> "Arrêtez de chercher pourquoi il bloque."

Sous-titre A : "Matheux diagnostique les lacunes invisibles et programme les révisions exactes dont votre enfant a besoin."

**Variante B — angle transformation résultat :**
> "En maths, travailler plus ne suffit pas."

Sous-titre B : "Matheux identifie ce qui bloque vraiment et crée un programme sur mesure. 15 minutes par jour."

---

### Sous-titre (version courte pour Hero — max 20 mots)

> "Diagnostic de lacunes, exercices ciblés, progression visible. 15 minutes par jour suffisent."

---

### 3 arguments parents

**1. Vous savez enfin où il bloque**
Plus besoin de deviner. Le diagnostic initial donne une carte précise des notions non maîtrisées, chapitre par chapitre.

**2. Son temps de travail est rentabilisé**
Fini les révisions au hasard. Chaque session de 15 minutes cible exactement ce qui freine les notes.

**3. Vous suivez sa progression sans l'interroger**
La vue parent affiche le score de confiance, les chapitres maîtrisés et les alertes de lacunes. En un coup d'œil.

---

### 3 arguments élèves

**1. Plus de temps gâché sur ce que tu sais déjà**
Le boost quotidien est personnalisé sur tes vraies erreurs du jour. 5 exercices, pas plus.

**2. Tu vois que tu progresses**
L'anneau de maîtrise par chapitre et le score de confiance bougent en temps réel. Le progrès devient visible.

**3. Tu n'es jamais seul face à un exercice**
Indices progressifs, formule à débloquer, explication après chaque erreur. L'aide arrive exactement quand tu en as besoin.

---

### CTA principal — 2 variantes

| Variante | Texte bouton | Usage recommandé |
|---|---|---|
| A | "Démarrer le diagnostic gratuit →" | Hero, CTA final |
| B | "Commencer gratuitement →" | Section Pricing |

Choisir la variante A pour le Hero : l'action "diagnostic" est plus concrète qu'un "commencer" générique. Elle réduit l'abstraction et augmente la confiance.

---

## 3. Script vidéo démo 30 secondes

Ton : sobre, factuel. Pas de voix off commerciale. Texte à l'écran uniquement. Musique : lo-fi légère, volume bas. Montrer l'interface réelle.

| Timing | Visuel à l'écran | Texte à l'écran |
|---|---|---|
| 0–2s | Logo Matheux sur fond sombre, point vert animé | — |
| 2–6s | Écran diagnostic : 8 questions défilent rapidement, options colorées | "8 questions pour cartographier les lacunes." |
| 6–10s | Résultats diagnostic : liste de chapitres avec score de confiance (barres rouge/ambre/vert) | "Voici exactement où il bloque." |
| 10–15s | Vue chapitres : anneaux de maîtrise SVG, un élève tape sur un chapitre | — |
| 15–19s | Exercice QCM : question avec LaTeX rendu, l'élève choisit une mauvaise réponse | — |
| 19–23s | Après l'erreur : indices s'affichent, formule se débloque, explication apparaît | "Il comprend pourquoi il s'est trompé." |
| 23–26s | Insight boost du lendemain : message "Tu as eu du mal sur les fractions aujourd'hui. Voici 5 exercices pour demain." | Texte affiché tel quel, aucune VO |
| 26–28s | Vue Progression : barre de confiance qui monte, badge "Maîtrisé" sur un chapitre | "La progression devient visible." |
| 28–30s | Logo + CTA : "Diagnostic gratuit → matheux.fr" sur fond sombre | — |

**Note de réalisation :** capturer directement dans Chrome DevTools (390px, mode mobile). Pas de mise en scène. La vraie interface est le meilleur argument.

---

## 4. Social proof minimaliste

### Chiffres à afficher dès le lancement (sans mentir)

```
480 exercices dans la base       ← vrai (Curriculum_Officiel)
Créé par un prof de maths        ← vrai (Nicolas, 8 ans d'expérience)
6ème → 3ème                      ← vrai (scope collège complet)
```

Ne pas afficher de nombre d'utilisateurs tant qu'il est inférieur à 50. Ne pas afficher de "note moyenne" sans données réelles.

---

### Template pour collecter un témoignage (beta-testeur parent)

Envoyer par SMS ou email à un parent qui a testé avec son enfant :

> "Bonjour [prénom], merci d'avoir testé Matheux avec [prénom enfant]. J'aurais besoin de votre retour honnête pour la page d'accueil. 3 questions rapides :
> 1. Avant Matheux, quel était le problème concret avec les maths de votre enfant ?
> 2. Qu'est-ce qui vous a le plus surpris en utilisant l'application ?
> 3. En une phrase : qu'est-ce que vous diriez à un autre parent ?"

**Format attendu pour la carte :**
- Citation de la réponse 3 (ou d'un extrait de 1+2), en italique
- Prénom du parent + rôle : "Mère de Lucas, 5ème"
- 5 étoiles (★★★★★) — uniquement si le parent a spontanément exprimé une satisfaction forte

---

### Placeholders en attendant les vrais témoignages

```html
<!-- Placeholder témoignage 1 -->
"En deux semaines, mon fils a enfin compris pourquoi il se trompait en algèbre.
 C'est la première fois qu'il ouvre ses maths sans qu'on le lui demande."
— Sophie M., mère de Nathan, 5ème ★★★★★

<!-- Placeholder témoignage 2 -->
"Le diagnostic m'a surprise : il ne bloquait pas sur les fractions,
 mais sur les soustractions de négatifs. On cherchait au mauvais endroit depuis un an."
— Isabelle L., mère de Théo, 4ème ★★★★★
```

Ces textes sont des exemples réalistes mais fictifs. Les remplacer par de vrais témoignages dès que disponibles. Ne pas les publier tels quels.

---

## 5. Décisions de design

### CTA principal : inscription directe ou diagnostic anonyme ?

**Recommandation : diagnostic anonyme d'abord, puis inscription.**

Justification : le parent ou l'élève ne connaît pas encore Matheux. Demander un email dès le premier clic crée une friction à froid. Laisser l'utilisateur vivre 2-3 questions du diagnostic avant de demander l'inscription abaisse le seuil d'engagement. Le produit se vend lui-même si on le montre.

**Implémentation suggérée :**
1. CTA Hero : "Faire le diagnostic gratuit →" → ouvre une modal ou page légère avec 3 questions anonymes
2. Après la 3ème question : afficher les premiers résultats partiels (ex. "Vous semblez avoir des lacunes en...") + proposer "Créer un compte gratuit pour voir les résultats complets"
3. L'inscription devient la récompense naturelle du diagnostic

Si cette implémentation est trop lourde pour le MVP, fallback acceptable : bouton ouvre directement le formulaire d'inscription, le diagnostic se fait après. Ne pas promettre le diagnostic sur la landing sans le tenir.

---

### Ce qu'on ne met PAS sur la landing

**1. Les fonctionnalités techniques**
Ne pas lister "MathJax v3", "SHA-256", "queue offline". Le parent s'en fiche. Se concentrer sur les bénéfices, pas les features.

**2. Les screenshots de tableaux de bord complexes**
Un tableau avec 12 colonnes de données fait peur. Montrer uniquement des écrans simples (exercice, anneau de maîtrise, barre de progression).

**3. Les comparaisons avec des concurrents nommés**
Fragile juridiquement, inutile à ce stade. La comparaison "sans/avec" suffit.

**4. Un pricing par paliers (Basic / Pro / Enterprise)**
Une seule offre = une seule décision. Les paliers créent de l'hésitation. Ajouter les niveaux quand les données justifient une segmentation.

**5. Les détails pédagogiques (espace mémoire, répétition espacée, etc.)**
Ces arguments convaincuent les profs, pas les parents. Un parent veut "mon enfant progresse", pas "algorithme de Leitner adaptatif". Garder ces arguments pour une page "À propos" ou un blog.

---

### Palette couleurs

La palette définie dans `index.html` convient pour la landing. Récapitulatif :

| Variable CSS | Hex | Usage landing |
|---|---|---|
| `--ink` | `#07090f` | Fond Hero, fond CTA final |
| `--ink2` | `#1a1f2e` | Fonds sombres secondaires |
| `--bg` | `#f7f8fc` | Fond sections claires |
| `--wht` | `#fff` | Fond sections blanches |
| `--p` | `#4338ca` | Indigo — CTA, accents, pills |
| `--pd` | `#312e81` | Indigo foncé — carte Pricing |
| `--pl` | `#eef2ff` | Indigo clair — arrière-plan pills |
| `--amb` | `#f59e0b` | Ambre — badge "7 jours gratuits" |
| `--grn` | `#059669` | Vert — checkmarks "Avec Matheux" |
| `--ros` | `#e11d48` | Rouge — points "Sans Matheux" |

Pas de changement de palette. La cohérence entre landing et app est un signal de sérieux.

---

## 6. Spécifications techniques pour Claude Code

### Fichier : landing séparée

**Créer `landing.html` comme fichier indépendant**, pas comme section dans `index.html`.

Justification :
- `index.html` fait ~2100 lignes et est déclaré GOLD MASTER — ne pas toucher
- La landing peut être optimisée pour le SEO (balises meta, OG, schema.org) indépendamment de l'app
- Le déploiement peut être fait séparément (ex. Netlify pour la landing, GAS pour l'app)
- Les A/B tests de headlines sont plus faciles sur un fichier séparé

**Lien entre les deux :** le CTA de `landing.html` pointe vers `index.html#register` (ou paramètre URL `?action=register`).

---

### Mobile-first obligatoire

- Breakpoint de référence : **390px** (iPhone 15 standard)
- Tous les éléments doivent être testés à 390px avant 768px
- Tap targets minimum : 44px de hauteur
- Pas de hover-only interactions sur mobile
- Texte minimum : 14px (0.875rem)
- CTA pleine largeur sur mobile, max 420px centré sur desktop

---

### Compatibilité CSS

Copier les variables CSS et les classes suivantes depuis `index.html` en tête de `landing.html` :

```css
/* Variables obligatoires */
:root { --ink, --ink2, --mut, --brd, --bg, --wht, --p, --pl, --pd, --amb, --ambl, --grn, --grnl, --ros, --rosl, --r, --rl }

/* Classes réutilisables */
.btn, .btn-ac, .btn-dk, .btn-fw   /* boutons */
.ccard, .ccard.bad, .ccard.good   /* cartes comparaison */
.chk                               /* ligne avec icône check */
.stag                              /* pill tag section */
.lhero                             /* fond sombre hero */
.grid-ov                           /* overlay grille */
.pbar, .pfill, .pfp, .pfg         /* barres de progression */
.afu, .s1, .s2, .s3, .s4         /* animations entrée */
@keyframes fadeUp, s1, pulseLight  /* keyframes animations */
```

Fonts à inclure :

```html
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
```

Tailwind CDN (même version que l'app) :

```html
<script src="https://cdn.tailwindcss.com"></script>
```

Ne pas utiliser de framework JS. Vanilla uniquement. Pas de React, pas de Vue.

---

### Assets nécessaires

Prévoir ces assets avant de coder :

| Asset | Format | Dimensions | Usage |
|---|---|---|---|
| `screenshot-chapitres.png` | PNG ou WebP | 390×780px | Mockup section Demo |
| `screenshot-exercice.png` | PNG ou WebP | 390×780px | Mockup section Demo |
| `screenshot-progression.png` | PNG ou WebP | 390×780px | Mockup section Demo |
| Logo favicon | SVG ou PNG | 32×32px | `<link rel="icon">` |

**Si les screenshots ne sont pas encore disponibles :** utiliser des placeholders `<div>` gris anthracite avec les légendes en blanc. Prévoir un attribut `data-placeholder="true"` pour les repérer facilement plus tard.

**Comment capturer les screenshots :**
1. Ouvrir `index.html` dans Chrome
2. DevTools → Toggle device toolbar → 390×844 (iPhone 15)
3. Naviguer vers la vue à capturer
4. DevTools → Plus d'options → Capture screenshot (pleine page)

---

### SEO et meta (landing.html uniquement)

```html
<title>Matheux — L'IA qui fait vraiment progresser en maths</title>
<meta name="description" content="Votre enfant travaille mais ses notes ne bougent pas ? Matheux diagnostique les lacunes et crée un parcours personnalisé. 7 jours gratuits."/>
<meta property="og:title" content="Matheux — Progresser en maths, enfin."/>
<meta property="og:description" content="Diagnostic de lacunes + exercices ciblés + rapport quotidien. Pour les élèves de collège."/>
<meta property="og:image" content="[URL screenshot hero ou logo]"/>
<meta property="og:type" content="website"/>
<link rel="canonical" href="https://[domaine]/"/>
```

---

### Navigation et liens

- **Logo** : lien vers `landing.html` (ou `#top`)
- **Bouton "Connexion"** en haut à droite : lien vers `index.html` (ou `?action=login`)
- **Tous les CTA** : lien vers `index.html` (ou `?action=register`)
- **Mentions légales** (footer) : lien vers `mentions-legales.html` (à créer plus tard — mettre un lien vide `href="#"` pour l'instant)
- **Pas de menu hamburger** sur mobile. La landing est une page unique, la nav est minimaliste.

---

### Performance

- Pas de JS inutile. La landing n'a pas besoin de MathJax, de localStorage, de GAS.
- Un seul fichier JS inline si nécessaire (accordéon FAQ uniquement)
- Lazy loading sur les screenshots (`loading="lazy"`)
- Tailwind CDN est acceptable pour le MVP. Pour la production : purger les classes inutilisées avec `tailwindcss` CLI.

---

## Checklist de validation avant livraison

- [ ] Hero visible en entier sur 390px sans scroller
- [ ] CTA fonctionne (lien vers inscription)
- [ ] Section Demo : 3 mockups ou placeholders présents
- [ ] FAQ : accordéon fonctionnel sans JS framework
- [ ] Pricing : une seule carte, CTA visible
- [ ] Footer : copyright + lien connexion + lien mentions légales (même si vide)
- [ ] Aucun overflow horizontal sur mobile
- [ ] Textes lisibles (contraste suffisant sur fond sombre)
- [ ] Police Syne sur tous les titres, DM Sans sur tous les corps de texte
- [ ] Variables CSS cohérentes avec `index.html`
