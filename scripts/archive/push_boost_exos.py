#!/usr/bin/env python3
"""Push boost exercises to BoostExos Google Sheet tab."""
import json, sys
sys.path.insert(0, '/home/nicolas/Bureau/algebra live/algebra')

SHEET_ID = "1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4"

with open("/home/nicolas/Bureau/algebra live/algebra/boost_exos.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = [["Niveau", "Categorie", "ExosJSON"]]
for niveau, cats in data.items():
    for cat_name, exos in cats.items():
        rows.append([niveau, cat_name, json.dumps(exos, ensure_ascii=False)])

from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    "/home/nicolas/Bureau/algebra live/algebra/algebreboost-sheets-2595a71cadfb.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
api = svc.spreadsheets()

# Create tab if needed
try:
    api.batchUpdate(spreadsheetId=SHEET_ID, body={
        "requests": [{"addSheet": {"properties": {"title": "BoostExos"}}}]
    }).execute()
    print("✅ Onglet BoostExos créé")
except Exception as e:
    if "already exists" in str(e):
        print("ℹ️  Onglet BoostExos existe déjà")
    else:
        raise

# Clear and write
api.values().clear(spreadsheetId=SHEET_ID, range="BoostExos!A:Z").execute()
api.values().update(
    spreadsheetId=SHEET_ID,
    range="BoostExos!A1",
    valueInputOption="RAW",
    body={"values": rows}
).execute()
print(f"✅ {len(rows)-1} lignes poussées dans BoostExos")
