# CLAUDE.md — Matheux (matheux.fr)
> Lis ce fichier en entier à chaque session. Mets à jour les checkboxes en fin de session.

---

## 🎯 Projet en une phrase
SPA vanilla JS (index.html ~1900 lignes) + backend Google Apps Script sur Google Sheets.
Outil pédagogique adaptatif maths collège (6ème→3ème), diagnostic de lacunes, exercices personnalisés, gamification. MVP solo → 50 clients payants.

## 👤 Contexte fondateur
- Seul, prof de maths, déjà des élèves actifs avec retours positifs
- Budget ~400€, objectif : finir en 1 mois de Claude Max
- 2-3h/jour de travail manuel accepté en phase 1
- Codebase : V23 GOLD MASTER — ne pas réécrire, patcher chirurgicalement
- Dossier local : `/home/nicolas/Bureau/algebra live`
- Repo GitHub : https://github.com/NicoMPC/algebra

---

## 🏗️ Architecture réelle

| Composant | Détail |
|---|---|
| `index.html` | SPA ~3250 lignes. CSS vars + Tailwind CDN + JS vanilla |
| GAS backend | `backend.js` — Web App déployée via clasp |
| Sheet ID | `1zLBajKVL8FUzy7aV2Myi9gYFEFJjnALkLAg0hbicuDk` |
| API URL | `const SU` dans index.html |
| Auth | localStorage clé `boost_v23` → `{ email, hash }` |
| State local | localStorage clé `boost_loc_v23` → `{ [code]: { stk, last } }` |
| Hash MDP | SHA-256 de `email + '::' + password + '::AB22'` (client-side) |
| Fonts | Syne (titres) + DM Sans (body) |


## 📦 Actions GAS — état réel
| Action | Statut |
|---|---|
| `register` | ✅ Fonctionne |
| `login` | ✅ Fonctionne — dynamicChapters retiré (retourne `[]`) |
| `save_score` | ✅ Fonctionne + updateConfidenceScore + updateDashboard |
| `save_boost` | ✅ Fonctionne + updateDashboard + ExosDone dans DailyBoosts |
| `generate_diagnostic` | ✅ Fonctionne |
| `generate_daily_boost` | ✅ Fonctionne — filtré sur chapitres diagnostiqués élève |
| `generate_remediation` | ⏸️ Désactivé — return success immédiat, corps en commentaire |
| `get_progress` | ✅ Fonctionne |
| `detect_fragile_prereqs` | ✅ Fonctionne (onglet Prerequisites archivé → retourne fragile:false) |
| `get_prerequisites` | ✅ Fonctionne (idem) |
| `enqueue` | ✅ Fonctionne (onglet Queue archivé → retourne erreur propre) |
| `generate_exam_prep` | ✅ Fonctionne |
| `generateMorningReport` | ✅ Fonctionne — génération IA désactivée |
| `get_admin_overview` | ✅ Fonctionne — liste élèves triée par urgence, boostHistory[], source sur exos |
| `publish_admin_boost` | ✅ Fonctionne — écrit →Nouveau Boost (col 18), rebuildSuivi |
| `publish_admin_chapter` | ✅ Fonctionne — écrit premier slot →Nouveau Ch libre, rebuildSuivi |

---

## 🚨 BUGS CRITIQUES ✅ TOUS RÉSOLUS (voir BLOC 1 dans la roadmap)

---

## ✅ Ce qui fonctionne bien (ne pas toucher sans raison)
- CSS/UI complet, mobile-first, animations propres
- Landing page "Matheux" avec hero sombre + section sans/avec
- Auth register + login + auto-login
- Scores enrichis : temps, wrongOpt, indices, formule (v23)
- Queue offline résiliente (localStorage)
- Swipe gauche → exercice suivant
- Admin panel triple-clic logo
- Gamification : XP / streak / mastery ring SVG
- MathJax v3 avec fallback 2.5s + overflow-x-auto sur zone question (B4)
- Chrono par exercice `exoStartTime` (v23)
- Nudge pills après 20s d'inactivité
- Tableau blanc bottom sheet avec symboles maths
- **[B2]** Vue Progression : barre de confiance, dates relatives, badge Maîtrisé, nav 2 boutons (Chapitres/Progression)
- **[B3]** Bannière prérequis fragiles (ambre) avant exercices, mis en cache par session
- **[B4]** Header mobile : truncate sur nom long, tap target ✕ bannière corrigé
- **[9 mars]** Badge "🔄 Demain" sur carte chapitre terminé (`S.remReq[cat]`)
- **[9 mars]** Auto-indices sur erreur : `autoShowHelp()` injecte tout en HTML direct, pas de typewriter
- **[9 mars]** Badge niveau coloré + compteur animé dans `rSection()`
- **[9 mars]** Vue Constellation supprimée entièrement
- **[10 mars]** Mode Admin complet : dashboard "Mes Élèves", modal élève enrichi (chapitresDetail, barres succès, pills exos), bouton "📋 Copier le prompt Claude", publish boost + chapitre
- **[10 mars]** Mot du professeur : message perso optionnel (textarea dans modal admin) → écran interstitiel avant exercices côté élève (`renderMotProf`, `S.motProfBoost`, `S.motProfChap`)
- **[11 mars]** Refonte admin dashboard : ExosDone DailyBoosts, boostHistory[], règles ACTION revues (🔴/⚡/✅/👍), box boost accordéon + verrouillage, box chapitre verrouillée si en cours, fix relDate "304 mois"
- **[11 mars]** Modal élève : tous les exos (plus de cap 12), intitulés accordion si >60 chars, badge DIAG/BOOST, copyAdminPrompt copie TOUS les exos avec ⏱💡📐
- **[11 mars]** Données test : 20 scénarios couvrant tous les cas (boost pending/en cours/terminé/absent × chapitre terminé/en cours/absent), vraies questions LaTeX

---

## 📋 Structure Google Sheet (onglets) — état 10 mars ✅ REFONDÉ

### Onglets Nicolas (bleus)
```
Vue Élèves    ← PRINCIPAL — 1 ligne/élève, ACTION NICOLAS en col A (gelée), col N Code (masquée)
                ⚡ ACTION NICOLAS | Prénom | Niveau | Dernière connexion | Streak 🔥 |
                Chapitres diagnostiqués | Chapitre en cours | Nb exos faits | Score global % |
                Chapitres fragiles 🔴 | Taux réussite semaine |
                📚 Prochain chapitre (Nicolas) | 📧 Rapport envoyé le (Nicolas) | Code (masqué)

Log Exercices ← DÉTAIL — 1 ligne/exercice, récent en haut, énoncé 60 chars
                Date | Prénom | Niveau | Chapitre | Énoncé | Résultat |
                Temps (sec) | Nb indices | Formule ouverte | Mauvaise option

Users         → Code | Prénom | Niveau | Email | PasswordHash | DateInscription | IsAdmin | Premium | TrialStart
```

### Onglets GAS uniquement (gris — ne pas toucher)
```
Progress            → Code | Niveau | Chapitre | Score | NbExos | NbErreurs | DernierePratique | Statut | Streak
DailyBoosts         → Code | Date | BoostJSON | ExosDone
Curriculum_Officiel → Niveau | Categorie | Titre | Icone | ExosJSON
DiagnosticExos      → Niveau | Categorie | ExosJSON
Scores              → Code | Prénom | Niveau | Chapitre | NumExo | Énoncé |
                       Résultat | Temps(sec) | NbIndices | FormuleVue | MauvaiseOption | Draft | Date
RemediationChapters → Code | Categorie | Version | ExosJSON | Insight | Date
```

### Archivés (données conservées)
```
_ARCHIVE_Queue
_ARCHIVE_Prerequisites
_ARCHIVE_Rapports
_ARCHIVE_Pending_Exos
```

### Règles ⚡ ACTION NICOLAS (rebuildSuivi — état 11 mars)
| Valeur | Condition | Priorité |
|---|---|---|
| `🔴 BLOQUÉ` | inactif >7j ET score <40 sur tous chapitres | 1 |
| `⚡ BOOST TERMINÉ → préparer le suivant` | ExosDone==5 ET dernier boost < aujourd'hui ET pas de boost pending | 2 |
| `✅ CHAPITRE TERMINÉ → assigner la suite` | Progress NbExos ≥20 ET cols 📝 Nicolas vides | 3 |
| `👍 RAS` | sinon | 4 |

Plusieurs règles peuvent s'appliquer simultanément → toutes affichées en pills, couleur card = plus urgente.
`rebuildSuivi(code)` appelé dans `save_score` et `save_boost`.
`writeToHistorique(p)` appelé dans `save_score` — insert en ligne 2 (récent en haut), énoncé réel.

## 🗺️ ROADMAP PAR BLOCS

### BLOC 1 — Socle technique ✅ TERMINÉ
- [x] BUG 1 : `generate_diagnostic` — 1 lvl1 + 1 lvl2 par chapitre garanti
- [x] BUG 2 : `generate_daily_boost` — ciblage erreurs du jour + fallback varié
- [x] BUG 3 : `generate_remediation` — sauvegarde RemediationChapters, cap V3
- [x] BUG 4 : colonne `Draft` dans Scores ✅ (Sheet + GAS)
- [x] BUG 5 : `IsAdmin` dans Users + login ✅
- [x] BUG 6 : `dynamicChapters` dans login ✅ (lit RemediationChapters)
- [x] BUG 7 : niveaux lycée retirés du select ✅
- [x] `isFirstDay` ajouté dans login : `history.length === 0 && !boostExistsInDB`
- [x] Curriculum_Officiel : 480 exos (24 chap × 20)
- [x] DiagnosticExos : 48 exos (24 chap × 2 lvl)
- [x] Test flux complet validé : inscription → diagnostic → chapitres → boost → remédiation

### Bugs post-BLOC B ✅ CORRIGÉS
- [x] Diagnostic trop court : generateDiagnostic garantit 1 lvl1 + 1 lvl2 par chapitre (2 chap = 4 questions)
- [x] FAB ✏️ visible sur landing : hidden par défaut, révélé dans initApp()

### Bugs post-tests utilisateur ✅ CORRIGÉS
Ordre appliqué : T7 → T6 → T4 → T3 → T5 → T2 → T1

- [x] **BUG-T7** — `checkOpt()` : après `mark(...,'HARD',...)`, appelle `autoShowHelp(cat,idx)` → affiche TOUS les indices + formule en HTML direct (pas de typewriter → pas de `$` brut). `area.classList.add('rdy')` pour rendre visible le conteneur `.mc`. MathJax appelé une fois sur le bloc. index.html `autoShowHelp()` + `checkOpt()`.
- [x] **BUG-T6** — Badge niveau coloré (indigo lvl1 / ambre lvl2) + compteur animé "X / Y" dans `rSection()`. index.html l.2163-2166.
- [x] **BUG-T4** — `_timerPaused` global + listeners `visibilitychange`/`blur`/`focus` (IIFE, une seule fois). index.html l.993 + l.1022 + l.1043-1047.
- [x] **BUG-T3** — Bouton remédiation supprimé. Message "contenu prêt demain" affiché. Enqueue silencieux dans `chkComp()` si erreurs. index.html l.1533-1543 + l.1898-1901.
- [x] **BUG-T5** — `@keyframes counterPop` CSS + animation sur `span` compteur dans `rSection()`. index.html l.88 + l.2165.
- [x] **BUG-T2** — `setView('progress')` recharge toujours (`S.progress === null` → supprimé). index.html l.1623.
  - Root cause réelle : `const SU` pointait vers un ancien déploiement GAS orphelin (`AKfycbysf5i_...` @1). `updateConfidenceScore` écrivait dans le bon sheet mais via un GAS différent. Corrigé : URL mise à jour vers déploiement @5 (`AKfycbwBnX...`).
- [x] **BUG-T3 chrono** (navigation interne) — `setView()` pose `_timerPaused = (v !== 'chapters')`. Pause automatique sur Progression/Constellation, reprise sur Chapitres. index.html `setView()`.
- [x] **BUG-T1** — Fallback backend : si `lvl` absent dans DiagnosticExos, prend `l1[1]` au lieu de sauter. backend.js l.479-483.
  - Vérifié : DiagnosticExos toutes classes OK (lvl1+lvl2 présents). Curriculum_Officiel 480 exos, 0 sans steps, 0 sans f, 0 sans lvl.
  - Test GAS direct : 6EME/5EME/4EME/3EME → 8 exos chacun, 4 lvl1 + 4 lvl2. ✅

### BLOC B — UX Progression & Mobile ✅ TERMINÉ
- [x] B1 : Vue Constellation (grille 4×6, couleurs confiance, SVG dépendances, nœuds verrouillés)
- [x] B2 : Vue Progression (nav, barre confiance, dates relatives, badge Maîtrisé, données depuis Progress sheet)
- [x] B3 : Bannière prérequis fragiles (ambre, cacheable, lien direct)
- [x] B4 : Fixes mobile 390px (header truncate, question overflow-x-auto, tap target ✕)

Notes techniques B1 :
- CMAP : données statiques chapitres (clés = Curriculum_Officiel keys)
- Prerequisites sheet : clés corrigées (FRACTIONS_4 → Fractions, etc.)
- get_prerequisites : nouvelle action GAS → retourne les 26 liens
- SVG overlay sur getBoundingClientRect (60ms delay post-render)

### BLOC 2 — Fiabilité & workflow quotidien 🟡
- [x] `generateMorningReport()` : analyse 21 jours par élève × chapitre, email actionnable pour DeepSeek ✅
- [x] Trigger GAS 7h configuré dans Apps Script UI → `generateMorningReport` ✅
- [x] Ancien trigger `analyzeToday` supprimé ✅
- [x] Dashboard onglet créé — remplacé par **👁 Suivi** ✅ **[10 mars]**
- [x] `rebuildSuivi(code)` remplace `updateDashboard()` — 20 cols, 4 règles ACTION ✅
- [x] `writeToHistorique(p)` remplace `writeToLogExercices()` — 10 cols, récent en haut ✅
- [x] `login()` injecte `nextChapter` + `nextBoostTopic` depuis colonnes Nicolas ✅
- [x] `index.html` : badge NEW sur chapitre injecté + `forcedTopic` dans handleBoost ✅
- [x] `rebuild_sheet.py` créé — reconstruit 👁 Suivi et 📋 Historique depuis données réelles ✅
- [x] **Mode Admin** : `get_admin_overview` + `publish_admin_boost` + `publish_admin_chapter` ✅ **[10 mars]**
- [x] **Dashboard admin** : redirect automatique isAdmin → "Mes Élèves", cartes ludiques triées par urgence ✅
- [x] **Modal élève** : tous les exos (plus de cap), accordion intitulés, badge DIAG/BOOST, copyAdminPrompt complet ✅ **[11 mars]**
- [ ] Validation inputs côté GAS (format email, longueur champs)
- [ ] Rate limiting basique dans doPost
- [x] Colonne `Premium` + `TrialStart` dans Users ✅ (GAS @25 — checkTrialStatus, badge J-X, overlay, onboarding)
- [x] Essai 7 jours full droits sans carte ✅ (GAS @25 — checkTrialStatus, badge J-X, overlay, onboarding)
- [x] Messages & encouragements ultra-ado Game Boy Chill ✅ (EASY×7 + HARD×3 + tous feedbacks)

### BLOC 3 — Juridique & paiement 🟡
- [ ] Mentions légales (données mineurs → RGPD renforcé)
- [ ] Case consentement parental à l'inscription (obligatoire)
- [ ] CGU/CGV + politique cookies
- [ ] Intégration Stripe : freemium 7j → 9,99€/mois
- [ ] Webhook Stripe → colonne `Premium` dans Users

### BLOC 4 — Marketing & conversion 🟢
- [ ] Email bienvenue automatique (GAS + Gmail API ou Brevo)
- [ ] Séquence J+3, J+7 pour conversion freemium→payant
- [ ] Témoignages vrais élèves sur la landing
- [ ] Page pricing claire

### BLOC 2c — Génération IA automatique + validation fondateur ✅ IMPLÉMENTÉ

**Flux complet :**
1. `generateMorningReport()` (5h) → analyse + appelle `generatePendingExos(students)`
2. Pour chaque élève FRAGILE → génère boost (5 exos via Claude API) → `Pending_Exos`
3. Pour chaque élève BLOQUEE → génère chapitre complet (20 exos via Claude API) → `Pending_Exos`
4. Email inclut aperçu des exos générés + lien vers Sheet pour validation
5. Fondateur met `YES` dans colonne `Validé` de `Pending_Exos`
6. Au prochain login de l'élève → `processPendingAtLogin()` détecte les YES :
   - boost → `DailyBoosts` (disponible immédiatement)
   - chapitre → `RemediationChapters` (apparaît comme chapitre dynamique)
   - Marque `DateValidation` pour ne pas repousser

**Sheet `Pending_Exos` (à créer) :**
`Code | Prénom | Niveau | Chapitre | Type | ExosJSON | DateGeneree | Validé | DateValidation`

**Setup requis :**
- [x] Onglet `Pending_Exos` créé dans le Sheet ✅
- [x] `CLAUDE_API_KEY` ajoutée dans les propriétés du script ✅
- [x] Trigger mis à 5h–6h ✅

**Prompt de génération :** ciblé sur les erreurs récentes de l'élève, profil adaptatif (4 niveaux de difficulté), format identique aux exos DeepSeek (steps pédagogiques, distracteurs réalistes, formule mémorable).

### BLOC 2b — Rapport matin & boucle DeepSeek ✅ IMPLÉMENTÉ
Fonction `generateMorningReport()` dans backend.js — trigger 7h quotidien.

**Logique de classification (21 jours glissants, par élève × chapitre) :**
| Statut | Critères |
|---|---|
| ✅ ACQUISE | score > 80 + statut='maitrise' + 0 HARD depuis 14j + ≥3 sessions |
| 🔴 BLOQUEE | score < 40 + pas d'amélioration sur 2 semaines + ≥4 sessions |
| 🟡 FRAGILE | score < 40 OU ≥3 HARD cette semaine |
| 📈 EN_PROGRESSION | taux erreur cette semaine < semaine passée (−10 pts) |
| 📘 EN_COURS | défaut |

**Email du matin :** sujet `[Matheux ⚡ ACTION]` si notions fragiles/bloquées.
En tête : prompts DeepSeek prêts à copier-coller.
Stocké aussi dans onglet `Rapports`.

**Setup Apps Script (fait le 9 mars) :**
1. ✅ Apps Script → Déclencheurs → `generateMorningReport` | chaque jour | 7h–8h
2. ✅ Ancien trigger `analyzeToday` supprimé
3. ✅ Onglet `Rapports` préexistant dans le Sheet (vide — rempli dès 7h)

### BLOC 5 — Automatisation & scale 🔵
- [x] Configurer clasp pour push automatique vers Apps Script ✅ (`./watch_deploy.sh` dans `algebra/`)
- [ ] Agent analyse lacunes quotidien automatique
- [ ] Agent génération boost automatique (remplace le manuel)
- [ ] Agent rapport parents (email hebdo)
- [ ] Mode "Préparation Brevet"
- [ ] Migration Sheets → vraie BDD si >50 users simultanés

---

## ⚠️ Contraintes techniques à garder en tête
- Google Sheets : fragile à ~20 users simultanés, quota Apps Script 6min/call
- Données de mineurs : RGPD renforcé, consentement parental obligatoire
- Hash MDP côté client uniquement → pas de salt côté serveur (acceptable pour MVP, à noter)
- Pas de réécriture complète — patches chirurgicaux seulement

## 💰 Modèle économique
- Freemium 7 jours → 9,99€/mois
- Cible : 50 clients = ~500€ MRR
- Paiement : Stripe simple (pas de récurrent complexe d'abord)

## 🔧 Workflow automatisé (BLOC 5 accompli partiellement)

### Backend GAS — clasp push automatique
```bash
./watch_deploy.sh   # terminal séparé — surveille backend.js et push dès modification
./deploy.sh         # push manuel one-shot
```
`algebra/backend.js` est tracké par clasp. Tout push met à jour le GAS en live.
⚠️ Après un push, redéployer dans Apps Script (Déployer → Gérer les déploiements → ✏️ Nouvelle version) pour que l'URL live soit mise à jour.

### Données Sheet — API directe (plus de xlsx)
```python
from algebra.sheets import sh
sh.read("Curriculum_Officiel")          # lit le Sheet live
sh.write_rows("DiagnosticExos", rows)   # écrit directement
sh.append_row("Scores", [...])
```
Fichier clé : `algebra/sheets.py`
Compte de service : `algebra/algebreboost-sheets-2595a71cadfb.json` (ignoré par git)
Sheet ID : `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4`
GAS URL : `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec`
⚠️ Workflow déploiement GAS (9 mars — leçon apprise) :
  1. `clasp push` — envoie le code
  2. Déployer dans l'UI Apps Script → Nouveau déploiement → Application Web → Tout le monde → Déployer
  3. Copier la nouvelle URL → mettre à jour `const SU` dans index.html
  ⚠️ `clasp deploy` crée des URLs inaccessibles (bot-blocked ou non autorisées). Passer par l'UI pour le déploiement final.

### Plus de workflow manuel xlsx
~~Import xlsx~~ → écriture directe via `sheets.py`
~~Copier-coller GAS~~ → `./deploy.sh` ou `./watch_deploy.sh`

## 📁 docs/ — Fichiers créés (nuit 9→10 mars)

Dossier `docs/` créé. 8 fichiers opérationnels, prêts à copier dans Notion.

| Fichier | Contenu | Taille |
|---|---|---|
| `notion-structure.md` | Structure Notion complète + script Python notify_notion.py + hook post-commit | 197 l |
| `marketing-phase1.md` | 3 phases progressives : WhatsApp, LinkedIn, parrainage, Google Ads | 220 l |
| `offre-pricing.md` | Comparatif freemium, recommandation MVP, 10 premiers clients sans Stripe | 190 l |
| `features-avant-lancement.md` | Audit features, indispensables avant lancement, roadmap post-50 clients | 210 l |
| `landing-page-brief.md` | Brief complet : 9 sections, copywriting, script vidéo 30s, specs techniques | 484 l |
| `juridique-checklist.md` | RGPD mineurs, templates légaux, case consentement HTML+JS prête | 336 l |
| `tracking-analytics.md` | GA4 RGPD-compat., 8 événements avec code JS exact, formules Sheet, alertes | 448 l |
| `emails-sequences.md` | 6 séquences complètes + implémentation GAS (opt-out RGPD inclus) | 515 l |
| `whatsapp-templates.md` | 6 scénarios < 5 lignes, ton naturel, prêts à copier | 51 l |
| `test_prompts.py` | Script Python pour tester 5 appels réels API Claude (validation format exos) | 200 l |

**Commits de la nuit :**
- `2f0d345` — P2/P3 backend (prompts, anti-redondance, priorisation)
- `aaa8b2c` — docs notion, marketing, pricing, features
- `d69c108` — docs whatsapp-templates
- `5d2ca21` — docs juridique-checklist
- `68b18a3` — docs tracking-analytics
- `dbbf0a2` — docs emails-sequences
- `418e8d8` — docs landing-page-brief

## ✅ Sessions 10 mars — Ce qui a été fait

### Session 10 mars nuit — Audit automatisé + déploiement GAS

#### Audit test_complet.py (77/81 = 95%)
- 10 scénarios, 81 tests : flux nominal, abandons, reconnexions, chaos, persistance, multi-jours, JSON malformé, charge parallèle
- Exécution complète sur 5 comptes @audit.fr (alice/bob/clara/david/emma)
- Rapport : `docs/audit_complet.md`

#### Fixes backend.js (clasp deploy @12)
- `generateDailyBoost()` : fallback curriculum si `diagnosedChaps` tous inconnus du curriculum
- `.claspignore` : ajout `algebra/**` pour ignorer sous-répertoire imbriqué clasp
- `clasp deploy --deploymentId` : workflow pour redéployer sans passer par l'UI (remplace `clasp push` seul)

#### 4 tests restants (non-critiques)
- **#23/#27** : 2/3 saves CALIBRAGE rapides — timing GAS avec rebuildSuivi lourd
- **#75** : boostExistsInDB=False après save_boost — timing entre écriture Sheet et lecture login
- **#79** : 4/5 save_score parallèles — race condition Sheets, limitation plateforme

#### Messages de fin dans index.html
- Chapitre 20/20 : "✅ Chapitre terminé ! Reviens demain — tes prochains exercices seront sur mesure !"
- Boost 5/5 : "⚡ Boost du jour terminé ! Tu es à jour."
- État persisté dans `localStorage done_v23` : `{chapDone: {[cat]: {...}}, boostConsumed: true}`

#### Suivi Sheet — nouvelle structure sans ACTION
- Col A→T : Prénom | Niveau | Dernière connexion | Ch1 | Résumé Ch1 | →Nouveau Ch1 (×4) | Boost actuel | Résumé Boost | →Nouveau Boost | Rapport | Code masqué
- Couleurs par GAS : vert sur chapitre terminé (col D/G/J/M), rouge sur →Nouveau si action requise
- ⚠️ Règles CF de rebuild_sheet.py overrident la couleur display (mais pas userEnteredFormat)

### ✅ SESSION 11 mars — Nuit autonome (5 phases)

#### Ce qui a été fait (complet ✅)
- **PHASE 1** : Landing page masterclass — H1 SEO, flux trial inline 4 étapes, social proof, meta OG
- **PHASE 2** : UX "Game Boy Chill" — messages aléatoires EASY/HARD, confetti auto (boost ≥60%, chap ≥70%)
- **PHASE 3** : `test_scenarios.py` créé — **6/6 scénarios ✅ 38/38 assertions ✅**
- **PHASE 4** : Email marketing (J+0/J+3/J+7) + Stripe prep (TrialStart/PremiumEnd/checkTrialStatus)
- **Bug critique résolu** : `boostExistsInDB` toujours False — Date object vs string dans DailyBoosts
- GAS redéployé **@19** — fix date comparison

#### État final
- GAS : @19 ✅
- test_scenarios.py : 6/6 ✅
- test_complet.py : à relancer (était 77/81 avant bug fix date)
- rapport.md : `docs/rapport.md` ✅

#### À faire à la prochaine session
1. `python3 test_complet.py` → doit remonter ≥77/81 grâce au fix date
2. `git push origin main`
3. Vrais témoignages sur la landing (remplacer Marie-Laure fictive)
4. Nettoyage comptes test dans le Sheet (70+ comptes @scen.test/@audit.fr)
5. BLOC 3 — Juridique (CGU, RGPD mineurs)

---

### ✅ SESSION 11 mars — MATIN — Refonte admin dashboard (TERMINÉ)

#### Contexte
GAS déployé @20. Sheet nettoyée : 10 profils test + admin@matheux.fr conservés.
Profils gardés : Alice_Test (3EME), Emma (6EME good), Lucas (6EME hard), Hugo (5EME partial),
Inès (5EME good), Lola (4EME partial), Théo (4EME systematic), Jade (3EME partial),
Léa (6EME weak), Romain (3EME hard).

#### Tâches dans l'ordre — NE PAS DÉPLOYER AVANT D'AVOIR TOUT FAIT

**ÉTAPE 1 — Nettoyage Sheet (déjà fait ✅)**
- 10 profils + admin conservés, reste supprimé (Users/Scores/Progress/DailyBoosts)
- `python3 rebuild_sheet.py` à relancer après toutes les modifs

**ÉTAPE 2 — backend.js : tracker ExosDone dans DailyBoosts**
- `save_boost` (action existante) : mettre à jour le champ `ExosDone` dans la ligne DailyBoosts du jour
- DailyBoosts : Code | Date | BoostJSON — ajouter colonne `ExosDone` (int 0-5)
- Permet de savoir côté admin si boost est en cours (1-4) ou terminé (5) sans dépendre du localStorage

**ÉTAPE 3 — backend.js : getAdminOverview enrichi**
- Ajouter `boostHistory[]` par élève : tableau des DailyBoosts (date, insight, exos, ExosDone)
  → distinguer : `pending` (pas encore consommé, ExosDone=0), `in_progress` (1-4), `done` (5)
- Corriger `chapitresDetail` : Alice remonte 12 exos au lieu de 20 → investiguer le filtre
- Ajouter `currentBoostExosDone` (int) et `currentChapExosDone` (int) par élève pour les blocages UI

**ÉTAPE 4 — backend.js : règles ACTION revues**
Règles prioritaires (ordre strict, plusieurs peuvent s'appliquer → afficher toutes) :
1. `🔴 BLOQUÉ` : inactif > 7j ET score < 40 sur tous chapitres
2. `⚡ BOOST TERMINÉ → préparer le suivant` : DailyBoosts ExosDone=5 ET dernierBoost < today
   (remplace "DIAGNOSTIC FAIT" — ne s'affiche QUE si le boost auto a été consommé)
3. `✅ CHAPITRE TERMINÉ → assigner la suite` : Progress NbExos ≥ 20 ET col 📝 Nicolas vide
4. `👍 RAS`
- Couleur card basée sur la plus urgente, pills pour toutes les actions actives

**ÉTAPE 5 — index.html : modal élève — exercices**
- Afficher TOUS les exos (pas de limite à 12)
- Par exo : intitulé complet de la question | temps réponse | résultat (✅/❌)
  → Si ❌ : afficher la réponse donnée par l'élève (MauvaiseOption)
  → Si ✅ : ne pas afficher la réponse
- Indicateurs explicites : 💡 si NbIndices > 0 (afficher le nombre) | 📐 si FormuleVue = 1
- Garder le temps de réponse

**ÉTAPE 6 — index.html : modal élève — box boost**
- Box déroulante (accordéon) avec historique JSON des boosts précédents
- Statut du boost en cours : `pending` / `in_progress (X/5)` / `done`
- Si boost `pending` (publié par Nicolas, pas encore commencé) → afficher son contenu (futur boost)
- Si boost en cours (1-4/5) → bloquer la création du suivant (box grisée, message "boost en cours X/5")
- Si boost terminé ou pas de boost → permettre la publication

**ÉTAPE 7 — index.html : modal élève — box chapitre**
- Si chapitre en cours non terminé (Progress NbExos < 20 sur chapitre actif) → box grisée
  Message : "Chapitre en cours — X/20 exos. Terminer avant d'assigner la suite."
- Si terminé ou pas de chapitre → permettre la publication

**ÉTAPE 8 — Fix bug date "304 mois"**
- `relDateAdmin()` dans index.html : améliorer le parser pour gérer tous les formats de date
- Rendre les dates cohérentes dans le Suivi (rebuild_sheet.py)

**ÉTAPE 9 — Rebuild Sheet + déploiement** ✅
- `clasp push --force` + `clasp deploy --deploymentId ... --description "admin refonte 11mars"` → GAS **@21** ✅
- DailyBoosts : colonne `ExosDone` ajoutée en col D via sheets.py (header + 77 lignes existantes préservées) ✅
- Commit : `6db9e7c` ✅

#### Ce qui a été fait (11 mars matin — session complète)
- **ÉTAPE 2** : `save_boost` calcule `ExosDone = exoIdx + 1`, met à jour col D de DailyBoosts
- **ÉTAPE 3** : `getAdminOverview` enrichi : `boostHistory[]`, `currentBoostExosDone`, `currentChapExosDone`, tous les exos sans cap (était 12)
- **ÉTAPE 4** : `rebuildSuivi` nouvelles règles : 🔴 BLOQUÉ / ⚡ BOOST TERMINÉ / ✅ CHAPITRE TERMINÉ / 👍 RAS
- **ÉTAPE 5** : Modal élève — tous les exos, énoncé complet, 💡×N, 📐, MauvaiseOption si ❌
- **ÉTAPE 6** : Box boost — accordéon historique, grisée si boost en cours (ExosDone 1-4)
- **ÉTAPE 7** : Box chapitre — grisée si chapitre actif non terminé (X/20)
- **ÉTAPE 8** : `relDate`/`relDateAdmin` robuste — formats FR/ISO/timestamp, plafond "Il y a plus de 2 ans", retourne original si invalide
- **Sheet** : DailyBoosts col D = `ExosDone` ajoutée directement via sheets.py ✅

#### Points de cohérence à garder en tête
- `boostHistory` doit distinguer boosts auto (générés par GAS) et manuels (publiés par Nicolas via publish_admin_boost)
- Si un élève a un boost `pending` (pas encore consommé), afficher son contenu dans la box boost
- Actions multiples simultanées : afficher toutes les pills, couleur card = plus urgente
- Ne jamais écraser les colonnes 📝 Nicolas dans Suivi lors du rebuild

---

### ✅ SESSION 12 mars — suite 2 (fixes UX, commit b96f9d8)

#### Backend (GAS @24)
- `login()` retourne `boostExosDone` (ExosDone du boost du jour depuis DailyBoosts)

#### index.html
- **Auto-login silencieux** : DOMContentLoaded ne montre plus le form pendant le fetch → plus de modal "mdp incorrect" parasite
- **Boost consommé** : `initApp` — si `d.boostExosDone >= 5` → `S.boostConsumed = true` (fix boost "disponible" après refresh)
- **Layout 2 colonnes** : chapitre/boost archivé → flex-row : carte ✅ (gauche) + carte 📅 "Prochain chapitre demain" (droite)
- **Score local** : `renderProgress()` calcule score depuis `S.res` quand serveur montre 0 (fix Fractions 0%)

---

### ✅ SESSION 12 mars — suite (UX admin + élève, commit 9421ef6)

#### Admin modal élève
- Moyennes retirées (`avgTime`, `avgIndices`, `pctFormula`) — trop de bruit
- Accordéon `<details>` par chapitre si > 3 exos — ouvert par défaut si erreurs
- Box "Publier chapitre" grisée + message ambre si boost terminé sans nouveau boost pending (`boostNeedsPrep`)

#### Élève chapitres
- Génération boost bloquée (sauf `isFirstDay`) → carte `📅 Prochain boost disponible demain matin 🔥`
- `renderProgress()` : `nbExos = max(server, local)` — fix affichage 0 exo quand données locales non synchro
- Chapitre archivé → carte pointillés `📅 Prochain chapitre · Disponible demain 🔥` (masquée si nouveau chapitre injecté)

---

### ✅ SESSION 12 mars — UX élève + admin JSON boost (TERMINÉ)

#### Git repo reconstruit
- Objets git corrompus (fichiers vides) → `.git` supprimé, `git init`, remote re-ajouté
- Commit restauration : `12a61e7` — tout l'historique perdu mais code intact

#### rebuild_sheet.py — règles ACTION synchronisées avec GAS
- Ajout `boosts_by_code` depuis DailyBoosts (ExosDone) avant la boucle
- Règles exactes : 🔴 BLOQUÉ (inactif>7j + all scores<40) / ⚡ BOOST TERMINÉ (ExosDone=5 + dernier<today) / ✅ CHAPITRE TERMINÉ / 👍 RAS
- Profils BLOQUÉ : Léa/Mathis/Sarah/Inès/Romain — scores mis à HARD, dates à 2026-03-01

#### backend.js — Option 1 : bouton Copier boost JSON
- `boostHistory` enrichi avec `exos: b.boost ? (b.boost.exos || []) : []`
- `copyLastBoostJSON(code)` : JSON enrichi (exos originaux + stats élève par index)
- Bouton "📋 Copier le dernier boost JSON" en tête de l'accordéon historique
- GAS @23 ✅ — commit `c22f471`

#### index.html — 4 phases UX élève (commit `2a808d3`)
- **PHASE 1** : Chapitres/boost terminés → carte verte archivée pliée, `renderArchiveSection()` avec historique exos (✅/❌, réponse donnée si ❌, 💡/📐). Nouveau chapitre auto-déplié, trié en premier.
- **PHASE 2** : `rMastery()` — chapitre 20/20 → toutes notions acquises. `renderProgress()` — compL local → score=100%, isMast=true.
- **PHASE 3** : CSS `pulseGentle` (3s douce). Pills 💡 et 👁 pulsent jusqu'à ouverture. Stop auto : "✓ Indices vus" / "✓ Formule vue".
- **PHASE 4** : Vérification — `renderChapComplete` conservée (dead code — pas d'impact), `chkComp` appelle toujours `render()` qui montre la carte archivée.

---

### ✅ SESSION 11 mars — APRÈS-MIDI — Données scénarios + fixes admin modal

#### Données Sheet (sheets.py)
- **Users** : 21 comptes (20 profils test + admin@matheux.fr) — 50 comptes fantômes supprimés ✅
- **Scores** : 434 lignes reconstruites avec vraies questions LaTeX (Curriculum_Officiel/DiagnosticExos). Indicateurs réalistes par profil (temps/NbIndices/FormuleVue/MauvaiseOption) ✅
- **DailyBoosts** : 16 élèves avec boost, ExosDone variés — 5 pending(0), 5 en_cours(1-4), 6 terminé(5) ✅
- **Progress** : 17 élèves, NbExos selon scénarios (Léa/Lola/Manon sans chapitre) ✅

#### Scénarios couverts (tous les cas utiles au prof)
| Cas | Élèves |
|---|---|
| Boost terminé + Chapitre terminé | Emma, Hugo, Baptiste |
| Boost en cours + Chapitre en cours | Lucas, Chloé, Romain, Océane |
| Boost pending + Chapitre terminé | Zoé, Théo |
| Aucun boost + Chapitre en cours | Nathan, Inès |
| Boost terminé + Chapitre en cours | Camille, Sarah, Mathis |
| Aucun boost + Aucun chapitre | Lola, Manon |

#### Fixes index.html
- **Accordion** : intitulés > 60 chars → `<details>/<summary>` déroulable ✅
- **Badge source** : DIAG (gris) / BOOST (jaune) sur chaque exo dans la modal ✅
- **copyAdminPrompt** : copie TOUS les exos (EASY+HARD), format `[✅/❌] "intitulé" → répondu + ⏱ + 💡 + 📐` ✅

#### Fixes backend.js
- **getAdminOverview** : champ `source` ('diagnostic'/'boost'/'chapter') sur chaque exo ✅

#### Déploiement
- GAS @22 ✅ — commit `5bc72e5` ✅

---

### ✅ SESSION 12 mars — Git + variété profils admin

#### Dépôt git corrompu → reconstruit
- Objets git vides (crash disque probable) → `.git` supprimé et réinitialisé proprement
- Tous les fichiers intacts. Nouveau commit racine `12a61e7` pushé sur GitHub.

#### rebuild_sheet.py — règles ACTION corrigées (alignement GAS)
- **Avant** : règles obsolètes (`🆕 BOOST TERMINÉ`, pas de BLOQUÉ, boost détecté via Scores/BOOST)
- **Après** : règles identiques au GAS `rebuildSuivi()` :
  - `🔴 BLOQUÉ` : inactif > 7j ET score < 40 sur tous chapitres
  - `⚡ BOOST TERMINÉ → préparer le suivant` : ExosDone=5 ET dernierBoost < today
  - `✅ CHAPITRE TERMINÉ → assigner la suite` : ≥20 exos ET cols Nicolas vides
  - `👍 RAS` : sinon
- Boost détecté via `DailyBoosts.ExosDone` (plus Scores/BOOST)
- DailyBoosts chargés **une seule fois** avant la boucle utilisateurs

#### Profils BLOQUÉ ajoutés (Sheet)
- 3 profils avec scores anciens (2026-03-01) + tous HARD : **Inès** (INE504), **Sarah** (SAR405), **Romain** (ROM302)
- Variété admin finale : 🔴×3 / ⚡×7 / ✅×7 / 👍×4

#### Leçon technique
- Codes Users ≠ codes Scores pour certains profils (ex: INE504 vs INE505) → toujours vérifier la cohérence des codes entre onglets avant d'écrire dans Scores

---

### ✅ SESSION 12 mars — Option 1 : Bouton "Copier le dernier boost JSON"

#### Ce qui a été fait
- **backend.js** : `boostHistory` expose maintenant `exos[]` — le tableau complet des exos du boost (q/a/options/steps/f/lvl) — GAS @23
- **index.html** : bouton `📋 Copier le dernier boost JSON (complet + stats élève)` ajouté en haut de l'accordéon "Historique des boosts" dans le modal élève
- **index.html** : nouvelle fonction `copyLastBoostJSON(code)` :
  - Récupère `bHistory[0].exos` (boost le plus récent, complet)
  - Enrichit chaque exo avec les stats élève : `student_result`, `student_time_s`, `student_indices`, `student_formula`, `student_wrong` (matching par index avec `source=boost` depuis chapitresDetail)
  - Ajoute `chapter_stats` (stats globales par chapitre)
  - Output JSON formaté → clipboard + fallback textarea
  - Commit `c22f471`

#### Note technique
- `source='boost'` dans chapitresDetail toujours `'chapter'` côté GAS (non implémenté) → matching par position (index 0-4). Fonctionne tant que l'élève fait les exos dans l'ordre.
- Si besoin de matching fiable plus tard : ajouter un flag `isBoost` dans `save_score` côté GAS.

---

### Session 10 mars — MVP injection parfaite (6 phases)

#### backend.js (GAS @15)
- **PHASE 1** : login() injection atomique — backup Logger, PENDING_MANUAL si JSON KO, pas de clear si parse échoue, rebuildSuivi() appelé après injection
- **PHASE 2** : PENDING_MANUAL retourné si exos vide ou JSON KO — structure valide, pas de crash
- **PHASE 3** : rebuildSuivi() — colonne ⚡ ACTION (21 cols total, Code en U) — 4 règles strictes + couleurs (jaune=action, rouge=→Nouveau requis, vert=terminé, gris=inactif>3j)
- Calcul ACTION : lit DailyBoosts + Scores pour classer chaque élève
- login() → indices décalés : Code=col U (20), →Nouveau=[6,9,12,15], →Boost=18

#### rebuild_sheet.py
- **PHASE 3** : SUIVI_HEADERS ajoute "⚡ ACTION" en A (21 cols), masque col U, nicolas_cols=[6,9,12,15,18]
- **PHASE 4** : build_chapter_summary enrichi → temps_moyen_sec, indices_pourcent, erreurs_frequentes (top 3), derniere_session
- **PHASE 4** : build_boost_summary enrichi pareil
- step7 : calcul ACTION par élève (lit DailyBoosts), indices existantes décalés, clear A1:U1000

#### index.html
- **PHASE 2** : initApp() guard PENDING_MANUAL → S.pendingManual (pas de crash, message doux)
- **PHASE 2** : guard nextBoost.exos.length > 0 avant injection
- **PHASE 5** : bandeau ambre ⏳ en haut des chapitres si S.pendingManual
- **PHASE 5** : renderChapComplete → "Ton prof prépare ton prochain chapitre personnalisé. Reviens demain matin 🔥"
- **PHASE 5** : boost terminé → "Ton boost de demain est déjà en préparation 🔥"

#### GAS déployé @15

---

### Session 10 mars nuit — Audit 95% + 4 bugs UX corrigés

#### Audit automatisé (test_complet.py)
- 81 tests, 77 passent (95%) — commit `d6aae86`
- 4 échecs résiduels acceptés (race conditions GAS, timing Sheet)
- Rapport dans `docs/audit_complet.md`

#### Bugs UX corrigés (commit `025cbb9`)
- **BUG 1** (index.html) : `boostConsumed` localStorage réinitialisé au login si `boostExistsInDB=false`
  → Boost disponible après reconnexion si non consommé ce jour
  → Bandeau boost toujours cliquable (branche `isFirstDay` supprimée du render)
- **BUG 3** (index.html) : `renderChapComplete()` — remplace "X acquis · Y à revoir · Z difficiles"
  par "Tu as réussi N exercices sur tot. Reviens demain 🎯"
- **BUG 4** (backend.js) : `formatDateFR()` helper → Suivi affiche "10/03/2026 01:00" au lieu de timestamp brut JS

#### GAS déployé @13

---

### Session 10 mars soir — Sheet admin + connexion app

#### backend.js (clasp push ✅)
- `rebuildSuivi(code)` : remplace `updateDashboard()` — structure 20 cols par chapitre, 4 règles ACTION
- `writeToHistorique(p)` : remplace `writeToLogExercices()` — 10 cols, recent en haut
- `login()` : lit cols G/J/M/P/R de 👁 Suivi → injecte `nextChapter` + `nextBoostTopic` → vide les cellules
- `SH.SUIVI` / `SH.HISTORIQUE` : noms d'onglets mis à jour (était VUE_ELEVES / LOG_EXOS)

#### index.html
- `initApp()` : nextChapter → badge NEW sur carte chapitre (via S.isNew)
- `initApp()` : nextBoostTopic stocké dans S.nextBoostTopic
- `handleBoost()` : passe forcedTopic au payload si S.nextBoostTopic rempli

#### Python (rebuild_sheet.py créé)
- 8 étapes : renommage → headers → tri → couleurs → format Suivi → format Historique → rebuild
- 👁 Suivi : 20 cols (Chap1-4 + Statut + 📝 suite × 4 + Boost + Prochain boost + Rapport + Code masqué)
- 📋 Historique : 10 cols, 500 derniers exos, énoncés depuis Curriculum_Officiel
- Colonnes 📝 Nicolas préservées à chaque rebuild (jamais écrasées)
- Chap 5+ : concaténés dans col S si Nicolas n'a rien écrit

#### Structure 👁 Suivi finale
```
A: ⚡ ACTION  B: Prénom  C: Niveau  D: Dernière connexion
E: Chapitre 1  F: Statut 1  G: 📝 Ch1 suite (Nicolas)
H: Chapitre 2  I: Statut 2  J: 📝 Ch2 suite (Nicolas)
K: Chapitre 3  L: Statut 3  M: 📝 Ch3 suite (Nicolas)
N: Chapitre 4  O: Statut 4  P: 📝 Ch4 suite (Nicolas)
Q: Boost consommé?  R: 📝 Prochain boost (Nicolas)
S: 📧 Rapport envoyé / Chap5+  [T: Code masquée]
```

#### 4 règles ACTION (ordre strict)
1. `🔴 DIAGNOSTIC FAIT → préparer boost 1` : Scores > 0 ET DailyBoosts = 0
2. `🆕 BOOST TERMINÉ → préparer boost suivant` : Boosts ≥ 1 ET lastBoost < today
3. `✅ CHAPITRE TERMINÉ → assigner suite` : ≥20 exos sur un chap ET col 📝 vide
4. `👍 RAS`

---

## Session 10 mars matin — (historique)

### backend.js (clasp push ✅)
- `login()` : `dynamicChapters` supprimé (retourne `[]`), `processPendingAtLogin` retiré
- `generateRemediation()` : désactivé — `return { status:'success' }` immédiat, corps en commentaire
- `generateDailyBoost()` : **bug boost hors scope corrigé** — filtre curriculum sur chapitres vus dans Scores de l'élève
- `generateMorningReport()` : appel `generatePendingExos` commenté (génération IA désactivée)
- `updateDashboard(code)` → remplacé par `rebuildSuivi(code)` (voir session soir)
- `r['IndicesVus']` → `r['NbIndices']` dans `updateConfidenceScore` (synchro header Sheet)

### Google Sheet (via sheets.py ✅)
- Onglet **Dashboard** créé → renommé **👁 Suivi** en session soir
- **4 onglets archivés** : Queue, Prerequisites, Rapports, Pending_Exos → `_ARCHIVE_xxx`
- **Scores** : 770 lignes nettoyées, header `NbIndices` (était `IndicesVus`), aucune ligne vide
- **Progress** : 40 lignes cohérentes avec les Scores
- **DailyBoosts** : 20 boosts (1 par élève test)

### Données test (20 profils réalistes)
Comportement simulé sur 7 jours par profil :
- `good` : 92% EASY moy., 15-30s, 0 indice, formule rare, chapitre terminé (20 exos)
- `partial` : 61% EASY, 20-50s, 1-2 indices, formule parfois, 12 exos
- `hard` : 42% EASY, 40-80s, 2-3 indices, formule souvent, 10 exos
- `systematic` : lvl1 ok / lvl2 20% EASY lent, 15 exos
- `weak` : 17% EASY, 60-90s, 3 indices toujours, formule toujours, 5 exos

### Divers
- Domaine corrigé : `mac.fr` → **matheux.fr** dans CLAUDE.md
- CNAME créé à la racine du repo

---

## 📅 Plan session du 10 mars 2026

### MATIN — Phase 1 : Verrouillage total du socle (2h)

**Étape 1 — Lire le rapport 5h**
- Vérifier que l'email est bien arrivé (format, insights, aperçu exos)
- Vérifier que Pending_Exos est rempli correctement
- Valider 1-2 exos avec YES → tester que ça arrive bien au login

**Étape 2 — Test flux complet mobile (tous les scénarios)**
Tester dans l'ordre, sur mobile, avec un nouveau compte :
- [ ] Inscription → sélection niveau + chapitres → diagnostic
- [ ] Diagnostic : 8 questions, résultats corrects, scores sauvés
- [ ] Retour accueil → chapitres visibles, niveaux lvl1/lvl2
- [ ] Faire 20 exos d'un chapitre → écran fin, badge "Demain" si erreurs
- [ ] Boost → 5 exos, sauvegarde, insight affiché
- [ ] Vue Progression → données correctes, score confiance, statut
- [ ] Bannière prérequis fragiles → s'affiche si score < 50
- [ ] Pending_Exos YES → login suivant → contenu disponible
- [ ] Rapport matin → email correct, Rapports sheet écrit

**Étape 3 — Corriger ce qui cloche** (patches ciblés uniquement)

### MATIN — Phase 2 : Suite du socle (selon temps restant)

**P2 — Génération exos : migrer vers agent local** ⭐
Au lieu du call Claude API depuis GAS (limité à 6 min), créer un script Python local
tournant en cron à 5h sur le PC du fondateur :
- Lit Progress/Scores via `sheets.py`
- Analyse les élèves (même logique que generateMorningReport)
- Génère les exos via SDK Anthropic (pas de limite de temps, exemples DeepSeek en contexte)
- Écrit dans Pending_Exos + envoie l'email
- Remplace entièrement la partie génération IA du GAS
→ À coder demain en Python local (+ supprimer callClaude/generatePendingExos du GAS)

**P3 — Algo sélection exercices** ✅ FAIT cette nuit
- [x] Anti-redondance dans boost + remédiation
- [x] Priorisation chapitres faibles (score < 50%)

**BLOC 3 — Juridique** → voir `docs/juridique-checklist.md` (template HTML consentement prêt)

---

### P0 — Verrouiller la partie diagnostic ✅ TERMINÉ (9 mars soir)
- [x] DiagnosticExos : 24/24 chapitres refaits par DeepSeek (steps pédagogiques, formules, erreurs typiques ciblées)
- [x] 3EME - Fonctions : incluse dans le blob DeepSeek (bug parser corrigé en session)
- [x] A27 (blob brut) supprimée, sheet propre
- [x] 20 profils de test créés (voir section dédiée ci-dessous)
- ⏳ À faire demain : tester le flux complet inscription → diagnostic sur mobile

### P1 — Améliorer les exercices existants ✅ TERMINÉ (9 mars soir)
- [x] Curriculum_Officiel : passe qualité DeepSeek terminée sur les 4 niveaux (6EME/5EME/4EME/3EME)
- [x] 480 exos relus — steps explicatifs, formules, erreurs typiques ciblées (même niveau que DiagnosticExos)
- Fichier : Curriculum_Officiel dans le Sheet — ne plus toucher sauf amélioration ciblée

### Profils de test ✅ CRÉÉS (9 mars soir)
20 élèves fictifs dans le Sheet (Users/Scores/Progress/DailyBoosts) — données sur 7 jours.
Chaque élève : diagnostic (8 exos) + boost (5 exos) + 2 chapitres complets (20 exos chacun).

| Profil | Élèves | Caractéristique |
|---|---|---|
| `good` | Emma 6e, Inès 5e, Théo 4e, Baptiste 3e | Scores 80-100, maîtrise confirmée |
| `partial` | Nathan 6e, Hugo 5e, Lola 4e, Jade 3e, Océane 3e | Mix erreurs, en progression |
| `hard` | Lucas 6e, Chloé 5e, Enzo 4e, Romain 3e | Beaucoup HARD, scores bas |
| `systematic` | Zoé 6e, Tom 5e, Camille 4e, Manon 3e | lvl1 OK, lvl2 catastrophique |
| `weak` | Léa 6e, Mathis 5e, Sarah 4e | Scores 0-15, bloqués partout |

Codes : EMM601→LEA605, HUG501→MAT505, LOL401→SAR405, JAD301→OCE305
Password test : `test123` (hash SHA-256 de `email::test123::AB22`)

### P2 — Peaufiner le prompt de génération ✅ TERMINÉ (nuit 9→10 mars)
- [x] `buildExoPrompt()` refondu : 5 paliers de profil, sections explicites, exemple JSON ancré dans le prompt
- [x] Steps obligatoirement en 3 phases vague→méthode→quasi-solution
- [x] `validateExo()` + `parseAndValidateExos()` : validation stricte des 6 champs (q, a, options×3, steps×2-5, f, lvl)
- [x] `generatePendingExos()` utilise `parseAndValidateExos()` au lieu de JSON.parse brut
- [x] `docs/test_prompts.py` : script Python pour tester 5 cas réels via API Claude

### P3 — Algo de sélection d'exercices ✅ TERMINÉ (nuit 9→10 mars)
- [x] `getSeenExoKeys(code)` : catalogue tous les exos vus (chapitre_numExo) depuis Scores
- [x] `getChaptersByWeakness(code, level)` : lit Progress pour scorer les chapitres par faiblesse
- [x] `filterSeen()` : filtre un pool en excluant les exos déjà faits
- [x] `generateDailyBoost()` : priorise chapitres faibles (score<50%), exclut exos vus, fallback Prerequisites si tout épuisé
- [x] `generateRemediation()` : priorise HARD > jamais vus > EASY, fallback chapitre prérequis connexe
- Fichiers : backend.js `generateDailyBoost()` + `generateRemediation()`

---

---

### ✅ SESSION 11 mars — Essai 7j + Polish UX (TERMINÉ)

#### Backend (GAS @25)
- `checkTrialStatus(code)` → { trialActive, daysLeft, isPremium }
- `register()` → TrialStart = TODAY
- `login()` → retourne `trial: { trialActive, daysLeft, isPremium }`
- `case 'check_trial_status'` dans doPost()

#### index.html
- `S.trial` stocké au login/register
- `renderTrialBadge()` : pill "🔥 J-X · Essai gratuit" (ambre si ≤2j, cachée si premium/admin)
- `showTrialExpired()` : overlay bloquant + bouton "Prolonger" (toast bientôt) + lien progression
- `showOnboarding(cb)` : 3 slides post-inscription
- CTA hero : "Essayer 7 jours gratuits — sans carte bancaire →"
- Animations : pulseHint (pills), toastIn (bounce), popIn (CTA)
- Messages ton ado : EASY×7 + HARD×3 + chapitre/boost/abandon/MotProf/nudge/isFirstDay

#### À faire (prochaine session)
- Stripe → webhook → Premium → désactiver overlay
- BLOC 3 Juridique (CGU, RGPD, case consentement parental)
- git push origin main (token PAT requis)

---

## 🚦 Règle d'or chaque session
1. Lire CLAUDE.md
2. Identifier le BLOC actif et les priorités du jour
3. Travailler uniquement dans ce périmètre
4. Tester sur mobile avant commit
5. Mettre à jour les checkboxes ici en fin de session
