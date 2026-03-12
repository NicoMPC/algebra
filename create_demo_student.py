#!/usr/bin/env python3
"""
create_demo_student.py — Crée un profil élève démo + simule diagnostic + boost du jour.

Profil créé : élève classique (IsTest=0), niveau 4EME.
Usage : python3 create_demo_student.py

Après test : utiliser le panel admin pour le marquer IsTest si besoin.
"""

import json, hashlib, time, random, urllib.request, urllib.error, sys

GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)

# ── Profil élève démo ────────────────────────────────────────
STUDENT_NAME  = "Théo Lambert"
STUDENT_EMAIL = "theo.lambert.2026@gmail.com"
STUDENT_PASS  = "Algebre2026!"
STUDENT_LEVEL = "4EME"

def sha256_hash(email, password):
    return hashlib.sha256(f"{email}::{password}::AB22".encode()).hexdigest()

def gas(payload, label=""):
    body = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(GAS_URL, data=body,
                                  headers={"Content-Type": "application/json"},
                                  method="POST")
    try:
        with urllib.request.urlopen(req, timeout=35) as r:
            d = json.loads(r.read().decode("utf-8"))
            status = d.get("status","?")
            ok = "✅" if status == "success" else "❌"
            print(f"  {ok} {label or payload.get('action','?')} → {status}"
                  + (f" ({d.get('message','')})" if status != "success" else ""))
            return d
    except Exception as e:
        print(f"  ❌ {label or payload.get('action','?')} → ERREUR : {e}")
        return {}

# ══════════════════════════════════════════════════════════════
print(f"\n🎓 Création du profil démo : {STUDENT_NAME} ({STUDENT_LEVEL})")
print("─" * 55)

# 1. Inscription
pwd_hash = sha256_hash(STUDENT_EMAIL, STUDENT_PASS)
r = gas({
    "action": "register",
    "name": STUDENT_NAME,
    "email": STUDENT_EMAIL,
    "level": STUDENT_LEVEL,
    "password": pwd_hash,
    "consent": True
}, "register")

if r.get("status") not in ("success", "already_exists") and "existe" not in r.get("message",""):
    print(f"\n❌ Impossible de créer le compte. Abandon.")
    sys.exit(1)

# 2. Login pour récupérer code + diagExos + curriculum
print("\n📥 Connexion initiale…")
r = gas({
    "action": "login",
    "email": STUDENT_EMAIL,
    "password": pwd_hash
}, "login")

if r.get("status") != "success":
    print("❌ Login échoué. Abandon.")
    sys.exit(1)

profile   = r.get("profile", {})
code      = profile.get("code", "")

print(f"  → Code : {code}")

# 3. Génération + simulation du diagnostic
print("\n🧪 Génération du diagnostic…")
time.sleep(0.5)
r = gas({"action": "generate_diagnostic", "level": STUDENT_LEVEL}, "generate_diagnostic")
diag_exos = r.get("exos", [])  # liste plate d'exercices avec champ 'categorie'
print(f"  → {len(diag_exos)} exercices de diagnostic")

# Résultats : 50% HARD pour forcer un boost utile
errors = []
for i, exo in enumerate(diag_exos):
    cat      = exo.get("categorie", "")
    resultat = "HARD" if i % 2 == 0 else "EASY"
    if resultat == "HARD" and cat not in errors:
        errors.append(cat)
    time.sleep(0.4)
    gas({
        "action":       "save_score",
        "code":         code,
        "name":         STUDENT_NAME,
        "level":        STUDENT_LEVEL,
        "categorie":    cat,
        "exercice_idx": 0,
        "resultat":     resultat,
        "q":            exo.get("q", ""),
        "time":         random.randint(18, 45),
        "source":       "CALIBRAGE"
    }, f"  diag {cat[:20]} ({resultat})")

print(f"  → Chapitres faibles détectés : {errors[:3]}")

# 4. Génération du boost du jour
print("\n⚡ Génération du boost du jour…")
time.sleep(0.5)
r = gas({
    "action":  "generate_daily_boost",
    "code":    code,
    "level":   STUDENT_LEVEL,
    "errors":  errors[:3]
}, "generate_daily_boost")

boost = r.get("boost", {})
boost_exos = boost.get("exos", [])
print(f"  → {len(boost_exos)} exercices dans le boost ({boost.get('categorie','?')})")

# 5. Simulation du boost (5 exos, résultats variés)
if boost_exos:
    print("\n🏃 Simulation du boost du jour…")
    resultats = ["EASY", "EASY", "HARD", "EASY", "EASY"]  # profil "presque bon"
    for i in range(min(5, len(boost_exos))):
        time.sleep(0.4)
        gas({
            "action":  "save_boost",
            "code":    code,
            "boost":   boost,
            "exoIdx":  i
        }, f"  boost Q{i+1} ({resultats[i]})")

# ══════════════════════════════════════════════════════════════
print("\n" + "═" * 55)
print("✅ Profil démo prêt !")
print(f"   Prénom  : {STUDENT_NAME}")
print(f"   Email   : {STUDENT_EMAIL}")
print(f"   MDP     : {STUDENT_PASS}")
print(f"   Code    : {code}")
print(f"   Niveau  : {STUDENT_LEVEL}")
print(f"\n   Pour tester 'simuler le lendemain' :")
print(f"   → Se connecter avec ce compte")
print(f"   → Ajouter ?sim=1 dans l'URL de la page")
print("═" * 55 + "\n")
