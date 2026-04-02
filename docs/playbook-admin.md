# Playbook — Admin & Workflow Nicolas

> Domaine : tout ce qui concerne le dashboard admin, le workflow boost/chapitre, les emails parents.
> Déclencheurs : "je vois pas un élève", "l'onglet À FAIRE est vide", "le boost se publie pas", "le mail parent part pas"

> ⚠️ **Depuis 02/04/2026** : l'API est Supabase Edge Functions (`index.ts`). Les références `backend.js` / lignes GAS sont legacy (emails uniquement).

---

## User flow (Nicolas)

```
Triple-clic logo → Dashboard admin
  → Onglet À FAIRE : élèves avec actions (boost terminé, chapitre terminé, bloqué)
  → Onglet NOUVEAU : inscrits du jour (progression J0)
  → Onglet FAIT : journal des actions traitées (today/7j)
  → Onglet MAILS : J+0 à envoyer
  → Onglet INACTIFS : >3j sans activité
  → Onglet RAPPORT : bilans hebdo parents
```

## Fonctions clés

| Fonctionnalité | Frontend (index.html) | Backend (backend.js) | Sheet |
|---|---|---|---|
| Accès admin | `triggerAdmin()` L.2567 | `verifyAdmin()` L.3006 | Users.IsAdmin |
| Dashboard | `renderAdminDashboard()` L.10673 | `getAdminOverview()` L.3033 | Users, Suivi, Scores, DailyBoosts, Progress, Emails |
| Actions élève | `_computeActions()` L.10729 | — | — |
| Publish boost | via modale | `publishAdminBoost()` L.3797 | 👁 Suivi col.S (→Nouveau Boost) |
| Publish chapitre | via modale | `publishAdminChapter()` L.3882 | 👁 Suivi cols.7/10/13/16 |
| Log email | `_ckMarkEmail()` L.11313 | `logManualEmail()` L.4197 | Emails |
| Journal actions | `_ckMarkDone()` L.11339 | — | localStorage mx_admin_journal |

## Classification élèves (_computeActions)

| Rank | Action | Condition |
|---|---|---|
| 2 | ⚡ BOOST TERMINÉ | ExosDone≥5 + pas de boost pending + pas en cours |
| 3 | 📚 CHAPITRE TERMINÉ | chapTermine + chapNewCount=0 |
| — | 👍 RAS | Aucune action requise |

## Checklist diagnostic

1. **Élève invisible dans admin** → Vérifier IsTest dans Users (doit être 0). Vérifier IsAdmin (ne doit pas être 1). Frontend filtre `!st.isTest`.
2. **Chapitre terminé pas détecté** → P10 : vérifier le tri par DernierePratique. Si 2 chapitres même date, celui avec le plus d'exos doit passer en premier.
3. **Boost terminé pas détecté** → Vérifier DailyBoosts.ExosDone ≥ 5. Vérifier qu'aucun boost pending dans Suivi col.S.
4. **Publish boost échoue** → Vérifier JSON valide. Chaque exo doit avoir q, a, options avec a ∈ options.
5. **Publish chapitre échoue** → Vérifier qu'un slot est libre dans Suivi (cols 7/10/13/16).
6. **Journal actions perdu** → `_adminDoneActions` est en mémoire, pas persisté. Normal après refresh. `_adminJournal` est dans localStorage (7j max).

## Points de défaillance connus

| Bug | Cause | Fix | Date |
|-----|-------|-----|------|
| Charlie invisible | Tri instable DernierePratique — chapitre en cours masquait chapitre terminé | P10 — tri par nbExos décroissant en cas d'égalité | 2026-03-22 |

## Règles CLAUDE.md

A1-A5 (admin), P5 (assignation manuelle), P10 (tri stable chapTermine)
