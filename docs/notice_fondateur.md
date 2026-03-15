# Notice fondateur -- Matheux

> Si tu lis ce document, c'est que tu reprends le projet.
> Tout ce qu'il faut pour comprendre, maintenir et faire grandir Matheux est ici.
> Mise a jour : 15 mars 2026 -- GAS @77

---

## Table des matieres

1. [Ce qu'est Matheux](#1-ce-quest-matheux)
2. [A qui ca s'adresse](#2-a-qui-ca-sadresse)
3. [Comment ca marche cote eleve](#3-comment-ca-marche-cote-eleve)
4. [Le modele economique](#4-le-modele-economique)
5. [Ce que tu vois dans l'admin](#5-ce-que-tu-vois-dans-ladmin)
6. [Ta routine quotidienne](#6-ta-routine-quotidienne)
7. [Les emails](#7-les-emails)
8. [Google Sheets -- ta base de donnees](#8-google-sheets--ta-base-de-donnees)
9. [L'architecture technique (simplifie)](#9-larchitecture-technique-simplifie)
10. [Deployer une modification](#10-deployer-une-modification)
11. [Les comptes de test](#11-les-comptes-de-test)
12. [Avant le lancement -- 3 actions manuelles](#12-avant-le-lancement--3-actions-manuelles)
13. [En cas de probleme](#13-en-cas-de-probleme)
14. [La philosophie du produit](#14-la-philosophie-du-produit)
15. [Strategie de croissance](#15-strategie-de-croissance)
16. [Liens et acces](#16-liens-et-acces)
17. [Glossaire](#17-glossaire)

---

## 1. Ce qu'est Matheux

Matheux (matheux.fr) est un outil de soutien scolaire en maths pour les collegiens (6eme a 3eme) et les lyceens (1ere Spe Maths). C'est une application web (pas une app native -- elle tourne dans le navigateur, sur telephone comme sur ordinateur).

**Le principe :** un eleve fait un diagnostic initial, puis recoit chaque jour un "boost" de 5 exercices personnalises. Un prof de maths (Nicolas, le fondateur) supervise tout depuis un dashboard admin : il prepare les boosts, assigne les chapitres, relance les parents par email.

**Ce qui rend Matheux different :**
- Ce n'est pas "juste un algorithme". Il y a un humain derriere qui suit chaque eleve.
- Apres 30 jours, l'app connait les patterns d'erreur de l'eleve, sa vitesse, ses lacunes. Cette "empreinte cognitive" ne peut pas etre transferee ailleurs.
- 19,99 EUR/mois -- soit 0,66 EUR/jour, 25x moins cher qu'un cours particulier.

**Les chiffres cles :**

| Donnee | Valeur |
|---|---|
| Niveaux | 6EME, 5EME, 4EME, 3EME, 1ERE Spe Maths |
| Chapitres | 54 (44 college + 10 lycee) |
| Exercices | 1 872 au total (1 080 curriculum + 108 diagnostic + 540 boost + 144 brevet) -- audites et corriges, score qualite ~98% |
| Prix | 19,99 EUR/mois |
| Essai gratuit | 7 jours, acces complet, sans carte bancaire |
| Limite beta | 50 vrais eleves |

---

## 2. A qui ca s'adresse

### L'eleve (11-17 ans)
- Collegien ou lyceen avec des lacunes en maths
- Utilise son telephone ou la tablette familiale
- 10-15 minutes par jour suffisent
- Sensible a la gamification : streak (jours consecutifs), XP, confettis, progression visible

### Le parent (le vrai client)
- Cherche une solution abordable et serieuse
- Compare avec les cours particuliers (25-40 EUR/h) et les applis gratuites
- A besoin de confiance : savoir qu'un prof de maths est derriere, pas juste un algorithme
- Recoit des emails de suivi et un rapport hebdomadaire

### Toi (le fondateur/operateur)
- 2-3h de travail par jour en phase de lancement
- Gere les boosts quotidiens, les chapitres, les relances parents
- Utilise Google Sheets + le dashboard admin comme outils principaux
- Pas besoin d'etre developpeur -- mais il faut comprendre les workflows

---

## 3. Comment ca marche cote eleve

### Le parcours complet d'un nouvel eleve

```
Etape 1 : Le parent arrive sur matheux.fr
         Il voit la landing page (argumentaire, temoignages, prix)

Etape 2 : Il clique "Voir ou en est mon enfant"
         Un overlay plein ecran s'ouvre (quiz diagnostic)

Etape 3 : Choix de la classe (6eme a 3eme)
         Puis selection des chapitres deja vus a l'ecole

Etape 4 : Quiz diagnostic (4 a 10 questions)
         L'eleve repond directement -- pas encore inscrit

Etape 5 : Choix de l'objectif
         4 options : Combler mes lacunes / Un chapitre par jour /
         Preparer le brevet / Tout reviser
         Cet objectif personnalise les emails et le suivi

Etape 6 : Inscription (prenom + email + mot de passe)
         Consentement parental obligatoire (RGPD mineurs)
         Le compte est cree instantanement (code 6 caracteres)

Etape 7 : Onboarding (3 ecrans d'accueil)
         Explication du fonctionnement + incitation a lancer le Boost

Etape 8 : Premier Boost du jour
         5 exercices personnalises generes a partir du diagnostic
         L'eleve commence immediatement
```

### La routine quotidienne de l'eleve

1. **Boost du jour** (obligatoire moralement, pas techniquement) : 5 exercices cibles, ~10 min
2. **Quartier libre** (apres le boost) : chapitres a la demande, Brevet Blanc, revisions
3. A chaque reponse : feedback immediat, indices si erreur, formule cle
4. En fin de boost : feedback "Comment ca s'est passe ?" (4 choix : Difficile/Moyen/Bien/Top)
5. Confettis + redirection vers les chapitres

### Ce que l'eleve voit sur son ecran

- **Mon Boost du jour** : carte principale avec 5 exercices. Apres completion : navigation Precedent/Suivant pour revoir ses reponses.
- **Chapitres** : liste de tous les chapitres avec barre de progression. Guide "Commence par la" apparu seulement apres le premier boost consomme.
- **Cours** : debloques par paliers (5/10/15/20 exercices faits)
- **Brevet Blanc** (3eme uniquement) : quiz sans indices, style Brevet reel
- **Brouillon + Calculette** : outils contextuels (symboles adaptes au chapitre)
- **Mode nuit** : bouton lune dans le header, persisté entre sessions

### La conversion a J+7

1. A partir de J+5 : un badge "J-X" apparait discretement
2. A J+7 : un overlay bloquant dit "19,99 EUR/mois pour continuer"
3. L'email J+7 est envoye avec un lien Stripe direct
4. L'eleve peut quand meme voir sa progression (bouton "Voir quand meme")

---

## 4. Le modele economique

| Element | Detail |
|---|---|
| Prix | 19,99 EUR/mois |
| Essai | 7 jours gratuits, acces complet, sans carte bancaire |
| Paiement | Stripe |
| Cible phase 1 | 50 clients = ~1 000 EUR MRR |
| Marge | Quasi 100% (infrastructure gratuite : GitHub Pages + Google Sheets + GAS) |

### Offre flash (conversion boostee)

A J+2 ou J+3, si l'eleve est engage (boost fait, streak actif), tu peux envoyer manuellement une offre -50% premier mois (9,99 EUR). C'est un lien Stripe separe cree en 2 minutes sur le dashboard Stripe. Zero code requis.

### Offres futures (a decider apres 10-15 clients)

La colonne "Objectif" dans Google Sheets te dira ce que les clients veulent. Exemples possibles :

| Si majorite declare | Offre envisagee | Prix |
|---|---|---|
| `lacunes` | Offre actuelle (deja bien) | 19,99 EUR/mois |
| `brevet` | Pack "Prepa Brevet" | 24,99 EUR/mois |
| `chapitre_jour` | Offre "Suivi annuel" (engagement 10 mois) | 14,99 EUR/mois |
| `toutes_matieres` | Offre "Multi-niveaux" (fratrie) | 29,99 EUR/mois |

**Regle d'or : ne pas creer ces offres avant d'avoir les donnees.**

---

## 5. Ce que tu vois dans l'admin

### Comment acceder

Triple-clic sur le logo Matheux en haut de la page. Le dashboard admin apparait (seuls les comptes `IsAdmin` y ont acces).

### Le cockpit -- 3 onglets

Le dashboard affiche 3 onglets : **A FAIRE** / **FAIT** / **TEST**.

**A FAIRE** : chaque eleve qui a des actions en attente apparait sous forme de carte. Les actions sont triees par priorite :

| Rang | Action | Declencheur | Comment c'est traite |
|---|---|---|---|
| 1 | Contacter le parent | Inactif >7j ET score <40% partout | Bouton "Marquer contacte" |
| 2 | Boost termine | 5 exos faits, pas de boost en attente | Copier prompt -> coller JSON -> Publier |
| 3 | Chapitre termine | 20 exos faits, pas de chapitre assigne | Copier prompt -> coller JSON -> Publier |
| 4 | Cours a rediger | Palier 5/10/15/20 atteint, cours vide | Aller a l'editeur de cours |
| 5 | Brevet en attente | PendingBrevet + 3EME | Ouvrir la fiche -> publier |
| 6 | Email J+0 | Inscription, email non envoye | Voir template -> Copier -> Marquer envoye |
| 7 | Email J+3/J+5/J+7 | Selon date inscription | Voir template -> Copier -> Marquer envoye |

Les cartes avec actions de rang 1-5 (contenu a creer) apparaissent en premier.
Les cartes avec seulement des emails (rang 6-7) en dessous.

Bordure gauche de la carte :
- Rouge = contact parent urgent
- Bleu = boost / chapitre / cours / brevet
- Orange = email

Chaque action a son workflow directement SUR la carte : pas besoin d'ouvrir une fiche separee.

**FAIT** : journal horodate des actions traitees pendant la session + liste des eleves a jour.

**TEST** : comptes de test (IsTest=1), meme structure de carte mais pas comptes dans le total A FAIRE.

Le bouton "Actualiser" recharge les donnees fraiches depuis le serveur.

### Comment preparer un boost

C'est l'action la plus frequente. Voici le workflow :

1. L'onglet A FAIRE montre une carte avec l'action "Boost termine"
2. Tu cliques "Copier le prompt Claude" sur la carte -> ca copie un texte
3. Tu colles ce texte dans Claude (claude.ai) -> Claude genere un JSON de 5 exercices
4. Tu copies le JSON et le colles dans le champ "Coller le JSON ici" sur la carte
5. Le bouton "Publier" s'active -> tu cliques -> le boost est enregistre
6. La carte passe automatiquement dans l'onglet FAIT + journal horodate
7. Au prochain login de l'eleve, il verra son nouveau boost

Le meme workflow existe pour les chapitres.

### La fiche d'un eleve (modale)

Disponible en cliquant sur un eleve depuis certaines actions (brevet, revision). Contient :

- Boost : apercu, historique, publication
- Chapitres : progression detaillee, scores, temps
- Brevet blanc : selection chapitres + publication (3eme)
- Revision : assignation chapitres d'une autre annee
- Emails : templates editables J+0/J+3/J+5/J+7

---

## 6. Ta routine quotidienne

### Le matin (30-45 min)

1. **Ouvre le dashboard admin** (matheux.fr -> triple-clic logo)
2. **Regarde l'onglet "A FAIRE"** -- toutes les actions classees par priorite
3. **Traite de haut en bas** :
   - Contact parents urgents (bordure rouge) -> "Marquer contacte"
   - Boosts termines (bordure bleue) -> Copier prompt -> JSON -> Publier
   - Chapitres termines -> meme workflow
   - Cours a rediger -> aller a l'editeur
   - Emails J+0/J+3/J+5/J+7 (bordure orange) -> Voir template -> Copier -> Marquer envoye
4. **Chaque action traitee passe dans l'onglet FAIT** avec un horodatage
5. Quand l'onglet A FAIRE est vide -> c'est fini pour la journee

### En continu

- Les eleves font leurs boosts a leur rythme
- Le dashboard se met a jour en temps reel (clique "Actualiser")
- Les resultats arrivent dans Google Sheets automatiquement

### Le dimanche

- Le bouton "Rapport parents" apparait dans le cockpit admin (en haut, a cote de Actualiser)
- Il envoie automatiquement un bilan personnalise a chaque parent
- Le bilan contient : nombre d'exercices faits, % de reussite, chapitres maitrises

### Ce qui se passe automatiquement (sans toi)

| Tache | Declencheur |
|---|---|
| Boost genere a partir du diagnostic | Inscription eleve |
| Progression mise a jour | Chaque reponse de l'eleve |
| Streak calcule | Chaque jour d'activite |
| Cours debloques | Paliers 5/10/15/20 exercices |
| Detection inactivite | Chaque chargement du dashboard |
| Email J+0 (tentative auto) | Inscription (si alias Gmail ok) |

### Ce que tu fais toi (manuellement)

| Tache | Frequence |
|---|---|
| Preparer les boosts quotidiens | Chaque matin |
| Assigner les nouveaux chapitres | Quand un chapitre est termine |
| Envoyer les emails J+3/J+5/J+7 | Selon le timing de chaque eleve |
| Relancer les parents d'inactifs | Quand le dashboard le signale |
| Publier les brevets blancs (3eme) | Quand demande |
| Rediger les cours par chapitre | Progressivement (pas urgent pour le lancement) |
| Email fondateur mensuel | 1x/mois -- 20 min a ecrire, fort impact retention |

---

## 7. Les emails

### La sequence automatique

| Email | Quand | Destinataire | Contenu |
|---|---|---|---|
| J+0 | Inscription | Parent | Bienvenue, 3 etapes, rappel 7j gratuit |
| J+3 | 3 jours apres | Parent | Encouragement + rappel boost quotidien |
| J+5 | 5 jours apres | Parent | "Encore 2 jours" -- urgence douce + lien Stripe |
| J+7 | Fin du trial | Parent | Trial expire -> lien Stripe direct |
| Rapport hebdo | Dimanche | Parents actifs | Bilan semaine avec stats reelles |
| Reset MDP | Sur demande | Eleve/parent | Code 6 chiffres, expire 15 min |

### Comment les emails fonctionnent

- **J+0** : tente de s'envoyer automatiquement a l'inscription. Si ca echoue (alias Gmail pas configure), tu le fais manuellement depuis le dashboard (bouton "Copier mail de bienvenue").
- **J+3, J+5, J+7** : generes par `triggerDailyMarketing` (un programme qui tourne chaque matin entre 9h et 10h). **Ce trigger doit etre active manuellement** (voir section 12).
- **Rapport hebdo** : genere par `triggerWeeklyParentReport`. Le dimanche, un bouton "Rapport parents" apparait dans le cockpit admin pour l'envoyer manuellement. Peut aussi etre automatise via un trigger Apps Script (a configurer).

### Les emails sont adaptes a l'objectif

L'objectif choisi par l'eleve a l'inscription (lacunes, brevet, chapitre par jour, tout reviser) personalise le contenu des emails J+3, J+5 et J+7. Par exemple, un eleve "brevet" recevra un argumentaire sur les 144 exercices type brevet, tandis qu'un eleve "lacunes" recevra un message sur le diagnostic personnalise.

### Les boutons email dans le dashboard

Depuis la fiche d'un eleve :
1. Tu cliques sur l'email a envoyer (ex: "Copier J+3")
2. Une mini-modale s'ouvre avec l'objet et le corps de l'email -- **editables**
3. Tu ajustes si besoin -> "Copier"
4. Tu colles dans Gmail et envoies
5. Tu cliques "Marquer comme envoye" -> l'email disparait de la checklist

### Identite des emails

| Element | Valeur | Pourquoi |
|---|---|---|
| Expediteur | `no-reply@matheux.fr` | Alias GmailApp |
| Reply-to | `nicolas@matheux.fr` | Les parents qui repondent arrivent sur ta boite |
| Contact public | `contact@matheux.fr` | Affiche sur le site |
| Signature | "Nicolas - Prof de maths - Matheux" | Jamais "L'equipe Matheux" |
| Ton | Vouvoiement parents, tutoiement eleves | Prof humain, pas startup |

### Actions parent

Le dashboard te suggere aussi des messages proactifs a envoyer aux parents :

| Action | Declencheur | Message |
|---|---|---|
| Feliciter le parent | Premier boost termine | "Votre enfant a termine son premier exercice !" |
| Partager le streak | 7 jours consecutifs | "Lucas travaille depuis 7 jours d'affilee" |
| Relance douce | Inactif 3 jours | "On n'a pas vu Lucas depuis 3 jours..." |
| Resultats brevet | Brevet blanc termine | Bilan personnalise |
| Bilan chapitre | 20 exercices completes | Progres sur le chapitre |

Chaque bouton genere un email pret a coller, signe "Nicolas - Prof de maths - Matheux".

---

## 8. Google Sheets -- ta base de donnees

Toutes les donnees de Matheux sont stockees dans un seul fichier Google Sheets. C'est simple mais efficace pour 50-100 eleves.

**ID du fichier :** `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4`

### Les onglets que tu consultes

| Onglet | Ce que tu y trouves |
|---|---|
| **Users** | Tous les comptes : code, prenom, email, niveau, objectif, date d'inscription, statut premium |
| **Suivi** | Ton tableau de bord : 1 ligne par eleve avec action prioritaire, chapitres, boost, derniere connexion |
| **Historique** | Journal de toutes les reponses (les plus recentes en haut) |
| **Emails** | Archive de tous les emails envoyes (type, date, statut) |
| **Insights** | Feedbacks des eleves (signalements d'erreur + ressenti de session) |

### Les onglets techniques (ne pas toucher)

| Onglet | Contenu |
|---|---|
| **Scores** | Toutes les reponses individuelles |
| **Progress** | Score par chapitre par eleve |
| **DailyBoosts** | Boosts generes par jour |
| **Curriculum_Officiel** | Les 1 080 exercices (54 chapitres x 20) |
| **BoostExos** | Les 540 exercices dedies aux boosts quotidiens |
| **DiagnosticExos** | Les 108 exercices de diagnostic |
| **BrevetExos** | Les 144 exercices type brevet (3eme) |
| **Cours** | Cours par chapitre rediges depuis l'admin |
| **BrevetResults** | Resultats des brevets blancs |
| **Rapports** | Rapports quotidiens automatiques |

### Les colonnes cles de Users

| Colonne | Nom | Ce que ca contient |
|---|---|---|
| A | Code | Identifiant unique 6 caracteres (ex: FP48QF) |
| B | Prenom | Prenom de l'eleve |
| C | Niveau | 6EME / 5EME / 4EME / 3EME / 1ERE |
| D | Email | Adresse de l'eleve ou du parent |
| G | IsAdmin | 1 = compte admin (toi) |
| H | Premium | 0 ou 1 |
| I | TrialStart | Date de debut de l'essai gratuit |
| K | IsTest | 1 = compte de test (ne compte pas dans la limite 50) |
| N | Objectif | lacunes / chapitre_jour / brevet / toutes_matieres |

### Regle critique

**Ne jamais modifier les colonnes de Google Sheets manuellement.** Les numeros de colonnes sont codes en dur dans le backend. Si tu deranges une colonne, tout casse. La seule colonne que tu peux modifier a la main est `IsAdmin` (colonne G).

---

## 9. L'architecture technique (simplifie)

### Comment les pieces s'assemblent

```
matheux.fr (le site)                    Google Apps Script (le serveur)
   = index.html                           = backend.js
   Heberge sur GitHub Pages               Heberge gratuitement par Google
   Se deploie auto quand on                Lit et ecrit dans Google Sheets
   pousse du code sur GitHub
        |                                        |
        |  <-- appels reseau (fetch) -->         |
        |                                        |
                                          Google Sheets (la base de donnees)
                                            = 1 fichier avec 13+ onglets
```

**En clair :**
- Le site web (ce que l'eleve voit) est un seul fichier HTML heberge gratuitement sur GitHub Pages
- Quand l'eleve fait quelque chose (repondre a un exercice, se connecter), le site envoie une requete au backend
- Le backend est un programme Google Apps Script (gratuit) qui lit et ecrit dans Google Sheets
- Google Sheets fait office de base de donnees

### Pourquoi c'est comme ca

- **Cout : 0 EUR/mois** (tout est gratuit : GitHub Pages, Google Apps Script, Google Sheets)
- **Simplicite** : pas de serveur a maintenir, pas de base de donnees a gerer
- **Limites** : ca tient pour ~50-100 eleves simultanes. Au-dela, il faudra migrer vers une vraie base de donnees (Supabase/PostgreSQL). Ne pas faire cette migration avant d'avoir le probleme.

### Les fichiers du projet

| Fichier | Role |
|---|---|
| `index.html` | Tout le site web (~9 700 lignes) : HTML + CSS + JavaScript |
| `backend.js` | Tout le backend (~5 100 lignes) : API + logique metier |
| `deploy.sh` | Script de deploiement rapide (1 commande) |
| `scripts/*.py` | Scripts utilitaires Python (tests, nettoyage, import) |
| `docs/` | Documentation technique |

### Le deploiement

Quand tu veux mettre a jour le site :

```bash
# Se placer dans le dossier du projet
cd "/home/nicolas/Bureau/algebra live/algebra"

# Deployer le backend (Google Apps Script)
./deploy.sh "description du changement"

# Deployer le frontend (site web)
git add index.html
git commit -m "description du changement"
git push origin main
```

Le frontend se deploie automatiquement sur matheux.fr quand tu pousses sur GitHub.
Le backend se deploie via `clasp` (un outil en ligne de commande pour Google Apps Script).

### Outils necessaires sur la machine

| Outil | Role | Installation |
|---|---|---|
| `git` | Gestion du code source | Pre-installe sur Linux/Mac |
| `clasp` | Deploiement Google Apps Script | `npm install -g @google/clasp` |
| `node` | Necessaire pour clasp | `apt install nodejs` |
| `python3` | Scripts utilitaires | Pre-installe |

---

## 10. Deployer une modification

### Cas 1 : Tu modifies le backend (backend.js)

C'est le cas quand on change la logique serveur (nouvelles actions, corrections de bugs).

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"

# Methode rapide (push + deploy en 1 commande)
./deploy.sh "description du changement"

# Methode manuelle
clasp push --force
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "desc"
```

Le site utilise toujours la meme URL de backend. Le deployment ID ne change jamais.

### Cas 2 : Tu modifies le frontend (index.html)

C'est le cas quand on change ce que l'eleve voit (interface, textes, logique frontend).

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"
git add index.html
git commit -m "feat: description du changement"
git push origin main
```

GitHub Pages redéploie automatiquement en 1-2 minutes.

### Cas 3 : Tu modifies les deux

Fais le backend d'abord (deploy.sh), puis le frontend (git push).

### Verifier les logs du backend

Si quelque chose ne marche pas cote serveur :
1. Va sur script.google.com
2. Ouvre le projet Matheux
3. Menu "Executions" (icone play a gauche)
4. Tu verras les erreurs recentes

---

## 11. Les comptes de test

Ces comptes sont pre-configures pour tester et faire des demos :

| Code | Prenom | Email | MDP | Niveau | Etat |
|---|---|---|---|---|---|
| AUG001 | Auguste | augustecapronm@icloud.com | auguste | 1ERE | Premium 30j, diagnostic simule |
| PR3CMB | Nicolas | nico@nico.fr | niconcico | 4EME | Trial 7j, 5 chapitres multi-sessions |
| 3M4ZAB | Charlie | charlieboitel6@gmail.com | charlie | 3EME | Trial 7j, diagnostic fait, boost pret |

Les comptes de test sont marques `IsTest=1` dans Google Sheets et ne comptent pas dans la limite de 50 eleves.

Le **compte admin** pour acceder au dashboard : code `HMD493`.

---

## 12. Avant le lancement -- 3 actions manuelles

Le code est 100% pret. Il reste 3 choses a faire manuellement avant d'accepter des vrais clients :

### Action 1 -- Passer Stripe en production

Actuellement, le lien de paiement est un lien de TEST (pas de vrai argent). Il faut le remplacer par un lien de production.

1. Cree un produit "Matheux -- 19,99 EUR/mois" sur dashboard.stripe.com
2. Copie le lien de paiement
3. Remplace `test_14AdRacgw76N7vQcxqa3u00` dans **3 fichiers** :
   - `index.html` (le bouton de paiement)
   - `backend.js` (l'email J+7)
   - `cgv.html` (les conditions de vente)
4. Deploie les deux (`./deploy.sh` + `git push`)

### Action 2 -- Creer les adresses email

Il te faut 2 adresses :
- **contact@matheux.fr** -- adresse publique affichee sur le site
- **no-reply@matheux.fr** -- alias Gmail pour les emails automatiques

Pour l'alias :
1. Va dans Gmail -> Parametres -> Comptes -> "Ajouter une autre adresse"
2. Ajoute `no-reply@matheux.fr`
3. Suis la procedure de verification

### Action 3 -- Activer l'envoi automatique des emails

1. Va sur script.google.com (le projet Matheux)
2. Menu "Declencheurs" (icone horloge a gauche)
3. Clique "Ajouter un declencheur"
4. Configure :
   - Fonction : `triggerDailyMarketing`
   - Frequence : Chaque jour
   - Heure : 9h-10h

Ca activera l'envoi automatique des emails J+3, J+5 et J+7.

Pour le rapport parent hebdo, ajouter un 2eme declencheur :
   - Fonction : `triggerWeeklyParentReport`
   - Frequence : Chaque semaine
   - Jour : Dimanche
   - Heure : 17h-18h

---

## 13. En cas de probleme

### Problemes frequents et solutions

| Symptome | Cause probable | Solution |
|---|---|---|
| "Erreur serveur" sur le site | Bug dans backend.js | Va sur script.google.com -> Executions -> regarde l'erreur |
| Emails pas envoyes | Trigger pas active | Verifie l'Action 3 de la section 12 |
| Eleve ne peut pas s'inscrire | Limite 50 atteinte | Verifie le nombre de vrais eleves dans Users (IsTest=0) |
| Dashboard admin vide | Pas connecte en admin | Connecte-toi avec le compte admin (HMD493) |
| Page blanche apres deploiement | Erreur JavaScript | Ouvre la console du navigateur (F12) -> onglet Console |
| Le site ne se met pas a jour | Cache navigateur | Ctrl+Shift+R (ou vider le cache) |
| Un exercice est faux | Erreur dans les donnees | L'eleve peut cliquer "Signaler" -> ca arrive dans l'onglet Insights |
| L'eleve ne voit pas son boost | Le boost n'est pas encore publie | Verifie la fiche de l'eleve dans l'admin |
| Le rapport hebdo ne s'envoie pas | Trigger pas configure ou pas dimanche | Utilise le bouton "Rapport parents" dans le cockpit admin (visible le dimanche) |

### Ou regarder les logs

1. **Backend (Google Apps Script)** : script.google.com -> Projet Matheux -> Executions
2. **Frontend** : Dans le navigateur, F12 -> Console
3. **Google Sheets** : Ouvre le fichier directement pour voir les donnees

### Contacts techniques

- **Code source** : github.com/NicoMPC/algebra
- **Documentation** : dossier `docs/` dans le projet
- **L'IA** : Tu peux ouvrir ce projet dans Claude Code et lui demander de l'aide. Il connait le projet (grace au fichier CLAUDE.md et au dossier docs/).

---

## 14. La philosophie du produit

### L'IA fait le travail. Le fondateur prend la responsabilite.

C'est la phrase cle. Un parent qui a un probleme sait qu'il peut ecrire a nicolas@matheux.fr et avoir une reponse humaine. Duolingo n'a personne a appeler. Matheux si. C'est ca le fosse.

### Ce qui ne doit JAMAIS changer

1. **L'adresse de reponse** : `nicolas@matheux.fr` (ou l'adresse du repreneur -- jamais un "no-reply")
2. **La signature** : "Nicolas - Prof de maths - Matheux" (pas "L'equipe Matheux")
3. **Le ton** : vouvoiement parents, tutoiement eleves
4. **La transparence** : ne jamais pretendre que tu as ecrit quelque chose que tu n'as pas ecrit
5. **La premiere personne** : "J'ai remarque que..." et jamais "Notre algorithme a detecte que..."

### Le timing humain

Les emails partent entre 9h et 10h (variations naturelles). Les rapports du dimanche entre 17h45 et 18h15. Ca doit avoir l'air envoye par un humain, pas par un robot.

### L'email fondateur (1x/mois)

Un email court, signe du fondateur, envoye a toute la base. Une observation reelle sur le mois ecoule, un conseil, une anecdote pedagogique. 20 minutes a ecrire. Impact fort sur la retention. C'est le genre de chose qu'un parent fait lire a son enfant.

### La pedagogie

- **Diagnostic avant exercices** : on identifie les lacunes avant de travailler
- **5 exercices par jour = habitude, pas surcharge** (comme Duolingo mais en maths)
- **Indices progressifs** : 1 a 3 etapes + formule cle revelee apres erreur
- **2 niveaux de difficulte** : lvl 1 = fondamental, lvl 2 = avance (type controle/brevet)
- **Pas de note** : des scores de confiance (0-100), des barres de progression, des statuts (Fragile/En progres/Solide/Maitrise)

### Qualite des exercices (audit mars 2026)

1 872 exercices ont ete audites et corriges par une IA specialisee le 15 mars 2026 :

| Dimension | Score |
|---|---|
| Correction mathematique | 100% |
| Conformite programme officiel (BO 2024-2026) | 100% |
| Notation decimale francaise ({,}) | ~99,5% |
| Indices progressifs S1/S2/S3 | ~100% |
| Qualite globale ponderee | **~98%** |

Corrections appliquees : 270 notations decimales normalisees, 48 indices S1 reformules (ne donnent plus la reponse directement), 14 exercices 1ERE/Probabilites_Cond reencrits originaux, notations trigonometriques LaTeX standardisees.

Les exercices couvrent **~100% du programme officiel** du college (BO Eduscol) + 1ere Specialite Maths (programme 2019).

---

## 15. Strategie de croissance

### Phase 1 : 0 a 50 eleves (maintenant)

- **Acquisition** : bouche-a-oreille, reseaux sociaux, groupes parents
- **Retention** : suivi personnalise (chaque eleve a un humain derriere)
- **Conversion** : emails J+3/J+5/J+7 + offre flash a J+3
- **Travail fondateur** : 2-3h/jour de boosts + relances + chapitres

### Phase 2 : 50 a 200 eleves

- **Automatisation des boosts** : un agent IA tourne chaque nuit, lit les erreurs, genere automatiquement le boost suivant. Le fondateur valide les anomalies.
- **Rapport parent hebdomadaire automatique** : deja pret dans le code, a activer via trigger
- **Profil d'apprentissage dans l'overlay trial** : montrer a l'eleve ce que Matheux sait sur lui a J+7 ("ces donnees disparaissent dans 48h")
- **Travail fondateur** : 30-45 min/jour (supervision + exceptions)

### Phase 3 : 200+ eleves

- **Migration base de donnees** : Google Sheets -> Supabase (PostgreSQL). A faire quand Sheets montre des signes de lenteur (~100 clients). Budget : 3-5 sessions de dev.
- **Migration emails** : GmailApp -> Brevo ou Resend (300 emails/jour gratuit)
- **Le fondateur passe de "executant" a "superviseur"** : valide les anomalies, repond aux emails humains, redige les cours, envoie les actions parent. 15-20 min/jour max.

### Les mecaniques de retention

| Mecanique | Principe | Etat |
|---|---|---|
| Empreinte cognitive | Apres 30j, l'app te connait -- impossible a transferer | Actif (implicite) |
| Streak comme identite | "Lucas a travaille 12 jours d'affilee -- top 5%" | Actif |
| Rapport parent | Le parent voit les progres chaque semaine | Pret (trigger a activer) |
| Profil avec cadenas a J+7 | "Ces donnees disparaissent dans 48h" | A developper |
| Cout de reconstruction | "Ailleurs il faudrait X semaines pour retrouver ca" | A implementer (wording) |

**Regle d'or : rendre le depart douloureux, pas l'abonnement obligatoire.**

---

## 16. Liens et acces

### Services en production

| Service | URL / ID | Role |
|---|---|---|
| Site web | matheux.fr | Ce que les eleves voient |
| Code source | github.com/NicoMPC/algebra | Depot Git du projet |
| Google Sheets | ID `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` | Base de donnees |
| Google Apps Script | script.google.com (projet Matheux) | Backend API |
| Stripe | dashboard.stripe.com | Paiements |
| Google Analytics | analytics.google.com, propriete `G-7R2DW4585Y` | Statistiques de visite |

### Identifiants techniques

| Element | Valeur |
|---|---|
| URL backend GAS | `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec` |
| Deployment ID | `AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF` |
| Service account (Python) | `algebreboost-sheets-2595a71cadfb.json` (fichier local, pas dans Git) |
| Hash MDP | SHA-256(`email::password::AB22`) -- cote navigateur |

### Pages legales

5 pages en production (accessibles via le footer du site) :
- `mentions-legales.html` -- SIRET 837 763 713 00059
- `cgu.html` -- mineurs, essai 7j, resiliation, clause beta
- `cgv.html` -- 19,99 EUR/mois, droit de retractation 14j
- `politique-confidentialite.html` -- RGPD renforce mineurs
- `politique-cookies.html` -- localStorage + GA4 consentement explicite

---

## 17. Glossaire

| Terme | Definition |
|---|---|
| **Boost** | Les 5 exercices personnalises que l'eleve recoit chaque jour |
| **Chapitre** | Un groupe de 20 exercices sur une notion (ex: Fractions, Pythagore) |
| **Diagnostic** | Le quiz initial qui detecte les lacunes de l'eleve |
| **Streak** | Le nombre de jours consecutifs ou l'eleve a fait son boost |
| **Trial** | La periode d'essai gratuit de 7 jours |
| **GAS** | Google Apps Script -- la technologie qui fait tourner le backend |
| **Clasp** | L'outil en ligne de commande pour deployer le backend |
| **Dashboard admin** | L'interface d'administration (accessible via triple-clic logo) |
| **Checklist** | L'onglet "Aujourd'hui" du dashboard avec toutes les actions a faire |
| **Deploy** | Mettre a jour le code en production (rendre les changements visibles) |
| **Suivi** | L'onglet Google Sheets avec la vue synthetique de chaque eleve |
| **Frontend** | Ce que l'eleve voit (le site web) |
| **Backend** | Ce qui tourne cote serveur (la logique, la base de donnees) |
| **JSON** | Un format de donnees utilise pour les exercices et les boosts |
| **Prompt Claude** | Le texte qu'on copie dans Claude pour generer des exercices |
| **Empreinte cognitive** | Le profil d'apprentissage unique accumule par l'eleve |
| **MRR** | Monthly Recurring Revenue (revenu mensuel recurrent) |
| **@77** | Numero de version actuel du backend (incremente a chaque deploiement) |

---

*Matheux -- GAS @77 -- 15 mars 2026*
*Document de reference pour la reprise du projet.*
*Si tu as des questions, le code source et la documentation technique (dossier docs/) contiennent tous les details.*
