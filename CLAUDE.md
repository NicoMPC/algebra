# CLAUDE.md — Matheux (matheux.fr)
> Lis ce fichier en entier à chaque session. Mets à jour les checkboxes en fin de session.

---

## 🎯 Projet en une phrase
SPA vanilla JS (index.html ~3500 lignes) + backend Google Apps Script sur Google Sheets.
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
| `index.html` | SPA ~4700 lignes. CSS vars + Tailwind CDN + JS vanilla |
| GAS backend | `backend.js` — Web App déployée via clasp |
| Sheet ID | `1zLBajKVL8FUzy7aV2Myi9gYFEFJjnALkLAg0hbicuDk` |
| API URL | `const SU` dans index.html |
| Auth | localStorage clé `boost_v23` → `{ email, hash }` (auth uniquement — données depuis GAS) |
| State local | localStorage clé `boost_loc_v23` → `{ [code]: { stk, last } }` |
| Hash MDP | SHA-256 de `email + '::' + password + '::AB22'` (client-side) |
| Fonts | Syne (titres) + DM Sans (body) |

## 🔧 Workflow déploiement GAS
```bash
clasp push --force
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "description"
```
- GAS URL : `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec`
- Sheet ID scripts Python : `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4`
- Compte de service : `algebra/algebreboost-sheets-2595a71cadfb.json` (ignoré par git)
- ⚠️ `clasp deploy` seul sans `--deploymentId` crée des URLs inaccessibles → toujours passer l'ID
- `deploy.sh "description"` fait push + deploy en une commande

## 📦 Actions GAS — état réel (@34)
| Action | Statut |
|---|---|
| `register` | ✅ Fonctionne — TrialStart = TODAY |
| `login` | ✅ Fonctionne — retourne `trial: { trialActive, daysLeft, isPremium }` + `boostExosDone` |
| `save_score` | ✅ Fonctionne + updateConfidenceScore + rebuildSuivi + writeToHistorique |
| `save_boost` | ✅ Fonctionne + ExosDone dans DailyBoosts + rebuildSuivi |
| `generate_diagnostic` | ✅ Fonctionne — guest (sans code) pour landing flow |
| `generate_daily_boost` | ✅ Fonctionne — filtré sur chapitres diagnostiqués élève |
| `generate_remediation` | ⏸️ Désactivé — return success immédiat |
| `get_progress` | ✅ Fonctionne |
| `detect_fragile_prereqs` | ✅ Fonctionne (onglet Prerequisites archivé → fragile:false) |
| `get_prerequisites` | ✅ Fonctionne |
| `enqueue` | ✅ Fonctionne (onglet Queue archivé → erreur propre) |
| `generate_exam_prep` | ✅ Fonctionne — per-chapter, 10 questions (7 lvl2 + 3 lvl1 non acquis) |
| `generate_brevet` | ✅ DISPONIBLE — multi-chapitres niveau, ~15q style Brevet (UI désactivé — code conservé) |
| `generate_revision` | ✅ DISPONIBLE — révision niveau inférieur sur chapitres faibles (UI désactivé — code conservé) |
| `submit_feedback` | ✅ NOUVEAU — écrit dans onglet Insights (créé auto si absent) |
| `generateMorningReport` | ✅ Fonctionne — génération IA désactivée |
| `get_admin_overview` | ✅ Fonctionne — boostHistory[], source exos, chapitresDetail cap 20 |
| `publish_admin_boost` | ✅ Fonctionne — écrit →Nouveau Boost (col 18), rebuildSuivi |
| `publish_admin_chapter` | ✅ Fonctionne — écrit premier slot →Nouveau Ch libre, rebuildSuivi |
| `check_trial_status` | ✅ Fonctionne — { trialActive, daysLeft, isPremium } |
| `import_chapters` | ✅ One-shot admin — pousse chapitres dans Curriculum_Officiel + DiagnosticExos via GAS |
| `send_test_email` | ✅ Admin — envoie email J+0 test à l'adresse du fondateur (vérifie alias no-reply@matheux.fr) |
| `mark_all_test`   | ✅ Admin one-shot — marque tous les comptes non-admin sans IsTest comme IsTest=1 |

---

## 📋 Structure Google Sheet — état 12 mars

### Onglets Nicolas (bleus)
```
Vue Élèves    ← PRINCIPAL — 1 ligne/élève, ACTION NICOLAS en col A (gelée)
                ⚡ ACTION NICOLAS | Prénom | Niveau | Dernière connexion | Streak 🔥 |
                Chapitres diagnostiqués | Chapitre en cours | Nb exos faits | Score global % |
                Chapitres fragiles 🔴 | Taux réussite semaine |
                📚 Prochain chapitre (Nicolas) | 📧 Rapport envoyé le (Nicolas) | Code (masqué)

Log Exercices ← DÉTAIL — 1 ligne/exercice, récent en haut, énoncé 60 chars
                Date | Prénom | Niveau | Chapitre | Énoncé | Résultat |
                Temps (sec) | Nb indices | Formule ouverte | Mauvaise option

Users         → Code | Prénom | Niveau | Email | PasswordHash | DateInscription | IsAdmin | Premium | TrialStart | PremiumEnd | IsTest
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
_ARCHIVE_Queue / _ARCHIVE_Prerequisites / _ARCHIVE_Rapports / _ARCHIVE_Pending_Exos
```

### Règles ⚡ ACTION NICOLAS (rebuildSuivi — état 11 mars)
| Valeur | Condition | Priorité |
|---|---|---|
| `🔴 BLOQUÉ` | inactif >7j ET score <40 sur tous chapitres | 1 |
| `⚡ BOOST TERMINÉ → préparer le suivant` | ExosDone==5 ET dernier boost < aujourd'hui ET pas de boost pending | 2 |
| `✅ CHAPITRE TERMINÉ → assigner la suite` | Progress NbExos ≥20 ET cols 📝 Nicolas vides | 3 |
| `👍 RAS` | sinon | 4 |

Plusieurs règles simultanées → toutes affichées en pills, couleur card = plus urgente.
`rebuildSuivi(code)` appelé dans `save_score` et `save_boost`.
`writeToHistorique(p)` appelé dans `save_score` — insert en ligne 2 (récent en haut), énoncé réel.

### 👁 Suivi — structure colonnes (GAS : Code en col U = index 20 1-based)
```
A: ⚡ ACTION  B: Prénom  C: Niveau  D: Dernière connexion
E: Chapitre 1  F: Statut 1  G: 📝 Ch1 suite (Nicolas)
H: Chapitre 2  I: Statut 2  J: 📝 Ch2 suite (Nicolas)
K: Chapitre 3  L: Statut 3  M: 📝 Ch3 suite (Nicolas)
N: Chapitre 4  O: Statut 4  P: 📝 Ch4 suite (Nicolas)
Q: Boost consommé?  R: 📝 Prochain boost (Nicolas)
S: 📧 Rapport envoyé / Chap5+  [T: Code masquée]
```
→Nouveau Ch : indices [6,9,12,15] | →Boost : index 18

---

## 🗺️ ROADMAP PAR BLOCS

### BLOC 1 — Socle technique ✅ TERMINÉ
- [x] generate_diagnostic / generate_daily_boost / isFirstDay / boostExistsInDB ✅
- [x] Curriculum_Officiel : 480 exos (24 chap × 20) ✅
- [x] DiagnosticExos : 48 exos (24 chap × 2 lvl) ✅
- [x] Bugs T1→T7 post-tests utilisateur tous corrigés ✅
- [x] BLOC B — UX Progression & Mobile (B1 Constellation supprimée, B2 Progression, B3 fragiles, B4 mobile) ✅

### BLOC 2 — Fiabilité & workflow quotidien ✅ (quasi terminé)
- [x] `generateMorningReport()` + trigger GAS 7h ✅
- [x] `rebuildSuivi(code)` + `writeToHistorique(p)` ✅
- [x] `login()` injecte `nextChapter` + `nextBoostTopic` depuis colonnes Nicolas ✅
- [x] Mode Admin : get_admin_overview + publish_admin_boost + publish_admin_chapter ✅
- [x] Dashboard admin : redirect isAdmin → "Mes Élèves", cartes urgence ✅
- [x] Modal élève : tous les exos, accordion, badge DIAG/BOOST, copyAdminPrompt complet ✅
- [x] Modal admin refondu : DIAG/CH séparés, chapitres triés (terminés>en cours>diag), boost lock (pending/in_progress/done) ✅
- [x] ExosDone dans DailyBoosts col D ✅
- [x] chapLocked sur chapitre actif uniquement + section archivés modal ✅
- [x] Cap 20 exos chapitresDetail + cohérence renderArchiveSection ✅
- [x] Colonne `Premium` + `TrialStart` dans Users ✅
- [x] Essai 7 jours full droits sans carte ✅ (checkTrialStatus, badge J-X, overlay expiry, onboarding 3 slides)
- [x] Messages & encouragements ultra-ado Game Boy Chill ✅ (EASY×7 + HARD×3 + feedbacks partout)
- [x] Flow landing + diagnostic GAS complet ✅ (rSection CALIBRAGE, guest generate_diagnostic, queue 24h, auto-login)
- [x] Landing vendeuse refaite ✅ (hero émotionnel, 4 cartes, témoignages, CTA final)
- [x] CORS fixé : plus de Content-Type header sur les fetch GAS ✅
- [x] LocalStorage : auth uniquement, données toujours depuis GAS ✅
- [x] Backend pills priorité ⚡>✅>🔴>👍 + boostPending + chapTermine ✅
- [x] Bouton "Copier le dernier boost JSON" dans modal admin ✅
- [x] Smart question count : `_pickDiagExos()` — 1ch→4q, 2ch→6q, 3ch→8q, 4+→10q, ≥1/chap ✅
- [x] Fix "Diagnostic - 6ème" après flow guest : calDone=true + S.calState=null avant initApp ✅
- [x] Quiz inline landing step 3 : fond sombre + card blanche, `_flowRenderQuestion()` / `_flowAnswerOpt()` ✅
- [x] Tutorial première question (landing + rSection CALIBRAGE idx===0) ✅
- [x] Step 4 guest adapté dynamiquement : score affiché, sans mot de passe, `_flowActivateStep4Guest()` ✅
- [x] Suppression `_flowLaunchAppDiag()`, `_flowShowGuestRegister()`, `S._guestMode` ✅
- [x] Fix `_onbRender` : `background:` prefix sur `sl.color` (texte blanc sur fond blanc) ✅
- [x] Fix quiz inline CTA : `class="mc rdy"` sur énoncé (opacity:0 → visible immédiatement) ✅
- [x] Onboarding guest cohérent : "Ton boost du jour est prêt !" + "Une chose à faire aujourd'hui" ✅
- [x] boostFromDiag() déclenché en background pendant onboarding guest ✅
- [x] Bypass limite : emails @matheux.fr → IsTest=1 auto, jamais comptés ✅
- [x] Colonne `IsTest` dans Users — 110 comptes existants migrés IsTest=1 via Python ✅
- [x] Limite bêta portée à 50 vrais élèves (IsTest=0, non-admin) ✅
- [x] Dashboard admin : compteur X/50 coloré + section 🧪 Comptes test repliable ✅
- [ ] Créer adresse contact@matheux.fr (hébergeur email + alias Gmail)
- [ ] Validation inputs côté GAS (format email, longueur champs)
- [ ] Rate limiting basique dans doPost

### BLOC 2b — Rapport matin ✅ IMPLÉMENTÉ
Fonction `generateMorningReport()` dans backend.js — trigger 7h quotidien.

| Statut | Critères |
|---|---|
| ✅ ACQUISE | score > 80 + statut='maitrise' + 0 HARD depuis 14j + ≥3 sessions |
| 🔴 BLOQUEE | score < 40 + pas d'amélioration sur 2 semaines + ≥4 sessions |
| 🟡 FRAGILE | score < 40 OU ≥3 HARD cette semaine |
| 📈 EN_PROGRESSION | taux erreur cette semaine < semaine passée (−10 pts) |
| 📘 EN_COURS | défaut |

Email sujet `[Matheux ⚡ ACTION]` si fragiles/bloquées. Stocké dans onglet `Rapports`.

### BLOC 2c — Génération IA automatique ✅ IMPLÉMENTÉ (désactivée en prod)
Flux : `generateMorningReport(5h)` → analyse → `generatePendingExos()` → `Pending_Exos` → fondateur met YES → `processPendingAtLogin()` au login élève.
Onglet `Pending_Exos` : `Code | Prénom | Niveau | Chapitre | Type | ExosJSON | DateGeneree | Validé | DateValidation`

### BLOC 3 — Juridique & paiement 🟢
- [x] Mentions légales (`mentions-legales.html`) — SIRET 837 763 713 00059, données mineurs, CNIL ✅
- [x] CGU (`cgu.html`) — mineurs, essai 7j, résiliation, clause bêta 40 familles ✅
- [x] CGV (`cgv.html`) — 9,99€/mois, droit de rétractation 14j ✅
- [x] Politique confidentialité (`politique-confidentialite.html`) — RGPD renforcé mineurs ✅
- [x] Politique cookies (`politique-cookies.html`) — localStorage + GA4 consentement explicite ✅
- [x] Case consentement parental à l'inscription (auth + landing step 4) ✅
- [x] Footer légal intégré sur landing + app ✅
- [x] Bannière cookies RGPD (consentement avant chargement GA4) ✅
- [x] GA4 conditionnel (chargé seulement après consentement, IP anonymisée) ✅ — Measurement ID **G-7R2DW4585Y** intégré
- [x] Limite bêta 40 familles dans register() GAS → Waitlist sheet ✅
- [x] Email bienvenue J+0 automatique au register() ✅
- [x] Page premium.html — offre + lien email contact@matheux.fr ✅
- [x] Overlay trial → lien Stripe direct `https://buy.stripe.com/test_14AdRacgw76N7vQcxqa3u00` ✅ (`__trialProlonger()` — bouton "9,99 €/mois")
- [x] Email J+7 → lien Stripe direct ✅
- [x] Emails envoyés depuis `no-reply@matheux.fr` via GmailApp ✅
- [ ] Webhook Stripe → colonne `Premium` dans Users

### BLOC 4 — Marketing & conversion 🟢
- [x] Email bienvenue J+0 déclenché au register() (voir BLOC 3) ✅
- [ ] Activer triggerDailyMarketing : Apps Script UI → Déclencheurs → Chaque jour 9h-10h
- [ ] Séquence J+3, J+7 activée via triggerDailyMarketing (code complet — activer trigger)
- [ ] Témoignages vrais élèves sur la landing
- [x] Page pricing comparative (cours particulier vs Matheux vs autres applis) ✅
- [x] Section fondateur Nicolas sur landing ✅
- [x] Carousel testimonials mobile snap-scroll ✅

### BLOC 5 — Automatisation & scale 🔵
- [x] clasp push automatique (`./watch_deploy.sh`) ✅
- [ ] Agent analyse lacunes quotidien automatique
- [ ] Agent génération boost automatique
- [ ] Agent rapport parents (email hebdo)
- [x] Mode "Préparation Brevet" (GAS generate_brevet + code conservé, **UI désactivé demande Nicolas**) ✅
- [x] Mode Révision niveau inférieur (GAS generate_revision + code conservé, **UI désactivé demande Nicolas**) ✅
- [x] Système feedback élève (submit_feedback GAS + modal + onglet Insights) ✅
- [x] 5 chapitres prioritaires poussés en prod (Probabilités 3EME, Racines carrées 3EME, Nombres décimaux 6EME, Fonctions linéaires 4EME, Statistiques 6EME) ✅
- [ ] Migration Sheets → vraie BDD si >50 users simultanés

---

## ✅ Ce qui fonctionne bien (ne pas toucher sans raison)
- CSS/UI complet, mobile-first, animations propres (pulseGentle, toastIn, popIn)
- Landing page vendeuse : hero émotionnel, 4 cartes, témoignages, CTA sans carte + pricing comparaison + Nicolas fondateur
- Mode Brevet : GAS generate_brevet multi-chapitres — **code complet conservé, UI désactivé (tab masqué, loadBrevet() bloqué)**
- Mode Révision : GAS generate_revision (niveau inférieur, chapitres faibles) — **code complet conservé, UI désactivé (card masquée, launchRevision() bloqué)**
- Feedback non-intrusif : bouton "Signaler" post-réponse + modal 3 types + GAS submit_feedback → onglet Insights
- Auth register + login + auto-login silencieux
- Scores enrichis : temps, wrongOpt, indices, formule (v23)
- Swipe gauche → exercice suivant
- Admin panel triple-clic logo → redirect auto isAdmin
- Gamification : XP / streak / mastery ring SVG
- MathJax v3 avec fallback 2.5s + overflow-x-auto
- Chrono par exercice `exoStartTime` + `_timerPaused` (visibilitychange/blur/focus)
- Nudge pills après 20s d'inactivité
- Tableau blanc bottom sheet avec symboles maths
- Vue Progression : barre confiance, dates relatives, badge Maîtrisé
- Bannière prérequis fragiles (ambre) avant exercices, mis en cache par session
- Auto-indices sur erreur : `autoShowHelp()` injecte HTML direct (pas de typewriter)
- Badges niveau colorés + compteur animé dans `rSection()`
- Essai 7j : badge J-X, overlay bloquant, onboarding 3 slides
- Flow landing CTA : niveau → chapitres → quiz inline step 3 → form step 4 → switch app → onboarding → chapitres
- `_pickDiagExos(exos, chapCount)` : smart count (1ch→4q … 4+→10q), ≥1 par chapitre
- `_flowRenderQuestion(idx)` : renderer MCQ inline (card blanche sur fond sombre landing), tutorial Q0
- `_flowActivateStep4Guest()` : adapte step 4 dynamiquement (score, sans MDP) → `_flowGuestRegister()`
- `rSection('CALIBRAGE', ...)` : banner tutorial sur idx===0 (app normale)
- Messages ton ado : EASY×7 HARD×3 + abandon/chapitre/boost/nudge/MotProf
- Modal admin : DIAG/CH séparés, chapitres triés, boost lock intelligent, copyBoostJSON
- `relDate`/`relDateAdmin` robuste : formats FR/ISO/timestamp, plafond "2 ans"

---

## ⚠️ Contraintes techniques
- Google Sheets : fragile à ~20 users simultanés, quota Apps Script 6min/call
- Données de mineurs : RGPD renforcé, consentement parental obligatoire
- Hash MDP côté client uniquement → pas de salt côté serveur (acceptable MVP)
- Pas de réécriture complète — patches chirurgicaux seulement
- CORS GAS : ne jamais ajouter `Content-Type` header sur les fetch (mode no-cors)
- `source='boost'` dans chapitresDetail toujours `'chapter'` côté GAS → matching par position (index 0-4)
- Guest flow CTA : mot de passe auto-généré `Matheux2026!` (hash SHA-256) — non communiqué à l'user
- `_flowGuestRegister()` lit `#fl-name` / `#fl-email` (step 4 landing), pas de champ password

## 💰 Modèle économique
- Freemium 7 jours → 9,99€/mois
- Cible : 50 clients = ~500€ MRR
- Paiement : Stripe simple

---

## 📁 docs/ — Fichiers clés
| Fichier | Contenu |
|---|---|
| `rapport-condense-2026-03-12.md` | **RÉFÉRENCE UNIQUE** — état complet au 12 mars, remplace tous les anciens rapports |
| `notice-utilisation.md` | Guide complet site pour Nicolas (élèves, Sheet, admin, tech) — Version 12 mars |
| `programme-français-verif.md` | Couverture Eduscol ~85% avec +5 chap., 12 notions manquantes identifiées |
| `audit_complet.md` | Audit test_complet.py 89/93 (96%) |
| `juridique-checklist.md` | RGPD mineurs, templates légaux, case consentement HTML+JS |
| `landing-page-brief.md` | Brief landing 9 sections + copywriting |
| `marketing-phase1.md` | 3 phases : WhatsApp, LinkedIn, parrainage, Google Ads |
| `emails-sequences.md` | 6 séquences email + implémentation GAS (opt-out RGPD) |
| `tracking-analytics.md` | GA4 RGPD-compat., 8 événements JS, formules Sheet |

### Python scripts (algebra/)
```python
from algebra.sheets import sh
sh.read("Curriculum_Officiel")       # lit le Sheet live
sh.write_rows("DiagnosticExos", rows)
sh.append_row("Scores", [...])
```
- `rebuild_sheet.py` : reconstruit 👁 Suivi et 📋 Historique depuis données réelles — règles ACTION synchronisées avec GAS
- `audit_formats.py` : audit conformité exercices Curriculum_Officiel + DiagnosticExos
- `push_new_chapters.py` : push 5 nouveaux chapitres (Probabilités 3EME, Racines carrées 3EME, Nombres décimaux 6EME, Fonctions linéaires 4EME, Statistiques 6EME) → données dans `new_chapters_2026-03-12.json` → copier vers `/tmp/exos_data.json` avant de lancer
- `test_workflows.py` : 38 tests GAS (groupes A+B), 37/38 PASS après deploy @31

## ⚠️ Actions manuelles requises (13 mars 2026)
- ✅ GAS @34 déployé (verifyAdmin fix + import_chapters)
- ✅ 5 chapitres poussés en prod via `push_via_gas.py`
- **⚡ GAS @35 à déployer** : `bash deploy.sh "waitlist + email J0"` — contient waitlist 40 fam. + email bienvenue J+0
- ✅ **GA4** : `G-7R2DW4585Y` intégré dans index.html — GA4 actif après consentement cookies
- ✅ **Stripe** : lien `https://buy.stripe.com/test_14AdRacgw76N7vQcxqa3u00` dans overlay trial + email J+7
- **⚡ Stripe** : quand le lien PROD est prêt, remplacer `test_14AdRacgw76N7vQcxqa3u00` dans index.html + backend.js + cgv.html (3 occurrences)
- Apps Script UI → Déclencheurs → ajouter `triggerDailyMarketing` → Chaque jour 9h-10h (séquences J+3 / J+7)
- `python3 audit_formats.py` — à lancer pour vérifier conformité des 5 nouveaux chapitres

---

## 📅 Historique sessions — condensé

| Date | GAS | Résumé | Commits clés |
|---|---|---|---|
| 9 mars | @5 | DiagnosticExos refaits, 20 profils test créés, bugs T1-T7, test flux complet | — |
| 9→10 mars nuit | @8 | Prompt génération refondu, algo sélection exos, docs/ 8 fichiers | 2f0d345 aaa8b2c d69c108 68b18a3 dbbf0a2 |
| 10 mars matin | @10 | login() nettoyé, generateDailyBoost bug hors-scope corrigé, 4 onglets archivés | — |
| 10 mars soir | @15 | rebuildSuivi(), writeToHistorique(), rebuild_sheet.py, structure 👁 Suivi 20 cols | — |
| 10 mars nuit | @13 | Audit 95% test_complet.py, 4 bugs UX (boostConsumed, relDate, renderChapComplete) | d6aae86 025cbb9 |
| 11 mars nuit | @19 | Landing SEO+trial inline, messages ado, test_scenarios.py 6/6, email J+3/J+7, bug date boostExistsInDB fixé | — |
| 11 mars matin | @22 | Admin dashboard refondu, ExosDone DailyBoosts, rebuildSuivi règles revues, modal élève enrichi, données 20 scénarios | 6db9e7c 5bc72e5 |
| 11 mars après-midi | @28 | Fix chapLocked actif uniquement, section archivés modal, cap 20 exos chapitresDetail, essai 7j complet | ab58d6d 72d200d |
| 11 mars soir | @30 | CORS fix, landing CALIBRAGE+flow guest, admin modal DIAG/CH, pills prioritaires, landing vendeuse, essai 7j onboarding | 80a247f 50c7bdb 0da6a26 a2ee071 4e1a30e 6564c30 ab58d6d 72d200d a66879c 61b2924 f917a29 7e63b0f 372ac76 d7be47f |
| 12 mars | @24→23 | Git reconstruit (12a61e7), UX admin/élève, boostJSON copie, rebuild_sheet.py synchronisé, fix auto-login, boostConsumed | 12a61e7 c22f471 2a808d3 9421ef6 b96f9d8 |
| 12 mars (soir) | @30 | Smart question count, fix Diagnostic-6ème guest, onboarding adapté, boost auto guest | 9524e3a ac046e4 |
| 12 mars (nuit) | @30 | Quiz inline landing (step 3 card blanche), tutorial Q1, fix onbRender bg, cohérence messages | 544a112 |
| 12 mars (nuit 2) | @30 | Simulation 20 profils/5j, messages parent/ado refondus, BLOC 3 juridique complet (5 pages + footer + consentement) | — |
| 13 mars | @31 | BLOCS 4-5 : landing pricing+fondateur+carousel, programme-français-verif.md (66% couv.), audit_formats.py, Mode Brevet (GAS+UI 3 screens), Mode Révision (GAS+card), Feedback (modal+Insights tab), 7 bugs fixes (showT/SHEET_ID/Array.find/chkComp/togCat/res2/sendScore), test_workflows.py 37/38 PASS (97%) | — |
| 12 mars 2026 | @34 | Désactivation UI Brevet+Révision (code conservé), 5 chapitres poussés en prod (100 exos), verifyAdmin fix (TRUE/1), rapport condensé, notice refaite, programme ~85% | — |
| 13 mars 2026 | @35 | BLOC 3 🟢 complet : waitlist 40 fam. GAS, email J+0 auto, GA4 consentement, bannière cookies RGPD, premium.html, trial→premium.html, CGU clause bêta, politique-cookies GA4 | — |
| 13 mars 2026 | @36 | GA4 G-7R2DW4585Y intégré, overlay trial → Stripe direct 9,99€/mois, email J+7 → Stripe, GmailApp from no-reply@matheux.fr, GA4 ID dans politique-cookies.html | — |
| 13 mars 2026 | @37 | Dashboard admin : bloc "Outils Fondateur" en haut (Stripe TEST badge + btn, Email test via send_test_email GAS) | — |
| 13 mars 2026 | @38 | Fix quiz CTA invisible (mc rdy), bypass 40-fam pour @matheux.fr, note contact@matheux.fr dans dashboard | — |
| 13 mars 2026 | @39 | Colonne IsTest Users, limite 50 vrais élèves, dashboard compteur X/50 + section test repliable, mark_all_test GAS, migration Python (110 comptes → IsTest=1) | — |
| 13 mars 2026 | @40 | UX post-boost : confettis + auto-redirect chapitres 5s + boost card "Prochain dispo demain 🔥" ; Hints/Formule : contraste amber-800 + fond coloré (pill + autoShowHelp + showHintInline + revFInline) ; Admin BOOST TERMINÉ : fix condition (today inclus) ; Admin modal : indicateurs email J0/J3/J7 (trialStart GAS) | — |
| 13 mars 2026 | @41 | Fix admin : actionPriority + actions mis à jour localement après publishBoost/publishChapter (compteur instantané) ; rebuildSuivi : suppression `lastBoostDate < todayStr` (cohérence avec getAdminOverview) ; login() : crée DailyBoosts exosDone=0 à la livraison du boost → admin voit ⏳ En attente au lieu de faux BOOST TERMINÉ | — |

---

## 🚦 Règle d'or chaque session
1. Lire CLAUDE.md
2. Identifier le BLOC actif et les priorités du jour
3. Travailler uniquement dans ce périmètre
4. Tester sur mobile avant commit
5. Mettre à jour les checkboxes ici en fin de session
