# Architecture — Matheux

> Structure technique frontend/backend, flux de données, scripts utilitaires.
> Voir aussi [claude.md](claude.md) pour les règles, [database.md](database.md) pour le schéma Sheets, [product.md](product.md) pour le produit.

---

## Vue d'ensemble

```
                    matheux.fr (GitHub Pages)
                    ┌─────────────────────────────────────┐
                    │                                     │
                    │  index.html (Next.js SSG ~4000L)    │  ← Landing marketing SEO
                    │  Visiteur froid → conversion         │  ⚠️ Ne pas modifier le DOM (React hydration)
                    │  Connecté → redirect /app.html      │
                    │                                     │
                    │  app.html (vanilla JS ~13000L)      │  ← SPA applicative
                    │  Non-connecté → écran minimal       │
                    │  Connecté → auto-login → dashboard  │
                    │                                     │
                    └────────────┬────────────────────────┘
                                 │
                    fetch POST (JSON body)
                                 │
                    ┌────────────▼────────────────────────┐
                    │  SUPABASE EDGE FUNCTION (index.ts)  │
                    │  HTTP POST → dispatch action        │
                    │  ~37 actions, Deno runtime           │
                    │  Lit/écrit Supabase PostgreSQL       │
                    └────────────┬────────────────────────┘
                                 │
                    Supabase PostgreSQL (prod)
                    Project: matheux-prod (West EU Paris)
                    14 tables + RLS
                                 │
                    ┌────────────▼────────────────────────┐
                    │  GOOGLE APPS SCRIPT (backend.js)    │
                    │  Emails uniquement (GmailApp)       │
                    │  Proxyé depuis Edge Function         │
                    └─────────────────────────────────────┘
```

| Composant | Technologie | Fichier | Taille |
|---|---|---|---|
| Landing SEO | Next.js SSG (build exporté, source hors repo) | `index.html` | ~4000 lignes |
| App SPA | HTML + CSS vars + Tailwind CDN + JS vanilla | `app.html` | ~13000 lignes |
| Backend API | Supabase Edge Function (Deno) | `supabase/functions/api/index.ts` | ~900 lignes |
| Backend emails | Google Apps Script (V8) — GmailApp only | `backend.js` | ~5300 lignes |
| Base de données | Supabase PostgreSQL (West EU Paris) | `supabase/schema.sql` | 14 tables + RLS |
| Base legacy | Google Sheets (backup, emails) | — | 14 onglets |
| Hébergement | GitHub Pages | `matheux.fr` | Auto-deploy sur push |
| Backend hosting | Supabase Edge Functions | `xlfzhcanzmqqlxtavzrd.supabase.co` | — |
| Auth | SHA-256 client-side → Supabase Auth (bcrypt) | localStorage `boost_v23` | Hash SHA-256 = mot de passe Supabase |
| Emails | GAS GmailApp (proxy depuis Edge Function) | `send_welcome_email` | Migration Resend prévue à ~50 users |
| PWA | manifest.json + sw.js (cache v11) | `app.html` scope | Standalone, portrait. Nudge toutes les 2 connexions (`mx_pwa_logins`). Tracking `_trackPwa()` → localStorage + GAS `log_event` |

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
| Landing (app.html) | Écran minimal dans `#landing-screen` (logo + 2 CTA + rassurance) | Non-connecté sur /app.html. La landing marketing SEO est dans index.html (Next.js) |
| Trial Flow | `startTrialFlow()` → overlay fullscreen (`#trial-flow.flow-fs`) | Quiz diagnostic inline pre-inscription. `flowSelectLevel()` skip direct au diag pour 3EME. guestDiag supprimé (pas de resume). Fill filtré (`_pickDiagExos`) |
| Chapitres | `rSection('CHAPITRES', ...)` | Liste des chapitres + "Mon Boost du jour" |
| Exercice | `rSection('EXERCICE', ...)` | Quiz avec indices/formule. Format v4 : contexte parapluie sticky (`data._ctx`), tables HTML (`data.table`), consigne dessin (`data.draw`), formule masquable (`data.f_disabled`) |
| Calibrage | `rSection('CALIBRAGE', ...)` | Diagnostic express (5 questions, ~1 min). Banque 54 questions dans DiagnosticExos |
| Progression | `rSection('PROGRESSION', ...)` | Barres de progression par chapitre |
| Brevet | `rSection('BREVET', ...)` | Mode brevet blanc (3EME only) |
| Admin | `rSection('ADMIN', ...)` | Cockpit admin @88 — 6 onglets : À FAIRE / NOUVEAU / FAIT / MAILS / INACTIFS / RAPPORT. NOUVEAU = inscrits du jour + statut mail J+0. Boutons "Copier JSON complet" (exos+résultats+temps+indices+formule). Profils test visibles. |

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
- Toutes les données viennent de Supabase à chaque login (pas de cache de données)

### Librairies externes (CDN)

- **Tailwind CSS** : utilities responsive
- **KaTeX v0.16.9** : rendu LaTeX (defer + queue retry, fallback 3s)
- **Syne** + **DM Sans** : Google Fonts

### Gamification

- **XP** : points d'expérience cumulés
- **Streak** : jours consécutifs d'activité
- **Mastery ring** : cercle SVG de progression par chapitre
- **Confettis** : animation post-boost terminé
- **Timer exercice** : cercle SVG 60s par exercice (pas CALIBRAGE/BREVET). Doux, ambre après dépassement, désactivable. `_isTimerOn()`, `_startTimer(id)`, `_stopTimer()`. Persisté `mx_timer_{code}`
- **Mode Flow** : 5 EASY consécutifs en ≤60s → XP ×2 pendant 5 exos. `_checkFlowOnAnswer()`, `_flowXPMultiplier()`. Badge ⚡×2 dans gamif-row. Overlay activation
- **Tri chapitres dashboard** : BOOST (fixe en tête) → **assignés par le prof** (`S.assignedByProf`, persisté `mx_assigned_{code}` localStorage) → entamés (exos faits hors calibrage, pas terminés) → révision (cross-niveau) → pas commencés → terminés. Basé sur `S.chapTouched` (exclut `source=CALIBRAGE` et `source=BOOST`). Flèches tendance via `S.chapSessions` (même filtrage — pas de session fantôme sur chapitres seulement diagnostiqués). Le tri s'applique aussi dans `renderProgress()` (vue progression) : les chapitres `assignedByProf` sont pinnés en premier
- **Panneau inscrits admin** : clic sur KPI "Inscrits total" → toggle liste triée par jours actifs décroissant (prénom, niveau, email, jours actifs, date inscription). `activeDays` = dates distinctes dans Scores (toutes sources, sans cutoff)
- **Messages adaptatifs** : système `_msg(key, vars)` avec `_MSGS` (~35 entrées), adaptation niveau (6EME/3EME/def), arrays aléatoires, substitution variables `{name}` `{n}` `{s}`. Coach marks persistés localStorage (`mx_coach_v1`). Voir [messages.md](messages.md)
- **Brouillon contextuel + Calculette** : mobile = bottom sheet 50vh avec onglets (brouillon|calculette), desktop = panneau latéral droit 1/3 écran avec les 2 fusionnés (calculette en haut, brouillon en bas). Brouillon : symboles adaptés au chapitre via `getContextSymbols(niv, cat)`, mode quadrillé toggle. Calculette : adaptée par niveau/chapitre (trig si géo, π si aires/volumes, puissances si 5EME+, fractions si 6EME), mémoire M+/MR, copie vers brouillon.
- **Figures géométriques SVG** : auto-détection depuis le texte de la question + catégorie. Moteur `autoDetectFigure(q, cat)` → `renderFig(fig)` → SVG inline animé. **18 types** : triangle rectangle, trigo, Thalès, cercle (+ mode diamètre), rectangle/carré, angle (3 lettres), parallèles/perpendiculaires, symétrie axiale/centrale (3 paires A/A'), cube/pavé, cylindre, cône, pyramide, sphère, section de solide, homothétie, triangles semblables, transformations, **vecteurs/produit scalaire** (1ERE), **repère orthonormé** (1ERE), **cercle trigonométrique** (1ERE). Lettres de points extraites dynamiquement de l'énoncé (`pts[]`). Filtrage `nonGeoChaps` (pas de figure sur algèbre/stats/probas). viewBox 280×210, `overflow:visible`. Champ `fig` optionnel dans les exercices JSON pour override manuel. Fallback safe : pas de figure si non détecté. **3 garde-fous anti-fuite** (@audit 2026-03-19) : (1) filtre V/F + questions de cours (regex vrai/faux, théorème, définition, énoncer, citer, compléter → `return null`), (2) exclusion angles opposés par le sommet (la figure révèle visuellement la réponse), (3) labels fallback masqués — quand aucun point n'est extrait de l'énoncé, `_fb:true` → `pts` remplacés par espaces pour ne pas afficher A/B/C génériques.

---

## Backend API — Supabase Edge Functions

> Depuis le 02/04/2026. Remplace GAS comme API principale.
> Source : `supabase/functions/api/index.ts` (~900 lignes, Deno runtime)
> URL : `https://xlfzhcanzmqqlxtavzrd.supabase.co/functions/v1/api`
> Dispatch sur `action` dans le body JSON (même pattern que l'ancien GAS `doPost`)

Toutes les actions métier (register, login, save_score, publish, etc.) passent par l'Edge Function.
GAS est conservé uniquement pour l'envoi d'emails (GmailApp). L'Edge Function proxy vers GAS pour `send_welcome_email`.

### Optimisations scale (02/04/2026)

| Optimisation | Avant | Après | Impact |
|---|---|---|---|
| **save_score UPSERT** | SELECT count dedup + INSERT | Single UPSERT ON CONFLICT | -1 query/score |
| **save_scores_batch** | 5 appels HTTP/boost (1 par exo) | 1 appel batch (jusqu'à 25 scores) | ÷5 appels réseau |
| **Cache curriculum** | Query DB à chaque login | In-memory cache 5 min TTL | -1 query/login |
| **History 60 jours** | SELECT * sans limite temporelle | `.gte("date", 60j)` + colonnes allégées | Réponse login plus légère |

### Améliorations futures (Supabase Pro, ~100+ users actifs)

- **Connection pooling PgBouncer** — pool dédié, meilleure gestion des connexions concurrentes
- **Read replicas** — séparer lectures lourdes (login) des écritures (save_score)
- **Monitoring intégré** — alertes latence, erreurs, usage DB
- **Backup PITR** — point-in-time recovery (inclus dans Pro)
- **Migration Resend** — remplacer GAS emails par Resend (~3$/mois) pour fiabilité et templates FR

---

### Actions Supabase Edge Function (complètes)

> Source : `supabase/functions/api/index.ts`. Dispatch sur `action` dans le body JSON.

**Actions métier (implémentées) :**

| Action | Description |
|---|---|
| `register` | Inscription élève. Auth Supabase + profil + email J+0 (proxy GAS) |
| `login` | Connexion. Retourne profil, boost, chapitres, history, cours, trial |
| `save_score` | Sauvegarde réponse (UPSERT dedup) + MAJ progress + ExosDone |
| `save_scores_batch` | Batch jusqu'à 25 scores en 1 appel (frontend flushQ) |
| `save_boost` | Sauvegarde fin de boost (ExosDone) |
| `save_calibration_batch` | Sauvegarde diagnostic (batch scores calibrage) |
| `generate_diagnostic` | Génère quiz diagnostic (5 questions, fuzzy match chapitres) |
| `get_progress` | Progression par chapitre + boost du jour / rattrapage |
| `check_trial_status` | Vérifie trial { trialActive, daysLeft, isPremium } |
| `submit_feedback` | Feedback élève → table insights |
| `report_exo` | Signalement exercice → table insights |
| `log_contact` | Contact parent → table insights |
| `send_contact` | Formulaire contact → table contact |
| `forgot_password` | Reset MDP via Supabase Auth |
| `reset_password` | Nouveau MDP (token Supabase Auth) |
| `unsubscribe` | Désinscription email → table emails |
| `get_admin_overview` | Vue admin complète (tous les élèves + statuts) |
| `publish_admin_boost` | Admin publie boost (suivi.boost JSON + publishDate) |
| `publish_admin_chapter` | Admin publie chapitre (suivi.chap1..4 JSON + publishDate) |
| `log_manual_email` | Admin logue email envoyé manuellement |
| `get_cours_admin` | Admin récupère cours par chapitre |
| `save_cours` | Admin sauvegarde cours (section_10, section_20) |
| `get_brevet_chapters` | Liste chapitres BrevetExos |
| `generate_brevet_session` | Génère session brevet (chapitres → exos mélangés) |
| `save_brevet_result` | Sauvegarde résultat brevet |
| `stripe_webhook` | Webhook Stripe (paiement → premium) |

**Actions NOOP (retournent success, à implémenter si besoin) :**
`add_teasing_early`, `detect_fragile_prereqs`, `enqueue`, `generate_daily_boost`, `generate_revision`, `log_event`, `mark_all_test`, `simulate_next_day`, `get_audit_exos`, `get_audit_remarks`, `publish_admin_brevet`, `publish_admin_revision`, `request_brevet_chapter`

**Actions proxyées vers GAS (emails uniquement) :**
`send_test_email`, `send_weekly_report`, `send_custom_email`, `send_session_rapport`

---

## Backend Emails — Google Apps Script (LEGACY)

> `backend.js` (~5300L) — conservé uniquement pour GmailApp (envoi d'emails).
> Plus aucune action métier ne passe par GAS. Le frontend appelle Supabase Edge Functions.
> L'Edge Function proxy vers GAS pour les 4 actions email ci-dessus.
> Migration vers Resend (~3$/mois) prévue à ~50 users actifs.

---

## Flux de données principaux

### Inscription → premier boost

**Flux A — Trial Flow (parcours principal, CTA landing) @92**
```
1. Choix niveau (6EME→3EME) → sélection chapitres ("Je ne sais pas trop" = auto-select 65%)
2. Quiz diagnostic inline guest (4-10 questions, AVANT inscription)
3. Carte résultat (barre animée + récit + tags chapitres solides/faibles + objectif picker intégré)
4. Formulaire prénom + email + mdp → register() Supabase Edge Function
5. Edge Function : crée profile + Supabase Auth + email J+0 auto (via GAS proxy)
6. Scores CALIBRAGE sauvés fire-and-forget
7. calDone=true localStorage + suppression CALIBRAGE des cats
8. boostFromDiag() en background → DailyBoosts
9. Onboarding guest (2 slides : "Ton espace est créé" + "Ton entraînement est prêt")
10. render() → élève voit son premier boost
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
2. Frontend → sendScore() ajoute le payload (avec answeredAt = date client) dans S.scoreQueue (persisté localStorage['sq'])
3. flushQ() envoie un par un → vérifie response.ok + json.status === 'success' avant de retirer de la queue
4. Si échec réseau/serveur : retry backoff exponentiel (2s→30s) + flush périodique toutes les 30s
5. GAS saveScore() : utilise p.answeredAt (date réelle de la réponse) au lieu de today()
6. GAS : écrit Scores + updateConfidenceScore(Progress) + rebuildSuivi(code) + writeToHistorique
7. 👁 Suivi mis à jour → ACTION NICOLAS recalculé
8. Nicolas voit l'action dans le dashboard admin
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
| GitHub Pages | Frontend (index.html, app.html, pages légales) | Gratuit |
| **Supabase Edge Functions** | **Backend API principal** (Deno, ~37 actions) | Gratuit (Free tier) |
| **Supabase PostgreSQL** | **Base de données principale** (14 tables, RLS) | Gratuit (Free tier, 500 MB) |
| **Supabase Auth** | Authentification (bcrypt, JWT ECC) | Gratuit (Free tier, 50K users) |
| Google Apps Script | **Emails uniquement** (GmailApp — J+0, rapports, notifs) | Gratuit (quotas Google) |
| Google Sheets | **Legacy backup** — référence historique, plus écrit en prod | Gratuit |
| Gmail (GmailApp) | Alias no-reply@matheux.fr. Migration Resend prévue à ~50 users | Gratuit |
| Stripe | Paiement PROD (19,99€/mois, webhook déployé @85) | ~0,39€/transaction |
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
| `test_full_v2.py` | Suite de tests complète (66/72, 6 fails = gate J+1 attendu) |
| `test_coherence_boost.py` | Test régression calibrage/boost (14/14) |
| `validate_exos.py` | Gate qualité exercices JSON |
| `check_students.py` | Health check données élèves |
| `audit_exos.py` | Audit qualité exercices collège |
| `deploy.sh` | Script de déploiement GAS (push + deploy) — emails uniquement |

### Legacy (encore présents mais utilisent Google Sheets — plus en prod)

| Script | Usage |
|---|---|
| `sheets.py` | Bibliothèque accès Google Sheets (legacy, backup) |
| `rebuild_sheet.py` | Reconstruit 👁 Suivi + 📋 Historique (legacy) |
| `test_simulation_40.py` | Simulation 40 élèves × 15 jours (legacy) |

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
- Admin cockpit (triple-clic logo) : 6 onglets À FAIRE / NOUVEAU / FAIT / MAILS / INACTIFS / RAPPORT — À FAIRE = boost+chapitre uniquement, emails dans onglet dédié, inactifs >3j visibles, rapport dimanche avec JSON semaine
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
- **Admin master password** (@122) : `ADMIN_MASTER_PWD` dans Script Properties. Login avec le master pwd sur n'importe quel compte élève → `isAdminLogin=true` → mode read-only complet (ne consomme pas nextChapter/nextBoost, n'écrit pas dans DailyBoosts, ne rebuildSuivi pas). Permet à Nicolas de vérifier l'état d'un élève sans interférer avec ses données
