# 52 — Légal : CGV, CGU, confidentialité (brouillons)

> Agent : growth-cro · 24/09/2026 · Statut : **brouillon, non publié, non relu par un professionnel**
> ⚠️ **Rien dans ce fichier n'est un avis juridique.** Ce sont des brouillons rédigés pour gagner du temps.
> Tout ce qui est marqué ⚠️ **doit être relu par un juriste** (avocat en droit de la consommation / numérique,
> ou service juridique d'une CCI / d'un réseau d'indépendants) **avant publication**. Les numéros d'articles
> ont été vérifiés quand c'est indiqué ; les autres sont à contrôler.
> Liés : `50-offre-conversion.md`, `51-emails.md`.

---

## 0. Points bloquants avant de vendre la nouvelle offre

| # | Bloquant | Pourquoi | Où |
|---|---|---|---|
| B1 | **CGV à réécrire** | Elles vendent 29,99 € « jusqu'au 30 juin 2026 » : produit, prix et durée faux. Vendre le diagnostic ou le programme sous ces CGV = information précontractuelle erronée. | §8 |
| B2 | **Case de renonciation + confirmation sur support durable** pour le diagnostic | Sans elles, le droit de rétractation reste entier. Pire : si l'information sur la rétractation est absente ou fausse, le délai est **prolongé de 12 mois** (art. L221-20). | §2 |
| B3 | **Ne jamais inciter l'ado à acheter ni à convaincre ses parents** | Pratique commerciale réputée agressive envers les enfants (liste noire). Le paywall ado et la landing sont concernés. | §6 |
| B4 | **Politique de confidentialité fausse** | Elle annonce Google Sheets / Apps Script comme hébergeur unique. En réalité : Supabase, Resend, Stripe, GitHub Pages, GA4, et potentiellement un LLM. Aucun de ces sous-traitants n'est listé. | §10 |
| B5 | **Consentement parental non vérifié** | Aujourd'hui, c'est l'ado qui coche « je certifie être son responsable légal ». Il faut une confirmation par le parent (email). | §4 |
| B6 | **Emails de conversion sans opt-in** | Prospection par email B2C = consentement préalable (art. L34-5 CPCE), sauf exception « client » discutable pour un compte gratuit. | §7 |
| B7 | **Suppression effective des anciennes données** | La décision « anciens comptes supprimés » (contrat §7) doit couvrir **aussi** le Google Sheet de backup, les tables `emails`/`email_logs` et Stripe (clients), sinon la politique affichée est fausse. | §5.4 |

Non bloquants mais à corriger au passage : mention « EI », plateforme RLL européenne (fermée), médiateur (contrat à vérifier), CGU « réservé aux 3e » (redevient vrai), badge « Droit de rétractation 14 jours » de `premium.html`.

---

## 1. État des lieux (lu le 24/09/2026)

| Document | Problème | Gravité |
|---|---|---|
| `cgv.html` | 29,99 € + « accès jusqu'au 30 juin 2026 (Brevet 2026) » : contraire à T2 et à la nouvelle offre | 🔴 |
| `cgv.html` art. 6 | Droit de rétractation 14 jours sans aucune exception, alors que le contenu est numérique. Ça ne correspond à aucun mécanisme réel de renonciation. | 🔴 |
| `cgv.html` art. 10 | Lien vers la plateforme européenne RLL (ec.europa.eu/consumers/odr) : **fermée définitivement le 20/07/2025**, la mention n'est plus requise ([source](https://www.haas-avocats.com/plateformes/cgv/fermeture-de-la-plateforme-odr-e-commercants-mettez-a-jour-vos-cgv/)) | 🟠 |
| `cgv.html` art. 10 | Médiateur CNPM cité : ⚠️ **vérifier qu'un contrat d'adhésion est en cours** (la désignation d'un médiateur suppose une convention avec lui) | 🟠 |
| `cgv.html` / `cgu.html` / mentions | « auto-entrepreneur » : depuis la loi du 14/02/2022, l'entrepreneur individuel doit faire figurer « EI » ou « entrepreneur individuel » à côté de son nom sur ses documents ⚠️ vérifier | 🟡 |
| `cgu.html` | « Gratuitement pour 1 chapitre complet » : l'offre gratuite devient « diagnostic express + 5 exos/jour ». « Réservé aux élèves de 3ème » : redevient exact. | 🟠 |
| `cgu.html` art. 4 | « Consentement obligatoire pour les moins de 15 ans » : ça ne dit pas **comment** il est recueilli. En pratique, il est coché par l'ado. | 🔴 |
| `politique-confidentialite.html` | Hébergement Google Sheets/Apps Script, sous-traitant Google uniquement, pas de Stripe/Resend/Supabase/GitHub/GA4, « durée du compte + 1 an » (conservation après suppression injustifiée), pas de mention du partage de bilan, du PDF, des emails marketing | 🔴 |
| `premium.html` | « Droit de rétractation 14 jours » en badge rassurant : présenter un droit légal comme argument commercial = risque de pratique trompeuse. Et c'est inexact si on fait renoncer. | 🟠 |
| `docs/product.md` | Parle encore de CGV « 19,99 €/mois » et d'« essai 7 j » | 🟡 (doc interne) |

---

## 2. Vente de contenu numérique : droit de rétractation

### 2.1 Rappel des textes (vérifiés sur Légifrance le 24/09/2026 pour L221-28)

- **L221-18** : 14 jours de rétractation pour les contrats à distance.
- **L221-28 13°** (version en vigueur depuis le 28/05/2022) : pas de rétractation pour la « fourniture d'un contenu numérique sans support matériel dont l'exécution a commencé avant la fin du délai de rétractation » si **a)** le consommateur a donné son **consentement exprès préalable** à l'exécution immédiate, **b)** il a **reconnu qu'il perdra son droit de rétractation**, **c)** le professionnel lui a **fourni une confirmation** conformément à **L221-13 al. 2** (support durable). ([Légifrance](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044563170))
- **L221-28 1°** : pas de rétractation pour les services **pleinement exécutés** avant la fin du délai, avec accord exprès et reconnaissance de la perte du droit.
- **L221-25** : si le consommateur a demandé que l'exécution d'un **service** commence pendant le délai et qu'il se rétracte ensuite, il paie un **montant proportionnel** à ce qui a été fourni. ⚠️ Vérifier le régime exact des « services numériques » après l'ordonnance 2021-1734.
- **L221-20** : si l'information sur le droit de rétractation n'a pas été fournie, le délai est **prolongé de 12 mois**.
- **L221-14** : le bouton de commande doit indiquer clairement l'obligation de paiement (« commande avec obligation de paiement » ou une formule analogue sans ambiguïté). Le bouton « Payer » de Stripe Checkout est a priori conforme ⚠️.

### 2.2 Qualification des deux produits ⚠️ juriste

| Produit | Qualification proposée | Conséquence |
|---|---|---|
| **Diagnostic complet + PDF** (19 €) | **Contenu numérique** fourni sans support matériel (un test interactif et un bilan généré, livrés en quelques heures ou jours). Exécution = ouverture du module 1. | **Renonciation possible** (L221-28 13°) avec case + confirmation. |
| **Programme Brevet** (49 € / 30 €) | Plutôt un **service numérique** continu (entraînement, re-diagnostic mensuel, brevets blancs sur ~9 mois). Il n'est pas « pleinement exécuté » en 14 jours. | **Rétractation 14 jours maintenue**, avec montant proportionnel possible si l'exécution a commencé à la demande (L221-25). **En pratique : notre garantie 30 jours rembourse intégralement**, donc on ne retient jamais de prorata. |

Question pour le juriste : un produit mixte (passation interactive + PDF) peut-il être intégralement qualifié de contenu numérique ? Si ce n'est pas le cas, la renonciation ne jouerait que sur le PDF. Avec la garantie 30 jours, l'enjeu financier est quasi nul, mais **la qualité de l'information précontractuelle, elle, n'est pas négociable** (L221-20).

### 2.3 Parcours de commande et textes exacts

Capturés **sur notre page** (app ou `bilan.html`), avant la redirection vers Stripe, **horodatés et enregistrés côté serveur** (table proposée `consentements(id, code, produit, texte_version, texte_hash, created_at)`, pas d'IP). Aucune case pré-cochée.

**Information avant les cases** (encart, obligatoire en L221-5 / L111-1, ⚠️ liste à valider) :
> Diagnostic complet de maths 3e : environ 40 minutes en 3 parties, bilan PDF et carte complète dans l'application. Accessible sur navigateur récent (ordinateur, tablette, téléphone). **Prix : 19,00 € TTC, paiement unique** (TVA non applicable, art. 293 B du CGI). Vendeur : Nicolas Follezou EI. Garantie légale de conformité applicable. Garantie commerciale « satisfait ou remboursé » 30 jours. [CGV]

**Case A (tous produits, obligatoire)**
> ☐ J'ai lu et j'accepte les [Conditions générales de vente]. Je suis majeur(e) et je suis le représentant légal de {prenom}, ou j'agis avec son accord.

**Case B (diagnostic complet, obligatoire)**
> ☐ Je demande que le diagnostic complet soit accessible immédiatement. Je reconnais que je perdrai mon droit de rétractation de 14 jours dès que {prenom} aura commencé le diagnostic. *La garantie « satisfait ou remboursé » de 30 jours reste applicable.*

**Case B' (Programme Brevet, obligatoire)**
> ☐ Je demande que l'accès au Programme Brevet commence immédiatement. Je conserve mon droit de rétractation de 14 jours ; si j'en use après le début de l'utilisation, un montant proportionnel pourrait être retenu. *En pratique, la garantie de 30 jours me rembourse intégralement.*

⚠️ Juriste : peut-on rendre la case B obligatoire (pas d'option « accès différé après 14 jours ») ? C'est courant, mais à confirmer.

**Stripe (Payment Link)** : activer « Exiger l'acceptation des conditions d'utilisation » (URL = `cgv.html`) avec un texte personnalisé :
> J'accepte les CGV de Matheux et je demande l'accès immédiat. Pour le diagnostic complet, je reconnais perdre mon droit de rétractation dès le début du diagnostic (garantie 30 jours maintenue).

C'est un doublon volontaire de la case capturée chez nous : si l'élève arrive sur Stripe par un lien direct (email), la trace existe quand même.

**Confirmation sur support durable** : email **P-ACH1 / P-ACH2** (`51-emails.md`), envoyé dès le webhook, qui reprend : produit, prix, date, identité du vendeur, **texte exact de la renonciation acceptée avec date et heure**, lien vers la version des CGV acceptée. Le reçu Stripe seul ne suffit pas (il ne contient pas la renonciation). Conserver les **versions successives des CGV** (fichier daté, par exemple `cgv-2026-10-01.html`).

---

## 3. Garantie « satisfait ou remboursé » 30 jours

À distinguer de la **garantie légale de conformité** des contenus et services numériques (art. L224-25-12 et suivants, ⚠️ vérifier les numéros), qui s'applique de toute façon et **doit être mentionnée** dans les CGV. ⚠️ Vérifier s'il existe un encadré légal type pour les contenus numériques (décret 2022-424 : encadré obligatoire pour les biens, à contrôler pour le numérique).

**Clause proposée (CGV art. 7)** ⚠️
> **Article 7 — Garantie « satisfait ou remboursé » 30 jours**
> 7.1 En plus des garanties légales, Matheux offre une garantie commerciale : pendant 30 jours à compter de l'achat, l'acheteur peut obtenir le remboursement intégral de son achat (Diagnostic complet ou Programme Brevet), **sans avoir à se justifier**, même si le diagnostic a été réalisé ou le bilan téléchargé.
> 7.2 Pour en bénéficier, il suffit d'envoyer un email à contact@matheux.fr depuis l'adresse utilisée pour l'achat, ou en indiquant le prénom de l'élève. Le remboursement est effectué sur le moyen de paiement utilisé, dans un délai maximal de 14 jours après la demande.
> 7.3 Le remboursement met fin à l'accès payant correspondant. L'accès gratuit est conservé.
> 7.4 La garantie s'applique une fois par foyer (même adresse email ou même élève).
> 7.5 Cette garantie ne remplace ni ne limite le droit de rétractation (article 6) ni la garantie légale de conformité (article 8).

---

## 4. Achat par un parent pour un mineur, consentement parental

### 4.1 Principes ⚠️ juriste

- **Capacité** : un mineur non émancipé ne peut conclure seul que des actes courants autorisés par l'usage, à des conditions normales (C. civ. art. 1146 et 1148, ⚠️ vérifier). À 19-49 €, un achat en ligne par carte bancaire reste discutable, mais la question ne se pose pas si **c'est le parent qui paie** : c'est lui le contractant, l'ado est bénéficiaire ou utilisateur.
- **RGPD** : art. 8 RGPD + art. 45 de la loi Informatique et Libertés : en France, un mineur peut consentir seul au traitement de ses données par un service de la société de l'information **à partir de 15 ans**. En dessous, il faut un **consentement conjoint** (mineur + titulaire de l'autorité parentale), **lorsque la base légale est le consentement**. Les élèves de 3e ont 14-15 ans : il y a les deux cas dans une même classe.
- **Base légale proposée** : **exécution du contrat** (CGU) pour faire fonctionner le service (compte, diagnostic, entraînement). Le **contractant est le parent** pour tous les comptes, quel que soit l'âge, ce qui est plus simple et uniforme. Le consentement ne sert de base que pour les emails marketing et GA4. ⚠️ À valider : c'est le point juridique central du modèle.
- **Vérification raisonnable** : la CNIL recommande de vérifier l'âge et l'accord parental par des moyens proportionnés. **Proposition** : confirmation par email du parent (P-X0, `51-emails.md`). Sans confirmation sous 30 jours, le compte est supprimé. Tant que ce n'est pas confirmé : usage possible, **aucun email marketing, aucun partage de bilan par email vers une autre adresse**.

### 4.2 Textes proposés

**Case à l'inscription (cochée par la personne qui remplit, souvent l'ado)** : remplace la case actuelle :
> ☐ J'accepte les [CGU] et j'ai lu la [politique de confidentialité]. L'email indiqué est celui d'un de mes parents : il recevra un message pour confirmer mon inscription.

**Page de confirmation parent** (`{lien_confirm}`) :
> **Confirmer l'inscription de {prenom} sur Matheux**
> {prenom} a créé un espace d'entraînement en maths avec votre adresse email. Matheux conserve son prénom, sa classe, ses réponses aux exercices et les résultats de ses diagnostics, uniquement pour faire fonctionner le service. Rien n'est vendu ni utilisé pour de la publicité.
> ☐ Je suis le parent ou le représentant légal de {prenom}, j'accepte les [CGU] et j'autorise {prenom} à utiliser Matheux. *(obligatoire)*
> ☐ Je souhaite recevoir des conseils et les offres Matheux par email (2 à 4 par mois au maximum, désinscription en 1 clic). *(facultatif)*
> *(si email ado saisi)* ☐ J'autorise Matheux à envoyer à {prenom}, sur l'adresse {email_eleve}, des rappels d'entraînement (jamais de publicité). *(facultatif)*
> [ Confirmer ]
> Vous n'êtes pas d'accord ? [ Supprimer l'espace de {prenom} ] (suppression immédiate et définitive)

### 4.3 Clause CGU (art. 2 bis) ⚠️
> **Article 2 bis — Élèves mineurs et responsables légaux**
> Matheux s'adresse à des élèves mineurs. Le compte est ouvert au nom de l'élève, mais le contrat d'utilisation est conclu avec son **représentant légal**, identifié par l'adresse email renseignée à l'inscription. Le représentant légal confirme l'inscription par le lien reçu par email. À défaut de confirmation dans les 30 jours, le compte et les données associées sont supprimés. Le représentant légal peut à tout moment retirer son accord et demander la suppression du compte, à contact@matheux.fr ou via le lien présent dans chaque email. Les achats sont effectués par une personne majeure, qui déclare être le représentant légal de l'élève ou agir avec son accord.

---

## 5. Données de diagnostic : conservation, partage, PDF

### 5.1 Nature des données
Réponses aux questions (y compris les mauvaises réponses et les erreurs types détectées), temps de réponse, niveau de maîtrise par compétence, carte (express et complète), bilan PDF, plan de travail, date du brevet blanc (si saisie). Ce ne sont **pas des données sensibles** au sens de l'art. 9 RGPD. Mais ce sont des **données sur les difficultés scolaires d'un mineur** : on les protège comme telles (minimisation, pas de partage, durée courte).

**Profilage** : la carte est un profilage pédagogique automatisé. Il ne produit **aucun effet juridique** ni affectant de manière significative (pas de décision d'orientation, pas de note officielle), donc l'art. 22 RGPD ne s'applique a priori pas ⚠️. On l'explique tout de même clairement (transparence, art. 13).

**Avertissement « diagnostic »** (CGU + pied du PDF) :
> Le « diagnostic » Matheux est une évaluation pédagogique automatisée des compétences en mathématiques, réalisée à partir des réponses de l'élève. Il ne constitue ni un bilan médical ou paramédical (il ne détecte pas de trouble des apprentissages comme la dyscalculie), ni une évaluation officielle de l'Éducation nationale, ni une prédiction de la note au Brevet.

### 5.2 Durées de conservation proposées ⚠️

| Donnée | Durée | Justification |
|---|---|---|
| Compte non confirmé par le parent | **30 jours**, puis suppression | Pas de base sans accord parental |
| Compte actif (profil, scores, cartes, maîtrise) | Tant que le compte est utilisé ; **suppression automatique après 12 mois sans connexion**, avec un email d'avertissement 30 jours avant | Minimisation. Remplace « durée du compte + 1 an », sans fondement. |
| Suppression demandée | **Immédiate** (≤ 30 jours pour les sauvegardes techniques) | Droit à l'effacement, renforcé pour les données collectées pendant l'enfance (art. 17.1.f) |
| Lien de partage du bilan (token + instantané) | **30 jours**, ou jusqu'à révocation par l'élève | Voir §5.3 |
| PDF | Pas stocké s'il est généré dans le navigateur. Sinon : lien signé valable 30 jours, régénérable depuis l'app, fichier supprimé avec le compte. | Minimisation |
| Données de facturation (Stripe, registre des recettes) | **10 ans** | Obligation comptable (C. com. L123-22) ⚠️ |
| Preuves de consentement (CGV, renonciation, accord parental, opt-in) | Durée de la relation + **5 ans** | Prescription civile de droit commun (C. civ. 2224) ⚠️ |
| `email_logs` | **3 ans** après le dernier contact | Recommandation CNIL (prospection) |
| Liste de désinscription (`UNSUB`) | **3 ans** minimum, conservée même après suppression du compte (email seul) | Pour pouvoir respecter l'opposition |
| `funnel_events` | **13 mois** | Statistiques internes |
| Données de connexion (streak) | 6 mois glissants (existant) | — |

### 5.3 Clause « partage du bilan par lien » (confidentialité + CGU) ⚠️
> **Partage du bilan.** L'élève peut créer un lien personnel pour montrer sa carte de compétences à ses parents. Ce lien donne accès, sans connexion, à une page affichant son prénom, sa classe, la date du diagnostic, la synthèse par domaine et son point prioritaire. Il n'affiche ni ses réponses détaillées, ni son adresse email, ni aucune autre donnée. Le lien est aléatoire et non devinable, n'est pas référencé par les moteurs de recherche, expire après 30 jours et peut être désactivé à tout moment par l'élève. Toute personne qui possède le lien peut voir la page : il ne doit être transmis qu'aux parents ou représentants légaux. Si l'élève envoie le lien par email via Matheux, l'adresse du destinataire est utilisée uniquement pour cet envoi, puis conservée dans le journal des envois pendant 3 ans (preuve d'envoi) et jamais réutilisée à d'autres fins.

### 5.4 Suppression des anciennes données (décision du 24/09)
Pour que la politique affichée soit vraie, la suppression des anciens comptes doit couvrir : les tables Supabase (`profiles`, `scores`, `progress`, `daily_boosts`, `emails`, `email_logs`, `insights`, etc.), **Supabase Auth**, le **Google Sheet legacy** (ID dans CLAUDE.md §7) et ses copies, les **clients Stripe** (ou au moins leur anonymisation, les paiements eux-mêmes restent 10 ans), et les exports locaux éventuels (`docs/audit-*.md` qui contiendraient des prénoms). ⚠️ Nicolas : faire un backup chiffré avant suppression, puis **le supprimer aussi** à une date fixée (par exemple 3 mois), sinon la suppression n'en est pas une.

---

## 6. Pratiques commerciales et mineurs

- **Liste noire des pratiques agressives** (Code de la consommation, **art. L121-7**, ⚠️ vérifier le numéro exact de l'alinéa ; directive 2005/29, annexe I, point 28) : « dans une publicité, inciter directement les enfants à acheter ou à persuader leurs parents ou d'autres adultes de leur acheter le produit faisant l'objet de la publicité ». La pratique est **réputée** agressive, sans qu'il soit besoin de prouver un effet.
  - **Conséquence pour Matheux** : aucun écran ou email destiné à l'ado ne contient de bouton d'achat, d'appel à « débloquer », à « demander à tes parents de t'offrir ». Le partage de la carte est une **information** : le libellé « Montrer ma carte à mes parents » et le message pré-rempli (sans prix, sans appel à l'achat) sont décrits dans `50` §3. ⚠️ Juriste : faire valider **précisément** le paywall ado (`50` §2.3), en particulier la phrase « Le diagnostic complet est payant (19 €). C'est une décision pour tes parents, pas pour toi. »
- **Pratiques trompeuses** (art. L121-2 à L121-4, ⚠️ numéros à vérifier) : présenter les droits légaux comme un avantage propre à l'offre (d'où la suppression du badge « Droit de rétractation 14 jours »), affirmer faussement une disponibilité limitée dans le temps, faux avis, fausse urgence.
- **Prix barrés** : le prix de référence d'une réduction doit être le prix le plus bas pratiqué dans les 30 jours précédents (art. L112-1-1, depuis 2022 ⚠️). Reco `50` : **aucun prix barré**.
- **Avis clients** : si on en publie un jour, il faut indiquer s'ils sont contrôlés et comment (art. L111-7-2 ⚠️), et recueillir un accord écrit du parent pour tout témoignage qui mentionne un mineur.
- **Ancrage « cours particulier »** : autorisé s'il est **vrai, sourcé et daté** (`50` §1.1). À revérifier à chaque rentrée.

---

## 7. Emails : prospection et transactionnel

- **Art. L34-5 du Code des postes et communications électroniques** : la prospection par email vers un particulier exige son **consentement préalable**. Exception (« soft opt-in ») : les coordonnées ont été recueillies à l'occasion d'une **vente ou d'une prestation de services**, pour des produits analogues du même professionnel, avec possibilité de s'opposer dès la collecte et à chaque message. ⚠️ Juriste : un compte **gratuit** est-il une « prestation de services » au sens de l'exception ? La doctrine est partagée. **Reco : ne pas s'y appuyer**, et recueillir un **opt-in explicite** du parent (case non cochée sur la page de confirmation, §4.2).
- **Après achat**, le parent devient client : le soft opt-in s'applique pour les produits analogues (upsell programme). On garde quand même la désinscription en 1 clic.
- **Transactionnel** (confirmation d'inscription, confirmation d'achat, PDF, bilan partagé à la demande de l'élève) : pas de consentement requis, **pas d'offre commerciale dans le corps** (sinon l'email devient mixte, donc de la prospection). `51-emails.md` respecte cette règle : P-X0, P-SH, P-ACH, P-PDF ne contiennent pas de prix. ⚠️ P-X0 contient un lien vers la page bilan, qui elle contient l'offre : à valider.
- **Emails à l'ado (mineur)** : **jamais de prospection**, même avec consentement. Uniquement des rappels pédagogiques, avec l'accord du parent (§4.2).
- **Mentions dans chaque email P/M** : identité de l'expéditeur, lien de désinscription fonctionnel, origine de l'adresse (« Vous recevez cet email car {prenom} utilise Matheux avec votre adresse »).

---

## 8. CGV : texte proposé (remplace intégralement `cgv.html`) ⚠️ tout l'article à relire

> **Conditions générales de vente — Matheux**
> Version du {JJ/MM/AAAA}. Les versions précédentes sont disponibles sur demande.
>
> **Article 1 — Vendeur**
> Nicolas Follezou, entrepreneur individuel (EI), SIRET 837 763 713 00059, 30 rue Lucie Aubrac, 17137 L'Houmeau. Email : contact@matheux.fr.
>
> **Article 2 — Objet et offres**
> Matheux est un service en ligne d'entraînement en mathématiques pour les élèves de 3e. Il est proposé :
> - **Accès gratuit** : diagnostic express (environ 15 questions), carte partielle des compétences, entraînement de 5 exercices par jour sur le point prioritaire identifié. Sans limite de durée, sans moyen de paiement.
> - **Diagnostic complet** : évaluation d'environ 40 minutes en 3 parties, carte complète des compétences dans l'application, bilan PDF et plan de travail de 4 semaines, un re-test de suivi environ 4 semaines après.
> - **Programme Brevet** : diagnostic complet inclus, entraînement illimité sur l'ensemble des compétences, re-diagnostic mensuel, brevets blancs, bilan hebdomadaire par email au représentant légal.
> Les caractéristiques essentielles de chaque offre sont présentées avant la commande. Le service est accessible depuis un navigateur web récent (ordinateur, tablette, smartphone) avec une connexion Internet.
>
> **Article 3 — Prix**
> Diagnostic complet : **19,00 € TTC**. Programme Brevet : **49,00 € TTC**, ou **30,00 € TTC** pour l'acheteur ayant déjà acquis le Diagnostic complet pour le même élève (déduction sans limite de durée). Paiement unique : aucun abonnement, aucun renouvellement, aucun prélèvement ultérieur. TVA non applicable, article 293 B du CGI. Le prix applicable est celui affiché au moment de la commande.
>
> **Article 4 — Commande et paiement**
> La commande est passée par une personne majeure, qui déclare être le représentant légal de l'élève ou agir avec son accord. Le paiement est réalisé par carte bancaire via Stripe. Matheux n'a jamais accès aux données bancaires. La commande est définitive après validation du paiement. Un email de confirmation reprenant les informations de la commande est envoyé à l'acheteur.
>
> **Article 5 — Accès et durée**
> L'accès payant est activé dès la confirmation du paiement, pour l'élève désigné lors de la commande. Il est **sans limitation de durée** tant que le service est exploité. En cas d'arrêt définitif du service, les utilisateurs sont prévenus au moins 3 mois à l'avance et peuvent récupérer leurs bilans. Si l'arrêt intervient avant la fin de l'année scolaire au cours de laquelle le Programme Brevet a été acheté, le prix est remboursé au prorata des mois restants jusqu'au 30 juin de cette année. ⚠️ *(clause d'engagement volontaire, à valider)*
>
> **Article 6 — Droit de rétractation**
> 6.1 L'acheteur consommateur dispose en principe d'un délai de 14 jours à compter de la commande pour se rétracter, sans motif, par email à contact@matheux.fr ou au moyen du formulaire type ci-dessous.
> 6.2 **Diagnostic complet** : conformément à l'article L221-28 13° du Code de la consommation, le droit de rétractation ne peut plus être exercé une fois que l'élève a commencé le diagnostic, si l'acheteur a expressément demandé l'accès immédiat et reconnu la perte de son droit de rétractation lors de la commande. Ce choix lui est confirmé par email.
> 6.3 **Programme Brevet** : l'acheteur conserve son droit de rétractation pendant 14 jours. S'il a demandé que l'accès commence immédiatement et se rétracte ensuite, un montant proportionnel au service fourni jusqu'à la rétractation peut lui être demandé (article L221-25). ⚠️
> 6.4 Le remboursement intervient dans les 14 jours suivant la rétractation, par le même moyen de paiement.
> 6.5 Ces règles ne limitent pas la garantie « satisfait ou remboursé » de l'article 7, plus favorable.
> *Formulaire type de rétractation : « À l'attention de Nicolas Follezou EI, contact@matheux.fr : je vous notifie par la présente ma rétractation du contrat portant sur [Diagnostic complet / Programme Brevet], commandé le [date], au nom de [nom], adresse email [email], date, signature (si papier). »* ⚠️ vérifier le modèle de l'annexe à l'article R221-1.
>
> **Article 7 — Garantie « satisfait ou remboursé » 30 jours** : texte du §3.
>
> **Article 8 — Garantie légale de conformité**
> Matheux est tenu de fournir un contenu et un service numériques conformes au contrat, dans les conditions des articles L224-25-12 et suivants du Code de la consommation ⚠️. En cas de défaut, l'acheteur peut demander la mise en conformité, puis, à défaut, une réduction du prix ou la résolution du contrat. *[encadré légal éventuel, ⚠️]*
>
> **Article 9 — Nature du service**
> Matheux est un outil pédagogique complémentaire. Le diagnostic est une évaluation pédagogique automatisée (voir CGU, article « Nature du diagnostic »). Il ne remplace ni l'enseignement scolaire, ni un avis médical ou paramédical. Les résultats scolaires dépendent de nombreux facteurs indépendants du service, et aucun résultat au Brevet n'est garanti.
>
> **Article 10 — Données personnelles** : voir la politique de confidentialité.
>
> **Article 11 — Réclamations, médiation, droit applicable**
> Réclamation : contact@matheux.fr. À défaut d'accord amiable, le consommateur peut saisir gratuitement le médiateur de la consommation : {nom, adresse, site du médiateur ⚠️ vérifier que l'adhésion est en cours}. Droit français. Pour le consommateur, le tribunal compétent est déterminé selon les règles légales ⚠️ *(la clause « tribunal de La Rochelle » est inopposable à un consommateur : à retirer)*.

---

## 9. CGU : modifications

| Article | Changement | Texte |
|---|---|---|
| Bandeau | Remplacer « le responsable légal certifie avoir donné son consentement » | « Matheux est utilisé par des élèves mineurs. L'inscription est confirmée par un parent ou représentant légal, par email (article 2 bis). » |
| Art. 2 Accès | Nouvelle offre gratuite | « Gratuitement : diagnostic express, carte partielle et 5 exercices par jour sur le point prioritaire, sans limite de durée. Offres payantes : voir CGV. L'accès est destiné aux élèves de 3e. » |
| **Art. 2 bis** | Nouveau | §4.3 |
| Art. 3 Compte | Préciser les deux adresses | « … L'adresse email du compte est celle du représentant légal. L'élève peut ajouter sa propre adresse, avec l'accord du représentant légal, pour recevoir des rappels d'entraînement. » |
| Art. 4 Données | Renvoyer à la politique, retirer les engagements imprécis | « Voir la politique de confidentialité, qui détaille les données, leurs finalités, leur durée de conservation et vos droits. » |
| **Art. 4 bis Nature du diagnostic** | Nouveau | Texte « Avertissement diagnostic » du §5.1 + « Les résultats reposent sur un nombre limité de questions ; une compétence n'est jamais déclarée en lacune sur la base d'une seule réponse. » |
| **Art. 4 ter Partage du bilan** | Nouveau | §5.3 (partie utilisateur) + « L'élève s'engage à ne transmettre le lien qu'à ses parents ou représentants légaux. » |
| Art. 5 PI | Ajouter | « Le bilan PDF est destiné à l'usage personnel de la famille et des enseignants ou intervenants de l'élève. » |
| Art. 8 Résiliation | Ajouter la suppression automatique | « Le compte est supprimé automatiquement après 12 mois sans connexion (avertissement par email 30 jours avant), ou 30 jours après l'inscription s'il n'a pas été confirmé par un représentant légal. La suppression du compte ne donne pas droit à remboursement au-delà des garanties prévues aux CGV. » |
| Art. 9 | Retirer la clause de juridiction (inopposable aux consommateurs ⚠️) | « Droit français. » |

---

## 10. Politique de confidentialité : sections à réécrire ⚠️

**Responsable** : Nicolas Follezou EI (identique). DPO non obligatoire a priori ⚠️. Remplacer « Email DPO » par « Contact données personnelles ».

**Données, finalités, bases, durées** (remplace le tableau actuel) :

| Données | Finalité | Base légale | Durée |
|---|---|---|---|
| Prénom de l'élève, classe | Faire fonctionner le compte | Contrat (CGU) | §5.2 |
| Email du représentant légal | Authentification, confirmation parentale, emails de service | Contrat | §5.2 |
| Email de l'élève (facultatif) | Rappels d'entraînement | Consentement du représentant légal | Jusqu'au retrait |
| Réponses, maîtrise par compétence, cartes, bilans | Diagnostic, entraînement adapté, suivi de progression | Contrat | §5.2 |
| Date du brevet blanc (facultatif) | Plan de révision daté | Contrat | Jusqu'à la fin de l'année scolaire |
| Emails de conseils et d'offres | Information commerciale au représentant légal | **Consentement** (opt-in), ou intérêt légitime / soft opt-in après achat | Jusqu'au retrait ; preuve 3 ans |
| Paiement (email payeur, montant, date, référence Stripe) | Facturation, garantie, comptabilité | Obligation légale / contrat | 10 ans |
| Preuves de consentement | Preuve | Obligation légale / intérêt légitime | Relation + 5 ans |
| Statistiques d'usage internes (`funnel_events`, sans IP) | Améliorer le service | Intérêt légitime | 13 mois |
| Mesure d'audience GA4 | Statistiques de visite | Consentement (bandeau cookies) | Selon la politique cookies |

**Destinataires et sous-traitants** (⚠️ vérifier pour chacun le DPA, la localisation et le mécanisme de transfert) :

| Prestataire | Rôle | Localisation / transfert |
|---|---|---|
| Supabase | Base de données, authentification, API | Projet hébergé dans la région UE (Paris), selon CLAUDE.md §7 ⚠️ vérifier |
| Resend | Envoi des emails | Société américaine, domaine configuré en région UE ⚠️ DPF / CCT à vérifier |
| Stripe | Paiement | Stripe Payments Europe (Irlande), **responsable de traitement distinct** pour les données de paiement |
| GitHub (Pages) | Hébergement du site (journaux techniques, adresses IP) | États-Unis ⚠️ DPF / CCT |
| Google (Analytics 4) | Mesure d'audience, **uniquement après consentement** | ⚠️ DPF |
| Google (Sheets / Apps Script) | **À retirer** si le legacy est supprimé (§5.4). Sinon, le déclarer. | — |
| **Fournisseur de modèle d'IA** (si l'agent de génération reçoit des réponses d'élèves) | Génération de contenus pédagogiques | ⚠️ **Reco : n'envoyer que des données pseudonymisées** (pas de prénom, pas d'email, pas de code : seulement des réponses et des erreurs agrégées). Ainsi aucune donnée personnelle ne quitte le système. Sinon, le déclarer ici avec son mécanisme de transfert. |

**Nouvelles sections à ajouter** : « Diagnostic et profilage pédagogique » (§5.1 : ce qu'on calcule, à quoi ça sert, que ça n'a aucun effet juridique, que l'algorithme ne conclut jamais sur une seule réponse) · « Partage du bilan » (§5.3) · « Emails » (catégories T/P/M, désinscription, jamais de publicité à l'élève) · « Suppression automatique » · « Vos droits » (inchangé, et **l'élève peut exercer ses droits lui-même** ; CNIL).

**Version courte pour les ados** (en tête de la politique, CNIL : information adaptée aux mineurs) :
> **En bref, pour toi**
> - On garde ton prénom, ta classe et tes réponses aux exos. C'est tout. Pas ton nom de famille, pas ta photo, pas ta position.
> - Ça sert à une seule chose : te proposer les bons exercices et te montrer ta progression.
> - On ne vend rien de toi à personne, et on ne te montre pas de pub.
> - Tes parents ont confirmé ton inscription. Ils voient ton bilan si tu leur envoies ou s'ils achètent le diagnostic complet.
> - Tu peux demander à tout effacer, quand tu veux : contact@matheux.fr.
> - Si tu ne te connectes pas pendant un an, ton compte s'efface tout seul.

---

## 11. Autres points

- **Note / facture** : pour une prestation de services à un particulier d'au moins 25 € TTC, la remise d'une note est obligatoire (arrêté n° 83-50/A ⚠️ vérifier l'applicabilité aux services en ligne). À 49 €, activer la **création de facture** sur les Payment Links Stripe (ou envoyer une note dans P-ACH2), avec les mentions obligatoires, dont « TVA non applicable, art. 293 B du CGI ».
- **Franchise en base de TVA** : ⚠️ vérifier le seuil applicable en 2026 (réforme des seuils débattue en 2025) et le chiffre d'affaires cumulé.
- **Mentions légales** : ajouter « EI », l'hébergeur réel du site (GitHub Pages) et de l'app (Supabase), et retirer toute mention Google si elle n'est plus vraie.
- **Politique cookies** : GitHub Pages ne dépose pas de cookie, localStorage = session (exempté). GA4 : refus aussi simple que l'acceptation (`50` §9.8).

---

## 12. Checklist de mise en conformité (ordre suggéré)

1. ☐ Juriste : valider §2.2 (qualification), §4.1 (base légale / contractant parent), §6 (paywall ado), §7 (P-X0 et P-SH transactionnels)
2. ☐ Réécrire CGV (§8), CGU (§9), confidentialité (§10), mentions légales (§11), puis archiver les anciennes versions datées
3. ☐ Cases A/B/B' + journal des consentements côté serveur (ingénieur adaptatif)
4. ☐ Email de confirmation P-ACH1/P-ACH2 avec le bloc légal
5. ☐ Confirmation parentale (P-X0 + page de confirmation) + suppression à J+30
6. ☐ Opt-in marketing enregistré, et vérifié avant chaque email M
7. ☐ Retirer le badge « Droit de rétractation 14 jours » de `premium.html` (ou retirer la page si elle est remplacée)
8. ☐ Suppression complète des anciennes données (§5.4), y compris le Google Sheet et le backup (à date fixée)
9. ☐ Pseudonymiser les données envoyées au modèle d'IA, ou les déclarer
10. ☐ Vérifier le contrat du médiateur, les factures, le seuil de TVA

---

## ❓ Questions pour Nicolas

1. **Tu fais relire ce fichier par un juriste avant le lancement ?** → Reco : **oui, au minimum §2, §4, §6 et §8** (1 à 2 h de consultation, c'est l'assurance la moins chère du projet).
2. **Le parent est-il le contractant pour tous les comptes, quel que soit l'âge de l'ado ?** → Reco : **oui** (uniforme, et cohérent avec « acheteur = parent »).
3. ~~Médiateur CNPM~~ → **Décision Nicolas 24/09 : pas de médiateur pour l'instant.** Risque connu : obligation légale (art. L612-1 C. conso), amende administrative possible. À réexaminer si les ventes décollent.
4. **Suppression automatique des comptes après 12 mois d'inactivité ?** → Reco : **oui**.
5. **Données d'élèves envoyées à un modèle d'IA (admin-auto, cours adaptatifs) : on pseudonymise ?** → Reco : **oui**, et on ne le déclare comme sous-traitant qu'à défaut.
6. **Clause d'engagement « remboursement au prorata si Matheux ferme avant la fin de l'année scolaire » ?** → Reco : **oui**, c'est rassurant pour un parent face à un fondateur solo, et le coût est quasi nul.
