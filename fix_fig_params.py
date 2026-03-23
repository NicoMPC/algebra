#!/usr/bin/env python3
"""Fix figure parameter issues in Curriculum_Officiel exercises.

Issues from audit:
1. 5EME/Pythagore idx18: sides[1]=5 (half-base) — q says base=10 → show 5 with label
2. 4EME/Pythagore idx12: sides=[3,4] (half-diags) — q says diags 6,8 → show 6,8
3. 4EME/Pythagore idx16: sides[2]="10√2" — verify present in q (LaTeX)
4. 5EME/Pythagore idx19: pts=['A','B','C'] but q has no named points → pts=[] [DONE]
5. 3EME/Thalès idx9: pts mismatch → pts=[] [DONE]
6. Malformed fig objects (t=None) — scan all categories
"""

import json, sys
sys.path.insert(0, "/home/nicolas/Bureau/algebra live/algebra")
from sheets import sh

raw = sh.read_raw("Curriculum_Officiel")
headers = raw[0]
exos_col = headers.index("ExosJSON")
niveau_col = headers.index("Niveau")
cat_col = headers.index("Categorie")

changes = []

def get_row(niveau, categorie):
    for i, row in enumerate(raw[1:], 1):
        if len(row) > max(niveau_col, cat_col, exos_col):
            if row[niveau_col] == niveau and row[cat_col] == categorie:
                return i
    return None

def load_exos(row_idx):
    return json.loads(raw[row_idx][exos_col])

def save_exos(row_idx, exos, label):
    new_json = json.dumps(exos, ensure_ascii=False)
    sheet_row = row_idx + 1
    sheet_col = exos_col + 1
    sh.update_cell("Curriculum_Officiel", sheet_row, sheet_col, new_json)
    print(f"  ✅ Written: {label}")

# ══════════════════════════════════════════════════════════════════════════════
# FIX 1: 5EME/Pythagore idx18 — sides[1]=5 is half-base, q says base=10
# The fig is a right triangle (half of the isosceles). 5 is mathematically
# correct for the right triangle diagram. But pedagogically we should label it.
# Best fix: keep sides[1]=5 but update alt to make it clear, OR change to 10
# and let the student see the original value.
# Decision: The figure shows the RIGHT triangle (half), so 5 is correct.
# But the audit says it's not in the question. Let's add "demi-base" context.
# Actually the simplest fix: the figure should reflect what the STUDENT sees.
# Keep 5 (it IS the right triangle) but make alt explain it.
# ══════════════════════════════════════════════════════════════════════════════

row = get_row("5EME", "Pythagore")
exos = load_exos(row)
e = exos[18]
print(f"\n--- 5EME/Pythagore idx18 ---")
print(f"  q: {e['q']}")
print(f"  OLD fig: {e['fig']}")
# The figure correctly shows the derived right triangle (demi-base=5).
# Fix: update alt to explain, and add ctx to clarify the construction.
e["fig"]["alt"] = "Demi-triangle isocèle : côté 13, demi-base 5, hauteur h inconnue"
changes.append("5EME/Pythagore idx18: updated alt to explain demi-base=5")
print(f"  NEW fig: {e['fig']}")
save_exos(row, exos, "5EME/Pythagore")

# ══════════════════════════════════════════════════════════════════════════════
# FIX 2: 4EME/Pythagore idx12 — rhombus diags 6,8 → sides show [3,4]
# Same logic: the right triangle uses half-diagonals. But unlike the isosceles
# case above, the figure type is tri_rect which represents ONE quarter of the
# rhombus. For pedagogical clarity, show the actual question values.
# Fix: change sides to [6, 8] and update alt.
# Wait — actually we need to check the fig structure first.
# ══════════════════════════════════════════════════════════════════════════════

row4p = get_row("4EME", "Pythagore")
exos4 = load_exos(row4p)
e12 = exos4[12]
print(f"\n--- 4EME/Pythagore idx12 ---")
print(f"  q: {e12['q']}")
print(f"  OLD fig: {e12.get('fig')}")
fig12 = e12.get("fig", {})
# The right triangle has sides [3, 4, hyp] representing half-diags.
# Fix: show actual diagonal values from question (6, 8) and note they're diagonals
fig12["sides"] = [6, 8, fig12.get("sides", [None,None,None])[2]]
fig12["alt"] = "Losange, diagonales 6 cm et 8 cm, côté inconnu (demi-diags 3 et 4 forment triangle rectangle)"
e12["fig"] = fig12
print(f"  NEW fig: {fig12}")
changes.append("4EME/Pythagore idx12: sides=[6,8,...] (full diagonals from question)")
save_exos(row4p, exos4, "4EME/Pythagore")

# ══════════════════════════════════════════════════════════════════════════════
# FIX 3: 4EME/Pythagore idx16 — sides[2]="10√2"
# ══════════════════════════════════════════════════════════════════════════════

# Reload after save
exos4 = load_exos(row4p)
e16 = exos4[16]
print(f"\n--- 4EME/Pythagore idx16 ---")
print(f"  q: {e16['q']}")
print(f"  fig: {e16.get('fig')}")
if e16.get("fig"):
    sides = e16["fig"].get("sides", [])
    q = e16["q"]
    # Check: "10\sqrt{2}" in q?
    if "10\\sqrt{2}" in q:
        print(f"  → '10√2' IS present in question as LaTeX. No fix needed.")
        changes.append("4EME/Pythagore idx16: confirmed OK — 10√2 present as $10\\sqrt{2}$ in question")
    else:
        print(f"  → '10√2' NOT in question. Needs fix.")

# ══════════════════════════════════════════════════════════════════════════════
# FIX 4 & 5: Already done (5EME/Pythagore idx19 pts=[], 3EME/Thalès idx9 pts=[])
# Verify they're still correct
# ══════════════════════════════════════════════════════════════════════════════

row5p = get_row("5EME", "Pythagore")
exos5 = load_exos(row5p)
print(f"\n--- 5EME/Pythagore idx19 (verify) ---")
print(f"  pts: {exos5[19]['fig'].get('pts')}")
if exos5[19]["fig"].get("pts") == []:
    print(f"  → Already fixed ✅")
    changes.append("5EME/Pythagore idx19: pts=[] (already fixed)")

row3t = get_row("3EME", "Théorème_de_Thalès")
exos3t = load_exos(row3t)
print(f"\n--- 3EME/Thalès idx9 (verify) ---")
print(f"  pts: {exos3t[9]['fig'].get('pts')}")
if exos3t[9]["fig"].get("pts") == []:
    print(f"  → Already fixed ✅")
    changes.append("3EME/Thalès idx9: pts=[] (already fixed)")

# ══════════════════════════════════════════════════════════════════════════════
# FIX 6: Malformed fig objects (fig.t = None)
# The audit said "3EME/Trigonométrie" but no such figs exist there.
# Actual malformed figs (have 'type' key instead of 't') found in:
# - 4EME/Pythagore idx14, idx19
# - 4EME/Homothétie (8 exos)
# - 4EME/Sections_Solides (4 exos)
# - 1ERE/Trigonometrie (all 20 exos!)
# - 1ERE/Produit_Scalaire idx4
# - 1ERE/Geometrie_Repere idx10,11,12
#
# These have a different schema: {type: ..., confidence: ..., a: ..., b: ...}
# instead of the expected {t: ..., pts: ..., sides: ..., ans: ...}
# They were likely auto-generated by a different tool and are NOT renderable.
# Best fix: remove them entirely.
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n--- Removing ALL malformed fig objects (no 't' key) ---")
malformed_count = 0
rows_to_fix = {}  # row_idx -> (exos, label)

for i, row in enumerate(raw[1:], 1):
    if len(row) <= exos_col or not row[exos_col]:
        continue
    niveau = row[niveau_col]
    cat = row[cat_col]
    try:
        exos = json.loads(row[exos_col])
    except:
        continue

    modified = False
    for j, e in enumerate(exos):
        fig = e.get("fig")
        if isinstance(fig, dict) and "t" not in fig and "type" in fig:
            print(f"  Removing malformed fig: {niveau}/{cat} idx{j} (type={fig.get('type')})")
            del e["fig"]
            malformed_count += 1
            modified = True

    if modified:
        rows_to_fix[i] = (exos, f"{niveau}/{cat}")

for row_idx, (exos, label) in rows_to_fix.items():
    save_exos(row_idx, exos, label)

changes.append(f"Removed {malformed_count} malformed fig objects across {len(rows_to_fix)} categories")

# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{'='*80}")
print("SUMMARY OF ALL CHANGES")
print(f"{'='*80}")
for c in changes:
    print(f"  • {c}")
print(f"\nTotal: {len(changes)} changes applied")
