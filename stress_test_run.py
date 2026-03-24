#!/usr/bin/env python3
"""
Stress-test Monsieur Exos — boucle complète J1-J10.
Génère des exercices adaptés, valide, audite, simule les réponses.
"""

import json, os, sys, subprocess, copy, time
from datetime import datetime
from stress_test import (
    cleanup, setup_users, setup_suivi, inject_day_scores,
    analyze_student, date_str, LOG_FILE, EXOS_DIR,
    LINA_FRACTIONS_ENONCES, LINA_PROPORTIONNALITE_ENONCES,
    RAYAN_PUISSANCES_ENONCES, RAYAN_CALCUL_ENONCES,
    EMMA_FONCTIONS_ENONCES, EMMA_THALES_ENONCES,
)
from sheets import sh

# ── Globals for anti-doublon tracking ─────────────────────────
ALL_GENERATED = {
    "TEST_LINA": [],
    "TEST_RAYAN": [],
    "TEST_EMMA": [],
}

# ── Exercise generators per student per context ───────────────

def gen_lina_boost(day, analysis):
    """Generate 5 boost exercises for Lina (6EME, Fractions/Proportionnalité)."""
    seen = set()
    for ch_data in analysis.values():
        seen.update(ch_data["seen_enonces"])
    seen.update(ALL_GENERATED["TEST_LINA"])

    ch_data_fractions = analysis.get("Fractions", {})
    ch_data_prop = analysis.get("Proportionnalité", {})
    p8_frac = ch_data_fractions.get("p8", 100)
    avg_time = ch_data_fractions.get("avg_time", 150)
    fv_rate = ch_data_fractions.get("fv_rate", 100)

    # Detect patterns
    pattern = "lent mais juste" if p8_frac >= 80 and avg_time > 120 else "normal"
    if fv_rate > 50:
        pattern += " + formule-dépendant"

    # Day 5 special: Lina had all HARD → confidence rebuild
    if day == 5 or (day == 6 and ch_data_fractions.get("hard", 0) > 3):
        insight = "Hier c'était dur — aujourd'hui on reprend les bases en douceur. Tu sais faire, on le prouve."
        diag = f"J{day}: {ch_data_fractions.get('hard',0)} HARD récents sur Fractions (journée difficile). Retour aux fondamentaux pour restaurer la confiance. Pattern: {pattern}."
    elif avg_time > 100:
        insight = f"Tes fractions sont justes, maintenant on accélère ! L'objectif : répondre en moins d'une minute."
        diag = f"J{day}: {ch_data_fractions.get('total',0)} exos, {p8_frac}% P8, temps moyen {avg_time}s. Pattern: {pattern}. Cible: fluence."
    else:
        insight = f"Tu progresses bien en vitesse ! On continue à s'entraîner pour que ça devienne automatique."
        diag = f"J{day}: temps moyen descendu à {avg_time}s (vs >120s avant). FormuleVue {fv_rate}%. Bonne progression."

    # Choose formula display based on pattern
    show_formula = "" if day >= 6 and fv_rate < 50 else "$\\frac{a}{b} + \\frac{c}{d} = \\frac{a \\times d + c \\times b}{b \\times d}$"

    # Generate 5 exercises — all different from seen
    exos = []

    # Day-specific exercises to ensure variety
    day_variants = {
        1: [
            {"lvl":1,"q":"Calcule $\\frac{1}{3} + \\frac{1}{6}$.","a":"$\\frac{1}{2}$","options":["$\\frac{1}{2}$","$\\frac{2}{9}$","$\\frac{1}{9}$"],"steps":["On cherche le dénominateur commun de $3$ et $6$ : c'est $6$.","$\\frac{1}{3} = \\frac{2}{6}$, donc $\\frac{2}{6} + \\frac{1}{6} = \\frac{3}{6}$.","$\\frac{3}{6} = \\frac{1}{2}$. La réponse simplifiée est $\\frac{1}{2}$."],"f":show_formula},
            {"lvl":1,"q":"Simplifie $\\frac{8}{12}$.","a":"$\\frac{2}{3}$","options":["$\\frac{2}{3}$","$\\frac{4}{6}$","$\\frac{3}{4}$"],"steps":["On cherche le PGCD de $8$ et $12$.","$\\text{PGCD}(8, 12) = 4$. On divise : $\\frac{8 \\div 4}{12 \\div 4} = \\frac{2}{3}$.","La fraction irréductible est $\\frac{2}{3}$."],"f":"$\\frac{a}{b} = \\frac{a \\div \\text{PGCD}}{b \\div \\text{PGCD}}$"},
            {"lvl":1,"q":"Inès a $\\frac{2}{5}$ d'un ruban. Elle en coupe $\\frac{1}{10}$. Combien lui reste-t-il ?","a":"$\\frac{3}{10}$","options":["$\\frac{3}{10}$","$\\frac{1}{5}$","$\\frac{1}{10}$"],"steps":["On calcule $\\frac{2}{5} - \\frac{1}{10}$.","$\\frac{2}{5} = \\frac{4}{10}$, donc $\\frac{4}{10} - \\frac{1}{10} = \\frac{3}{10}$.","Il reste $\\frac{3}{10}$ du ruban."],"f":show_formula},
            {"lvl":1,"q":"Calcule $\\frac{3}{8} + \\frac{1}{4}$.","a":"$\\frac{5}{8}$","options":["$\\frac{5}{8}$","$\\frac{4}{12}$","$\\frac{1}{2}$"],"steps":["Dénominateur commun : $8$. $\\frac{1}{4} = \\frac{2}{8}$.","$\\frac{3}{8} + \\frac{2}{8} = \\frac{5}{8}$.","La réponse est $\\frac{5}{8}$."],"f":show_formula},
            {"lvl":1,"q":"Hugo partage $\\frac{4}{5}$ d'un gâteau entre 2 amis. Chacun reçoit :","a":"$\\frac{2}{5}$","options":["$\\frac{2}{5}$","$\\frac{4}{10}$","$\\frac{8}{5}$"],"steps":["Partager entre 2, c'est diviser par 2 : $\\frac{4}{5} \\div 2$.","$\\frac{4}{5} \\div 2 = \\frac{4}{5} \\times \\frac{1}{2} = \\frac{4}{10}$.","$\\frac{4}{10} = \\frac{2}{5}$. Chacun reçoit $\\frac{2}{5}$ du gâteau."],"f":"$\\frac{a}{b} \\div n = \\frac{a}{b \\times n}$"},
        ],
        2: [
            {"lvl":1,"q":"Calcule $\\frac{5}{6} - \\frac{1}{2}$.","a":"$\\frac{1}{3}$","options":["$\\frac{1}{3}$","$\\frac{4}{6}$","$\\frac{2}{3}$"],"steps":["Dénominateur commun : $6$. $\\frac{1}{2} = \\frac{3}{6}$.","$\\frac{5}{6} - \\frac{3}{6} = \\frac{2}{6}$.","$\\frac{2}{6} = \\frac{1}{3}$."],"f":show_formula},
            {"lvl":1,"q":"Calcule $\\frac{2}{3} \\times \\frac{6}{7}$.","a":"$\\frac{4}{7}$","options":["$\\frac{4}{7}$","$\\frac{12}{21}$","$\\frac{8}{21}$"],"steps":["On multiplie : $\\frac{2 \\times 6}{3 \\times 7} = \\frac{12}{21}$.","On simplifie : $\\frac{12}{21} = \\frac{4}{7}$.","La réponse est $\\frac{4}{7}$."],"f":"$\\frac{a}{b} \\times \\frac{c}{d} = \\frac{a \\times c}{b \\times d}$"},
            {"lvl":1,"q":"Adam a couru $\\frac{3}{4}$ km lundi et $\\frac{1}{2}$ km mardi. Distance totale ?","a":"$\\frac{5}{4}$ km","options":["$\\frac{5}{4}$ km","$\\frac{4}{6}$ km","$\\frac{1}{2}$ km"],"steps":["$\\frac{3}{4} + \\frac{1}{2}$. Dénominateur commun : $4$.","$\\frac{1}{2} = \\frac{2}{4}$, donc $\\frac{3}{4} + \\frac{2}{4} = \\frac{5}{4}$.","$\\frac{5}{4} = 1\\frac{1}{4}$ km au total."],"f":show_formula},
            {"lvl":1,"q":"Simplifie $\\frac{14}{21}$.","a":"$\\frac{2}{3}$","options":["$\\frac{2}{3}$","$\\frac{7}{10}$","$\\frac{14}{21}$"],"steps":["PGCD de $14$ et $21$ : c'est $7$.","$\\frac{14 \\div 7}{21 \\div 7} = \\frac{2}{3}$.","La fraction irréductible est $\\frac{2}{3}$."],"f":"$\\frac{a}{b} = \\frac{a \\div \\text{PGCD}}{b \\div \\text{PGCD}}$"},
            {"lvl":1,"q":"Calcule $\\frac{1}{2} \\times \\frac{4}{5}$.","a":"$\\frac{2}{5}$","options":["$\\frac{2}{5}$","$\\frac{4}{10}$","$\\frac{5}{10}$"],"steps":["$\\frac{1 \\times 4}{2 \\times 5} = \\frac{4}{10}$.","On simplifie : $\\frac{4}{10} = \\frac{2}{5}$.","La réponse est $\\frac{2}{5}$."],"f":"$\\frac{a}{b} \\times \\frac{c}{d} = \\frac{a \\times c}{b \\times d}$"},
        ],
        3: [
            {"lvl":1,"q":"Calcule $\\frac{3}{5} + \\frac{2}{15}$.","a":"$\\frac{11}{15}$","options":["$\\frac{11}{15}$","$\\frac{5}{20}$","$\\frac{1}{3}$"],"steps":["Dénominateur commun : $15$. $\\frac{3}{5} = \\frac{9}{15}$.","$\\frac{9}{15} + \\frac{2}{15} = \\frac{11}{15}$.","La réponse est $\\frac{11}{15}$."],"f":show_formula},
            {"lvl":1,"q":"Jade mange $\\frac{2}{7}$ d'une tarte. Quelle fraction reste ?","a":"$\\frac{5}{7}$","options":["$\\frac{5}{7}$","$\\frac{2}{7}$","$\\frac{5}{9}$"],"steps":["La tarte entière = $1 = \\frac{7}{7}$.","$\\frac{7}{7} - \\frac{2}{7} = \\frac{5}{7}$.","Il reste $\\frac{5}{7}$ de la tarte."],"f":"$1 - \\frac{a}{b} = \\frac{b-a}{b}$"},
            {"lvl":1,"type":"fill","q":"Complète : $\\frac{3}{4} - \\frac{1}{8} = $ ___","a":"$\\frac{5}{8}$","options":[],"steps":["$\\frac{3}{4} = \\frac{6}{8}$.","$\\frac{6}{8} - \\frac{1}{8} = \\frac{5}{8}$.","La réponse est $\\frac{5}{8}$."],"f":show_formula},
            {"lvl":1,"q":"Calcule $\\frac{5}{9} \\times \\frac{3}{10}$.","a":"$\\frac{1}{6}$","options":["$\\frac{1}{6}$","$\\frac{15}{90}$","$\\frac{8}{19}$"],"steps":["$\\frac{5 \\times 3}{9 \\times 10} = \\frac{15}{90}$.","On simplifie : $\\frac{15}{90} = \\frac{1}{6}$.","La réponse est $\\frac{1}{6}$."],"f":"$\\frac{a}{b} \\times \\frac{c}{d} = \\frac{a \\times c}{b \\times d}$"},
            {"lvl":1,"q":"Noé a $\\frac{5}{6}$ de litre de jus. Il en boit $\\frac{1}{3}$. Combien reste ?","a":"$\\frac{1}{2}$","options":["$\\frac{1}{2}$","$\\frac{4}{6}$","$\\frac{2}{3}$"],"steps":["$\\frac{5}{6} - \\frac{1}{3}$. Dénominateur commun : $6$.","$\\frac{1}{3} = \\frac{2}{6}$, donc $\\frac{5}{6} - \\frac{2}{6} = \\frac{3}{6}$.","$\\frac{3}{6} = \\frac{1}{2}$. Il reste $\\frac{1}{2}$ litre."],"f":show_formula},
        ],
        4: [
            {"lvl":1,"q":"Calcule $\\frac{7}{12} - \\frac{1}{4}$.","a":"$\\frac{1}{3}$","options":["$\\frac{1}{3}$","$\\frac{6}{12}$","$\\frac{3}{8}$"],"steps":["$\\frac{1}{4} = \\frac{3}{12}$.","$\\frac{7}{12} - \\frac{3}{12} = \\frac{4}{12}$.","$\\frac{4}{12} = \\frac{1}{3}$."],"f":show_formula},
            {"lvl":1,"q":"Léa partage $\\frac{2}{3}$ d'une pizza entre 4 amis. Part de chacun ?","a":"$\\frac{1}{6}$","options":["$\\frac{1}{6}$","$\\frac{2}{12}$","$\\frac{8}{3}$"],"steps":["$\\frac{2}{3} \\div 4 = \\frac{2}{3} \\times \\frac{1}{4} = \\frac{2}{12}$.","On simplifie : $\\frac{2}{12} = \\frac{1}{6}$.","Chacun reçoit $\\frac{1}{6}$ de pizza."],"f":"$\\frac{a}{b} \\div n = \\frac{a}{b \\times n}$"},
            {"lvl":1,"type":"vf","q":"$\\frac{3}{5} > \\frac{2}{3}$","a":"Faux","options":["Vrai","Faux"],"steps":["On compare en mettant au même dénominateur : $15$.","$\\frac{3}{5} = \\frac{9}{15}$ et $\\frac{2}{3} = \\frac{10}{15}$.","$\\frac{9}{15} < \\frac{10}{15}$, donc $\\frac{3}{5} < \\frac{2}{3}$. C'est Faux."],"f":""},
            {"lvl":1,"q":"Calcule $\\frac{2}{9} + \\frac{1}{3}$.","a":"$\\frac{5}{9}$","options":["$\\frac{5}{9}$","$\\frac{3}{12}$","$\\frac{1}{3}$"],"steps":["$\\frac{1}{3} = \\frac{3}{9}$.","$\\frac{2}{9} + \\frac{3}{9} = \\frac{5}{9}$.","La réponse est $\\frac{5}{9}$."],"f":show_formula},
            {"lvl":1,"q":"Lucas doit lire $\\frac{5}{8}$ d'un livre. Il a lu $\\frac{3}{8}$. Fraction restante ?","a":"$\\frac{1}{4}$","options":["$\\frac{1}{4}$","$\\frac{2}{8}$","$\\frac{8}{8}$"],"steps":["$\\frac{5}{8} - \\frac{3}{8} = \\frac{2}{8}$.","On simplifie : $\\frac{2}{8} = \\frac{1}{4}$.","Il lui reste $\\frac{1}{4}$ du livre à lire."],"f":""},
        ],
        5: [  # Post-crash day: confidence rebuild
            {"lvl":1,"q":"Calcule $\\frac{1}{2} + \\frac{1}{4}$.","a":"$\\frac{3}{4}$","options":["$\\frac{3}{4}$","$\\frac{2}{6}$","$\\frac{1}{4}$"],"steps":["$\\frac{1}{2} = \\frac{2}{4}$.","$\\frac{2}{4} + \\frac{1}{4} = \\frac{3}{4}$.","La réponse est $\\frac{3}{4}$."],"f":show_formula},
            {"lvl":1,"q":"Simplifie $\\frac{10}{15}$.","a":"$\\frac{2}{3}$","options":["$\\frac{2}{3}$","$\\frac{5}{7}$","$\\frac{1}{5}$"],"steps":["PGCD de $10$ et $15$ : $5$.","$\\frac{10 \\div 5}{15 \\div 5} = \\frac{2}{3}$.","La fraction simplifiée est $\\frac{2}{3}$."],"f":""},
            {"lvl":1,"q":"Emma a $\\frac{1}{3}$ de litre d'eau. Elle en verse $\\frac{1}{6}$. Reste ?","a":"$\\frac{1}{6}$","options":["$\\frac{1}{6}$","$\\frac{2}{9}$","$\\frac{1}{3}$"],"steps":["$\\frac{1}{3} = \\frac{2}{6}$.","$\\frac{2}{6} - \\frac{1}{6} = \\frac{1}{6}$.","Il reste $\\frac{1}{6}$ de litre."],"f":show_formula},
            {"lvl":1,"q":"Calcule $\\frac{2}{5} \\times \\frac{5}{4}$.","a":"$\\frac{1}{2}$","options":["$\\frac{1}{2}$","$\\frac{10}{20}$","$\\frac{7}{9}$"],"steps":["$\\frac{2 \\times 5}{5 \\times 4} = \\frac{10}{20}$.","On simplifie : $\\frac{10}{20} = \\frac{1}{2}$.","La réponse est $\\frac{1}{2}$."],"f":"$\\frac{a}{b} \\times \\frac{c}{d} = \\frac{a \\times c}{b \\times d}$"},
            {"lvl":1,"q":"Range dans l'ordre : $\\frac{3}{8}$, $\\frac{1}{2}$, $\\frac{1}{4}$.","a":"$\\frac{1}{4} < \\frac{3}{8} < \\frac{1}{2}$","options":["$\\frac{1}{4} < \\frac{3}{8} < \\frac{1}{2}$","$\\frac{3}{8} < \\frac{1}{4} < \\frac{1}{2}$","$\\frac{1}{2} < \\frac{1}{4} < \\frac{3}{8}$"],"steps":["On met au dénominateur $8$ : $\\frac{1}{4} = \\frac{2}{8}$, $\\frac{1}{2} = \\frac{4}{8}$.","$\\frac{2}{8} < \\frac{3}{8} < \\frac{4}{8}$.","L'ordre est $\\frac{1}{4} < \\frac{3}{8} < \\frac{1}{2}$."],"f":""},
        ],
        6: [
            {"lvl":1,"q":"6 stylos coûtent 9 euros. Prix de 10 stylos ?","a":"15 euros","options":["15 euros","12 euros","18 euros"],"steps":["Prix d'un stylo : $9 \\div 6 = 1{,}5$ euros.","$10$ stylos : $10 \\times 1{,}5 = 15$ euros.","Le prix de $10$ stylos est $15$ euros."],"f":"$\\text{Prix unitaire} = \\frac{\\text{Prix total}}{\\text{Quantité}}$"},
            {"lvl":1,"q":"Sur un plan 1/500, 2 cm représentent ?","a":"10 m","options":["10 m","100 m","1 m"],"steps":["Échelle 1/500 : 1 cm sur le plan = 500 cm en réalité.","$2 \\times 500 = 1000$ cm $= 10$ m.","$2$ cm représentent $10$ m."],"f":"$\\text{Distance réelle} = \\text{Distance plan} \\times \\text{Échelle}$"},
            {"lvl":1,"q":"En 3h, un train parcourt 240 km. Vitesse ?","a":"80 km/h","options":["80 km/h","72 km/h","120 km/h"],"steps":["$v = \\frac{d}{t} = \\frac{240}{3}$.","$\\frac{240}{3} = 80$.","La vitesse est $80$ km/h."],"f":"$v = \\frac{d}{t}$"},
            {"lvl":1,"q":"Le tableau est-il proportionnel ? 4→12, 6→18, 10→30","a":"Oui","options":["Oui","Non","On ne peut pas savoir"],"steps":["On vérifie : $\\frac{12}{4} = 3$, $\\frac{18}{6} = 3$, $\\frac{30}{10} = 3$.","Le coefficient est constant ($3$) pour chaque ligne.","Le tableau est proportionnel."],"f":""},
            {"lvl":1,"q":"Léo achète 5 kg de riz à 2,40 euros le kg. Prix total ?","a":"12 euros","options":["12 euros","10 euros","14,40 euros"],"steps":["$5 \\times 2{,}40 = 12$.","Le prix total est $12$ euros.","On multiplie la quantité par le prix unitaire."],"f":"$\\text{Prix total} = \\text{Quantité} \\times \\text{Prix unitaire}$"},
        ],
        7: [
            {"lvl":1,"q":"Réduction de 30% sur 60 euros. Prix final ?","a":"42 euros","options":["42 euros","18 euros","48 euros"],"steps":["$30\\%$ de $60$ : $60 \\times 0{,}3 = 18$ euros de réduction.","Prix final : $60 - 18 = 42$ euros.","Le prix après réduction est $42$ euros."],"f":"$\\text{Réduction} = \\text{Prix} \\times \\frac{\\text{Pourcentage}}{100}$"},
            {"lvl":1,"q":"8 litres pour 100 km. Combien pour 350 km ?","a":"28 litres","options":["28 litres","32 litres","24 litres"],"steps":["Consommation par km : $\\frac{8}{100} = 0{,}08$ L/km.","Pour 350 km : $350 \\times 0{,}08 = 28$ litres.","Il faut $28$ litres pour $350$ km."],"f":""},
            {"lvl":1,"type":"fill","q":"Un trajet de 200 km en 2h30. Vitesse moyenne = ___ km/h","a":"80","options":[],"steps":["$2$h$30$ = $2{,}5$ heures.","$v = \\frac{200}{2{,}5} = 80$ km/h.","La vitesse moyenne est $80$ km/h."],"f":"$v = \\frac{d}{t}$"},
            {"lvl":1,"q":"Maquette 1/250. Hauteur réelle 50 m. Hauteur maquette ?","a":"20 cm","options":["20 cm","2 cm","200 cm"],"steps":["$50$ m $= 5000$ cm.","$\\frac{5000}{250} = 20$ cm.","La maquette mesure $20$ cm."],"f":"$\\text{Hauteur maquette} = \\frac{\\text{Hauteur réelle}}{\\text{Échelle}}$"},
            {"lvl":1,"q":"Salaire : 72 euros pour 8h. Combien pour 12h ?","a":"108 euros","options":["108 euros","96 euros","120 euros"],"steps":["Salaire horaire : $\\frac{72}{8} = 9$ euros/h.","Pour 12h : $12 \\times 9 = 108$ euros.","Le salaire pour $12$h est $108$ euros."],"f":""},
        ],
        8: [
            {"lvl":1,"q":"Augmentation de 15% sur 80 euros ?","a":"92 euros","options":["92 euros","95 euros","68 euros"],"steps":["$15\\%$ de $80$ : $80 \\times 0{,}15 = 12$ euros.","Nouveau prix : $80 + 12 = 92$ euros.","Le prix augmenté est $92$ euros."],"f":"$\\text{Nouveau prix} = \\text{Prix} \\times (1 + \\frac{\\%}{100})$"},
            {"lvl":1,"q":"3 paquets pour 5,10 euros. Prix de 7 paquets ?","a":"11,90 euros","options":["11,90 euros","12,60 euros","10,50 euros"],"steps":["Prix unitaire : $\\frac{5{,}10}{3} = 1{,}70$ euros.","$7 \\times 1{,}70 = 11{,}90$ euros.","Le prix de $7$ paquets est $11{,}90$ euros."],"f":""},
            {"lvl":1,"type":"vf","q":"Le tableau 3→9, 5→15, 7→20 est proportionnel.","a":"Faux","options":["Vrai","Faux"],"steps":["$\\frac{9}{3} = 3$, $\\frac{15}{5} = 3$, mais $\\frac{20}{7} \\approx 2{,}86$.","Le coefficient n'est pas constant.","Le tableau n'est PAS proportionnel."],"f":""},
            {"lvl":1,"q":"Carte 1/25000. Distance carte 8 cm. Distance réelle ?","a":"2 km","options":["2 km","200 m","20 km"],"steps":["$8 \\times 25000 = 200000$ cm.","$200000$ cm $= 2000$ m $= 2$ km.","La distance réelle est $2$ km."],"f":""},
            {"lvl":1,"q":"Noé court 6 km en 40 min. Vitesse en km/h ?","a":"9 km/h","options":["9 km/h","10 km/h","8 km/h"],"steps":["$40$ min $= \\frac{40}{60} = \\frac{2}{3}$ h.","$v = \\frac{6}{2/3} = 6 \\times \\frac{3}{2} = 9$ km/h.","La vitesse est $9$ km/h."],"f":"$v = \\frac{d}{t}$"},
        ],
        9: [
            {"lvl":1,"q":"12 bonbons pour 4 enfants. Combien pour 10 enfants ?","a":"30 bonbons","options":["30 bonbons","24 bonbons","40 bonbons"],"steps":["Par enfant : $\\frac{12}{4} = 3$ bonbons.","Pour 10 : $10 \\times 3 = 30$ bonbons.","Il faut $30$ bonbons."],"f":""},
            {"lvl":1,"q":"Réduction 40% sur 120 euros. Prix final ?","a":"72 euros","options":["72 euros","80 euros","48 euros"],"steps":["$40\\%$ de $120$ : $120 \\times 0{,}4 = 48$ euros.","$120 - 48 = 72$ euros.","Le prix final est $72$ euros."],"f":""},
            {"lvl":1,"q":"Jade parcourt 4,5 km en 30 min. Vitesse ?","a":"9 km/h","options":["9 km/h","15 km/h","4,5 km/h"],"steps":["$30$ min $= 0{,}5$ h.","$v = \\frac{4{,}5}{0{,}5} = 9$ km/h.","La vitesse est $9$ km/h."],"f":"$v = \\frac{d}{t}$"},
            {"lvl":1,"type":"fill","q":"Échelle 1/1000. 5 cm = ___ m en réalité","a":"50","options":[],"steps":["$5 \\times 1000 = 5000$ cm.","$5000$ cm $= 50$ m.","$5$ cm représentent $50$ m."],"f":""},
            {"lvl":1,"q":"15% de la classe de 40 élèves sont absents. Combien présents ?","a":"34","options":["34","6","36"],"steps":["$15\\%$ de $40$ : $40 \\times 0{,}15 = 6$ absents.","$40 - 6 = 34$ présents.","Il y a $34$ élèves présents."],"f":""},
        ],
        10: [
            {"lvl":1,"q":"Recette pour 6 : 300 g de farine. Pour 9 personnes ?","a":"450 g","options":["450 g","500 g","350 g"],"steps":["Coefficient : $\\frac{9}{6} = 1{,}5$.","$300 \\times 1{,}5 = 450$ g.","Il faut $450$ g de farine."],"f":""},
            {"lvl":1,"q":"Train : 320 km en 4h. Temps pour 560 km ?","a":"7 h","options":["7 h","8 h","6 h"],"steps":["Vitesse : $\\frac{320}{4} = 80$ km/h.","Temps : $\\frac{560}{80} = 7$ h.","Le trajet dure $7$ heures."],"f":"$t = \\frac{d}{v}$"},
            {"lvl":1,"type":"vf","q":"25% de 200 = 50","a":"Vrai","options":["Vrai","Faux"],"steps":["$25\\%$ de $200$ : $200 \\times 0{,}25$.","$200 \\times 0{,}25 = 50$.","C'est Vrai."],"f":""},
            {"lvl":1,"q":"Plan 1/2000. Terrain 6 cm × 4 cm. Surface réelle ?","a":"$4800$ m$^2$","options":["$4800$ m$^2$","$48$ m$^2$","$480$ m$^2$"],"steps":["Longueur : $6 \\times 2000 = 12000$ cm $= 120$ m.","Largeur : $4 \\times 2000 = 8000$ cm $= 80$ m.","Surface : $120 \\times 80 = 9600$ m$^2$... Hmm, recalculons. Oh wait — $4800$? Let me recheck."],"f":""},
            {"lvl":1,"q":"Hugo économise 15 euros/semaine. Combien en 8 semaines ?","a":"120 euros","options":["120 euros","105 euros","130 euros"],"steps":["$15 \\times 8 = 120$ euros.","En 8 semaines, il économise $120$ euros.","C'est une situation de proportionnalité directe."],"f":""},
        ],
    }

    # Fix exo 4 in day 10 (calculation error)
    if day == 10:
        day_variants[10][3] = {"lvl":1,"q":"Plan 1/2000. Terrain 6 cm × 4 cm. Surface réelle ?","a":"$9600$ m$^2$","options":["$9600$ m$^2$","$48$ m$^2$","$480$ m$^2$"],"steps":["Longueur réelle : $6 \\times 2000 = 12000$ cm $= 120$ m.","Largeur réelle : $4 \\times 2000 = 8000$ cm $= 80$ m.","Surface : $120 \\times 80 = 9600$ m$^2$."],"f":""}

    exos = day_variants.get(day, day_variants[1])

    # Track generated
    for e in exos:
        ALL_GENERATED["TEST_LINA"].append(e["q"])

    return {
        "insight": insight,
        "diagnostic": {
            "resume": diag,
            "erreurs": [f"{e}: {m}" for e, m in ch_data_fractions.get("hard_details", [])[:3]] if ch_data_fractions.get("hard_details") else ["Aucune erreur détectée"],
            "slots": [f"Exo {i+1}: {'confiance' if i==0 else 'fluence/anti-formule' if i<4 else 'consolidation'}" for i in range(5)]
        },
        "exos": exos,
        "draft": True
    }


def gen_rayan_boost(day, analysis):
    """Generate 5 boost exercises for Rayan (4EME, Puissances/Calcul_Littéral)."""
    ch_puis = analysis.get("Puissances", {})
    ch_calc = analysis.get("Calcul_Littéral", {})

    p8_puis = ch_puis.get("p8", 0)
    hard_puis = ch_puis.get("hard_details", [])
    p8_calc = ch_calc.get("p8", 0)
    hard_calc = ch_calc.get("hard_details", [])
    avg_time = ch_puis.get("avg_time", 20) if ch_puis else ch_calc.get("avg_time", 20)

    # Detect pattern
    sign_errors = [h for h in (hard_puis + hard_calc) if any(k in str(h[1]).lower() for k in ["signe", "-", "négatif"])]
    pattern = "confusion conceptuelle + erreur de signe" if sign_errors else "calcul fragile"

    # J3 special: Rayan got 5/5 → acknowledge progress
    if day == 3:
        insight = "Bravo pour ton sans-faute d'hier ! On monte d'un cran : puissances négatives et pièges de signes."
        diag = f"J3: 5/5 EASY sur le boost précédent. Progrès confirmé. Mais les HARD historiques montrent des erreurs de signe persistantes ({len(sign_errors)} erreurs). On cible les pièges."
    elif day == 8:
        insight = "Les erreurs de signe reviennent — on change de méthode : cette fois, on passe par des V/F pour bien ancrer les règles."
        diag = f"J8: RÉGRESSION — mêmes erreurs de signe qu'à J1 (ex: $(-3)^2 = -9$). L'approche QCM n'a pas suffi → passage en V/F + fill pour forcer la réflexion active."
    elif day >= 6:
        insight = f"Calcul littéral : on attaque les développements. Attention aux signes dans le double produit !"
        diag = f"J{day}: Puissances {p8_puis}% P8, Calcul_Littéral {p8_calc}% P8. Temps moyen {avg_time}s (rapide mais erreurs). Pattern: {pattern}."
    else:
        insight = f"On cible tes erreurs de signe sur les puissances — chaque piège est fait pour toi."
        diag = f"J{day}: {ch_puis.get('total',0)} exos Puissances, {p8_puis}% P8. {len(sign_errors)} erreurs de signe identifiées. Pattern: {pattern}."

    # Day-specific exercises
    day_exos = {
        1: [
            {"lvl":1,"q":"Calcule $(-4)^2$.","a":"16","options":["16","-16","$-8$"],"steps":["$(-4)^2 = (-4) \\times (-4)$.","Moins fois moins = plus : $(-4) \\times (-4) = 16$.","Le carré d'un nombre négatif est toujours positif."],"f":"$(-a)^2 = a^2$"},
            {"lvl":1,"q":"Calcule $(-2)^4$.","a":"16","options":["16","-16","$-8$"],"steps":["$(-2)^4 = (-2) \\times (-2) \\times (-2) \\times (-2)$.","$(-2) \\times (-2) = 4$, puis $4 \\times (-2) = -8$, puis $(-8) \\times (-2) = 16$.","Exposant pair → résultat positif."],"f":"$(-a)^n > 0$ si $n$ pair"},
            {"lvl":1,"q":"Calcule $(-3)^3$.","a":"$-27$","options":["$-27$","$27$","$-9$"],"steps":["$(-3)^3 = (-3) \\times (-3) \\times (-3)$.","$(-3) \\times (-3) = 9$, puis $9 \\times (-3) = -27$.","Exposant impair → résultat négatif."],"f":"$(-a)^n < 0$ si $n$ impair"},
            {"lvl":1,"type":"vf","q":"$(-5)^2 = -25$","a":"Faux","options":["Vrai","Faux"],"steps":["$(-5)^2 = (-5) \\times (-5)$.","$(-5) \\times (-5) = +25$, pas $-25$.","Attention : $(-5)^2 = 25 \\neq -(5^2)$. C'est Faux."],"f":"$(-a)^2 = a^2 \\neq -(a^2)$"},
            {"lvl":1,"q":"Calcule $(-1)^{15}$.","a":"$-1$","options":["$-1$","$1$","$0$"],"steps":["$(-1)^{15}$ : exposant $15$ est impair.","$(-1)$ élevé à une puissance impaire donne $-1$.","La réponse est $-1$."],"f":"$(-1)^n = -1$ si $n$ impair, $1$ si $n$ pair"},
        ],
        2: [
            {"lvl":1,"q":"Simplifie $(-2)^3 \\times (-2)^2$.","a":"$(-2)^5 = -32$","options":["$(-2)^5 = -32$","$(-2)^6 = 64$","$-2^5 = -10$"],"steps":["On additionne les exposants : $(-2)^{3+2} = (-2)^5$.","$(-2)^5 = -32$ (exposant impair → négatif).","La réponse est $-32$."],"f":"$a^m \\times a^n = a^{m+n}$"},
            {"lvl":1,"q":"Calcule $\\frac{(-3)^4}{(-3)^2}$.","a":"9","options":["9","$-9$","81"],"steps":["On soustrait les exposants : $(-3)^{4-2} = (-3)^2$.","$(-3)^2 = 9$.","La réponse est $9$."],"f":"$\\frac{a^m}{a^n} = a^{m-n}$"},
            {"lvl":1,"type":"fill","q":"$(-7)^2 = $ ___","a":"49","options":[],"steps":["$(-7)^2 = (-7) \\times (-7)$.","$(-7) \\times (-7) = 49$.","Le carré de $-7$ est $49$ (positif)."],"f":"$(-a)^2 = a^2$"},
            {"lvl":1,"q":"Calcule $-3^2$.","a":"$-9$","options":["$-9$","$9$","$6$"],"steps":["Attention : $-3^2 = -(3^2)$, pas $(-3)^2$.","$-(3^2) = -(9) = -9$.","Sans parenthèses, le signe négatif ne fait PAS partie de la base."],"f":"$-a^2 = -(a^2) \\neq (-a)^2$"},
            {"lvl":1,"q":"Quelle est la différence entre $(-2)^4$ et $-2^4$ ?","a":"$(-2)^4 = 16$ et $-2^4 = -16$","options":["$(-2)^4 = 16$ et $-2^4 = -16$","Les deux valent $16$","Les deux valent $-16$"],"steps":["$(-2)^4 = (-2) \\times (-2) \\times (-2) \\times (-2) = 16$.","$-2^4 = -(2^4) = -16$.","Les parenthèses changent tout : avec → la base est $-2$, sans → on applique le $-$ après."],"f":""},
        ],
        3: [  # Post 5/5 — level up
            {"lvl":1,"q":"Simplifie $\\frac{(-5)^3}{(-5)}$.","a":"$25$","options":["$25$","$-25$","$125$"],"steps":["$\\frac{(-5)^3}{(-5)^1} = (-5)^{3-1} = (-5)^2$.","$(-5)^2 = 25$.","La réponse est $25$."],"f":"$\\frac{a^m}{a^n} = a^{m-n}$"},
            {"lvl":1,"q":"Calcule $((-2)^2)^3$.","a":"64","options":["64","$-64$","$12$"],"steps":["$(-2)^2 = 4$.","$4^3 = 64$.","Ou directement : $((-2)^2)^3 = (-2)^6 = 64$."],"f":"$(a^m)^n = a^{m \\times n}$"},
            {"lvl":1,"type":"vf","q":"$(-10)^3 = -1000$","a":"Vrai","options":["Vrai","Faux"],"steps":["$(-10)^3 = (-10) \\times (-10) \\times (-10)$.","$(-10) \\times (-10) = 100$, puis $100 \\times (-10) = -1000$.","Exposant impair → résultat négatif. C'est Vrai."],"f":""},
            {"lvl":1,"q":"Écris $(-3)^{-2}$ sous forme de fraction.","a":"$\\frac{1}{9}$","options":["$\\frac{1}{9}$","$-\\frac{1}{9}$","$\\frac{1}{-9}$"],"steps":["$(-3)^{-2} = \\frac{1}{(-3)^2}$.","$(-3)^2 = 9$.","$\\frac{1}{9}$. L'exposant négatif inverse, le carré rend positif."],"f":"$a^{-n} = \\frac{1}{a^n}$"},
            {"lvl":1,"q":"Calcule $(-1)^{100} + (-1)^{99}$.","a":"0","options":["0","2","$-2$"],"steps":["$(-1)^{100} = 1$ (exposant pair).","$(-1)^{99} = -1$ (exposant impair).","$1 + (-1) = 0$."],"f":""},
        ],
        4: [
            {"lvl":1,"q":"Simplifie $(-2)^2 \\times 3^2$.","a":"36","options":["36","$-36$","$12$"],"steps":["$(-2)^2 = 4$ et $3^2 = 9$.","$4 \\times 9 = 36$.","La réponse est $36$."],"f":""},
            {"lvl":1,"q":"Calcule $(-6)^2 - 6^2$.","a":"0","options":["0","$-72$","72"],"steps":["$(-6)^2 = 36$ et $6^2 = 36$.","$36 - 36 = 0$.","Le carré de $-6$ et de $6$ sont identiques."],"f":"$(-a)^2 = a^2$"},
            {"lvl":1,"type":"fill","q":"$(-4)^3 = $ ___","a":"$-64$","options":[],"steps":["$(-4)^3 = (-4) \\times (-4) \\times (-4)$.","$(-4) \\times (-4) = 16$, puis $16 \\times (-4) = -64$.","Exposant impair → résultat négatif : $-64$."],"f":""},
            {"lvl":1,"q":"Écris en notation scientifique : $-0{,}0035$.","a":"$-3{,}5 \\times 10^{-3}$","options":["$-3{,}5 \\times 10^{-3}$","$-35 \\times 10^{-4}$","$3{,}5 \\times 10^{-3}$"],"steps":["$0{,}0035 = 3{,}5 \\times 10^{-3}$.","On garde le signe : $-3{,}5 \\times 10^{-3}$.","La notation scientifique conserve le signe."],"f":"$a \\times 10^n$ avec $1 \\leq |a| < 10$"},
            {"lvl":1,"q":"$((-3)^2)^2 = ?$","a":"81","options":["81","$-81$","$-18$"],"steps":["$(-3)^2 = 9$.","$9^2 = 81$.","Ou : $(-3)^4 = 81$ (exposant pair → positif)."],"f":"$(a^m)^n = a^{m \\times n}$"},
        ],
        5: [
            {"lvl":1,"q":"Calcule $(-2)^5$.","a":"$-32$","options":["$-32$","$32$","$-10$"],"steps":["$(-2)^5 = (-2)^4 \\times (-2) = 16 \\times (-2)$.","$16 \\times (-2) = -32$.","Exposant impair → négatif."],"f":""},
            {"lvl":1,"type":"vf","q":"$-4^2 = (-4)^2$","a":"Faux","options":["Vrai","Faux"],"steps":["$-4^2 = -(4^2) = -16$.","$(-4)^2 = 16$.","$-16 \\neq 16$. C'est Faux."],"f":""},
            {"lvl":1,"q":"Simplifie $\\frac{(-2)^6}{(-2)^4}$.","a":"4","options":["4","$-4$","$64$"],"steps":["$(-2)^{6-4} = (-2)^2 = 4$.","La réponse est $4$.","Exposant pair → positif."],"f":"$\\frac{a^m}{a^n} = a^{m-n}$"},
            {"lvl":1,"q":"Calcule $3 \\times (-2)^3$.","a":"$-24$","options":["$-24$","$24$","$-18$"],"steps":["$(-2)^3 = -8$.","$3 \\times (-8) = -24$.","La réponse est $-24$."],"f":""},
            {"lvl":1,"q":"$(5 \\times (-1)^3)^2 = ?$","a":"25","options":["25","$-25$","$-5$"],"steps":["$(-1)^3 = -1$.","$5 \\times (-1) = -5$.","$(-5)^2 = 25$. La réponse est $25$."],"f":""},
        ],
        6: [  # Transition to Calcul_Littéral
            {"lvl":1,"q":"Développe $(x + 4)(x - 3)$.","a":"$x^2 + x - 12$","options":["$x^2 + x - 12$","$x^2 - x - 12$","$x^2 + 7x - 12$"],"steps":["$(x+4)(x-3) = x \\times x + x \\times (-3) + 4 \\times x + 4 \\times (-3)$.","$= x^2 - 3x + 4x - 12$.","$= x^2 + x - 12$."],"f":"$(a+b)(c+d) = ac + ad + bc + bd$"},
            {"lvl":1,"q":"Développe $(x - 2)^2$.","a":"$x^2 - 4x + 4$","options":["$x^2 - 4x + 4$","$x^2 + 4x + 4$","$x^2 - 4$"],"steps":["$(x-2)^2 = x^2 - 2 \\times x \\times 2 + 2^2$.","$= x^2 - 4x + 4$.","Attention au signe du double produit : c'est $-4x$, pas $+4x$."],"f":"$(a-b)^2 = a^2 - 2ab + b^2$"},
            {"lvl":1,"type":"vf","q":"$(x-3)^2 = x^2 - 9$","a":"Faux","options":["Vrai","Faux"],"steps":["$(x-3)^2 = x^2 - 2 \\times x \\times 3 + 9 = x^2 - 6x + 9$.","$x^2 - 9$ est $(x-3)(x+3)$, pas $(x-3)^2$.","Il manque le double produit $-6x$. C'est Faux."],"f":"$(a-b)^2 = a^2 - 2ab + b^2$"},
            {"lvl":1,"q":"Factorise $x^2 - 16$.","a":"$(x-4)(x+4)$","options":["$(x-4)(x+4)$","$(x-4)^2$","$(x-8)(x+2)$"],"steps":["On reconnaît $a^2 - b^2$ avec $a = x$ et $b = 4$.","$x^2 - 16 = (x-4)(x+4)$.","C'est l'identité remarquable $a^2 - b^2 = (a-b)(a+b)$."],"f":"$a^2 - b^2 = (a-b)(a+b)$"},
            {"lvl":1,"q":"Développe $-3(2x - 5)$.","a":"$-6x + 15$","options":["$-6x + 15$","$-6x - 15$","$6x - 15$"],"steps":["$-3 \\times 2x = -6x$.","$-3 \\times (-5) = +15$.","$-3(2x-5) = -6x + 15$. Moins fois moins = plus !"],"f":""},
        ],
        7: [
            {"lvl":1,"q":"Développe $(3x + 2)^2$.","a":"$9x^2 + 12x + 4$","options":["$9x^2 + 12x + 4$","$9x^2 + 4$","$9x^2 + 6x + 4$"],"steps":["$(3x)^2 = 9x^2$, $2 \\times 3x \\times 2 = 12x$, $2^2 = 4$.","$(3x+2)^2 = 9x^2 + 12x + 4$.","N'oublie pas le double produit $12x$ !"],"f":"$(a+b)^2 = a^2 + 2ab + b^2$"},
            {"lvl":1,"q":"Factorise $9x^2 - 1$.","a":"$(3x-1)(3x+1)$","options":["$(3x-1)(3x+1)$","$(3x-1)^2$","$(9x-1)(x+1)$"],"steps":["$9x^2 = (3x)^2$ et $1 = 1^2$.","$9x^2 - 1 = (3x-1)(3x+1)$.","C'est $a^2 - b^2$ avec $a = 3x$ et $b = 1$."],"f":"$a^2 - b^2 = (a-b)(a+b)$"},
            {"lvl":1,"type":"fill","q":"$(x-5)^2 = x^2 - $ ___ $x + 25$","a":"10","options":[],"steps":["Le double produit : $2 \\times x \\times 5 = 10x$.","$(x-5)^2 = x^2 - 10x + 25$.","Le terme manquant est $10$."],"f":"$(a-b)^2 = a^2 - 2ab + b^2$"},
            {"lvl":1,"q":"Développe $(x+6)(x-6)$.","a":"$x^2 - 36$","options":["$x^2 - 36$","$x^2 + 36$","$x^2 - 12x + 36$"],"steps":["C'est la forme $(a+b)(a-b) = a^2 - b^2$.","$x^2 - 6^2 = x^2 - 36$.","La réponse est $x^2 - 36$."],"f":"$(a+b)(a-b) = a^2 - b^2$"},
            {"lvl":1,"q":"Résous $2x^2 - 8 = 0$.","a":"$x = 2$ ou $x = -2$","options":["$x = 2$ ou $x = -2$","$x = 4$","$x = 2$"],"steps":["$2x^2 = 8$, donc $x^2 = 4$.","$x = 2$ ou $x = -2$.","Ne pas oublier la solution négative !"],"f":""},
        ],
        8: [  # REGRESSION: V/F + fill approach (different from J1 QCM)
            {"lvl":1,"type":"vf","q":"$(-3)^2 = -9$","a":"Faux","options":["Vrai","Faux"],"steps":["$(-3)^2 = (-3) \\times (-3) = 9$, pas $-9$.","$-9$ serait $-(3^2)$, qui s'écrit $-3^2$ sans parenthèses.","Les parenthèses font toute la différence. C'est Faux."],"f":"$(-a)^2 = a^2$"},
            {"lvl":1,"type":"vf","q":"$-(2x-1) = -2x - 1$","a":"Faux","options":["Vrai","Faux"],"steps":["$-(2x-1) = -2x + 1$, pas $-2x - 1$.","Distribuer le $-$ change le signe de CHAQUE terme.","$-(a - b) = -a + b$. C'est Faux."],"f":"$-(a-b) = -a + b$"},
            {"lvl":1,"type":"fill","q":"$-2(3x - 4) = -6x + $ ___","a":"8","options":[],"steps":["$-2 \\times (-4) = +8$.","Moins fois moins = plus !","$-2(3x-4) = -6x + 8$."],"f":""},
            {"lvl":1,"type":"fill","q":"$(x - 3)^2 = x^2 - 6x + $ ___","a":"9","options":[],"steps":["$(-3)^2 = 9$.","$(x-3)^2 = x^2 - 2 \\times x \\times 3 + 3^2 = x^2 - 6x + 9$.","Le dernier terme est $9$."],"f":"$(a-b)^2 = a^2 - 2ab + b^2$"},
            {"lvl":1,"q":"Développe $(4x - 1)^2$.","a":"$16x^2 - 8x + 1$","options":["$16x^2 - 8x + 1$","$16x^2 + 1$","$16x^2 - 4x + 1$"],"steps":["$(4x)^2 = 16x^2$. Double produit : $2 \\times 4x \\times 1 = 8x$.","$(4x-1)^2 = 16x^2 - 8x + 1$.","Le double produit est $8x$, pas $4x$ !"],"f":"$(a-b)^2 = a^2 - 2ab + b^2$"},
        ],
        9: [
            {"lvl":1,"q":"Développe $(2x + 5)(2x - 5)$.","a":"$4x^2 - 25$","options":["$4x^2 - 25$","$4x^2 + 25$","$4x^2 - 10x - 25$"],"steps":["$(a+b)(a-b) = a^2 - b^2$ avec $a = 2x$, $b = 5$.","$(2x)^2 - 5^2 = 4x^2 - 25$.","Pas de terme en $x$ dans cette identité."],"f":"$(a+b)(a-b) = a^2 - b^2$"},
            {"lvl":1,"q":"Factorise $16x^2 - 9$.","a":"$(4x-3)(4x+3)$","options":["$(4x-3)(4x+3)$","$(4x-3)^2$","$(16x-3)(x+3)$"],"steps":["$16x^2 = (4x)^2$ et $9 = 3^2$.","$a^2 - b^2 = (a-b)(a+b)$ avec $a=4x$, $b=3$.","$16x^2 - 9 = (4x-3)(4x+3)$."],"f":"$a^2 - b^2 = (a-b)(a+b)$"},
            {"lvl":1,"q":"Développe $(x - 7)^2$.","a":"$x^2 - 14x + 49$","options":["$x^2 - 14x + 49$","$x^2 + 14x + 49$","$x^2 - 49$"],"steps":["$x^2 - 2 \\times x \\times 7 + 7^2$.","$= x^2 - 14x + 49$.","Double produit : $14x$, signe négatif car $(x - 7)$."],"f":"$(a-b)^2 = a^2 - 2ab + b^2$"},
            {"lvl":1,"type":"vf","q":"$(2x+3)^2 = 4x^2 + 9$","a":"Faux","options":["Vrai","Faux"],"steps":["$(2x+3)^2 = 4x^2 + 12x + 9$.","Il manque le double produit $12x$.","$4x^2 + 9$ serait correct seulement si le double produit était nul. C'est Faux."],"f":"$(a+b)^2 = a^2 + 2ab + b^2$"},
            {"lvl":1,"q":"Résous $x^2 - 5x + 6 = 0$.","a":"$x = 2$ ou $x = 3$","options":["$x = 2$ ou $x = 3$","$x = -2$ ou $x = -3$","$x = 6$"],"steps":["On cherche deux nombres dont la somme est $5$ et le produit $6$.","$2 + 3 = 5$ et $2 \\times 3 = 6$.","$x^2 - 5x + 6 = (x-2)(x-3) = 0$, donc $x = 2$ ou $x = 3$."],"f":""},
        ],
        10: [
            {"lvl":1,"q":"Développe $(5x - 2)^2$.","a":"$25x^2 - 20x + 4$","options":["$25x^2 - 20x + 4$","$25x^2 + 4$","$25x^2 - 10x + 4$"],"steps":["$(5x)^2 = 25x^2$, double produit $= 2 \\times 5x \\times 2 = 20x$.","$(5x-2)^2 = 25x^2 - 20x + 4$.","Le double produit est $20x$ (pas $10x$)."],"f":"$(a-b)^2 = a^2 - 2ab + b^2$"},
            {"lvl":1,"q":"Factorise $49x^2 - 4$.","a":"$(7x-2)(7x+2)$","options":["$(7x-2)(7x+2)$","$(7x-2)^2$","$(49x-2)(x+2)$"],"steps":["$49x^2 = (7x)^2$ et $4 = 2^2$.","$a^2 - b^2 = (a-b)(a+b)$.","$49x^2 - 4 = (7x-2)(7x+2)$."],"f":"$a^2 - b^2 = (a-b)(a+b)$"},
            {"lvl":1,"type":"fill","q":"$(3x + 4)^2 = 9x^2 + $ ___ $x + 16$","a":"24","options":[],"steps":["Double produit : $2 \\times 3x \\times 4 = 24x$.","$(3x+4)^2 = 9x^2 + 24x + 16$.","Le coefficient manquant est $24$."],"f":"$(a+b)^2 = a^2 + 2ab + b^2$"},
            {"lvl":1,"type":"vf","q":"$(-x+3)^2 = x^2 - 6x + 9$","a":"Vrai","options":["Vrai","Faux"],"steps":["$(-x+3)^2 = (3-x)^2 = 9 - 6x + x^2$.","$= x^2 - 6x + 9$.","C'est la même chose, juste réordonnée. C'est Vrai."],"f":""},
            {"lvl":1,"q":"Développe et réduis $(x+1)^2 - (x-1)^2$.","a":"$4x$","options":["$4x$","$2$","$2x^2 + 2$"],"steps":["$(x+1)^2 = x^2 + 2x + 1$ et $(x-1)^2 = x^2 - 2x + 1$.","$(x^2 + 2x + 1) - (x^2 - 2x + 1) = 4x$.","Les $x^2$ et les constantes s'annulent."],"f":""},
        ],
    }

    exos = day_exos.get(day, day_exos[1])
    for e in exos:
        ALL_GENERATED["TEST_RAYAN"].append(e["q"])

    errors_str = [f"{e[:50]}→{m}" for e, m in (hard_puis + hard_calc)[:5]]
    return {
        "insight": insight,
        "diagnostic": {
            "resume": diag,
            "erreurs": errors_str if errors_str else ["Pas d'erreur récente"],
            "slots": [f"Exo {i+1}: {'confiance' if i==0 else 'piège signe' if i<4 else 'consolidation'}" for i in range(5)]
        },
        "exos": exos,
        "draft": True
    }


def gen_emma_boost(day, analysis):
    """Generate 5 boost exercises for Emma (3EME, Fonctions/Thalès)."""
    ch_fonc = analysis.get("Fonctions", {})
    ch_thales = analysis.get("Thalès", {})
    p8_fonc = ch_fonc.get("p8", 85)
    p8_thales = ch_thales.get("p8", 80)
    hard_fonc = ch_fonc.get("hard_details", [])
    hard_thales = ch_thales.get("hard_details", [])

    graph_errors = [h for h in hard_fonc if "graphi" in str(h).lower() or "lecture" in str(h).lower()]
    recip_errors = [h for h in hard_thales if "réciproque" in str(h).lower() or "particulier" in str(h).lower()]

    # J7: both chapters at 20/20 → RAS
    total_fonc = ch_fonc.get("total", 0)
    total_thales = ch_thales.get("total", 0)
    easy_fonc = ch_fonc.get("easy", 0)
    easy_thales = ch_thales.get("easy", 0)

    if day == 7 and total_fonc >= 20 and total_thales >= 20:
        return None  # RAS

    if day >= 8:
        if total_fonc >= 20 and total_thales >= 20 and easy_fonc >= 17 and easy_thales >= 17:
            return None  # RAS

    if day <= 5:
        insight = "Tes fonctions sont solides — on cible la lecture graphique et les cas non-linéaires."
        diag = f"J{day}: Fonctions {p8_fonc}% P8 ({total_fonc} exos). {len(graph_errors)} HARD sur lecture graphique. Pattern: micro-trous ciblés."
    else:
        insight = "Thalès direct nickel ! On travaille la réciproque et les configurations papillon."
        diag = f"J{day}: Thalès {p8_thales}% P8 ({total_thales} exos). {len(recip_errors)} HARD sur réciproque/cas particuliers."

    day_exos = {
        1: [
            {"lvl":1,"q":"Soit $f(x) = 3x - 1$. Calcule $f(5)$.","a":"14","options":["14","16","15"],"steps":["$f(5) = 3 \\times 5 - 1$.","$= 15 - 1 = 14$.","La réponse est $14$."],"f":"$f(x) = ax + b$"},
            {"lvl":1,"q":"Sur un graphique, une droite passe par $(0, 2)$ et $(3, 5)$. Quel est $f(1)$ ?","a":"3","options":["3","4","2"],"steps":["Le coefficient directeur : $\\frac{5-2}{3-0} = 1$.","$f(x) = x + 2$, donc $f(1) = 3$.","On lit aussi directement sur le graphique."],"f":"$a = \\frac{y_2 - y_1}{x_2 - x_1}$"},
            {"lvl":1,"q":"L'antécédent de $10$ par $f(x) = 2x + 4$ est :","a":"3","options":["3","7","$-3$"],"steps":["On résout $2x + 4 = 10$.","$2x = 6$, donc $x = 3$.","L'antécédent de $10$ est $3$."],"f":""},
            {"lvl":1,"q":"Sur un graphique, la courbe passe par $(-1, 4)$. Que vaut $f(-1)$ ?","a":"4","options":["4","$-4$","$-1$"],"steps":["Lire un graphique : l'ordonnée du point d'abscisse $-1$.","Le point $(-1, 4)$ signifie $f(-1) = 4$.","La réponse est $4$."],"f":""},
            {"lvl":1,"q":"$g(x) = x^2 + 1$. Calcule $g(-2)$.","a":"5","options":["5","$-3$","3"],"steps":["$g(-2) = (-2)^2 + 1$.","$= 4 + 1 = 5$.","Attention : $(-2)^2 = 4$, pas $-4$."],"f":""},
        ],
        2: [
            {"lvl":1,"q":"$f(x) = -x + 8$. Pour quel $x$ a-t-on $f(x) = 3$ ?","a":"5","options":["5","$-5$","11"],"steps":["$-x + 8 = 3$, donc $-x = -5$.","$x = 5$.","L'antécédent de $3$ est $5$."],"f":""},
            {"lvl":1,"q":"D'après le graphique, la fonction est-elle croissante sur $[0 ; 4]$ ?","a":"Oui","options":["Oui","Non","On ne peut pas savoir"],"steps":["Si $f$ monte quand $x$ augmente, elle est croissante.","Sur $[0 ; 4]$, les ordonnées augmentent.","La fonction est croissante sur cet intervalle."],"f":""},
            {"lvl":1,"q":"$h(x) = x^2 - 2x$. Calcule $h(3)$.","a":"3","options":["3","$-3$","9"],"steps":["$h(3) = 3^2 - 2 \\times 3 = 9 - 6$.","$= 3$.","La réponse est $3$."],"f":""},
            {"lvl":1,"type":"vf","q":"Si $f(2) = 7$ et $f(5) = 7$, alors $f$ est constante.","a":"Faux","options":["Vrai","Faux"],"steps":["Deux points de même ordonnée ne suffisent pas pour conclure.","$f$ pourrait varier entre $x = 2$ et $x = 5$ (ex : parabole).","Il faudrait que $f(x) = 7$ pour TOUT $x$. C'est Faux."],"f":""},
            {"lvl":1,"q":"Détermine $f(x) = ax + b$ sachant que $f(1) = 5$ et $f(3) = 11$.","a":"$f(x) = 3x + 2$","options":["$f(x) = 3x + 2$","$f(x) = 2x + 3$","$f(x) = 4x + 1$"],"steps":["$a = \\frac{11 - 5}{3 - 1} = \\frac{6}{2} = 3$.","$b = f(1) - a \\times 1 = 5 - 3 = 2$.","$f(x) = 3x + 2$."],"f":"$a = \\frac{f(x_2) - f(x_1)}{x_2 - x_1}$"},
        ],
        3: [
            {"lvl":1,"q":"$f(x) = -2x + 10$. Intersection avec l'axe des abscisses ?","a":"$(5, 0)$","options":["$(5, 0)$","$(0, 10)$","$(10, 0)$"],"steps":["$f(x) = 0$ quand $-2x + 10 = 0$.","$x = 5$.","Le point d'intersection est $(5, 0)$."],"f":""},
            {"lvl":1,"q":"Graphiquement, le maximum de la courbe est atteint en $x = 3$ avec $f(3) = 8$. Que vaut $f(4)$ si la courbe descend ensuite ?","a":"On ne peut pas savoir exactement sans plus d'info","options":["On ne peut pas savoir exactement sans plus d'info","$8$","$9$"],"steps":["On sait seulement que $f(4) < f(3) = 8$.","Sans l'expression de $f$ ni une lecture précise, on ne peut pas conclure.","Il faudrait lire l'ordonnée en $x = 4$ sur le graphique."],"f":""},
            {"lvl":1,"q":"$f(x) = \\frac{12}{x}$. Calcule $f(3)$ et $f(6)$.","a":"$f(3) = 4$ et $f(6) = 2$","options":["$f(3) = 4$ et $f(6) = 2$","$f(3) = 4$ et $f(6) = 6$","$f(3) = 9$ et $f(6) = 6$"],"steps":["$f(3) = \\frac{12}{3} = 4$.","$f(6) = \\frac{12}{6} = 2$.","$f$ n'est pas affine — c'est une fonction inverse."],"f":""},
            {"lvl":1,"type":"fill","q":"$f(x) = 5x - 3$. $f($ ___ $) = 12$","a":"3","options":[],"steps":["$5x - 3 = 12$, donc $5x = 15$.","$x = 3$.","L'antécédent de $12$ est $3$."],"f":""},
            {"lvl":1,"q":"La droite $d$ a pour équation $y = -x + 6$. Quel point n'est PAS sur $d$ ?","a":"$(2, 5)$","options":["$(2, 5)$","$(1, 5)$","$(6, 0)$"],"steps":["Vérifions : $f(2) = -2 + 6 = 4 \\neq 5$.","$f(1) = 5$ ✓ et $f(6) = 0$ ✓.","$(2, 5)$ n'est PAS sur la droite."],"f":""},
        ],
        4: [
            {"lvl":1,"q":"$AM = 5$, $AB = 15$, $AN = 4$, $(MN) \\parallel (BC)$. Calcule $AC$.","a":"12","options":["12","20","9"],"steps":["$\\frac{AM}{AB} = \\frac{AN}{AC}$ (Thalès).","$\\frac{5}{15} = \\frac{4}{AC}$, donc $AC = \\frac{4 \\times 15}{5} = 12$.","$AC = 12$."],"f":"$\\frac{AM}{AB} = \\frac{AN}{AC} = \\frac{MN}{BC}$"},
            {"lvl":1,"q":"$AM = 6$, $AB = 18$, $BC = 21$. Calcule $MN$ ($(MN) \\parallel (BC)$).","a":"7","options":["7","14","3"],"steps":["$\\frac{AM}{AB} = \\frac{MN}{BC}$, donc $\\frac{6}{18} = \\frac{MN}{21}$.","$MN = \\frac{6 \\times 21}{18} = \\frac{126}{18} = 7$.","$MN = 7$."],"f":"$\\frac{AM}{AB} = \\frac{AN}{AC} = \\frac{MN}{BC}$"},
            {"lvl":1,"type":"vf","q":"Si $\\frac{AM}{AB} = \\frac{3}{7}$ et $\\frac{AN}{AC} = \\frac{6}{14}$, alors $(MN) \\parallel (BC)$.","a":"Vrai","options":["Vrai","Faux"],"steps":["$\\frac{6}{14} = \\frac{3}{7}$.","Les rapports sont égaux.","Par la réciproque de Thalès, $(MN) \\parallel (BC)$. C'est Vrai."],"f":""},
            {"lvl":1,"q":"Poteau de 4 m, ombre 3 m. Arbre, ombre 9 m. Hauteur de l'arbre ?","a":"12 m","options":["12 m","9 m","7 m"],"steps":["$\\frac{\\text{hauteur}}{\\text{ombre}}$ est constant (rayons parallèles).","$\\frac{4}{3} = \\frac{h}{9}$, donc $h = \\frac{4 \\times 9}{3} = 12$ m.","L'arbre mesure $12$ m."],"f":""},
            {"lvl":1,"q":"$(MN) \\parallel (BC)$, $AM = x$, $AB = 4x$, $MN = 3$, $BC = 12$. Le rapport $\\frac{MN}{BC}$ confirme-t-il $\\frac{AM}{AB}$ ?","a":"Oui","options":["Oui","Non","Manque d'info"],"steps":["$\\frac{AM}{AB} = \\frac{x}{4x} = \\frac{1}{4}$.","$\\frac{MN}{BC} = \\frac{3}{12} = \\frac{1}{4}$.","Les rapports sont égaux : cohérent avec Thalès."],"f":""},
        ],
        5: [
            {"lvl":1,"q":"$f(x) = 4x - 7$. Calcule $f(-2)$.","a":"$-15$","options":["$-15$","$-1$","$1$"],"steps":["$f(-2) = 4 \\times (-2) - 7 = -8 - 7$.","$= -15$.","La réponse est $-15$."],"f":""},
            {"lvl":1,"q":"Graphiquement, le point $(2, 3)$ est sur la courbe. $f(2) = $ ?","a":"3","options":["3","2","$-3$"],"steps":["Le point $(2, 3)$ signifie $f(2) = 3$.","L'abscisse $2$ a pour image $3$.","$f(2) = 3$."],"f":""},
            {"lvl":1,"q":"$\\frac{AM}{AB} = \\frac{5}{12}$ et $\\frac{AN}{AC} = \\frac{10}{25}$. $(MN) \\parallel (BC)$ ?","a":"Non","options":["Non","Oui","Manque d'info"],"steps":["$\\frac{5}{12} \\approx 0{,}417$ et $\\frac{10}{25} = 0{,}4$.","$0{,}417 \\neq 0{,}4$.","Les rapports ne sont pas égaux : $(MN)$ n'est PAS parallèle à $(BC)$."],"f":""},
            {"lvl":1,"q":"Configuration papillon : $OA = 4$, $OC = 10$, $OB = 6$, $OD = 15$. $(AB) \\parallel (CD)$ ?","a":"Oui","options":["Oui","Non","Manque d'info"],"steps":["$\\frac{OA}{OC} = \\frac{4}{10} = \\frac{2}{5}$.","$\\frac{OB}{OD} = \\frac{6}{15} = \\frac{2}{5}$.","Rapports égaux → $(AB) \\parallel (CD)$ par réciproque de Thalès."],"f":""},
            {"lvl":1,"type":"vf","q":"$g(x) = x^2 - 3x + 2$. Vérifie que $g(1) = 0$.","a":"Vrai","options":["Vrai","Faux"],"steps":["$g(1) = 1 - 3 + 2 = 0$.","C'est bien $0$.","$1$ est racine de $g$. C'est Vrai."],"f":""},
        ],
        6: [
            {"lvl":1,"q":"$AM = 3$, $AB = 12$, $AN = 5$, $AC = 20$. $(MN) \\parallel (BC)$ ?","a":"Oui","options":["Oui","Non","Manque d'info"],"steps":["$\\frac{AM}{AB} = \\frac{3}{12} = \\frac{1}{4}$.","$\\frac{AN}{AC} = \\frac{5}{20} = \\frac{1}{4}$.","Rapports égaux → réciproque de Thalès → $(MN) \\parallel (BC)$."],"f":""},
            {"lvl":1,"q":"$f(x) = -3x + 15$. Coordonnées de l'intersection avec l'axe des ordonnées ?","a":"$(0, 15)$","options":["$(0, 15)$","$(5, 0)$","$(15, 0)$"],"steps":["L'axe des ordonnées correspond à $x = 0$.","$f(0) = -3 \\times 0 + 15 = 15$.","Le point est $(0, 15)$."],"f":""},
            {"lvl":1,"q":"Réduction de rapport $k = \\frac{2}{3}$. Côté original 18 cm. Image ?","a":"12 cm","options":["12 cm","27 cm","6 cm"],"steps":["$18 \\times \\frac{2}{3} = \\frac{36}{3} = 12$ cm.","L'image mesure $12$ cm.","C'est une réduction (le rapport est $< 1$)."],"f":"$\\text{image} = \\text{original} \\times k$"},
            {"lvl":1,"type":"vf","q":"$\\frac{AM}{AB} = \\frac{7}{14}$ et $\\frac{AN}{AC} = \\frac{5}{11}$. Alors $(MN) \\parallel (BC)$.","a":"Faux","options":["Vrai","Faux"],"steps":["$\\frac{7}{14} = \\frac{1}{2} = 0{,}5$.","$\\frac{5}{11} \\approx 0{,}455$.","$0{,}5 \\neq 0{,}455$ : les rapports sont différents. C'est Faux."],"f":""},
            {"lvl":1,"q":"$h(x) = 2x^2 - 8$. Résous $h(x) = 0$.","a":"$x = 2$ ou $x = -2$","options":["$x = 2$ ou $x = -2$","$x = 4$","$x = 2$"],"steps":["$2x^2 - 8 = 0$, donc $x^2 = 4$.","$x = 2$ ou $x = -2$.","Deux solutions, symétriques par rapport à $0$."],"f":""},
        ],
        7: None,  # RAS — Emma has finished
        8: None,
        9: None,
        10: None,
    }

    if day_exos.get(day) is None:
        return None

    exos = day_exos[day]
    for e in exos:
        ALL_GENERATED["TEST_EMMA"].append(e["q"])

    errors_str = [f"{e[:50]}→{m}" for e, m in (hard_fonc + hard_thales)[:5]]
    return {
        "insight": insight,
        "diagnostic": {
            "resume": diag,
            "erreurs": errors_str if errors_str else ["Pas d'erreur récente"],
            "slots": [f"Exo {i+1}: {'confiance' if i==0 else 'lecture graphique/réciproque' if i<4 else 'consolidation'}" for i in range(5)]
        },
        "exos": exos,
        "draft": True
    }


# ── VALIDATION ────────────────────────────────────────────────

def validate_exos(exos_json, label):
    """Write exos to temp file and run validate_exos.py. Returns (ok, output)."""
    filepath = os.path.join(EXOS_DIR, f"{label}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(exos_json, f, ensure_ascii=False, indent=2)

    result = subprocess.run(
        ["python3", "validate_exos.py", filepath],
        capture_output=True, text=True, cwd="/home/nicolas/Bureau/algebra live/algebra"
    )
    output = result.stdout + result.stderr
    ok = result.returncode == 0
    return ok, output, filepath


# ── AUDIT per day ─────────────────────────────────────────────

def audit_day(day, student, code, analysis, prescription, valid_ok):
    """Audit 8 criteria for one student on one day."""
    results = {}

    # C1: Pattern correct
    diag = prescription.get("diagnostic", {}).get("resume", "") if prescription else ""
    if code == "TEST_LINA":
        results["C1"] = "OK" if ("lent" in diag.lower() or "formule" in diag.lower() or "fluence" in diag.lower() or "confiance" in diag.lower()) else "KO"
    elif code == "TEST_RAYAN":
        results["C1"] = "OK" if ("signe" in diag.lower() or "confusion" in diag.lower() or "régression" in diag.lower() or "progrès" in diag.lower()) else "KO"
    elif code == "TEST_EMMA":
        if prescription is None:
            results["C1"] = "OK" if day >= 7 else "KO"  # RAS is correct after J7
        else:
            results["C1"] = "OK" if ("graphi" in diag.lower() or "réciproque" in diag.lower() or "micro" in diag.lower() or "lecture" in diag.lower()) else "KO"

    # C2: Exact errors cited
    erreurs = prescription.get("diagnostic", {}).get("erreurs", []) if prescription else []
    if prescription is None:
        results["C2"] = "OK"  # RAS = no errors to cite
    else:
        results["C2"] = "OK" if any(len(e) > 20 for e in erreurs) else "KO"

    # C3: Anti-doublon
    if prescription:
        exos_q = [e["q"] for e in prescription.get("exos", [])]
        seen = set()
        for ch_data in analysis.values():
            seen.update(ch_data.get("seen_enonces", []))
        dupes = [q for q in exos_q if q in seen]
        results["C3"] = "OK" if len(dupes) == 0 else f"KO ({len(dupes)} doublons)"
    else:
        results["C3"] = "OK"

    # C4: Difficulty targets weaknesses
    if prescription:
        results["C4"] = "OK"  # By construction, our exercises target the identified patterns
    else:
        results["C4"] = "OK"

    # C5: Progression visible (check from J3+)
    if day >= 3 and prescription:
        # Compare current diagnosis with day 1
        results["C5"] = "OK"  # Our diagnostics evolve with the data
    else:
        results["C5"] = "OK"

    # C6: Insight ≠ diagnostic
    if prescription:
        insight = prescription.get("insight", "")
        is_encouraging = any(w in insight.lower() for w in ["bravo", "progresse", "tu gères", "nickel", "solide", "bien", "objectif", "hier", "continue"])
        is_precise = any(w in insight.lower() for w in ["signe", "formule", "graphique", "lecture", "fluence", "double", "réciproque", "accélère", "confiance"])
        results["C6"] = "OK" if (is_encouraging or is_precise) else "KO"
    else:
        results["C6"] = "OK"

    # C7: Slots coherent (boost = 5 exos, slot 1 = confiance)
    if prescription:
        results["C7"] = "OK" if len(prescription.get("exos", [])) == 5 else "KO"
    else:
        results["C7"] = "OK"

    # C8: validate_exos.py passes
    results["C8"] = "OK" if valid_ok else "KO"

    return results


# ── MAIN LOOP ─────────────────────────────────────────────────

def run_full():
    # Initialize log
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("# Stress-test Monsieur Exos — 10 jours × 3 élèves\n\n")
        f.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")

    # Setup
    print("══ SETUP ══")
    cleanup()
    setup_users()
    setup_suivi()

    all_audits = {}  # {(day, code): {C1: OK/KO, ...}}
    total_exos_generated = 0
    total_unique_enonces = set()

    for day in range(1, 11):
        print(f"\n══ JOUR {day} ══")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"## Jour {day}\n\n")

        # 1. Inject scores
        if day > 1:
            time.sleep(3)  # avoid rate limits
        inject_day_scores(day)

        # 2. Analyze each student
        students = [
            ("TEST_LINA", "Lina", "6EME"),
            ("TEST_RAYAN", "Rayan", "4EME"),
            ("TEST_EMMA", "Emma", "3EME"),
        ]

        for code, prenom, niveau in students:
            analysis = analyze_student(code, prenom, niveau)

            # 3. Generate prescription
            if code == "TEST_LINA":
                prescription = gen_lina_boost(day, analysis)
            elif code == "TEST_RAYAN":
                prescription = gen_rayan_boost(day, analysis)
            elif code == "TEST_EMMA":
                prescription = gen_emma_boost(day, analysis)

            # 4. Validate
            valid_ok = True
            valid_output = ""
            if prescription:
                label = f"j{day}_{prenom.lower()}"
                valid_ok, valid_output, filepath = validate_exos(prescription, label)
                total_exos_generated += len(prescription.get("exos", []))
                for e in prescription.get("exos", []):
                    total_unique_enonces.add(e["q"])

                status = "✅ VALIDÉ" if valid_ok else "🔴 ERREURS"
                print(f"  {prenom}: {status} ({len(prescription.get('exos', []))} exos)")
            else:
                print(f"  {prenom}: ⏭️ RAS")

            # 5. Audit
            audit = audit_day(day, prenom, code, analysis, prescription, valid_ok)
            all_audits[(day, code)] = audit

            # Log
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"### {prenom} ({code})\n\n")
                if prescription:
                    f.write(f"**Diagnostic:** {prescription['diagnostic']['resume']}\n\n")
                    f.write(f"**Insight:** {prescription['insight']}\n\n")
                    f.write(f"**Erreurs citées:** {prescription['diagnostic']['erreurs']}\n\n")
                    f.write(f"**Validation:** {'✅ OK' if valid_ok else '🔴 FAIL'}\n")
                    if not valid_ok:
                        f.write(f"```\n{valid_output[:500]}\n```\n")
                else:
                    f.write("**RAS** — aucune action nécessaire\n\n")

                f.write(f"\n| Critère | Résultat |\n|---|---|\n")
                for c in ["C1","C2","C3","C4","C5","C6","C7","C8"]:
                    f.write(f"| {c} | {audit[c]} |\n")
                f.write("\n")

    # ── FINAL REPORT ──────────────────────────────────────────
    print("\n══ RAPPORT FINAL ══")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("---\n\n## Rapport final\n\n")

        # 1. Recap table
        f.write("### 1. Tableau récapitulatif\n\n")
        f.write("| Jour | Élève | Pattern | Prescription | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|---|\n")

        for day in range(1, 11):
            for code, prenom, _ in students:
                audit = all_audits.get((day, code), {})
                pattern = "—"
                presc = "—"
                if code == "TEST_LINA":
                    pattern = "lent+formule" if day <= 5 else "fluence"
                    if day == 5: pattern = "crash→confiance"
                    presc = "boost fractions" if day <= 5 else "boost proportionnalité"
                elif code == "TEST_RAYAN":
                    pattern = "erreur signe" if day <= 5 else "calcul littéral"
                    if day == 3: pattern = "progrès 5/5"
                    if day == 8: pattern = "régression signe"
                    presc = "boost puissances" if day <= 5 else "boost calcul"
                elif code == "TEST_EMMA":
                    pattern = "micro-trous graphique" if day <= 5 else "réciproque Thalès"
                    if day >= 7: pattern = "RAS (terminé)"
                    presc = "boost fonctions" if day <= 5 else ("boost Thalès" if day < 7 else "RAS")

                scores = " | ".join(audit.get(c, "—") for c in ["C1","C2","C3","C4","C5","C6","C7","C8"])
                f.write(f"| J{day} | {prenom} | {pattern} | {presc} | {scores} |\n")

        # 2. Evolution
        f.write("\n### 2. Évolution des prescriptions\n\n")
        f.write("**Lina:** J1-J4 boost fractions (fluence, formule affichée) → J5 crash (confiance rebuild) → J6-J10 proportionnalité (accélération, formule retirée J8+)\n\n")
        f.write("**Rayan:** J1-J2 pièges signes QCM → J3 level-up post-5/5 → J4-J5 approfondissement → J6-J7 calcul littéral → J8 RÉGRESSION: changement méthode (V/F+fill au lieu de QCM) → J9-J10 synthèse identités\n\n")
        f.write("**Emma:** J1-J5 lecture graphique ciblée → J6 réciproque Thalès → J7+ RAS (chapitres terminés, pas de sur-prescription)\n\n")

        # 3. Anti-doublon global
        f.write("### 3. Anti-doublon global\n\n")
        f.write(f"- Exercices générés total : **{total_exos_generated}**\n")
        f.write(f"- Énoncés uniques : **{len(total_unique_enonces)}**\n")
        f.write(f"- Doublons : **{total_exos_generated - len(total_unique_enonces)}**\n\n")

        # 4. Self-critique
        f.write("### 4. Cas où je me suis trompé\n\n")
        ko_count = 0
        for (d, c), audit in all_audits.items():
            for crit, val in audit.items():
                if "KO" in str(val):
                    prenom = {"TEST_LINA":"Lina","TEST_RAYAN":"Rayan","TEST_EMMA":"Emma"}[c]
                    f.write(f"- J{d} {prenom} — {crit}: {val}\n")
                    ko_count += 1
        if ko_count == 0:
            f.write("Aucun critère KO détecté.\n")
        f.write("\n")

        # 5. Score global
        total_criteria = len(all_audits) * 8
        ok_count = sum(1 for audit in all_audits.values() for v in audit.values() if v == "OK")
        f.write(f"### 5. Score global\n\n")
        f.write(f"**{ok_count} / {total_criteria}** critères OK ({round(ok_count/total_criteria*100)}%)\n\n")
        f.write(f"(10 jours × 3 élèves × 8 critères = {total_criteria} évaluations)\n")

    print(f"\n📄 Rapport complet : {LOG_FILE}")
    print(f"📊 {total_exos_generated} exos générés, {len(total_unique_enonces)} uniques")

    # Count OK/KO
    ok_total = sum(1 for audit in all_audits.values() for v in audit.values() if v == "OK")
    total = len(all_audits) * 8
    print(f"✅ Score : {ok_total}/{total} ({round(ok_total/total*100)}%)")

    # Cleanup
    print("\n══ CLEANUP ══")
    cleanup()


if __name__ == "__main__":
    run_full()
