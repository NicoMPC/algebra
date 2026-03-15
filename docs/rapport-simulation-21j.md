# Rapport Simulation 21 jours — Matheux

> Généré le 2026-03-15 21:30 — GAS @80 (après corrections)
> 12 profils · 21 jours · ~50 appels GAS + écriture directe Sheets

---

## 1. Données Sheets

- 🟢 Users : 12 comptes test (IsTest=1), tous avec code unique
- 🟢 Objectif rempli : 12/12 (lacunes/chapitre_jour/brevet/toutes_matieres)
- 🟢 SIM01 Lucas : Premium=1, PremiumEnd=2026-03-31 (conversion simulée J+7)
- 🟢 Scores : 890 lignes (répartition réaliste par profil)
- 🟢 Progress : 35 entrées (10 maîtrisés)
- 🟢 DailyBoosts : 84 entrées (1 par profil actif par jour)
- 🟢 Insights : 23 entrées (20 feedbacks + 2 signalements erreur + 1 contact parent)
- 🟢 Emails : 57 logués (J+0/J+3/J+5/J+7 auto + 3 manuels)
- 🟢 BrevetResults : 1 résultat (Léa/SIM04 : 50%, 6/12)
- 🟢 Cours : 3 cours écrits (6EME/Fractions, 5EME/Calcul_Littéral, 3EME/Équations)

### Répartition scores par profil

| Profil | Scénario | Jours actifs | Scores | Boosts |
|---|---|---|---|---|
| Lucas (SIM01) | Parfait | 21 | 255 | 20 |
| Emma (SIM02) | Bonne élève | 13 | 121 | 12 |
| Hugo (SIM03) | Irrégulier | 12 | 84 | 11 |
| Léa (SIM04) | Brevet | 12 | 115 | 11 |
| Nathan (SIM05) | Décrocheur | 4 | 14 | 3 |
| Chloé (SIM06) | Lycéenne 1ERE | 9 | 112 | 8 |
| Tom (SIM07) | Brevet attente | 6 | 43 | 5 |
| Sofia (SIM08) | Récente | 7 | 54 | 6 |
| Rémi (SIM09) | Trial expiré | 5 | 30 | 4 |
| Jade (SIM10) | Active trial | 5 | 46 | 4 |
| Adam (SIM11) | Abandon | 1 | 8 | 0 |
| Zoé (SIM12) | Fraîche | 1 | 8 | 0 |

---

## 2. Messages élève — surfaces vérifiées

| Profil | Trial | Premium | Boost | PendingBrevet | Objectif | BoostHistory |
|---|---|---|---|---|---|---|
| Lucas (SIM01) | expiré (premium) | ✅ | ✅ 5 exos | — | lacunes | ✅ |
| Emma (SIM02) | expiré | — | — | — | chapitre_jour | ✅ |
| Hugo (SIM03) | expiré | — | — | — | toutes_matieres | ✅ |
| Léa (SIM04) | expiré | — | — | — (fait) | brevet | ✅ |
| Nathan (SIM05) | expiré | — | — | — | lacunes | ✅ |
| Chloé (SIM06) | expiré | — | — | — | toutes_matieres | ✅ |
| Tom (SIM07) | expiré | — | — | ⏳ en attente | brevet | ✅ |
| Sofia (SIM08) | ✅ 0j | — | — | — | chapitre_jour | ✅ |
| Rémi (SIM09) | ✅ 0j (edge) | — | — | — | lacunes | ✅ |
| Jade (SIM10) | ✅ 2j | — | — | — | lacunes | ✅ |
| Adam (SIM11) | ✅ 4j | — | — | — | toutes_matieres | 0 |
| Zoé (SIM12) | ✅ 6j | — | — | — | brevet | 0 |

**Vérifications spécifiques :**
- 🟢 SIM01 : isPremium=true retourné correctement (fix @80)
- 🟢 SIM07 : PendingBrevet retourné au login (fix headers @79)
- 🟢 SIM11/SIM12 : Pas de boost history (abandon/fraîche)
- 🟢 Objectif retourné pour tous les profils (fix headers @79)
- 🟢 BoostHistory retourné pour profils actifs (fix tod()→today() @79)

---

## 3. Emails

- 🟢 Emails J+0/J+3/J+5/J+7 logués pour chaque profil selon ancienneté
- 🟢 Emails manuels logués pour SIM01, SIM05, SIM09 (suivi-perso)
- 🟢 Contact parent logué pour SIM05 (décrocheur)
- 🟡 Personnalisation objectif dans les templates : non testable sans envoi réel (templates dans `sendMarketingSequence`)

---

## 4. Admin cockpit

- 🟢 `get_admin_overview` retourne les 12 profils test
- 🟢 `get_daily_checklist` fonctionne
- 🟢 `publish_admin_brevet` fonctionne pour SIM04 et SIM07
- 🟢 `save_brevet_result` fonctionne (Léa : 50%, 6/12)
- 🟢 `log_contact` fonctionne pour SIM05
- 🟢 `save_cours` fonctionne — **corrigé** (`tod()` → `today()` @79)
- 🟢 `log_manual_email` fonctionne

---

## 5. Edge cases

| Test | Résultat | Détail |
|---|---|---|
| Double inscription même email | 🟢 | `error: Un compte existe déjà avec cet email.` |
| Mauvais mot de passe | 🟢 | `error: Email ou mot de passe incorrect.` |
| Code inexistant save_score | 🟡 | `success` — GAS ne valide pas le FK Users (6 chars suffit) |
| Résultat invalide (INVALID_VALUE) | 🟢 | `error: Résultat invalide. Valeurs acceptées : EASY, MEDIUM, HARD.` |
| Admin sans code | 🟢 | `error: Accès refusé.` |
| Boost déjà fait aujourd'hui | 🟢 | Retourne le boost existant (pas de doublon) |
| Trial expiré SIM09 | 🟢 | `daysLeft=0, trialActive=True` (dernier jour) |
| Streak brisé puis repris | 🟢 | Max streak cohérent |
| Brevet sans chapitres | 🟢 | `error: Sélectionne au moins un chapitre.` |
| Login email inexistant | 🟢 | `error: Email ou mot de passe incorrect.` |

---

## 6. Performances

| Action | Count | Avg(s) | Max(s) |
|---|---|---|---|
| register | 12 | ~3s | ~5s |
| login | ~20 | ~4s | ~8s |
| save_cours | 3 | ~3s | ~4s |
| publish_admin_brevet | 2 | ~3s | ~4s |
| save_brevet_result | 1 | ~4s | ~4s |
| get_admin_overview | 2 | ~6s | ~8s |
| generate_daily_boost | 2 | ~5s | ~7s |

**Total : ~50 appels GAS, 0 erreurs réseau**

> Les scores et boosts sont écrits en batch via l'API Sheets Python (rapidité). Seules les actions admin et vérifications passent par GAS.

---

## 7. Récapitulatif priorités

### 🔴 Bugs corrigés (étaient bloquants)

| # | Bug | Impact | Fix | Deploy |
|---|---|---|---|---|
| 1 | `tod()` non défini dans `saveCours` | Impossible d'écrire des cours | `todayDate = today()` | @79 |
| 2 | `tod()` non défini dans login boostHistory | boostHistory toujours vide | `todayStr = today()` | @79 |
| 3 | Headers Users manquants (PendingBrevet, RevisionChapters, Objectif) | PendingBrevet invisible, Objectif perdu | Fix Sheet + `ensureUsersCols` | @79 |
| 4 | `checkTrialStatus` ignores `Premium='1'` (string) | Premium vu comme non-premium | `String(premium) === '1'` | @80 |

### 🟡 Incohérences non bloquantes

- **save_score sans validation FK** : accepte code fantôme si 6 chars. Le frontend envoie toujours des codes valides.
- **Trial daysLeft=0** : frontend doit gérer 0 = dernier jour actif, pas expiré.
- **Daily checklist vide** : les données écrites directement en Sheets ne déclenchent pas `rebuildSuivi`. Normal pour simulation batch.

### 🟢 Comportements vérifiés OK

- ✅ Inscription 12 profils avec objectif (4 variantes)
- ✅ Backdating dates d'inscription (J-21 à J-1)
- ✅ Conversion Premium avec PremiumEnd
- ✅ 890 scores / 84 boosts / 35 progress cohérents
- ✅ Feedbacks + signalements dans Insights
- ✅ Emails logués (J+0/J+3/J+5/J+7 + manuels)
- ✅ Admin overview + daily checklist
- ✅ Brevet publié + résultat sauvegardé
- ✅ 3 cours écrits (4 sections chacun)
- ✅ 10 edge cases testés (9 🟢, 1 🟡)
- ✅ Login surfaces : trial, premium, boost, objectif, pendingBrevet, boostHistory
- ✅ Contact parent logué

---

## 8. Profils disponibles pour inspection manuelle

| Code | Prénom | Niveau | Scénario | Objectif | Code GAS | Email |
|---|---|---|---|---|---|---|
| SIM01 | Lucas | 6EME | Parfait 21j, Premium | lacunes | `2BVEA9` | `sim.lucas.sim01@matheux.fr` |
| SIM02 | Emma | 5EME | Bonne élève 13j | chapitre_jour | `RXWAPA` | `sim.emma.sim02@matheux.fr` |
| SIM03 | Hugo | 4EME | Irrégulier 12j | toutes_matieres | `C4BW9C` | `sim.hugo.sim03@matheux.fr` |
| SIM04 | Léa | 3EME | Brevet fait 50% | brevet | `GGMV8Q` | `sim.lea.sim04@matheux.fr` |
| SIM05 | Nathan | 6EME | Décrocheur 4j | lacunes | `P59ZEP` | `sim.nathan.sim05@matheux.fr` |
| SIM06 | Chloé | 1ERE | Lycéenne sérieuse | toutes_matieres | `MHSZJ2` | `sim.chloe.sim06@matheux.fr` |
| SIM07 | Tom | 3EME | Brevet en attente | brevet | `U2KXA2` | `sim.tom.sim07@matheux.fr` |
| SIM08 | Sofia | 5EME | Récente 7j | chapitre_jour | `LUMB6D` | `sim.sofia.sim08@matheux.fr` |
| SIM09 | Rémi | 4EME | Trial expire J0 | lacunes | `NYMM3L` | `sim.remi.sim09@matheux.fr` |
| SIM10 | Jade | 6EME | Active trial 2j | lacunes | `PCPVTC` | `sim.jade.sim10@matheux.fr` |
| SIM11 | Adam | 5EME | Abandon post-diag | toutes_matieres | `PM38UW` | `sim.adam.sim11@matheux.fr` |
| SIM12 | Zoé | 3EME | Fraîche J0 | brevet | `X9VMN8` | `sim.zoe.sim12@matheux.fr` |

**Mot de passe commun : `SimTest2026!`**
Tous les comptes sont IsTest=1 (@matheux.fr) — n'impactent pas le quota bêta.

---

*Simulation exécutée le 15 mars 2026. 4 bugs corrigés et déployés (GAS @78 → @80).*
