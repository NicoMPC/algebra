# Audit cohérence Sheet — Matheux

**Date :** 10/03/2026
**Sheet ID :** `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4`
**GAS URL :** `...AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF...`
**Script :** `run_audit.py` (racine du projet)

---

## Tableau récapitulatif

| Contrôle | Description | Statut |
|----------|-------------|--------|
| C1 | Users → Scores (orphelins) | ⚠️ WARN |
| C2 | Scores → Progress (cohérence) | ✅ OK |
| C3 | Scores → Dashboard | ⚠️ WARN |
| C4 | DiagnosticExos → Curriculum_Officiel | ✅ OK |
| C5 | DailyBoosts → chapitres diagnostiqués | ⚠️ WARN |
| C6 | Simulation compte neuf (GAS) | ✅ OK |

---

## Contrôle 1 — Users → Scores (orphelins)

⚠️ **19 utilisateur(s) sans aucune ligne Scores**

> **Interprétation : normal, non bloquant.**
> Les orphelins se répartissent en 3 catégories :
> - **Comptes de débogage/audit** créés lors des sessions de test : G74D5P, SWH9S5, KLL3KQ, DMSSJB, JW6XRS, ID-BROFCC2TN, ID-6T9R0BP02 — à nettoyer manuellement avant lancement.
> - **Compte admin** : ADMIN1 (Nicolas) — n'a pas vocation à faire des exercices.
> - **Profils de test incomplets** : les 20 élèves fictifs créés le 9 mars ont été partiellement remplis. Seuls 8 profils sur 20 ont des données Scores (ceux du tableau `good/partial/hard`). Les 12 autres (LUC602, ZOE603, NAT604, CHO502, TOM503, INE504, ENZ402, CAM403, THE404, ROM302, MAN303, BAP304) ont été créés dans Users sans données d'exercice.

<details><summary>Détail par élève (nb lignes Scores)</summary>

```
  ID-BROFCC2TN (Noam 4EME)      : 0
  ID-6T9R0BP02 (charlie 3EME)   : 0
  ADMIN1       (Nicolas ADMIN)   : 0
  EMM601       (Emma 6EME)       : 53  ← actif
  LUC602       (Lucas 6EME)      : 0
  ZOE603       (Zoé 6EME)        : 0
  NAT604       (Nathan 6EME)     : 0
  LEA605       (Léa 6EME)        : 23  ← actif
  HUG501       (Hugo 5EME)       : 37  ← actif
  CHO502       (Chloé 5EME)      : 0
  TOM503       (Tom 5EME)        : 0
  INE504       (Inès 5EME)       : 0
  MAT505       (Mathis 5EME)     : 23  ← actif
  LOL401       (Lola 4EME)       : 37  ← actif
  ENZ402       (Enzo 4EME)       : 0
  CAM403       (Camille 4EME)    : 0
  THE404       (Théo 4EME)       : 0
  SAR405       (Sarah 4EME)      : 23  ← actif
  JAD301       (Jade 3EME)       : 37  ← actif
  ROM302       (Romain 3EME)     : 0
  MAN303       (Manon 3EME)      : 0
  BAP304       (Baptiste 3EME)   : 0
  OCE305       (Océane 3EME)     : 37  ← actif
  JW6XRS       (NICOLAS 3EME)    : 0
  G74D5P       (AuditTest 6EME)  : 0   ← compte audit
  SWH9S5       (AuditTest 6EME)  : 0   ← compte audit
  KLL3KQ       (AuditTest 6EME)  : 0   ← compte audit
  DMSSJB       (AuditTest 6EME)  : 3   ← compte audit (scores de simulation)
  QWM3N7       (AuditTest 6EME)  : 3   ← compte audit (scores de simulation)
```
</details>

**Action à prendre avant lancement :** supprimer les lignes AuditTest (G74D5P, SWH9S5, KLL3KQ, DMSSJB, QWM3N7) et les IDs temporaires (ID-*) des onglets Users, DailyBoosts, Scores, Progress.

---

## Contrôle 2 — Scores → Progress (cohérence)

✅ **41 paires (code, chapitre) dans Scores | 41 lignes Progress | 0 paires manquantes | 0 scores aberrants**

Toutes les paires (élève × chapitre) présentes dans Scores ont bien une ligne correspondante dans Progress. Aucun score hors de la plage 0–100. La synchronisation `save_score` → `updateConfidenceScore` → Progress fonctionne parfaitement.

---

## Contrôle 3 — Scores → Dashboard

⚠️ **12 élèves avec entrée Dashboard / 9 manquants**

> **Interprétation : non bloquant — onglet Dashboard non implémenté dans le GAS.**
> L'onglet "Dashboard" existe dans le Sheet mais n'est écrit par aucune action GAS actuelle. Les 9 élèves actifs (ayant des Scores) dont l'email n'est pas dans Dashboard ne subissent aucun dysfonctionnement — cet onglet n'est pas utilisé par le frontend. À surveiller si une vue admin Dashboard est ajoutée.

<details><summary>Élèves actifs absents du Dashboard</summary>

```
  OCE305  oceane.robert@test.fr
  HUG501  hugo.moreau@test.fr
  EMM601  emma.martin@test.fr
  LOL401  lola.david@test.fr
  JAD301  jade.michel@test.fr
  MAT505  mathis.girard@test.fr
  SAR405  sarah.laurent@test.fr
  LEA605  lea.simon@test.fr
  DMSSJB  audit_test_1773135073@test.fr  ← compte audit
```
</details>

---

## Contrôle 4 — DiagnosticExos → Curriculum_Officiel

✅ **24/24 paires (Niveau, Categorie) vérifiées — 0 absentes de Curriculum_Officiel**

Tous les chapitres présents dans DiagnosticExos existent bien dans Curriculum_Officiel. La cohérence entre les deux onglets est totale — le diagnostic peut pointer vers n'importe lequel des 24 chapitres et trouver les exercices correspondants.

---

## Contrôle 5 — DailyBoosts → chapitres diagnostiqués

⚠️ **46 boosts analysés | 101 exos dans scope | 54 exos hors-scope**

> **Interprétation : comportement intentionnel du fallback, non bloquant.**
> Le GAS `generateDailyBoost` a deux modes :
> 1. **Mode ciblé** (élève avec erreurs récentes) : pioche dans les chapitres HARD de l'élève → exos dans scope.
> 2. **Mode fallback** (pas d'erreurs récentes ou compte neuf) : pioche dans Curriculum_Officiel un pool varié → exos potentiellement hors scope.
>
> Les 54 exos hors-scope appartiennent tous à des comptes sans erreurs récentes (8FNJL7, E2GVTR, B2M6NH, 49RUYR, MDYSTE, NS8HY4 — profils de test "good" ou comptes audit). C'est exactement le fallback documenté dans CLAUDE.md. Pour les élèves avec des HARD réels, les boosts sont correctement ciblés (101 exos in-scope).
>
> Amélioration possible (non urgente) : n'enregistrer un boost que si l'élève a des erreurs récentes, sinon retourner un boost "entraînement libre" sans le sauvegarder dans DailyBoosts.

<details><summary>Détail des 30 premiers exos hors-scope</summary>

```
  8FNJL7: _cat='Fractions'            absent des Scores
  8FNJL7: _cat='Calcul_Littéral'      absent des Scores
  8FNJL7: _cat='Pythagore'            absent des Scores
  8FNJL7: _cat='Fractions'            absent des Scores
  8FNJL7: _cat='Calcul_Littéral'      absent des Scores
  E2GVTR: _cat='Proportionnalité'     absent des Scores
  E2GVTR: _cat='Équations'            absent des Scores
  E2GVTR: _cat='Pythagore'            absent des Scores
  E2GVTR: _cat='Pythagore'            absent des Scores
  E2GVTR: _cat='Équations'            absent des Scores
  B2M6NH: _cat='Théorème_de_Thalès'   absent des Scores
  B2M6NH: _cat='Théorème_de_Thalès'   absent des Scores
  B2M6NH: _cat='Statistiques'         absent des Scores
  B2M6NH: _cat='Équations'            absent des Scores
  B2M6NH: _cat='Équations'            absent des Scores
  49RUYR: _cat='Fractions'            absent des Scores
  49RUYR: _cat='Calcul_Littéral'      absent des Scores
  49RUYR: _cat='Fractions'            absent des Scores
  49RUYR: _cat='Puissances'           absent des Scores
  49RUYR: _cat='Calcul_Littéral'      absent des Scores
  MDYSTE: _cat='Puissances'           absent des Scores
  MDYSTE: _cat='Fractions'            absent des Scores
  MDYSTE: _cat='Fractions'            absent des Scores
  MDYSTE: _cat='Pythagore'            absent des Scores
  MDYSTE: _cat='Proportionnalité'     absent des Scores
  NS8HY4: _cat='Calcul_Littéral'      absent des Scores
  NS8HY4: _cat='Proportionnalité'     absent des Scores
  NS8HY4: _cat='Calcul_Littéral'      absent des Scores
  NS8HY4: _cat='Pythagore'            absent des Scores
  NS8HY4: _cat='Fractions'            absent des Scores
```
</details>

---

## Contrôle 6 — Simulation compte neuf (GAS)

✅ **Flux complet validé | compte test : QWM3N7**

Email test : `audit_test_1773135207@test.fr`
Compte à supprimer manuellement du Sheet après lecture.

| Étape | Statut | Résultat |
|-------|--------|----------|
| 6.1 register | ✅ OK | `{"status":"success","profile":{"code":"QWM3N7","name":"AuditTest","level":"6EME","isAdmin":false,"premium":false}}` |
| 6.2 login | ✅ OK | code=QWM3N7 récupéré, curriculumOfficiel retourné |
| 6.3 generate_diagnostic | ✅ OK | 4 exos retournés (2 chap × 2 lvl = 1 lvl1 + 1 lvl2 par chapitre) |
| 6.4 save_score × 3 | ✅ OK | 3/3 scores sauvés (EASY, HARD, EASY sur Nombres_entiers) |
| 6.5 generate_daily_boost | ✅ OK | 5 exos boost retournés |
| 6.6 save_boost | ✅ OK | `{"status":"success"}` |
| 6.7 vérif Sheet | ✅ OK | 3 Scores + 1 Progress + 2 DailyBoosts trouvés pour ce code |
| 6.8 nettoyage | ℹ️ INFO | Compte laissé dans le Sheet — suppression manuelle requise |

**Note technique découverte :** le GAS `save_score` attend les champs `name` / `level` / `exercice_idx` (et non `prenom` / `niveau` / `numExo`). Le frontend v23 envoie les bons champs — aucun bug actif. La divergence était dans la documentation CLAUDE.md uniquement.

---

## Actions recommandées

| Priorité | Action |
|----------|--------|
| Avant lancement | Supprimer les comptes audit du Sheet : G74D5P, SWH9S5, KLL3KQ, DMSSJB, QWM3N7 + comptes ID-* |
| Avant lancement | Compléter ou supprimer les 12 profils de test sans Scores (LUC602, ZOE603, etc.) |
| Non urgent | Implémenter l'écriture Dashboard dans GAS si une vue admin est prévue |
| Non urgent | Conditionner l'enregistrement DailyBoosts à la présence d'erreurs récentes (évite les boosts hors-scope) |

---

*Généré par `run_audit.py` le 10/03/2026 — audit complet Sheet + simulation GAS live*
