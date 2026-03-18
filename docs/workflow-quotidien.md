# Workflow quotidien Nicolas — Matheux

> Chaque matin entre 8h et 10h. Maximum 10 minutes.
> Tout se passe dans l'admin (triple-clic logo sur matheux.fr).

## Les 6 onglets admin

| Onglet | Contenu |
|---|---|
| **NOUVEAU** | Inscrits du jour + statut mail J+0 |
| **À FAIRE** | Boosts et chapitres terminés → préparer le suivant |
| **FAIT** | Journal des actions traitées aujourd'hui |
| **📧 MAILS** | Emails à confirmer (J+0/J+3/J+5/J+7) avec badge compteur |
| **💤 INACTIFS** | Élèves inactifs >3j ou jamais connectés |
| **📊 RAPPORT** | Dimanche : rapport hebdo par élève, copier JSON semaine |

## Workflow quotidien (5-8 min)

### 1. Onglet À FAIRE — Boost et chapitres

**Pour chaque boost à préparer :**
1. Clic "📋 Copier dernier boost + résultats" → copie le dernier boost complet avec les résultats de l'élève (réponses, temps, indices, formule)
2. Coller dans Claude → il génère le prochain boost adapté
3. Copier le JSON retourné
4. Coller dans le textarea
5. Clic "Publier" → carte passe en FAIT

**Pour chaque chapitre à assigner :**
1. Clic "📋 Copier le prompt Claude"
2. Même workflow, JSON de 20 exercices

### 2. Onglet MAILS — Confirmer les emails

Pour chaque email dû : "Voir" le template, puis "✓ Envoyé" après envoi.
Badge compteur sur l'onglet si des emails sont en attente.

### 3. Onglet INACTIFS — Surveiller

Liste des élèves inactifs >3j avec email et dernière connexion.
Pas d'action directe — juste un suivi visuel.

### 4. Onglet FAIT — Vérifier

Journal du jour + élèves à jour.

## Le dimanche — Onglet RAPPORT

1. Pour chaque élève actif cette semaine :
   - "📋 Copier JSON semaine" → copie tous les boosts de la semaine avec exercices, indices, formules
   - Coller dans Claude → il rédige le rapport parent
   - "✅ Rapport envoyé" une fois le mail parti
2. Bouton "📨 Envoyer le rapport automatique" pour l'envoi groupé

## Ce qui se passe sans toi

- Progression élève → mise à jour à chaque exercice
- Streak → calculé automatiquement
- Cours débloqués → automatique (paliers 5/10/15/20)
- Emails J+3/J+5/J+7 → manuels pour l'instant (trigger à activer dès 10 clients)
