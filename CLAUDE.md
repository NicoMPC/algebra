# CLAUDE.md — Matheux (matheux.fr)

> Point d'entrée projet. Référence complète : **[docs/claude.md](docs/claude.md)**

## Projet

SPA vanilla JS (`index.html` ~9700 lignes) + backend Google Apps Script (`backend.js` ~5100 lignes) sur Google Sheets.
Outil pédagogique adaptatif maths 6ème→3ème + 1ère Spé Maths. MVP solo → 50 clients à 19,99 €/mois. **GAS @77** — 1872 exercices audités (score qualité ~98%).

## Documentation — `docs/`

| Document | Quand le lire |
|---|---|
| **[docs/claude.md](docs/claude.md)** | **Toujours** — règles, workflow, conventions |
| **[docs/architecture.md](docs/architecture.md)** | Quand on touche au code |
| **[docs/database.md](docs/database.md)** | Quand on touche aux données |
| **[docs/product.md](docs/product.md)** | Pour comprendre le produit |
| **[docs/roadmap.md](docs/roadmap.md)** | Pour savoir quoi faire |

## Règles critiques

1. **Ne jamais réécrire** — patches chirurgicaux uniquement
2. **CORS GAS** — ne JAMAIS mettre `Content-Type: application/json` sur les fetch
3. **Schéma Sheets** — ne jamais modifier les colonnes sans documenter
4. **Estimer les tokens** avant toute tâche lourde → attendre validation

Détail complet dans [docs/claude.md](docs/claude.md).

## Déploiement rapide

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"
clasp push --force
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "desc"
git add index.html && git commit -m "feat: ..." && git push origin main
```

## URLs clés

| Ressource | Valeur |
|---|---|
| GAS URL | `https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec` |
| Sheet ID (prod) | `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |
| GitHub | `https://github.com/NicoMPC/algebra` |
| Stripe (TEST) | `https://buy.stripe.com/test_14AdRacgw76N7vQcxqa3u00` |
| GA4 | `G-7R2DW4585Y` |
