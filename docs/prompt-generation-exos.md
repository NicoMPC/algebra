# Prompt de génération d'exercices — Matheux v1.0

> Ce fichier est LA référence unique pour générer des exercices.
> Ne jamais utiliser un autre prompt. Si ce prompt doit évoluer, versionner ici.

---

## Le prompt

Copie-colle ce prompt dans Claude en remplaçant les `{variables}` :

```
Tu es un professeur de maths expert. Génère {nombre} exercices QCM pour le niveau {niveau} ({6EME|5EME|4EME|3EME|1ERE}), chapitre "{chapitre}".

RÈGLES STRICTES :

ÉNONCÉ (q) :
- 1-2 phrases, question finale claire
- LaTeX obligatoire pour toute expression math entre $...$
- lvl:1 = calcul direct, vocabulaire simple
- lvl:2 = mise en situation ou multi-étapes
- Adapter le vocabulaire au niveau (6EME=concret, 3EME=technique)

RÉPONSE (a) :
- Copie EXACTE d'une des 4 options (même format LaTeX, même espaces)
- VÉRIFIE LE CALCUL — une réponse fausse est inacceptable

OPTIONS (exactement 4) :
- Chaque distracteur = une erreur de calcul PLAUSIBLE
  (oublier un signe, inverser num/denom, ne pas simplifier, erreur d'exposant)
- Jamais de doublon, jamais de valeur absurde
- Si Vrai/Faux → type:"vf" + options:["Vrai","Faux"]

STEPS (exactement 3 indices progressifs) :
- Step 1 : Identifie la méthode/propriété à utiliser
- Step 2 : Montre le calcul intermédiaire AVEC les valeurs de l'énoncé
- Step 3 : Conclut avec le résultat détaillé
- Chaque step SPÉCIFIQUE à l'exercice
- INTERDIT : "Applique la formule...", "Vérifie ton calcul...", phrases passe-partout

FORMULE (f) :
- La formule GÉNÉRALE du chapitre en LaTeX (rappel théorique, pas la solution)

FORMAT JSON — un array d'objets, chaque objet :
{
  "lvl": 1 ou 2,
  "q": "énoncé en LaTeX",
  "a": "réponse exacte (copie d'une option)",
  "options": ["opt1", "opt2", "opt3", "opt4"],
  "steps": ["étape 1", "étape 2", "étape 3"],
  "f": "formule générale LaTeX"
}

Répartition : {nombre/2} exos lvl:1 (fondamentaux) + {nombre/2} exos lvl:2 (avancés).

AVANT DE RÉPONDRE : vérifie chaque calcul. Une erreur = un élève qui perd confiance.
```

---

## Variantes

### Pour un boost (5 exos ciblés sur lacunes)
Remplacer la dernière ligne par :
```
Génère exactement 5 exercices ciblés sur les erreurs suivantes : {liste des erreurs}.
Mélange les chapitres. Commence par un exo facile pour mettre en confiance.
```

### Pour des exercices Brevet (3EME)
Ajouter :
```
Format Brevet : exercices multi-étapes, contextualisés (situations réelles),
avec extraction de données dans l'énoncé. Chaque exo doit tester 1-2 compétences.
```

### Pour Vrai/Faux
```
{
  "lvl": 1,
  "type": "vf",
  "q": "Affirmation à évaluer",
  "a": "Vrai",
  "options": ["Vrai", "Faux"],
  "steps": ["step1", "step2", "step3"],
  "f": "formule"
}
```

---

## Checklist post-génération

Après avoir reçu le JSON de Claude :

1. **Vérifier les calculs** — refaire mentalement chaque exo
2. **Vérifier `a ∈ options`** — la réponse est bien dans les options
3. **Vérifier 4 options** — pas 3, pas 2 (sauf VF)
4. **Vérifier les steps** — spécifiques, pas génériques
5. **Lancer l'audit** : `python3 audit_exos.py` + `python3 audit_latex.py`
6. **Logger** dans `docs/logs/`

---

## Erreurs connues à surveiller

| Fréquence | Erreur | Comment détecter |
|---|---|---|
| 21.7% | 3 options au lieu de 4 | Comptage automatique |
| 17.7% | Steps génériques copiés-collés | Rechercher "Applique la formule", "Vérifie ton calcul" |
| 3.3% | VF sans type:"vf" (2 options) | Comptage options = 2 sans type |
| 1.1% | Format LaTeX incohérent a vs options | Comparaison stricte |

---

## Historique versions

| Version | Date | Changement |
|---|---|---|
| v1.0 | 2026-03-22 | Création — basé sur analyse de 1872 exos existants |
