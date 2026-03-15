# Roadmap — Matheux

> Priorités de développement par blocs. Voir aussi [claude.md](claude.md) pour les règles et [product.md](product.md) pour le produit.

---

## État global — 15 mars 2026

**Matheux est fonctionnel à 100% côté code. Seuls manques : Stripe PROD + 2 actions manuelles.**

> ✅ **Audit + bugfixes réalisés le 13 mars 2026** (simulation 7j × 5 profils sur GAS réel).
> BUG-01 à BUG-12 corrigés dans backend.js @60.
> ✅ **Simulation QA 40 élèves le 14 mars 2026** — 6 bugs corrigés (BUG-SIM-01→06) + **test live 1616 appels API : 0 erreur**. GAS @63.
> ✅ **Niveau 1ERE Spé Maths ajouté le 14 mars 2026** — 10 chapitres, 330 exercices (200 curriculum + 20 diag + 100 boost + 10 restants), compte Auguste (AUG001) prêt pour visio. GAS @64.
> ✅ **Admin panel upgrade le 15 mars 2026** — email modal éditable, coursNeeded, renommage BLOQUÉ→Sans nouvelles, dark mode onboarding, 6 profils test. GAS @69.
> ✅ **Objectif élève post-quiz le 15 mars 2026** — overlay 4 choix après diagnostic, colonne Users N, emails J+5/J+7 personnalisés, badge admin. GAS @70.
> ✅ **Simulation 10 profils le 15 mars 2026** — 111 appels GAS, 10/10 profils OK. Fix `ss is not defined` dans getAdminOverview + sw.js exclu de GAS. GAS @72.
> ✅ **Message architecture system le 15 mars 2026** — `_msg()` adaptatif niveau, coach marks, _OK/_KO contextuels, onboarding objectif, emails J+3/J+5/J+7 personnalisés objectif, triggerWeeklyParentReport. GAS @74.

| Dimension | État |
|---|---|
| Tests automatisés | **74/74 (100%)** + simulation 40 élèves **17/17 PASS** (1616 appels API, 0 erreur) |
| Couverture programme | **~100%** — 54 chapitres (1080 exos curriculum + 108 diag + 540 boost + 144 brevet) — tous audités ✅ |
| Niveau 1ERE Spé | **10 chapitres expérimentaux** — backend prêt, frontend non modifié (connexion uniquement), 3 types SVG dédiés |
| Juridique | Complet (5 pages + consentement parental + RGPD) |
| Paiement | ⏳ Lien Stripe TEST actif — **à passer en PROD manuellement** |
| Emails auto | ✅ J+0 auto + J+3/J+5/J+7 personnalisés objectif — **trigger à activer manuellement** + rapport hebdo parent (`triggerWeeklyParentReport`) |
| Analytics | ✅ GA4 RGPD-compliant |
| Limite bêta | 50 vrais élèves (IsTest=0) |
| Messages élèves | ✅ Système adaptatif `_msg()` — ~35 entrées, niveau, objectif, coach marks, _OK/_KO contextuels |
| Admin smart | ✅ GAS @69 — email modal éditable, coursNeeded, Sans nouvelles, dark mode onboarding, 6 profils test |
| Emails (@matheux.fr) | ⏳ **à créer manuellement** : contact@ + alias no-reply@ |

---

## Actions manuelles — à faire par Nicolas (bloquantes prod)

| # | Action | Où | Priorité |
|---|---|---|---|
| 1 | **Stripe TEST → PROD** — remplacer `test_14AdRacgw76N7vQcxqa3u00` (3 occurrences : `index.html`, `backend.js`, `cgv.html`) | Stripe dashboard + éditeur | 🔴 |
| 2 | **Créer `contact@matheux.fr`** (adresse publique) + **alias `no-reply@matheux.fr`** dans Gmail (pour GmailApp) | Hébergeur email + Gmail Paramètres → Comptes | 🔴 |
| 3 | **Activer trigger `triggerDailyMarketing`** → Apps Script UI → Déclencheurs → `triggerDailyMarketing` → Chaque jour → 9h-10h | Google Apps Script UI | 🔴 |
| 4 | **Webhook Stripe → colonne `Premium`** dans Users | Stripe dashboard → Webhooks | 🟡 après Stripe PROD |
| 5 | Vrais témoignages élèves/parents sur landing | À collecter après premiers clients | 🔵 |
| 6 | **Design overhaul landing** — hero glow, social proof fold, CTA shimmer, glass stats, step numbers watermark, avatars+Vérifié, 0,66€/jour, guarantee badge, sticky mobile CTA | ✅ Fait @68 (14 mars 2026) | 🟢 |

## Priorités code — prochaines sessions

| # | Action | Statut | Priorité |
|---|---|---|---|
| 0 | **Fixes bugs audit** (BUG-01 à BUG-12 dans [test_debug.md](test_debug.md)) | ✅ Corrigés @60 | 🟢 |
| 1 | Validation inputs GAS (format email, longueur champs) | ✅ Corrigé @63 (register + saveScore) | 🟢 |
| 2 | Rate limiting global dans doPost (60/min, 15/min sensibles) | ✅ Corrigé @63 | 🟢 |
| 3 | **BUG-AUDIT-01** : `Systèmes_Équations 3EME exo#16` — réponse corrigée | ✅ Corrigé (déjà en prod) | 🟢 |
| 4 | **BUG-AUDIT-02/03** : Boost `Transformations 5EME` + `Homothétie 4EME` — tiret unicode | ✅ Corrigé (déjà en prod) | 🟢 |
| 5 | **BUG-AUDIT-04** : 5 doublons Boost/Curriculum collège | ✅ Corrigé (déjà en prod) | 🟢 |
| 11 | **Doublons 1ERE** : 19 doublons Boost/Curriculum dans 6 chapitres 1ERE (insert_1ere.py) | ❌ À faire | 🟡 |
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
- [ ] **Créer alias `no-reply@matheux.fr`** (GmailApp) + `contact@matheux.fr` (public) — **⚠️ Manuel hébergeur**
- [ ] **Passer Stripe TEST → PROD** (3 occurrences) — **⚠️ Manuel après lien Stripe PROD**
- [ ] **Webhook Stripe → colonne Premium** — **⚠️ Manuel Stripe dashboard**

---

## BLOC 4 — Marketing & conversion 🟢

- [x] Landing vendeuse — refonte complète 13 mars (hero parent, programme Eduscol 4 niveaux, sur mesure + IA x humain, mockup scree.png, témoignages x3, fondateur "Ancien chef de projet Aérospatiale", FAQ accordion, compteurs animés 44/880/100%, chapitres sur mesure à l'infini, CTA "Les bons exercices")
- [x] Email J+0 auto
- [x] **Objectif élève post-quiz** — overlay 4 choix, colonne Users N, emails J+5/J+7 personnalisés selon objectif, badge dans fiche admin (@70, 15 mars 2026)
- [ ] **Activer trigger `triggerDailyMarketing`** (J+3/J+5/J+7) — **⚠️ Manuel Apps Script UI → 9h-10h**
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
- [x] **Mode nuit landing** — toggle lune dans la nav, fond sombre sur toutes les sections claires, persisté localStorage (14 mars 2026)
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
- [ ] **Objectif élève post-quiz** — slide 4 choix (lacunes/chapitre_jour/brevet/toutes_matieres), col N Users, emails J+5/J+7 personnalisés par objectif. Prompt prêt (15 mars 2026)
- [ ] **Admin panel upgrade** — emails éditables avant copie, duplication supprimée, 💤 Sans nouvelles, action cours (coursNeeded), dark mode onboarding only, profils test diversifiés. Prompt prêt (15 mars 2026)
- [ ] **Simulation test complète** — script Python 10 profils × tous les workflows, rapport friction. Prompt prêt (15 mars 2026)
- [ ] **Profil d'apprentissage élève** — page dédiée montrant : 3 points forts identifiés, 2 lacunes en cours, vitesse de progression, streak record. Affiché avec cadenas dans l'overlay trial J+7 ("ces données disparaissent dans 48h")
- [ ] **Automatisation boosts nuit** — agent qui tourne chaque nuit, lit les erreurs depuis Scores, génère le JSON boost, pousse dans Suivi sans intervention Nicolas. Déclencheur : rebuildSuivi détecte BOOST TERMINÉ → GAS génère automatiquement. Priorité : dès 30 clients actifs
- [x] **Rapport parent hebdo automatique** — `triggerWeeklyParentReport` dimanche 17h-18h, stats réelles (nb exos, % réussite, chapitres maîtrisés), mot adapté au score. **Trigger à activer manuellement dans Apps Script** (15 mars 2026, @74)
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
- [x] GAS @64 stable — 28+ actions, bugfixes audit complets, niveau 1ERE
- [x] Google Sheet prod
- [x] Validation inputs GAS (register + saveScore — @63)
- [x] Rate limiting doPost (global 60/min, sensibles 15/min — @63)

### Acquisition & conversion
- [x] Landing + flow CTA + quiz inline + onboarding
- [x] Trial 7j + badge J-X + overlay → Stripe
- [x] Email J+0 auto (avec dédup cron/register)
- [ ] **Stripe PROD** ⚠️ Manuel
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
