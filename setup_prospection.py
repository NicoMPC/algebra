"""
Setup onglet Prospection dans Google Sheets.
35 lignes pré-remplies : 15×A, 15×B, 5×C
Formule auto : tu tapes le prénom → le message se génère en col E.

Usage : python3 setup_prospection.py
"""
from sheets import sh

SHEET_ID = "1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4"
TAB = "Prospection"

# ── Templates ──
MSG_A = (
    "Salut __NOM__ ! J'ai vu ton annonce pour les cours de maths. "
    "Je suis Nicolas, entrepreneur — j'ai accompagné des dizaines d'élèves en maths ces dernières années. "
    "J'ai créé matheux.fr, un outil d'entraînement quotidien qui complète les cours particuliers : "
    "entre tes séances, tes élèves s'entraînent 10 min/jour sur des exos ciblés sur leurs lacunes. "
    "Toi tu reçois un rapport hebdo pour voir exactement où ils galèrent → tu arrives à ta prochaine séance "
    "en sachant quoi bosser. C'est pas fait pour te remplacer, c'est fait pour que tes élèves progressent "
    "plus vite grâce à toi. Tu voudrais le tester gratuitement et me dire ce que t'en penses ? 🙏"
)

MSG_B = (
    "Hello __NOM__ ! Je suis Nicolas, entrepreneur — j'ai accompagné des dizaines d'élèves en maths ces dernières années "
    "et j'ai créé matheux.fr, un complément aux cours particuliers. "
    "Le principe : entre tes séances, chaque élève reçoit 5 exos personnalisés par jour, adaptés à ses vraies lacunes. "
    "Toi, tu reçois un rapport chaque semaine avec leurs points faibles → tu prépares tes cours en sachant exactement "
    "quoi cibler. Ça remplace pas tes cours, au contraire : les parents voient que leur enfant bosse tous les jours "
    "ET qu'il a un prof qui suit tout. Résultat, ils te gardent plus longtemps. "
    "7 jours gratuits, sans CB. Tu veux jeter un œil ?"
)

MSG_C = (
    "Re __NOM__ ! Content que t'aies pu regarder. Du coup si ça te plaît, je te propose un deal simple : "
    "tu recommandes matheux.fr aux parents de tes élèves comme complément à tes cours. "
    "Chaque élève qui s'abonne, tu touches 10€. T'as 5 élèves qui s'abonnent = 50€ direct. "
    "Je te crée un code perso PROF-__NOM_MAJ__ pour tracker. Ça t'intéresse ?"
)

MSG_D = (
    "Salut __NOM__ ! Je suis Nicolas, entrepreneur — j'ai accompagné des dizaines d'élèves en maths ces dernières années "
    "et j'ai créé matheux.fr, un outil d'entraînement quotidien pour les collégiens "
    "(5 exos perso/jour ciblés sur leurs lacunes). Je te propose un deal simple : "
    "tu recommandes matheux.fr aux parents de tes élèves comme complément à tes cours. "
    "Chaque élève qui s'abonne, tu touches 10€. 5 élèves = 50€ direct. "
    "Les parents voient que leur enfant bosse entre tes séances, toi tu reçois un rapport hebdo "
    "sur leurs points faibles → tout le monde y gagne. Je te crée un code perso PROF-__NOM_MAJ__ pour tracker. "
    "7 jours gratuits pour tester toi-même avant. Ça t'intéresse ?"
)

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

# ── Headers + données (USER_ENTERED pour les formules) ──
HEADERS = ["#", "Prénom", "Plateforme", "Type", "Message", "Date Envoi", "Réponse", "Statut", "Notes",
           "", "TemplateA", "TemplateB", "TemplateC", "TemplateD"]

rows = [HEADERS]

# Ligne 2 : templates stockés en K2, L2, M2 (colonnes cachées)
# On les met sur la première ligne de données, les autres lignes K/L/M restent vides

n = 1
types_plan = ["A"] * 15 + ["B"] * 15 + ["D"] * 5

for i, t in enumerate(types_plan):
    r = i + 2  # numéro de ligne Sheet

    # Formule col E — locale FR (points-virgules)
    NOM = "__NOM__"
    MAJ = "__NOM_MAJ__"
    formula = (
        f'=IF(B{r}="";"";'
        f'SUBSTITUTE(SUBSTITUTE('
        f'IF(D{r}="A";$K$2;IF(D{r}="B";$L$2;IF(D{r}="C";$M$2;IF(D{r}="D";$N$2;""))));'
        f'"{NOM}";B{r});'
        f'"{MAJ}";UPPER(B{r})))'
    )

    # Formule col F (Date Envoi) — auto TODAY quand prénom rempli
    date_formula = f'=IF(B{r}="";"";AUJOURDHUI())'

    # Formule col H (Statut) — auto "✅ Envoyé" quand prénom rempli
    statut_formula = f'=IF(B{r}="";"⏳ À envoyer";"✅ Envoyé")'

    row = [n, "", "LeBonCoin", t, formula, date_formula, "", statut_formula, ""]

    # Première ligne : ajouter les templates en K, L, M
    if i == 0:
        row += ["", MSG_A, MSG_B, MSG_C, MSG_D]

    rows.append(row)
    n += 1

# ── Écrire tout d'un coup (USER_ENTERED pour interpréter les formules) ──
sh._api.values().clear(spreadsheetId=SHEET_ID, range=TAB).execute()
sh._api.values().update(
    spreadsheetId=SHEET_ID,
    range=f"{TAB}!A1",
    valueInputOption="USER_ENTERED",
    body={"values": rows}
).execute()

# ── Récupérer le sheetId de l'onglet Prospection ──
meta = sh._api.get(spreadsheetId=SHEET_ID).execute()
sheet_id = None
for s in meta["sheets"]:
    if s["properties"]["title"] == TAB:
        sheet_id = s["properties"]["sheetId"]
        break

# ── Mise en forme conditionnelle : ligne verte si prénom rempli (col B) ──
if sheet_id is not None:
    sh._api.batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [
            # D'abord supprimer les règles existantes
            {"deleteConditionalFormatRule": {"sheetId": sheet_id, "index": 0}}
        ]}
    ).execute() if False else None  # skip delete, on ajoute direct

    sh._api.batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [{
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{
                        "sheetId": sheet_id,
                        "startRowIndex": 1,   # après header
                        "endRowIndex": 36,
                        "startColumnIndex": 0,  # col A
                        "endColumnIndex": 9     # col I
                    }],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{"userEnteredValue": '=$B2<>""'}]
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
    print("🟢 Mise en forme conditionnelle : ligne verte quand prénom rempli")

print(f"✅ {TAB} : {len(rows)-1} lignes écrites")
print("📋 Tu tapes un prénom en col B → le message apparaît en col E")
print("📊 Split : 15×A (lignes 2-16) | 15×B (lignes 17-31) | 5×D (lignes 32-36)")
print("💡 Tu peux changer le Type (col D) de n'importe quelle ligne — le message s'adapte")
print("🔧 Templates modifiables en K2, L2, M2 (colonnes cachées)")
