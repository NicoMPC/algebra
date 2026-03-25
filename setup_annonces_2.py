"""
Setup onglet Annonces_LBC_2 — 20 nouvelles villes, titres frais, mêmes 3 textes.
Usage : python3 setup_annonces_2.py
"""
from sheets import sh

SHEET_ID = "1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4"
TAB = "Annonces_LBC_2"

# ── 20 nouvelles villes (pas dans le batch 1) ──
VILLES = [
    "Versailles", "Aix-en-Provence", "Nîmes", "Villeurbanne", "Le Havre",
    "Saint-Denis", "Mulhouse", "Avignon", "La Rochelle", "Antibes",
    "Colmar", "Chambéry", "Valence", "Troyes", "Lorient",
    "Saint-Malo", "Bayonne", "Cannes", "Évry", "Cergy",
]

# ── 20 titres frais (différents du batch 1) ──
TITRES = [
    "Maths collège — 10 min/jour pour combler les lacunes",
    "Soutien maths adaptatif — créé par un entrepreneur passionné",
    "Matheux.fr — chaque jour, 5 exos ciblés pour votre enfant",
    "Votre enfant perd pied en maths ? On peut l'aider",
    "Maths 6ème à 3ème — entraînement quotidien personnalisé",
    "Soutien maths en ligne — 7 jours gratuits, sans engagement",
    "Maths : un coaching quotidien adapté au niveau de votre enfant",
    "Prépa brevet maths — 10 min/jour, résultats visibles",
    "Matheux — l'entraînement maths qui s'adapte vraiment",
    "Cours de maths personnalisés — 19,99€/mois tout compris",
    "Maths collège — votre enfant progresse à son rythme",
    "Soutien maths quotidien — plus efficace qu'1h par semaine",
    "Matheux.fr — le complément idéal aux cours de maths",
    "Maths : des exercices ciblés sur les vraies lacunes",
    "Votre enfant mérite un soutien maths adapté — Matheux",
    "Maths 4ème 3ème — exercices personnalisés chaque matin",
    "Soutien scolaire maths — résultats concrets en 2 semaines",
    "Matheux — 5 exos de maths par jour, adaptés à votre enfant",
    "Aide en maths collège — entraînement quotidien en ligne",
    "Maths : arrêtez les exos génériques, passez au sur-mesure",
]

# ── 3 textes (identiques au batch 1) ──
TEXTE_1 = """Votre enfant a du mal en maths ? Il n'est pas seul.

J'ai accompagné des dizaines d'élèves en maths ces dernières années, et j'ai créé Matheux pour résoudre un problème simple : entre les cours, les élèves ne s'entraînent pas assez.

Matheux, c'est un entraînement quotidien de 10 minutes, adapté aux vraies lacunes de votre enfant. Chaque jour, il reçoit 5 exercices ciblés sur ce qu'il ne maîtrise pas encore — pas des exercices génériques, des exercices choisis pour lui.

✅ Programme Éducation Nationale (6ème → 3ème + 1ère Spé)
✅ S'adapte au niveau réel de votre enfant
✅ Vous recevez un suivi de sa progression
✅ Créé par un entrepreneur qui a accompagné des dizaines d'élèves

👉 7 jours gratuits, sans carte bancaire : matheux.fr

Une question ? Contactez-moi directement ici ou par mail."""

TEXTE_2 = """10 minutes par jour. C'est tout ce qu'il faut.

Un cours particulier, c'est bien — mais 1h par semaine ne suffit pas si l'élève ne s'entraîne pas entre les séances. Matheux comble ce vide.

Chaque matin, votre enfant reçoit 5 exercices de maths personnalisés, calibrés sur ses lacunes réelles. Pas de cours vidéo à regarder passivement. Que de la pratique ciblée.

💰 19,99€/mois au lieu de 30-50€/h pour un prof particulier
📱 Accessible sur téléphone, tablette ou ordinateur
📊 Suivi de progression — vous voyez exactement où il en est
🎯 Programme officiel de l'Éducation Nationale

👉 Testez gratuitement pendant 7 jours (sans CB) : matheux.fr"""

TEXTE_3 = """"Mon fils a remonté sa moyenne de 3 points en un mois."

C'est l'objectif de Matheux : des progrès concrets, rapides, visibles.

Comment ça marche ?
1️⃣ Votre enfant s'inscrit et passe un diagnostic rapide
2️⃣ Matheux identifie ses lacunes précises
3️⃣ Chaque jour, 5 exercices ciblés — 10 min chrono
4️⃣ L'outil s'adapte : s'il progresse, la difficulté monte. S'il galère, on renforce.

Ça marche pour les élèves de la 6ème à la 3ème, et en 1ère Spé Maths.

Pas d'engagement, pas de CB pour essayer.
👉 matheux.fr — 7 jours gratuits."""

# 7/7/6 split pour 20 annonces
TEXTES = [TEXTE_1] * 7 + [TEXTE_2] * 7 + [TEXTE_3] * 6
TEXTE_LABELS = ["Texte 1"] * 7 + ["Texte 2"] * 7 + ["Texte 3"] * 6

# ── Créer l'onglet si besoin ──
tabs = sh.list_tabs()
if TAB not in tabs:
    sh._api.batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [{"addSheet": {"properties": {"title": TAB}}}]}
    ).execute()
    print(f"✅ Onglet '{TAB}' créé")
else:
    print(f"ℹ️ Onglet '{TAB}' existe déjà — on écrase")

# ── Construire les lignes ──
HEADERS = ["✅", "#", "Ville", "Titre", "Type", "Texte", "Date"]

rows = [HEADERS]
for i in range(20):
    r = i + 2
    date_formula = f'=IF(A{r};AUJOURDHUI();"")'
    rows.append([
        False,
        i + 1,
        VILLES[i],
        TITRES[i],
        TEXTE_LABELS[i],
        TEXTES[i],
        date_formula,
    ])

# ── Écrire ──
sh._api.values().clear(spreadsheetId=SHEET_ID, range=TAB).execute()
sh._api.values().update(
    spreadsheetId=SHEET_ID,
    range=f"{TAB}!A1",
    valueInputOption="USER_ENTERED",
    body={"values": rows}
).execute()

# ── Sheet ID pour formatting ──
meta = sh._api.get(spreadsheetId=SHEET_ID).execute()
sheet_id = None
for s in meta["sheets"]:
    if s["properties"]["title"] == TAB:
        sheet_id = s["properties"]["sheetId"]
        break

if sheet_id is not None:
    # Checkboxes col A
    sh._api.batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [{
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": 21,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "rule": {
                    "condition": {"type": "BOOLEAN"},
                    "strict": True,
                    "showCustomUi": True
                }
            }
        }]}
    ).execute()
    print("☑️ Checkboxes col A")

    # Ligne verte quand coché
    sh._api.batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [{
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": 21,
                        "startColumnIndex": 0,
                        "endColumnIndex": 7
                    }],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{"userEnteredValue": '=$A2=TRUE'}]
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 0.85,
                                "green": 0.95,
                                "blue": 0.85
                            }
                        }
                    }
                },
                "index": 0
            }
        }]}
    ).execute()
    print("🟢 Ligne verte quand coché")

print(f"✅ {TAB} : 20 annonces prêtes")
print("📋 20 nouvelles villes — aucun doublon avec batch 1")
