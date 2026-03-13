# Historique des sessions — Matheux

> Journal chronologique de toutes les sessions de développement. Voir aussi [roadmap.md](roadmap.md) pour les priorités et [claude.md](claude.md) pour les règles.

---

## Mars 2026

### 9 mars — Sessions @5
- DiagnosticExos refaits, 20 profils test créés
- Bugs T1-T7 post-tests utilisateurs tous corrigés
- Test flux complet

### 9-10 mars (nuit) — Sessions @8
- Prompt génération refondu, algo sélection exos
- docs/ 8 fichiers créés
- Commits : 2f0d345, aaa8b2c, d69c108, 68b18a3, dbbf0a2

### 10 mars matin — Session @10
- login() nettoyé
- generateDailyBoost bug hors-scope corrigé
- 4 onglets archivés

### 10 mars soir — Session @15
- rebuildSuivi(), writeToHistorique(), rebuild_sheet.py
- Structure 👁 Suivi 20 colonnes

### 10 mars nuit — Session @13
- Audit 95% test_complet.py
- 4 bugs UX (boostConsumed, relDate, renderChapComplete)
- Commits : d6aae86, 025cbb9

### 11 mars nuit — Session @19
- Landing SEO + trial inline
- Messages ton ado
- test_scenarios.py 6/6
- Email J+3/J+7
- Bug date boostExistsInDB fixé

### 11 mars matin — Session @22
- Admin dashboard refondu
- ExosDone DailyBoosts
- rebuildSuivi règles revues
- Modal élève enrichi, données 20 scénarios
- Commits : 6db9e7c, 5bc72e5

### 11 mars après-midi — Session @28
- Fix chapLocked actif uniquement
- Section archivés modal
- Cap 20 exos chapitresDetail
- Essai 7j complet
- Commits : ab58d6d, 72d200d

### 11 mars soir — Session @30
- CORS fix
- Landing CALIBRAGE + flow guest
- Admin modal DIAG/CH
- Pills prioritaires
- Landing vendeuse
- Essai 7j onboarding
- Commits : 80a247f, 50c7bdb, 0da6a26, a2ee071, 4e1a30e, 6564c30, a66879c, 61b2924, f917a29, 7e63b0f, 372ac76, d7be47f

### 12 mars — Sessions @24→@23
- Git reconstruit (12a61e7)
- UX admin/élève
- boostJSON copie
- rebuild_sheet.py synchronisé
- Fix auto-login, boostConsumed
- Commits : 12a61e7, c22f471, 2a808d3, 9421ef6, b96f9d8

### 12 mars soir — Session @30
- Smart question count `_pickDiagExos()`
- Fix Diagnostic-6ème guest
- Onboarding adapté, boost auto guest
- Commits : 9524e3a, ac046e4

### 12 mars nuit — Session @30
- Quiz inline landing (step 3 card blanche)
- Tutorial Q1
- Fix onbRender bg
- Cohérence messages
- Commit : 544a112

### 12 mars nuit 2 — Session @30
- Simulation 20 profils/5j
- Messages parent/ado refondus
- BLOC 3 juridique complet (5 pages + footer + consentement)

### 13 mars — Session @31
- BLOCS 4-5 : landing pricing + fondateur + carousel
- programme-français-verif.md (66% couverture)
- Mode Brevet (GAS + UI 3 screens)
- Mode Révision (GAS + card)
- Feedback (modal + Insights tab)
- 7 bugs fixes (showT/SHEET_ID/Array.find/chkComp/togCat/res2/sendScore)
- test_workflows.py 37/38 PASS (97%)

### 12 mars — Session @34
- Désactivation UI Brevet + Révision (code conservé)
- 5 chapitres poussés en prod (100 exos)
- verifyAdmin fix (TRUE/1)
- Rapport condensé, notice refaite, programme ~85%

### 13 mars — Session @35
- BLOC 3 complet : waitlist 40 fam. GAS
- Email J+0 auto
- GA4 consentement
- Bannière cookies RGPD
- premium.html
- CGU clause bêta

### 13 mars — Session @36
- GA4 G-7R2DW4585Y intégré
- Overlay trial → Stripe direct 9,99€/mois
- Email J+7 → Stripe
- GmailApp from no-reply@matheux.fr

### 13 mars — Session @37
- Dashboard admin : bloc "Outils Fondateur" (Stripe TEST badge, email test via GAS)

### 13 mars — Session @38
- Fix quiz CTA invisible (mc rdy)
- Bypass 40-fam pour @matheux.fr
- Note contact@matheux.fr dans dashboard

### 13 mars — Session @39
- Colonne IsTest Users
- Limite 50 vrais élèves
- Dashboard compteur X/50 + section test repliable
- mark_all_test GAS
- Migration Python (110 comptes → IsTest=1)

### 13 mars — Session @40
- UX post-boost : confettis + auto-redirect 5s + boost card "Prochain dispo demain"
- Hints/Formule : contraste amber-800 + fond coloré
- Admin BOOST TERMINÉ fix (today inclus)
- Modal admin : indicateurs email J0/J3/J7

### 13 mars — Session @41
- Fix admin : actionPriority + actions mis à jour localement après publish (compteur instantané)
- rebuildSuivi : suppression `lastBoostDate < todayStr` (cohérence)
- login() : crée DailyBoosts exosDone=0 → admin voit ⏳ En attente

### 14 mars — Session @44
- UX landing quiz : même style que boost
- Post-boost review : indices+formule pré-déployés (_previewHelp)
- Admin 3 onglets (À faire/Traité/Test) + BLOQUÉ section repliable
- Email J+0 HTML branded + archive 📧 Emails GAS
- test_full_v2.py 73/74 (99%)
- Landing : sections fictives supprimées

### 14 mars — Session @45
- Fix stats Progression : score% = complétion (nbExos/total)
- Message reprise chapitre simplifié
- revFInline : fmtL() sur formule avant typewriter
- Commit : ce423ae

### 14 mars — Session @47
- Profil démo Théo Lambert 4EME
- GAS simulate_next_day + bouton 🔮 (si ?sim=1)
- Boost done card : pulsation amber + compteur "dans Xh Ymn"
- Header mobile : "Espace de" ligne séparée
- generate_diagnostic injecte categorie dans chaque exo

### 14 mars — Session @48
- **Nettoyage base prod** : 136 comptes supprimés, toutes données vidées, onglets inutiles supprimés
- Scripts Python archivés (7 scripts)
- audit_complet.md + new_chapters → docs/archive/
- notice-utilisation.md + CLAUDE.md mis à jour
- Commit : f266559

### 12 mars — Session @50
- **Dark mode admin** (toggle, localStorage, 44 règles CSS)
- **Gamif-row hidden** pour admin
- **Modales contextuelles** (BOOST/CHAPITRE séparés/combinés)
- **5 profils réalistes** (Emma/Lucas/Inès/Théo/Chloé)
- **Polish UX** : 9 messages corrigés + animation douce + bandeau guide
- Commits : eab5bef, bf1b2be, 942b0c2

### 15 mars — Session @51
- **Mode Brevet Blanc complet** : fix_lucas_ines.py
- Backend +6 actions (generate_brevet_session, save_brevet_result, publish_admin_brevet, get_brevet_chapters, request_brevet_chapter, import_brevet_exos)
- Onglets BrevetExos + BrevetResults
- brevet_exos_3eme.json : 15 chap × 8 exos = 120 exercices
- import_brevet_exos.py : 120 exos poussés en prod

### 13 mars — Session @52
- **GOD MODE AUDIT — 4 bugs critiques corrigés** :
  1. ExosDone DailyBoosts jamais mis à jour → saveScore incrémente quand source=BOOST
  2. Boost admin daté demain → login() utilise todayStr
  3. login() isAdmin/premium fragiles → vérification robuste (true/TRUE/1/'1')
  4. generateDailyBoost écrit 3 cols → 4 cols avec ExosDone=0
- Audit complet ~10000 lignes, 0 CORS violation

---

## Bugs résolus — index

| Date | Bug | Fix | GAS |
|---|---|---|---|
| 9 mars | Bugs T1→T7 post-tests | Corrigés | @5 |
| 10 mars | generateDailyBoost hors-scope | Corrigé | @10 |
| 11 mars | boostExistsInDB toujours False | Fix format date | @19 |
| 12 mars | Auto-login silencieux KO | Fix localStorage | @24 |
| 12 mars | Quiz inline landing fond cassé | Fix card blanche | @30 |
| 12 mars | Diagnostic "6ème" post-guest | calDone=true + calState=null | @30 |
| 13 mars | showToast → showT() | Fix Brevet/Révision | @31 |
| 13 mars | 4 bugs mineurs | SHEET_ID, Array.find, chkComp, togCat | @31 |
| 13 mars | Quiz CTA invisible | mc rdy class | @38 |
| 13 mars | verifyAdmin TRUE/1 | Corrigé | @34 |
| 13 mars | BOOST TERMINÉ condition | today inclus | @40 |
| 13 mars | Actions admin sans refresh | Corrigé | @41 |
| 13 mars | BOOST TERMINÉ rebuildSuivi | Suppression lastBoostDate < today | @41 |
| 13 mars | Faux BOOST TERMINÉ admin | DailyBoosts exosDone=0 | @41 |
| 14 mars | Stats Progression score% | Complétion au lieu de qualité | @45 |
| 14 mars | Formule LaTeX pill | fmtL() avant typewriter | @45 |
