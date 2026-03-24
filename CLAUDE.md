# CLAUDE.md — Matheux · Règles du jeu

> Document unique. Point d'entrée + règles métier + contraintes techniques.
> Tout ce qui n'est pas ici est dans docs/ ou dans le code.
> GAS @112 · Lancé le 18 mars 2026

---

## 0. Projet en 30 secondes

Matheux (matheux.fr) est une SPA vanilla JS (`index.html` ~9900L) + backend Google Apps Script (`backend.js` ~5300L) sur Google Sheets.
Soutien scolaire maths adaptatif, 6ème→3ème + 1ère Spé Maths.
Fondateur solo : Nicolas Follezou. Objectif : 50 clients à 19,99€/mois.

---

## 1. Rôle de l'IA

> Ce rôle s'applique à **l'agent principal** (conversation par défaut). Les agents spécialisés (prescribe, ux-audit) ont leur propre identité définie dans `.claude/agents/`.

Tu es le **dev senior** du projet Matheux. Nicolas décide, tu exécutes.

1. **Comprendre** les demandes de Nicolas
2. **Implémenter** dans la codebase existante (patches chirurgicaux)
3. **Maintenir** la documentation vivante
4. **Alerter** si une action risque de casser l'architecture ou la BDD
5. **Déléguer** aux agents spécialisés quand c'est leur domaine

### Agents spécialisés — l'équipe

| Agent | Fichier | Rôle | Quand l'utiliser |
|---|---|---|---|
| **Monsieur Exos** | `.claude/agents/prescribe.md` | Analyse des résultats élèves, génération d'exercices personnalisés, injection en brouillon | Chaque matin : "prépare les exos" |
| **UX Engineer** | `.claude/agents/ux-audit.md` | Audit cohérence états/affichage, vérification invariants, détection edge cases | Après chaque session de code, ou sur demande |
| **Luna** | `.claude/agents/growth.md` | Acquisition, contenu, stratégie growth, calendrier d'actions | Quand Nicolas parle d'acquisition, marketing, landing page, réseaux sociaux |

**Règles de délégation :**
- Quand Nicolas parle d'exercices (créer, corriger, prescrire) → lancer **Monsieur Exos** (`/agent prescribe`)
- Quand Nicolas demande un audit, une vérification, ou après des modifs front → lancer **UX Engineer** (`/agent ux-audit`)
- Quand Nicolas parle d'acquisition, marketing, contenu, landing page → lancer **Luna** (`/agent growth`)
- Le CTO (toi) coordonne et code. Les agents diagnostiquent et proposent, Nicolas valide.

---

## 2. Règles de développement — INVARIANTS TECHNIQUES

### Patches chirurgicaux uniquement
- Codebase **GOLD MASTER** — ne jamais réécrire
- `index.html` ~9900 lignes → **ne jamais diviser**
- Vanilla JS, pas de framework, pas de bundler
- Modifier **uniquement** la fonction concernée par la tâche
- Ghost divs z-index : `renderArchiveSection` content needs `position:relative;z-index:3` to render above `.chap-stack-ghost` elements

### CORS GAS — critique
```
⛔ INTERDIT : headers: { 'Content-Type': 'application/json' }
✅ CORRECT  : fetch(URL, { method: 'POST', body: JSON.stringify({...}) })
```
Preflight OPTIONS non supporté par GAS → CORS bloqué depuis matheux.fr.

### Schéma Google Sheets
- Ne **jamais** changer de colonnes sans documenter dans [database.md](docs/database.md)
- Index de colonnes **hardcodés** dans le backend → toute modification non documentée casse tout
- ⚠️ `Users.Code` (col A) = **clé primaire** — le backend `getRows` mappe par header, donc si la colonne ou le header disparaît, `user['Code']` = undefined → tous les `history`, `progress`, `boost` reviennent vides → quiz diagnostic forcé pour tous les élèves (incident 2026-03-23)

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

### Pas de sur-ingénierie
- Pas de feature flags, pas d'abstractions prématurées
- Si faisable manuellement par Nicolas en 2 min → ne pas automatiser
- 3 lignes dupliquées > 1 abstraction inutile

---

## 3. Règles métier — INVARIANTS PRODUIT

> Ces règles définissent le comportement attendu du produit.
> Les modifier sans validation Nicolas = bug métier.

### 3.1 Pédagogie

| # | Règle | Détail |
|---|-------|--------|
| P1 | **Diagnostic avant tout** | L'élève est testé sur ses chapitres sélectionnés avant de commencer |
| P2 | **Boost quotidien = 5 exercices** | Ciblés sur les lacunes, ~10 min |
| P3 | **Chapitres = 20 exercices** | 10 fondamentaux (lvl:1) + 10 avancés (lvl:2) |
| P4 | **Tous les chapitres accessibles** | Pas de verrou, pas de limite 1/jour |
| P5 | **Nicolas assigne manuellement** | Prochain chapitre et prochain boost via admin |
| P6 | **Indices progressifs** | 1-3 étapes + formule clé révélée après erreur |
| P7 | **3 types d'exercices** | QCM (défaut), Vrai/Faux (`vf`), Trou à compléter (`fill`). Fill : rendu `___` en 2 temps — `\text{___}` dans LaTeX → `\boxed{\phantom{xx}}` avant KaTeX, puis `___` texte brut → span HTML stylé après KaTeX. Comparaison réponse via `_normFill()` : normalise `\frac{a}{b}` → `a/b`, `\times` → `×`, supprime `$`, espaces, `\text{}`. Pas de bouton "Révéler la réponse" sur les fill (guard `exoType !== 'fill'`) |
| P8 | **Scoring tri-niveau** | EASY = correct 1er essai (succès, compte pour le %). MEDIUM = correct après indices ("hésitation", ne compte PAS). HARD = mauvaise réponse (ne compte PAS). Score % = EASY / total exercices × 100. S'applique partout : scores chapitres, sessions retro, pills, flèches tendance, comparaison live |
| P9 | **Boost rattrapage** | Si aucun boost aujourd'hui, servir le dernier boost non terminé (ExosDone < 5). Le save_score incrémente la bonne ligne. Un boost n'est jamais perdu silencieusement |
| P10 | **Chapitre terminé — tri stable** | Quand plusieurs chapitres ont la même DernierePratique, celui avec le plus d'exos (≥20 = terminé) est prioritaire. Évite qu'un chapitre en cours masque un chapitre terminé dans l'admin |

### 3.2 Trial & Conversion

| # | Règle | Détail |
|---|-------|--------|
| T1 | **7 jours gratuits** | Accès complet, sans carte bancaire |
| T2 | **19,99 €/mois** | Prix unique, pas de paliers |
| T3 | **Badge trial progressif** | J-5 bleu → J-3 jaune → J-1 orange |
| T4 | **J+7 overlay bloquant** | Lien Stripe direct |
| T5 | **Emails séquencés** | J+0 auto, J+3/J+5/J+7 manuels (trigger à activer dès 10 clients) |
| T6 | **Désinscription emails** | `unsubscribe.html` + action GAS `unsubscribe` → log UNSUB dans onglet Emails. Check `_isUnsubscribed()` avant chaque envoi marketing |

### 3.3 Messages — invariants figés @95

> **Prouvés par simulation (274 API calls, 267 messages, 0 incohérence).**
> **Ne JAMAIS modifier sans relancer `python3 sim_7days_messages.py` après.**

| # | Invariant | Détail |
|---|-----------|--------|
| M1 | **Toast mutex** | `_toastBusy` + `_toastQueue` — jamais 2 toasts visibles. `dur=0` bypass (loading). `hideT()` reset tout |
| M2 | **Hero CTA exclusif** | Cascade P1→P2→P3→P4→P4b→P5 + fallback DONE. Exactement 1 hero par session. Chaque niveau a `if (!_hero)` + `break`. **P2** : chapitres `assignedByProf` (persisté `mx_assigned_{code}` localStorage) → hero "Ton prof te recommande" **prioritaire sur chapitres en cours et boost**. P3 : chapitre en cours (done > 0). P4 : chapitre ciblé par boost. P4b : chapitre NEW (isNew flag) |
| M3 | **boostConsumed date-stamped** | `boostConsumedDate` dans localStorage. Expire si `!== tod()`. Jamais stale le lendemain |
| M4 | **Coach tip vs toast ko** | `if/else` exclusif dans `validateAnswer`. Coach tip AVANT le panel aide |
| M5 | **Milestones/Coach namespacés** | `mx_ms_{code}` / `mx_co_{code}` dans localStorage. Pas de pollution cross-user |
| M6 | **Streak dedup** | Toast login skip si `_stkMileDup` (milestone streak_3/7 va fire) |
| M7 | **"demain"** | Autorisé dans `boost_preparing` et les bandeaux post-complétion (hero vert, archive boost, archive chapitre). Interdit dans les toasts et coach tips |
| M8 | **pendingManual cleanup** | Effacé dans les 3 branches de `nextChapter` (PENDING_MANUAL / JSON / string) |

### 3.4 Gamification

| # | Règle | Détail |
|---|-------|--------|
| G1 | **XP** | +200 boost, +300 chapitre (4×75 par slot si ≥20 exos) — même les erreurs comptent |
| G2 | **6 paliers maîtrise** | À découvrir / En cours / En progrès / Solide / Maîtrisé / Expert |
| G3 | **Streak freeze** | 1j/semaine si streak ≥2 et avant-hier actif |
| G4 | **6 milestones** | Premier boost, 10 exos, streak 3j/7j, 1er chapitre, 100 exos |
| G5 | **Tour guidé** | 8 étapes (incl. chrono), 1 seule fois post-inscription, guard `_needsCoach('TOUR')` / `_markCoach('TOUR')` |
| G6 | **Tuto régressif** | 8 micro-tips first-use (T1-T8), `_needsCoach/_markCoach`, disparaissent après 1 affichage |
| G7 | **Slots de 5** | Chapitres ≥20 exos découpés en 4 slots visuels (5/10/15/20). Overlay récompense +75 XP aux paliers 5/10/15. Palier 20 absorbé par `chkComp`. Chapitres <20 exos : pas de slots, +300 XP classique. Count-based (pas index-based) — fire au 5ème exo fait, quel que soit l'ordre. Absorbe `_checkCoursMilestone` quand un slot fire |
| G8 | **Daily goal** | Mission du jour = 5 exos (tous types). Overlay +50 XP au 5ème exo. Absorbé dans le slot overlay si simultané. Absorbé silencieusement si `chkComp` fire. Compteur `🎯 n/5` dans le header. Reset quotidien via `mx_daily_{code}` localStorage |
| G9 | **Sessions retro avec %** | Chapitres et boosts terminés : pills par **date** (pas "Passage N"). Score % coloré sur chaque pill (vert ≥70%, ambre ≥40%, rose <40%) + flèche `↑/↓/→` vs session précédente. Pas de ligne "Terminé le...". Carte fermée : dernier score % + `×N passages` + flèche tendance. Exercices retro affichés en read-only (même template visuel que les exercices actifs) avec **barre de numéros cliquable** (dots colorés : vert=EASY, ambre=MEDIUM, rouge=HARD, gris=non répondu) pour navigation directe. Système de pills unifié pour chapitres et boosts |
| G10 | **Comparaison live** | Chapitre en cours (ouvert, `done > 0`, pas terminé) : bandeau gris `Session en cours — xx% (n/done) ↑ vs yy%`. Affiché uniquement si ≥1 passage complet existe. Compare le % instantané (EASY/done) vs le % du dernier passage complet |
| G11 | **Message anticipation** | Post-complétion boost : "Tes prochains exos sur mesure arrivent demain matin 🔥". Post-complétion chapitre : "Tes prochains exos sur mesure arrivent demain matin 🎯". Crée l'anticipation du retour J+1 |
| G12 | **Timer exercice** | 60s par exercice, cercle SVG animé. Doux (bleu→ambre après 60s), aucune pénalité. Désactivable via clic toggle (persisté `mx_timer_{code}`). Pas affiché sur CALIBRAGE. Coach tip `tip_timer` au premier usage |
| G13 | **Mode Flow** | 5 exos EASY consécutifs répondus en ≤60s → XP ×2 pendant 5 exos. Overlay activation. Badge ⚡×2 dans gamif-row. Multiplie uniquement les XP exercices (pas slot/daily/chapitre). Reset streak si HARD/SKIP/overtime (sauf si flow déjà actif) |

### 3.5 Admin

| # | Règle | Détail |
|---|-------|--------|
| A1 | **Triple-clic logo** | Accès admin (comptes IsAdmin uniquement) |
| A2 | **6 onglets** | À FAIRE / NOUVEAU / FAIT / MAILS / INACTIFS / RAPPORT |
| A3 | **4 statuts ACTION** | 🔴 BLOQUÉ (inactif >7j + <40%) / ⚡ BOOST TERMINÉ / ✅ CHAPITRE TERMINÉ / 👍 RAS |
| A4 | **Workflow boost/chapitre** | Semi-auto : IA analyse + génère → admin "📦 À VALIDER" → aperçu élève → publier. Fallback manuel : Copier JSON → Claude → coller → publier |
| A5 | **Limite bêta** | 50 vrais élèves (IsTest=0) |

---

## 4. Workflow technique

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
python3 sim_7days_messages.py   # Simulation messages — 0 incohérence
python3 rebuild_sheet.py        # Reconstruire Suivi + Historique
```

### Setup élève existant (bypass onboarding)

Quand Nicolas veut ajouter un élève déjà connu (visio en cours) **sans lui faire passer le quiz diagnostic** :

1. **Créer le user** dans `Users` via `sheets.py` (ou via inscription normale)
2. **Injecter 1 score CALIBRAGE minimal** dans `Scores` (chapitre ≠ celui qu'on veut vierge) → `history.length > 0` → bypass le quiz diagnostic (condition ligne ~4939 : `d.history.length === 0 ? 'sel' : null`)
3. **Injecter le chapitre prioritaire** dans `👁 Suivi` col G (JSON complet avec `categorie`, `titre`, `icone`, `exos`, `insight`) → au login, le backend le consomme via `nextChapter` + vide la cellule. Le frontend set `S.assignedByProf` + persiste dans `mx_assigned_{code}` localStorage
4. **Le boost du jour** doit rester à `ExosDone=0` pour que l'élève ait son entraînement à faire

⚠️ **Pièges** :
- `nextChapter` est **one-shot** : le backend le consomme au premier login et vide Suivi col G. Si on doit réinjecter, remettre le JSON dans col G
- Les scores CALIBRAGE sur un chapitre X comptent dans le `n/20` de ce chapitre → injecter le score CALIBRAGE sur un **autre** chapitre que celui qu'on veut à 0
- `assignedByProf` est persisté dans localStorage (`mx_assigned_{code}`) → survit aux refresh. Le hero P4b l'utilise pour afficher "Ton prof te recommande"

### Tokens
⚠️ Toujours estimer avant génération massive → présenter options → attendre validation.

---

## 5. Conventions de code

### Frontend (index.html)
- CSS : variables custom + Tailwind CDN
- JS : vanilla, fonctions globales, pas de classes
- Vues : via `rSection()` injectant du HTML dans `#main`
- Fonts : Syne (titres) + DM Sans (body)
- KaTeX v0.16.9, fallback 1.5s
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

## 6. URLs, identifiants & comptes de test

| Ressource | Valeur |
|---|---|
| GAS URL | `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec` |
| Deployment ID | `AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF` |
| Sheet ID (prod) | `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |
| GitHub | `https://github.com/MatheuxApp/algebra` (privé, org Enterprise trial) |
| Stripe PROD | `https://buy.stripe.com/cNicN7b0ebU9bOE9WTb3q01` |
| GA4 | `G-7R2DW4585Y` |
| Service account | `algebreboost-sheets-2595a71cadfb.json` (ignoré par git) |

| Code | Prénom | Niveau | Email | MDP |
|---|---|---|---|---|
| AUG001 | Auguste | 1ERE | augustecapronm@icloud.com | auguste |
| PR3CMB | Nicolas | 4EME | nico@nico.fr | niconcico |
| 3M4ZAB | Charlie | 3EME | charlieboitel6@gmail.com | charlie |
| HMD493 | Admin | — | (admin) | — |

---

## 7. Vulnérabilités connues

> À sécuriser avant J+7 (vendredi 20 mars).

| # | Risque | Sévérité | Fix |
|---|--------|----------|-----|
| V1 | ~~Webhook Stripe sans HMAC-SHA256~~ | ✅ FIXÉ | `_verifyWebhookHmac()` + fallback metadata.secret. GAS n'expose pas les headers HTTP → HMAC via `_sig/_ts` payload (2026-03-22) |
| V2 | ~~`SHARED_SECRET` hardcodé backend.js~~ | ✅ FIXÉ | `PropertiesService.getScriptProperties()` — configurer dans Apps Script → Paramètres → Propriétés de script (2026-03-22) |
| V3 | ~~Race condition saveScore/ExosDone~~ | ✅ FIXÉ | LockService.tryLock(10000) dans saveScore (2026-03-20) |
| V4 | Race condition ensureUsersCols | 🟡 MOYEN | Lock ou check post-insert |
| V5 | Rate limiting par email (changeable) | 🟡 MOYEN | Acceptable MVP |
| V6 | ~~Scores perdus si réseau instable~~ | ✅ FIXÉ | flushQ retry+backoff, answeredAt client→backend (2026-03-22) |
| V7 | ~~Calibrage pollue tri chapitres + flèches tendance~~ | ✅ FIXÉ | `S.chapTouched` + filtre `r.source !== 'CALIBRAGE'` dans sessions (2026-03-22) |

---

## 8. Documentation vivante

### Structure docs/

```
CLAUDE.md                      → Ce fichier (règles du jeu)
docs/architecture.md           → Technique (frontend + backend + flux)
docs/database.md               → Schéma Sheets (16 onglets + colonnes)
docs/product.md                → Produit (vision + parcours + business)
docs/roadmap.md                → Priorités + calendrier
docs/messages.md               → Voice & tone guide
docs/workflow-quotidien.md     → Workflow quotidien Nicolas (6 onglets admin)
docs/prompt-generation-exos.md → Prompt unique pour générer des exercices (v2.0)
docs/direction-technique.md    → Direction technique : analyse élève → prescription → anti-doublon
```

### Exercices — agent "Monsieur Exos"

Quand Nicolas parle d'exercices (créer, corriger, prescrire), **lancer l'agent** `/agent prescribe`. L'agent lit `docs/prompt-generation-exos.md` + `docs/direction-technique.md`, analyse les Scores, génère le brief, attend validation Nicolas, génère les exos, valide via `validate_exos.py`, et injecte en brouillon (`draft:true`) dans Suivi. Structure obligatoire : 4 slots de 5 exos à difficulté homogène.

### Cohérence UX — agent "UX Engineer"

Après chaque session de code touchant le frontend, **lancer l'agent** `/agent ux-audit`. L'agent vérifie la cohérence entre états techniques et affichage élève : hero cascade, cartes, retro, messages, gamification, override, transitions. Rapport OK/KO avec sévérité.

### Playbooks — diagnostic par domaine

Quand un problème est signalé, **TOUJOURS lire le playbook du domaine concerné** avant d'investiguer :

| Déclencheur | Playbook |
|---|---|
| Inscription, quiz, onboarding, mail J+0, badge trial, overlay J+7 | `docs/playbook-inscription.md` |
| Boost, exercices, XP, streak, daily goal, timer, messages, coach tips | `docs/playbook-boucle.md` |
| Chapitres, progression, slots, complétion, sessions retro | `docs/playbook-chapitres.md` |
| Dashboard admin, workflow publish, emails parents, journal | `docs/playbook-admin.md` |
| Trial, Stripe, premium, paiement | `docs/playbook-paiement.md` |

### Règles obligatoires
1. **Mettre à jour** CLAUDE.md si les règles ou le workflow changent
2. **Mettre à jour** le fichier doc concerné
3. **Supprimer ou fusionner** les informations obsolètes
4. **Ne jamais créer** de doc inutile
5. **Archiver** tout document devenu obsolète

---

## 9. Scripts disponibles

| Script | Description |
|---|---|
| `sheets.py` | Bibliothèque Google Sheets API |
| `rebuild_sheet.py` | Reconstruit Suivi + Historique |
| `test_full_v2.py` | Suite de tests complète (74/74) |
| `test_simulation_40.py` | Stress test 40 élèves × 15 jours |
| `sim_21days.py` | Simulation 21j — 12 profils QA |
| `sim_7days_messages.py` | Simulation messages — 274 API calls, 0 incohérence |
| `audit_exos.py` | Audit qualité exercices |
| `audit_latex.py` | Audit rendu LaTeX/KaTeX sur tous les exercices — couvre Curriculum_Officiel, DiagnosticExos, BrevetExos, BoostExos |
| `validate_exos.py` | Gate qualité bloquant — valide JSON avant injection Sheet. Checks : `$` impairs, LaTeX brut hors `$...$` (BLOQUANT), UNICODE_MIX, a∈options, doublons. Usage : `python3 validate_exos.py exos.json` ou `--sheet TAB NIVEAU CAT` |
| `fix_latex.py` | Fix automatique des formules LaTeX sans `$...$` — couvre Curriculum_Officiel, DiagnosticExos, BrevetExos, BoostExos (`--apply` pour écrire) |
| `verify_hints.py` | Audit qualité des indices |
| `test_coherence_boost.py` | Test régression calibrage/boost |
| `deploy.sh` | Push + deploy GAS en une commande |
| `stress_test.py` | Setup + injection scores simulés pour stress-test Monsieur Exos (3 élèves fictifs) |
| `stress_test_run.py` | Boucle 10 jours complète : injection → prescription → validation → audit. 238/240 OK |

---

## 10. Règle d'or — chaque session

1. Lire ce fichier (CLAUDE.md)
2. Lire `docs/roadmap.md` pour les priorités
3. Patches chirurgicaux uniquement
4. Tester sur mobile avant commit
5. Mettre la doc à jour à chaque modification
