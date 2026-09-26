# 53 — Audit de la séquence email (état réel, 26/09/2026)

> Agent : growth-cro · 26/09/2026 · Branche `feat/diagnostic-3e`
> Méthode : lecture d'`index.ts` (planificateur `mxPlanEmails`, `mxContenuD3`, `mxEmailBilanExpress`,
> `mxEmailsAchat`, `mxEmailsBilanComplet`, `sendShareEmail`, `mxEnvoyerEmail`, `emailWrap`), **simulation de
> 30 jours** sur un backend de dev privé (4 profils créés par l'API + les 3 comptes du seed, cron chaque jour,
> `/dev/time`), puis contrôle DNS avec `dig`. Script de simulation : hors dépôt (scratchpad), reproductible
> avec `dev/smoke_test.ts` qui fait la même chose sur 15 jours.
> Liés : `51-emails.md` (séquence en place, mise à jour), `50-offre-conversion.md`, `52-legal.md`.

---

## 1. Frise : ce qui part réellement (simulation du 26/09 au 26/10)

Profils : **Alice** (invitée → inscrite, confirmation + opt-in, s'entraîne 7 jours, n'achète rien) ·
**Bruno** (invité → inscrit, ne confirme pas, ne revient jamais) · **Chloé** (confirmation + opt-in, achète le
diagnostic à J+1, le finit à J+3, s'entraîne) · **David** (confirmation + opt-in, achète le Programme à J+2, finit
le diagnostic à J+4). Tous ont une adresse ado, sauf Bruno. J0 = samedi 26/09 : le samedi, seul `A-MENS` part,
et le dimanche seul `P-HEBDO`, ce qui décale au lundi ce qui tombe le week-end.

| Jour | Qui (dest.) | Type · cat. | Objet | But | Déclencheur |
|---|---|---|---|---|---|
| J0 | les 4 parents | P-X0 · T | Le bilan maths d'Alice (et une confirmation à faire) | Confirmation parentale + restitution du diagnostic express | Fin du diag express avec un compte (ou `register` qui rattache le diag invité) |
| J1 | Chloé parent (payeur) | P-ACH1 · T | Confirmation : diagnostic complet de Chloe | Confirmation légale (support durable, renonciation) | Webhook Stripe `diag_complet` |
| J1 | Chloé ado | A-ACH1 · P | Ton diagnostic complet est débloqué | Faire démarrer le diag complet | Idem (si adresse ado + accord parent) |
| J2 | David parent | P-ACH2 · T | Confirmation : Programme Brevet de David | Confirmation légale | Webhook `programme_brevet` |
| J2 | David ado | A-ACH2 · P | Bienvenue dans le Programme Brevet | Accueil | Idem |
| J2 | Alice parent | P-X1 · M | Ce que le diagnostic express ne dit pas encore sur Alice | Expliquer le diag complet (19 €, garantie) | Cron, express +2 à +5 j, point fragile, opt-in |
| J2 | Alice ado | A-X0 · P | Ta carte de maths est prête, Alice | Premier entraînement | Cron, express +0 à +3 j, pas d'achat |
| J3 | Chloé parent | P-PDF · T | Le bilan maths de Chloe est prêt | Restitution du diag complet | Fin du diag complet |
| J3 | Chloé ado | A-PDF · P | Ta carte complète est là, Chloe | Restitution ado | Idem |
| J3 | Bruno parent | P-X0R1 · T | Rappel : l'espace maths de Bruno attend votre accord | Obtenir la confirmation | Cron, ≥ 3 j après P-X0, pas de confirmation, pas d'achat |
| J4 | David parent / ado | P-PDF · T / A-PDF · P | Le bilan maths de David est prêt / Ta carte complète est là | Restitution | Fin du diag complet |
| J6 | Alice parent | P-X2 · M | La première semaine d'Alice en maths | Chiffres réels de la semaine + mention du complet | Cron, express +6 à +11 j, ≥ 2 jours actifs |
| J6 | Bruno parent | P-X2b · P | Bruno n'a pas encore repris ses exercices | Relancer l'usage (sans vente) | Cron, express +6 à +11 j, ≤ 1 jour actif |
| J6 | Chloé parent | P-UP1 · M | Comment utiliser le plan de 4 semaines de Chloe | Utiliser le plan + upsell 30 € | Cron, complet +3 à +6 j |
| J8, 15, 22, 29 | David parent | P-HEBDO · P | La semaine de David : 20 exercices | Suivi hebdo (promesse du programme) | Dimanche, programme ≥ 3 j, activité < 14 j |
| J13 | Alice parent | P-X3 · M | Je ne vous relancerai plus sur le diagnostic | Dernière relance + « qu'est-ce qui vous a retenu ? » | Cron, express +13 à +20 j, P-X1 ou P-X2 parti |
| J13 | Chloé parent | P-UP2 · M | Chloe et sa priorité n° 1 : où on en est | Progrès mesurés + upsell 30 € | Cron, complet +10 à +15 j, ≥ 3 jours actifs |
| J20 | Bruno parent | P-X0R2 · T | Rappel : l'espace maths de Bruno attend votre accord | 2e et dernier rappel | Cron, ≥ 3 j après R1, inscription +20 à +29 j |
| — | Lina (seed, sans diag) | P-X0N · T puis R1, R2 | L'espace maths de Lina : une confirmation à faire | Confirmation sans diagnostic | Cron, inscription +1 à +29 j |
| à la demande | parent ou proche | P-SH · T | Tom vous a envoyé son bilan de maths | Partage de la carte par l'ado | Action `send_share_email` (3/24 h, respecte UNSUB) |

**Volumes sur 30 jours** : Alice parent 4 (dont 3 M), ado 1 · Bruno 4 (3 T + 1 P) · Chloé parent 5 (2 M), ado 2 ·
David parent 3 + 4 hebdos, ado 2. Aucun jour avec 2 emails de séquence à la même adresse. Pas de commercial à
moins de 72 h d'un autre. Rien au-delà de J+20 pour un non-acheteur.

---

## 2. Audit

### 2.1 Au niveau de la séquence

| Critère | Verdict | Détail |
|---|---|---|
| Pilotée par les événements | ✅ | Achat, fin de diagnostic et partage partent tout de suite ; le reste dépend de l'état (achat, activité, confirmation) et non plus du calendrier seul. |
| Deux audiences | ✅ | Parent : vouvoiement, signé « Nicolas, Fondateur de Matheux ». Ado : tutoiement, « Nicolas, de Matheux », jamais de prix (vérifié par le smoke test). |
| Opt-in commercial | ✅ (corrigé) | M exige l'opt-in, et désormais **aussi la confirmation parentale**, voir §3 et le P0 du §4. |
| Arrêt après achat | ✅ | P-X1/X2/X3 s'arrêtent dès le 1er achat ; P-UP* ne partent jamais à un client du programme. |
| Fatigue | ✅ | 1 email/jour/parent, M : 72 h d'écart et 5 sur 30 jours, pause du 15/05 au 31/08, ado : 3 par semaine. Rien le week-end, sauf l'hebdo (dimanche) et `A-MENS` (1er samedi). |
| Cohérence avec l'état réel | ⚠️ → ✅ | 2 défauts vus en simulation et corrigés : rappels « attend votre accord » envoyés à un **client du programme** ; « Ta carte est prête » envoyé à l'ado **après** « Ton diagnostic complet est débloqué ». |
| Emails ado | 🔴 inopérants | `email_eleve` n'est **jamais demandé dans l'interface** (`set_preferences` n'est appelé ni par `app.html` ni par `bilan.html`). En prod, **aucun email A-\* ne part**. La page de confirmation n'a pas non plus la case « j'autorise Matheux à écrire à {prenom} » (`52` §4.2). |
| Mesure | 🔴 | Les CTA portent `?src=email_{type}`, mais personne ne lit ce paramètre : impossible de savoir quel email fait cliquer ou acheter. |

### 2.2 Email par email

Légende : ✅ bon · ⚠️ à améliorer · 🔧 corrigé dans ce passage.

| Email | Objectif / CTA | Objet · préheader | Personnalisation | Remarques |
|---|---|---|---|---|
| **P-X0** | Confirmer (1 bouton) ; le bilan est devenu un lien secondaire 🔧 | 56 car. ✅ ; préheader « 5 à travailler » sans nom 🔧 → « 5 domaines à travailler » | Prénom, point fragile, erreur type, cause racine ✅ ; « de Alice » 🔧 → « d'Alice » ; « 6 compétences sur **49** » alors que P-X1 dit « sur **46** » 🔧 (même calcul partout) ; « point le plus fragile » affiché même quand il est acquis 🔧 | Respectait la désinscription alors que ses rappels (T) l'ignorent : un parent désinscrit ne pouvait plus confirmer 🔧. Dédup par adresse seule : un compte recréé avec la même adresse ne recevait jamais P-X0 🔧 (dédup par élève). ⚠️ Lien vers la page bilan, qui porte l'offre : à faire valider (`52` §7). |
| **P-X0N / R1 / R2** | Confirmer ✅ | ✅ | Prénom ✅ | Partaient aussi aux **acheteurs** jamais confirmés (vu : Sarah, programme payé, 2 rappels) 🔧. ⚠️ Aucun email ne dit ce qui se passe sans confirmation : c'est cohérent tant que la suppression à J+30 n'est pas codée. |
| **P-X1** · M | Page bilan (offre + cases légales avant Stripe) ✅ | 56 car. ✅ | Point fragile, compétences restantes ✅ | Ancrage prix et garantie honnêtes ✅. Mots « gratuits / remboursé / 19 € » : risque spam faible avec DKIM et DMARC en place. |
| **P-X2** · M | ✅ | Chiffres réels dans le préheader ✅ | Exos, jours, évolution de maîtrise ✅ | « C'est normal sur **une notion ancienne** » affiché même pour une notion de 3e (inexact) 🔧 : dit « notion de 5e » seulement quand c'est le cas. |
| **P-X2b / P-UP2b** · P | Ouvrir l'app ✅ | ✅ | ⚠️ « il y a une semaine / 10 jours » en dur, alors que l'envoi peut glisser 🔧 (délai réel). | ⚠️ Part aussi à une adresse **non confirmée** (Bruno). Ça dévoile qu'un mineur ne s'entraîne pas à une adresse que personne n'a validée. Reco §4, non fait (le smoke test attend l'envoi). |
| **P-X3** · M | Page bilan + 5 raisons en `mailto` ✅ | « Je ne vous relancerai plus… » : objet fort, honnête ✅ | ✅ | Promesse tenue par le code : plus aucune relance ensuite. ⚠️ Les raisons ne sont pas enregistrées (spec : 1 clic → `funnel_events`). |
| **P-MOD** · P | ✅ | ✅ | Parties faites/restantes ✅ | Propose le remboursement : honnête ✅ |
| **P-UP1** · M | Page bilan ✅ | ✅ | Objectif de la semaine 1 ✅ | Utile même sans achat ✅ |
| **P-UP2** · M | ✅ | Objet de ~100 caractères avec le titre de la compétence 🔧 → « Chloe et sa priorité n° 1 : où on en est », titre dans le préheader | Exos, maîtrise avant/après ✅ | « notion ancienne » 🔧 |
| **P-HEBDO** · P | Ouvrir l'app ✅ | Objet « **0 exercice** » en semaine creuse 🔧 → « La semaine de David sur Matheux » | ✅ ; phrase d'introduction ajoutée 🔧 | ⚠️ Le parent n'a pas de compte : « Ouvrir Matheux » le mène à l'écran de connexion de l'ado. Mieux : lien vers la page bilan. |
| **P-ACH1 / P-ACH2** · T | ✅ | ✅ | Montant, référence, date, heure du consentement, version des CGV ✅ | Bloc légal complet ✅. ⚠️ Texte de rétractation du programme à faire valider (`52` §2.2). ⚠️ Même remarque « Ouvrir Matheux » pour le parent. |
| **P-PDF** · T | Page bilan ✅ | Préheader promettait « les points forts » même sans point fort 🔧 | Priorité n° 1, cause racine ✅ ; « 1 minutes » 🔧 (pluriel, durée masquée sous 5 min) | Pas d'offre ✅. ⚠️ Part à `profiles.email`, alors que P-ACH part au payeur : si les adresses diffèrent, le payeur ne reçoit pas le bilan. |
| **P-SH** · T | ✅ | ✅ | ✅ | Respecte la désinscription, 3 envois par 24 h, aucun prix ✅ |
| **A-X0 / A-X1 / A-MOD / A-MENS / A-ACH / A-PDF** | 1 CTA ✅ | Virgule en trop sans prénom (« …prête, ») 🔧 ; A-PDF annonçait « tes points forts » sans point fort 🔧 | ✅ | Ton ado juste, pas de prix ✅. A-X0 cadré : ≤ 3 j, jamais après un achat 🔧. Mais aucun ne part en prod (§2.1). |

### 2.3 Forme, mobile, délivrabilité

| Point | Avant | Maintenant |
|---|---|---|
| Structure HTML | Fragment sans `<html>` | 🔧 `<!doctype html><html lang="fr">`, viewport, `color-scheme: light` (évite l'inversion sauvage des couleurs en mode sombre) |
| Préheader | Bourrage d'espaces : Gmail pouvait afficher le début du corps après lui | 🔧 bourrage `&zwnj;&nbsp;` ×60 |
| Version texte | HTML seul | 🔧 partie `text` générée (liens « libellé : url »), `multipart/alternative` |
| Mobile | Table 520 px, `max-width:100%`, 16 px, boutons 14×32 px ✅ | inchangé |
| Liens / texte | 1-2 liens + désinscription, ratio sain ✅ | inchangé |
| List-Unsubscribe | P et M : one-click signé (RFC 8058) + mailto ✅ | inchangé |
| Lien de désinscription | Signé HMAC ✅, par adresse ✅ | inchangé |
| Identité de l'expéditeur | « Matheux · matheux.fr » | 🔧 « Matheux (Nicolas Follezou EI) · matheux.fr » avec lien vers les mentions légales (L34-5 CPCE, LCEN art. 20). Pas d'adresse postale : elle n'est pas exigée dans un email en France, et elle est déjà dans les mentions légales. |
| Expéditeur | `Matheux <no-reply@matheux.fr>` + reply-to `contact@` | ⚠️ non changé (§4) : « no-reply » contredit « Répondez-moi, c'est moi qui lis » |

**DNS de matheux.fr (`dig`, 26/09)**

| Enregistrement | Valeur | Verdict |
|---|---|---|
| SPF racine | `v=spf1 include:_spf-eu.ionos.com ~all` | ✅ pour la messagerie IONOS (contact@) |
| SPF `send.matheux.fr` (Return-Path Resend) | `v=spf1 include:amazonses.com ~all` + MX `feedback-smtp.eu-west-1.amazonses.com` | ✅ aligné en mode relâché |
| DKIM `resend._domainkey` | clé RSA 1024 bits, **avec des espaces au milieu de la valeur** | ✅ toléré (la RFC 6376 autorise les espaces), mais à recoller proprement depuis Resend par sécurité |
| DMARC `_dmarc` | **CNAME vers `dmarc.ionos.fr`** = `v=DMARC1; p=none;` (enregistrement générique IONOS, sans `rua`) | ⚠️ aucun rapport, aucune politique propre. À remplacer (§5) |
| MX racine | IONOS (mx00/mx01) | ✅ : `contact@` peut recevoir. Vérifier que la boîte existe et qu'elle est lue. |
| BIMI, MTA-STS | absents | sans objet à ce volume |

### 2.4 Légal

| Point | Verdict |
|---|---|
| Opt-in commercial du parent (L34-5) | ✅ case non cochée sur `bilan.html?confirmer=1`, journalisée dans `consentements` ; M le vérifie. 🔴 Voir P0 : l'ado peut le poser lui-même. |
| Pas d'incitation de l'ado à acheter | ✅ aucun prix, aucun lien `/b/` ni Stripe dans les emails A-\* (testé) |
| Aucun email ado avant l'accord parental | ✅ cron et emails d'événement vérifient `consentement_parent_at` |
| Transactionnel sans offre | ✅ P-ACH, P-PDF, P-SH. ⚠️ P-X0 renvoie vers une page qui porte l'offre (à valider) |
| Mentions dans P/M | ✅ expéditeur, origine de l'adresse, désinscription |
| Confirmation d'achat sur support durable (L221-13) | ✅ P-ACH1/2 : produit, prix, date, heure de la renonciation, version des CGV, vendeur, TVA |
| Durées de conservation (`52` §5 : `email_logs` 3 ans) | ⚠️ aucune purge codée |
| Suppression à J+30 sans confirmation, avertissement avant suppression à 12 mois | ⚠️ non codés. Les emails ne les promettent plus, donc rien de faux n'est écrit. Mais la CGU proposée (`52` §8) les annonce. |

---

## 3. Corrections faites (templates et logique email uniquement)

Fichiers : `supabase/functions/api/index.ts` (fonctions email) et `supabase/tests/emails_test.ts`.
`deno check` OK · `deno test -A supabase/tests/` : 25 OK · `dev/smoke_test.ts` : 126 OK, 0 KO.

1. **Planificateur** (`mxPlanEmails`)
   - Plus de P-X0N / R1 / R2 après un achat : le payeur a déclaré être le représentant légal.
   - Les emails **M** exigent l'opt-in **et** la confirmation parentale. C'est une ceinture de sécurité contre un opt-in posé depuis la session de l'ado.
   - **A-X0** : dans les 3 jours après le diagnostic express seulement, et jamais après un achat.
2. **Dédup par élève** : `mxEnvoyerEmail`, `mxEmailBilanExpress` et les logs lus par `mxEmailContexte` filtrent sur `code`. Un compte recréé avec la même adresse repart de zéro. UNSUB reste par adresse.
3. **P-X0** : il ignore UNSUB, comme les autres emails T. Il utilise le même résumé que la séquence (`mxResumeCarte` : mêmes totaux, point fragile seulement s'il est réellement fragile). Un seul bouton ; `src=email_P-X0`.
4. **Textes** : élision `mxDe()` (d'Alice, d'Hugo, de Yanis) sur tous les objets et corps parent. Résumé « 5 domaines à travailler ». « Notion ancienne » réservé aux vraies notions d'avant la 3e (P-X2, P-UP2). Délai réel dans P-X2b/P-UP2b. P-HEBDO sans « 0 exercice ». P-UP2 : objet court. P-PDF et A-PDF : préheader fidèle au contenu, durée au pluriel. A-X0 et A-PDF : plus de virgule pendante.
5. **Layout** : document HTML complet (`lang`, viewport, thème clair), préheader étanche, version texte, identité légale dans le pied.
6. **Tests ajoutés** : acheteur non confirmé (pas de rappel), opt-in sans confirmation (pas de M), A-X0 (pas après un achat, pas après 3 jours), élision. Les invariants du fuzz (300 élèves) couvrent aussi ces 3 règles.

---

## 4. Recommandations priorisées (non implémentées)

| Prio | Quoi | Pourquoi | Qui |
|---|---|---|---|
| **P0** | Retirer `optin_marketing` et `consentement_parent` de `set_preferences` (seul `confirm_parent`, depuis le lien reçu par le parent, doit pouvoir les poser) | Aujourd'hui l'ado connecté peut « confirmer » à la place de son parent et s'inscrire aux offres. Ma correction du §3 bloque les M sans confirmation, mais la confirmation se pose par le même trou. | QA / ingénieur (hors fonctions email) |
| **P1** | Collecter `email_eleve` (facultatif) sur la page de confirmation parent, avec la case d'autorisation `52` §4.2 | Sans ça, les 8 emails ado sont du code mort | dev-ux + ingénieur |
| **P1** | Lire `?src=email_*` dans `app.html` et `bilan.html`, puis le logger dans `funnel_events` (`email_click`) | Sans ça, aucun KPI par email n'existe | dev-ux |
| **P1** | Webhook Stripe : poser `consentement_parent_at` (et une ligne `consentements` produit=achat) si vide | Un client qui ne confirme pas n'a aucun email ado et reste « non confirmé » (suppression J+30 à venir) | ingénieur |
| **P1** | DMARC propre + Google Postmaster Tools (§5) | Visibilité sur la délivrabilité, protection du domaine | Nicolas |
| **P2** | Expéditeur parent `Nicolas de Matheux <nicolas@matheux.fr>` (boîte IONOS réelle), reply-to identique | Cohérent avec « c'est moi qui lis » ; meilleure ouverture ; « no-reply » pénalise la confiance | Nicolas (boîte) + 1 ligne dans `resendSend` |
| **P2** | P-X2b / P-UP2b seulement si `consentement \|\| achat` | Ne pas écrire à une adresse non validée que « Bruno ne s'entraîne pas » | growth + mettre à jour le smoke test (Tom) |
| **P2** | « Ouvrir Matheux » dans les emails parent (P-HEBDO, P-ACH, P-MOD, P-X2b) → page bilan `/b/` du parent, ou texte « Demandez à {prenom} d'ouvrir Matheux » | Le parent n'a pas de session : il tombe sur l'écran de connexion de l'ado | growth |
| **P2** | P-PDF aussi au payeur si son adresse diffère de `profiles.email` | Celui qui a payé doit recevoir ce qu'il a acheté | growth |
| **P2** | Resend → webhook `email.bounced` / `email.complained` → ligne `UNSUB` (statut `bounce`/`plainte`) | Ne pas réécrire à une adresse morte ou plaignante (réputation) | ingénieur |
| **P2** | **S-DEC** « Avant le bulletin » (1re semaine de décembre, M, 1 email) | Seul moment saisonnier avant février : **à coder avant le 30/11** | growth |
| **P3** | Trous de séquence : **P-REPRISE** (1 fois, P, 7 jours sans exo après ≥ 3 jours actifs) ; **P-MOIS** mensuel sans prix pour les gratuits confirmés ; **P-MENS** (résultat du re-diag du programme au parent) ; **A-RT/P-UP3** (re-test J+28) ; **fin de programme** (bilan de l'année fin juin, pause de P-HEBDO en juillet-août) ; **P-REMB** (confirmation de remboursement, T) | Aujourd'hui, un gratuit actif n'a plus aucune nouvelle après J+13 ; un inactif réactivable est perdu | growth |
| **P3** | Purge `email_logs` > 3 ans (hors UNSUB), suppression J+30 non confirmé + email d'avertissement à 12 mois | Aligner le code sur la politique de confidentialité proposée | ingénieur |
| **P3** | P-X3 : raisons en 1 clic loggées (`funnel_events`) au lieu de `mailto` | Taux de réponse bien plus élevé | growth + ingénieur |

⚠️ **À faire relire par un professionnel** (juriste, droit de la consommation et RGPD des mineurs) : le lien vers l'offre depuis P-X0 (transactionnel), la clause de rétractation de P-ACH2 (qualification contenu numérique ou service), le fait de traiter l'achat comme une confirmation parentale, et le soft opt-in après achat (aujourd'hui non utilisé : on exige l'opt-in même chez les clients, ce qui est plus prudent).

---

## 5. Ce que Nicolas doit configurer

**DNS (IONOS)**
1. Supprimer le **CNAME** `_dmarc.matheux.fr → dmarc.ionos.fr` et créer un **TXT** `_dmarc` :
   `v=DMARC1; p=none; rua=mailto:dmarc@matheux.fr; adkim=r; aspf=r; fo=1`
   (créer l'alias `dmarc@` ou utiliser un service gratuit de lecture des rapports). Après 3-4 semaines de rapports propres : `p=quarantine`.
2. Dans Resend → Domains → matheux.fr : recopier la valeur DKIM (`resend._domainkey`) **sans espaces** et vérifier que le domaine reste « Verified ».
3. Test réel : envoyer `send_test_email` vers une adresse Gmail. Dans « Afficher l'original », on doit lire `SPF: PASS`, `DKIM: PASS`, `DMARC: PASS`. Faire aussi un test mail-tester.com (viser ≥ 9/10).

**Resend**
4. Laisser **désactivé** le suivi des ouvertures et des clics (réécriture des liens, pixels : inutile ici et intrusif pour des mineurs). La mesure passe par `src=` (§4 P1).
5. Webhooks bounce/complaint (quand l'ingénieur aura la route) ; surveiller dans le dashboard : bounce < 2 %, plaintes < 0,1 %.

**Boîtes**
6. Vérifier que `contact@matheux.fr` existe et est lue (reply-to de tous les emails, remboursements, P-X3). Option : créer `nicolas@matheux.fr` (§4 P2).

**Google Postmaster Tools**
7. Ajouter matheux.fr (vérification TXT) pour suivre la réputation du domaine et le taux de spam chez Gmail.

---

## 6. KPIs à suivre (une fois `src` loggé)

| KPI | Source | Repère |
|---|---|---|
| Taux de confirmation parentale à 7 j (P-X0 → `parent_confirm`) | `funnel_events` | > 50 % |
| Taux d'opt-in à la confirmation | `consentements` | suivre ; pas de cible (c'est un vrai choix) |
| Clic par email (`email_click` avec `src`) / envois (`email_logs`) | les deux | P-X0 > 30 %, P-X1 > 8 % |
| P-X1/P-X2/P-X3 → `checkout_click` → achat à 7 j | `funnel_events`, `achats` | à mesurer, puis optimiser l'objet de P-X1 en premier |
| P-X2b → reprise de l'entraînement sous 3 jours | `reponses_items` | > 25 % |
| Désinscription par type | `email_logs` UNSUB après envoi | < 0,5 % par envoi ; au-delà, revoir le message |
| Bounce / plaintes | Resend, Postmaster | < 2 % / < 0,1 % |
| Raisons P-X3 | boîte contact@ | lecture qualitative mensuelle |

---

## ❓ Pour Nicolas

1. **P0 sécurité/légal** : on retire l'opt-in et la confirmation parentale de `set_preferences` ? → **Reco : oui, tout de suite** (un autre agent, hors fonctions email).
2. **Expéditeur** « Nicolas de Matheux <nicolas@matheux.fr> » au lieu de no-reply ? → **Reco : oui** (il faut créer la boîte IONOS).
3. **DMARC** : tu remplaces le CNAME IONOS par notre TXT avec `rua` ? → **Reco : oui, 5 minutes dans IONOS.**
4. **Achat = confirmation parentale** (le payeur déclare être le représentant légal) ? → **Reco : oui**, à faire valider par un juriste.
5. **S-DEC** (1 email début décembre aux parents opt-in non clients) : je le prépare pour fin novembre ? → **Reco : oui.**
