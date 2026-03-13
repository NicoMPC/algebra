# Base de données — Google Sheets — Matheux

> Schéma complet de la base de données Google Sheets.
> Voir aussi [architecture.md](architecture.md) pour les flux, [claude.md](claude.md) pour les règles, [product.md](product.md) pour le produit.

---

## Informations de connexion

| Environnement | Sheet ID |
|---|---|
| **Production** (GAS) | `1zLBajKVL8FUzy7aV2Myi9gYFEFJjnALkLAg0hbicuDk` |
| **Staging** (Python) | `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |

Service account : `algebreboost-sheets-2595a71cadfb.json` (ignoré par git).

---

## Onglets — Vue d'ensemble

### Onglets Nicolas (lecture + écriture via Admin)

| Onglet | Rôle | Qui y accède |
|---|---|---|
| `👁 Suivi` | Tableau de bord quotidien (1 ligne/élève) | Nicolas (principal), GAS (écriture via rebuildSuivi) |
| `📋 Historique` | Log chronologique exercices (récent en haut) | Nicolas (lecture), GAS (écriture via writeToHistorique) |

### Onglets GAS (ne pas modifier manuellement)

| Onglet | Rôle | Modifier ? |
|---|---|---|
| `Users` | Comptes utilisateurs | ❌ Sauf IsAdmin manuellement |
| `Progress` | Score/statut par chapitre par élève | ❌ |
| `Scores` | Toutes les réponses individuelles | ❌ |
| `DailyBoosts` | Historique des boosts quotidiens | Lecture + admin panel |
| `Curriculum_Officiel` | Exercices par chapitre (580 exos) | ❌ Via scripts Python seulement |
| `DiagnosticExos` | Exercices de diagnostic (58 exos) | ❌ Via scripts Python seulement |
| `RemediationChapters` | Chapitres de remédiation (désactivé) | ❌ |
| `BrevetExos` | Exercices style brevet (120 exos) | ❌ Via script Python seulement |
| `BrevetResults` | Résultats brevets blancs | ❌ |
| `📧 Emails` | Archive des emails envoyés | Lecture seule |
| `Insights` | Feedbacks élèves + demandes chapitres | Lecture seule |
| `Rapports` | Rapports quotidiens 7h | Lecture seule |

### Onglets archivés (données conservées)

```
_ARCHIVE_Queue / _ARCHIVE_Prerequisites / _ARCHIVE_Rapports / _ARCHIVE_Pending_Exos
```

---

## Schéma détaillé par onglet

### Users

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Code | String | Identifiant unique 6 chars (ex: `FP48QF`) |
| B | Prénom | String | |
| C | Niveau | String | `6EME` / `5EME` / `4EME` / `3EME` |
| D | Email | String | lowercase, trimmed |
| E | PasswordHash | String | SHA-256(`email::password::AB22`) |
| F | DateInscription | Date | `yyyy-MM-dd` |
| G | IsAdmin | Number | `0` ou `1` (ou `true`/`TRUE`) |
| H | Premium | Number | `0` ou `1` |
| I | TrialStart | Date | Date début essai 7 jours |
| J | PremiumEnd | Date | Date fin premium (futur Stripe) |
| K | IsTest | Number | `0` = vrai élève, `1` = compte test |
| L | PendingBrevet | String | JSON `{chapitres:[], message, date}` quand admin publie un brevet blanc |

**Règles importantes :**
- Emails `@matheux.fr` → `IsTest=1` automatiquement au `register()`
- Limite bêta : 50 vrais élèves (`IsTest=0`, non-admin uniquement)
- `login()` vérifie `isAdmin` et `premium` de façon robuste (`true`/`TRUE`/`1`/`'1'`)

### Scores

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Code | String | FK → Users |
| B | Prénom | String | |
| C | Niveau | String | |
| D | Chapitre | String | Identifiant catégorie (ex: `Fractions`) |
| E | NumExo | Number | Index 1-based |
| F | Énoncé | String | Texte exact de la question (tronqué 60 chars dans Historique) |
| G | Résultat | String | `EASY` / `MEDIUM` / `HARD` |
| H | Temps(sec) | Number | Durée sur l'exercice |
| I | NbIndices | Number | Nombre d'indices demandés |
| J | FormuleVue | Number | `0` ou `1` |
| K | MauvaiseOption | String | Option choisie si erreur QCM |
| L | Draft | String | Texte brouillon de l'élève |
| M | Date | Date | `yyyy-MM-dd` |

### Progress

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Code | String | FK → Users |
| B | Niveau | String | |
| C | Chapitre | String | Identifiant catégorie |
| D | Score | Number | Score de confiance 0-100 |
| E | NbExos | Number | Nombre total d'exercices faits |
| F | NbErreurs | Number | Nombre d'erreurs (HARD) |
| G | DernierePratique | Date | Date du dernier exercice |
| H | Statut | String | `en_cours` / `maitrise` |
| I | Streak | Number | Série en cours |

### DailyBoosts

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Code | String | FK → Users |
| B | Date | Date | `yyyy-MM-dd` (date du boost) |
| C | BoostJSON | String | JSON `{insight, exos:[...5 exercices]}` |
| D | ExosDone | Number | Nombre d'exercices complétés (0-5) |

**Règles :**
- `login()` crée l'entrée avec `ExosDone=0` quand un boost est livré
- `save_score` incrémente `ExosDone` quand `source=BOOST`
- `generateDailyBoost` écrit 4 colonnes (dont `ExosDone=0`)

### Curriculum_Officiel

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Niveau | String | `6EME` / `5EME` / `4EME` / `3EME` |
| B | Categorie | String | Identifiant unique (ex: `Fractions`) |
| C | Titre | String | Nom affiché (ex: `Fractions 🍕`) |
| D | Icone | String | Emoji |
| E | ExosJSON | String | JSON tableau de 20 exercices |

**Format exercice :**
```json
{
  "lvl": 1,
  "q": "Calcule : $\\frac{3}{4} + \\frac{1}{2}$",
  "a": "$\\frac{5}{4}$",
  "options": ["$\\frac{5}{4}$", "$\\frac{4}{6}$", "$\\frac{3}{8}$"],
  "f": "Formule clé (floue au début, révélée au tap)",
  "steps": ["Indice 1", "Indice 2", "Indice 3"]
}
```

- 10 exercices `lvl:1` (fondamentaux) + 10 `lvl:2` (avancés) par chapitre
- 29 chapitres × 20 exos = **580 exercices** en prod

### BoostExos

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Niveau | String | `6EME` / `5EME` / `4EME` / `3EME` |
| B | Categorie | String | Identifiant catégorie (même noms que Curriculum_Officiel) |
| C | ExosJSON | String | JSON tableau de 10 exercices (5 lvl1 + 5 lvl2) |

Pool d'exercices **dédiée aux boosts quotidiens**, séparée de Curriculum_Officiel pour éviter que les exercices de boost polluent la progression des chapitres. Même format d'exercice, mêmes compétences, mais nombres et wording différents.

29 chapitres × 10 exos = **290 exercices boost** en prod.

**Fallback** : si l'onglet BoostExos est absent ou vide pour un niveau, `generateDailyBoost()` utilise Curriculum_Officiel automatiquement.

### DiagnosticExos

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Niveau | String | |
| B | Categorie | String | Identifiant chapitre |
| C | ExosJSON | String | JSON tableau de 2 exercices (1 lvl1 + 1 lvl2) |

29 chapitres × 2 exos = **58 exercices** de diagnostic.

### BrevetExos

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Niveau | String | (toujours `3EME`) |
| B | Categorie | String | Chapitre brevet |
| C | ExosJSON | String | JSON tableau de 8 exercices `{q, opts:[], ans:int, hint, diff}` |

15 chapitres × 8 exos = **120 exercices** style brevet.

### BrevetResults

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Code | String | FK → Users |
| B | Prénom | String | |
| C | Niveau | String | |
| D | Date | Date | |
| E | Chapitres | String | Liste chapitres testés |
| F | NbQuestions | Number | |
| G | NbCorrect | Number | |
| H | Score% | Number | |
| I | DetailJSON | String | Détail par chapitre |
| J | Message | String | Message admin si brevet publié |

**Isolation** : BrevetResults est séparé de Progress/Scores → ne perturbe pas l'algorithme adaptatif.

### 👁 Suivi

Structure colonnes (GAS : Code en col U = index 20, 1-based) :

```
A: ⚡ ACTION NICOLAS    B: Prénom    C: Niveau    D: Dernière connexion
E: Chapitre 1    F: Statut 1    G: 📝 Ch1 suite (Nicolas)
H: Chapitre 2    I: Statut 2    J: 📝 Ch2 suite (Nicolas)
K: Chapitre 3    L: Statut 3    M: 📝 Ch3 suite (Nicolas)
N: Chapitre 4    O: Statut 4    P: 📝 Ch4 suite (Nicolas)
Q: Boost consommé?    R: 📝 Prochain boost (Nicolas)
S: 📧 Rapport envoyé / Chap5+    [T: Code masquée]
```

→Nouveau Ch : indices [6, 9, 12, 15] | →Boost : index 18

### Règles ⚡ ACTION NICOLAS (rebuildSuivi)

| Valeur | Condition | Priorité |
|---|---|---|
| `🔴 BLOQUÉ` | inactif >7j ET score <40 sur tous chapitres | 1 |
| `⚡ BOOST TERMINÉ → préparer le suivant` | ExosDone==5 ET pas de boost pending (inclut boost du jour) | 2 |
| `✅ CHAPITRE TERMINÉ → assigner la suite` | Progress NbExos ≥20 ET colonnes 📝 Nicolas vides | 3 |
| `📝 BREVET EN ATTENTE → à faire` | PendingBrevet non vide ET niveau 3EME | 3b |
| `👍 RAS` | sinon | 4 |

Plusieurs règles simultanées → toutes affichées en pills, couleur card = plus urgente.

---

## Relations entre onglets

```
Users (Code) ──┬── Scores (Code)
               ├── Progress (Code)
               ├── DailyBoosts (Code)
               ├── BrevetResults (Code)
               └── 👁 Suivi (Code en col T)

Curriculum_Officiel (Niveau, Categorie) ── DiagnosticExos (Niveau, Categorie)
BoostExos (Niveau, Categorie) ── même structure que Curriculum (pool séparée)
BrevetExos (Niveau, Categorie) ── standalone (pas de FK vers Curriculum)
Insights ── standalone (feedback libre)
📧 Emails ── standalone (archive)
Rapports ── standalone (archive)
```

---

## Chapitres disponibles — 29 chapitres en prod

| Niveau | Chapitres |
|---|---|
| 6EME | Nombres_entiers, Fractions, Proportionnalité, Géométrie, PérimètresAires, Angles, Nombres_decimaux, Statistiques_6eme |
| 5EME | Fractions, Nombres_relatifs, Proportionnalité, Calcul_Littéral, Pythagore, Puissances |
| 4EME | Puissances, Fractions, Proportionnalité, Calcul_Littéral, Équations, Pythagore, Fonctions_lineaires |
| 3EME | Calcul_Littéral, Équations, Fonctions, Théorème_de_Thalès, Trigonométrie, Statistiques, Probabilités, Racines_carrees |

Total : **29 chapitres × 20 exos = 580 exercices** + **29 × 10 = 290 boost** + **29 × 2 = 58 diagnostics** + **15 × 8 = 120 brevet**
