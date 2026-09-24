#!/usr/bin/env python3
"""check_banque.py — cohérence de la banque d'items 3e avec le référentiel.

Usage :
  python3 data/banque_3eme/check_banque.py                 # tous les fichiers <DOM>.<THEME>.json
  python3 data/banque_3eme/check_banque.py EG AP           # + couverture complète de ces domaines
  python3 data/banque_3eme/check_banque.py --files a.json b.json

Contrôles (bloquants) :
  - JSON = tableau d'items ; ids uniques (dans toute la banque)
  - comp existe dans data/referentiel_3eme/competences.json ; préfixe de fichier = domaine.theme
  - chaque id d'erreur de `err` existe ET appartient à la compétence de l'item
  - qcm/vf : `a` ∈ options, options sans doublon, chaque distracteur a une entrée `err`,
    chaque clé de `err` est une option (≠ a) ; vf : options = ["Vrai", "Faux"]
  - fill : `a` non vide, clés `err` ≠ a, q contient au moins un `$` (sinon fmtL() de app.html
    englobe tout l'énoncé dans $…$ à cause de ___)
  - steps 1..3, champ f présent, lvl ∈ {1,2,3}, usage ⊂ {diag, train}
  - au moins 3 items `diag` par compétence présente ; au moins 2 erreurs types distinctes
    couvertes par compétence (quand le référentiel en propose ≥ 2)
  - avec des domaines en argument : toutes les compétences de ces domaines ont ≥ 3 items diag
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "referentiel_3eme", "competences.json")


def main(argv):
    files, domaines = [], []
    if "--files" in argv:
        files = argv[argv.index("--files") + 1:]
    else:
        domaines = argv
        files = sorted(f for f in glob.glob(os.path.join(HERE, "*.json"))
                       if re.match(r"^[A-Z]{2}\.[A-Z]{3,5}\.json$", os.path.basename(f)))

    ref = {c["id"]: c for c in json.load(open(REF, encoding="utf-8"))}
    errs, warns = [], []
    ids = set()
    per_comp = defaultdict(list)

    for path in files:
        name = os.path.basename(path)
        try:
            items = json.load(open(path, encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            errs.append(f"{name}: JSON invalide ({e})")
            continue
        if not isinstance(items, list):
            errs.append(f"{name}: attendu un tableau d'items")
            continue
        prefix = name[:-5]
        for it in items:
            iid = it.get("id", "?")
            p = f"{name}:{iid}"
            if iid in ids:
                errs.append(f"{p}: id en double")
            ids.add(iid)
            comp = it.get("comp")
            if comp not in ref:
                errs.append(f"{p}: comp inconnue {comp!r}")
                continue
            if not comp.startswith(prefix + "."):
                errs.append(f"{p}: comp {comp} rangée dans {name}")
            if not str(iid).startswith(comp + "-"):
                warns.append(f"{p}: id ne commence pas par {comp}-")
            per_comp[comp].append(it)

            err_ids = {e["id"] for e in ref[comp].get("erreurs", [])}
            err = it.get("err") or {}
            for k, v in err.items():
                if v not in err_ids:
                    errs.append(f"{p}: erreur {v!r} absente de {comp} (clé {k!r})")

            typ = it.get("type", "qcm")
            a = it.get("a")
            opts = it.get("options") or []
            if a in (None, ""):
                errs.append(f"{p}: a vide")
            if typ in ("qcm", "vf"):
                if a not in opts:
                    errs.append(f"{p}: a={a!r} absent des options")
                if len(opts) != len(set(opts)):
                    errs.append(f"{p}: options en double")
                if typ == "vf" and opts != ["Vrai", "Faux"]:
                    errs.append(f"{p}: vf doit avoir options ['Vrai', 'Faux']")
                if typ == "qcm" and len(opts) < 3:
                    errs.append(f"{p}: qcm < 3 options")
                for o in opts:
                    if o != a and o not in err:
                        errs.append(f"{p}: distracteur sans err : {o!r}")
                for k in err:
                    if k not in opts:
                        errs.append(f"{p}: clé err hors options : {k!r}")
                    if k == a:
                        errs.append(f"{p}: la bonne réponse est taguée erreur")
            elif typ == "fill":
                if opts:
                    warns.append(f"{p}: fill avec options non vides")
                if a in err:
                    errs.append(f"{p}: la bonne réponse est taguée erreur")
                if "$" not in it.get("q", ""):
                    errs.append(f"{p}: fill sans $ dans q (rendu fmtL cassé par ___)")
                if not err:
                    warns.append(f"{p}: fill sans err")
            else:
                errs.append(f"{p}: type inconnu {typ!r}")

            st = it.get("steps") or []
            if not 1 <= len(st) <= 3:
                errs.append(f"{p}: {len(st)} steps (attendu 1-3)")
            if "f" not in it:
                errs.append(f"{p}: champ f absent")
            if it.get("lvl") not in (1, 2, 3):
                errs.append(f"{p}: lvl invalide {it.get('lvl')!r}")
            us = it.get("usage") or []
            if not us or not set(us) <= {"diag", "train"}:
                errs.append(f"{p}: usage invalide {us!r}")

    for comp, its in sorted(per_comp.items()):
        nd = sum("diag" in (i.get("usage") or []) for i in its)
        if nd < 3:
            errs.append(f"{comp}: {nd} item(s) diag (attendu ≥ 3)")
        covered = {v for i in its for v in (i.get("err") or {}).values()}
        if len(ref[comp].get("erreurs", [])) >= 2 and len(covered) < 2:
            errs.append(f"{comp}: {len(covered)} erreur type couverte (attendu ≥ 2)")
        if sum(i.get("type") == "vf" for i in its if "diag" in (i.get("usage") or [])) > 1:
            warns.append(f"{comp}: plus d'un vf en diag")

    for d in domaines:
        for cid, c in ref.items():
            if c["domaine"] == d and cid not in per_comp:
                errs.append(f"{cid}: aucune question dans la banque")

    n = sum(len(v) for v in per_comp.values())
    types = defaultdict(int)
    for its in per_comp.values():
        for i in its:
            types[i.get("type")] += 1
    print(f"{len(files)} fichier(s), {n} items, {len(per_comp)} compétences — types : {dict(types)}")
    for w in warns:
        print("  ⚠️ ", w)
    for e in errs:
        print("  ❌", e)
    print("✅ OK" if not errs else f"🔴 {len(errs)} erreur(s)")
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
