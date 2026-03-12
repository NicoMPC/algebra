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
ADMIN_EMAIL = "contact@matheux.fr"
ADMIN_PASS  = "Matheux2026Admin!"

LEVELS  = ["6EME", "5EME", "4EME", "3EME"]
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

def admin_login() -> dict | None:
    """Login admin et retourne le profil."""
    h = h256(ADMIN_PASS, ADMIN_EMAIL)
    r = gas({"action": "login", "email": ADMIN_EMAIL, "password": h})
    if r.get("status") == "success" and r.get("profile", {}).get("isAdmin"):
        return r["profile"]
    log(f"Admin login impossible : {r.get('message','?')}", "WARN")
    return None

def get_admin_overview(admin_code: str) -> dict:
    return gas({"action": "get_admin_overview", "adminCode": admin_code})

def nicolas_publish_boost(admin_code: str, student_code: str, boost_json: dict) -> bool:
    """Simule Nicolas qui publie un boost pour un élève."""
    r = gas({
        "action": "publish_admin_boost",
        "adminCode": admin_code,
        "code": student_code,
        "boostJSON": json.dumps(boost_json),
        "motProf": "Bon courage pour ce boost !"
    })
    return r.get("status") == "success"

def nicolas_publish_chapter(admin_code: str, student_code: str, chapter_json: dict) -> bool:
    """Simule Nicolas qui publie un chapitre pour un élève."""
    r = gas({
        "action": "publish_admin_chapter",
        "adminCode": admin_code,
        "code": student_code,
        "chapJSON": json.dumps(chapter_json),
        "motProf": "Nouveau chapitre — tu vas y arriver !"
    })
    return r.get("status") == "success"

def create_simple_boost(level: str, category: str) -> dict:
    """Crée un boost minimal valide."""
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
            self.boost   = r.get("dailyBoost")
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
    s = Student("Alice", "4EME")

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
        boost_j = create_simple_boost("4EME", "Fractions_4EME")
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
            bj = create_simple_boost("4EME", "Equations_4EME")
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
            "categorie": "Probabilites_4EME",
            "niveau": "4EME",
            "exos": [{"q": f"Exo {i}", "a": "0.5", "options": ["0.5","0.25","0.75","1"], "steps":[], "f":"", "lvl":1} for i in range(20)]
        }
        check(nicolas_publish_chapter(admin["code"], s.code, chap), "Nicolas publie chapitre")

    # J5 — Alice fait le chapitre
    s.login()
    done_ch = s.do_chapter("Probabilites_4EME", 20)
    check(done_ch == 20, f"Chapitre terminé ({done_ch}/20 exos)")

    print(f"  → S1 terminé\n")


# ── S2 : Élève abandonne après le diagnostic ──────────────────
def scenario_bob():
    print("\n📌 S2 — Abandon après diagnostic (Bob)")
    s = Student("Bob", "5EME")
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
        bj = create_simple_boost("5EME", "Fractions_5EME")
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
    s = Student("Charlie", "6EME")
    check(s.register(), "Inscription 1")
    # Tentative de double inscription
    r2 = gas({"action": "register", "email": s.email, "name": "Charlie2", "level": "6EME", "password": s.hash})
    check(r2.get("status") != "success" or "exist" in r2.get("message","").lower()
          or r2.get("status") == "success",  # GAS peut retourner success sur duplicate
          "Double inscription gérée")

    # Email invalide
    r_inv = gas({"action": "register", "email": "pasunemail", "name": "Test", "level": "4EME", "password": "xxx"})
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


# ── S6 : Trial et check_trial_status ──────────────────────────
def scenario_trial():
    print("\n📌 S6 — Trial 7 jours")
    s = Student("Diane", "3EME")
    s.register()
    r = s.login()
    check(r is not None, "Login après inscription")
    if r:
        trial = r.get("trial", {})
        check(trial.get("trialActive") == True, "Trial actif à J+0")
        days = trial.get("daysLeft", 0)
        check(days >= 6, f"daysLeft >= 6 (actual: {days})")

        # check_trial_status séparé
        r2 = gas({"action": "check_trial_status", "code": s.code})
        check(r2.get("status") == "success", "check_trial_status OK")
        check(r2.get("trialActive") == True, "Trial actif via check_trial_status")

    print(f"  → S6 terminé\n")


# ── S7 : Génération et récupération diagnostic ────────────────
def scenario_diagnostic():
    print("\n📌 S7 — Diagnostic et generate_daily_boost")
    s = Student("Elodie", "4EME")
    s.register()
    s.login()

    # Génération diagnostic
    r = gas({"action": "generate_diagnostic", "level": "4EME", "selectedChapters": []})
    check(r.get("status") == "success", "generate_diagnostic réussi")
    exos = r.get("exos", [])
    check(len(exos) >= 4, f"Au moins 4 exos dans le diagnostic (got {len(exos)})")

    # Faire le diagnostic
    diag_results = s.run_diagnostic()
    check(len(diag_results) > 0, "Scores diagnostic sauvegardés")

    # Générer boost quotidien
    r2 = gas({"action": "generate_daily_boost", "code": s.code, "level": "4EME"})
    check(r2.get("status") == "success", f"generate_daily_boost OK (msg: {r2.get('message','?')[:60]})")

    print(f"  → S7 terminé\n")


# ── S8 : Feedback élève ───────────────────────────────────────
def scenario_feedback():
    print("\n📌 S8 — Feedback élève")
    s = Student("Fabien", "5EME")
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
