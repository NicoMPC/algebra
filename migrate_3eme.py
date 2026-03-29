"""
migrate_3eme.py — Migration Brevet 2026
Injecte les 22 chapitres + diagnostic 3EME dans Curriculum_Officiel et DiagnosticExos.

Stratégie :
  - Curriculum_Officiel : REMPLACE les lignes 3EME existantes, garde les autres niveaux intacts
  - DiagnosticExos : REMPLACE les lignes 3EME existantes, garde les autres niveaux intacts
  - Ajoute les colonnes Timer et Ordered (nouvelles cols F et G)

Usage :
  python3 migrate_3eme.py          # dry-run (affiche ce qui serait fait)
  python3 migrate_3eme.py --apply  # applique les changements dans la sheet PROD

Pré-requis : pip install google-auth google-api-python-client
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

# ── Fichiers chapitres (21) ──────────────────────────────────────────────────
CHAPTER_FILES = [
    # Nombres & Calculs
    "Fractions_Brevet.json",
    "Puissances_Brevet.json",
    "Racines_Carrees_Brevet.json",
    "Arithmetique_Brevet.json",
    "Calcul_Litteral_Brevet.json",
    "Equations_Brevet.json",
    "Inequations_Brevet.json",
    # Fonctions & Proportionnalité
    "Fonctions_Brevet.json",
    "Fonctions_Affines_Brevet.json",
    "Proportionnalite_Brevet.json",
    # Géométrie
    "Pythagore_Brevet.json",
    "Thales_Brevet.json",
    "Trigonometrie_Brevet.json",
    "Geometrie_Espace_Brevet.json",
    "Transformations_Brevet.json",
    # Stats & Probas
    "Statistiques_Brevet.json",
    "Probabilites_Brevet.json",
    # Algorithmique
    "Scratch_Brevet.json",
    # Automatismes
    "Auto_Calcul.json",
    "Auto_Litteral.json",
    "Auto_Geometrie.json",
    "Auto_Stats_Probas.json",
]

DIAGNOSTIC_FILE = "diagnostic_3eme.json"

CURRICULUM_HEADERS = ["Niveau", "Categorie", "Titre", "Icone", "ExosJSON", "Timer", "Ordered"]
DIAGNOSTIC_HEADERS = ["Niveau", "Categorie", "ExosJSON"]


def load_chapters():
    """Charge les 22 fichiers chapitres et retourne les lignes Curriculum_Officiel."""
    rows = []
    for fname in CHAPTER_FILES:
        path = os.path.join(DATA_DIR, fname)
        if not os.path.exists(path):
            print(f"  MANQUANT : {fname}")
            continue
        with open(path, "r", encoding="utf-8") as f:
            ch = json.load(f)

        niveau = ch["niveau"]
        categorie = ch["categorie"]
        titre = ch["titre"]
        icone = ch["icone"]
        exos_json = json.dumps(ch["exos"], ensure_ascii=False)
        timer = ch.get("timer", "")
        ordered = ch.get("ordered", "")

        rows.append([niveau, categorie, titre, icone, exos_json, timer, ordered])
    return rows


def load_diagnostic():
    """Charge le diagnostic 3EME et retourne les lignes DiagnosticExos."""
    path = os.path.join(DATA_DIR, DIAGNOSTIC_FILE)
    with open(path, "r", encoding="utf-8") as f:
        items = json.load(f)

    rows = []
    for item in items:
        niveau = item["niveau"]
        categorie = item["categorie"]
        exos_json = json.dumps(item["exos"], ensure_ascii=False)
        rows.append([niveau, categorie, exos_json])
    return rows


def migrate(apply=False):
    print("=" * 60)
    print("MIGRATION BREVET 2026 — Refonte 3EME")
    print("=" * 60)
    print()

    # ── 1. Charger les nouvelles données ──────────────────────────────────────
    new_curriculum = load_chapters()
    new_diagnostic = load_diagnostic()

    print(f"Chapitres chargés : {len(new_curriculum)} ({sum(len(json.loads(r[4])) for r in new_curriculum)} exos)")
    print(f"Diagnostic chargé : {len(new_diagnostic)} chapitres ({sum(len(json.loads(r[2])) for r in new_diagnostic)} exos)")
    print()

    if not apply:
        print("DRY-RUN — aperçu des changements :")
        print()
        print("Curriculum_Officiel — lignes 3EME à injecter :")
        for r in new_curriculum:
            timer_info = f" [timer={r[5]}]" if r[5] else ""
            ordered_info = " [ordered]" if r[6] else ""
            n_exos = len(json.loads(r[4]))
            print(f"  {r[0]} | {r[1]:30s} | {r[2]:25s} | {r[3]} | {n_exos} exos{timer_info}{ordered_info}")

        print()
        print("DiagnosticExos — lignes 3EME à injecter :")
        for r in new_diagnostic:
            n_exos = len(json.loads(r[2]))
            print(f"  {r[0]} | {r[1]:30s} | {n_exos} exos")

        print()
        print("Pour appliquer : python3 migrate_3eme.py --apply")
        return

    # ── 2. Connexion à la sheet ───────────────────────────────────────────────
    sys.path.insert(0, SCRIPT_DIR)
    from sheets import sh

    # ── 3. Curriculum_Officiel ─────────────────────────────────────────────────
    print("Lecture Curriculum_Officiel...")
    existing = sh.read_raw("Curriculum_Officiel")
    old_headers = existing[0] if existing else []
    old_rows = existing[1:] if len(existing) > 1 else []

    # Garder les lignes NON-3EME
    kept = [r for r in old_rows if len(r) > 0 and r[0] != "3EME"]
    removed_3eme = len(old_rows) - len(kept)
    print(f"  Lignes existantes : {len(old_rows)} (dont {removed_3eme} × 3EME à remplacer)")
    print(f"  Lignes autres niveaux conservées : {len(kept)}")
    print(f"  Nouvelles lignes 3EME : {len(new_curriculum)}")

    # Compléter les lignes kept à 7 colonnes si nécessaire (anciennes lignes sans Timer/Ordered)
    for i, r in enumerate(kept):
        while len(r) < len(CURRICULUM_HEADERS):
            kept[i].append("")

    # Assembler
    final_curriculum = [CURRICULUM_HEADERS] + kept + new_curriculum
    print(f"  Total final : {len(final_curriculum) - 1} lignes")

    sh.write_rows("Curriculum_Officiel", final_curriculum)
    print()

    # ── 4. DiagnosticExos ─────────────────────────────────────────────────────
    print("Lecture DiagnosticExos...")
    existing_diag = sh.read_raw("DiagnosticExos")
    old_diag_rows = existing_diag[1:] if len(existing_diag) > 1 else []

    kept_diag = [r for r in old_diag_rows if len(r) > 0 and r[0] != "3EME"]
    removed_diag = len(old_diag_rows) - len(kept_diag)
    print(f"  Lignes existantes : {len(old_diag_rows)} (dont {removed_diag} × 3EME à remplacer)")
    print(f"  Nouvelles lignes 3EME : {len(new_diagnostic)}")

    final_diagnostic = [DIAGNOSTIC_HEADERS] + kept_diag + new_diagnostic
    print(f"  Total final : {len(final_diagnostic) - 1} lignes")

    sh.write_rows("DiagnosticExos", final_diagnostic)
    print()

    # ── 5. Résumé ─────────────────────────────────────────────────────────────
    total_exos = sum(len(json.loads(r[4])) for r in new_curriculum) + sum(len(json.loads(r[2])) for r in new_diagnostic)
    print("=" * 60)
    print(f"MIGRATION TERMINÉE — {total_exos} exercices injectés")
    print(f"  Curriculum_Officiel : {len(new_curriculum)} chapitres ({removed_3eme} anciens → {len(new_curriculum)} nouveaux)")
    print(f"  DiagnosticExos : {len(new_diagnostic)} chapitres ({removed_diag} anciens → {len(new_diagnostic)} nouveaux)")
    print("=" * 60)


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    migrate(apply=apply)
