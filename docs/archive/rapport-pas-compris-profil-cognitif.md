# Rapport — Bouton "J'ai pas compris" + Profil cognitif @81

**Date** : 15 mars 2026
**Déploiement** : GAS @81 + GitHub push OK

---

## Variables globales réelles utilisées

| Variable spec | Variable réelle | Usage |
|---|---|---|
| `_currentCat` | `cat` (param de `rSection`) | Catégorie exercice |
| `_currentExoIdx` | `idx` (param de `rSection`) | Index exercice |
| `_currentSource` | Déduit de `cat` (`BOOST`→`boost`, sinon `chapitre`) | Source pour Insights |
| `_currentExo` | `data` (param de `rSection`) | Objet exercice |
| `S.code` | `S.prof.code` | Code élève |
| `S.niv` | `S.niv` (correct) | Niveau |

---

## Champ `draft` dans exosList

**Statut** : **AJOUTÉ** — `r['Draft']` lu dans le mapping des scores de `getAdminOverview` (backend.js).
Colonne L (Draft) du schéma Scores est maintenant incluse dans chaque entrée de `exosList`.

---

## Fonctions modifiées — index.html

| Fonction | Lignes (approx.) | Modification |
|---|---|---|
| `_MSGS` | ~2130 | Ajout clé `pas_compris` (6 niveaux × 3 messages) |
| `rSection()` | ~6267-6270 | Bouton "J'ai pas compris" (cas `scored && !catDone`) |
| `rSection()` | ~6347-6349 | Bouton "J'ai pas compris" (cas `catDone && scored`) |
| `copyAdminPrompt()` | ~7921-7956 | Section PROFIL COGNITIF + POINTS FAIBLES + INCOMPRÉHENSIONS |
| `_buildModalHTML()` | ~9391-9430 | Accordéon "Profil cognitif" (comportement, weakPoints, vélocité, brevet) |

## Fonctions créées — index.html

| Fonction | Lignes (approx.) | Rôle |
|---|---|---|
| `_handlePasCompris(cat, idx, exoQ)` | ~6192 | Gestionnaire clic : masque, sessionStorage, toast, fetch fire-and-forget |
| `_pcMetric(val, label, note)` | ~6828 | Helper HTML pour métriques comportement (grille 2×2) |

## Fonctions créées — backend.js

| Fonction | Lignes (approx.) | Rôle |
|---|---|---|
| `logPasCompris(p)` | ~3943 | Écrit dans Insights (type `pas_compris`, schéma respecté) |

## Fonctions modifiées — backend.js

| Fonction | Lignes (approx.) | Modification |
|---|---|---|
| `doPost()` | ~116 | Ajout case `log_pas_compris` |
| `getAdminOverview()` | ~2981 | Ajout `draft` dans mapping scores |
| `getAdminOverview()` | ~2941 | Filter insightsBySess inclut `pas_compris` |
| `getAdminOverview()` | ~3433-3530 | Calcul `profilCognitif` (erreursByChap, comportement, vélocité, weakPoints, predictionBrevet) |
| `getAdminOverview()` | ~3577 | Ajout `profilCognitif` dans objet student retourné |

---

## Aucune régression

- Scoring / streak / progression : **non touchés**
- Admin cockpit existant : **intact** (profil cognitif en accordéon séparé)
- Schéma Insights : **aucune colonne ajoutée** (type `pas_compris` utilise les colonnes existantes)
- CORS : **pas de Content-Type header** dans le fetch

---

## Commandes de déploiement (exécutées)

```bash
cd "/home/nicolas/Bureau/algebra live/algebra"
./deploy.sh "feat: log_pas_compris + profilCognitif @81"   # ✅ Deployed @81
git add index.html backend.js docs/database.md CLAUDE.md
git commit -m "feat: bouton pas compris + profil cognitif fiche admin @81"
git push origin main                                        # ✅ Pushed
```
