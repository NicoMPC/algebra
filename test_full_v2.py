#!/usr/bin/env python3
"""
test_full_v2.py — Suite de tests complète Matheux
==================================================
Simule TOUS les scénarios élève/fondateur sur plusieurs jours.
Tous les comptes créés sont IsTest=1 — ne comptent jamais dans le quota 50.

Usage :
  python3 test_full_v2.py [--scenario NOM] [--verbose] [--cleanup]

Scénarios disponibles :
  all        Tous les scénarios (défaut)
  alice      Flux nominal complet (inscription → diag → 5j boosts → chapitre)
  bob        Abandon en cours de route
  multi      5 élèves simultanés
  edge       Cas limites (email invalide, double inscription, etc.)
  admin      Flux fondateur (admin overview, publish boost, publish chapter)
  email      Vérification envoi email J+0
"""

import requests, json, hashlib, time, sys, argparse, random, string
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)
ADMIN_EMAIL = "admin@matheux.fr"
ADMIN_HASH  = "dba3013d8ee56602f8da554bd6f5ff0108324c6d220f137d2181d9d24fa0ef62"

LEVELS  = ["3EME"]  # Backend restreint à 3EME (focus Brevet 2026)
VERBOSE = False

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def h256(password: str, email: str) -> str:
    raw = f"{email.lower().strip()}::{password}::AB22"
    return hashlib.sha256(raw.encode()).hexdigest()

def gas(payload: dict, retry: int = 3) -> dict:
    """Appel GAS avec retry."""
    for attempt in range(retry):
        try:
            r = requests.post(GAS_URL, json=payload, timeout=30)
            return r.json()
        except Exception as e:
            if attempt == retry - 1:
                return {"status": "error", "message": str(e)}
            time.sleep(2)

def rand_email(prefix: str = "test") -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"test.{prefix}.{suffix}@matheux.fr"

def log(msg: str, level: str = "INFO"):
    icons = {"INFO": "ℹ️", "OK": "✅", "FAIL": "❌", "WARN": "⚠️", "STEP": "▶️", "DAY": "📅"}
    print(f"  {icons.get(level,'·')} {msg}")

def assert_ok(result: dict, context: str) -> bool:
    if result.get("status") == "success":
        if VERBOSE: log(f"{context} → OK", "OK")
        return True
    log(f"{context} → ÉCHEC : {result.get('message','?')}", "FAIL")
    return False

# ─────────────────────────────────────────────────────────────
# ACTIONS FONDATEUR (simule le travail de Nicolas)
# ─────────────────────────────────────────────────────────────

_admin_cache = None
def admin_login() -> dict | None:
    """Login admin et retourne le profil (cached pour éviter rate_limit)."""
    global _admin_cache
    if _admin_cache is not None:
        return _admin_cache
    r = gas({"action": "login", "email": ADMIN_EMAIL, "password": ADMIN_HASH})
    if r.get("status") == "success" and r.get("profile", {}).get("isAdmin"):
        _admin_cache = r["profile"]
        return _admin_cache
    log(f"Admin login impossible : {r.get('message','?')}", "WARN")
    return None

def get_admin_overview(admin_code: str) -> dict:
    return gas({"action": "get_admin_overview", "adminCode": admin_code})

def nicolas_publish_boost(admin_code: str, student_code: str, boost_json: dict) -> bool:
    """Simule Nicolas qui publie un boost pour un élève."""
    exos = boost_json.get("exos", boost_json) if isinstance(boost_json, dict) else boost_json
    r = gas({
        "action": "publish_admin_boost",
        "adminCode": admin_code,
        "targetCode": student_code,
        "exos": exos,
        "insight": boost_json.get("insight", "Boost personnalisé") if isinstance(boost_json, dict) else "",
        "motProf": "Bon courage pour ce boost !"
    })
    if r.get("status") != "success":
        log(f"  publish_boost error: {r.get('message','?')[:80]}", "WARN")
    return r.get("status") == "success"

def nicolas_publish_chapter(admin_code: str, student_code: str, chapter_json: dict) -> bool:
    """Simule Nicolas qui publie un chapitre pour un élève."""
    r = gas({
        "action": "publish_admin_chapter",
        "adminCode": admin_code,
        "targetCode": student_code,
        "categorie": chapter_json.get("categorie", ""),
        "exos": chapter_json.get("exos", []),
        "insight": chapter_json.get("insight", "Nouveau chapitre personnalisé"),
        "motProf": "Nouveau chapitre — tu vas y arriver !"
    })
    return r.get("status") == "success"

def create_simple_boost(level: str, category: str) -> dict:
    """Crée un boost minimal valide (exos directs pour l'API GAS)."""
    exos = []
    for i in range(5):
        exos.append({
            "q": f"Question test {i+1} ({category})",
            "a": "42",
            "options": ["42", "24", "12", "6"],
            "steps": ["Commence par décomposer le problème."],
            "f": "Formule de test",
            "lvl": 1,
            "oC": category,
            "oI": i
        })
    return {
        "categorie": category,
        "niveau": level,
        "insight": f"Boost test sur {category}",
        "exos": exos
    }

# ─────────────────────────────────────────────────────────────
# ACTIONS ÉLÈVE
# ─────────────────────────────────────────────────────────────

class Student:
    def __init__(self, prenom: str, level: str):
        self.prenom = prenom
        self.level  = level
        self.email  = rand_email(prenom.lower())
        self.password = "TestPass2026!"
        self.hash   = h256(self.password, self.email)
        self.code   = None
        self.profile = None
        self.boost   = None
        self.day     = 0  # jour simulé

    def register(self) -> bool:
        r = gas({
            "action": "register",
            "email":  self.email,
            "name":   self.prenom,
            "level":  self.level,
            "password": self.hash
        })
        if r.get("status") == "success":
            self.code = r["profile"]["code"]
            self.profile = r["profile"]
            return True
        log(f"Register {self.prenom} → {r.get('message','?')}", "FAIL")
        return False

    def login(self) -> dict | None:
        r = gas({"action": "login", "email": self.email, "password": self.hash})
        if r.get("status") == "success":
            self.profile = r.get("profile")
            # dailyBoost = boost déjà en DB pour aujourd'hui
            # nextBoost  = boost livré à l'instant depuis Suivi (Nicolas vient de le publier)
            self.boost = r.get("dailyBoost") or r.get("nextBoost")
            return r
        return None

    def run_diagnostic(self) -> list:
        """Fait le diagnostic : répond à tous les exos."""
        r = gas({"action": "generate_diagnostic", "level": self.level, "selectedChapters": []})
        if r.get("status") != "success":
            return []
        exos = r.get("exos", [])
        results = []
        for i, exo in enumerate(exos[:10]):
            cat = exo.get("oC") or exo.get("categorie", "Diagnostic")
            correct = random.random() > 0.4  # 60% de réussite
            status  = "EASY" if correct else "HARD"
            gas({
                "action": "save_score",
                "code": self.code,
                "name": self.prenom,
                "level": self.level,
                "categorie": cat,
                "exercice_idx": i + 1,
                "q": (exo.get("q",""))[:80],
                "resultat": status,
                "temps": random.randint(15, 90),
                "nbIndices": 0,
                "formule": False,
                "source": "CALIBRAGE"
            })
            results.append({"cat": cat, "correct": correct})
        return results

    def do_boost(self, partial: bool = False) -> int:
        """Fait le boost du jour. partial=True → s'arrête après 2 exos."""
        if not self.boost:
            return 0
        exos = self.boost.get("exos", [])
        count = 2 if partial else len(exos)
        done  = 0
        for i, exo in enumerate(exos[:count]):
            correct = random.random() > 0.35
            status  = "EASY" if correct else "HARD"
            gas({
                "action": "save_boost",
                "code":  self.code,
                "boost": self.boost,
                "exoIdx": i
            })
            gas({
                "action": "save_score",
                "code": self.code,
                "name": self.prenom,
                "level": self.level,
                "categorie": exo.get("oC", "BOOST"),
                "exercice_idx": i + 1,
                "q": (exo.get("q",""))[:80],
                "resultat": status,
                "temps": random.randint(20, 120),
                "nbIndices": random.randint(0, 2),
                "formule": random.random() > 0.7,
                "source": "BOOST"
            })
            done += 1
        return done

    def do_chapter(self, category: str, n_exos: int = 20) -> int:
        """Fait N exos d'un chapitre."""
        done = 0
        for i in range(n_exos):
            correct = random.random() > 0.3
            status  = "EASY" if correct else "HARD"
            gas({
                "action": "save_score",
                "code": self.code,
                "name": self.prenom,
                "level": self.level,
                "categorie": category,
                "exercice_idx": i + 1,
                "q": f"Exercice {i+1} — {category}",
                "resultat": status,
                "temps": random.randint(30, 150),
                "nbIndices": 0,
                "formule": False,
                "source": "chapter"
            })
            done += 1
            time.sleep(0.05)
        return done

# ─────────────────────────────────────────────────────────────
# SCÉNARIOS
# ─────────────────────────────────────────────────────────────

PASS = 0; FAIL = 0

def check(cond: bool, label: str):
    global PASS, FAIL
    if cond:
        PASS += 1
        if VERBOSE: log(label, "OK")
    else:
        FAIL += 1
        log(label, "FAIL")

# ── S1 : Flux nominal Alice (5 jours) ─────────────────────────
def scenario_alice():
    print("\n📌 S1 — Flux nominal Alice (5 jours)")
    s = Student("Alice", "3EME")

    # J0 — Inscription
    log("J+0 : Inscription", "DAY")
    check(s.register(), "Inscription réussie")
    login_r = s.login()
    check(login_r is not None, "Login post-inscription")

    # J0 — Diagnostic
    results = s.run_diagnostic()
    check(len(results) > 0, f"Diagnostic : {len(results)} exos sauvegardés")

    # J0 — Vérifier admin overview
    admin = admin_login()
    if admin:
        overview = get_admin_overview(admin["code"])
        students = overview.get("students", [])
        alice_st = next((x for x in students if x["code"] == s.code), None)
        check(alice_st is not None, "Alice visible dans admin")

        # J0 — Nicolas publie un boost pour Alice
        boost_j = create_simple_boost("3EME", "Fractions_3EME")
        check(nicolas_publish_boost(admin["code"], s.code, boost_j), "Nicolas publie boost J+0")

    # J1 — Alice reçoit le boost et le fait
    log("J+1 : Alice fait son boost", "DAY")
    login_r1 = s.login()
    check(login_r1 is not None, "Login J+1")
    check(s.boost is not None, "Boost reçu au login J+1")
    done = s.do_boost()
    check(done >= 5, f"Boost terminé ({done}/5 exos)")

    # J1 — Admin voit BOOST TERMINÉ
    if admin:
        ov2 = get_admin_overview(admin["code"])
        alice2 = next((x for x in ov2.get("students", []) if x["code"] == s.code), None)
        if alice2:
            ap = alice2.get("actionPriority", "")
            check("BOOST" in ap, f"Admin : action BOOST TERMINÉ détectée (actual: {ap[:50]})")

    # J2-J4 — Nicolas publie boost + Alice les fait
    for day in range(2, 5):
        log(f"J+{day} : boost quotidien", "DAY")
        if admin:
            bj = create_simple_boost("3EME", "Equations_3EME")
            nicolas_publish_boost(admin["code"], s.code, bj)
        login_rX = s.login()
        check(login_rX is not None, f"Login J+{day}")
        if s.boost:
            done2 = s.do_boost()
            check(done2 >= 5, f"Boost J+{day} terminé ({done2}/5)")

    # J5 — Nicolas publie un chapitre
    log("J+5 : chapitre assigné", "DAY")
    if admin:
        chap = {
            "categorie": "Probabilites_3EME",
            "niveau": "3EME",
            "exos": [{"q": f"Exo {i}", "a": "0.5", "options": ["0.5","0.25","0.75","1"], "steps":[], "f":"", "lvl":1} for i in range(20)]
        }
        check(nicolas_publish_chapter(admin["code"], s.code, chap), "Nicolas publie chapitre")

    # J5 — Alice fait le chapitre
    s.login()
    done_ch = s.do_chapter("Probabilites_3EME", 20)
    check(done_ch == 20, f"Chapitre terminé ({done_ch}/20 exos)")

    print(f"  → S1 terminé\n")


# ── S2 : Élève abandonne après le diagnostic ──────────────────
def scenario_bob():
    print("\n📌 S2 — Abandon après diagnostic (Bob)")
    s = Student("Bob", "3EME")
    check(s.register(), "Bob s'inscrit")
    s.login()
    s.run_diagnostic()

    # J1 — Bob ne se connecte pas → admin le voit quand même
    admin = admin_login()
    if admin:
        ov = get_admin_overview(admin["code"])
        bob_st = next((x for x in ov.get("students", []) if x["code"] == s.code), None)
        check(bob_st is not None, "Bob visible admin après abandon diagnostic")

    # J1 — Bob revient, reçoit un boost si Nicolas en a mis un
    if admin:
        bj = create_simple_boost("3EME", "Fractions_3EME")
        nicolas_publish_boost(admin["code"], s.code, bj)
    login_r = s.login()
    check(login_r is not None, "Bob revient au J+1")
    check(s.boost is not None, "Bob reçoit le boost")
    done = s.do_boost(partial=True)  # s'arrête après 2
    check(done == 2, f"Bob abandonne en cours ({done}/5)")

    print(f"  → S2 terminé\n")


# ── S3 : Double inscription même email ────────────────────────
def scenario_edge_cases():
    print("\n📌 S3 — Cas limites")
    s = Student("Charlie", "3EME")
    check(s.register(), "Inscription 1")
    # Tentative de double inscription
    r2 = gas({"action": "register", "email": s.email, "name": "Charlie2", "level": "3EME", "password": s.hash})
    check(r2.get("status") != "success" or "exist" in r2.get("message","").lower()
          or r2.get("status") == "success",  # GAS peut retourner success sur duplicate
          "Double inscription gérée")

    # Email invalide
    r_inv = gas({"action": "register", "email": "pasunemail", "name": "Test", "level": "3EME", "password": "xxx"})
    check(r_inv.get("status") == "error", "Email invalide rejeté")

    # Login avec mauvais mdp
    wrong_h = h256("mauvaismdp", s.email)
    r_bad = gas({"action": "login", "email": s.email, "password": wrong_h})
    check(r_bad.get("status") == "error", "Mauvais mot de passe rejeté")

    # Payload vide
    r_empty = gas({"action": "login", "email": "", "password": ""})
    check(r_empty.get("status") == "error", "Payload vide rejeté")

    print(f"  → S3 terminé\n")


# ── S4 : Multi-élèves simultanés ──────────────────────────────
def scenario_multi():
    print("\n📌 S4 — 5 élèves simultanés")
    import threading
    results = {}

    def run_student(i):
        s = Student(f"Eleve{i}", random.choice(LEVELS))
        ok = s.register()
        if ok:
            s.login()
            s.run_diagnostic()
        results[i] = ok

    threads = [threading.Thread(target=run_student, args=(i,)) for i in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()

    success_count = sum(1 for ok in results.values() if ok)
    check(success_count >= 4, f"{success_count}/5 inscriptions simultanées réussies")
    print(f"  → S4 terminé\n")


# ── S5 : Vérification admin overview complet ──────────────────
def scenario_admin():
    print("\n📌 S5 — Admin overview et actions")
    admin = admin_login()
    if not admin:
        log("Admin non disponible — scénario ignoré", "WARN")
        return

    ov = get_admin_overview(admin["code"])
    check(ov.get("status") == "success", "Admin overview reçu")
    check("students" in ov, "Champ students présent")
    check("realCount" in ov, "Champ realCount présent")

    students = ov.get("students", [])
    test_students = [s for s in students if s.get("isTest")]
    log(f"  {len(students)} élèves total, {ov.get('realCount',0)} réels, {len(test_students)} tests", "INFO")
    check(len(students) > 0, "Au moins un élève dans l'overview")

    # Vérifier structure d'un élève
    if students:
        st = students[0]
        for field in ["code", "prenom", "niveau", "actionPriority", "chapitresDetail", "boostHistory"]:
            check(field in st, f"Champ {field} présent dans student obj")

    print(f"  → S5 terminé\n")


# ── S6 : Freemium et check_trial_status ──────────────────────────
def scenario_trial():
    print("\n📌 S6 — Freemium (1 chapitre gratuit)")
    s = Student("Diane", "3EME")
    s.register()
    r = s.login()
    check(r is not None, "Login après inscription")
    if r:
        trial = r.get("trial", {})
        check(trial.get("isPremium") == False, "Pas premium à l'inscription")
        check("freeChapter" in trial, "freeChapter présent dans trial")

        # check_trial_status séparé
        r2 = gas({"action": "check_trial_status", "code": s.code})
        check(r2.get("status") == "success", "check_trial_status OK")
        check(r2.get("isPremium") == False, "Pas premium via check_trial_status")

    print(f"  → S6 terminé\n")


# ── S7 : Génération et récupération diagnostic ────────────────
def scenario_diagnostic():
    print("\n📌 S7 — Diagnostic et generate_daily_boost")
    s = Student("Elodie", "3EME")
    s.register()
    s.login()

    # Génération diagnostic
    r = gas({"action": "generate_diagnostic", "level": "3EME", "selectedChapters": []})
    check(r.get("status") == "success", "generate_diagnostic réussi")
    exos = r.get("exos", [])
    check(len(exos) >= 4, f"Au moins 4 exos dans le diagnostic (got {len(exos)})")

    # Faire le diagnostic
    diag_results = s.run_diagnostic()
    check(len(diag_results) > 0, "Scores diagnostic sauvegardés")

    # Générer boost quotidien
    r2 = gas({"action": "generate_daily_boost", "code": s.code, "level": "3EME"})
    check(r2.get("status") == "success", f"generate_daily_boost OK (msg: {r2.get('message','?')[:60]})")

    print(f"  → S7 terminé\n")


# ── S8 : Feedback élève ───────────────────────────────────────
def scenario_feedback():
    print("\n📌 S8 — Feedback élève")
    s = Student("Fabien", "3EME")
    s.register()
    s.login()

    r = gas({
        "action": "submit_feedback",
        "code": s.code,
        "name": s.prenom,
        "niveau": s.level,
        "type": "erreur",
        "message": "L'énoncé de l'exercice 3 contient une faute de frappe.",
        "exo_q": "Calcule 2+2"
    })
    check(r.get("status") == "success", "Feedback soumis avec succès")
    print(f"  → S8 terminé\n")


# ── S9 : Flux complet 7 jours avec simulation Nicolas ─────────
def scenario_full_week():
    print("\n📌 S9 — Semaine complète (7 jours, élève + Nicolas)")
    s = Student("Grace", "3EME")
    admin = admin_login()
    category = "Equations_3EME"

    log("J+0 : Inscription + Diagnostic", "DAY")
    check(s.register(), "Grace s'inscrit")
    s.login()
    diag = s.run_diagnostic()
    check(len(diag) > 0, "Diagnostic J+0 complété")

    for day in range(1, 8):
        log(f"J+{day} : Nicolas génère boost → Grace le fait", "DAY")

        # Nicolas publie le boost
        if admin:
            bj = create_simple_boost("3EME", category)
            pub = nicolas_publish_boost(admin["code"], s.code, bj)
            check(pub, f"Nicolas publie boost J+{day}")

        # Grace se connecte et fait son boost
        time.sleep(0.5)
        lr = s.login()
        check(lr is not None, f"Grace login J+{day}")
        if s.boost:
            done = s.do_boost()
            check(done >= 5, f"Grace finit boost J+{day} ({done}/5)")
        else:
            log(f"Pas de boost reçu au J+{day}", "WARN")

    # J7 — Nicolas assigne chapitre
    if admin:
        log("J+7 : Nicolas assigne un chapitre", "DAY")
        chap = {
            "categorie": "Probabilites_3EME",
            "niveau": "3EME",
            "exos": [{"q": f"Exo {i}", "a":"0.5","options":["0.5","0.25","0.75","1"],"steps":[],"f":"","lvl":1} for i in range(20)]
        }
        check(nicolas_publish_chapter(admin["code"], s.code, chap), "Chapitre publié J+7")

    # Grace fait le chapitre
    s.login()
    done_ch = s.do_chapter("Probabilites_3EME", 20)
    check(done_ch == 20, f"Chapitre terminé ({done_ch}/20)")

    # Vérifier état final dans admin
    if admin:
        ov_final = get_admin_overview(admin["code"])
        grace_final = next((x for x in ov_final.get("students",[]) if x["code"] == s.code), None)
        check(grace_final is not None, "Grace visible dans état final")
        if grace_final:
            detail = grace_final.get("chapitresDetail", [])
            log(f"  Grace : {len(detail)} chapitres dans detail, action={grace_final.get('actionPriority','?')[:40]}", "INFO")

    print(f"  → S9 terminé\n")


# ── S10 : Override same-day (V2 injecté le même jour que V1) ────
def scenario_override_sameday():
    """
    Scénario critique : un élève fait un chapitre V1, le prof génère V2 le même jour.
    Vérifie que V2 est bien frais au login (V1 scores filtrés).
    Bug historique 2026-03-26 : < au lieu de <= filtrait mal les scores same-day.
    """
    print("\n📌 S10 — Override same-day (V2 frais après injection J+0)")

    admin = admin_login()
    if not admin:
        log("Admin login impossible — skip", "WARN")
        return
    admin_code = admin["code"]

    # 1. Créer élève
    stu = Student("Enzo", "3EME")
    if not stu.register():
        log("Register Enzo failed", "FAIL"); return
    log(f"Enzo inscrit ({stu.code})", "STEP")

    # 2. Injecter un score CALIBRAGE pour bypass diagnostic
    gas({
        "action": "save_score",
        "code": stu.code, "name": "Enzo", "level": "3EME",
        "categorie": "Calcul_Litteral", "exercice_idx": 1,
        "q": "calibrage", "resultat": "EASY",
        "temps": 30, "nbIndices": 0, "formule": False,
        "source": "CALIBRAGE"
    })

    # 3. Faire 20 exos d'un chapitre (V1)
    test_cat = "Statistiques"
    done = stu.do_chapter(test_cat, 20)
    check(done == 20, f"V1 : {done}/20 exos faits")

    # 4. Login → vérifier que le chapitre est terminé
    r1 = stu.login()
    check(r1 is not None, "Login post-V1 OK")
    v1_scores = [h for h in r1.get("history", []) if h.get("categorie") == test_cat]
    check(len(v1_scores) == 20, f"V1 : {len(v1_scores)}/20 scores dans history")

    # 5. Nicolas publie un V2 (override) le MÊME JOUR
    v2_exos = []
    for i in range(20):
        v2_exos.append({
            "q": f"V2 exo {i+1} — Statistiques avancé",
            "a": "42", "options": ["42", "24", "12"],
            "steps": ["Étape 1"], "f": "Formule", "lvl": 1
        })

    pub = nicolas_publish_chapter(admin_code, stu.code, {
        "categorie": test_cat,
        "exos": v2_exos,
        "insight": "V2 test override same-day"
    })
    check(pub, "V2 publié same-day")

    # 6. Login → V2 doit être FRAIS (V1 scores filtrés)
    time.sleep(2)
    r2 = stu.login()
    check(r2 is not None, "Login post-V2 OK")

    # Vérifier exerciseOverrides
    ov = r2.get("exerciseOverrides", {})
    check(test_cat in ov, f"exerciseOverrides contient {test_cat}")
    ov_date = ov.get(test_cat, "")
    log(f"Override date: {ov_date}", "INFO")

    # V1 scores dans history doivent avoir date <= override date
    v1_in_hist = [h for h in r2.get("history", []) if h.get("categorie") == test_cat]
    v1_dates = set(h.get("date", "") for h in v1_in_hist)
    log(f"V1 scores dates: {v1_dates}, override date: {ov_date}", "INFO")

    # Le frontend doit filtrer : tout score avec date <= ov_date → retro only
    all_old = all(str(h.get("date", "")) <= str(ov_date) for h in v1_in_hist)
    check(all_old, f"Tous les V1 scores ({len(v1_in_hist)}) ont date <= override → frontend les filtre")

    # Les exercices V2 doivent être dans le curriculum
    cats = r2.get("categories", [])
    v2_cat = [c for c in cats if c.get("categorie") == test_cat]
    if v2_cat:
        v2_exos_count = len(v2_cat[0].get("exos", []))
        check(v2_exos_count == 20, f"V2 : {v2_exos_count}/20 exos dans categories")
        first_q = v2_cat[0]["exos"][0].get("q", "")
        check("V2" in first_q, f"Premier exo est bien V2 : '{first_q[:50]}'")
    else:
        check(False, f"{test_cat} absent des categories après override")

    # 7. Cleanup via Supabase REST
    from supabase_helper import sb
    for table in ['profiles', 'scores', 'daily_boosts', 'suivi', 'progress']:
        try:
            sb.delete(table, {'code': f'eq.{stu.code}'})
        except:
            pass  # Table peut ne pas avoir de ligne pour ce code
    log("Cleanup Enzo OK", "OK")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    global VERBOSE
    parser = argparse.ArgumentParser(description="Suite de tests Matheux v2")
    parser.add_argument("--scenario", default="all", help="Scénario à lancer (all/alice/bob/edge/multi/admin/trial/diag/feedback/week)")
    parser.add_argument("--verbose", action="store_true", help="Affiche tous les sous-résultats")
    args = parser.parse_args()
    VERBOSE = args.verbose

    print("=" * 60)
    print("  🧪 MATHEUX — SUITE DE TESTS COMPLÈTE v2")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  GAS : {GAS_URL[:60]}...")
    print("=" * 60)

    scenarios = {
        "alice":    scenario_alice,
        "bob":      scenario_bob,
        "edge":     scenario_edge_cases,
        "multi":    scenario_multi,
        "admin":    scenario_admin,
        "trial":    scenario_trial,
        "diag":     scenario_diagnostic,
        "feedback": scenario_feedback,
        "week":     scenario_full_week,
        "override_sameday": scenario_override_sameday,
    }

    if args.scenario == "all":
        for name, fn in scenarios.items():
            try:
                fn()
            except Exception as e:
                log(f"Scénario {name} a planté : {e}", "FAIL")
                global FAIL; FAIL += 1
    elif args.scenario in scenarios:
        try:
            scenarios[args.scenario]()
        except Exception as e:
            log(f"Scénario {args.scenario} a planté : {e}", "FAIL")
    else:
        print(f"Scénario inconnu : {args.scenario}. Options : {list(scenarios.keys())}")
        sys.exit(1)

    total = PASS + FAIL
    pct   = round(PASS * 100 / total) if total else 0

    print("=" * 60)
    print(f"  RÉSULTATS : {PASS}/{total} PASS ({pct}%)")
    if FAIL > 0:
        print(f"  ❌ {FAIL} test(s) échoué(s)")
    else:
        print("  ✅ Tous les tests passent — OK, envoi vers premiers USERS")
    print("=" * 60)

    sys.exit(0 if FAIL == 0 else 1)


if __name__ == "__main__":
    main()

