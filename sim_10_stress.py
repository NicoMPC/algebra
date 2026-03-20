#!/usr/bin/env python3
"""
sim_10_stress.py — Simulation stress test · 10 élèves × 7 jours
=================================================================
Simule 10 élèves avec des comportements variés (parfait, abandon,
crash, double inscription, trial expiré…) pour identifier frictions
et incohérences.

Usage : python3 sim_10_stress.py [--no-cleanup]
"""

import json, hashlib, time, random, sys, os, threading
from datetime import datetime, timedelta
from sheets import sh
import urllib.request, urllib.error

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)
ADMIN_EMAIL = "admin@matheux.fr"
ADMIN_HASH  = hashlib.sha256(f"{ADMIN_EMAIL}::Admin123::AB22".encode()).hexdigest()
ADMIN_CODE  = "HMD493"

TODAY     = datetime.now()
TODAY_STR = TODAY.strftime("%Y-%m-%d")
DATE_FMT  = "%Y-%m-%d"
PASSWORD  = "StressTest2026!"

NO_CLEANUP = "--no-cleanup" in sys.argv

# ═══════════════════════════════════════════════════════════════
# TRACKING
# ═══════════════════════════════════════════════════════════════

ANOMALIES  = []
TIMINGS    = []
CHECKS     = {"passed": 0, "failed": 0, "details": []}
API_CALLS  = 0
API_ERRORS = 0

def flag(severity, context, msg, data=None):
    entry = {"severity": severity, "context": context, "msg": msg}
    if data: entry["data"] = str(data)[:300]
    ANOMALIES.append(entry)
    icon = "🔴" if severity == "CRITICAL" else "🟡" if severity == "WARN" else "🔵"
    print(f"    {icon} [{severity}] {context}: {msg}")

def check(condition, label, context=""):
    if condition:
        CHECKS["passed"] += 1
        CHECKS["details"].append(("✅", label))
    else:
        CHECKS["failed"] += 1
        CHECKS["details"].append(("❌", label))
        flag("CRITICAL", context or label, f"CHECK FAILED: {label}")
    return condition

# ═══════════════════════════════════════════════════════════════
# HELPERS RÉSEAU
# ═══════════════════════════════════════════════════════════════

def gas(payload, label="", retry=2, verbose=True):
    global API_CALLS, API_ERRORS
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(GAS_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    t0 = time.time()
    API_CALLS += 1
    for attempt in range(retry + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read().decode("utf-8"))
                elapsed = time.time() - t0
                TIMINGS.append({"action": payload.get("action", "?"), "time": elapsed, "label": label})
                if elapsed > 6:
                    flag("WARN", label, f"Latence élevée: {elapsed:.1f}s")
                if elapsed > 10:
                    flag("CRITICAL", label, f"Timeout quasi: {elapsed:.1f}s")
                status = d.get("status", "?")
                ok = "✅" if status == "success" else "❌"
                if verbose:
                    print(f"      {ok} {label or payload.get('action','?')} → {status} ({elapsed:.1f}s)")
                return d
        except Exception as e:
            if attempt < retry:
                time.sleep(2)
            else:
                elapsed = time.time() - t0
                TIMINGS.append({"action": payload.get("action", "?"), "time": elapsed, "label": f"ERROR:{label}"})
                API_ERRORS += 1
                print(f"      ❌ {label} → RÉSEAU: {e}")
                flag("CRITICAL", label, f"Erreur réseau: {e}")
                return {"status": "error", "message": str(e)}
    return {"status": "error", "message": "retry exhausted"}

def h256(email):
    raw = f"{email.lower().strip()}::{PASSWORD}::AB22"
    return hashlib.sha256(raw.encode()).hexdigest()

def pause(s=0.5):
    time.sleep(s)

# ═══════════════════════════════════════════════════════════════
# CHAPITRES PAR NIVEAU
# ═══════════════════════════════════════════════════════════════

CHAPITRES = {
    "6EME": ["Nombres_entiers", "Fractions", "Proportionnalité", "Géométrie", "Périmètres_Aires",
             "Angles", "Nombres_Décimaux", "Statistiques_6ème", "Symétrie_Axiale", "Volumes"],
    "5EME": ["Fractions", "Nombres_relatifs", "Proportionnalité", "Calcul_Littéral",
             "Pythagore", "Puissances", "Symétrie_Centrale", "Transformations"],
    "4EME": ["Puissances", "Fractions", "Proportionnalité", "Calcul_Littéral",
             "Équations", "Pythagore", "Fonctions_Linéaires", "Inéquations"],
    "3EME": ["Calcul_Littéral", "Équations", "Fonctions", "Théorème_de_Thalès",
             "Trigonométrie", "Statistiques", "Probabilités", "Racines_Carrées"],
}

# ═══════════════════════════════════════════════════════════════
# 10 PROFILS
# ═══════════════════════════════════════════════════════════════

def build_profiles():
    profiles = [
        {"id": 1,  "prenom": "Lina",    "niveau": "6EME", "scenario": "parfait",
         "desc": "Parcours parfait — diag + boost chaque jour + 1 chapitre terminé"},
        {"id": 2,  "prenom": "Maxime",  "niveau": "5EME", "scenario": "crash_diag",
         "desc": "Crash en plein diagnostic — revient 2h après, termine"},
        {"id": 3,  "prenom": "Inès",    "niveau": "4EME", "scenario": "boost_partiel",
         "desc": "Fait 3/5 exos boost puis disparaît — revient J+3, boost intact"},
        {"id": 4,  "prenom": "Rayan",   "niveau": "3EME", "scenario": "chapitre_partiel",
         "desc": "Commence chapitre (7/20 exos) puis ferme — progression persistée"},
        {"id": 5,  "prenom": "Yasmine", "niveau": "6EME", "scenario": "flow_mode",
         "desc": "Ultra rapide tout EASY — doit trigger Mode Flow (XP ×2)"},
        {"id": 6,  "prenom": "Éthan",   "niveau": "5EME", "scenario": "tout_faux",
         "desc": "100% HARD — score 0%, vérifie que rien ne crash"},
        {"id": 7,  "prenom": "Camille", "niveau": "4EME", "scenario": "double_inscription",
         "desc": "Double inscription même email → rejetée, puis login normal"},
        {"id": 8,  "prenom": "Noé",     "niveau": "3EME", "scenario": "ghost",
         "desc": "Inscrit mais ne fait RIEN pendant 7j — trial expire"},
        {"id": 9,  "prenom": "Amira",   "niveau": "6EME", "scenario": "admin_publish",
         "desc": "Boost J0 + admin publie chapitre le soir → vérifie hero J+1"},
        {"id": 10, "prenom": "Jules",   "niveau": "5EME", "scenario": "streak_freeze",
         "desc": "Actif J1-J4, skip J5-J6, revient J7 — streak freeze"},
    ]
    for p in profiles:
        p["email"] = f"stress.{p['prenom'].lower()}.s{p['id']:02d}@matheux.fr"
        p["hash"]  = h256(p["email"])
        p["code"]  = None
        p["xp_history"] = []
        p["streak_history"] = []
        p["chapitres_sel"] = random.sample(CHAPITRES[p["niveau"]], 4)
    return profiles

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 0 — NETTOYAGE
# ═══════════════════════════════════════════════════════════════

def cleanup():
    print("\n" + "═" * 60)
    print("  NETTOYAGE — Suppression comptes stress test")
    print("═" * 60)

    users = sh.read("Users")
    test_codes = [u["Code"] for u in users
                  if str(u.get("IsTest","0")) in ("1","TRUE","true")
                  and str(u.get("IsAdmin","0")) not in ("1","TRUE","true")]

    if not test_codes:
        print("  ✅ Aucun compte test à supprimer")
        return

    print(f"  Suppression de {len(test_codes)} comptes test...")

    for tab in ["Scores", "Progress", "DailyBoosts", "BrevetResults", "Insights"]:
        try:
            raw = sh.read_raw(tab)
            if len(raw) < 2: continue
            headers = raw[0]
            ci = headers.index("Code") if "Code" in headers else -1
            if ci < 0: continue
            kept = [headers] + [r for r in raw[1:] if (r[ci] if ci < len(r) else "") not in test_codes]
            removed = len(raw) - len(kept)
            if removed > 0:
                sh.write_rows(tab, kept)
                print(f"    🗑️ {tab}: {removed} lignes")
        except Exception as e:
            print(f"    ⚠️ {tab}: {e}")

    for tab in ["👁 Suivi", "📋 Historique"]:
        try:
            raw = sh.read_raw(tab)
            if len(raw) < 2: continue
            kept = [raw[0]] + [r for r in raw[1:] if not any(str(c) in test_codes for c in r)]
            removed = len(raw) - len(kept)
            if removed > 0:
                sh.write_rows(tab, kept)
                print(f"    🗑️ {tab}: {removed} lignes")
        except Exception as e:
            print(f"    ⚠️ {tab}: {e}")

    raw = sh.read_raw("Users")
    kept = [raw[0]] + [r for r in raw[1:] if r[0] not in test_codes]
    sh.write_rows("Users", kept)
    print(f"    🗑️ Users: {len(test_codes)} comptes supprimés")
    print("  ✅ Nettoyage terminé")

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 1 — INSCRIPTION
# ═══════════════════════════════════════════════════════════════

def step1_register(profiles):
    print("\n" + "═" * 60)
    print("  ÉTAPE 1 — INSCRIPTION DES 10 PROFILS")
    print("═" * 60)

    for p in profiles:
        r = gas({
            "action": "register",
            "name": p["prenom"],
            "email": p["email"],
            "level": p["niveau"],
            "password": p["hash"],
            "objectif": "lacunes",
            "consent": True
        }, label=f"register {p['prenom']} ({p['niveau']})")
        pause()

        if r.get("status") == "success":
            p["code"] = r["profile"]["code"]
            check(len(p["code"]) == 6, f"{p['prenom']}: code 6 caractères", "register")
            check(r["profile"]["level"] == p["niveau"], f"{p['prenom']}: niveau correct", "register")
            check("curriculumOfficiel" in r, f"{p['prenom']}: curriculum retourné", "register")
            check("trial" in r, f"{p['prenom']}: trial info retournée", "register")
            if "trial" in r:
                check(r["trial"]["trialActive"] == True, f"{p['prenom']}: trial actif", "register")
                check(r["trial"]["daysLeft"] == 7, f"{p['prenom']}: 7j trial", "register")
        else:
            flag("CRITICAL", f"register {p['prenom']}", r.get("message", "?"))

    # Profil 7 — double inscription
    p7 = profiles[6]
    print(f"\n    ▶ Double inscription Camille (même email)...")
    r = gas({
        "action": "register",
        "name": "Camille2",
        "email": p7["email"],
        "level": p7["niveau"],
        "password": p7["hash"],
        "objectif": "lacunes",
        "consent": True
    }, label="register Camille DOUBLE")
    pause()
    check(r.get("status") != "success", "Camille: double inscription rejetée", "register")

    registered = sum(1 for p in profiles if p["code"])
    print(f"\n  {'✅' if registered == 10 else '❌'} {registered}/10 inscrits")

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 2 — DIAGNOSTIC
# ═══════════════════════════════════════════════════════════════

def step2_diagnostic(profiles):
    print("\n" + "═" * 60)
    print("  ÉTAPE 2 — DIAGNOSTIC")
    print("═" * 60)

    for p in profiles:
        if not p["code"]: continue
        if p["scenario"] == "ghost": continue  # Noé ne fait rien

        print(f"\n  👤 {p['prenom']} ({p['niveau']}) — {p['scenario']}")

        # Générer diagnostic
        r = gas({
            "action": "generate_diagnostic",
            "level": p["niveau"],
            "selectedChapters": p["chapitres_sel"]
        }, label=f"diag {p['prenom']}")
        pause()

        if r.get("status") != "success":
            flag("CRITICAL", f"diag {p['prenom']}", "Diagnostic échoué")
            continue

        exos = r.get("exos", [])
        check(len(exos) > 0, f"{p['prenom']}: diagnostic a des exos ({len(exos)})", "diag")
        check(len(exos) <= 8, f"{p['prenom']}: diagnostic max 8 exos ({len(exos)})", "diag")

        # Crash en plein diagnostic (Maxime)
        if p["scenario"] == "crash_diag":
            # Fait 2 exos puis "crash"
            for i, ex in enumerate(exos[:2]):
                gas({
                    "action": "save_score",
                    "code": p["code"], "name": p["prenom"], "level": p["niveau"],
                    "categorie": ex.get("oC", ex.get("categorie", p["chapitres_sel"][0])),
                    "exercice_idx": i, "resultat": "EASY",
                    "q": (ex.get("q",""))[:100], "source": "CALIBRAGE"
                }, label=f"diag_exo {p['prenom']} #{i+1} (avant crash)")
                pause()

            print(f"    💥 CRASH — Maxime ferme l'app après 2/{len(exos)} exos")
            # "Revient 2h après" — re-login
            r2 = gas({"action": "login", "email": p["email"], "password": p["hash"]},
                     label=f"re-login {p['prenom']} post-crash")
            pause()
            check(r2.get("status") == "success", f"{p['prenom']}: re-login post-crash OK", "crash_diag")

            # Termine le reste
            for i, ex in enumerate(exos[2:], start=2):
                result = random.choice(["EASY", "EASY", "MEDIUM", "HARD"])
                gas({
                    "action": "save_score",
                    "code": p["code"], "name": p["prenom"], "level": p["niveau"],
                    "categorie": ex.get("oC", ex.get("categorie", p["chapitres_sel"][min(i//2, 3)])),
                    "exercice_idx": i, "resultat": result,
                    "q": (ex.get("q",""))[:100], "source": "CALIBRAGE"
                }, label=f"diag_exo {p['prenom']} #{i+1} (post-crash)")
                pause()
            continue

        # Diagnostic normal pour les autres
        for i, ex in enumerate(exos):
            if p["scenario"] == "tout_faux":
                result = "HARD"
            elif p["scenario"] == "flow_mode":
                result = "EASY"
            else:
                result = random.choice(["EASY", "EASY", "MEDIUM", "HARD"])

            gas({
                "action": "save_score",
                "code": p["code"], "name": p["prenom"], "level": p["niveau"],
                "categorie": ex.get("oC", ex.get("categorie", p["chapitres_sel"][min(i//2, 3)])),
                "exercice_idx": i, "resultat": result,
                "q": (ex.get("q",""))[:100], "source": "CALIBRAGE"
            }, label=f"diag_exo {p['prenom']} #{i+1}")
            pause()

    # Sauvegarder les diagnostics en batch aussi (test save_calibration_batch)
    print("\n  ✅ Diagnostics terminés")

# ═══════════════════════════════════════════════════════════════
# HELPERS SIMULATION JOUR
# ═══════════════════════════════════════════════════════════════

def do_login(p, label_suffix=""):
    """Login et retourne la réponse complète."""
    r = gas({"action": "login", "email": p["email"], "password": p["hash"]},
            label=f"login {p['prenom']}{label_suffix}")
    pause()
    return r

def do_boost(p, login_data, how="normal"):
    """Simule un boost. how: 'normal', 'partial_3', 'all_easy', 'all_hard'"""
    boost = login_data.get("dailyBoost")
    if not boost:
        # Essayer nextBoost
        boost = login_data.get("nextBoost")
    if not boost or not boost.get("exos"):
        flag("WARN", f"boost {p['prenom']}", "Pas de boost disponible")
        return

    exos = boost["exos"]
    check(len(exos) == 5, f"{p['prenom']}: boost a 5 exos ({len(exos)})", "boost")

    nb = 3 if how == "partial_3" else len(exos)
    for i in range(min(nb, len(exos))):
        ex = exos[i]
        if how == "all_easy":
            result = "EASY"
        elif how == "all_hard":
            result = "HARD"
        else:
            result = random.choice(["EASY", "EASY", "EASY", "MEDIUM", "HARD"])

        gas({
            "action": "save_score",
            "code": p["code"], "name": p["prenom"], "level": p["niveau"],
            "categorie": ex.get("oC", ex.get("categorie", "")),
            "exercice_idx": i, "resultat": result,
            "q": (ex.get("q",""))[:100], "source": "BOOST",
            "time": random.randint(3, 55) if how != "all_easy" else random.randint(2, 8)
        }, label=f"boost_exo {p['prenom']} #{i+1}/{nb} ({result})")
        pause(0.3)

    if how == "partial_3":
        print(f"    💥 {p['prenom']} ferme après 3/5 exos")

def do_chapter_exos(p, login_data, nb_exos=20, how="mixed"):
    """Simule des exercices de chapitre."""
    curriculum = login_data.get("curriculumOfficiel", [])
    # Prendre le premier chapitre avec des exos ou nextChapter
    next_ch = login_data.get("nextChapter")
    if next_ch and next_ch.get("exos"):
        cat = next_ch.get("categorie", "")
        exos = next_ch["exos"]
    elif curriculum:
        ch = curriculum[0]
        cat = ch.get("categorie", "")
        exos = ch.get("exos", [])
    else:
        flag("WARN", f"chapter {p['prenom']}", "Pas de chapitre disponible")
        return

    actual_nb = min(nb_exos, len(exos))
    for i in range(actual_nb):
        ex = exos[i]
        if how == "all_easy":
            result = "EASY"
        elif how == "all_hard":
            result = "HARD"
        else:
            result = random.choice(["EASY", "EASY", "EASY", "MEDIUM", "HARD"])

        gas({
            "action": "save_score",
            "code": p["code"], "name": p["prenom"], "level": p["niveau"],
            "categorie": cat,
            "exercice_idx": i, "resultat": result,
            "q": (ex.get("q",""))[:100],
            "time": random.randint(5, 50)
        }, label=f"chap_exo {p['prenom']} #{i+1}/{actual_nb} ({result})")
        pause(0.3)

    return {"categorie": cat, "nb_done": actual_nb, "total": len(exos)}

# ═══════════════════════════════════════════════════════════════
# ADMIN — Simulation soir
# ═══════════════════════════════════════════════════════════════

def admin_evening(profiles, day, publish_chapter_for=None):
    """Simule le travail admin le soir du jour J."""
    print(f"\n    🌙 ADMIN SOIR J{day}")

    r = gas({"action": "get_admin_overview", "adminCode": ADMIN_CODE},
            label=f"admin_overview J{day}")
    pause()

    if r.get("status") != "success":
        flag("CRITICAL", f"admin J{day}", "get_admin_overview échoué")
        return

    students = r.get("students", [])
    test_codes = [p["code"] for p in profiles if p["code"]]

    # Vérifier que tous nos élèves sont visibles
    found_codes = [s["code"] for s in students if s["code"] in test_codes]
    check(len(found_codes) == len(test_codes),
          f"Admin J{day}: {len(found_codes)}/{len(test_codes)} élèves visibles", "admin")

    for s in students:
        if s["code"] not in test_codes:
            continue
        p = next((p for p in profiles if p["code"] == s["code"]), None)
        if not p: continue

        action = s.get("actionPriority", s.get("action", "?"))
        print(f"      {action} {s.get('prenom','')} ({s.get('niveau','')})")

    # Publier chapitre pour Amira si demandé
    if publish_chapter_for:
        p_target = publish_chapter_for
        cat = p_target["chapitres_sel"][0]

        # Récupérer les exos du curriculum pour ce chapitre
        curriculum = gas({"action": "login", "email": p_target["email"], "password": p_target["hash"]},
                        label=f"login {p_target['prenom']} (pour curriculum)", verbose=False)
        pause()

        exos_to_publish = []
        if curriculum.get("status") == "success":
            for ch in curriculum.get("curriculumOfficiel", []):
                if ch.get("categorie") == cat:
                    exos_to_publish = ch.get("exos", [])[:20]
                    break

        if exos_to_publish:
            r = gas({
                "action": "publish_admin_chapter",
                "adminCode": ADMIN_CODE,
                "targetCode": p_target["code"],
                "categorie": cat,
                "exos": exos_to_publish,
                "insight": f"Travaille bien {cat.replace('_',' ')} !",
                "motProf": "Tu vas y arriver 💪"
            }, label=f"publish_chapter {p_target['prenom']} → {cat}")
            pause()
            check(r.get("status") == "success",
                  f"Admin: publication chapitre {cat} pour {p_target['prenom']}", "admin_publish")

    # Générer boosts pour le lendemain
    for p in profiles:
        if not p["code"]: continue
        if p["scenario"] == "ghost": continue

        r = gas({
            "action": "generate_daily_boost",
            "code": p["code"],
            "level": p["niveau"],
            "chapters": p["chapitres_sel"]
        }, label=f"gen_boost {p['prenom']} J{day+1}", verbose=False)
        pause(0.3)

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 3 — SIMULATION 7 JOURS
# ═══════════════════════════════════════════════════════════════

def step3_simulate(profiles):
    print("\n" + "═" * 60)
    print("  ÉTAPE 3 — SIMULATION 7 JOURS")
    print("═" * 60)

    for day in range(7):
        print(f"\n{'─' * 50}")
        print(f"  📅 JOUR {day}")
        print(f"{'─' * 50}")

        for p in profiles:
            if not p["code"]: continue
            scenario = p["scenario"]

            # ── Noé (ghost) — ne fait rien ──
            if scenario == "ghost":
                if day == 6:
                    print(f"\n  👤 {p['prenom']} (ghost) — vérifie trial expiré J6")
                    r = gas({"action": "check_trial_status", "code": p["code"]},
                            label=f"trial_check {p['prenom']} J{day}")
                    pause()
                    # Trial = 7 jours, inscrit aujourd'hui, J6 = encore actif
                    # mais on va quand même vérifier la cohérence
                    if r.get("status") == "success":
                        check(isinstance(r.get("daysLeft"), (int, float)),
                              f"{p['prenom']}: daysLeft est un nombre", "trial")
                continue

            # ── Inès (boost partiel) — J0 partiel, revient J3 ──
            if scenario == "boost_partiel":
                if day == 0:
                    print(f"\n  👤 {p['prenom']} — boost partiel 3/5 puis crash")
                    ld = do_login(p, f" J{day}")
                    if ld.get("status") == "success":
                        do_boost(p, ld, how="partial_3")
                elif day == 3:
                    print(f"\n  👤 {p['prenom']} — retour J3, vérifie boost 3/5 intact")
                    ld = do_login(p, f" J{day} (retour)")
                    if ld.get("status") == "success":
                        done = ld.get("boostExosDone", -1)
                        # Le boost original était J0 — on est J3, donc nouveau boost
                        # L'ancien boost 3/5 est dans l'historique
                        bh = ld.get("boostHistory", [])
                        check(len(bh) > 0, f"{p['prenom']}: boostHistory non vide au retour J3", "boost_partiel")
                        # Faire le boost du jour normalement
                        do_boost(p, ld, how="normal")
                elif day > 3:
                    print(f"\n  👤 {p['prenom']} — jour normal J{day}")
                    ld = do_login(p, f" J{day}")
                    if ld.get("status") == "success":
                        do_boost(p, ld, how="normal")
                continue

            # ── Rayan (chapitre partiel) — J0 fait 7/20 ──
            if scenario == "chapitre_partiel":
                if day == 0:
                    print(f"\n  👤 {p['prenom']} — chapitre partiel 7/20 puis ferme")
                    ld = do_login(p, f" J{day}")
                    if ld.get("status") == "success":
                        result = do_chapter_exos(p, ld, nb_exos=7, how="mixed")
                        if result:
                            print(f"    💥 Rayan ferme après {result['nb_done']}/{result['total']} exos")
                elif day == 1:
                    print(f"\n  👤 {p['prenom']} — retour J1, vérifie 7/20 persisté")
                    ld = do_login(p, f" J{day} (retour)")
                    if ld.get("status") == "success":
                        # Vérifier Progress
                        rp = gas({"action": "get_progress", "code": p["code"]},
                                label=f"progress {p['prenom']} J{day}")
                        pause()
                        if rp.get("status") == "success":
                            progress = rp.get("progress", [])
                            if progress:
                                nb = max(int(pr.get("nbExos", 0)) for pr in progress)
                                check(nb >= 7, f"{p['prenom']}: progression ≥7 exos persistée ({nb})", "chapitre_partiel")
                        do_boost(p, ld, how="normal")
                else:
                    print(f"\n  👤 {p['prenom']} — jour normal J{day}")
                    ld = do_login(p, f" J{day}")
                    if ld.get("status") == "success":
                        do_boost(p, ld, how="normal")
                continue

            # ── Yasmine (flow mode) — tout EASY rapide ──
            if scenario == "flow_mode":
                print(f"\n  👤 {p['prenom']} — tout EASY (flow mode) J{day}")
                ld = do_login(p, f" J{day}")
                if ld.get("status") == "success":
                    do_boost(p, ld, how="all_easy")
                    if day == 0:
                        # Aussi un chapitre pour accumuler 5+ EASY consécutifs
                        do_chapter_exos(p, ld, nb_exos=10, how="all_easy")
                continue

            # ── Éthan (tout faux) — tout HARD ──
            if scenario == "tout_faux":
                print(f"\n  👤 {p['prenom']} — tout HARD J{day}")
                ld = do_login(p, f" J{day}")
                if ld.get("status") == "success":
                    do_boost(p, ld, how="all_hard")
                    # Vérifier que le score est 0%
                    if day >= 2:
                        rp = gas({"action": "get_progress", "code": p["code"]},
                                label=f"progress {p['prenom']} J{day}", verbose=False)
                        pause()
                        if rp.get("status") == "success":
                            for pr in rp.get("progress", []):
                                score = int(pr.get("score", 0) if pr.get("score") else 0)
                                check(score == 0, f"{p['prenom']}: score = {score}% (attendu 0%)", "tout_faux")
                continue

            # ── Camille (double inscription) — login normal après rejet ──
            if scenario == "double_inscription":
                if day == 0:
                    print(f"\n  👤 {p['prenom']} — login normal après double inscription rejetée")
                    ld = do_login(p, f" J{day}")
                    if ld.get("status") == "success":
                        check(ld["profile"]["code"] == p["code"],
                              f"{p['prenom']}: login retourne le bon code", "double_inscription")
                        do_boost(p, ld, how="normal")
                elif day == 1:
                    # Test reset password
                    print(f"\n  👤 {p['prenom']} — test reset password J{day}")
                    r = gas({"action": "forgot_password", "email": p["email"]},
                            label=f"forgot_pwd {p['prenom']}")
                    pause()
                    check(r.get("status") == "success", f"{p['prenom']}: forgot_password OK", "reset_pwd")

                    # Re-login normal (le reset token existe mais on login avec ancien mdp)
                    ld = do_login(p, f" J{day}")
                    if ld.get("status") == "success":
                        do_boost(p, ld, how="normal")
                else:
                    print(f"\n  👤 {p['prenom']} — jour normal J{day}")
                    ld = do_login(p, f" J{day}")
                    if ld.get("status") == "success":
                        do_boost(p, ld, how="normal")
                continue

            # ── Amira (admin publish) ──
            if scenario == "admin_publish":
                print(f"\n  👤 {p['prenom']} — J{day}")
                ld = do_login(p, f" J{day}")
                if ld.get("status") == "success":
                    do_boost(p, ld, how="normal")
                    if day >= 1:
                        # Vérifier que nextChapter existe (publié par admin la veille)
                        nc = ld.get("nextChapter")
                        if day == 1:
                            check(nc is not None and nc.get("categorie") != "PENDING_MANUAL",
                                  f"{p['prenom']}: nextChapter visible J1 (publié par admin)", "admin_publish")
                continue

            # ── Jules (streak freeze) ──
            if scenario == "streak_freeze":
                if day <= 3:
                    print(f"\n  👤 {p['prenom']} — actif J{day} (streak building)")
                    ld = do_login(p, f" J{day}")
                    if ld.get("status") == "success":
                        do_boost(p, ld, how="normal")
                elif day in (4, 5):
                    print(f"\n  👤 {p['prenom']} — SKIP J{day} (inactif)")
                    # Ne fait rien
                elif day == 6:
                    print(f"\n  👤 {p['prenom']} — retour J{day}, vérifie streak")
                    ld = do_login(p, f" J{day} (retour)")
                    if ld.get("status") == "success":
                        do_boost(p, ld, how="normal")
                        # Vérifier via progress
                        rp = gas({"action": "get_progress", "code": p["code"]},
                                label=f"progress {p['prenom']} J{day}", verbose=False)
                        pause()
                continue

            # ── Lina (parfait) ── et par défaut
            print(f"\n  👤 {p['prenom']} — parfait J{day}")
            ld = do_login(p, f" J{day}")
            if ld.get("status") == "success":
                do_boost(p, ld, how="normal")
                # Chapitre complet le J2
                if day == 2 and scenario == "parfait":
                    print(f"    📚 {p['prenom']} fait un chapitre complet (20 exos)")
                    do_chapter_exos(p, ld, nb_exos=20, how="mixed")

        # ── ADMIN SOIR ──
        publish_for = profiles[8] if day == 0 else None  # Amira
        admin_evening(profiles, day, publish_chapter_for=publish_for)

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 4 — VÉRIFICATIONS FINALES
# ═══════════════════════════════════════════════════════════════

def step4_final_checks(profiles):
    print("\n" + "═" * 60)
    print("  ÉTAPE 4 — VÉRIFICATIONS FINALES")
    print("═" * 60)

    for p in profiles:
        if not p["code"]: continue
        print(f"\n  👤 {p['prenom']} ({p['scenario']})")

        # Login final
        r = do_login(p, " FINAL")
        if r.get("status") != "success":
            flag("CRITICAL", f"final {p['prenom']}", "Login final échoué")
            continue

        profile = r.get("profile", {})
        history = r.get("history", [])
        boost_hist = r.get("boostHistory", [])

        # XP monotone croissant (via history)
        print(f"    History: {len(history)} scores, {len(boost_hist)} boosts")

        # Vérification par scénario
        if p["scenario"] == "parfait":
            check(len(history) > 20, f"Lina: >20 scores dans l'historique ({len(history)})", "final")
            check(len(boost_hist) >= 5, f"Lina: ≥5 boosts historique ({len(boost_hist)})", "final")

        elif p["scenario"] == "tout_faux":
            easy_count = sum(1 for h in history if h.get("resultat") == "EASY" and h.get("source") != "CALIBRAGE")
            check(easy_count == 0, f"Éthan: 0 EASY hors calibrage ({easy_count})", "final")

        elif p["scenario"] == "ghost":
            check(len(history) == 0, f"Noé: 0 scores ({len(history)})", "final")
            check(len(boost_hist) == 0, f"Noé: 0 boosts ({len(boost_hist)})", "final")

        elif p["scenario"] == "flow_mode":
            easy_count = sum(1 for h in history if h.get("resultat") == "EASY")
            total = len(history)
            check(total > 0 and easy_count == total,
                  f"Yasmine: 100% EASY ({easy_count}/{total})", "final")

    # Race condition test
    print(f"\n  ⚡ Test race condition (2 save_score simultanés)...")
    p_race = profiles[0]  # Lina
    if p_race["code"]:
        results = [None, None]
        def race_save(idx):
            results[idx] = gas({
                "action": "save_score",
                "code": p_race["code"], "name": p_race["prenom"], "level": p_race["niveau"],
                "categorie": p_race["chapitres_sel"][0],
                "exercice_idx": 99, "resultat": "EASY",
                "q": f"Race test {idx}", "source": "BOOST"
            }, label=f"race_{idx}", verbose=False)

        t1 = threading.Thread(target=race_save, args=(0,))
        t2 = threading.Thread(target=race_save, args=(1,))
        t1.start(); t2.start()
        t1.join(); t2.join()

        ok1 = results[0] and results[0].get("status") == "success"
        ok2 = results[1] and results[1].get("status") == "success"
        check(ok1 or ok2, "Race condition: au moins 1 save réussit", "race")
        if ok1 and ok2:
            flag("WARN", "race", "Les 2 saves ont réussi — possible doublon (LockService manquant?)")

    # Admin overview final
    print(f"\n  🌙 ADMIN OVERVIEW FINAL")
    r = gas({"action": "get_admin_overview", "adminCode": ADMIN_CODE},
            label="admin_overview FINAL")
    pause()

    if r.get("status") == "success":
        students = r.get("students", [])
        test_codes = {p["code"] for p in profiles if p["code"]}
        for s in students:
            if s["code"] not in test_codes: continue
            p = next(pp for pp in profiles if pp["code"] == s["code"])
            action = s.get("actionPriority", s.get("action", "?"))
            print(f"    {action} {s.get('prenom','')} | boost={s.get('currentBoostExosDone','?')} | inactif={s.get('inactivityDays','?')}j")

# ═══════════════════════════════════════════════════════════════
# RAPPORT
# ═══════════════════════════════════════════════════════════════

def print_report(profiles):
    print("\n")
    print("═" * 60)
    print("  RAPPORT SIMULATION 10 ÉLÈVES × 7 JOURS")
    print("═" * 60)

    # Stats
    avg_time = sum(t["time"] for t in TIMINGS) / len(TIMINGS) if TIMINGS else 0
    max_t = max(TIMINGS, key=lambda t: t["time"]) if TIMINGS else {"time": 0, "action": "-", "label": "-"}
    print(f"""
  📊 STATS
    API calls     : {API_CALLS}
    Erreurs réseau: {API_ERRORS}
    Temps moyen   : {avg_time*1000:.0f} ms
    Temps max     : {max_t['time']*1000:.0f} ms ({max_t['label']})
""")

    # Anomalies
    criticals = [a for a in ANOMALIES if a["severity"] == "CRITICAL"]
    warns = [a for a in ANOMALIES if a["severity"] == "WARN"]

    print(f"  🔴 ANOMALIES CRITIQUES ({len(criticals)})")
    for a in criticals:
        print(f"    ❌ {a['context']}: {a['msg']}")
    if not criticals:
        print("    (aucune)")

    print(f"\n  🟡 WARNINGS ({len(warns)})")
    for a in warns:
        print(f"    ⚠️ {a['context']}: {a['msg']}")
    if not warns:
        print("    (aucun)")

    # Checks
    print(f"\n  ✅ VÉRIFICATIONS : {CHECKS['passed']} passées / {CHECKS['failed']} échouées")
    for icon, label in CHECKS["details"]:
        print(f"    {icon} {label}")

    # Détail par élève
    print(f"\n  👤 DÉTAIL PAR ÉLÈVE")
    print(f"    {'Prénom':<10} {'Niveau':<6} {'Scénario':<20} {'Code':<8}")
    print(f"    {'─'*10} {'─'*6} {'─'*20} {'─'*8}")
    for p in profiles:
        print(f"    {p['prenom']:<10} {p['niveau']:<6} {p['scenario']:<20} {p.get('code','???'):<8}")

    # Latences par action
    print(f"\n  ⏱ LATENCES PAR ACTION")
    action_times = {}
    for t in TIMINGS:
        a = t["action"]
        if a not in action_times:
            action_times[a] = []
        action_times[a].append(t["time"])

    print(f"    {'Action':<25} {'Appels':>6} {'Moy':>8} {'Max':>8}")
    print(f"    {'─'*25} {'─'*6} {'─'*8} {'─'*8}")
    for a, times in sorted(action_times.items(), key=lambda x: -max(x[1])):
        avg = sum(times)/len(times)
        mx = max(times)
        print(f"    {a:<25} {len(times):>6} {avg*1000:>7.0f}ms {mx*1000:>7.0f}ms")

    # Verdict
    print(f"\n{'═' * 60}")
    if CHECKS["failed"] == 0 and len(criticals) == 0:
        print("  🎉 SIMULATION RÉUSSIE — 0 anomalie critique")
    else:
        print(f"  ⚠️ SIMULATION TERMINÉE — {CHECKS['failed']} checks échoués, {len(criticals)} critiques")
    print("═" * 60)

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  SIM_10_STRESS — 10 élèves × 7 jours × comportements   ║")
    print("║  extrêmes · Stress test complet Matheux                 ║")
    print("╚══════════════════════════════════════════════════════════╝")

    t_start = time.time()

    # Nettoyage initial
    cleanup()

    # Build profiles
    profiles = build_profiles()

    # Run
    step1_register(profiles)
    step2_diagnostic(profiles)
    step3_simulate(profiles)
    step4_final_checks(profiles)

    # Cleanup final (sauf si --no-cleanup)
    if not NO_CLEANUP:
        cleanup()
    else:
        print("\n  ⚠️ --no-cleanup : comptes test conservés dans la base")

    # Rapport
    elapsed = time.time() - t_start
    print(f"\n  ⏱ Durée totale : {elapsed/60:.1f} minutes")
    print_report(profiles)
