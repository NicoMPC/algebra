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
- [x] **4b.5b** Fix final : min 2 chapitres diag + bandeau boost cohérent + polish UI ✅ (17 mars)
- [x] **4b.5c** Fix diagnostic + Boost géo ✅ (17 mars) — 251 figures SVG, 14 reformulations, espaces LaTeX, doublon Systèmes
- [ ] **4b.6** Test admin workflow en conditions → **mardi 17 aprem**
- [x] **4b.7** Test parent parcours complet ✅ (17 mars) — landing → diag → inscription → onboarding → boost → mail J+0 → admin
- [ ] **4b.8** Test admin ergonomie → **mardi 17 aprem**
- [ ] **4b.9** Test réouverture user (Auguste, Charlie, Nicolas) → **mardi 17 soir**

## 5. Vérifs jour J (mercredi 18 mars)

- [ ] **5.1** DNS + HTTPS OK sur matheux.fr
- [ ] **5.2** GA4 reçoit des events (mode debug Chrome)
- [ ] **5.3** Admin HMD493 accessible (triple-clic logo)
- [ ] **5.4** Publier un boost depuis l'admin → visible élève
- [x] Pages légales accessibles depuis footer (5 pages) ✅ + TVA art. 293 B CGI
- [ ] ~~Prix 19,99€ cohérent partout ✅ vérifié @83~~ **⛔ FAUX** — cgu.html dit 9,99€ (L54), premium.html dit 9,99€ (L6/141/173). À corriger.

## 5b. Audit pré-lancement — 17 mars 2026 (Claude)

### ⛔ BLOQUANTS (avant GO LIVE)
- [ ] **5b.1** Fix prix cgu.html L54 : 9,99€ → 19,99€
- [ ] **5b.2** Fix prix premium.html L6/141/173 : 9,99€ → 19,99€
- [ ] **5b.3** Supprimer alerte "bêta fermée 40 familles" dans cgu.html L43-45

### 🔴 CRITIQUES (avant J+7)
- [ ] **5b.4** Webhook Stripe : implémenter vérif HMAC-SHA256 (`stripe-signature` header) — actuellement seul check = `metadata.secret === 'MATHEUX_STRIPE_2026'` en clair
- [ ] **5b.5** Déplacer `SHARED_SECRET` de backend.js L5404 vers `PropertiesService.getScriptProperties()`
- [ ] **5b.6** Fix `triggerDailyMarketing()` L4635 : ajouter `String(premium) === '1'` pour ne pas relancer les payants

### 🟡 IMPORTANTS (sprint 1 post-lancement)
- [ ] **5b.7** Avertissement progressif trial expiry (toast J-3/J-2/J-1 avant overlay bloquant)
- [ ] **5b.8** Unifier messages boost : "demain" vs "bientôt" → un seul message clair
- [ ] **5b.9** Inverser ordre boutons : "Valider" en bas (sticky) > "Je ne sais pas" au-dessus
- [ ] **5b.10** Audit mode nuit : vérifier texte blanc sur fond clair sur tous éléments `.app-night`
- [ ] **5b.11** KaTeX fallback : 3s → 1.5s + spinner "Chargement maths..."
- [ ] **5b.12** Fix manifest.json : copier scree.png à la racine ou supprimer la ref
- [ ] **5b.13** Supprimer ou mettre à jour premium.html (page orpheline, bouton Stripe commenté)

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
