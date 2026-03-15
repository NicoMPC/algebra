# Notice fondateur — Matheux

> Tout ce que tu dois savoir pour lancer et gérer Matheux au quotidien.
> Mise à jour : 15 mars 2026 — GAS @72

---

## 1. Ton site en un coup d'oeil

Matheux (matheux.fr) est un outil de soutien scolaire en maths, 6ème → 3ème + 1ère Spé Maths. L'élève fait un diagnostic, reçoit un boost personnalisé chaque jour, et toi tu suis tout depuis un dashboard admin.

| Donnée | Valeur |
|---|---|
| Niveaux | 6EME, 5EME, 4EME, 3EME, 1ERE Spé |
| Chapitres | 54 (44 collège + 10 lycée) |
| Exercices | 1 872 (1 080 curriculum + 108 diag + 540 boost + 144 brevet) |
| Prix | 19,99 €/mois |
| Essai gratuit | 7 jours, accès complet, sans CB |
| Limite bêta | 50 vrais élèves |
| Tests QA | 74/74 unitaires + simulation 10 profils (111 appels API, 0 erreur) |

---

## 2. Parcours d'un élève

```
Landing → Diagnostic (4-10 questions) → Choix objectif → Inscription
   → Onboarding (3 slides) → Boost J0 (5 exos) → Routine quotidienne
   → J+7 : overlay conversion → Stripe → Premium
```

### Choix de l'objectif (nouveau @70)

Après le quiz diagnostic, un écran plein écran propose 4 choix :

| Bouton | Clé stockée | Usage |
|---|---|---|
| Combler mes lacunes | `lacunes` | Template email par défaut |
| Un chapitre par jour | `chapitre_jour` | Emails adaptés "rythme quotidien" |
| Préparer le brevet | `brevet` | Emails "144 exos brevet + blancs" |
| Tout réviser | `toutes_matieres` | Emails "accès complet" |

L'objectif est stocké dans la **colonne N (Objectif)** de Users et visible dans le dashboard admin (badge vert sur la fiche élève).

---

## 3. Ce que tu vois dans l'admin

### Fiche élève

```
[Avatar] Lucas
         6EME · il y a 2j  🎯 Combler ses lacunes
```

Pour chaque élève tu vois :
- **Niveau + dernière connexion**
- **Badge objectif** (vert) — ou "objectif non renseigné" si inscrit avant @70
- **Boost du jour** : en cours (2/5), terminé, ou "aucun boost"
- **Chapitres actifs** (max 4 slots) avec statut et progression
- **Action prioritaire** : ce qu'il faut faire pour cet élève

### Actions prioritaires (tri automatique)

Le dashboard trie les élèves par urgence :

| Action | Signification | Ce que tu fais |
|---|---|---|
| BOOST TERMINE | L'élève a fini ses 5 exos | Prépare le prochain boost ou assigne un chapitre |
| Chapitre terminé | 20 exos faits sur un chapitre | Assigne le chapitre suivant |
| Sans nouvelles | Inactif > 7 jours | Relance personnalisée |
| RAS | Tout va bien | Rien à faire |

### Emails à envoyer

L'admin affiche les emails en attente par élève :

| Email | Quand | Contenu |
|---|---|---|
| J+0 | Inscription | Bienvenue (envoyé automatiquement) |
| J+3 | 3 jours après | Relance douce |
| J+5 | 5 jours avant fin trial | Urgence "plus que 2 jours" |
| J+7 | Fin du trial | Conversion avec lien Stripe |

Les boutons "Copier J+X" génèrent un email **adapté à l'objectif** de l'élève. Tu n'as qu'à coller et envoyer.

### Brevet blanc (3EME)

Tu peux publier un brevet blanc personnalisé par élève :
1. Clique sur un élève 3EME
2. Sélectionne les chapitres à évaluer
3. Publie → l'élève voit un brevet blanc à son prochain login

---

## 4. Routine quotidienne (2-3h)

### Le matin (9h-10h)

1. **Ouvre le dashboard admin** sur matheux.fr (connexion admin)
2. **Traite les actions urgentes** (en haut de liste) :
   - Boost terminé → prépare le suivant
   - Chapitre terminé → assigne le prochain
   - Sans nouvelles → relance par email
3. **Envoie les emails** J+3/J+5/J+7 (boutons "Copier" dans le dashboard)
4. **Vérifie les inscriptions** du jour (J+0 envoyé automatiquement)

### En continu

- Les élèves font leurs boosts à leur rythme
- Le dashboard se met à jour en temps réel
- Tu reçois les résultats dans Google Sheets

---

## 5. Google Sheets — ton tableau de bord

### Onglets principaux

| Onglet | Contenu |
|---|---|
| **Users** | Tous les comptes (Code, Prénom, Email, Niveau, Objectif, TrialStart, Premium) |
| **Scores** | Tous les résultats (Code, Chapitre, Résultat EASY/MEDIUM/HARD, Temps, Source) |
| **DailyBoosts** | Boosts générés par jour (Code, Date, ExosDone, BoostJSON) |
| **Progress** | Progression par chapitre (Code, Chapitre, NbExos, Score, Statut) |
| **Suivi** | Vue synthétique admin (Action, Chapitres, Boost, Dernière connexion) |
| **Emails** | Log de tous les emails envoyés (Email, Type, Date, Statut) |

### Colonnes clés de Users

| Colonne | Contenu |
|---|---|
| A — Code | Identifiant unique 6 caractères |
| C — Niveau | 6EME / 5EME / 4EME / 3EME / 1ERE |
| E — Email | Adresse de l'élève/parent |
| I — TrialStart | Date début essai (format YYYY-MM-DD) |
| J — Premium | `trial` / `premium` / `expired` |
| N — Objectif | `lacunes` / `chapitre_jour` / `brevet` / `toutes_matieres` |
| O — IsTest | `1` = compte de test (pas compté dans la limite 50) |

---

## 6. Avant de lancer — 3 actions manuelles obligatoires

### Action 1 — Stripe TEST vers PROD

Remplacer le lien Stripe de test par le lien de production dans **3 fichiers** :

| Fichier | Chercher | Remplacer par |
|---|---|---|
| `index.html` | `test_14AdRacgw76N7vQcxqa3u00` | Ton lien Stripe PROD |
| `backend.js` | `test_14AdRacgw76N7vQcxqa3u00` | Ton lien Stripe PROD |
| `cgv.html` | `test_14AdRacgw76N7vQcxqa3u00` | Ton lien Stripe PROD |

Puis redéployer : `./deploy.sh "Stripe PROD"`

### Action 2 — Créer les adresses email

1. **contact@matheux.fr** — adresse publique visible sur le site
2. **no-reply@matheux.fr** — alias Gmail pour les emails automatiques (GmailApp)

Configuration : Hébergeur email + Gmail → Paramètres → Comptes → Ajouter un alias

### Action 3 — Activer le trigger emails automatiques

1. Ouvre Apps Script (script.google.com)
2. Menu : Déclencheurs (icône horloge)
3. Ajouter un déclencheur :
   - Fonction : `triggerDailyMarketing`
   - Fréquence : Chaque jour
   - Heure : 9h-10h

---

## 7. Déploiement du code

Quand tu modifies le code (ou qu'on le fait ensemble) :

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"

# Méthode rapide (push + deploy en 1 commande)
./deploy.sh "description du changement"

# Commit Git
git add . && git commit -m "feat: ..."
git push origin main
```

---

## 8. Comptes de test

Ces comptes sont prêts pour démonstration :

| Code | Prénom | Email | MDP | Niveau | État |
|---|---|---|---|---|---|
| AUG001 | Auguste | augustecapronm@icloud.com | auguste | 1ERE | Premium 30j, diag simulé |
| PR3CMB | Nicolas | nico@nico.fr | niconcico | 4EME | Trial 7j, 5 chapitres multi-sessions |

Les 10 profils SIM01-SIM10 (@sim.matheux.fr) sont des profils de simulation automatique (IsTest=1), visibles dans l'admin pour tester tous les scénarios.

---

## 9. En cas de problème

| Symptôme | Cause probable | Solution |
|---|---|---|
| "Erreur serveur" sur le site | Bug backend GAS | Regarde les logs : Apps Script → Exécutions |
| Emails pas envoyés | Trigger pas activé | Vérifie Action 3 ci-dessus |
| Élève ne peut pas s'inscrire | Limite 50 atteinte | Vérifier Users (IsTest=0 uniquement) |
| Dashboard admin vide | Pas connecté en admin | Se connecter avec le compte admin (HMD493) |
| Page blanche après déploiement | sw.js poussé dans GAS | Vérifier que sw.js est dans .claspignore |

---

## 10. Liens utiles

| Ressource | URL |
|---|---|
| Site | matheux.fr |
| Google Sheets (données) | sheets.google.com → ID `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |
| Apps Script (code backend) | script.google.com → Projet Matheux |
| GitHub (code source) | github.com/NicoMPC/algebra |
| Stripe (paiements) | dashboard.stripe.com |
| Analytics | analytics.google.com → G-7R2DW4585Y |

---

*Matheux — GAS @72 — 15 mars 2026*
