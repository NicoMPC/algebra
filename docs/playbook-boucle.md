# Playbook — Boucle quotidienne

> Domaine : login, boost du jour, exercices, XP, streak, daily goal, timer, messages, coach tips.
> Déclencheurs : "le boost arrive pas", "les scores sont faux", "le message est bizarre", "l'XP compte pas", "le streak a reset"

> ⚠️ **Depuis 02/04/2026** : l'API est Supabase Edge Functions (`index.ts`). Les références `backend.js` / lignes GAS sont legacy (emails uniquement).

---

## User flow

```
Login → get_progress → chargement état
  → Hero CTA (cascade P1→P5, exactement 1)
  → Boost du jour (5 exos ciblés sur lacunes)
  → Réponse → validation → XP + streak + daily goal
  → Complétion boost → +200 XP → message anticipation J+1
  → (Si pas de boost aujourd'hui → rattrapage P9)
```

## Fonctions clés

| Étape | Frontend (index.html) | Backend (backend.js) | Sheet |
|---|---|---|---|
| Login | `initApp()` L.4635 | `login()` L.359 | Users, Scores, DailyBoosts, Suivi, Progress |
| Hero CTA | cascade L.7920-8120 | — | — |
| Boost affichage | `handleBoost()` L.5355, `loadBoost()` L.5172 | `generateDailyBoost()` L.991 | DailyBoosts, BoostExos |
| Réponse | `validateAnswer()` L.5457, `mark()` L.5500 | `saveScore()` L.665 | Scores, DailyBoosts.ExosDone |
| Complétion | `chkComp('BOOST')` L.5688 | — | — |
| Rattrapage | — | login L.415-440 (fallback boost non terminé) | DailyBoosts |

## Checklist diagnostic

1. **Boost pas affiché** → Vérifier DailyBoosts a une ligne pour cet élève. Si pas de boost aujourd'hui, P9 doit servir le dernier non terminé (ExosDone < 5). Vérifier `boostExistsInDB` dans la réponse login.
2. **Boost "consommé" alors que pas fait** → M3 : vérifier `boostConsumedDate` dans localStorage `done_v23`. Expire si `!== tod()`. Vider le localStorage de l'élève si stale.
3. **Score pas enregistré** → Vérifier `saveScore()` ne timeout pas (LockService 10s). Vérifier `S.scoreQueue` (flush retry). Vérifier réseau (flushQ backoff).
4. **XP incorrect** → G1 : +200 boost complet, +75 par slot, +50 daily goal. Mode flow (G13) double les XP exercices. Vérifier `S._flowActive`.
5. **Streak reset** → Vérifier `boost_loc_v23` dans localStorage. Logique : hier=continue, avant-hier+stk≥2=freeze (1/semaine), sinon reset à 1.
6. **Message hors contexte** → Vérifier `_nudgeTimers` (fix C1 : clearNudge dans render()). Vérifier `_needsCoach()` / `_markCoach()` dans `mx_co_{code}`.
7. **Toast doublon** → M1 : `_toastBusy` + `_toastQueue`. Vérifier qu'il n'y a pas de `showT()` sans passer par le mutex.
8. **Hero CTA absent ou double** → M2 : cascade P1→P5. Chaque niveau a `if(!_hero) break`. Vérifier que le fallback DONE existe.
9. **Daily goal ne compte pas** → G8 : vérifier `mx_daily_{code}` localStorage. Reset si `date !== tod()`. Absorbé silencieusement par `chkComp`.
10. **Mode flow ne s'active pas** → G13 : 5 EASY consécutifs en ≤60s. Timer doit être activé. HARD/SKIP/overtime reset le streak flow.

## Points de défaillance connus

| Bug | Cause | Fix | Date |
|-----|-------|-----|------|
| Boost perdu après J+0 | Backend ne servait que le boost du jour | P9 — fallback dernier boost non terminé | 2026-03-22 |
| Toast "Psst indice" hors contexte | Nudge timer 20s pas annulé au changement de vue | C1 — clearNudge dans render() | 2026-03-22 |
| Race condition ExosDone | Deux save_score simultanés | V3 — LockService.tryLock(10000) | 2026-03-20 |
| Scores perdus réseau instable | fetch échoue sans retry | V6 — flushQ retry+backoff | 2026-03-22 |

## Invariants messages (M1-M8)

| # | Règle | Vérification rapide |
|---|---|---|
| M1 | Toast mutex | `_toastBusy` + `_toastQueue` — jamais 2 visibles |
| M2 | Hero CTA exclusif | `if(!_hero) break` — exactement 1 par session |
| M3 | boostConsumed date-stamped | Expire si `!== tod()` |
| M4 | Coach tip vs toast KO | `if/else` exclusif dans `validateAnswer()` |
| M5 | Milestones/Coach namespacés | `mx_ms_{code}` / `mx_co_{code}` |
| M6 | Streak dedup | Login skip si `_stkMileDup` |
| M7 | "demain" | Autorisé dans boost_preparing et bandeaux post-complétion uniquement |
| M8 | pendingManual cleanup | Effacé dans les 3 branches de `nextChapter` |

## Règles CLAUDE.md

P1 (diagnostic avant tout), P2 (boost=5 exos), P8 (scoring tri-niveau), P9 (boost rattrapage), M1-M8, G1 (XP), G4 (milestones), G8 (daily goal), G12 (timer), G13 (mode flow)
