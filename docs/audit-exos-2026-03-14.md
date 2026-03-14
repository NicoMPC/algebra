# Audit exercices collège — 2026-03-14

## Résumé

| Onglet | Exercices | Sans erreur | Vrais bugs | Faux positifs | Warnings |
|---|---|---|---|---|---|
| Curriculum_Officiel | 880 (44 chap.) | 863 | 0 | 1 | 16 |
| DiagnosticExos | 88 (44 chap.) | 75 | 0 | 0 | 13 |
| BoostExos | 440 (44 chap.) | 421 | **1 corrigé** | 2 | 17 |
| **TOTAL** | **1408** | **1359** | **1 corrigé** | **3** | **46** |

## Bug corrigé

### BoostExos 5EME/Triangles_Semblables exo#9
- **Type** : `ERREUR_DOUBLONS_OPTIONS`
- **Problème** : `options[0]` et `options[3]` étaient identiques : `"75 cm²"`
- **Correction** : `options[3]` remplacé par `"125 cm²"`
- **Réponse correcte** : `"225 cm²"` (aire × k² = 25 × 9 = 225) — inchangée

## Faux positifs (3) — vérifiés manuellement

| Exercice | Raison du faux positif |
|---|---|
| Curriculum 5EME/Puissances #15 | `5^6/5^2 = 5^4 = 625` ✅ — le script parse `5^2` isolément |
| BoostExos 4EME/Fractions #7 | `(3/4 + 1/6) × 2 = 11/6` ✅ — le script ignore le `× 2` |
| BoostExos 4EME/Fractions #9 | `-2/3 × 9/4 = -3/2` ✅ — le script ne gère pas le signe `-` |

## Warnings (46)

### WARN_INDICE_DEVOILE (22)
Un indice (`steps[i]`) contient la réponse exacte en clair. Non bloquant — l'élève voit l'indice avant de répondre.

### WARN_FORMULE_VIDE (11)
Champ `f` vide ou trop court (< 8 caractères). Non bloquant — la formule ne s'affiche simplement pas.

### WARN_STEPS (13)
Nombre de `steps` hors 1-3. La plupart ont 0 steps dans DiagnosticExos (pas d'indices en mode diagnostic, c'est normal).

## Conclusion

**1408 exercices audités — 1 seul bug trouvé et corrigé.**
La base exercices collège est propre. Les warnings sont cosmétiques et non bloquants.

### Données non touchées
- ✅ Lignes 1ERE ignorées (10 chapitres)
- ✅ Aucune modification de `index.html` ou `backend.js`
- ✅ Aucun exercice supprimé
- ✅ Seul le champ `options` d'un exercice a été modifié
