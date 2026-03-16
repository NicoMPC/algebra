# Workflow quotidien Nicolas — Matheux

> Chaque matin entre 8h et 10h. Maximum 10 minutes.
> Tout se passe dans l'admin (triple-clic logo sur matheux.fr).

## Les 3 étapes

### 1. Ouvrir l'onglet À FAIRE (30 secondes)

Les cartes sont triées par urgence.
Contenu d'abord (contact, boost, chapitre, cours).
Emails ensuite (J+0/J+3/J+5/J+7).

### 2. Traiter dans l'ordre (5-8 minutes)

**Pour chaque boost à préparer :**
1. Clic "Copier le prompt Claude"
2. Coller dans claude.ai (ou Claude Code)
3. Copier le JSON retourné
4. Coller dans le textarea "Coller le JSON ici"
5. Clic "Publier" → carte passe en FAIT automatiquement

**Pour chaque chapitre à assigner :**
Même workflow, JSON de 20 exercices.

**Pour chaque cours à rédiger :**
Même workflow, JSON des 4 sections (5/10/15/20 exos).

**Pour chaque email dû :**
1. "Voir le template" → éditer si besoin (max 2 phrases)
2. "Copier dans le presse-papier"
3. Coller dans Gmail, envoyer
4. "Marquer envoyé" → coche automatique

**Pour un élève inactif :**
"Marquer contacté" après avoir envoyé un message WhatsApp au parent.

### 3. Vérifier l'onglet FAIT (10 secondes)

Si tout est traité → "Tout est à jour"
Sinon → revenir sur les cartes restantes.

## Format du prompt Claude pour un boost

Copié automatiquement par l'admin. Contient :
- Prénom + niveau
- Historique des exercices (réussi/raté avec temps et indices)
- Points faibles prioritaires
- Erreurs systématiques détectées
- Incompréhensions déclarées ("j'ai pas compris")
- Consigne : 5 exercices JSON format strict

## Le dimanche

Un bouton "Rapport parents" apparaît dans l'admin.
Un clic → envoie automatiquement le bilan hebdo à tous les parents actifs.

## Ce qui se passe sans toi

- Emails J+3/J+5/J+7 → automatiques (trigger 9h-10h)
- Progression élève → mise à jour à chaque exercice
- Streak → calculé automatiquement
- Cours débloqués → automatique (paliers 5/10/15/20)
