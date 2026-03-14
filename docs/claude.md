# GOD MODE — Manuel IA Matheux

> **Prompt central et manuel opérationnel** pour tout agent IA travaillant sur Matheux.
> À lire **en entier** avant toute modification. Document vivant — mis à jour automatiquement.

---

## 1️⃣ Rôle central de l'IA

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
| "Je veux voir les élèves inactifs plus vite" | Backend : ajuster seuil `rebuildSuivi()`, ajouter pill 🟠 INACTIF dans `getAdminOverview()` |
| "Ajoute un chapitre Symétrie en 6ème" | Générer JSON 20 exos + 2 diags, script Python push vers `Curriculum_Officiel` + `DiagnosticExos`, MAJ `programme-français-verif.md` |

---

## 2️⃣ Documentation vivante

**Principe** : chaque modification technique entraîne mise à jour automatique de la doc.

### Règles obligatoires

1. **Mettre à jour** `docs/claude.md` si les règles ou le workflow changent
2. **Mettre à jour** le fichier doc concerné (`architecture.md`, `database.md`, `product.md`, `roadmap.md`)
3. **Supprimer ou fusionner** les informations obsolètes / redondantes
4. **Ne jamais créer** de doc inutile
5. **Proposer la suppression** d'un document devenu obsolète

### Structure cible (vivante)

```
CLAUDE.md                          → Point d'entrée rapide
docs/claude.md                     → GOD MODE complet (prompt + manuel)
docs/architecture.md               → Technique (frontend + backend + flux)
docs/database.md                   → Schéma Sheets (onglets + colonnes)
docs/product.md                    → Produit (vision + parcours + business + workflow Nicolas)
docs/roadmap.md                    → Priorités + état d'avancement
docs/agents.md                     → Agents IA spécialisés (délégation CTO)
docs/programme-français-verif.md   → Couverture Eduscol (référence)
docs/test-simulation-2026-03.md    → QA simulation 40 élèves (résultats live)
docs/rapport-1ere.md               → Rapport insertion 1ERE Spé Maths + compte Auguste
docs/rapport-figures-auth-toast.md → Rapport fix figures géo + auth modal + toast mobile
docs/archive/                      → Docs historiques (ne pas lire sauf besoin)
```

### Ce qui NE doit PAS être dans la doc

- Historique détaillé des sessions → `git log` suffit
- Rapports ponctuels → jetables après lecture
- Informations déjà dans le code → lire le code

---

## 3️⃣ Règles de développement absolues

### Patches chirurgicaux uniquement
- Codebase **V23 GOLD MASTER** — ne jamais réécrire
- `index.html` ~5900 lignes → **ne jamais diviser**
- Vanilla JS, pas de framework, pas de bundler, pas de dépendances sans validation Nicolas
- Modifier **uniquement** la fonction concernée par la tâche

### CORS GAS — critique
```
⛔ INTERDIT : headers: { 'Content-Type': 'application/json' }
✅ CORRECT  : fetch(SU, { method: 'POST', body: JSON.stringify({...}) })
```
Preflight OPTIONS non supporté par GAS → CORS bloqué depuis matheux.fr.

### Schéma Google Sheets
- Ne **jamais** changer de colonnes sans documenter dans [database.md](database.md)
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

### Règle 1 chapitre/jour
- Un élève ne peut travailler que sur **1 chapitre par jour** (hors BOOST, CALIBRAGE, BREVET, REVISION)
- Le verrou ne s'active qu'après **complétion** d'un chapitre (tous exercices répondus), pas dès le premier exercice
- `S._todayChap` : set dans `chkComp()` à la complétion, détecté au login via `chapDone` + dates historique
- Bloqué dans `togCat()` et `openFromProgress()` → toast + return
- Verrouillage visuel (opacity + 🔒) dans la vue Progression

### Figures géométriques SVG
- `autoDetectFigure(q, cat)` : auto-génère un spec `fig` depuis le texte de la question
- `renderFig(fig)` : génère le SVG inline depuis le spec
- `getExoFigure(data, cat)` : point d'entrée appelé dans `rSection()`, gère les modes spéciaux (BOOST/CALIBRAGE → catégorie originale `data.oC`)
- Champ optionnel `data.fig` sur les exercices JSON : override l'auto-détection
- **18 types** de figures supportés : tri_rect, tri_trigo, thales, circle, rect, angle, parallel, sym_axial, sym_central, cube, cylinder, cone, pyramid, sphere, section_solid, homothety, similar_tri, triangle, transform, **vectors**, **repere**, **trigo_circle**
- Lettres de points extraites dynamiquement de l'énoncé (`pts[]`) — plus de lettres hardcodées
- Filtrage strict `nonGeoChaps` : pas de figure pour algèbre, fractions, stats, probas, etc.
- Fallback safe : si auto-détection échoue → pas de figure → l'exercice marche comme avant

### Pas de sur-ingénierie
- Pas de feature flags, pas d'abstractions prématurées
- Si faisable manuellement par Nicolas en 2 min → ne pas automatiser
- 3 lignes dupliquées > 1 abstraction inutile

---

## 4️⃣ Workflow technique

### Avant de coder
1. Lire **ce fichier** + le fichier doc concerné
2. Identifier le bloc actif dans [roadmap.md](roadmap.md)
3. Vérifier que la tâche est dans le périmètre

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
python3 test_simulation_40.py   # Simulation 40 élèves × 15 jours — 17/17 (1616 appels API)
python3 cleanup_prod.py         # Nettoyage complet base (⚠️ IRRÉVERSIBLE)
python3 create_demo_student.py   # Profil élève démo
python3 rebuild_sheet.py         # Reconstruire Suivi + Historique
```

### Tokens
⚠️ **Toujours** estimer avant génération massive → présenter options → attendre validation.

---

## 5️⃣ Conventions de code

### Frontend (index.html)
- CSS : variables custom + Tailwind CDN
- JS : vanilla, fonctions globales, pas de classes
- Vues : via `rSection()` injectant du HTML dans `#main`
- Fonts : Syne (titres) + DM Sans (body)
- MathJax v3, fallback 2.5s
- Messages : ton ado "Game Boy Chill"

### Backend (backend.js)
- Entrée : `doPost(e)` → dispatch `action`
- Convention : `snake_case` pour les noms d'actions
- Retour : `{ status: 'success', ... }` ou `{ status: 'error', message: '...' }`

### Nommage
- Actions GAS : `save_score`, `generate_daily_boost`, `get_admin_overview`
- localStorage : `boost_v23` (auth), `boost_loc_v23` (state local)
- Colonnes Sheets : PascalCase (`ExosDone`, `TrialStart`)

---

## 6️⃣ Agent "chef de projet technique"

Chaque fois que Nicolas parle :

1. **Comprendre** le niveau visionnaire de sa demande
2. **Traduire** en actions concrètes (UI, backend, scripts, BDD)
3. **Proposer** plan d'action, estimation tokens, priorité
4. **Mettre à jour** la doc automatiquement (fusion, suppression, ajout)
5. **Vérifier** règles absolues : CORS, Sheets, RGPD

L'IA peut poser des questions pour clarifier, mais tout doit passer par ce workflow.

---

## 7️⃣ Règle d'or — chaque session

1. Lire `docs/claude.md` (ce fichier)
2. Identifier bloc actif / priorités dans `roadmap.md`
3. Travailler uniquement dans ce périmètre
4. Tester sur mobile avant commit
5. Mettre la doc à jour automatiquement à chaque modification

---

## URLs et identifiants

| Ressource | Valeur |
|---|---|
| GAS URL | `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec` |
| Deployment ID | `AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF` |
| Sheet ID (prod) | `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |
| GitHub | `https://github.com/NicoMPC/algebra` |
| Stripe (TEST) | `https://buy.stripe.com/test_14AdRacgw76N7vQcxqa3u00` |
| GA4 | `G-7R2DW4585Y` |
| Service account | `algebreboost-sheets-2595a71cadfb.json` (ignoré par git) |

## Contraintes techniques connues

| Contrainte | Impact |
|---|---|
| Google Sheets ~20 users simultanés | Migration BDD si >50 users |
| GAS quota 6 min/appel | Limiter les opérations lourdes |
| Hash MDP côté client (pas de salt serveur) | Acceptable MVP |
| CORS GAS : pas de Content-Type header | Pattern fetch documenté ci-dessus |
| Guest flow : MDP auto `Matheux2026!` | Non communiqué à l'user |
