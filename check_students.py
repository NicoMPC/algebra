#!/usr/bin/env python3
"""
check_students.py — Health check données élèves
================================================
Vérifie la cohérence des données de TOUS les vrais élèves.
5 checks, 30 secondes, vert ou rouge.

Usage : python3 check_students.py
"""

from sheets import Sheets
from collections import defaultdict
import json, sys

s = Sheets()
OK = 0
FAIL = 0

def check(cond, label):
    global OK, FAIL
    if cond:
        OK += 1
    else:
        FAIL += 1
        print(f"  ❌ {label}")

def warn(label):
    print(f"  ⚠️  {label}")

# ── Charger les données ──────────────────────────────────────

print("🔍 Chargement des données...")
users = s.read('Users')
scores_raw = s.read_raw('Scores')
scores_h = scores_raw[0]
scores = scores_raw[1:]
boosts_raw = s.read_raw('DailyBoosts')
boosts_h = boosts_raw[0]
boosts = boosts_raw[1:]
suivi_raw = s.read_raw('👁 Suivi')
suivi_h = suivi_raw[0]
suivi = suivi_raw[1:]
remed_raw = s.read_raw('RemediationChapters')
remed_h = remed_raw[0]
remed = remed_raw[1:]

# Index code → lignes
code_idx_suivi = suivi_h.index('Code') if 'Code' in suivi_h else -1

real_users = [u for u in users if u.get('IsAdmin') != '1' and u.get('Code', '') != 'HMD493']
print(f"📋 {len(real_users)} élèves à vérifier\n")

for user in real_users:
    code = user.get('Code', '')
    name = user.get('Prénom', user.get('Prenom', '?'))
    level = user.get('Niveau', '')
    email = user.get('Email', '')
    
    print(f"── {name} ({code}) {'─' * (40 - len(name) - len(code))}")
    
    # ── CHECK 1 : Champs critiques ──
    check(bool(code), f"Code manquant")
    check(bool(level), f"Niveau manquant")
    check(bool(email), f"Email manquant")
    
    # ── CHECK 2 : Doublons scores ──
    my_scores = [r for r in scores if len(r) > 0 and r[0] == code]
    seen = set()
    dupes = 0
    for r in my_scores:
        if len(r) < 14: continue
        key = (r[0], r[3], r[4], r[12], r[13])  # Code, Chapitre, NumExo, Date, Source
        if key in seen:
            dupes += 1
        seen.add(key)
    check(dupes == 0, f"{dupes} doublon(s) dans Scores")
    
    # ── CHECK 3 : Suivi cohérent ──
    my_suivi = None
    for row in suivi:
        if code_idx_suivi >= 0 and len(row) > code_idx_suivi and row[code_idx_suivi] == code:
            my_suivi = row
            break
    
    if my_suivi:
        # Vérifier que les résumés correspondent aux scores
        for ch_idx, res_idx in [(4, 5), (7, 8), (10, 11), (13, 14)]:
            ch_name = my_suivi[ch_idx] if ch_idx < len(my_suivi) else ''
            resume = my_suivi[res_idx] if res_idx < len(my_suivi) else ''
            if ch_name and resume:
                try:
                    data = json.loads(resume)
                    claimed = data.get('exos_faits', 0)
                    # Suivi compte TOUS les scores (y compris CALIBRAGE), sauf BOOST
                    actual = len([r for r in my_scores if len(r) > 13 and r[3] == ch_name and r[13] != 'BOOST'])
                    check(claimed == actual, f"Suivi {ch_name}: exos_faits={claimed} vs Scores={actual}")
                except:
                    pass  # Résumé pas JSON, skip
    else:
        warn(f"Pas de ligne Suivi")
    
    # ── CHECK 4 : Override cohérent ──
    my_remed = [r for r in remed if len(r) > 0 and r[0] == code]
    for rem in my_remed:
        cat = rem[1] if len(rem) > 1 else ''
        date_col = rem[5] if len(rem) > 5 else ''
        if cat and date_col:
            # Les scores V1 doivent avoir date <= override date
            v1_scores = [r for r in my_scores if len(r) > 13 and r[3] == cat and r[13] not in ('CALIBRAGE', 'BOOST')]
            v1_dates = set(r[12] for r in v1_scores if len(r) > 12)
            future_scores = [d for d in v1_dates if d > str(date_col)[:10]]
            check(len(future_scores) == 0, f"Override {cat}: {len(future_scores)} score(s) V1 postérieurs à la date override ({date_col[:10]})")
        elif cat and not date_col:
            check(False, f"Override {cat}: colonne Date VIDE → filtrage V1 impossible")
    
    # ── CHECK 5 : Boost cohérent ──
    my_boosts = [r for r in boosts if len(r) > 0 and r[0] == code]
    for b in my_boosts:
        if len(b) > 4:
            try:
                exos_done = int(b[4]) if b[4] else 0
            except:
                exos_done = 0
            boost_date = b[1] if len(b) > 1 else ''
            boost_scores = [r for r in my_scores if len(r) > 13 and r[13] == 'BOOST' and r[12] == boost_date]
            # ExosDone peut être >= nombre de scores BOOST si rattrapage (P9)
            if exos_done > 0 and len(boost_scores) == 0 and boost_date:
                # Chercher scores BOOST sur d'autres dates (rattrapage P9)
                all_boost_scores = [r for r in my_scores if len(r) > 13 and r[13] == 'BOOST']
                check(len(all_boost_scores) >= exos_done, f"Boost {boost_date}: ExosDone={exos_done} mais {len(all_boost_scores)} scores BOOST total")
    
    # Résumé élève
    non_calib = [r for r in my_scores if len(r) > 13 and r[13] not in ('CALIBRAGE',)]
    if OK > 0 or FAIL > 0:
        status = "✅" if FAIL == 0 else "⚠️"
    print(f"  📊 {len(my_scores)} scores ({len(non_calib)} hors calibrage), {len(my_remed)} override(s), {len(my_boosts)} boost(s)")
    print()

# ── Verdict ──────────────────────────────────────────────────

print("=" * 50)
if FAIL == 0:
    print(f"✅ TOUT EST PROPRE — {OK} checks OK, 0 problème")
else:
    print(f"⚠️  {FAIL} PROBLÈME(S) DÉTECTÉ(S) — {OK} OK, {FAIL} KO")
print("=" * 50)

sys.exit(0 if FAIL == 0 else 1)
