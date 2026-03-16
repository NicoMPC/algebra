#!/usr/bin/env python3
"""
import_brevet_exos.py — Pousse les exercices Brevet dans le Google Sheet (BrevetExos).

Usage : python3 import_brevet_exos.py
"""

import json, urllib.request, hashlib, sys

GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)

ADMIN_EMAIL = "admin@matheux.fr"
ADMIN_HASH  = "dba3013d8ee56602f8da554bd6f5ff0108324c6d220f137d2181d9d24fa0ef62"

# Récupérer le code admin via login
def get_admin_code():
    r = gas({"action": "login", "email": ADMIN_EMAIL, "password": ADMIN_HASH}, "login admin")
    code = r.get("profile", {}).get("code", "")
    if not code:
        print("❌ Impossible de récupérer le code admin")
        sys.exit(1)
    return code

def gas(payload, label=""):
    body = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        GAS_URL, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode("utf-8"))
            status = d.get("status", "?")
            ok = "✅" if status == "success" else "❌"
            print(f"  {ok} {label}: {status}" +
                  (f" ({d.get('message', '')})" if status != "success" else ""))
            return d
    except Exception as e:
        print(f"  ❌ {label}: ERREUR {e}")
        return {}

# ── Charger le JSON ──────────────────────────────────────────────────────────
with open("brevet_exos_3eme.json", "r", encoding="utf-8") as f:
    brevet_data = json.load(f)

# ── Préparer le payload ──────────────────────────────────────────────────────
data = []
total_exos = 0
for niveau, chapitres in brevet_data.items():
    for categorie, exos in chapitres.items():
        data.append({
            "niveau":    niveau,
            "categorie": categorie,
            "exos":      exos
        })
        total_exos += len(exos)

print(f"\n🎓 Import exercices Brevet Blanc")
print(f"   {len(data)} chapitres · {total_exos} exercices")
print("─" * 50)

# ── Récupérer le code admin ───────────────────────────────────────────────────
print("🔑 Connexion admin…")
admin_code = get_admin_code()
print(f"   Code admin : {admin_code}")

# ── Envoyer via GAS import_brevet_exos ───────────────────────────────────────
r = gas({
    "action":    "import_brevet_exos",
    "adminCode": admin_code,
    "data":      data
}, "import_brevet_exos")

if r.get("status") == "success":
    print(f"\n✅ Import terminé !")
    print(f"   Insérés : {r.get('inserted', 0)}")
    print(f"   Mis à jour : {r.get('updated', 0)}")
    print(f"   Total : {r.get('total', 0)}")
else:
    print(f"\n❌ Import échoué : {r.get('message', 'erreur inconnue')}")
    sys.exit(1)

print("\n" + "═" * 50)
print("   Chapitres créés dans l'onglet BrevetExos :")
for item in data:
    print(f"   · {item['niveau']} — {item['categorie']} ({len(item['exos'])} exos)")
print("═" * 50 + "\n")
