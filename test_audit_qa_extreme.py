#!/usr/bin/env python3
"""
test_audit_qa_extreme.py — Suite de tests de sécurité + robustesse Edge Function.
Créé 2026-04-10 pour l'audit QA pré-lancement indie hacker.

⚠️ À LIRE AVANT DE LANCER :
- Ne cible QUE l'API publique (aucun appel direct Supabase service key).
- N'injecte AUCUNE donnée réelle. Utilise des codes/emails factices.
- Sortie : audit_logs/extreme-{date}.jsonl avec 1 ligne = 1 check.
- Les tests marqués [EXPLOIT] DOIVENT échouer tant que le fix n'est pas déployé.

Usage :
    python3 test_audit_qa_extreme.py

Résumat :
    ✅ vert  = comportement sain
    ❌ rouge = bug / exploit / régression
    ⚠️ warn  = comportement douteux à discuter
"""
import json, os, time, sys
from datetime import date
import requests

API = "https://xlfzhcanzmqqlxtavzrd.supabase.co/functions/v1/api"
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"extreme-{date.today().isoformat()}.jsonl")

# ── Fake identifiers — jamais de vraies valeurs ──
FAKE_VICTIM_EMAIL = "audit-fake-NEVER-A-REAL-USER-zzz@matheux.audit"
FAKE_CODE = "AUDITZ"  # 6 chars, n'existe pas en prod

PASS, FAIL, WARN = 0, 0, 0
ROWS = []

def log(name, severity, expected, got, payload_summary=""):
    global PASS, FAIL, WARN
    row = {
        "ts": time.time(),
        "name": name,
        "severity": severity,        # "ok" | "fail" | "warn"
        "expected": expected,
        "got": got,
        "payload": payload_summary,
    }
    ROWS.append(row)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    icon = {"ok": "✅", "fail": "❌", "warn": "⚠️"}[severity]
    print(f"{icon} {name}")
    print(f"    attendu : {expected}")
    print(f"    obtenu  : {got}")
    if severity == "ok": PASS += 1
    elif severity == "fail": FAIL += 1
    else: WARN += 1

def post(payload):
    try:
        r = requests.post(API, json=payload, timeout=20)
        return r.status_code, r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text
    except Exception as e:
        return 0, {"exception": str(e)}

# ── Tests ───────────────────────────────────────────────

def test_stripe_webhook_forged():
    """[EXPLOIT P0] Webhook Stripe sans signature : un POST forgé accorde premium."""
    code, body = post({
        "type": "checkout.session.completed",
        "data": {"object": {"customer_details": {"email": FAKE_VICTIM_EMAIL}}},
    })
    if body.get("status") == "success":
        log("stripe_webhook_forged",
            "fail",
            "Webhook refusé (signature Stripe manquante)",
            f"{code} {body}",
            "type=checkout.session.completed forged")
    else:
        log("stripe_webhook_forged", "ok", "webhook refusé", body)

def test_action_inconnue():
    code, body = post({"action": "zzz_nope"})
    if body.get("status") == "error" and "inconnue" in str(body.get("message", "")).lower():
        log("action_inconnue", "ok", "rejet propre", body)
    else:
        log("action_inconnue", "fail", "rejet propre", body)

def test_register_invalid_email():
    code, body = post({"action": "register", "name": "X", "email": "not an email",
                       "level": "3EME", "raw_password": "abc123"})
    if "invalide" in str(body.get("message", "")).lower():
        log("register_invalid_email", "ok", "format refusé", body)
    else:
        log("register_invalid_email", "fail", "format refusé", body)

def test_register_invalid_level():
    code, body = post({"action": "register", "name": "X", "email": "fake-audit-1@matheux.audit",
                       "level": "MATERNELLE", "raw_password": "abc123"})
    if "niveau" in str(body.get("message", "")).lower():
        log("register_invalid_level", "ok", "niveau refusé", body)
    else:
        log("register_invalid_level", "fail", "niveau refusé", body)

def test_save_score_invalid_result():
    code, body = post({"action": "save_score", "code": FAKE_CODE, "name": "X", "level": "3EME",
                       "categorie": "Fractions", "exercice_idx": 1, "resultat": "HAXX"})
    if "Résultat invalide" in str(body.get("message", "")):
        log("save_score_invalid_result", "ok", "résultat refusé", body)
    else:
        log("save_score_invalid_result", "fail", "résultat refusé", body)

def test_save_score_missing_fields():
    code, body = post({"action": "save_score", "code": FAKE_CODE})
    if "manquant" in str(body.get("message", "")).lower():
        log("save_score_missing_fields", "ok", "champ manquant détecté", body)
    else:
        log("save_score_missing_fields", "fail", "champ manquant détecté", body)

def test_save_score_code_too_short():
    code, body = post({"action": "save_score", "code": "AB", "name": "X", "level": "3EME",
                       "categorie": "Fractions", "exercice_idx": 1, "resultat": "EASY"})
    if "code" in str(body.get("message", "")).lower():
        log("save_score_short_code", "ok", "code refusé", body)
    else:
        log("save_score_short_code", "fail", "code refusé", body)

def test_identity_check_without_email():
    """[BUG] Sans email fourni, aucune vérification → potentiel squat de code."""
    code, body = post({"action": "save_score", "code": FAKE_CODE, "name": "Z", "level": "3EME",
                       "categorie": "Fractions", "exercice_idx": 1, "resultat": "EASY", "source": "BOOST"})
    # Élève introuvable car code bidon — mais le path montre qu'aucun email check n'a eu lieu
    msg = str(body.get("message", ""))
    if "introuvable" in msg.lower():
        log("identity_check_without_email",
            "warn",
            "Should require email unconditionally (defense in depth)",
            body,
            "no email in payload — relies on code being unknown")
    else:
        log("identity_check_without_email", "ok", "rejet", body)

def test_cors_options():
    try:
        r = requests.options(API, headers={"Origin": "https://matheux.fr"}, timeout=10)
        h = r.headers
        if h.get("Access-Control-Allow-Origin") == "*":
            log("cors_options", "ok", "CORS *", dict(h))
        else:
            log("cors_options", "fail", "CORS *", dict(h))
    except Exception as e:
        log("cors_options", "fail", "CORS réponse", str(e))

def test_generate_diagnostic_level_ok():
    code, body = post({"action": "generate_diagnostic", "level": "3EME", "selectedChapters": []})
    if body.get("status") == "success":
        log("generate_diagnostic_3eme", "ok", "diag généré", f"{len(body.get('exos', []))} exos")
    else:
        log("generate_diagnostic_3eme", "warn", "success", body)

def test_forgot_password_unknown_email():
    code, body = post({"action": "forgot_password", "email": "ghost-audit@matheux.audit"})
    # Ne doit pas révéler si l'email existe ou non (enumeration)
    log("forgot_password_unknown",
        "warn" if body.get("status") == "error" and "introuvable" in str(body).lower() else "ok",
        "pas d'enumeration",
        body)

def test_login_brute_force_shape():
    code, body = post({"action": "login", "email": "ghost-audit@matheux.audit", "password": "xxxxxxxxxxxxxxxxx"})
    log("login_wrong_creds", "ok" if body.get("status") == "error" else "fail",
        "rejet", body)

# ── Run ──────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"=== AUDIT QA EXTRÊME Matheux — {date.today().isoformat()} ===")
    print(f"Log : {LOG_FILE}")
    print(f"API : {API}\n")

    tests = [
        test_action_inconnue,
        test_register_invalid_email,
        test_register_invalid_level,
        test_save_score_invalid_result,
        test_save_score_missing_fields,
        test_save_score_code_too_short,
        test_identity_check_without_email,
        test_cors_options,
        test_generate_diagnostic_level_ok,
        test_forgot_password_unknown_email,
        test_login_brute_force_shape,
        test_stripe_webhook_forged,  # EXPLOIT — laissé en dernier
    ]
    for t in tests:
        try:
            t()
        except Exception as e:
            log(t.__name__, "fail", "exécution propre", f"exception: {e}")
        print()

    print("=" * 60)
    print(f"  ✅ {PASS} OK · ❌ {FAIL} FAIL · ⚠️ {WARN} WARN")
    print("=" * 60)
    sys.exit(0 if FAIL == 0 else 1)
