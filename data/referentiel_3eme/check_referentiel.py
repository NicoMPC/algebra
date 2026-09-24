#!/usr/bin/env python3
"""Vérifie le référentiel de compétences 3e (contrat docs/specs/00-contrat-commun.md §2).

Usage : python3 data/referentiel_3eme/check_referentiel.py [chemin/competences.json]

Erreurs bloquantes (code retour 1) :
  - JSON invalide / pas une liste / champ obligatoire manquant ou mal typé
  - ID mal formé (<DOMAINE>.<THEME>.<nn>), domaine inconnu, theme/domaine incohérents avec l'ID
  - ID dupliqué, ID d'erreur mal formé ou dupliqué
  - prérequis inexistant, auto-référence, graphe non acyclique
  - compétence 3EME sans erreur type ; erreur type sans libelle / libelle_parent / remediation
  - compétence orpheline (aucun prérequis ET prérequis de personne)
  - compétence hors périmètre : niveau ≠ 3EME, poids_brevet = 1 et prérequis d'aucune autre
    compétence (ni évaluée au Brevet, ni utile pour remonter aux causes)
  - poids_brevet hors {1,2,3}, niveau_origine hors {6EME,5EME,4EME,3EME}
  - chapitre legacy inexistant (data/<chap>_v4.json)
Avertissements (non bloquants) :
  - prérequis d'un niveau postérieur à la compétence
  - compétence avec moins de 2 ou plus de 4 erreurs types
"""
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.dirname(HERE)
DOMAINES = {"NC", "DF", "GM", "EG", "AP"}
NIVEAUX = ["6EME", "5EME", "4EME", "3EME"]
ID_RE = re.compile(r"^(NC|DF|GM|EG|AP)\.([A-Z]{3,5})\.(\d{2})$")
ERR_RE = re.compile(r"^(?P<comp>[A-Z]{2}\.[A-Z]{3,5}\.\d{2})#[a-z0-9_]+$")
CHAMPS = {"id": str, "domaine": str, "theme": str, "titre": str, "titre_eleve": str,
          "niveau_origine": str, "prerequis": list, "poids_brevet": int,
          "chapitres_legacy": list, "erreurs": list}


def main(path):
    errors, warns = [], []
    try:
        with open(path, encoding="utf-8") as f:
            ref = json.load(f)
    except Exception as e:  # noqa: BLE001
        print(f"❌ JSON invalide : {e}")
        return 1
    if not isinstance(ref, list) or not ref:
        print("❌ Le référentiel doit être une liste non vide")
        return 1

    ids = [c.get("id") for c in ref]
    dup = [i for i, n in Counter(ids).items() if n > 1]
    if dup:
        errors.append(f"IDs dupliqués : {dup}")
    by_id = {c.get("id"): c for c in ref}
    err_ids = []

    for c in ref:
        cid = c.get("id", "?")
        for k, t in CHAMPS.items():
            if k not in c:
                errors.append(f"{cid} : champ manquant '{k}'")
            elif not isinstance(c[k], t) or (t is int and isinstance(c[k], bool)):
                errors.append(f"{cid} : champ '{k}' doit être {t.__name__}")
        m = ID_RE.match(cid)
        if not m:
            errors.append(f"ID mal formé : {cid}")
            continue
        if c.get("domaine") != m.group(1) or c.get("theme") != m.group(2):
            errors.append(f"{cid} : domaine/theme incohérents avec l'ID")
        if c.get("niveau_origine") not in NIVEAUX:
            errors.append(f"{cid} : niveau_origine invalide {c.get('niveau_origine')}")
        if c.get("poids_brevet") not in (1, 2, 3):
            errors.append(f"{cid} : poids_brevet invalide {c.get('poids_brevet')}")
        for t in ("titre", "titre_eleve"):
            if not str(c.get(t, "")).strip():
                errors.append(f"{cid} : {t} vide")
        for p in c.get("prerequis", []):
            if p == cid:
                errors.append(f"{cid} : se référence lui-même")
            elif p not in by_id:
                errors.append(f"{cid} : prérequis introuvable {p}")
            elif NIVEAUX.index(by_id[p]["niveau_origine"]) > NIVEAUX.index(c["niveau_origine"]):
                warns.append(f"{cid} ({c['niveau_origine']}) dépend de {p} ({by_id[p]['niveau_origine']})")
        if len(set(c.get("prerequis", []))) != len(c.get("prerequis", [])):
            errors.append(f"{cid} : prérequis en double")
        for ch in c.get("chapitres_legacy", []):
            if not os.path.exists(os.path.join(DATA, f"{ch}_v4.json")):
                errors.append(f"{cid} : chapitre legacy inconnu {ch}")
        errs = c.get("erreurs", [])
        if c.get("niveau_origine") == "3EME" and not errs:
            errors.append(f"{cid} : compétence 3EME sans erreur type")
        if errs and not (2 <= len(errs) <= 4):
            warns.append(f"{cid} : {len(errs)} erreur(s) type (cible 2-4)")
        for e in errs:
            eid = e.get("id", "")
            em = ERR_RE.match(eid)
            if not em or em.group("comp") != cid:
                errors.append(f"{cid} : ID d'erreur mal formé {eid!r}")
            err_ids.append(eid)
            for k in ("libelle", "libelle_parent", "remediation"):
                if not str(e.get(k, "")).strip():
                    errors.append(f"{eid} : champ '{k}' vide ou manquant")
    dup_e = [i for i, n in Counter(err_ids).items() if n > 1]
    if dup_e:
        errors.append(f"IDs d'erreur dupliqués : {dup_e}")

    # Graphe : acyclicité (DFS itératif avec couleurs)
    graph = {c["id"]: [p for p in c.get("prerequis", []) if p in by_id] for c in ref if "id" in c}
    color = dict.fromkeys(graph, 0)
    for root in graph:
        if color[root]:
            continue
        stack = [(root, iter(graph[root]))]
        color[root] = 1
        trail = [root]
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                color[node] = 2
                stack.pop()
                trail.pop()
            elif color[nxt] == 1:
                cyc = trail[trail.index(nxt):] + [nxt]
                errors.append("Cycle : " + " → ".join(cyc))
                color[nxt] = 2
            elif color[nxt] == 0:
                color[nxt] = 1
                stack.append((nxt, iter(graph[nxt])))
                trail.append(nxt)

    # Orphelins et ancrage des prérequis
    dependants = {i: [] for i in graph}
    for cid, ps in graph.items():
        for p in ps:
            dependants[p].append(cid)
    for cid in graph:
        if not graph[cid] and not dependants[cid]:
            errors.append(f"{cid} : orphelin (aucun prérequis, prérequis de personne)")

    for cid in graph:
        c = by_id[cid]
        if c["niveau_origine"] != "3EME" and c["poids_brevet"] == 1 and not dependants[cid]:
            errors.append(f"{cid} : hors périmètre ({c['niveau_origine']}, poids 1, prérequis de personne)")

    # Profondeur maximale (information)
    memo = {}

    def depth(cid):
        if cid not in memo:
            memo[cid] = 0
            memo[cid] = 1 + max((depth(p) for p in graph[cid]), default=0)
        return memo[cid]

    if not any(e.startswith("Cycle") for e in errors):
        deepest = max(graph, key=depth)
    # Rapport
    dom = Counter(c["domaine"] for c in ref)
    niv = Counter(c["niveau_origine"] for c in ref)
    n_err = sum(len(c.get("erreurs", [])) for c in ref)
    n_arcs = sum(len(v) for v in graph.values())
    print(f"Référentiel : {path}")
    print(f"  {len(ref)} compétences · {n_err} erreurs types · {n_arcs} arcs de prérequis")
    print("  par domaine : " + ", ".join(f"{d}={dom[d]}" for d in ["NC", "DF", "GM", "EG", "AP"]))
    print("  par niveau  : " + ", ".join(f"{n}={niv[n]}" for n in NIVEAUX))
    print("  poids       : " + ", ".join(f"{p}={Counter(c['poids_brevet'] for c in ref)[p]}" for p in (3, 2, 1)))
    if not any(e.startswith("Cycle") for e in errors):
        print(f"  chaîne de prérequis la plus longue : {depth(deepest)} niveaux (depuis {deepest})")
    for w in warns:
        print(f"  ⚠️  {w}")
    if errors:
        for e in errors:
            print(f"  ❌ {e}")
        print(f"❌ {len(errors)} erreur(s)")
        return 1
    print("✅ Référentiel valide (IDs, prérequis résolus, graphe acyclique, erreurs types, aucun orphelin)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "competences.json")))
