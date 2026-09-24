# 50 — Offre, paywall, upsell, KPIs (Growth / CRO)

> Agent : growth-cro · 24/09/2026 · Branche `feat/diagnostic-3e` · Statut : **proposition, non implémentée**
> Lit : `00-contrat-commun.md`, CLAUDE.md §3.3, `premium.html`, `cgv.html`, `index.ts` (templates J*, cron, webhook).
> Liés : `51-emails.md` (séquence), `52-legal.md` (clauses, rétractation, RGPD).
> Principe : **on fait payer parce que c'est utile.** Chaque levier ci-dessous doit rester vrai si un parent
> le lit à voix haute devant un inspecteur de la DGCCRF.

---

## 0. Résumé en 10 lignes

- **Prix : on garde 19 € / 49 €**, avec 19 € déduits **sans date limite**. 49 € reste sous le seuil des 50 € et vaut ~2 h de cours particulier pour 9 mois de préparation. On ne relève le prix qu'après 10 clients payants, pour les nouveaux acheteurs seulement, sans prix barré.
- **Deux options présentées côte à côte** au paywall (Diagnostic 19 € / Programme 49 €, diagnostic inclus). L'« order bump » se fait **sur notre page avant Stripe**, pas dans Stripe.
- **Garantie 30 jours, remboursement intégral sans justification**, sur les deux produits. Elle va plus loin que le droit légal, donc c'est un vrai argument.
- **L'acheteur est le parent.** Côté ado on montre de la valeur et on propose de **partager** le bilan. On ne lui dit **jamais** « demande à tes parents de payer » (interdit, cf. §7 et `52-legal.md`).
- Les 5 leviers principaux : ① une phrase personnalisée qui repose sur une vraie donnée, ② un aperçu PDF réel, ③ le lien parent, ④ la déduction plus la garantie (zéro regret), ⑤ l'urgence réelle (semaines restantes avant le Brevet, date du brevet blanc saisie par l'élève).

---

## 1. Offre et échelle de prix

### 1.1 Benchmarks (consultés le 24/09/2026)

| Offre | Prix constaté | Ce que c'est | Source / fiabilité |
|---|---|---|---|
| Cours particulier maths 3e (moyenne) | **~21 €/h** (Superprof, moyenne maths) · **21-25 €/h après crédit d'impôt** en 3e | Humain, 1 h | [Superprof blog](https://www.superprof.fr/blog/prix-cours-particuliers/), [Groupe Réussite](https://groupe-reussite.fr/ressources/cp-tarifs-cours-particuliers-maths/), secondaire |
| Acadomia à domicile, collège | **48,80 €/h** avant crédit, **24,40 €/h** après + abonnement 29,80 €/mois (14,90 € après crédit) | Humain | [acadomia.fr/tarif-cours-particuliers](https://www.acadomia.fr/tarif-cours-particuliers.html), officiel |
| Acadomia en ligne, collège | dès **43 €/h** + 39 € d'inscription annuelle | Humain, visio | idem, officiel |
| Acadomia stage vacances collège (Brevet) | **245 €** pour 10 h en petit groupe | Humain, intensif | [FAQ Acadomia stages](https://www.acadomia.fr/qui-sommes-nous/faq/tarifs/combien-coute-un-stage-de-vacances-acadomia-pour-les-eleves/), officiel (via recherche) |
| Kartable Premium | 14,99 €/mois · **109,89 €/année scolaire** (9,99 € × 11) · 183,77 € sur 2 ans, reconduction auto | Toutes matières, contenus + IA | [kartable.fr/premium](https://www.kartable.fr/premium), officiel |
| SchoolMouv | 11,99 à 39,99 €/mois selon formule et durée · ~180 €/an max en Premium | Toutes matières, vidéos | [trajectio.fr](https://trajectio.fr/schoolmouv-soutien-scolaire/), [offres.schoolmouv.fr](https://offres.schoolmouv.fr/plans/), **secondaire, à vérifier** |
| Maxicours | ~9,99 à 21,99 €/mois selon engagement | Toutes matières | [mastercours.fr](https://www.mastercours.fr/maxicours.html), **secondaire, chiffres incohérents entre sources = estimation** |
| Diagnostic payant seul (concurrents) | **Pas d'équivalent grand public trouvé.** Les réseaux proposent un « bilan pédagogique » **gratuit** comme produit d'appel avant la vente d'heures. | — | recherche infructueuse = **estimation** |

Ce qu'on en retire :
1. **L'ancrage vrai, c'est l'heure de cours** : 20-25 € après crédit d'impôt, ~49 € avant. 19 € < 1 h. 49 € ≈ 2 h ≈ 1 h Acadomia sans crédit d'impôt.
2. **Face aux abonnements** (Kartable ~110 €/an, SchoolMouv jusqu'à ~180 €/an), 49 € en une fois, sans reconduction, reste bas. Mais ces plateformes couvrent toutes les matières : **on ne se compare pas frontalement à elles**. On se compare au cours particulier de maths, qui est l'alternative réelle d'un parent inquiet pour les maths.
3. **Le diagnostic payant est un pari** : ailleurs, le bilan est gratuit. Pour que 19 € se justifie, il faut que la **carte express gratuite soit déjà utile** et que le **PDF soit visiblement plus riche** (aperçu réel, §2.5). Sinon, le palier unique (§1.3) devient meilleur.

### 1.2 Recommandation : on garde 19 € / 49 €, avec déduction sans date limite

| Produit | Prix | Contenu | Pourquoi ce prix |
|---|---|---|---|
| **Diagnostic complet + bilan PDF** | **19 €** | ~40 min en 3 modules reprenables → carte complète (toutes les compétences, causes racines, erreurs types avec exemples) → PDF parent + plan 4 semaines. Accès à la carte complète dans l'app. | < 1 h de cours. Sous le seuil des 20 €, où la décision reste impulsive pour un parent. |
| **Programme Brevet** | **49 €** (ou **30 €** si le diagnostic est déjà acheté) | Diagnostic complet inclus + entraînement illimité sur toute la carte + re-diagnostic mensuel + brevets blancs Matheux + bilan parent hebdo. Accès non expirant (T2). | ≈ 2 h de cours pour ~9 mois. < 50 €. Moitié moins cher qu'un an de Kartable. |

**La déduction n'expire pas.** Pas de « 19 € déduits si vous passez au programme sous 7 jours » : ce serait une urgence artificielle, et ça contredirait T2 (le piège de la date en dur). Le parent paie 49 € au total, qu'il prenne le programme maintenant ou en mars. C'est ce qui permet la phrase la plus rassurante de tout le funnel :

> « Commencez par le diagnostic. Si vous passez au programme plus tard, les 19 € sont déduits. Vous ne payez jamais deux fois. »

**49 € ou plus ?** On pourrait défendre 59-69 €, puisque l'ancrage à 2-3 h de cours reste vrai. Mais avec 10 élèves visés, 10 € de plus × 3 ventes = 30 €, ce qui ne pèse rien face au risque de freiner les premières conversions. **On ne teste un prix plus haut qu'après 10 programmes vendus**, sur les nouveaux acheteurs uniquement. Les anciens gardent leur prix. Pas de prix barré, pas de « promo de lancement » (voir §7 : le prix de référence d'un prix barré doit être le plus bas pratiqué sur 30 jours).

### 1.3 Alternatives étudiées

| Option | Pour | Contre | Verdict |
|---|---|---|---|
| **Palier unique 39 €** (diagnostic + programme) | 1 seule décision, message simple | Plus de porte d'entrée à faible risque. Le PDF (objet tangible pour le parent) perd son rôle de preuve. 39 € d'un coup sur une marque inconnue. | ❌ en v1. **Plan B** si < 1 achat de diagnostic sur 30 cartes partielles vues. |
| **Diagnostic 9 €** | Friction minimale | Signale « pas sérieux », rend le PDF anecdotique, marge nulle après frais Stripe (~0,25 € + 1,5 %) | ❌ |
| **Programme en abonnement** (ex. 9 €/mois) | Revenu récurrent | Contredit T2 (paiement unique). Churn. Les parents détestent les reconductions (et la loi aussi : résiliation en 3 clics obligatoire). | ❌ |
| **Diagnostic gratuit, programme 49 €** | Conversion du diagnostic × 3-5 | Plus de filtre, plus de revenu intermédiaire. Le complet (40 min) sans engagement risque d'être abandonné. | ❌, mais à garder en tête si le taux diagnostic → programme est excellent (> 50 %) |
| **Garantie « satisfait ou remboursé »** | Lève le risque perçu (marque inconnue, fondateur solo) | Abus possible (télécharger le PDF puis se faire rembourser) | ✅ **30 jours, sans justification, sur les deux produits.** À 19 €, quelques abus coûtent moins que les ventes gagnées. Garde-fou : 1 remboursement par foyer (email). |

**Pourquoi 30 jours et pas 14 ?** Le droit de rétractation légal est de 14 jours et ne peut pas être présenté comme un avantage propre à l'offre (pratique trompeuse, cf. `52-legal.md`). Une garantie de 30 jours va plus loin que la loi, donc on peut la mettre en avant. Elle couvre aussi le cas du diagnostic, pour lequel le droit de rétractation est perdu dès l'accès (renonciation).

### 1.4 Clients existants

Sans objet : décision de Nicolas du 24/09 (contrat §7), tous les anciens comptes sont supprimés et on repart de zéro. Il n'y a ni grand-père tarifaire, ni séquence de réactivation. Les anciens Payment Links à 29,99 € (4 niveaux + l'ancien « Brevet 2026 ») sont à **archiver dans Stripe** au moment de la bascule, pour qu'aucun lien qui traîne ne vende l'ancienne offre.

### 1.5 Où vit le prix (règle du contrat : un seul endroit)

Une seule constante côté API, par exemple `OFFRES = { diag: {prix: 19, lien: …}, programme: {prix: 49, lien: …}, upgrade: {prix: 30, lien: …} }`, exposée au front via `check_trial_status` ou `login`. **À implémenter par l'ingénieur adaptatif.** Les pages légales citent les prix en dur, donc toute modification de prix = mise à jour des CGV le même jour.

---

## 2. Anatomie du paywall de la carte partielle

### 2.1 Quand il apparaît

1. **Fin du diagnostic express** → la carte partielle s'affiche **d'abord en entier**, sans aucun paywall au-dessus de la ligne de flottaison. L'élève voit ce qu'il a gagné avant qu'on lui parle d'argent.
2. Sous la carte : le bloc « Ce que le diagnostic complet ajoute » (§2.3), jamais en modal bloquante.
3. Le bouton principal au-dessus du bloc est **gratuit** : « Commencer mes 5 exos sur {point faible} ». La valeur d'abord.
4. Le bloc revient dans l'app **2 fois maximum** : quand le quota quotidien gratuit (5 exos) est atteint, avec un encart discret sous « reviens demain », et depuis l'onglet Carte (permanent, non intrusif).
5. **Jamais** en plein milieu d'un exercice, jamais en pop-up à l'ouverture de l'app.

### 2.2 Ce qui est montré, estimé, masqué : règle d'honnêteté

| Élément | Affichage | Règle |
|---|---|---|
| 5 domaines colorés | Montrés, avec la mention « **estimation express** · 3 questions par domaine » | On ne présente pas une couleur fondée sur 3 questions comme un verdict |
| 1 point faible détaillé | **Montré en entier** : titre élève, erreur type repérée **avec sa vraie réponse**, explication courte, compétences qu'il bloque (si `cause_racine`) | C'est la preuve que le diagnostic « voit » quelque chose. Il faut qu'il soit bon. |
| Autres compétences | **Titres lisibles**, statut ⚪ « pas encore mesuré » | ⛔ **On ne floute jamais un résultat inventé.** Si la compétence n'a pas été mesurée, on l'écrit. Le flou sert seulement pour l'**aperçu du PDF** (exemple fictif, étiqueté « exemple »). |
| Compteur | « Le diagnostic express a mesuré **{n_mesurees}** compétences sur **{n_total}**. Le complet les mesure toutes. » | Chiffres réels, calculés à partir de la carte |

Le flou « appât » (du texte flou qui suggère qu'on sait déjà mais qu'on cache) est une petite malhonnêteté. Ce qui est vrai et qui convertit tout aussi bien, c'est : « on n'a pas encore regardé, voilà ce qu'on regardera ».

### 2.3 Bloc paywall, côté ado (tutoiement, ton 3e : sobre, orienté résultats)

La phrase personnalisée est choisie selon la carte réelle. On prend **le premier cas vrai** :

| Cas (données de la carte) | Phrase personnalisée |
|---|---|
| Point faible = `cause_racine` avec `bloque` ≥ 1 | « **{prenom}, ton point à travailler c'est {titre_eleve}.** Et c'est pas un détail : ça coince aussi {bloque_1_titre}{ et {n_autres} autre(s) chose(s)} du programme de 3e. » |
| Point faible sans cause racine | « **{prenom}, ton point à travailler c'est {titre_eleve}.** On a repéré l'erreur exacte, et elle se corrige. » |
| Erreur type identifiée (`err` matché) | ajouter : « Tu as répondu **{reponse_eleve}** au lieu de **{a}**. C'est une erreur très classique : {libelle court}. » |
| Aucune lacune détectée (express tout vert) | « **Solide, {prenom}.** L'express n'a rien trouvé d'inquiétant. Le complet sert surtout à chercher les points de détail qui font perdre des points au Brevet. » (et **on n'insiste pas**, §2.7) |

Copy du bloc (sous la phrase personnalisée) :

> **Ce que le diagnostic complet ajoute**
> 40 minutes, en 3 parties que tu peux faire en plusieurs fois.
> - Toutes les compétences de 3e mesurées, pas seulement {n_mesurees}
> - Les **vraies causes** : parfois ce qui bloque en 3e date de la 5e, et le complet le trouve
> - Tes erreurs types, avec tes propres réponses en exemple
> - Un plan de 4 semaines, dans l'ordre qui rapporte le plus de points au Brevet
>
> *[aperçu de 2 pages du bilan — « exemple »]*
>
> **Le diagnostic complet est payant (19 €).** C'est une décision pour tes parents, pas pour toi.
> Si tu veux, envoie-leur ta carte : ils verront exactement ce que tu vois, et ce que contient le complet.
>
> [ 📨 Montrer ma carte à mes parents ] (bouton secondaire)
> [ Continuer gratuitement → mes 5 exos du jour ] (bouton principal, même taille ou plus grand)

Règles copy côté ado : **pas de prix mis en avant** (mentionné une fois, en texte normal), **pas de bouton « Acheter »**, pas de « demande à tes parents de te l'offrir ». Le bouton de partage parle de *montrer*, pas de *faire acheter*. ⚠️ Cette ligne rouge est juridique (`52-legal.md` §6), pas seulement éthique.

Un lien discret « Je suis le parent » bascule vers la vue parent (§2.4) sur le même appareil, cas fréquent où le parent est assis à côté.

### 2.4 Bloc paywall, côté parent (vouvoiement, factuel)

Affiché sur la page parent (`bilan.html?t=…`, §3) et sur la vue « Je suis le parent ».

> **Le bilan express de {prenom} : ce qu'il montre, et ce qu'il ne montre pas encore**
>
> En {duree_min} minutes et {n_questions} questions, le diagnostic express a mesuré {n_mesurees} compétences de 3e sur {n_total}.
>
> **Ce qu'il a trouvé** : {titre_parent_point_faible}. {libelle_parent_erreur}.
> {si cause_racine} Cette notion est un prérequis de {n_bloque} autres points du programme, dont {bloque_1_titre_parent}. C'est souvent là que « ça ne rentre pas » en 3e sans qu'on sache pourquoi.
>
> **Ce qu'il ne dit pas encore** : l'état des {n_total - n_mesurees} autres compétences, et l'origine exacte des difficultés.
>
> ---
> **Le diagnostic complet : 19 €**
> - Environ 40 minutes, en 3 parties que {prenom} peut faire en plusieurs fois
> - Un **bilan PDF de {n_pages} pages** pour vous : les 5 domaines, les compétences acquises, fragiles et en lacune, les causes racines, les erreurs types avec les réponses de {prenom} en exemple, et un **plan de travail de 4 semaines**
> - *[Aperçu : 2 pages d'un bilan exemple, cliquables en plein écran]*
>
> **Pour comparer** : une heure de cours particulier de maths en 3e coûte en moyenne 20 à 25 € après crédit d'impôt (environ 49 € avant).
>
> **Garantie 30 jours** : si le bilan ne vous est pas utile, écrivez-moi et je vous rembourse intégralement, sans justification.
>
> [ Obtenir le diagnostic complet — 19 € ] (principal)
>
> **Ou directement le Programme Brevet : 49 €, diagnostic inclus**
> Entraînement illimité sur toute la carte, un re-diagnostic chaque mois pour voir la progression, des brevets blancs, un bilan chaque semaine. Paiement unique, pas d'abonnement, accès jusqu'au Brevet et au-delà.
> Si vous commencez par le diagnostic, les 19 € seront déduits du programme : **vous ne payez jamais deux fois**, et rien ne presse.
> [ Programme Brevet — 49 € ] (secondaire)
>
> *Sans rien acheter, {prenom} garde son entraînement gratuit : 5 exercices par jour sur son point faible.*
>
> Nicolas Follezou — j'ai créé Matheux après des années de cours de maths. Une question avant de décider ? contact@matheux.fr, je réponds moi-même.

Pourquoi le diagnostic est mis en avant plutôt que le programme : c'est le plus petit pas. Avec la déduction, le parent ne perd rien à commencer par là. Et le PDF devient ensuite le meilleur argument pour le programme. On maximise la confiance d'abord, le panier ensuite.

### 2.5 Aperçu PDF

- 2 pages réelles du gabarit PDF (`js/bilan-pdf.js`, agent PDF), générées sur un **élève fictif clairement étiqueté** (bandeau « EXEMPLE — élève fictif »), pas sur un vrai élève, même anonymisé.
- Page 1 = vue d'ensemble (5 domaines). Page 2 = une cause racine avec erreur type et plan. Le reste du PDF est listé (table des matières), sans flou.
- Au clic : plein écran, lisible sur mobile. Si l'aperçu est illisible sur téléphone, il ne sert à rien.

### 2.6 Ancrage : ce qu'on dit et ce qu'on ne dit pas

- ✅ « Une heure de cours particulier de maths en 3e coûte en moyenne 20 à 25 € après crédit d'impôt. » (vérifiable, sources §1.1, on revérifie chaque rentrée)
- ✅ « Paiement unique, pas d'abonnement. »
- ❌ « 25× moins cher qu'un cours particulier » (ancienne phrase de `product.md`, comparaison non homogène)
- ❌ « Valeur 120 € » ou prix barré sans prix antérieur réel
- ❌ « Un prof analyse les résultats de {prenom} » : c'est automatique désormais (le contrat supprime « ton prof prépare la suite »). On peut dire « conçu par un ancien ingénieur qui accompagne des élèves en maths depuis des années ».

### 2.7 Quand on ne pousse pas

- Carte express **tout verte** → pas de bloc diagnostic mis en avant. On propose à la place : « Viser la mention ? Le Programme Brevet, c'est surtout des brevets blancs et de l'entraînement sur les points de détail. » Vendre un diagnostic de lacunes à un élève sans lacunes = remboursement + mauvais bouche-à-oreille.
- Élève qui n'a **fait aucun exercice gratuit** depuis 7 jours → on ne relance pas le parent sur l'achat (voir `51-emails.md`). Relancer d'abord l'usage.

---

## 3. Mécanique « Montre ta carte à tes parents »

### 3.1 Principe

L'ado a vu la valeur, le parent a le moyen de payer : le lien de partage fait le pont. Il sert à **informer**, pas à faire acheter. Le parent reçoit une page qui lui parle à lui, avec l'offre.

### 3.2 Parcours

1. L'ado tape [📨 Montrer ma carte à mes parents].
2. Feuille de partage :
   > **Montre ta carte à tes parents**
   > Ils verront : tes 5 domaines, ton point à travailler, et ce que contient le diagnostic complet.
   > Ils ne verront pas : tes réponses une par une, ton email, ton mot de passe.
   > Le lien marche 30 jours. Tu peux le désactiver quand tu veux depuis ta carte.
   >
   > [ WhatsApp ] [ SMS ] [ Email ] [ Copier le lien ]
3. Canaux :
   - **WhatsApp** : `https://wa.me/?text=<message encodé>`. L'ado choisit le contact dans WhatsApp. On ne collecte aucun numéro.
   - **SMS** : `sms:?&body=<message>` (iOS : `sms:&body=`). Envoyé depuis le téléphone de l'ado, **zéro coût, zéro numéro stocké**.
   - **Partage natif** : `navigator.share({title, text, url})` quand il est dispo (couvre les deux cas ci-dessus sur mobile).
   - **Email** : champ « Email de ton parent » **pré-rempli avec l'email du compte** (qui est déjà l'email du parent, `profiles.email`), modifiable. Envoi par Resend, template `P-SH` (`51-emails.md`). Un seul envoi par lien, 2 liens actifs max.
   - **Copier le lien** : presse-papier.
4. Message prérempli (modifiable par l'ado, à la 1re personne, **sans mention de prix**) :
   > « J'ai fait un diagnostic de maths sur Matheux. Voilà ma carte, ça montre où j'en suis : {lien} »
5. Le parent ouvre `https://matheux.fr/bilan.html?t=<token>` → page parent (§3.3).

### 3.3 Page parent (`bilan.html?t=…`)

Structure (maquette : agent UX ; copy : ici) :

1. **En-tête** : « {prenom} vous a partagé son bilan de maths » · date du diagnostic · « Lien personnel, valable jusqu'au {date_expiration} ».
2. **Ce qu'est Matheux, en 2 lignes** : « Matheux est un entraînement en maths pour les élèves de 3e, conçu par un ancien ingénieur qui accompagne des élèves en maths depuis des années. Le diagnostic repère ce qui bloque et remonte jusqu'aux notions des années précédentes quand c'est là que se trouve le problème. »
3. **La carte** (5 domaines + point faible) : même contenu que l'ado, rédaction parent (`libelle_parent`, `titre` au lieu de `titre_eleve`).
4. **Bloc offre** : §2.4 à l'identique.
5. **FAQ courte (5 questions)** :
   - *Combien de temps ça prend ?* « Environ 40 minutes pour le diagnostic complet, en 3 parties. {prenom} peut s'arrêter et reprendre. L'entraînement quotidien, c'est 5 à 10 minutes. »
   - *C'est un abonnement ?* « Non. Paiement unique, rien ne se renouvelle. »
   - *Et si ça ne sert à rien ?* « Garantie 30 jours : je rembourse intégralement, sur simple email. »
   - *Qui voit les résultats de mon enfant ?* « Vous, {prenom}, et moi pour le support. Rien n'est vendu ni partagé. Ce lien expire dans 30 jours et {prenom} peut le désactiver. »
   - *Est-ce que ça remplace les cours ?* « Non. C'est un complément : ça dit précisément quoi travailler, et ça fait travailler un peu chaque jour. Si {prenom} a déjà un prof particulier, le bilan PDF lui fera gagner les premières séances. »
6. **Bas de page** : « Vous n'êtes pas le parent de {prenom} ? Ignorez cette page. » · lien confidentialité · contact.

Paiement depuis cette page : les boutons ouvrent le Payment Link avec `client_reference_id={code}` (§4), **sans connexion**. Le parent n'a pas besoin de compte. C'est le raccourci qui compte le plus dans tout le funnel.

### 3.4 Exigences techniques (à transmettre à l'ingénieur adaptatif / UX)

- Token aléatoire ≥ 128 bits (pas le `code` élève, qui est court et devinable), table proposée `bilan_partages(token, code, type_carte, created_at, expires_at, revoked_at, vues, dernier_vu_at)`. Voir `52-legal.md` §5 pour la conservation.
- La page affiche un **instantané** de la carte express, pas les réponses brutes ni l'email.
- `<meta name="robots" content="noindex,nofollow">`, pas de GA4 sur cette page (visiteur non consentant), `Referrer-Policy: no-referrer`.
- Expiration 30 jours + révocation par l'ado. Lien expiré → « Ce lien a expiré. Demandez à {prenom} de vous en renvoyer un. » (sans afficher le prénom si le token est inconnu).
- Logger `share_created(canal)`, `share_viewed` (1re vue) pour les KPIs (§8).

---

## 4. Checkout Stripe

### 4.1 Architecture recommandée (v1, 10 élèves) : Payment Links

Trois Payment Links **à créer par Nicolas** (rien n'est créé ici) :

| Lien | Prix | `metadata` du Payment Link | Visible pour |
|---|---|---|---|
| Diagnostic complet 3e | 19 € | `produit=diag_complet`, `niveau=3EME`, `offre_version=2026-09` | tout non-acheteur |
| Programme Brevet 3e | 49 € | `produit=programme_brevet`, `niveau=3EME`, `offre_version=2026-09` | tout non-acheteur du programme sans diagnostic |
| Programme Brevet 3e, passage depuis le diagnostic | 30 € | `produit=programme_upgrade`, `niveau=3EME`, `offre_version=2026-09` | uniquement les acheteurs du diagnostic |

Paramètres d'URL ajoutés par le front : `?client_reference_id={code}&prefilled_email={email_compte}`.

- **`client_reference_id` = code élève.** C'est la clé fiable, parce que le parent paie souvent avec un autre email que celui du compte. ⚠️ **Conflit avec le code actuel** : le webhook fait `niveau = metadata.niveau || client_reference_id`. Si on passe le code en `client_reference_id`, il faut changer cette ligne pour que le code n'atterrisse pas dans `premium_niveau`. **À signaler à l'ingénieur adaptatif.**
- Le webhook doit : lire `metadata.produit`, retrouver le profil par `client_reference_id` (fallback : email), écrire les droits (`diag_complet_paye`, `programme_paye` ou équivalent), **enregistrer `session.id`, le montant et la date** (pour les remboursements et la garantie), puis déclencher l'email de confirmation `P-ACH1`/`P-ACH2` (`51-emails.md`), qui porte la confirmation de renonciation (obligation légale).
- `programme_upgrade` acheté **sans** diagnostic préalable (lien partagé) : on accorde le programme quand même. Perte de 19 € possible, acceptable à ce volume : on logge, on ne bloque pas.
- Métadonnées : le Payment Link recopie ses metadata sur les Checkout Sessions qu'il crée (c'est déjà ce sur quoi repose `metadata.niveau` aujourd'hui). À vérifier sur un paiement test en mode test Stripe.
- **Réglages Payment Link** : « Exiger l'acceptation des conditions » activé (lien CGV), texte personnalisé de la case (voir `52-legal.md` §2.3), redirection après paiement vers `app.html?achat={produit}` (ou `bilan.html?t=…&merci=1` si l'achat vient de la page parent), codes promo **désactivés** (pas de chasse au code, pas de fausse promo), facture/reçu Stripe activé.

**v2 (au-delà de ~50 clients)** : créer les sessions côté serveur (`create_checkout`, clé secrète Stripe dans l'Edge Function). Le serveur calcule 49 ou 30 €, ce qui ferme la fuite de l'upgrade et permet un vrai bump. Inutile maintenant.

### 4.2 Order bump : sur notre page, pas dans Stripe

Les *cross-sells* Stripe ajouteraient le programme **en plus** du diagnostic (19 + 49 = 68 €), ce qui est faux par rapport à notre promesse de déduction. Le « bump » honnête, c'est le **choix entre deux boutons** (§2.4) avant la redirection :

> ☐ Diagnostic complet — 19 €
> ☐ Programme Brevet — 49 € (diagnostic inclus · soit 30 € de plus pour tout le reste)
> *Même prix au total maintenant ou plus tard : si vous prenez le diagnostic aujourd'hui, les 19 € seront déduits.*

Rien n'est pré-sélectionné. La case de renonciation (`52-legal.md` §2.3) est capturée **ici, sur notre page**, horodatée côté serveur, avant la redirection vers Stripe. Elle est répétée dans le texte de la case CGV Stripe.

### 4.3 Remboursements (garantie 30 jours)

Nicolas rembourse depuis le dashboard Stripe (2 minutes, pas d'automatisation, règle « pas de sur-ingénierie »). Il retire ensuite les droits à la main dans Supabase, ou via un event `charge.refunded` en v2. Le délai de remboursement annoncé est de 14 jours maximum. Stripe prend quelques jours ouvrés.

---

## 5. Upsell et rétention

### 5.1 Après l'achat du diagnostic (19 €)

| Moment | Canal | Contenu | Upsell ? |
|---|---|---|---|
| Juste après le paiement | App (ado) + email P-ACH1 (parent) | « C'est parti : module 1 (15 min) ». Le parent sait que c'est à l'ado de jouer. | Non |
| Diagnostic complet terminé | App : **carte complète** + PDF · email P-PDF | La restitution. **Pas de vente sur cet écran.** Seule une ligne en bas du PDF (page « Et maintenant ? ») présente les 2 chemins : gratuit (5 exos/jour sur la priorité n° 1) ou programme (tout le plan). | Doux |
| J+3 après le PDF | Email P-UP1 | « Comment utiliser le plan de 4 semaines » : utile même sans acheter. Mention du programme à 30 €. | Oui |
| J+10 | Email P-UP2 | Progrès **factuels** sur la priorité n° 1 (maîtrise avant/après, nombre d'exos). Si aucun progrès ou aucune activité : on le dit, et on propose de l'aide, pas une vente. | Conditionnel |
| **J+28 : mini re-test offert** | App (ado) + email | « Prouve ta progression » : 10 questions sur tes 3 priorités, comparées au diagnostic. **Offert aux acheteurs du diagnostic** (c'est le re-diagnostic mensuel du programme, en version courte). | Oui : c'est la démonstration du programme |
| Après le re-test | Email P-UP3 | « {prenom} est passé de {x} à {y} sur {priorité} ». Si ça progresse : « le programme fait ça sur toute la carte, chaque mois ». Si ça ne progresse pas : on propose d'en parler (répondre à l'email), sans vendre. | Conditionnel |

### 5.2 Moments réels de l'année (urgence vraie)

| Période | Fait réel | Message |
|---|---|---|
| Tout au long de l'année | Semaines restantes avant le Brevet (fin juin 2027, **date officielle à vérifier et à mettre en constante**) | « Il reste {n} semaines avant le Brevet. » C'est un compte à rebours vrai, vers une date réelle. Jamais « offre valable 48 h ». |
| Novembre-décembre | Conseils de classe, **bulletin du 1er trimestre** | Email parent début décembre (au plus 1) : « Avant le bulletin : ce que la carte de {prenom} dit, compétence par compétence. » |
| Décembre-février | **Brevets blancs des collèges** (date variable selon l'établissement) | Dans l'app, on demande à l'ado **« C'est quand ton brevet blanc ? »** (facultatif). Si c'est renseigné : plan de révision daté, et un email parent 3 semaines avant. C'est l'urgence la plus honnête qui soit : c'est **sa** date. |
| Janvier | **Brevet blanc Matheux n° 1** (programme) | Pour les non-acheteurs : un sujet blanc **complet** mais **corrigé sans analyse détaillée** en gratuit ? → ❓ question pour Nicolas. Reco : le brevet blanc reste inclus au programme. Pour les gratuits : un « mini-blanc » de 20 min offert. |
| Avril | J-60 Brevet, **brevet blanc Matheux n° 2** | Email parent unique « dernière ligne droite » |
| Mai-juin | Révisions finales, brevet blanc n° 3 | Rétention programme uniquement. Plus aucune relance de vente aux gratuits après le 15 mai : ce serait jouer sur le stress. |

### 5.3 Rétention du Programme Brevet (ce qui fait revenir)

1. **Re-diagnostic mensuel** (1er week-end du mois) : la carte évolue, les couleurs virent au vert. C'est l'effet « prouve ta progression » côté ado, et un rapport côté parent.
2. **Bilan parent hebdo** (dimanche) : 5 lignes max, factuel (exos faits, compétences passées au vert, prochaine priorité).
3. **Brevets blancs Matheux** (janvier, avril, mai) : 3 rendez-vous annoncés dès l'achat, donc une raison de rester.
4. **Streak et quota quotidien** (existants) : on garde, avec le streak freeze (G3).
5. **Pas de relance culpabilisante** : un ado inactif 7 jours reçoit 1 message au ton léger. Son parent en reçoit 1 au 10e jour : « Voulez-vous que je vous aide à relancer ? ». Puis plus rien avant le re-diagnostic suivant.

---

## 6. Recueil de feedback (au lieu d'A/B tests)

À 10 élèves, aucun A/B test n'est significatif. On remplace par :
- Page de remerciement après achat : **1 question, en 1 clic** : « Qu'est-ce qui vous a décidé ? » (le bilan express · l'aperçu du PDF · le prix · la garantie · la demande de mon enfant · autre).
- Dernier email de conversion (`P-X3`) : « Qu'est-ce qui vous a retenu ? » (le prix · pas le temps · mon enfant n'accroche pas · on a déjà un prof · autre), avec des liens qui loggent la réponse.
- Nicolas appelle ou écrit aux 5 premiers acheteurs. Ça ne passe pas à l'échelle, et c'est exactement pour ça qu'il faut le faire maintenant.

---

## 7. Interdits (dark patterns à ne jamais utiliser)

| ⛔ Interdit | Pourquoi / exemple | Alternative honnête |
|---|---|---|
| **Exhorter l'ado à acheter ou à convaincre ses parents** | « Demande à tes parents de te l'offrir ! », « Débloque maintenant ». Pratique commerciale réputée agressive (liste noire UCPD, point 28). | « Montre ta carte à tes parents » (information) |
| Emails marketing ou prix envoyés à l'ado | Mineur, pas l'acheteur | Emails ado = pédagogiques uniquement (`51-emails.md`) |
| Faux avis, témoignages inventés, « 1 200 familles nous font confiance » | Faux | Aucun avis tant qu'on n'en a pas de vrais, datés, avec accord écrit |
| Fausse rareté (« plus que 3 places ») | Faux, c'est du numérique | — |
| Faux compte à rebours, « offre expire dans 24 h », déduction limitée dans le temps | Faux, et contraire à T2 | Semaines avant le Brevet, date du brevet blanc de l'élève |
| Prix barré fictif, « valeur 120 € » | Le prix de référence doit être le plus bas pratiqué sur 30 jours | Ancrage cours particulier, sourcé |
| **Dramatiser les lacunes** (« votre enfant a 2 ans de retard », rouge partout) | Joue sur l'angoisse parentale, et c'est souvent faux sur 15 questions | Vocabulaire du contrat (lacune / fragile / acquis / non évalué), toujours accompagné du point fort |
| Flouter des résultats qui n'existent pas | Suggère un savoir qu'on n'a pas | « Pas encore mesuré » |
| Promesse de résultat (« +4 points au Brevet garantis ») | Invérifiable | « Vous saurez précisément quoi travailler » |
| Confirmshaming (« Non merci, je ne veux pas que mon enfant réussisse ») | Manipulation | « Continuer gratuitement » |
| Case pré-cochée (programme, newsletter, renonciation) | Nul juridiquement, et déloyal | Toutes les cases vides par défaut |
| Paywall bloquant avant d'avoir montré la carte | Valeur avant paywall | Carte d'abord, toujours |
| Abonnement caché ou reconduction | Contraire à T2 | Paiement unique, écrit partout |
| Remboursement rendu difficile (formulaire, justificatif) | Roach motel | 1 email suffit |
| Présenter le droit de rétractation légal comme un avantage (« 14 jours pour changer d'avis ! » en badge) | Pratique trompeuse (droits légaux présentés comme propres à l'offre) | La garantie 30 jours, qui va au-delà de la loi |
| Laisser croire qu'un humain analyse chaque élève | C'est l'algorithme (contrat : fin du « ton prof prépare la suite ») | « Conçu par un ancien ingénieur qui accompagne des élèves en maths depuis des années » · « je lis vos réponses » (si vrai) |
| Emails après désinscription, relances nocturnes, > 1 relance marketing / 72 h | Harcèlement | Plafonds de `51-emails.md` |
| Relancer la vente aux gratuits après le 15 mai | Joue sur le stress de l'examen | Stop, et entraînement gratuit maintenu |

---

## 8. KPIs du funnel et logging minimal

### 8.1 Funnel (cohorte = semaine d'inscription)

| # | Étape | Event à logger | KPI | Cible (hypothèse) |
|---|---|---|---|---|
| 1 | Diagnostic express commencé | `diag_express_start` | — | — |
| 2 | Diagnostic express fini | `diag_express_done` | finis / commencés | ≥ 70 % |
| 3 | Compte créé | `signup` (existant : `profiles`) | comptes / diagnostics finis | ≥ 50 % |
| 4 | Bloc offre vu | `paywall_view` (ado ou parent, `meta.vue`) | — | — |
| 5 | Carte partagée | `share_created` (`meta.canal`) | partages / comptes | ≥ 25 % |
| 6 | Page parent ouverte | `share_viewed` (1re vue) | vues / partages | ≥ 60 % |
| 7 | Clic checkout | `checkout_click` (`meta.produit`, `meta.source` = app/parent/email) | — | — |
| 8 | **Achat diagnostic** | `purchase` (webhook, `meta.produit`, `meta.montant`) | achats diag / comptes | **5-10 %** |
| 9 | Diagnostic complet terminé | `diag_complet_done` (+ `module_done` ×3) | terminés / achetés | ≥ 80 % (sinon problème produit, pas marketing) |
| 10 | PDF ouvert | `pdf_open` | ouverts / générés | ≥ 70 % |
| 11 | **Achat programme** | `purchase` (`programme_*`) | programmes / diagnostics | **25-35 %** |
| 12 | Remboursement | `refund` (manuel) | remboursés / achats | < 10 % (au-delà, le produit ne tient pas la promesse) |
| 13 | Rétention | dérivé de `scores` | % actifs à J+7 et J+30 (≥ 1 exo dans la semaine) | J+7 ≥ 50 %, J+30 ≥ 30 % |

Indicateur n° 1 à regarder chaque lundi : **achats (diag + programme) / diagnostics express finis**. Indicateur n° 2 : **taux de remboursement**, qui est l'honnêteté mesurée.

### 8.2 Ce qu'il faut logger, et rien de plus

- **Une seule table** proposée à l'ingénieur adaptatif : `funnel_events(id, code nullable, event text, meta jsonb, created_at)`. Pas d'IP, pas d'user-agent, pas d'email. On logge côté serveur (first-party, pas de cookie). Ça ne dépend donc pas du consentement GA4, qui ne verra qu'une fraction du trafic.
- Les ~12 events ci-dessus, **pas un de plus**. Les emails sont déjà dans `email_logs`, les scores dans `scores`.
- Conservation 13 mois (voir `52-legal.md`).
- Lecture : 1 requête SQL « funnel de la semaine » à mettre dans `check_students.py` ou dans l'onglet RAPPORT de l'admin. **Pas de dashboard dédié** (règle « pas de sur-ingénierie »).
- Liens email : ajouter `?src=email_{type}` aux CTA pour attribuer `checkout_click`. **Pas d'UTM vers GA4.**

---

## 9. Copy landing (prête à l'emploi pour l'agent landing)

> Règles : **aucun faux avis, aucun faux chiffre.** Les seuls nombres autorisés sont ceux du produit lui-même (durées, nombres de questions, prix), et ils viennent de constantes. `{N_COMP}` = nombre réel de compétences dans `data/referentiel_3eme/competences.json`, calculé au build ou écrit à la main **après** vérification ; s'il n'est pas connu, on retire la phrase. `{SEMAINES_BREVET}` = calcul JS depuis une constante de date (Brevet 2027, date officielle à confirmer) ; si la constante est vide, on retire la mention. Pas de logos d'établissements, pas de « vu dans », pas de compteur d'inscrits.
> Double audience : le **hero parle à l'ado** (c'est lui qui passe le test, il faut qu'il ait envie de cliquer), le **sous-titre et tout le bas de page parlent au parent** (c'est lui qui lit la page jusqu'au bout et qui paie). Contrainte légale : la landing ne dit jamais à l'ado d'acheter ni de convaincre ses parents (§7).

### 9.1 Hero

- **Surtitre** : `Maths · 3e · Brevet 2027`
- **H1 (ado)** : **Sache exactement ce qui te bloque en maths.**
  - Variante A : **Tes maths de 3e, en carte. Tu vois ce qui coince, tu sais quoi faire.**
  - Variante B : **Pas « nul en maths ». Juste 2 ou 3 trucs qui coincent. On les trouve.**
- **Sous-titre (parent)** : Un diagnostic de maths conçu par un prof, qui repère les notions fragiles de votre enfant, y compris celles des années précédentes qui bloquent en 3e, et lui donne quoi travailler chaque jour. Gratuit pour commencer.
- **CTA principal** : `Faire le diagnostic gratuit →`
- **Microcopie sous le CTA** : `~8 min · 15 questions · sans carte bancaire`
- **CTA secondaire (lien texte)** : `Je suis parent : comment ça marche ?` → ancre §9.3
- **Ligne d'urgence réelle** (si `{SEMAINES_BREVET}` est défini) : `Brevet dans {SEMAINES_BREVET} semaines.` Discret, pas de couleur d'alerte, pas de secondes qui défilent.

### 9.2 Comment ça marche (3 étapes)

1. **Diagnostic express, gratuit.** 15 questions qui s'adaptent à tes réponses. En 8 minutes, tu obtiens ta carte : 5 domaines, et ton point le plus fragile expliqué.
2. **Entraînement gratuit, 5 exos par jour.** Sur ton point fragile, avec des indices quand tu bloques. 10 minutes max.
3. **Diagnostic complet, pour aller au fond (19 €).** 40 minutes en 3 parties. Toutes les compétences de 3e, les causes qui remontent aux années d'avant, et un bilan PDF avec un plan de 4 semaines.

CTA sous le bloc : `Commencer par le gratuit →`

### 9.3 Bénéfices

**Pour toi (ado)**
- **Tu sais par où commencer.** Fini le « je révise tout et je ne sais pas quoi ».
- **Ça remonte à la source.** Si les équations coincent à cause des fractions de 5e, on te le dit, et on repart de là.
- **10 minutes par jour.** Pas une séance de 2 heures. 5 exos, des indices, et c'est fini.
- **Tu vois ta carte passer au vert.** Chaque mois, un re-test te montre ce qui a bougé.

**Pour vous (parent)**
- **Un constat précis, pas une impression.** « Fragile en calcul littéral, à cause des priorités opératoires », plutôt que « a du mal en maths ».
- **Un bilan que vous pouvez lire en 5 minutes.** Le PDF du diagnostic complet est écrit pour vous : ce qui est acquis, ce qui bloque, par quoi commencer.
- **Un travail régulier, sans que vous ayez à le surveiller.** L'entraînement suit le plan tout seul.
- **Paiement unique, pas d'abonnement.** Rien ne se renouvelle.
- **Remboursé si ça ne sert pas.** Garantie 30 jours, sur simple email.

*[Visuel : aperçu de 2 pages d'un bilan PDF, bandeau « EXEMPLE — élève fictif »]*

### 9.4 Bloc offre et prix

> **Titre** : Commencez gratuitement. Payez seulement si c'est utile.

| | **Gratuit** | **Diagnostic complet** | **Programme Brevet** |
|---|---|---|---|
| Prix | 0 € | **19 €** · une fois | **49 €** · une fois, diagnostic inclus |
| Diagnostic express (15 questions) + carte des 5 domaines | ✓ | ✓ | ✓ |
| Point le plus fragile expliqué | ✓ | ✓ | ✓ |
| Entraînement quotidien | 5 exos/jour sur le point fragile | 5 exos/jour sur la priorité n° 1 | **Illimité, sur toute la carte** |
| Diagnostic complet (~40 min, toutes les compétences, causes racines) | — | ✓ | ✓ |
| Bilan PDF pour les parents + plan 4 semaines | — | ✓ | ✓ |
| Re-diagnostic chaque mois pour mesurer la progression | — | 1 re-test offert à 4 semaines | ✓ |
| Brevets blancs corrigés | — | — | ✓ |
| Bilan parent chaque semaine | — | — | ✓ |
| CTA | `Faire le diagnostic gratuit` | `Commencer par le diagnostic` | `Choisir le programme` |

Sous le tableau (3 lignes, dans cet ordre) :
- **Déjà pris le diagnostic ? Les 19 € sont déduits du programme** (30 € au lieu de 49 €). Vous ne payez jamais deux fois, et rien ne presse.
- **Garantie 30 jours** : si ce n'est pas utile, un email et je vous rembourse intégralement.
- **Pour comparer** : une heure de cours particulier de maths en 3e coûte en moyenne 20 à 25 € après crédit d'impôt. *(Mention en petit : « Moyennes constatées en septembre 2026 sur des plateformes de cours particuliers. » On revérifie chaque rentrée.)*

Microcopies :
- Sous les CTA payants : `Paiement sécurisé Stripe · pas d'abonnement · TVA non applicable, art. 293 B du CGI`
- ⛔ **Pas de badge « Droit de rétractation 14 jours »** (l'actuel `premium.html` en a un : à retirer, cf. §7 et `52-legal.md`).
- Sur mobile, le bloc gratuit est **au-dessus**. Le payant n'est jamais la première chose vue.

### 9.5 Le fondateur (bloc de confiance, 100 % vrai)

> **Qui est derrière Matheux ?**
> Je m'appelle Nicolas Follezou. Ancien ingénieur, j'accompagne depuis des années des dizaines d'élèves en soutien scolaire de maths, et le même constat revenait sans cesse : un élève « nul en maths » ne l'est presque jamais. Il bute sur 2 ou 3 notions, souvent vues des années plus tôt, et tout le reste s'écroule par-dessus. Matheux sert à trouver ces notions-là, puis à les retravailler un peu chaque jour.
> Matheux est un petit projet indépendant. Si vous m'écrivez, c'est moi qui réponds : contact@matheux.fr.

✅ Parcours validé par Nicolas le 24/09 : ancien ingénieur, accompagne depuis des années des dizaines d'élèves en soutien scolaire maths. **Ne jamais écrire « prof de maths ».** **Pas de photo stock** : une vraie photo, ou pas de photo.

### 9.6 FAQ parent (8 questions)

1. **Combien de temps ça prend à mon enfant ?**
   Le diagnostic express prend environ 8 minutes. L'entraînement quotidien, 5 à 10 minutes. Le diagnostic complet (payant) prend environ 40 minutes, en 3 parties que votre enfant peut faire en plusieurs fois.
2. **Qu'est-ce que je reçois exactement pour 19 € ?**
   Votre enfant passe le diagnostic complet, qui mesure toutes les compétences de maths de 3e et remonte aux notions des années précédentes quand c'est là que se trouve le blocage. Vous recevez un bilan PDF : les 5 domaines du programme, ce qui est acquis, fragile ou en lacune, les erreurs types avec ses propres réponses en exemple, et un plan de travail de 4 semaines.
3. **C'est un abonnement ?**
   Non. Chaque offre se paie une seule fois. Rien ne se renouvelle, il n'y a rien à résilier.
4. **Et si ce n'est pas utile ?**
   Pendant 30 jours après l'achat, un simple email à contact@matheux.fr suffit pour être remboursé intégralement, sans justification.
5. **Est-ce que ça remplace un professeur particulier ?**
   Non, c'est un complément. Matheux dit précisément quoi travailler et fait travailler un peu chaque jour. Si votre enfant a déjà un professeur, le bilan PDF peut lui faire gagner les premières séances.
6. **Mon enfant a de bonnes notes. Est-ce utile ?**
   Peut-être moins. Si le diagnostic express ne trouve rien d'inquiétant, on vous le dira, et on ne vous poussera pas à acheter le diagnostic complet. Le Programme Brevet sert alors surtout à s'entraîner sur des sujets de type Brevet.
7. **Que faites-vous des données de mon enfant ?**
   Nous collectons son prénom (pas son nom), sa classe, votre email et ses réponses aux exercices, uniquement pour faire fonctionner le service. Rien n'est vendu ni utilisé pour de la publicité. Vous pouvez tout supprimer sur simple demande. Détails dans la [politique de confidentialité](politique-confidentialite.html).
8. **Qui décide de l'achat ?**
   Vous. Votre enfant peut utiliser la partie gratuite seul, et vous envoyer sa carte s'il le souhaite. Le paiement se fait par carte bancaire, par un adulte, via Stripe.

### 9.7 FAQ ado (5 questions)

1. **C'est une interro ?**
   Non. Pas de note, personne ne te juge. Si tu ne sais pas, tu cliques « Je ne sais pas ». Ça aide le diagnostic plus qu'une réponse au hasard.
2. **Ça prend combien de temps ?**
   8 minutes pour le diagnostic express. Ensuite, 5 exos par jour, 10 minutes max.
3. **Je suis nul en maths, ça sert à quelque chose ?**
   C'est justement pour ça. En général, on n'est pas « nul en maths » : il y a 2 ou 3 trucs qui coincent. Le diagnostic les trouve, et tu repars de là.
4. **C'est gratuit ?**
   Le diagnostic express et 5 exos par jour, oui, pour de vrai et sans limite de durée. Le diagnostic complet et le programme Brevet sont payants : ça, c'est à voir avec tes parents.
5. **Mes parents vont voir mes résultats ?**
   Seulement si tu leur envoies ta carte, ou s'ils ont le bilan du diagnostic complet. L'email de ton compte est celui d'un parent : il reçoit un message quand tu t'inscris.

### 9.8 CTA final et microcopies diverses

- **Bloc final (ado)** : **8 minutes pour savoir où tu en es.** → `Faire le diagnostic gratuit →` · `Sans carte bancaire · sans inscription pour commencer`
  - ⚠️ « sans inscription pour commencer » : **seulement si** l'express se passe avant la création du compte (parcours actuel : diagnostic → résultats → inscription). À confirmer avec l'agent UX.
- **Bloc final (parent)** : Vous voulez voir avant votre enfant ? `Voir un exemple de bilan →` (ouvre l'aperçu PDF d'exemple)
- **Footer** : `Matheux · soutien en maths pour la 3e · conçu par un ancien ingénieur qui accompagne des élèves en maths depuis des années · Mentions légales · CGU · CGV · Confidentialité · Cookies · contact@matheux.fr`
- **Bandeau cookies** : aucun GA4 avant accord (existant, à conserver). Boutons `Accepter` et `Refuser` de même taille et même couleur.
- **États de boutons** : chargement `Un instant…` · erreur réseau `Oups, la connexion a coupé. Réessaie.`

---

## ❓ Questions pour Nicolas

1. **Prix 19 / 49 € avec déduction sans date limite ?** → Reco : **oui**, test à 59 € seulement après 10 programmes vendus.
2. **Garantie 30 jours sans justification sur les deux produits ?** → Reco : **oui** (1 remboursement par foyer).
3. **Mise en avant du diagnostic plutôt que du programme sur le paywall parent ?** → Reco : **diagnostic en principal** (plus petit pas, confiance d'abord).
4. **Mini re-test offert à J+28 aux acheteurs du diagnostic ?** → Reco : **oui**, c'est la meilleure démo du programme.
5. **Brevet blanc Matheux : inclus au programme uniquement, et « mini-blanc » 20 min offert aux gratuits ?** → Reco : **oui**.
6. **Demander à l'ado la date de son brevet blanc (facultatif) ?** → Reco : **oui**, c'est l'urgence la plus honnête du funnel.
7. **Tu crées les 3 Payment Links (19 / 49 / 30) avec `metadata.produit` ?** → Reco : oui, en mode test d'abord. On vérifie la recopie des metadata sur un paiement test avant de publier.
8. **Landing : H1 principal ou variante A/B (§9.1) ?** → Reco : H1 principal « Sache exactement ce qui te bloque en maths. »
9. **Bloc fondateur (§9.5) : tu valides le texte et tu fournis une vraie photo ?** → Reco : oui, c'est le seul « social proof » honnête qu'on a aujourd'hui.
