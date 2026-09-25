#!/usr/bin/env python3
"""Applique les verdicts du relecteur : `corrige` → remplace l'item par `correction`,
`rejet` → retire l'item. Usage : python3 apply_reviews.py DF GM  (préfixes de domaine).
Lit *.review.json et *.train-review.json (relecture du complément d'entraînement)."""
import json, sys, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
# --train : relectures du complément (*.train-review.json) ; sinon relectures du diagnostic (*.review.json).
# ⚠️ Ne pas ré-appliquer les *.review.json déjà appliqués : des corrections manuelles ont été faites
# ensuite (fusion EG.TRANS.02#vecteur_inverse, usage train des compétences hors programme).
TRAIN = '--train' in args
doms = [a for a in args if a != '--train']
for rp in sorted(glob.glob('*.train-review.json') if TRAIN else [f for f in glob.glob('*.review.json') if not f.endswith('.train-review.json')]):
    src = rp.replace('.train-review.json', '.json').replace('.review.json', '.json')
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
