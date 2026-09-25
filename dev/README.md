# Matheux en local (backend de dev)

Tout le site tourne sur **http://localhost:8787** : landing, app, bilan et l'API.
L'API, c'est `supabase/functions/api/index.ts` tel quel. Seul Supabase est remplacé, par une base
en mémoire. **Rien ne part vers la prod** : pas de Supabase, pas de Resend, pas de Stripe, pas de GAS.

## Lancer

```bash
./matheux.sh          # lance le serveur et ouvre le navigateur (Ctrl+C pour arrêter)
./matheux.sh reset    # remet la base à l'état initial (marche aussi serveur lancé)
./matheux.sh test     # smoke test API + test navigateur (Chrome headless : diagnostic, sw.js, bilan.html?confirmer=1)
```

Tu peux aussi double-cliquer sur `Matheux.desktop` (ça ouvre un terminal).
Il faut Deno (`~/.deno/bin/deno`) et python3. Au premier lancement, la base est créée automatiquement.

## Comptes de test

Mot de passe pour tous les comptes : **`matheux-dev`**. Les codes restent les mêmes à chaque reset.

| Qui | Email | Code | État |
|---|---|---|---|
| Admin de dev | admin@dev.matheux.local | ADMDEV | admin (`is_admin`), triple-clic sur le logo |
| Lina | lina@exemple.fr | MDX7DK | vient de s'inscrire, rien fait |
| Tom | tom@exemple.fr | AQPTSK | diagnostic express fait hier en invité puis rattaché à l'inscription, accès gratuit |
| Sarah | sarah@exemple.fr | 6LDHJ5 | Programme Brevet payé, diag complet, 10 jours d'entraînement (streak 10) |

L'admin de dev est fictif (aucune donnée de la prod dans le dépôt). Les comptes élèves ont été créés **en passant par l'API** (register, diagnostic, webhook Stripe signé,
get_training, save_score), avec l'horloge reculée dans le temps. Leur état est donc celui que la
prod produirait avec les mêmes réponses.

Les actions élève exigent le **jeton de session** (`access_token` renvoyé par `login`, `register`, `login_token`) :
`curl localhost:8787/api -d '{"action":"get_carte","code":"AQPTSK"}'` est refusé (`auth_requise`). Tom a fait son
diagnostic express **en invité** (sans compte), rattaché ensuite au `register` : c'est le parcours cible.

## Outils de dev : http://localhost:8787/dev

- **Emails** : http://localhost:8787/dev/outbox (fichiers dans `dev/data/outbox/*.html`). Tout ce qu'index.ts
  envoie à Resend arrive ici, mails de réinitialisation du mot de passe compris.
- **Paiement simulé** : `curl -X POST 'localhost:8787/dev/pay?code=AQPTSK&produit=diag_complet'`
  (ou `programme_brevet`, qui devient `programme_upgrade` à 30 € si le diagnostic complet est déjà acheté).
  Ça envoie un vrai webhook `checkout.session.completed`, signé avec le secret de dev, au chemin Stripe
  d'index.ts. Dans le navigateur, un clic sur un lien `buy.stripe.com` ouvre ce paiement simulé au lieu de Stripe.
- **Séquence emails** (`docs/specs/51-emails.md`) : le cron n'est pas planifié en local. Pour voir ce qui part :
  `curl localhost:8787/api -d '{"action":"cron_send_emails","access_token":"<jeton admin>"}'` (jeton : `login` de
  `admin@dev.matheux.local`), puis `/dev/time?jours=1` et recommencer. La réponse liste `details` (« CODE type → envoyé /
  raison »). Le smoke test fait ça sur 15 jours pour Lina, Tom, Sarah et un profil neuf (Nora, opt-in) et affiche le calendrier.
  Aperçu d'un email pour un élève : action admin `send_test_email {targetEmail, type:"P-X1", code_eleve}`.
- **Service worker** : neutralisé sur `/sw.js` ; le vrai est servi sur `/sw.js?reel=1` (utilisé par `browser_test.ts`).
- **Horloge** : `/dev/time?jours=1` avance d'un jour (pour tester le streak, le lendemain, le re-diagnostic à 30 jours).
  `/dev/time?reset` revient à aujourd'hui. Le décalage est perdu au redémarrage.
- **Base** : `/dev/health` (nombre de lignes par table), `/dev/db/<table>?code=XXX` (lignes en JSON).
  Le fichier est `dev/data/db.json`, ignoré par git.

## Limites du faux backend

- On ne gère que le sous-ensemble de PostgREST et de GoTrue qu'index.ts utilise vraiment :
  filtres eq/neq/gt/gte/lt/lte/is/like/ilike/in/not/or, order, limit/range, count, single/maybeSingle,
  insert/upsert/update/delete, et côté auth : admin users, login par mot de passe, recover.
  Il n'y a pas de rpc, pas de jointures, pas de realtime.
- Le schéma vient de `supabase/schema.sql`, puis `fix_schema.sql`, puis `migrations/*.sql`. Une colonne
  absente de ces fichiers est **refusée**, comme en prod. Un `on_conflict` sans contrainte unique qui
  correspond aussi (erreur 42P10). NOT NULL et unicité sont vérifiés.
- Pas de RLS, pas de clés étrangères, pas de CHECK. À la place, si une requête REST porte le JWT d'un
  élève au lieu de la clé service_role, elle est **rejetée** (DEV_RLS), pour qu'on voie le problème.
- Le paiement ne passe pas par Stripe Checkout : le formulaire, les CGV et la page de succès ne sont pas testés.
- Le service worker est neutralisé en local, pour ne pas garder une vieille version de l'app en cache.
- Ce qui passe par le navigateur (Google Fonts, KaTeX CDN, GA4) sort normalement sur Internet. Ce ne sont
  pas des appels à la prod Matheux.

## Fichiers

`server.ts` (serveur, capture de `Deno.serve` d'index.ts, interception des fetch) · `fake_supabase.ts` ·
`schema.ts` (lecture du SQL) · `seed.ts` (reprend la logique de `supabase/import_referentiel_banque.py`
via python3) · `clock.ts` · `smoke_test.ts` · `browser_test.ts` (puppeteer-core, stocké dans le cache Deno, hors repo).
