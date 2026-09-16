# Refonte 6e→3e, rentrée 2026-2027 (ATTENTE TOKEN)

> Créé le 16/09/2026, session interrompue par une limite de session API (reset 19h20 Paris)
> puis clôturée par Nicolas pour la journée. Ce fichier est le point de reprise : lis-le
> intégralement avant de continuer, avec CLAUDE.md.

---

## Contexte en une phrase

Le repo cloné pointait par défaut sur la branche `root` (obsolète, GAS/Sheets) — la vraie
prod tourne sur `main` (Supabase + Next.js landing + `app.html`). Une fois `main` audité :
le pivot one-shot 29,99€ était déjà en place mais figé sur "Brevet 2026" (date codée en
dur, expirée depuis juin), le produit ne couvrait en réalité que la 3ème, et il n'existait
**aucun algorithme serveur** pour choisir les exercices du boost quotidien — tout passait
par une génération LLM (agent `admin-auto`, 2×/jour). Objectif de la refonte : étendre à
6e-5e-4e-3e, remplacer cette génération quotidienne par une banque + un algorithme
déterministe, et relancer proprement la monétisation déjà validée.

Tout le travail est sur la branche **`feat/refonte-6e-3e-algo`** (pas pushée, pas mergée
sur `main` — rien n'est en prod tant que ce n'est pas décidé explicitivement).

---

## État au 16/09/2026 (fin de session)

### ✅ Fait et commité
- **Monétisation** : bug critique corrigé (`premium_end` codé en dur au 30/06/2026 →
  accès non expirant). 4 Payment Links Stripe créés (6EME/5EME/4EME/3EME, 29,99€,
  `metadata.niveau`), routés depuis `app.html` (`_stripeUrl`) et les emails serveur
  (`templateJ7`/`templateJ14`). Ancien produit dupliqué par erreur (2999€) supprimé
  dans Stripe. **L'ancien lien "jusqu'au Brevet 2026" est encore actif** — à archiver
  dans le dashboard Stripe une fois les 4 nouveaux liens vérifiés en conditions réelles.
- **Algorithme** : nouvelle action `generate_adaptive_boost` dans
  `supabase/functions/api/index.ts` — sélection pondérée par lacune (`progress.score`),
  anti-doublon, zéro LLM. Additive, pas encore branchée en remplacement du flux existant.
  **Pas testée contre de vraies données** (pas de credentials Supabase dans ce repo).
- **Bug de fond corrigé** : `updateConfidenceScore` avait un `onConflict` sur une colonne
  qui n'existe pas (`code,chapitre` au lieu de `code,categorie`) — la table `progress` ne
  se peuplait jamais à la 1ère pratique d'un chapitre. Sans ce fix, tout ciblage de
  lacune (UI existante + nouvel algo) tournait aveugle. Corrigé.
- **Outillage** : `validate_exos.py` ne savait valider que l'ancien format flat, pas le
  format v4 "exercice-parapluie" (4×5 questions) déjà utilisé en prod — chaque banque v4
  remontait 4 fausses erreurs bloquantes. Fixé (`_flatten_v4`), rétrocompatible.
- **Banque d'exercices** (générée, validée `validate_exos.py`, **pas encore importée en
  Supabase** — nécessite les credentials `.env` de Nicolas) :
  - 6EME : 6/13 chapitres ✅ — Nombres_entiers, Fractions, Proportionnalité, Angles,
    Périmètres_Aires, Géométrie
  - 5EME : 5/10 chapitres ✅ — Pythagore, Fractions, Proportionnalité, Calcul_Littéral,
    Nombres_relatifs
  - 4EME : 5/10 chapitres ✅ — Équations, Fractions, Proportionnalité, Calcul_Littéral,
    Puissances
- **Docs nettoyées** : `CLAUDE.md` (branche prod, scope 6e-3e, pricing, §3.7 moteur
  adaptatif, A7 cadence admin-auto), `.claude/agents/matheux.md` (décisions périmées),
  `.claude/agents/admin-auto.md` (2×/jour → réassort mensuel), `docs/product.md` (modèle
  économique).

### ❌ Pas fait / bloqué
- **Banque incomplète** — chapitres restants :
  - 6EME (7) : Nombres_Décimaux, Statistiques_6ème, Symétrie_Axiale, Volumes,
    Agrandissement_Réduction, Conversions_Unités, Puissances_10
  - 5EME (5) : Puissances, Symétrie_Centrale, Transformations, Racines_Carrées,
    Triangles_Semblables
  - 4EME (5) : Pythagore, Fonctions_Linéaires, Inéquations, Homothétie, Sections_Solides
  - 3EME : déjà complet en prod (22 chapitres format Brevet), rien à faire ici
- **Pages SEO** : agent lancé, **0 page produite** (a échoué avant tout écrit à cause de
  la limite de session). Objectif inchangé : 33 pages notion (6e/5e/4e) + 3 pages hub,
  sur le modèle des 5 pages 3e existantes (`pythagore-brevet.html` etc.), maillage
  interne + sitemap.xml.
- **Import Supabase** : aucun fichier `data/bank_*eme/*.json` n'est en base — ce repo n'a
  pas les credentials (`.env` gitignoré). À faire par Nicolas via `supabase_helper.py`.
- **Test réel de l'algorithme** : `generate_adaptive_boost` n'a jamais tourné contre de
  vraies données (ni même contre les profils de test `create_test_profiles.py`).
- **`docs/roadmap.md`** : pas mis à jour (seul `product.md` a été nettoyé) — encore
  centré sur le seul objectif 3ème Brevet.
- Branche pas pushée sur `origin`, pas de PR, rien mergé sur `main`.

---

## Calendrier de reprise — slots quotidiens

> Un slot = une session de travail. Cocher au fur et à mesure. Si une session est
> interrompue par une limite de tokens/session avant la fin d'un slot, reprendre le
> lendemain là où ça s'est arrêté plutôt que de repartir du début du slot.

### Lundi 21/09 — Banque 6EME complète
- [ ] Générer les 7 chapitres 6EME restants (voir liste ci-dessus), format v4, mix
  2 fill + 2 qcm + 1 vf par slot — suivre `docs/prompt-generation-exos.md`
- [ ] Valider chaque fichier (`python3 validate_exos.py data/bank_6eme/<X>.json`)
- [ ] Si Nicolas a fourni les credentials Supabase d'ici là : importer les 13 chapitres
  6EME dans `curriculum` via `supabase_helper.py`

### Mardi 22/09 — Banque 5EME + 4EME complètes
- [ ] Générer les 5 chapitres 5EME restants + 5 chapitres 4EME restants
- [ ] Valider chacun
- [ ] Import Supabase si credentials disponibles (5EME + 4EME)
- [ ] À ce stade : banque 6e→3e complète (54 chapitres) pour la première fois

### Mercredi 23/09 — Cocon SEO 6e/5e/4e
- [ ] Construire/adapter le template des pages notion existantes (3e) en générateur
  réutilisable
- [ ] Générer les 33 pages notion + 3 pages hub (6e/5e/4e)
- [ ] Maillage interne (footer pages ↔ pages, pages ↔ hub, hub ↔ hub, + lien depuis
  `app.html` qui n'existait pas avant)
- [ ] Mettre à jour `sitemap.xml`, corriger au passage le bug JSON-LD FAQPage sans FAQ
  visible sur `pythagore-brevet.html`/`thales-brevet.html`
- [ ] Fusionner `exercices-maths-3eme.html` / `exercices-maths-3eme-brevet.html`
  (cannibalisation SEO déjà identifiée)

### Jeudi 24/09 — Déploiement & tests réels
- [ ] Nicolas : déployer l'Edge Function (`npx supabase functions deploy api`) avec le
  nouveau `generate_adaptive_boost` + les fix (`onConflict`, `premium_end`, niveau Stripe)
- [ ] Tester `generate_adaptive_boost` sur les profils de test
  (`TS1INE/TS2HUG/TS3JAD/TS4ADA`) — vérifier que le ciblage lacune fonctionne et qu'il
  n'y a pas de doublon d'exercice
- [ ] Tester un paiement Stripe réel (mode test) sur chacun des 4 niveaux, vérifier que
  `profiles.premium`/`premium_niveau` se met à jour correctement et n'expire jamais
- [ ] Une fois vérifié : archiver l'ancien Payment Link "Brevet 2026" dans Stripe

### Vendredi 25/09 — QA globale & merge
- [ ] Rejouer `test_full_v2.py`, `test_pipeline_auto.py`, `test_publishdate_proof.py`,
  `check_students.py`
- [ ] Mettre à jour `docs/roadmap.md` (scope 4 niveaux, retirer les objectifs
  "3ème Brevet only" obsolètes)
- [ ] Revue de la branche `feat/refonte-6e-3e-algo`, décision de merge sur `main`
  (déploiement GitHub Pages automatique dès le merge — à faire consciemment, pas par
  accident)
- [ ] Si merge : premier lot de relance (emails/annonces vers la base existante si elle
  existe, sinon reprise du plan growth Phase 0/1 de `.claude/agents/growth.md` — mais ce
  fichier date de la branche `root`, à vérifier s'il a un équivalent sur `main`)

### Semaines suivantes (non planifiées jour par jour)
- Contenu éditorial récurrent (1-2 articles/mois façon `comment-reviser-brevet-maths.html`)
- Niveau 1ERE (10 chapitres, marqué "expérimental" — backend prêt, jamais priorisé)
- Décision sur le pack "collège complet" multi-niveaux vs prix séparé (actuellement :
  prix séparé par niveau, décision de Nicolas du 16/09)
- Le diagnostic comme aimant à leads partageable (profil d'apprentissage) — idée posée le
  16/09, pas commencée
