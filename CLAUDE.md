# CLAUDE.md — Matheux (matheux.fr)

> Point d'entrée projet. Lis ce fichier puis consulte les docs détaillées selon la tâche.

---

## Projet en une phrase

SPA vanilla JS (`index.html` ~5900 lignes) + backend Google Apps Script (`backend.js` ~4200 lignes) sur Google Sheets.
Outil pédagogique adaptatif maths collège (6ème→3ème), diagnostic de lacunes, exercices personnalisés, gamification.
MVP solo → 50 clients payants à 9,99 €/mois.

## Contexte fondateur

- Nicolas Follezou, prof de maths, seul développeur
- Codebase V23 GOLD MASTER — patches chirurgicaux, pas de réécriture
- Dossier : `/home/nicolas/Bureau/algebra live`
- Repo : https://github.com/NicoMPC/algebra

---

## Documentation — `docs/`

| Document | Contenu | Quand le lire |
|---|---|---|
| **[docs/claude.md](docs/claude.md)** | GOD MODE — Manuel IA complet (règles, workflow, conventions) | **Toujours** — avant toute modification |
| **[docs/architecture.md](docs/architecture.md)** | Structure frontend/backend, flux API, déploiement | Quand on touche au code |
| **[docs/database.md](docs/database.md)** | Schéma Google Sheets (onglets, colonnes, relations) | Quand on touche aux données |
| **[docs/product.md](docs/product.md)** | Vision produit, parcours utilisateur, workflow Nicolas | Pour comprendre le produit |
| **[docs/roadmap.md](docs/roadmap.md)** | Priorités par blocs, checklist, actions en attente | Pour savoir quoi faire |
| **[docs/agents.md](docs/agents.md)** | Agents IA spécialisés, workflow de délégation CTO | Pour déléguer une tâche |
| **[docs/programme-français-verif.md](docs/programme-français-verif.md)** | Couverture programme Eduscol (~100% — 44 chapitres) | Référence programme |

---

## Règles critiques — rappel rapide

1. **Ne jamais réécrire** — patches chirurgicaux sur le code existant
2. **CORS GAS** — ne JAMAIS mettre `Content-Type: application/json` sur les fetch
3. **Schéma Sheets** — ne jamais modifier les colonnes sans documenter (index hardcodés)
4. **Données mineurs** — RGPD renforcé, consentement parental obligatoire
5. **Estimer les tokens** avant toute tâche lourde → attendre validation
6. **Doc vivante** — mettre à jour, supprimer l'obsolète, ne pas créer de fichiers inutiles

Détail complet dans [docs/claude.md](docs/claude.md).

---

## Déploiement rapide

```bash
# Backend GAS
cd "/home/nicolas/Bureau/algebra live/algebra"
clasp push --force
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "description"

# Frontend
git add index.html && git commit -m "feat: ..." && git push origin main
```

---

## URLs clés

| Ressource | Valeur |
|---|---|
| GAS URL | `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec` |
| Sheet ID (prod) | `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |
| GitHub | `https://github.com/NicoMPC/algebra` |
| Stripe (TEST) | `https://buy.stripe.com/test_14AdRacgw76N7vQcxqa3u00` |
| GA4 | `G-7R2DW4585Y` |
