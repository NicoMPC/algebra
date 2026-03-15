# Fondateur — Architecture de présence humaine · Matheux

> Ce document définit comment Nicolas reste présent dans l'expérience élève et parent,
> même quand 95% des tâches sont automatisées par l'IA.
> À lire avant de modifier tout message, email, ou wording dans le produit.

---

## Le principe fondateur

**L'IA fait le travail. Nicolas prend la responsabilité.**

Pas que Nicolas soit présent à chaque exercice — mais qu'il y ait quelqu'un qui répond si quelque chose va mal.
Un parent qui a un problème sait qu'il peut écrire à nicolas@matheux.fr et avoir une réponse humaine.
Duolingo n'a personne à appeler. Matheux si. C'est ça le fossé.

---

## Ce que l'IA fait en silence

| Tâche | Déclencheur | Contrôle Nicolas |
|---|---|---|
| Génération des boosts | Chaque nuit, rebuildSuivi détecte BOOST TERMINÉ | Valide les anomalies |
| Analyse des patterns d'erreur | Après save_score | Lecture dashboard |
| Rapport parent hebdo | Trigger dimanche 18h | Signe le contenu |
| Détection inactivité | getAdminOverview | Reçoit alerte admin |
| Cours par chapitre | Milestone 5/10/15/20 exos | Rédige les sections |
| Emails de séquence J+3/J+5/J+7 | triggerDailyMarketing | Personnalise si besoin |

---

## Ce que Nicolas fait vraiment

- Valide les cas flagrants (élève sans nouvelles depuis 7j)
- Répond aux emails parents qui demandent un échange humain
- Prépare les boosts manuellement tant que l'automatisation n'est pas active
- Rédige les cours par chapitre (sections 5/10/15/20 exos)
- Publie les brevets blancs pour les 3èmes
- Envoie les 5 actions parent proactives (félicitation, streak, relance, brevet, chapitre)

---

## Les signaux de présence humaine à maintenir absolument

### 1. Timing humain sur les emails automatiques
Jamais envoyés à la seconde exacte pour tout le monde.
`triggerDailyMarketing` tourne entre 9h et 10h — variations naturelles.
Les rapports du dimanche : entre 17h45 et 18h15.

### 2. La première personne dans tous les messages
Jamais : "Notre algorithme a détecté que..."
Toujours : "J'ai remarqué que..." ou "Cette semaine j'ai vu que..."
La première personne maintient la présence de Nicolas même quand c'est l'IA qui génère.

### 3. Les 5 actions parent proactives (admin panel)
Déclenchées par des événements réels, rédigées comme des messages humains.
Nicolas les envoie manuellement depuis la fiche admin — pas automatiquement.
C'est le 5% humain qui justifie le positionnement "prof derrière l'app".

| Action | Déclencheur | Message |
|---|---|---|
| 🎉 Félicitation | Premier boost terminé (J+1) | Chaleureux, court, humain |
| 🔥 Partage streak | Streak ≥ 7 jours | Valorisant, factuel |
| 💬 Relance douce | Inactif 3j (avant 7j) | Bienveillant, sans culpabilisation |
| 📊 Résultats brevet | Après brevet blanc | Analytique, constructif |
| 📚 Bilan chapitre | Chapitre terminé (20 exos) | Progressif, encourageant |

### 4. Le feedback de session comme signal d'écoute
L'élève donne son ressenti à la fin de chaque boost/brevet/chapitre (4 émojis).
Nicolas le voit dans la fiche admin en préparant le prochain contenu.
Si 2 feedbacks "Difficile" consécutifs → le prochain boost doit être allégé.
C'est la boucle de feedback humain que l'algorithme seul ne peut pas faire.

### 5. L'email de Nicolas (1x/mois)
Un email court, signé Nicolas, envoyé à toute la base.
Pas personnalisé — mais humain.
Contenu : une observation réelle sur le mois écoulé, un conseil, une anecdote pédagogique.
20 minutes à écrire. Impact fort sur la rétention.

---

## Ce qui ne doit JAMAIS changer

- L'adresse de réponse : `nicolas@matheux.fr` (pas un no-reply)
- La signature dans les emails : "Nicolas · Prof de maths · Matheux" (pas "L'équipe Matheux")
- Le ton : vouvoiement pour les parents, tutoiement pour les élèves
- La transparence : ne jamais prétendre que Nicolas a écrit quelque chose qu'il n'a pas écrit

---

## À terme (après 200 clients)

L'automatisation s'étend mais la présence humaine reste.
Nicolas passe de "exécutant" à "superviseur" :
- Il valide les anomalies détectées par l'agent
- Il répond aux emails humains (les rares qui arrivent)
- Il rédige les cours et ajuste les templates
- Il envoie les 5 actions parent proactives (15-20 min/jour max)

Le produit scale. La confiance reste.
