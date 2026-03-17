# Checklist lancement — Matheux · 18 mars 2026

## 1. Config emails (lundi 16 mars — 14h30) ✅

- [x] Boîtes mail créées sur Ionos : contact@, no-reply@, nicolas@ ✅
- [x] **1.1** Alias Gmail : `no-reply@matheux.fr` ajouté dans seopourvous (SMTP Ionos port 465 SSL) ✅
- [x] **1.2** Alias visible dans Gmail → Comptes → "Envoyer en tant que" ✅

## 2. Code — fix emails + formulaire contact + merge sécu (lundi 16 mars — 15h) ✅

- [x] **2.1** Fix backend L4707 : `from: 'no-reply@matheux.fr'` sur rapport parent hebdo ✅
- [x] **2.2** Nouvelle action GAS `send_contact` → email à contact@matheux.fr + log onglet Contact ✅
- [x] **2.3** Formulaire contact dans index.html (3 footers : teasing, landing, app) + `_toast()` ✅
- [x] **2.4** Merge sécurité freelance (SECUmain → main) : Stripe webhook MAXIMAL PARANOID + Premium Guard ✅
- [x] **2.5** GitHub Pages reconfiguré sur branche main ✅
- [x] **2.6** Déployer backend (@88) + frontend ✅

## 3. Tests emails (lundi 16 mars — 15h30) ✅

- [x] **3.1** Compte test → email J+0 reçu depuis `no-reply@matheux.fr` ✅
- [x] **3.2** Mot de passe oublié → email reset reçu depuis `no-reply@matheux.fr` ✅
- [x] **3.3** Formulaire contact → email reçu sur `contact@matheux.fr` ✅
- [x] **3.4** Apps Script → Déclencheurs → liste vide (aucun trigger automatique) ✅

## 4. Stripe (lundi 16 mars — 16h) ✅ config

- [x] **4.1** Stripe Payment Link → CGV ajouté ✅
- [x] **4.2** Stripe Payment Link → Politique de confidentialité ajoutée ✅
- [x] **4.3** TVA décochée (art. 293 B CGI — exonéré) ✅
- [x] **4.4** Limite 50 paiements activée sur le Payment Link ✅
- [x] **4.5** Bandeau rappel limite Stripe ajouté dans admin dashboard ✅
- [ ] **4.6** Vrai paiement CB (19,99€) → à tester quand webhook endpoint finalisé
- [ ] **4.7** Vérifier : colonne Premium = 1 dans Users (webhook)
- [ ] **4.8** Vérifier : élève voit statut Premium dans l'app
- [ ] **4.9** Rembourser depuis Stripe Dashboard

## 4b. Tests utilisateur (16-17 mars) ⏳

- [x] **4b.1** Test élève 6EME ✅ (16 mars)
- [x] **4b.2** Test élève 5EME ✅ (16 mars)
- [x] **4b.3** Test élève 4EME ✅ (16 mars)
- [x] **4b.4** Test élève 3EME ✅ (17 mars)
- [x] **4b.5** Fix 27 frictions élève ✅ (17 mars) — 20 initiales + 7 post-test live (exo 1 bloqué, night mode texte, bandeau bienvenue, retro indices, seuil "Bon retour", boost demain, brevet lock)
- [ ] **4b.6** Test admin workflow en conditions → **mardi 17**
- [ ] **4b.7** Test parent parcours complet → **mardi 17**
- [ ] **4b.8** Test admin ergonomie → **mardi 17**

## 5. Vérifs jour J (mercredi 18 mars)

- [ ] **5.1** DNS + HTTPS OK sur matheux.fr
- [ ] **5.2** GA4 reçoit des events (mode debug Chrome)
- [ ] **5.3** Admin HMD493 accessible (triple-clic logo)
- [ ] **5.4** Publier un boost depuis l'admin → visible élève
- [x] Pages légales accessibles depuis footer (5 pages) ✅ + TVA art. 293 B CGI
- [x] Prix 19,99€ cohérent partout ✅ vérifié @83

## 6. Post-lancement J+1

- [ ] Premier vrai boost préparé pour le premier vrai élève
- [ ] Vérifier Suivi Sheets (rebuildSuivi correct)
- [ ] Lire le mail J+0 reçu par le parent

---

## Emails — architecture actuelle et automatisation future

### Aujourd'hui (lancement)

| Email | Mode | Expéditeur |
|---|---|---|
| **J+0 bienvenue** | ✅ Auto (à l'inscription) | no-reply@matheux.fr |
| **Reset mot de passe** | ✅ Auto (forgot_password) | no-reply@matheux.fr |
| **Formulaire contact** | ✅ Auto (envoi à contact@) | no-reply@matheux.fr |
| J+3 / J+5 / J+7 marketing | ❌ Manuel via admin | — |
| Rapport parent hebdo | ❌ Manuel via admin | — |
| Rapport matin Nicolas | ❌ Manuel | — |

### À automatiser plus tard (après 20-30 clients)

| Email | Trigger à créer | Priorité |
|---|---|---|
| **J+3 relance** | `triggerDailyMarketing` → cron 9h-10h | 🟡 Dès 10 clients |
| **J+5 urgence** | idem | 🟡 Dès 10 clients |
| **J+7 conversion** | idem | 🟡 Dès 10 clients |
| **Rapport parent hebdo** | `triggerWeeklyParentReport` → dimanche 17h | 🟡 Dès 20 clients |
| **Rapport matin** | `generateMorningReport` → cron 7h | 🔵 Dès 30 clients |
| **Relance inactifs** | Nouveau trigger à créer | 🔵 Phase 2 |
