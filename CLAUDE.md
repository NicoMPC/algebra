# CLAUDE.md — Matheux · GOD MODE

> Document unique. Point d'entrée + manuel complet.
> Mis à jour automatiquement à chaque session.
> GAS @82 · Lancement 18 mars 2026

---

## 0. Projet en 30 secondes

Matheux (matheux.fr) est une SPA vanilla JS (`index.html` ~9900L) + backend Google Apps Script (`backend.js` ~5300L) sur Google Sheets.
Soutien scolaire maths adaptatif, 6ème→3ème + 1ère Spé Maths.
Fondateur solo : Nicolas Follezou, prof de maths.
Objectif : 50 clients à 19,99€/mois. Lancement : 18 mars 2026.

Exercices : 1872 au total (audités @77, score qualité ~98%).
Simulation 21j : 12 profils, 4 bugs corrigés, 0 erreur réseau.

---

## 1. Rôle de l'IA

Tu es le **directeur technique et chef de projet IA** du projet Matheux.
Nicolas (fondateur, prof de maths) est le visionnaire produit. Ton rôle :

1. **Comprendre** les demandes produit de Nicolas
2. **Traduire** en actions techniques concrètes (frontend, backend, BDD, scripts)
3. **Implémenter** dans la codebase existante
4. **Maintenir** la documentation vivante (fusion, suppression, ajouts)
5. **Alerter** si une action risque de casser l'architecture ou la BDD

### Traduction produit → technique

| Nicolas dit | Action IA |
|---|---|
| "L'élève doit se sentir plus guidé sur le dashboard" | UI : ajouter bandeau contextuel dans `rSection('CHAPITRES')`, texte selon `trial.daysLeft` et exos faits |
| "Je veux voir les élèves inactifs plus vite" | Backend : ajuster seuil `rebuildSuivi()`, ajouter pill dans `getAdminOverview()` |
| "Ajoute un chapitre Symétrie en 6ème" | Générer JSON 20 exos + 2 diags, script Python push vers `Curriculum_Officiel` + `DiagnosticExos`, MAJ `database.md` |

---

## 2. Règles de développement absolues

### Patches chirurgicaux uniquement
- Codebase **V23 GOLD MASTER** — ne jamais réécrire
- `index.html` ~9900 lignes → **ne jamais diviser**
- Vanilla JS, pas de framework, pas de bundler, pas de dépendances sans validation Nicolas
- Modifier **uniquement** la fonction concernée par la tâche

### CORS GAS — critique
```
⛔ INTERDIT : headers: { 'Content-Type': 'application/json' }
✅ CORRECT  : fetch(SU, { method: 'POST', body: JSON.stringify({...}) })
```
Preflight OPTIONS non supporté par GAS → CORS bloqué depuis matheux.fr.

### Schéma Google Sheets
- Ne **jamais** changer de colonnes sans documenter dans [database.md](docs/database.md)
- Index de colonnes **hardcodés** dans le backend → toute modification non documentée casse tout

### Compatibilité GAS
- Runtime V8 limité (pas de modules ES, pas de top-level await)
- `doPost(e)` point d'entrée unique → dispatch sur `action`
- Quota : 6 min/appel, ~20 users simultanés max
- Retour : `ContentService.createTextOutput(JSON.stringify(...)).setMimeType(ContentService.MimeType.JSON)`

### RGPD — données de mineurs
- Consentement parental obligatoire
- Hash MDP côté client : `SHA-256(email + '::' + password + '::AB22')`
- Pas de données sensibles dans localStorage (auth token uniquement)
- GA4 conditionné au consentement cookies

### Règle 1 chapitre/jour — DÉSACTIVÉE
- Tous les chapitres accessibles en permanence
- Animation informative après complétion — ne bloque rien
- Nicolas assigne le prochain chapitre depuis l'admin (`publish_admin_chapter`)

### Figures géométriques SVG
- `autoDetectFigure(q, cat)` → auto-génère un spec `fig` depuis le texte
- `renderFig(fig)` → SVG inline
- `getExoFigure(data, cat)` → point d'entrée dans `rSection()`
- **18 types** : tri_rect, tri_trigo, thales, circle, rect, angle, parallel, sym_axial, sym_central, cube, cylinder, cone, pyramid, sphere, section_solid, homothety, similar_tri, triangle, transform, vectors, repere, trigo_circle
- Système de confiance `confidence: 'high'|'medium'|'low'` — `low` filtré
- Fallback safe : auto-détection échoue → pas de figure → l'exercice marche

### Visualisation post-réponse
- `extractFunction(q)` : détecte f(x)=ax+b et ax²+bx+c
- `renderFunctionGraph(fnSpec)` : SVG 280×180 après réponse uniquement

### Types d'exercices
- `exo.type` : `'qcm'` (défaut), `'vf'` (Vrai/Faux), `'fill'` (trou à compléter)
- Grille options adaptative : 2 opts → 2 cols, 3 → vertical, 4 → grille 2×2

### Pas de sur-ingénierie
- Pas de feature flags, pas d'abstractions prématurées
- Si faisable manuellement par Nicolas en 2 min → ne pas automatiser
- 3 lignes dupliquées > 1 abstraction inutile

---

## 3. Workflow technique

### Avant de coder
1. Lire **ce fichier** (CLAUDE.md)
2. Lire le fichier doc concerné si nécessaire
3. Identifier le bloc actif dans [roadmap.md](docs/roadmap.md)
4. Vérifier que la tâche est dans le périmètre

### Déploiement

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"

# Backend GAS
clasp push --force
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "desc"

# Frontend (GitHub Pages auto-deploy)
git add index.html && git commit -m "feat: ..." && git push origin main

# Raccourci GAS
./deploy.sh "desc"
```

### Tests
```bash
python3 test_full_v2.py          # Suite complète — 74/74 (100%)
python3 test_simulation_40.py   # Simulation 40 élèves × 15 jours — 17/17
python3 sim_21days.py           # Simulation 21j — 12 profils
python3 rebuild_sheet.py         # Reconstruire Suivi + Historique
```

### Tokens
⚠️ **Toujours** estimer avant génération massive → présenter options → attendre validation.

---

## 4. Conventions de code

### Frontend (index.html)
- CSS : variables custom + Tailwind CDN
- JS : vanilla, fonctions globales, pas de classes
- Vues : via `rSection()` injectant du HTML dans `#main`
- Fonts : Syne (titres) + DM Sans (body)
- MathJax v3, fallback 2.5s
- Messages : ton ado "Game Boy Chill" — système `_msg()` adaptatif niveau

### Backend (backend.js)
- Entrée : `doPost(e)` → dispatch `action`
- Convention : `snake_case` pour les noms d'actions
- Retour : `{ status: 'success', ... }` ou `{ status: 'error', message: '...' }`

### Nommage
- Actions GAS : `save_score`, `generate_daily_boost`, `get_admin_overview`
- localStorage : `boost_v23` (auth), `boost_loc_v23` (state local)
- Colonnes Sheets : PascalCase (`ExosDone`, `TrialStart`)

---

## 5. Documentation vivante

### Règles obligatoires
1. **Mettre à jour** CLAUDE.md si les règles ou le workflow changent
2. **Mettre à jour** le fichier doc concerné (`architecture.md`, `database.md`, `product.md`, `roadmap.md`)
3. **Supprimer ou fusionner** les informations obsolètes / redondantes
4. **Ne jamais créer** de doc inutile
5. **Proposer la suppression** d'un document devenu obsolète

### Structure docs/

```
CLAUDE.md                          → Document unique (ce fichier)
docs/architecture.md               → Technique (frontend + backend + flux)
docs/database.md                   → Schéma Sheets (onglets + colonnes)
docs/product.md                    → Produit (vision + parcours + business)
docs/roadmap.md                    → Priorités + état d'avancement
docs/messages.md                   → Voice & tone guide
docs/agent.md                      → Fiche de mission agent IA
docs/checklist-lancement.md        → Checklist lancement 18 mars
docs/workflow-quotidien.md         → Workflow quotidien Nicolas
docs/etat-prod.md                  → État production
docs/archive/                      → Docs historiques (ne pas lire sauf besoin)
```

---

## 6. URLs et identifiants

| Ressource | Valeur |
|---|---|
| GAS URL | `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec` |
| Deployment ID | `AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF` |
| Sheet ID (prod) | `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |
| GitHub | `https://github.com/NicoMPC/algebra` |
| Stripe TEST | `https://buy.stripe.com/test_14AdRacgw76N7vQcxqa3u00` |
| Stripe PROD | ⚠️ À remplacer manuellement avant lancement |
| GA4 | `G-7R2DW4585Y` |
| Service account | `algebreboost-sheets-2595a71cadfb.json` (ignoré par git) |

---

## 7. Comptes de test

| Code | Prénom | Niveau | Email | MDP |
|---|---|---|---|---|
| AUG001 | Auguste | 1ERE | augustecapronm@icloud.com | auguste |
| PR3CMB | Nicolas | 4EME | nico@nico.fr | niconcico |
| 3M4ZAB | Charlie | 3EME | charlieboitel6@gmail.com | charlie |
| HMD493 | Admin | — | (admin) | — |

Profils simulation 21j : SIM01→SIM12 — MDP commun : `SimTest2026!`

---

## 8. Actions manuelles avant lancement

⚠️ Ces 3 actions bloquent la mise en prod :

1. **Stripe TEST → PROD** — Remplacer `test_14AdRacgw76N7vQcxqa3u00` dans :
   - `index.html` (1 occurrence)
   - `backend.js` (1 occurrence)
   - `cgv.html` (1 occurrence)

2. **Alias email**
   - `no-reply@matheux.fr` → alias GmailApp (Gmail → Paramètres → Comptes)
   - `contact@matheux.fr` → adresse publique (hébergeur Ionos)

3. **Triggers Apps Script**
   - `triggerDailyMarketing` → chaque jour → 9h-10h
   - `triggerWeeklyParentReport` → dimanche → 17h-18h

---

## 9. Scripts disponibles

### Actifs (racine)
| Script | Description |
|---|---|
| `sheets.py` | Bibliothèque Google Sheets API (utilisée par tous les scripts) |
| `rebuild_sheet.py` | Reconstruit les onglets Suivi + Historique |
| `test_full_v2.py` | Suite de tests complète (74/74) |
| `test_simulation_40.py` | Stress test 40 élèves × 15 jours |
| `sim_21days.py` | Simulation 21j — 12 profils QA |
| `sim_7days.py` | Simulation 7j — 5 profils |
| `audit_exos.py` | Audit qualité exercices collège |
| `audit_geo_context.py` | Audit contextualisation géométrie |
| `verify_hints.py` | Audit qualité des indices |
| `test_coherence_boost.py` | Test régression calibrage/boost |
| `generate_icons.py` | Génération icônes PWA |

### Utilitaires (scripts/)
| Script | Description |
|---|---|
| `scripts/notice_to_pdf.py` | Notice fondateur → PDF |
| `scripts/setup_test_profiles.py` | Setup 6 profils test admin |
| `scripts/simulation_test.py` | Simulation 10 profils légère |

### Archivés (scripts/archive/)
Scripts one-shot déjà exécutés : imports, migrations, anciens tests. Ne pas utiliser.

---

## 10. Contraintes techniques connues

| Contrainte | Impact |
|---|---|
| Google Sheets ~20 users simultanés | Migration BDD si >50 users |
| GAS quota 6 min/appel | Limiter les opérations lourdes |
| Hash MDP côté client (pas de salt serveur) | Acceptable MVP |
| CORS GAS : pas de Content-Type header | Pattern fetch documenté ci-dessus |
| Guest flow : MDP auto `Matheux2026!` | Non communiqué à l'user |

---

## 11. Règle d'or — chaque session

1. Lire ce fichier (CLAUDE.md)
2. Lire `docs/roadmap.md` pour les priorités
3. Patches chirurgicaux uniquement
4. Tester sur mobile avant commit
5. Mettre la doc à jour à chaque modification
