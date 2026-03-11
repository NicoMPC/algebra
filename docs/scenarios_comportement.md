# Matheux — Scénarios de comportement complets
> Dernière mise à jour : 2026-03-10

---

## PARTIE 1 — L'ÉLÈVE (flux complet)

### S-E1 · Première inscription
**Contexte :** Un nouvel élève arrive sur matheux.fr

1. L'élève clique "Commencer" sur la landing
2. Remplit : Prénom, Email, Mot de passe, Niveau (6EME/5EME/4EME/3EME)
3. Sélectionne 2 à 6 chapitres à réviser (affichés selon son niveau)
4. Clique "Lancer mon diagnostic"
→ **GAS :** `register` crée le compte (Users) + `generate_diagnostic` pioche 1 exercice lvl1 + 1 lvl2 par chapitre sélectionné (DiagnosticExos)
→ **Frontend :** L'élève voit les exercices QCM enchaînés, MathJax rendu, timer visible

**Test couvert :** S1 #01-04

---

### S-E2 · Diagnostic initial
**Contexte :** L'élève répond aux exercices de diagnostic

1. 2 exercices par chapitre sélectionné (ex : 2 chapitres = 4 exercices)
2. Sur chaque exercice : 3 options, bouton "Indice" (coût en XP), bouton "Formule"
3. Réponse → feedback immédiat (vert/rouge) + explication étape par étape
4. Résultat EASY ou HARD stocké dans Scores (avec temps, indices, formule, mauvaise option)
5. Après le dernier exercice : résumé + insight + accès aux chapitres
→ **GAS :** `save_score` × N → `rebuildSuivi(code)` → `writeToHistorique(p)`
→ **Frontend :** Cartes chapitres avec badge vert si déjà vu, badge NEW si injecté par Nicolas

**Test couvert :** S1 #05, S2 #22-23

---

### S-E3 · Exercices de chapitre (20 exercices)
**Contexte :** L'élève travaille un chapitre

1. Sélectionne un chapitre depuis l'accueil
2. Exercices QCM niveau 1 puis niveau 2 (mélangés si remédiation)
3. Swipe gauche = passer, Swipe droite = valider
4. Timer par exercice (compte-tours, pause si onglet caché)
5. Nudge pédagogique après 20s d'inactivité
6. Après 20 exercices : "✅ Chapitre terminé ! Ton prof prépare ton prochain chapitre personnalisé."
7. Badge "🔄 Demain" sur la carte du chapitre
→ **GAS :** `save_score` × 20 → `rebuildSuivi` → l'ACTION passe à "✅ CHAPITRE TERMINÉ → assigner suite"
→ **Nicolas** voit le badge rouge dans le dashboard → agit

**Test couvert :** S1 #10, S4 #40-45

---

### S-E4 · Boost quotidien (5 exercices)
**Contexte :** L'élève fait son boost du jour

1. Bouton ⚡ Boost du jour (visible si boost disponible)
2. 5 exercices ciblés sur ses lacunes (ou injectés par Nicolas)
3. Insight motivant en tête du boost
4. Après 5 exercices : "⚡ Boost du jour terminé ! Tu es à jour."
→ **GAS :** `generate_daily_boost` pioche dans Curriculum_Officiel (chapitres diagnostiqués, HARD prioritaires)
   OU boost injecté par Nicolas → reçu via `nextBoost` au login
→ **Frontend :** `boostConsumed` = true → le bouton Boost devient grisé ce jour

**Test couvert :** S1 #06-07, S3 #30-37

---

### S-E5 · Réception du contenu de Nicolas
**Contexte :** Nicolas a publié un boost ou un chapitre pour cet élève

1. L'élève se reconnecte
2. `login()` lit la colonne →Nouveau du Suivi
3. Si →Nouveau Ch rempli → `nextChapter` injecté dans la réponse → cellule vidée
4. Si →Nouveau Boost rempli → `nextBoost` injecté → cellule vidée
5. `rebuildSuivi()` appelé → couleurs mises à jour
→ **Frontend :** Badge "🆕 NEW" sur la carte du chapitre, ou boost disponible immédiatement

**Test couvert :** S1 #14-19, S7 #68, S11 #89, #92

---

### S-E6 · Vue Progression
**Contexte :** L'élève veut voir sa progression

1. Clic sur "Progression" dans la nav
2. Liste des chapitres : barre de confiance colorée, dates relatives, badge "Maîtrisé" si score > 80%
3. Données issues de Progress sheet (via `get_progress`)

**Test couvert :** (non automatisé — test visuel)

---

### S-E7 · Bannière prérequis fragiles
**Contexte :** L'élève a des prérequis insuffisants

1. Avant chaque session exercices, `detect_fragile_prereqs` vérifié
2. Bannière ambre si prérequis fragile détecté
3. Clic sur bannière → redirigé vers le chapitre prérequis

**Test couvert :** (non automatisé)

---

### S-E8 · Reconnexion multiple sans action
**Contexte :** L'élève se reconnecte 5x sans faire d'exercice

- Aucun doublon dans Scores, Suivi, DailyBoosts
- Progression conservée (history stable)
- `sent` Set empêche les doublons de save_score

**Test couvert :** S5 #46-48

---

### S-E9 · Déconnexion mid-chapitre
**Contexte :** L'élève ferme l'appli au milieu d'un chapitre

1. Les scores déjà envoyés sont dans Scores (sauvegarde immédiate à chaque exo)
2. Aucune perte de données
3. Reconnexion → history contient les scores partiels
4. Le chapitre reprend au bon compteur côté frontend

**Test couvert :** S4 #40-43

---

## PARTIE 2 — NICOLAS (flux admin)

### S-A1 · Connexion admin → dashboard automatique
**Contexte :** Nicolas se connecte à matheux.fr avec son compte

1. Entre email + mot de passe → login GAS
2. `login()` retourne `isAdmin: true`
3. `initApp()` détecte `S.prof.isAdmin` → skip le flux élève
4. FAB ✏️ caché, nav cachée
5. Redirigé directement sur "Mes Élèves" (renderAdminDashboard)
→ **GAS :** `get_admin_overview` appelé automatiquement

**Test couvert :** S11 #82-83

---

### S-A2 · Lecture du dashboard "Mes Élèves"
**Contexte :** Nicolas voit la liste de tous ses élèves

1. Cartes triées : urgents en tête (🔴 > 🆕 > ✅), puis par dernière connexion
2. Sur chaque carte :
   - Avatar initiale colorée + Prénom + Niveau
   - Badge action coloré si action requise
   - Barre de réussite globale (% EASY sur 30 jours) + compteur d'erreurs
   - Chapitres en cours avec % de réussite par chapitre
   - Badges "⚡ boost prêt" / "📚 chap prêt" si déjà publié en attente
3. Badge rouge "N actions" dans l'en-tête si des élèves ont besoin d'action

**Les 4 types d'ACTION :**
| Badge | Condition | Priorité |
|-------|-----------|----------|
| 🔴 DIAGNOSTIC FAIT → préparer boost 1 | A fait des exercices mais 0 boost | 1 |
| 🆕 BOOST TERMINÉ → préparer boost suivant | A consommé le boost d'hier | 2 |
| ✅ CHAPITRE TERMINÉ → assigner suite | ≥20 exos sur un chap + col Nicolas vide | 3 |
| 👍 RAS | Tout est OK | — |

**Test couvert :** S11 #82-84, #93

---

### S-A3 · Ouverture du modal élève
**Contexte :** Nicolas clique sur une carte

1. Modal s'ouvre (bottom sheet mobile / centered desktop)
2. Header : Avatar + Prénom + Niveau + date dernière connexion
3. Badge action coloré en tête
4. Section "📊 Exercices par chapitre (30 jours)" :
   - Un bloc par chapitre (trié : le plus fragile en premier)
   - Barre de réussite colorée (rouge < 50%, ambre 50-75%, vert > 75%)
   - Métriques : ⏱ temps moyen, 💡 indices moy., 🧮 % formule
   - Liste des exercices : ✅/❌ + énoncé + pills (temps, indices, formule)
   - **Bouton "📋 Copier le prompt Claude — Boost ciblé [Chapitre]"**

**Test couvert :** S11 #86

---

### S-A4 · Génération d'exercices via Claude
**Flux normal (30 secondes en tout) :**

1. Nicolas clique "📋 Copier le prompt Claude — Boost ciblé Fractions"
2. Le prompt est automatiquement copié dans le presse-papier (**pas besoin de rien faire**)
3. Toast : "📋 Prompt copié ! Colle-le dans Claude ou ChatGPT."
4. Nicolas ouvre Claude/ChatGPT (nouvel onglet) → Ctrl+V → Envoyer
5. Claude retourne le JSON
6. Nicolas sélectionne le JSON → Ctrl+C → retour sur Matheux
7. Colle dans la textarea "⚡ Publier un boost" ou "📚 Publier un chapitre"
8. Clique "Enregistrer ce boost" ou "Enregistrer ce chapitre"
9. ✅ Toast vert + carte de l'élève passe au vert + modal se ferme

**Ce que contient le prompt généré automatiquement :**
- Prénom, niveau de l'élève
- Statistiques du chapitre (taux réussite, temps moyen, indices, formule)
- Liste des erreurs ciblées (énoncé + mauvaise réponse + contexte)
- Format JSON strict avec exemple complet
- Règles impératives (a dans options, steps 2-4, lvl 1 ou 2, etc.)

**Test couvert :** Testé fonctionnellement (copyAdminPrompt) — pas de test automatisé (clipboard)

---

### S-A5 · Publication d'un boost
**Contexte :** Nicolas a le JSON, le colle dans la textarea et publie

1. Validation JSON côté frontend (try/catch + vérif exos[])
2. Si invalide → toast ❌ clair, textarea reste remplie
3. Si valide → POST `publish_admin_boost` au GAS
4. **GAS :** Validation format (q, a, options, a∈options) + écriture JSON dans Suivi col S (→Nouveau Boost) + `rebuildSuivi()`
5. **Frontend :** Toast ✅ + mise à jour carte en mémoire (action → RAS, boostNew → true) + modal fermé
6. **L'élève :** Au prochain login, `login()` lit col S → injecte `nextBoost` → vide la cellule → l'élève voit les exercices immédiatement

**Test couvert :** S11 #87-90

---

### S-A6 · Publication d'un chapitre complet
**Contexte :** L'élève a terminé un chapitre → Nicolas lui assigne le suivant

1. Nicolas clique le bouton "📋 Copier le prompt Claude — Chapitre complet [Nom]"
2. Même flux que S-A4 mais pour 20 exercices (lvl1 × 10 + lvl2 × 10)
3. Colle le JSON dans "📚 Publier un chapitre complet"
4. **GAS :** Écrit dans la première colonne →Nouveau Ch libre (G/J/M/P) ; fallback écrase la plus ancienne si tout plein
5. **L'élève :** Au prochain login → `nextChapter` injecté → badge NEW sur la carte chapitre

**Test couvert :** S11 #91-92

---

### S-A7 · Gestion de la charge (>10 élèves actifs simultanément)
**Contexte :** Nicolas a beaucoup d'élèves actifs

- Dashboard chargé en 1 appel GAS (`get_admin_overview` lit Suivi + Scores en une fois)
- Cartes scrollables, recherche visuelle rapide (action en couleur)
- Modal fermé avec ✕ ou clic en dehors

---

### S-A8 · Cas limites et guards
| Situation | Comportement attendu |
|-----------|---------------------|
| JSON invalide collé | Toast ❌ clair, pas d'envoi GAS |
| JSON sans champ "a" dans "options" | GAS retourne erreur 400, toast ❌ |
| Élève non encore dans Suivi | GAS appelle `rebuildSuivi()` + retry |
| 4 slots →Nouveau Ch tous pleins | Écrase le slot le plus ancien (col G) |
| Code admin invalide | GAS retourne "Accès refusé" |
| Réseau coupé pendant publish | Toast ❌ "Erreur réseau", bouton reset |

**Test couvert :** S11 #85, S6 #56-60, S9 #76-78

---

## PARTIE 3 — COUVERTURE DU TEST AUTOMATISÉ

### Mapping scénarios → tests

| Scénario | Tests | Couverture |
|----------|-------|------------|
| S-E1 Inscription | #01-04 | ✅ Complet |
| S-E2 Diagnostic | #05, #22-23, #27-28 | ✅ Complet |
| S-E3 Chapitre 20 exos | #10, #40-45 | ✅ Complet |
| S-E4 Boost | #06-07, #30-37, #65-66 | ✅ Complet |
| S-E5 Réception contenu Nicolas | #14-19, #68, #89, #92 | ✅ Complet |
| S-E8 Reconnexion multiple | #46-48 | ✅ Complet |
| S-E9 Déconnexion mid-chapitre | #40-43 | ✅ Complet |
| S-A1 Login admin redirect | #82-83 | ✅ Couvert |
| S-A2 Dashboard avec tri | #83, #93 | ✅ Couvert |
| S-A3 Données modal riches | #84, #86 | ✅ Couvert |
| S-A4 Prompt Claude | — | ⚠️ Test visuel (clipboard non testable en auto) |
| S-A5 Publish boost | #87-90 | ✅ Complet : publish + réception login |
| S-A6 Publish chapitre | #91-92 | ✅ Complet : publish + réception login |
| S-A8 Guards JSON/access | #85, S6+S9 | ✅ Couvert |

### Résultat attendu : **89/93 tests OK** (4 race conditions GAS acceptées : #23, #27, #75, #79)

---

## PARTIE 4 — LOGIQUE DE BOUT EN BOUT (pour la présentation)

```
ÉLÈVE          MATHEUX (GAS)            NICOLAS
  │                  │                      │
  │── login ────────▶│                      │
  │◀── curriculum ───│                      │
  │                  │                      │
  │── save_score ───▶│── rebuildSuivi() ──▶ Suivi Sheet
  │   × 20 exos      │   ACTION = ✅ TERMINÉ│
  │                  │                      │
  │                  │                 [Dashboard]
  │                  │              Nicolas voit le badge
  │                  │              "✅ CHAPITRE TERMINÉ"
  │                  │                      │
  │                  │              [1 clic] Copier prompt
  │                  │              [30s]   Claude génère JSON
  │                  │              [1 clic] Coller + Enregistrer
  │                  │                      │
  │                  │◀── publish_admin ─────│
  │                  │    _chapter()         │
  │                  │── Suivi →Nouveau ──▶ col G remplie
  │                  │                      │
  │── login ────────▶│                      │
  │◀── nextChapter ──│ (col G lue + vidée)  │
  │   badge "🆕 NEW" │                      │
  │                  │                      │
```
