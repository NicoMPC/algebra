# Checklist juridique — Matheux (mac.fr)

> Ce document est une checklist pratique de départ, pas du conseil juridique professionnel. Pour toute situation complexe ou litige, consulter un avocat spécialisé en droit numérique.

Contexte : SPA pédagogique française, utilisateurs = collégiens 11-15 ans, fondateur auto-entrepreneur, backend Google Apps Script / Sheets, hébergement GitHub Pages, pas encore de paiement en ligne.

---

## 1. RGPD mineurs — obligatoire avant le premier utilisateur

### 1.1 Âge minimum et consentement parental

| Élément | Statut | Priorité | Action concrète |
|---|---|---|---|
| Âge minimum légal 13 ans | - [ ] À faire | BLOQUANT | Ajouter un champ "année de naissance" ou case "J'ai au moins 13 ans" dans le formulaire d'inscription. Bloquer les moins de 13 ans côté JS. |
| Consentement parental obligatoire pour les moins de 15 ans | - [ ] À faire | BLOQUANT | En pratique : la quasi-totalité des collégiens ayant entre 11 et 15 ans, traiter TOUS les inscrits comme nécessitant un consentement parental. C'est plus simple et conforme. |
| Email collecté = email du parent (pas de l'élève) | - [ ] À faire | BLOQUANT | Modifier le libellé du champ email dans le formulaire : "Email du parent ou tuteur légal". Ne jamais demander l'email de l'élève directement. |

**Ce que doit contenir le consentement parental :**

- **Qui consent** : le titulaire de l'autorité parentale (père, mère, tuteur légal)
- **Sur quoi** : la création d'un compte pédagogique pour leur enfant sur Matheux, incluant la collecte du prénom de l'enfant, de son niveau scolaire et de ses résultats aux exercices
- **Comment le prouver** : pour un MVP, une case à cocher non pré-cochée avec texte explicite suffit (voir section 3). Conserver un log horodaté dans Google Sheets (colonne `ConsentDate` dans l'onglet Users) avec la date et l'IP est recommandé.
- **Limite du dispositif** : la case à cocher ne prouve pas formellement l'identité du parent — c'est acceptable pour un MVP. Pour aller plus loin : email de confirmation au parent.

### 1.2 Durée de conservation des données

| Données | Durée recommandée | Justification |
|---|---|---|
| Scores / résultats aux exercices | 2 ans après la dernière connexion | Durée pédagogiquement utile, raisonnable pour un collégien |
| Email parent | Durée du compte actif + 1 an | Nécessaire pour les communications et la suppression sur demande |
| Hash mot de passe | Durée du compte actif uniquement | Supprimer à la clôture du compte |
| Données de progression (Progress sheet) | 2 ans après la dernière connexion | Même logique que les scores |

Procédure concrète pour le MVP : purge manuelle trimestrielle. Identifier les comptes sans connexion depuis 2 ans dans l'onglet Users (colonne `DernierePratique`) et supprimer toutes les lignes associées dans tous les onglets.

### 1.3 Droit à l'oubli — procédure manuelle MVP

- [ ] Créer une adresse email dédiée type `contact@mac.fr` ou `rgpd@mac.fr` pour les demandes de suppression
- [ ] Mentionner cette adresse dans la politique de confidentialité
- [ ] Délai légal de réponse : **1 mois** à compter de la demande
- [ ] Procédure de suppression dans Google Sheets :
  1. Filtrer l'onglet `Users` sur le code élève concerné → supprimer la ligne
  2. Filtrer l'onglet `Scores` sur le code → supprimer toutes les lignes
  3. Faire de même dans `Progress`, `DailyBoosts`, `RemediationChapters`, `DiagnosticExos` (si données individuelles), `Rapports`, `Pending_Exos`, `Queue`
  4. Confirmer la suppression par email au demandeur
- [ ] Documenter chaque demande traitée dans un fichier local (date, demande, action effectuée) — preuve en cas de contrôle CNIL

### 1.4 Données à ne jamais collecter

- [ ] Notes de bulletin scolaire ou résultats d'examens officiels (brevet, etc.)
- [ ] Données de santé (même si un élève évoque des difficultés de type "dys")
- [ ] Photos, vidéos ou enregistrements audio de l'élève
- [ ] Adresse postale (inutile pour le service)
- [ ] Numéro de téléphone sans raison explicite
- [ ] Données sur la situation familiale (séparation, garde, etc.)
- [ ] Email direct de l'élève mineur (passer par le parent)

### 1.5 Transfert de données hors UE — Google Sheets

Google LLC est une entreprise américaine. Les données stockées dans Google Sheets peuvent transiter ou être stockées sur des serveurs hors UE.

| Élément | Statut | Priorité | Action concrète |
|---|---|---|---|
| Google a signé les Clauses Contractuelles Types (SCCs) avec ses clients | - [ ] À vérifier | Important | Vérifier dans les conditions Google Workspace / Apps Script que les SCCs RGPD sont bien applicables. Google les a intégrées depuis 2022 dans ses DPA (Data Processing Addendum). |
| Mentionner le transfert dans la politique de confidentialité | - [ ] À faire | Important | Indiquer explicitement : "Vos données sont hébergées chez Google LLC (USA) dans le cadre de clauses contractuelles types conformes au RGPD." |
| DPA Google | - [ ] À faire | Recommandé | Signer le Data Processing Addendum Google (gratuit, en ligne sur myaccount.google.com ou admin.google.com) pour couvrir formellement le transfert. |

---

## 2. Documents légaux à rédiger

### 2.1 Mentions légales

**Contenu minimum requis :**
- Identité du responsable de publication (nom, prénom ou raison sociale, statut juridique)
- Adresse de contact (email suffit pour un auto-entrepreneur sans local commercial)
- Nom et coordonnées de l'hébergeur
- Numéro SIRET si auto-entrepreneur enregistré

**Template condensé :**

```
## Mentions légales

**Responsable de publication**
[Prénom Nom], auto-entrepreneur
SIRET : [à compléter]
Contact : contact@mac.fr

**Hébergeur**
GitHub Pages — GitHub Inc., 88 Colin P Kelly Jr St, San Francisco, CA 94107, USA
Backend : Google LLC, 1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA (Google Apps Script)

**Propriété intellectuelle**
Le contenu pédagogique (exercices, méthodes, textes) est la propriété exclusive de [Prénom Nom].
Toute reproduction sans autorisation est interdite.

**Droit applicable**
Droit français. Tout litige relève de la compétence des tribunaux français.
```

### 2.2 Conditions Générales d'Utilisation (CGU)

**Contenu minimum requis :**
- Objet du service
- Conditions d'accès (âge minimum, consentement parental)
- Droits de l'utilisateur sur le service
- Droits du service (suspension de compte, modification du service)
- Clause de non-responsabilité pédagogique
- Droit applicable

**Template condensé :**

```
## Conditions Générales d'Utilisation

**1. Objet**
Matheux est un outil pédagogique d'entraînement aux mathématiques destiné aux collégiens
(classes de 6ème à 3ème). Il ne se substitue pas à l'enseignement scolaire.

**2. Accès au service**
L'inscription est réservée aux collégiens âgés de 13 ans minimum.
Pour les élèves de moins de 15 ans, le consentement d'un parent ou tuteur légal est obligatoire.
L'email fourni à l'inscription doit être celui du parent ou tuteur légal.

**3. Droits de l'utilisateur**
L'utilisateur peut accéder à ses données, demander leur correction ou suppression
à tout moment via contact@mac.fr. Réponse garantie sous 1 mois.

**4. Droits du service**
Matheux se réserve le droit de modifier, suspendre ou interrompre le service à tout moment,
notamment en cas d'utilisation abusive ou frauduleuse.

**5. Non-responsabilité pédagogique**
Les résultats affichés dans l'application sont indicatifs. Matheux ne peut être tenu responsable
des résultats scolaires de l'élève. Aucune garantie de progression n'est fournie.

**6. Propriété intellectuelle**
Les exercices, méthodes et contenus sont protégés. Toute copie ou diffusion est interdite.

**7. Droit applicable**
Les présentes CGU sont soumises au droit français.
```

### 2.3 Politique de confidentialité

**Contenu minimum requis (RGPD art. 13) :**
- Identité du responsable du traitement
- Données collectées et finalité de chaque traitement
- Base légale de chaque traitement
- Durée de conservation
- Destinataires des données (dont transferts hors UE)
- Droits des personnes (accès, rectification, effacement, opposition)
- Contact pour exercer ces droits
- Droit de réclamation auprès de la CNIL

**Template condensé :**

```
## Politique de confidentialité

**Responsable du traitement**
[Prénom Nom] — contact@mac.fr

**Données collectées**
| Donnée | Finalité | Base légale | Durée |
|---|---|---|---|
| Email du parent | Connexion, communication | Consentement | Durée du compte + 1 an |
| Prénom de l'élève | Personnalisation | Consentement parental | Durée du compte + 1 an |
| Niveau scolaire | Adaptation pédagogique | Consentement parental | Durée du compte + 1 an |
| Résultats aux exercices | Suivi progression | Consentement parental | 2 ans après dernière connexion |

**Destinataires**
Données hébergées chez Google LLC (USA) via Google Sheets et Google Apps Script,
dans le cadre de clauses contractuelles types conformes au RGPD.
Aucune donnée n'est vendue ou partagée avec des tiers.

**Vos droits**
Accès, rectification, effacement, opposition, limitation, portabilité.
Demande à adresser à : contact@mac.fr — Réponse sous 1 mois.
Réclamation possible auprès de la CNIL : www.cnil.fr

**Cookies**
Ce site n'utilise pas de cookies de traçage à ce jour.
[Mettre à jour si Google Analytics ou Stripe sont ajoutés.]

**Mineurs**
Conformément à l'article 8 du RGPD, le traitement des données d'enfants de moins de 15 ans
requiert le consentement du titulaire de l'autorité parentale.
```

### 2.4 Politique cookies

**Situation actuelle (MVP sans Stripe ni Analytics) :**

- [ ] Aujourd'hui : seul `localStorage` est utilisé (clés `boost_v23`, `boost_loc_v23`) — pas un cookie au sens technique, mais une donnée locale. Aucun bandeau cookies n'est légalement requis si aucun cookie tiers n'est déposé.
- [ ] Dès l'ajout de Google Analytics : bandeau cookies obligatoire avec opt-in explicite (pas opt-out)
- [ ] Dès l'ajout de Stripe.js : Stripe dépose des cookies de fraude/sécurité — ils sont exemptés de consentement car strictement nécessaires au paiement, mais doivent être mentionnés dans la politique

**Template pour quand Stripe et/ou Analytics seront intégrés :**

```
## Politique cookies

**Cookies strictement nécessaires (pas de consentement requis)**
| Cookie | Émetteur | Finalité | Durée |
|---|---|---|---|
| __stripe_mid | Stripe Inc. | Prévention de la fraude | 1 an |
| __stripe_sid | Stripe Inc. | Sécurité transaction | 30 min |

**Cookies analytiques (consentement requis)**
| Cookie | Émetteur | Finalité | Durée |
|---|---|---|---|
| _ga | Google Analytics | Mesure d'audience anonyme | 2 ans |

**Données locales (localStorage)**
L'application stocke localement sur votre appareil vos préférences de session
et votre progression hors-ligne. Ces données ne quittent pas votre appareil.

**Gérer vos préférences**
[Bouton : Accepter les cookies analytiques] [Bouton : Refuser]
```

---

## 3. Case de consentement parental — template HTML

```html
<!-- À insérer dans le formulaire d'inscription, après le champ email -->
<div class="consent-block" style="margin: 16px 0;">
  <label style="display: flex; align-items: flex-start; gap: 10px; cursor: pointer;">
    <input
      type="checkbox"
      id="parentalConsent"
      name="parentalConsent"
      required
      style="margin-top: 3px; flex-shrink: 0; width: 18px; height: 18px; cursor: pointer;"
    />
    <span style="font-size: 0.875rem; line-height: 1.5; color: #374151;">
      En tant que parent ou tuteur légal, je consens à la création d'un compte
      pédagogique pour mon enfant sur Matheux et au traitement de ses données
      (prénom, niveau scolaire, résultats aux exercices) conformément à la
      <a href="/politique-confidentialite.html" target="_blank"
         style="color: #6366f1; text-decoration: underline;">
        politique de confidentialité
      </a>.
      Je certifie que mon enfant a au moins 13 ans.
    </span>
  </label>
  <p id="consentError" style="display: none; color: #dc2626; font-size: 0.8rem; margin: 6px 0 0 28px;">
    Le consentement parental est obligatoire pour créer un compte.
  </p>
</div>
```

**Validation JS côté client à ajouter dans la fonction d'inscription :**

```javascript
// À appeler avant tout envoi au backend GAS
function validateParentalConsent() {
  const checkbox = document.getElementById('parentalConsent');
  const errorMsg = document.getElementById('consentError');

  if (!checkbox || !checkbox.checked) {
    if (errorMsg) errorMsg.style.display = 'block';
    checkbox && checkbox.focus();
    return false;
  }
  if (errorMsg) errorMsg.style.display = 'none';
  return true;
}

// Intégration dans la fonction existante finalizeOnboarding() ou handleRegister() :
// if (!validateParentalConsent()) return;
```

**Côté backend GAS — stocker le consentement :**

Ajouter dans l'action `register` l'écriture d'une colonne `ConsentDate` dans l'onglet `Users` avec la date ISO du moment de l'inscription. Cela constitue une trace horodatée suffisante pour un MVP.

---

## 4. Risques à éviter absolument

| # | Risque | Gravité | Action préventive |
|---|---|---|---|
| R1 | Collecter l'email de l'élève (mineur) directement | **Critique** | Changer le libellé du champ email en "Email du parent ou tuteur légal". Ne jamais stocker un email d'élève. Si un élève s'inscrit avec son propre email, les données ne peuvent légalement pas être conservées. |
| R2 | Publier ou afficher des données de performance d'élèves sans consentement explicite | **Critique** | Ne jamais afficher de classement public, de palmarès ou de comparaison nommée entre élèves. Les données de progression restent privées et accessibles uniquement au compte concerné. |
| R3 | Utiliser des photos, prénoms + noms complets ou témoignages réels d'élèves dans la communication | **Élevé** | Pour les témoignages marketing : utiliser des données anonymisées ("un élève de 4ème") ou obtenir un consentement écrit signé du parent. Jamais de nom complet, jamais de photo sans accord signé. |
| R4 | Absence de procédure de suppression des données (droit à l'oubli) | **Élevé** | Mettre en place la procédure manuelle décrite en section 1.3 dès le lancement. Publier l'adresse de contact dans la politique de confidentialité. Même une procédure manuelle sur email est conforme pour un MVP. |
| R5 | Hash mot de passe côté client uniquement sans salt serveur | **Moyen** | Le hash SHA-256 client-side est acceptable pour un MVP mais doit être documenté comme limitation connue. Ne pas faire miroiter une sécurité enterprise. Si un utilisateur reporte une inquiétude, ne pas minimiser. Prévoir migration vers hash serveur (bcrypt) avant la mise à l'échelle. |

---

## 5. Ordre de priorité

### Avant le premier client payant — Semaine 1 (BLOQUANT)

- [ ] **Changer le libellé du champ email** → "Email du parent ou tuteur légal"
- [ ] **Ajouter la case de consentement parental** (template section 3) dans le formulaire d'inscription
- [ ] **Ajouter validation JS** côté client bloquant l'inscription sans consentement
- [ ] **Ajouter colonne `ConsentDate`** dans l'onglet Users du Sheet (horodatage du consentement)
- [ ] **Rédiger et publier la politique de confidentialité** (template section 2.3) — une page HTML statique suffit
- [ ] **Rédiger et publier les mentions légales** (template section 2.1) — footer ou page dédiée
- [ ] **Créer l'adresse email de contact** (type contact@mac.fr) pour les demandes RGPD
- [ ] **Ajouter l'âge minimum** : case "Je certifie que mon enfant a au moins 13 ans" dans le formulaire (incluse dans le template section 3)

### Avant de dépasser 50 clients — Mois 2-3 (Important)

- [ ] **Rédiger et publier les CGU** (template section 2.2)
- [ ] **Signer le DPA Google** (Data Processing Addendum) pour couvrir le transfert hors UE
- [ ] **Documenter la procédure droit à l'oubli** et la tester une fois manuellement
- [ ] **Vérifier l'absence de données d'élèves hors périmètre** (audit rapide des onglets Sheets)
- [ ] **Mettre en place la purge trimestrielle** des comptes inactifs depuis 2 ans
- [ ] **Colonnes `Premium` et `TrialStart`** dans Users (nécessaires pour Stripe — RGPD impose de justifier la durée de conservation des données de paiement)
- [ ] **Politique cookies** : préparer le template (section 2.4) avant l'ajout de Stripe ou Analytics
- [ ] **Case consentement parental côté GAS** : enregistrer et vérifier `consentDate` dans l'action `register`

### Si expansion (scale, +50 clients, paiement en ligne, communications marketing)

- [ ] **Désigner un DPO (Délégué à la Protection des Données)** — obligatoire si traitement à grande échelle de données de mineurs
- [ ] **Tenir un registre des traitements** (article 30 RGPD) — tableau listant chaque traitement, sa finalité, sa base légale, sa durée
- [ ] **Bandeau cookies conforme** (opt-in) dès l'ajout de Google Analytics
- [ ] **Intégration Stripe** : mettre à jour la politique de confidentialité et la politique cookies
- [ ] **Email de confirmation parental** : envoyer un email au parent avec lien de validation du consentement (remplace la simple case à cocher)
- [ ] **Migration hash serveur** : passer de SHA-256 client-side à bcrypt côté GAS ou une vraie API d'auth
- [ ] **Mentions légales enrichies** avec numéro SIRET, TVA intracommunautaire si applicable
- [ ] **CGV (Conditions Générales de Vente)** distinctes des CGU, obligatoires dès la mise en place du paiement
- [ ] **Droit de rétractation 14 jours** (obligatoire pour les ventes en ligne B2C en France) — à mentionner dans les CGV
- [ ] **Formulaire de contact RGPD intégré** dans l'app (remplace la procédure email manuelle)
- [ ] **Consultation CNIL** via le guichet des démarches si traitement de données sensibles ou à grande échelle

---

> Dernière mise à jour : mars 2026. À réviser si la législation évolue ou si l'architecture technique change significativement (ajout de paiement, analytics, stockage tiers).
