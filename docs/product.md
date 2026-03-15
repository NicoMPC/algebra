# Produit — Matheux

> Vision, cible, parcours utilisateur, workflow quotidien Nicolas.
> Voir aussi [claude.md](claude.md) pour les règles et [roadmap.md](roadmap.md) pour les priorités.

---

## Vision

**Matheux est un outil de soutien scolaire en maths pour les collégiens et lycéens (6ème → 3ème + 1ère Spé Maths), qui détecte automatiquement les lacunes d'un élève et lui prépare des exercices personnalisés chaque jour.**

Le fondateur (Nicolas Follezou, prof de maths) fait le lien humain : il analyse les résultats, prépare les boosts quotidiens, et assigne les chapitres suivants. Objectif : accompagnement quasi-individuel à 19,99 €/mois — 25× moins cher qu'un cours particulier.

**Positionnement différenciant** :
Matheux n'est pas "des exercices personnalisés" — tout le monde dit ça.
Matheux c'est une **empreinte cognitive unique** : après 30 jours, l'app connaît
les patterns d'erreur de l'élève, sa vitesse de progression, ses lacunes réelles.
Cette mémoire ne peut pas être transférée. C'est le levier de rétention le plus puissant.

Argument commercial principal : "Un prof de maths derrière, pas juste un algorithme."
Personne ne peut copier ça facilement — ça demande Nicolas.

---

## Utilisateurs cibles

### L'élève (11-17 ans)
- Collégien (6ème→3ème) ou lycéen (1ère Spé Maths), lacunes en maths
- Téléphone ou tablette familiale, 10-15 min/jour
- Sensible à la gamification (streak, XP, confettis)

### Le parent
- Cherche solution abordable et sérieuse
- Compare avec cours particuliers (25-40 €/h) et applis gratuites
- Besoin de confiance : prof de maths derrière, pas juste un algorithme

### Nicolas (fondateur)
- Seul sur le projet, 2-3h/jour de travail manuel en phase 1
- Gère boosts quotidiens, chapitres, relances
- Google Sheets + Admin Panel comme outils principaux

---

## Parcours utilisateur

### Acquisition (landing → inscription)
1. Parent arrive sur matheux.fr → hero ciblé parent : "Votre enfant mérite un prof qui le connaît vraiment." → 11 sections (chiffres, programme, comment ça marche, **ce que Matheux sait** (empreinte cognitive), sur mesure, mockup, témoignages ×4, fondateur, prix, FAQ ×7, CTA)
2. CTA "Voir où en est mon enfant →" → overlay fullscreen (masque la landing, focus total)
3. Step 1 : choix classe (6e-3e) → Step 2 : chapitres déjà vus
4. Step 3 : quiz diagnostic inline (4-10 questions, box stable sans jump)
5. Step 4 : formulaire inscription (prénom + email + MDP + consentement parental)
6. Compte créé → code 6 chars → accès immédiat

### Onboarding (J0)
1. Auto-login → **slide objectif** (4 choix post-quiz : lacunes / chapitre_jour / brevet / toutes_matieres)
   → stocké en col N Users → personnalise les emails J+5/J+7 et futurs pitch d'offres
   → onboarding 3 slides (dernier slide incite à "Lancer ton Boost du jour")
2. Boost personnalisé généré en background (`boostFromDiag`)
3. L'élève voit son premier "Mon Boost du jour" immédiatement

### Routine quotidienne (J1-J7)
1. "Mon Boost du jour" : 5 exercices, 10-15 min
2. Feedback immédiat + indices si erreur + formule clé
3. Boost terminé → confettis + redirect chapitres
4. Peut explorer les chapitres librement
5. Nicolas voit l'avancement dans le dashboard admin

### Conversion (J7)
1. Badge J-X visible dès J5
2. J7 : overlay bloquant → "19,99 €/mois pour continuer"
3. Email J+7 avec lien Stripe direct
4. Bouton "Voir ma progression quand même" (ferme l'overlay)

---

## Modèle économique

| Élément | Détail |
|---|---|
| Prix | 19,99 €/mois |
| Essai | 7 jours gratuits, accès complet, sans carte bancaire |
| Paiement | Stripe — **lien TEST actif, à passer en PROD manuellement** (3 occurrences : `index.html`, `backend.js`, `cgv.html`) |
| Cible | 50 clients = ~500 € MRR |
| Offre flash | -50% premier mois (9,99€) envoyée manuellement à J+2/J+3 aux élèves engagés | Lien Stripe séparé, zéro code |
| Offres futures | Basées sur données col Objectif — décision après 10-15 clients | Ne pas créer avant |

---

## Pédagogie

- **Diagnostic avant exercices** : on identifie les lacunes avant de travailler
- **Boost quotidien** : 5 exercices/jour = habitude, pas surcharge
- **Indices progressifs** : 1-3 étapes + formule clé révélée après erreur
- `lvl:1` = fondamental, `lvl:2` = avancé (type contrôle/brevet)
- 54 chapitres × 20 exos = **1080 exercices** + 108 diagnostics + 540 boost + 144 brevet (3EME, 15 chap, format standard)
- Couverture **~100%** programme collège officiel + 1ère Spé Maths (10 chapitres expérimentaux) — détail dans [programme-français-verif.md](programme-français-verif.md)

---

## Emails automatiques

| Email | Déclencheur | Destinataire | Contenu |
|---|---|---|---|
| J+0 | `register()` auto OU manuel admin (voir ci-dessous) | Parent | Bienvenue, 3 étapes (diagnostic → boost → progression), CTA matheux.fr, rappel 7j gratuit sans CB |
| J+3 | `triggerDailyMarketing` (⚠️ trigger à activer manuellement) | Parent | Encouragement + rappel boost quotidien |
| J+5 | `triggerDailyMarketing` (⚠️ trigger à activer manuellement) | Parent | "Encore 2 jours" — urgence douce + lien Stripe |
| J+7 | `triggerDailyMarketing` (⚠️ trigger à activer manuellement) | Parent | Trial expire → lien Stripe direct |
| Reset MDP | `sendPasswordReset()` | Élève/parent | Code 6 chiffres, expire 15 min |

**Architecture email :**
- Expéditeur : `no-reply@matheux.fr` (alias GmailApp via seopourvous@gmail.com)
- Reply-to : `nicolas@matheux.fr` (les parents qui répondent arrivent sur la boîte pro)
- Contact public affiché sur le site : `contact@matheux.fr`
- Rapport matin Nicolas : `FOUNDER_EMAIL = 'seopourvous@gmail.com'` (à migrer vers `nicolas@matheux.fr` plus tard)

**Ton des emails :** vouvoiement — le destinataire est le **parent**. Le prénom utilisé est celui de **l'élève**. Ton rassurant de prof humain, pas startup.

**Mail de bienvenue manuel (fallback) :**
GmailApp ne peut pas envoyer depuis `no-reply@matheux.fr` sans alias Gmail fonctionnel. Si J+0 auto échoue ou n'a pas été envoyé, le modal élève affiche un bouton `📧 Copier mail de bienvenue` → copie le texte complet prêt à coller dans Gmail (champ À, Objet, corps). Un second bouton `✓ Marquer comme envoyé` appelle `log_manual_email` GAS → insère une ligne `J+0-manuel / envoyé` dans l'onglet Emails. L'indicateur J0 passe de ⏳ à ✅ instantanément. Le bouton n'apparaît que si aucun log J+0/J+0-manuel n'existe pour cet élève.

---

## Juridique

5 pages légales en production :
- `mentions-legales.html` — SIRET 837 763 713 00059
- `cgu.html` — mineurs, essai 7j, résiliation, clause bêta
- `cgv.html` — 19,99€/mois, droit de rétractation 14j
- `politique-confidentialite.html` — RGPD renforcé mineurs
- `politique-cookies.html` — localStorage + GA4 consentement explicite

---

## Workflow quotidien Nicolas (Admin Panel)

### Accès
Triple-clic sur le logo → Admin Panel (comptes `IsAdmin: true` uniquement).

### Procédure quotidienne (~10 min/matin)
1. Scanner les cartes élèves triées par urgence (🔴 en tête)
2. Pour chaque `⚡ BOOST TERMINÉ` :
   - Cliquer sur l'élève → voir ses lacunes
   - "📋 Copier le prompt Claude" → coller dans Claude → JSON → "Publier un boost"
3. Pour chaque `✅ CHAPITRE TERMINÉ` :
   - Même procédure → "Publier un chapitre"
4. Vérifier les `🔴 BLOQUÉ` → message parent si nécessaire

### Les 4 statuts `⚡ ACTION NICOLAS`

| Statut | Signification | Action |
|---|---|---|
| `🔴 BLOQUÉ` | Inactif >7j ET scores <40% | Message WhatsApp parent |
| `⚡ BOOST TERMINÉ` | A fini ses 5 exos | Publier le prochain boost |
| `✅ CHAPITRE TERMINÉ` | >20 exos sur ce chapitre | Assigner le suivant |
| `👍 RAS` | Tout va bien | Rien |

### Ce que l'admin voit par élève
- Toutes les réponses (badge DIAG/BOOST)
- Scores par chapitre triés : terminés → en cours → diagnostiqués
- Statut boost : ⏳ En attente → 🔄 En cours X/5 → ✓ Terminé
- Métriques : ⏱ temps moyen, 💡 indices, 🧮 % formule
- 📧 Indicateurs emails J0/J3/J7 (J0 réel depuis onglet Emails — ✅ si envoyé, ⏳ si non)
- 📧 Bouton "Copier mail de bienvenue" si J0 pas encore envoyé + "Marquer comme envoyé"
- Actions : publier boost, publier chapitre, publier brevet blanc (3EME), copier prompt Claude

### Vues élève
- **📚 Chapitres** : boost quotidien + chapitres par progression
- **📊 Progression** : barres de progression + scores par chapitre
- **🎓 Brevet** (3EME) : quiz brevet sans indices, 120 exos, résultats par chapitre
- **🔁 Révision** : chapitres d'une autre année assignés par l'admin (col M `RevisionChapters`), badge 🔁 + toast élève
- **Brouillon + Calculette** : mobile = bottom sheet 50vh avec onglets, desktop = panneau latéral 1/3 écran. Symboles adaptés au chapitre, mode quadrillé, calculette contextuelle (trig, fractions, etc.)
- **Feedback** : bouton "📢 Signaler" après chaque exercice → onglet Insights
