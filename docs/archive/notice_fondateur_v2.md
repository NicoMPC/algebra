# Notice fondateur — Matheux

> Si tu lis ce document, c'est que tu reprends le projet.
> Tout ce qu'il faut pour comprendre, maintenir et faire grandir Matheux est ici.
> Mise à jour : 17 mars 2026 — GAS @85+ · Lancement J-1

---

## Table des matières

1. [Ce qu'est Matheux](#1-ce-quest-matheux)
2. [À qui ça s'adresse](#2-à-qui-ça-sadresse)
3. [Comment ça marche côté élève](#3-comment-ça-marche-côté-élève)
4. [Le modèle économique](#4-le-modèle-économique)
5. [Ce que tu vois dans l'admin](#5-ce-que-tu-vois-dans-ladmin)
6. [Ta routine quotidienne](#6-ta-routine-quotidienne)
7. [Les emails](#7-les-emails)
8. [Google Sheets — ta base de données](#8-google-sheets--ta-base-de-données)
9. [L'architecture technique (simplifié)](#9-larchitecture-technique-simplifié)
10. [Déployer une modification](#10-déployer-une-modification)
11. [Les comptes de test](#11-les-comptes-de-test)
12. [Avant le lancement — actions restantes](#12-avant-le-lancement--actions-restantes)
13. [En cas de problème](#13-en-cas-de-problème)
14. [La philosophie du produit](#14-la-philosophie-du-produit)
15. [Stratégie de croissance](#15-stratégie-de-croissance)
16. [Liens et accès](#16-liens-et-accès)
17. [Glossaire](#17-glossaire)

---

## 1. Ce qu'est Matheux

Matheux (matheux.fr) est un outil de soutien scolaire en maths pour les collégiens (6ème à 3ème) et les lycéens (1ère Spé Maths). C'est une application web (pas une app native — elle tourne dans le navigateur, sur téléphone comme sur ordinateur).

**Le principe :** un élève fait un diagnostic initial, puis reçoit chaque jour un "boost" de 5 exercices personnalisés. Un prof de maths (Nicolas, le fondateur) supervise tout depuis un dashboard admin : il prépare les boosts, assigne les chapitres, relance les parents par email.

**Ce qui rend Matheux différent :**
- Ce n'est pas "juste un algorithme". Il y a un humain derrière qui suit chaque élève.
- Après 30 jours, l'app connaît les patterns d'erreur de l'élève, sa vitesse, ses lacunes. Cette "empreinte cognitive" ne peut pas être transférée ailleurs.
- 19,99 €/mois — soit 0,66 €/jour, 25× moins cher qu'un cours particulier.

**Les chiffres clés :**

| Donnée | Valeur |
|---|---|
| Niveaux | 6EME, 5EME, 4EME, 3EME, 1ERE Spé Maths |
| Chapitres | 54 (44 collège + 10 lycée) |
| Exercices | 1 872 au total (1 080 curriculum + 108 diagnostic + 540 boost + 144 brevet) — audités et corrigés, score qualité ~98% |
| Prix | 19,99 €/mois |
| Essai gratuit | 7 jours, accès complet, sans carte bancaire |
| Limite bêta | 50 vrais élèves |

---

## 2. À qui ça s'adresse

### L'élève (11-17 ans)
- Collégien ou lycéen avec des lacunes en maths
- Utilise son téléphone ou la tablette familiale
- 10-15 minutes par jour suffisent
- Sensible à la gamification : streak (jours consécutifs), XP, confettis, progression visible

### Le parent (le vrai client)
- Cherche une solution abordable et sérieuse
- Compare avec les cours particuliers (25-40 €/h) et les applis gratuites
- A besoin de confiance : savoir qu'un prof de maths est derrière, pas juste un algorithme
- Reçoit des emails de suivi et un rapport hebdomadaire

### Toi (le fondateur/opérateur)
- 2-3h de travail par jour en phase de lancement
- Gère les boosts quotidiens, les chapitres, les relances parents
- Utilise Google Sheets + le dashboard admin comme outils principaux
- Pas besoin d'être développeur — mais il faut comprendre les workflows

---

## 3. Comment ça marche côté élève

### Le parcours complet d'un nouvel élève

```
Étape 1 : Le parent arrive sur matheux.fr
         Il voit la landing page (11 sections : problème, solution, contraste, système, témoignages, fondateur, prix, FAQ)

Étape 2 : Il clique "Voir où en est mon enfant"
         Un overlay plein écran s'ouvre (quiz diagnostic)

Étape 3 : Choix de la classe (6ème à 3ème)
         Puis sélection des chapitres déjà vus à l'école (min 2 chapitres)

Étape 4 : Quiz diagnostic (4 à 10 questions)
         L'élève répond directement — pas encore inscrit

Étape 5 : Choix de l'objectif
         4 options : Combler mes lacunes / Un chapitre par jour /
         Préparer le brevet / Tout réviser
         Cet objectif personnalise les emails et le suivi

Étape 6 : Inscription (prénom + email + mot de passe)
         Consentement parental obligatoire (RGPD mineurs)
         Le compte est créé instantanément (code 6 caractères)

Étape 7 : Onboarding (3 écrans d'accueil)
         Explication du fonctionnement + incitation à lancer le Boost

Étape 8 : Premier Boost du jour
         5 exercices personnalisés générés à partir du diagnostic
         L'élève commence immédiatement
```

### La routine quotidienne de l'élève

1. **Boost du jour** (obligatoire moralement, pas techniquement) : 5 exercices ciblés, ~10 min
2. **Quartier libre** (après le boost) : chapitres à la demande, Brevet Blanc, révisions
3. À chaque réponse : feedback immédiat, indices si erreur, formule clé
4. En fin de boost : feedback "Comment ça s'est passé ?" (4 choix : Difficile/Moyen/Bien/Top)
5. Confettis + redirection vers les chapitres

### Ce que l'élève voit sur son écran

- **Mon Boost du jour** : carte principale avec 5 exercices. Après complétion : navigation Précédent/Suivant pour revoir ses réponses.
- **Chapitres** : liste de tous les chapitres avec barre de progression. Cartes premium (cadeau irisé pour chapitres jamais ouverts, badge "À découvrir ✨"). Tri intelligent : chapitres du boost > touchés > reste.
- **Cours** : débloqués par paliers (5/10/15/20 exercices faits)
- **Brevet Blanc** (3ème uniquement) : quiz sans indices, style Brevet réel. Verrouillé avec teaser "bientôt disponible".
- **Brouillon + Calculette** : outils contextuels (symboles adaptés au chapitre). Mobile : bottom sheet. Desktop : panneau latéral.
- **Mode nuit** : bouton 🌙 dans le header, persisté entre sessions
- **Signaler une erreur** : bouton 📢 sur tous les modes (boost, chapitre, retro)
- **Figures géométriques SVG** : 18 types auto-détectés depuis l'énoncé (triangles, cercles, parallèles, solides...)
- **Types d'exercices** : QCM (défaut), Vrai/Faux, trous à compléter

### La conversion à J+7

1. À partir de J+5 : un badge "J-X" apparaît discrètement
2. À J+7 : un overlay bloquant dit "19,99 €/mois pour continuer"
3. L'email J+7 est envoyé avec un lien Stripe direct
4. L'élève peut quand même voir sa progression (bouton "Voir quand même")

---

## 4. Le modèle économique

| Élément | Détail |
|---|---|
| Prix | 19,99 €/mois |
| Essai | 7 jours gratuits, accès complet, sans carte bancaire |
| Paiement | Stripe PROD — lien actif `cNicN7b0ebU9bOE9WTb3q01` (limite 50 paiements) |
| Cible phase 1 | 50 clients = ~1 000 € MRR |
| Marge | Quasi 100% (infrastructure gratuite : GitHub Pages + Google Sheets + GAS) |

### Offre flash (conversion boostée)

À J+2 ou J+3, si l'élève est engagé (boost fait, streak actif), tu peux envoyer manuellement une offre -50% premier mois (9,99 €). C'est un lien Stripe séparé créé en 2 minutes sur le dashboard Stripe. Zéro code requis.

### Offres futures (à décider après 10-15 clients)

La colonne "Objectif" dans Google Sheets te dira ce que les clients veulent.

**Règle d'or : ne pas créer ces offres avant d'avoir les données.**

---

## 5. Ce que tu vois dans l'admin

### Comment accéder

Triple-clic sur le logo Matheux en haut de la page. Le dashboard admin apparaît (seuls les comptes `IsAdmin` y ont accès).

### Le cockpit — 3 onglets

Le dashboard affiche 3 onglets : **À FAIRE** / **FAIT** / **TEST**.

**À FAIRE** : chaque élève qui a des actions en attente apparaît sous forme de carte. Les actions sont triées par priorité :

| Rang | Action | Déclencheur | Comment c'est traité |
|---|---|---|---|
| 1 | Contacter le parent | Inactif >7j ET score <40% partout | Bouton "Marquer contacté" |
| 2 | Boost terminé | 5 exos faits, pas de boost en attente | Copier prompt → coller JSON → Publier |
| 3 | Chapitre terminé | 20 exos faits, pas de chapitre assigné | Copier prompt → coller JSON → Publier |
| 4 | Cours à rédiger | Palier 5/10/15/20 atteint, cours vide | Aller à l'éditeur de cours |
| 5 | Brevet en attente | PendingBrevet + 3EME | Ouvrir la fiche → publier |
| 6 | Email J+0 | Inscription, email non envoyé | Voir template → Copier → Marquer envoyé |
| 7 | Email J+3/J+5/J+7 | Selon date inscription | Voir template → Copier → Marquer envoyé |

Bordure gauche de la carte :
- Rouge = contact parent urgent
- Bleu = boost / chapitre / cours / brevet
- Orange = email

**FAIT** : journal horodaté des actions traitées pendant la session + liste des élèves à jour.

**TEST** : comptes de test (IsTest=1), même structure mais pas comptés dans le total À FAIRE.

### Comment préparer un boost

1. L'onglet À FAIRE montre une carte avec l'action "Boost terminé"
2. Tu cliques "Copier le prompt Claude" sur la carte → ça copie un texte
3. Tu colles ce texte dans Claude (claude.ai) → Claude génère un JSON de 5 exercices
4. Tu copies le JSON et le colles dans le champ "Coller le JSON ici" sur la carte
5. Le bouton "Publier" s'active → tu cliques → le boost est enregistré
6. La carte passe automatiquement dans l'onglet FAIT + journal horodaté
7. Au prochain login de l'élève, il verra son nouveau boost

Le même workflow existe pour les chapitres.

### La fiche d'un élève (modale)

- Boost : aperçu, historique, publication
- Chapitres : progression détaillée, scores, temps
- Brevet blanc : sélection chapitres + publication (3ème)
- Révision : assignation chapitres d'une autre année
- Emails : templates éditables J+0/J+3/J+5/J+7
- Profil cognitif : incompréhensions déclarées par l'élève

---

## 6. Ta routine quotidienne

### Le matin (30-45 min)

1. **Ouvre le dashboard admin** (matheux.fr → triple-clic logo)
2. **Regarde l'onglet "À FAIRE"** — toutes les actions classées par priorité
3. **Traite de haut en bas** :
   - Contact parents urgents (bordure rouge) → "Marquer contacté"
   - Boosts terminés (bordure bleue) → Copier prompt → JSON → Publier
   - Chapitres terminés → même workflow
   - Cours à rédiger → aller à l'éditeur
   - Emails J+0/J+3/J+5/J+7 (bordure orange) → Voir template → Copier → Marquer envoyé
4. **Chaque action traitée passe dans l'onglet FAIT** avec un horodatage
5. Quand l'onglet À FAIRE est vide → c'est fini pour la journée

### En continu

- Les élèves font leurs boosts à leur rythme
- Le dashboard se met à jour en temps réel (clique "Actualiser")
- Les résultats arrivent dans Google Sheets automatiquement

### Le dimanche

- Le bouton "Rapport parents" apparaît dans le cockpit admin
- Un clic → envoie automatiquement le bilan hebdo à chaque parent actif
- Le bilan contient : nombre d'exercices faits, % de réussite, chapitres maîtrisés

### Ce qui se passe automatiquement (sans toi)

| Tâche | Déclencheur |
|---|---|
| Boost généré à partir du diagnostic | Inscription élève |
| Progression mise à jour | Chaque réponse de l'élève |
| Streak calculé | Chaque jour d'activité |
| Cours débloqués | Paliers 5/10/15/20 exercices |
| Détection inactivité | Chaque chargement du dashboard |
| Email J+0 (tentative auto) | Inscription (si alias Gmail ok) |

### Ce que tu fais toi (manuellement)

| Tâche | Fréquence |
|---|---|
| Préparer les boosts quotidiens | Chaque matin |
| Assigner les nouveaux chapitres | Quand un chapitre est terminé |
| Envoyer les emails J+3/J+5/J+7 | Selon le timing de chaque élève |
| Relancer les parents d'inactifs | Quand le dashboard le signale |
| Publier les brevets blancs (3ème) | Quand demandé |
| Rédiger les cours par chapitre | Progressivement |
| Email fondateur mensuel | 1×/mois — 20 min à écrire, fort impact rétention |

---

## 7. Les emails

### La séquence

| Email | Quand | Mode | Expéditeur |
|---|---|---|---|
| J+0 bienvenue | Inscription | ✅ Auto | no-reply@matheux.fr |
| Reset mot de passe | Sur demande | ✅ Auto | no-reply@matheux.fr |
| Formulaire contact | Envoi formulaire | ✅ Auto | no-reply@matheux.fr |
| J+3 relance | 3 jours après | Manuel (admin) | — |
| J+5 urgence | 5 jours après | Manuel (admin) | — |
| J+7 conversion | Fin trial | Manuel (admin) | — |
| Rapport parent hebdo | Dimanche | Manuel (bouton admin) | no-reply@matheux.fr |

Les emails J+3/J+5/J+7 pourront être automatisés via le trigger `triggerDailyMarketing` dès 10-20 clients.

### Les boutons email dans le dashboard

1. Tu cliques sur l'email à envoyer (ex: "Copier J+3")
2. Une mini-modale s'ouvre avec l'objet et le corps — **éditables**
3. Tu ajustes si besoin → "Copier"
4. Tu colles dans Gmail et envoies
5. Tu cliques "Marquer comme envoyé" → l'email disparaît de la checklist

### Identité des emails

| Élément | Valeur |
|---|---|
| Expéditeur | `no-reply@matheux.fr` (alias GmailApp via Ionos SMTP) |
| Reply-to | `nicolas@matheux.fr` |
| Contact public | `contact@matheux.fr` |
| Signature | "Nicolas — Prof de maths — Matheux" |
| Ton | Vouvoiement parents, tutoiement élèves |

---

## 8. Google Sheets — ta base de données

Toutes les données de Matheux sont stockées dans un seul fichier Google Sheets. C'est simple mais efficace pour 50-100 élèves.

**ID du fichier :** `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4`

### Les onglets que tu consultes

| Onglet | Ce que tu y trouves |
|---|---|
| **Users** | Tous les comptes : code, prénom, email, niveau, objectif, date d'inscription, statut premium |
| **Suivi** | Ton tableau de bord : 1 ligne par élève avec action prioritaire, chapitres, boost, dernière connexion |
| **Historique** | Journal de toutes les réponses (les plus récentes en haut) |
| **Emails** | Archive de tous les emails envoyés (type, date, statut) |
| **Insights** | Feedbacks des élèves (signalements d'erreur + ressenti de session + incompréhensions) |

### Les onglets techniques (ne pas toucher)

| Onglet | Contenu |
|---|---|
| **Scores** | Toutes les réponses individuelles |
| **Progress** | Score par chapitre par élève |
| **DailyBoosts** | Boosts générés par jour |
| **Curriculum_Officiel** | Les 1 080 exercices (54 chap × 20) |
| **BoostExos** | Les 540 exercices dédiés aux boosts quotidiens |
| **DiagnosticExos** | Les 108 exercices de diagnostic |
| **BrevetExos** | Les 144 exercices type brevet (3ème) |
| **Cours** | Cours par chapitre rédigés depuis l'admin |
| **BrevetResults** | Résultats des brevets blancs |
| **Rapports** | Rapports quotidiens automatiques |
| **Teasing_Early** | Emails collectés en pré-lancement |

### Règle critique

**Ne jamais modifier les colonnes de Google Sheets manuellement.** Les numéros de colonnes sont codés en dur dans le backend. Si tu déranges une colonne, tout casse. La seule colonne que tu peux modifier à la main est `IsAdmin` (colonne G).

---

## 9. L'architecture technique (simplifié)

### Comment les pièces s'assemblent

```
matheux.fr (le site)                    Google Apps Script (le serveur)
   = index.html                           = backend.js
   Hébergé sur GitHub Pages               Hébergé gratuitement par Google
   (repo privé MatheuxApp/algebra)        Lit et écrit dans Google Sheets
        |                                        |
        |  <-- appels réseau (fetch) -->         |
        |                                        |
                                          Google Sheets (la base de données)
                                            = 1 fichier avec 13+ onglets
```

**Coût : 0 €/mois** — tout est gratuit (GitHub Pages, Google Apps Script, Google Sheets).

### Les fichiers du projet

| Fichier | Rôle |
|---|---|
| `index.html` | Tout le site web (~9 900 lignes) : HTML + CSS + JavaScript |
| `backend.js` | Tout le backend (~5 300 lignes) : API + logique métier |
| `deploy.sh` | Script de déploiement rapide (1 commande) |
| `scripts/*.py` | Scripts utilitaires Python (tests, nettoyage, import) |
| `docs/` | Documentation technique |

### Le déploiement

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"

# Déployer le backend (Google Apps Script)
./deploy.sh "description du changement"

# Déployer le frontend (site web)
git add index.html
git commit -m "feat: description du changement"
git push origin main
```

### Outils nécessaires sur la machine

| Outil | Rôle | Installation |
|---|---|---|
| `git` | Gestion du code source | Pré-installé sur Linux/Mac |
| `clasp` | Déploiement Google Apps Script | `npm install -g @google/clasp` |
| `node` | Nécessaire pour clasp | `apt install nodejs` |
| `python3` | Scripts utilitaires | Pré-installé |

---

## 10. Déployer une modification

### Cas 1 : Tu modifies le backend (backend.js)

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"
./deploy.sh "description du changement"
```

Le site utilise toujours la même URL de backend. Le deployment ID ne change jamais.

### Cas 2 : Tu modifies le frontend (index.html)

```bash
git add index.html
git commit -m "feat: description du changement"
git push origin main
```

GitHub Pages redéploie automatiquement en 1-2 minutes.

### Cas 3 : Tu modifies les deux

Backend d'abord (deploy.sh), puis frontend (git push).

---

## 11. Les comptes de test

| Code | Prénom | Email | MDP | Niveau | État |
|---|---|---|---|---|---|
| AUG001 | Auguste | augustecapronm@icloud.com | auguste | 1ERE | Premium 30j, diagnostic simulé |
| PR3CMB | Nicolas | nico@nico.fr | niconcico | 4EME | Trial 7j, 5 chapitres multi-sessions |
| 3M4ZAB | Charlie | charlieboitel6@gmail.com | charlie | 3EME | Trial 7j, diagnostic fait, boost prêt |

Les comptes de test sont marqués `IsTest=1` dans Google Sheets et ne comptent pas dans la limite de 50 élèves.

Le **compte admin** pour accéder au dashboard : code `HMD493`.

---

## 12. Avant le lancement — actions restantes

Le code est 100% prêt. Il reste des actions manuelles :

### ⛔ Avant J+7 (critique)

1. **Finaliser endpoint webhook Stripe** — Stripe Dashboard → Webhooks → créer destination URL GAS + vérifier `whsec_`
2. **Tester un vrai paiement CB** — 19,99€ → vérifier colonne Premium=1 dans Users

### 🟡 Plus tard

3. **Triggers Apps Script** — activer `triggerDailyMarketing` (emails auto J+3/J+5/J+7) dès 10-20 clients
4. **Centraliser les 3 mails** — nicolas@, contact@, no-reply@matheux.fr dans un seul endroit (jeudi 19 mars)
5. **Vidéo fondateur** — tourner + intégrer section landing (18 mars)
6. **Cohérence messages** — vérifier wording après refonte landing (vendredi 20 mars)

---

## 13. En cas de problème

| Symptôme | Cause probable | Solution |
|---|---|---|
| "Erreur serveur" sur le site | Bug dans backend.js | script.google.com → Exécutions → regarder l'erreur |
| Emails pas envoyés | Trigger pas activé | Voir section 12 |
| Élève ne peut pas s'inscrire | Limite 50 atteinte | Vérifier nombre de vrais élèves (IsTest=0) |
| Dashboard admin vide | Pas connecté en admin | Se connecter avec HMD493 |
| Page blanche après déploiement | Erreur JavaScript | F12 → onglet Console |
| Le site ne se met pas à jour | Cache navigateur | Ctrl+Shift+R |
| Un exercice est faux | Erreur dans les données | L'élève clique "Signaler" → ça arrive dans Insights |
| L'élève ne voit pas son boost | Boost pas encore publié | Vérifier la fiche élève dans l'admin |

### Où regarder les logs

1. **Backend** : script.google.com → Projet Matheux → Exécutions
2. **Frontend** : F12 → Console
3. **Google Sheets** : ouvrir le fichier directement

### L'IA comme assistant

Tu peux ouvrir ce projet dans Claude Code et lui demander de l'aide. Il connaît le projet (grâce au fichier CLAUDE.md et au dossier docs/).

---

## 14. La philosophie du produit

### L'IA fait le travail. Le fondateur prend la responsabilité.

Un parent qui a un problème sait qu'il peut écrire à nicolas@matheux.fr et avoir une réponse humaine. Duolingo n'a personne à appeler. Matheux si. C'est ça le fossé.

### Ce qui ne doit JAMAIS changer

1. **L'adresse de réponse** : `nicolas@matheux.fr` (jamais un "no-reply")
2. **La signature** : "Nicolas — Prof de maths — Matheux" (pas "L'équipe Matheux")
3. **Le ton** : vouvoiement parents, tutoiement élèves
4. **La transparence** : ne jamais prétendre que tu as écrit quelque chose que tu n'as pas écrit
5. **La première personne** : "J'ai remarqué que..." et jamais "Notre algorithme a détecté que..."

### La pédagogie

- **Diagnostic avant exercices** : on identifie les lacunes avant de travailler
- **5 exercices par jour = habitude, pas surcharge** (comme Duolingo mais en maths)
- **Indices progressifs** : 1 à 3 étapes + formule clé révélée après erreur
- **2 niveaux de difficulté** : lvl 1 = fondamental, lvl 2 = avancé (type contrôle/brevet)
- **Pas de note** : des scores de confiance (0-100), des barres de progression, des statuts (Fragile/En progrès/Solide/Maîtrisé)

### Qualité des exercices (audit mars 2026)

1 872 exercices audités et corrigés :

| Dimension | Score |
|---|---|
| Correction mathématique | 100% |
| Conformité programme officiel (BO 2024-2026) | 100% |
| Notation décimale française ({,}) | ~99,5% |
| Indices progressifs S1/S2/S3 | ~100% |
| Qualité globale pondérée | **~98%** |

---

## 15. Stratégie de croissance

### Phase 1 : 0 à 50 élèves (maintenant)

- **Acquisition** : bouche-à-oreille, réseaux sociaux, groupes parents
- **Rétention** : suivi personnalisé (chaque élève a un humain derrière)
- **Conversion** : emails J+3/J+5/J+7 + offre flash à J+3
- **Travail fondateur** : 2-3h/jour de boosts + relances + chapitres

### Phase 2 : 50 à 200 élèves

- Automatisation des boosts (agent IA nocturne)
- Rapport parent hebdomadaire automatique
- Travail fondateur : 30-45 min/jour

### Phase 3 : 200+ élèves

- Migration Google Sheets → Supabase (PostgreSQL)
- Migration emails → Brevo ou Resend
- Le fondateur passe de "exécutant" à "superviseur" : 15-20 min/jour

---

## 16. Liens et accès

### Services en production

| Service | URL / ID |
|---|---|
| Site web | matheux.fr |
| Code source | github.com/MatheuxApp/algebra (privé, org Enterprise trial) |
| Google Sheets | ID `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |
| Google Apps Script | script.google.com (projet Matheux) |
| Stripe | dashboard.stripe.com — lien PROD `cNicN7b0ebU9bOE9WTb3q01` |
| Google Analytics | G-7R2DW4585Y |

### Identifiants techniques

| Élément | Valeur |
|---|---|
| URL backend GAS | `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec` |
| Deployment ID | `AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF` |
| Service account (Python) | `algebreboost-sheets-2595a71cadfb.json` (fichier local, pas dans Git) |
| Hash MDP | SHA-256(`email::password::AB22`) — côté navigateur |

### Pages légales

5 pages en production (accessibles via le footer) :
- `mentions-legales.html` — SIRET 837 763 713 00059
- `cgu.html` — mineurs, essai 7j, résiliation, clause bêta
- `cgv.html` — 19,99 €/mois, droit de rétractation 14j
- `politique-confidentialite.html` — RGPD renforcé mineurs
- `politique-cookies.html` — localStorage + GA4 consentement explicite

---

## 17. Glossaire

| Terme | Définition |
|---|---|
| **Boost** | Les 5 exercices personnalisés que l'élève reçoit chaque jour |
| **Chapitre** | Un groupe de 20 exercices sur une notion (ex: Fractions, Pythagore) |
| **Diagnostic** | Le quiz initial qui détecte les lacunes de l'élève |
| **Streak** | Le nombre de jours consécutifs où l'élève a fait son boost |
| **Trial** | La période d'essai gratuit de 7 jours |
| **GAS** | Google Apps Script — la technologie qui fait tourner le backend |
| **Clasp** | L'outil en ligne de commande pour déployer le backend |
| **Dashboard admin** | L'interface d'administration (accessible via triple-clic logo) |
| **JSON** | Un format de données utilisé pour les exercices et les boosts |
| **Prompt Claude** | Le texte qu'on copie dans Claude pour générer des exercices |
| **Empreinte cognitive** | Le profil d'apprentissage unique accumulé par l'élève |
| **MRR** | Monthly Recurring Revenue (revenu mensuel récurrent) |

---

*Matheux — GAS @85+ — 17 mars 2026*
*Document de référence pour la reprise du projet.*
