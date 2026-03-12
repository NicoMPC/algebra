# Notice d'utilisation — Matheux
## Ce que fait le site. Comment ça marche. Pour qui.
> Version 13 mars 2026 | Rédigée pour Nicolas (fondateur)

---

## En une phrase

**Matheux est une application web de soutien scolaire en maths pour les collégiens (6ème→3ème), qui détecte automatiquement les lacunes d'un élève et lui prépare des exercices personnalisés chaque jour.**

---

## Nouveautés — Mars 2026

| Date | Nouveauté |
|---|---|
| 12 mars | Mode Brevet et Mode Révision désactivés (code conservé — bientôt disponibles) |
| 12 mars | 5 nouveaux chapitres poussés en prod (Probabilités, Racines carrées, Décimaux, Fonctions linéaires, Statistiques) — 100 exos + 10 diags |
| 13 mars | Feedback élèves (bouton Signaler → onglet Insights) |
| 12 mars | Juridique complet (5 pages légales + consentement parental) |
| 12 mars | Landing vendeuse : pricing comparatif, fondateur Nicolas, carousel témoignages |
| 13 mars | Waitlist, limite bêta portée à **50 vrais élèves** (IsTest=0) |
| 13 mars | Email bienvenue J+0 automatique au register() |
| 13 mars | GA4 **G-7R2DW4585Y** actif (bannière consentement RGPD, IP anonymisée) |
| 13 mars | Overlay trial expiré → lien Stripe direct **9,99 €/mois** |
| 13 mars | Email J+7 → lien Stripe direct intégré |
| 13 mars | Emails envoyés depuis **no-reply@matheux.fr** (GmailApp alias) |
| 13 mars | Fix quiz CTA : questions invisibles corrigées (fond blanc) |
| 13 mars | Colonne **IsTest** dans Users — 110 comptes existants migrés test, vrais élèves comptés sur 50 |
| 13 mars | Dashboard admin : compteur X/50, section 🧪 Comptes test repliable, Outils Fondateur (Stripe + email test) |

---

## 1. Comment fonctionne le site — vue d'ensemble

```
PARENT                          ÉLÈVE                        NICOLAS (toi)
  │                               │                               │
  │ S'inscrit sur landing         │ Fait le diagnostic            │ Voit tout dans
  │ (crée le compte enfant)       │ (5-10 min, 1 fois)            │ Google Sheet
  │                               │                               │ "👁 Suivi"
  │ ← reçoit code 6 lettres       │ Résultats immédiats           │
  │                               │ → lacunes identifiées         │ Assigne le boost
  │                               │                               │ du lendemain
  │                               │ Boost quotidien               │
  │                               │ 5 exos / 10-15 min            │ Voit l'avancement
  │                               │ chaque matin                  │ en temps réel
  │                               │                               │
  │                               │ Chapitres au menu             │ Rapport 7h tous
  │                               │ (peut explorer librement)     │ les matins
  │                               │                               │
  │                               │ Feedback "Signaler" après     │
  │                               │ chaque exercice → Insights    │
  │                               └───────────────────────────────┘
```

---

## 2. Le parcours d'un nouvel élève — étape par étape

### Étape 1 : Inscription (parent, 2 min)
1. Le parent arrive sur **matheux.fr** (landing page)
2. Il clique sur **"Démarrer les 7 jours offerts"**
3. Il choisit le niveau (6ème, 5ème, 4ème ou 3ème)
4. Il sélectionne les chapitres à travailler (1 à 4 chapitres)
5. **Quiz de calibrage rapide** : 4 à 10 questions inline — directement sur la landing, sans créer de compte
6. Il remplit son prénom + email → crée le compte
7. ✅ L'élève reçoit un **code à 6 caractères** (ex: `FP48QF`) et accède immédiatement à l'app

**Ce qui se passe dans le Sheet :** Une ligne est créée dans l'onglet `Users` avec l'email, le hash du mot de passe, la date d'inscription (= début du trial 7 jours).

### Étape 2 : Diagnostic (élève, 5-10 min, 1 seule fois)
- Le quiz de calibrage landing **EST** le diagnostic — les résultats sont sauvegardés automatiquement
- Pas de re-diagnostic dans l'app (évite la frustration)
- Un premier **boost personnalisé** est généré automatiquement en arrière-plan pendant l'onboarding
- Si l'élève abandonne à mi-diagnostic sur la landing : reprise possible pendant 24h

**Ce qui se passe dans le Sheet :** Les scores sont enregistrés dans `Scores`, une entrée dans `Progress` par chapitre, le boost est préparé dans `DailyBoosts`.

### Étape 3 : Routine quotidienne (élève, 10-15 min/jour)
- Chaque jour, **5 exercices du Boost** attendent l'élève
- Les exercices sont sélectionnés par Nicolas (toi) dans l'Admin Panel → publiés
- L'élève répond, voit immédiatement si c'est juste ou faux
- Si faux : indices disponibles + formule clé révélée + explication étape par étape
- Swipe gauche → exercice suivant (navigation mobile naturelle)
- **Streak** : compteur de jours consécutifs (motivation gamification)
- Après chaque réponse : lien discret "📢 Signaler" pour envoyer un feedback

**Ce qui se passe dans le Sheet :** `save_score` écrit dans `Scores` + met à jour `Progress` + `rebuildSuivi()` recalcule `👁 Suivi` + `writeToHistorique()` ajoute à `📋 Historique`.

### Étape 4 : Fin du trial (J+7)
- Un **badge J-X** apparaît dans l'interface dès J+5
- À J+7 : overlay bloquant → "Passe à l'abonnement pour continuer"
- Prix : **9,99€/mois** — page premium.html active, paiement via contact@matheux.fr en attendant Stripe
- L'élève peut toujours voir sa progression en cliquant "Voir ma progression quand même"

---

## 3. Ce que tu vois toi (Nicolas) dans Google Sheet

### Onglet `👁 Suivi` — ton tableau de bord quotidien
C'est ton outil de travail principal. Chaque ligne = 1 élève.

| Colonne | Ce que tu vois | Ce que tu fais |
|---|---|---|
| `⚡ ACTION NICOLAS` | 4 statuts possibles (voir ci-dessous) | Tu lis et tu agis |
| `Prénom` | Le prénom de l'élève | Info |
| `Niveau` | 6EME / 5EME / 4EME / 3EME | Info |
| `Dernière connexion` | Date en JJ/MM | Si inactif >5j → relance WhatsApp |
| `Chapitre 1/2/3/4` | Chapitre + statut (score %) | Vois la progression |
| `📝 Ch1 suite` | **TU PEUX ÉCRIRE ICI** (ou via Admin Panel) | Prochain chapitre à débloquer |
| `Boost consommé?` | Oui/Non | A-t-il fait son boost ? |
| `📝 Prochain boost` | **TU PEUX ÉCRIRE ICI** (ou via Admin Panel) | JSON du boost |

### Les 4 statuts `⚡ ACTION NICOLAS`
| Statut | Signification | Que faire |
|---|---|---|
| `🔴 BLOQUÉ` | Inactif >7j ET scores <40% | Message WhatsApp parent |
| `⚡ BOOST TERMINÉ → préparer le suivant` | A fini ses 5 exos | Mettre le prochain boost JSON via Admin |
| `✅ CHAPITRE TERMINÉ → assigner la suite` | >20 exos sur ce chapitre | Écrire le prochain chapitre via Admin |
| `👍 RAS` | Tout va bien | Rien à faire |

### Procédure admin quotidienne (10 min/matin)
1. Ouvrir l'app → triple-clic sur le logo → Admin Panel
2. Scanner les cartes élèves triées par urgence (🔴 en tête)
3. Pour chaque `⚡ BOOST TERMINÉ` :
   - Cliquer sur l'élève → voir ses lacunes
   - Copier le prompt Claude (bouton "📋 Copier")
   - Coller dans Claude → obtenir le JSON → coller dans "Publier un boost" → Enregistrer
4. Pour chaque `✅ CHAPITRE TERMINÉ` :
   - Même procédure avec "Publier un chapitre"
5. Vérifier les élèves `🔴 BLOQUÉ` → message parent si nécessaire

### Rapport quotidien 7h
Chaque matin à 7h, un email automatique liste :
- Les élèves avec chapitres **BLOQUÉS ou FRAGILES**
- Un prompt prêt à copier dans Claude pour générer de nouveaux exercices

---

## 4. Les vues de l'application (côté élève)

### Vue "📚 Chapitres"
- **Boost quotidien** en premier (card violette ⚡)
- Puis chapitres par ordre de progression
- Chaque card affiche : icône, nom, barre de progression, date dernière pratique
- Badge "🆕 NEW" si Nicolas vient d'assigner un nouveau chapitre

### Vue "📊 Progression"
- Résumé : X chapitres maîtrisés / X commencés
- Liste de toutes les cards chapitres avec barres de progression et scores
- **Mode Révision** : ⏳ désactivé temporairement — code prêt pour activation future

### Vue "🎓 Brevet"
- **⏳ Désactivée temporairement** — tab masqué
- Code complet conservé, sera activé prochainement pour les 3EME

### Feedback après exercice
- Lien discret "📢 Signaler une erreur dans cet exercice" sous chaque question
- 3 types rapides : 🐛 Erreur / ❓ Pas clair / 👍 Utile + commentaire texte libre
- Enregistré dans l'onglet `Insights` du Sheet (créé automatiquement)

---

## 5. Les exercices — format et structure

Chaque exercice dans le Sheet a ce format JSON :
```json
{
  "q": "Énoncé de la question (avec $latex$ si besoin)",
  "a": "La bonne réponse (doit être dans options)",
  "options": ["réponse A", "bonne réponse", "réponse C", "réponse D"],
  "steps": ["Étape 1 d'aide", "Étape 2", "Formule clé"],
  "f": "Formule LaTeX ou texte",
  "lvl": 1
}
```

- `lvl:1` = exercice de base (fondamentaux)
- `lvl:2` = exercice avancé (type contrôle/brevet)
- Chaque chapitre a **20 exercices** dans `Curriculum_Officiel` (10 lvl1 + 10 lvl2)
- Le **boost quotidien** : 5 exercices sélectionnés + personnalisés par Nicolas
- Les **diagnostics** : 2 exercices par chapitre (1 lvl1 + 1 lvl2) dans `DiagnosticExos`

---

## 6. Les chapitres disponibles — état au 12 mars 2026

### Curriculum_Officiel (24 chapitres × 20 exos = 480 exos)
| Niveau | Chapitres |
|---|---|
| 6EME | Nombres_entiers, Fractions, Proportionnalité, Géométrie, PérimètresAires, Angles |
| 5EME | Fractions, Nombres_relatifs, Proportionnalité, Calcul_Littéral, Pythagore, Puissances |
| 4EME | Puissances, Fractions, Proportionnalité, Calcul_Littéral, Équations, Pythagore |
| 3EME | Calcul_Littéral, Équations, Fonctions, Théorème_de_Thalès, Trigonométrie, Statistiques |

### Ajoutés le 12 mars 2026 ✅ EN PROD
| Chapitre | Niveau | Exos |
|---|---|---|
| Probabilités | 3EME | 20 exos + 2 diags |
| Racines_carrees | 3EME | 20 exos + 2 diags |
| Nombres_decimaux | 6EME | 20 exos + 2 diags |
| Fonctions_lineaires | 4EME | 20 exos + 2 diags |
| Statistiques_6eme | 6EME | 20 exos + 2 diags |

Total curriculum : **29 chapitres × 20 exos = 580 exos** | DiagnosticExos : **29 chapitres × 2 = 58 exos**

---

## 7. Les onglets Google Sheet — rôles

| Onglet | Qui l'utilise | Contenu | Toucher ? |
|---|---|---|---|
| `Users` | GAS + toi (lecture) | Un compte par élève | Lecture seule (sauf IsAdmin) |
| `Scores` | GAS uniquement | Toutes les réponses | ❌ Ne jamais modifier |
| `Progress` | GAS uniquement | Score/statut par chapitre | ❌ Ne jamais modifier |
| `DailyBoosts` | GAS + admin | Historique des boosts | Lecture + admin panel |
| `Curriculum_Officiel` | GAS uniquement | 480+ exercices (24 chap × 20) | ❌ Via scripts Python seulement |
| `DiagnosticExos` | GAS uniquement | 48 exercices de diagnostic | ❌ Via scripts Python seulement |
| `👁 Suivi` | **TOI** | Tableau de bord principal | ✅ Ton outil quotidien |
| `📋 Historique` | GAS + toi (lecture) | Log chronologique des exercices | Lecture seule |
| `Insights` | GAS + toi (lecture) | Feedbacks des élèves | Consulte régulièrement |
| `Rapports` | GAS + toi (lecture) | Rapports quotidiens 7h | Lecture seule |
| `RemediationChapters` | GAS uniquement | Chapitres de remédiation | ❌ Archivé |

**Onglets archivés (ne pas toucher) :** `_ARCHIVE_Queue`, `_ARCHIVE_Prerequisites`, `_ARCHIVE_Rapports`, `_ARCHIVE_Pending_Exos`

---

## 8. L'architecture technique — simplifié

```
NAVIGATEUR (index.html ~4750 lignes)       GOOGLE APPS SCRIPT (backend.js)
        │                                              │
        │  fetch POST (JSON, SANS Content-Type !)      │
        ├──────────────────────────────────────────────►
        │  { action: 'save_score',                     │  Lit/écrit dans
        │    code: 'ABC123',                           │  Google Sheet
        │    categorie: 'Fractions',                   │  via Spreadsheet API
        │    resultat: 'EASY', ... }                   │
        │  ◄─────────────────────────────────────────  │
        │  { status: 'success' }                       │
        │                                              │
  localStorage                                   Google Sheets (prod)
  - boost_v23: {email, hash}              ID: 1zLBajKVL8FUzy7aV2Myi9gYFEFJjnALkLAg0hbicuDk
  - boost_loc_v23: {stk, last}
```

⚠️ **Règle CORS critique** : Ne JAMAIS ajouter `Content-Type: application/json` sur les fetch vers GAS. Déclenche un preflight OPTIONS que GAS ne gère pas → erreur CORS. Le fetch doit être sans headers.

**Limite** : ~20 utilisateurs simultanés max (Google Sheets).

---

## 9. Gestion du trial 7 jours

- À l'inscription : `TrialStart = date du jour` enregistré dans `Users`
- À chaque login : GAS calcule `daysLeft = 7 - (today - TrialStart)`
- Si `daysLeft <= 0` : `trialActive: false` → overlay bloquant côté frontend
- Badge `J-X` visible dans le header dès J+5
- Le trial donne **accès complet** à toutes les fonctionnalités actives
- Bouton "Voir ma progression quand même" : ferme l'overlay et affiche la progression

---

## 10. L'admin panel (compte admin)

Accessible uniquement aux comptes avec `IsAdmin: true` dans `Users`.

**Connexion :** ton email admin → login normal → redirection automatique vers "Mes Élèves"

**Ce que tu vois par élève :**
- Toutes ses réponses (badge DIAG = diagnostic, BOOST = entraînement)
- Scores par chapitre triés : terminés → en cours → diagnostiqués
- Statut boost (pending/in_progress/done)
- Métriques : ⏱ temps moyen, 💡 indices, 🧮 % formule
- Section "Archivés" (chapitres complétés >20 exos)

**Ce que tu peux faire :**
- 📋 **Copier le prompt Claude** pour un chapitre → Claude génère le JSON d'exercices
- ⚡ **Publier un boost** (JSON 5 exercices) → disponible au prochain login élève
- 📚 **Publier un chapitre** (JSON 20 exercices) → badge NEW chez l'élève
- 📋 **Copier le dernier boost JSON** pour le modifier

**Flux complet (30 secondes) :**
1. Clic "📋 Copier le prompt Claude"
2. Coller dans Claude (Ctrl+V) → Entrée → JSON généré
3. Sélectionner le JSON → Ctrl+C → retour sur Matheux
4. Coller dans "Publier" → Enregistrer → ✅ Toast vert

---

## 11. Système de feedback élèves

Après chaque exercice répondu, un lien discret apparaît :
> "📢 Signaler une erreur dans cet exercice"

L'élève peut choisir :
- 🐛 **Erreur** : l'exercice contient une erreur
- ❓ **Pas clair** : l'énoncé est confus
- 👍 **Utile** : l'exercice lui a été utile

Avec un commentaire texte libre optionnel.

Tout est enregistré dans l'onglet `Insights` du Sheet (créé automatiquement au premier feedback).
→ Consulte `Insights` régulièrement pour identifier les exercices à corriger.

---

## 12. Ce qui N'EST PAS encore fait (13 mars 2026)

| Fonctionnalité | Statut | Priorité |
|---|---|---|
| Paiement Stripe | ❌ Non intégré — premium.html prêt, bouton email actif | 🔴 Sprint suivant |
| Webhook Stripe → colonne Premium | ❌ À faire après Stripe | 🔴 Sprint suivant |
| Séquences email J+3/J+7 | ⏳ Code prêt — activer trigger Apps Script | 🟡 Important |
| Measurement ID GA4 réel | ⏳ Remplacer G-XXXXXXXXXX dans index.html | 🟡 Important |
| Mode Brevet | ⏳ Code prêt, UI désactivé | 🟡 Bientôt |
| Mode Révision | ⏳ Code prêt, UI désactivée | 🟡 Bientôt |
| Action delete_test_users (GAS) | ❌ À créer | 🟡 Utile |
| Validation inputs GAS (email) | ❌ À faire | 🟢 Mineur |
| Migration BDD >50 users | ❌ Sheets limite ~20 simultanés | 🔵 Long terme |

---

## 13. Procédure de déploiement

### Modifier le backend (backend.js)
```bash
cd "/home/nicolas/Bureau/algebra live/algebra"
clasp push --force
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "description du changement"
```

### Modifier le frontend (index.html)
Push vers GitHub Pages (auto-deploy) :
```bash
cd "/home/nicolas/Bureau/algebra live/algebra"
git add index.html
git commit -m "feat: description"
git push origin main
```

### Pousser les 5 nouveaux chapitres
```bash
cd "/home/nicolas/Bureau/algebra live/algebra"
python3 push_new_chapters.py --dry-run   # prévisualisation
python3 push_new_chapters.py             # push réel
python3 audit_formats.py                 # vérification conformité
```

---

## 14. Actions manuelles en attente (13 mars 2026)

| Action | Où | Priorité |
|---|---|---|
| ✅ IsAdmin mis à 1 pour `contact@matheux.fr` | Sheet Users | Fait |
| ✅ GAS @34 déployé | Terminal | Fait |
| ✅ 5 chapitres poussés en prod | push_via_gas.py | Fait |
| **⚡ GAS @35 déployer** : `bash deploy.sh "waitlist + email J0"` | Terminal | 🔴 Maintenant |
| **⚡ GA4** : remplacer `G-XXXXXXXXXX` par votre Measurement ID | index.html ligne ~21 | 🟡 Dès que compte GA4 créé |
| Apps Script UI → Déclencheurs → `triggerDailyMarketing` → Chaque jour 9h-10h | Apps Script | 🟡 Cette semaine |
| Stripe → décommenter btn-stripe dans premium.html | premium.html | 🔴 Sprint suivant |
| git push tous les fichiers modifiés | Terminal | 🟡 À faire |

---

## 15. Contacts et ressources

- **Fondateur** : Nicolas Follezou — contact@matheux.fr
- **GitHub** : https://github.com/NicoMPC/algebra
- **Sheet prod** : ID `1zLBajKVL8FUzy7aV2Myi9gYFEFJjnALkLAg0hbicuDk`
- **GAS URL** : `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec`
- **Rapport condensé** : `docs/rapport-condense-2026-03-12.md`

---

*Notice générée le 12 mars 2026 — Matheux v23 GOLD MASTER*
