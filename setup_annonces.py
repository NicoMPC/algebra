"""
Setup onglet Annonces_LBC dans Google Sheets.
30 annonces prêtes à copier-coller : 10×Texte1, 10×Texte2, 10×Texte3
Chaque ligne = 1 ville + 1 titre + 1 texte complet

Usage : python3 setup_annonces.py
"""
from sheets import sh

SHEET_ID = "1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4"
TAB = "Annonces_LBC"

# ── 30 villes ──
VILLES = [
    "Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux",
    "Nantes", "Lille", "Strasbourg", "Montpellier", "Nice",
    "Rennes", "Grenoble", "Rouen", "Toulon", "Saint-Étienne",
    "Angers", "Dijon", "Brest", "Le Mans", "Clermont-Ferrand",
    "Reims", "Metz", "Orléans", "Amiens", "Limoges",
    "Perpignan", "Caen", "Besançon", "Poitiers", "Pau",
]

# ── 30 titres (variés pour éviter le flag) ──
TITRES = [
    "Maths collège — votre enfant progresse en 10 min/jour",
    "Soutien maths 6ème à 3ème — entraînement quotidien adapté",
    "Matheux — l'appli qui cible les lacunes en maths",
    "Maths : 5 exercices par jour adaptés au niveau de votre enfant",
    "Votre enfant galère en maths ? 10 min/jour suffisent",
    "Soutien scolaire maths — adaptatif, quotidien, 19,99€/mois",
    "Prépa brevet maths — entraînement personnalisé chaque jour",
    "Maths collège : progrès visibles en 2 semaines",
    "Alternative cours particuliers maths — moins cher, tous les jours",
    "Matheux.fr — le soutien maths qui s'adapte à votre enfant",
    "Soutien maths personnalisé — 7 jours gratuits sans CB",
    "Maths 3ème/Brevet — entraînement quotidien ciblé",
    "Votre enfant décroche en maths ? Matheux peut l'aider",
    "Exercices de maths sur mesure — collège et lycée",
    "Maths : un entraînement quotidien qui complète les cours",
    "Soutien maths en ligne — programme Éducation Nationale",
    "Maths 6ème 5ème 4ème 3ème — 5 exos/jour ciblés",
    "Progrès en maths — outil créé par un entrepreneur",
    "Matheux — le coach maths quotidien de votre enfant",
    "Cours de maths en ligne — entraînement adaptatif 10 min/jour",
    "Maths collège — entraînement personnalisé chaque matin",
    "Soutien maths adaptatif — testez 7 jours gratuitement",
    "Votre enfant peut progresser en maths — 10 min/jour",
    "Maths : fini les lacunes — exercices ciblés quotidiens",
    "Matheux.fr — 5 exos de maths personnalisés chaque jour",
    "Soutien maths collège — plus efficace qu'un cours par semaine",
    "Maths : l'entraînement quotidien qui change les notes",
    "Brevet maths — préparez votre enfant avec Matheux",
    "Maths en ligne — adapté aux lacunes réelles de votre enfant",
    "Matheux — progresser en maths sans prof particulier",
]

# ── 3 textes ──
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

TEXTES = [TEXTE_1] * 10 + [TEXTE_2] * 10 + [TEXTE_3] * 10
TEXTE_LABELS = ["Texte 1"] * 10 + ["Texte 2"] * 10 + ["Texte 3"] * 10

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
for i in range(30):
    r = i + 2
    # Checkbox en col A (FALSE par défaut, TRUE quand coché)
    # Date auto en col G quand checkbox cochée
    date_formula = f'=IF(A{r};AUJOURDHUI();"")'
    rows.append([
        False,  # checkbox
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

# ── Mise en forme conditionnelle : ligne verte si publiée ──
meta = sh._api.get(spreadsheetId=SHEET_ID).execute()
sheet_id = None
for s in meta["sheets"]:
    if s["properties"]["title"] == TAB:
        sheet_id = s["properties"]["sheetId"]
        break

if sheet_id is not None:
    # D'abord : checkboxes en col A (lignes 2-31)
    sh._api.batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [{
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": 31,
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
    print("☑️ Checkboxes ajoutées en col A")

    # Ensuite : mise en forme conditionnelle
    sh._api.batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [{
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": 31,
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
    print("🟢 Mise en forme : ligne verte quand ✅ en col F")

print(f"✅ {TAB} : 30 annonces prêtes")
print("📋 Copier-coller : col B (ville) + col C (titre) + col E (texte)")
print("📊 Split : 10×Texte1 (lignes 2-11) | 10×Texte2 (12-21) | 10×Texte3 (22-31)")
print("✅ Quand publiée : mettre ✅ en col F → ligne verte + date auto")
