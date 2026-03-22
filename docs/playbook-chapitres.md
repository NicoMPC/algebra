# Playbook — Chapitres & Progression

> Domaine : sélection chapitre, progression 20 exos, slots, complétion, sessions retro, assignation admin.
> Déclencheurs : "le chapitre apparaît pas", "il est bloqué à 15 exos", "les sessions retro sont fausses", "le slot reward s'affiche pas"

---

## User flow

```
Dashboard chapitres (tri : entamés → révision → pas commencés → terminés)
  → Clic chapitre → exercices (QCM/VF/fill)
  → Progression : slots visuels 5/10/15/20 (si ≥20 exos)
  → Comparaison live vs dernier passage (G10)
  → Complétion → overlay récompense + XP
  → Sessions retro : pills par date, dots colorés, exos read-only
  → Admin assigne prochain chapitre → publish_admin_chapter
```

## Fonctions clés

| Étape | Frontend (index.html) | Backend (backend.js) | Sheet |
|---|---|---|---|
| Affichage chapitres | `render()` L.7853 | `login()` (curriculumOfficiel) | Curriculum_Officiel |
| Exercice | `rSection()` L.8527 | — | — |
| Réponse | `validateAnswer()` L.5457, `mark()` L.5500 | `saveScore()` L.665 | Scores, Progress |
| Slot reward | `_checkSlotReward()` L.5251, `_showSlotReward()` L.5270 | — | — |
| Comparaison live | bandeau L.8448 | — | — |
| Complétion | `chkComp()` L.5688 | `updateConfidenceScore()` | Progress |
| Sessions retro | `renderArchiveSection()` L.7137 | — | Scores (historique) |
| Assignation admin | — | `publishAdminChapter()` L.3882 | 👁 Suivi cols.7/10/13/16 |

## Checklist diagnostic

1. **Chapitre pas affiché** → Vérifier `LVL[S.niv].cats[cat]` existe. Vérifier Curriculum_Officiel a des exos pour ce niveau/chapitre. Si chapitre assigné par admin, vérifier colonne Suivi (slots 7/10/13/16).
2. **Bloqué à N exos (pas 20)** → Vérifier Progress sheet : `NbExos` pour ce Code/Chapitre. Vérifier que les exos sont bien dans `LVL[niv].cats[cat]` (20 entrées). Vérifier que `saveScore()` incrémente Progress.
3. **Slot reward pas affiché** → G7 : slots uniquement si chapitre ≥20 exos. Fire à 5/10/15 (pas 20). Count-based pas index-based. Guard dedup `sessionStorage _slotShown_{cat}_{slotNum}`.
4. **Comparaison live absente** → G10 : affiché uniquement si chapitre ouvert + done > 0 + pas terminé + ≥1 passage complet existe.
5. **Chapitre terminé pas détecté par admin** → P10 : tri par DernierePratique puis nbExos décroissant. Si 2 chapitres même date, celui avec ≥20 exos passe en premier.
6. **Sessions retro incorrectes** → G9 : pills par date (boost) ou par passage (chapitre). Score % = EASY/total. Vérifier filtre `source !== 'CALIBRAGE'` (V7).
7. **Nouveau chapitre assigné pas visible** → Vérifier Suivi cols 7/10/13/16 a le JSON. Vérifier que l'élève se reconnecte (injection au login). Vérifier format JSON valide (q, a, options, a ∈ options).

## Slots de 5 (G7) — Détail

| Condition | Comportement |
|---|---|
| Chapitre ≥20 exos | 4 slots visuels (5/10/15/20) |
| Chapitre <20 exos | Pas de slots, +300 XP classique |
| Fire au 5ème/10ème/15ème exo | Overlay +75 XP |
| Fire au 20ème exo | Absorbé par `chkComp` (pas de double) |
| Daily goal simultané | Absorbé dans le slot overlay (+50 XP inclus) |
| Count-based | Fire au Nème exo fait, quel que soit l'ordre |

## Points de défaillance connus

| Bug | Cause | Fix | Date |
|-----|-------|-----|------|
| Chapitre terminé invisible admin | Tri instable DernierePratique | P10 — tri par nbExos décroissant | 2026-03-22 |
| Calibrage polluait sessions retro | Scores CALIBRAGE comptés | V7 — filtre source !== 'CALIBRAGE' | 2026-03-22 |

## Règles CLAUDE.md

P3 (chapitres=20 exos), P4 (tous accessibles), P5 (assignation manuelle), P8 (scoring), P10 (tri stable), G2 (6 paliers maîtrise), G7 (slots de 5), G9 (sessions retro), G10 (comparaison live), G11 (message anticipation)
