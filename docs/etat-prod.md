# État production — Matheux

> Mis à jour le 16 mars 2026 · GAS @83

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

## Taille fichiers clés

| Fichier | Lignes | Taille |
|---|---|---|
| index.html | 9919 | 534K |
| backend.js | 5341 | 240K |

## Derniers déploiements

```
0a9f6c1 feat: bouton "J'ai pas compris" + profil cognitif fiche admin @81
9118806 docs: mise à jour références @77 → @80
d01dd91 fix: 4 bugs GAS corrigés @79-@80 + simulation 21j complète
e8e3ebe feat: send_session_rapport action GAS @78
b89a6a1 seo: retirer 1ère Spé des meta tags — collège uniquement
8974b81 seo: sitemap.xml + robots.txt + meta tags optimisés
bce6376 docs: notice fondateur PDF régénéré @78
218a9fa docs: mise à jour complète @77 — fusion, archive, notice fondateur
78cda66 feat: dark mode app + guide boost fix + titres chapitres gras + boost reopen nav @77
d966c31 docs: audit corrections applied — 39 fixes in Sheets (15 mars 2026)
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
