#!/usr/bin/env python3
"""
create_5_students.py — Crée 5 profils élèves réalistes avec 4 jours d'utilisation variée.

Scénarios :
  1. Emma Petit    (6EME) — La perfectionniste     : 4j, 90% EASY, BOOST TERMINÉ
  2. Lucas Martin  (5EME) — Le progrès en cours    : 3j, 60% EASY, chapitre presque terminé
  3. Inès Dupont   (3EME) — La bloquée             : 2j puis stop, 70% HARD, inactive 8j
  4. Théo Bernard  (4EME) — Le régulier            : 4j, 75% EASY, boost en cours (3/5)
  5. Chloé Rousseau(5EME) — La débutante hésitante : 1j diag seulement, 50% HARD, pas de boost

Usage : python3 create_5_students.py
"""

import json, hashlib, time, random, urllib.request, urllib.error, sys

GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)

# ── Admin ─────────────────────────────────────────────────────────────────────
ADMIN_EMAIL = "admin@matheux.fr"
ADMIN_HASH  = "dba3013d8ee56602f8da554bd6f5ff0108324c6d220f137d2181d9d24fa0ef62"


def sha256_hash(email, password):
    raw = f"{email.lower().strip()}::{password}::AB22"
    return hashlib.sha256(raw.encode()).hexdigest()

# ── Helpers réseau ────────────────────────────────────────────────────────────

def gas(payload, label="", retry=2):
    body = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        GAS_URL, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    for attempt in range(retry + 1):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                d      = json.loads(r.read().decode("utf-8"))
                status = d.get("status", "?")
                ok     = "✅" if status == "success" else "❌"
                msg    = d.get("message", "")
                print(f"  {ok} {label or payload.get('action','?')} → {status}"
                      + (f" ({msg})" if status != "success" and msg else ""))
                return d
        except Exception as e:
            if attempt < retry:
                print(f"  ⚠️  {label or payload.get('action','?')} → tentative {attempt+1} échouée ({e}), retry…")
                time.sleep(2)
            else:
                print(f"  ❌ {label or payload.get('action','?')} → ERREUR finale : {e}")
                return {}
    return {}


def sleep(s=0.5):
    time.sleep(s)

# ── Login admin ───────────────────────────────────────────────────────────────

def login_admin():
    r = gas({"action": "login", "email": ADMIN_EMAIL, "password": ADMIN_HASH}, "login admin")
    code = r.get("profile", {}).get("code", "")
    if not code:
        print("❌ Impossible de récupérer le code admin. Abandon.")
        sys.exit(1)
    print(f"  → Code admin : {code}")
    return code


def simulate_next_day(admin_code, target_code, day_label=""):
    return gas({
        "action":     "simulate_next_day",
        "adminCode":  admin_code,
        "targetCode": target_code
    }, f"simulate_next_day {day_label}")

# ── Helpers scénarios ─────────────────────────────────────────────────────────

def register_and_login(name, email, password, level):
    """Inscrit l'élève puis retourne (code, diag_exos, curriculum)."""
    pwd_hash = sha256_hash(email, password)

    r = gas({
        "action":   "register",
        "name":     name,
        "email":    email,
        "level":    level,
        "password": pwd_hash,
        "consent":  True
    }, f"register {name}")

    status  = r.get("status", "")
    message = r.get("message", "")
    if status not in ("success", "already_exists") and "existe" not in message:
        print(f"  ❌ register échoué pour {name} — abandon de ce profil.")
        return None, [], []

    sleep()
    r = gas({"action": "login", "email": email, "password": pwd_hash}, f"login {name}")
    if r.get("status") != "success":
        print(f"  ❌ login échoué pour {name} — abandon.")
        return None, [], []

    profile = r.get("profile", {})
    code    = profile.get("code", "")
    print(f"  → Code : {code}")
    return code, pwd_hash


def do_diagnostic(code, name, level, hard_rate=0.3):
    """
    Génère et simule le diagnostic.
    hard_rate : fraction des exercices répondus HARD (0.0 → 1.0).
    Retourne la liste des catégories en erreur.
    """
    sleep(0.5)
    r = gas({"action": "generate_diagnostic", "level": level}, f"generate_diagnostic {name}")
    diag_exos = r.get("exos", [])
    print(f"  → {len(diag_exos)} exos diagnostic")

    errors = []
    for i, exo in enumerate(diag_exos):
        cat      = exo.get("categorie", "")
        resultat = "HARD" if random.random() < hard_rate else "EASY"
        if resultat == "HARD" and cat not in errors:
            errors.append(cat)
        sleep(0.4)
        gas({
            "action":       "save_score",
            "code":         code,
            "name":         name,
            "level":        level,
            "categorie":    cat,
            "exercice_idx": 0,
            "resultat":     resultat,
            "q":            exo.get("q", ""),
            "time":         random.randint(15, 50),
            "source":       "CALIBRAGE"
        }, f"  diag {cat[:22]} ({resultat})")

    print(f"  → Chapitres faibles : {errors[:3]}")
    return errors


def fetch_boost(code, level, errors):
    """Génère le boost du jour et retourne l'objet boost."""
    sleep(0.5)
    r = gas({
        "action": "generate_daily_boost",
        "code":   code,
        "level":  level,
        "errors": errors[:3]
    }, f"generate_daily_boost")
    boost = r.get("boost", {})
    nb    = len(boost.get("exos", []))
    print(f"  → {nb} exos dans le boost ({boost.get('categorie','?')})")
    return boost


def do_boost(code, boost, nb_exos, hard_rate=0.2):
    """Simule nb_exos exercices du boost avec un taux d'erreur donné."""
    exos = boost.get("exos", [])
    done = min(nb_exos, len(exos))
    for i in range(done):
        resultat = "HARD" if random.random() < hard_rate else "EASY"
        sleep(0.4)
        gas({
            "action": "save_boost",
            "code":   code,
            "boost":  boost,
            "exoIdx": i
        }, f"  boost Q{i+1} ({resultat})")


def do_chapter_exos(code, name, level, errors, nb_exos, hard_rate=0.25):
    """
    Simule nb_exos exercices de chapitre sur les catégories issues du diagnostic.
    Utilise les catégories des erreurs pour rester cohérent.
    """
    if not errors:
        return
    cat = errors[0]
    for i in range(nb_exos):
        resultat = "HARD" if random.random() < hard_rate else "EASY"
        sleep(0.4)
        gas({
            "action":       "save_score",
            "code":         code,
            "name":         name,
            "level":        level,
            "categorie":    cat,
            "exercice_idx": i,
            "resultat":     resultat,
            "q":            f"Exercice {i+1} chapitre {cat[:20]}",
            "time":         random.randint(20, 60),
            "source":       "chapter"
        }, f"  ch_exo {i+1}/{nb_exos} {cat[:20]} ({resultat})")


# ══════════════════════════════════════════════════════════════════════════════
# SCÉNARIOS
# ══════════════════════════════════════════════════════════════════════════════

def scenario_emma(admin_code):
    """Élève 1 — Emma Petit (6EME) : La perfectionniste (4j, 90% EASY, BOOST TERMINÉ)."""
    name     = "Emma Petit"
    email    = "emma.petit.2026@gmail.com"
    password = "Emma2026!"
    level    = "6EME"

    print(f"\n{'═'*60}")
    print(f"👩‍🎓 Scénario 1 — {name} ({level}) : La perfectionniste")
    print(f"{'═'*60}")

    code, pwd_hash = register_and_login(name, email, password, level)
    if not code:
        return None

    # Jour 0 : diagnostic très bon + boost complet (5/5, 5% HARD)
    print("\n  📅 Jour 0 — Diagnostic + boost")
    errors = do_diagnostic(code, name, level, hard_rate=0.10)
    boost  = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=5, hard_rate=0.05)

    # Jour 1
    print("\n  📅 Jour 1")
    simulate_next_day(admin_code, code, "J+1")
    boost = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=5, hard_rate=0.05)

    # Jour 2
    print("\n  📅 Jour 2")
    simulate_next_day(admin_code, code, "J+2")
    boost = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=5, hard_rate=0.0)

    # Jour 3 → BOOST TERMINÉ aujourd'hui, besoin du prochain
    print("\n  📅 Jour 3 — boost terminé (besoin du suivant)")
    simulate_next_day(admin_code, code, "J+3")
    boost = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=5, hard_rate=0.0)

    return {"name": name, "email": email, "password": password, "level": level, "code": code}


def scenario_lucas(admin_code):
    """Élève 2 — Lucas Martin (5EME) : Le progrès en cours (3j, 60% EASY, 18/20 exos)."""
    name     = "Lucas Martin"
    email    = "lucas.martin.2026@gmail.com"
    password = "Lucas2026!"
    level    = "5EME"

    print(f"\n{'═'*60}")
    print(f"👨‍🎓 Scénario 2 — {name} ({level}) : Le progrès en cours")
    print(f"{'═'*60}")

    code, pwd_hash = register_and_login(name, email, password, level)
    if not code:
        return None

    # Jour 0 : diagnostic mixte + boost partiel (3/5)
    print("\n  📅 Jour 0 — Diagnostic + boost partiel")
    errors = do_diagnostic(code, name, level, hard_rate=0.40)
    boost  = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=3, hard_rate=0.35)

    # Jour 1 : boost complet + 8 exos chapitre
    print("\n  📅 Jour 1 — boost complet + 8 exos chapitre")
    simulate_next_day(admin_code, code, "J+1")
    boost = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=5, hard_rate=0.25)
    do_chapter_exos(code, name, level, errors, nb_exos=8, hard_rate=0.30)

    # Jour 2 : 10 exos chapitre supplémentaires (total 18/20 → CHAPITRE TERMINÉ si 20)
    print("\n  📅 Jour 2 — 10 exos chapitre (total ~18)")
    simulate_next_day(admin_code, code, "J+2")
    do_chapter_exos(code, name, level, errors, nb_exos=10, hard_rate=0.20)

    return {"name": name, "email": email, "password": password, "level": level, "code": code}


def scenario_ines(admin_code):
    """Élève 3 — Inès Dupont (3EME) : La bloquée (2j, 70% HARD, inactive 8j → BLOQUÉ)."""
    name     = "Inès Dupont"
    email    = "ines.dupont.2026@gmail.com"
    password = "Ines2026!"
    level    = "3EME"

    print(f"\n{'═'*60}")
    print(f"👩‍🎓 Scénario 3 — {name} ({level}) : La bloquée")
    print(f"{'═'*60}")

    code, pwd_hash = register_and_login(name, email, password, level)
    if not code:
        return None

    # Jour 0 : diagnostic mauvais + boost raté (2/5, tous HARD)
    print("\n  📅 Jour 0 — Diagnostic difficile + boost partiel raté")
    errors = do_diagnostic(code, name, level, hard_rate=0.70)
    boost  = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=2, hard_rate=1.0)

    # Jour 1 : boost (1/5, HARD) — découragée
    print("\n  📅 Jour 1 — boost abandonné (1 exo seulement)")
    simulate_next_day(admin_code, code, "J+1")
    boost = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=1, hard_rate=1.0)

    # Jours 2-8 sans activité : simuler le passage du temps
    print("\n  📅 Jours 2-8 — inactive (simulation passage du temps)")
    for d in range(2, 9):
        simulate_next_day(admin_code, code, f"J+{d}")
        sleep(0.3)

    return {"name": name, "email": email, "password": password, "level": level, "code": code}


def scenario_theo(admin_code):
    """Élève 4 — Théo Bernard (4EME) : Le régulier (4j, 75% EASY, boost en cours 3/5)."""
    name     = "Théo Bernard"
    email    = "theo.bernard.2026@gmail.com"
    password = "Theo2026!"
    level    = "4EME"

    print(f"\n{'═'*60}")
    print(f"👨‍🎓 Scénario 4 — {name} ({level}) : Le régulier")
    print(f"{'═'*60}")

    code, pwd_hash = register_and_login(name, email, password, level)
    if not code:
        return None

    # Jour 0 : diagnostic correct + boost complet
    print("\n  📅 Jour 0 — Diagnostic + boost complet")
    errors = do_diagnostic(code, name, level, hard_rate=0.25)
    boost  = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=5, hard_rate=0.20)

    # Jour 1 : boost complet + 5 exos chapitre
    print("\n  📅 Jour 1 — boost complet + 5 exos chapitre")
    simulate_next_day(admin_code, code, "J+1")
    boost = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=5, hard_rate=0.25)
    do_chapter_exos(code, name, level, errors, nb_exos=5, hard_rate=0.20)

    # Jour 2 : boost complet + 5 exos chapitre
    print("\n  📅 Jour 2 — boost complet + 5 exos chapitre")
    simulate_next_day(admin_code, code, "J+2")
    boost = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=5, hard_rate=0.20)
    do_chapter_exos(code, name, level, errors, nb_exos=5, hard_rate=0.25)

    # Jour 3 : boost en cours (3/5 exos faits, pas terminé)
    print("\n  📅 Jour 3 — boost en cours (3/5)")
    simulate_next_day(admin_code, code, "J+3")
    boost = fetch_boost(code, level, errors)
    if boost.get("exos"):
        do_boost(code, boost, nb_exos=3, hard_rate=0.20)

    return {"name": name, "email": email, "password": password, "level": level, "code": code}


def scenario_chloe(admin_code):
    """Élève 5 — Chloé Rousseau (5EME) : La débutante hésitante (1j diag seulement, pas de boost)."""
    name     = "Chloé Rousseau"
    email    = "chloe.rousseau.2026@gmail.com"
    password = "Chloe2026!"
    level    = "5EME"

    print(f"\n{'═'*60}")
    print(f"👩‍🎓 Scénario 5 — {name} ({level}) : La débutante hésitante")
    print(f"{'═'*60}")

    code, pwd_hash = register_and_login(name, email, password, level)
    if not code:
        return None

    # Jour 0 : diagnostic seulement — pas de boost
    print("\n  📅 Jour 0 — Diagnostic seulement (pas de boost)")
    do_diagnostic(code, name, level, hard_rate=0.50)
    print("  → Pas de boost lancé (hésitante)")

    return {"name": name, "email": email, "password": password, "level": level, "code": code}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    random.seed(42)

    print("\n" + "═"*60)
    print("🏫  create_5_students.py — Matheux.fr")
    print("    Création de 5 profils élèves réalistes")
    print("═"*60)

    # Récupération du code admin
    print("\n🔑 Connexion admin…")
    admin_code = login_admin()

    # Lancement des 5 scénarios
    results = []

    r = scenario_emma(admin_code)
    if r:
        results.append(r)

    r = scenario_lucas(admin_code)
    if r:
        results.append(r)

    r = scenario_ines(admin_code)
    if r:
        results.append(r)

    r = scenario_theo(admin_code)
    if r:
        results.append(r)

    r = scenario_chloe(admin_code)
    if r:
        results.append(r)

    # ── Récapitulatif ──────────────────────────────────────────────────────────
    print("\n" + "═"*60)
    print("✅  RÉCAPITULATIF — comptes créés")
    print("═"*60)
    scenarios_desc = [
        "La perfectionniste    — 4j, 90% EASY, BOOST TERMINÉ",
        "Le progrès en cours   — 3j, 60% EASY, ~18/20 exos chap.",
        "La bloquée            — 2j, 70% HARD, inactive 8j → BLOQUÉ",
        "Le régulier           — 4j, 75% EASY, boost en cours 3/5",
        "La débutante hésitante— 1j diag seul., boost disponible",
    ]
    for i, s in enumerate(results):
        desc = scenarios_desc[i] if i < len(scenarios_desc) else ""
        print(f"\n  {i+1}. {s['name']} ({s['level']})")
        print(f"     Email  : {s['email']}")
        print(f"     MDP    : {s['password']}")
        print(f"     Code   : {s['code']}")
        print(f"     Profil : {desc}")

    print("\n" + "═"*60)
    print("   → Vérifier dans le panel admin (triple-clic logo)")
    print("   → Onglet 'À faire' pour voir les actions à effectuer")
    print("═"*60 + "\n")


if __name__ == "__main__":
    main()
