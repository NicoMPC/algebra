"""
algebreboost — utilitaire Google Sheets API
Lecture et écriture directe dans le Sheet live.

Usage :
  from sheets import sh
  sh.read("Users")                        → liste de dicts
  sh.write_rows("DiagnosticExos", rows)   → remplace tout l'onglet
  sh.append_row("Scores", [v1, v2, ...])  → ajoute une ligne
  sh.update_cell("Users", 2, 3, "val")    → modifie une cellule
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE  = "/home/nicolas/Bureau/algebra live/algebra/algebreboost-sheets-2595a71cadfb.json"
SHEET_ID  = "1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4"
SCOPES    = ["https://www.googleapis.com/auth/spreadsheets"]


class Sheets:
    def __init__(self):
        creds = service_account.Credentials.from_service_account_file(
            KEY_FILE, scopes=SCOPES
        )
        self._svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
        self._api = self._svc.spreadsheets()

    # ── Lecture ─────────────────────────────────────────────────────────────

    def read(self, tab: str) -> list[dict]:
        """Retourne toutes les lignes d'un onglet comme liste de dicts {header: valeur}."""
        res = self._api.values().get(
            spreadsheetId=SHEET_ID, range=tab
        ).execute()
        rows = res.get("values", [])
        if len(rows) < 2:
            return []
        headers = rows[0]
        return [
            {headers[i]: row[i] if i < len(row) else "" for i in range(len(headers))}
            for row in rows[1:]
        ]

    def read_raw(self, tab: str) -> list[list]:
        """Retourne toutes les lignes brutes (liste de listes)."""
        res = self._api.values().get(
            spreadsheetId=SHEET_ID, range=tab
        ).execute()
        return res.get("values", [])

    # ── Écriture ─────────────────────────────────────────────────────────────

    def write_rows(self, tab: str, rows: list[list], include_header: bool = True):
        """
        Remplace tout l'onglet par rows.
        rows[0] doit être les en-têtes si include_header=True.
        """
        self._api.values().clear(
            spreadsheetId=SHEET_ID, range=tab
        ).execute()
        self._api.values().update(
            spreadsheetId=SHEET_ID,
            range=f"{tab}!A1",
            valueInputOption="RAW",
            body={"values": rows}
        ).execute()
        print(f"✅ {tab} mis à jour ({len(rows)-1 if include_header else len(rows)} lignes)")

    def append_row(self, tab: str, row: list):
        """Ajoute une ligne à la fin de l'onglet."""
        self._api.values().append(
            spreadsheetId=SHEET_ID,
            range=f"{tab}!A1",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [row]}
        ).execute()

    def update_cell(self, tab: str, row: int, col: int, value):
        """Met à jour une cellule (row et col en 1-indexé)."""
        col_letter = chr(64 + col)
        self._api.values().update(
            spreadsheetId=SHEET_ID,
            range=f"{tab}!{col_letter}{row}",
            valueInputOption="RAW",
            body={"values": [[value]]}
        ).execute()

    def update_range(self, tab: str, range_a1: str, values: list[list]):
        """Met à jour une plage en notation A1 (ex: 'A2:E10')."""
        self._api.values().update(
            spreadsheetId=SHEET_ID,
            range=f"{tab}!{range_a1}",
            valueInputOption="RAW",
            body={"values": values}
        ).execute()

    # ── Utilitaires ──────────────────────────────────────────────────────────

    def list_tabs(self) -> list[str]:
        """Retourne la liste des onglets."""
        res = self._api.get(spreadsheetId=SHEET_ID).execute()
        return [s["properties"]["title"] for s in res["sheets"]]


# Instance globale — importer et utiliser directement
sh = Sheets()


if __name__ == "__main__":
    print("Onglets :", sh.list_tabs())
    users = sh.read("Users")
    print(f"Users : {len(users)} ligne(s)")
    for u in users:
        print(" ", u.get("Prénom"), u.get("Niveau"))
