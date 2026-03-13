#!/usr/bin/env python3
"""
test_coherence_boost.py — Vérifie la cohérence du fix CALIBRAGE/BOOST.

Bug corrigé : les scores diagnostics étaient sauvés avec categorie = nom_chapitre
au lieu de 'CALIBRAGE', ce qui faisait apparaître des chapitres "entamés" fantômes.

Le fix touche :
  - index.html ~2095 : categorie: 'CALIBRAGE' (sauvegarde diagnostic)
  - index.html ~2205 : categorie: 'CALIBRAGE' (modal flow)
  - backend.js ~364  : login() filtre CALIBRAGE du history
  - backend.js ~525  : saveScore() exclut CALIBRAGE de Progress
  - backend.js ~1344 : rebuildSuivi() filtre CALIBRAGE
  - backend.js ~2798 : getAdminOverview() filtre CALIBRAGE

Usage: python3 test_coherence_boost.py
Exit 0 si tout passe, 1 sinon.
"""

import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(BASE, 'index.html')
BACKEND = os.path.join(BASE, 'backend.js')

passed = 0
failed = 0


def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}")
        if detail:
            print(f"        -> {detail}")


def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def lines(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()


# ──────────────────────────────────────────────────────────────
# 1. FRONTEND — index.html
# ──────────────────────────────────────────────────────────────
print("\n=== FRONTEND (index.html) ===\n")

html = read(INDEX)
html_lines = lines(INDEX)

# 1a. Diagnostic save (~line 2095): categorie must be 'CALIBRAGE'
#     Search for the save_score block with source: 'CALIBRAGE' near _flowExos.map
region_diag = None
for i, line in enumerate(html_lines):
    if '_flowExos.map' in line and 'save' in line.lower():
        # Grab surrounding 20 lines
        region_diag = ''.join(html_lines[i:i+20])
        break

check(
    "Diagnostic save uses categorie: 'CALIBRAGE'",
    region_diag is not None and re.search(r"categorie:\s*'CALIBRAGE'", region_diag),
    "Expected categorie: 'CALIBRAGE' in _flowExos.map save block"
)

check(
    "Diagnostic save does NOT use exo.oC or exo.categorie for categorie",
    region_diag is not None and not re.search(r"categorie:\s*(exo\.oC|exo\.categorie)", region_diag),
    "categorie should NOT reference exo.oC or exo.categorie"
)

check(
    "Diagnostic save includes source: 'CALIBRAGE'",
    region_diag is not None and re.search(r"source:\s*'CALIBRAGE'", region_diag),
    "source field should also be 'CALIBRAGE'"
)

# 1b. Modal flow save (~line 2205): categorie must be 'CALIBRAGE'
#     Search for _flowResults.forEach with save_score
region_modal = None
for i, line in enumerate(html_lines):
    if '_flowResults.forEach' in line:
        region_modal = ''.join(html_lines[i:i+25])
        break

check(
    "Modal flow save uses categorie: 'CALIBRAGE'",
    region_modal is not None and re.search(r"categorie:\s*'CALIBRAGE'", region_modal),
    "Expected categorie: 'CALIBRAGE' in _flowResults.forEach block"
)

check(
    "Modal flow save does NOT use exo.categorie for categorie",
    region_modal is not None and not re.search(r"categorie:\s*(exo\.categorie|exo\.oC)", region_modal),
    "categorie should NOT reference exo.categorie"
)

check(
    "Modal flow save includes source: 'CALIBRAGE'",
    region_modal is not None and re.search(r"source:\s*'CALIBRAGE'", region_modal),
    "source field should also be 'CALIBRAGE'"
)

# 1c. initApp — CALIBRAGE keys in S.res are harmless (no fix needed)
#     Just verify that initApp doesn't explicitly strip CALIBRAGE (it doesn't need to)
#     because keys like '5EME-CALIBRAGE-0' won't match any curriculum chapter.
calibrage_strip_in_initapp = bool(re.search(r"function\s+initApp.*?CALIBRAGE", html, re.DOTALL))
# This is informational — not a failure either way
print(f"  INFO  initApp mentions CALIBRAGE: {calibrage_strip_in_initapp} (harmless either way)")


# ──────────────────────────────────────────────────────────────
# 2. BACKEND — backend.js
# ──────────────────────────────────────────────────────────────
print("\n=== BACKEND (backend.js) ===\n")

backend = read(BACKEND)
backend_lines = lines(BACKEND)

# 2a. login() filters out CALIBRAGE from history
#     Look for the filter block that excludes CALIBRAGE
login_region = None
for i, line in enumerate(backend_lines):
    if "Exclure CALIBRAGE" in line or ("CALIBRAGE" in line and "filter" in ''.join(backend_lines[max(0,i-5):i])):
        login_region = ''.join(backend_lines[max(0,i-3):i+5])
        break

check(
    "login() filters CALIBRAGE from history",
    login_region is not None and "=== 'CALIBRAGE'" in login_region and "return false" in login_region,
    "Expected chap === 'CALIBRAGE' → return false in login history filter"
)

# 2b. saveScore() skips Progress update for CALIBRAGE
save_score_calibrage = re.search(
    r"source\s*!==\s*'CALIBRAGE'|source\s*!==\s*['\"]BOOST['\"]\s*&&\s*source\s*!==\s*['\"]CALIBRAGE['\"]",
    backend
)
check(
    "saveScore() excludes CALIBRAGE from Progress update",
    save_score_calibrage is not None,
    "Expected source !== 'CALIBRAGE' check in saveScore confidence/streak block"
)

# 2c. rebuildSuivi() filters out CALIBRAGE
rebuild_match = re.search(r"cat\s*===\s*'CALIBRAGE'", backend)
check(
    "rebuildSuivi() filters out CALIBRAGE",
    rebuild_match is not None,
    "Expected cat === 'CALIBRAGE' filter in rebuildSuivi"
)

# 2d. getAdminOverview() filters out CALIBRAGE
admin_match = re.search(r"cat\s*===\s*'CALIBRAGE'.*cat\s*===\s*'BOOST'|cat\s*===\s*'BOOST'.*cat\s*===\s*'CALIBRAGE'", backend)
# Alternative: just check the line with both CALIBRAGE and BOOST in getAdminOverview context
admin_line_found = False
for i, line in enumerate(backend_lines):
    if 'CALIBRAGE' in line and 'BOOST' in line and 'return' in line:
        admin_line_found = True
        break

check(
    "getAdminOverview() filters out CALIBRAGE (and BOOST)",
    admin_match is not None or admin_line_found,
    "Expected CALIBRAGE + BOOST filter in admin overview scores"
)


# ──────────────────────────────────────────────────────────────
# 3. CONSISTENCY — all places agree on the keyword 'CALIBRAGE'
# ──────────────────────────────────────────────────────────────
print("\n=== CONSISTENCY ===\n")

# Count occurrences of the CALIBRAGE keyword in both files
html_calibrage = re.findall(r"'CALIBRAGE'|\"CALIBRAGE\"", html)
backend_calibrage = re.findall(r"'CALIBRAGE'|\"CALIBRAGE\"", backend)

check(
    f"index.html uses 'CALIBRAGE' consistently ({len(html_calibrage)} occurrences)",
    len(html_calibrage) >= 4,  # at least: 2x categorie + 2x source
    f"Found {len(html_calibrage)} occurrences, expected >= 4"
)

check(
    f"backend.js uses 'CALIBRAGE' consistently ({len(backend_calibrage)} occurrences)",
    len(backend_calibrage) >= 3,  # login filter + saveScore + rebuildSuivi + adminOverview
    f"Found {len(backend_calibrage)} occurrences, expected >= 3"
)

# Ensure no typos like 'calibrage' (lowercase) or 'Calibrage' (mixed case)
bad_case_html = re.findall(r"['\"](?:calibrage|Calibrage)['\"]", html, re.IGNORECASE)
bad_case_html = [m for m in bad_case_html if 'CALIBRAGE' not in m]
bad_case_backend = re.findall(r"['\"](?:calibrage|Calibrage)['\"]", backend, re.IGNORECASE)
bad_case_backend = [m for m in bad_case_backend if 'CALIBRAGE' not in m]

check(
    "No case-variant typos of CALIBRAGE in index.html",
    len(bad_case_html) == 0,
    f"Found variants: {bad_case_html}"
)

check(
    "No case-variant typos of CALIBRAGE in backend.js",
    len(bad_case_backend) == 0,
    f"Found variants: {bad_case_backend}"
)


# ──────────────────────────────────────────────────────────────
# SUMMARY
# ──────────────────────────────────────────────────────────────
total = passed + failed
print(f"\n{'='*50}")
print(f"  {passed}/{total} checks passed, {failed} failed")
print(f"{'='*50}\n")

sys.exit(0 if failed == 0 else 1)
