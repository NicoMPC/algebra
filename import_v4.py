#!/usr/bin/env python3
"""Import v4 exercice-parapluie into Matheux via GAS endpoint."""
import json, glob, os, requests

GAS_URL = "https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
ADMIN_CODE = "HMD493"

# Chapter metadata
CHAPTER_META = {
    "Arithmetique_Brevet": ("Arithmétique", "🔢"),
    "Calcul_Litteral_Brevet": ("Calcul Littéral", "📝"),
    "Equations_Brevet": ("Équations", "🎯"),
    "Fonctions_Brevet": ("Fonctions", "📈"),
    "Fonctions_Affines_Brevet": ("Fonctions Affines", "📈"),
    "Fractions_Brevet": ("Fractions", "🔢"),
    "Geometrie_Espace_Brevet": ("Géométrie dans l'Espace", "📐"),
    "Inequations_Brevet": ("Inéquations", "📊"),
    "Probabilites_Brevet": ("Probabilités", "🎲"),
    "Proportionnalite_Brevet": ("Proportionnalité", "📊"),
    "Puissances_Brevet": ("Puissances", "🔢"),
    "Pythagore_Brevet": ("Théorème de Pythagore", "📐"),
    "Racines_Carrees_Brevet": ("Racines Carrées", "√"),
    "Scratch_Brevet": ("Scratch / Algorithmique", "💻"),
    "Statistiques_Brevet": ("Statistiques", "📊"),
    "Thales_Brevet": ("Théorème de Thalès", "📐"),
    "Transformations_Brevet": ("Transformations", "📐"),
    "Trigonometrie_Brevet": ("Trigonométrie", "📐"),
    "Auto_Calcul": ("Automatismes Calcul", "⚡"),
    "Auto_Geometrie": ("Automatismes Géométrie", "⚡"),
    "Auto_Litteral": ("Automatismes Littéral", "⚡"),
    "Auto_Stats_Probas": ("Automatismes Stats & Probas", "⚡"),
}

# Step 1: Clear existing curriculum rows via GAS
print("Step 1: Calling clear_curriculum...")
r = requests.post(GAS_URL, data=json.dumps({
    "action": "clear_curriculum",
    "adminCode": ADMIN_CODE,
    "niveau": "3EME"
}), allow_redirects=True)
print(f"  Response: {r.status_code} {r.text[:200]}")

# Step 2: Build chapters payload from v4 JSON files
chapters = []
for fname in sorted(glob.glob("data/*_v4.json")):
    cat = os.path.basename(fname).replace("_v4.json", "")
    if cat not in CHAPTER_META:
        print(f"  SKIP {cat} (not in meta)")
        continue
    titre, icone = CHAPTER_META[cat]
    exos = json.load(open(fname))
    chapters.append({
        "niveau": "3EME",
        "categorie": cat,
        "titre": titre,
        "icone": icone,
        "exos": exos
    })
    print(f"  Loaded {cat}: {len(exos)} exercises")

print(f"\nStep 2: Importing {len(chapters)} chapters...")

# Step 3: Import via GAS (importChapters action)
payload = {
    "action": "import_chapters",
    "adminCode": ADMIN_CODE,
    "chapters": chapters
}

r = requests.post(GAS_URL, data=json.dumps(payload), allow_redirects=True)
print(f"  Response: {r.status_code}")
try:
    result = r.json()
    print(f"  Status: {result.get('status')}")
    for msg in result.get('results', []):
        print(f"    {msg}")
except:
    print(f"  Raw: {r.text[:500]}")

print("\nDone!")
