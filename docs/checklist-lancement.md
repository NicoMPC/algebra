# Checklist lancement — Matheux · 18 mars 2026

## 1. Config emails (lundi 16 mars — 14h30)

- [x] Boîtes mail créées sur Ionos : contact@, no-reply@, nicolas@ ✅
- [ ] **1.1** Alias Gmail : ajouter `no-reply@matheux.fr` dans seopourvous (SMTP Ionos)
- [ ] **1.2** Vérifier alias visible dans Gmail → Comptes → "Envoyer en tant que"

## 2. Code — fix emails + formulaire contact (lundi 16 mars — 14h50)

- [ ] **2.1** Fix backend L4707 : `from: 'no-reply@matheux.fr'` sur rapport parent hebdo
- [ ] **2.2** Nouvelle action GAS `send_contact` → email à contact@matheux.fr + log onglet Contact
- [ ] **2.3** Formulaire contact dans index.html (style du site, accessible depuis footer)
- [ ] **2.4** Déployer backend : `./deploy.sh "fix emails + formulaire contact"`
- [ ] **2.5** Déployer frontend : `git push origin main`

## 3. Tests (lundi 16 mars — 15h15)

- [ ] **3.1** Créer un compte test → email J+0 reçu ? Expéditeur = `no-reply@matheux.fr` ?
- [ ] **3.2** Mot de passe oublié → email reset reçu ? Expéditeur = `no-reply@matheux.fr` ?
- [ ] **3.3** Formulaire contact → email reçu sur `contact@matheux.fr` ?
- [ ] **3.4** Apps Script → Déclencheurs → liste vide (aucun trigger automatique)

## 4. Stripe (lundi 16 mars — 15h15)

- [ ] **4.1** Stripe Dashboard → Payment Links → ajouter lien CGU (matheux.fr/cgu.html)
- [ ] **4.2** Stripe Dashboard → Payment Links → ajouter lien CGV (matheux.fr/cgv.html)
- [ ] **4.3** Vrai paiement CB (19,99€)
- [ ] **4.4** Vérifier : colonne Premium = 1 dans Users (webhook)
- [ ] **4.5** Vérifier : élève voit statut Premium dans l'app
- [ ] **4.6** Rembourser depuis Stripe Dashboard

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
