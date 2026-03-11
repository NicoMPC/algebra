# Notion — Structure Matheux (copier-coller prêt)

## Page principale : Matheux

### Tableau KPIs globaux

| KPI | Valeur | Cible | Source données |
|-----|--------|-------|----------------|
| Users inscrits (total) | — | 50 | Sheet `Users` COUNT |
| Users actifs 7j | — | 30 | Sheet `Scores` COUNTUNIQUE(Code) last 7j |
| MRR (€) | — | 499,50 € | Sheet `Users` COL `Premium` × 9,99 |
| Taux conversion freemium→payant | — | 30 % | Premium / Total × 100 |
| Streak moyen | — | ≥ 5j | Sheet `Progress` AVG `Streak` |
| NPS | — | > 50 | Formulaire manuel mensuel |

---

## Pages domaine

### 🛠 Produit

**Roadmap par blocs**

| Bloc | Titre | Statut | Date cible |
|------|-------|--------|------------|
| BLOC 1 | Socle technique (bugs 1–7) | ✅ Terminé | mars 2026 |
| BLOC B | UX Progression & Mobile | ✅ Terminé | mars 2026 |
| BLOC 2 | Fiabilité & workflow quotidien | 🟡 En cours | avril 2026 |
| BLOC 3 | Juridique & paiement | 🔴 À faire | avril 2026 |
| BLOC 4 | Marketing & conversion | 🔴 À faire | mai 2026 |
| BLOC 5 | Automatisation & scale | 🔴 À faire | juin 2026 |

**Bugs ouverts** (sous-page)
- Colonne : ID | Description | Priorité (🔴/🟡/🟢) | Fichier concerné | Statut | Fix appliqué

**Features en cours** (sous-page)
- P2 — Agent local Python génération exos (remplace callClaude dans GAS)
- P3 — Algo sélection exos : no-repeat + priorisation score < 50 %

**Changelog** (sous-page)
- Une ligne par session : date | résumé du patch | fichiers modifiés | commit hash

---

### 📣 Marketing

**Pipeline campagnes**

| Canal | Campagne | Statut | Reach estimé | Résultat |
|-------|----------|--------|--------------|----------|
| Instagram | Reel avant/après diagnostic | 🔴 À faire | — | — |
| WhatsApp parents | Message direct 10 contacts | 🟡 En cours | 10 | — |
| Bouche-à-oreille élèves | Parrainage 1 mois offert | 🔴 À faire | — | — |

**Tests A/B landing**
- Version A : hero actuel (fond sombre + CTA "Commencer")
- Version B : à tester — social proof avec témoignage élève réel
- Métrique : taux clic CTA sur mobile

---

### ⚖️ Juridique

**Checklist RGPD (données mineurs — priorité haute)**

| Item | Statut | Date limite | Note |
|------|--------|-------------|------|
| Mentions légales sur index.html | 🔴 À faire | 15 avril 2026 | Nom + adresse fondateur |
| Case consentement parental à l'inscription | 🔴 À faire | 15 avril 2026 | Obligatoire -15 ans |
| CGU / CGV | 🔴 À faire | 15 avril 2026 | Modèle Jurislogic OK pour MVP |
| Politique cookies | 🔴 À faire | 30 avril 2026 | Pas de tracking tiers pour l'instant |
| DPO désigné | 🔴 À faire | Avant 1er paiement | Fondateur = DPO pour MVP |
| Registre traitements | 🔴 À faire | Avant 1er paiement | Tableur simple suffit |

---

### 💰 Finance

**Suivi MRR**

| Mois | Users payants | MRR (€) | Coûts (€) | Marge |
|------|--------------|---------|-----------|-------|
| Avril 2026 | 0 | 0 | — | — |
| Mai 2026 | — | — | — | — |
| Juin 2026 | — | — | — | — |

**Coûts fixes mensuels**

| Poste | Coût estimé | Notes |
|-------|-------------|-------|
| Claude API (génération exos) | 5–20 € | ~5 000 tokens/élève/semaine |
| Stripe | 1,4 % + 0,25 € par transaction | Pas de frais fixes |
| Domaine mac.fr | ~1 € | Déjà payé |
| Hébergement | 0 € | GitHub Pages + GAS gratuit |
| Budget total | ~400 € (one-shot) | Objectif : 1 mois Claude Max |

**Projection 6 mois**

| Mois | Users payants | MRR | Coûts | Résultat |
|------|--------------|-----|-------|----------|
| M+1 | 5 | 50 € | 30 € | +20 € |
| M+2 | 15 | 150 € | 40 € | +110 € |
| M+3 | 30 | 300 € | 55 € | +245 € |
| M+6 | 50 | 499 € | 70 € | +429 € |

---

### 📧 Emails

**Séquences configurées**

| Séquence | Déclencheur | Emails | Statut |
|----------|-------------|--------|--------|
| Bienvenue | Inscription | J0 : accueil + tuto | 🔴 À faire |
| Conversion | J+3 sans abonnement | J+3, J+7 | 🔴 À faire |
| Rapport hebdo parents | Chaque lundi | Résumé progrès élève | 🔴 À faire |

**Métriques par email** (à remplir après envoi)

| Email | Envois | Taux ouverture | Taux clic | Conversions |
|-------|--------|---------------|-----------|-------------|
| Bienvenue J0 | — | — | — | — |
| Relance J+3 | — | — | — | — |

---

### 📊 Analytics

**Dashboard hebdo — 5 KPIs à regarder chaque lundi matin**

1. Users actifs 7j (source : Sheet `Scores` → COUNTUNIQUE Code last 7j)
2. Taux completion diagnostic (source : `DiagnosticExos` vs `Scores` par élève)
3. Nombre HARD cette semaine (source : `Scores` Résultat='HARD' last 7j)
4. Boost consommés (source : `DailyBoosts` Count last 7j)
5. Nouveaux inscrits (source : `Users` DateInscription last 7j)

**Alertes à configurer**
- Si users actifs 7j chute > 20 % → investiguer bug backend
- Si HARD > 60 % des scores → qualité exos à revoir
- Si 0 nouvel inscrit en 48h → vérifier landing + lien inscription

---

## Template BLOC

### Structure standard pour chaque bloc

| Status | Titre | Date cible | Responsable | Next action concrète | Lien PR/commit |
|--------|-------|------------|-------------|----------------------|----------------|
| ✅ Fait | generate_diagnostic GAS | mars 2026 | Nicolas | — | d2da698 |
| ✅ Fait | generate_daily_boost GAS | mars 2026 | Nicolas | — | d2da698 |
| ✅ Fait | generate_remediation GAS | mars 2026 | Nicolas | — | d2da698 |
| ✅ Fait | Curriculum_Officiel 480 exos | mars 2026 | Nicolas | — | d2da698 |
| 🟡 En cours | Agent Python génération exos | avril 2026 | Nicolas | Coder `gen_exos.py` lisant Progress via sheets.py | — |
| 🟡 En cours | Algo no-repeat + priorisation | avril 2026 | Nicolas | Ajouter onglet `SeenExos` dans Sheet | — |
| 🔴 À faire | Validation inputs GAS | avril 2026 | Nicolas | Ajouter check email regex dans doPost | — |
| 🔴 À faire | Colonne Premium + TrialStart | avril 2026 | Nicolas | ALTER Users sheet + login retourne premium | — |

---

## Intégration Claude Code → Notion

### Étape 1 — Créer l'intégration Notion

1. Aller sur notion.so/my-integrations → "New integration"
2. Nom : `Matheux Claude Code`, type : Internal
3. Copier le token : `secret_xxxxxxxxxxxx`
4. Ouvrir la database Notion cible → "..." → "Add connections" → sélectionner `Matheux Claude Code`
5. Copier l'ID de la database depuis l'URL : `notion.so/{workspace}/{DATABASE_ID}?v=...`

### Étape 2 — Structure JSON requête API

```json
POST https://api.notion.com/v1/pages
Authorization: Bearer secret_xxxxxxxxxxxx
Notion-Version: 2022-06-28
Content-Type: application/json

{
  "parent": { "database_id": "VOTRE_DATABASE_ID" },
  "properties": {
    "Titre": { "title": [{ "text": { "content": "BLOC 2 terminé" } }] },
    "Date": { "date": { "start": "2026-03-10" } },
    "Statut": { "select": { "name": "✅ Fait" } },
    "Notes": { "rich_text": [{ "text": { "content": "Rapport matin + génération IA implémentés" } }] }
  }
}
```

### Étape 3 — Script Python `docs/notify_notion.py`

```python
#!/usr/bin/env python3
import argparse, requests, os
from datetime import date

TOKEN = os.environ.get("NOTION_TOKEN")
DB_ID = os.environ.get("NOTION_DB_ID")

parser = argparse.ArgumentParser()
parser.add_argument("--milestone", required=True)
parser.add_argument("--date", default=str(date.today()))
args = parser.parse_args()

r = requests.post(
    "https://api.notion.com/v1/pages",
    headers={"Authorization": f"Bearer {TOKEN}", "Notion-Version": "2022-06-28"},
    json={
        "parent": {"database_id": DB_ID},
        "properties": {
            "Titre": {"title": [{"text": {"content": args.milestone}}]},
            "Date": {"date": {"start": args.date}},
            "Statut": {"select": {"name": "✅ Fait"}}
        }
    }
)
print("OK" if r.status_code == 200 else f"Erreur {r.status_code}: {r.text}")
```

Usage : `NOTION_TOKEN=secret_xxx NOTION_DB_ID=xxx python3 docs/notify_notion.py --milestone "BLOC 2 terminé"`

### Étape 4 — Hook post-commit Claude Code

Créer `.git/hooks/post-commit` (chmod +x) :

```bash
#!/bin/bash
MSG=$(git log -1 --pretty=%s)
if echo "$MSG" | grep -q "BLOC"; then
  NOTION_TOKEN=secret_xxx NOTION_DB_ID=xxx \
    python3 /home/nicolas/Bureau/essai/docs/notify_notion.py \
    --milestone "$MSG"
fi
```

Le hook se déclenche automatiquement après chaque commit contenant "BLOC" dans le message.
