# CLAUDE.md — Matheux · Règles du jeu

> Document unique. Point d'entrée + règles métier + contraintes techniques.
> Tout ce qui n'est pas ici est dans docs/ ou dans le code.
> GAS @97 · Lancé le 18 mars 2026

---

## 0. Projet en 30 secondes

Matheux (matheux.fr) est une SPA vanilla JS (`index.html` ~9900L) + backend Google Apps Script (`backend.js` ~5300L) sur Google Sheets.
Soutien scolaire maths adaptatif, 6ème→3ème + 1ère Spé Maths.
Fondateur solo : Nicolas Follezou. Objectif : 50 clients à 19,99€/mois.

---

## 1. Rôle de l'IA

Tu es le **directeur technique et chef de projet IA** du projet Matheux.
Nicolas (fondateur) est le visionnaire produit. Ton rôle :

1. **Comprendre** les demandes produit de Nicolas
2. **Traduire** en actions techniques concrètes
3. **Implémenter** dans la codebase existante (patches chirurgicaux)
4. **Maintenir** la documentation vivante
5. **Alerter** si une action risque de casser l'architecture ou la BDD

---

## 2. Règles de développement — INVARIANTS TECHNIQUES

### Patches chirurgicaux uniquement
- Codebase **GOLD MASTER** — ne jamais réécrire
- `index.html` ~9900 lignes → **ne jamais diviser**
- Vanilla JS, pas de framework, pas de bundler
- Modifier **uniquement** la fonction concernée par la tâche

### CORS GAS — critique
```
⛔ INTERDIT : headers: { 'Content-Type': 'application/json' }
✅ CORRECT  : fetch(URL, { method: 'POST', body: JSON.stringify({...}) })
```
Preflight OPTIONS non supporté par GAS → CORS bloqué depuis matheux.fr.

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
| P7 | **3 types d'exercices** | QCM (défaut), Vrai/Faux (`vf`), Trou à compléter (`fill`) |

### 3.2 Trial & Conversion

| # | Règle | Détail |
|---|-------|--------|
| T1 | **7 jours gratuits** | Accès complet, sans carte bancaire |
| T2 | **19,99 €/mois** | Prix unique, pas de paliers |
| T3 | **Badge trial progressif** | J-5 bleu → J-3 jaune → J-1 orange |
| T4 | **J+7 overlay bloquant** | Lien Stripe direct |
| T5 | **Emails séquencés** | J+0 auto, J+3/J+5/J+7 manuels (trigger à activer dès 10 clients) |

### 3.3 Messages — invariants figés @95

> **Prouvés par simulation (274 API calls, 267 messages, 0 incohérence).**
> **Ne JAMAIS modifier sans relancer `python3 sim_7days_messages.py` après.**

| # | Invariant | Détail |
|---|-----------|--------|
| M1 | **Toast mutex** | `_toastBusy` + `_toastQueue` — jamais 2 toasts visibles. `dur=0` bypass (loading). `hideT()` reset tout |
| M2 | **Hero CTA exclusif** | Cascade P1→P5 + fallback DONE. Exactement 1 hero par session. Chaque niveau a `if (!_hero)` + `break` |
| M3 | **boostConsumed date-stamped** | `boostConsumedDate` dans localStorage. Expire si `!== tod()`. Jamais stale le lendemain |
| M4 | **Coach tip vs toast ko** | `if/else` exclusif dans `validateAnswer`. Coach tip AVANT le panel aide |
| M5 | **Milestones/Coach namespacés** | `mx_ms_{code}` / `mx_co_{code}` dans localStorage. Pas de pollution cross-user |
| M6 | **Streak dedup** | Toast login skip si `_stkMileDup` (milestone streak_3/7 va fire) |
| M7 | **"demain"** | Uniquement dans `boost_preparing`. Partout ailleurs → "bientôt" ou "continue tes chapitres" |
| M8 | **pendingManual cleanup** | Effacé dans les 3 branches de `nextChapter` (PENDING_MANUAL / JSON / string) |

### 3.4 Gamification

| # | Règle | Détail |
|---|-------|--------|
| G1 | **XP** | +200 boost, +300 chapitre — même les erreurs comptent |
| G2 | **6 paliers maîtrise** | À découvrir / En cours / En progrès / Solide / Maîtrisé / Expert |
| G3 | **Streak freeze** | 1j/semaine si streak ≥2 et avant-hier actif |
| G4 | **6 milestones** | Premier boost, 10 exos, streak 3j/7j, 1er chapitre, 100 exos |
| G5 | **Tour guidé** | 7 étapes, 1 seule fois post-inscription, guard `_needsCoach('TOUR')` / `_markCoach('TOUR')` |
| G6 | **Tuto régressif** | 8 micro-tips first-use (T1-T8), `_needsCoach/_markCoach`, disparaissent après 1 affichage |

### 3.5 Admin

| # | Règle | Détail |
|---|-------|--------|
| A1 | **Triple-clic logo** | Accès admin (comptes IsAdmin uniquement) |
| A2 | **6 onglets** | À FAIRE / NOUVEAU / FAIT / MAILS / INACTIFS / RAPPORT |
| A3 | **4 statuts ACTION** | 🔴 BLOQUÉ (inactif >7j + <40%) / ⚡ BOOST TERMINÉ / ✅ CHAPITRE TERMINÉ / 👍 RAS |
| A4 | **Workflow boost/chapitre** | Copier résultats → Claude → JSON → publier |
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
| V1 | Webhook Stripe sans HMAC-SHA256 | 🔴 CRITIQUE | Implémenter `stripe-signature` header |
| V2 | `SHARED_SECRET` hardcodé backend.js | 🔴 CRITIQUE | → `PropertiesService` |
| V3 | Race condition saveScore/ExosDone | 🟡 MOYEN | LockService |
| V4 | Race condition ensureUsersCols | 🟡 MOYEN | Lock ou check post-insert |
| V5 | Rate limiting par email (changeable) | 🟡 MOYEN | Acceptable MVP |

---

## 8. Documentation vivante

### Structure docs/

```
CLAUDE.md                    → Ce fichier (règles du jeu)
docs/architecture.md         → Technique (frontend + backend + flux)
docs/database.md             → Schéma Sheets (16 onglets + colonnes)
docs/product.md              → Produit (vision + parcours + business)
docs/roadmap.md              → Priorités + calendrier
docs/messages.md             → Voice & tone guide
docs/workflow-quotidien.md   → Workflow quotidien Nicolas (6 onglets admin)
docs/archive/                → Docs historiques + audits + rapports
```

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
| `verify_hints.py` | Audit qualité des indices |
| `test_coherence_boost.py` | Test régression calibrage/boost |
| `deploy.sh` | Push + deploy GAS en une commande |

---

## 10. Règle d'or — chaque session

1. Lire ce fichier (CLAUDE.md)
2. Lire `docs/roadmap.md` pour les priorités
3. Patches chirurgicaux uniquement
4. Tester sur mobile avant commit
5. Mettre la doc à jour à chaque modification
