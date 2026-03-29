# Session validation Johanna (HM9LD7) — 2026-03-27, 19h-20h30

> Première vraie cliente (inscription via Google Ads). Session complète : debug admin, fix backend, régénération exos, audit qualité, nettoyage données.

---

## 1. Master password admin (@120)

Nicolas voulait consulter le dashboard de Johanna sans son mdp.
- Implémenté `ADMIN_MASTER_PWD` dans Script Properties
- Login backend : recalcule `SHA-256(email + '::' + masterPwd + '::AB22')`
- Déployé GAS @120

## 2. Bug critique : admin login consomme les données one-shot (@122)

**Problème** : en se connectant avec le master pwd, le backend a consommé :
- `nextChapter` (Thalès 20 exos) — Suivi col G vidé
- `nextBoost` (5 exos) — DailyBoosts créé

Johanna aurait vu un dashboard vide à sa vraie connexion.

**Fix** : `isAdminLogin = true` quand master pwd utilisé. Skip les 4 mutations :
1. Clear Suivi chapitre (col G)
2. Clear Suivi boost
3. Write DailyBoosts
4. Rebuild Suivi

Déployé GAS @122. Voir aussi V10 dans CLAUDE.md.

## 3. Régénération exercices

Monsieur Exos a regénéré :
- **Chapitre Thalès** : 20 exos (4 slots progressifs)
- **Boost** : 5 exos ciblant le pattern "fausse certitude" (calibrage 50%)

Brief validé par Nicolas. Injecté en brouillon (`draft:true`) puis publié.

## 4. Audit qualité — 6 corrections

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | Champ `f` (formule) manquant sur 25 exos | 🟡 | Ajouté (Thalès direct, réciproque, contexte, racines, probas) |
| 2 | `lvl` non progressif (tous lvl:1) | 🟡 | Corrigé par slot : [1,1,1,1,1], [1,1,1,2,2], [1,1,2,2,2], [1,2,2,2,2] |
| 3 | Steps leakaient la réponse (20/25) | 🟡 | Résultats remplacés par `?` |
| 4 | Exo 20 (phare) : erreur math | 🔴 | Observateur au sommet mais calcul au sol. Remplacé par pylône/ombre |
| 5 | Boost 2 : doublon exact avec chapitre exo 8 | 🔴 | Mêmes valeurs 5/3/10→16. Nouvelles valeurs 4/6/8→20 |
| 6 | Exo 15 : "Jade est sur [AB]" confusion prénom/point | 🟡 | → "$J$ est sur $[AB]$" |
| 7 | Boost 5 : quasi-doublon calibrage (somme 2 dés) | 🟡 | Remplacé par probas complémentaire |

## 5. Nettoyage données

- Supprimé boost parasite dans DailyBoosts (créé par admin login avant le fix @122)
- Vérifié toutes les sheets : Users, Scores, Suivi, DailyBoosts, Progress, Historique, Curriculum, Emails — OK

## 6. Triple audit final (3 agents en parallèle)

| Agent | Résultat |
|---|---|
| Audit exos | 25/25 OK (math, LaTeX, pédagogie, anti-doublon) |
| Audit données | Toutes sheets cohérentes, 0 critique |
| Audit frontend | Parcours complet tracé ligne par ligne, 0 bloquant |

**1 point MOYEN identifié** : hero P2 dit "Commence par" même après reprise partielle (done > 0). Devrait dire "Continue". Ajouté au backlog roadmap.

---

## Lecons apprises

1. **Master password admin DOIT etre read-only** — ne jamais consommer de données one-shot lors d'un login admin
2. **Exercices IA = vérification obligatoire** : champ `f`, lvl par slot, steps sans réponse, math correcte
3. **`nextChapter` est one-shot (fragile)** — fix long terme : sheet `ChapAssigned` (comme DailyBoosts)
4. **Toujours vérifier DailyBoosts après un login admin** — données parasites possibles

## Deployments

- GAS @120 : master password admin
- GAS @122 : admin login read-only (fix consommation one-shot)
