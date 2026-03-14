# Rapport — Insertion niveau 1ERE Spé Maths

> Date : 2026-03-14 | Build : @64

---

## Ce qui a été fait

### Étape 1 — Exercices (330 exercices insérés)
- **Curriculum_Officiel** : 10 chapitres × 20 exercices = 200 exercices
- **DiagnosticExos** : 10 chapitres × 2 exercices = 20 exercices
- **BoostExos** : 10 chapitres × 10 exercices = 100 exercices (+ 10 de marge)
- Les 3 pools utilisent des `variant` différents → pas de doublons entre curriculum/diag/boost
- JSON valides : **30/30**

### Chapitres 1ERE
| Categorie | Titre | Exos curriculum | Diag | Boost |
|---|---|---|---|---|
| Second_Degre | Second degré 📐 | 20 | 2 | 10 |
| Suites | Suites numériques 🔢 | 20 | 2 | 10 |
| Derivation | Dérivation 📈 | 20 | 2 | 10 |
| Exponentielle | Fonction exponentielle 🌿 | 20 | 2 | 10 |
| Trigonometrie | Trigonométrie 🔵 | 20 | 2 | 10 |
| Produit_Scalaire | Produit scalaire ✕ | 20 | 2 | 10 |
| Geometrie_Repere | Géométrie repérée 📍 | 20 | 2 | 10 |
| Probabilites_Cond | Probabilités conditionnelles 🎲 | 20 | 2 | 10 |
| Variables_Aleatoires | Variables aléatoires 🎯 | 20 | 2 | 10 |
| Algorithmique | Algorithmique & Python 💻 | 20 | 2 | 10 |

### Étape 2 — Compte Auguste
- Code : `AUG001`
- Email : augustecapronm@icloud.com
- Mot de passe : `auguste`
- Niveau : 1ERE
- Premium : oui (30 jours)
- IsTest : 1

### Étape 3 — Diagnostic simulé
- 10 chapitres avec scores variés (30-75%)
- 20 lignes Scores (source CALIBRAGE)
- Progress : 10 lignes, streak = 1
- Chapitres faibles : Exponentielle (30%), Variables aléatoires (35%), Suites (40%)

### Étape 4 — Boost du jour
- Ciblé sur Exponentielle + Suites (2 plus faibles)
- 5 exercices (2 Expo lvl1 + 2 Suites lvl1 + 1 Expo lvl2)
- ExosDone = 0, prêt à être consommé

### Étape 5 — backend.js
3 patches chirurgicaux :
1. `ALLOWED_LEVELS` : ajout `'1ERE'`
2. Message d'erreur `generateDailyBoost` : ajout `1ERE`
3. `niveauOrder` dans `generateRevision` : ajout `'1ERE'`

### Étape 7 — Déploiement
- `clasp push --force` : 9 fichiers
- `clasp deploy @64` : "feat: niveau 1ERE experimental + compte Auguste"

## Erreurs rencontrées
Aucune.

---

## Instructions pour la visio

### Connexion
- **URL** : https://matheux.fr
- **Email** : augustecapronm@icloud.com
- **Mot de passe** : auguste

### Ce qu'Auguste verra
1. **Diagnostic déjà fait** : 10 chapitres avec des scores variés
2. **Boost du jour prêt** : 5 exercices ciblés (Exponentielle + Suites)
3. **10 chapitres accessibles** : tous les chapitres de 1ère Spé Maths

### Ordre recommandé pour la session
1. **Boost du jour** → 5 exercices ciblés sur ses points faibles
2. Puis chapitres librement (commencer par Second degré — meilleur score)

### Limitations connues
- Le frontend (index.html) n'a **pas** été modifié → le sélecteur de niveau au register ne montre pas "1ERE"
- Auguste doit se connecter avec ses identifiants, pas s'inscrire
- Les exercices sont générés par templates Python (qualité correcte, pas artisanale)
