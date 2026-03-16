# Rapport session nuit — 15 mars 2026

## Résumé en 5 lignes

Session nettoyage + documentation avant lancement 18 mars.
13 scripts one-shot archivés dans `scripts/archive/`, `scripts_archive/` consolidé et supprimé.
CLAUDE.md fusionné (docs/claude.md absorbé → un seul fichier racine complet).
4 nouveaux docs créés : agent.md, checklist-lancement.md, workflow-quotidien.md, etat-prod.md.
Vérifications .claspignore/.gitignore OK, roadmap mise à jour @81.

---

## BLOC 1 — Nettoyage

### Fichiers archivés (racine → scripts/archive/)

| Script | Raison |
|---|---|
| cleanup_prod.py | One-shot — base nettoyée 14 mars |
| create_5_students.py | One-shot — profils déjà créés |
| create_demo_student.py | One-shot — supplanté par setup_test_profiles.py |
| fix_categorie_names.py | One-shot — accents corrigés 12 mars |
| fix_lucas_ines.py | One-shot — ajustement démo |
| generate_boost_exos.py | One-shot — données déjà dans Sheet |
| import_brevet_exos.py | One-shot — import fait |
| insert_1ere.py | One-shot — 1ERE ajouté @64 |
| push_boost_exos.py | One-shot — push fait |
| push_new_chapters_phase1_2.py | One-shot — chapitres déployés |
| push_sprint4.py | One-shot — sprint terminé |
| boost_exos.json | Données source — déjà dans Sheet |
| brevet_exos_3eme.json | Données source — déjà dans Sheet |

### Consolidation dossiers

- `scripts_archive/` (7 fichiers) → fusionné dans `scripts/archive/` → dossier supprimé
- `docs/archive/test_prompts.py` → déplacé vers `scripts/archive/`
- `docs/archive/watch_deploy.sh` → déplacé vers `scripts/archive/`
- `__pycache__/` → supprimé (couvert par .gitignore)
- `docs/rapport-pas-compris-profil-cognitif.md` → archivé
- `docs/rapport-simulation-21j.md` → archivé

### Scripts GARDÉS (racine)

| Script | Rôle |
|---|---|
| sheets.py | Bibliothèque Sheets API (dépendance de tous) |
| rebuild_sheet.py | Reconstruit Suivi + Historique |
| test_full_v2.py | Suite tests 74/74 |
| test_simulation_40.py | Stress test 40 élèves |
| sim_21days.py | Simulation 21j QA |
| sim_7days.py | Simulation 7j |
| audit_exos.py | Audit qualité exercices |
| audit_geo_context.py | Audit contextualisation géo |
| verify_hints.py | Audit indices |
| test_coherence_boost.py | Régression calibrage/boost |
| generate_icons.py | Icônes PWA |

### Structure finale

```
/algebra/
├── index.html, backend.js          ← prod (non touchés)
├── CLAUDE.md                        ← GOD MODE fusionné
├── *.py (11 scripts actifs)
├── sheets.py                        ← bibliothèque commune
├── deploy.sh, .clasp.json, appsscript.json
├── *.html (5 pages légales + premium + offline)
├── manifest.json, sw.js, robots.txt, sitemap.xml, CNAME
├── docs/
│   ├── agent.md                     ← NOUVEAU
│   ├── architecture.md
│   ├── checklist-lancement.md       ← NOUVEAU
│   ├── database.md
│   ├── etat-prod.md                 ← NOUVEAU
│   ├── messages.md
│   ├── notice_fondateur.md + .pdf
│   ├── product.md
│   ├── roadmap.md                   ← MIS À JOUR @81
│   ├── workflow-quotidien.md        ← NOUVEAU
│   └── archive/ (30 fichiers historiques)
├── scripts/
│   ├── notice_to_pdf.py
│   ├── setup_test_profiles.py
│   ├── simulation_test.py
│   └── archive/ (20 fichiers archivés)
└── icons/ (images PWA)
```

---

## BLOC 2 — CLAUDE.md

### Ce qui a été fusionné
- docs/claude.md (GOD MODE 231 lignes) → absorbé intégralement dans CLAUDE.md racine
- Structure : 11 sections numérotées (projet → règle d'or)
- Ajout : section Scripts disponibles, section Comptes de test, section Actions manuelles

### Ce qui a été supprimé
- Renvois circulaires CLAUDE.md ↔ docs/claude.md
- Références obsolètes (@60, anciens noms de fonctions)

### Liens mis à jour
- docs/roadmap.md : lien claude.md → ../CLAUDE.md
- docs/claude.md → déplacé vers docs/archive/claude-pre-fusion.md

---

## BLOC 3 — agent.md

Créé dans `docs/agent.md` — 6 sections :
1. Qui est Nicolas
2. Ce qu'est Matheux (vision cognitive)
3. Architecture décisionnelle
4. Les 3 utilisateurs (élève, parent, opérateur)
5. Comportement agent attendu (FAIT / NE FAIT PAS)
6. Roadmap décisionnelle + métriques + défendabilité

---

## BLOC 4 — Rapports générés

- `docs/checklist-lancement.md` — 3 blocs (bloquant / important / J+1)
- `docs/workflow-quotidien.md` — 3 étapes quotidiennes + dimanche + autonome
- `docs/etat-prod.md` — données Sheets réelles (24 users, 1375 scores, 114 boosts)
- `docs/roadmap.md` — mis à jour @81, ajout section "Semaine du lancement 16-18 mars"

---

## BLOC 5 — Vérifications

### .claspignore
Complété — ajout `docs/`, `scripts/`, `*.md`, pages légales HTML, `icons/`, `CNAME`, `robots.txt`, `sitemap.xml`, `.claude/`. Seuls `backend.js` et `appsscript.json` sont pushés vers GAS.

### .gitignore
OK — `*.json` (sauf appsscript/clasp/manifest), `__pycache__/`, `*.bak`, `node_modules/`. Le service account n'est PAS traqué par git.

### Taille fichiers
- index.html : 9919 lignes / 534K
- backend.js : 5341 lignes / 240K

### Git log (10 derniers commits)
```
0a9f6c1 feat: bouton "J'ai pas compris" + profil cognitif fiche admin @81
9118806 docs: mise à jour références @77 → @80
d01dd91 fix: 4 bugs GAS corrigés @79-@80 + simulation 21j complète
e8e3ebe feat: send_session_rapport action GAS @78
b89a6a1 seo: retirer 1ère Spé des meta tags — collège uniquement
8974b81 seo: sitemap.xml + robots.txt + meta tags optimisés
bce6376 docs: notice fondateur PDF régénéré @78
218a9fa docs: mise à jour complète @77 — fusion, archive, notice fondateur
78cda66 feat: dark mode app + guide boost fix + titres chapitres gras + boost reopen nav @77
d966c31 docs: audit corrections applied — 39 fixes in Sheets (15 mars 2026)
```

Aucun fichier sensible commité par erreur.

---

## Ce qu'il reste à faire manuellement

### Bloquant lancement (Nicolas)
1. **Stripe TEST → PROD** — 3 fichiers (index.html, backend.js, cgv.html)
2. **contact@matheux.fr** — créer chez Ionos
3. **no-reply@matheux.fr** — alias Gmail
4. **Triggers Apps Script** — triggerDailyMarketing (9h) + triggerWeeklyParentReport (dim 17h)
5. **Nettoyer base** — supprimer SIM01-SIM12 avant lancement

### Optionnel
- Valider PWA en prod (Lighthouse)
- Préparer premier boost pour premier vrai élève

---

## Commandes de déploiement

Aucun fichier déployable modifié (index.html et backend.js non touchés).
Seuls des fichiers de documentation ont été créés/modifiés → git commit suffit.

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"
git add -A && git commit -m "docs: nettoyage repo + CLAUDE.md fusionné + 4 docs lancement"
git push origin main
```
