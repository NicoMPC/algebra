#!/usr/bin/env python3
"""
Test du prompt de génération d'exercices — Matheux
Appelle l'API Claude 5 fois avec des profils variés et valide le format retourné.
Résultats sauvegardés dans docs/test_prompts.json

Usage :
  pip install anthropic
  ANTHROPIC_API_KEY=sk-... python3 docs/test_prompts.py
"""

import os
import json
import re
import sys
import anthropic

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "test_prompts.json")

# ── Reproduction du buildExoPrompt JS ──────────────────────────
def build_prompt(prenom, niveau, chapitre, type_, hard_questions, score, statut):
    n = 5 if type_ == "boost" else 20

    if score < 20:
        profile = (f"PROFIL TRÈS FAIBLE (score {score}/100). Partir des bases absolues. "
                   "Chaque question doit être décomposable étape par étape. "
                   "Utiliser des contextes très concrets et familiers. Ne jamais supposer qu'une notion est connue.")
    elif score < 40:
        profile = (f"PROFIL FRAGILE (score {score}/100). Les fondamentaux sont instables. "
                   "Chaque step doit expliquer le POURQUOI avant le COMMENT. "
                   "Varier légèrement les présentations.")
    elif score < 60:
        profile = (f"PROFIL EN PROGRESSION (score {score}/100). Les bases existent mais les transferts sont difficiles. "
                   "Partir d'un exemple concret puis généraliser.")
    elif score < 80:
        profile = (f"PROFIL CORRECT (score {score}/100). Consolider les acquis et introduire des variantes.")
    else:
        profile = (f"PROFIL FORT (score {score}/100). Proposer des exercices challengeants avec légère complexité lvl2.")

    if hard_questions:
        errors_section = (
            "ERREURS RÉCENTES DE L'ÉLÈVE (questions où il/elle a échoué — à cibler en priorité) :\n"
            + "\n".join(f"{i+1}. {q}" for i, q in enumerate(hard_questions[:6]))
            + f"\n→ Construire au moins {min(len(hard_questions), 3)} exercice(s) testant exactement ces lacunes."
        )
    else:
        errors_section = "Aucune erreur spécifique récente — générer une progression équilibrée couvrant les points essentiels du chapitre."

    if type_ == "boost":
        lvl_instructions = (
            "RÉPARTITION NIVEAUX pour ce boost de 5 exos :\n"
            "- 2 exos lvl:1 (accessible, fondamental, guidé)\n"
            "- 3 exos lvl:2 (application, légèrement plus complexe)\n"
            "→ Si l'élève est très faible (score < 30), inverser : 3 lvl:1 + 2 lvl:2"
        )
    else:
        lvl_instructions = (
            "RÉPARTITION NIVEAUX pour ce chapitre de 20 exos :\n"
            "- Exos 1–10 : lvl:1 — fondamentaux, contextes concrets, très bien guidé\n"
            "- Exos 11–20 : lvl:2 — application, autonomie, légèrement plus complexe\n"
            "→ Progression croissante de difficulté au sein de chaque groupe"
        )

    example = json.dumps({
        "lvl": 1,
        "q": "Une pizza coûte $12{,}50$ €. Sarah a $8$ €. Combien lui manque-t-il ?",
        "a": "4,50 €",
        "options": ["4,50 €", "3,50 €", "20,50 €"],
        "steps": [
            "Indice 1 : Cherche ce qui manque = ce qu'il faut ajouter à ce qu'on a pour atteindre le prix.",
            "Indice 2 : Pose la soustraction : $12{,}50 - 8 = ?$",
            "Indice 3 : $12{,}50 - 8 = 4{,}50$ €. Vérifie : $8 + 4{,}50 = 12{,}50$ ✓"
        ],
        "f": "Manquant = Prix total $-$ Argent disponible"
    }, ensure_ascii=False, indent=2)

    return "\n".join([
        "Tu es un professeur de maths expérimenté créant des exercices pédagogiques pour collégiens français (niveaux 6ème–3ème).",
        "",
        "══════ CONTEXTE ÉLÈVE ══════",
        f"Prénom : {prenom} | Niveau : {niveau} | Chapitre : {chapitre}",
        f"Score de confiance : {score}/100 | Statut : {statut}",
        "",
        profile,
        "",
        "══════ ERREURS À CIBLER ══════",
        errors_section,
        "",
        "══════ OBJECTIF ══════",
        f"Générer EXACTEMENT {n} exercices pour le chapitre \"{chapitre}\".",
        lvl_instructions,
        "",
        "══════ RÈGLES IMPÉRATIVES ══════",
        "1. STEPS — 3 étapes obligatoires, progression vague→méthode→quasi-solution :",
        "   • Step 1 : indice vague sur la stratégie (\"De quoi as-tu besoin ?\", \"Quelle opération…\")",
        "   • Step 2 : méthode concrète avec formule ou calcul intermédiaire",
        "   • Step 3 : quasi-solution (calcul final ou vérification guidée)",
        "2. OPTIONS — 3 valeurs exactes dont la bonne réponse + 2 distracteurs ciblant des erreurs fréquentes :",
        "   • \"a\" doit apparaître mot pour mot dans \"options\"",
        "3. FORMULE — \"f\" = règle clé en 1 ligne max, en LaTeX si math",
        "4. LATEX — utiliser $ $ pour tout symbole maths : $\\frac{3}{4}$, $\\times$, $\\div$, $\\sqrt{25}$, $x^2$",
        "5. CONTEXTES — exos lvl:1 dans des contextes concrets du quotidien",
        "6. LVL — doit être exactement 1 (fondamental) ou 2 (application)",
        "7. \"a\" — réponse avec unité si nécessaire (ex: \"4,50 €\", \"12 cm\")",
        "",
        "══════ EXEMPLE D'EXERCICE CONFORME ══════",
        example,
        "",
        "══════ FORMAT DE RÉPONSE ══════",
        f"Retourne UNIQUEMENT un JSON array de {n} objets, sans texte avant ni après, sans balise markdown.",
        "Chaque objet DOIT avoir exactement ces 6 champs : lvl, q, a, options, steps, f",
        "",
        "["
    ])


# ── Validation d'un exercice ───────────────────────────────────
def validate_exo(ex):
    errors = []
    if not isinstance(ex.get("q"), str) or len(ex["q"].strip()) < 5:
        errors.append("q manquant ou trop court")
    if not isinstance(ex.get("a"), str) or not ex["a"].strip():
        errors.append("a manquant")
    if not isinstance(ex.get("options"), list) or len(ex["options"]) != 3:
        errors.append(f"options doit avoir 3 éléments (a {len(ex.get('options', []))})")
    elif ex.get("a") not in ex["options"]:
        errors.append(f"'a' ({ex['a']!r}) absent de options {ex['options']}")
    if not isinstance(ex.get("steps"), list) or not (2 <= len(ex["steps"]) <= 5):
        errors.append(f"steps doit avoir 2–5 éléments (a {len(ex.get('steps', []))})")
    if not isinstance(ex.get("f"), str) or not ex["f"].strip():
        errors.append("f (formule) manquant")
    if ex.get("lvl") not in (1, 2):
        errors.append(f"lvl doit être 1 ou 2 (a {ex.get('lvl')!r})")
    return errors


# ── Cas de test ────────────────────────────────────────────────
TEST_CASES = [
    {
        "id": "boost_fragile_fractions_6eme",
        "prenom": "Lucas",
        "niveau": "6EME",
        "chapitre": "Fractions",
        "type": "boost",
        "hard_questions": [
            "Calcule $\\frac{1}{2} + \\frac{1}{3}$",
            "Simplifie $\\frac{6}{9}$"
        ],
        "score": 25,
        "statut": "FRAGILE"
    },
    {
        "id": "boost_bloquee_equations_4eme",
        "prenom": "Chloé",
        "niveau": "4EME",
        "chapitre": "Equations_1er_degre",
        "type": "boost",
        "hard_questions": [
            "Résoudre $2x + 3 = 11$",
            "Résoudre $5x - 7 = 3x + 1$"
        ],
        "score": 15,
        "statut": "BLOQUEE"
    },
    {
        "id": "boost_no_errors_pythagore_3eme",
        "prenom": "Inès",
        "niveau": "3EME",
        "chapitre": "Theoreme_Pythagore",
        "type": "boost",
        "hard_questions": [],
        "score": 55,
        "statut": "EN_COURS"
    },
    {
        "id": "chapter_weak_proportionnalite_5eme",
        "prenom": "Nathan",
        "niveau": "5EME",
        "chapitre": "Proportionnalite",
        "type": "chapter",
        "hard_questions": [
            "3 stylos coûtent 4,50€. Quel est le prix de 7 stylos ?",
            "Un train roule à 120 km/h. Quelle distance parcourt-il en 2h30 ?"
        ],
        "score": 30,
        "statut": "FRAGILE"
    },
    {
        "id": "boost_strong_calcul_litteral_4eme",
        "prenom": "Théo",
        "niveau": "4EME",
        "chapitre": "Calcul_litteral",
        "type": "boost",
        "hard_questions": [],
        "score": 78,
        "statut": "EN_COURS"
    }
]


def parse_exos_from_response(text):
    """Extrait et parse le JSON array de la réponse Claude."""
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("Pas de JSON array trouvé dans la réponse")
    return json.loads(text[start:end + 1])


def run_tests():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERREUR : ANTHROPIC_API_KEY non définie.", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    results = []

    for tc in TEST_CASES:
        print(f"\n{'='*60}")
        print(f"Test : {tc['id']}")
        print(f"  {tc['prenom']} | {tc['niveau']} | {tc['chapitre']} | score={tc['score']} | type={tc['type']}")

        prompt = build_prompt(
            prenom=tc["prenom"],
            niveau=tc["niveau"],
            chapitre=tc["chapitre"],
            type_=tc["type"],
            hard_questions=tc["hard_questions"],
            score=tc["score"],
            statut=tc["statut"]
        )

        try:
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8000,
                messages=[{"role": "user", "content": prompt}]
            )
            raw = message.content[0].text
            exos = parse_exos_from_response(raw)

            expected_count = 5 if tc["type"] == "boost" else 20
            validation_errors = []
            per_exo = []

            for i, ex in enumerate(exos):
                errs = validate_exo(ex)
                per_exo.append({"index": i + 1, "valid": len(errs) == 0, "errors": errs})
                if errs:
                    validation_errors.extend([f"Exo {i+1}: {e}" for e in errs])

            valid_count = sum(1 for e in per_exo if e["valid"])
            status = "PASS" if valid_count == len(exos) and len(exos) >= expected_count * 0.8 else "FAIL"

            print(f"  Exos reçus : {len(exos)} (attendu : {expected_count})")
            print(f"  Valides : {valid_count}/{len(exos)}")
            print(f"  Statut : {status}")
            if validation_errors:
                print("  Erreurs :")
                for e in validation_errors[:5]:
                    print(f"    - {e}")

            result = {
                "id": tc["id"],
                "status": status,
                "expected_count": expected_count,
                "received_count": len(exos),
                "valid_count": valid_count,
                "validation_errors": validation_errors,
                "per_exo": per_exo,
                "exos": exos,
                "raw_response_length": len(raw)
            }

        except Exception as exc:
            print(f"  ERREUR : {exc}")
            result = {
                "id": tc["id"],
                "status": "ERROR",
                "error": str(exc),
                "exos": []
            }

        results.append(result)

    # Résumé
    print(f"\n{'='*60}")
    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"RÉSULTAT GLOBAL : {passed}/{len(results)} tests PASS")
    for r in results:
        icon = "✓" if r["status"] == "PASS" else "✗"
        print(f"  {icon} {r['id']} — {r['status']}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nRésultats sauvegardés dans {OUTPUT_FILE}")


if __name__ == "__main__":
    run_tests()
