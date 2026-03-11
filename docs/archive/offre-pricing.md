# Offre & Pricing — Matheux (mac.fr)
> Document de travail fondateur — MVP solo, objectif 50 clients × 9,99€/mois

---

## 1. Comparatif modèles freemium

| Modèle | Description | Avantages | Risques | À quel stade ? |
|---|---|---|---|---|
| **Free limité** (ex: 3 exos/jour) | Accès partiel permanent, quota journalier | Rétention longue, L'élève revient chaque jour | Frustration si mur trop tôt, "3 exos c'est rien" → désinstall | Stade 2+ (quand tu as 20+ clients, tu testes le mur) |
| **Freemium 7 jours plein accès** | Accès total 7 jours, puis payant | L'élève voit TOUTE la valeur avant de payer, conversion sur usage réel | Si l'élève ne crée pas d'habitude en 7j, il part. Délai avant revenu. | Stade MVP (maintenant) — modèle recommandé |
| **Free avec pub** | Google Ads in-app, version gratuite financée par pub | Pas de friction paiement, volume d'abord | Pub sur contenu éducatif pour mineurs : RGPD/COPPA problématique, très mauvaise image parental, revenus pub dérisoires à petite échelle | À éviter — incompatible avec la cible parents sérieux |
| **Payant direct** (diagnostic gratuit, reste payant) | Diagnostic gratuit offert, chapitres + boost derrière paywall | Revenu immédiat dès J1, pas de freeloaders | Friction haute avant valeur démontrée, panier moyen cible → parents hésitants sans preuve | Stade 2 (quand tu as des témoignages et la notoriété) |
| **Essai sans CB, conversion email** | Accès libre, puis relance email manuelle | Zéro friction à l'entrée, permet volume rapide, idéal sans Stripe | Taux conversion email faible (5-15%), fastidieux à gérer manuellement au-delà de 20 inscrits | Stade MVP — parfait pour les 10 premiers clients |

**Synthèse :** Pour un fondateur solo sans Stripe intégré, la combinaison **freemium 7 jours + relance email manuelle** est la plus adaptée maintenant.

---

## 2. Inscription d'abord vs diagnostic d'abord

### Parcours A — Inscription email → accès app → diagnostic → chapitres

**Flux :** page d'accueil → formulaire email/mdp/niveau → diagnostic → chapitres

| Critère | Analyse |
|---|---|
| Taux de conversion à l'entrée | Moyen (30-50% des visiteurs) — la friction email filtre les curieux mais garde les motivés |
| Valeur démontrée | Retardée : l'élève doit s'inscrire AVANT de voir quoi que ce soit |
| Friction | Forte au départ (formulaire), faible ensuite |
| Données RGPD | Email collecté dès le départ — consentement parental requis si <15 ans, obligatoire en France |
| Avantages | Données tracées dès J1, relance email possible, compte persistant garanti |
| Inconvénients | Si le diagnostic est décevant, l'élève s'est quand même inscrit — experience potentiellement négative liée au compte |

### Parcours B — Diagnostic anonyme → résultats → email pour sauvegarder

**Flux :** page d'accueil → diagnostic sans compte → résultats + lacunes → "Crée un compte pour sauvegarder et continuer"

| Critère | Analyse |
|---|---|
| Taux de conversion à l'entrée | Élevé (60-80% des visiteurs essaient le diagnostic) — pas de friction initiale |
| Valeur démontrée | Immédiate : l'élève voit ses lacunes AVANT de s'inscrire |
| Friction | Faible à l'entrée, mais "rupture" au moment de créer le compte |
| Données RGPD | Aucune donnée collectée avant consentement — plus sain pour les mineurs, moins de risque juridique au lancement |
| Avantages | Démo de valeur avant engagement, taux d'essai plus haut, preuve concrète pour les parents |
| Inconvénients | Résultats du diagnostic potentiellement perdus si l'élève ne s'inscrit pas, complexité technique légèrement plus haute |

### Recommandation

**Conserver le Parcours A pour le MVP**, avec une modification clé : **réduire au maximum le formulaire d'inscription** (juste email + mot de passe + niveau scolaire, sans prénom obligatoire côté parents).

Justification :
1. **La codebase actuelle est Parcours A** — le changer maintenant est coûteux et risqué pour un solo.
2. **La cible parents** cherche un outil sérieux, pas un jeu en ligne. L'inscription email crée un signal de sérieux : "je confie les données de mon enfant à un professionnel".
3. **RGPD mineurs** : le Parcours B collecte techniquement des réponses au diagnostic sur un mineur sans consentement préalable. En France, si l'élève a moins de 15 ans, c'est une zone grise. Avec le Parcours A, le consentement est recueilli à l'inscription.
4. **Le diagnostic comme accroche marketing** : présenter des exemples de questions du diagnostic sur la landing page suffit à démontrer la valeur sans les inconvénients du Parcours B.

Évolution future : tester le Parcours B à partir de 50 clients et une landing page avec témoignages.

---

## 3. Options de pricing

### 9,99€/mois

| | |
|---|---|
| **Pour qui** | Parents qui budgétisent mois par mois, veulent tester avant de s'engager |
| **Argument principal** | Prix psychologique sous 10€, comparable à une séance de 5 minutes avec un prof particulier, sans les 25€/heure |
| **Contre-argument** | Churn mensuel élevé si l'élève "n'a plus besoin" (fin de trimestre, vacances), revenu MRR instable |
| **Friction Stripe** | Standard — une CB à renseigner, renouvellement automatique |
| **Valeur perçue** | Faible si pas de comparaison explicite ("moins cher qu'un cours particulier") |
| **À quel stade** | Maintenant — prix de lancement à maintenir jusqu'à 50 clients |

### 79€/an (= 6,58€/mois, économie de 40,76€)

| | |
|---|---|
| **Argument principal** | Encaissement immédiat d'un an de revenu, MRR prédictible, parents "set and forget" |
| **Comment le présenter** | "79€/an — économisez 40,76€ par rapport au mensuel", "moins de 22cts/jour pour 1h de maths personnalisées" |
| **Contre-argument** | Engagement fort demandé avant que l'élève ait prouvé son usage. Parents réticents au virement annuel pour un outil inconnu. |
| **Avantages MRR** | 1 client annuel = 6,6 clients mensuels en encaissement immédiat. À 10 clients annuels, c'est 790€ cash day 1. |
| **À quel stade** | Stade 2 (après 10 clients satisfaits avec témoignages). Proposer en upsell sur la page de renouvellement mensuel. |

### Pack famille (2 enfants = 15€/mois)

| | |
|---|---|
| **Argument principal** | +50% de revenu par famille, NPS explose (les parents ont 2+ enfants en collège), effet "bouche à oreille familial" |
| **Contre-argument** | Complexité technique légère (2 comptes liés), à ne pas proposer avant que le produit soit stable |
| **Impact LTV** | LTV × 1,5 avec churn similaire — une famille qui reste 12 mois = 180€ vs 120€ |
| **Comment proposer** | "Vous avez un deuxième enfant au collège ? Ajoutez-le pour 5€/mois de plus" |
| **À quel stade** | Stade 2-3, après validation produit sur 20+ familles |

### Pricing par niveau scolaire (6ème ≠ 3ème)

| | |
|---|---|
| **Argument** | 3ème = brevet = enjeu plus fort → parents potentiellement prêts à payer plus (12,99€?) |
| **Contre-argument** | Complexité inutile au MVP. Parents comparent entre frères et sœurs. Injuste perçu ("pourquoi mon 6ème vaut moins ?"). Segmentation prématurée. |
| **Verdict** | À éviter — un seul prix pour tous les niveaux jusqu'à 200+ clients |

---

## 4. Recommandation MVP

**Modèle retenu : Freemium 7 jours plein accès, puis 9,99€/mois, relance email manuelle, sans Stripe jusqu'à 10 clients.**

1. Les 7 premiers jours sont gratuits sans CB — zéro friction, l'élève crée l'habitude quotidienne.
2. À J7, email automatique (GAS + Gmail) : "Votre accès gratuit se termine dans 48h — continuez pour 9,99€/mois" avec lien PayPal.me ou virement.
3. Prix unique 9,99€/mois pour tous les niveaux, pas de plan annuel avant 10 clients satisfaits.
4. **Ce qu'on teste en premier** : est-ce que les parents payent après 7 jours d'usage ? Si oui → on automatise. Si non → on interroge les 3-5 non-convertis pour comprendre pourquoi.
5. Seuil Stripe : dès le 10ème client, intégrer Stripe Checkout pour automatiser les relances et éviter les impayés.

---

## 5. 10 premiers clients sans Stripe

### Avant tout : tenir un tableur de suivi

Créer un Google Sheet "Clients Matheux" avec les colonnes :
`Prénom | Email | Niveau élève | Date inscription | Date fin essai | Moyen paiement | Date paiement | Statut | Notes`

Statuts possibles : `ESSAI` / `RELANCÉ` / `PAYÉ` / `ABANDONNÉ` / `GRATUIT_EXCEPTIONNEL`

---

### Option 1 — Virement bancaire (recommandé pour les premiers)

**Avantages :** zéro commission, professionnel perçu, traçable.

**Procédure :**
1. Envoyer un email à J7 avec ton IBAN et le montant (9,99€).
2. Objet suggéré : "Votre accès Matheux — comment continuer ?"
3. Mettre un **libellé obligatoire** : `MATHEUX-[PRÉNOM]-[MOIS]` pour identifier les virements.
4. Vérifier les arrivées bancaires chaque lundi, mettre à jour le tableur.
5. Envoyer un email de confirmation dès réception : "Paiement reçu, accès prolongé jusqu'au [date+30j]".

**Limite :** fastidieux au-delà de 15 clients, pas de renouvellement automatique.

---

### Option 2 — PayPal.me

**Avantages :** immédiat, pas besoin de compte pro, lien cliquable dans l'email.

**Procédure :**
1. Créer un compte PayPal personnel ou pro (gratuit).
2. Lien direct dans l'email : `paypal.me/tonnom/9.99EUR` — le parent clique, entre sa CB, c'est fait.
3. Commission PayPal : ~2,9% + 0,35€ = environ 0,64€ par transaction. Acceptable à ce stade.
4. PayPal envoie un email de notification à chaque paiement → reporter dans le tableur.

**Limite :** pas de renouvellement automatique, chaque mois nécessite une relance.

---

### Option 3 — HelloAsso

**Avantages :** zéro commission pour l'émetteur (les frais sont optionnellement pris en charge par le payeur), génère un reçu automatique, adapté aux indépendants et associations.

**Procédure :**
1. Créer une "campagne de don" ou "adhésion" sur HelloAsso (compte gratuit).
2. Titre : "Abonnement Matheux — 9,99€/mois"
3. Envoyer le lien dans l'email de relance.
4. HelloAsso envoie un reçu automatique au parent — professionnel et rassurant.

**Note :** HelloAsso est prévu pour associations, mais rien n'interdit un indépendant. À utiliser si tu veux des reçus sans micro-entreprise active.

---

### Option 4 — Sumeria (ex-Lydia Pro) ou Lydia

**Avantages :** lien de paiement direct par SMS ou email, très simple pour les parents peu technophiles.

**Procédure :**
1. Créer un compte Sumeria Pro (gratuit jusqu'à un certain volume).
2. Envoyer une demande de paiement directement depuis l'app.
3. Le parent reçoit un SMS/email et paie en 2 clics.

**Limite :** moins professionnel visuellement qu'un vrai checkout, adapté surtout à une relation directe (si tu connais l'élève IRL comme prof).

---

### Relance mensuelle manuelle

**Procédure à répéter chaque mois (< 1h pour 10 clients) :**

1. Le 1er de chaque mois : filtrer le tableur sur les clients dont le paiement date de >28 jours.
2. Envoyer l'email de relance (template à préparer une fois) :
   > Sujet : "Matheux — renouvellement de [Prénom]"
   > "Bonjour, l'abonnement de [Prénom] se renouvelle ce mois-ci. Pour continuer : [lien PayPal / IBAN]. Montant : 9,99€. Merci !"
3. Si pas de paiement sous 5 jours : envoyer un rappel.
4. Si pas de paiement sous 10 jours : désactiver le compte manuellement (changer le hash ou ajouter un flag dans Users sheet).
5. Reporter le paiement dans le tableur dès réception.

**Temps estimé :** 5 min par client par mois, soit 50 min pour 10 clients.

---

### Quand migrer vers Stripe

**Seuil recommandé : 10 clients actifs payants.**

Signaux pour migrer :
- Les relances manuelles prennent plus d'1h/semaine.
- Tu as au moins 1 impayé à gérer (Stripe automatise les relances d'échec).
- Tu veux proposer l'abonnement annuel (Stripe gère ça nativement).

**Migration Stripe :**
1. Créer un compte Stripe (micro-entreprise ou auto-entrepreneur requis).
2. Utiliser Stripe Checkout (pas besoin de dev) — crée un lien de paiement en 5 min.
3. Intégrer le webhook Stripe → colonne `Premium` dans Users (déjà prévu dans la roadmap BLOC 3).
4. Communiquer aux clients existants : "Nous passons à un paiement automatique — cliquez ici pour renseigner votre CB une seule fois".

**Coût Stripe :** 1,4% + 0,25€ par transaction pour les cartes européennes = ~0,39€ sur 9,99€. Négligeable.
