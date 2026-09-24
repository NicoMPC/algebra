#!/usr/bin/env python3
"""Applique les verdicts du relecteur : `corrige` → remplace l'item par `correction`,
`rejet` → retire l'item. Usage : python3 apply_reviews.py DF GM  (préfixes de domaine)."""
import json, sys, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
doms = sys.argv[1:]
for rp in sorted(glob.glob('*.review.json')):
    src = rp.replace('.review.json', '.json')
    if doms and src.split('.')[0] not in doms:
        continue
    R = json.load(open(rp)); R = R['items'] if isinstance(R, dict) else R
    rev = {i['id']: i for i in R}
    items = json.load(open(src))
    out, n_c, n_r = [], 0, 0
    for it in items:
        v = rev.get(it['id'])
        if v and v['verdict'] == 'rejet':
            n_r += 1; continue
        if v and v['verdict'] == 'corrige':
            it = v['correction']; n_c += 1
        out.append(it)
    json.dump(out, open(src, 'w'), ensure_ascii=False, indent=2)
    print(f"{src}: {n_c} corrigés, {n_r} rejetés, {len(out)} items")
