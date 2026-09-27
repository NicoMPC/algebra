# 80 — Matrice QA « persona × moment »

> Agent qa-parcours · 26/09/2026 · branche `feat/diagnostic-3e`. Script : `dev/qa_matrice.ts`.
> Objectif : quel que soit l'état de l'utilisateur (droits, jour, séance), la suite du site est cohérente.

## Relancer

```bash
deno run -A dev/qa_matrice.ts            # matrice seule (~4-5 min, serveur isolé port 8795, base temporaire)
deno run -A dev/qa_matrice.ts "parent"   # seulement les cases dont le nom contient « parent »
QA_SHOTS=/tmp/qa-shots deno run -A dev/qa_matrice.ts   # + captures 375 px pleine page
./matheux.sh test                        # smoke + navigateur + matrice + e2e visiteur (si serveur lancé)
```

Les états sont construits **par l'API** (register, diagnostic, `save_score` comme l'app, `/dev/pay`,
`/dev/time`), puis la page est ouverte dans Chrome headless (375 px) avec la session injectée dans
`boost_v23`. Quand l'horloge serveur est avancée, celle du navigateur l'est aussi.

**Contrôles communs à chaque écran ado** : 0 erreur console / JS / HTTP ≥ 400 ; aucun bouton d'achat
(`€`, « acheter », « obtenir », « choisir le programme », « offrir »… — contrat §7) ; jamais « ton prof /
prépare la suite » ; pas de `undefined`/`NaN` ; pas de scroll horizontal.

## Matrice (37 cases — état au 26/09 : 37/37 ✅)

| Persona | Moment / état | Résultat |
|---|---|---|
| Invité | diag en cours → rechargement → reprise proposée | OK |
| Invité | express fini sans compte → carte partielle, « M'entraîner gratuitement », « Envoyer à mes parents » | OK |
| Gratuit | J0 séance pas faite → séance prête + chip Gratuit ; paywall ado sans achat ; vue parent 19/49 € | OK |
| Gratuit | J0 séance faite → « Séance faite », pas de « C'est parti », 🎯 5/5 | OK (après fix harnais) |
| Gratuit | séance commencée 2/5 → « Continue, encore 3 exos » | OK |
| Gratuit | dernier exo dans l'app → écran de fin + « Voir ce qui est inclus » sans achat | OK |
| Gratuit | J+1 / J+7 / J+31 → nouvelle séance, pas de check-up | OK (voir bug 2) |
| Gratuit | zone maîtrisée → « Ton point faible est réglé », partage sans prix | OK |
| Gratuit | compte sans diagnostic → « Lancer mon diagnostic » | OK |
| Diag complet | retour `?achat=diag_complet` → « Diagnostic complet débloqué » → hub | OK |
| Diag complet | avant les modules : chip, carte « 3 modules », pas de « pas encore mesurées » ; clic chip | **corrigé** (bug 1) |
| Diag complet | pendant (module 1 fait) → accueil « Module 2 / 3 », hub « Fait ✓ » | OK |
| Diag complet | après les 3 modules → carte complète, PDF généré (≥ 4 pages) | OK |
| Diag complet | séance faite après le complet → fin de séance sans « pas encore mesuré » | **corrigé** (bug 1) |
| Diag complet | J+31 → pas de check-up promis | OK |
| Programme direct | retour `?achat=programme_brevet` → « Programme Brevet activé » | OK |
| Programme direct | J0 : pas de chip, diag complet inclus, « S'entraîner sur… » lance 5 exos, aucun paywall | OK |
| Programme | séance faite → « Check-up dans N jours » | OK |
| Programme | J+31 → « Check-up du mois » lançable ; fini → carte « Depuis ta dernière carte » | OK |
| Upgrade | page parent (diag payé) → Programme 30 € « au lieu de 49 € », plus de vente du diag | OK |
| Upgrade | paiement → `programme_upgrade`, `?achat=programme_upgrade`, « S'entraîner sur… », page parent sans offre | OK |
| Parent `bilan.html` | lien gratuit → 19 € + 49 €, vouvoiement, aperçu PDF sans erreur | OK |
| Parent | lien diag payé → pas de 2e vente du diag · lien Programme → aucune offre | OK |
| Parent | lien révoqué / expiré (J+31) / inconnu → « n'est plus actif », sans prénom si inconnu | OK |
| Parent | `?merci=1` → bandeau paiement enregistré | OK |
| Parent | `?confirmer=1` (déjà couvert par `dev/browser_test.ts`) + case emails ado | **ajouté** (point 2 audit) |
| Admin | monitoring lecture seule + fiche élève, pas de séance | OK |
| Autre appareil | connexion email + mot de passe → accueil, carte, séance | OK |
| Session | jeton expiré + refresh valide → renouvelée ; jetons invalides → diag/connexion, pas d'écran vide | OK |
| Prix | 19/49/30 identiques API (`MX_PRODUITS`), `OFFRE` app + bilan, emails ; pas de 29,99 € ; pas de re-test ; brevets blancs jamais présentés comme disponibles | OK |
| Emails | inscription UI avec « Ton email (facultatif) » → parent l'autorise sur `?confirmer=1` · sans la case → adresse effacée | **ajouté** |
| Emails | `?src=email_*` → `funnel_events.email_click` (app connecté, app anonyme, bilan) ; `src` arbitraire refusé | **ajouté** |

## Bugs trouvés et corrigés

1. **CTA d'achat côté ado (contrat §7)** — un acheteur du seul diagnostic qui touchait sa chip
   « Diagnostic complet ✓ » (ou « Voir ce qui est inclus » en fin de séance) tombait directement sur la vue
   parent avec « Choisir le Programme Brevet · 30 € ». → `openPaywall` montre maintenant à l'ado
   `_paywallProgrammeAdo` (ce que le Programme ajoute, prix cité une fois, « décision pour tes parents »,
   partage + lien « Je suis le parent »). Fin de séance : texte selon l'état (« le reste n'est pas encore
   mesuré » seulement en gratuit ; diag payé non fait → bouton « Mon diagnostic complet → »).
2. **Jour client ≠ jour serveur** — `tod()` utilisait le fuseau du navigateur, le serveur `todayParis()`.
   Hors fuseau Paris (DOM-TOM, étranger, ou appareil mal réglé), la séance du jour pouvait s'afficher
   « faite » avec la veille, ou refaite. → `tod()` renvoie le jour de Paris (repli local).
3. **P0 légal/sécurité (audit emails 53 §4)** — `set_preferences` laissait l'ado connecté poser
   `consentement_parent` et `optin_marketing`. → refusé (`refuse: true`) ; seul `confirm_parent` (lien du
   mail parent) les pose. L'ado peut encore **retirer** l'opt-in (`optin_marketing: false`). Test d'attaque
   dans `dev/smoke_test.ts` (« attaque : set_preferences … → refusé, rien écrit »).
4. **Emails ado jamais envoyés** — `email_eleve` n'était demandé nulle part. → champ « Ton email à toi
   (facultatif) » dans la feuille d'inscription (E5), enregistré par `set_preferences` **avant** la
   confirmation parentale seulement (après : refusé, c'est le parent qui décide ; jamais l'email du parent).
   Sur `bilan.html?confirmer=1`, case 52 §4.2 « J'autorise Matheux à envoyer à {prénom}, sur l'adresse
   m•••@…, des rappels d'entraînement » (champ adresse si l'ado n'en a pas mis). `confirm_parent
   {autoriser_eleve, email_eleve}` : case non cochée → adresse effacée ; cochée → case `emails_eleve`
   journalisée dans `consentements`. Smoke : A-X0 part bien à Nora.
5. **Clics email non mesurés** — `?src=email_*` → `log_funnel_event {event:'email_click', meta:{src, page}}`
   depuis `app.html` (3 s après le boot : code rattaché seulement si la session est prouvée) et `bilan.html`
   (code prouvé par le jeton de partage). Aucun cookie. `src` validé `^email_[\w-]{1,40}$`.
6. **Alignement légal (26/09)** — brevets blancs présentés « (bientôt) » / « corrigé compétence par
   compétence » / listés comme inclus sur `bilan.html` → « ils arrivent en cours d'année » partout ;
   aucune promesse de re-test (vérifié app, bilan, emails) ; `CONSENT_VERSION` app = `2026-09-26`,
   `textes_version` bilan = `bilan-2026-09-26`.
7. Au passage : `deno check` de `dev/e2e_parcours.ts` (référence `lib dom` manquante).

Faux positifs du harnais corrigés (pas des bugs produit) : `innerText` renvoie le texte en majuscules
CSS (tests insensibles à la casse), `save_score` doit être envoyé comme l'app (`categorie: BOOST`,
`exercice_idx` = rang), prix des emails au format « 19,00 € ».

## ❓ Points ouverts pour Nicolas

1. **Liens Stripe 49 € et 30 € toujours vides** : dans l'app et sur `bilan.html`, les boutons Programme
   mènent à « Paiement bientôt disponible : écrivez-nous ». Cohérent mais c'est une impasse commerciale.
   → Reco : créer les 2 Payment Links (REPRISE.md §2) ; aucune autre modif nécessaire.
2. **« Je suis le parent » dans le paywall ado** ouvre la vue d'achat sur l'appareil de l'ado (50 §2.3).
   C'est un lien discret, pas un CTA, mais c'est le seul chemin d'achat depuis l'app. → Reco : garder.
3. **Admin** : le monitoring ne distingue que « Programme » ; les acheteurs du seul diagnostic n'ont pas de
   badge (les données `achats` sont déjà renvoyées par `get_admin_overview`). → Reco : ajouter un badge
   « Diagnostic » (5 lignes), si utile.
4. **Email ado après confirmation** : si le parent a déjà confirmé, ni l'ado ni le parent ne peuvent ajouter
   l'adresse ado ensuite (pas de page réglages parent). → Reco : acceptable en v1.
5. **Jour de référence = Paris** pour tous (DOM-TOM : la séance change à minuit heure de Paris). → Reco : ok.
6. **Durée** : la matrice prend ~4-5 min ; `./matheux.sh test` complet ~8 min.
