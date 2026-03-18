# Roadmap — Matheux

> Priorités de développement par blocs. Voir aussi [CLAUDE.md](../CLAUDE.md) pour les règles et [product.md](product.md) pour le produit.

---

## État global — 17 mars 2026

**Matheux 100% prêt. Tests élève 5/5 ✅. Test parent ✅. 27 frictions fixées + cartes premium + messages perso. Landing GOD MODE déployée. GitHub privé (MatheuxApp).**
**Reste : endpoint webhook Stripe + tests admin. "Valider la réponse" ✅. "Je ne sais pas" ✅. Lancement confirmé : mercredi 18 mars 2026 à 9h.**

> ✅ **Bugfixes @60** — BUG-01 à BUG-12 corrigés (simulation 7j × 5 profils). 13 mars.
> ✅ **Simulation 40 élèves @63** — 6 bugs corrigés + 1616 appels API, 0 erreur. 14 mars.
> ✅ **1ERE Spé Maths @64** — 10 chapitres, 330 exercices, compte Auguste. 14 mars.
> ✅ **Admin panel @69-@76** — email modal, cockpit 3 onglets, log_contact, 6 profils test. 15 mars.
> ✅ **Messages _msg() @74** — adaptatif niveau, coach marks, emails personnalisés objectif. 15 mars.
> ✅ **Audit pédagogique @77** — 1872 exos, score ~98%, UX mode nuit, nav boost. 15 mars.
> ✅ **Simulation 21j @79-@80** — 12 profils SIM01-SIM12, 4 bugs corrigés, 0 erreur. 15 mars.
> ✅ **Bouton "J'ai pas compris" + profil cognitif @81** — incompréhensions déclarées + profil admin. 15 mars.
> ✅ **Page teasing pré-lancement @82** — countdown, waitlist email, accès bêta, auto-switch mercredi 9h. 16 mars.

| Dimension | État |
|---|---|
| Tests automatisés | **74/74 (100%)** + simulation 40 élèves **17/17 PASS** (1616 appels API, 0 erreur) |
| Couverture programme | **~100%** — 54 chapitres (1080 exos curriculum + 108 diag + 540 boost + 144 brevet) — tous audités ✅ |
| Niveau 1ERE Spé | **10 chapitres expérimentaux** — backend prêt, frontend non modifié (connexion uniquement), 3 types SVG dédiés |
| Juridique | Complet (5 pages + consentement parental + RGPD + TVA art. 293 B CGI) |
| Paiement | ✅ Lien Stripe PROD actif (19,99/mois) |
| Emails auto | ✅ J+0 auto (inscription) + reset MDP auto — J+3/J+5/J+7 et rapport parent = **manuels via admin** (automatisation prévue dès 10-20 clients) |
| Analytics | ✅ GA4 RGPD-compliant |
| Limite bêta | 50 vrais élèves (IsTest=0) |
| Messages élèves | ✅ Système adaptatif `_msg()` — ~35 entrées, niveau, objectif, coach marks, _OK/_KO contextuels |
| Admin cockpit | ✅ GAS @88 — cockpit 5 onglets À FAIRE/FAIT/MAILS/INACTIFS/RAPPORT, boost+chapitre uniquement dans À FAIRE, boutons "Copier JSON complet" (exos+résultats+temps+indices+formule), profils test visibles, fix publish chapitre+JSON parse. 17 mars |
| Exercices | ✅ Audit final 17 mars — 1728 exos vérifiés (3 onglets), 2 LaTeX fixés (1ERE/Second_Degre), 3 faux positifs calcul confirmés OK. Score 98,3%. 24 doublons 1ERE non bloquants. **0 bloquant.** |
| UX élève | ✅ @77 — mode nuit app, guide boost, titres gras, nav boost reopen |
| Profil cognitif | ✅ @81 — bouton "j'ai pas compris" + profil cognitif dans fiche admin |
| Page teasing | ✅ @82 — countdown live, waitlist email (Teasing_Early), auto-switch 18 mars 9h, `?noteasing` pour dev |
| Sécurité Stripe | ✅ @84-@85 — webhook handler (Premium auto) + premium guard client (vérif 5 min) |
| Simulation 21j | ✅ @80 — 12 profils, 890 scores, 84 boosts, 0 erreur |
| Emails (@matheux.fr) | ✅ contact@ + no-reply@ + nicolas@ créés (Ionos) — alias Gmail no-reply@ branché ✅ — formulaire contact ✅ — centralisation 3 boîtes jeudi 19 |

---

## Semaine du lancement — 16-18 mars 2026

### Lundi 16 mars (Nicolas) ✅
- [x] Créer contact@matheux.fr (Ionos) ✅
- [x] Créer no-reply@matheux.fr (Ionos) ✅
- [x] Alias no-reply@matheux.fr dans Gmail (SMTP Ionos port 465 SSL) ✅
- [x] Fix backend : `from: 'no-reply@matheux.fr'` sur rapport parent ✅
- [x] Action GAS `send_contact` + formulaire contact (3 footers) ✅
- [x] Merge sécurité freelance SECUmain → main (Stripe MAXIMAL PARANOID + Premium Guard) ✅
- [x] GitHub Pages reconfiguré sur main ✅
- [x] Tests emails : J+0 ✅ / Reset MDP ✅ / Contact ✅ / Pas de triggers ✅
- [x] Stripe : CGV + confidentialité + TVA décochée + limite 50 paiements ✅
- [x] Bandeau rappel limite Stripe dans admin dashboard ✅
- [x] Nettoyage base : SIM01-SIM12 + anciens profils supprimés, gardé admin+Auguste+Charlie ✅
- [x] Test élève : 6EME ✅ / 5EME ✅ / 4EME ✅ — 15 frictions notées (3EME à finir dans le bus)

### Mardi 17 mars matin (Nicolas) ✅
- [x] **Test élève 3EME** ✅ — remarques intégrées
- [x] 🔧 **Fix 27 frictions élève** ✅ — mode nuit, exo 1 bloqué, bienvenue, retro, bon retour, boost demain, lune, IA retiré, signaler erreur, onboarding responsive, cartes premium, tri intelligent, messages perso, cohérence onboarding, bouton retour trial flow
- [x] **Test parent parcours complet** ✅ — landing → diag → inscription → onboarding → boost → mail J+0 → admin
- [x] **Refonte landing teasing + prod GOD MODE** ✅ — 11 sections restructurées, section Problème, contraste 10min/jour, fondateur court/humain, pricing pills engagement
- [x] **Checklist fix final** ✅ — min 2 chapitres diag, bandeau boost cohérent, polish UI
- [x] **GitHub → MatheuxApp** ✅ — repo privé, Enterprise trial 30j, Pages OK
- [x] **Relecture exos quizz** ✅ — remarques diag 3EME/5EME (triangles, formules, LaTeX)
- [x] **Audit diag+boost géo** ✅ — 168 exos, 93 figures SVG à ajouter, 16 reformulations

### Mardi 17 mars après-midi (Nicolas + Claude)
- [x] 🔬 **Fix diagnostic + Boost J1** ✅ — 251 figures SVG ajoutées (Thalès/Trigo/Sections/Pythagore/Périmètres/Volumes/Homothétie), 14 reformulations ciblées (Thalès contextualisé, Trigo angle précisé, Sym Axiale vocabulaire, Sections "depuis sommet"), espaces LaTeX fixés, doublon Systèmes corrigé
- [x] ✅ **Implémenter "Valider la réponse"** — selectOpt+validateAnswer, .os (selected), .validate-wrap sticky, .btn-validate disabled→enabled, mode nuit, reset goEx/togCat
- [x] ✅ **Implémenter "Je ne sais pas"** — bouton .opt-skip, resultat='SKIP' (traité comme HARD), supprimé ancien lien + log_pas_compris. 17 mars.
- [x] 🖥️ **Refonte admin cockpit** ✅ — 5 onglets (À FAIRE/FAIT/MAILS/INACTIFS/RAPPORT), À FAIRE = boost+chapitre uniquement, boutons "Copier JSON complet" (exos+résultats élève), onglet MAILS séparé, onglet INACTIFS (>3j), onglet RAPPORT dimanche. 17 mars.
- [x] 🔧 **Fix admin @88** ✅ — profils test visibles dans À FAIRE (filtre isTest retiré), bouton Publier chapitre (ID mismatch), JSON parse "bad control character" (fallback nettoyage), 3 profils test créés (Léa 6E, Maxime 4E, Sofia 3E). 17 mars.
- [x] 🔬 **Audit final exercices** ✅ — 1728 exos, 3 scripts + 7 vérifs manuelles (indices, figures, LaTeX, options, niveau, notation, doublons). 2 LaTeX cassés fixés (1ERE/Second_Degre "Non factorisable $"). 3 erreurs calcul = faux positifs. 24 doublons 1ERE = non bloquant. **Score 98,3% — 0 bloquant — GO PROD.** 17 mars.
- [ ] 🎮 Test admin workflow en conditions → fix frictions
- [ ] 🧪 Test réouverture user (Auguste, Charlie, Nicolas)
- [x] 🔍 **Audit pré-lancement complet** ✅ — 24 points identifiés (3 bloquants, 3 critiques, 7 importants, 8 frictions UX, 3 cohérence). Voir `docs/checklist-lancement.md` §5b. 17 mars.

### Jeudi 19 mars — J+1 SUIVI + STRATÉGIE

**Matin**
- [ ] 09:00 👀 Admin cockpit — inscrits + boosts + emails
- [ ] 09:35 📧 Centraliser 3 mails matheux.fr
- [ ] 10:10 📊 Stratégie marketing — cible + canal + message
- [ ] 10:45 🤖 Réflexion automatisation (boosts, relances, agents)
- [ ] 11:20 💼 Post LinkedIn lancement

**Après-midi**
- [ ] 14:15 📞 Relances + nouveaux contacts (one-to-one)
- [ ] 14:50 🏫 Contact établissements + profs influenceurs
- [ ] 15:25 👀 Surveiller réponses + GA4
- [ ] 16:00 🏁 Bilan jour 2

### Vendredi 20 mars — J+2 PRODUIT + CONTENU

**Matin**
- [ ] 09:30 👀 Admin cockpit matin
- [ ] 10:05 🎬 Tuto onboarding élève (vidéo ou guide visuel)
- [ ] 10:35 📱 Vérif PWA mobile (install + offline + icône)
- [ ] 11:10 📧 Test rapport parent hebdo (trigger manuel + relecture)

**Après-midi**
- [x] 12:00 🎯 ~~Système de points~~ ✅ Fait @90 (XP + milestones + paliers)
- [ ] 12:35 🔐 Double confirmation mot de passe (dev)
- [ ] 13:10 ✉️ Template email inscription
- [ ] 13:45 ✉️ Template email rapport parent
- [x] 14:20 🔤 ~~Cohérence messages~~ ✅ Fait @90 (boost→entraînement, chap_done corrigé, mode nuit)

### Mercredi 18 mars — JOUR J LANCEMENT

**Matin — Audit fixes + tests + go live**
- [x] 09:00 ⛔ Fix 18 bloquants audit pré-lancement ✅ @89
- [x] 09:15 🔴 Fix triggerDailyMarketing Premium='1' string ✅ @89
- [ ] 09:25 🎮 Test admin workflow (simuler un matin d'admin)
- [ ] 09:55 🧪 Test réouverture user (Auguste, Charlie, Nicolas)
- [ ] 10:20 🔧 Fix frictions test (admin + user)
- [ ] 10:45 💳 Test paiement CB Stripe (19,99€ → vérif Premium → rembourser)
- [ ] 11:15 ✉️ Rédiger messages parents
- [ ] 11:30 🔐 Décision webhook Stripe HMAC-SHA256 (avant ou après J+7)
- [x] ⚡ **Gamification MVP** ✅ @90 — XP visible + animation +XP, paliers maîtrise (6 niveaux), streak freeze 1j/semaine, milestones (6 événements célébrés), card "Session terminée", temps estimé hero, onglet Progression débloqué, mastery ring enrichi, passe cohérence messages, mode nuit couvert
- [x] 📋 **Tuto régressif** ✅ @91 — 8 micro-tips contextuels first-use (sélection, erreur, indices, formule, brouillon, skip, XP, pills) — disparaissent après 1 affichage

**Après-midi — GO LIVE + diffusion**
- [ ] 14:00 🚀 GO LIVE — TEASING_MODE = false + push
- [ ] 14:15 🎥 Vidéo fondateur + intégration landing
- [ ] 14:50 📱 Diffusion cercle proche (SMS, WhatsApp, messages perso)
- [ ] 15:25 📱 Diffusion réseaux (LinkedIn, Facebook, waitlist)
- [ ] 16:00 🏫 Contact établissements + micro-influenceurs
- [ ] 16:35 👀 Surveiller inscriptions + GA4 + répondre
- [ ] 17:10 🏁 Bilan jour 1

---

## Actions manuelles — à faire par Nicolas (bloquantes prod)

| # | Action | Où | Priorité |
|---|---|---|---|
| 1 | ~~**Stripe TEST → PROD**~~ — ✅ Fait @82 (16 mars 2026) — lien PROD `cNicN7b0ebU9bOE9WTb3q01` | ✅ | 🟢 |
| 2 | ~~**Créer `contact@matheux.fr`**~~ ✅ + ~~**alias `no-reply@matheux.fr`**~~ ✅ (SMTP Ionos port 465 SSL) | ✅ | 🟢 |
| 3 | **Automatiser trigger `triggerDailyMarketing`** → dès 10 clients actifs (manuel via admin en attendant) | Google Apps Script UI | 🟡 |
| 4 | **Webhook Stripe → colonne `Premium`** — code déployé @85, Payment Link configuré (CGV + confidentialité + limite 50 + TVA off), **endpoint Stripe à finaliser**. ⚠️ **Audit 17 mars** : aucune vérif HMAC-SHA256 Stripe, `SHARED_SECRET` en clair dans backend.js L5404 → à sécuriser avant J+7 | Stripe dashboard → Webhooks → créer destination | 🔴 |
| 5 | Vrais témoignages élèves/parents sur landing | À collecter après premiers clients | 🔵 |
| 6 | **Migration serveur + backend** — envisager après ~10 clients : remplacer GAS+Sheets par serveur dédié (Node/Python) + BDD (Postgres/Supabase). Limite GAS : 20 users simultanés, 6 min/appel, pas de cron fiable. Mode Brevet à déployer proprement après migration. | Architecture | 🟡 |
| 6 | **Design overhaul landing** — ~~@68 (14 mars)~~ → **Refonte GOD MODE @86 (17 mars)** : 11 sections, section Problème, contraste 10min/jour, fondateur humain, pills engagement | ✅ Fait @86 | 🟢 |
| 7 | **Vidéo fondateur** — tourner courte vidéo Nicolas pour section "Derrière Matheux" landing | 18 mars (lancement) | 🟡 |
| 8 | **Cohérence messages** — vérifier wording génériques/circonstanciels après refonte landing | Vendredi 20 mars (1h) | 🟡 |
| 9 | **UX sans boost** — ajouter bandeau "ton boost arrive bientôt" si aucun boost généré (actuellement : rien ne s'affiche, pas d'erreur). Nicolas génère manuellement en attendant. | Frontend index.html | 🟡 |

## Priorités code — prochaines sessions

| # | Action | Statut | Priorité |
|---|---|---|---|
| 0 | **Fixes bugs audit** (BUG-01 à BUG-12 dans [test_debug.md](test_debug.md)) | ✅ Corrigés @60 | 🟢 |
| 1 | Validation inputs GAS (format email, longueur champs) | ✅ Corrigé @63 (register + saveScore) | 🟢 |
| 2 | Rate limiting global dans doPost (60/min, 15/min sensibles) | ✅ Corrigé @63 | 🟢 |
| 3 | **BUG-AUDIT-01** : `Systèmes_Équations 3EME exo#16` — réponse corrigée | ✅ Corrigé (déjà en prod) | 🟢 |
| 4 | **BUG-AUDIT-02/03** : Boost `Transformations 5EME` + `Homothétie 4EME` — tiret unicode | ✅ Corrigé (déjà en prod) | 🟢 |
| 5 | **BUG-AUDIT-04** : 5 doublons Boost/Curriculum collège | ✅ Corrigé (déjà en prod) | 🟢 |
| 11 | **Doublons 1ERE** : 24 doublons Diag/Boost/Curriculum dans chapitres 1ERE — non bloquant, élève voit même exo 2× | ❌ À faire (post-lancement) | 🟡 |
| 10 | **BUG-1ERE-JSON** : `a ∉ options` dans `insert_1ere.py` — réponses marquées fausses même si correctes (Dérivation + 5 autres chapitres) | ✅ Corrigé 14 mars — assert guard ajouté dans `_exo()` | 🟢 |
| 6 | **BUG-AUDIT-05** : BrevetExos convertis au format standard `{lvl, q, a, options, f, steps}` + 3 doublons fusionnés (18→15 chap) | ✅ Corrigé 14 mars | 🟢 |
| 7 | **Figures géo SVG** : lettres dynamiques depuis l'énoncé, filtrage nonGeoChaps, 3 nouveaux types 1ERE (vectors, repere, trigo_circle), cercle diamètre, angle 3 lettres, symétries 3 paires | ✅ Corrigé @65 | 🟢 |
| 8 | **Auth modal CTA** : showAuth() gardé contre interruption trial-flow + auto-login silencieux | ✅ Corrigé @65 | 🟢 |
| 9 | **Toast mobile** : white-space normal + max-width 88vw + word-break pour wrap multi-ligne | ✅ Corrigé @65 | 🟢 |

### Améliorations exercices — sprints suivants

> Détail complet dans l'archive docs/archive/ — Score global 4,0/5 → 4,5/5 après corrections.

| Priorité | Action | Chapitres concernés | Volume |
|---|---|---|---|
| 1 | **AMÉLIO-01** : Réécrire indices révélateurs (guidants sans dévoiler) | Homothétie 4EME (17), Agrandissement_Réduction 6EME (15), Conversions_Unités 6EME (15), Racines_Carrées 5EME (10), Triangles_Semblables 5EME (10), Fonctions 3EME (12), Inéquations 3EME (8) | ~103 exos |
| 2 | **AMÉLIO-02** : Ajouter 3ème indice aux exos à 1 seul indice | Fonctions 3EME, Puissances 5EME, Calcul_Littéral 5EME | ~20 exos |
| 3 | **AMÉLIO-03** : Contextualisation (passer de 2 % à 20 % d'exos en situation réelle) | Priorité 5EME + 3EME | long terme |

---

## BLOC 1 — Socle technique ✅ TERMINÉ

- [x] generate_diagnostic / generate_daily_boost / isFirstDay / boostExistsInDB
- [x] Curriculum_Officiel : 1080 exos (54 chap × 20) — programme collège 100% + 1ERE Spé (Sprint 1→4 + @64)
- [x] DiagnosticExos : 108 exos (54 chap × 2)
- [x] BoostExos : 540 exos (54 chap × 10)
- [x] BrevetExos : 144 exos (15 chap × 8-16) — format standard, 3 doublons fusionnés
- [x] CHAPS_BY_LEVEL : 54 chapitres exposés (44 collège + 10 1ERE Spé) dans sélecteur diagnostic
- [x] Bugs T1→T7 post-tests utilisateur tous corrigés
- [x] UX Progression & Mobile (Progression, fragiles, mobile)
- [x] Harmonisation `_doLoginAndLaunch` / `_flowGuestRegister` — fix onboarding fantôme + double diagnostic (13 mars)

---

## BLOC 2 — Fiabilité & workflow quotidien ✅ TERMINÉ

- [x] `generateMorningReport()` + trigger GAS 7h
- [x] `rebuildSuivi(code)` + `writeToHistorique(p)`
- [x] `login()` injecte `nextChapter` + `nextBoostTopic` depuis colonnes Nicolas
- [x] Mode Admin : get_admin_overview + publish_admin_boost + publish_admin_chapter
- [x] Dashboard admin : redirect isAdmin → "Mes Élèves", cartes urgence
- [x] Modal élève : tous les exos, accordion, badge DIAG/BOOST, copyAdminPrompt
- [x] Modal admin refondu : DIAG/CH séparés, chapitres triés, boost lock
- [x] ExosDone dans DailyBoosts col D
- [x] Colonne `Premium` + `TrialStart` dans Users
- [x] Essai 7 jours full droits sans carte
- [x] Messages & encouragements ton ado Game Boy Chill
- [x] Flow landing + diagnostic GAS complet (guest, quiz inline, onboarding)
- [x] CORS fixé
- [x] LocalStorage : auth uniquement, données toujours depuis GAS
- [x] Smart question count diagnostic
- [x] Colonne IsTest + limite 50 vrais élèves
- [x] UX post-boost : confettis + auto-redirect 5s
- [x] Fix admin : actions mises à jour instantanément
- [x] Fix mot du prof affiché élève au login (S._motProfScreen @56)
- [x] Fix aperçu boost admin structuré (motProf + insight + questions, col S avant login élève)
- [x] Mail de bienvenue manuel : bouton "Copier" + "Marquer comme envoyé" dans modal élève si J0 absent (`log_manual_email` GAS, indicateur J0 temps réel depuis onglet Emails)
- [x] Admin smart @59 : catégories capitale/secondaire/ras, onglet "📧 Suivi", emailsDue J+3/J+5/J+7, copie + marquage depuis modal
- [x] **Email modal éditable** — mini-modal overlay avec objet + corps éditables avant copie, bouton marquer envoyé post-copie (15 mars 2026)
- [x] **Templates email marketing v2** — J+0/J+3/J+7 réécrits ton prof humain, comparaison prix 66ct/jour (15 mars 2026)
- [x] **BLOQUÉ → Sans nouvelles** — renommage `🔴 BLOQUÉ` → `💤 Sans nouvelles` backend + frontend (15 mars 2026)
- [x] **coursNeeded dans getAdminOverview** — détection cours manquants par milestone, card cyan "Cours à compléter" dans fiche admin, message élève "cours en préparation" si section non rédigée (15 mars 2026)
- [x] **Dark mode → onboarding uniquement** — toggle déplacé de la landing vers les slides onboarding (15 mars 2026)
- [x] **Profils test diversifiés** — `scripts/setup_test_profiles.py`, 6 comptes test (J+0/J+3/J+5/J+7/cours/inactif) créés automatiquement (15 mars 2026)
- [x] Messages élèves : streak break alert, boost en cours nudge, chapitre maîtrisé, milestones streak 3j/7j
- [x] Email J+5 "Encore 2 jours" dans séquence marketing
- [x] **Message architecture system** — `_msg()` adaptatif niveau (6EME/3EME/def), coach marks (indice/boost/brouillon), _OK/_KO contextuels, onboarding slide 3 selon objectif, emails J+3/J+5/J+7 personnalisés objectif, rapport parent hebdo (15 mars 2026, @74)
- [x] **Checklist quotidienne admin** — onglet 📋 Aujourd'hui, items par priorité (boost/chapitre/emails/parent/brevet/inactifs), coches manuelles + auto-coches publishBoost/publishChapter, rapport hebdo manuel dimanche, fix logManualEmail statut (15 mars 2026, @75)
- [x] Validation inputs côté GAS (format email, longueur) — @63
- [x] Rate limiting global dans doPost — @63
- [x] **BUG-01→12** — bugfixes audit corrigés @60 (13 mars)

### BLOC 2b — Rapport matin ✅
`generateMorningReport()` + trigger 7h quotidien.

### BLOC 2c — Génération IA automatique ✅ (désactivée en prod)
`generateMorningReport` → analyse → `generatePendingExos` → `Pending_Exos` → validation → `processPendingAtLogin`.

---

## BLOC 3 — Juridique & paiement 🟢

- [x] 5 pages légales (mentions, CGU, CGV, confidentialité, cookies)
- [x] Consentement parental + footer légal
- [x] GA4 RGPD-compliant (bannière consentement, IP anonymisée)
- [x] Waitlist + limite bêta 50 familles
- [x] Email J+0 — refonte template vouvoiement parent (15 mars 2026)
- [ ] replyTo: nicolas@matheux.fr sur J+3, J+7 et reset MDP
- [x] Overlay trial → Stripe direct 19,99€/mois (lien TEST)
- [x] Email J+7 → lien Stripe
- [x] **`contact@matheux.fr`** créé (Ionos) — ✅ 16 mars 2026
- [x] **Alias `no-reply@matheux.fr`** (Gmail → SMTP Ionos port 465 SSL) ✅ 16 mars
- [x] **Formulaire contact** — `send_contact` GAS + modal 3 footers + `_toast()` ✅ 16 mars
- [x] **Merge sécurité freelance** (SECUmain → main) — Stripe MAXIMAL PARANOID + Premium Guard ✅ 16 mars
- [x] **GitHub Pages** reconfiguré sur branche main ✅ 16 mars
- [x] **Tests emails** — J+0 ✅ / Reset MDP ✅ / Contact ✅ / Pas de triggers ✅ 16 mars
- [x] **Stripe TEST → PROD** — ✅ Fait @82 (16 mars 2026)
- [x] **Webhook Stripe → colonne Premium** — code déployé @85 (security layer 1 + 2) — endpoint Stripe à finaliser manuellement

---

## BLOC 4 — Marketing & conversion 🟢

- [x] Landing vendeuse — refonte complète 13 mars (hero parent, programme Eduscol 4 niveaux, sur mesure + IA x humain, mockup scree.png, témoignages x3, fondateur "Ancien chef de projet Aérospatiale", FAQ accordion, compteurs animés 44/880/100%, chapitres sur mesure à l'infini, CTA "Les bons exercices")
- [x] Email J+0 auto
- [x] **Objectif élève post-quiz** — overlay 4 choix, colonne Users N, emails J+5/J+7 personnalisés selon objectif, badge dans fiche admin (@70, 15 mars 2026)
- [ ] **Automatiser emails J+3/J+5/J+7** — trigger `triggerDailyMarketing` → **à activer plus tard (dès 10 clients)**, manuel via admin pour l'instant
- [ ] Vrais témoignages élèves/parents

---

## BLOC 5 — Automatisation & scale 🔵

- [x] Mode Brevet Blanc complet (BrevetExos, quiz, résultats, admin publie)
- [x] Feedback élève → Insights
- [x] 5 chapitres prioritaires en prod
- [x] **Mode Révision** — admin ouvre chapitres d'une autre année depuis la fiche élève → dashboard élève + badge 🔁 + toast notification (13 mars 2026)
- [x] **Brouillon contextuel + Calculette** — symboles adaptés par chapitre/niveau, onglets Brouillon|Calculette, sin/cos/tan si géo/trigo, copie vers brouillon (13 mars 2026)
- [x] **Niveau 1ERE Spé Maths** — 10 chapitres, 330 exercices, backend `ALLOWED_LEVELS` + `niveauOrder` patchés @64. Frontend non modifié (pas de sélecteur 1ERE à l'inscription). Compte test Auguste (AUG001) prêt. Voir [rapport-1ere.md](rapport-1ere.md) (14 mars 2026)
- [x] **Fix BUG-1ERE-JSON** — `a ∉ options` dans 6/10 chapitres 1ERE (Dérivation, Suites, Exponentielle, Trigo, Produit scalaire, Géométrie repérée, Probas cond, Variables aléatoires, Algorithmique). Assert guard permanent dans `_exo()`. 600 exercices validés (14 mars 2026)
- [x] **Figures géo SVG v2** — lettres dynamiques, filtrage strict, 18 types (3 nouveaux 1ERE : vectors, repere, trigo_circle), viewBox 280×210 (14 mars 2026)
- [x] **Auth modal protégé** — showAuth() gardé trial-flow + auto-login silencieux sans modale imposée (14 mars 2026)
- [x] **Toast mobile responsive** — white-space normal, max-width 88vw, word-break, border-radius 18px (14 mars 2026)
- [x] **Brouillon/Calculette desktop** — panneau latéral droit 1/3 écran, les 2 fusionnés (calc en haut, brouillon en bas). Mobile : bottom sheet 50vh (énoncé reste visible) (14 mars 2026)
- [x] ~~**Mode nuit landing**~~ — supprimé @82 (16 mars 2026)
- [x] **Brevet Blanc UX v2** — écran d'accueil enrichi (nb questions, durée estimée, conditions), chronomètre discret pendant le quiz, écran résultats refondu (mentions Très bien/Bien/Passable/À retravailler, chapitres faibles en rouge, bouton "Voir mes erreurs", temps écoulé) (14 mars 2026)
- [x] **Progression enrichie** — tri chapitres par score ASC (faibles en premier), labels Fragile/En progrès/Solide/Maîtrisé, badge ⚠️ À reprendre si >7j inactif, accordéon chapitres maîtrisés, synthèse globale (nb chapitres, exos, streak) (14 mars 2026)
- [x] **Figures géo v3 — système de confiance** — chaque figure a un score confidence (high/medium/low), figures low filtrées, triangle "à prouver rectangle" → triangle neutre, cercle sans rayon numérique → pas de figure, angle à calculer → pas de figure (14 mars 2026)
- [x] **Visualisation courbes post-réponse** — extractFunction détecte f(x)=ax+b et ax²+bx+c dans l'énoncé, renderFunctionGraph trace en SVG après réponse, intégré dans _previewHelp (14 mars 2026)
- [x] **Types d'exercices enrichis** — support VF (2 gros boutons + justification post-réponse), fill (trou ___ mis en évidence indigo), grille options adaptative (2→2 cols, 3→vertical, 4→2×2) (14 mars 2026)
- [x] **Signaler uniformisé** — bouton "📢 Une erreur dans cet exercice ?" ajouté dans renderArchiveSection (historique), présent sur tous les modes (14 mars 2026)
- [x] **Audit messages & onboarding** — tous les messages vérifiés cohérents (prix, nb exos, ton, français), aucune incohérence détectée (14 mars 2026)
- [x] **Documentation nettoyée** — CLAUDE.md épuré en point d'entrée, 7 rapports archivés, docs vivantes mises à jour (14 mars 2026)
- [x] **PWA — Progressive Web App** — manifest.json, sw.js (Cache First + Network First GAS), offline.html, 11 icônes (72→512px + maskable + apple-touch), balises PWA head, bannière install Android (`beforeinstallprompt`), iOS hint 1x (localStorage) — code commité, **déploiement Netlify/GitHub Pages à valider** (14 mars 2026)
- [x] **Landing refonte wording** — axe "empreinte cognitive + prof humain + FOMO rétention" : hero, stats, programme, étapes, nouvelle section "Ce que Matheux sait", 4ème témoignage, fondateur renforcé, prix, 2 FAQ, CTA final, sticky mobile. Aucune modif JS/CSS. (15 mars 2026)
- [x] **Objectif élève post-quiz** — slide 4 choix (lacunes/chapitre_jour/brevet/toutes_matieres), col N Users, emails J+5/J+7 personnalisés par objectif (@70, 15 mars 2026)
- [x] **Admin panel upgrade** — emails éditables avant copie, duplication supprimée, 💤 Sans nouvelles, action cours (coursNeeded), dark mode onboarding only, profils test diversifiés (@69, 15 mars 2026)
- [x] **Simulation test complète** — script Python 10 profils × tous les workflows, 10/10 OK, 111 appels GAS (@72, 15 mars 2026)
- [ ] **Profil d'apprentissage élève** — page dédiée montrant : 3 points forts identifiés, 2 lacunes en cours, vitesse de progression, streak record. Affiché avec cadenas dans l'overlay trial J+7 ("ces données disparaissent dans 48h")
- [ ] **Automatisation boosts nuit** — agent qui tourne chaque nuit, lit les erreurs depuis Scores, génère le JSON boost, pousse dans Suivi sans intervention Nicolas. Déclencheur : rebuildSuivi détecte BOOST TERMINÉ → GAS génère automatiquement. Priorité : dès 30 clients actifs
- [x] **Rapport parent hebdo automatique** — `triggerWeeklyParentReport` dimanche 17h-18h, stats réelles (nb exos, % réussite, chapitres maîtrisés), mot adapté au score. **Trigger à activer manuellement dans Apps Script** (15 mars 2026, @74)
- [x] **Admin cockpit refonte** — 3 onglets À FAIRE/FAIT/TEST, cartes inline avec workflows, journal horodaté, `log_contact` (15 mars 2026, @76)
- [x] **Mode nuit app** — bouton 🌙 header, `body.app-night`, localStorage `app_night` (15 mars 2026, @77)
- [x] **Boost terminé — navigation** — Précédent/Suivant disponible après boost (15 mars 2026, @77)
- [x] **Guide "Commence par là"** — corrigé : affiché uniquement après boost consommé (15 mars 2026, @77)
- [x] **Titres chapitres gras** — `font-weight:800` explicite (15 mars 2026, @77)
- [x] **Audit pédagogique complet** — 1872 exercices audités + corrigés : notation décimale FR, indices S1 reformulés, doublons 1ERE réécrits. Score qualité ~98% (15 mars 2026, @77)
- [x] **Page teasing pré-lancement** — `#teasing-screen` avec countdown live (18 mars 9h Paris), champ email waitlist (`add_teasing_early` → onglet `Teasing_Early`), lien "Accès bêta" (login only), auto-switch vers vraie landing à 9h, `?noteasing` pour dev. Mode nuit landing supprimé. (16 mars 2026, @82)
- [ ] Agent analyse lacunes quotidien automatique
- [ ] **Migration Sheets → Supabase** — à déclencher à 80-100 clients payants (pas avant).
  Capacité actuelle estimée : ~15 connexions simultanées, ~8 save_score simultanés, 100 clients actifs confortables.
  Stack cible : Supabase (PostgreSQL) + GAS comme proxy ou Node.js sur Railway.
  Emails : remplacer GmailApp par Brevo (300/j gratuit) ou Resend.
  Durée estimée : 3-5 sessions Claude Code + 2-3 semaines de tests.
  **Ne pas faire avant d'avoir le problème.**

---

## Couverture programme — chapitres manquants

### Priorité critique (programme officiel, souvent au Brevet)
| Notion | Niveau | Statut |
|---|---|---|
| Systèmes d'équations | 3EME | Sprint 2 — Extension Équations |

### Priorité importante (programme officiel)
| Notion | Niveau | Effort |
|---|---|---|
| Symétrie axiale | 6EME | +1 chapitre |
| Symétrie centrale | 5EME | +1 chapitre |
| Volumes | 6EME | Extension PérimètresAires |
| Transformations (translations, rotations) | 5EME | +1 chapitre |
| Inéquations | 3EME | Extension Équations |
| Notation scientifique | 3EME | Extension Puissances |

Détail complet : [programme-français-verif.md](programme-français-verif.md)

---

## Checklist "Prêt pour 50 élèves"

### Infrastructure
- [x] GAS @80 stable — 30+ actions, bugfixes complets, niveau 1ERE, audit exercices, simulation 21j OK (4 bugs corrigés)
- [x] Google Sheet prod
- [x] Validation inputs GAS (register + saveScore — @63)
- [x] Rate limiting doPost (global 60/min, sensibles 15/min — @63)

### Acquisition & conversion
- [x] Landing + flow CTA + quiz inline + onboarding
- [x] Trial 7j + badge J-X + overlay → Stripe
- [x] Email J+0 auto (avec dédup cron/register)
- [x] **Stripe PROD** ✅ Fait @82
- [ ] **Séquences J+3/J+5/J+7 activées** ⚠️ Manuel (trigger Apps Script)

### Légal
- [x] 5 pages légales + consentement parental + RGPD + GA4

### Pédagogie
- [x] 1080 exos curriculum + 108 diag + 540 boost + 144 brevet — programme complet ~100% + 1ERE Spé

### UX
- [x] Mobile-first, gamification, messages ado
- [x] Post-boost confettis, feedback, indices lisibles
- [~] **PWA installable** — code prêt (manifest + SW + icônes + bannière), **à valider en prod** (Chrome DevTools → Application → tout vert, Lighthouse PWA ≥ 90)

### Admin
- [x] Dashboard trié, modal complet, publish 1-clic, toast overwrite chapitre
- [x] Rapport matin, compteur X/50, dark mode
- [x] Emails dus J+3/J+5/J+7, onglet Suivi, indicateurs J0
- [x] Email modal éditable + templates marketing v2 + coursNeeded + Sans nouvelles + 6 profils test (@69)

---

## PHASE 2 — Après 20 clients payants

| # | Feature | Description | Priorité |
|---|---|---|---|
| 1 | Doc vivante par élève/chapitre | Fiche notion + faiblesses identifiées, in-app, adaptée niveau/âge. Admin : bouton "Générer fiche chapitre" → JSON → injection. Frontend : modal/drawer in-app. | 🟡 |
| 2 | Graphes de fonctions post-réponse avancés | Tracé automatique depuis l'énoncé — exponentielles, trigo, fonctions par morceaux | 🟡 |
| 3 | Arbres de probabilités post-réponse | Détection auto "arbre" dans l'énoncé → arbre pondéré SVG après réponse | 🟡 |
| 4 | Types d'exercices enrichis — rollout | VF, fill, compléter — rollout progressif sur les nouveaux exercices générés | 🟡 |
| 5 | Audit géométrie contextuelle | Exercices trop courts/abstraits à reformuler (voir audit-geo-context) | 🔵 |

### Offres différenciées — décision basée sur données réelles

> **Ne pas créer avant d'avoir lu la colonne `Objectif` sur 10-15 clients.**
> Les données de la colonne N (Users) diront quoi construire.

| Si majorité déclare | Offre envisagée | Prix |
|---|---|---|
| `lacunes` | Offre actuelle — déjà bien positionnée | 19,99€/mois |
| `brevet` | Pack "Prépa Brevet" — accès prioritaire brevets blancs + suivi dédié | 24,99€/mois |
| `chapitre_jour` | Offre "Suivi annuel" — engagement 10 mois, prix réduit | 14,99€/mois |
| `toutes_matieres` | Offre "Multi-niveaux" — accès tous niveaux (fratrie) | 29,99€/mois |

**Workflow de migration** : email personnalisé selon objectif déclaré → lien Stripe vers nouveau plan.
Aucun client existant verrouillé (pas de CB pendant le trial).

**Offre flash de conversion** : à J+2/J+3, si l'élève est engagé (boost fait, streak actif),
envoyer manuellement une offre -50% premier mois ("9,99€ ce mois-ci, sans engagement").
Lien Stripe séparé créé en 2 min. Envoi manuel depuis la fiche admin. Zéro code requis.

**Quand décider** : après 10-15 clients, regarder la répartition `Objectif` dans Users.

### Rétention & FOMO — mécaniques psychologiques

> Objectif : rendre le départ douloureux, pas l'abonnement obligatoire.
> Principe : la valeur accumulée doit être visible et concrète.

**Mécanique 1 — Profil d'apprentissage avec cadenas**
À J+7, overlay trial ne dit pas juste "19,99€/mois".
Il montre le profil construit : points forts, lacunes identifiées, streak, vitesse de progression.
Avec un message : "Ces données disparaissent dans 48h. Continue pour garder ton profil."
Honnête, factuel, puissant.

**Mécanique 2 — Streak comme identité (pas comme peur)**
Pas "tu vas perdre ton streak" à la Duolingo.
Mais : "Lucas a travaillé 12 jours d'affilée — top 5% des élèves Matheux."
La perte devient une fierté à protéger, pas une anxiété.

**Mécanique 3 — Rapport parent comme lien émotionnel**
Email hebdo formulé comme bilan humain :
"Cette semaine Hugo a débloqué les fractions — une notion qui lui résistait depuis septembre.
Son score de confiance est passé de 34 à 61/100."
Le parent ne désabonne pas ce qui progresse.

**Mécanique 4 — Personnalisation explicite dans les messages**
Pas "exercices personnalisés" (générique).
Mais : "Ton prof a remarqué que tu fais toujours la même erreur sur les fractions
avec dénominateurs différents — voici pourquoi."
Sentiment de relation, pas d'outil.

**Mécanique 5 — Coût de reconstruction visible**
À J+30 : "Si tu recommences ailleurs, il faudra X semaines pour retrouver
ce niveau de personnalisation." Ancré dans la réalité — un service concurrent repart de zéro.

**À implémenter dans l'ordre** :
1. Profil d'apprentissage dans l'overlay trial (PHASE 2 priorité 1)
2. Rapport parent hebdo automatique (dès 20 clients)
3. Streak comme identité dans les toasts (petit patch, fort impact)
4. Personnalisation explicite dans les messages post-exo (wording uniquement)
