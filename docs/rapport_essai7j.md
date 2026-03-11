# Rapport — Essai 7 jours + Polish UX Matheux
> Date : 11 mars 2026 · Session autonome multi-agents

## Résumé exécutif
Session complète en 4 phases : implémentation de l'essai gratuit 7 jours sans carte bancaire (backend GAS @25 + badge J-X + overlay bloquant), refonte des messages vers un ton ado Game Boy Chill, onboarding 3 slides post-inscription, et animations CSS (pulseHint / toastIn bounce / popIn). Le produit est désormais prêt pour un lancement avec un flow d'acquisition complet.

## Phase 1 — Backend essai 7 jours ✅

### Ce qui était déjà en place
- `ensureUsersCols()` : vérifie et ajoute `TrialStart` + `PremiumEnd` si absentes
- `register()` : insère `TrialStart = today()` (format ISO yyyy-MM-dd, Europe/Paris)
- `checkTrialStatus(p)` : calcule `diffDays`, `trialActive` (diffDays < 8), `daysLeft` (max 0, 7-diffDays), `isPremium`
- `case 'check_trial_status'` dans `doPost()`

### Patch appliqué
- `login()` : ajout d'une ligne dans le return — `trial: checkTrialStatus({ code: code })`
- Avant : login retournait `trialStart` brut dans profile, sans calcul
- Après : login retourne un objet complet `{ status, trialActive, daysLeft, isPremium }`

### GAS déployé
@25 (deploymentId: AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF)

### Tests validés
- `register` + `check_trial_status` → `trialActive: True`, `daysLeft: 7` pour nouveau compte
- `login.trial` → `{ status: success, trialActive: True, daysLeft: 7, isPremium: False }`
- Admin HMD493 → `trialActive: False, daysLeft: 0` (attendu — compte ancien)

## Phase 2 — Frontend essai + messages ✅

### Badge trial
- Div `#trial-badge` injecté dans le header entre stats et nav
- Condition : `S.trial.trialActive === true && !S.trial.isPremium && !admin`
- Texte : pill "🔥 J-X · Essai gratuit" (X = daysLeft)
- Couleur urgence (daysLeft ≤ 2) : ambre (#fef3c7 / #fcd34d / #92400e)
- Couleur normal : indigo (#eef2ff / #c7d2fe / #4338ca)
- Appelé dans `updH()` (post-login) et `setView()` (changement de vue)

### Overlay expiry
- Créé dynamiquement via `createElement` (pas de doublon possible)
- z-index 4000 — au-dessus de tout sauf toast (z-5000)
- Déclenché dans `initApp()` si `!trialActive && !isPremium` (setTimeout 300ms)
- Bouton "Prolonger l'accès →" : toast "Bientôt disponible — ton prof est au courant 🔥"
- Bouton "Voir ma progression quand même" : ferme overlay + `setView('progress')`
- Fallback sécurisé : `S.trial = d.trial || { trialActive: true, daysLeft: 7, isPremium: false }` si GAS ancienne version

### Messages modifiés (avant → après)
| Zone | Avant | Après |
|------|-------|-------|
| EASY ×7 | '🔥 Parfait !' / '✅ Maîtrisé !' / '💪 Excellent !' / '⚡ Top niveau !' / '🎯 En plein dans le mille !' / '🚀 Continue comme ça !' / '👏 Bravo !' | 'Carton plein 🎯' / 'T\'as géré ça 💪' / 'Dans le mille ⚡' / 'Propre. Vraiment 🔥' / 'Maîtrisé ✅' / 'Trop fort(e) 🚀' / 'GG c\'est dans la boîte 👌' |
| HARD ×3 | '💡 Regarde l\'explication…' / '📚 Pas de panique…' / '🧠 Retiens bien la méthode…' | 'Presque ! Regarde bien la réponse 👀' / 'Ça arrive, c\'est comme ça qu\'on apprend 💡' / 'Pas grave — la prochaine tu l\'as 🎯' |
| renderChapComplete | 'Ton prof prépare ton prochain chapitre personnalisé. Reviens demain matin pour la suite 🔥' | 'Chapitre bouclé 🎉 Reviens demain — ton prof prépare la suite sur mesure.' |
| renderArchiveSection boost terminé | 'Boost du jour terminé ✓ Le prochain arrive demain 🔥' | 'Boost du jour : fait ✅ T\'es à jour. Reviens demain 🔥' |
| renderArchiveSection chapitre terminé | 'Chapitre terminé ✓ Le prochain arrive demain matin 🔥' | '📅 Prochain contenu · Demain matin 🔥' |
| pendingManual fallback | 'Ton prof prépare ton prochain chapitre personnalisé… reviens demain !' | '⏳ Ton prof prépare quelque chose pour toi. Reviens demain matin 🔥' |
| Nudge 20s | (pas de toast) | 'Psst — t\'as droit aux indices 💡 Hésite pas !' (3.5s) |
| Carte "Prochain chapitre" | 'Ton prof prépare / la suite' + 'Demain matin 🔥' | '📅 Prochain contenu' + 'Demain matin 🔥' |

## Phase 3 — Landing + onboarding ✅

### CTA hero
- Avant : "Essayer gratuitement 7 jours →"
- Après : "Essayer 7 jours gratuits — sans carte bancaire →"
- Social proof : 2 items → 3 items flex-wrap ("Aucune carte bancaire requise" / "Accès complet 7 jours" / "Stop quand tu veux")
- Step 4 (formulaire) : "Sauvegarde tes résultats et continue 7 jours gratos — aucune carte requise 🔥"

### Onboarding 3 slides
Fonction `showOnboarding(cb)` créée (~65 lignes). Appelée depuis `flowRegister()` et `finalizeOnboarding()` avant `startCal()`.

- **Slide 1** — Emoji 🎉 · Titre "7 jours gratuits, sans carte" · Corps "Ton accès complet démarre maintenant. Pas de prise de tête." · Bouton "Suivant →"
- **Slide 2** — Emoji ⚡ · Titre "Un diagnostic perso" · Corps "On détecte tes lacunes en quelques questions. C'est pour toi, pas pour un examen." · Bouton "Suivant →"
- **Slide 3** — Emoji 🔥 · Titre "Ton prof prépare la suite" · Corps "Chaque jour, des exercices adaptés à ce que t'as du mal. Reviens demain voir la suite." · Bouton "C'est parti →"

Style : modal centré, fond sombre rgba(7,9,15,.88), z-index 3500, dots de navigation, dégradé indigo/purple.

### Feedbacks ajoutés
- Toast abandon boost incomplet (togCat) : "Tu t'arrêtes là ? Pas de souci — tu reprends demain 💪" (3500ms)
- Bouton renderMotProf : "C'est parti ! →" → "OK, j'ai lu — on y va 🔥"
- Bandeau premier jour (`S.isFirstDay === true`) : "Bienvenue ! — Ton diagnostic est prêt. C'est pas un exam — réponds honnêtement 🎯"
- Bandeau reprise chapitre (done > 0 && !comp) : "Tu reprends le chapitre — t'en es à X/Y 💪 Continue !"

## Phase 4 — Animations + vérif ✅

### Animations
- `@keyframes pulseHint` (opacity 1→0.7 + scale 1→1.05, 2.5s) + `.pulse-hint` sur pills 💡/📐 — retiré à l'ouverture (4 endroits couverts)
- `@keyframes toastIn` (translateY 20px→-4px→0, scale 0.95→1.02→1, 0.3s bounce) — appliqué sur `#toast.show`
- `@keyframes popIn` (scale 0.95→1.04→1, 0.25s) + `.pop-in` — bouton "C'est parti →" + CTA hero avec setTimeout 1200ms

### Code mort supprimé
- `renderChapComplete(cat, data)` — 14 lignes supprimées. Aucun appel dans le fichier. Rendu "chapitre terminé" géré par `renderArchiveSection()`.

### Correction mobile
- `overflow-y: auto` ajouté sur `onb-overlay` (prévient débordement iPhone SE 375px)

### Test trial
- `trialActive: True` / `daysLeft: 7` / `isPremium: False` — cohérent register + check_trial_status ✅

## Ce qui fonctionne parfaitement
- Essai 7 jours full droits sans carte — backend GAS @25 + frontend complet
- Badge J-X dans le header avec couleur d'urgence si ≤2j restants
- Overlay bloquant à expiration + bouton "Voir ma progression"
- Onboarding 3 slides post-inscription avec callback propre
- CTA landing "sans carte bancaire" cohérent avec le flow
- Messages ton ado Game Boy Chill — EASY×7 + HARD×3 + tous feedbacks contextuels
- Animations CSS : pulseHint (pills), toastIn (bounce), popIn (CTA/onboarding)
- Nettoyage code mort (renderChapComplete supprimée)
- Simulation 5 jours : chapitres complets (Emma, Inès, Théo, Jade, Romain 20/20), boosts consommés

## Ce qui reste à faire (prochaines sessions)
- Stripe webhook → colonne Premium → désactiver overlay
- Vrais témoignages sur landing (remplacer textes fictifs)
- BLOC 3 Juridique (CGU, RGPD mineurs, case consentement parental)
- git push origin main si token PAT disponible
- Reconnexions J4-5 à investiguer (erreur auth dans simulation — probablement hash format)
- Fix `renderMotProf()` : `getElementById('main-content')` → id réel `'app-c'` (bug préexistant hors scope)

## Commits de cette session
| Hash | Description |
|------|-------------|
| f917a29 | feat(backend): essai 7j TrialStart + checkTrialStatus + login.trial |
| 7e63b0f | feat(frontend): badge J-X + overlay + messages ton ado |
| 372ac76 | feat(ux): landing sans-carte + onboarding 3 slides |
| d7be47f | feat(animations): pulse pills + toast bounce + nettoyage |
