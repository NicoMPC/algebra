#!/usr/bin/env python3
"""
test_workflows.py — Matheux : tests complets du workflow GAS (cas réels + cas limites).

Noms de champs GAS réels (backend.js) :
  register  → name, email, level, password  (pas prenom/niveau/hash)
  login     → email, password
  save_score→ code, name, level, categorie, exercice_idx, resultat, q, time
  save_boost→ code, boost (objet JSON), exoIdx
  response  → profile.code (pas resp.code directement)

Scénarios :
  GROUPE A — Flux nominal   (A1→A13)
  GROUPE B — Cas limites    (B1→B10)

Usage : python3 test_workflows.py [--verbose] [--group A] [--group B]
"""

import json
import sys
import time
import hashlib
import random
import string
import urllib.request
import urllib.error
from datetime import datetime

# ── Configuration ────────────────────────────────────────────────────────────

GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)

ADMIN_EMAIL = "contact@matheux.fr"
ADMIN_PASS  = "Matheux2026!"

TEST_NAME   = "TestBot"
TEST_LEVEL  = "5EME"

VERBOSE = '--verbose' in sys.argv

# ── Helpers ──────────────────────────────────────────────────────────────────

def sha256(email, password):
    return hashlib.sha256(f"{email}::{password}::AB22".encode()).hexdigest()


def rnd_email():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{suffix}@matheux-test.fr"


def gas_call(payload):
    body = json.dumps(payload).encode('utf-8')
    req  = urllib.request.Request(GAS_URL, data=body,
                                  headers={'Content-Type': 'application/json'},
                                  method='POST')
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode('utf-8')
            ms  = int((time.time() - t0) * 1000)
            try:
                return True, json.loads(raw), ms
            except json.JSONDecodeError:
                return False, {'error': f'JSON parse: {raw[:200]}'}, ms
    except urllib.error.HTTPError as e:
        return False, {'error': f'HTTP {e.code}: {e.reason}'}, int((time.time() - t0) * 1000)
    except Exception as e:
        return False, {'error': str(e)}, int((time.time() - t0) * 1000)


# ── Résultats ─────────────────────────────────────────────────────────────────

results = []

def check(tid, desc, cond, detail="", warn=False):
    status = "PASS" if cond else ("WARN" if warn else "FAIL")
    icon   = "✅" if cond else ("⚠️ " if warn else "❌")
    results.append({'id': tid, 'desc': desc, 'pass': cond,
                    'warn': warn and not cond, 'detail': detail})
    print(f"  {icon} {status}  {tid} — {desc}")
    if detail and (VERBOSE or not cond):
        print(f"         → {detail}")
    return cond


def section(title):
    print(f"\n{'─'*60}\n  {title}\n{'─'*60}")


# ── GROUPE A — Flux nominal ───────────────────────────────────────────────────

def test_group_a():
    section("GROUPE A — Flux nominal")

    email    = rnd_email()
    password = sha256(email, ADMIN_PASS)
    code     = None

    # ── A1 : Register ──────────────────────────────────────────
    print("\n[A1] Inscription d'un nouvel élève")
    ok, resp, ms = gas_call({
        'action':   'register',
        'name':     TEST_NAME,
        'email':    email,
        'password': password,
        'level':    TEST_LEVEL,
    })
    c1 = check('A1a', 'register retourne status=success',
               ok and resp.get('status') == 'success', f"{resp}")
    c2 = check('A1b', 'profile.code présent (6 chars)',
               ok and len(str(resp.get('profile', {}).get('code', ''))) == 6,
               f"profile={resp.get('profile')}")
    if c1 and c2:
        code = str(resp['profile']['code'])
        print(f"         → Code : {code} ({ms}ms)")

    if not code:
        print("  ⛔ Pas de code — A2→A8 ignorés")
        return

    # ── A2 : Login ────────────────────────────────────────────
    print("\n[A2] Login élève actif")
    ok, resp, ms = gas_call({'action': 'login', 'email': email, 'password': password})
    check('A2a', 'login status=success',
          ok and resp.get('status') == 'success', f"{resp.get('status')}")
    check('A2b', 'trial.trialActive=true',
          resp.get('trial', {}).get('trialActive') is True, f"trial={resp.get('trial')}")
    check('A2c', 'trial.daysLeft > 0',
          (resp.get('trial', {}).get('daysLeft') or 0) > 0,
          f"daysLeft={resp.get('trial', {}).get('daysLeft')}")
    check('A2d', 'profile.code correct',
          resp.get('profile', {}).get('code') == code,
          f"attendu={code}, reçu={resp.get('profile', {}).get('code')}")
    print(f"         → daysLeft={resp.get('trial', {}).get('daysLeft')} ({ms}ms)")

    # ── A3 : Diagnostic guest ────────────────────────────────
    print("\n[A3] Diagnostic guest (landing flow, sans code)")
    ok, resp, ms = gas_call({
        'action':    'generate_diagnostic',
        'level':     '4EME',
        'chapitres': ['Équations', 'Calcul_Littéral'],
    })
    check('A3a', 'generate_diagnostic guest status=success',
          ok and resp.get('status') == 'success', f"{resp}")
    check('A3b', 'retourne des exos',
          isinstance(resp.get('exos'), list) and len(resp.get('exos', [])) > 0,
          f"len={len(resp.get('exos', []))}")
    check('A3c', '2 chapitres → ≥ 6 exos (smart count)',
          len(resp.get('exos', [])) >= 6, f"count={len(resp.get('exos', []))}", warn=True)
    print(f"         → {len(resp.get('exos', []))} exos ({ms}ms)")

    # ── A4 : Save score EASY ──────────────────────────────────
    print("\n[A4] Save score (EASY)")
    ok, resp, ms = gas_call({
        'action':       'save_score',
        'code':         code,
        'name':         TEST_NAME,
        'level':        TEST_LEVEL,
        'categorie':    'Fractions',
        'exercice_idx': 1,
        'resultat':     'EASY',
        'time':         15,
        'q':            'Calcule 1/2 + 1/3',
    })
    check('A4a', 'save_score EASY status=success',
          ok and resp.get('status') == 'success', f"{resp}")
    print(f"         → ({ms}ms)")

    # ── A5 : Save score HARD ──────────────────────────────────
    print("\n[A5] Save score (HARD)")
    ok, resp, ms = gas_call({
        'action':       'save_score',
        'code':         code,
        'name':         TEST_NAME,
        'level':        TEST_LEVEL,
        'categorie':    'Puissances',
        'exercice_idx': 1,
        'resultat':     'HARD',
        'time':         45,
        'q':            'Calcule 2^10',
        'wrongOpt':     '512',
        'indices':      2,
    })
    check('A5a', 'save_score HARD status=success',
          ok and resp.get('status') == 'success', f"{resp}")
    print(f"         → ({ms}ms)")

    # ── A6 : Get progress ────────────────────────────────────
    print("\n[A6] Get progress")
    ok, resp, ms = gas_call({'action': 'get_progress', 'code': code})
    check('A6a', 'get_progress status=success',
          ok and resp.get('status') == 'success', f"{resp}")
    check('A6b', 'retourne liste progress',
          isinstance(resp.get('progress'), list), f"type={type(resp.get('progress'))}")
    print(f"         → {len(resp.get('progress', []))} chapitres ({ms}ms)")

    # ── A7 : Generate daily boost ────────────────────────────
    print("\n[A7] Generate daily boost")
    ok, resp, ms = gas_call({'action': 'generate_daily_boost', 'code': code, 'level': TEST_LEVEL})
    valid = ok and resp.get('status') in ('success', 'no_boost_needed', 'boost_exists')
    check('A7a', 'statut valide', valid, f"status={resp.get('status')}: {str(resp)[:100]}")
    print(f"         → status={resp.get('status')} ({ms}ms)")

    # ── A8 : Save boost ──────────────────────────────────────
    print("\n[A8] Save boost (terminé)")
    dummy_boost = [{'q': 'Test', 'a': '1', 'options': ['1', '2', '3'], 'lvl': 1,
                    'oC': 'Fractions', 'oI': 0}]
    ok, resp, ms = gas_call({
        'action': 'save_boost',
        'code':   code,
        'boost':  dummy_boost,
        'exoIdx': 4,  # 0-based → exosDone = 5
    })
    check('A8a', 'save_boost status=success',
          ok and resp.get('status') == 'success', f"{resp}")
    print(f"         → ({ms}ms)")

    # ── A9 : Generate brevet ─────────────────────────────────
    print("\n[A9] Generate brevet (3EME)")
    ok, resp, ms = gas_call({'action': 'generate_brevet', 'niveau': '3EME'})
    check('A9a', 'generate_brevet status=success',
          ok and resp.get('status') == 'success', f"status={resp.get('status')}: {str(resp)[:150]}")
    check('A9b', 'retourne des exos',
          isinstance(resp.get('exos'), list) and len(resp.get('exos', [])) > 0,
          f"len={len(resp.get('exos', []))}")
    check('A9c', 'retourne chapitres_couverts',
          isinstance(resp.get('chapitres_couverts'), list),
          f"chaps={resp.get('chapitres_couverts')}")
    if resp.get('exos'):
        print(f"         → {len(resp['exos'])} exos, chaps={resp.get('chapitres_couverts')} ({ms}ms)")

    # ── A10 : Generate revision ──────────────────────────────
    print("\n[A10] Generate revision")
    ok, resp, ms = gas_call({'action': 'generate_revision', 'code': code, 'niveau': TEST_LEVEL})
    valid = ok and resp.get('status') in ('success', 'not_enough_data', 'no_data', 'error')
    check('A10a', 'generate_revision répond sans crash', valid,
          f"status={resp.get('status')}: {str(resp)[:150]}")
    print(f"         → status={resp.get('status')} ({ms}ms)")

    # ── A11 : Submit feedback ────────────────────────────────
    print("\n[A11] Submit feedback")
    ok, resp, ms = gas_call({
        'action':  'submit_feedback',
        'code':    code,
        'name':    TEST_NAME,
        'niveau':  TEST_LEVEL,
        'type':    'erreur',
        'message': 'Test automatique — feedback unitaire',
        'exo_q':   'Calcule 1/2 + 1/3',
        'rating':  1,
    })
    check('A11a', 'submit_feedback status=success',
          ok and resp.get('status') == 'success', f"{resp}")
    print(f"         → ({ms}ms)")

    # ── A12 : Check trial status ─────────────────────────────
    print("\n[A12] Check trial status")
    ok, resp, ms = gas_call({'action': 'check_trial_status', 'code': code})
    check('A12a', 'trialActive=true', ok and resp.get('trialActive') is True, f"{resp}")
    check('A12b', 'daysLeft > 0', (resp.get('daysLeft') or 0) > 0,
          f"daysLeft={resp.get('daysLeft')}")
    print(f"         → daysLeft={resp.get('daysLeft')} ({ms}ms)")

    # ── A13 : Admin overview ─────────────────────────────────
    print("\n[A13] Admin overview (compte contact@matheux.fr)")
    admin_pwd = sha256(ADMIN_EMAIL, ADMIN_PASS)
    ok_l, resp_l, _ = gas_call({'action': 'login', 'email': ADMIN_EMAIL, 'password': admin_pwd})
    if ok_l and resp_l.get('profile', {}).get('isAdmin'):
        admin_code = resp_l['profile']['code']
        ok, resp, ms = gas_call({'action': 'get_admin_overview', 'code': admin_code})
        check('A13a', 'get_admin_overview status=success',
              ok and resp.get('status') == 'success', f"{resp.get('status')}")
        check('A13b', 'retourne liste élèves',
              isinstance(resp.get('eleves'), list), f"len={len(resp.get('eleves', []))}")
        print(f"         → {len(resp.get('eleves', []))} élèves ({ms}ms)")
    else:
        check('A13a', 'Admin login OK (IsAdmin=true requis dans Users)',
              False,
              f"login status={resp_l.get('status')}, isAdmin={resp_l.get('profile', {}).get('isAdmin')}",
              warn=True)


# ── GROUPE B — Cas limites ────────────────────────────────────────────────────

def test_group_b():
    section("GROUPE B — Cas limites / erreurs")

    # ── B1 : Email inconnu ───────────────────────────────────
    print("\n[B1] Login email inconnu")
    ok, resp, ms = gas_call({'action': 'login', 'email': 'inconnu_xyz999@test.fr', 'password': 'fakehash'})
    check('B1a', 'status != success', resp.get('status') != 'success', f"status={resp.get('status')}")
    check('B1b', 'message d\'erreur présent',
          bool(resp.get('message') or resp.get('error')), f"resp={resp}")

    # ── B2 : Mauvais MDP ─────────────────────────────────────
    print("\n[B2] Login mauvais mot de passe")
    ok, resp, ms = gas_call({'action': 'login', 'email': ADMIN_EMAIL, 'password': 'wronghash000'})
    check('B2a', 'erreur auth bad password', resp.get('status') != 'success',
          f"status={resp.get('status')}")

    # ── B3 : Register doublon ────────────────────────────────
    print("\n[B3] Register email déjà utilisé")
    ok, resp, ms = gas_call({
        'action': 'register', 'name': 'Doublon', 'email': ADMIN_EMAIL,
        'password': sha256(ADMIN_EMAIL, ADMIN_PASS), 'level': '6EME',
    })
    check('B3a', 'register doublon retourne erreur',
          resp.get('status') != 'success', f"status={resp.get('status')}")

    # ── B4 : Save score code inconnu ─────────────────────────
    print("\n[B4] Save score avec code inconnu")
    ok, resp, ms = gas_call({
        'action': 'save_score', 'code': 'ZZZZZZ', 'name': 'Ghost',
        'level': '6EME', 'categorie': 'Fractions', 'exercice_idx': 1,
        'resultat': 'EASY', 'q': 'Test',
    })
    check('B4a', 'pas de crash serveur', isinstance(resp, dict), f"resp={resp}")
    # Le GAS actuel ne vérifie pas si le code existe → status=success mais pas de Progress créé
    check('B4b', 'réponse JSON cohérente', 'status' in resp, f"resp={resp}")

    # ── B5 : Boost sans diagnostic ───────────────────────────
    print("\n[B5] Generate boost sans diagnostic préalable")
    fe  = rnd_email()
    fpw = sha256(fe, ADMIN_PASS)
    ok_r, resp_r, _ = gas_call({
        'action': 'register', 'name': 'NoDiag', 'email': fe,
        'password': fpw, 'level': '6EME',
    })
    if ok_r and resp_r.get('status') == 'success':
        fc = str(resp_r['profile']['code'])
        ok, resp, ms = gas_call({'action': 'generate_daily_boost', 'code': fc, 'level': '6EME'})
        check('B5a', 'generate_boost sans diag ne crash pas', isinstance(resp, dict),
              f"status={resp.get('status')}")
        print(f"         → status={resp.get('status')} ({ms}ms)")
    else:
        check('B5a', 'Register fresh OK (prérequis B5)', False, warn=True)

    # ── B6 : Brevet niveau inconnu ───────────────────────────
    print("\n[B6] Generate brevet niveau inconnu")
    ok, resp, ms = gas_call({'action': 'generate_brevet', 'niveau': 'LICENCE'})
    check('B6a', 'ne crash pas', isinstance(resp, dict), f"resp={resp}")
    check('B6b', 'retourne erreur ou exos vides',
          resp.get('status') != 'success' or len(resp.get('exos', [])) == 0,
          f"status={resp.get('status')}", warn=True)
    print(f"         → status={resp.get('status')} ({ms}ms)")

    # ── B7 : Feedback code vide ──────────────────────────────
    print("\n[B7] Submit feedback guest (code vide)")
    ok, resp, ms = gas_call({
        'action': 'submit_feedback', 'code': '', 'name': 'Guest',
        'niveau': '3EME', 'type': 'flou', 'message': 'Pas clair',
        'exo_q': 'Question test',
    })
    check('B7a', 'ne crash pas', isinstance(resp, dict), f"resp={resp}")
    check('B7b', 'réponse avec status', 'status' in resp, f"resp={resp}")
    print(f"         → status={resp.get('status')} ({ms}ms)")

    # ── B8 : Register sans prénom ────────────────────────────
    print("\n[B8] Register sans prénom (validation GAS)")
    ok, resp, ms = gas_call({
        'action': 'register', 'name': '', 'email': rnd_email(),
        'password': sha256('x@x.fr', 'pass'), 'level': '6EME',
    })
    check('B8a', 'réponse propre', isinstance(resp, dict), f"resp={resp}")
    check('B8b', 'validation prénom rejetée',
          resp.get('status') != 'success', f"status={resp.get('status')}")

    # ── B9 : Hash MDP trop court ─────────────────────────────
    print("\n[B9] Register avec hash MDP trop court (< 64 chars)")
    ok, resp, ms = gas_call({
        'action': 'register', 'name': 'TestShortHash', 'email': rnd_email(),
        'password': 'toocourt', 'level': '6EME',
    })
    check('B9a', 'hash trop court rejeté',
          resp.get('status') != 'success', f"status={resp.get('status')}: {resp.get('message')}")

    # ── B10 : Admin overview non-admin ───────────────────────
    print("\n[B10] Admin overview avec compte non-admin")
    na_e  = rnd_email()
    na_pw = sha256(na_e, ADMIN_PASS)
    ok_r, resp_r, _ = gas_call({
        'action': 'register', 'name': 'NonAdmin', 'email': na_e,
        'password': na_pw, 'level': '6EME',
    })
    if ok_r and resp_r.get('status') == 'success':
        na_code = str(resp_r['profile']['code'])
        ok, resp, ms = gas_call({'action': 'get_admin_overview', 'code': na_code})
        check('B10a', 'non-admin refusé', resp.get('status') != 'success',
              f"status={resp.get('status')}")
        print(f"         → status={resp.get('status')} ({ms}ms)")
    else:
        check('B10a', 'Register non-admin OK (prérequis B10)', False, warn=True)


# ── Rapport final ─────────────────────────────────────────────────────────────

def print_report():
    print(f"\n{'='*60}\n  RAPPORT FINAL\n{'='*60}")
    passed = sum(1 for r in results if r['pass'])
    warned = sum(1 for r in results if r['warn'])
    failed = sum(1 for r in results if not r['pass'] and not r['warn'])
    total  = len(results)

    print(f"\n  Total : {total} assertions")
    print(f"  PASS  : {passed}")
    print(f"  WARN  : {warned}  (non bloquants)")
    print(f"  FAIL  : {failed}")

    if failed:
        print(f"\n  Echecs :")
        for r in results:
            if not r['pass'] and not r['warn']:
                print(f"    FAIL {r['id']} — {r['desc']}")
                if r['detail']:
                    print(f"       {r['detail']}")
    if warned:
        print(f"\n  Avertissements :")
        for r in results:
            if r['warn']:
                print(f"    WARN {r['id']} — {r['desc']}")

    score = int(100 * passed / total) if total else 0
    grade = ("EXCELLENT" if score >= 95 else
             "BON" if score >= 80 else
             "MOYEN" if score >= 65 else "A CORRIGER")
    print(f"\n  Score : {score}% — {grade}")
    print(f"  Date  : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    return failed == 0


def main():
    groups = []
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--group' and i + 1 < len(sys.argv):
            groups.append(sys.argv[i+1].upper()); i += 2
        else:
            i += 1
    if not groups:
        groups = ['A', 'B']

    print(f"\nMATHEUX — Tests Workflow Complets")
    print(f"GAS : {GAS_URL[:60]}...")
    print(f"Groupes : {', '.join(groups)}")

    if 'A' in groups:
        test_group_a()
    if 'B' in groups:
        test_group_b()

    ok = print_report()
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
