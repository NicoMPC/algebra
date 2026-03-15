# Rapport session — 15 mars 2026

## Objectif élève post-quiz — GAS @70

### Fonctions créées
- `_showObjectifPicker(callback)` — overlay plein écran 4 choix objectif
- `_selectObjectif(key)` — capture le choix et ferme l'overlay

### Fonctions modifiées

| Fichier | Fonction | Modification |
|---|---|---|
| index.html | `_flowActivateStep4Guest` | Intercept `_flowSetStep(4)` → objectif picker d'abord |
| index.html | `_flowGuestRegister` | Ajout `objectif: _flowObjectif` dans fetch register |
| index.html | `flowRegister` | Ajout `objectif: _flowObjectif` dans fetch register |
| index.html | auth modal register | Ajout `objectif: _flowObjectif` dans fetch register |
| index.html | `copySequenceEmail` | 4 variantes J+5 et J+7 selon `st.objectif` |
| index.html | `copyWelcomeEmail` | Phrase de contexte J+0 selon objectif |
| index.html | `_buildModalHTML` | Badge objectif dans header + encart objectif dans action zone emails |
| backend.js | `register` | Colonne N Objectif dans appendRow |
| backend.js | `login` | Lecture + retour `objectif` dans profile |
| backend.js | `getAdminOverview` | Lecture + retour `objectif` par élève |

### Colonne ajoutée
- Users col N : `Objectif` (String) — valeurs : `lacunes` / `chapitre_jour` / `brevet` / `toutes_matieres`

### Docs mises à jour
- `docs/database.md` — colonne N documentée
- `docs/roadmap.md` — section offres différenciées futures
- `docs/notice_fondateur.md` — guide Nicolas (nouveau)

---

## Message Architecture System — GAS @74

### Fonctions créées (index.html)
- `_msg(key, vars)` — fonction centrale messages adaptatifs (niveau + random + pluriel + substitution)
- `_MSGS` — objet ~35 entrées multi-niveau (6EME/3EME/def) + arrays aléatoires
- `_coachShown` / `_markCoach(key)` / `_needsCoach(key)` — coach marks persistés localStorage `mx_coach_v1`

### Fonctions créées (backend.js)
- `triggerWeeklyParentReport()` — rapport parent hebdomadaire dimanche 17h-18h (stats semaine, % réussite, chapitres maîtrisés)

### Fonctions modifiées

| Fichier | Fonction/Zone | Modification |
|---|---|---|
| index.html | `renderDiagInsight` | 3 headlines → `_msg('diag_strong/mid/low')` |
| index.html | `renderBoostInsight` | 3 headlines → `_msg('boost_perfect/good/low')` + streaks → `_msg('streak_3/7/gen')` + boost preparing → `_msg('boost_preparing')` |
| index.html | `rSection('CHAPITRES')` ctxMsg | 4 messages dashboard → `_msg('ctx_*')` |
| index.html | `_checkCoursMilestone` | 4 milestones + cours_prep → `_msg('cours_*')` |
| index.html | `chkComp` chapitre terminé | Hardcodé → `_msg('chap_done')` |
| index.html | `chkComp` boost in-progress | Hardcodé → `_msg('boost_in_progress')` |
| index.html | `boostFromDiag` | Hardcodé → `_msg('boost_ready')` + vibration mobile |
| index.html | choix réponse (L~3853) | `_OK[]`/`_KO[]` → `_msg(_okKey)`/`_msg(_koKey)` contextuels (boost/6eme/3eme/chap) |
| index.html | `showHintInline` | Coach mark premier indice ajouté |
| index.html | `handleBoost` | Coach mark premier boost ajouté |
| index.html | `switchDraftTab` | Coach mark brouillon ajouté |
| index.html | `showOnboarding` | Slide 3 dynamique selon `_flowObjectif` |
| backend.js | `sendMarketingSequence` | 4ème param `objectif` + J+3/J+5/J+7 personnalisés |
| backend.js | `triggerDailyMarketing` | Lecture colonne Objectif + passage à sendMarketingSequence |

### Doc créée
- `docs/messages.md` — référence vivante Voice & Tone Guide (~35 entrées, règles, inventaire)

### Docs mises à jour
- `docs/notice_fondateur.md` — section messages adaptatifs @74, rapport hebdo, coach marks
- `docs/roadmap.md` — message architecture + rapport parent hebdo cochés
- `docs/architecture.md` — tailles fichiers, actions GAS @74, messages adaptatifs

### Tailles fichiers
- `index.html` : 9278 → 9401 lignes (+123)
- `backend.js` : 4717 → 4823 lignes (+106)
