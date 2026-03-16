# Agent Matheux — Fiche de mission

> À lire avant toute session. Complète CLAUDE.md (technique) avec
> le contexte humain, business et la vision produit.
> Mise à jour : mars 2026

---

## Qui est Nicolas

Nicolas Follezou, 40 ans, prof de maths, fondateur solo de Matheux.
Travaille vite, pense en vision, délègue l'exécution à l'IA.
Il ne veut pas d'explication — il veut que ça marche.
Il pense en métiers (pédagogue, dev, marketeur, opérateur) et
jongle entre eux dans une même journée.

Style de communication : direct, informel, parfois en flux de
conscience. L'IA doit savoir extraire l'essentiel et l'exécuter.
Quand Nicolas dit "fais ça propre", ça veut dire : zéro dette
technique, doc à jour, rien de mort dans le repo.

---

## Ce qu'est Matheux (vision réelle)

Ce n'est pas "un générateur d'exercices de maths".
C'est un profil cognitif qui s'affine à chaque réponse.

Après 30 jours, Matheux sait :
- Les patterns d'erreur exacts de l'élève (pas juste le chapitre)
- Sa vitesse de progression chapitre par chapitre
- Son comportement face à la difficulté (indices, brouillon, blocages)
- Ses incompréhensions déclarées (bouton "j'ai pas compris")
- Son créneau d'activité, son streak, sa progression réelle

Cette mémoire ne peut pas être transférée ailleurs.
C'est le levier de rétention central du produit.

L'argument commercial : "Un prof de maths derrière, pas juste
un algorithme." Le parent sait qu'il peut écrire à
nicolas@matheux.fr et avoir une réponse humaine.
Duolingo n'a personne à appeler. Matheux si.

Prix : 19,99€/mois — 0,66€/jour — 25× moins cher qu'un cours particulier.

---

## Architecture décisionnelle

```
Nicolas (vision + validation) → IA (exécution + doc)
```

Nicolas ne code pas. Il prompt. Il valide. Il vend.
L'IA fait tout le reste, mais Nicolas reste le décideur final
sur les choix produit, pédagogiques et commerciaux.

---

## Les 3 utilisateurs

### L'élève (11-17 ans)
- Veut : progresser vite, être encouragé, ne pas s'ennuyer
- Sensible à : gamification, ton direct, emojis encourageants
- Mobile first. 10-15 min/jour max

### Le parent (le vrai client)
- Veut : voir son enfant progresser, avoir confiance
- Sensible à : ton prof humain, données chiffrées, prix vs cours particulier
- Reçoit : emails J+0/J+3/J+5/J+7 + rapport hebdo dimanche

### Nicolas (l'opérateur)
- Veut : dashboard clair, workflow < 10 min/matin, zéro friction
- Utilise : admin cockpit → copier prompt → Claude → JSON → publier
- Objectif phase 1 : 50 clients, 2-3h/jour de travail

---

## Comportement agent attendu

### Ce que l'IA FAIT
- Lit CLAUDE.md + le doc concerné AVANT de toucher au code
- Exécute des patches chirurgicaux, jamais de réécriture
- Met à jour la doc après chaque modification (vivante)
- Génère un rapport lisible par Nicolas à la fin de chaque session
- Alerte si une action risque de casser l'architecture ou la BDD
- Estime les tokens avant toute tâche massive → attend validation

### Ce que l'IA NE FAIT PAS
- Réécrire index.html ou backend.js (trop gros, trop risqué)
- Ajouter des dépendances sans validation
- Modifier le schéma Google Sheets sans documenter dans database.md
- Mettre `Content-Type: application/json` dans un fetch GAS (CORS fatal)
- Créer des features non demandées même si "évidentes"
- Laisser des scripts morts ou de la doc obsolète

### Ton attendu dans les rapports
- Factuel, direct, en français
- Ce qui a été fait (liste exhaustive avec fichiers et numéros de lignes)
- Ce qui reste à faire manuellement (clairement séparé)
- Aucun rembourrage, aucune répétition

---

## Roadmap décisionnelle (mars 2026)

### Maintenant — avant lancement
1. Stripe TEST → PROD (manuel Nicolas)
2. Alias email (manuel Nicolas)
3. Triggers Apps Script (manuel Nicolas)

### Semaine 1 post-lancement
- Observer les premiers élèves réels
- Préparer les premiers boosts personnalisés
- Vérifier les emails automatiques

### Phase 2 — après 20 clients
- Automatisation boosts nocturne
- Rapport parent hebdo automatique (trigger à activer)
- Offres différenciées selon colonne Objectif

### Phase 3 — après 50 clients
- Migration Sheets → Supabase
- Migration emails → Brevo/Resend
- Agent IA analyse nocturne

### Ne jamais faire avant d'en avoir besoin
- Migration technique (Supabase, React, serveur)
- Offres prix sans données réelles
- Automatisation de ce que Nicolas n'a pas encore compris à la main

---

## Métriques de succès

| Métrique | Valeur cible | État |
|---|---|---|
| Clients payants | 50 | 0 (lancement J0) |
| MRR | ~1000€ | 0 |
| Taux conversion trial | >20% | — |
| Temps admin/matin | <10 min | ~15 min actuellement |
| Score qualité exercices | >98% | ~98% (@77) |
| Tests automatisés | 100% | 74/74 |

---

## Ce qui rend Matheux défendable

1. **La mémoire cognitive** (30j de données = impossible à recréer ailleurs)
2. **Le prof humain derrière** (nicolas@matheux.fr répond)
3. **Le prix** (19,99€ vs 25-40€/h de cours particulier)
4. **La progression documentée** (rapport parent hebdo avec chiffres réels)

Personne ne peut copier les 3 en même temps rapidement. C'est le fossé.
