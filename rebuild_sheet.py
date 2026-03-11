#!/usr/bin/env python3
"""
rebuild_sheet.py — Recrée les onglets admin "👁 Suivi" et "📋 Historique"
à partir des données réelles du Sheet.

Run une fois pour configurer la structure, puis à la demande pour resynchroniser.

Tâches :
  1. Renommer Dashboard/Vue Élèves → "👁 Suivi", Log Exercices → "📋 Historique"
  2. Écrire les bons headers
  3. Réordonner tous les onglets
  4. Colorier les onglets (bleu = Nicolas, gris = GAS-only)
  5. Formatter "👁 Suivi" (freeze, masquer col Q, CF, largeurs)
  6. Formatter "📋 Historique" (freeze row 1, largeurs)
  7. Reconstruire "👁 Suivi" depuis données réelles
  8. Reconstruire "📋 Historique" depuis Scores + Curriculum_Officiel
"""

import sys
import json
from datetime import date, timedelta, datetime

sys.path.insert(0, '/home/nicolas/Bureau/algebra live/algebra')
from sheets import sh

SHEET_ID = "1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4"

TAB_SUIVI      = "👁 Suivi"
TAB_HISTORIQUE = "📋 Historique"

# ── Helpers API ───────────────────────────────────────────────────────────────

def get_sheet_metadata() -> dict:
    meta = sh._api.get(spreadsheetId=SHEET_ID).execute()
    return {s["properties"]["title"]: s["properties"] for s in meta["sheets"]}


def tab_ref(name: str, rng: str) -> str:
    if ' ' in name or "'" in name or any(ord(c) > 127 for c in name):
        safe = name.replace("'", "\\'")
        return f"'{safe}'!{rng}"
    return f"{name}!{rng}"


def write_to_tab(tab: str, rng: str, values: list):
    sh._api.values().update(
        spreadsheetId=SHEET_ID,
        range=tab_ref(tab, rng),
        valueInputOption="RAW",
        body={"values": values}
    ).execute()


def clear_tab(tab: str):
    sh._api.values().clear(
        spreadsheetId=SHEET_ID,
        range=tab_ref(tab, "A:Z")
    ).execute()


def today_str() -> str:
    return date.today().strftime("%Y-%m-%d")


def days_since(d_str: str) -> int:
    if not d_str:
        return 999
    try:
        d = datetime.strptime(d_str[:10], "%Y-%m-%d").date()
        delta = date.today() - d
        return max(0, delta.days)
    except Exception:
        return 999


# ════════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 1 — Renommer / créer les onglets
# ════════════════════════════════════════════════════════════════════════════════

# Anciens noms possibles → nouveau nom
RENAMES = {
    "Dashboard":    TAB_SUIVI,
    "Vue Élèves":   TAB_SUIVI,
    "Log Exercices": TAB_HISTORIQUE,
}


def step1_rename_create():
    print("\n── Étape 1 : Renommer / créer ──")
    sheets = get_sheet_metadata()
    requests = []

    for old, new in RENAMES.items():
        if old in sheets and new not in sheets:
            requests.append({
                "updateSheetProperties": {
                    "properties": {"sheetId": sheets[old]["sheetId"], "title": new},
                    "fields": "title"
                }
            })
            print(f"  {old} → {new}")

    if TAB_SUIVI not in sheets and not any(old in sheets for old in ("Dashboard", "Vue Élèves")):
        requests.append({"addSheet": {"properties": {"title": TAB_SUIVI}}})
        print(f"  Création {TAB_SUIVI}")

    if TAB_HISTORIQUE not in sheets and "Log Exercices" not in sheets:
        requests.append({"addSheet": {"properties": {"title": TAB_HISTORIQUE}}})
        print(f"  Création {TAB_HISTORIQUE}")

    if requests:
        sh._api.batchUpdate(spreadsheetId=SHEET_ID, body={"requests": requests}).execute()
    print("✅ Onglets prêts")


# ════════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 2 — Headers
# ════════════════════════════════════════════════════════════════════════════════

SUIVI_HEADERS = [
    "⚡ ACTION",                                            # A — règle du jour pour Nicolas
    "Prénom", "Niveau", "Dernière connexion",              # B C D
    "Chapitre 1", "Résumé Ch1", "→ Nouveau Ch1",           # E F G  ← Nicolas colle JSON ici
    "Chapitre 2", "Résumé Ch2", "→ Nouveau Ch2",           # H I J
    "Chapitre 3", "Résumé Ch3", "→ Nouveau Ch3",           # K L M
    "Chapitre 4", "Résumé Ch4", "→ Nouveau Ch4",           # N O P
    "Boost actuel", "Résumé Boost", "→ Nouveau Boost",     # Q R S  ← Nicolas colle JSON ici
    "📧 Rapport envoyé",                                    # T
    "Code"                                                  # U — masquée
]

HISTORIQUE_HEADERS = [
    "Date", "Prénom", "Niveau", "Chapitre", "Énoncé",
    "Résultat", "Temps (s)", "Indices", "Formule vue", "Mauvaise option"
]


def step2_headers():
    print("\n── Étape 2 : Headers ──")
    sheets = get_sheet_metadata()
    for tab, headers in [(TAB_SUIVI, SUIVI_HEADERS), (TAB_HISTORIQUE, HISTORIQUE_HEADERS)]:
        if tab in sheets:
            sh._api.values().clear(
                spreadsheetId=SHEET_ID, range=tab_ref(tab, "A1:Z1")
            ).execute()
            col_end = chr(64 + len(headers))
            write_to_tab(tab, f"A1:{col_end}1", [headers])
    print("✅ Headers écrits")


# ════════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 3 — Réordonner les onglets
# ════════════════════════════════════════════════════════════════════════════════

TARGET_ORDER = [
    TAB_SUIVI,
    TAB_HISTORIQUE,
    "Users",
    "Progress",
    "DailyBoosts",
    "Curriculum_Officiel",
    "DiagnosticExos",
    "Scores",
    "RemediationChapters",
]


def step3_reorder():
    print("\n── Étape 3 : Réordonnement ──")
    sheets = get_sheet_metadata()
    for i, name in enumerate(TARGET_ORDER):
        if name in sheets:
            sh._api.batchUpdate(spreadsheetId=SHEET_ID, body={
                "requests": [{
                    "updateSheetProperties": {
                        "properties": {"sheetId": sheets[name]["sheetId"], "index": i},
                        "fields": "index"
                    }
                }]
            }).execute()
    print("✅ Onglets réordonnés")


# ════════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 4 — Couleurs des onglets
# ════════════════════════════════════════════════════════════════════════════════

NICOLAS_TABS = {TAB_SUIVI, TAB_HISTORIQUE, "Users"}
GAS_TABS = {"Progress", "DailyBoosts", "Curriculum_Officiel",
            "DiagnosticExos", "Scores", "RemediationChapters"}

BLUE_TAB = {"red": 0.27, "green": 0.51, "blue": 0.71}
GRAY_TAB = {"red": 0.75, "green": 0.75, "blue": 0.75}


def step4_tab_colors():
    print("\n── Étape 4 : Couleurs onglets ──")
    sheets = get_sheet_metadata()
    requests = []
    for name, color in [(t, BLUE_TAB) for t in NICOLAS_TABS] + [(t, GRAY_TAB) for t in GAS_TABS]:
        if name in sheets:
            requests.append({
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheets[name]["sheetId"],
                        "tabColorStyle": {"rgbColor": color}
                    },
                    "fields": "tabColorStyle"
                }
            })
    sh._api.batchUpdate(spreadsheetId=SHEET_ID, body={"requests": requests}).execute()
    print("✅ Couleurs (bleu = Nicolas, gris = GAS)")


# ════════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 5 — Mise en forme 👁 Suivi
#   - Freeze row 1 + col A
#   - Masquer col Q (index 16 = Code)
#   - Header gras + fond gris clair
#   - Col A large (290px)
#   - CF : rouge si 🔴, jaune si 🟡/🆕, gris si inactif > 3j
# ════════════════════════════════════════════════════════════════════════════════

def step5_format_suivi():
    print("\n── Étape 5 : Mise en forme 👁 Suivi ──")
    sheets = get_sheet_metadata()
    if TAB_SUIVI not in sheets:
        print("  ⚠️  Onglet introuvable — saut")
        return
    sid = sheets[TAB_SUIVI]["sheetId"]

    # Nouvelle structure : A=ACTION, G/J/M/P=→Nouveau ChN (0-based: 6,9,12,15), S=→Nouveau Boost (0-based: 18)
    # Couleurs colonnes Nicolas (→Nouveau) : fond vert pâle pour signaler que c'est là qu'on colle
    nicolas_cols = [6, 9, 12, 15, 18]  # G, J, M, P, S (0-based)

    requests = [
        # Freeze row 1 uniquement (plus de col A gelée : Prénom, pas ACTION)
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sid,
                    "gridProperties": {"frozenRowCount": 1, "frozenColumnCount": 0}
                },
                "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"
            }
        },
        # Masquer col U (index 20 = Code)
        {
            "updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": 20, "endIndex": 21},
                "properties": {"hiddenByUser": True},
                "fields": "hiddenByUser"
            }
        },
        # Header gras + fond gris clair
        {
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.88, "green": 0.88, "blue": 0.88}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Largeur col A (ACTION) : 250px
        {
            "updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
                "properties": {"pixelSize": 250},
                "fields": "pixelSize"
            }
        },
        # Largeur cols Résumé (F=5, I=8, L=11, O=14, R=17) : 250px (JSON lisible)
        *[{
            "updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "COLUMNS",
                          "startIndex": col_idx, "endIndex": col_idx + 1},
                "properties": {"pixelSize": 250},
                "fields": "pixelSize"
            }
        } for col_idx in [5, 8, 11, 14, 17]],
        # Fond vert très pâle sur cols →Nouveau (G=6, J=9, M=12, P=15, S=18)
        # pour distinguer visuellement les colonnes où Nicolas colle
        *[{
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": 1,
                          "startColumnIndex": col_idx, "endColumnIndex": col_idx + 1},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.90, "green": 0.97, "blue": 0.90}
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        } for col_idx in nicolas_cols],
    ]

    sh._api.batchUpdate(spreadsheetId=SHEET_ID, body={"requests": requests}).execute()
    print("✅ Mise en forme 👁 Suivi")


# ════════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 6 — Mise en forme 📋 Historique
# ════════════════════════════════════════════════════════════════════════════════

def step6_format_historique():
    print("\n── Étape 6 : Mise en forme 📋 Historique ──")
    sheets = get_sheet_metadata()
    if TAB_HISTORIQUE not in sheets:
        print("  ⚠️  Onglet introuvable — saut")
        return
    sid = sheets[TAB_HISTORIQUE]["sheetId"]

    requests = [
        # Freeze row 1
        {
            "updateSheetProperties": {
                "properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 1}},
                "fields": "gridProperties.frozenRowCount"
            }
        },
        # Header gras + fond gris clair
        {
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.88, "green": 0.88, "blue": 0.88}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Largeur col E (Énoncé) : 300px
        {
            "updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5},
                "properties": {"pixelSize": 300},
                "fields": "pixelSize"
            }
        },
        # CF : fond rouge pâle si HARD
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sid, "startRowIndex": 1}],
                    "booleanRule": {
                        "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "HARD"}]},
                        "format": {"backgroundColor": {"red": 1.0, "green": 0.85, "blue": 0.85}}
                    }
                },
                "index": 0
            }
        },
    ]
    sh._api.batchUpdate(spreadsheetId=SHEET_ID, body={"requests": requests}).execute()
    print("✅ Mise en forme 📋 Historique")


# ════════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 7 — Reconstruire 👁 Suivi depuis données réelles
# ════════════════════════════════════════════════════════════════════════════════

def build_chapter_summary(cat: str, niveau: str, cat_scores: list) -> str:
    """Génère le JSON résumé d'un chapitre pour DeepSeek."""
    if not cat_scores:
        return ""
    total = len(cat_scores)
    easy  = [r for r in cat_scores if r.get("Résultat") == "EASY"]
    hard  = [r for r in cat_scores if r.get("Résultat") == "HARD"]
    taux  = round(len(easy) / total * 100) if total else 0

    # Temps moyen (exclure 0)
    temps_vals = [int(r.get("Temps(sec)", 0) or 0) for r in cat_scores if int(r.get("Temps(sec)", 0) or 0) > 0]
    temps_moyen = round(sum(temps_vals) / len(temps_vals)) if temps_vals else 0

    # % d'exos avec indices
    avec_indices = sum(1 for r in cat_scores if int(r.get("NbIndices", 0) or 0) > 0)
    indices_pourcent = round(avec_indices / total * 100) if total else 0

    # Erreurs fréquentes (top 3 MauvaiseOption)
    wrong_opts: dict = {}
    for r in cat_scores:
        w = str(r.get("MauvaiseOption", "")).strip()
        if w:
            wrong_opts[w] = wrong_opts.get(w, 0) + 1
    erreurs_frequentes = sorted(wrong_opts.items(), key=lambda x: -x[1])[:3]

    # Dernière session
    dates = [str(r.get("Date", "")) for r in cat_scores if r.get("Date")]
    derniere_session = max(dates) if dates else ""

    erreurs = []
    for r in hard[-5:]:
        enonce = str(r.get("Énoncé", ""))[:80]
        if enonce:
            erreurs.append({
                "enonce": enonce,
                "mauvaise_reponse": str(r.get("MauvaiseOption", "")),
                "indices_vus": int(r.get("NbIndices", 0) or 0),
                "formule_vue": bool(r.get("FormuleVue"))
            })

    seen, reussites = set(), []
    for r in easy:
        q = str(r.get("Énoncé", ""))[:60]
        if q and q not in seen:
            seen.add(q); reussites.append(q)

    try:
        return json.dumps({
            "chapitre": cat, "niveau": niveau,
            "exos_faits": total, "taux_reussite": f"{taux}%",
            "temps_moyen_sec": temps_moyen,
            "indices_pourcent": f"{indices_pourcent}%",
            "erreurs_frequentes": [{"option": k, "fois": v} for k, v in erreurs_frequentes],
            "derniere_session": derniere_session,
            "erreurs": erreurs, "reussites": reussites[:3]
        }, ensure_ascii=False)
    except Exception:
        return ""


def build_boost_summary(boost_scores: list) -> str:
    """Génère le JSON résumé du boost pour DeepSeek."""
    if not boost_scores:
        return ""
    total = len(boost_scores)
    easy  = [r for r in boost_scores if r.get("Résultat") == "EASY"]
    hard  = [r for r in boost_scores if r.get("Résultat") == "HARD"]

    # Temps moyen
    temps_vals = [int(r.get("Temps(sec)", 0) or 0) for r in boost_scores if int(r.get("Temps(sec)", 0) or 0) > 0]
    temps_moyen = round(sum(temps_vals) / len(temps_vals)) if temps_vals else 0

    # % avec indices
    avec_indices = sum(1 for r in boost_scores if int(r.get("NbIndices", 0) or 0) > 0)
    indices_pourcent = round(avec_indices / total * 100) if total else 0

    # Erreurs fréquentes top 3
    wrong_opts: dict = {}
    for r in boost_scores:
        w = str(r.get("MauvaiseOption", "")).strip()
        if w:
            wrong_opts[w] = wrong_opts.get(w, 0) + 1
    erreurs_frequentes = sorted(wrong_opts.items(), key=lambda x: -x[1])[:3]

    erreurs = []
    for r in hard[-5:]:
        enonce = str(r.get("Énoncé", ""))[:80]
        if enonce:
            erreurs.append({
                "enonce": enonce,
                "mauvaise_reponse": str(r.get("MauvaiseOption", "")),
                "indices_vus": int(r.get("NbIndices", 0) or 0)
            })

    try:
        return json.dumps({
            "boost_date": today_str(),
            "exos_faits": total,
            "taux_reussite": f"{round(len(easy)/total*100)}%" if total else "—",
            "temps_moyen_sec": temps_moyen,
            "indices_pourcent": f"{indices_pourcent}%",
            "erreurs_frequentes": [{"option": k, "fois": v} for k, v in erreurs_frequentes],
            "erreurs": erreurs,
            "reussites": [str(r.get("Énoncé",""))[:60] for r in easy[:3] if r.get("Énoncé")]
        }, ensure_ascii=False)
    except Exception:
        return ""


def step7_rebuild_suivi():
    print("\n── Étape 7 : Reconstruire 👁 Suivi ──")
    today = today_str()

    # Charger les données source
    users_rows  = sh.read("Users")
    scores_rows = sh.read("Scores")

    # Indexer scores par code
    scores_by_code = {}
    for r in scores_rows:
        c = r.get("Code", "")
        if c:
            scores_by_code.setdefault(c, []).append(r)

    # Lire les colonnes Nicolas existantes (nouvelle structure 0-based)
    # →Ch1=5, →Ch2=8, →Ch3=11, →Ch4=14, →Boost=17, Rapport=18, Code=19
    existing_nicolas = {}
    try:
        raw = sh.read_raw(TAB_SUIVI)
        for row in raw[1:]:
            if len(row) >= 21:
                code_val = str(row[20])
                existing_nicolas[code_val] = {
                    "new_ch1":   str(row[6])  if len(row) > 6  else "",
                    "new_ch2":   str(row[9])  if len(row) > 9  else "",
                    "new_ch3":   str(row[12]) if len(row) > 12 else "",
                    "new_ch4":   str(row[15]) if len(row) > 15 else "",
                    "new_boost": str(row[18]) if len(row) > 18 else "",
                    "rapport":   str(row[19]) if len(row) > 19 else "",
                }
    except Exception:
        pass

    rows_out = [SUIVI_HEADERS]

    for user in users_rows:
        code   = str(user.get("Code", ""))
        prenom = str(user.get("Prénom", ""))
        niveau = str(user.get("Niveau", ""))

        scores = scores_by_code.get(code, [])

        # Dernière activité
        dates     = sorted([r.get("Date", "") for r in scores if r.get("Date")])
        last_date = dates[-1] if dates else ""

        # Chapitres dans l'ordre de première apparition (sans CALIBRAGE ni BOOST)
        chap_count  = {}
        chap_first  = {}
        chap_scores = {}  # cat → [score rows]
        for r in scores:
            cat = r.get("Chapitre", "")
            d   = r.get("Date", "")
            if not cat or cat in ("CALIBRAGE", "BOOST"):
                continue
            chap_count[cat]  = chap_count.get(cat, 0) + 1
            chap_scores.setdefault(cat, []).append(r)
            if cat not in chap_first or d < chap_first[cat]:
                chap_first[cat] = d
        chap_order = sorted(chap_count.keys(), key=lambda c: chap_first.get(c, ""))

        # Boost : compter exos BOOST aujourd'hui
        boost_today_scores = [r for r in scores
                              if r.get("Chapitre") == "BOOST" and r.get("Date") == today]
        boost_today_done   = len(boost_today_scores)
        boost_consumed     = boost_today_done >= 5

        if boost_consumed:
            boost_actuel = f"Consommé ✅ ({boost_today_done}/5)"
        elif boost_today_done > 0:
            boost_actuel = f"En cours ({boost_today_done}/5)"
        else:
            boost_actuel = "—"

        # Récupérer les colonnes Nicolas existantes (→Nouveau)
        nic        = existing_nicolas.get(code, {})
        new_ch1    = nic.get("new_ch1",   "")
        new_ch2    = nic.get("new_ch2",   "")
        new_ch3    = nic.get("new_ch3",   "")
        new_ch4    = nic.get("new_ch4",   "")
        new_boost  = nic.get("new_boost", "")
        rapport    = nic.get("rapport",   "")

        # Chapitres 5+ → col S si rapport vide
        extra_chaps = chap_order[4:]
        if extra_chaps and not rapport:
            rapport = "Chap+: " + ", ".join(
                f"{c}({chap_count.get(c,0)})" for c in extra_chaps
            )

        chaps    = chap_order[:4]
        new_cols = [new_ch1, new_ch2, new_ch3, new_ch4]
        while len(chaps) < 4:
            chaps.append("")

        # Résumés JSON par chapitre
        resumes = [
            build_chapter_summary(cat, niveau, chap_scores.get(cat, []))
            if cat else ""
            for cat in chaps
        ]
        resume_boost = build_boost_summary(boost_today_scores)

        # Calcul ACTION (4 règles, ordre strict)
        total_scores_non_calib = sum(
            1 for r in scores if r.get("Chapitre") not in ("CALIBRAGE",)
        )
        boost_rows = sh.read("DailyBoosts")
        all_user_boosts = [r for r in boost_rows if str(r.get("Code","")) == code]
        last_boost_date = max((str(r.get("Date","")) for r in all_user_boosts), default="")
        chap_termine_sans_suite = any(
            chap_count.get(c, 0) >= 20 and not new_cols[i]
            for i, c in enumerate(chaps) if c
        )
        if total_scores_non_calib > 0 and len(all_user_boosts) == 0:
            action = "🔴 DIAGNOSTIC FAIT → préparer boost 1"
        elif len(all_user_boosts) >= 1 and last_boost_date < today and not new_boost:
            action = "🆕 BOOST TERMINÉ → préparer boost suivant"
        elif chap_termine_sans_suite:
            action = "✅ CHAPITRE TERMINÉ → assigner suite"
        else:
            action = "👍 RAS"

        rows_out.append([
            action,                                                # A ⚡ ACTION
            prenom, niveau, last_date,                             # B C D
            chaps[0], resumes[0], new_cols[0],                    # E F G
            chaps[1], resumes[1], new_cols[1],                    # H I J
            chaps[2], resumes[2], new_cols[2],                    # K L M
            chaps[3], resumes[3], new_cols[3],                    # N O P
            boost_actuel, resume_boost, new_boost,                # Q R S
            rapport,                                              # T
            code                                                  # U (masquée)
        ])

    # Effacer et réécrire
    sh._api.values().clear(
        spreadsheetId=SHEET_ID, range=tab_ref(TAB_SUIVI, "A1:U1000")
    ).execute()
    write_to_tab(TAB_SUIVI, "A1", rows_out)
    print(f"✅ 👁 Suivi : {len(rows_out) - 1} élève(s)")


# ════════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 8 — Reconstruire 📋 Historique depuis Scores + Curriculum_Officiel
# ════════════════════════════════════════════════════════════════════════════════

def step8_rebuild_historique():
    print("\n── Étape 8 : Reconstruire 📋 Historique ──")

    # Index Curriculum_Officiel : (NIVEAU, Categorie) → liste d'exos
    curriculum_index = {}
    for r in sh.read("Curriculum_Officiel"):
        key = (str(r.get("Niveau", "")).upper(), str(r.get("Categorie", "")))
        try:
            curriculum_index[key] = json.loads(r.get("ExosJSON", "[]"))
        except Exception:
            curriculum_index[key] = []

    def get_enonce(level: str, categorie: str, exo_idx) -> str:
        key = (str(level).upper(), str(categorie))
        exos = curriculum_index.get(key, [])
        try:
            idx = int(exo_idx) - 1
            if 0 <= idx < len(exos):
                return str(exos[idx].get("q", ""))[:60]
        except Exception:
            pass
        return ""

    scores_rows = sh.read("Scores")
    # Trier par date décroissante (plus récent en haut)
    scores_sorted = sorted(scores_rows, key=lambda r: r.get("Date", ""), reverse=True)

    rows_out = [HISTORIQUE_HEADERS]
    for r in scores_sorted[:500]:  # cap à 500 lignes
        enonce = get_enonce(r.get("Niveau", ""), r.get("Chapitre", ""), r.get("NumExo", 0))
        rows_out.append([
            str(r.get("Date",        "")),
            str(r.get("Prénom",      "")),
            str(r.get("Niveau",      "")),
            str(r.get("Chapitre",    "")),
            enonce,
            str(r.get("Résultat",    "")),
            str(r.get("Temps(sec)",  "")),
            str(r.get("NbIndices",   "")),
            "oui" if r.get("FormuleVue") else "non",
            str(r.get("MauvaiseOption", ""))
        ])

    sh._api.values().clear(
        spreadsheetId=SHEET_ID, range=tab_ref(TAB_HISTORIQUE, "A1:J2000")
    ).execute()
    write_to_tab(TAB_HISTORIQUE, "A1", rows_out)
    print(f"✅ 📋 Historique : {len(rows_out) - 1} ligne(s)")


# ════════════════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    step1_rename_create()
    step2_headers()
    step3_reorder()
    step4_tab_colors()
    step5_format_suivi()
    step6_format_historique()
    step7_rebuild_suivi()
    step8_rebuild_historique()
    print("\n🎉 Sheet admin reconstruit.")
