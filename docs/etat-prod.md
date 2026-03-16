# État production — Matheux

> Mis à jour le 16 mars 2026 · GAS @85

## Exercices

| Pool | Chapitres | Exercices | Audit |
|---|---|---|---|
| Curriculum_Officiel | 54 | 1080 | @77 |
| BoostExos | 54 | 540 | @77 |
| DiagnosticExos | 54 | 108 | @77 |
| BrevetExos | 15 | 144 | @77 |
| **Total** | | **1872** | **~98% qualité** |

## Comptes Google Sheets (données réelles)

| Métrique | Valeur |
|---|---|
| Users total | 24 |
| Vrais élèves (IsTest=0, IsAdmin=0) | 11 |
| Comptes test (IsTest=1) | 12 |
| Comptes admin (IsAdmin=1) | 1 |
| Lignes Scores | 1375 |
| Lignes Progress | 63 |
| Lignes DailyBoosts | 114 |

Note : les 11 "vrais élèves" incluent les profils de simulation (SIM01-SIM12) qui ne sont pas marqués IsTest. Base à nettoyer avant lancement réel.

## Actions manuelles restantes avant lancement

1. ~~**Stripe TEST → PROD**~~ — ✅ Fait @82-@83 (16 mars 2026)
2. ~~**contact@matheux.fr**~~ — ✅ Créé (Ionos, 16 mars 2026)
3. **Alias no-reply@matheux.fr** — Gmail → Paramètres → Comptes — ⛔ Non fait
4. **Triggers Apps Script** — triggerDailyMarketing + triggerWeeklyParentReport — ⛔ Non fait
5. **Tester un vrai paiement CB** — ⛔ Non fait
6. **Finaliser endpoint webhook Stripe** — URL GAS + vérifier whsec_ — ⛔ Non fait

## Sécurité

| Couche | Description | Statut |
|---|---|---|
| Security Layer 1 (backend) | Webhook Stripe → Premium auto dans Users + log Webhook_Log | ✅ Code déployé @85 — endpoint Stripe à finaliser |
| Security Layer 2 (frontend) | Premium Guard anti-tampering, vérif toutes les 5 min | ✅ Déployé @84 |

## Taille fichiers clés

| Fichier | Lignes | Taille |
|---|---|---|
| index.html | 9919 | 534K |
| backend.js | 5341 | 240K |

## Derniers déploiements

```
1c702e1 fix: remove shared secret check from webhook @85
4253e7c feat: security layers — Stripe webhook + premium guard @84
9cffac7 docs: TVA art. 293 B CGI + mise à jour checklist/roadmap/etat-prod
2421273 up
5e73cf9 fix: wording teasing — sur mesure, 15 min, IA + prof
720a75d feat: page teasing pré-lancement + waitlist email @82
0a9f6c1 feat: bouton "J'ai pas compris" + profil cognitif fiche admin @81
```

## Scripts disponibles

| Script | Description |
|---|---|
| `test_full_v2.py` | Suite complète — 74/74 (100%) |
| `test_simulation_40.py` | Stress test 40 élèves × 15 jours |
| `sim_21days.py` | Simulation 21j — 12 profils |
| `sim_7days.py` | Simulation 7j — 5 profils |
| `rebuild_sheet.py` | Reconstruit Suivi + Historique |
| `audit_exos.py` | Audit qualité exercices |
| `verify_hints.py` | Audit qualité indices |
| `scripts/setup_test_profiles.py` | Setup profils test admin |
