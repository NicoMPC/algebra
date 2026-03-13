# Produit — Matheux

> Vision, cible, parcours utilisateur, workflow quotidien Nicolas.
> Voir aussi [claude.md](claude.md) pour les règles et [roadmap.md](roadmap.md) pour les priorités.

---

## Vision

**Matheux est un outil de soutien scolaire en maths pour les collégiens (6ème → 3ème), qui détecte automatiquement les lacunes d'un élève et lui prépare des exercices personnalisés chaque jour.**

Le fondateur (Nicolas Follezou, prof de maths) fait le lien humain : il analyse les résultats, prépare les boosts quotidiens, et assigne les chapitres suivants. Objectif : accompagnement quasi-individuel à 9,99 €/mois — 25× moins cher qu'un cours particulier.

---

## Utilisateurs cibles

### L'élève (11-15 ans)
- Collégien de la 6ème à la 3ème, lacunes en maths
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
1. Parent arrive sur matheux.fr → hero direct : problème → solution → prix
2. CTA "Commencer le diagnostic →" → overlay fullscreen (masque la landing, focus total)
3. Step 1 : choix classe (6e-3e) → Step 2 : chapitres déjà vus
4. Step 3 : quiz diagnostic inline (4-10 questions, box stable sans jump)
5. Step 4 : formulaire inscription (prénom + email + MDP + consentement parental)
6. Compte créé → code 6 chars → accès immédiat

### Onboarding (J0)
1. Auto-login → onboarding 3 slides (dernier slide incite à "Lancer ton Boost du jour")
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
2. J7 : overlay bloquant → "9,99 €/mois pour continuer"
3. Email J+7 avec lien Stripe direct
4. Bouton "Voir ma progression quand même" (ferme l'overlay)

---

## Modèle économique

| Élément | Détail |
|---|---|
| Prix | 9,99 €/mois |
| Essai | 7 jours gratuits, accès complet, sans carte bancaire |
| Paiement | Stripe (lien TEST actif — à passer en PROD) |
| Cible | 50 clients = ~500 € MRR |

---

## Pédagogie

- **Diagnostic avant exercices** : on identifie les lacunes avant de travailler
- **Boost quotidien** : 5 exercices/jour = habitude, pas surcharge
- **Indices progressifs** : 1-3 étapes + formule clé révélée après erreur
- `lvl:1` = fondamental, `lvl:2` = avancé (type contrôle/brevet)
- 29 chapitres × 20 exos = 580 exercices + 58 diagnostics + 120 brevet
- Couverture ~85% programme officiel — détail dans [programme-français-verif.md](programme-français-verif.md)

---

## Emails automatiques

| Email | Déclencheur | Contenu |
|---|---|---|
| J+0 | `register()` | Bienvenue + code accès + premiers pas |
| J+3 | `triggerDailyMarketing` | Encouragement + rappel boost |
| J+7 | `triggerDailyMarketing` | Trial expire → lien Stripe direct |

Envoyés depuis `no-reply@matheux.fr` via GmailApp.

---

## Juridique

5 pages légales en production :
- `mentions-legales.html` — SIRET 837 763 713 00059
- `cgu.html` — mineurs, essai 7j, résiliation, clause bêta
- `cgv.html` — 9,99€/mois, droit de rétractation 14j
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
- 📧 Indicateurs emails J0/J3/J7
- Actions : publier boost, publier chapitre, publier brevet blanc (3EME), copier prompt Claude

### Vues élève
- **📚 Chapitres** : boost quotidien + chapitres par progression
- **📊 Progression** : barres de progression + scores par chapitre
- **🎓 Brevet** (3EME) : quiz brevet sans indices, 120 exos, résultats par chapitre
- **Feedback** : bouton "📢 Signaler" après chaque exercice → onglet Insights
