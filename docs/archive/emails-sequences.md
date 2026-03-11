# Séquences emails — Matheux

Envoi via Gmail API depuis Google Apps Script. Destinataires : parents d'élèves.
Ton : chaleureux, humain, direct. Pas de jargon startup.

---

## Email J0 — Bienvenue

**Déclencheur :** immédiatement après inscription réussie (`register` GAS).
**Objectif :** confirmer l'inscription, rassurer, donner le premier pas concret.
**Variables :** `{{prenom_eleve}}`, `{{niveau}}`, `{{prenom_parent}}`

### Variante A — sujet

```
Matheux : {{prenom_eleve}} est inscrit(e) ✓
```

### Variante B — sujet

```
Bienvenue sur Matheux — voici comment démarrer
```

### Corps

> Bonjour {{prenom_parent}},
>
> {{prenom_eleve}} vient de rejoindre Matheux — l'outil que j'ai créé pour aider les élèves de collège à combler leurs lacunes en maths, à leur rythme.
>
> Je suis Nicolas, prof de maths. J'ai conçu Matheux pour que chaque élève parte de là où il en est vraiment, pas d'un programme générique.
>
> **Premier pas :** {{prenom_eleve}} peut se connecter dès maintenant et faire son diagnostic (8 questions, ~5 min). Ça me permettra de savoir exactement sur quoi concentrer les exercices.
>
> Quelques points pratiques :
> - Les données de {{prenom_eleve}} sont stockées en sécurité, jamais partagées avec des tiers.
> - Vous pouvez me contacter directement en répondant à cet email.
> - L'essai est gratuit pendant 7 jours, sans carte bancaire.
>
> À très vite,
> Nicolas
>
> ---
> *Pour ne plus recevoir ces emails : [Se désabonner]({{lien_desabonnement}})*

**CTA unique :** "Faire le diagnostic" — lien vers l'app, vue diagnostic.

**Notes de personnalisation :**
- Si `prenom_parent` non collecté à l'inscription : remplacer par "Bonjour," sans prénom.
- `{{niveau}}` peut être injecté dans le corps si besoin : "élève de {{niveau}}".

---

## Email J+3 — Relance si pas connecté

**Déclencheur :** 3 jours après inscription, 0 connexion enregistrée (pas d'entrée dans Scores pour ce code).
**Objectif :** réactiver sans culpabiliser.
**Variables :** `{{prenom_eleve}}`, `{{prenom_parent}}`

### Variante A — sujet

```
{{prenom_eleve}} n'a pas encore démarré — besoin d'aide ?
```

### Variante B — sujet

```
3 jours déjà — Matheux attend {{prenom_eleve}}
```

### Corps

> Bonjour {{prenom_parent}},
>
> Je voulais juste vérifier que tout allait bien — {{prenom_eleve}} ne s'est pas encore connecté(e) depuis l'inscription.
>
> Pas d'inquiétude, ça arrive souvent. Parfois il suffit d'un créneau de 5 minutes pour démarrer.
>
> Le diagnostic de départ ne prend que ~5 minutes et ça change vraiment la suite : les exercices proposés sont adaptés à ce que {{prenom_eleve}} ne maîtrise pas encore.
>
> Si quelque chose bloque (connexion, mot de passe, autre), répondez directement à cet email — je regarde.
>
> Nicolas

**CTA unique :** "Démarrer le diagnostic" — lien direct vers l'app.

**Notes de personnalisation :**
- Pas de majuscule sur "nicolas" en signature — volontairement informel.
- Ne pas envoyer si l'élève s'est connecté dans les 72h (vérifier Scores au moment du trigger).

---

## Email J+6 — Conversion (veille fin d'essai)

**Déclencheur :** J-1 avant la fin du freemium 7 jours.
**Objectif :** convertir sans pression. Mettre en avant ce que l'élève a fait.
**Variables :** `{{prenom_eleve}}`, `{{prenom_parent}}`, `{{nb_exercices_faits}}`, `{{streak}}`, `{{chapitre_fort}}`

### Variante A — sujet

```
L'essai de {{prenom_eleve}} se termine demain
```

### Variante B — sujet

```
{{nb_exercices_faits}} exercices en 7 jours — la suite ?
```

### Corps (si données disponibles — nb_exercices_faits > 0)

> Bonjour {{prenom_parent}},
>
> L'essai gratuit de {{prenom_eleve}} se termine demain.
>
> En 7 jours, {{prenom_eleve}} a fait **{{nb_exercices_faits}} exercices**, avec {{streak}} jours de pratique consécutifs. Son point fort du moment : **{{chapitre_fort}}**.
>
> C'est un bon début. Le travail régulier, même 10 minutes par jour, est vraiment ce qui fait la différence sur la durée — et Matheux est conçu pour ça.
>
> Pour continuer, c'est **9,99 €/mois**, sans engagement. Vous pouvez arrêter à tout moment.
>
> Si vous avez des questions avant de décider, répondez à cet email — je vous réponds personnellement.
>
> Nicolas
>
> [Continuer avec Matheux →]({{lien_paiement}})
>
> ---
> *Pour ne plus recevoir ces emails : [Se désabonner]({{lien_desabonnement}})*

### Corps alternatif (si 0 exercice fait)

> Bonjour {{prenom_parent}},
>
> L'essai gratuit de {{prenom_eleve}} se termine demain, et il n'a pas encore été utilisé.
>
> Je ne veux pas vous vendre quelque chose que vous n'avez pas testé — donc je ne vous propose pas de passer à l'abonnement tout de suite.
>
> Si vous souhaitez quand même essayer avant la fin, je peux décaler l'essai de quelques jours. Répondez simplement à cet email.
>
> Nicolas
>
> ---
> *Pour ne plus recevoir ces emails : [Se désabonner]({{lien_desabonnement}})*

**CTA unique :** "Continuer avec Matheux →" — lien vers page paiement Stripe.

**Notes de personnalisation :**
- Choisir le corps selon `nb_exercices_faits > 0` au moment du déclenchement.
- `{{chapitre_fort}}` : prendre le chapitre avec le score Progress le plus élevé.
- `{{streak}}` : lire depuis Progress sheet.

---

## Email — Mot de passe oublié

**Déclencheur :** demande de reset mot de passe (action GAS `reset_password`).
**Objectif :** transactionnel pur, rapide.
**Variables :** `{{prenom_eleve}}`, `{{lien_reset}}`

### Sujet (unique, pas d'A/B)

```
Réinitialisation du mot de passe Matheux
```

### Corps

> Bonjour,
>
> Vous avez demandé à réinitialiser le mot de passe du compte de {{prenom_eleve}} sur Matheux.
>
> [Choisir un nouveau mot de passe →]({{lien_reset}})
>
> Ce lien est valable 1 heure. Si vous n'êtes pas à l'origine de cette demande, ignorez cet email — le mot de passe actuel reste inchangé.
>
> Nicolas — Matheux
>
> ---
> *Pour ne plus recevoir ces emails : [Se désabonner]({{lien_desabonnement}})*

**CTA unique :** "Choisir un nouveau mot de passe →"

**Notes de personnalisation :**
- Pas de personnalisation chaleureuse — ton neutre et rassurant adapté au contexte.
- Le lien reset doit contenir un token à usage unique, expirant en 1h. À implémenter côté GAS : génère un UUID, le stocke dans Users avec une colonne `ResetToken` + `ResetExpiry`, le vérifie au moment du clic.

---

## Email — Rapport hebdo parents

**Déclencheur :** chaque lundi matin (trigger GAS 7h), pour tous les comptes actifs la semaine précédente.
**Objectif :** montrer la valeur concrète, fidéliser, déclencher conversion pour les comptes gratuits.
**Variables :** `{{prenom_eleve}}`, `{{prenom_parent}}`, `{{nb_exercices_semaine}}`, `{{streak}}`, `{{chapitre_travaille}}`, `{{score_progres}}`

### Variante A — sujet

```
La semaine de {{prenom_eleve}} en maths — résumé du {{date_lundi}}
```

### Variante B — sujet

```
{{prenom_eleve}} : {{nb_exercices_semaine}} exercices cette semaine 📊
```

### Corps

> Bonjour {{prenom_parent}},
>
> Voici le résumé de la semaine de {{prenom_eleve}} sur Matheux.
>
> **Cette semaine :**
> - {{nb_exercices_semaine}} exercices réalisés
> - {{streak}} jours de pratique consécutifs
> - Chapitre principal travaillé : **{{chapitre_travaille}}**
> - Évolution : **{{score_progres}}**
>
> **Ce qui va bien :**
> {{point_fort}} *(ex : "{{prenom_eleve}} maîtrise maintenant les priorités opératoires — les erreurs sur ce chapitre ont quasi disparu.")*
>
> **Ce sur quoi on travaille :**
> {{point_a_travailler}} *(ex : "Les fractions restent difficiles — c'est normal à ce stade, c'est souvent le chapitre qui bloque le plus en 5ème.")*
>
> **Mon conseil pour la semaine à venir :**
> {{conseil_nicolas}} *(ex : "10 minutes par jour valent mieux qu'une heure le dimanche soir. Si {{prenom_eleve}} pouvait ouvrir l'app en rentrant de l'école, même juste 2-3 exercices, ce serait parfait.")*
>
> À la semaine prochaine,
> Nicolas
>
> ---
> *Matheux — outil pédagogique maths collège*
> *Pour ne plus recevoir ces emails : [Se désabonner]({{lien_desabonnement}})*

**CTA unique :** aucun CTA commercial pour les abonnés actifs. Pour les comptes en fin d'essai : ajouter une ligne avant la signature : "L'essai gratuit de {{prenom_eleve}} se termine le {{date_fin_essai}}. [Continuer →]({{lien_paiement}})"

**Notes de personnalisation :**
- `{{point_fort}}` et `{{point_a_travailler}}` : générés par `generateMorningReport()` (déjà implémenté dans backend.js via l'analyse des statuts ACQUISE/FRAGILE/BLOQUEE).
- `{{conseil_nicolas}}` : texte statique par défaut, peut être personnalisé si le rapport matin le précise.
- Ne pas envoyer si `nb_exercices_semaine === 0` — envoyer le rappel inactivité à la place.
- `{{date_lundi}}` : format "lundi 10 mars".

---

## Email — Rappel après 3 jours d'inactivité

**Déclencheur :** 3 jours consécutifs sans connexion (pas d'entrée Scores depuis 72h).
**Objectif :** ramener l'élève sans culpabiliser. Rappeler le streak si > 0.
**Variables :** `{{prenom_eleve}}`, `{{prenom_parent}}`, `{{streak}}`

### Variante A — sujet (streak > 2)

```
{{prenom_eleve}} est à {{streak}} jours de suite — dommage de s'arrêter là
```

### Variante B — sujet (streak = 0 ou 1)

```
{{prenom_eleve}} n'a pas fait de maths depuis 3 jours
```

### Corps (si streak > 2)

> Bonjour {{prenom_parent}},
>
> Petit mot rapide : {{prenom_eleve}} avait un super rythme avec {{streak}} jours consécutifs de pratique. Ça fait 3 jours qu'il/elle n'a pas ouvert Matheux.
>
> Pas de pression — mais c'est souvent à ce moment-là qu'on perd le fil. 5 minutes suffisent pour reprendre.
>
> Nicolas
>
> [Reprendre les exercices →]({{lien_app}})

### Corps (si streak = 0 ou 1)

> Bonjour {{prenom_parent}},
>
> {{prenom_eleve}} n'a pas pratiqué depuis 3 jours. Les maths, ça s'entretient mieux avec un peu de régularité qu'avec de longues sessions ponctuelles.
>
> Si quelque chose bloque (trop dur, pas motivant), n'hésitez pas à me le faire savoir en répondant à cet email.
>
> Nicolas
>
> [Reprendre les exercices →]({{lien_app}})
>
> ---
> *Pour ne plus recevoir ces emails : [Se désabonner]({{lien_desabonnement}})*

**CTA unique :** "Reprendre les exercices →"

**Notes de personnalisation :**
- Maximum 1 rappel par semaine par élève — ne pas spammer.
- Ne pas envoyer si un email a déjà été envoyé dans les 5 derniers jours.

---

## Implémentation GAS

### Fonction d'envoi de base

```javascript
/**
 * Envoie un email transactionnel depuis le compte Gmail du fondateur.
 * @param {string} to - Adresse email du destinataire
 * @param {string} subject - Sujet de l'email
 * @param {string} body - Corps HTML de l'email
 */
function sendEmail(to, subject, body) {
  const fullBody = body + buildUnsubscribeFooter(to);

  GmailApp.sendEmail(to, subject, '', {
    htmlBody: fullBody,
    name: 'Nicolas — Matheux',
    replyTo: 'nicolas@mac.fr' // adresse réelle du fondateur
  });
}

/**
 * Construit le footer RGPD avec lien de désinscription.
 * Le token est l'email encodé en base64 — simple pour un MVP.
 */
function buildUnsubscribeFooter(email) {
  const token = Utilities.base64Encode(email);
  const unsubUrl = ScriptApp.getService().getUrl()
    + '?action=unsubscribe&token=' + encodeURIComponent(token);

  return `
    <hr style="margin-top:32px;border:none;border-top:1px solid #eee;">
    <p style="font-size:12px;color:#999;margin-top:8px;">
      Pour ne plus recevoir ces emails :
      <a href="${unsubUrl}" style="color:#999;">Se désabonner</a>
    </p>
  `;
}
```

### Appel depuis un trigger quotidien

```javascript
/**
 * Trigger GAS : chaque jour à 7h via Apps Script → Déclencheurs.
 * Gère les envois J+3 (relance), J+6 (conversion), rapport hebdo (lundi).
 */
function dailyEmailTrigger() {
  const today = new Date();
  const dayOfWeek = today.getDay(); // 0=dim, 1=lun

  // Rapport hebdo — uniquement le lundi
  if (dayOfWeek === 1) {
    sendWeeklyReports();
  }

  // Relance J+3 et conversion J+6 — tous les jours
  sendOnboardingSequence();

  // Rappel inactivité 3 jours — tous les jours
  sendInactivityReminders();
}

function sendOnboardingSequence() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const users = ss.getSheetByName('Users').getDataRange().getValues();
  const scores = ss.getSheetByName('Scores').getDataRange().getValues();
  const now = new Date();

  // Index des connexions par code élève
  const connectionsByCode = {};
  scores.slice(1).forEach(row => {
    const code = row[0];
    if (!connectionsByCode[code]) connectionsByCode[code] = [];
    connectionsByCode[code].push(new Date(row[12])); // colonne Date
  });

  users.slice(1).forEach(row => {
    const [code, prenom, niveau, email, , dateInscription] = row;
    if (!email) return;

    const inscritLe = new Date(dateInscription);
    const joursDepuis = Math.floor((now - inscritLe) / 86400000);
    const connexions = connectionsByCode[code] || [];

    // J+3 : pas de connexion depuis l'inscription
    if (joursDepuis === 3 && connexions.length === 0) {
      const subject = `${prenom} n'a pas encore démarré — besoin d'aide ?`;
      const body = buildEmailJ3(prenom);
      sendEmail(email, subject, body);
    }

    // J+6 : veille fin d'essai
    if (joursDepuis === 6) {
      const nbExos = connexions.length; // approximation — idéalement lire Progress
      const subject = nbExos > 0
        ? `L'essai de ${prenom} se termine demain`
        : `L'essai de ${prenom} se termine demain`;
      const body = buildEmailJ6(prenom, nbExos);
      sendEmail(email, subject, body);
    }
  });
}
```

### Appel depuis doPost (email transactionnel)

```javascript
// Dans doPost(), dans le switch(action) :
case 'send_welcome_email': {
  const { email, prenom, niveau } = params;
  const subject = `Matheux : ${prenom} est inscrit(e) ✓`;
  const body = buildEmailWelcome(prenom, niveau);
  sendEmail(email, subject, body);
  return jsonOk({ status: 'sent' });
}

case 'reset_password': {
  const { email } = params;
  const token = Utilities.getUuid();
  const expiry = new Date(Date.now() + 3600000).toISOString(); // +1h

  // Stocker token dans Users (colonnes ResetToken, ResetExpiry)
  storeResetToken(email, token, expiry);

  const resetUrl = ScriptApp.getService().getUrl()
    + '?action=do_reset&token=' + token;
  const body = buildEmailReset(token, resetUrl);
  sendEmail(email, 'Réinitialisation du mot de passe Matheux', body);
  return jsonOk({ status: 'sent' });
}
```

### Gestion des désinscriptions (RGPD obligatoire)

```javascript
/**
 * Appelé via GET ?action=unsubscribe&token=...
 * À gérer dans doGet() du GAS.
 */
function handleUnsubscribe(token) {
  try {
    const email = Utilities.newBlob(
      Utilities.base64Decode(decodeURIComponent(token))
    ).getDataAsString();

    const ss = SpreadsheetApp.openById(SHEET_ID);
    const users = ss.getSheetByName('Users');
    const data = users.getDataRange().getValues();

    for (let i = 1; i < data.length; i++) {
      if (data[i][3] === email) { // colonne Email
        // Colonne EmailOptOut à ajouter dans Users
        users.getRange(i + 1, /* col EmailOptOut */ 10).setValue('YES');
        break;
      }
    }

    return HtmlService.createHtmlOutput(
      '<p>Vous avez bien été désinscrit(e) des emails Matheux.</p>'
    );
  } catch (e) {
    return HtmlService.createHtmlOutput('<p>Lien invalide.</p>');
  }
}

// Dans doGet() :
function doGet(e) {
  const action = e.parameter.action;
  if (action === 'unsubscribe') {
    return handleUnsubscribe(e.parameter.token);
  }
  if (action === 'do_reset') {
    return handlePasswordReset(e.parameter.token);
  }
  // ... autres GET
}

/**
 * Vérifier l'opt-out avant chaque envoi.
 * À appeler au début de sendEmail().
 */
function isUnsubscribed(email) {
  const users = SpreadsheetApp.openById(SHEET_ID)
    .getSheetByName('Users')
    .getDataRange().getValues();
  return users.slice(1).some(row => row[3] === email && row[9] === 'YES');
}

// Version finale de sendEmail avec vérification opt-out :
function sendEmail(to, subject, body) {
  if (isUnsubscribed(to)) return; // respecter le choix RGPD

  const fullBody = body + buildUnsubscribeFooter(to);
  GmailApp.sendEmail(to, subject, '', {
    htmlBody: fullBody,
    name: 'Nicolas — Matheux',
    replyTo: 'nicolas@mac.fr'
  });
}
```

### Colonne à ajouter dans Users

```
Users → ajouter colonne en position 10 :
EmailOptOut   (vide = OK, 'YES' = désinscrit)
```

### Limites Gmail API à garder en tête

- Quota Gmail via GAS : **100 emails/jour** en compte gratuit, **1500/jour** avec Google Workspace.
- Pour un MVP à <50 élèves, le quota gratuit est largement suffisant.
- Si dépassement : GAS lance une exception — à encadrer dans un try/catch et logger dans un onglet `EmailErrors`.
