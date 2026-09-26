# 51 — Séquence emails déclenchée par le diagnostic (état en place)

> Agent : growth-cro · créé le 24/09/2026 (proposition) · **mis à jour le 26/09/2026 : décrit la séquence
> réellement codée** dans `supabase/functions/api/index.ts`. Audit, frise simulée sur 30 jours, DNS et
> recommandations : `53-audit-emails.md`.
> Le texte exact de chaque email est dans le code (`templateBilanExpressParent`, `mxContenuD3`, `mxEmailsAchat`,
> `mxEmailsBilanComplet`, `sendShareEmail`). Ce document décrit les règles, pas la copie mot à mot.
> Liés : `50-offre-conversion.md` (offre, interdits), `52-legal.md` (consentements, prospection).

---

## 0. Principes (en vigueur)

1. **Événements d'abord.** Achat, fin de diagnostic et partage partent immédiatement depuis l'action concernée. Le reste est calculé chaque jour par un planificateur **pur** (`mxPlanEmails`) à partir de l'état de l'élève (dates, activité, confirmation, opt-in, emails déjà partis).
2. **Deux audiences, deux adresses.**
   - **Parent** (`profiles.email`) : vouvoiement, signé « Nicolas · Fondateur de Matheux ». **Seul destinataire d'offres.**
   - **Ado** (`profiles.email_eleve`, facultatif) : tutoiement, signé « Nicolas, de Matheux », pédagogique uniquement. **Jamais de prix, jamais de lien de paiement ni de page bilan.** Rien ne part à l'ado sans `consentement_parent_at`. ⚠️ L'interface ne demande pas encore cette adresse : en prod, aucun email ado ne part (`53` §4).
3. **Trois catégories** (`email_logs.categorie`) :

| Cat. | Contenu | Désinscription (UNSUB) | Condition |
|---|---|---|---|
| **T** transactionnel | confirmation parentale et rappels, confirmation d'achat, bilan prêt, partage demandé par l'ado | ignorée (sauf P-SH, qui la respecte car l'adresse est libre) | aucune ; pas d'offre dans le corps |
| **P** pédagogique | relance d'usage, modules, bilan hebdo, emails ado | respectée | — |
| **M** commercial | P-X1, P-X2, P-X3, P-UP1, P-UP2 | respectée | **opt-in du parent ET confirmation parentale**, plafonds §4 |

4. **Honnêteté** : tout chiffre vient de la carte, de `reponses_items`, de `maitrise` ou de `MX_PRODUITS`. Une phrase sans donnée saute (l'email ne part pas si la donnée clé manque). Aucune phrase ne dit qu'un humain « analyse ». « Notion ancienne » seulement pour une notion d'avant la 3e.
5. **Personnalisation** : prénom avec élision (`mxDe` : « d'Alice », « de Léo »), point fragile, erreur type, cause racine, priorité n° 1, objectif de la semaine 1, maîtrise avant/après (arrondie à 5, affichée seulement si ≥ 3 exos et + 10 points).

---

## 1. Séquence en place

Notation : `J` = jours depuis l'événement de référence. Types `D3:<type>` dans `email_logs`.

### Emails d'événement (immédiats)

| Type | Dest. · cat. | Déclencheur | Condition | Contenu |
|---|---|---|---|---|
| **P-X0** | parent · T | fin du diag express avec un compte, ou `register` qui rattache un diag invité fini | 1 par élève | Bouton « Je confirme l'inscription » (lien `/b/<token>?confirmer=1`, avec l'opt-in facultatif sur la page) ; résumé de la carte, point fragile, cause racine ; lien secondaire vers le bilan ; aucun prix |
| **P-ACH1 / P-ACH2** | payeur · T | webhook Stripe | 1 par élève | Montant, référence, date, contenu, garantie 30 j (date limite), bloc légal (renonciation horodatée ou rétractation), version des CGV, vendeur, TVA |
| **A-ACH1 / A-ACH2** | ado · P | idem | adresse ado + accord parental | « Ton diagnostic complet est débloqué » / « Bienvenue dans le Programme Brevet » |
| **P-PDF** | parent · T | fin du diagnostic complet | — | Lien vers le bilan, priorité n° 1 (+ cause racine), points forts s'il y en a, où télécharger le PDF ; aucune offre |
| **A-PDF** | ado · P | idem | adresse ado + accord | Carte complète, priorité n° 1 |
| **P-SH:{token}** | adresse choisie par l'ado · T | `send_share_email` | 3 envois par 24 h et par élève, 1 par adresse et par 24 h, respecte UNSUB | Lien de partage (30 j), version courte si P-X0 reçu dans les 24 h ; aucun prix |

### Emails du cron (1×/jour, `0 15 * * *` UTC = 17 h Paris l'été, 16 h l'hiver)

| Type | Dest. · cat. | Fenêtre | Condition |
|---|---|---|---|
| **P-X0N** | parent · T | inscription +1 à +29 j | pas de diag express, pas de confirmation, **pas d'achat**, P-X0 non parti |
| **P-X0R1** | parent · T | ≥ 3 j après P-X0/P-X0N, inscription ≤ +19 j | pas de confirmation, **pas d'achat** |
| **P-X0R2** | parent · T | ≥ 3 j après R1, inscription +20 à +29 j | idem (2 rappels max) |
| **P-X1** · M | parent | express +2 à +5 j | pas d'achat, point fragile, inscription ≤ 30 j |
| **P-X2** · M | parent | express +6 à +11 j | pas d'achat, ≥ 2 jours actifs, pas de P-X2b |
| **P-X2b** · P | parent | express +6 à +11 j | pas d'achat, ≤ 1 jour actif, pas de P-X2 |
| **P-X3** · M | parent | express +13 à +20 j | pas d'achat, P-X1 ou P-X2 parti. **Dernière relance de conversion.** |
| **P-MOD** · P | parent | achat +5 à +9 j | diag complet non terminé |
| **P-UP1** · M | parent | complet +3 à +6 j | pas de programme |
| **P-UP2** · M | parent | complet +10 à +15 j | pas de programme, ≥ 3 jours actifs depuis le complet |
| **P-UP2b** · P | parent | complet +10 à +15 j | pas de programme, < 3 jours actifs |
| **P-HEBDO:{AAAA-Www}** · P | parent | chaque **dimanche** | programme depuis ≥ 3 j, au moins 1 jour actif sur 14 j (sinon suspendu) |
| **A-X0** · P | ado | express +0 à +3 j | **pas d'achat** |
| **A-X1** · P | ado | express +1 à +2 j, après A-X0 | aucun exo depuis le début, pas actif aujourd'hui |
| **A-MOD** · P | ado | achat +2 à +4 j | diag complet non terminé, pas actif aujourd'hui |
| **A-MENS:{AAAA-MM}** · P | ado | **1er samedi du mois** | programme, re-diagnostic dû |

Tous les emails ado exigent `email_eleve` **et** `consentement_parent_at`.

### Pas encore codé (prévu dans la proposition du 24/09)

A-RT / P-UP3 (re-test J+28), P-MENS (résultat du re-diag au parent), saisonniers S-DEC / S-BB / S-AVR, suppression à J+30 sans confirmation, avertissement avant suppression à 12 mois, raisons de P-X3 en 1 clic loggées. Priorités : `53` §4.

---

## 2. Plafonds et arrêts (codés dans `mxPlanEmails`)

| Règle | Parent | Ado |
|---|---|---|
| Emails de cron par jour | 1 au maximum, et aucun si un email est déjà parti ce jour-là (événement compris) | 1 au maximum |
| Commercial (M) | 72 h minimum entre deux ; 5 max sur 30 jours glissants ; relances de conversion seulement dans les 30 jours après l'inscription ; **aucun du 15 mai au 31 août** | jamais |
| Pédagogique | — | 3 max sur 7 jours |
| Week-end | samedi : rien (sauf A-MENS) ; dimanche : P-HEBDO seulement | idem |
| Arrêts | UNSUB (P, M) ; 1er achat (P-X0N/R*, P-X1/2/3) ; programme (P-UP*) | UNSUB ; pas d'accord parental |

Les emails d'événement (P-X0, P-ACH*, P-PDF, P-SH, A-ACH*, A-PDF) ne sont pas soumis aux plafonds du cron, mais ils comptent pour la règle « 1 par jour » du cron.

---

## 3. `email_logs`, dédup, désinscription

| Besoin | En place |
|---|---|
| Colonnes | `email, prenom, type, statut ('envoyé' / 'erreur' / 'unsub'), details, categorie (T/P/M), code, created_at` (migration `20260924_diagnostic_3e.sql`) |
| Dédup | `(email, type, code, statut='envoyé')` : par élève, pour qu'un compte recréé avec la même adresse reparte de zéro. Les types récurrents portent leur période (`P-HEBDO:2026-W41`, `A-MENS:2026-11`, `P-SH:{token}`). |
| Désinscription | ligne `type='UNSUB'` **par adresse** (parent et ado indépendants). Lien signé `unsubscribe?email=…&k=HMAC` (page `unsubscribe.html`), et en-têtes `List-Unsubscribe` (one-click RFC 8058 vers l'API + `mailto:`) sur P et M. |
| Pied de page | « Matheux (Nicolas Follezou EI) · matheux.fr » (lien vers les mentions légales) + origine de l'adresse + « Se désinscrire » (P, M) |
| Format | HTML complet (`lang="fr"`, viewport, thème clair), préheader, **partie texte générée** (`mxTexteBrut`) |
| Expéditeur | `Matheux <no-reply@matheux.fr>`, reply-to `contact@matheux.fr` (changement proposé : `53` §4) |
| Outils admin | `send_marketing_email {code_eleve, type}` (envoie un email dû aujourd'hui, mêmes garde-fous) · `send_test_email {targetEmail, type, code_eleve}` (aperçu préfixé [TEST], sans dédup, types du cron uniquement) |
| Tests | `supabase/tests/emails_test.ts` (planificateur : scénarios + fuzz de 300 élèves) · `dev/smoke_test.ts` (15 jours de cron en HTTP, outbox, désinscription) |

---

## 4. Mapping avec l'ancienne séquence

`templateJ0…J14` et `cronSendEmails` (J+1/3/7/14 à 29,99 €) sont **supprimés**. Le cron `cron_send_emails` est conservé, mais il est piloté par l'état. Plus aucune mention de 29,99 €, ni de « ton prof », ni de « bilan chaque semaine » promis aux gratuits (vérifié par le smoke test).

---

## ❓ Décisions prises / restantes

- Confirmation parentale par email : **en place** (P-X0 / P-X0N + 2 rappels). La suppression à J+30 n'est **pas** codée, et aucun email ne l'annonce.
- Email ado facultatif : **prévu côté API**, pas encore demandé dans l'interface.
- Signature ado « Nicolas, de Matheux » : **en place**.
- PDF : **lien** vers la page bilan + téléchargement dans l'app (pas de pièce jointe).
- Cron à 17 h Paris : **en place** (16 h l'hiver, décalage accepté).
- Aucun commercial du 15 mai au 31 août : **en place**.
- Restent ouvertes : voir `53-audit-emails.md` « ❓ Pour Nicolas ».
