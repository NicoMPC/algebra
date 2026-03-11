# Notice d'utilisation — Matheux
## Ce que fait le site. Comment ça marche. Pour qui.
> Version 13 mars 2026 | Rédigée pour Nicolas (fondateur)

---

## En une phrase

**Matheux est une application web de soutien scolaire en maths pour les collégiens (6ème→3ème), qui détecte automatiquement les lacunes d'un élève et lui prépare des exercices personnalisés chaque jour.**

---

## 1. Comment fonctionne le site — vue d'ensemble

```
PARENT                          ÉLÈVE                        NICOLAS (toi)
  │                               │                               │
  │ S'inscrit sur landing         │ Fait le diagnostic            │ Voit tout dans
  │ (crée le compte enfant)       │ (5-10 min, 1 fois)            │ Google Sheet
  │                               │                               │ "👁 Suivi"
  │ ← reçoit code 6 lettres       │ Résultats immédiats           │
  │                               │ → lacunes identifiées         │ Assign le boost
  │                               │                               │ du lendemain
  │                               │ Boost quotidien               │
  │                               │ 5 exos / 10-15 min            │ Voit l'avancement
  │                               │ chaque matin                  │ en temps réel
  │                               │                               │
  │                               │ Chapitres au menu             │ Rapport 7h tous
  │                               │ (peut explorer librement)     │ les matins
  │                               │                               │
  │                               │ Mode Brevet (3EME)            │
  │                               │ Mode Révision bases           │
  │                               └───────────────────────────────┘
```

---

## 2. Le parcours d'un nouvel élève — étape par étape

### Étape 1 : Inscription (parent, 2 min)
1. Le parent arrive sur **matheux.fr** (landing page)
2. Il clique sur **"Démarrer les 7 jours offerts"**
3. Il choisit le niveau (6ème, 5ème, 4ème ou 3ème)
4. Il sélectionne les chapitres à travailler (les matières qui coincent)
5. **Quiz de calibrage rapide** : 4-10 questions (1 par chapitre sélectionné) — directement sur la landing
6. Il remplit son prénom + email → crée le compte
7. ✅ L'élève reçoit un **code à 6 caractères** (ex: `FP48QF`) et accède immédiatement à l'app

**Ce qui se passe dans le Sheet :** Une ligne est créée dans l'onglet `Users` avec l'email, le hash du mot de passe, la date d'inscription (= début du trial 7 jours).

### Étape 2 : Diagnostic (élève, 5-10 min, 1 seule fois)
- L'élève voit l'écran "Prêt ?" → clique "Lancer le diagnostic"
- Questions de niveau 1 et 2 sur chaque chapitre sélectionné
- L'algorithme détecte : EASY (maîtrisé) / MEDIUM (fragile) / HARD (lacune)
- **Résultat immédiat** : "Tu es fort en Fractions, les Équations résistent encore"
- Un premier **boost personnalisé** est généré automatiquement

**Ce qui se passe dans le Sheet :** Les scores sont enregistrés dans `Scores`, une entrée est créée dans `Progress` par chapitre, le boost est préparé dans `DailyBoosts`.

### Étape 3 : Routine quotidienne (élève, 10-15 min/jour)
- Chaque jour, **5 exercices du Boost** attendent l'élève
- Les exercices sont sélectionnés par Nicolas (toi) dans le Sheet → publiés via l'admin
- L'élève répond, voit immédiatement si c'est juste ou faux
- Si faux : indices disponibles + formule clé révélée
- Swipe gauche → exercice suivant (navigation mobile naturelle)
- **Streak** : compteur de jours consécutifs (motivation)

**Ce qui se passe dans le Sheet :** `save_score` écrit dans `Scores` + met à jour `Progress` + `rebuildSuivi()` recalcule l'onglet `👁 Suivi` + `writeToHistorique()` ajoute à `📋 Historique`.

### Étape 4 : Fin du trial (J+7)
- Un **badge J-X** apparaît dans l'interface dès J+5
- À J+7 : overlay bloquant → "Passe à l'abonnement pour continuer"
- Prix : **9,99€/mois** (Stripe — pas encore intégré au 13 mars 2026)

---

## 3. Ce que tu vois toi (Nicolas) dans Google Sheet

### Onglet `👁 Suivi` — ton tableau de bord quotidien
C'est ton outil de travail principal. Chaque ligne = 1 élève.

| Colonne | Ce que tu vois | Ce que tu fais |
|---|---|---|
| `⚡ ACTION NICOLAS` | 4 statuts possibles (voir ci-dessous) | Tu lis et tu agis |
| `Prénom` | Le prénom de l'élève | Info |
| `Niveau` | 6EME / 5EME / 4EME / 3EME | Info |
| `Dernière connexion` | Date en JJ/MM | Si inactif >5j → relance |
| `Chapitre 1/2/3/4` | Chapitre + statut (score %) | Vois la progression |
| `📝 Ch1 suite` | **TU ÉCRIS ICI** le prochain chapitre à débloquer | Ton action |
| `Boost consommé?` | Oui/Non | A-t-il fait son boost ? |
| `📝 Prochain boost` | **TU ÉCRIS ICI** le JSON du boost | Ton action |

### Les 4 statuts `⚡ ACTION NICOLAS`
| Statut | Signification | Que faire |
|---|---|---|
| `🔴 BLOQUÉ` | Inactif >7j ET scores <40% | Message WhatsApp parent |
| `⚡ BOOST TERMINÉ → préparer le suivant` | A fini ses 5 exos | Mettre le prochain boost JSON dans la colonne R |
| `✅ CHAPITRE TERMINÉ → assigner la suite` | >20 exos sur ce chapitre | Écrire le prochain chapitre dans colonne G/J/M/P |
| `👍 RAS` | Tout va bien | Rien à faire |

### Comment publier un boost (action la plus fréquente)
1. Tu vois `⚡ BOOST TERMINÉ` pour un élève
2. Tu ouvres l'**Admin Panel** (triple-clic sur le logo de l'app)
3. Tu cliques sur le nom de l'élève → tu vois ses chapitres et lacunes
4. Tu copies le JSON du dernier boost pour voir le format
5. Tu cliques "Préparer le prochain boost" → tu entres le JSON → "Publier"
6. Le lendemain matin, l'élève a ses 5 nouveaux exercices

### Rapport quotidien 7h
Chaque matin à 7h, tu reçois un email avec :
- Les élèves qui ont des **chapitres BLOQUÉS ou FRAGILES**
- Un prompt prêt à copier dans DeepSeek pour générer de nouveaux exercices

---

## 4. Les vues de l'application (côté élève)

### Vue "📚 Chapitres"
- Liste tous les chapitres débloqués
- **Boost quotidien** en premier (card violette ⚡)
- Si Mode Révision actif : REVISION en premier (card verte 🔁)
- Puis chapitres par ordre de progression
- Chaque card affiche : icône, nom, barre de progression, date dernière pratique

### Vue "📊 Progression"
- Résumé : X chapitres maîtrisés / X commencés
- Card "Révision [niveau inférieur]" → lance le Mode Révision
- Liste de toutes les cards chapitres avec barres de progression et scores

### Vue "🎓 Brevet" (3EME et autres niveaux)
- **Écran lancement** : description du mode, "Lancer l'examen blanc →"
- **Examen en cours** : ~15 questions multi-chapitres, progression visible, nom du chapitre source affiché
- **Résultat** : score %, grade (🏆/👍/📈/💪), chapitres couverts, bouton "Refaire"

### Mode Révision (accessible depuis vue Progression)
- Identifie les 3 chapitres les plus faibles du niveau inférieur
- Génère 6-9 exercices de révision (2 lvl1 + 1 lvl2 par chapitre)
- Injecté comme catégorie temporaire dans la vue Chapitres

---

## 5. Les exercices — comment ils sont structurés

Chaque exercice dans le Sheet a ce format JSON :
```json
{
  "q": "Énoncé de la question",
  "a": "La bonne réponse",
  "options": ["réponse A", "réponse B", "bonne réponse", "réponse D"],
  "steps": ["Étape 1 d'aide", "Étape 2", "Formule clé"],
  "f": "Formule LaTeX ou texte",
  "lvl": 1
}
```

- `lvl:1` = exercice de base (fondamentaux)
- `lvl:2` = exercice avancé (type contrôle/brevet)
- Chaque chapitre a **20 exercices** dans `Curriculum_Officiel`
- Le **boost quotidien** : 5 exercices sélectionnés par Nicolas + GAS
- Les **diagnostics** : 2 exercices par chapitre (1 lvl1 + 1 lvl2)

---

## 6. Les onglets Google Sheet — rôles

| Onglet | Qui l'utilise | Contenu |
|---|---|---|
| `Users` | GAS + toi (lecture) | Un compte par élève |
| `Scores` | GAS uniquement | Toutes les réponses enregistrées |
| `Progress` | GAS uniquement | Score/statut par chapitre par élève |
| `DailyBoosts` | GAS + toi (via admin) | Historique des boosts quotidiens |
| `Curriculum_Officiel` | GAS uniquement | 480+ exercices (24 chapitres × 20) |
| `DiagnosticExos` | GAS uniquement | 48 exercices de diagnostic |
| `👁 Suivi` | **TOI** | Tableau de bord principal |
| `📋 Historique` | GAS + toi (lecture) | Log chronologique des exercices |
| `Insights` | GAS + toi (lecture) | Feedbacks des élèves |
| `Rapports` | GAS + toi (lecture) | Rapports quotidiens 7h |

**Ne jamais modifier manuellement** : `Scores`, `Progress`, `DailyBoosts`, `Curriculum_Officiel`, `DiagnosticExos`.

---

## 7. L'architecture technique — simplifié

```
NAVIGATEUR (index.html)                    GOOGLE APPS SCRIPT (backend.js)
        │                                              │
        │  fetch POST (JSON)                           │
        ├──────────────────────────────────────────────►
        │                                              │
        │  { action: 'save_score',                     │  Lit/écrit dans
        │    code: 'ABC123',                           │  Google Sheet
        │    categorie: 'Fractions',                   │  via Spreadsheet API
        │    resultat: 'EASY', ... }                   │
        │                                              │
        │  ◄─────────────────────────────────────────  │
        │  { status: 'success' }                       │
        │                                              │
  localStorage                                   Google Sheets
  - boost_v23: {email, hash}              (base de données)
  - boost_loc_v23: {streak, last}
  - done_v23: {chapDone, boostConsumed}
```

**Pas de serveur propre** — tout passe par Google Apps Script gratuit.
**Limite** : ~20 utilisateurs simultanés max (Google Sheets).

---

## 8. Gestion du trial 7 jours

- À l'inscription : `TrialStart = date du jour` enregistré dans `Users`
- À chaque login : GAS calcule `daysLeft = 7 - (today - TrialStart)`
- Si `daysLeft <= 0` : `trialActive: false` → overlay bloquant côté frontend
- Badge `J-X` visible dans le header dès J+5
- Le trial donne **accès complet** à toutes les fonctionnalités

---

## 9. L'admin panel (triple-clic logo)

Uniquement accessible aux comptes avec `IsAdmin: true` dans `Users`.

**Ce que tu vois par élève :**
- Toutes ses réponses (badge DIAG = diagnostic, BOOST = entraînement)
- Scores par chapitre (triés : terminés → en cours → diagnostiqués)
- Statut boost (pending/in_progress/done)
- Section "Archivés" (chapitres complétés >20 exos)

**Ce que tu peux faire :**
- Publier le prochain boost (entrer le JSON des 5 exercices)
- Assigner le prochain chapitre
- Copier un prompt DeepSeek pour générer des exos
- Voir l'historique complet des boosts

---

## 10. Système de feedback élèves

Après chaque exercice répondu, un lien discret apparaît :
> "📢 Signaler une erreur dans cet exercice"

L'élève peut :
- Signaler 🐛 Erreur / ❓ Pas clair / 👍 Utile
- Ajouter un commentaire texte libre

Tout est enregistré dans l'onglet `Insights` du Sheet (créé automatiquement).
→ Tu consultes `Insights` pour identifier les exercices à corriger.

---

## 11. Ce qui N'EST PAS encore fait (13 mars 2026)

| Fonctionnalité | Statut |
|---|---|
| Paiement Stripe | ❌ Non intégré |
| Email bienvenue automatique | ❌ Non intégré |
| Séquences email J+3/J+7 | ❌ Non intégrées |
| Suppression profils de test (GAS) | ❌ À créer |
| Probabi lités / Racines carrées (3EME) | 🔄 En cours |
| Nombres décimaux (6EME) | 🔄 En cours |
| Fonctions linéaires (4EME) | 🔄 En cours |

---

## 12. Procédure de déploiement

Chaque modification du backend :
```bash
cd "/home/nicolas/Bureau/algebra live/algebra"
clasp push --force
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "description du changement"
```

Pour le frontend (`index.html`) : push vers GitHub Pages (auto-deploy).

---

## 13. Contacts et support

- **Fondateur** : Nicolas Follezou — contact@matheux.fr
- **GitHub** : https://github.com/NicoMPC/algebra
- **Sheet** : ID `1zLBajKVL8FUzy7aV2Myi9gYFEFJjnALkLAg0hbicuDk`
- **GAS URL** : `https://script.google.com/macros/s/AKfycbx.../exec`

---

*Notice générée le 13 mars 2026 — Matheux v23 GOLD MASTER*
