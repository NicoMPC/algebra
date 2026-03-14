# Roadmap — Matheux

> Priorités de développement par blocs. Voir aussi [claude.md](claude.md) pour les règles et [product.md](product.md) pour le produit.

---

## État global — 14 mars 2026

**Matheux est fonctionnel à 100% côté code. Seuls manques : Stripe PROD + 2 actions manuelles.**

> ✅ **Audit + bugfixes réalisés le 13 mars 2026** (simulation 7j × 5 profils sur GAS réel).
> BUG-01 à BUG-12 corrigés dans backend.js @60.
> ✅ **Simulation QA 40 élèves le 14 mars 2026** — 6 bugs corrigés (BUG-SIM-01→06) + **test live 1616 appels API : 0 erreur**. GAS @63.
> ✅ **Niveau 1ERE Spé Maths ajouté le 14 mars 2026** — 10 chapitres, 330 exercices (200 curriculum + 20 diag + 100 boost + 10 restants), compte Auguste (AUG001) prêt pour visio. GAS @64.

| Dimension | État |
|---|---|
| Tests automatisés | **74/74 (100%)** + simulation 40 élèves **17/17 PASS** (1616 appels API, 0 erreur) |
| Couverture programme | **~100%** — 54 chapitres (1080 exos curriculum + 108 diag + 540 boost + 144 brevet) |
| Niveau 1ERE Spé | **10 chapitres expérimentaux** — backend prêt, frontend non modifié (connexion uniquement) |
| Juridique | Complet (5 pages + consentement parental + RGPD) |
| Paiement | ⏳ Lien Stripe TEST actif — **à passer en PROD manuellement** |
| Emails auto | ✅ J+0 auto + fallback manuel admin, J+3/J+5/J+7 code prêt — **trigger à activer manuellement** |
| Analytics | ✅ GA4 RGPD-compliant |
| Limite bêta | 50 vrais élèves (IsTest=0) |
| Messages élèves | ✅ Streak alert, boost en cours, chapitre maîtrisé, milestones 3/7j |
| Admin smart | ✅ GAS @64 — bugfixes audit + simulation QA, rate limiting global, validation inputs, 1ERE Spé |
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

## Priorités code — prochaines sessions

| # | Action | Statut | Priorité |
|---|---|---|---|
| 0 | **Fixes bugs audit** (BUG-01 à BUG-12 dans [test_debug.md](test_debug.md)) | ✅ Corrigés @60 | 🟢 |
| 1 | Validation inputs GAS (format email, longueur champs) | ✅ Corrigé @63 (register + saveScore) | 🟢 |
| 2 | Rate limiting global dans doPost (60/min, 15/min sensibles) | ✅ Corrigé @63 | 🟢 |
| 3 | **BUG-AUDIT-01** : `Systèmes_Équations 3EME exo#16` — `"a": "4 lapins"` absent des options numériques | ❌ À faire | 🔴 |
| 4 | **BUG-AUDIT-02/03** : Boost `Transformations 5EME` + `Homothétie 4EME` — tiret unicode `−` vs `-` (réponse hors options) | ❌ À faire | 🔴 |
| 5 | **BUG-AUDIT-04** : 5 doublons Boost/Curriculum (`Fonctions_Linéaires 4EME`, `Notation_Scientifique 3EME`, `Sections_Solides 4EME` ×2, `Puissances_10 6EME`) | ❌ À faire | 🟡 |
| 6 | **BUG-AUDIT-05** : Vérifier compatibilité `diff` "easy/medium/hard" BrevetExos vs `index.html` (le code attend 1/2 selon database.md) | ❌ À faire | 🟡 |

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
- [x] BrevetExos : 144 exos (18 chap × 8) — tous chapitres 3EME couverts
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
- [x] Messages élèves : streak break alert, boost en cours nudge, chapitre maîtrisé, milestones streak 3j/7j
- [x] Email J+5 "Encore 2 jours" dans séquence marketing
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
- [ ] Email J+0 — refonte template vouvoiement parent + replyTo nicolas@matheux.fr (brief dans product.md § Emails automatiques)
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
- [ ] Agent analyse lacunes quotidien automatique
- [ ] Agent génération boost automatique
- [ ] Agent rapport parents (email hebdo)
- [ ] Migration Sheets → vraie BDD si >50 users simultanés

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

### Admin
- [x] Dashboard trié, modal complet, publish 1-clic, toast overwrite chapitre
- [x] Rapport matin, compteur X/50, dark mode
- [x] Emails dus J+3/J+5/J+7, onglet Suivi, indicateurs J0
