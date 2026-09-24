# Contrat commun — Refonte « Diagnostic 3e » (24/09/2026)

> Source de vérité partagée par tous les agents du chantier. Toute évolution de ce
> contrat passe par le chef de projet (session principale), jamais par un agent seul.
> Branche de travail : `feat/diagnostic-3e` (partie de `feat/refonte-6e-3e-algo`).
> Rien n'est déployé, rien n'est pushé, aucun commit par les agents.

## Vision validée par Nicolas

Le produit = **le diagnostic**. Une cartographie fine des compétences de l'élève de 3e,
qui remonte aux causes (prérequis) et nomme les erreurs types. L'entraînement adaptatif
en découle. L'acheteur est le **parent**, l'utilisateur l'**ado**.

Parcours cible :
1. Landing (parle parent + ado)
2. **Diagnostic express gratuit** (~15 q, ~8 min, adaptatif)
3. Carte partielle : 5 domaines colorés + 1 point faible détaillé, reste flouté
4. Entraînement gratuit : 5 exos/jour sur le point faible révélé
5. **Diagnostic complet payant** (~40 min, 3 modules reprenables) → **PDF récap**
6. Upsell **Programme Brevet** (prix du diagnostic déduit) : entraînement illimité sur
   toute la carte + re-diagnostic mensuel + brevets blancs

Hypothèses de prix (à confirmer par Nicolas, ne pas coder en dur ailleurs qu'en un seul
endroit) : Diagnostic complet **19 €**, Programme Brevet **49 €** (19 € déduits si déjà
acheté le diagnostic). Accès non expirant (règle T2 — jamais de date d'expiration codée
en dur).

Objectif d'autonomie : si des élèves arrivent demain, Nicolas n'a **rien** à faire.
Plus d'assignation manuelle, plus de « ton prof prépare la suite ».

## 1. Domaines (programme cycle 4, 5 thèmes officiels)

| Code | Domaine |
|---|---|
| `NC` | Nombres et calculs |
| `DF` | Organisation et gestion de données, fonctions (stats, probas, proportionnalité, fonctions) |
| `GM` | Grandeurs et mesures |
| `EG` | Espace et géométrie |
| `AP` | Algorithmique et programmation |

Le calcul littéral / équations est rangé dans `NC` (conforme au programme).

## 2. Identifiants de compétences

Format : `<DOMAINE>.<THEME>.<nn>` — ex. `NC.FRAC.03`, `EG.PYTH.02`, `NC.REL.01`.
- `THEME` : 3-5 lettres majuscules, sans accent.
- Une compétence = **un savoir-faire atomique évaluable en 1 question** (« additionner
  deux fractions de dénominateurs différents », pas « les fractions »).
- Les compétences de **prérequis** vues en 6e/5e/4e sont dans le même référentiel, avec
  `niveau_origine` ≠ `3EME`. Elles servent à remonter aux causes.

Fichier : `data/referentiel_3eme/competences.json`

```json
[{
  "id": "NC.FRAC.03",
  "domaine": "NC",
  "theme": "FRAC",
  "titre": "Additionner deux fractions de dénominateurs différents",
  "titre_eleve": "Additionner des fractions qui n'ont pas le même dénominateur",
  "niveau_origine": "5EME",
  "prerequis": ["NC.FRAC.01", "NC.ARITH.02"],
  "poids_brevet": 2,
  "chapitres_legacy": ["Fractions_Brevet"],
  "erreurs": [
    {"id": "NC.FRAC.03#somme_directe",
     "libelle": "Additionne numérateurs et dénominateurs entre eux (1/3+1/4=2/7)",
     "libelle_parent": "Applique une règle intuitive mais fausse sur les fractions",
     "remediation": "Revenir au sens : 1/3 et 1/4 ne sont pas des parts de même taille"}
  ]
}]
```

- `prerequis` : graphe **acyclique** (vérifié par script).
- `poids_brevet` : 1 (rare) / 2 (fréquent) / 3 (incontournable au Brevet).
- `chapitres_legacy` : lien vers les 22 chapitres existants (`data/*_Brevet_v4.json`,
  `data/Auto_*_v4.json`) pour la rétrocompatibilité app.

## 3. Format des items (nouvelle banque)

Items **atomiques** (1 question), compatibles avec les champs déjà rendus par `app.html`
(`q`, `a`, `type`, `options`, `steps`, `f`, `lvl`) + nouveaux champs :

```json
{
  "id": "NC.FRAC.03-017",
  "comp": "NC.FRAC.03",
  "q": "Calcule $\\frac{1}{3} + \\frac{1}{4}$. ___",
  "a": "7/12",
  "type": "fill",
  "options": [],
  "err": {"2/7": "NC.FRAC.03#somme_directe"},
  "steps": ["…", "… ?"],
  "f": "$\\frac{a}{b} + \\frac{c}{d} = \\frac{ad + cb}{bd}$",
  "lvl": 1,
  "usage": ["diag", "train"],
  "contexte": false
}
```

- `lvl` : 1 (application directe) / 2 (standard Brevet) / 3 (piège ou contexte long).
- `err` : **mauvaise réponse → id d'erreur type**. Obligatoire sur chaque distracteur de
  QCM, et sur les mauvaises réponses fill prévisibles. C'est ce qui rend la carte
  « intelligente ».
- `usage` : `diag` (calibré pour le diagnostic), `train` (entraînement), ou les deux.
- Les exercices v4 « parapluie » (contexte + 5 sous-questions) sont conservés comme
  **problèmes Brevet** ; chaque sous-question reçoit un `comp`.

Fichiers : `data/banque_3eme/<DOMAINE>.<THEME>.json` (tableau d'items).

## 4. Modèle de maîtrise (côté serveur)

Par élève × compétence : `maitrise` ∈ [0,1], `n_obs`, `derniere_obs`, `erreurs_vues`
(compteur par id d'erreur). Statut affiché :
- 🔴 **Lacune** (< 0.4, n_obs ≥ 2) · 🟠 **Fragile** (0.4-0.7) · 🟢 **Acquis** (> 0.7)
- ⚪ **Non évalué** (n_obs < 2) — on ne conclut jamais sur 1 seule réponse
- 🔗 **Cause racine** : compétence en lacune qui est prérequis d'au moins une autre
  compétence en lacune.

EASY (1er essai) = succès. Indices/erreur/« je ne sais pas » = échec (cohérent P8).

## 5. Objet « Carte » (sortie du diagnostic, entrée du PDF et de l'UI)

```json
{
  "eleve": {"prenom": "Léa", "niveau": "3EME"},
  "type": "complet",
  "date": "2026-09-24",
  "duree_min": 38,
  "n_questions": 64,
  "score_global": 58,
  "domaines": [{"code": "NC", "libelle": "Nombres et calculs", "maitrise": 0.62,
                "statut": "fragile", "n_comp": 24, "n_lacunes": 4}],
  "competences": [{"id": "NC.FRAC.03", "titre_eleve": "…", "statut": "lacune",
                   "maitrise": 0.25, "cause_racine": true,
                   "bloque": ["NC.EQUA.04", "DF.PROB.02"],
                   "erreurs": [{"id": "NC.FRAC.03#somme_directe", "libelle": "…",
                                "exemple": {"q": "…", "reponse_eleve": "2/7", "a": "7/12"}}]}],
  "priorites": ["NC.REL.02", "NC.FRAC.03", "EG.PYTH.01"],
  "plan_4_semaines": [{"semaine": 1, "focus": ["NC.REL.02"], "objectif": "…"}],
  "points_forts": ["EG.THAL.01", "DF.STAT.02"],
  "message_parent": "…"
}
```

Champs optionnels ajoutés le 24/09 (lus par le PDF, avec fallback) : `phrase_cle` (racine,
1 phrase « l'essentiel »), `niveau_origine` sur chaque compétence, `libelle_parent` et
`remediation` sur chaque erreur (copiés depuis le référentiel).

Pour le diagnostic express : même objet, `"type": "express"`, compétences partielles.

## 6. Répartition des fichiers (qui écrit où)

| Agent | Écrit dans | Lit |
|---|---|---|
| Didacticien | `data/referentiel_3eme/**`, `docs/specs/10-referentiel.md` | tout |
| Ingénieur adaptatif | `supabase/functions/api/index.ts`, `supabase/migrations/2026092*_*.sql`, `docs/specs/20-moteur.md` | tout |
| Dev PDF | `js/bilan-pdf.js`, `bilan-preview.html`, `docs/specs/30-pdf.md` | tout, dont `/home/liline/Bureau/freelance/HUMANA/humana-lite/src/lib/pdf/` |
| UX / épuration | `docs/specs/40-parcours-epuration.md` (+ maquettes HTML dans `docs/specs/maquettes/`) | tout — **ne modifie pas `app.html`** à ce stade |
| Growth / CRO / légal | `docs/specs/50-offre-conversion.md`, `docs/specs/51-emails.md`, `docs/specs/52-legal.md` | tout |
| Landing | `landing/**` (nouvelle landing vanilla, remplacera `index.html` + `_next/` au merge), `docs/specs/60-landing.md` | tout |

## 7. Décisions Nicolas du 24/09

- **Anciens comptes supprimés** : repart à zéro (Léo compris). Aucune rétrocompat élève à
  préserver ; le code legacy peut être retiré sans migration de données utilisateur.
  Suppression effective en base faite au moment du déploiement (backup avant).
- **Nouvelle landing** en HTML/CSS/JS vanilla, remplace le build Next.js (source perdue).
- **Aucune incitation de l'ado à faire acheter ses parents** (contrainte légale) : côté ado,
  le CTA est « Montre ta carte à tes parents » (partage du bilan, sans prix). Tout le
  discours commercial vit sur la page parent / les emails parent.
- Recos UX adoptées par défaut : pas de correction pendant le diag, carte partielle avant
  compte, email parent obligatoire + bilan express auto, G16 (J+1) abandonné pour le
  contenu algo, gratuit 5 exos/jour sans limite de durée, streak serveur, brevet blanc et
  automatismes en v1.1, admin read-only.

Personne ne touche aux fichiers d'un autre. Personne ne commit, ne push, ne déploie, ne
modifie Stripe ni Supabase prod. Les questions pour Nicolas vont en fin de livrable dans
une section **« ❓ Questions pour Nicolas »** (courtes, avec la reco par défaut).

## 8. Exigences remontées pour l'intégration `app.html` (lots dev-ux)

- ✅ Fait 24/09 : `_toNum` strict (parseFloat acceptait « 4x+3 » pour « 4x+12 » — bug prod),
  unités courantes tolérées en fin de réponse.
- Énoncés multi-lignes : les `\n` de `q` sont perdus au rendu (≥ 8 sites `fmtL(…q)`).
  Indispensable pour les scripts Scratch (AP) : conserver retours à la ligne ET
  indentation (ex. conteneur `white-space:pre-wrap` hors LaTeX, ou bloc code dédié).
- Pas de rendu de courbe / diagramme (`renderFigure` = géométrie seulement) : les items
  DF graphes sont décrits en texte en attendant un type de figure « courbe/barres ».
- Compétences hors programme (poids 1 : `NC.RAC.03/04`, `EG.REP.02`, quartiles…) :
  `usage: ["train"]` uniquement, jamais en diagnostic (reco didacticien adoptée).
- Remontés par la relecture DF/GM : (a) un `alt` « 25% » fait accepter « 0,25 »/« 1/4 »
  dans une case « ___ % » → comparer sans conversion % quand l'énoncé porte déjà le « % » ;
  (b) `_normFill` doit retirer un préfixe `x=` / `a=` ; (c) normaliser la saisie avant
  lookup dans les clés `err` ; (d) la vue rétro `_renderRetroExo` n'affiche pas les `table`.
- Relecture EG/AP (24/09) : **calculatrice autorisée** pendant le diagnostic (items trigo) —
  à écrire dans la consigne d'accueil du diag. Scripts Scratch : ligne « Fin répéter »
  explicite (convention mise à jour). Moins Unicode `−` et préfixe `x=` gérés dans
  `_normFill`/`_toNum` (fait, test : `node supabase/tests/fill_match_node.js`).

## 9. Évolutions du format (24/09)

- `err` peut pointer vers une erreur d'un **prérequis direct** de `comp` (ex. oublier la
  racine dans un exo de réciproque de Pythagore = erreur de `EG.PYTH.01`). Le moteur
  impute alors l'observation d'erreur au prérequis : c'est une piste de cause racine.
- Compétence `"diag": false` dans le référentiel (hors programme : `NC.RAC.03/04`,
  `EG.REP.02`) → jamais servie en diagnostic, items `usage: ["train"]`.
- `EG.TRANS.02#vecteur_inverse` fusionnée dans `#soustrait_vecteur` ; nouvelle erreur
  `EG.TRANS.02#ajoute_coordonnees_image`.
- Scripts utilitaires : `data/banque_3eme/check_banque.py`, `apply_reviews.py`,
  `_legacy/check_legacy.py`, `data/referentiel_3eme/check_referentiel.py`.
