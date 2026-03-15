# Messages — Matheux · Voice & Tone Guide

> Document vivant. Toute modification d'un message dans le code doit être reflétée ici.
> Référence : `_MSGS` dans `index.html` + templates email dans `backend.js`.
> Mise à jour : 2026-03-15 — GAS @77

---

## Principes fondateurs

### Ton élève
- **Tutoiement** toujours — jamais de vouvoiement avec l'élève
- **Direct et court** — max 1 phrase pour les toasts
- **Jamais culpabilisant** — "pas grave" > "tu as raté"
- **Jamais bloquant** — toujours une porte de sortie
- Emoji : **encourageant**, pas décoratif

### Ton parent (emails)
- **Vouvoiement** toujours
- **Ton prof humain** — Nicolas parle à la première personne
- **Factuel avant émotionnel** — chiffres d'abord, encouragements ensuite
- Signature : "Nicolas · Prof de maths · Matheux"

### Adaptation au niveau
| Niveau | Ton | Longueur | Emojis | Spécificité |
|---|---|---|---|---|
| 6EME | Enthousiaste, chaleureux | Court, simple | Nombreux | Aucune ref brevet |
| 5EME-4EME | Encourageant, direct | Moyen | Modérés | Standard |
| 3EME | Respectueux, focus résultats | Précis | Sobres | Brevet central |
| 1ERE | Sérieux, par-il | Dense | Rares | Lycée |

---

## Inventaire complet par catégorie

### 1. Toasts — Exercices (adaptatifs via `_msg()`)

| Situation | Clés _MSGS | Niveaux adaptés |
|---|---|---|
| Bonne réponse boost | `ok_boost` (5 variantes) | Tous |
| Bonne réponse chapitre | `ok_chap` (5 variantes) | Défaut |
| Bonne réponse 6EME | `ok_6eme` (5 variantes) | 6EME |
| Bonne réponse 3EME/1ERE | `ok_3eme` (5 variantes) | 3EME, 1ERE |
| Mauvaise réponse boost | `ko_boost` (3 variantes) | Tous |
| Mauvaise réponse chapitre | `ko_chap` (3 variantes) | Défaut |
| Mauvaise réponse 6EME | `ko_6eme` (3 variantes) | 6EME |
| Mauvaise réponse 3EME/1ERE | `ko_3eme` (3 variantes) | 3EME, 1ERE |

### 2. Écrans contextuels (adaptatifs)

| Écran | Clé _MSGS | Niveaux adaptés |
|---|---|---|
| Post-diagnostic ≥75% | `diag_strong` | 6EME/3EME/def |
| Post-diagnostic 50-74% | `diag_mid` | 6EME/3EME/def |
| Post-diagnostic <50% | `diag_low` | 6EME/3EME/def |
| Post-boost 100% | `boost_perfect` | 6EME/3EME/def |
| Post-boost ≥60% | `boost_good` | 6EME/3EME/def |
| Post-boost <60% | `boost_low` | 6EME/3EME/def |
| Streak 3j | `streak_3` | 6EME/3EME/def |
| Streak 7j | `streak_7` | 6EME/3EME/def |
| Streak autre | `streak_gen` | 6EME/3EME/def |

### 3. Dashboard contextuel

| Condition | Clé _MSGS |
|---|---|
| Tout maîtrisé (3EME) | `ctx_all_mastered_brevet` |
| Tout maîtrisé (autres) | `ctx_all_mastered` |
| Streak ≥3 | `ctx_streak` |
| Chapitre maîtrisé récent | `ctx_mastered_week` |
| Inactif ≥3j | `ctx_inactive` |

### 4. Cours milestones (adaptatifs)

| Seuil | Clé _MSGS | Niveaux |
|---|---|---|
| 5 exos | `cours_5` | 6EME/3EME/def |
| 10 exos | `cours_10` | 6EME/3EME/def |
| 15 exos | `cours_15` | 6EME/3EME/def |
| 20 exos | `cours_20` | 6EME/3EME/def |
| Cours pas encore rédigé | `cours_prep` | 6EME/3EME/def |

### 5. Boost & Chapitre

| Situation | Clé _MSGS |
|---|---|
| Boost prêt | `boost_ready` |
| Boost en préparation | `boost_preparing` |
| Boost en cours | `boost_in_progress` |
| Chapitre terminé | `chap_done` (adaptatif) |

### 6. Coach marks (première fois, persistés localStorage `mx_coach_v1`)

| Feature | Clé _MSGS | Déclencheur |
|---|---|---|
| Premiers indices | `coach_hint` | 1er indice ouvert |
| Premier boost | `coach_boost_first` | 1er clic handleBoost |
| Brouillon | `coach_brouillon` | 1re ouverture switchDraftTab |

### 7. Onboarding (3 slides, slide 3 adapté selon objectif)

| Objectif | Titre slide 3 | Corps |
|---|---|---|
| lacunes | "Ton Boost du jour t'attend !" | Exercices ciblés sur tes vraies lacunes |
| chapitre_jour | "Un chapitre par jour" | Boost + chapitres à ton rythme |
| brevet | "La prépa brevet commence maintenant" | Chapitres clés du brevet |
| toutes_matieres | "Tout le programme est là" | 54 chapitres disponibles |

### 8. Emails automatiques (backend.js)

| Email | Sujet | Personnalisé objectif |
|---|---|---|
| J+0 | "{prénom} vient de rejoindre Matheux 🚀" | Non |
| J+3 | "Comment ça se passe pour {prénom} ? 💪" | Paragraphe central |
| J+5 | "Encore 2 jours, {prénom} 📅" | Accroche avant Stripe |
| J+7 | "Bilan de la semaine de {prénom} ⭐" | Liste résultats |
| Rapport hebdo | "Bilan de la semaine de {prénom} 📊" | Stats réelles |

### 9. Rapport parent hebdomadaire

**Trigger** : `triggerWeeklyParentReport` — dimanche 17h-18h (à activer manuellement dans Apps Script)
**Contenu** : nb exos semaine, % réussite, chapitres maîtrisés, mot adapté au score
**Condition** : ≥1 exercice dans la semaine + trial actif (≤30j)

---

## Règles de validation

### Avant d'ajouter un nouveau message
1. Existe-t-il déjà dans `_MSGS` ? Si oui → utiliser l'existant
2. Le ton est-il cohérent avec le niveau ?
3. Toast ≤ 60 chars idéalement
4. Vérifier absence de doublon hardcodé

### Script de vérification
```bash
# Messages migrés — résultat attendu : 0 ligne
grep -n "Solides bases\|Bon début.*Points\|Quelques notions à retravailler" index.html
grep -n "3 jours d'affilée — une habitude\|7 jours — tu es en mode champion" index.html
grep -n "Ton cours est prêt ! Consulte\|Cours avancé débloqué" index.html
```
