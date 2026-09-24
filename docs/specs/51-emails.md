# 51 — Séquence emails déclenchée par le diagnostic

> Agent : growth-cro · 24/09/2026 · Statut : **proposition, non implémentée**
> Remplace la séquence J+0/J+1/J+3/J+7/J+14 d'`index.ts` (`templateJ0…J14`, `cronSendEmails`).
> Les anciens comptes sont supprimés (contrat §7), donc **aucune séquence de réactivation ni branche legacy** :
> la nouvelle séquence s'applique à tous les comptes créés après le déploiement.
> Liés : `50-offre-conversion.md` (offre, liens, interdits), `52-legal.md` (consentements, prospection).

---

## 0. Principes

1. **Les emails suivent des événements, pas le calendrier.** Un email part parce qu'il s'est passé quelque chose (diagnostic fini, bilan partagé, achat, PDF prêt, inactivité), et plus seulement parce qu'il s'est écoulé N jours.
2. **Deux audiences, deux adresses, deux règles.**
   - **Parent** (`profiles.email`, déjà « Email du parent » à l'inscription) : vouvoiement, factuel, signé Nicolas. C'est **le seul destinataire de messages commerciaux.**
   - **Ado** (`profiles.email_eleve`, **nouveau champ facultatif**, à créer par l'ingénieur adaptatif) : tutoiement, pédagogique uniquement. **Jamais de prix, jamais de lien de paiement, jamais d'incitation à faire acheter** (`52-legal.md` §6).
3. **Trois catégories**, qui ne suivent pas les mêmes règles :

| Catégorie | Exemples | Désinscription (`UNSUB`) | Plafond | Consentement |
|---|---|---|---|---|
| **T : transactionnel** | confirmation d'achat, PDF prêt, bilan partagé à la demande de l'ado, confirmation de l'inscription, reset MDP | **N'arrête pas** (nécessaire au service) | aucun | exécution du contrat |
| **P : pédagogique** | rappel d'entraînement, re-test, bilan hebdo (programme) | Arrête | voir §4 | exécution du contrat / intérêt légitime ⚠️ |
| **M : marketing** | explication de l'offre, relances de conversion, moments saisonniers | Arrête | voir §4 | **opt-in parent** (case non cochée à la confirmation, §2 P-X0) ⚠️ `52-legal.md` §7 |

4. **Honnêteté** : tout chiffre cité vient de la carte ou de `scores`. Si la donnée manque, la phrase saute (chaque bloc a une condition). On n'écrit jamais « Nicolas a analysé » : c'est l'algorithme qui analyse, et Nicolas lit les réponses.
5. **Signature parent** : « Nicolas · Fondateur de Matheux, prof de maths » (reprend `emailWrap`). **Signature ado** : « L'équipe Matheux 🎯 » ou « Nicolas, de Matheux » (❓ question). Reply-to : `contact@matheux.fr` (existant).

---

## 1. Variables disponibles

| Variable | Source |
|---|---|
| `{prenom}` | `profiles.prenom` |
| `{point_faible_parent}` / `{point_faible_eleve}` | carte express : 1re compétence en lacune/fragile, `titre` / `titre_eleve` |
| `{erreur_parent}` | `erreurs[0].libelle_parent` (si présent) |
| `{bloque_1_parent}`, `{n_bloque}` | `bloque[]` si `cause_racine` |
| `{n_mesurees}`, `{n_total}` | carte express |
| `{domaines_resume}` | ex. « 2 domaines solides, 2 fragiles, 1 à travailler » (calcul) |
| `{n_exos_semaine}`, `{n_jours_actifs}` | `scores` |
| `{maitrise_avant}`, `{maitrise_apres}` | modèle de maîtrise (en %, arrondi à 5) |
| `{priorite_1_parent}` | `carte.priorites[0]` |
| `{semaines_brevet}` | constante de date du Brevet (à confirmer) |
| `{lien_app}` | `https://matheux.fr/app.html?src=email_{type}` |
| `{lien_bilan}` | `https://matheux.fr/bilan.html?t={token}` (page parent, `50` §3.3) |
| `{lien_diag}`, `{lien_prog}`, `{lien_upgrade}` | Payment Links + `client_reference_id={code}` (`50` §4) |
| `{lien_pdf}` | lien signé vers le PDF (durée limitée, cf. `52-legal.md` §5) |
| `{lien_confirm}` | lien de confirmation parent (token), §2 P-X0 |

---

## 2. Séquence

Notation : **P-** = parent, **A-** = ado. `type` = valeur écrite dans `email_logs.type` (préfixe `D3:` pour « diagnostic 3e », pour ne pas croiser les anciens `J+N`).

### Vue d'ensemble

```
Inscription + diagnostic express fini (événement E1)
 ├─ P-X0  [T+M] immédiat : bilan express + confirmation parentale (+ opt-in conseils)
 ├─ A-X0  [P]   immédiat, si email_eleve : ta carte
 ├─ A-X1  [P]   J+1 17h, si 0 exo depuis l'inscription
 ├─ P-X1  [M]   J+2, si pas d'achat et opt-in : ce que le complet ajoute
 ├─ P-X2  [M]   J+6, si pas d'achat, opt-in et ≥ 2 jours actifs : 1re semaine
 ├─ P-X2b [P]   J+6 à la place de P-X2, si 0-1 jour actif : relancer l'usage, pas la vente
 └─ P-X3  [M]   J+13, si pas d'achat et opt-in : dernier message sur le sujet → STOP conversion

Carte partagée par l'ado via email (E2) ─ P-SH [T] immédiat
Achat diagnostic (E3) ─ P-ACH1 [T] + A-ACH1 [P] ; relances modules A-MOD J+2, P-MOD J+5
Diagnostic complet fini (E4) ─ P-PDF [T] + A-PDF [P] ; P-UP1 J+3 [M] ; P-UP2 J+10 [M]
J+28 après PDF (E5) ─ A-RT [P] re-test offert ; P-UP3 [M] après le re-test
Achat programme (E6) ─ P-ACH2 [T] + A-ACH2 [P] ; P-HEBDO [P] chaque dimanche ; A-MENS [P] 1er samedi du mois
Saisonniers (M, parent, non-acheteurs du programme, opt-in) : S-DEC (début déc.), S-BB (3 sem. avant le brevet blanc saisi), S-AVR (J-60 Brevet). Aucun après le 15 mai.
```

---

### P-X0 — Bilan express + confirmation parentale · `D3:P-X0` · T (+ opt-in M)

**Déclencheur** : diagnostic express fini **et** compte créé (remplace `templateJ0`, envoyé depuis `register()` ou à la sauvegarde de la carte, selon l'ordre final du parcours).
**Condition** : toujours. Transactionnel : il porte la confirmation parentale.

- **Objet** : `Le bilan maths de {prenom} (et une confirmation à faire)`
- **Préheader** : `{domaines_resume}. 1 clic pour confirmer l'inscription.`

> Bonjour,
>
> {prenom} vient de passer le diagnostic express de maths sur Matheux et a créé son espace avec votre adresse email.
>
> **1. Merci de confirmer l'inscription**
> {prenom} est mineur(e) : j'ai besoin de votre accord de parent pour conserver son espace et ses résultats.
> **[ Je confirme l'inscription de {prenom} ]** → `{lien_confirm}`
> *Sur la page de confirmation, vous pourrez aussi choisir de recevoir mes conseils et offres (facultatif). Si ce n'est pas vous, ou si vous n'êtes pas d'accord, ignorez ce message : sans confirmation sous 30 jours, l'espace est supprimé.*
>
> **2. Ce que montre le diagnostic express**
> En quelques minutes, il a mesuré {n_mesurees} compétences de 3e sur {n_total}. Résultat : {domaines_resume}.
> *{si point faible}* Le point le plus fragile : **{point_faible_parent}**. {erreur_parent}.
> *{si cause_racine}* C'est une notion dont dépendent {n_bloque} autres points du programme, dont {bloque_1_parent}.
> *{si rien de fragile}* Rien d'inquiétant sur cet échantillon, ce qui est une bonne nouvelle.
>
> **3. Et maintenant ?**
> Dès aujourd'hui, {prenom} a accès gratuitement à 5 exercices par jour sur ce point. 10 minutes suffisent. Aucune carte bancaire n'est demandée.
> [ Voir le bilan de {prenom} ] → `{lien_bilan}`
>
> Une question ? Répondez à cet email, c'est moi qui lis.
> Nicolas

**Notes** : pas de prix dans cet email (il est d'abord transactionnel). Le prix apparaît sur la page bilan, que le parent ouvre volontairement. **La page `{lien_confirm}` porte la case d'opt-in marketing** (non cochée) : « Je souhaite recevoir par email des conseils et les offres Matheux pour accompagner {prenom} (2 à 4 emails par mois maximum, désinscription en 1 clic). » Sans opt-in : seuls T et P partent.

Relance de confirmation : **`D3:P-X0R`** à J+3 et J+20 si pas de confirmation (T, 2 max). Objet : `Rappel : l'espace maths de {prenom} attend votre accord`. Corps : les 3 premières phrases du bloc 1 et le bouton. ❓ Suppression à J+30 : voir questions.

---

### A-X0 — Ta carte · `D3:A-X0` · P

**Condition** : `email_eleve` renseigné.

- **Objet** : `Ta carte de maths est prête, {prenom}`
- **Préheader** : `Ton point à travailler, et tes 5 exos du jour.`

> Salut {prenom},
>
> Ta carte est prête. Ton point à travailler : **{point_faible_eleve}**.
> *{si cause_racine}* Et c'est un point clé : quand il est solide, {bloque_1_eleve} devient beaucoup plus facile.
>
> 5 exos t'attendent dessus. 10 minutes, des indices si tu bloques.
> [ Faire mes 5 exos → ] `{lien_app}`
>
> À tout de suite 🎯

---

### A-X1 — Rappel doux J+1 · `D3:A-X1` · P

**Condition** : `email_eleve` renseigné, 0 exercice depuis l'inscription, envoi à 17h (§4).

- **Objet** : `5 exos, 10 minutes, et c'est fini`
- **Préheader** : `Sur {point_faible_eleve}, pile ce qu'il te faut.`

> Hey {prenom},
> Tes 5 exos sur **{point_faible_eleve}** sont prêts. Commence par le premier, tu verras bien.
> [ C'est parti → ] `{lien_app}`

Un seul rappel de ce type. Si l'ado ne vient pas, on ne le relance plus avant le re-test (règle anti-harcèlement).

---

### P-X1 — Ce que le complet ajoute · `D3:P-X1` · M · J+2

**Condition** : aucun achat, opt-in marketing = oui, carte express avec au moins 1 point fragile (**si tout est vert, on n'envoie pas P-X1** : `50` §2.7).

- **Objet** : `Ce que le diagnostic express ne dit pas encore sur {prenom}`
- **Préheader** : `{n_total - n_mesurees} compétences restent à mesurer.`

> Bonjour,
>
> Le diagnostic express de {prenom} a mesuré {n_mesurees} compétences sur {n_total}. Il a trouvé un point fragile, **{point_faible_parent}**, mais il ne dit pas encore deux choses importantes :
> - **où en sont les {n_total - n_mesurees} autres compétences** du programme de 3e ;
> - **d'où vient la difficulté.** En 3e, un blocage vient souvent d'une notion de 5e ou de 4e jamais consolidée. Tant qu'on ne l'a pas trouvée, on révise au mauvais endroit.
>
> C'est le rôle du **diagnostic complet** : environ 40 minutes pour {prenom}, en 3 parties. Pour vous, un **bilan PDF** : les compétences acquises, fragiles et en lacune, les causes racines, les erreurs types avec ses propres réponses, et un plan de 4 semaines.
> *[image : aperçu 2 pages d'un bilan exemple]*
>
> **19 €, une seule fois.** Pour comparer, une heure de cours particulier de maths en 3e coûte en moyenne 20 à 25 € après crédit d'impôt.
> **Garantie 30 jours** : si le bilan ne vous est pas utile, je vous rembourse sur simple email.
>
> [ Obtenir le diagnostic complet — 19 € ] `{lien_diag}`
>
> Et si vous ne souhaitez rien acheter : {prenom} garde ses 5 exercices gratuits par jour, sans limite de durée.
> Nicolas

---

### P-X2 — Première semaine · `D3:P-X2` · M · J+6

**Condition** : aucun achat, opt-in = oui, `n_jours_actifs` ≥ 2 depuis l'inscription.

- **Objet** : `La première semaine de {prenom} en maths`
- **Préheader** : `{n_exos_semaine} exercices, {n_jours_actifs} jours d'entraînement.`

> Bonjour,
>
> Voici la semaine de {prenom} sur Matheux, en chiffres :
> - **{n_exos_semaine} exercices** faits, sur **{n_jours_actifs} jours**
> - Sur **{point_faible_parent}** : *{si progrès}* de {maitrise_avant} % à {maitrise_apres} % de réussite au premier essai. *{sinon}* pas encore de progrès net, ce qui est normal sur une notion ancienne : il faut en général 2 à 3 semaines.
>
> Ce que je vous conseille à ce stade : laisser {prenom} continuer au même rythme. La régularité compte plus que la durée.
>
> Si vous voulez aller plus loin, le **diagnostic complet** (19 €) cartographie tout le programme et donne un plan de travail pour les 4 prochaines semaines. S'il ne vous est pas utile, il est remboursé pendant 30 jours.
> [ Voir le diagnostic complet ] `{lien_bilan}`
> Nicolas

### P-X2b — Relancer l'usage, pas la vente · `D3:P-X2b` · P · J+6

**Condition** : aucun achat, 0 ou 1 jour actif. **Remplace P-X2** (jamais les deux). Aucune condition d'opt-in (pédagogique).

- **Objet** : `{prenom} n'a pas encore repris ses exercices`
- **Préheader** : `5 minutes suffisent pour relancer.`

> Bonjour,
>
> {prenom} a fait le diagnostic il y a une semaine, mais l'entraînement n'a pas encore vraiment démarré. C'est très fréquent, et ça se relance facilement.
> Une idée qui marche bien : proposer à {prenom} de faire les 5 exercices du jour **à côté de vous**, juste une fois. Ça prend 10 minutes, et le plus dur, c'est le premier.
> [ Ouvrir Matheux ] `{lien_app}`
> Si quelque chose bloque (un bug, un exercice incompréhensible), répondez-moi : je corrige.
> Nicolas

Pas de lien de paiement dans cet email.

---

### P-X3 — Dernier message sur le sujet · `D3:P-X3` · M · J+13

**Condition** : aucun achat, opt-in = oui, P-X1 **ou** P-X2 déjà envoyé. **C'est la dernière relance de conversion** : ensuite, seuls les saisonniers (3 par an au plus) partent.

- **Objet** : `Je ne vous relancerai plus sur le diagnostic`
- **Préheader** : `Une dernière info, et une question.`

> Bonjour,
>
> C'est mon dernier message sur le diagnostic complet de {prenom}. Promis, je ne vous relancerai plus à ce sujet.
>
> Pour résumer : **19 €** une fois, environ 40 minutes pour {prenom}, un bilan PDF avec un plan de 4 semaines, et remboursé pendant 30 jours s'il ne vous sert pas. Si vous passez un jour au Programme Brevet, ces 19 € seront déduits.
> [ Diagnostic complet — 19 € ] `{lien_diag}`
>
> Dans tous les cas, {prenom} garde son entraînement gratuit.
>
> **Une question, si vous avez 5 secondes** : qu'est-ce qui vous a retenu ?
> [ Le prix ] [ Pas le temps ] [ Mon enfant n'accroche pas ] [ On a déjà un prof ] [ Autre ]
> *(1 clic = réponse enregistrée : liens `?src=email_D3:P-X3&raison=…` qui loggent `funnel_events`)*
>
> Merci d'avoir essayé Matheux.
> Nicolas

---

### P-SH — Carte partagée par l'ado · `D3:P-SH:{token}` · T

**Déclencheur** : l'ado choisit « Email » dans la feuille de partage (`50` §3.2). **Dédup par token** : 1 envoi par lien, 2 liens actifs max.
**Condition** : si P-X0 a été envoyé **à la même adresse il y a moins de 24 h**, on envoie la version courte.

- **Objet** : `{prenom} vous a envoyé son bilan de maths`
- **Préheader** : `Sa carte : ce qui va, ce qui coince.`

> Bonjour,
>
> {prenom} a souhaité vous montrer son bilan de maths, fait sur Matheux.
> [ Voir le bilan de {prenom} ] `{lien_bilan}`
> Le lien est personnel et valable jusqu'au {date_expiration}. {prenom} peut le désactiver à tout moment.
>
> *(version longue uniquement)* Matheux est un entraînement en maths pour la 3e, conçu par un prof de maths. Le diagnostic repère les notions fragiles, y compris celles des années précédentes.
>
> Vous n'êtes pas le parent de {prenom} ? Ignorez simplement ce message.
> Nicolas

Pas de prix dans l'email (l'offre est sur la page). C'est ce qui le garde transactionnel : l'envoi est demandé par l'utilisateur. ⚠️ `52-legal.md` §7.

---

### P-ACH1 — Confirmation d'achat du diagnostic · `D3:P-ACH1` · T

**Déclencheur** : webhook `produit=diag_complet`. **Obligatoire légalement** : c'est la confirmation sur support durable, avec la renonciation (`52-legal.md` §2).

- **Objet** : `Confirmation : diagnostic complet de {prenom}`
- **Préheader** : `Voici comment ça se passe.`

> Bonjour,
>
> Merci. Votre paiement de **19,00 €** pour le **diagnostic complet de maths (3e)** de {prenom} est bien reçu (réf. {stripe_session_court}, le {date_achat}).
>
> **Comment ça se passe**
> 1. {prenom} ouvre Matheux : le diagnostic complet l'attend, en 3 parties d'environ 15 minutes.
> 2. On peut s'arrêter entre deux parties et reprendre plus tard.
> 3. À la fin, vous recevez par email le bilan PDF.
> [ Ouvrir Matheux ] `{lien_app}`
>
> **Garantie 30 jours** : jusqu'au {date_achat + 30 j}, un simple email à contact@matheux.fr suffit pour être remboursé intégralement.
>
> **Informations légales** : lors de votre commande, le {date_consentement} à {heure}, vous avez demandé l'accès immédiat au diagnostic et reconnu qu'en conséquence vous perdiez votre droit de rétractation légal de 14 jours dès le début du diagnostic. Cela ne change rien à la garantie de 30 jours ci-dessus. CGV applicables : `https://matheux.fr/cgv.html` (version du {version_cgv}). Vendeur : Nicolas Follezou, EI, SIRET 837 763 713 00059. TVA non applicable, art. 293 B du CGI.
> Nicolas

### A-ACH1 — C'est parti · `D3:A-ACH1` · P
**Condition** : `email_eleve`.
- **Objet** : `Ton diagnostic complet est débloqué`
- **Corps** : « Salut {prenom}, ton diagnostic complet est prêt : 3 parties d'environ 15 min, tu peux faire une pause entre chaque. À la fin, tu verras ta carte en entier. [ Commencer la partie 1 → ] »

### A-MOD / P-MOD — Diagnostic complet non terminé · `D3:A-MOD`, `D3:P-MOD` · P
- **A-MOD** (J+2 après l'achat, si le diagnostic n'est pas terminé) : objet `Il te reste {n_modules_restants} partie(s) sur 3`. Corps : « Tu en es à {n_modules_faits}/3. La prochaine partie prend environ 15 min, et ensuite ta carte complète s'affiche. [ Reprendre → ] »
- **P-MOD** (J+5, si le diagnostic n'est toujours pas terminé) : objet `Le diagnostic de {prenom} est à {n_modules_faits}/3`. Corps : « Il reste {n_modules_restants} partie(s) d'environ 15 minutes. Le bilan PDF arrive dès la fin. Si quelque chose bloque, répondez-moi. *Et si finalement ce n'est pas le moment, je peux vous rembourser : il suffit de me le demander.* »
- 1 seul envoi de chaque.

---

### P-PDF — Le bilan est prêt · `D3:P-PDF` · T

- **Objet** : `Le bilan maths de {prenom} est prêt`
- **Préheader** : `{n_lacunes} priorité(s), {n_points_forts} point(s) fort(s), et un plan de 4 semaines.`

> Bonjour,
>
> {prenom} a terminé son diagnostic complet ({duree_min} minutes, {n_questions} questions). Voici son bilan :
> [ Télécharger le bilan PDF ] `{lien_pdf}` *(ou en pièce jointe, ❓ question)*
>
> **L'essentiel en 3 lignes**
> - Points forts : {points_forts_parent_2}
> - Priorité n° 1 : **{priorite_1_parent}** *{si cause_racine}* (elle en débloque {n_bloque} autres)
> - Le plan des 4 prochaines semaines est en page {page_plan}.
>
> Mon conseil : prenez 5 minutes pour lire la page 1 avec {prenom}. Ce sont souvent des découvertes pour les deux.
> Nicolas

Pas d'offre dans cet email. On laisse la valeur parler.

### A-PDF — Ta carte complète · `D3:A-PDF` · P
- **Objet** : `Ta carte complète est là, {prenom}`
- **Corps** : « Tu as tout fini, bravo 👏 Ta carte est complète. Tes points forts : {points_forts_eleve_2}. Ta priorité n° 1 : **{priorite_1_eleve}**, et tes exos du jour sont déjà dessus. [ Voir ma carte → ] »

### P-UP1 — Utiliser le plan · `D3:P-UP1` · M · J+3 après le PDF

**Condition** : pas de programme, opt-in.
- **Objet** : `Comment utiliser le plan de 4 semaines de {prenom}`
- **Préheader** : `Même sans rien acheter de plus.`

> Bonjour,
>
> Le bilan de {prenom} contient un plan de 4 semaines. Voici comment l'utiliser :
> - **Semaine 1** : {plan_s1_objectif}. Les 5 exercices gratuits du jour sont déjà réglés dessus.
> - **Ensuite** : suivez l'ordre du plan. Il commence par les causes racines, parce que c'est ce qui débloque le reste.
> - **Le bon rythme** : 5 jours sur 7, 10 minutes. Pas plus.
>
> Le **Programme Brevet** permet de travailler tout le plan en même temps (entraînement illimité), avec un re-diagnostic chaque mois pour voir la progression, et des brevets blancs. Comme vous avez déjà le diagnostic, il vous coûte **30 €** au lieu de 49 €, et cette déduction n'a pas de date limite.
> [ Passer au Programme Brevet — 30 € ] `{lien_upgrade}`
> Nicolas

### P-UP2 — Premiers effets · `D3:P-UP2` · M · J+10 après le PDF
**Condition** : pas de programme, opt-in, **au moins 3 jours actifs** depuis le PDF. Sinon, envoyer P-X2b adapté (usage) à la place.
- **Objet** : `{prenom} sur {priorite_1_parent} : où on en est`
- **Corps** : « En 10 jours, {prenom} a fait {n_exos} exercices sur sa priorité n° 1. *{si progrès}* Réussite au premier essai : de {maitrise_avant} % à {maitrise_apres} %. *{sinon}* Pas encore de progrès net : c'est une notion ancienne, et il faut compter 2 à 3 semaines. Dans 18 jours, {prenom} pourra faire un **re-test offert** pour mesurer l'évolution. Programme Brevet : 30 € (diagnostic déduit). [ lien ] »

### A-RT — Re-test offert · `D3:A-RT` · P · J+28 après le PDF
- **Objet** : `Prouve-le : 10 questions pour voir ce qui a bougé`
- **Corps** : « Ça fait 4 semaines. 10 questions sur tes 3 priorités, et on compare avec ton diagnostic. [ Faire le re-test → ] » + copie au parent si pas d'`email_eleve` (version vouvoiement, T).

### P-UP3 — Résultat du re-test · `D3:P-UP3` · M
**Déclencheur** : re-test fini. **Condition** : pas de programme, opt-in.
- **Objet** : `{prenom} : avant / après en 4 semaines`
- **Corps (progrès)** : « Sur ses 3 priorités : {priorite_1} {avant} % → {apres} % · {priorite_2} … Le Programme Brevet fait ce même point chaque mois, sur toute la carte. 30 €, diagnostic déduit. [ lien ] »
- **Corps (pas de progrès)** : « Les résultats n'ont pas encore bougé. Souvent, c'est un problème de régularité, parfois un exercice mal expliqué. Répondez-moi, on regarde ensemble. » **Aucun lien de paiement.**

---

### P-ACH2 — Confirmation Programme Brevet · `D3:P-ACH2` · T
- **Objet** : `Confirmation : Programme Brevet de {prenom}`
- **Corps** : montant ({49,00 € ou 30,00 €}), référence, date. Ce qui est inclus : entraînement illimité, re-diagnostic mensuel (1er week-end du mois), brevets blancs (janvier, avril, mai : dates annoncées dans l'app), bilan chaque dimanche. Garantie 30 jours. **Bloc légal** : ⚠️ selon la qualification retenue dans `52-legal.md` §2.2. Soit la renonciation (si contenu numérique), soit « Vous disposez de 14 jours pour vous rétracter ; si {prenom} a commencé à utiliser le programme à votre demande, un montant proportionnel pourra être retenu. En pratique, la garantie de 30 jours vous rembourse intégralement. » CGV + version, vendeur, TVA.

### A-ACH2 — Bienvenue dans le programme · `D3:A-ACH2` · P
- « Tout est débloqué, {prenom} : ta carte entière, sans limite d'exos. Rendez-vous le 1er week-end du mois pour ton re-diagnostic. »

### P-HEBDO — Bilan du dimanche · `D3:P-HEBDO:{AAAA-Www}` · P (programme uniquement)
- **Objet** : `La semaine de {prenom} : {n_exos_semaine} exos, {n_comp_vertes} compétence(s) passée(s) au vert`
- **Corps** : 5 lignes max. Exos et jours actifs · compétences passées au vert · prochaine priorité · date du prochain re-diagnostic ou brevet blanc. **Semaine à 0 exo** : 1 ligne « Pas d'entraînement cette semaine. Ça arrive. Le plus simple pour reprendre : 5 exos, 10 min. » **2 semaines à 0 exo de suite** : l'email hebdo est suspendu jusqu'à la reprise (on n'envoie pas « 0 » chaque dimanche).

### A-MENS — Re-diagnostic du mois · `D3:A-MENS:{AAAA-MM}` · P (programme)
- **Objet** : `Re-diagnostic du mois : ta carte va-t-elle virer au vert ?`
- **Corps** : « 15 min, et tu vois ce qui a bougé depuis le mois dernier. » Résultat → email parent `D3:P-MENS:{AAAA-MM}` (T/P) : avant/après par domaine.

---

### Saisonniers (M, parents non-acheteurs du programme, opt-in, 1 par période)

| Type | Quand | Objet | Idée du corps |
|---|---|---|---|
| `D3:S-DEC:2026` | 1re semaine de décembre | `Avant le bulletin : la carte maths de {prenom}` | Le 1er trimestre se termine. Voici ce que la carte dit, compétence par compétence. Lien vers le bilan. Offre en 1 ligne. |
| `D3:S-BB` | 21 jours avant `date_brevet_blanc` (si saisie par l'ado) | `Brevet blanc de {prenom} dans 3 semaines` | Plan de révision daté (gratuit, priorités de la carte). Programme en 1 ligne. |
| `D3:S-AVR:2027` | ~J-60 Brevet | `Brevet dans {semaines_brevet} semaines : les 3 priorités de {prenom}` | Les 3 priorités restantes, un planning. Offre en 1 ligne. |

**Aucun email marketing après le 15 mai 2027** (`50` §7).

---

## 3. Mapping avec l'existant

| Ancien | Devient |
|---|---|
| `templateJ0` (bienvenue, « exos demain matin », « bilan chaque semaine ») | **P-X0**. L'ancien promettait un bilan hebdo à tous : c'est désormais réservé au programme, donc à ne plus promettre. |
| `templateJ1` (« boost prêt ») | **A-X1** (à l'ado, s'il n'a rien fait) |
| `templateJ3` (check-in) | fusionné dans **P-X1** (J+2) / **P-X2b** |
| `templateJ7` (bilan + 29,99 €) | **P-X2** (J+6, chiffres réels) |
| `templateJ14` (nudge conversion) | **P-X3** (J+13, dernier message) |
| `cronSendEmails` (J+1/3/7/14 depuis `date_inscription`) | Cron conservé (1×/jour) mais **piloté par l'état** : pour chaque profil, calculer l'étape (dates d'événements : `diag_express_at`, `diag_paye_at`, `diag_complet_at`, `programme_at`, `consentement_parent_at`, `optin_marketing`), puis envoyer ce qui est dû. Les emails d'événement (P-X0, P-SH, P-ACH*, P-PDF) partent **immédiatement** depuis l'action concernée, pas depuis le cron. |
| `sendMarketingEmail` (check UNSUB + dédup) | Scindé en `sendEmail(cat, …)` : **T** ignore UNSUB, **P/M** le respectent. **M** exige en plus `optin_marketing` et le plafond. |
| Templates « Débloquer tous les chapitres », « 29,99 € » | **Supprimés** (produit disparu) |

**Champs à ajouter** (pour l'ingénieur adaptatif, schéma à documenter dans `database.md` / `schema.sql`) : `profiles.email_eleve`, `consentement_parent_at`, `optin_marketing` (bool) + `optin_marketing_at`, `date_brevet_blanc`, et les dates d'événements ci-dessus. Ou alors les dériver de `funnel_events` (`50` §8), qui est plus simple : pas de colonne par événement.

---

## 4. Plafonds, horaires, arrêts

| Règle | Parent | Ado |
|---|---|---|
| Max M | **1 par 72 h**, **5 max sur les 30 premiers jours**, puis saisonniers seulement (≤ 3/an) | **0, jamais** |
| Max P | 1/jour | **3/semaine**, jamais 2 le même jour |
| Heure d'envoi (cron) | 17h-19h Paris, idéalement ❓ | 17h Paris (après les cours). Jamais entre 20h et 8h. |
| Pas de rappel d'usage si… | — | l'ado a déjà fait des exos aujourd'hui |
| Arrêt immédiat | UNSUB (P+M), achat (branche conversion concernée), compte supprimé, pas de confirmation parentale à J+30 | UNSUB, compte supprimé, parent a retiré son accord |
| Weekend | Samedi : rien, sauf A-MENS. Dimanche : P-HEBDO seulement. | idem |

Cron : un seul job quotidien, **déplacé de 9h à 17h Paris** (`0 15 * * *` UTC en été, `0 16 * * *` en hiver : pg_cron est en UTC, soit on accepte une heure de décalage, soit on le règle 2 fois par an ❓). Le plafond se vérifie **avant chaque envoi** par une requête `email_logs` sur les 72 dernières heures (type LIKE `D3:%`, catégorie M).

---

## 5. Compatibilité `email_logs` / dédup / désinscription

`email_logs` (non documentée dans `schema.sql`, colonnes lues dans `index.ts` : `email, prenom, type, statut, details, created_at`). **À documenter** par l'ingénieur adaptatif (règle CLAUDE.md « schéma »).

| Besoin | Solution |
|---|---|
| Dédup | Inchangée : `(email, type, statut='envoyé')`. Les types récurrents portent leur période dans le `type` (`D3:P-HEBDO:2026-W41`, `D3:A-MENS:2026-11`, `D3:P-SH:{token}`), donc la dédup reste une égalité simple. |
| Catégorie (plafond M) | Ajouter la colonne `categorie` (`T`/`P`/`M`), ou encoder dans le type (`D3:M:P-X1`). Reco : **colonne** (plus lisible pour Nicolas). |
| Lien au profil | Ajouter `code` (nullable). Aujourd'hui, on ne relie que par email. Or l'ado et le parent ont 2 adresses. |
| Désinscription | Existant : ligne `type='UNSUB'` par email. **Conservé**, par adresse : désinscrire le parent ne désinscrit pas l'ado, et inversement. T ignore UNSUB. |
| Lien de désinscription | Aujourd'hui `unsubscribe?email=…` en clair : n'importe qui peut désinscrire n'importe qui. Reco : ajouter `&k=HMAC(email)` et vérifier côté API. Faible priorité, mais simple. |
| En-têtes | Ajouter `List-Unsubscribe` + `List-Unsubscribe-Post: List-Unsubscribe=One-Click` via Resend (`headers`) sur P et M. Gmail et Yahoo l'attendent des expéditeurs en volume ; ici c'est une bonne pratique qui aide la délivrabilité. |
| Pied de page | P/M : lien « Se désinscrire » (existant) + « Vous recevez cet email car {prenom} utilise Matheux avec votre adresse. » T : pas de lien de désinscription, mais la même phrase d'origine. |
| Test | `send_test_email` doit accepter les nouveaux types (`type` au lieu de `day`). |

---

## ❓ Questions pour Nicolas

1. **Double confirmation parentale (P-X0) avec suppression du compte à J+30 sans confirmation ?** → Reco : **confirmation oui, sans jamais bloquer l'ado pendant 30 jours.** Suppression à J+30 : oui (c'est la preuve de consentement la plus propre, `52-legal.md` §4).
2. **Collecter un email ado facultatif ?** → Reco : **oui, facultatif**, et utilisé seulement après la confirmation parentale.
3. **Signature des emails ado : « Nicolas, de Matheux » ou « L'équipe Matheux » ?** → Reco : **« Nicolas, de Matheux »** (cohérent avec le côté humain, et vrai).
4. **PDF en pièce jointe ou en lien ?** → Reco : **lien signé, valable 30 jours**, régénérable depuis l'app (pas de données de mineur qui dorment dans les boîtes mail pour toujours).
5. **Cron à 17h Paris au lieu de 9h ?** → Reco : **oui**, avec 1 h de décalage accepté au changement d'heure.
6. **Aucun email marketing aux gratuits après le 15 mai ?** → Reco : **oui**.
