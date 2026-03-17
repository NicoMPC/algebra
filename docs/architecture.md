# Architecture — Matheux

> Structure technique frontend/backend, flux de données, scripts utilitaires.
> Voir aussi [claude.md](claude.md) pour les règles, [database.md](database.md) pour le schéma Sheets, [product.md](product.md) pour le produit.

---

## Vue d'ensemble

```
NAVIGATEUR (index.html)              GOOGLE APPS SCRIPT (backend.js)
        │                                        │
        │  fetch POST (JSON, SANS Content-Type)  │
        ├───────────────────────────────────────►│
        │  { action: 'save_score',               │  Lit/écrit dans
        │    code: 'ABC123', ... }               │  Google Sheets
        │  ◄─────────────────────────────────── │  via SpreadsheetApp
        │  { status: 'success', ... }            │
        │                                        │
  localStorage                             Google Sheets (prod)
  - boost_v23: {email, hash}        ID: 1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4
  - boost_loc_v23: {stk, last}
```

| Composant | Technologie | Fichier | Taille |
|---|---|---|---|
| Frontend | HTML + CSS vars + Tailwind CDN + JS vanilla | `index.html` | ~9900 lignes |
| Backend | Google Apps Script (V8) | `backend.js` | ~5300 lignes |
| Base de données | Google Sheets | — | 16 onglets actifs |
| Hébergement frontend | GitHub Pages | `matheux.fr` | Auto-deploy sur push |
| Hébergement backend | Google Apps Script Web App | URL fixe via deployment ID | — |
| Auth | SHA-256 client-side | localStorage `boost_v23` | `email + '::' + password + '::AB22'` |

---

## Frontend — SPA vanilla JS

### Structure du fichier `index.html`

Le fichier est organisé en sections :

1. **CSS** (~1500 lignes) : variables CSS custom, Tailwind utilities, animations (`pulseGentle`, `toastIn`, `popIn`, `pulseNewChap`)
   - ⚠️ **Règle spécificité** : ne JAMAIS utiliser de sélecteurs ID (`#flow-sX`) pour définir `display` sur des éléments qui utilisent `.hidden` de Tailwind — l'ID (spécificité `1,0,0`) écrase la classe `.hidden` (`0,1,0`). Utiliser des classes (`.flow-step:not(.hidden)`) à la place.
2. **HTML** : structure minimale (header, main, footer, modales)
3. **JavaScript** (~3500 lignes) : logique applicative complète

### Système de vues (SPA)

Les vues sont des fonctions JS qui injectent du HTML dans `#main` :

| Vue | Fonction | Description |
|---|---|---|
| Landing | Rendu directement dans le HTML | Page d'accueil marketing |
| Trial Flow | `startTrialFlow()` → overlay fullscreen (`#trial-flow.flow-fs`) | Quiz diagnostic inline pre-inscription, 4 steps (classe → chapitres → quiz → inscription) |
| Chapitres | `rSection('CHAPITRES', ...)` | Liste des chapitres + "Mon Boost du jour" |
| Exercice | `rSection('EXERCICE', ...)` | Quiz MCQ avec indices/formule |
| Calibrage | `rSection('CALIBRAGE', ...)` | Diagnostic (quiz initial) |
| Progression | `rSection('PROGRESSION', ...)` | Barres de progression par chapitre |
| Brevet | `rSection('BREVET', ...)` | Mode brevet blanc (3EME only) |
| Admin | `rSection('ADMIN', ...)` | Cockpit admin @88 — 5 onglets : À FAIRE / FAIT / MAILS / INACTIFS / RAPPORT. Boutons "Copier JSON complet" (exos+résultats+temps+indices+formule). Profils test visibles. |

### Navigation

- `initApp()` : point d'entrée après login, route vers la bonne vue
- Admin détecté via `S.prof.isAdmin` → redirect auto vers vue admin
- Onglets bas de page : 📚 Chapitres | 📊 Progression | 🎓 Brevet (3EME)
- Swipe gauche → exercice suivant (mobile)

### State management

```javascript
const S = {
  prof: { code, name, level, isAdmin, premium, trial },
  exos: [],           // exercices en cours
  idx: 0,             // index exercice actif
  calState: null,     // état calibrage
  // ...
};
```

- `localStorage('boost_v23')` : `{ email, hash }` — auth uniquement
- `localStorage('boost_loc_v23')` : `{ [code]: { stk, last } }` — streak local
- `localStorage('app_night')` : `'1'` si mode nuit app actif — persisté entre sessions
- `localStorage('mx_coach_v1')` : coach marks affichés (indice/boost/brouillon)
- Toutes les données viennent du GAS à chaque login (pas de cache de données)

### Librairies externes (CDN)

- **Tailwind CSS** : utilities responsive
- **KaTeX v0.16.9** : rendu LaTeX (defer + queue retry, fallback 3s)
- **Syne** + **DM Sans** : Google Fonts

### Gamification

- **XP** : points d'expérience cumulés
- **Streak** : jours consécutifs d'activité
- **Mastery ring** : cercle SVG de progression par chapitre
- **Confettis** : animation post-boost terminé
- **Messages adaptatifs** : système `_msg(key, vars)` avec `_MSGS` (~35 entrées), adaptation niveau (6EME/3EME/def), arrays aléatoires, substitution variables `{name}` `{n}` `{s}`. Coach marks persistés localStorage (`mx_coach_v1`). Voir [messages.md](messages.md)
- **Brouillon contextuel + Calculette** : mobile = bottom sheet 50vh avec onglets (brouillon|calculette), desktop = panneau latéral droit 1/3 écran avec les 2 fusionnés (calculette en haut, brouillon en bas). Brouillon : symboles adaptés au chapitre via `getContextSymbols(niv, cat)`, mode quadrillé toggle. Calculette : adaptée par niveau/chapitre (trig si géo, π si aires/volumes, puissances si 5EME+, fractions si 6EME), mémoire M+/MR, copie vers brouillon.
- **Figures géométriques SVG** : auto-détection depuis le texte de la question + catégorie. Moteur `autoDetectFigure(q, cat)` → `renderFig(fig)` → SVG inline animé. **18 types** : triangle rectangle, trigo, Thalès, cercle (+ mode diamètre), rectangle/carré, angle (3 lettres), parallèles/perpendiculaires, symétrie axiale/centrale (3 paires A/A'), cube/pavé, cylindre, cône, pyramide, sphère, section de solide, homothétie, triangles semblables, transformations, **vecteurs/produit scalaire** (1ERE), **repère orthonormé** (1ERE), **cercle trigonométrique** (1ERE). Lettres de points extraites dynamiquement de l'énoncé (`pts[]`). Filtrage `nonGeoChaps` (pas de figure sur algèbre/stats/probas). viewBox 280×210, `overflow:visible`. Champ `fig` optionnel dans les exercices JSON pour override manuel. Fallback safe : pas de figure si non détecté.

---

## Backend — Google Apps Script

### Point d'entrée

```javascript
function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  switch(data.action) {
    case 'register': return register(data);
    case 'login': return login(data);
    case 'save_score': return saveScore(data);
    // ...
  }
}
```

### Actions GAS — état @88

> @88 : admin cockpit 5 onglets (À FAIRE/FAIT/MAILS/INACTIFS/RAPPORT), boutons "Copier JSON complet", profils test visibles, fix publish chapitre + JSON parse.
> @87 : bouton "Valider la réponse" (selectOpt+validateAnswer), bouton "Je ne sais pas" (resultat='SKIP'), 251 figures SVG ajoutées, 14 reformulations.
> @77 : mode nuit app, guide "Commence par là", titres chapitres gras, nav boost reopen. Audit 1872 exercices (~98%).
> @76 : refonte admin cockpit initial. @64 : 1ERE Spé Maths. @63 : rate limiting + validation inputs.

| Action | Description | Statut |
|---|---|---|
| `register` | Inscription élève. TrialStart = TODAY, email J+0 auto (si alias Gmail opérationnel) | ✅ |
| `login` | Connexion. Retourne trial, boostExosDone, pendingBrevet, nextChapter, nextBoostTopic, **revisionChapters** | ✅ |
| `save_score` | Sauvegarde réponse. MAJ Progress + rebuildSuivi + writeToHistorique + ExosDone si BOOST. Persiste `source` (col N Scores) | ✅ |
| `save_boost` | Sauvegarde fin de boost. ExosDone + rebuildSuivi | ✅ |
| `generate_diagnostic` | Génère diagnostic. Mode guest (sans code) pour landing flow | ✅ |
| `generate_daily_boost` | Génère boost quotidien depuis BoostExos (fallback Curriculum_Officiel), ciblé sur chapitres sélectionnés par l'élève | ✅ |
| `generate_remediation` | ⏸️ Désactivé — return success immédiat | ⏸️ |
| `get_progress` | Récupère progression par chapitre | ✅ |
| `detect_fragile_prereqs` | Détection prérequis fragiles (archivé → false) | ✅ |
| `get_prerequisites` | Liste prérequis | ✅ |
| `enqueue` | File d'attente (archivée → erreur propre) | ✅ |
| `generate_exam_prep` | Préparation examen par chapitre (10q : 7 lvl2 + 3 lvl1) | ✅ |
| `generate_brevet` | Brevet multi-chapitres (~15q style Brevet) — UI désactivé | ✅ |
| `generate_revision` | Révision niveau inférieur — UI désactivé | ✅ |
| `submit_feedback` | Feedback élève → onglet Insights. Types : signalement erreur (general) ou feedback session (boost/brevet/chapitre). Champs : source, ref, rating (1-5), type (difficile/moyen/bien/super) | ✅ |
| `generateMorningReport` | Rapport matin 7h (génération IA désactivée) | ✅ |
| `get_admin_overview` | Vue admin complète. Retourne `email` + `j0Sent` + `emailsDue` + `secondaryActions` + `category` + `trialDays` + `inactivityDays` + `neverStarted` + **`revisionChapters`** par élève + **`allChapsByLevel`** global. boostPendingContent alimenté depuis col S si élève n'a pas encore récupéré le boost | ✅ |
| `publish_admin_boost` | Admin publie boost (→Nouveau Boost col 18) + rebuildSuivi | ✅ |
| `publish_admin_chapter` | Admin publie chapitre (→Nouveau Ch libre) + rebuildSuivi. Retourne `overwrite:true` si >4 chapitres en attente (toast ⚠️ côté frontend) | ✅ |
| `log_manual_email` | Admin — logue un email envoyé manuellement dans l'onglet Emails. Params : `adminCode`, `userEmail`, `type` (ex: `J+0-manuel`). Statut='envoyé' (fix @75) | ✅ |
| `get_daily_checklist` | Checklist quotidienne admin — lit Users/Emails/Boosts/Suivi/Progress, retourne items triés par priorité (boost/chapitre/emails/parent/brevet/inactifs). @75 | ✅ |
| `send_weekly_report` | Envoi manuel du rapport parent hebdo depuis le dashboard admin. Appelle `triggerWeeklyParentReport`. @75 | ✅ |
| `check_trial_status` | Vérifie trial actif { trialActive, daysLeft, isPremium } | ✅ |
| `triggerWeeklyParentReport` | Rapport parent hebdo dimanche 17h-18h (stats semaine, % réussite, chapitres maîtrisés) — trigger à activer manuellement | ✅ |
| `import_chapters` | One-shot admin — pousse chapitres dans Curriculum_Officiel + DiagnosticExos | ✅ |
| `send_test_email` | Admin — envoie email J+0 test | ✅ |
| `mark_all_test` | Admin one-shot — marque tous comptes non-admin sans IsTest → IsTest=1 | ✅ |
| `generate_brevet_session` | Génère session brevet (chapitres → exos mélangés) | ✅ |
| `save_brevet_result` | Sauvegarde résultat brevet dans BrevetResults | ✅ |
| `publish_admin_brevet` | Admin publie brevet blanc personnalisé | ✅ |
| `get_brevet_chapters` | Liste chapitres disponibles dans BrevetExos | ✅ |
| `request_brevet_chapter` | Élève demande chapitre manquant → Insights | ✅ |
| `import_brevet_exos` | One-shot admin — pousse exercices dans BrevetExos | ✅ |
| `publish_admin_revision` | Admin assigne chapitres d'une autre année à un élève → Users col M `RevisionChapters` (JSON) + rebuildSuivi. Payload : `adminCode, targetCode, chapters:[{niveau,categorie}]`. Vide si `chapters=[]` | ✅ |
| `log_contact` | Admin — logue un contact parent effectué dans Insights. Params : `adminCode`, `code`, `prenom`, `niveau`. @76 | ✅ |

### Fonctions internes clés

| Fonction | Rôle |
|---|---|
| `rebuildSuivi(code)` | Recalcule la ligne 👁 Suivi de l'élève (appelé dans save_score, save_boost) |
| `writeToHistorique(p)` | Insère en ligne 2 de 📋 Historique (récent en haut) |
| `updateConfidenceScore(...)` | Met à jour Progress après chaque réponse |
| `_pickDiagExos(exos, chapCount)` | Smart count diagnostic : 1ch→4q, 2ch→6q, 3ch→8q, 4+→10q |

### Rapport matin (generateMorningReport)

Trigger GAS quotidien 7h. Analyse chaque élève :

| Statut | Critères |
|---|---|
| ✅ ACQUISE | score > 80, statut='maitrise', 0 HARD depuis 14j, ≥3 sessions |
| 🔴 BLOQUEE | score < 40, pas d'amélioration 2 semaines, ≥4 sessions |
| 🟡 FRAGILE | score < 40 OU ≥3 HARD cette semaine |
| 📈 EN_PROGRESSION | taux erreur semaine < semaine passée (−10 pts) |
| 📘 EN_COURS | défaut |

Email sujet `[Matheux ⚡ ACTION]` si fragiles/bloquées.

---

## Flux de données principaux

### Inscription → premier boost

**Flux A — Trial Flow (parcours principal, CTA landing)**
```
1. Choix niveau (6EME→3EME) → sélection chapitres déjà vus
2. Quiz diagnostic inline guest (4-10 questions, AVANT inscription)
3. Formulaire prénom + email + mdp → register() GAS
4. GAS : crée Users + email J+0 auto
5. Scores CALIBRAGE sauvés fire-and-forget
6. calDone=true localStorage + suppression CALIBRAGE des cats
7. boostFromDiag() en background → DailyBoosts
8. Onboarding guest (3 slides : bienvenue + boost prêt + action)
9. render() → élève voit son premier boost
```
Deux variantes convergentes : `_flowGuestRegister()` (guest complet) et `_doLoginAndLaunch()` (via `flowRegister()`). Les deux suivent la même logique quand `_flowDiagDone=true`.

**Flux B — Auth Screen (modale connexion/inscription, secondaire)**
```
1. Inscription (prénom + niveau + email + mdp + consentement)
2. Sélection chapitres → finalizeOnboarding()
3. generate_diagnostic API + login silencieux
4. Onboarding 3 slides → startCal() → diagnostic DANS l'app
5. chkComp('CALIBRAGE') → boostFromDiag() → boost prêt
```

### Exercice → suivi admin

```
1. Élève répond à un exercice
2. Frontend → save_score(code, categorie, resultat, temps, ...)
3. GAS : écrit Scores + updateConfidenceScore(Progress) + rebuildSuivi(code) + writeToHistorique
4. 👁 Suivi mis à jour → ACTION NICOLAS recalculé
5. Nicolas voit l'action dans le dashboard admin
```

### Publication boost (admin)

```
1. Nicolas ouvre admin → voit ⚡ BOOST TERMINÉ
2. Copie prompt Claude → génère JSON 5 exos (+ motProf optionnel)
3. Colle dans "Publier un boost" → publish_admin_boost GAS
4. GAS : écrit { insight, exos, motProf } dans →Nouveau Boost (col S Suivi) + rebuildSuivi
5. Admin clique sur l'élève (onglet Traité) → aperçu structuré : motProf + insight + 5 questions
   (boostPendingContent lu depuis col S tant que l'élève n'a pas encore récupéré le boost)
6. Au prochain login élève : login() lit col S → crée DailyBoosts (exosDone=0) + vide col S
7. Si motProf présent : S._motProfScreen = 'boost' → écran "Un mot de ton prof 💬" avant les exos
8. Admin voit ⏳ En attente dans DailyBoosts
```

---

## Infrastructure

| Service | Usage | Coût |
|---|---|---|
| GitHub Pages | Frontend (index.html, pages légales) | Gratuit |
| Google Apps Script | Backend API | Gratuit (quotas Google) |
| Google Sheets | Base de données | Gratuit |
| Gmail (GmailApp) | Emails auto (J+0, J+3, J+5, J+7 personnalisés objectif + rapport parent hebdo) — alias no-reply@matheux.fr requis | Gratuit |
| Stripe | Paiement PROD (19,99€/mois, limite 50, webhook déployé @85) | ~0,39€/transaction |
| GA4 | Analytics | Gratuit |

Commandes de déploiement : voir [claude.md](claude.md#déploiement).

### Vulnérabilités connues — audit 17 mars 2026

| Risque | Sévérité | Détail | Fix |
|--------|----------|--------|-----|
| Webhook Stripe sans HMAC-SHA256 | 🔴 CRITIQUE | Seule vérif = `metadata.secret` en clair → faux webhook possible | Implémenter `stripe-signature` header |
| `SHARED_SECRET` hardcodé | 🔴 CRITIQUE | backend.js L5404 en plain text | → `PropertiesService` |
| `triggerDailyMarketing` Premium='1' | 🟠 HAUTE | String '1' non détecté → emails relance aux payants | Ajouter `String(premium)==='1'` L4635 |
| `ensureUsersCols` race condition | 🟡 MOYEN | 2 requêtes simultanées → colonnes dupliquées | Lock ou check post-insert |
| `saveScore` DailyBoosts ExosDone | 🟡 MOYEN | Si row DailyBoosts pas encore créée → ExosDone=0 | Créer row si absente |
| Rate limiting par email | 🟡 MOYEN | Changer email = reset compteur | Acceptable MVP |

---

## Scripts Python utilitaires

### Actifs (racine)

| Script | Usage |
|---|---|
| `sheets.py` | Bibliothèque accès Google Sheets (utilisée par tous les scripts) |
| `rebuild_sheet.py` | Reconstruit 👁 Suivi + 📋 Historique |
| `test_full_v2.py` | Suite de tests complète (74/74) |
| `test_simulation_40.py` | Simulation 40 élèves × 15 jours (17/17, 1616 appels) |
| `sim_21days.py` | Simulation 21j — 12 profils QA |
| `audit_exos.py` | Audit qualité exercices collège |
| `verify_hints.py` | Audit qualité des indices |
| `test_coherence_boost.py` | Test régression calibrage/boost |
| `deploy.sh` | Script de déploiement GAS (push + deploy) |

### Utilitaires (scripts/)

| Script | Usage |
|---|---|
| `scripts/setup_test_profiles.py` | Setup 6 profils test admin |

### Archivés (scripts/archive/)

Scripts one-shot déjà exécutés : imports, migrations, fix one-shot, anciens tests, sécurité freelance. Ne pas utiliser.

---

## Fonctionnalités stables

> Ne pas toucher sans raison explicite.

- CSS/UI complet, mobile-first, animations
- **3 classes dark distinctes** : `land-night` (landing, toggle nav), `adm-dark` (admin cockpit), `app-night` (app élève, bouton 🌙 header, localStorage `app_night`)
- Landing page : hero direct, 3 faits, prix seul, CTA final
- Mode Brevet Blanc : onglet 🎓 Brevet (3EME), 120 exos, quiz sans indices, résultats détaillés
- Mode Révision : admin assigne chapitres d'une autre année → badge 🔁 + toast élève (col M `RevisionChapters`)
- Feedback non-intrusif : bouton "Signaler" → Insights
- Auth register + login + auto-login silencieux (modale protégée contre interruption trial-flow CTA)
- Scores enrichis : temps, wrongOpt, indices, formule
- Swipe gauche → exercice suivant
- Admin cockpit (triple-clic logo) : 5 onglets À FAIRE / FAIT / MAILS / INACTIFS / RAPPORT — À FAIRE = boost+chapitre uniquement, emails dans onglet dédié, inactifs >3j visibles, rapport dimanche avec JSON semaine
- Gamification : XP, streak, mastery ring SVG
- KaTeX v0.16.9 (rendu maths), chrono par exercice
- Nudge pills après 20s, tableau blanc maths
- Vue Progression refonte : header (maîtrisés/streak/score moy.), barre colorée progressive (rouge→orange→bleu→vert), message contextuel, tri en cours/maîtrisés/non commencés, bannière prérequis fragiles
- Règle 1 chapitre/jour : **DÉSACTIVÉE** — tous les chapitres accessibles en permanence. Animation informative "prochain chapitre en préparation" après complétion (chapitre + boost), ne bloque rien
- Essai 7j : badge J-X, overlay, onboarding 3 slides
- Flow landing CTA complet
- Post-boost : confettis + auto-redirect 5s
- Modales admin contextuelles (BOOST/CHAPITRE séparés)
- Indicateurs emails J0/J3/J5/J7 smart dans modal admin (vert=envoyé, rose=DUE, gris=pas encore)
- Onglet "📧 Suivi" : élèves avec actions secondaires (emails dus, inactifs, jamais commencés)
- Messages élèves adaptatifs : `_msg()` + `_MSGS` (~35 entrées), coach marks (indice/boost/brouillon), _OK/_KO contextuels par niveau/mode, onboarding dynamique selon objectif
- **Mode nuit app** : bouton 🌙 dans le header, `body.app-night`, persisté `localStorage('app_night')`
- **Boost reopen nav** : navigation Précédent/Suivant après boost terminé (comme les chapitres)
- **Guide "Commence par là"** : affiché uniquement après boost consommé (pas au premier chargement)
- **Titres chapitres** : `font-weight:800` explicite pour cohérence visuelle
