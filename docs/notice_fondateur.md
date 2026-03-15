# Notice fondateur — Objectif élève

> Ce que ton site fait maintenant, et ce que toi tu dois faire.

---

## Ce qui a changé (15 mars 2026, @70)

### Nouveau flow élève

**Avant** : Quiz diagnostic → Inscription
**Maintenant** : Quiz diagnostic → **Écran "Quel est ton objectif ?"** → Inscription

Après le quiz, un overlay plein écran apparaît avec 4 choix :

| Choix | Clé stockée |
|---|---|
| 🎯 Combler mes lacunes | `lacunes` |
| 📅 Un chapitre par jour | `chapitre_jour` |
| 📝 Préparer le brevet | `brevet` |
| 🚀 Tout réviser | `toutes_matieres` |

L'élève clique sur un bouton → son choix est stocké dans la **colonne N (Objectif)** de l'onglet Users dans Google Sheets → il passe à l'inscription normalement.

---

## Ce que tu vois dans l'admin

### Badge objectif dans la fiche élève

Quand tu cliques sur un élève dans "Mes Élèves", tu vois maintenant :

```
[Avatar] Prénom
         4EME · il y a 2j  🎯 Combler ses lacunes
```

Le badge vert à droite du niveau montre l'objectif déclaré. Si l'élève n'en a pas (inscrit avant cette mise à jour), tu vois "objectif non renseigné" en gris.

### Emails personnalisés

Quand un email J+5 ou J+7 est à envoyer, tu vois maintenant :

1. Un **encart jaune** "💡 Objectif déclaré : 🎯 Combler ses lacunes — le template sera adapté"
2. Quand tu cliques **"📧 Copier J+5"** ou **"📧 Copier J+7"**, le texte de l'email est automatiquement adapté à l'objectif de l'élève

**Exemple concret :**

- Élève avec objectif `brevet` → le J+5 parle des "144 exercices style brevet + brevets blancs complets"
- Élève avec objectif `chapitre_jour` → le J+5 parle du "rythme un chapitre par jour, 10 minutes"
- Élève sans objectif → le template par défaut (lacunes) est utilisé

Le J+0 (bienvenue) inclut aussi une phrase de contexte selon l'objectif.

---

## Ce que tu dois faire

### Rien de spécial côté technique

Tout est automatique :
- L'overlay s'affiche tout seul après le quiz
- L'objectif est sauvegardé automatiquement à l'inscription
- Les emails sont adaptés automatiquement

### Ce que tu dois observer

1. **Après tes 10 premiers vrais clients** → va dans l'onglet Users de Google Sheets, regarde la colonne N (Objectif) → note la répartition
2. Si la majorité dit `brevet` → tu pourras envisager un pack "Prépa Brevet" à un prix légèrement supérieur
3. Si la majorité dit `chapitre_jour` → tu pourras proposer un abonnement annuel à prix réduit/mois

### Pour les élèves déjà inscrits

Les élèves inscrits avant cette mise à jour n'ont pas d'objectif. Leur colonne N est vide. C'est normal — ça n'impacte rien. Les emails utilisent le template par défaut (lacunes).

---

## Résumé en 3 points

1. **L'élève choisit son objectif** juste après le quiz (moment de motivation maximale)
2. **Toi tu le vois** dans la fiche admin (badge vert) + les emails sont adaptés automatiquement
3. **Dans quelques semaines**, les données d'objectifs te diront quelles offres créer
