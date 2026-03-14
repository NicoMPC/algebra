# Rapport — Figures géo + Auth modal + Toast mobile

**Date :** 14 mars 2026

---

## 1. Figures géométriques SVG

### Lettres dynamiques
Toutes les figures extraient désormais les lettres de points depuis l'énoncé (`pts[]`).
Les lettres sont transmises via `fig.pts` à `renderFig()` qui les utilise au lieu des lettres hardcodées A/B/C/D.

**Types patchés (11) :** tri_rect, tri_trigo, thales, circle, rect, angle, sym_axial, sym_central, homothety, similar_tri, triangle

### Filtrage strict
- `nonGeoChaps` bloque les figures pour : calcul_litt, fraction, statistiq, probabilit, nombre, puissance, algorith, suite, exponent, variable_al, probabilites_cond, notation_sci
- Faux positifs bloqués : "cercle trigonométrique" hors trigo, "triangle de Pascal", "inégalité triangulaire" hors géo, exercices Python/algorithme

### 3 nouveaux types (1ERE Spé)
- **vectors** — produit scalaire : point O + vecteurs u/v + angle θ
- **repere** — géométrie repérée : repère orthonormé + droite
- **trigo_circle** — cercle trigonométrique : cercle unité + point M + projections cos/sin

### Améliorations visuelles
- viewBox passé à 280×210
- `overflow="visible"` sur tous les SVG
- `dominant-baseline="central"` sur les labels
- Cercle : mode diamètre avec 2 points nommés
- Angle : 3 lettres de l'angle affichées, mesure à l'intérieur de l'arc
- Symétrie axiale : 3 paires A/A', B/B', C/C' + axe pointillés bien visible
- Symétrie centrale : 3 paires + O coloré au centre

---

## 2. Modale auth — flow CTA protégé

### Patch A — showAuth() gardé
`showAuth()` vérifie si `#trial-flow` est visible. Si oui, retour silencieux — le quiz inline n'est jamais interrompu.

### Patch B — Auto-login silencieux
L'appel `showAuth('login')` dans DOMContentLoaded (échec auto-login) a été **supprimé**. L'email est pré-rempli en fond mais la modale n'est plus imposée.

### Audit
Un seul appel `auth-screen.classList.remove('hidden')` existe dans tout le fichier : dans `showAuth()` elle-même, qui est maintenant gardée. Les appels explicites (bouton Connexion nav + footer) passent par `showAuth()` — tous protégés.

---

## 3. Toast mobile — wrapping

### CSS modifié (#toast)
- `white-space: nowrap` → `white-space: normal`
- `border-radius: 99px` → `18px`
- Ajouté : `word-break: break-word`, `text-align: center`, `line-height: 1.4`
- Ajouté : `max-width: min(88vw, 400px)`, `box-sizing: border-box`

### JS (showT)
Aucune width forcée en JS — le CSS gère tout.
