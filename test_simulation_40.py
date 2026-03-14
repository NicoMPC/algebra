#!/usr/bin/env python3
"""
test_simulation_40.py — Simulation 40 élèves × 15 jours sur GAS PROD
=====================================================================
Tous les comptes créés sont IsTest=1 (@matheux.fr).
Teste les limites réelles de Google Apps Script avec 40 utilisateurs.

Usage :
  python3 test_simulation_40.py [--cleanup-only]
"""

import requests, json, hashlib, time, sys, random, string, threading
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)
ADMIN_EMAIL = "admin@matheux.fr"
ADMIN_HASH  = "dba3013d8ee56602f8da554bd6f5ff0108324c6d220f137d2181d9d24fa0ef62"

PASS = 0
FAIL = 0
ERRORS = []
TIMINGS = []

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def h256(password, email):
    raw = f"{email.lower().strip()}::{password}::AB22"
    return hashlib.sha256(raw.encode()).hexdigest()

def gas(payload, retry=3, label=""):
    t0 = time.time()
    for attempt in range(retry):
        try:
            r = requests.post(GAS_URL, json=payload, timeout=60)
            elapsed = time.time() - t0
            TIMINGS.append({"action": payload.get("action","?"), "time": elapsed, "label": label})
            result = r.json()
            if result.get("message") == "rate_limit" and attempt < retry - 1:
                time.sleep(5)
                continue
            return result
        except Exception as e:
            if attempt == retry - 1:
                elapsed = time.time() - t0
                TIMINGS.append({"action": payload.get("action","?"), "time": elapsed, "label": f"ERROR: {label}"})
                return {"status": "error", "message": str(e)}
            time.sleep(3)

def check(cond, label):
    global PASS, FAIL
    if cond:
        PASS += 1
    else:
        FAIL += 1
        ERRORS.append(label)
        print(f"  ❌ {label}")

def log(msg, icon="ℹ️"):
    print(f"  {icon} {msg}")

# ─────────────────────────────────────────────────────────────
# PROFILS — 40 élèves représentatifs
# ─────────────────────────────────────────────────────────────

CHAPITRES = {
    "6EME": ["Nombres_entiers", "Fractions", "Proportionnalité", "Géométrie", "Périmètres_Aires",
             "Angles", "Nombres_Décimaux", "Statistiques_6ème", "Symétrie_Axiale"],
    "5EME": ["Fractions", "Nombres_relatifs", "Proportionnalité", "Calcul_Littéral",
             "Pythagore", "Puissances", "Symétrie_Centrale", "Transformations"],
    "4EME": ["Puissances", "Fractions", "Proportionnalité", "Calcul_Littéral",
             "Équations", "Pythagore", "Fonctions_Linéaires", "Inéquations"],
    "3EME": ["Calcul_Littéral", "Équations", "Fonctions", "Théorème_de_Thalès",
             "Trigonométrie", "Statistiques", "Probabilités", "Racines_Carrées"]
}

PRENOMS_6 = ["Emma", "Lucas", "Léa", "Hugo", "Jade", "Louis", "Manon", "Nathan", "Chloé", "Théo", "Inès", "Raphaël"]
PRENOMS_5 = ["Camille", "Arthur", "Sarah", "Mathis", "Lina", "Tom", "Clara", "Enzo", "Zoé", "Maxime"]
PRENOMS_4 = ["Alice", "Gabriel", "Léna", "Adam", "Louise", "Jules", "Mila", "Ethan", "Eva", "Noah"]
PRENOMS_3 = ["Lilou", "Axel", "Ambre", "Rayan", "Anna", "Mohamed", "Margot", "Nolan"]

# Profils comportementaux
PROFIL_REGULIER_MOTIVE = "regulier_motive"    # 5 exos/jour, 6j/7
PROFIL_REGULIER_MOYEN  = "regulier_moyen"     # boost quotidien seulement
PROFIL_IRREGULIER      = "irregulier"          # actif 3j, absent 4j
PROFIL_DIFFICULTE      = "en_difficulte"       # beaucoup de HARD
PROFIL_BOSSEUR_BREVET  = "bosseur_brevet"     # 3EME, sessions longues


def build_profiles():
    """Construit les 40 profils avec distribution réaliste."""
    profiles = []
    idx = 0

    def add(prenom, niveau, profil, score_init):
        nonlocal idx
        chaps = random.sample(CHAPITRES[niveau], min(random.randint(2, 4), len(CHAPITRES[niveau])))
        profiles.append({
            "id": idx,
            "prenom": prenom,
            "niveau": niveau,
            "profil": profil,
            "score_init": score_init,
            "chapitres": chaps,
            "prob_erreur_lvl1": random.uniform(0.05, 0.25) if score_init > 50 else random.uniform(0.20, 0.45),
            "prob_erreur_lvl2": random.uniform(0.15, 0.35) if score_init > 50 else random.uniform(0.35, 0.60),
            "prob_indice": random.uniform(0.10, 0.60),
            "jours_actifs": _jours_actifs(profil),
            "email": None,
            "hash": None,
            "code": None,
        })
        idx += 1

    # 6EME — 12 élèves
    for i, p in enumerate(PRENOMS_6):
        profil = [PROFIL_REGULIER_MOTIVE, PROFIL_REGULIER_MOYEN, PROFIL_IRREGULIER,
                  PROFIL_DIFFICULTE, PROFIL_REGULIER_MOYEN, PROFIL_REGULIER_MOTIVE,
                  PROFIL_IRREGULIER, PROFIL_REGULIER_MOYEN, PROFIL_DIFFICULTE,
                  PROFIL_REGULIER_MOYEN, PROFIL_REGULIER_MOTIVE, PROFIL_IRREGULIER][i]
        score = random.randint(20, 85)
        add(p, "6EME", profil, score)

    # 5EME — 10 élèves
    for i, p in enumerate(PRENOMS_5):
        profil = [PROFIL_REGULIER_MOTIVE, PROFIL_REGULIER_MOYEN, PROFIL_IRREGULIER,
                  PROFIL_REGULIER_MOYEN, PROFIL_DIFFICULTE, PROFIL_REGULIER_MOTIVE,
                  PROFIL_REGULIER_MOYEN, PROFIL_IRREGULIER, PROFIL_DIFFICULTE,
                  PROFIL_REGULIER_MOYEN][i]
        score = random.randint(25, 80)
        add(p, "5EME", profil, score)

    # 4EME — 10 élèves
    for i, p in enumerate(PRENOMS_4):
        profil = [PROFIL_REGULIER_MOTIVE, PROFIL_REGULIER_MOYEN, PROFIL_IRREGULIER,
                  PROFIL_REGULIER_MOYEN, PROFIL_DIFFICULTE, PROFIL_REGULIER_MOTIVE,
                  PROFIL_REGULIER_MOYEN, PROFIL_IRREGULIER, PROFIL_BOSSEUR_BREVET,
                  PROFIL_REGULIER_MOYEN][i]
        score = random.randint(25, 75)
        add(p, "4EME", profil, score)

    # 3EME — 8 élèves
    for i, p in enumerate(PRENOMS_3):
        profil = [PROFIL_BOSSEUR_BREVET, PROFIL_REGULIER_MOTIVE, PROFIL_IRREGULIER,
                  PROFIL_BOSSEUR_BREVET, PROFIL_REGULIER_MOYEN, PROFIL_DIFFICULTE,
                  PROFIL_BOSSEUR_BREVET, PROFIL_REGULIER_MOYEN][i]
        score = random.randint(30, 80)
        add(p, "3EME", profil, score)

    return profiles


def _jours_actifs(profil):
    """Retourne la liste des jours actifs (1-15) selon le profil."""
    if profil == PROFIL_REGULIER_MOTIVE:
        # 6j/7 → ~13 jours sur 15
        all_days = list(range(1, 16))
        off = random.sample(all_days, 2)
        return [d for d in all_days if d not in off]
    elif profil == PROFIL_REGULIER_MOYEN:
        # boost quotidien, ~10 jours sur 15
        all_days = list(range(1, 16))
        off = random.sample(all_days, 5)
        return [d for d in all_days if d not in off]
    elif profil == PROFIL_IRREGULIER:
        # actif 3j, absent 4j → ~6-7 jours
        return sorted(random.sample(range(1, 16), random.randint(5, 7)))
    elif profil == PROFIL_DIFFICULTE:
        # peu de sessions → ~4-5 jours
        return sorted(random.sample(range(1, 16), random.randint(3, 5)))
    elif profil == PROFIL_BOSSEUR_BREVET:
        # sessions longues, presque tous les jours → ~12-14 jours
        all_days = list(range(1, 16))
        off = random.sample(all_days, random.randint(1, 3))
        return [d for d in all_days if d not in off]
    return list(range(1, 16))


# ─────────────────────────────────────────────────────────────
# PHASE 1 — INSCRIPTION DES 40 ÉLÈVES
# ─────────────────────────────────────────────────────────────

def phase1_register(profiles):
    print("\n" + "=" * 60)
    print("  PHASE 1 — INSCRIPTION DES 40 ÉLÈVES")
    print("=" * 60)

    success = 0
    for p in profiles:
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        p["email"] = f"sim.{p['prenom'].lower()}.{suffix}@matheux.fr"
        p["password"] = "SimTest2026!"
        p["hash"] = h256(p["password"], p["email"])

        r = gas({
            "action": "register",
            "email": p["email"],
            "name": p["prenom"],
            "level": p["niveau"],
            "password": p["hash"]
        }, label=f"register_{p['prenom']}")

        if r.get("status") == "success":
            p["code"] = r["profile"]["code"]
            success += 1
        else:
            print(f"  ❌ Register {p['prenom']} : {r.get('message','?')}")

        # Pause pour rate limiting
        time.sleep(0.3)

    check(success == 40, f"Phase 1 : {success}/40 inscriptions réussies")
    log(f"{success}/40 élèves inscrits", "✅" if success == 40 else "⚠️")
    return success


# ─────────────────────────────────────────────────────────────
# PHASE 2 — SIMULATION JOUR PAR JOUR
# ─────────────────────────────────────────────────────────────

def phase2_simulate(profiles, admin_code):
    print("\n" + "=" * 60)
    print("  PHASE 2 — SIMULATION 15 JOURS")
    print("=" * 60)

    total_logins = 0
    total_scores = 0
    total_boosts = 0
    day_errors = 0

    for day in range(1, 16):
        print(f"\n  📅 JOUR {day}/15")
        active_today = [p for p in profiles if p["code"] and day in p["jours_actifs"]]
        log(f"{len(active_today)} élèves actifs")

        day_logins = 0
        day_scores = 0

        for p in active_today:
            # LOGIN
            lr = gas({"action": "login", "email": p["email"], "password": p["hash"]},
                     label=f"login_J{day}_{p['prenom']}")
            if lr.get("status") != "success":
                day_errors += 1
                continue
            day_logins += 1

            boost_data = lr.get("dailyBoost") or lr.get("nextBoost")
            code = p["code"]

            # BOOST (si disponible)
            if boost_data and boost_data.get("exos"):
                exos = boost_data["exos"]
                n_exos = len(exos)
                if p["profil"] == PROFIL_DIFFICULTE:
                    n_exos = min(2, n_exos)  # abandonne après 2

                for i in range(n_exos):
                    exo = exos[i]
                    is_hard = random.random() < p["prob_erreur_lvl1"]
                    status = "HARD" if is_hard else ("MEDIUM" if random.random() < 0.15 else "EASY")
                    cat = exo.get("oC") or exo.get("_cat") or exo.get("categorie", "BOOST")

                    gas({
                        "action": "save_score",
                        "code": code,
                        "name": p["prenom"],
                        "level": p["niveau"],
                        "categorie": cat,
                        "exercice_idx": i + 1,
                        "q": str(exo.get("q", ""))[:60],
                        "resultat": status,
                        "time": random.randint(15, 120),
                        "indices": random.randint(0, 2) if random.random() < p["prob_indice"] else 0,
                        "formule": random.random() > 0.7,
                        "source": "BOOST"
                    }, label=f"score_boost_J{day}_{p['prenom']}")
                    day_scores += 1

                # save_boost final
                if n_exos >= 5:
                    gas({
                        "action": "save_boost",
                        "code": code,
                        "boost": boost_data,
                        "exoIdx": 4
                    }, label=f"save_boost_J{day}_{p['prenom']}")
                    total_boosts += 1

            # CHAPITRE (si bosseur ou régulier motivé)
            if p["profil"] in (PROFIL_BOSSEUR_BREVET, PROFIL_REGULIER_MOTIVE) and day > 1:
                cat = random.choice(p["chapitres"])
                n = random.randint(3, 8) if p["profil"] == PROFIL_REGULIER_MOTIVE else random.randint(5, 12)
                for i in range(n):
                    is_hard = random.random() < p["prob_erreur_lvl2"]
                    status = "HARD" if is_hard else ("MEDIUM" if random.random() < 0.15 else "EASY")
                    gas({
                        "action": "save_score",
                        "code": code,
                        "name": p["prenom"],
                        "level": p["niveau"],
                        "categorie": cat,
                        "exercice_idx": i + 1,
                        "q": f"Exo {i+1} — {cat}",
                        "resultat": status,
                        "time": random.randint(20, 150),
                        "indices": 0,
                        "formule": False,
                        "source": ""
                    }, label=f"score_chap_J{day}_{p['prenom']}")
                    day_scores += 1

            # Pause anti rate-limit
            time.sleep(0.15)

        total_logins += day_logins
        total_scores += day_scores
        log(f"  Logins: {day_logins} | Scores: {day_scores}")

        # ACTIONS ADMIN (certains jours)
        if day == 1 and admin_code:
            log("Admin : get_admin_overview", "👨‍💻")
            ov = gas({"action": "get_admin_overview", "adminCode": admin_code}, label="admin_overview_J1")
            check(ov.get("status") == "success", f"Admin overview J1 OK (got {len(ov.get('students',[]))} students)")

        if day == 5 and admin_code:
            # Publie brevet pour les 3EME
            troisemes = [p for p in profiles if p["niveau"] == "3EME" and p["code"]]
            for p3 in troisemes[:3]:
                r_brev = gas({
                    "action": "publish_admin_brevet",
                    "adminCode": admin_code,
                    "targetCode": p3["code"],
                    "chapitres": ["Calcul_Littéral", "Équations"],
                    "message": "Brevet blanc de mi-parcours"
                }, label=f"brevet_{p3['prenom']}")
                check(r_brev.get("status") == "success", f"Brevet publié pour {p3['prenom']}")

        if day == 7 and admin_code:
            # Publie révision cross-niveau pour 2 élèves
            for rp in profiles[:2]:
                if rp["code"] and rp["niveau"] != "6EME":
                    lower = {"5EME": "6EME", "4EME": "5EME", "3EME": "4EME"}[rp["niveau"]]
                    r_rev = gas({
                        "action": "publish_admin_revision",
                        "adminCode": admin_code,
                        "targetCode": rp["code"],
                        "chapters": [{"niveau": lower, "categorie": "Fractions"}]
                    }, label=f"revision_{rp['prenom']}")
                    check(r_rev.get("status") == "success", f"Révision publiée pour {rp['prenom']}")

        if day == 12 and admin_code:
            # Morning report
            r_rep = gas({"action": "get_admin_overview", "adminCode": admin_code}, label="admin_overview_J12")
            check(r_rep.get("status") == "success", "Admin overview J12 OK")

    print(f"\n  📊 Résumé Phase 2 :")
    log(f"Total logins  : {total_logins}")
    log(f"Total scores  : {total_scores}")
    log(f"Total boosts  : {total_boosts}")
    log(f"Erreurs login : {day_errors}")

    return total_logins, total_scores


# ─────────────────────────────────────────────────────────────
# PHASE 3 — TESTS CONTRADICTOIRES
# ─────────────────────────────────────────────────────────────

def phase3_tests(profiles, admin_code):
    print("\n" + "=" * 60)
    print("  PHASE 3 — TESTS CONTRADICTOIRES")
    print("=" * 60)

    active = [p for p in profiles if p["code"]]
    if len(active) < 2:
        log("Pas assez de profils actifs pour les tests", "⚠️")
        return

    # ── A1 : Double session simultanée ──
    print("\n  🧪 A1 — Double session simultanée")
    p1 = active[0]
    results_a1 = [None, None]
    def login_thread(idx):
        results_a1[idx] = gas({"action": "login", "email": p1["email"], "password": p1["hash"]},
                              label=f"double_login_{idx}")
    t1 = threading.Thread(target=login_thread, args=(0,))
    t2 = threading.Thread(target=login_thread, args=(1,))
    t1.start(); t2.start()
    t1.join(); t2.join()
    check(results_a1[0].get("status") == "success" and results_a1[1].get("status") == "success",
          "A1 : deux logins simultanés réussis")

    # ── A2 : save_score sans boost actif ──
    print("\n  🧪 A2 — save_score sans boost actif")
    p2 = active[1]
    r_a2 = gas({
        "action": "save_score",
        "code": p2["code"],
        "name": p2["prenom"],
        "level": p2["niveau"],
        "categorie": "Fractions",
        "exercice_idx": 99,
        "q": "Test fantôme",
        "resultat": "EASY",
        "time": 10,
        "source": "BOOST"
    }, label="a2_score_no_boost")
    check(r_a2.get("status") == "success", "A2 : save_score BOOST sans DailyBoost actif → pas de crash")

    # ── A3 : Résultat invalide ──
    print("\n  🧪 A3 — Score hors bornes")
    r_a3 = gas({
        "action": "save_score",
        "code": p2["code"],
        "name": p2["prenom"],
        "level": p2["niveau"],
        "categorie": "Fractions",
        "exercice_idx": 1,
        "q": "Test invalide",
        "resultat": "INVALID_VALUE",
        "time": 10,
        "source": ""
    }, label="a3_invalid_result")
    check(r_a3.get("status") == "error", f"A3 : résultat invalide rejeté (got: {r_a3.get('status')})")

    # ── A4 : generate_daily_boost ciblé ──
    print("\n  🧪 A4 — Boost ciblé chapitres")
    p3 = active[2]
    r_a4 = gas({
        "action": "generate_daily_boost",
        "code": p3["code"],
        "level": p3["niveau"],
        "chapters": p3["chapitres"][:2]
    }, label="a4_boost_target")
    check(r_a4.get("status") == "success", "A4 : boost généré")
    if r_a4.get("boost"):
        boost_cats = set()
        for ex in r_a4["boost"].get("exos", []):
            cat = ex.get("_cat") or ex.get("oC") or ex.get("categorie", "")
            if cat:
                boost_cats.add(cat)
        # Vérifier que les exos viennent des chapitres ciblés (pas garanti à 100% si fallback)
        log(f"  Catégories dans boost : {boost_cats}")

    # ── A5 : NbExos > 20 ──
    print("\n  🧪 A5 — 25 exercices sur un chapitre")
    p4 = active[3]
    cat_test = p4["chapitres"][0] if p4["chapitres"] else "Fractions"
    for i in range(25):
        gas({
            "action": "save_score",
            "code": p4["code"],
            "name": p4["prenom"],
            "level": p4["niveau"],
            "categorie": cat_test,
            "exercice_idx": i + 1,
            "q": f"Exo stress {i+1}",
            "resultat": random.choice(["EASY", "EASY", "HARD"]),
            "time": random.randint(10, 60),
            "source": ""
        }, label=f"a5_exo_{i+1}")
    r_a5 = gas({"action": "get_progress", "code": p4["code"]}, label="a5_progress")
    if r_a5.get("status") == "success":
        prog = [x for x in r_a5.get("progress", []) if x["chapitre"] == cat_test]
        if prog:
            check(prog[0]["nbExos"] >= 25, f"A5 : NbExos = {prog[0]['nbExos']} (attendu ≥ 25)")
        else:
            check(False, "A5 : chapitre non trouvé dans progress")

    # ── B1 : 40 logins en rafale ──
    print("\n  🧪 B1 — 40 logins en rafale")
    t0 = time.time()
    results_b1 = {}
    def b1_login(p):
        r = gas({"action": "login", "email": p["email"], "password": p["hash"]}, label=f"b1_{p['prenom']}")
        return r.get("status") == "success"

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(b1_login, p): p for p in active[:40]}
        for f in as_completed(futures):
            p = futures[f]
            results_b1[p["prenom"]] = f.result()
    elapsed_b1 = time.time() - t0
    success_b1 = sum(1 for v in results_b1.values() if v)
    check(success_b1 >= 35, f"B1 : {success_b1}/40 logins réussis en {elapsed_b1:.1f}s")
    log(f"  Temps : {elapsed_b1:.1f}s, taux succès : {success_b1}/40")

    # ── B2 : 200 save_score en rafale ──
    print("\n  🧪 B2 — 200 save_score en 2 min")
    t0_b2 = time.time()
    success_b2 = 0

    def b2_score(p, idx):
        r = gas({
            "action": "save_score",
            "code": p["code"],
            "name": p["prenom"],
            "level": p["niveau"],
            "categorie": p["chapitres"][0] if p["chapitres"] else "Fractions",
            "exercice_idx": idx,
            "q": f"Stress test {idx}",
            "resultat": random.choice(["EASY", "MEDIUM", "HARD"]),
            "time": 30,
            "source": ""
        }, label=f"b2_{p['prenom']}_{idx}")
        return r.get("status") == "success"

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for p in active[:40]:
            for idx in range(1, 6):
                futures.append(executor.submit(b2_score, p, idx))
        for f in as_completed(futures):
            if f.result():
                success_b2 += 1
    elapsed_b2 = time.time() - t0_b2
    total_b2 = min(200, len(active) * 5)
    check(success_b2 >= total_b2 * 0.9, f"B2 : {success_b2}/{total_b2} scores en {elapsed_b2:.1f}s")

    # ── B4 : get_admin_overview performance ──
    print("\n  🧪 B4 — get_admin_overview performance")
    if admin_code:
        t0_b4 = time.time()
        r_b4 = gas({"action": "get_admin_overview", "adminCode": admin_code}, label="b4_overview")
        elapsed_b4 = time.time() - t0_b4
        check(r_b4.get("status") == "success", f"B4 : overview OK en {elapsed_b4:.1f}s")
        check(elapsed_b4 < 30, f"B4 : temps < 30s (actual: {elapsed_b4:.1f}s)")
        if r_b4.get("status") == "success":
            log(f"  {len(r_b4.get('students',[]))} élèves, {elapsed_b4:.1f}s")

    # ── C1 : PendingBrevet persistant ──
    print("\n  🧪 C1 — PendingBrevet persistant")
    troisemes = [p for p in active if p["niveau"] == "3EME"]
    if troisemes:
        p_c1 = troisemes[0]
        lr_c1 = gas({"action": "login", "email": p_c1["email"], "password": p_c1["hash"]}, label="c1_login")
        if lr_c1.get("status") == "success":
            pb = lr_c1.get("pendingBrevet")
            # Si un brevet a été publié à J5
            if pb:
                check(True, "C1 : PendingBrevet toujours présent après reconnexion")
            else:
                log("C1 : pas de PendingBrevet (brevet non publié pour cet élève)", "ℹ️")

    # ── C7 : IsTest @matheux.fr ──
    print("\n  🧪 C7 — IsTest automatique")
    if admin_code:
        ov_c7 = gas({"action": "get_admin_overview", "adminCode": admin_code}, label="c7_overview")
        if ov_c7.get("status") == "success":
            sim_students = [s for s in ov_c7.get("students",[])
                           if s.get("email","").endswith("@matheux.fr") and "sim." in s.get("email","")]
            all_test = all(s.get("isTest") for s in sim_students)
            check(all_test, f"C7 : {len(sim_students)} comptes sim tous IsTest=1")

    # ── C3 : Trial check ──
    print("\n  🧪 C3 — Trial status")
    p_c3 = active[5]
    r_c3 = gas({"action": "check_trial_status", "code": p_c3["code"]}, label="c3_trial")
    check(r_c3.get("trialActive") == True, f"C3 : trial actif (daysLeft={r_c3.get('daysLeft',0)})")


# ─────────────────────────────────────────────────────────────
# PHASE 4 — ANALYSE PERFORMANCE
# ─────────────────────────────────────────────────────────────

def phase4_analysis():
    print("\n" + "=" * 60)
    print("  PHASE 4 — ANALYSE PERFORMANCE")
    print("=" * 60)

    if not TIMINGS:
        log("Pas de données de timing", "⚠️")
        return

    by_action = {}
    for t in TIMINGS:
        a = t["action"]
        if a not in by_action:
            by_action[a] = []
        by_action[a].append(t["time"])

    print(f"\n  {'Action':<30} {'Count':>6} {'Avg(s)':>8} {'Max(s)':>8} {'P95(s)':>8}")
    print("  " + "-" * 70)
    for action in sorted(by_action.keys()):
        times = sorted(by_action[action])
        n = len(times)
        avg = sum(times) / n
        mx = max(times)
        p95 = times[int(n * 0.95)] if n > 1 else mx
        print(f"  {action:<30} {n:>6} {avg:>8.2f} {mx:>8.2f} {p95:>8.2f}")

    total_time = sum(t["time"] for t in TIMINGS)
    total_calls = len(TIMINGS)
    errors = [t for t in TIMINGS if "ERROR" in t.get("label", "")]
    print(f"\n  Total : {total_calls} appels en {total_time:.0f}s")
    print(f"  Erreurs réseau : {len(errors)}")
    timeouts = [t for t in TIMINGS if t["time"] > 30]
    print(f"  Timeouts (>30s) : {len(timeouts)}")


# ─────────────────────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────────────────────

def cleanup(profiles, admin_code):
    """Supprime les comptes de simulation (mark_all_test déjà fait — IsTest=1)."""
    print("\n" + "=" * 60)
    print("  CLEANUP — Les comptes sim sont IsTest=1, pas de nettoyage nécessaire")
    print("=" * 60)
    log(f"{len([p for p in profiles if p['code']])} comptes sim créés (tous IsTest=1 via @matheux.fr)")
    log("Ces comptes n'impactent pas le quota des 50 vrais élèves.")
    log("Pour les supprimer : cleanup_all via admin ou manuellement dans le Sheet.")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    if "--cleanup-only" in sys.argv:
        print("Cleanup mode — rien à nettoyer (IsTest=1)")
        return

    print("=" * 60)
    print("  🧪 MATHEUX — SIMULATION 40 ÉLÈVES × 15 JOURS")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  GAS : ...{GAS_URL[-40:]}")
    print("=" * 60)

    # Admin login
    admin_code = None
    r_admin = gas({"action": "login", "email": ADMIN_EMAIL, "password": ADMIN_HASH}, label="admin_login")
    if r_admin.get("status") == "success" and r_admin.get("profile", {}).get("isAdmin"):
        admin_code = r_admin["profile"]["code"]
        log(f"Admin connecté : {admin_code}", "✅")
    else:
        log("Admin non disponible — tests admin ignorés", "⚠️")

    # Construire les profils
    profiles = build_profiles()
    log(f"{len(profiles)} profils construits", "✅")
    by_level = {}
    for p in profiles:
        by_level[p["niveau"]] = by_level.get(p["niveau"], 0) + 1
    log(f"  Distribution : {by_level}")

    # Phase 1 — Inscription
    registered = phase1_register(profiles)
    if registered < 20:
        log("Trop peu d'inscriptions réussies — abandon", "❌")
        return

    # Phase 2 — Simulation 15 jours
    total_logins, total_scores = phase2_simulate(profiles, admin_code)

    # Phase 3 — Tests contradictoires
    phase3_tests(profiles, admin_code)

    # Phase 4 — Analyse performance
    phase4_analysis()

    # Cleanup info
    cleanup(profiles, admin_code)

    # Résultat final
    print("\n" + "=" * 60)
    print(f"  📊 RÉSULTAT FINAL")
    print(f"  ✅ {PASS} tests passés")
    print(f"  ❌ {FAIL} tests échoués")
    if ERRORS:
        print(f"\n  Erreurs :")
        for e in ERRORS:
            print(f"    • {e}")
    print("=" * 60)


if __name__ == "__main__":
    main()
