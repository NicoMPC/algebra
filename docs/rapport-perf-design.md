# Rapport Performances / Design / Responsive — 14 mars 2026

## AXE 1 — Performances

### 1a — Tailwind CDN → Tailwind purgé
- **Avant** : CDN ~3+ Mo (tailwindcss.com, script JS)
- **Après** : `dist/tailwind.css` = **41 Ko** (purgé + minifié)
- Build : `npx @tailwindcss/cli -i ./src/input.css -o ./dist/tailwind.css --minify`
- Tailwind v4.2.1

### 1b — Fonts Google : preload + async
- `preconnect` vers fonts.googleapis.com ET fonts.gstatic.com
- `preload` du stylesheet fonts
- Chargement async via `media="print" onload="this.media='all'"`
- Fallback `<noscript>` ajouté

### 1c — MathJax → KaTeX
- **Migration complète : OUI**
- MathJax (~800 Ko, bloquant) remplacé par KaTeX (~280 Ko, defer)
- `rMath()` réécrit pour utiliser `renderMathInElement()`
- Tous les appels `MathJax.typesetPromise()` → `rMath(element)`
- 0 référence MathJax restante

### 1d — Image scree.png
- `loading="lazy"` : déjà présent
- `width="606" height="1096"` : **ajouté** → zéro CLS

### 1e — Meta perf
- `<meta name="theme-color" content="#4338ca">` ajouté
- `<link rel="dns-prefetch" href="https://script.google.com">` ajouté

## AXE 2 — Design

### 2a — Micro-animations afu
- Déjà en place sur tous les blocs principaux (cards, bandeaux, sections)

### 2b — Cards chapitres terminés
- Déjà implémenté : `border-emerald-200`, `background:#f0fdf4`, badge `✅ Terminé`

### 2c — Boutons : tap feedback mobile
- `.btn` : ajout `touch-action:manipulation; user-select:none;` + `:active opacity:.8`
- `.opt` (QCM) : idem + `:active scale(.97) opacity(.8)` sauf si déjà répondu

### 2d — Toast : border-radius adaptatif
- `border-radius: clamp(12px, 3vw, 99px)` — pill desktop, rond mobile

### 2e — Barre de progression
- Déjà en place : `.pfill { transition: width .5s cubic-bezier(.4,0,.2,1) }`

### 2f — Hero mobile
- h1 : `font-size: clamp(1.6rem, 7vw, 2.8rem)` (responsive fluide)
- CTA : `min-height: 56px` (zone tactile confortable)

## AXE 3 — Responsive mobile

### 3a — Admin cards
- `.adm-card` : ajout `max-width:100%; word-break:break-word`

### 3b — Admin modal scroll
- `max-height:90vh; overflow-y:auto; -webkit-overflow-scrolling:touch`

### 3c — Progress : scroll horizontal
- N/A — vue en cartes verticales, pas de tableau/barre horizontale

### 3d — Brouillon/Calculette : padding-bottom
- `app-c.style.paddingBottom = '55vh'` quand tiroir ouvert (mobile uniquement)
- Reset à la fermeture

### 3e — Boutons QCM hauteur
- Déjà en place : `.opt { min-height: 56px; display:flex; align-items:center }`

### 3f — Landscape mobile
- `#trial-flow.flow-fs` : ajout `max-height: 100dvh` (dynamic viewport height)

## Fichiers modifiés
- `index.html` — toutes les modifications
- `src/input.css` — source Tailwind v4
- `dist/tailwind.css` — CSS purgé (41 Ko)

## Fichiers ajoutés
- `tailwind.config.js` (auto-généré, non utilisé en v4)
- `package.json` / `node_modules/` — dépendances dev Tailwind
