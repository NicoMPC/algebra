#!/usr/bin/env python3
"""
import_referentiel_banque.py — Charge le référentiel de compétences et la banque d'items 3e dans Supabase
(tables `competences` et `items`, migration 20260924_diagnostic_3e.sql).

Sources (par défaut) :
  - data/referentiel_3eme/competences.json
  - data/banque_3eme/<DOM>.<THEME>.json      (items diag + train)
  - data/banque_3eme/_legacy/**/*.json (dont bank_6eme/5eme/4eme)         (sous-questions v4 taggées, source/parapluie_id/num)

Usage :
  python3 supabase/import_referentiel_banque.py --dry-run            # valide tout, n'écrit rien (aucun credential requis)
  python3 supabase/import_referentiel_banque.py                      # upsert en base (SUPABASE_SERVICE_ROLE_KEY requis)
  python3 supabase/import_referentiel_banque.py --desactiver-absents # + passe actif=false aux items absents des fichiers

Contrôles bloquants : ids, domaines, niveaux, poids, prérequis existants, graphe acyclique, items rattachés à une
compétence connue, ids d'items uniques, type/lvl/usage valides, réponse QCM parmi les options.
Avertissements : distracteur QCM sans `err`, id d'erreur absent du référentiel.
"""
import argparse, glob, json, os, re, sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)

DOMAINES = {"NC", "DF", "GM", "EG", "AP"}
NIVEAUX = {"6EME", "5EME", "4EME", "3EME"}
HORS_DIAG = {"NC.RAC.03", "NC.RAC.04", "EG.REP.02"}  # contrat §8 — aligné sur MX_HORS_DIAG (index.ts)
RE_COMP = re.compile(r"^(NC|DF|GM|EG|AP)\.[A-Z]{3,5}\.\d{2}$")


def charger_json(chemin):
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def valider_referentiel(comps, erreurs):
    ids = {}
    for c in comps:
        cid = c.get("id", "")
        if not RE_COMP.match(cid):
            erreurs.append(f"compétence id invalide : {cid!r}")
        if cid in ids:
            erreurs.append(f"compétence en double : {cid}")
        ids[cid] = c
        if c.get("domaine") not in DOMAINES:
            erreurs.append(f"{cid} : domaine invalide {c.get('domaine')!r}")
        if c.get("niveau_origine") not in NIVEAUX:
            erreurs.append(f"{cid} : niveau_origine invalide {c.get('niveau_origine')!r}")
        if c.get("poids_brevet") not in (1, 2, 3):
            erreurs.append(f"{cid} : poids_brevet invalide {c.get('poids_brevet')!r}")
    for c in comps:
        for p in c.get("prerequis", []):
            if p not in ids:
                erreurs.append(f"{c['id']} : prérequis inconnu {p}")
    # acyclicité (DFS 3 couleurs)
    etat = {}
    def dfs(n, chemin):
        etat[n] = 1
        for p in ids.get(n, {}).get("prerequis", []):
            if p not in ids:
                continue
            if etat.get(p) == 1:
                erreurs.append("cycle : " + " → ".join(chemin + [p]))
            elif not etat.get(p):
                dfs(p, chemin + [p])
        etat[n] = 2
    for n in ids:
        if not etat.get(n):
            dfs(n, [n])
    return ids


def charger_items(dossier):
    re_banque = re.compile(r"^(NC|DF|GM|EG|AP)\.[A-Z]{2,5}\.json$")  # exclut *.review.json (verdicts relecteur)
    fichiers = sorted(f for f in glob.glob(os.path.join(dossier, "*.json")) if re_banque.match(os.path.basename(f)))
    fichiers += sorted(f for f in glob.glob(os.path.join(dossier, "_legacy", "**", "*.json"), recursive=True) if ".review" not in f)
    items = []
    for f in fichiers:
        data = charger_json(f)
        if not isinstance(data, list):
            continue  # fichiers annexes éventuels
        for it in data:
            it["_fichier"] = os.path.relpath(f, RACINE)
            items.append(it)
    return fichiers, items


def valider_items(items, comps, erreurs, avert):
    vus = set()
    errs_ref = {e["id"] for c in comps.values() for e in c.get("erreurs", [])}
    for it in items:
        iid = it.get("id", "")
        where = f"{iid} ({it.get('_fichier')})"
        if not iid:
            erreurs.append(f"item sans id dans {it.get('_fichier')}")
            continue
        if iid in vus:
            erreurs.append(f"item en double : {where}")
        vus.add(iid)
        if it.get("comp") not in comps:
            erreurs.append(f"{where} : compétence inconnue {it.get('comp')!r}")
        t = it.get("type") or ("qcm" if it.get("options") else "fill")
        if t not in ("qcm", "vf", "fill"):
            erreurs.append(f"{where} : type invalide {t!r}")
        if it.get("lvl", 1) not in (1, 2, 3):
            erreurs.append(f"{where} : lvl invalide")
        if not set(it.get("usage", ["diag", "train"])) <= {"diag", "train"}:
            erreurs.append(f"{where} : usage invalide {it.get('usage')}")
        if not str(it.get("q", "")).strip() or str(it.get("a", "")).strip() == "":
            erreurs.append(f"{where} : q ou a vide")
        if t == "qcm":
            opts = it.get("options") or []
            if it.get("a") not in opts:
                erreurs.append(f"{where} : réponse absente des options")
            for o in opts:
                if o != it.get("a") and o not in (it.get("err") or {}):
                    avert.append(f"{where} : distracteur sans err {o!r}")
        for v in (it.get("err") or {}).values():
            if v not in errs_ref:
                avert.append(f"{where} : erreur type inconnue du référentiel {v}")


def lignes_competences(comps):
    return [{
        "id": c["id"], "domaine": c["domaine"], "theme": c.get("theme", c["id"].split(".")[1]),
        "titre": c["titre"], "titre_eleve": c.get("titre_eleve"), "niveau_origine": c["niveau_origine"],
        "prerequis": c.get("prerequis", []), "poids_brevet": c["poids_brevet"],
        "chapitres_legacy": c.get("chapitres_legacy", []), "erreurs": c.get("erreurs", []),
        "diag_autorise": not (c["id"] in HORS_DIAG or c.get("hors_programme") or c.get("diag") is False
                              or c.get("diag_autorise") is False),
        "actif": True,
    } for c in comps.values()]


def lignes_items(items):
    out = []
    for it in items:
        j = {k: v for k, v in it.items() if k != "_fichier"}
        t = j.get("type") or ("qcm" if j.get("options") else "fill")
        out.append({
            "id": j["id"], "comp": j["comp"], "type": t, "lvl": j.get("lvl", 1),
            "usage": j.get("usage", ["diag", "train"]), "item_json": j,
            "source": j.get("source"), "parapluie_id": j.get("parapluie_id"), "num": j.get("num"),
            "depend_question_precedente": bool(j.get("depend_question_precedente")), "actif": True,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--referentiel", default=os.path.join(RACINE, "data/referentiel_3eme/competences.json"))
    ap.add_argument("--banque", default=os.path.join(RACINE, "data/banque_3eme"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--desactiver-absents", action="store_true")
    args = ap.parse_args()

    erreurs, avert = [], []
    comps = valider_referentiel(charger_json(args.referentiel), erreurs)
    fichiers, items = charger_items(args.banque)
    valider_items(items, comps, erreurs, avert)

    par_comp = {}
    for it in items:
        par_comp.setdefault(it.get("comp"), []).append(it)
    sans_diag = [c for c in comps if c not in HORS_DIAG and not any("diag" in i.get("usage", []) for i in par_comp.get(c, []))]
    print(f"Référentiel : {len(comps)} compétences · Banque : {len(items)} items dans {len(fichiers)} fichiers")
    print(f"Compétences sans item : {sum(1 for c in comps if c not in par_comp)} · sans item diag : {len(sans_diag)}")
    for a in avert[:20]:
        print("  ⚠", a)
    if len(avert) > 20:
        print(f"  ⚠ … {len(avert) - 20} autres avertissements")
    if erreurs:
        for e in erreurs[:50]:
            print("  ✗", e)
        print(f"{len(erreurs)} erreur(s) bloquante(s) — import annulé.")
        sys.exit(1)
    if args.dry_run:
        print("Dry-run OK — rien n'a été écrit.")
        return

    from supabase_helper import sb  # import tardif : pas de credentials nécessaires en dry-run
    lc = lignes_competences(comps)
    for i in range(0, len(lc), 200):
        sb.insert("competences", lc[i:i + 200], upsert=True)
    li = lignes_items(items)
    for i in range(0, len(li), 200):
        sb.insert("items", li[i:i + 200], upsert=True)
    print(f"Upsert : {len(lc)} compétences, {len(li)} items.")
    if args.desactiver_absents:
        presents = {x["id"] for x in li}
        en_base = sb.read("items", select="id", filters={"actif": "eq.true"})
        absents = [r["id"] for r in en_base if r["id"] not in presents]
        for iid in absents:
            sb.update("items", {"id": f"eq.{iid}"}, {"actif": False})
        print(f"Désactivés (absents des fichiers) : {len(absents)}")
    print("Rappel : le cache du référentiel dans l'Edge Function dure 5 min.")


if __name__ == "__main__":
    main()
