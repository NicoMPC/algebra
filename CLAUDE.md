# CLAUDE.md — Matheux · GOD MODE

> Document unique. Point d'entrée + manuel complet.
> Mis à jour automatiquement à chaque session.
> GAS @88 · Lancement 18 mars 2026

---

## 0. Projet en 30 secondes

Matheux (matheux.fr) est une SPA vanilla JS (`index.html` ~9900L) + backend Google Apps Script (`backend.js` ~5300L) sur Google Sheets.
Soutien scolaire maths adaptatif, 6ème→3ème + 1ère Spé Maths.
Fondateur solo : Nicolas Follezou.
Objectif : 50 clients à 19,99€/mois. Lancement : 18 mars 2026.

Exercices : 1872 au total (audités @77, score qualité ~98%).
Simulation 21j : 12 profils, 4 bugs corrigés, 0 erreur réseau.

---

## 1. Rôle de l'IA

Tu es le **directeur technique et chef de projet IA** du projet Matheux.
Nicolas (fondateur) est le visionnaire produit. Ton rôle :

1. **Comprendre** les demandes produit de Nicolas
2. **Traduire** en actions techniques concrètes (frontend, backend, BDD, scripts)
3. **Implémenter** dans la codebase existante
4. **Maintenir** la documentation vivante (fusion, suppression, ajouts)
5. **Alerter** si une action risque de casser l'architecture ou la BDD

### Traduction produit → technique

| Nicolas dit | Action IA |
|---|---|
| "L'élève doit se sentir plus guidé sur le dashboard" | UI : ajouter bandeau contextuel dans `rSection('CHAPITRES')`, texte selon `trial.daysLeft` et exos faits |
| "Je veux voir les élèves inactifs plus vite" | Backend : ajuster seuil `rebuildSuivi()`, ajouter pill dans `getAdminOverview()` |
| "Ajoute un chapitre Symétrie en 6ème" | Générer JSON 20 exos + 2 diags, script Python push vers `Curriculum_Officiel` + `DiagnosticExos`, MAJ `database.md` |

---

## 2. Règles de développement absolues

### Patches chirurgicaux uniquement
- Codebase **V23 GOLD MASTER** — ne jamais réécrire
- `index.html` ~9900 lignes → **ne jamais diviser**
- Vanilla JS, pas de framework, pas de bundler, pas de dépendances sans validation Nicolas
- Modifier **uniquement** la fonction concernée par la tâche

### CORS GAS — critique
```
⛔ INTERDIT : headers: { 'Content-Type': 'application/json' }
✅ CORRECT  : fetch(SU, { method: 'POST', body: JSON.stringify({...}) })
```
Preflight OPTIONS non supporté par GAS → CORS bloqué depuis matheux.fr.

### Messages & Toasts — INVARIANTS FIGÉS @95
> **Ces règles sont prouvées par simulation (274 API calls, 267 messages, 0 incohérence).**
> **Ne JAMAIS modifier sans relancer `python3 sim_7days_messages.py` après.**

1. **Toast mutex** : `_toastBusy` + `_toastQueue` — jamais 2 toasts visibles. `dur=0` bypass (loading). `hideT()` reset tout.
2. **Hero CTA exclusif** : cascade P1→P5 + fallback DONE. Exactement 1 hero par session. Chaque niveau a `if (!_hero)` + `break`.
3. **`boostConsumed` date-stamped** : `boostConsumedDate` sauvé dans localStorage. Expire si `!== tod()`. Jamais stale le lendemain.
4. **Coach tip vs toast ko** : `if/else` exclusif dans `validateAnswer`. Coach tip AVANT le panel aide (immédiat vs 900ms).
5. **Milestones/Coach namespacés** : `mx_ms_{code}` / `mx_co_{code}` dans localStorage. Pas de pollution entre comptes.
6. **Streak dedup** : toast login skip si `_stkMileDup` (milestone streak_3/7 va fire dans `_checkMilestone`).
7. **"demain"** : uniquement dans `boost_preparing` (post-boost insight). Partout ailleurs → "bientôt" ou "continue tes chapitres".
8. **`pendingManual` cleanup** : effacé dans les 3 branches de `nextChapter` (PENDING_MANUAL / JSON / string).

### Schéma Google Sheets
- Ne **jamais** changer de colonnes sans documenter dans [database.md](docs/database.md)
- Index de colonnes **hardcodés** dans le backend → toute modification non documentée casse tout

### Compatibilité GAS
- Runtime V8 limité (pas de modules ES, pas de top-level await)
- `doPost(e)` point d'entrée unique → dispatch sur `action`
- Quota : 6 min/appel, ~20 users simultanés max
- Retour : `ContentService.createTextOutput(JSON.stringify(...)).setMimeType(ContentService.MimeType.JSON)`

### RGPD — données de mineurs
- Consentement parental obligatoire
- Hash MDP côté client : `SHA-256(email + '::' + password + '::AB22')`
- Pas de données sensibles dans localStorage (auth token uniquement)
- GA4 conditionné au consentement cookies

### Règle 1 chapitre/jour — DÉSACTIVÉE
- Tous les chapitres accessibles en permanence
- Animation informative après complétion — ne bloque rien
- Nicolas assigne le prochain chapitre depuis l'admin (`publish_admin_chapter`)

### Figures géométriques SVG
- `autoDetectFigure(q, cat)` → auto-génère un spec `fig` depuis le texte
- `renderFig(fig)` → SVG inline
- `getExoFigure(data, cat)` → point d'entrée dans `rSection()`
- **18 types** : tri_rect, tri_trigo, thales, circle, rect, angle, parallel, sym_axial, sym_central, cube, cylinder, cone, pyramid, sphere, section_solid, homothety, similar_tri, triangle, transform, vectors, repere, trigo_circle
- Système de confiance `confidence: 'high'|'medium'|'low'` — `low` filtré
- Fallback safe : auto-détection échoue → pas de figure → l'exercice marche

### Visualisation post-réponse
- `extractFunction(q)` : détecte f(x)=ax+b et ax²+bx+c
- `renderFunctionGraph(fnSpec)` : SVG 280×180 après réponse uniquement

### Types d'exercices
- `exo.type` : `'qcm'` (défaut), `'vf'` (Vrai/Faux), `'fill'` (trou à compléter)
- Grille options adaptative : 2 opts → 2 cols, 3 → vertical, 4 → grille 2×2

### Pas de sur-ingénierie
- Pas de feature flags, pas d'abstractions prématurées
- Si faisable manuellement par Nicolas en 2 min → ne pas automatiser
- 3 lignes dupliquées > 1 abstraction inutile

---

## 3. Workflow technique

### Avant de coder
1. Lire **ce fichier** (CLAUDE.md)
2. Lire le fichier doc concerné si nécessaire
3. Identifier le bloc actif dans [roadmap.md](docs/roadmap.md)
4. Vérifier que la tâche est dans le périmètre

### Déploiement

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"

# Backend GAS
clasp push --force
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "desc"

# Frontend (GitHub Pages auto-deploy)
git add index.html && git commit -m "feat: ..." && git push origin main

# Raccourci GAS
./deploy.sh "desc"
```

### Tests
```bash
python3 test_full_v2.py          # Suite complète — 74/74 (100%)
python3 test_simulation_40.py   # Simulation 40 élèves × 15 jours — 17/17
python3 sim_21days.py           # Simulation 21j — 12 profils
python3 rebuild_sheet.py         # Reconstruire Suivi + Historique
```

### Tokens
⚠️ **Toujours** estimer avant génération massive → présenter options → attendre validation.

---

## 4. Conventions de code

### Frontend (index.html)
- CSS : variables custom + Tailwind CDN
- JS : vanilla, fonctions globales, pas de classes
- Vues : via `rSection()` injectant du HTML dans `#main`
- Fonts : Syne (titres) + DM Sans (body)
- MathJax v3, fallback 2.5s
- Messages : ton ado "Game Boy Chill" — système `_msg()` adaptatif niveau

### Backend (backend.js)
- Entrée : `doPost(e)` → dispatch `action`
- Convention : `snake_case` pour les noms d'actions
- Retour : `{ status: 'success', ... }` ou `{ status: 'error', message: '...' }`

### Nommage
- Actions GAS : `save_score`, `generate_daily_boost`, `get_admin_overview`
- localStorage : `boost_v23` (auth), `boost_loc_v23` (state local)
- Colonnes Sheets : PascalCase (`ExosDone`, `TrialStart`)

---

## 5. Documentation vivante

### Règles obligatoires
1. **Mettre à jour** CLAUDE.md si les règles ou le workflow changent
2. **Mettre à jour** le fichier doc concerné (`architecture.md`, `database.md`, `product.md`, `roadmap.md`)
3. **Supprimer ou fusionner** les informations obsolètes / redondantes
4. **Ne jamais créer** de doc inutile
5. **Proposer la suppression** d'un document devenu obsolète

### Structure docs/ (7 fichiers vivants)

```
CLAUDE.md                          → Document unique (ce fichier)
docs/architecture.md               → Technique @88 (frontend + backend + flux)
docs/database.md                   → Schéma Sheets (16 onglets + colonnes)
docs/product.md                    → Produit (vision + parcours + business)
docs/roadmap.md                    → Priorités + calendrier lancement
docs/messages.md                   → Voice & tone guide
docs/checklist-lancement.md        → Checklist lancement 18 mars
docs/workflow-quotidien.md         → Workflow quotidien Nicolas (6 onglets admin)
docs/archive/                      → Docs historiques + audits + rapports (ne pas lire sauf besoin)
```

---

## 6. URLs et identifiants

| Ressource | Valeur |
|---|---|
| GAS URL | `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec` |
| Deployment ID | `AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF` |
| Sheet ID (prod) | `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |
| GitHub | `https://github.com/MatheuxApp/algebra` (privé, org Enterprise trial) |
| Stripe PROD | `https://buy.stripe.com/cNicN7b0ebU9bOE9WTb3q01` ✅ |
| Stripe Webhook | Endpoint à finaliser dans Stripe Dashboard |
| GA4 | `G-7R2DW4585Y` |
| Service account | `algebreboost-sheets-2595a71cadfb.json` (ignoré par git) |

---

## 7. Comptes de test

| Code | Prénom | Niveau | Email | MDP |
|---|---|---|---|---|
| AUG001 | Auguste | 1ERE | augustecapronm@icloud.com | auguste |
| PR3CMB | Nicolas | 4EME | nico@nico.fr | niconcico |
| 3M4ZAB | Charlie | 3EME | charlieboitel6@gmail.com | charlie |
| HMD493 | Admin | — | (admin) | — |

Profils simulation 21j : SIM01→SIM12 **supprimés** le 16 mars (nettoyage base pré-lancement).

---

## 8. État pré-lancement — 17 mars 2026

> **Lancement confirmé : mercredi 18 mars 2026 à 9h.**
> Code 100% prêt. Tests 5/5 niveaux ✅. 27 frictions fixées. Landing GOD MODE déployée.
> GitHub privé (MatheuxApp org, Enterprise trial). Stripe PROD actif.
> Reste : endpoint webhook Stripe + tests admin + 2 features UX (Valider + Je ne sais pas).

### ✅ Fait (lundi 16 mars)

| # | Action |
|---|---|
| 1 | Stripe TEST → PROD — lien actif `cNicN7b0ebU9bOE9WTb3q01` |
| 2 | 3 boîtes mail Ionos : `contact@`, `no-reply@`, `nicolas@matheux.fr` |
| 3 | Alias Gmail `no-reply@matheux.fr` (SMTP Ionos port 465 SSL) |
| 4 | Sécurité Stripe déployée @85 — webhook handler + premium guard client |
| 5 | TVA art. 293 B CGI dans CGV |
| 6 | Formulaire contact — `send_contact` GAS + modal 3 footers + `_toast()` |
| 7 | Merge sécurité freelance (SECUmain → main) + GitHub Pages sur main |
| 8 | Tests emails — J+0 ✅ / Reset MDP ✅ / Contact ✅ / Pas de triggers ✅ |
| 9 | Stripe config — CGV + confidentialité + TVA décochée + limite 50 paiements |
| 10 | Bandeau rappel limite Stripe dans admin dashboard |
| 11 | Nettoyage base — SIM01-SIM12 supprimés, gardé admin + Auguste + Charlie |
| 12 | Test élève 6EME ✅ / 5EME ✅ / 4EME ✅ — 15 frictions notées |

### ✅ Fait (mardi 17 mars)

| # | Action | Détail |
|---|---|---|
| 1 | Test élève 3EME ✅ | Remarques intégrées |
| 2 | Fix 27 frictions élève ✅ | Mode nuit, exo 1 bloqué, bienvenue, retro, bon retour, boost demain, signaler erreur, onboarding responsive |
| 3 | Cartes premium + messages perso ✅ | Cartes cadeau/découvert/invite, tri intelligent, messages prénom/chapitre/palier |
| 4 | Landing refonte GOD MODE ✅ | 11 sections — Problème, contraste 10min/jour, fondateur humain, pricing pills. Teasing : "vraiment comprises" |
| 5 | GitHub → MatheuxApp org ✅ | Repo privé, Enterprise trial 30j, Pages OK, DNS OK |
| 6 | Fix final pré-lancement ✅ | Min 2 chapitres diag, bandeau boost cohérent, polish UI |
| 7 | Vérif boost auto ✅ | Exos = chapitres choisis élève uniquement (confirmé backend L895-915) |
| 8 | Test parent parcours ✅ | Landing → CTA → diag → inscription → onboarding → boost → mail J+0 → admin |
| 9 | Relecture exos quizz ✅ | Remarques diag 3EME/5EME notées (triangles nommés, formules, LaTeX) |
| 10 | Audit diag+boost géo ✅ | 168 exos audités → `docs/auditdiagboost.md` — 93 figures SVG à ajouter, 16 reformulations |
| 11 | **Audit final exercices** ✅ | 1728 exos × 3 scripts + 7 vérifs manuelles. 2 LaTeX fixés (1ERE/Second_Degre). 0 bloquant. Score 98,3%. |
| 12 | **Fix doublons 1ERE** ✅ | 21 exos remplacés (Boost 19 + Diag 2) — 0 doublon restant entre Curriculum/Boost/Diag. 3 "erreurs calcul" = faux positifs script. |

### ⏳ Mardi 17 mars après-midi

| # | Action | Détail |
|---|---|---|
| 1 | ✅ Fix diagnostic + Boost J1 | **FAIT** — 251 figures SVG, 14 reformulations, espaces LaTeX fixés, doublon Systèmes 3EME corrigé |
| 2 | ✅ Implémenter "Valider la réponse" | **FAIT** — selectOpt+validateAnswer, sticky bottom, mode nuit |
| 3 | ✅ Implémenter "Je ne sais pas" | **FAIT** — bouton .opt-skip, resultat='SKIP' (traité comme HARD) |
| 4 | ✅ Refonte admin cockpit @87-@88 | **FAIT** — 6 onglets (+ NOUVEAU @96), boutons JSON complet, 3 profils test |
| 5 | ✅ Audit final exercices | **FAIT** — 1728 exos, 3 scripts + 7 vérifs manuelles, 2 LaTeX fixés, 0 bloquant, score 98,3% |
| 6 | 🎮 Test admin workflow | En conditions réelles — boost, chapitre, email |
| 7 | 🧪 Test réouverture user | Auguste + Charlie + Nicolas — vérif post-27 fixes |
| 8 | ✅ Audit pré-lancement complet | **FAIT** — 24 points (3 bloquants, 3 critiques, 7 importants, 8 frictions UX). Voir checklist-lancement.md §5b. 17 mars. |

### ✅ Bloquants audit — corrigés (18 mars @89)

| # | Action | Statut |
|---|---|---|
| 1 | Fix prix 9,99€ → 19,99€ | ✅ cgu.html + premium.html |
| 2 | Supprimer alerte "bêta fermée 40 familles" | ✅ cgu.html |
| 3 | Fix triggerDailyMarketing Premium='1' string | ✅ backend.js |
| 4 | Messages boost cohérents (demain/bientôt) | ✅ index.html |
| 5 | ko_boost avec lien correction | ✅ index.html |
| 6 | Transition vouvoiement→tutoiement onboarding | ✅ index.html |
| 7 | Boutons Valider/Skip inversés (thumb zone) | ✅ index.html |
| 8 | Pills navigation ✓/✗ | ✅ index.html |
| 9 | KaTeX fallback 3s → 1.5s | ✅ index.html |
| 10 | Trial expiry toast J-3/J-2/J-1 | ✅ index.html |
| 11 | Mode nuit catch-all backgrounds blancs | ✅ index.html |
| 12 | Indicateur offline persistant | ✅ index.html |
| 13 | guestDiag localStorage purgé au login | ✅ index.html |
| 14 | Rate limiting global 30/min auth | ✅ backend.js |
| 15 | manifest.json screenshots supprimé | ✅ manifest.json |
| 16 | premium.html nettoyée (Stripe PROD, mentions) | ✅ premium.html |
| 17 | Contact form modal z-index | OK — z-index 5000, pas de bug |
| 18 | Messages "pas de boost" cohérents | ✅ index.html |

### ✅ Gamification MVP — 18 mars @90

| # | Feature | Détail |
|---|---|---|
| 1 | XP visible header + animation +XP | `showXP()` branché dans `mark()`, +200 boost, +300 chapitre |
| 2 | Paliers maîtrise (6 niveaux) | `_chapTier()` : À découvrir/En cours/En progrès/Solide/Maîtrisé/Expert — badge coloré sur cards |
| 3 | Streak freeze 1j/semaine | Si avant-hier + streak ≥2 + pas de freeze cette semaine → série maintenue |
| 4 | Milestones (6 événements) | Premier boost, 10 exos, streak 3j/7j, 1er chapitre, 100 exos — toasts célébrés |
| 5 | Card "Session terminée" | Fond émeraude, XP total + streak, "Reviens demain" — remplace l'ancien compact gris |
| 6 | Temps estimé hero CTA | `≈ Xmin` calculé depuis nb exos restants × 1.5 |
| 7 | Mastery ring enrichi | Compteur paliers + message retour contextuel (inactivité, streak, bienvenue) |
| 8 | Onglet Progression débloqué | `display:none` retiré — vue complète accessible |
| 9 | Cohérence messages | "boost"→"entraînement", chap_done sans "disponible demain", mode nuit bg-orange/bg-blue |

### ✅ Refonte Onboarding UX — 18 mars @93

| # | Feature | Détail |
|---|---|---|
| 1 | Stepper horizontal 4 étapes | Classe → Chapitres → Diagnostic → Inscription, dots ✓ quand complétés, labels masqués <380px |
| 2 | Slide animations | Transition horizontale left/right entre steps (au lieu de fadeIn vertical) |
| 3 | Micro-bounce niveau | Feedback visuel 300ms sur sélection de classe |
| 4 | Écran respiration | "C'est parti ! X questions" avec auto-dismiss 2s avant le diagnostic |
| 5 | Feedback diagnostic enrichi | Compteur ✓ bonnes réponses visible, +1 floating pop, encouragement mi-parcours |
| 6 | Carte résultat en 2 écrans | Écran émotion (score animé + tags) → Écran décision (objectif) — séparation conversion |
| 7 | Pourcentage animé | Counter 0→N% avec ease-out cubic + emoji contextuel (🎉/💪/🎯) |
| 8 | Copy conversationnel | "En quelle classe es-tu ?", "Tu reconnais quoi ?", "Comment tu t'appelles ?" |
| 9 | Reassurance améliorée | "Résiliable en 1 clic", placeholders plus naturels |

### ✅ Refonte Trial Flow UX — 18 mars @92

| # | Feature | Détail |
|---|---|---|
| 1 | Step 2 "Je ne sais pas trop" | Auto-sélection ~65% chapitres, minimum 2→1, titre/sous-titre plus accueillants |
| 2 | Tutorial allégé | 3 lignes → 1 ligne ("Réponds comme tu peux — pas de piège, pas de note.") |
| 3 | Carte résultat dédiée | Écran dédié dans step 3 : barre animée + récit + tags chapitres (solides/à travailler) |
| 4 | Objectif picker intégré | Les 4 choix d'objectif sont intégrés dans la carte résultat (plus de modal séparée) |
| 5 | Onboarding 3→2 slides | Guest flow : "Ton espace est créé" + "Ton entraînement est prêt" — plus rapide |
| 6 | `_flowGoToRegister()` | Nouvelle fonction : objectif → prépare step 4 (inscription) avec heading adapté |

### ✅ Tuto régressif — 18 mars @91

8 micro-tips contextuels first-use (système `_needsCoach/_markCoach` existant) :

| # | Déclencheur | Tip |
|---|---|---|
| T1 | 1er exo non-calibrage | "Choisis ta réponse puis appuie sur Valider" |
| T2 | 1ère mauvaise réponse | "Les indices et la correction s'affichent pour t'aider" |
| T3 | 1er hint cliqué | "Les indices se dévoilent un par un — utilise-les avant de répondre" (enrichi) |
| T4 | Formule auto-déployée | "La formule clé apparaît après ta réponse — retiens-la" |
| T5 | 3ème exercice | "Le brouillon et la calculette sont en bas — tape le crayon" |
| T6 | 2ème exercice | "Je ne sais pas montre la correction — zéro jugement" |
| T7 | 1er +XP | "Chaque réponse rapporte des XP — même les erreurs comptent" |
| T8 | Pills ≥2 réponses | "Les pastilles en haut te permettent de revoir chaque question" |

### ✅ Landing carrousel + phrase "Imaginez…" — 18 mars @94

| # | Feature | Détail |
|---|---|---|
| 1 | Carrousel screenshots visio | 4 photos cours (img/1-4.png), auto-scroll 3.5s, swipe tactile, dots navigation |
| 2 | Section vidéo remplacée | Placeholder vidéo → carrousel + légende fondateur |
| 3 | Légende fondateur | "C'est en donnant des cours que j'ai créé Matheux — pour rendre mes élèves autonomes. Conçu pour eux, avec eux." |
| 4 | Phrase transition "Imaginez…" | Nouvelle section 2b entre Problème et Solution — "Imaginez un endroit où toutes les erreurs, toutes les hésitations, sont gardées en mémoire — pour faire progresser votre enfant là où ça fait mal." |

### ✅ Audit cohérence messages + UX fixes — 18 mars @95

| # | Fix | Détail |
|---|-----|--------|
| 1 | Toast queue anti-overlap | `_toastQueue` + `_toastBusy` mutex — max 1 toast visible, les suivants en file |
| 2 | Milestones/coach par user | localStorage namespacé `mx_ms_{code}` / `mx_co_{code}` — plus de pollution cross-user |
| 3 | `boostConsumed` date freshness | `boostConsumedDate` sauvé — expire si jour différent, plus de "session terminée" stale |
| 4 | Coach tip avant aide | Tip "les indices s'affichent" AVANT le panel aide (plus après) |
| 5 | Streak dedup milestone | Toast login skip si milestone streak_3/7 va fire — 0 doublon |
| 6 | Trial badge J-5 | Badge visible dès J-5 (bleu discret), J-3 jaune, J-1 orange |
| 7 | `pendingManual` cleanup | Effacé quand chapitre réel reçu (JSON ou string) |
| 8 | Copy "demain" cohérent | `cours_prep` → "bientôt disponible", session terminée → "continue ou reviens demain" |
| 9 | Dead code supprimé | `no_boost_yet` jamais utilisé → supprimé |
| 10 | Modale connexion login only | Onglet "Nouveau" masqué — inscription uniquement via CTA |
| 11 | Bouton "Je ne sais pas" aéré | Sorti du sticky validate-wrap, pill discrète centrée, `mt-5` espace |

### 🔴 Reporté vendredi 20 mars (calendar)

| # | Action | Priorité |
|---|---|---|
| 1 | Webhook Stripe : implémenter vérif HMAC-SHA256 (`stripe-signature`) | ⛔ Avant J+7 |
| 2 | Déplacer `SHARED_SECRET` vers `PropertiesService` (en clair L5404) | ⛔ Avant J+7 |
| 3 | Tester un vrai paiement CB (19,99€ → vérifier Premium=1) | ⛔ Avant J+7 |
| 4 | Race condition saveScore/ExosDone — LockService | ⛔ Avant J+7 |
| 5 | Race condition ensureUsersCols | ⛔ Avant J+7 |

### 🟡 Avant ou après lancement

| # | Action | Priorité |
|---|---|---|
| 1 | Triggers Apps Script — automatiser dès 10-20 clients | 🟡 Plus tard |
| 2 | ~~Vidéo fondateur~~ → ✅ Remplacée par carrousel screenshots visio @94 | ✅ Fait |
| 3 | Centraliser 3 mails matheux.fr (Thunderbird/alias/redirection) | 🟡 Jeudi 19 mars |

---

## 9. Scripts disponibles

### Actifs (racine)
| Script | Description |
|---|---|
| `sheets.py` | Bibliothèque Google Sheets API (utilisée par tous les scripts) |
| `rebuild_sheet.py` | Reconstruit les onglets Suivi + Historique |
| `test_full_v2.py` | Suite de tests complète (74/74) |
| `test_simulation_40.py` | Stress test 40 élèves × 15 jours |
| `sim_21days.py` | Simulation 21j — 12 profils QA |
| `audit_exos.py` | Audit qualité exercices collège |
| `verify_hints.py` | Audit qualité des indices |
| `test_coherence_boost.py` | Test régression calibrage/boost |

### Utilitaires (scripts/)
| Script | Description |
|---|---|
| `scripts/setup_test_profiles.py` | Setup 6 profils test admin |

### Archivés (scripts/archive/)
Scripts one-shot déjà exécutés : imports, migrations, fix one-shot (`fix_diag_boost`, `fix_spaces`, `fix_thales_trigo`, `fix_double_prefix`), `cleanup_users`, `setup_3_test_profiles`, `notice_fondateur`, `generate_icons`, `audit_geo_context`, `sim_7days`, `security1.js`, `security2.js`. Ne pas utiliser.

---

## 10. Contraintes techniques connues

| Contrainte | Impact |
|---|---|
| Google Sheets ~20 users simultanés | Migration BDD si >50 users |
| GAS quota 6 min/appel | Limiter les opérations lourdes |
| Hash MDP côté client (pas de salt serveur) | Acceptable MVP |
| CORS GAS : pas de Content-Type header | Pattern fetch documenté ci-dessus |
| Guest flow : MDP auto `Matheux2026!` | Non communiqué à l'user |

---

## 11. Règle d'or — chaque session

1. Lire ce fichier (CLAUDE.md)
2. Lire `docs/roadmap.md` pour les priorités
3. Patches chirurgicaux uniquement
4. Tester sur mobile avant commit
5. Mettre la doc à jour à chaque modification
