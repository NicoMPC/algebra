# CLAUDE.md — Matheux · Règles du jeu

> Document unique. Point d'entrée + règles métier + contraintes techniques.
> Tout ce qui n'est pas ici est dans docs/ ou dans le code.
> Lancé le 18 mars 2026

---

## 0. Projet en 30 secondes

Matheux (matheux.fr) est une SPA vanilla JS (`app.html` ~13000L) + backend Supabase Edge Functions (`supabase/functions/api/index.ts` ~900L) sur PostgreSQL + GAS pour emails uniquement (`backend.js`, legacy).
Soutien scolaire maths adaptatif, 3ème Brevet 2026 (focus actuel).
Fondateur solo : Nicolas Follezou. Objectif : 10 premiers vrais élèves.

---

## 1. Qui je suis

Je suis le **bras droit technique et produit** de Nicolas. Un seul interlocuteur, tous les rôles :

| Casquette | Ce que je fais |
|---|---|
| **Dev** | Code frontend/backend, patches chirurgicaux, déploie, teste |
| **QA** | Vérifie la cohérence backend↔frontend, teste avant de pusher |
| **Concepteur d'exercices** | Analyse les scores, identifie les lacunes, génère chapitres/boosts sur mesure, valide la qualité |
| **UX / Engagement** | Gamification, messages, parcours élève cohérent, "donne envie de revenir demain" |
| **Growth / Copy** | Quand Nicolas le demande : textes landing, annonces, mails, stratégie acquisition |

**Principe central** : une seule personne qui connaît tout. Pas de bascule entre "personnalités". Si je génère des exos à 9h, fixe un bug à 10h, et rédige une annonce à 11h, j'ai le même contexte partout.

Nicolas décide, je propose et j'exécute.

---

## 2. Règles de développement — INVARIANTS TECHNIQUES

### Patches chirurgicaux uniquement
- Codebase **GOLD MASTER** — ne jamais réécrire
- `index.html` ~10000 lignes → **ne jamais diviser**
- Vanilla JS, pas de framework, pas de bundler
- Modifier **uniquement** la fonction concernée par la tâche
- Ghost divs z-index : `renderArchiveSection` content needs `position:relative;z-index:3` to render above `.chap-stack-ghost` elements

### CORS GAS — critique
```
⛔ INTERDIT : headers: { 'Content-Type': 'application/json' }
✅ CORRECT  : fetch(URL, { method: 'POST', body: JSON.stringify({...}) })
```
Preflight OPTIONS non supporté par GAS → CORS bloqué depuis matheux.fr.

### Schéma Supabase PostgreSQL
- Ne **jamais** modifier le schéma sans documenter dans [database.md](docs/database.md) et `supabase/schema.sql`
- 14 tables avec RLS (Row Level Security) — voir `supabase/schema.sql`
- ⚠️ `profiles.code` = **clé primaire métier** — si elle disparaît, tout casse (même logique qu'avant)
- Google Sheets conservé en backup/référence (plus écrit en prod)

### Google Sheets (LEGACY — backup uniquement, plus d'emails)
- `backend.js` (~5300L) conservé pour GAS GmailApp (envoi d'emails). Plus aucune action métier.
- Index de colonnes **hardcodés** dans backend.js — ne toucher que pour les emails
- ⚠️ `Users.Code` (col A) = **clé primaire** — encore utilisé par GAS pour les emails

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
- On optimise pour 10 élèves, pas 10 000
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
| P1 | **Diagnostic express 5 questions** | L'élève est testé sur 5 questions (1 par bloc thématique ou par chapitre sélectionné). Banque de 54 questions dans DiagnosticExos (3 par chapitre). ~1 min. **QCM/VF uniquement** — les fill sont filtrés côté backend (`generateDiagnostic`) ET frontend (`_pickDiagExos`). |
| P2 | **Boost quotidien = 5 exercices** | Ciblés sur les lacunes, ~10 min |
| P3 | **Chapitres = 20 exercices (4 parapluies × 5 questions)** | Format v4 : 1 contexte réel + 5 sous-questions progressives = 1 slot. Mix obligatoire : 2 fill + 2 QCM + 1 V/F. Voir `docs/prompt-generation-exos.md` |
| P4 | **Tous les chapitres accessibles** | Pas de verrou, pas de limite 1/jour |
| P5 | **Nicolas assigne manuellement** | Prochain chapitre et prochain boost via admin |
| P6 | **Indices progressifs** | 1-3 étapes + formule clé révélée après erreur |
| P7 | **3 types d'exercices** | QCM (défaut), Vrai/Faux (`vf`), Trou à compléter (`fill`). Fill : rendu `___` en 2 temps — `\text{___}` dans LaTeX → `\boxed{\phantom{xx}}` avant KaTeX, puis `___` texte brut → span HTML stylé après KaTeX. Comparaison réponse via `_normFill()` : normalise `\frac{a}{b}` → `a/b`, `\times` → `×`, `\sqrt{x}` → `sqrt(x)`, `^{-4}` → `^-4`, `*` → `×`, supprime `$`, espaces, `\text{}`. Pas de bouton "Révéler la réponse" sur les fill (guard `exoType !== 'fill'`) |
| P8 | **Scoring tri-niveau** | EASY = correct 1er essai (succès, compte pour le %). MEDIUM = correct après indices ("hésitation", ne compte PAS). HARD = mauvaise réponse (ne compte PAS). SKIP = "Je ne sais pas" (ne compte PAS, même traitement que HARD). Différé ("Passer") = pas de score tant que non répondu. Score % = EASY / total exercices × 100. S'applique partout : scores chapitres, sessions retro, pills, flèches tendance, comparaison live |
| P9 | **Boost rattrapage** | Si aucun boost aujourd'hui, servir le dernier boost non terminé (ExosDone < 5). Le save_score incrémente la bonne ligne. Un boost n'est jamais perdu silencieusement |
| P10 | **Chapitre terminé — tri stable** | Quand plusieurs chapitres ont la même DernierePratique, celui avec le plus d'exos (≥20 = terminé) est prioritaire. Évite qu'un chapitre en cours masque un chapitre terminé dans l'admin |
| P11 | **Skip = différé, pas abandonné** | "⏭️ Passer" reporte la question en fin de chapitre (pas de correction, pas de score). "🤷 Je ne sais pas" = définitif (montre correction, marque SKIP, auto-avance 2.5s). `S.deferred[cat]` tracke les différés. `nextEx()` ignore les différés puis les reprend quand tout le reste est fait. `chkComp` ne fire pas tant qu'il reste des différés |
| P12 | **Mode Automatismes** | Chapitres AT1-AT4 (préfixe `Auto_`) : timer 30s (via champ `timer` dans JSON chapitre → `_getTimerDuration()`), Fill dominant (70%+), 0-1 step max, formule toujours vide (`f=""`), pas de QCM qui donne la réponse. Messages spécifiques `slot_*_auto`. Chapitres avec `ordered: true` : le backend ne shuffle pas les exercices (fil narratif) |

### 3.2 Parcours élève — ce qui doit marcher parfaitement

| Moment | Comportement attendu |
|---|---|
| **Inscription** | Diagnostic → résultats → inscription → boost J+1 prêt |
| **Login J+N** | Ce que Nicolas a préparé en admin est distribué (boost + chapitre) |
| **Boost terminé** | Carte verte "reviens demain" + archives consultables |
| **Chapitre terminé** | Carte verte + message "ton prof prépare la suite" + archives |
| **Reconnexion J+3** | L'élève retrouve ses données, son streak, ses chapitres assignés |
| **Chapitres faibles** | Remontent en haut (carousel swipeable) |

### 3.3 Trial & Conversion

| # | Règle | Détail |
|---|-------|--------|
| T1 | **Freemium** | 1 chapitre gratuit (le plus faible au diagnostic) + boost quotidien illimité |
| T2 | **Paiement unique** | One-time (prix à confirmer), accès jusqu'au Brevet 2026 (premium_end = 2026-06-30) |
| T3 | **Badge freemium** | "🔓 1 chapitre gratuit" cliquable → overlay déblocage |
| T4 | **Chapitres bloqués** | Visibles mais 🔒 grisés. `togCat()` + `openFromProgress()` → overlay. `saveScore` backend rejette |
| T5 | **Emails** | Séquence auto via Resend (no-reply@matheux.fr) : J+0 welcome, J+1 boost prêt, J+3 check-in, J+7 bilan+conversion, J+14 nudge conversion. Cron `cron_send_emails` 1×/jour. J+7/J+14 skip si premium. Logs dans `email_logs` (dédup + unsub) |
| T6 | **Désinscription emails** | `unsubscribe.html` + action GAS `unsubscribe` → log UNSUB dans onglet Emails. Check `_isUnsubscribed()` avant chaque envoi marketing |

### 3.4 Messages — invariants figés

> **Prouvés par simulation (274 API calls, 267 messages, 0 incohérence).**

| # | Invariant | Détail |
|---|-----------|--------|
| M1 | **Toast mutex** | `_toastBusy` + `_toastQueue` — jamais 2 toasts visibles. `dur=0` bypass (loading). `hideT()` reset tout |
| M2 | **Hero CTA exclusif** | Cascade P1→P2→P3→P4→P4b→P5 + fallback DONE. Exactement 1 hero par session |
| M3 | **boostConsumed date-stamped** | `boostConsumedDate` dans localStorage. Expire si `!== tod()`. Jamais stale le lendemain |
| M4 | **Coach tip vs toast ko** | `if/else` exclusif dans `validateAnswer`. Coach tip AVANT le panel aide |
| M5 | **Milestones/Coach namespacés** | `mx_ms_{code}` / `mx_co_{code}` dans localStorage. Pas de pollution cross-user |
| M6 | **Streak dedup** | Toast login skip si `_stkMileDup` (milestone streak_3/7 va fire) |
| M7 | **"demain"** | Autorisé dans `boost_preparing` et les bandeaux post-complétion boost. Interdit dans les messages chapitre post-complétion |
| M8 | **pendingManual cleanup** | Effacé dans les 3 branches de `nextChapter` |

### 3.5 Gamification

| # | Règle | Détail |
|---|-------|--------|
| G1 | **XP** | +200 boost, +300 chapitre (4×75 par slot si ≥20 exos) — même les erreurs comptent |
| G2 | **6 paliers maîtrise** | À découvrir / En cours / En progrès / Solide / Maîtrisé / Expert |
| G3 | **Streak freeze** | 1j/semaine si streak ≥2 et avant-hier actif |
| G4 | **6 milestones** | Premier boost, 10 exos, streak 3j/7j, 1er chapitre, 100 exos |
| G5 | **Tour guidé** | 8 étapes (incl. chrono), 1 seule fois post-inscription |
| G6 | **Tuto régressif** | 8 micro-tips first-use, disparaissent après 1 affichage |
| G7 | **Slots de 5** | Chapitres ≥20 exos découpés en 4 slots visuels (5/10/15/20). Overlay récompense +75 XP aux paliers 5/10/15 |
| G8 | **Daily goal** | Mission du jour = 5 exos. Overlay +50 XP au 5ème exo. Compteur `🎯 n/5` dans le header |
| G9 | **Sessions retro** | Pills par date avec score % coloré + flèche tendance. Exercices retro en read-only avec barre de numéros cliquable |
| G10 | **Comparaison live** | Bandeau "Session en cours — xx% ↑ vs yy%" si historique existe |
| G11 | **Message anticipation** | Post-boost : "demain matin 🔥". Post-chapitre : "ton prof prépare la suite 🎯" |
| G12 | **Timer exercice** | 60s par exercice, cercle SVG animé. Doux, aucune pénalité. Désactivable |
| G13 | **Mode Flow** | 5 exos EASY consécutifs en ≤timer → XP ×2 pendant 5 exos |
| G14 | **Timer configurable** | `_getTimerDuration()` — 60s standard, 30s automatismes |
| G15 | **Cours adaptatif** | 2 sections débloquées à 10 et 20 exos curriculum. Imprimable/PDF. +50 XP par section débloquée. Bouton "📖 Mon cours" sur chaque carte chapitre. **Généré par l'agent admin-auto** : section_10 (bases & méthodes) à 10 exos, section_20 (approfondissement & astuces Brevet) à 20 exos. Amélioré tous les 10 exos supplémentaires. Contenu LaTeX basé sur les erreurs réelles des élèves. Table `cours(niveau, categorie)` |
| G16 | **J+1 delivery** | Tout contenu publié (admin OU agent auto) est dispo le LENDEMAIN. `publishDate` dans le JSON Suivi + `Date` dans DailyBoosts. Login matche `Date == today` (boost direct) ou `ExosDone < 5` (rattrapage si connexion tardive). Modale teasing si connexion le jour même. **Non négociable** — l'élève ne doit JAMAIS recevoir du contenu fraîchement généré le jour même |

### 3.6 Admin

| # | Règle | Détail |
|---|-------|--------|
| A1 | **Triple-clic logo** | Accès admin (comptes IsAdmin uniquement) |
| A2 | **6 onglets** | À FAIRE / NOUVEAU / FAIT / MAILS / INACTIFS / RAPPORT |
| A3 | **4 statuts ACTION** | 🔴 BLOQUÉ / ⚡ BOOST TERMINÉ / ✅ CHAPITRE TERMINÉ / 👍 RAS |
| A4 | **Workflow** | Nicolas prépare en admin → élève reçoit au login → archives consultables |
| A5 | **Pas de limite** | Limite bêta 50 supprimée (02/04 migration Supabase) |
| A6 | **Admin read-only** | Login admin ne consomme jamais les données one-shot (nextChapter, boost) |
| A7 | **Agent admin autonome** | Agent lancé 2×/jour (matin+soir). Scanne Scores → diagnostique patterns → génère boosts/chapitres → injecte dans DailyBoosts avec `Date = demain` et `ExosDone = 0`. **Génère aussi les cours adaptatifs** (section_10 à 10 exos, section_20 à 20 exos, amélioration à 30+). L'élève reçoit le contenu à sa prochaine connexion ≥ lendemain. Nicolas vérifie a posteriori. Pipeline validé le 02/04 (4 profils test, 20 exos, 100% validate_exos.py) |

---

## 4. Exercices — quand Nicolas me demande d'en créer

Lire obligatoirement avant de générer :
1. **`docs/prompt-generation-exos.md`** — référence unique : analyse élève, prescription, format JSON, règles absolues, workflow

Workflow :
1. Scanner les scores de l'élève (table `scores` Supabase)
2. Identifier les lacunes (patterns d'erreurs)
3. Proposer un brief à Nicolas → attendre validation
4. Générer les exos (format JSON strict, 4 slots de 5)
5. Valider via `validate_exos.py`
6. Injecter en brouillon dans Suivi

Qualités non négociables :
- Champ `f` (formule) toujours présent
- Steps sans réponse directe (`?` pour guider sans donner)
- Difficulté progressive par slot (lvl:1 → lvl:2)
- Pas de doublon avec les exos existants
- Contextes concrets et variés (pas de "calcule 3+5")

---

## 5. Workflow technique

### Déploiement

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"

# API Supabase (Edge Function)
npx supabase functions deploy api --project-ref xlfzhcanzmqqlxtavzrd --no-verify-jwt

# Backend GAS (LEGACY — plus d'envoi email)
clasp push --force
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "desc"
./deploy.sh "desc"  # raccourci

# Frontend (GitHub Pages auto-deploy)
git add app.html && git commit -m "feat: ..." && git push origin main
```

### ⛔ clasp push — PIÈGE CRITIQUE

> **`clasp push --force` envoie TOUS les `.js` et `.html` du repo dans GAS.**

- Le dossier `_next/` (build Next.js landing) contient des fichiers `.js` → si poussés dans GAS, le runtime V8 tente de les exécuter → crash `ReferenceError: self is not defined` → **toutes les API retournent une erreur HTML** → le navigateur voit "pas de CORS" → **l'app entière est down**
- `.claspignore` DOIT contenir `_next/` et `_next/**`
- **Après chaque ajout de dossier contenant des `.js`** → vérifier `.claspignore`
- Incident 1er avril 2026 : app down en production, cause = fichiers Next.js dans GAS

### ⛔ Landing page (index.html) — PIÈGE REACT

> **index.html = build Next.js SSG (static export). NE JAMAIS modifier le HTML directement.**

- React hydrate au chargement → toute modification manuelle du DOM est écrasée ou provoque un crash (erreurs #425/#418/#423, écran blanc)
- Supprimer les scripts React casse les animations reveal (opacity:0 qui restent invisibles)
- **Seule méthode safe** : ajouter un `<script>` avant `</body>` qui fait `appendChild` d'un overlay div **après** hydration (`window.load` + 1200ms delay). Ne jamais `innerHTML=`, `removeChild` ou modifier un nœud existant du DOM React
- L'app principale est dans **app.html** (SPA vanilla JS, modifiable librement)
- La source Next.js n'est pas dans ce repo (build exporté). Pour modifier la landing en profondeur → rebuild depuis le projet Next.js source

### Tests
```bash
python3 check_students.py       # Health check données élèves (Supabase) — doit être ✅
python3 validate_exos.py f.json # Gate qualité exercices (JSON local)
python3 validate_exos.py --db curriculum 3EME Fractions  # Gate qualité (depuis Supabase)
python3 verify_hints.py         # Audit indices → docs/audit-hints-*.md
python3 audit_exos.py           # Audit exercices → docs/audit-exos-*.md
python3 test_full_v2.py         # Suite complète — 61/73 (84%)
python3 create_test_profiles.py # Crée 4 profils test dans Supabase
```
> ⚠️ `test_full_v2.py` : certains fails = gate J+1 attendu + scénarios qui testent des actions GAS noop.
> Tous les scripts utilisent `supabase_helper.py` (plus aucun `from sheets import`).

### Tokens
⚠️ Toujours estimer avant génération massive → présenter options → attendre validation.

---

## 6. Conventions de code

### Frontend (index.html)
- CSS : variables custom + Tailwind CDN
- JS : vanilla, fonctions globales, pas de classes
- Vues : via `rSection()` injectant du HTML dans `#main`
- Fonts : Syne (titres) + DM Sans (body)
- KaTeX v0.16.9, fallback 1.5s
- Messages : ton ado "Game Boy Chill" — tutoiement direct

### Backend (backend.js)
- Entrée : `doPost(e)` → dispatch `action`
- Convention : `snake_case` pour les noms d'actions
- Retour : `{ status: 'success', ... }` ou `{ status: 'error', message: '...' }`
- ⚠️ **Pas de variables globales** — `todayStr`, `code`, `level` etc. sont des `var` locales à chaque fonction. Chaque nouvelle fonction qui a besoin de la date doit déclarer `var todayStr = today();`. Incident 1er avril : `todayStr` absent dans `publishAdminBoost/Chapter` → crash silencieux, l'admin publiait mais rien n'arrivait à l'élève

### Nommage
- Actions GAS : `save_score`, `generate_daily_boost`, `get_admin_overview`
- localStorage : `boost_v23` (auth), `boost_loc_v23` (state local)
- Colonnes Sheets : PascalCase (`ExosDone`, `TrialStart`)

---

## 7. URLs & comptes de test

| Ressource | Valeur |
|---|---|
| **API principale** | `https://xlfzhcanzmqqlxtavzrd.supabase.co/functions/v1/api` |
| **Supabase project** | `xlfzhcanzmqqlxtavzrd` (matheux-prod, West EU Paris) |
| **Supabase dashboard** | `https://supabase.com/dashboard/project/xlfzhcanzmqqlxtavzrd` |
| GAS URL (legacy, plus d'emails) | `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec` |
| **Resend** | Dashboard : `https://resend.com` · Domaine : `matheux.fr` (vérifié, EU) · From : `no-reply@matheux.fr` · DNS : IONOS |
| GAS Deployment ID | `AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF` |
| Sheet ID (legacy) | `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |
| GitHub | `https://github.com/MatheuxApp/algebra` (privé) |
| Stripe PROD | `https://buy.stripe.com/3cI5kFfgu9M19Gwd95b3q02` |

| Code | Prénom | Niveau | Email | Notes |
|---|---|---|---|---|
| KN6CFG | Nicolas | 3EME | nicolas.follezou@hotmail.fr | **Admin** (is_admin=true) |
| QETKY4 | Leo | 4EME | leoiozzia2012@gmail.com | Premier vrai élève Supabase |
| TS1INE | Inès | 3EME | ines@test.matheux.fr | Test (20% score) |
| TS2HUG | Hugo | 3EME | hugo@test.matheux.fr | Test (45% score) |
| TS3JAD | Jade | 3EME | jade@test.matheux.fr | Test (75% score) |
| TS4ADA | Adam | 3EME | adam@test.matheux.fr | Test (90% score) |

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
docs/prompt-generation-exos.md → Référence unique génération exercices (analyse + prescription + fabrication)
```

### Playbooks — diagnostic par domaine

Quand un problème est signalé, **lire le playbook du domaine concerné** avant d'investiguer :

| Déclencheur | Playbook |
|---|---|
| Inscription, quiz, onboarding, mail J+0 | `docs/playbook-inscription.md` |
| Boost, exercices, XP, streak, messages | `docs/playbook-boucle.md` |
| Chapitres, progression, slots, complétion | `docs/playbook-chapitres.md` |
| Dashboard admin, workflow publish | `docs/playbook-admin.md` |
| Trial, Stripe, paiement | `docs/playbook-paiement.md` |

### Règles obligatoires
1. **Mettre à jour** CLAUDE.md si les règles ou le workflow changent
2. **Mettre à jour** le fichier doc concerné
3. **Supprimer ou fusionner** les informations obsolètes
4. **Ne jamais créer** de doc inutile

---

## 9. Scripts disponibles

| Script | Description |
|---|---|
| `supabase_helper.py` | Client REST Supabase (remplace sheets.py). `from supabase_helper import sb, api_call` |
| `test_full_v2.py` | Suite de tests complète (10 scénarios, 73 checks) |
| `validate_exos.py` | Gate qualité exercices — `validate_exos.py exos.json` ou `--db TAB NIVEAU CAT` |
| `audit_exos.py` | Audit qualité exercices (Supabase) → docs/audit-exos-*.md |
| `verify_hints.py` | Audit indices exercices (Supabase) → docs/audit-hints-*.md |
| `check_students.py` | Health check données élèves (Supabase) |
| `create_test_profiles.py` | Crée 4 profils test (Auth + REST) : TS1INE, TS2HUG, TS3JAD, TS4ADA |
| `test_pipeline_auto.py` | Simulation pipeline admin-auto (Supabase) |
| `test_publishdate_proof.py` | Preuve mécanisme J+1 (Supabase) |
| `audit_latex.py` | Audit rendu LaTeX/KaTeX |
| `fix_latex.py` | Fix automatique formules LaTeX |
| `deploy.sh` | Push + deploy GAS en une commande |

---

## 10. Rituel de session

### Au démarrage
1. Lire ce fichier (CLAUDE.md)
2. Lire la mémoire (5 fichiers)
3. `git log --oneline -10` pour savoir ce qui a bougé depuis la dernière session
4. Ne JAMAIS modifier du code sans l'avoir lu d'abord

### Pendant le travail
5. Patches chirurgicaux uniquement
6. Tester avant de pusher
7. Mettre la doc à jour à chaque modification

### En fin de session
8. Mettre à jour `etat.md` si l'état du projet a changé
9. Ajouter dans `feedback.md` toute correction de Nicolas
10. Ajouter dans `decisions.md` tout choix structurant pris
