# 40 — Parcours cible & épuration de l'app (UX)

> Agent : dev-ux (volet UX) · 24/09/2026 · branche `feat/diagnostic-3e`
> Entrées : `00-contrat-commun.md` (vision, objet Carte, décisions §7), `CLAUDE.md`, `docs/product.md`,
> `docs/messages.md`, `docs/playbook-*.md`, lecture réelle de `app.html` (13 796 L), `premium.html`, `index.html`.
> Maquettes : `docs/specs/maquettes/0X-*.html` + captures `.png` (375 px, Chrome headless, ×2).
> Rien n'a été modifié dans `app.html`. C'est un document de conception.

---

## 0. En une page

**Le produit tient en une boucle : diagnostic → carte → séance du jour → la carte bouge.**
Tout ce qui ne sert pas cette boucle part. Tout ce qui suppose que Nicolas fasse quelque chose part aussi.

- **Écran d'accueil = une seule carte "Ta séance du jour"** (5 exos, prête tout de suite, choisie par le moteur). Il n'y a plus de liste de chapitres, plus de cascade hero P1→P6, plus d'archives.
- **L'unité visible devient la compétence** (statuts 🔴🟠🟢⚪ du contrat §4), plus le chapitre ni le %. La carte sert en même temps de tableau de progression, de menu d'entraînement (en payant) et de support de vente.
- **La sensation "l'appli s'adapte à moi"** repose sur 3 micro-éléments, pas sur des features : (1) un « 💡 Pourquoi cet exo ? » sur chaque séance, (2) l'**erreur type nommée** après une mauvaise réponse (grâce au champ `err` des items), (3) un bloc « **Ce qui a bougé aujourd'hui** » en fin de séance (🔴→🟠).
- **Gamification** : il reste le streak 🔥 (avec son freeze) et la mission du jour 🎯 n/5. On coupe XP, paliers, milestones, slots, mode flow, tour guidé, tuto, onboarding, et presque tous les confettis.
- **Le parent est l'acheteur** : le partage du bilan (lien + aperçu WhatsApp/SMS, page parent dédiée, envoi auto par mail à l'inscription) est le **levier de conversion principal**. Le CTA de l'ado dans le paywall est « Demander à mes parents ».

---

## 1. Inventaire de `app.html` (existant réel)

Légende : ✅ garder tel quel · ✏️ adapter · ❌ supprimer · 💤 masquer (le code reste, non branché, réactivable)
⚠️ = dépendance dangereuse (retirer ce code peut casser autre chose, voir §1.2).
Contexte : tous les anciens comptes sont supprimés (contrat §7). **Aucune rétrocompat élève à préserver**, donc le code legacy passe en ❌ sans migration.

### 1.1 Tableau

#### A. Coque, boot, infra

| # | Feature / écran | Fonctions · ~lignes | Verdict | Justification |
|---|---|---|---|---|
| A1 | Meta SEO, JSON-LD, OG (« Brevet 2026 », 29,99 €) | `<head>` L1-120 | ✏️ | Contenu périmé (Brevet 2026, ancien prix) ; `app.html` passe en `noindex`, le SEO revient à la nouvelle landing. |
| A2 | GA4 conditionné + bannière cookies | `loadGA4` L131, bannière L13391, `_track` L13424 | ✅ | Obligation RGPD, déjà correct. |
| A3 | KaTeX + fallback cdnjs | L151-170, `_doKatex` L2384, `rMath` L2397 | ✅ | Indispensable pour le rendu des items. |
| A4 | Tailwind CDN + CSS custom, variables `--mx-*` / `--p` | L170-1300 | ✅ | Charte conservée ; pas de réécriture. |
| A5 | Offline queue des scores | `sendScore` L2424, `flushQ` L2470, `_scheduleRetry` L2490 | ✅ | Critique : aucune réponse ne doit être perdue (et encore plus pendant un diagnostic payant). |
| A6 | Hash MDP, `tod()`, `fmtL` | L2151-2192 | ✅ | Règle RGPD (hash client) + utilitaires. |
| A7 | Toast mutex (M1) | `showT`/`hideT` L2206-2237 ; doublon `_toast` L13477 | ✅ | Invariant M1 conservé. `_toast` peut rester (contact form). |
| A8 | Modale alerte générique | `alert2`/`closeAlert` L2341 | ✅ | Utile pour les erreurs réseau. |
| A9 | Page teasing pré-lancement (compte à rebours 18/03, waitlist) | HTML L1484-1568, IIFE L2517-2610 (`isBeforeLaunch`, `showTeasing`, `_teasingSubmitEmail`) | ❌ ⚠️ | Date passée depuis 6 mois. ⚠️ L'IIFE contient aussi le **hash routing** (`#diag-*`, `#login`) et fait `return` si `#teasing-screen` est absent : il faut sortir le routing **avant** de supprimer le HTML. |
| A10 | Hash routing landing → app | dans l'IIFE L2566-2590 | ✏️ | Nouveau contrat d'entrée : `app.html#diag` (+ `?src=`), `#login`, `#bilan-<token>` (cf. §4). |
| A11 | PWA : nudge d'install, tuto iOS | `_checkPwaInstall` L13520, `_showIosTuto` L13629, `_trackPwa` L13618 | ✏️ | Garder, mais déclencher après la **3e séance faite**, jamais pendant le diagnostic (aujourd'hui : 5 s après login + dans le tour). |
| A12 | Mode nuit | `toggleAppNight` L2617, CSS `body.app-night` | ✅ | Apprécié des ados le soir, et ne coûte rien. |
| A13 | Formulaire contact + modale feedback + footer légal | `openContactForm` L13484, modale L13430 | ✅ | Seul canal humain, asynchrone. |
| A14 | Panneau DEV (simTime, forceFail) | HTML L2021-2034, `triggerAdmin`/`simTime`/`forceFailChap` L2158-2171, branche `S.forceFail` dans `mark` | ❌ | Outil de test mort, et il pollue `mark()`. |
| A15 | Constantes legacy `DEMO_QS`, `CHAPS_BY_LEVEL`, `BREVET_PACK`, `CHAP_BLOCS`, `TS` | L2058-2078 | ❌ | Liées aux chapitres et au diag 5 questions. Remplacées par le référentiel (domaines/compétences). |
| A16 | Mode `lite` (`S.lite`) | ~25 branches (`render`, `_isChapLocked`, `_needsCoach`…) | ❌ | Mode sans boost ni gratuit, jamais documenté, plus aucun compte concerné. |
| A17 | Stubs figures morts | `autoDetectFigure`/`renderFig`/`isGeoCat` L9744-9746 | ❌ | Retournent `null`/`''`/`false`. |

#### B. Entrée, diagnostic express, inscription

| # | Feature / écran | Fonctions · ~lignes | Verdict | Justification |
|---|---|---|---|---|
| B1 | Écran d'accueil minimal dans l'app (« 1 minute pour savoir où tu en es ») | HTML L1574-1648 | ✏️ | Devient l'**intro du diagnostic** (E1) : 15 q, ~8 min, pas de note. Faux social proof (« Utilisé partout en France ») supprimé. |
| B2 | Stepper Diagnostic → Inscription | L1652-1665, `_flowSetStep` L2839 | ✏️ | On garde la barre segmentée des questions (maquette 01). Le stepper 2 étapes disparaît : l'inscription arrive après la carte. |
| B3 | Step 1 « Comment on t'aide ? » + choix par blocs | HTML `flow-s1` L1667-1690, `_flowPickBrevet`, `_flowPickBlocs`, `_flowToggleBloc`, `_flowBackToChoice` L2879-2924 | ❌ | Déjà du code mort (commenté « Mort code »). Le moteur choisit les questions lui-même. |
| B4 | Diagnostic express 5 questions | `flowSelectLevel` L2871, `flowToStep3` L2925, `_pickDiagExos` L2944, `_flowStartDiag` L2984 (`generate_diagnostic`) | ✏️ | ~15 q **adaptatives** : question suivante demandée au serveur (API du 20-moteur). Fini le tirage de 5 questions côté client. |
| B5 | Rendu question + réponses du diag | `_flowRenderQuestion` L3045, `_flowAnswerOpt` L3141, `_flowAnswerFill` L3208, `_flowAnswerJsp` L3245 | ✏️ | Rendu conservé (même UX que les exos). **Pendant le diag : on retire les indices et la formule** (sinon ça fausse la mesure). On garde « 🤷 Je ne sais pas », qui est une vraie donnée. Pas de correction immédiate (Q1). |
| B6 | `guestDiag` localStorage (« fresh start toujours ») | L2998-3005, purge L2826 | ✏️ | À 8 min, un abandon coûte cher : on **reprend** le diag express (TTL 24 h, id de session serveur). Seul l'id va en localStorage, pas les réponses (RGPD). |
| B7 | Écran résultat (barre %, récit, tags chapitres) | `_flowActivateStep3Guest` L3396-3493 | ✏️ | Remplacé par la **carte partielle** (maquette 02), rendue depuis l'objet Carte `type:"express"`. Même renderer que dans l'app. |
| B8 | Choix d'objectif (lacunes / brevet…) | `_showObjectifPicker` L3343, `_flowShowObjectifScreen` L3495, `_flowGoToRegister` L3508, slide 3 d'onboarding | ❌ | Le moteur ne s'en sert pas. C'est une friction de plus. |
| B9 | Upsell avant inscription (29,99 €) | `_flowShowUpsell` L3514, `_flowSkipUpsell` L3567 | ❌ | Demander de payer avant d'avoir montré de la valeur, ça fait fuir. Le paywall vit désormais dans la carte partielle (zone floutée). |
| B10 | Formulaire d'inscription (prénom, email parent, mdp, consentement) | HTML `flow-s3` L1697-1724, `_flowToRegisterDirect` L3579, `_flowGuestRegister` L3595-3740 | ✏️ | Garder les 3 champs. Le bouton devient « Créer mon espace et envoyer ma carte à mes parents » : il déclenche l'envoi auto du bilan express (Q3). `save_calibration_batch` est remplacé par le rattachement de la session diag au profil. |
| B11 | Lancement post-inscription | `flowRegister` L3743, `_doLoginAndLaunch` L3760-3918 | ✏️ | Retirer tour, onboarding et `boostFromDiag`. Enchaîner directement sur l'accueil quotidien avec la séance n°1 prête. |
| B12 | Écran auth (login / register / tabs) | HTML L1742-1848, `showAuth` L2635, `switchTab` L2671, `submitAuth` L3926, `updateLevelChapters` L2761 | ✏️ | **Login seulement.** On ne s'inscrit plus qu'en passant par le diagnostic (un seul chemin, un seul état à tester). |
| B13 | Mot de passe oublié | `showForgotForm`…`submitResetPassword` L2684-2760 | ✅ | Nécessaire, fonctionne. |
| B14 | Chemin d'inscription legacy avec choix de chapitres + calibrage in-app | `finalizeOnboarding` L3982, `startCal` L5334, `S.calState 'sel'/'test'` dans `render` L8206-8240, branche `CALIBRAGE` de `chkComp`, `renderDiagInsight` L7838 | ❌ | Chemin parallèle, jamais atteint depuis le flow invité : deux diagnostics différents, c'est une source de bugs. |
| B15 | Onboarding 2-3 slides | `showOnboarding` L4136, `_onbRender` L4161, `_onbNext` | ❌ | Décision Nicolas (couper). La carte suffit comme accueil. |
| B16 | Tour guidé 8 étapes (spotlight + PWA) | `_startTour`…`_tourEnd` L4198-4385 | ❌ ⚠️ | Décision Nicolas. ⚠️ Le bouton d'install PWA vit dans le tour : il passe dans A11. |

#### C. Monétisation & sécurité

| # | Feature / écran | Fonctions · ~lignes | Verdict | Justification |
|---|---|---|---|---|
| C1 | Badge « 🔓 1 chapitre gratuit » | `renderTrialBadge` L4389 | ✏️ | Devient un petit chip « Gratuit » dans le header, qui ouvre le paywall. Plus de notion de chapitre gratuit. |
| C2 | Overlay chapitre verrouillé | `showLockedOverlay` L4411, `__unlockAll`, `__lockedDismiss`, `showTrialExpired` L4406 | ✏️ | Remplacé par l'**écran paywall** (maquette 03) : 2 offres + « Demander à mes parents ». |
| C3 | Liens Stripe par niveau + `_stripeUrl` (client_reference_id, prefilled_email) | L4437-4461 | ✏️ | On garde le mécanisme `client_reference_id=code`. Liens remplacés par **2 produits** (Diagnostic 19 €, Programme 49 €, plus un lien « upgrade » à 30 €). Prix et liens dans **une seule constante `OFFRE`** (contrat). |
| C4 | Retour Stripe `?payment=success` + poll | L4053-4121, `_showPaymentSuccess`, `_showPaymentFallback` | ✏️ | Message propre à chaque produit (« Diagnostic complet débloqué → Commencer le module 1 »). Le texte « Bon courage pour le Brevet » sort. |
| C5 | Garde premium 9 modules (poll 5 min, scellement, hash d'intégrité, boucle 30 s, visibilité, **détection DevTools**, **anti-debugger**, gate synchrone) | L4819-5003 : `startPremiumGuard`, `_verifyPremiumStatus`, `_sealTrial`, `_trialHash`, `_updateIntegrityHash`, `_checkLocalIntegrity`, `_startLocalIntegrityLoop`, `_startVisibilityGuard`, `_detectDevTools`, `_startAntiDebugger`, `isPremiumOrTrialValid` | ❌ ⚠️ | C'est du théâtre de sécurité : le serveur est le seul vrai gate (il ne sert que les items autorisés). L'anti-debugger coûte en perf et en risque de faux positifs. On le remplace par `S.acces` rafraîchi au login et au `visibilitychange`. ⚠️ `_sealTrial` **gèle** `S.trial` (on ne peut plus lui ajouter de champs), et `_updateIntegrityHash` est appelé depuis l'inscription (L3672). Tout retirer ensemble. |
| C6 | Gate freemium par chapitre | `_isChapLocked` L5657, appels dans `togCat`, `openFromProgress`, hero, cartes | ✏️ | Remplacé par `_can(feature)` sur `S.acces = {diag_complet, programme}`. Gratuit = séance du jour sur le point faible uniquement. |

#### D. Boucle d'exercice (le cœur, à préserver)

| # | Feature / écran | Fonctions · ~lignes | Verdict | Justification |
|---|---|---|---|---|
| D1 | Rendu exercice QCM / VF / fill, bannière contexte, tableaux, consigne de tracé | `rSection` L9122-9381 | ✅ | Solide, compatible avec les champs d'items du contrat §3. Ajout ✏️ mineur : ligne « 💡 Pourquoi cet exo ? » (lot L6). |
| D2 | Sélection + validation, normalisation fill (P7) | `selectOpt`/`validateAnswer` L5420-5536, `_normFill` L5369, `_toNum`, `_matchFill` | ✅ | Invariants P7 conservés. ✏️ ajout : si la réponse fausse figure dans `item.err`, **nommer l'erreur type** dans le feedback. |
| D3 | Flashcard « Révéler la réponse » + auto-évaluation À revoir / Je doute / Acquis | `verify` L5537, `acts` L9187-9200 | ❌ | L'auto-évaluation pollue la maîtrise (c'est l'ado qui décide « Acquis »). Tous les nouveaux items ont un type fermé ou fill. |
| D4 | `mark()` : score, XP, streak, milestone, daily, slot, cours, auto-avance | L5545-5655 | ✏️ ⚠️ | Réduit à : score → streak → mission du jour → avance → fin de séance. ⚠️ Voir §1.2 (payload XP, branche `_slotNum`, overlay série perdue). |
| D5 | Passer (différé P11) / Je ne sais pas (SKIP) | `S.deferred`, `nextEx` L5792, `_flowAnswerJsp` | ✅ | En séance : on garde les deux. En diag : JSP seulement (un différé n'a pas de sens dans un test adaptatif). |
| D6 | Indices progressifs + formule (P6), aide auto après erreur | help pills, `_previewHelp` L9063, `autoShowHelp` L10129, `typewriter` L10112 | ✅ | C'est la vraie aide pédagogique. Masqués pendant les diagnostics uniquement. |
| D7 | Nudge « Psst, un indice ? » après 20 s | `startNudge`/`clearNudge` L10230-10255, appel dans `render` L8184 | ❌ ⚠️ | Bruit, et source d'un bug connu (C1). ⚠️ `render()` appelle `clearNudge` sur `_nudgeTimers` : retirer l'appel en même temps. |
| D8 | Figures paramétrées + graphes de fonctions | `_fig*` L9748-10011, `extractFunction`/`renderFunctionGraph` L10020-10108 | ✅ | Utiles en géométrie et en fonctions. |
| D9 | Brouillon + calculette (FAB ✏️, symboles contextuels) | HTML L1933-2006, `toggleDraft` L9501, `switchDraftTab`, `getContextSymbols` L9395, `calc*` L9536-9743 | ✅ | Outil de travail réel. Aucune dépendance au modèle chapitre, à part `getDraftCat`, à brancher sur le domaine. |
| D10 | Timer 60 s / 30 s automatismes (G12, G14) | `_getTimerDuration`…`_renderTimerSVG` L10260-10412 | 💤 | Pas utile au diagnostic, et stressant en séance. On le garde pour le brevet blanc (réactivable). |
| D11 | Mode Flow ×2 (G13) | `_checkFlowOnAnswer`, `_flowXPMultiplier`, `_showFlowActivated` L10356-10401, `flow-box` | ❌ | Gamification coupée, et dépend des XP. |
| D12 | Coach marks / tuto régressif (G6) | `_needsCoach`, `_markCoach`, `_MSGS.coach_*`, branche coach de `validateAnswer` (M4) | ❌ ⚠️ | Décision Nicolas. ⚠️ M4 : garder la branche « toast ko » quand on retire la branche coach. |

#### E. Boost, chapitres, progression

| # | Feature / écran | Fonctions · ~lignes | Verdict | Justification |
|---|---|---|---|---|
| E1 | Boost du jour : chargement, génération depuis le diag | `handleBoost` L5275, `loadBoost` L5047, `boostFromDiag` L5300, `startTs` L5317, loader `S.boostPreping` | ✏️ | Devient `startSession()` : le moteur renvoie les 5 items du jour **instantanément**, sans passer par un LLM. `boostFromDiag` ❌. |
| E2 | `boostConsumed` date-stamped en localStorage (M3), `done_v23` | `DK` L2055, restauration L4633-4646, `chkComp` | ✏️ | L'état « séance du jour faite » passe **côté serveur** (multi-appareil). Le store local `done_v23` part. |
| E3 | Rattrapage boost non terminé (P9) | côté serveur (login) | ✏️ | Même esprit : une séance commencée se reprend là où on s'est arrêté. Géré par le moteur. |
| E4 | Hero CTA cascade P1→P6 + fallback DONE (M2) | `render` L8342-8580 | ❌ | Remplacé par la carte « Ta séance du jour » et sa machine à 4 états (§2, E7). Invariant M2 remplacé par H1 (§2.0). |
| E5 | Liste des chapitres : tri, carousel prioritaires, sections par bloc, cartes actives, verrouillées, terminées, ghost stack | `render` L8262-8858, `_catToBloc` L5738, `_carouselNav` L8981 | ❌ | L'unité devient la compétence. En payant, on s'entraîne en touchant une compétence de la carte. |
| E6 | Bandeaux « PENDING_MANUAL », « prof prépare la suite », chapitres de révision ajoutés par le prof | `render` L8319-8333, `initApp` L4648-4666 | ❌ | Ils supposent une action de Nicolas. Interdit par la vision. |
| E7 | Bandeau prérequis par chapitre | `prereqBanner`, `dismissPrereq` L5750 | ❌ | Remplacé par les causes racines 🔗 de la carte. |
| E8 | Navigation dans une série | `togCat` L5666, `goEx` L5758, `nextEx` L5792 | ✏️ | Garder la navigation (← / suivant / swipe) à l'intérieur d'une séance. Le concept `cat` devient `session`. |
| E9 | Complétion `chkComp` (boost / brevet / révision / chapitre, XP bonus, `enqueue remediation`, `assignedByProf`, persistance locale) | L5835-5938 | ✏️ ⚠️ | Réduit à « fin de séance → écran bilan séance ». ⚠️ Contient `enqueue` (remédiation par LLM), `_showSessionFeedback` et le nettoyage `assignedByProf` : les retirer ensemble. |
| E10 | 6 paliers de maîtrise (G2) | `_chapTier` L5943 | ❌ | Remplacés par les 4 statuts du contrat §4. |
| E11 | Anneau de maîtrise | `rMastery` L5966, `#mastery-w` | ❌ | Remplacé par la mini-carte des 5 domaines. |
| E12 | Vue Progression (onglet déjà masqué) | `loadProgress` L6984, `renderProgress` L7047-7268, `openFromProgress` L7032, `relDate`, `getChapProgress` | ❌ | La carte **est** la progression. |
| E13 | Nav 3 onglets Chapitres / Progression / Brevet | HTML L1893-1910, `updNav` L6034, `setView` L6061 | ✏️ | Plus de nav à onglets : l'accueil suffit. Un lien « Ma carte » ouvre la carte. `setView` sert encore à admin/carte/hub. |
| E14 | Sessions rétro : pills par date, modale « série précédente », exo en lecture seule (G9) | `renderArchiveSection` L7275-7475, `_renderRetroExo` L7477, `_openPrevRetroModal` L7626, `_openRetroModal` L7802, helpers | 💤 | Pas prioritaire. Plus tard, `_renderRetroExo` pourra servir un « Revoir mes erreurs » par compétence. |
| E15 | Comparaison live + flèches de tendance (G10) | bandeau L8709, `_chapTrend`/`_trendArrow` L9015-9039 | ❌ | Remplacé par « Ce qui a bougé ». |
| E16 | Regroupement de l'historique en passages de chapitre | `initApp` L4680-4737 | ❌ | Modèle chapitre, et plus de données legacy à relire. |
| E17 | Écran insight post-boost | `renderBoostInsight` L7882 | ✏️ | Devient l'**écran fin de séance** (maquette 05, état B) : score au 1er essai, streak, « ce qui a bougé », erreur type. |
| E18 | Feedback de session 4 emojis | `_showSessionFeedback` L7975, `_sendSessionFeedback`, `_skipSessionFeedback` | 💤 | Donnée lue par Nicolas seulement. On pourra la réactiver en 1 tap si le moteur l'utilise. |
| E19 | Comptes à rebours « prochain contenu 9 h demain », countdown boost | `_startBoostCountdown` L8115, `_startNextContentTimer` L9041 | ❌ | Le gating J+1 disparaît (Q4). |
| E20 | Modale teasing J+1 « ton prof a préparé… » | `_showTeasingModal` L8962, `initApp` L4742 | ❌ | Humain + J+1. |
| E21 | Simuler le lendemain `?sim=1` | `_simulateNextDay` L8134 | ❌ | Outil de test lié au J+1. |
| E22 | Mot du prof (boost / chapitre) | `renderMotProf` L8155, `S.motProf*`, `S._motProfScreen` | ❌ | Manuel. |
| E23 | Cours adaptatif (sections débloquées à 10/20, impression, jalons) | `openCoursView` L8863, `closeCoursView`, `_printCours` L8953, `_checkCoursMilestone` L8990, CSS print L1727 | 💤 | Généré par LLM et validé par Nicolas, donc contraire à l'autonomie. À remplacer plus tard par une « fiche méthode » par compétence (champ `remediation` du référentiel). |
| E24 | Mode Brevet blanc (sélection chapitres, quiz, résultats, config admin) | `loadBrevet` L6394 … `renderBrevet` L6872 (~590 L), `nav-brev` | 💤 | Promis dans le Programme, mais à rebrancher sur les items `usage` problèmes Brevet (v1.1, Q7). |
| E25 | Révision « autre année » publiée par l'admin | `launchRevision` L6951, `S.revisionCats`, `initApp` L4580-4610 | ❌ | Les prérequis 6e-4e sont désormais **dans** la carte. |
| E26 | Chapitres de remédiation dynamiques `_V<n>` + `enqueue` | `initApp` L4518-4528, `chkComp` | ❌ | Circuit LLM par élève abandonné. |
| E27 | Injection `nextChapter` / `nextBoost` / `pendingBrevet` (colonnes Suivi) | `initApp` L4530-4631 | ❌ | Assignation manuelle (P5), supprimée. |

#### F. Gamification

| # | Feature / écran | Fonctions · ~lignes | Verdict | Justification |
|---|---|---|---|---|
| F1 | Streak 🔥 + freeze 1 j/semaine (G3) + toast de login (M6) | `mark` L5566-5620, `initApp` L4799-4807, `LK` localStorage | ✏️ | On garde (décision Nicolas). **Calcul côté serveur** (dates de séance), parce qu'aujourd'hui il vit dans le localStorage et se perd en changeant d'appareil. L'overlay plein écran « 😢 Série perdue » devient un toast doux. |
| F2 | Mission du jour 🎯 n/5 (G8) | `_dailyTarget`, `_cycleDailyTarget`, `_dailyGoal`, `_dailyInc` L5091-5125, `daily-box` | ✏️ | On garde le compteur. Cible fixe à 5 (`_cycleDailyTarget` ❌). L'overlay +50 XP (`_showDailyReward` L5249) devient l'écran fin de séance. |
| F3 | XP 💎 (+100/+50/+10, +200 boost, +300 chapitre, ×2 flow) (G1) | `showXP` L2350, `S.xp`, `#ui-xp`, `chkComp` | ❌ ⚠️ | Décision Nicolas. ⚠️ `sendScore(…, xp, …)` envoie `xp` au serveur : envoyer `0`, ou retirer le champ si le 20-moteur l'accepte. |
| F4 | Slots de 5 + overlay +75 XP (G7) | `_slotCount`, `_checkSlotReward`, `_showSlotReward` L5131-5248, `_MSGS.slot_*` | ❌ ⚠️ | ⚠️ `mark()` n'auto-avance **que si `!_slotNum`**, et le slot « absorbe » la mission du jour : voir §1.2. |
| F5 | 6 milestones (G4) | `_checkMilestone` L5060, `mx_ms_*` | ❌ | Décision Nicolas. |
| F6 | Confettis | `launchConfetti` L2365, `_boostInsightConfetti` L7952 | ✏️ | Une seule occasion : la révélation de la carte complète. |
| F7 | Header « En ligne » (point vert qui pulse) | HTML L1862-1865 | ❌ | Faux signal. |
| F8 | Messages `_MSGS` + `_msg` (ton adapté au niveau) | L2249-2330 | ✏️ | Retirer `slot_*`, `daily_bonus`, `cours_*`, `chap_done*` (« ton prof »), `pending_chapter`, `revision_done`, `ctx_*`, `diag_*`. Ajouter les clés du §2.1. Garder `ok_3eme` / `ko_3eme` (3e seulement). |

#### G. Outils internes

| # | Feature / écran | Fonctions · ~lignes | Verdict | Justification |
|---|---|---|---|---|
| G1a | Admin : workflows de publication (boost / chapitre / brevet / révision), prompt Claude, JSON, emails à copier-coller, journal, cours admin, aperçu J+1 | L10439-13354 (~2 900 L) : `copyAdminPrompt`, `_ckPublish*`, `publishBoost`, `publishChapter`, `publishBrevet`, `publishRevision`, `copySequenceEmail`, `_ckPreviewJ1`, `saveCours`… | ❌ | Tout ça est le travail manuel quotidien que la vision supprime. Les emails partent déjà via Resend (cron). |
| G1b | Admin : vue d'ensemble (liste élèves, KPI inscriptions, fiche élève) | `renderAdminDashboard` L10975, `_renderAdminCards` L11067, `openStudentModal` L12431 | ✏️ | Réduite à du **monitoring en lecture seule** : inscrits, achats, diag en cours ou fini, carte de l'élève, erreurs. A1 (triple-clic) et A6 (read-only) conservés. |
| G2 | Vue Audit (auditeur `WXHBJH` en dur) | `renderAuditView` … `_auditSendReport` L6079-6389 | 💤 | Outil QA d'items utile au relecteur, mais le compte est supprimé. À rebrancher sur un flag `is_auditor` et la nouvelle banque si besoin. |

#### H. Pages hors `app.html`

| # | Page | Verdict | Justification |
|---|---|---|---|
| H1 | `premium.html` (« accès jusqu'au Brevet », une seule offre) | ✏️ | Doit reprendre la maquette 03 (2 offres) ou rediriger vers `app.html#offres`. Texte actuel périmé (conflit avec T2). |
| H2 | `index.html` + `_next/` (landing Next.js) | ❌ | Remplacée par la landing vanilla (agent Landing, `landing/`, contrat §6-7). |
| H3 | **Nouveau** `bilan.html` (page parent publique) | nouveau | Page légère, sans auth, lue via token (maquette 06). Surtout pas `app.html` : 13 000 lignes à charger pour un parent sur WhatsApp. |

**Totaux** : 89 lignes d'inventaire sur l'existant (A-G).

| Verdict | Nb | Lignes |
|---|---|---|
| ✅ garder | 16 | A2-A8, A12, A13, B13, D1, D2, D5, D6, D8, D9 |
| ✏️ adapter | 30 | A1, A10, A11, B1, B2, B4-B7, B10-B12, C1-C4, C6, D4, E1-E3, E8, E9, E13, E17, F1, F2, F6, F8, G1b |
| ❌ supprimer | 37 | A9, A14-A17, B3, B8, B9, B14-B16, C5, D3, D7, D11, D12, E4-E7, E10-E12, E15, E16, E19-E22, E25-E27, F3-F5, F7, G1a |
| 💤 masquer | 6 | D10, E14, E18, E23, E24, G2 |

Hors ce tableau : H1 ✏️, H2 ❌ (hors périmètre, agent Landing), H3 nouveau. En volume, on retire ou masque environ **5 500 à 6 500 lignes** d'`app.html` (admin ~2 900, brevet ~590, audit ~310, rétro ~560, progression ~280, gamification ~600, flow legacy ~500, garde premium ~180).

### 1.2 Dépendances dangereuses (à traiter avant de couper)

1. **Hash routing dans l'IIFE teasing (A9/A10)**. Si `#teasing-screen` disparaît, l'IIFE fait `return` et on perd `#diag` / `#login`. **Il faut d'abord extraire le routing dans une fonction `_route()` appelée au `DOMContentLoaded`.**
2. **`mark()` (D4/F3/F4)** :
   - L'auto-avance (`nextEx` après 600 ms si EASY, 2,5 s si SKIP) n'existe que dans la branche `if (!_slotNum)`. Si on retire les slots, `_checkSlotReward` doit renvoyer `0` (stub), **sinon plus rien n'avance**.
   - La mission du jour est « absorbée » par l'overlay slot ou par `chkComp` : son affichage doit passer par la fin de séance.
   - `sendScore` transporte `xp` : garder la signature (valeur `0`) tant que le backend n'a pas changé.
   - La branche `S.forceFail` (panneau DEV) part avec A14.
3. **`_sealTrial` (C5)** fait un `Object.seal`/freeze de `S.trial`, donc tout nouveau champ d'accès s'ignore **en silence**. Et `_updateIntegrityHash()` est appelé depuis `_flowGuestRegister`. Retirer les 9 modules **en un seul patch**, avec l'appel.
4. **Coach tip et toast ko (M4)**. Dans `validateAnswer`, les deux sont en `if/else`. En retirant le coach, garder la branche toast ko sans condition.
5. **`render()`** appelle `clearNudge` (D7), `rMastery` (E11), `updNav` (E13), les vues `progress` / `brevet` / `diagInsight` / `boostInsight` / `motProf`. On réécrit le **dispatcher** de `render()` d'abord (accueil / séance / carte / hub / fin), puis on retire les renderers morts. Le « Ghost divs z-index » du CLAUDE.md devient caduc avec E5.
6. **`initApp()`** alimente `LVL[S.niv].cats` depuis `curriculumOfficiel`, et tout le rendu d'exercice (`res2`, `rSection`, clés `S.res` = `niveau-cat-idx`) en dépend. **Garder le format `LVL[niv].cats[<sessionKey>]`** pour la séance (clé `SESSION_<date>` ou `DIAG_<module>`). C'est le moyen le plus sûr de réutiliser `rSection` / `mark` / `nextEx` sans toucher au rendu.
7. **Streak (F1)**. Le calcul actuel est local : si on le passe côté serveur, il faut supprimer l'écriture `LK` dans `mark()`. Sinon deux sources de vérité.
8. **Admin (G1a/G1b)**. `openStudentModal` / `_buildModalHTML` mélange lecture et actions de publication : il faut le découper, ne pas le supprimer d'un bloc.
9. **`chkComp` (E9)** appelle `_showSessionFeedback` (💤 E18) : on retire l'appel, pas la fonction.

---

## 2. Nouveau parcours, écran par écran

### 2.0 Invariants UX (remplacent M2, M7, M8, G11, G16 côté front)

| # | Invariant |
|---|---|
| H1 | **Un seul CTA primaire par écran** (bouton plein bleu). Tout le reste est secondaire (bordure) ou lien. |
| H2 | **Jamais « ton prof »** ni aucune promesse d'action humaine dans l'app. Grep de contrôle : `prof prépare\|ton prof\|Nicolas prépare` = 0. |
| H3 | **On ne conclut jamais sur une seule réponse** : ⚪ « Pas vu » si `n_obs < 2` (contrat §4). La carte partielle l'affiche honnêtement. |
| H4 | « demain » autorisé uniquement dans l'écran fin de séance et dans l'accueil séance faite (hérite de M7). |
| H5 | Prix et liens de paiement lus depuis **une seule constante `OFFRE`** (`{diag:{prix:19,url}, prog:{prix:49,url}, upgrade:{prix:30,url}}`). Aucun montant en dur ailleurs. Accès non expirant (T2) : aucune date. |
| H6 | Rien n'attend un humain. Chaque écran a un état « prêt » calculable immédiatement par le serveur. Le gating J+1 (G16) est supprimé côté front (Q4). |
| H7 | Pas de pénalité visible : pas de score en %, pas de note. On montre des **statuts** et des **mouvements**. Le %, c'est réservé au parent (PDF). |
| H8 | Mobile-first 375 px, gouttière 16 px, cibles tactiles ≥ 48 px, pas de scroll horizontal. |

### 2.1 Carte des écrans

```
Landing (vanilla) ──CTA──▶ E1 Intro diag ─▶ E2 Diag express (15 q) ─▶ E3 Calcul ─▶ E4 Carte partielle (invité)
                                                                                      │            │
                                                                        « M'entraîner »│            │« Envoyer à mes parents »
                                                                                      ▼            ▼
                                                                          E5 Créer mon espace (envoie le bilan au parent)
                                                                                      │            └─▶ E6 Partage (lien + aperçu) ─▶ P1 Page parent ─▶ paiement
                                                                                      ▼
                                              ┌──────────── E7 Accueil quotidien (gratuit : point faible) ◀────────────┐
                                              │                 │ séance 5 exos ─▶ E7b Fin de séance ──────────────────┘
                                              │ flouté / « aller plus loin »
                                              ▼
                                         E8 Paywall ──paie (ado ou parent)──▶ E9 Hub diag complet (3 modules, reprise)
                                                                                      ▼
                                                                    E10 Carte complète + PDF ─▶ E11 Upsell Programme (30 €)
                                                                                      ▼
                                                 E12 Quotidien Programme (séance du jour + libre par compétence)
                                                                                      ▼  tous les 30 j
                                                                    E13 Check-up mensuel ─▶ carte avant/après ─▶ PDF parent
```

### 2.2 Écrans ado

Nouvelles clés de messages (ton « Game Boy Chill », tutoiement, phrases courtes, sans culpabiliser), indiquées dans chaque écran.

#### E1 — Intro du diagnostic express
- **Objectif** : lancer le diag en moins de 5 s.
- **Contenu** : « 15 questions, ~8 min. Pas de note. Si tu sais pas, dis-le. » · petite ligne « Tu es en 3e ? » (niveau pré-rempli ; 3e seulement sur cette branche) · lien discret « Déjà un compte ? Se connecter ».
- **CTA** : « Lancer mon diagnostic → ».
- **États** : *reprise possible* (session express < 24 h) → « Tu t'étais arrêté à la question 9. On reprend ? » [Reprendre] / « Recommencer » en lien · *erreur réseau* → « Pas de réseau 📡, réessaie » + bouton.
- **Parent qui arrive seul** : lien « C'est pour mon enfant » → « Passez-lui le téléphone : c'est à lui de répondre, 8 minutes, sans aide. Vous recevrez le bilan par mail. »

#### E2 — Diagnostic en cours (maquette `01-diag-en-cours`)
- **Objectif** : répondre, vite et honnêtement.
- **Contenu** : barre segmentée n/15 + « ≈ x min restantes » · étiquette du domaine + niveau d'origine (« Niveau 5e », qui rassure quand la question paraît facile) · question · 4 options / fill · « 🤷 Je ne sais pas » (pointillé, jamais caché) · encart « 🎯 Cette question dépend de tes réponses d'avant ».
- **Pas d'indices, pas de formule, pas de chrono, pas de correction** (Q1). Après validation : micro-transition de 250 ms, on passe à la suivante.
- **CTA** : « Valider → » (désactivé tant que rien n'est sélectionné).
- **États** : *chargement de la question* → skeleton 300 ms max (le serveur précharge n+1) · *hors ligne* → la réponse part en queue (`flushQ`) et on affiche « On garde ta réponse, on envoie dès que le réseau revient » · *quitter (✕)* → sheet « Tu gardes ta progression 24 h. » [Continuer] [Quitter].
- **Messages** : `diag_jsp_ok` « Noté. Mieux vaut ça qu'un coup au pif 👍 » (1 fois max) · `diag_mid` (à la question 8) « Mi-parcours. T'es régulier, c'est parfait. »

#### E3 — Calcul de la carte (2 s max)
- « On relie tes réponses… » puis « On cherche d'où viennent les erreurs… ». Pas de faux loader long : l'animation dure au plus la latence réelle + 600 ms.

#### E4 — Carte partielle, invité (maquette `02-carte-partielle`)
- **Objectif** : « ils ont compris mon problème » → vouloir continuer.
- **Contenu** :
  1. En-tête sombre : « Léa, on sait par où commencer. » + résumé en 1 phrase généré depuis la Carte.
  2. **5 domaines** colorés (statut + barre), ⚪ « Pas vu » assumé.
  3. **Point faible n°1 détaillé** : titre élève, niveau d'origine, badge 🔗 cause racine, **sa réponse fausse réelle** + libellé d'erreur, « Ça te bloque aussi sur » (`bloque[]`).
  4. **Liste floutée** (blur 3 px, lisible comme « il y a des choses là ») + cadenas « + 40 compétences à cartographier » → lien vers le paywall.
- **CTA primaire** : « M'entraîner gratuitement → » (ouvre E5). **Secondaire** : « 📩 Envoyer ma carte à mes parents » (ouvre E5 aussi, avec l'intention partage).
- **États** : *aucune erreur* (rare) → le point n°1 devient « Ton point le plus fragile » (plus bas `maitrise`), jamais « aucun point faible » · *tout en ⚪* (trop de JSP) → « On a besoin de quelques réponses de plus » + 5 questions bonus.
- **Messages** : `carte_titre_*` (3 variantes selon le nombre de lacunes), `carte_racine` « Bonne nouvelle : si on règle ça, d'autres trucs se débloquent. »

#### E5 — Créer mon espace (bottom sheet)
- **Objectif** : sauvegarder la carte en 30 s.
- **Champs** : prénom · **email d'un parent** (label : « Email d'un parent (on lui envoie ta carte) ») · mot de passe · case consentement existante (texte validé par 52-legal).
- **CTA** : « Créer mon espace → ». Sous-texte : « Ta carte part aussi par mail à ton parent. Gratuit, sans carte bancaire. »
- **États** : *email déjà pris + bon mdp* → connexion silencieuse (logique existante) · *mauvais mdp* → « Ce mail a déjà un compte. Connecte-toi » · *erreur* → toast `net_error`.
- **Après** : si l'intention était « partage », on ouvre E6 directement. Sinon on va sur E7 avec la séance n°1 prête.

#### E6 — Partager au parent (sheet natif ou fallback)
- **Objectif** : que le parent voie le bilan dans les 5 minutes.
- **Mécanique** : `navigator.share({title, text, url})` si disponible (iOS/Android). Sinon 4 boutons : WhatsApp (`wa.me/?text=`), SMS (`sms:?&body=`), Mail (`mailto:`), Copier le lien.
- **Message pré-rédigé (modifiable)** : « J'ai fait un test de maths sur Matheux. Regarde mon bilan 👀 {url} ».
- **Aperçu** : vignette de ce que le parent verra (image OG des 5 barres + « Le bilan maths de Léa (3e) »), voir le haut de la maquette 06.
- **Lien** : `matheux.fr/b/<token>` (token aléatoire ≥ 10 caractères, 1 par carte, révocable). La page parent P1 se sert de ce token.
- **États** : *partagé* → toast « Envoyé ✓ Tes parents vont voir ta carte » · *annulé* → rien.
- **Entrées vers E6** : E4, E5, paywall (« Demander à mes parents »), carte complète, fin de séance (1 fois, J+2 si le parent n'a pas ouvert : bandeau « Ta carte n'a pas encore été vue par tes parents »).

#### E7 — Accueil quotidien, gratuit (maquette `05-quotidien`, état A)
- **Objectif** : lancer la séance du jour.
- **Contenu** : « Salut Léa » + 🔥 streak + 🎯 n/5 · **carte « Ta séance du jour »** : focus (compétence), « 5 exos · ~8 min · niveau ajusté à hier », « 💡 Pourquoi ça ? » (phrase issue du moteur : cause racine / erreur vue / révision espacée) · mini-carte 5 domaines + « +1 compétence cette semaine » · rangée verrouillée « 40 compétences encore floues » → paywall.
- **CTA** : « C'est parti → » (ou « Continue, encore 3 exos » si la séance est commencée).
- **Machine à 4 états** (remplace la cascade hero) : `A prête` → `B en cours (n/5)` → `C faite` (écran E7b, puis accueil « faite » avec « Prochaine séance demain ») → `D rien à proposer` (point faible passé 🟢 en gratuit : le moteur prend le point faible suivant **connu**. S'il n'y en a plus, message « Ton point faible est réglé 💪. Pour aller plus loin, il faut voir le reste de ta carte » + paywall).
- **Erreur** : *séance indisponible* (réseau) → « On n'arrive pas à charger ta séance » + Réessayer. Pas de fallback local.

#### E7b — Séance + fin de séance (maquette 05, état B)
- **Pendant la séance** : `rSection` existant (indices, formule, brouillon, Passer, JSP). Après une erreur : si `item.err[réponse]` existe, feedback « **Erreur classique** : {libelle} » au-dessus de la correction. C'est le moment « l'appli me connaît ».
- **Fin** : « 4 sur 5 du premier coup. » (EASY / total, P8) · streak · **Ce qui a bougé aujourd'hui** (transitions de statut + erreur type repérée « elle reviendra demain ») · carte « T'as envie de continuer ? » → paywall (gratuit) ou « Encore une séance » (Programme).
- **Messages** : `seance_fin_parfait` « 5/5. Propre. Demain on monte d'un cran 🔥 » · `seance_fin_ok` « {n} sur 5 du premier coup. Ça avance. » · `seance_fin_dur` « Séance difficile, et c'est normal : on est pile sur ton point faible. Demain ça passe mieux. » · `bouge_up` « {comp} : {avant} → {après} » · `err_retour` « Erreur repérée : {libelle}. Elle reviendra, pour la faire disparaître. »

#### E8 — Paywall (maquette `03-paywall`)
- **Objectif** : choisir une offre, ou la faire payer par un parent.
- **Entrées** : zone floutée, rangée verrouillée, « Voir ce qui est inclus », fin de séance, badge « Gratuit ».
- **Contenu** : « Tu as vu 1 point faible sur ~45 » · titre « Débloque ta carte complète » · offre **Diagnostic complet 19 €** (5 bénéfices, bouton secondaire) · offre **Programme Brevet 49 €** (mise en avant, CTA primaire, « Déjà pris le diagnostic ? Les 19 € sont déduits ») · bloc sombre « C'est tes parents qui paient ? » → **« 📩 Demander à mes parents »** (E6, avec le lien vers P1 qui porte les boutons de paiement) · réassurance « Paiement unique · Pas d'abonnement · Accès sans date de fin · Stripe ».
- **États** : *diag déjà acheté* → une seule carte « Programme : 30 € au lieu de 49 € » · *programme acheté* → écran jamais affiché · *retour Stripe sans activation* → écran C4 « Paiement reçu, activation en cours » + poll.

#### E9 — Hub du diagnostic complet (maquette `07-diag-complet-modules`)
- **Objectif** : faire un module, pouvoir s'arrêter.
- **Contenu** : progression globale (questions + minutes restantes) · 3 modules : **1 Nombres et calculs (NC)**, **2 Fonctions, stats et algo (DF + AP)**, **3 Géométrie et mesures (EG + GM)**. Chacun est ~13 min et a un état *à faire* / *en cours n/N + ▶* / *fait ✓ (durée)* · encart pédagogique « si tu te trompes en 3e, on vérifie la base d'avant » · « À la fin : carte complète + PDF, envoyé aussi à tes parents ».
- **CTA** : « Commencer / Reprendre le module X → ». Un module fini n'est pas refaisable (Q : non, c'est le check-up mensuel qui refait).
- **Règles** : ordre libre (on recommande 1 → 2 → 3), reprise à la question près (état serveur), **mêmes règles que E2** (pas d'indices ni de chrono ni de correction). La séance du jour reste accessible pendant ce temps : le diag n'empêche pas de s'entraîner.
- **Messages** : `mod_fini` « Module {n} bouclé en {m} min. Plus que {k}. » · `mod_pause` « Pause ? Tout est gardé. Reviens quand tu veux. »

#### E10 — Carte complète + PDF (maquette `04-carte-complete`)
- **Objectif** : comprendre sa situation, et que le parent reçoive le PDF.
- **Contenu, dans l'ordre de lecture** : titre + phrase de synthèse (« 3 blocages expliquent presque tout le reste ») · 4 compteurs (Acquis / Fragiles / Lacunes / Pas vu) · **🔗 Causes racines** (compétence d'origine → compétences bloquées) · **Priorités 1-2-3** avec l'erreur réelle · **par domaine** (accordéon, une barre de segments = une compétence, tap → liste des compétences avec statut) · **points forts** · **bilan PDF** (Télécharger / Envoyer) · **plan 4 semaines** + upsell.
- **Confettis** : une seule fois, à la première ouverture.
- **États** : *PDF en génération* → bouton spinner « On prépare ton PDF… » (jsPDF côté client, voir 30-pdf) · *erreur PDF* → « Réessaie » + envoi mail serveur en secours · *carte incomplète* (module abandonné) → impossible, E10 n'existe qu'une fois les 3 modules finis.

#### E11 — Upsell Programme
- Bloc en bas de E10 (plan 4 semaines + « Activer mon plan — 30 € ») et **une** relance dans la fin de séance J+3. Jamais en modale bloquante.

#### E12 — Quotidien Programme
- Comme E7, sans rangée verrouillée. Séance du jour tirée **de toute la carte**, en suivant le plan 4 semaines. En plus :
  - « **S'entraîner sur…** » : un tap sur une compétence de la carte lance 5 exos dessus (illimité).
  - Carte « Brevet blanc » (💤 v1.1, Q7).
  - Bandeau « Check-up dans 9 jours ».

#### E13 — Check-up mensuel (re-diagnostic)
- **Déclencheur** : J+30 après la carte complète, bandeau sur l'accueil (jamais bloquant).
- **Format** : ~12 min, **ciblé** sur les compétences non 🟢 + un échantillon des 🟢 (vérifier que ça tient).
- **Sortie** : carte **avant / après** (flèches de statut, « 6 compétences passées au vert ce mois-ci ») + nouveau PDF envoyé au parent automatiquement.
- **Message** : `checkup_invite` « C'est l'heure de ton check-up. 12 min pour voir ce qui a changé. »

### 2.3 Écrans parent

#### P1 — Page parent partagée `bilan.html?t=<token>` (maquette `06-parent-partage`)
- **Objectif** : comprendre en 2 minutes, et payer si le bilan convainc.
- **Ton** : **vouvoiement**, factuel, jamais infantilisant, zéro gamification (pas de streak, pas d'emoji dans les titres).
- **Contenu** : en-tête « Le bilan maths de Léa » (prénom seulement, date, type express/complet) · « Léa a fait un diagnostic de 7 minutes… et a souhaité vous le transmettre » · vue d'ensemble 5 domaines (libellés parent : « À consolider » au lieu de « Fragile ») · **le point à surveiller** (`libelle_parent` + pourquoi ça compte au Brevet) · **« Ce que ce bilan ne dit pas encore »** (honnêteté : 15 questions ne suffisent pas, c'est l'argument de vente) · CTA **« Offrir le diagnostic complet — 19 € »** (Stripe avec `client_reference_id` = code élève, donc aucun compte parent requis) + lien Programme 49 € · confiance (fondateur, programme officiel, données minimales) · FAQ 4 questions.
- **Version complète** (après achat) : même page, domaines + priorités + **bouton PDF** + plan 4 semaines + (si Programme) « Dernière activité : il y a 1 jour · 6 séances ce mois-ci ».
- **États** : *token invalide ou révoqué* → « Ce lien n'est plus actif. Demandez à votre enfant de vous le renvoyer. » · *déjà payé* → CTA remplacé par « ✓ Diagnostic complet débloqué ».
- **Technique** : page statique légère (pas `app.html`), `<meta property="og:*">` générés côté serveur pour l'aperçu WhatsApp (sinon l'aperçu est générique : voir 20-moteur / edge function), `noindex`.

#### P2 — Mail parent (renvoi vers 51-emails)
- J+0 automatique à l'inscription : « Le bilan express de Léa » (même contenu que P1 en résumé + lien P1). C'est le premier contact avec l'acheteur, et il a lieu **sans que l'ado ait à y penser**.
- Après la carte complète : PDF en pièce jointe + lien P1.

---

## 3. Maquettes (375 px)

| Fichier | Écran | Points à regarder |
|---|---|---|
| `maquettes/01-diag-en-cours.html` / `.png` | E2 | Barre segmentée, niveau d'origine, JSP visible, pas d'indices |
| `maquettes/02-carte-partielle.html` / `.png` | E4 | 5 domaines, point faible avec réponse réelle, flouté + cadenas, 2 CTA |
| `maquettes/03-paywall.html` / `.png` | E8 | 2 offres, 19 € déduits, « Demander à mes parents » |
| `maquettes/04-carte-complete.html` / `.png` | E10/E11 | Causes racines, priorités, segments par domaine, PDF, plan 4 semaines + upsell 30 € |
| `maquettes/05-quotidien.html` / `.png` | E7 + E7b | État A (séance prête, pourquoi ça) et état B (séance faite, ce qui a bougé) |
| `maquettes/06-parent-partage.html` / `.png` | E6 + P1 | Aperçu WhatsApp, page parent vouvoyée, honnêteté, FAQ |
| `maquettes/07-diag-complet-modules.html` / `.png` | E9 | 3 modules, reprise, encart « on cherche la cause » |

Charte reprise d'`app.html` : `--p #1E40AF`, `--pd #0F172A`, `--grn`, `--amb`, `--ros`, `--bg #f7f8fc`, rayons 14/22 px, Syne (titres, 700-800) + DM Sans (texte). Tokens de statut ajoutés : `--lac` / `--fra` / `--acq` / `--ne` et leurs fonds clairs, à ajouter dans `:root` d'`app.html` (lot L5). Constat en itérant : Syne 800 est très large sur 375 px. Il faut **limiter Syne 800 aux H1** et passer les titres de carte en Syne 700 ≤ 1 rem, sinon ça wrappe mal (« dénominateur » coupé).

---

## 4. Landing → app (contenu et parcours attendus)

La landing est refaite en vanilla par l'agent Landing (`landing/`, `60-landing.md`). Ce que l'app attend d'elle :

- **Un seul point d'entrée** : tous les CTA pointent vers `app.html#diag?src=<section>` (ouvre E1 directement, le `src` est tracé en GA4). `#login` pour « Se connecter ». Le hash routing sera sorti de l'IIFE teasing (lot L1).
- **Double promesse** : ado (« 8 minutes pour savoir exactement ce qui coince en maths ») et parent (« Un diagnostic qui remonte aux causes, pas une note de plus »).
- **Sections attendues** : hero + CTA diag gratuit · « Comment ça marche » en 3 temps (diagnostic → carte → 10 min/jour) · **visuel de la carte** (reprendre la maquette 02 ou 04) · exemple de cause racine (« il bloque en équations à cause des relatifs de 5e ») · extrait du PDF parent · offres (Gratuit / Diagnostic 19 € / Programme 49 €, lues depuis la même source que `OFFRE`) · fondateur · **FAQ parent** (remplace un prof ? temps par jour ? seul ? lacunes anciennes ? données de mon enfant ? pas d'abonnement ?).
- **À ne plus dire** (présent dans la landing actuelle, et faux ou périmé) : « Brevet 2026 dans 83 jours », « parcours vérifié chaque soir par un accompagnant », « 82 % des élèves se trompent », « +35 points en 3 semaines », « 22 chapitres / 440 exercices », « Streaks, badges, XP », « 29,99 € jusqu'au Brevet 2026 ».

---

## 5. Plan d'implémentation dans `app.html` (lots ordonnés, patches chirurgicaux)

Principe : **on retire avant d'ajouter**, en gardant l'app fonctionnelle à chaque lot (smoke test manuel à 375 px : diag → inscription → séance 5 exos → fin). Après chaque lot : `grep` de contrôle + capture headless des écrans touchés.

| Lot | Contenu | Dépend de | Risques / garde-fous |
|---|---|---|---|
| **L1 — Code mort** | Extraire `_route()` du hash routing, **puis** supprimer la page teasing (A9). Supprimer flow-s1/blocs (B3), `finalizeOnboarding` / `startCal` / `calState` / `renderDiagInsight` (B14), panneau DEV (A14), mode lite (A16), `?sim=1` (E21), constantes legacy (A15), stubs (A17). | rien | Faible. Garde-fou : `#diag` et `#login` testés avant/après. ~−900 L. |
| **L2 — Gamification** | Stubs d'abord (`_checkSlotReward → 0`, `_flowXPMultiplier → 1`, `showXP → noop`), test, puis suppression : XP (F3), slots (F4), milestones (F5), flow (D11), paliers (E10), anneau (E11), onboarding (B15), tour (B16), coach (D12), nudge (D7), « En ligne » (F7), confettis réduits (F6). Réécrire `mark()` (D4) : score → streak → 🎯 → avance → fin. | L1 | **Moyen** : auto-avance (§1.2-2), M4 (§1.2-4), `sendScore` avec xp=0. Test : 5 exos EASY/HARD/SKIP/Passer, le compteur 🎯 et le streak bougent. |
| **L3 — Couper l'humain** | `initApp` : retirer les injections E27, E26, E25, motProf (E22), `pendingManual` et bandeaux (E6), teasing J+1 (E20), comptes à rebours (E19), `assignedByProf`, `done_v23` (E2), regroupement historique (E16). `chkComp` réduit (E9). Admin : supprimer G1a, découper la modale (§1.2-8), garder G1b en lecture seule. `_MSGS` nettoyé (F8). | L2 | Moyen : `initApp` est long et central. Garder `LVL[niv].cats` (§1.2-6). Grep H2 = 0. ~−3 500 L. |
| **L4 — Accès et paiement** | Retirer la garde premium en **un seul patch** (C5 + appel dans l'inscription). Introduire `S.acces` + `_can()` (C6), constante `OFFRE` (H5), écran paywall E8 (C2), badge (C1), retour Stripe par produit (C4), `premium.html` (H1). | backend : produits Stripe + webhook qui pose `acces` (20-moteur / 50-offre) | **Élevé côté business** : l'accès ne doit pas s'ouvrir sans paiement. Le serveur reste le gate (items servis ou refusés), le front ne fait qu'afficher. Test : les 3 profils (gratuit / diag / prog) × les 3 paiements. |
| **L5 — Diag express adaptatif + carte partielle** | Tokens de statut CSS. Brancher B4/B5 sur l'API moteur (`diag_start` / `diag_next` / `diag_answer` / `carte`, noms à caler sur 20-moteur). Masquer les aides en mode diag. Reprise (B6). Écran E3. Renderer `renderCarte(carte, mode)` partagé partiel/complet/parent (E4). Inscription fusionnée (B10/B11) + envoi auto du bilan (P2). Login seul (B12). | 10-référentiel (items `usage:diag`), 20-moteur (API + objet Carte), 51-emails (J+0 parent) | Élevé : c'est le nouveau cœur. Mesurer la durée réelle du diag (cible ≤ 8 min à la médiane) et la latence de `diag_next` (< 300 ms, sinon précharge). |
| **L6 — Accueil quotidien + séance** | Dispatcher `render()` (§1.2-5) : accueil E7 (machine 4 états), séance (réutilise `rSection` / `mark` / `nextEx` avec la clé `SESSION_<date>`), fin E7b (`renderBoostInsight` adapté). « Pourquoi cet exo » (D1), erreur type nommée (D2), « ce qui a bougé » (renvoyé par le serveur en fin de séance). Streak côté serveur (F1). Mini-carte. | L5, 20-moteur (`session_du_jour`, `fin_session` → deltas) | Moyen : suppression de E4/E5 (hero, liste de chapitres) dans le même lot que le nouveau rendu, pour ne jamais avoir un accueil vide. |
| **L7 — Partage parent** | E6 (Web Share + fallbacks), token de partage, nouvelle page `bilan.html` (P1) + OG image serveur, bandeau « pas encore vue par tes parents ». | 20-moteur (table des tokens de partage + endpoint public en lecture seule), 52-legal (données visibles) | Moyen (RGPD mineur) : prénom seulement, token non devinable, révocable, `noindex`, pas de données de réponse brutes au-delà de l'exemple d'erreur. |
| **L8 — Diag complet + carte complète + PDF** | Hub E9 (3 modules, reprise), écran E10, bouton PDF (`js/bilan-pdf.js` du Dev PDF), envoi du PDF, upsell E11. | L4, L5, 30-pdf | Moyen : reprise d'une session longue sur plusieurs jours et appareils (état serveur uniquement). |
| **L9 — Programme** | E12 « S'entraîner sur… » par compétence, check-up mensuel E13 (avant/après), réactivation Brevet blanc (E24 💤 → v1.1). | L6, L8, 20-moteur | Faible à moyen. |
| **L10 — Docs & règles** | Mettre à jour CLAUDE.md (règles impactées ci-dessous), `docs/messages.md`, playbooks, `product.md`. | tout | Voir la liste. |

**Règles CLAUDE.md impactées** (à réécrire par le chef de projet une fois validé) : P1 (5 q → ~15 adaptatives), P2 (boost → séance du jour), P3 (chapitres 20 exos → items atomiques), P4, P5 (supprimée), P9 (reprise séance), P10 (caduque), P12 (💤), T1-T4 (freemium chapitre → point faible + 2 offres), G1, G2, G4-G7, G9-G11, G13, G15 (supprimées ou 💤), G3/G8 (gardées), G12/G14 (💤), **G16 (J+1 abandonné, Q4)**, M2 / M7 / M8 (remplacées par H1 / H4, M8 caduque), A2-A5 et A7 (admin réduit), note « ghost divs z-index » (caduque).

---

## ❓ Questions pour Nicolas

| # | Question | Reco par défaut |
|---|---|---|
| Q1 | Montre-t-on la correction pendant le diagnostic ? | **Non.** Juste « réponse notée ». Les corrections apparaissent dans la carte (erreur réelle + explication). Plus court, moins décourageant, mesure plus propre. |
| Q2 | Carte partielle visible **avant** la création de compte ? | **Oui.** La valeur d'abord. Le compte est demandé pour s'entraîner ou partager. |
| Q3 | Email d'un parent obligatoire à l'inscription + envoi auto du bilan express au parent ? | **Oui.** C'est le levier de conversion n°1 et ça sert d'information parentale (à valider par 52-legal). |
| Q4 | On abandonne la règle J+1 (G16) : séance dispo immédiatement, recalculée chaque jour ? | **Oui.** Le J+1 servait à laisser le temps d'une validation humaine, qui n'existe plus. |
| Q5 | Gratuit : 5 exos/jour sans limite de durée, sur le point faible n°1 puis le suivant connu ? | **Oui, sans limite de durée.** Le gratuit prouve que ça marche, et il fait bouger la carte. |
| Q6 | Timer, sessions rétro, cours adaptatif, feedback emojis : masqués (💤) en v1 ? | **Oui.** On réactive si un usage réel le demande. |
| Q7 | Brevet blanc dans le Programme dès le lancement ? | **v1.1** (4-6 semaines après), une fois les problèmes Brevet taggés par compétence. Mention « bientôt » sur l'offre d'ici là. |
| Q8 | Le streak : garder le freeze 1 j/semaine et le passer côté serveur ? | **Oui aux deux.** |
| Q9 | Admin réduit à du monitoring lecture seule (plus aucune publication) ? | **Oui.** |
| Q10 | Page parent : afficher les deux prix (19 € et 49 €) ? | **Oui.** CTA principal 19 €, Programme en lien. |
| Q11 | Phrase de confiance « Nicolas Follezou, qui accompagne des collégiens en maths depuis des années » : exacte ? Formulation préférée ? | À confirmer. Sinon « conçu par un prof de maths » est à proscrire si c'est inexact. |
| Q12 | Automatismes (AT1-AT4, chrono 30 s) : dans le Programme ou 💤 ? | **💤 v1.** À réintégrer comme type de séance du Programme. |
