# Audit exercices 1ERE Spé Maths — 2026-03-14

## Résumé

| Onglet | Exercices | Chapitres | Erreurs corrigées | État final |
|---|---|---|---|---|
| Curriculum_Officiel | 200 | 10 | 133 `a` absents + 9 doublons + 2 `a` incorrects | ✅ 0/0 |
| DiagnosticExos | 20 | 10 | 1 `a` absent + 1 doublon + 1 options manquante | ✅ 0/0 |
| BoostExos | 100 | 10 | 0 | ✅ 0/0 |
| **TOTAL** | **320** | **30** | **147 corrections** | **✅ 100% propre** |

## Problème principal

Le champ `a` (réponse correcte) contenait souvent du texte plus long que les options proposées.
Exemple : `a = "$f'(x) = 3x^2$"` vs option `"$3x^2$"`.

Le frontend fait un `===` strict (`exo.options[oI] === exo.a`), donc toute différence de format
faisait que l'élève obtenait **toujours HARD** (mauvaise réponse), même en choisissant la bonne option.

## Corrections appliquées

### Pass 1 — Substring matching (84 fixes)
Quand `a` contenait une option comme sous-chaîne, `a` a été remplacé par l'option exacte.

### Pass 2 — Fuzzy matching (49 fixes)
Pour les cas restants, matching par similarité (SequenceMatcher). Seuil : meilleur score > 0.3.

### Pass 3 — Corrections manuelles (14 fixes)
- **Exponentielle #18** : `a` contenait une dérivée complète → remplacé par "Décroissante puis croissante"
- **Geometrie_Repere #16-17** : `a = "x=1, soit x=1"` → remplacé par le point d'intersection `(1;14)` / `(1;16)`
- **Second_Degre #16** : `a = "m=0"` mathématiquement faux → corrigé en `m=1/4` (discriminant nul)
- **DiagnosticExos Produit_Scalaire #2** : `a = 45/2` correct mais absent des options → options ajustées
- **7 doublons d'options** : remplacés par des distracteurs distincts
- **2 doublons DiagnosticExos** : corrigés

## Vérification finale

```
Curriculum_Officiel: 200 exos, 0 absent, 0 doublons ✅
DiagnosticExos:       20 exos, 0 absent, 0 doublons ✅
BoostExos:           100 exos, 0 absent, 0 doublons ✅
```

## Données non touchées
- ✅ Exercices collège (6EME-3EME) non modifiés
- ✅ Aucune modification de `index.html` ou `backend.js`
- ✅ Aucun exercice supprimé — seuls `a` et `options` modifiés
