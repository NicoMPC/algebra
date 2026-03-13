# Roadmap — Matheux

> Priorités de développement par blocs. Voir aussi [claude.md](claude.md) pour les règles et [product.md](product.md) pour le produit.

---

## État global — 13 mars 2026

**Matheux est fonctionnel à 99% — prêt pour les 50 premiers élèves. Seul manque : Stripe PROD.**

| Dimension | État |
|---|---|
| Tests automatisés | 73/74 (99%) — 1 race condition GAS acceptable |
| Couverture programme | **~100%** — 44 chapitres (880 exos curriculum + 88 diag + 440 boost + 144 brevet) |
| Juridique | Complet (5 pages + consentement parental + RGPD) |
| Paiement | ⏳ Lien Stripe TEST actif — passer en PROD |
| Emails auto | ✅ J+0 auto + fallback manuel admin, J+3/J+5/J+7 code prêt (trigger à activer) |
| Analytics | ✅ GA4 RGPD-compliant |
| Limite bêta | 50 vrais élèves (IsTest=0) |
| Messages élèves | ✅ Streak alert, boost en cours, chapitre maîtrisé, milestones 3/7j |
| Admin smart | ✅ GAS @59 — catégories capitale/secondaire, onglet Suivi, copie emails |

---

## Priorités immédiates

| # | Action | Statut | Priorité |
|---|---|---|---|
| 1 | Passer Stripe TEST → PROD (3 occurrences : index.html, backend.js, cgv.html) | ⏳ Attente lien prod | 🔴 |
| 2 | Créer contact@matheux.fr + alias no-reply@matheux.fr | ⏳ Manuel hébergeur | 🔴 |
| 3 | Activer trigger `triggerDailyMarketing` (Apps Script UI → 9h-10h) | ⏳ 5 min manuel | 🟡 |
| 4 | Webhook Stripe → colonne Premium dans Users | ❌ Après Stripe PROD | 🟡 |
| 5 | Validation inputs GAS (format email, longueur champs) | ❌ À faire | 🟢 |
| 6 | Rate limiting basique dans doPost | ❌ À faire | 🟢 |
| 7 | Vrais témoignages élèves/parents sur landing | ❌ À collecter | 🔵 |

---

## BLOC 1 — Socle technique ✅ TERMINÉ

- [x] generate_diagnostic / generate_daily_boost / isFirstDay / boostExistsInDB
- [x] Curriculum_Officiel : 880 exos (44 chap × 20) — programme collège 100% couvert (Sprint 1→4)
- [x] DiagnosticExos : 88 exos (44 chap × 2)
- [x] BoostExos : 440 exos (44 chap × 10)
- [x] BrevetExos : 144 exos (18 chap × 8) — tous chapitres 3EME couverts
- [x] CHAPS_BY_LEVEL : 44 chapitres exposés dans sélecteur diagnostic
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
- [ ] Validation inputs côté GAS (format email, longueur)
- [ ] Rate limiting basique dans doPost

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
- [x] Overlay trial → Stripe direct 9,99€/mois (lien TEST)
- [x] Email J+7 → lien Stripe
- [x] Emails from no-reply@matheux.fr
- [ ] **Passer Stripe TEST → PROD** (3 occurrences)
- [ ] **Webhook Stripe → colonne Premium**

---

## BLOC 4 — Marketing & conversion 🟢

- [x] Landing vendeuse — refonte complète 13 mars (hero parent, programme Eduscol 4 niveaux, sur mesure + IA x humain, mockup scree.png, témoignages x3, fondateur "Ancien chef de projet Aérospatiale", FAQ accordion, compteurs animés 44/880/100%, chapitres sur mesure à l'infini, CTA "Les bons exercices")
- [x] Email J+0 auto
- [ ] Activer trigger `triggerDailyMarketing` (J+3/J+7)
- [ ] Vrais témoignages élèves/parents

---

## BLOC 5 — Automatisation & scale 🔵

- [x] Mode Brevet Blanc complet (BrevetExos, quiz, résultats, admin publie)
- [x] Mode Révision (code conservé, UI désactivé)
- [x] Feedback élève → Insights
- [x] 5 chapitres prioritaires en prod
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
- [x] GAS @57 stable — 27 actions opérationnelles
- [x] Google Sheet prod
- [ ] Validation inputs GAS
- [ ] Rate limiting doPost

### Acquisition & conversion
- [x] Landing + flow CTA + quiz inline + onboarding
- [x] Trial 7j + badge J-X + overlay → Stripe
- [x] Email J+0 auto
- [ ] Stripe PROD
- [ ] Séquences J+3/J+7 activées

### Légal
- [x] 5 pages légales + consentement parental + RGPD + GA4

### Pédagogie
- [x] 580 exercices + 58 diagnostics + 120 brevet
- [x] Couverture ~85% programme officiel

### UX
- [x] Mobile-first, gamification, messages ado
- [x] Post-boost confettis, feedback, indices lisibles

### Admin
- [x] Dashboard trié, modal complet, publish 1-clic
- [x] Rapport matin, compteur X/50, dark mode
