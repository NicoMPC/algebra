# Architecture — Matheux

> Structure technique frontend/backend, flux de données, scripts utilitaires.
> Voir aussi [claude.md](claude.md) pour les règles, [database.md](database.md) pour le schéma Sheets, [product.md](product.md) pour le produit.

---

## Vue d'ensemble

```
NAVIGATEUR (index.html)              GOOGLE APPS SCRIPT (backend.js)
        │                                        │
        │  fetch POST (JSON, SANS Content-Type)  │
        ├───────────────────────────────────────►│
        │  { action: 'save_score',               │  Lit/écrit dans
        │    code: 'ABC123', ... }               │  Google Sheets
        │  ◄─────────────────────────────────── │  via SpreadsheetApp
        │  { status: 'success', ... }            │
        │                                        │
  localStorage                             Google Sheets (prod)
  - boost_v23: {email, hash}        ID: 1zLBajKVL8FUzy7aV2Myi9gYFEFJjnALkLAg0hbicuDk
  - boost_loc_v23: {stk, last}
```

| Composant | Technologie | Fichier | Taille |
|---|---|---|---|
| Frontend | HTML + CSS vars + Tailwind CDN + JS vanilla | `index.html` | ~5900 lignes |
| Backend | Google Apps Script (V8) | `backend.js` | ~4200 lignes |
| Base de données | Google Sheets | — | 12 onglets actifs |
| Hébergement frontend | GitHub Pages | `matheux.fr` | Auto-deploy sur push |
| Hébergement backend | Google Apps Script Web App | URL fixe via deployment ID | — |
| Auth | SHA-256 client-side | localStorage `boost_v23` | `email + '::' + password + '::AB22'` |

---

## Frontend — SPA vanilla JS

### Structure du fichier `index.html`

Le fichier est organisé en sections :

1. **CSS** (~1500 lignes) : variables CSS custom, Tailwind utilities, animations (`pulseGentle`, `toastIn`, `popIn`, `pulseNewChap`)
2. **HTML** : structure minimale (header, main, footer, modales)
3. **JavaScript** (~3500 lignes) : logique applicative complète

### Système de vues (SPA)

Les vues sont des fonctions JS qui injectent du HTML dans `#main` :

| Vue | Fonction | Description |
|---|---|---|
| Landing | Rendu directement dans le HTML | Page d'accueil marketing |
| Trial Flow | `startTrialFlow()` → overlay fullscreen (`#trial-flow.flow-fs`) | Quiz diagnostic inline pre-inscription, 4 steps (classe → chapitres → quiz → inscription) |
| Chapitres | `rSection('CHAPITRES', ...)` | Liste des chapitres + "Mon Boost du jour" |
| Exercice | `rSection('EXERCICE', ...)` | Quiz MCQ avec indices/formule |
| Calibrage | `rSection('CALIBRAGE', ...)` | Diagnostic (quiz initial) |
| Progression | `rSection('PROGRESSION', ...)` | Barres de progression par chapitre |
| Brevet | `rSection('BREVET', ...)` | Mode brevet blanc (3EME only) |
| Admin | `rSection('ADMIN', ...)` | Dashboard "Mes Élèves" |

### Navigation

- `initApp()` : point d'entrée après login, route vers la bonne vue
- Admin détecté via `S.prof.isAdmin` → redirect auto vers vue admin
- Onglets bas de page : 📚 Chapitres | 📊 Progression | 🎓 Brevet (3EME)
- Swipe gauche → exercice suivant (mobile)

### State management

```javascript
const S = {
  prof: { code, name, level, isAdmin, premium, trial },
  exos: [],           // exercices en cours
  idx: 0,             // index exercice actif
  calState: null,     // état calibrage
  // ...
};
```

- `localStorage('boost_v23')` : `{ email, hash }` — auth uniquement
- `localStorage('boost_loc_v23')` : `{ [code]: { stk, last } }` — streak local
- Toutes les données viennent du GAS à chaque login (pas de cache de données)

### Librairies externes (CDN)

- **Tailwind CSS** : utilities responsive
- **MathJax v3** : rendu LaTeX (fallback 2.5s si offline)
- **Syne** + **DM Sans** : Google Fonts

### Gamification

- **XP** : points d'expérience cumulés
- **Streak** : jours consécutifs d'activité
- **Mastery ring** : cercle SVG de progression par chapitre
- **Confettis** : animation post-boost terminé
- **Messages** : ton ado "Game Boy Chill" (EASY×7 variantes, HARD×3)

---

## Backend — Google Apps Script

### Point d'entrée

```javascript
function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  switch(data.action) {
    case 'register': return register(data);
    case 'login': return login(data);
    case 'save_score': return saveScore(data);
    // ...
  }
}
```

### Actions GAS — état @52

| Action | Description | Statut |
|---|---|---|
| `register` | Inscription élève. TrialStart = TODAY, email J+0 auto | ✅ |
| `login` | Connexion. Retourne trial, boostExosDone, pendingBrevet, nextChapter, nextBoostTopic | ✅ |
| `save_score` | Sauvegarde réponse. MAJ Progress + rebuildSuivi + writeToHistorique + ExosDone si BOOST | ✅ |
| `save_boost` | Sauvegarde fin de boost. ExosDone + rebuildSuivi | ✅ |
| `generate_diagnostic` | Génère diagnostic. Mode guest (sans code) pour landing flow | ✅ |
| `generate_daily_boost` | Génère boost quotidien filtré sur chapitres diagnostiqués | ✅ |
| `generate_remediation` | ⏸️ Désactivé — return success immédiat | ⏸️ |
| `get_progress` | Récupère progression par chapitre | ✅ |
| `detect_fragile_prereqs` | Détection prérequis fragiles (archivé → false) | ✅ |
| `get_prerequisites` | Liste prérequis | ✅ |
| `enqueue` | File d'attente (archivée → erreur propre) | ✅ |
| `generate_exam_prep` | Préparation examen par chapitre (10q : 7 lvl2 + 3 lvl1) | ✅ |
| `generate_brevet` | Brevet multi-chapitres (~15q style Brevet) — UI désactivé | ✅ |
| `generate_revision` | Révision niveau inférieur — UI désactivé | ✅ |
| `submit_feedback` | Feedback élève → onglet Insights | ✅ |
| `generateMorningReport` | Rapport matin 7h (génération IA désactivée) | ✅ |
| `get_admin_overview` | Vue admin complète (boostHistory, chapitresDetail, brevets) | ✅ |
| `publish_admin_boost` | Admin publie boost (→Nouveau Boost col 18) + rebuildSuivi | ✅ |
| `publish_admin_chapter` | Admin publie chapitre (→Nouveau Ch libre) + rebuildSuivi | ✅ |
| `check_trial_status` | Vérifie trial actif { trialActive, daysLeft, isPremium } | ✅ |
| `import_chapters` | One-shot admin — pousse chapitres dans Curriculum_Officiel + DiagnosticExos | ✅ |
| `send_test_email` | Admin — envoie email J+0 test | ✅ |
| `mark_all_test` | Admin one-shot — marque tous comptes non-admin sans IsTest → IsTest=1 | ✅ |
| `generate_brevet_session` | Génère session brevet (chapitres → exos mélangés) | ✅ |
| `save_brevet_result` | Sauvegarde résultat brevet dans BrevetResults | ✅ |
| `publish_admin_brevet` | Admin publie brevet blanc personnalisé | ✅ |
| `get_brevet_chapters` | Liste chapitres disponibles dans BrevetExos | ✅ |
| `request_brevet_chapter` | Élève demande chapitre manquant → Insights | ✅ |
| `import_brevet_exos` | One-shot admin — pousse exercices dans BrevetExos | ✅ |

### Fonctions internes clés

| Fonction | Rôle |
|---|---|
| `rebuildSuivi(code)` | Recalcule la ligne 👁 Suivi de l'élève (appelé dans save_score, save_boost) |
| `writeToHistorique(p)` | Insère en ligne 2 de 📋 Historique (récent en haut) |
| `updateConfidenceScore(...)` | Met à jour Progress après chaque réponse |
| `_pickDiagExos(exos, chapCount)` | Smart count diagnostic : 1ch→4q, 2ch→6q, 3ch→8q, 4+→10q |

### Rapport matin (generateMorningReport)

Trigger GAS quotidien 7h. Analyse chaque élève :

| Statut | Critères |
|---|---|
| ✅ ACQUISE | score > 80, statut='maitrise', 0 HARD depuis 14j, ≥3 sessions |
| 🔴 BLOQUEE | score < 40, pas d'amélioration 2 semaines, ≥4 sessions |
| 🟡 FRAGILE | score < 40 OU ≥3 HARD cette semaine |
| 📈 EN_PROGRESSION | taux erreur semaine < semaine passée (−10 pts) |
| 📘 EN_COURS | défaut |

Email sujet `[Matheux ⚡ ACTION]` si fragiles/bloquées.

---

## Flux de données principaux

### Inscription → premier boost

```
1. Parent remplit landing (niveau + chapitres)
2. Quiz calibrage inline (4-10 questions)
3. Formulaire prénom + email → register() GAS
4. GAS : crée Users + email J+0 auto
5. Auto-login → onboarding 3 slides
6. boostFromDiag() en background → DailyBoosts
7. Élève voit son premier boost
```

### Exercice → suivi admin

```
1. Élève répond à un exercice
2. Frontend → save_score(code, categorie, resultat, temps, ...)
3. GAS : écrit Scores + updateConfidenceScore(Progress) + rebuildSuivi(code) + writeToHistorique
4. 👁 Suivi mis à jour → ACTION NICOLAS recalculé
5. Nicolas voit l'action dans le dashboard admin
```

### Publication boost (admin)

```
1. Nicolas ouvre admin → voit ⚡ BOOST TERMINÉ
2. Copie prompt Claude → génère JSON 5 exos
3. Colle dans "Publier un boost" → publish_admin_boost GAS
4. GAS : écrit →Nouveau Boost (col 18 Suivi) + rebuildSuivi
5. Au prochain login élève : login() lit col 18 → crée DailyBoosts (exosDone=0)
6. Admin voit ⏳ En attente
```

---

## Infrastructure

| Service | Usage | Coût |
|---|---|---|
| GitHub Pages | Frontend (index.html, pages légales) | Gratuit |
| Google Apps Script | Backend API | Gratuit (quotas Google) |
| Google Sheets | Base de données | Gratuit |
| Gmail (GmailApp) | Emails auto (J+0, J+3, J+7) | Gratuit |
| Stripe | Paiement (TEST pour l'instant) | ~0,39€/transaction |
| GA4 | Analytics | Gratuit |

Commandes de déploiement : voir [claude.md](claude.md#déploiement).

---

## Scripts Python utilitaires

| Script | Usage | Dangereux ? |
|---|---|---|
| `sheets.py` | Bibliothèque accès Google Sheets (staging) | Non |
| `rebuild_sheet.py` | Reconstruit 👁 Suivi et 📋 Historique | Non |
| `create_demo_student.py` | Crée profil démo + simule diagnostic + boost | Non |
| `create_5_students.py` | Crée 5 profils variés (test scénarios) | Non |
| `test_full_v2.py` | Suite de tests GAS complète (73/74) | Non |
| `cleanup_prod.py` | Nettoyage complet base prod | ⚠️ IRRÉVERSIBLE |
| `fix_lucas_ines.py` | Ajuste profils démo spécifiques | Non |
| `import_brevet_exos.py` | Pousse brevet_exos_3eme.json → BrevetExos | One-shot |

Scripts archivés dans `scripts_archive/`.

---

## Fonctionnalités stables

> Ne pas toucher sans raison explicite.

- CSS/UI complet, mobile-first, animations
- Landing page : hero direct, 3 faits, prix seul, CTA final
- Mode Brevet Blanc : onglet 🎓 Brevet (3EME), 120 exos, quiz sans indices, résultats détaillés
- Mode Révision : code conservé, UI désactivé
- Feedback non-intrusif : bouton "Signaler" → Insights
- Auth register + login + auto-login silencieux
- Scores enrichis : temps, wrongOpt, indices, formule
- Swipe gauche → exercice suivant
- Admin panel (triple-clic logo), dark mode admin
- Gamification : XP, streak, mastery ring SVG
- MathJax v3 avec fallback, chrono par exercice
- Nudge pills après 20s, tableau blanc maths
- Vue Progression, bannière prérequis fragiles
- Essai 7j : badge J-X, overlay, onboarding 3 slides
- Flow landing CTA complet
- Post-boost : confettis + auto-redirect 5s
- Modales admin contextuelles (BOOST/CHAPITRE séparés)
- Indicateurs emails J0/J3/J7 dans modal admin
