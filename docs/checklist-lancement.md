# Checklist lancement — Matheux · 18 mars 2026

## Bloquant (sans ça pas de vrai client)

- [x] **Stripe TEST → PROD** — ✅ Fait @82 (16 mars 2026)
  - ~~Remplacer lien dans 3 fichiers~~ ✅
  - [ ] Tester un vrai paiement CB

- [ ] **Alias no-reply@matheux.fr**
  - Gmail → Paramètres → Comptes → Ajouter adresse
  - Tester envoi depuis l'admin

- [x] **contact@matheux.fr** — ✅ Fait (16 mars 2026)
  - ~~Créer sur hébergeur Ionos~~ ✅
  - ~~Vérifier que c'est affiché sur le site~~ ✅

- [ ] **Triggers Apps Script**
  - `triggerDailyMarketing` (chaque jour, 9h-10h)
  - `triggerWeeklyParentReport` (dimanche, 17h-18h)

## Important (à vérifier le jour J)

- [ ] DNS + HTTPS OK (A records GitHub + CNAME www)
- [ ] GA4 reçoit des events (mode debug Chrome)
- [ ] Admin HMD493 accessible (triple-clic logo)
- [ ] Publier un boost depuis l'admin → visible élève
- [ ] Email J+0 reçu dans la vraie boîte
- [x] Pages légales accessibles depuis footer (5 pages) — ✅ + mention TVA art. 293 B CGI
- [x] Prix 19,99€ cohérent partout (landing + overlay + CGV + emails) — ✅ vérifié @83

## Post-lancement J+1 (ne pas faire avant)

- [ ] Premier vrai boost préparé pour le premier vrai élève
- [ ] Vérifier Suivi Sheets (rebuildSuivi correct)
- [ ] Lire le mail J+0 reçu par le parent
