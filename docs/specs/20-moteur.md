# 20 — Moteur adaptatif « Diagnostic 3e » (livrable ingénieur adaptatif)

> Statut 24/09/2026 : implémenté dans `supabase/functions/api/index.ts` (bloc `MOTEUR_PUR_DEBUT…FIN` = logique pure,
> puis couche I/O), migration `supabase/migrations/20260924_diagnostic_3e.sql`, tests `supabase/tests/moteur_test.ts`
> (6/6 verts sur mini-référentiel ET référentiel réel 121 compétences). **Rien n'est déployé.**
> Contrat : `00-contrat-commun.md` §3 (items), §4 (maîtrise), §5 (Carte), §7-8 (décisions Nicolas).

## 0. Principes

- **Zéro humain, zéro LLM au runtime.** Tout est déterministe : mêmes réponses → même carte, même séance
  (seul le tirage d'items entre ex æquo varie par élève via un hash `code|item`, pas de `Math.random`).
- **Jamais de conclusion sur une seule réponse** (≥ 2 observations, 3 pour une lacune au complet).
- **On remonte aux causes** : échec sur une compétence de 3e → on descend dans ses prérequis (distance ≤ 2).
- **Le graphe est lu depuis la table `competences`** : le moteur ne connaît aucun id en dur, sauf la liste
  `MX_HORS_DIAG` (hors programme, contrat §8), doublée de la colonne `competences.diag_autorise`.
- Tous les paramètres sont dans l'objet `MX` (index.ts) : seuils, budgets, intervalles de révision. Les prix sont
  dans `MX_PRODUITS` (seul endroit).

## 1. Données

Voir `docs/database.md` (section « Refonte Diagnostic 3e ») et la migration. En bref :
`competences` (référentiel) · `items` (banque, `item_json` = item complet du contrat §3) · `maitrise`
(élève × compétence) · `diagnostics` (sessions + `etat_json` pour la reprise + `carte_json`) · `reponses_items`
(journal) · `achats` (droits) · `funnel_events`, `bilan_partages`, `consentements`, `email_logs` (growth/UX).

Chargement : référentiel + items actifs mis en cache 5 min dans l'instance (`mxChargerRef`). Items exclus du
service unitaire : `depend_question_precedente: true` (uniquement dans leur problème Brevet complet, v1.1).

## 2. Correction des réponses (serveur)

Le diagnostic n'affiche aucune correction, donc c'est le serveur qui juge (`mxCorriger`) :
- normalisation = portage exact de `_normFill` (app.html), moins Unicode et préfixe `x=` compris ; égalité texte,
  vrai/faux ↔ oui/non, `alt[]`. Les 18 cas de `supabase/tests/fill_match_node.js` donnent le même verdict côté serveur ;
- égalité numérique **stricte** (même règle que le correctif `_toNum` du 24/09) : nombre entier/décimal, fraction
  `a/b`, pourcentage `25 %`, unité courante tolérée en fin (`12 cm`). Jamais de `parseFloat` sur une entrée libre :
  « 4x+3 » ≠ « 4x+12 » ;
- erreur type : la réponse est comparée à chaque clé de `err` avec la même normalisation (clés brutes « 2,50 »,
  `\sqrt{10}`, « 3/15 » acceptées) → id d'erreur ;
- réponse vide = « je ne sais pas » = échec sans erreur type.

## 3. Modèle de maîtrise (contrat §4)

Par élève × compétence : loi Beta(α, β), prior Beta(1,1) (maîtrise initiale 0,5, sans avis).
Après chaque réponse (diagnostic **et** entraînement, et chapitres legacy si l'exo porte `comp`) :

```
α ← 1 + (α − 1)·0,9 + (succès ? w : 0)      β ← 1 + (β − 1)·0,9 + (échec ? 1 : 0)
maîtrise = α / (α + β)
```
- **Oubli 0,9** : les anciennes réponses pèsent de moins en moins (fenêtre effective ≈ 10 réponses) : la maîtrise suit
  les progrès de l'entraînement.
- **Poids d'un succès `w`** (limiter le hasard QCM) : fill = 1 ; QCM à k options = 1 − 1/k (3 options → 0,67) ;
  V/F = 0,5. Un échec vaut toujours 1. EASY (1er essai) = succès ; indices / erreur / « je ne sais pas » = échec (P8).
- Conséquence : 2 fill justes → acquis (0,74) ; 2 QCM justes → fragile (0,69), il faut une 3e preuve.
- Statut : ⚪ `non_evalue` (n_obs < 2) · 🔴 `lacune` (< 0,4) · 🟠 `fragile` (0,4-0,7) · 🟢 `acquis` (> 0,7).
- `erreurs_vues` : compteur par id d'erreur type (depuis `item.err`).
- **Erreur d'un prérequis direct** (contrat §9, ex. oublier la racine dans une réciproque de Pythagore → `EG.PYTH.01#…`) :
  l'observation d'erreur est **imputée au prérequis** (échec + `erreurs_vues` sur le prérequis, `mxImputer`), en plus de
  l'échec sur la compétence de l'item. En diagnostic, c'est une observation de session du prérequis (piste de cause racine).
- **Répétition espacée** (Leitner) : succès sur un acquis → révision à +2, 4, 8, 16, 32 jours (`boite` 0→4) ;
  échec sur un acquis → boîte 0, révision le lendemain.

## 4. Diagnostic adaptatif

### 4.1 Algorithme commun (`mxProchaineQuestion` / `mxEnregistrerReponse`)

État sérialisable (`diagnostics.etat_json`) : modules, observations de la session, pile de descente, compétence ouverte,
question en attente, décisions (`fermees`). À chaque appel :
1. une compétence est **ouverte** → on lui pose un nouvel item (voir 4.4) ;
2. sinon on dépile la **descente** (prérequis à explorer) ;
3. sinon la **cible suivante** du module (compétences de 3e triées par poids Brevet ↓, puis nb de prérequis ↓) ;
4. rien à faire ou budget du module épuisé → fin du module (`fin_module`, reprenable), puis fin du diagnostic.

**Décision sur une compétence** (évaluation de session, sans oubli) : on ferme dès que n ≥ 2 et maîtrise > 0,7
(acquis) ou < 0,4 (lacune, avec `minObsLacune` observations) ; sinon on continue jusqu'à `maxObs` puis on ferme
« fragile ». Garde-fou étourderie : si un **dépendant direct** vient d'être jugé acquis, conclure « lacune » exige une
observation de plus.

**Descente (cause racine)** : uniquement à partir d'un échec sur une compétence de **3e** (reco didacticien), ou en
poursuivant une descente déjà commencée : lacune, ou fragile avec maîtrise < `seuilDescente`. On empile les
prérequis directs non encore conclus (le plus structurant, poids + dépendants proches, en premier), profondeur max 2.
Succès → on passe à autre chose (les prérequis d'un acquis sont présumés, non testés).

### 4.2 Express (~15 q, ~8 min, gratuit)

| Paramètre | Valeur |
|---|---|
| Budget | 15 questions, 1 module |
| Cibles | 1 par domaine (la plus lourde au Brevet) = 5 cibles ; un domaine sans compétence de 3e (AP dans le référentiel réel) prend ses compétences du plus haut niveau |
| Phase 1 balayage | 2 questions par cible (≈ 10 q) → **5 domaines colorés** |
| Phase 2 descente | on creuse la lacune la plus lourde (poids × (1 − maîtrise)), jusqu'à 3 q par prérequis, profondeur 2 → **1 point faible détaillé** |
| Reste du budget | autres cibles 3e (bonus) |

### 4.3 Complet (≤ 64 q, ~40 min, 3 modules reprenables, payant)

Modules : **M1 = NC** (24 q) · **M2 = DF + AP** (20 q) · **M3 = EG + GM** (20 q). Entre deux modules la réponse porte
`fin_module` : l'élève peut s'arrêter, `start_diagnostic` reprend exactement où il en était (question en attente
comprise). Descente immédiate, `maxObs` 3 sur une cible et 4 sur un prérequis, lacune seulement après 3 observations,
descente aussi sur un fragile < 0,6.
**Graines** : les réponses de l'express sont reprises (hors budget). Ce qui est conclu n'est pas reposé ; la descente
reprend là où l'express l'a laissée.
Critère d'arrêt : budget du module ou plus rien à explorer (un très bon élève finit en ~13 q sur le mini-référentiel).

### 4.4 Choix de l'item (déterministe)

Parmi les items de la compétence marqués `diag` (repli : tous), jamais un item déjà posé dans la session, en évitant
ceux déjà vus par l'élève : niveau visé `lvl 2` pour une compétence de 3e, `lvl 1` pour un prérequis ; après un
**succès en QCM/VF, on confirme par un fill** ; léger avantage aux fill en général ; ex æquo départagés par hash
`code|item`. Envoyé au client **sans** `a`, `alt`, `err`, `steps`, `f` ; options mélangées de façon déterministe.

### 4.5 Re-diagnostic mensuel (Programme Brevet)

`type: "mensuel"`, 20 q : cibles = 8 premières priorités actuelles + 4 acquis les plus anciens (vérification) +
4 compétences de 3e jamais évaluées. `get_training` renvoie `rediagnostic_du: true` 30 jours après le dernier
complet/mensuel. La carte produite porte `evolution` (`score_avant`, `score_apres`, changements de statut).

### 4.6 Fiabilité (élève qui répond au hasard)

`carte.fiabilite = {niveau, reponses_rapides, inversions}` : ≥ 40 % de réponses en < 4 s, ou > 34 % d'**inversions**
(prérequis en lacune mais dépendant acquis) → `faible` + `carte.alerte` (« refaire au calme »). Testé : 100 % des
élèves « hasard » détectés, 0 faux positif sur les autres profils.

## 5. Carte (contrat §5, sortie de `mxCalculerCarte`)

Champs du contrat + compléments demandés (PDF, UX) :
- `competences[]` (compétences observées) : `id`, `titre`, `titre_eleve`, `domaine`, **`niveau_origine`**, `statut`,
  `maitrise`, `n_obs`, `cause_racine`, `racine_profonde`, `bloque[]`, `erreurs[]` = `{id, libelle,`
  **`libelle_parent`, `remediation`**, `n, exemple: {q, reponse_eleve, a}}` (copiés du référentiel).
- **Cause racine** : compétence en lacune qui est prérequis (distance 1 ou 2) d'une autre compétence en lacune.
  `racine_profonde` : aucun prérequis proche en lacune. `bloque` : dépendants proches (≤ 2) en lacune ou fragiles.
- **Priorités** : score = (1 − maîtrise) × facteur × impact, facteur 2 (cause racine profonde) / 1,5 (cause racine) / 1 ;
  impact = poids Brevet + (si cause racine) somme des poids de ce qu'elle bloque. Puis tri topologique : un prérequis
  **en lacune** passe toujours avant ce qu'il débloque.
- `point_faible` : 1re priorité qui est une cause racine, sinon 1re lacune, sinon 1re priorité.
- `zone_gratuite` : prérequis proches fragiles/lacunes du point faible + point faible + ce qu'il bloque.
- `domaines[]` : `maitrise` = taux pondéré par le poids Brevet (acquis 1, fragile 0,5, lacune 0) des compétences
  évaluées, `statut`, `n_comp`, `n_evalues`, `n_lacunes`. `score_global` = même taux sur les compétences de 3e évaluées
  (la moyenne brute des maîtrises était plafonnée ~74 % pour un élève parfait à cause du prior).
- `plan_4_semaines` : les priorités par paquets de charge 2 (lacune = 1, fragile = 0,5) ; semaine sans priorité =
  « entretenir les acquis, sujets type Brevet ».
- `points_forts` : 5 acquis, 3e d'abord, poids Brevet ↓.
- **`phrase_cle`** et `message_parent` : gabarits déterministes à partir de la cause racine principale. Aucun texte ne
  laisse croire qu'un humain analyse l'élève (vérifié par test).
- `fiabilite`, `alerte` (4.6), `evolution` (mensuel).
- En accès **free**, `get_carte` masque : seul le point faible est détaillé, les autres compétences ne gardent que
  `id/domaine/statut` + `masque: true`, 1 priorité, semaine 1 du plan.
- Compatible `MatheuxBilanPDF.render` (`30-pdf.md` §2) : exemples dans `supabase/tests/fixtures/carte_exemple_*.json`.

## 6. Entraînement quotidien (`mxChoisirEntrainement`, action `get_training`)

5 exos par jour, calculés à la demande et **disponibles immédiatement** (G16 abandonné pour le contenu algo, décision
du 24/09). Idempotent : 1 ligne `daily_boosts` par jour (l'app sait déjà rendre un boost ; `save_score` source BOOST
incrémente `exos_done`). Chaque exo porte `item_id`, `comp`, `role`.

| Rang | Rôle | Choix |
|---|---|---|
| 1 | `reussite` (échauffement) | un acquis, le moins récemment vu, lvl 1 (à défaut : le focus en lvl 1) |
| 2-3, 5 | `travail` | les 2 compétences du **focus** (motif 0,0,1,0,1) ; lvl 1 si lacune, 2 si fragile |
| 4 | `revision` | l'acquis dont la révision espacée est due depuis le plus longtemps |

**Focus** = priorités de la carte filtrées :
- *maîtrise d'abord* : une compétence n'est « prête » que si aucun de ses prérequis proches du périmètre n'est en
  lacune ou fragile (repli : pas de prérequis en lacune) ; une priorité bloquée **fait remonter** le prérequis qui la
  bloque ;
- *continuité* : ce qui a été travaillé ces 3 derniers jours reste au focus jusqu'à « acquis » ;
- tout est acquis → **découverte** de compétences de 3e non évaluées (diagnostic continu) ;
- complément si la banque manque : révisions dues, entretien des acquis, zone.

Items : jamais vu > vu il y a longtemps ; pénalité pour un item réussi il y a < 14 jours ; **jamais un item vu il y a
< 3 jours**. Si la banque ne suffit pas pour 5 items distincts : entretien de points forts (même hors zone), puis en
tout dernier recours reprise d'items de la zone, et `banque_insuffisante: true` dans le boost (à remonter au
concepteur d'items). Sur la banque réelle actuelle (médiane 6 items « train » par compétence, `NC.REL.02` : 3),
≈ 1/3 des séances simulées sont signalées : **viser ≥ 15 items « train » par compétence prioritaire**.
**Périmètre** : `free` et `diagnostic_complet` = `zone_gratuite` de la dernière carte ; `programme_brevet` = toute la
carte. Gratuit = 5 exos/jour sans limite de durée. `zone_maitrisee: true` quand toute la zone est acquise (le front
propose alors de montrer la carte aux parents, sans prix côté ado).

## 7. Droits d'accès (`mxDroits`, serveur uniquement)

| Accès | Obtenu par | Donne |
|---|---|---|
| `free` | défaut | express, carte partielle, 5 exos/jour sur la zone du point faible |
| `diagnostic_complet` | achat `metadata.produit=diag_complet` (19 €) | + diagnostic complet, carte complète, PDF |
| `programme_brevet` | `programme_brevet` (49 €) ou `programme_upgrade` (30 €), **ou `profiles.premium` legacy non expiré** | + entraînement sur toute la carte, re-diagnostic mensuel, brevets blancs (v1.1) |

Webhook Stripe : `client_reference_id` = **code élève** (repli email), `metadata.niveau` seul pour le niveau (plus de
repli sur `client_reference_id`), achat tracé dans `achats` (session, montant, offre). `diag_complet` ne passe pas
`premium` à true ; programme → `premium = true` (l'app actuelle reste cohérente). Sans `metadata.produit` : comportement
legacy inchangé. Le client ne fait jamais foi : chaque action recalcule les droits.

## 8. API (Edge Function, `{status: 'success'|'error'}`)

| Action | Entrée | Sortie |
|---|---|---|
| `start_diagnostic` | `code, access_token, type` · **sans code** : invité (§8 bis) | `diagnostic_id, question` (sans réponse), `progression`, `repris` ; refus `paywall` si non débloqué |
| `answer_diagnostic` | `code, access_token, diagnostic_id, item_id, reponse, temps?` (ou `diagnostic_id, guest_token, …` en invité) | question suivante ou `fin_module` ; à la fin `carte` (masquée selon droits) + `corrections` (récap). **Aucune correction avant la fin** |
| `get_carte` | `code, access_token, diagnostic_id?` | dernière carte (masquée, titres gardés, `non_mesurees`), `droits`, `streak`, diagnostics `en_cours` |
| `get_training` | `code, access_token, comp?` | `boost` du jour (5 exos + `err_libelles`, `focus_titres`, `pourquoi`), `rediagnostic_du`, `zone_maitrisee`, `streak`, `droits` ; avec `comp` : entraînement libre Programme (hors quota, n'écrit pas `daily_boosts`) |
| `get_acces` | `code, access_token` | `droits`, `produits` (prix en centimes : 1900 / 4900 / 3000 upgrade) |
| `set_preferences` | `code, email, email_eleve?, optin_marketing?, date_brevet_blanc?, consentement_parent?` | — |
| `log_consent` | `code, produit, texte_version, texte_hash, cases[]` | — (table `consentements`) |
| `log_funnel_event` | `event` ∈ {paywall_view, checkout_click, pdf_open, share_opened_app}, `meta` | — (les autres événements sont loggés côté serveur) |
| `create_share` / `revoke_share` | `code, canal?` / `code, token?` | `token`, `url` = `https://matheux.fr/b/<token>`, expiration 30 j |
| `get_bilan_partage` | `token` (**public**) | carte réduite (sans réponses ni email), `og {title, description}` pour WhatsApp, `code` (pour `client_reference_id`), `prix_cents` |
| `save_score` / `save_scores_batch` | + `item_id` (ou `comp`, `type`, `nbOptions`) facultatifs | maîtrise mise à jour ; sans ces champs, comportement inchangé |

**Toutes** les actions élève ci-dessus exigent `access_token` depuis le 25/09 (voir §8 bis). Contrats exacts :
`docs/specs/41-integration-log.md` section « Besoins API ».

### 8 bis. Ajouts du 25/09 (Besoins API 1-10, journal d'intégration)

- **Sécurité** : helper unique `mxSessionUid` (jeton → `auth.getUser`), utilisé par `mxAuth` (élève : le jeton doit
  appartenir au profil du `code` ; lecture admin autorisée sur `get_carte`, `get_acces`, `get_progress`,
  `check_trial_status`, `generate_adaptive_boost`) et par `requireAdmin` (garde centrale `ADMIN_ONLY`, 12 actions,
  même liste que le hotfix prod `4fc6123`). Refus = `{status:'error', auth_requise:true}`. `cron_send_emails` :
  `cron_send_emails {cron_secret}` (secret `CRON_SECRET`) ou jeton admin. Correctifs de l'audit prod du 11/04 portés
  (whitelist du prénom, erreurs d'upsert `scores` remontées, `progress` recalculé depuis `scores`, `free_chapter`
  pondéré, `send_admin_email`, `targetCode`).
- **Sessions** : `register` et `login` renvoient `access_token`, `refresh_token`, `expires_at` ; `login_token`
  (auto-login sans hash de mot de passe) et `refresh_session`.
- **Diagnostic invité** : table `diagnostics_invites` (jeton hashé, expiration 2 j). Maîtrise calculée en mémoire
  (`mxMaitriseDepuisObs`, bloc pur) ; `register {diagnostic_id, guest_token}` crée la ligne `diagnostics`, rejoue les
  observations (`maitrise`, `reponses_items`), recalcule la carte avec le prénom, puis vide la copie invitée.
- **Séance** : `err_libelles` par exo (`mxErrLibelles`), `focus_titres`, `pourquoi` (`mxPourquoi` : cause racine >
  erreur type vue > statut, + révision ; tutoiement, aucun humain cité). Séance libre : `source: "LIBRE"` dans
  `save_score` (contexte `train`, pas de `progress` legacy, Programme seulement).
- **Email P-X0** au parent (remplace `templateJ0`) : à la fin de l'express si le compte existe, sinon au `register` qui
  rattache un diag invité terminé. Dédup `email_logs` `D3:P-X0`, UNSUB respecté, lien `/b/<token>` (partage
  `canal = email_parent`) et `?confirmer=1` → action publique `confirm_parent {token, optin_marketing?}`.
- **Admin** : `get_admin_overview` ajoute `diagnostics` (+ `diagnostics_stats`), `invites`, `achats`, `ca_cents`, `funnel`.
- Tests : `supabase/tests/besoins_api_test.ts` (fonctions pures), `dev/smoke_test.ts` (parcours + attaques HTTP).

Streak (`mxStreak`) : jours avec ≥ 1 réponse (`reponses_items` + `scores`), gel d'1 jour par fenêtre de 7 (G3),
streak conservé tant que la journée n'est pas finie.

## 9. Ce qui change pour l'existant

- **P5 (assignation manuelle) et A7 (admin-auto)** : remplacés pour les nouveaux comptes 3e par `get_training`. Les
  actions `publish_admin_*` et `suivi` restent en place (admin read-only, décision 24/09) mais ne sont plus nécessaires.
- **G16 (J+1)** : abandonné pour le contenu sélectionné par l'algo (banque validée, pas de contenu fraîchement généré).
- **P1 (diagnostic 5 QCM)** : `generate_diagnostic` legacy intact ; le nouveau diagnostic utilise aussi des fill
  (corrigés serveur), plus fiables contre le hasard.
- **T1-T4 (freemium chapitre)** : `free_chapter` est encore renseigné avec le chapitre legacy du point faible
  (`chapitres_legacy[0]`) pour que l'app actuelle reste cohérente pendant la transition.
- **Chapitres legacy** : les sous-questions v4 reçoivent un `comp` (mapping didacticien) ; si l'app envoie ce `comp`
  dans `save_score`, la maîtrise se met à jour (contexte `legacy`). Anciens comptes supprimés (décision 24/09) :
  aucune migration de données élève (`supabase/purge_anciens_comptes.sql`, à lancer au déploiement).
- `generate_adaptive_boost` (algo v1 par chapitre) : conservé, non utilisé par le nouveau parcours.
- Messages « ton prof prépare la suite » (M7/G11) : à retirer côté app (lot UX).

## 10. Résultats des tests (`deno test --allow-read --allow-write supabase/tests/moteur_test.ts`)

Élèves simulés (probabilité de savoir par compétence, erreur type ou devinette sinon, apprentissage +0,07 par exo si
les prérequis sont là). Moteur déterministe, élève aléatoire → **campagnes de graines** : invariants durs vérifiés sur
chaque exécution, résultats en taux.

| Mini-référentiel (19 comp., 20 graines) | Taux |
|---|---|
| Relatifs : point faible express = relatifs / priorité n°1 complet = relatifs / cause racine identifiée | 100 / 100 / 100 % |
| Relatifs : ≥ 60 % du travail J1-5 sur les relatifs / REL.01+REL.02 acquis à J30 / gratuit : point faible acquis J30 | 100 / 95 / 100 % |
| Bon élève 1 trou : priorité n°1 = FRAC.03 / FRAC.03 acquis à J30 | 95 / 95 % |
| Hasard : fiabilité « faible » + alerte / score < 40 | 100 / 100 % |
| Moyen : priorité n°1 en 4e/3e (pas les bases) / lacunes en baisse à J30 | 100 / 100 % |

**Banque réelle** (846 items, vrais énoncés et clés `err`) : 100 % des réponses attendues reconnues par le correcteur
serveur ; `NC.REL.02` dans le top 3 des priorités et erreur type nommée ≥ 80 % ; hasard détecté 100 %.
**PDF** : `supabase/tests/carte_pdf_test.ts` passe les cartes du moteur dans `MatheuxBilanPDF.render` (jsPDF réel) :
complet 9 pages, aperçu express 3 pages, polices intégrées.

Référentiel réel (121 comp., 10 graines) : 5 domaines colorés en express 100 % ; `NC.REL.02` cause racine 90 % et
acquise à J30 100 % ; `NC.FRAC.02` trouvée chez le bon élève 90 % ; hasard détecté 100 %. Mensuel : score en hausse
100 %. Invariants durs : jamais de statut sur < 2 obs, cause racine toujours en lacune avec une lacune à distance ≤ 2,
express ≤ 15 q, complet ≤ 64 q en 3 modules, 5 exos/jour sans doublon, jamais de travail sur une compétence dont un
prérequis proche est en lacune, zone gratuite respectée, item jamais resservi avant 3 jours, hors programme jamais
en diagnostic, sous-questions dépendantes jamais servies seules, déterminisme.

## 11. Limites connues

- **Couverture du complet sur le référentiel réel** : 64 q concluent ~30 compétences sur 121 (49 de 3e). Les poids
  faibles restent « non évalués » et sont découverts à l'entraînement. Pour tout couvrir il faudrait ~90-100 q.
- La maîtrise ne met à jour que la compétence principale (`comp_secondaires` ignorées).
- Double comptage possible si l'app renvoie deux fois le même `save_score` (dédup `scores` silencieuse).
- ~~Identité par `code` seul~~ : corrigé le 25/09, jeton de session exigé (§8 bis).
- Problèmes Brevet complets (parapluies, `parapluie_id`/`num`, sous-questions `depend_question_precedente`), brevets
  blancs et automatismes : v1.1. Les items dépendants ne sont jamais servis seuls.
- Banque peu profonde (voir §6) : séances parfois < 5 exos, signalées.

## ❓ Questions pour Nicolas

1. **Faille existante** : l'action publique `stripe_webhook` (dispatch) accorde premium à n'importe quel email sans
   signature. *Reco : la retirer du dispatch (le vrai webhook signé passe par `checkout.session.completed`).*
2. Complet à 64 q = ~30 compétences conclues sur 121. *Reco : garder 64 q (~40 min) et laisser l'entraînement
   compléter ; alternative : 4e module optionnel.*
3. Acheteur du seul diagnostic complet : entraînement limité à la zone du point faible (comme le gratuit) ?
   *Reco : oui, la zone est recalculée sur la carte complète (plus juste).*
4. Upgrade 30 € via un 3e Payment Link : rien n'empêche un non-acheteur du diagnostic de l'utiliser. *Reco : accepté
   (growth l'a validé), on logge.*
5. MEDIUM (réussi avec indices) compté comme un échec plein (contrat §4). *Reco : garder pour l'instant, à revoir
   si la maîtrise monte trop lentement en conditions réelles.*
