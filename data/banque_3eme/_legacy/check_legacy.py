#!/usr/bin/env python3
"""check_legacy.py — vérifie la banque legacy convertie (data/banque_3eme/_legacy/**.json).

Contrôles : comp ∈ référentiel ; chaque id d'erreur de `err` existe et appartient à la
compétence de l'item ; clés `err` ≠ a (et ∈ options pour qcm/vf) ; ids uniques dans
_legacy ET vs les fichiers <DOM>.<THEME>.json de data/banque_3eme ; usage == ["train"].
Usage : python3 data/banque_3eme/_legacy/check_legacy.py
"""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REF = {c["id"]: c for c in json.load(open(os.path.join(HERE, "..", "..", "referentiel_3eme", "competences.json"), encoding="utf-8"))}
ERR = {e["id"]: c["id"] for c in REF.values() for e in c["erreurs"]}
norm = lambda s: re.sub(r"[\s$]", "", str(s)).lower()
errs, ids, n, n_err = [], {}, 0, 0
for f in sorted(glob.glob(os.path.join(HERE, "**", "*.json"), recursive=True)):
    name = os.path.relpath(f, HERE)
    for it in json.load(open(f, encoding="utf-8")):
        n += 1
        iid = it.get("id")
        if iid in ids: errs.append(f"{name}: id en double {iid} (déjà dans {ids[iid]})")
        ids[iid] = name
        if not re.match(r"^[A-Z]{2}\.[A-Z]{3,5}\.\d{2}-L\d{3}$", iid or ""): errs.append(f"{name}: id mal formé {iid}")
        c = it.get("comp")
        if c not in REF: errs.append(f"{name}:{iid} comp inconnue {c}")
        elif not iid.startswith(c + "-"): errs.append(f"{name}:{iid} id ne commence pas par comp")
        for s in it.get("comp_secondaires", []):
            if s not in REF: errs.append(f"{name}:{iid} comp secondaire inconnue {s}")
        if it.get("usage") != ["train"]: errs.append(f"{name}:{iid} usage ≠ ['train']")
        for w, e in it.get("err", {}).items():
            n_err += 1
            if e not in ERR: errs.append(f"{name}:{iid} erreur inconnue {e}")
            elif ERR[e] != c: errs.append(f"{name}:{iid} erreur {e} d'une autre compétence")
            if norm(w) == norm(it["a"]): errs.append(f"{name}:{iid} err sur la bonne réponse {w}")
            if it["type"] in ("qcm", "vf") and w not in it["options"]: errs.append(f"{name}:{iid} clé err hors options {w}")
        if it["type"] in ("qcm", "vf") and it["a"] not in it["options"]: errs.append(f"{name}:{iid} a ∉ options")
for f in glob.glob(os.path.join(HERE, "..", "*.json")):
    for it in json.load(open(f, encoding="utf-8")):
        if it.get("id") in ids: errs.append(f"id {it['id']} en collision avec {os.path.basename(f)}")
print(f"{n} items, {n_err} rattachements err, {len(ids)} ids uniques")
print("\n".join(errs) if errs else "✅ OK : comp, err et ids cohérents avec le référentiel")
sys.exit(1 if errs else 0)
