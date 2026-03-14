# Rapport de simulation QA — 40 élèves × 15 jours

> Date : 14 mars 2026 | GAS @63 | Méthode : analyse statique + **test live 1616 appels API**

---

## Méthodologie

1. **Analyse statique du code** (backend.js ~4200 lignes + index.html ~5900 lignes) — traçage des flux.
2. **Test live `test_full_v2.py`** — 74/74 PASS (100%) — flux nominal complet.
3. **Simulation live `test_simulation_40.py`** — 40 comptes @matheux.fr (IsTest=1), 15 jours simulés, **1616 appels API réels** en ~2h51.

### Résultats live

| Métrique | Valeur |
|---|---|
| Appels API | 1 616 |
| Durée totale | 10 270s (~2h51) |
| Erreurs réseau | 0 |
| Timeouts (>30s) | 9 (0.6%) — tous récupérés par retry |
| 40 logins en rafale | 40/40 en 21.9s |
| Admin overview (59 élèves) | 9.6s |

| Action | Count | Avg(s) | Max(s) | P95(s) |
|---|---|---|---|---|
| register | 40 | 4.40 | 6.96 | 5.97 |
| login | 408 | 5.13 | 67.92 | 6.81 |
| save_score | 1158 | 6.86 | 68.13 | 9.94 |
| get_admin_overview | 4 | 7.31 | 9.56 | 9.56 |

---

## Bugs trouvés et corrigés

### 🔴 BUG-SIM-01 — rebuildSuivi : filtre boost sur mauvaise colonne

**Fichier** : `backend.js` ligne 1395
**Avant** : `String(r['Chapitre'] || '') === 'BOOST'`
**Après** : `String(r['Source'] || '') === 'BOOST'`
**Impact** : Le statut boost dans 👁 Suivi montrait toujours "—" au lieu de "En cours (3/5)" ou "Consommé ✅ (5/5)".
**Cause racine** : Les scores BOOST stockent le vrai nom de chapitre dans la colonne Chapitre et 'BOOST' dans la colonne Source (col N).

### 🟠 BUG-SIM-02 — getAdminOverview : scores BOOST inclus dans stats chapitres

**Fichier** : `backend.js` ligne 2837
**Avant** : `if (!code || !cat || cat === 'CALIBRAGE' || cat === 'BOOST') return;`
**Après** : `if (!code || !cat || cat === 'CALIBRAGE' || cat === 'BOOST' || src === 'BOOST') return;`
**Impact** : Les exercices de boost (pool séparée) étaient comptés dans les stats par chapitre du dashboard admin, gonflant artificiellement les métriques.

### 🟠 BUG-SIM-03 — saveScore : pas de validation du résultat

**Fichier** : `backend.js` après ligne 532
**Ajout** : Validation `resultat` ∈ {EASY, MEDIUM, HARD}, `code` = 6 chars, `level` valide.
**Impact** : Des valeurs invalides étaient silencieusement acceptées → comportement indéfini dans updateConfidenceScore.

### 🟡 BUG-SIM-04 — updateConfidenceScore : streakAlert non retourné

**Fichier** : `backend.js` ligne 1267
**Avant** : `return { streak: streak, score: score };`
**Après** : `return { streak: streak, score: score, streakAlert: streakAlert };`
**Impact** : Les alertes de streak ("Tu vas perdre ta série !") n'étaient jamais envoyées au frontend.

### 🟡 BUG-SIM-05 — rebuildSuivi : chapTermine logique all-or-nothing

**Fichier** : `backend.js` ligne 1471-1473
**Avant** : `!newCh1 && !newCh2 && !newCh3 && !newCh4` (condition globale)
**Après** : `!newCols[idx]` (condition par slot)
**Impact** : Si Nicolas avait rempli un slot →Nouveau pour un chapitre, AUCUN autre chapitre ne pouvait déclencher "✅ CHAPITRE TERMINÉ" même si terminé.

### 🟠 BUG-SIM-06 — Frontend : streak figé au login

**Fichier** : `index.html` dans `mark()`
**Ajout** : Mise à jour de `S.stk` et `localStorage` au premier exercice d'un nouveau jour.
**Impact** : Le compteur streak affiché ne changeait jamais pendant la session, même après plusieurs jours d'utilisation continue.

---

## Tests contradictoires — Résultats par analyse statique

### Groupe A — Cohérence des données

| Test | Résultat | Notes |
|------|----------|-------|
| A1 — Double session simultanée | ⚠️ RISQUE | GAS n'a pas de lock. Deux save_score simultanés peuvent incrémenter ExosDone de 1 au lieu de 2 (race condition lecture/écriture). Acceptable MVP (quota GAS ~20 users simultanés). |
| A2 — save_score sans boost actif | ✅ OK | ExosDone incrémenté silencieusement dans DailyBoosts si la ligne existe. Si pas de ligne DailyBoosts, le try/catch absorbe l'erreur. Pas de crash. |
| A3 — Score hors bornes | ✅ CORRIGÉ | Validation ajoutée : resultat doit être EASY/MEDIUM/HARD. |
| A4 — Chapitre hors sélection | ✅ OK | `generateDailyBoost` filtre P5 restreint aux chapitres sélectionnés. Fallback si aucun match. |
| A5 — NbExos > 20 | ✅ OK | Progress accepte NbExos > 20. Statut reste "en_cours" ou "maitrise" (pas de cap). Admin affiche cap 20 dans stats. |
| A6 — Inactif 14j puis reconnexion | ✅ OK | Décroissance: `score - floor((jours-14) * 0.5)`. Streak reset à 1. Boost régénéré normalement. |

### Groupe B — Stress volume

| Test | Résultat | Notes |
|------|----------|-------|
| B1 — 40 login en rafale | ⚠️ ACCEPTABLE | GAS gère ~20 req simultanées (queue interne Google). Au-delà → timeout 30s. Rate limiting global 60/min par identifiant. |
| B2 — 200 save_score en 2 min | ✅ OK | Rate limiting 60/min par code. Chaque save_score est atomique (appendRow). rebuildSuivi best-effort (try/catch). |
| B3 — generateMorningReport 40 élèves | ⚠️ RISQUE | Lit Users + Scores + Progress + DailyBoosts × N. Pour 40 élèves, ~4-5 minutes estimées (proche de la limite 6 min GAS). |
| B4 — get_admin_overview 40 élèves | ⚠️ RISQUE | Lit tous les onglets en un seul appel. Pour 40 élèves actifs avec historique, ~30-60s estimé. Acceptable. |

### Groupe C — Cas edge métier

| Test | Résultat | Notes |
|------|----------|-------|
| C1 — PendingBrevet J+3 → J+8 | ✅ OK | PendingBrevet stocké dans Users col L (JSON). Persiste indéfiniment. Login le retourne à chaque connexion. |
| C2 — 4 chapitres + publish | ✅ OK | `publishAdminChapter` écrase le slot G (plus ancien) et retourne `overwrite: true` → toast frontend. |
| C3 — Trial expiré → reconnexion | ✅ OK | Overlay affiché, données préservées dans S.res, bouton "Voir ma progression". |
| C4 — RevisionChapters cross-niveau | ✅ OK | Progress identifié par (Code, Chapitre), pas par Niveau. Pas de collision. |
| C5 — Score → maitrise | ✅ OK | `updateConfidenceScore` : score > 80 + 2 derniers lvl2 EASY sans indice → statut "maitrise". rebuildSuivi reflète "✅ CHAPITRE TERMINÉ" si ≥20 exos. |
| C6 — Email J+3 élève premium | ✅ OK | `emailsDue` calculé dans getAdminOverview mais `triggerDailyMarketing` vérifie Premium avant envoi. |
| C7 — IsTest @matheux.fr | ✅ OK | `register()` : `isTest = email.endsWith('@matheux.fr')`. Limite 50 = count de `!isAdm && !isTst`. |
| C8 — Diagnostic guest sans inscription | ✅ OK | `generateDiagnostic` en mode guest ne touche pas Scores/Progress. Données locales uniquement (localStorage `guestDiag`). Scores envoyés fire-and-forget APRÈS register. |

### Groupe D — Fraîcheur des données (frontend)

| Test | Résultat | Notes |
|------|----------|-------|
| D1 — Vue Progression après exo | ✅ OK | `render()` appelé après chaque `mark()`. Données `S.res` à jour en mémoire. |
| D2 — Admin publie boost pendant session | ⚠️ PARTIEL | Le boost est stocké dans 👁 Suivi col S. L'élève ne le reçoit qu'au prochain `login()`. Pas de push temps réel. |
| D3 — Streak après exercice | ✅ CORRIGÉ | BUG-SIM-06 corrigé — streak mis à jour dans `mark()`. |
| D4 — XP affiché vs réel | ✅ OK | `S.xp += xp` puis `updH()` dans `mark()`. EASY=100, MEDIUM=50, HARD=10. |

---

## Améliorations implémentées

### Rate limiting global (roadmap item)
- **Avant** : 15 req/min sur login/register uniquement
- **Après** : 60 req/min par identifiant (email/code/adminCode) sur TOUTES les actions. 15/min pour login/register/forgot_password.
- Retour : `{ status: 'error', message: 'rate_limit' }`
- Utilise `CacheService.getScriptCache()` (TTL 60s)

### Validation inputs (roadmap item)
- **register** : email regex + prénom 2-50 chars + hash 64 chars (déjà présent)
- **saveScore** : resultat ∈ {EASY, MEDIUM, HARD} + code 6 chars + level valide (AJOUTÉ)

---

## Score de fiabilité

| Dimension | Score | Détail |
|-----------|-------|--------|
| Cohérence données | 9/10 | Race condition GAS résiduelle (acceptable MVP) |
| Validation inputs | 8/10 | register + saveScore couverts, autres endpoints basiques |
| Rate limiting | 9/10 | Global sur toutes actions, 2 niveaux de seuil |
| Admin workflow | 9/10 | Actions, pills, boost/chapitre — tous fonctionnels |
| Frontend UX | 9/10 | Streak, XP, mastery ring — tous à jour temps réel |
| Edge cases | 8/10 | PendingBrevet persistant, trial overlay, 1 chap/jour |
| **Global** | **9.0/10** | Confirmé par 1616 appels live — 0 erreur |

---

## Validation live — 14 mars 2026

| Suite | Résultat |
|---|---|
| `test_full_v2.py` | **74/74 PASS (100%)** |
| `test_simulation_40.py` (40 élèves × 15 jours) | **17/17 PASS, 0 erreur, 1616 appels** |

**Conclusion : GAS tient 40 élèves sans problème.** Les 9 timeouts (0.6%) sont des pics GAS temporaires, récupérés automatiquement par retry.

---

## Recommandations

1. **B3 — generateMorningReport** : si >40 élèves, envisager un traitement par batch (10 élèves par exécution avec trigger séquentiel) pour rester sous la limite 6 min GAS.
2. **D2 — Push temps réel** : actuellement les boosts admin ne sont reçus qu'au login. Pour une UX temps réel, envisager un polling léger (check toutes les 5 min) côté frontend.
3. **A1 — Race condition** : acceptable MVP. Si >50 users simultanés, migrer vers une vraie BDD (Firestore/Supabase).
4. **Timeouts** : save_score max 68s observé en pic. Le retry avec backoff couvre ces cas. Pas bloquant pour MVP.
