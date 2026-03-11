# Structure du nouveau Google Sheet — AlgèbreBoost

## Onglets à créer dans cet ordre

---

### 1. Users
| Colonne | Type | Notes |
|---|---|---|
| Code | String | Format : `ID-XXXXXXX` (généré à l'inscription) |
| Prénom | String | |
| Niveau | String | 6EME / 5EME / 4EME / 3EME uniquement |
| Email | String | lowercase, trimmed |
| PasswordHash | String | SHA-256(email::password::AB22) |
| DateInscription | Date | yyyy-MM-dd |
| IsAdmin | Number | 0 ou 1 (défaut : 0) |
| Premium | Number | 0 ou 1 (défaut : 0) |
| TrialStart | Date | Date début essai gratuit (pour Stripe plus tard) |

---

### 2. Scores
| Colonne | Type | Notes |
|---|---|---|
| Code | String | Clé étrangère vers Users |
| Prénom | String | |
| Niveau | String | |
| Chapitre | String | Identifiant catégorie (ex: FRACTIONS) |
| NumExo | Number | Index 1-based |
| Énoncé | String | Texte exact de la question |
| Résultat | String | EASY / MEDIUM / HARD |
| Temps(sec) | Number | Durée sur l'exercice |
| IndicesVus | Number | Nombre d'indices demandés |
| FormuleVue | Number | 0 ou 1 |
| MauvaiseOption | String | Option choisie si erreur QCM |
| Draft | String | Texte brouillon de l'élève |
| Date | Date | yyyy-MM-dd |

---

### 3. Curriculum_Officiel
| Colonne | Type | Notes |
|---|---|---|
| Niveau | String | 6EME / 5EME / 4EME / 3EME |
| Categorie | String | Identifiant unique ex: FRACTIONS_6 |
| Titre | String | Nom affiché ex: "Fractions 🍕" |
| Icone | String | Emoji |
| ExosJSON | JSON | Tableau de 20 exercices (format ci-dessous) |

**Format d'un exercice dans ExosJSON :**
```json
{
  "lvl": 1,
  "q": "Calcule : $\\frac{3}{4} + \\frac{1}{2}$",
  "a": "$\\frac{5}{4}$",
  "options": ["$\\frac{5}{4}$", "$\\frac{4}{6}$", "$\\frac{3}{8}$"],
  "f": "Pour additionner des fractions, on réduit au même dénominateur",
  "steps": ["Quel est le dénominateur commun ?", "3/4 = 6/8 et 1/2 = 4/8"]
}
```
- 10 exercices lvl:1 + 10 exercices lvl:2 par chapitre
- `options` : 1 bonne réponse + 2-3 erreurs classiques (shufflées côté frontend)
- `f` : formule clé (floue au début, révélée au tap)
- `steps` : indices progressifs (max 3)

---

### 4. DailyBoosts
| Colonne | Type | Notes |
|---|---|---|
| Code | String | Code élève |
| Date | Date | yyyy-MM-dd (date du boost) |
| BoostJSON | JSON | Format ci-dessous |

**Format BoostJSON :**
```json
{
  "insight": "Bravo Jules ! Tu progresses sur les fractions. Aujourd'hui on attaque les équations.",
  "exos": [
    { "lvl": 1, "q": "...", "a": "...", "options": [...], "f": "...", "steps": [...] },
    ...5 exercices au total
  ]
}
```

**Règle manuelle pour remplir DailyBoosts (toi, chaque soir entre 18h-20h) :**
- 2 exos sur les notions HARD d'hier
- 1 exo sur une notion MEDIUM pour consolider
- 1 exo facile sur une notion maîtrisée (confiance)
- 1 exo nouveau sur la prochaine notion du programme
- L'insight = 1 phrase d'encouragement personnalisée (2 min par élève)

---

### 5. DiagnosticExos
| Colonne | Type | Notes |
|---|---|---|
| Niveau | String | 6EME / 5EME / 4EME / 3EME |
| ExosJSON | JSON | 10 questions de diagnostic pour ce niveau |

**Contenu suggéré :** 2-3 questions par chapitre phare du niveau, level 1 uniquement, couvrant les notions fondamentales.

---

## Chapitres par niveau (CHAPS_BY_LEVEL du frontend)

```
6EME : ENTIERS_6, FRACTIONS_6, PROP_6, GEO_6, AIRES_6, ANGLES_6
5EME : FRACTIONS_5, RELATIFS_5, PROP_5, PUISSANCES_5, PYTHAGORE_5, LITTERAL_5
4EME : FRACTIONS_4, PUISSANCES_4, LITTERAL_4, EQUATIONS_4, PYTHAGORE_4, PROP_4
3EME : LITTERAL_3, EQUATIONS_3, FONCTIONS_3, THALES_3, TRIGO_3, STATS_3
```

Ces identifiants doivent matcher exactement ce qui est dans `Categorie` de `Curriculum_Officiel`.

---

## Ordre de remplissage recommandé
1. Créer le Sheet avec les 5 onglets et les bons en-têtes
2. Ajouter ton compte admin dans Users (IsAdmin = 1)
3. Commencer par le niveau de tes élèves actuels (4EME probablement)
4. Remplir DiagnosticExos pour ce niveau (10 questions)
5. Remplir Curriculum_Officiel pour ce niveau (6 chapitres × 20 exos)
6. Tester le flux complet avant de passer aux autres niveaux
