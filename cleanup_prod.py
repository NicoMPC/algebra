#!/usr/bin/env python3
"""
cleanup_prod.py — Nettoyage complet de la base de prod Matheux.

⚠️  IRRÉVERSIBLE — supprime tous les comptes non-admin et vide les données.

Usage : python3 cleanup_prod.py
"""

import json, hashlib, urllib.request, urllib.error, sys

GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)

ADMIN_EMAIL = "admin@matheux.fr"
ADMIN_PASS  = "Admin123"

def sha256_hash(email, password):
    return hashlib.sha256(f"{email}::{password}::AB22".encode()).hexdigest()

def gas(payload, label=""):
    body = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(GAS_URL, data=body,
                                  headers={"Content-Type": "application/json"},
                                  method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  ❌ {label} → ERREUR réseau : {e}")
        return {}

# ══════════════════════════════════════════════════════════════
print("\n🧹 NETTOYAGE BASE DE PROD MATHEUX")
print("═" * 50)
print("⚠️  Cette opération est IRRÉVERSIBLE.")
print(f"   Compte admin conservé : {ADMIN_EMAIL}")
print("   Tous les autres comptes seront supprimés.")
print("   Toutes les données (scores, boosts, etc.) seront vidées.")
print("═" * 50)

confirm = input("\nTaper 'CLEAN' pour confirmer : ").strip()
if confirm != "CLEAN":
    print("Annulé.")
    sys.exit(0)

# 1. Login admin pour récupérer le code
print("\n1. Login admin…")
pwd_hash = sha256_hash(ADMIN_EMAIL, ADMIN_PASS)
r = gas({"action": "login", "email": ADMIN_EMAIL, "password": pwd_hash}, "login")
if r.get("status") != "success":
    print(f"❌ Login échoué : {r.get('message', r)}")
    sys.exit(1)

admin_code = r.get("profile", {}).get("code", "")
admin_name = r.get("profile", {}).get("name", "")
print(f"   ✅ Connecté : {admin_name} (code={admin_code})")

if not admin_code:
    print("❌ Code admin introuvable. Abandon.")
    sys.exit(1)

# 2. Appel cleanup_all
print("\n2. Nettoyage en cours (peut prendre 15-30s)…")
r = gas({"action": "cleanup_all", "adminCode": admin_code}, "cleanup_all")

if r.get("status") != "success":
    print(f"❌ Erreur cleanup : {r.get('message', r)}")
    sys.exit(1)

print("\n✅ Nettoyage terminé !")
for line in r.get("results", []):
    print(f"   • {line}")

print("\n" + "═" * 50)
print("Base de prod nettoyée. Seul le compte admin reste.")
print("═" * 50 + "\n")
