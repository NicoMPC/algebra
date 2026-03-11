# Tracking & Analytics — Matheux

> Actionnable dès demain. Tout le code est prêt à copier-coller.

---

## 1. Google Analytics 4 — intégration dans index.html

### Snippet d'initialisation (à coller dans `<head>`, avant tout autre script)

```html
<!-- Google Analytics 4 — remplacer G-XXXXXXXXXX par ton Measurement ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX', {
    anonymize_ip: true,          // obligatoire RGPD
    allow_google_signals: false, // pas de remarketing sur mineurs
    allow_ad_personalization_signals: false
  });
</script>
```

> Obtenir le Measurement ID : GA4 → Admin → Flux de données → Web → Measurement ID (format `G-XXXXXXXXXX`).

---

### Les 8 événements à tracker — code JS exact

Coller ces appels aux endroits indiqués dans `index.html` / `backend.js` côté client.

#### 1. `inscription_complete` — après succès du `register`

Emplacement : dans le callback de succès de `finalizeOnboarding()`, après que le compte est créé.

```js
gtag('event', 'inscription_complete', {
  niveau: selectedLevel  // ex: '6EME', '5EME', '4EME', '3EME'
});
```

#### 2. `login_success` — après succès du `login`

Emplacement : dans `initApp()`, après réception d'un `status: 'success'` du GAS.

```js
gtag('event', 'login_success');
```

#### 3. `diagnostic_complete` — après fin du diagnostic

Emplacement : dans la fonction qui affiche l'écran de résultats du diagnostic, après le dernier exercice.

```js
gtag('event', 'diagnostic_complete', {
  nb_questions: diagExos.length,       // ex: 8
  nb_erreurs: diagResults.filter(r => r === 'HARD').length
});
```

#### 4. `exercice_fait` — après chaque exercice (EASY / MEDIUM / HARD)

Emplacement : dans `mark()` ou `sendScore()`, juste avant ou après l'appel au GAS.

```js
gtag('event', 'exercice_fait', {
  chapitre: cat,       // ex: 'Fractions'
  resultat: mark,      // 'EASY', 'MEDIUM' ou 'HARD'
  lvl: currentLvl      // 1 ou 2
});
```

#### 5. `boost_ouvert` — quand l'élève ouvre son boost quotidien

Emplacement : au début de `handleBoost()`, avant le call GAS.

```js
gtag('event', 'boost_ouvert');
```

#### 6. `boost_complete` — quand il finit les 5 exercices du boost

Emplacement : dans la logique de fin de boost, quand l'index d'exercice atteint `boostExos.length`.

```js
gtag('event', 'boost_complete');
```

#### 7. `vue_progression_ouverte` — quand l'élève consulte sa progression

Emplacement : dans `setView('progress')`, au moment où la vue est effectivement affichée.

```js
gtag('event', 'vue_progression_ouverte');
```

#### 8. `conversion_payant` — à déclencher manuellement quand un client paie

À appeler depuis le webhook Stripe (côté client après confirmation paiement) ou manuellement depuis la console si pas encore automatisé.

```js
gtag('event', 'conversion_payant', {
  value: 9.99,
  currency: 'EUR'
});
```

---

## 2. Ce qu'on ne doit absolument pas tracker (RGPD mineurs)

Les élèves sont des mineurs (collège, 11–15 ans). Le RGPD impose des obligations renforcées : consentement parental, minimisation des données, pas de profilage publicitaire.

### 6 choses à ne jamais envoyer à GA4

| # | Ce qu'il ne faut pas tracker | Pourquoi |
|---|---|---|
| 1 | **Email** de l'élève ou du parent | Donnée personnelle directement identifiante |
| 2 | **Prénom réel** de l'élève | Donnée personnelle, même seule |
| 3 | **Code élève** (`boost_v23` → `email`) | Le code dérive de l'email → identifiant indirect |
| 4 | **Score détaillé lié à une identité** | Combinaison score + prénom + école = profilage d'un mineur |
| 5 | **Données de localisation** (IP non anonymisée, ville précise) | Peut permettre de localiser un mineur |
| 6 | **Combinaison chapitre + résultat + identifiant** | Permet de reconstituer le profil scolaire d'un élève identifiable |

### Comment anonymiser correctement

**Règle absolue :** aucun PII (Personally Identifiable Information) dans les paramètres GA4.

```js
// ✅ Correct — paramètres anonymes
gtag('event', 'exercice_fait', {
  chapitre: 'Fractions',   // catégorie générique, pas l'ID de l'exo
  resultat: 'HARD',
  lvl: 2
  // ❌ PAS de : user_id, email, prenom, code
});

// ❌ Interdit
gtag('event', 'exercice_fait', {
  user_email: 'emma@example.com',   // PII direct
  user_code: 'EMM601',              // identifiant indirect
  prenom: 'Emma'                    // PII
});
```

**Pour les analyses cross-session** sans PII : utiliser un `client_id` anonyme généré aléatoirement et stocké dans localStorage, sans lien avec l'email.

```js
// Générer un ID anonyme à l'inscription, jamais lié à l'email
if (!localStorage.getItem('anon_id')) {
  localStorage.setItem('anon_id', crypto.randomUUID());
}
// Ne jamais envoyer cet ID à GA4 non plus — il reste local uniquement
```

**Configuration GA4 obligatoire** (déjà incluse dans le snippet ci-dessus) :
- `anonymize_ip: true` — tronque la dernière partie de l'IP
- `allow_google_signals: false` — désactive le remarketing
- `allow_ad_personalization_signals: false` — pas de ciblage pub

---

## 3. KPIs hebdomadaires — les 5 chiffres à regarder chaque lundi

### KPI 1 — Taux d'activation J1

| Champ | Valeur |
|---|---|
| **Définition** | % d'élèves inscrits qui ont fait ≥ 5 exercices dans les 24h suivant l'inscription |
| **Calcul** | (nb élèves avec ≥5 lignes dans Scores dont Date ≤ DateInscription + 1j) / (nb inscrits cette semaine) × 100 |
| **Source** | Onglet `Users` (DateInscription) + onglet `Scores` (Code, Date) |
| **Seuil d'alerte** | < 30% → l'onboarding ne convainc pas |

### KPI 2 — Rétention J7

| Champ | Valeur |
|---|---|
| **Définition** | % des élèves inscrits il y a 7 jours qui se sont reconnectés au moins une fois dans les 7 derniers jours |
| **Calcul** | (nb élèves inscrits entre J-14 et J-7 ayant une ligne Scores dans les 7 derniers jours) / (nb inscrits entre J-14 et J-7) × 100 |
| **Source** | `Users` (DateInscription) + `Scores` (Code, Date) |
| **Seuil d'alerte** | < 40% → problème de rétention, revoir le nudge ou le contenu |

### KPI 3 — Streak moyen

| Champ | Valeur |
|---|---|
| **Définition** | Moyenne des streaks courants de tous les élèves actifs (connectés dans les 7 derniers jours) |
| **Calcul** | AVERAGE des valeurs de la colonne Streak dans `Progress`, filtré sur les élèves actifs (dernière connexion < 7j) |
| **Source** | Onglet `Progress` (Streak) + `Scores` (Date) |
| **Seuil d'alerte** | < 2 → les élèves ne reviennent pas deux jours de suite |

### KPI 4 — Taux de conversion freemium → payant

| Champ | Valeur |
|---|---|
| **Définition** | % des élèves dont l'essai 7j a expiré et qui ont souscrit un abonnement payant |
| **Calcul** | (nb élèves avec Premium=1) / (nb élèves avec TrialStart < aujourd'hui − 7j) × 100 |
| **Source** | Onglet `Users` (Premium, TrialStart) |
| **Seuil d'alerte** | < 10% après 20 essais → revoir le pricing ou le CTA |

### KPI 5 — Churn mensuel

| Champ | Valeur |
|---|---|
| **Définition** | % d'abonnés payants ayant annulé (Premium passé de 1 à 0) ce mois-ci |
| **Calcul** | À implémenter quand Stripe est connecté : compter les événements `customer.subscription.deleted` du mois / abonnés actifs début du mois × 100 |
| **Source** | Webhook Stripe → colonne `Premium` dans `Users` (+ colonne `DateAnnulation` à ajouter) |
| **Seuil d'alerte** | > 15% → problème de valeur perçue ou de contenu |

---

## 4. Dashboard Google Sheet — formules concrètes

Créer un onglet `Dashboard` dans le Sheet. Les formules ci-dessous supposent les colonnes suivantes :
- `Users` : A=Code, B=Prénom, C=Niveau, D=Email, E=PasswordHash, F=DateInscription, G=IsAdmin, H=Premium, I=TrialStart
- `Scores` : A=Code, B=Prénom, C=Niveau, D=Chapitre, E=NumExo, F=Énoncé, G=Résultat, H=Temps, I=IndicesVus, J=FormuleVue, K=MauvaiseOption, L=Draft, M=Date
- `Progress` : A=Code, B=Niveau, C=Chapitre, D=Score, E=NbExos, F=NbErreurs, G=DernierePratique, H=Statut, I=Streak

### Cellules de référence à poser en haut du Dashboard

```
B1  =TODAY()                          (date du jour, pour les calculs relatifs)
B2  =B1-7                             (J-7)
B3  =B1-14                            (J-14)
```

### KPI 1 — Taux d'activation J1 (inscrits cette semaine)

```
=IFERROR(
  COUNTIFS(
    Users!F:F, ">="&B2,
    Users!F:F, "<="&B1,
    Users!A:A, "<>"
  ),
  0
)
```
— Nombre d'inscrits cette semaine (dénominateur), coller en C5.

```
=IFERROR(
  SUMPRODUCT(
    (COUNTIFS(Scores!A:A, Users!A2:A1000, Scores!M:M, ">="&Users!F2:F1000, Scores!M:M, "<="&Users!F2:F1000+1) >= 5)
    * (Users!F2:F1000 >= B2)
    * (Users!F2:F1000 <= B1)
  ),
  0
)
```
— Nombre d'activés J1 parmi les inscrits cette semaine (numérateur), coller en C6.

```
=IFERROR(C6/C5, 0)
```
— Taux d'activation J1, format %, coller en C7.

### KPI 2 — Rétention J7

```
=IFERROR(
  COUNTIFS(Users!F:F, ">="&B3, Users!F:F, "<="&B2),
  0
)
```
— Inscrits entre J-14 et J-7 (dénominateur), coller en C10.

```
=IFERROR(
  SUMPRODUCT(
    (COUNTIFS(Scores!A:A, Users!A2:A1000, Scores!M:M, ">="&B2) >= 1)
    * (Users!F2:F1000 >= B3)
    * (Users!F2:F1000 <= B2)
  ),
  0
)
```
— Parmi eux, ceux qui ont une activité dans les 7 derniers jours (numérateur), coller en C11.

```
=IFERROR(C11/C10, 0)
```
— Rétention J7, format %, coller en C12.

### KPI 3 — Streak moyen (élèves actifs 7 derniers jours)

```
=IFERROR(
  AVERAGEIF(
    Progress!G:G, ">="&B2,
    Progress!I:I
  ),
  0
)
```
— Streak moyen des élèves dont DernierePratique >= J-7, coller en C15. Format nombre, 1 décimale.

### KPI 4 — Taux de conversion freemium → payant

```
=IFERROR(
  COUNTIFS(Users!I:I, "<>"&"", Users!I:I, "<="&(B1-7)),
  0
)
```
— Essais expirés (TrialStart renseigné et > 7j), dénominateur, coller en C18.

```
=IFERROR(
  COUNTIFS(Users!H:H, 1),
  0
)
```
— Abonnés payants actuels (numérateur), coller en C19.

```
=IFERROR(C19/C18, 0)
```
— Taux de conversion, format %, coller en C20.

### KPI 5 — Churn mensuel

```
=IFERROR(
  COUNTIFS(Users!H:H, 0, Users!I:I, "<>"&""),
  0
)
```
— Élèves ayant eu un essai mais Premium=0 (proxy churn avant Stripe), coller en C23.

> Note : la formule churn réelle nécessite une colonne `DateAnnulation` dans Users. À ajouter dès que Stripe est connecté.

### Mise en forme conditionnelle suggérée pour le Dashboard

Appliquer sur les cellules de taux (C7, C12, C20) :
- Rouge si valeur < seuil d'alerte
- Vert si valeur > objectif

---

## 5. Alertes — quand agir immédiatement

### Alerte 1 — Taux d'activation J1 < 30%

**Seuil :** Dashboard C7 < 0.30

**Lecture :** plus de 7 inscrits sur 10 font le diagnostic mais ne reviennent pas le jour même.

**Actions concrètes :**
1. Relire le message affiché après le diagnostic — est-il encourageant ?
2. Vérifier que les chapitres s'affichent bien après le diagnostic (bug silencieux possible)
3. Tester le flux complet inscription → premier exercice sur mobile
4. Ajouter un email de bienvenue automatique envoyé dans l'heure (GAS + Gmail API)

---

### Alerte 2 — Aucune connexion depuis 3 jours pour un élève actif

**Détection :** dans `generateMorningReport()` (GAS, trigger 7h), ajouter ce bloc après la classification :

```js
// Alerte élèves actifs silencieux (≥5 exos total, inactif depuis 3j)
const today = new Date();
const threeDaysAgo = new Date(today - 3 * 86400000);
students.forEach(student => {
  const lastActivity = new Date(student.lastDate);
  const totalExos = student.totalExos;
  if (totalExos >= 5 && lastActivity < threeDaysAgo) {
    // Ajouter dans le corps de l'email de rapport
    alertLines.push(`⚠️ ${student.prenom} (${student.niveau}) — inactif depuis ${Math.floor((today - lastActivity) / 86400000)}j`);
  }
});
```

**Action :** envoyer un email de relance manuel (ou automatique via GAS + Gmail) :
> "Salut [Prénom], ton boost t'attend ! Tu as travaillé [chapitre] la dernière fois — continue sur ta lancée."

---

### Alerte 3 — 3 erreurs 500 consécutives dans les logs GAS

**Détection :** dans le GAS, wrapper tous les `doPost` avec un compteur d'erreurs :

```js
function doPost(e) {
  try {
    // ... code existant
  } catch(err) {
    const props = PropertiesService.getScriptProperties();
    const errorCount = parseInt(props.getProperty('consecutive_errors') || '0') + 1;
    props.setProperty('consecutive_errors', String(errorCount));
    if (errorCount >= 3) {
      GmailApp.sendEmail(
        Session.getActiveUser().getEmail(),
        '[Matheux URGENT] 3 erreurs 500 consécutives',
        `Dernière erreur : ${err.message}\nStack : ${err.stack}`
      );
      props.setProperty('consecutive_errors', '0'); // reset après alerte
    }
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error', message: err.message
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
// Réinitialiser le compteur sur succès
function resetErrorCount() {
  PropertiesService.getScriptProperties().setProperty('consecutive_errors', '0');
}
```

Appeler `resetErrorCount()` au début de chaque action réussie.

**Action :** vérifier dans Apps Script → Exécutions les logs d'erreur, puis redéployer si nécessaire.

---

### Alerte 4 — Streak moyen < 2

**Seuil :** Dashboard C15 < 2

**Lecture :** les élèves ne reviennent pas deux jours de suite en moyenne — la boucle d'engagement est cassée.

**Actions concrètes :**
1. Vérifier que le streak s'affiche bien sur l'écran d'accueil (badge visible, non tronqué)
2. Vérifier que le nudge après 20s d'inactivité fonctionne (`autoNudge()`)
3. Renforcer le message de fin d'exercice : afficher explicitement "Reviens demain pour garder ton streak !"
4. Si la feature email est prête : envoyer un rappel quotidien à 17h aux élèves sans activité du jour

---

### Alerte 5 — 0 conversion après 20 essais expirés

**Seuil :** C19 = 0 quand C18 >= 20

**Lecture :** la valeur perçue ne justifie pas le passage à l'acte d'achat.

**Actions concrètes (dans l'ordre) :**
1. Interroger 3 élèves directement : "Qu'est-ce qui t'empêcherait de payer 9,99€/mois ?"
2. Vérifier que le CTA de conversion s'affiche bien à l'expiration de l'essai
3. Tester une réduction de lancement (ex: 4,99€/mois le premier mois)
4. Ajouter des témoignages réels sur la landing (même 1 suffit)
5. Vérifier que Stripe est correctement configuré et que le paiement ne plante pas

---

*Document créé le 10 mars 2026 — à mettre à jour quand Stripe est connecté (KPI 4 et 5 à affiner).*
