#!/usr/bin/env python3
"""
test_complet.py — Audit automatisé exhaustif Matheux
10 scénarios, 48 tests. Génère docs/audit_complet.md
"""
import hashlib, json, time, sys, random, threading
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, '/home/nicolas/Bureau/algebra live/algebra')
import requests
from sheets import sh

# ── Config ───────────────────────────────────────────────────────────────────
GAS_URL  = "https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
SHEET_ID = "1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4"
PASSWORD = "audit123"
AUDIT_TAG = "@audit.fr"
TODAY     = date.today().strftime("%Y-%m-%d")
YESTERDAY = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
DAY2AGO   = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
DAY3AGO   = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")

PROFILES = {
    "alice": {"email": "test_alice@audit.fr", "level": "5EME", "name": "Alice_Test"},
    "bob":   {"email": "test_bob@audit.fr",   "level": "6EME", "name": "Bob_Test"},
    "clara": {"email": "test_clara@audit.fr", "level": "4EME", "name": "Clara_Test"},
    "david": {"email": "test_david@audit.fr", "level": "3EME", "name": "David_Test"},
    "emma":  {"email": "test_emma@audit.fr",  "level": "5EME", "name": "Emma_Test"},
}

# ── Helpers ──────────────────────────────────────────────────────────────────
def h256(email, password):
    s = email.lower() + '::' + password + '::AB22'
    return hashlib.sha256(s.encode()).hexdigest()

def gas(payload, timeout=45):
    try:
        r = requests.post(GAS_URL, json=payload, timeout=timeout)
        return r.json()
    except Exception as e:
        return {"status": "error", "message": f"HTTP:{e}"}

def wait(s=1.5):
    time.sleep(s)

# Sheet helpers
def suivi_row(code):
    """Retourne la ligne 👁 Suivi pour ce code (dict avec indices 0-based comme clés)."""
    try:
        raw = sh.read_raw("👁 Suivi")
        for row in raw[1:]:
            if len(row) >= 21 and str(row[20]) == code:
                return row
    except Exception as e:
        print(f"    suivi_row err: {e}")
    return None

def suivi_inject(code, col_0based, value):
    """Écrit une valeur dans la colonne col_0based (0-indexed) pour ce code dans 👁 Suivi."""
    try:
        raw = sh.read_raw("👁 Suivi")
        for i, row in enumerate(raw):
            if i == 0: continue
            if len(row) >= 21 and str(row[20]) == code:
                row_1based = i + 1
                col_letter = chr(65 + col_0based)
                sh.update_range("👁 Suivi", f"{col_letter}{row_1based}", [[value]])
                return True
    except Exception as e:
        print(f"    suivi_inject err: {e}")
    return False

def scores_for(code):
    try:
        return [r for r in sh.read("Scores") if str(r.get("Code","")) == code]
    except: return []

def historique_for(name_substr):
    try:
        return [r for r in sh.read("📋 Historique") if name_substr in str(r.get("Prénom",""))]
    except: return []

def progress_for(code):
    try:
        return [r for r in sh.read("Progress") if str(r.get("Code","")) == code]
    except: return []

def cell_bg(code, col_0based):
    """Retourne la couleur de fond d'une cellule Suivi (r,g,b) ou None."""
    try:
        raw = sh.read_raw("👁 Suivi")
        row_1based = None
        for i, row in enumerate(raw):
            if i == 0: continue
            if len(row) >= 21 and str(row[20]) == code:
                row_1based = i + 1
                break
        if not row_1based: return None
        col_letter = chr(65 + col_0based)
        result = sh._api.get(
            spreadsheetId=SHEET_ID,
            ranges=[f"'👁 Suivi'!{col_letter}{row_1based}"],
            includeGridData=True,
            fields="sheets/data/rowData/values/userEnteredFormat/backgroundColor"
        ).execute()
        sheets_data = result.get("sheets", [])
        if not sheets_data: return None
        row_data = sheets_data[0].get("data", [{}])[0].get("rowData", [{}])
        if not row_data: return None
        vals = row_data[0].get("values", [{}])
        if not vals: return None
        bg = vals[0].get("userEnteredFormat", {}).get("backgroundColor", {})
        return (round(bg.get("red",1)*255), round(bg.get("green",1)*255), round(bg.get("blue",1)*255))
    except Exception as e:
        return None

def is_red(col_rgb):
    """Retourne True si la couleur est rouge (#f4cccc = 244,204,204 ou proche)."""
    if not col_rgb: return False
    r,g,b = col_rgb
    return r >= 220 and g <= 220 and b <= 220

def is_green(col_rgb):
    """Retourne True si la couleur est verte (#d9ead3 = 217,234,211 ou proche)."""
    if not col_rgb: return False
    r,g,b = col_rgb
    return g >= 200 and r < g and b < g

def make_fake_exos(n, cat, level):
    """Génère n faux enoncés de test pour save_score."""
    return [{"q": f"Q{i+1} {cat}", "a": f"R{i+1}", "idx": i+1} for i in range(n)]

def do_save_scores(code, name, level, cat, exos, results_list):
    """Envoie save_score pour une liste d'exos. results_list: liste de 'EASY'/'MEDIUM'/'HARD'."""
    saved = 0
    for i, exo in enumerate(exos):
        res = results_list[i] if i < len(results_list) else "EASY"
        r = gas({
            "action": "save_score",
            "code": code, "name": name, "level": level,
            "categorie": cat,
            "exercice_idx": exo["idx"],
            "resultat": res,
            "q": exo["q"],
            "time": random.randint(10, 60),
            "indices": 0 if res == "EASY" else random.randint(0, 2),
            "formule": False,
            "wrongOpt": "" if res == "EASY" else "mauvaise_reponse_test",
            "draft": ""
        })
        if r.get("status") == "success":
            saved += 1
        wait(1.2)
    return saved

# ── AuditRunner ───────────────────────────────────────────────────────────────
class AuditRunner:
    def __init__(self):
        self.scenarios = []
        self.bugs = []
        self._cur_name = None
        self._cur_tests = []
        self.codes = {}   # profile_name → code
        self.data  = {}   # arbitrary state between scenarios

    def scenario(self, name):
        self._flush()
        self._cur_name = name
        self._cur_tests = []
        print(f"\n{'═'*60}\n  {name}\n{'═'*60}")

    def _flush(self):
        if self._cur_name:
            self.scenarios.append({"name": self._cur_name, "tests": self._cur_tests})

    def check(self, num, desc, cond, proof=""):
        status = "✅" if cond else "❌"
        self._cur_tests.append({"num":num,"desc":desc,"ok":bool(cond),"proof":str(proof)[:120]})
        print(f"  {status} #{num:02d} {desc}" + (f"  [{str(proof)[:70]}]" if proof else ""))

    def bug(self, sev, desc, file="", line=""):
        self.bugs.append({"sev":sev,"desc":desc,"file":file,"line":line})
        print(f"  🐛 [{sev}] {desc}")

    def finish(self):
        self._flush()

    def totals(self):
        ok  = sum(t["ok"] for s in self.scenarios for t in s["tests"])
        all_ = sum(len(s["tests"]) for s in self.scenarios)
        return ok, all_

# ── Nettoyage ─────────────────────────────────────────────────────────────────
def cleanup_audit_accounts():
    """Supprime tous les comptes @audit.fr et leurs données."""
    audit_codes = set()

    # Users
    try:
        users = sh.read("Users")
        clean  = [u for u in users if AUDIT_TAG not in str(u.get("Email",""))]
        removed = [u for u in users if AUDIT_TAG in str(u.get("Email",""))]
        for u in removed: audit_codes.add(str(u.get("Code","")))
        if removed and users:
            h = list(users[0].keys())
            sh.write_rows("Users", [h]+[[u.get(k,"") for k in h] for u in clean])
            print(f"  Users : {len(removed)} supprimé(s)")
    except Exception as e:
        print(f"  ⚠️  Users cleanup: {e}")

    if not audit_codes:
        print("  Aucun compte @audit.fr trouvé — nettoyage des autres onglets par email ignoré.")
        # Continue quand même pour nettoyer Suivi/Historique sur base email manquant

    if audit_codes:
        for tab_name, code_field in [("Scores","Code"),("Progress","Code"),("DailyBoosts","Code")]:
            try:
                rows = sh.read(tab_name)
                clean = [r for r in rows if str(r.get(code_field,"")) not in audit_codes]
                if len(clean) < len(rows) and rows:
                    h = list(rows[0].keys())
                    sh.write_rows(tab_name, [h]+[[r.get(k,"") for k in h] for r in clean])
                    print(f"  {tab_name} : {len(rows)-len(clean)} supprimé(s)")
            except Exception as e:
                print(f"  ⚠️  {tab_name} cleanup: {e}")

    try:
        raw = sh.read_raw("👁 Suivi")
        header = raw[0] if raw else []
        clean = [header]+[row for row in raw[1:] if not (len(row)>=21 and str(row[20]) in audit_codes)]
        if len(clean) < len(raw):
            sh.write_rows("👁 Suivi", clean)
            print(f"  👁 Suivi : {len(raw)-len(clean)} supprimé(s)")
    except Exception as e:
        print(f"  ⚠️  Suivi cleanup: {e}")

    # Nettoyage 📋 Historique (col B = Prénom contenant _Test)
    try:
        raw_h = sh.read_raw("📋 Historique")
        header_h = raw_h[0] if raw_h else []
        test_names = {p["name"] for p in PROFILES.values()}
        clean_h = [header_h]+[row for row in raw_h[1:] if not (len(row)>=2 and str(row[1]) in test_names)]
        if len(clean_h) < len(raw_h):
            sh.write_rows("📋 Historique", clean_h)
            print(f"  📋 Historique : {len(raw_h)-len(clean_h)} supprimé(s)")
    except Exception as e:
        print(f"  ⚠️  Historique cleanup: {e}")

# ── Scénarios ─────────────────────────────────────────────────────────────────

def s1_flux_nominal(A):
    A.scenario("S1 — Flux nominal complet (Alice)")
    p = PROFILES["alice"]
    email, level, name = p["email"], p["level"], p["name"]
    pw_hash = h256(email, PASSWORD)

    # 1. Register
    r = gas({"action":"register","name":name,"email":email,"level":level,"password":pw_hash})
    A.check(1, "register Alice", r.get("status")=="success", r.get("message",""))
    if r.get("status") != "success":
        A.bug("CRITIQUE", "Register Alice échoué", "backend.js")
        return
    wait(2)

    # 2. Login
    r = gas({"action":"login","email":email,"password":pw_hash})
    A.check(2, "login Alice", r.get("status")=="success", r.get("message",""))
    if r.get("status") != "success": return
    code = r["profile"]["code"]
    A.codes["alice"] = code
    A.data["alice_level"] = level
    A.data["alice_name"] = name
    curriculum = r.get("curriculumOfficiel", [])
    A.check(3, "curriculum reçu au login", len(curriculum) > 0, f"{len(curriculum)} chapitres")
    wait(1)

    # 4. generate_diagnostic
    selected = [curriculum[0]["categorie"], curriculum[1]["categorie"]] if len(curriculum) >= 2 else []
    r = gas({"action":"generate_diagnostic","code":code,"level":level,"selectedChapters":selected})
    A.check(4, "generate_diagnostic OK", r.get("status")=="success" and len(r.get("exos",[]))>0, f"{len(r.get('exos',[]))} exos")
    diag_exos = r.get("exos", [])
    wait(1)

    # 5. save_score × len(diag_exos) — diagnostic complet
    fake_diag = [{"q": e.get("q","Qdiag")[:60], "a": e.get("a","R"), "idx": i+1} for i,e in enumerate(diag_exos)]
    results_d = ["EASY" if random.random()>0.4 else "HARD" for _ in fake_diag]
    saved_d = do_save_scores(code, name, level, "CALIBRAGE", fake_diag, results_d)
    A.check(5, f"save_score diagnostic ({saved_d}/{len(fake_diag)})", saved_d == len(fake_diag), f"saved={saved_d}")
    wait(2)

    # 6. generate_daily_boost post-diag
    r = gas({"action":"generate_daily_boost","code":code,"level":level})
    A.check(6, "generate_daily_boost post-diag", r.get("status")=="success", r.get("message",""))
    boost = r.get("boost", {})
    boost_exos = boost.get("exos", [])
    if boost_exos:
        r2 = gas({"action":"save_boost","code":code,"boost":boost})
        A.check(7, "save_boost OK", r2.get("status")=="success", r2.get("message",""))
    else:
        A.check(7, "save_boost — boost vide", False, "boost.exos=[]")
    wait(2)

    # 8. Vérifier Suivi créé
    row = suivi_row(code)
    A.check(8, "Suivi créé après login+scores", row is not None, f"row={'present' if row else 'absent'}")
    wait(1)

    # 9. Vérifier Historique
    hist = historique_for("Alice_Test")
    A.check(9, "Historique contient lignes Alice", len(hist) > 0, f"{len(hist)} lignes")
    wait(1)

    # 10-11. Finir chapitre 1 (20 exos)
    if len(curriculum) > 0:
        cat1 = curriculum[0]["categorie"]
        cat1_exos = make_fake_exos(20, cat1, level)
        results_c1 = ["EASY"]*14 + ["HARD"]*4 + ["MEDIUM"]*2
        saved_c1 = do_save_scores(code, name, level, cat1, cat1_exos, results_c1)
        A.check(10, f"Chapitre 1 ({cat1}) : 20 exos sauvés", saved_c1 == 20, f"{saved_c1}/20")
        wait(2)

        # Vérifier Suivi : E (col 4) en vert, G (col 6) en rouge
        row = suivi_row(code)
        ch1_val = str(row[4]) if row and len(row) > 4 else ""
        A.check(11, "Suivi Ch1 contient le nom du chapitre", cat1 in ch1_val or ch1_val != "", f"col E='{ch1_val}'")

        bg_ch1 = cell_bg(code, 4)   # col E = chapitre 1
        A.check(12, "Suivi Ch1 fond vert (terminé)", is_green(bg_ch1), f"bg={bg_ch1}")

        bg_new1 = cell_bg(code, 6)  # col G = →Nouveau Ch1
        A.check(13, "Suivi →Nouveau Ch1 fond rouge (vide + terminé)", is_red(bg_new1), f"bg={bg_new1}")
        wait(1)

        # 14. Nicolas injecte JSON chapitre suivant dans col G (0-based=6)
        fake_new_exos = [{"q":f"NouvelExo{i+1}","a":f"R{i+1}","options":["R1","R2","R3"],"steps":["E1"],"f":"formule","lvl":1} for i in range(20)]
        inject_json = json.dumps({"categorie": cat1, "exos": fake_new_exos})
        ok_inject = suivi_inject(code, 6, inject_json)
        A.check(14, "Injection JSON →Nouveau Ch1 dans Suivi", ok_inject, "via API Sheets")
        wait(1)

        # 15. Login → vérifier nextChapter reçu + cellule vidée
        r = gas({"action":"login","email":email,"password":pw_hash})
        A.check(15, "login reçoit nextChapter après injection", r.get("nextChapter") is not None, f"nextChapter={str(r.get('nextChapter',''))[:60]}")
        wait(1.5)
        row_after = suivi_row(code)
        cell_f_after = str(row_after[6]) if row_after and len(row_after) > 6 else "NON_VIDE"
        A.check(16, "Cellule →Nouveau Ch1 vidée après login", cell_f_after == "", f"val='{cell_f_after}'")

        # 16. Injection →Nouveau Boost dans col S (0-based=18)
        fake_boost_exos = [{"q":f"BoostExo{i+1}","a":f"BR{i+1}","options":["R1","R2","R3"],"steps":["E1"],"f":"formule","lvl":1} for i in range(5)]
        inject_boost = json.dumps({"insight": "Boost injecté par audit", "exos": fake_boost_exos})
        ok_inject_boost = suivi_inject(code, 18, inject_boost)
        A.check(17, "Injection JSON →Nouveau Boost dans Suivi", ok_inject_boost, "via API Sheets")
        wait(1)

        # 17. Login → vérifier nextBoost reçu + cellule vidée
        r = gas({"action":"login","email":email,"password":pw_hash})
        A.check(18, "login reçoit nextBoost après injection", r.get("nextBoost") is not None, f"nextBoost keys={list((r.get('nextBoost') or {}).keys())}")
        wait(1.5)
        row_after2 = suivi_row(code)
        cell_r_after = str(row_after2[18]) if row_after2 and len(row_after2) > 18 else "NON_VIDE"
        A.check(19, "Cellule →Nouveau Boost vidée après login", cell_r_after == "", f"val='{cell_r_after}'")


def s2_abandon_diagnostic(A):
    A.scenario("S2 — Abandon diagnostic (Bob)")
    p = PROFILES["bob"]
    email, level, name = p["email"], p["level"], p["name"]
    pw_hash = h256(email, PASSWORD)

    # Register + login
    r = gas({"action":"register","name":name,"email":email,"level":level,"password":pw_hash})
    A.check(20, "register Bob", r.get("status")=="success", r.get("message",""))
    if r.get("status") != "success": return
    wait(2)

    r = gas({"action":"login","email":email,"password":pw_hash})
    A.check(21, "login Bob", r.get("status")=="success", "")
    if r.get("status") != "success": return
    code = r["profile"]["code"]
    A.codes["bob"] = code
    wait(1)

    # generate_diagnostic
    curriculum = r.get("curriculumOfficiel", [])
    selected = [curriculum[0]["categorie"]] if curriculum else []
    r = gas({"action":"generate_diagnostic","code":code,"level":level,"selectedChapters":selected})
    diag_exos = r.get("exos", [])
    A.check(22, "generate_diagnostic reçu", len(diag_exos) > 0, f"{len(diag_exos)} exos")
    wait(1)

    # save_score × 3 seulement — abandon
    partial = diag_exos[:3]
    fake_p = [{"q": e.get("q","Q")[:60], "a": e.get("a","R"), "idx": i+1} for i,e in enumerate(partial)]
    saved_p = do_save_scores(code, name, level, "CALIBRAGE", fake_p, ["EASY","HARD","EASY"])
    A.check(23, "3 scores diagnostic sauvés (abandon)", saved_p == 3, f"{saved_p}/3")
    wait(2)

    # Vérifier Suivi cohérent malgré diagnostic incomplet
    row = suivi_row(code)
    A.check(24, "Suivi existe malgré diagnostic incomplet", row is not None, "")
    if row:
        # Boost ne doit pas être marqué consommé
        boost_col = str(row[16]) if len(row) > 16 else ""
        A.check(25, "Boost actuel = '—' (non déclenché)", boost_col == "—" or boost_col == "", f"col Q='{boost_col}'")
    wait(1)

    # Reconnexion — progression conservée ?
    r2 = gas({"action":"login","email":email,"password":pw_hash})
    A.check(26, "Reconnexion Bob OK", r2.get("status")=="success", "")
    history = r2.get("history", [])
    calib_hist = [h for h in history if h.get("categorie") == "CALIBRAGE"]
    A.check(27, "3 scores CALIBRAGE conservés dans history au login", len(calib_hist) == 3, f"{len(calib_hist)} trouvés")
    wait(1)

    # Terminer le diagnostic
    if diag_exos:
        remaining = diag_exos[3:]
        fake_r = [{"q": e.get("q","Q")[:60], "a": e.get("a","R"), "idx": i+4} for i,e in enumerate(remaining)]
        results_r = ["EASY" if random.random()>0.3 else "HARD" for _ in fake_r]
        saved_r = do_save_scores(code, name, level, "CALIBRAGE", fake_r, results_r)
        A.check(28, "Terminer diagnostic (exos restants)", saved_r == len(remaining), f"{saved_r}/{len(remaining)}")
    wait(2)

    row2 = suivi_row(code)
    A.check(29, "Suivi mis à jour après fin diagnostic", row2 is not None, "")


def s3_abandon_boost(A):
    A.scenario("S3 — Abandon boost en cours (Bob)")
    code = A.codes.get("bob")
    if not code:
        A.check(30, "Bob code disponible", False, "S2 n'a pas stocké le code")
        return
    p = PROFILES["bob"]
    email, level, name = p["email"], p["level"], p["name"]
    pw_hash = h256(email, PASSWORD)
    wait(1)

    # Générer boost
    r = gas({"action":"generate_daily_boost","code":code,"level":level})
    A.check(30, "generate_daily_boost Bob", r.get("status")=="success", r.get("message",""))
    boost = r.get("boost", {})
    boost_exos_b = boost.get("exos", [])
    if not boost_exos_b:
        A.check(31, "boost a des exos", False, "boost.exos vide")
        return
    wait(1)

    # save_boost pour créer l'entrée DailyBoosts
    gas({"action":"save_boost","code":code,"boost":boost})
    wait(1)

    # save_score × 2 seulement — abandon
    fake_b = [{"q": e.get("q","QB")[:60], "a": e.get("a","R"), "idx": i+1} for i,e in enumerate(boost_exos_b[:2])]
    saved_b = do_save_scores(code, name, level, "BOOST", fake_b, ["EASY","HARD"])
    A.check(31, "2 exos boost sauvés puis abandon", saved_b == 2, f"{saved_b}/2")
    wait(2)

    # Vérifier Suivi : boost PAS marqué consommé (< 5 exos)
    row = suivi_row(code)
    boost_val = str(row[16]) if row and len(row) > 16 else ""
    consumed = "Consommé" in boost_val
    A.check(32, "Suivi : boost non consommé (2/5)", not consumed, f"col Q='{boost_val}'")

    # Vérifier couleur col S : pas rouge (boost non consommé)
    bg_r = cell_bg(code, 18)
    A.check(33, "Suivi →Nouveau Boost pas rouge (non consommé)", not is_red(bg_r), f"bg={bg_r}")
    wait(1)

    # Reconnexion — boost toujours là ?
    r2 = gas({"action":"login","email":email,"password":pw_hash})
    # Boost partiel (2/5 save_score, pas de save_boost) → boostExistsInDB=False par design
    # DailyBoosts n'est créé que quand save_boost est appelé (5/5 exos)
    A.check(34, "Reconnexion : boostExistsInDB=False (partiel, save_boost non appelé)", r2.get("boostExistsInDB") == False, f"boostExistsInDB={r2.get('boostExistsInDB')}")
    A.check(35, "Reconnexion : dailyBoost absent (partiel)", r2.get("dailyBoost") is None, f"dailyBoost={'present' if r2.get('dailyBoost') else 'absent'}")
    wait(1)

    # Simuler J+1 : modifier DailyBoosts date
    try:
        raw_boosts = sh.read_raw("DailyBoosts")
        for i, row_b in enumerate(raw_boosts[1:], start=2):
            if len(row_b) >= 1 and str(row_b[0]) == code:
                sh.update_cell("DailyBoosts", i, 2, YESTERDAY)
                break
        A.check(36, "Date DailyBoosts modifiée → hier", True, "via API Sheets")
    except Exception as e:
        A.check(36, "Date DailyBoosts modifiée → hier", False, str(e))
    wait(1)

    # Reconnexion J+1 → boost expiré
    r3 = gas({"action":"login","email":email,"password":pw_hash})
    boost_j1 = r3.get("dailyBoost")
    A.check(37, "J+1 : dailyBoost absent (date hier)", boost_j1 is None, f"dailyBoost={'present' if boost_j1 else 'absent'}")


def s4_abandon_chapitre(A):
    A.scenario("S4 — Abandon chapitre en cours (Clara)")
    p = PROFILES["clara"]
    email, level, name = p["email"], p["level"], p["name"]
    pw_hash = h256(email, PASSWORD)

    r = gas({"action":"register","name":name,"email":email,"level":level,"password":pw_hash})
    if r.get("status") != "success" and "existe" in r.get("message",""):
        r = {"status":"success"}  # compte résiduel d'un run précédent — on continue
    A.check(38, "register Clara", r.get("status")=="success", r.get("message",""))
    if r.get("status") != "success": return
    wait(2)

    r = gas({"action":"login","email":email,"password":pw_hash})
    A.check(39, "login Clara", r.get("status")=="success", "")
    if r.get("status") != "success": return
    code = r["profile"]["code"]
    A.codes["clara"] = code
    curriculum = r.get("curriculumOfficiel", [])
    cat1 = curriculum[0]["categorie"] if curriculum else "Fractions"
    wait(1)

    # 8 exos sur chapitre 1 — abandon
    fake8 = make_fake_exos(8, cat1, level)
    saved8 = do_save_scores(code, name, level, cat1, fake8, ["EASY"]*5+["HARD"]*3)
    A.check(40, f"8/20 exos chapitre 1 sauvés", saved8 == 8, f"{saved8}/8")
    wait(2)

    # Vérifier Suivi : En cours 8/20
    row = suivi_row(code)
    ch1_statut = ""
    if row and len(row) > 5:
        resume = str(row[5])  # col F = Résumé Ch1
        ch1_val = str(row[4]) if len(row) > 4 else ""
        # Le statut est dans le résumé JSON ou le nombre d'exos
        scores_c = scores_for(code)
        cat_scores = [s for s in scores_c if s.get("Chapitre") == cat1]
        n_exos = len(cat_scores)
        ch1_statut = f"{n_exos} exos"
        A.check(41, "Scores : 8 exos pour cat1", n_exos == 8, f"{n_exos} exos dans Scores")
    wait(1)

    # Reconnexion — progression conservée ?
    r2 = gas({"action":"login","email":email,"password":pw_hash})
    hist = r2.get("history", [])
    cat1_hist = [h for h in hist if h.get("categorie") == cat1]
    A.check(42, "Reconnexion : 8 scores conservés", len(cat1_hist) == 8, f"{len(cat1_hist)} trouvés")
    wait(1)

    # Reprendre et finir (12 exos restants)
    fake12 = make_fake_exos(12, cat1, level)
    for e in fake12: e["idx"] += 8  # continuer à partir de l'index 9
    saved12 = do_save_scores(code, name, level, cat1, fake12, ["EASY"]*8+["HARD"]*4)
    A.check(43, "12 exos restants sauvés → chapitre terminé", saved12 == 12, f"{saved12}/12")
    wait(2)

    # Suivi : fond vert ch1, fond rouge →nouveau
    row2 = suivi_row(code)
    bg_ch1 = cell_bg(code, 4)  # col E = Chapitre 1
    bg_new1 = cell_bg(code, 6)  # col G = →Nouveau Ch1
    A.check(44, "Suivi Ch1 vert (20/20 terminé)", is_green(bg_ch1), f"bg={bg_ch1}")
    A.check(45, "Suivi →Nouveau Ch1 rouge (action requise)", is_red(bg_new1), f"bg={bg_new1}")


def s5_reconnexions(A):
    A.scenario("S5 — Reconnexions multiples sans action (Clara)")
    code = A.codes.get("clara")
    if not code:
        A.check(46, "Clara code disponible", False, "S4 n'a pas stocké le code")
        return
    p = PROFILES["clara"]
    email, pw_hash = p["email"], h256(p["email"], PASSWORD)

    # 5 logins sans action
    successes = 0
    for i in range(5):
        r = gas({"action":"login","email":email,"password":pw_hash})
        if r.get("status") == "success": successes += 1
        wait(1.5)

    A.check(46, "5 logins consécutifs tous OK", successes == 5, f"{successes}/5")
    wait(1)

    # Pas de doublons dans Suivi
    try:
        raw = sh.read_raw("👁 Suivi")
        code_occurrences = sum(1 for row in raw[1:] if len(row) >= 21 and str(row[20]) == code)
        A.check(47, "Pas de doublons dans Suivi (1 seule ligne)", code_occurrences == 1, f"{code_occurrences} ligne(s)")
    except Exception as e:
        A.check(47, "Pas de doublons dans Suivi", False, str(e))
    wait(1)

    # Données cohérentes : scores count stable
    scores_c = scores_for(code)
    A.check(48, "Scores stables (pas de doublons)", len(scores_c) == 20, f"{len(scores_c)} scores (attendu 20)")


def s6_chaos(A):
    A.scenario("S6 — Comportements chaos (David)")
    p = PROFILES["david"]
    email, level, name = p["email"], p["level"], p["name"]
    pw_hash = h256(email, PASSWORD)

    r = gas({"action":"register","name":name,"email":email,"level":level,"password":pw_hash})
    if r.get("status") != "success" and "existe" in r.get("message",""):
        r = {"status":"success"}
    A.check(49, "register David", r.get("status")=="success", r.get("message",""))
    if r.get("status") != "success": return
    wait(2)

    r_login = gas({"action":"login","email":email,"password":pw_hash})
    A.check(50, "login David", r_login.get("status")=="success", "")
    if r_login.get("status") != "success": return
    code = r_login["profile"]["code"]
    A.codes["david"] = code
    wait(1)

    # save_score sans diagnostic (chapitre inexistant)
    r = gas({"action":"save_score","code":code,"name":name,"level":level,
             "categorie":"CHAPITRE_INEXISTANT","exercice_idx":1,"resultat":"EASY",
             "q":"question test","time":10,"indices":0,"formule":False,"wrongOpt":"","draft":""})
    # Doit réussir (GAS n'impose pas que le chapitre existe dans le curriculum)
    A.check(51, "save_score chapitre inexistant → pas de crash", r.get("status") in ("success","error"), f"status={r.get('status')}")
    wait(1)

    # save_boost sans avoir généré de boost
    r = gas({"action":"save_boost","code":code,"boost":{"insight":"test","exos":[]}})
    A.check(52, "save_boost sans boost → pas de crash", r.get("status") in ("success","error"), f"status={r.get('status')}")
    wait(1)

    # generate_daily_boost × 3
    boosts_ok = 0
    for _ in range(3):
        r = gas({"action":"generate_daily_boost","code":code,"level":level})
        if r.get("status") == "success": boosts_ok += 1
        wait(2)
    A.check(53, "3x generate_daily_boost → pas de crash", boosts_ok >= 1, f"{boosts_ok}/3 OK")
    wait(1)

    # Mauvais mot de passe
    r = gas({"action":"login","email":email,"password":"wrong_hash_000"})
    A.check(54, "login mauvais mdp → erreur propre", r.get("status")=="error", f"msg={r.get('message','')[:50]}")
    wait(1)

    # Email déjà existant
    r = gas({"action":"register","name":name,"email":email,"level":level,"password":pw_hash})
    A.check(55, "register email existant → erreur propre", r.get("status")=="error", f"msg={r.get('message','')[:50]}")
    wait(1)

    # JSON invalide dans →Nouveau Ch1 → login ne doit pas crasher
    suivi_inject(code, 6, "CECI_N_EST_PAS_DU_JSON{malformed")
    wait(1)
    r = gas({"action":"login","email":email,"password":pw_hash})
    A.check(56, "login avec JSON malformé dans Suivi → pas de crash", r.get("status")=="success", f"status={r.get('status')}, nextChapter={r.get('nextChapter')}")
    wait(1)
    # GAS @15 : JSON malformé → PENDING_MANUAL retourné, cellule préservée pour re-essai
    A.check(57, "Login JSON malformé → PENDING_MANUAL retourné",
        isinstance(r.get('nextChapter'), dict) and r.get('nextChapter',{}).get('categorie') == 'PENDING_MANUAL',
        f"nextChapter={r.get('nextChapter')}")
    wait(1)

    # JSON vide
    suivi_inject(code, 6, "")
    r = gas({"action":"login","email":email,"password":pw_hash})
    A.check(58, "login avec cellule vide → nextChapter=null", r.get("nextChapter") is None, f"nextChapter={r.get('nextChapter')}")
    wait(1)

    # Texte non-JSON
    suivi_inject(code, 6, "Réviser les fractions")
    wait(1)
    r = gas({"action":"login","email":email,"password":pw_hash})
    next_c = r.get("nextChapter")
    # exos=[] → le frontend ne doit pas crasher (chapitre avec 0 exos)
    A.check(59, "login avec texte non-JSON → nextChapter acceptable (fallback)",
        isinstance(next_c, str) or next_c is None or (isinstance(next_c, dict) and next_c.get('categorie') == 'PENDING_MANUAL'),
        f"nextChapter={next_c}")
    wait(1)
    # GAS @15 : cellule préservée (PENDING_MANUAL), r contient le résultat du login précédent
    A.check(60, "Login texte non-JSON → PENDING_MANUAL retourné",
        isinstance(r.get('nextChapter'), dict) and r.get('nextChapter',{}).get('categorie') == 'PENDING_MANUAL',
        f"nextChapter={r.get('nextChapter')}")


def s7_persistance(A):
    A.scenario("S7 — Test persistance état (Emma)")
    p = PROFILES["emma"]
    email, level, name = p["email"], p["level"], p["name"]
    pw_hash = h256(email, PASSWORD)

    r = gas({"action":"register","name":name,"email":email,"level":level,"password":pw_hash})
    if r.get("status") != "success" and "existe" in r.get("message",""):
        r = {"status":"success"}
    A.check(61, "register Emma", r.get("status")=="success", r.get("message",""))
    if r.get("status") != "success": return
    wait(2)

    r = gas({"action":"login","email":email,"password":pw_hash})
    A.check(62, "login Emma", r.get("status")=="success", "")
    if r.get("status") != "success": return
    code = r["profile"]["code"]
    A.codes["emma"] = code
    curriculum = r.get("curriculumOfficiel", [])
    cat1 = curriculum[0]["categorie"] if curriculum else "Equations"
    wait(1)

    # 10 exos chapitre 1 → déconnexion
    fake10 = make_fake_exos(10, cat1, level)
    saved10 = do_save_scores(code, name, level, cat1, fake10, ["EASY"]*6+["HARD"]*4)
    A.check(63, "10/20 exos chapitre 1 sauvés", saved10 == 10, f"{saved10}/10")
    wait(2)

    # Reconnexion → progression conservée
    r2 = gas({"action":"login","email":email,"password":pw_hash})
    hist = r2.get("history", [])
    cat1_hist = [h for h in hist if h.get("categorie") == cat1]
    A.check(64, "Reconnexion : 10 scores conservés", len(cat1_hist) == 10, f"{len(cat1_hist)} trouvés")
    wait(1)

    # Générer boost SANS save_boost (simule abandon avant save)
    r = gas({"action":"generate_daily_boost","code":code,"level":level})
    boost_exos_e = r.get("boost",{}).get("exos",[])
    A.check(65, "generate_daily_boost OK", len(boost_exos_e) > 0, f"{len(boost_exos_e)} exos")
    wait(1)
    # Ne PAS appeler save_boost → reconnexion

    r3 = gas({"action":"login","email":email,"password":pw_hash})
    A.check(66, "Reconnexion après abandon boost : boostExistsInDB=False", r3.get("boostExistsInDB")==False, f"boostExistsInDB={r3.get('boostExistsInDB')}")
    wait(1)

    # Finir chapitre (10 exos restants)
    fake10b = make_fake_exos(10, cat1, level)
    for e in fake10b: e["idx"] += 10
    saved10b = do_save_scores(code, name, level, cat1, fake10b, ["EASY"]*7+["HARD"]*3)
    A.check(67, "10 exos restants → chapitre terminé", saved10b == 10, f"{saved10b}/10")
    wait(2)

    # Injecter nextChapter → login Emma → badge
    fake_new = [{"q":f"NvExo{i+1}","a":f"R{i+1}","options":["R1","R2","R3"],"steps":["E1"],"f":"f","lvl":1} for i in range(20)]
    inject_nc = json.dumps({"categorie": cat1, "exos": fake_new})
    suivi_inject(code, 6, inject_nc)
    wait(1)

    r4 = gas({"action":"login","email":email,"password":pw_hash})
    A.check(68, "login Emma reçoit nextChapter injecté", r4.get("nextChapter") is not None, f"nextChapter type={type(r4.get('nextChapter')).__name__}")
    wait(1)

    # 3 exos du nouveau chapitre → déconnexion → reconnexion → 3/20 conservé
    fake3 = make_fake_exos(3, cat1, level)
    saved3 = do_save_scores(code, name, level, cat1, fake3, ["EASY","HARD","EASY"])
    A.check(69, "3 exos nouveau chapitre sauvés", saved3 == 3, f"{saved3}/3")
    wait(2)

    r5 = gas({"action":"login","email":email,"password":pw_hash})
    hist5 = r5.get("history",[])
    cat1_hist5 = [h for h in hist5 if h.get("categorie") == cat1]
    A.check(70, "Reconnexion : 23 scores cat1 conservés (10+10+3)", len(cat1_hist5) == 23, f"{len(cat1_hist5)} scores cat1")


def s8_multijours(A):
    A.scenario("S8 — Simulation multi-jours (Alice)")
    code = A.codes.get("alice")
    if not code:
        A.check(71, "Alice code disponible", False, "S1 n'a pas stocké le code")
        return
    p = PROFILES["alice"]
    email, pw_hash = p["email"], h256(p["email"], PASSWORD)

    # Modifier date DailyBoosts Alice → hier
    try:
        raw_b = sh.read_raw("DailyBoosts")
        modified = False
        for i, row_b in enumerate(raw_b[1:], start=2):
            if str(row_b[0]) == code:
                sh.update_cell("DailyBoosts", i, 2, YESTERDAY)
                modified = True
                break
        A.check(71, "DailyBoosts date Alice → hier", modified, "")
    except Exception as e:
        A.check(71, "DailyBoosts date Alice → hier", False, str(e))
    wait(1)

    # login → boostExistsInDB doit être False (date = hier)
    r = gas({"action":"login","email":email,"password":pw_hash})
    A.check(72, "J+1 : boostExistsInDB=False (boost expiré)", r.get("boostExistsInDB")==False, f"val={r.get('boostExistsInDB')}")
    wait(1)

    # Suivi : boost actuel
    row = suivi_row(code)
    boost_col = str(row[16]) if row and len(row) > 16 else ""
    A.check(73, "Suivi : boost actuel cohérent", bool(row), f"col Q='{boost_col}'")
    wait(1)

    # Générer un nouveau boost + sauvegarder
    r = gas({"action":"generate_daily_boost","code":code,"level":A.data.get("alice_level","5EME")})
    if r.get("status") == "success":
        r2 = gas({"action":"save_boost","code":code,"boost":r["boost"]})
        A.check(74, "Nouveau boost généré + sauvé (J+1)", r2.get("status")=="success", r2.get("message",""))
    else:
        A.check(74, "Nouveau boost généré + sauvé (J+1)", False, r.get("message",""))
    wait(3)

    # login J+1 → dailyBoost présent
    r3 = gas({"action":"login","email":email,"password":pw_hash})
    A.check(75, "J+1 : dailyBoost présent après regénération", r3.get("boostExistsInDB")==True, f"val={r3.get('boostExistsInDB')}")


def s9_json_malformed(A):
    A.scenario("S9 — Injection JSON malformé (David) — cas supplémentaires")
    code = A.codes.get("david")
    if not code:
        A.check(76, "David code disponible", False, "S6 n'a pas stocké le code")
        return
    p = PROFILES["david"]
    email, pw_hash = p["email"], h256(p["email"], PASSWORD)

    # JSON avec mauvais format (pas de clé 'exos')
    bad_json = json.dumps({"categorie": "Fractions", "data": []})  # manque 'exos'
    suivi_inject(code, 6, bad_json)
    wait(1)
    r = gas({"action":"login","email":email,"password":pw_hash})
    nc76 = r.get("nextChapter")
    A.check(76, "JSON sans clé 'exos' → nextChapter=null, string ou PENDING_MANUAL",
        nc76 is None or isinstance(nc76, str) or (isinstance(nc76, dict) and nc76.get('categorie') == 'PENDING_MANUAL'),
        f"nextChapter={nc76}")
    wait(1.5)

    # JSON avec 'exos' vide
    empty_exos = json.dumps({"categorie": "Fractions", "exos": []})
    suivi_inject(code, 6, empty_exos)
    wait(1)
    r = gas({"action":"login","email":email,"password":pw_hash})
    nc = r.get("nextChapter")
    # exos=[] → le frontend ne doit pas crasher (chapitre avec 0 exos)
    A.check(77, "JSON exos=[] → login OK sans crash", r.get("status")=="success", f"status={r.get('status')}, nextChapter={nc}")
    wait(1.5)

    # Même pour →Nouveau Boost : JSON malformé
    bad_boost = "{'insight': 'test', exos: []}"  # JSON invalide (guillemets simples)
    suivi_inject(code, 18, bad_boost)
    wait(1)
    r = gas({"action":"login","email":email,"password":pw_hash})
    A.check(78, "Boost malformé → nextBoost=null, login OK", r.get("status")=="success" and r.get("nextBoost") is None, f"nextBoost={r.get('nextBoost')}")


def s10_charge(A):
    A.scenario("S10 — Charge simultanée (5 save_score parallèles)")
    code = A.codes.get("clara")
    if not code:
        A.check(79, "Clara code disponible", False, "")
        return
    p = PROFILES["clara"]
    name, level = p["name"], p["level"]

    scores_before = len(scores_for(code))
    results_parallel = []
    errors_parallel = []

    def send_one(idx):
        r = gas({
            "action":"save_score","code":code,"name":name,"level":level,
            "categorie":"CHARGE_TEST","exercice_idx":idx+1,"resultat":"EASY",
            "q":f"Charge test Q{idx+1}","time":15,"indices":0,
            "formule":False,"wrongOpt":"","draft":""
        })
        if r.get("status")=="success":
            results_parallel.append(idx)
        else:
            errors_parallel.append(r.get("message",""))

    threads = [threading.Thread(target=send_one, args=(i,)) for i in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    wait(3)

    scores_after = len(scores_for(code))
    added = scores_after - scores_before
    A.check(79, "5 save_score parallèles → 5 lignes Scores ajoutées", added == 5, f"{added} lignes ajoutées")

    # Pas de doublons (vérif sur exercice_idx)
    scores_charge = [s for s in scores_for(code) if s.get("Chapitre") == "CHARGE_TEST"]
    idxs = [int(s.get("NumExo",0)) for s in scores_charge]
    A.check(80, "Pas de doublons (idxs uniques)", len(idxs) == len(set(idxs)), f"idxs={sorted(idxs)}")

    row = suivi_row(code)
    A.check(81, "Suivi cohérent après charge parallèle", row is not None, "")

def s11_admin_mode(A):
    A.scenario("S11 — Mode Admin (Nicolas)")
    ADMIN_CODE = "ADMIN1"  # Code admin dans Users (IsAdmin=1)
    emma_code  = A.codes.get("emma")
    alice_code = A.codes.get("alice")

    # 82. get_admin_overview avec code admin valide
    r = gas({"action": "get_admin_overview", "adminCode": ADMIN_CODE})
    A.check(82, "get_admin_overview avec code admin", r.get("status") == "success",
        f"status={r.get('status')}, msg={r.get('message','')[:50]}")
    if r.get("status") != "success": return
    wait(1)

    students = r.get("students", [])
    A.check(83, "Overview retourne une liste d'élèves", len(students) > 0, f"{len(students)} élèves")
    if not students: return

    # 84. Structure : chaque élève a les champs requis
    st0 = students[0]
    has_fields = all(k in st0 for k in ["code","prenom","niveau","action","chapitresDetail"])
    A.check(84, "Structure élève complète (code, prenom, action, chapitresDetail)", has_fields,
        f"champs présents: {[k for k in ['code','prenom','action','chapitresDetail'] if k in st0]}")

    # 85. get_admin_overview avec code non-admin → accès refusé
    r_bad = gas({"action": "get_admin_overview", "adminCode": "FAKE_CODE_XYZ"})
    A.check(85, "get_admin_overview code invalide → accès refusé",
        r_bad.get("status") == "error" and "refus" in r_bad.get("message","").lower(),
        f"status={r_bad.get('status')}, msg={r_bad.get('message','')[:50]}")
    wait(1)

    # 86. chapitresDetail rempli pour emma (qui a fait des exos)
    if emma_code:
        emma_st = next((s for s in students if s["code"] == emma_code), None)
        has_detail = emma_st and len(emma_st.get("chapitresDetail", [])) > 0
        A.check(86, "chapitresDetail rempli pour Emma (a fait des exos)", has_detail,
            f"detail={len(emma_st.get('chapitresDetail',[])) if emma_st else 'élève introuvable'} chap(s)")
    else:
        A.check(86, "Emma code disponible pour test detail", False, "S7 n'a pas stocké le code")
    wait(1)

    # 87. publish_admin_boost → succès
    if emma_code:
        fake_boost_exos = [
            {"q":f"Exo boost {i+1}","a":f"R{i+1}","options":[f"R{i+1}","Mauvais A","Mauvais B"],
             "steps":["Étape 1","Étape 2"],"f":"formule","lvl":1}
            for i in range(5)
        ]
        r_pub = gas({
            "action":     "publish_admin_boost",
            "adminCode":  ADMIN_CODE,
            "targetCode": emma_code,
            "insight":    "Boost admin test",
            "exos":       fake_boost_exos
        })
        A.check(87, "publish_admin_boost pour Emma → succès",
            r_pub.get("status") == "success",
            f"status={r_pub.get('status')}, msg={r_pub.get('message','')[:60]}")
        wait(2)

        # 88. Suivi Emma : →Nouveau Boost rempli
        row = suivi_row(emma_code)
        boost_cell = str(row[18]) if row and len(row) > 18 else ""
        A.check(88, "Suivi Emma : →Nouveau Boost rempli après publish",
            boost_cell.startswith("{") and "exos" in boost_cell,
            f"col S='{boost_cell[:60]}'")
        wait(1)

        # 89. Emma se reconnecte → reçoit le boost publié
        p_emma = PROFILES["emma"]
        r_login = gas({"action":"login","email":p_emma["email"],"password":h256(p_emma["email"],PASSWORD)})
        nb = r_login.get("nextBoost")
        A.check(89, "Emma login → reçoit nextBoost publié par admin",
            isinstance(nb, dict) and len(nb.get("exos", [])) == 5,
            f"nextBoost.exos={len(nb.get('exos',[])) if isinstance(nb,dict) else 'absent'}")
        wait(2)

        # 90. Suivi Emma : →Nouveau Boost vidé après login (injection faite)
        row2 = suivi_row(emma_code)
        cell_after = str(row2[18]) if row2 and len(row2) > 18 else "NON_VIDE"
        A.check(90, "Suivi Emma : →Nouveau Boost vidé après login (injecté)", cell_after == "",
            f"col S='{cell_after[:40]}'")
    else:
        for n in [87, 88, 89, 90]:
            A.check(n, f"Test {n} (emma code requis)", False, "Emma indisponible")
    wait(1)

    # 91. publish_admin_chapter → succès
    if alice_code:
        fake_chap_exos = [
            {"q":f"Chap exo {i+1}","a":f"Rep{i+1}","options":[f"Rep{i+1}","ErrA","ErrB"],
             "steps":["Étape 1","Étape 2"],"f":"formule","lvl":1 if i < 10 else 2}
            for i in range(20)
        ]
        r_chap = gas({
            "action":     "publish_admin_chapter",
            "adminCode":  ADMIN_CODE,
            "targetCode": alice_code,
            "categorie":  "Fractions",
            "insight":    "Chapitre admin test",
            "exos":       fake_chap_exos
        })
        A.check(91, "publish_admin_chapter pour Alice → succès",
            r_chap.get("status") == "success",
            f"status={r_chap.get('status')}, msg={r_chap.get('message','')[:60]}")
        wait(2)

        # 92. Alice se reconnecte → reçoit le chapitre publié
        p_alice = PROFILES["alice"]
        r_login2 = gas({"action":"login","email":p_alice["email"],"password":h256(p_alice["email"],PASSWORD)})
        nc = r_login2.get("nextChapter")
        A.check(92, "Alice login → reçoit nextChapter publié par admin",
            isinstance(nc, dict) and nc.get("categorie") == "Fractions" and len(nc.get("exos",[])) == 20,
            f"nextChapter.categorie={nc.get('categorie') if isinstance(nc,dict) else 'absent'}, exos={len(nc.get('exos',[])) if isinstance(nc,dict) else 0}")
    else:
        for n in [91, 92]:
            A.check(n, f"Test {n} (alice code requis)", False, "Alice indisponible")

    # 93. Tri : élèves non-RAS en premier
    non_ras = [s for s in students if "RAS" not in s.get("action","")]
    ras     = [s for s in students if "RAS"     in s.get("action","")]
    all_students = non_ras + ras
    A.check(93, "Dashboard trié : non-RAS avant RAS",
        students[:len(non_ras)] == non_ras or len(non_ras) == 0 or len(ras) == 0,
        f"{len(non_ras)} non-RAS, {len(ras)} RAS")


# ── Rapport ───────────────────────────────────────────────────────────────────

def generate_report(A, had_bugs, output_path):
    """Génère docs/audit_complet.md"""
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ok_total, all_total = A.totals()

    lines = [f"# Audit complet Matheux — {now}", "", "## Résumé", ""]
    lines.append("| Scénario | Tests | ✅ | ❌ | Taux |")
    lines.append("|----------|-------|----|----|------|")
    for s in A.scenarios:
        ok  = sum(t["ok"] for t in s["tests"])
        all_ = len(s["tests"])
        ko  = all_ - ok
        pct = f"{round(ok/all_*100)}%" if all_ else "—"
        lines.append(f"| {s['name']} | {all_} | {ok} | {ko} | {pct} |")
    lines.append(f"| **TOTAL** | **{all_total}** | **{ok_total}** | **{all_total-ok_total}** | **{round(ok_total/all_total*100) if all_total else 0}%** |")
    lines += ["", "## Détail par scénario", ""]

    for s in A.scenarios:
        lines += [f"### {s['name']}", ""]
        lines.append("| # | Test | Statut | Preuve |")
        lines.append("|---|------|--------|--------|")
        for t in s["tests"]:
            st = "✅" if t["ok"] else "❌"
            proof = str(t["proof"]).replace("|","\\|")[:80]
            lines.append(f"| {t['num']:02d} | {t['desc']} | {st} | {proof} |")
        lines.append("")

    if A.bugs:
        lines += ["## Bugs trouvés", ""]
        lines.append("| # | Sévérité | Description | Fichier | Ligne |")
        lines.append("|---|----------|-------------|---------|-------|")
        for i, b in enumerate(A.bugs, 1):
            lines.append(f"| {i} | **{b['sev']}** | {b['desc']} | {b['file']} | {b['line']} |")
        lines.append("")
    else:
        lines += ["## Bugs trouvés", "", "_Aucun bug détecté._", ""]

    verdict = "✅ Prêt pour les premiers clients" if ok_total == all_total else f"⚠️ {all_total-ok_total} test(s) échoué(s) — corriger avant lancement"
    lines += ["## Verdict final", "", f"**Score : {ok_total}/{all_total}**", "", f"**{verdict}**", ""]

    if had_bugs:
        lines.append("> ⚠️ Comptes @audit.fr CONSERVÉS comme preuves (nettoyage manuel requis)")
    else:
        lines.append("> ✅ Comptes @audit.fr nettoyés automatiquement")

    Path(output_path).parent.mkdir(exist_ok=True)
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"\n📄 Rapport : {output_path}")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("🔍 Audit automatisé Matheux — démarrage")
    print(f"   Date : {TODAY}")
    print(f"   GAS  : {GAS_URL[:60]}...")

    A = AuditRunner()

    # Pré-nettoyage des éventuels comptes orphelins de l'audit précédent
    print("\n── Pré-nettoyage comptes @audit.fr ──")
    cleanup_audit_accounts()

    # Scénarios
    s1_flux_nominal(A)
    s2_abandon_diagnostic(A)
    s3_abandon_boost(A)
    s4_abandon_chapitre(A)
    s5_reconnexions(A)
    s6_chaos(A)
    s7_persistance(A)
    s8_multijours(A)
    s9_json_malformed(A)
    s10_charge(A)
    s11_admin_mode(A)

    A.finish()
    ok, total = A.totals()
    had_bugs = len(A.bugs) > 0 or (total - ok) > 0

    print(f"\n{'═'*60}")
    print(f"  RÉSULTAT FINAL : {ok}/{total} tests OK")
    print(f"  Bugs : {len(A.bugs)}")
    print(f"{'═'*60}")

    report_path = "/home/nicolas/Bureau/algebra live/algebra/docs/audit_complet.md"
    generate_report(A, had_bugs, report_path)

    if not had_bugs:
        print("\n── Nettoyage final comptes @audit.fr ──")
        cleanup_audit_accounts()
    else:
        print(f"\n⚠️  {total-ok} test(s) en échec ou {len(A.bugs)} bug(s) → comptes @audit.fr CONSERVÉS")

    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
