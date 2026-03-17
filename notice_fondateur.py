#!/usr/bin/env python3
"""
Génère la Notice Fondateur Matheux en PDF (WeasyPrint)
et l'envoie par email via SMTP Ionos.
"""

import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from weasyprint import HTML
from datetime import datetime

PDF_PATH = "/home/nicolas/Bureau/algebra live/algebra/notice_fondateur.pdf"

# ── Contenu HTML ──────────────────────────────────────────────────────────

HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Syne:wght@700;800&display=swap');

  :root {
    --emerald: #10b981;
    --emerald-dark: #059669;
    --slate-900: #0f172a;
    --slate-700: #334155;
    --slate-500: #64748b;
    --slate-200: #e2e8f0;
    --amber-500: #f59e0b;
    --red-500: #ef4444;
    --blue-500: #3b82f6;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'DM Sans', sans-serif;
    color: var(--slate-900);
    line-height: 1.6;
    padding: 40px 50px;
    font-size: 11pt;
  }

  /* ── Header ── */
  .header {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 25px;
    border-bottom: 3px solid var(--emerald);
  }
  .header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 28pt;
    font-weight: 800;
    color: var(--slate-900);
    margin-bottom: 4px;
    letter-spacing: -0.5px;
  }
  .header h1 span { color: var(--emerald); }
  .header .subtitle {
    font-size: 13pt;
    color: var(--slate-500);
    font-weight: 500;
  }
  .header .date {
    margin-top: 10px;
    font-size: 10pt;
    color: var(--slate-500);
    background: #f1f5f9;
    display: inline-block;
    padding: 4px 16px;
    border-radius: 20px;
  }

  /* ── Sections ── */
  h2 {
    font-family: 'Syne', sans-serif;
    font-size: 15pt;
    font-weight: 700;
    color: var(--emerald-dark);
    margin: 28px 0 12px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid var(--slate-200);
  }
  h3 {
    font-size: 11pt;
    font-weight: 700;
    color: var(--slate-700);
    margin: 16px 0 8px 0;
  }

  /* ── Tables ── */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 16px 0;
    font-size: 10pt;
  }
  th {
    background: var(--slate-900);
    color: white;
    text-align: left;
    padding: 8px 12px;
    font-weight: 600;
  }
  td {
    padding: 7px 12px;
    border-bottom: 1px solid var(--slate-200);
  }
  tr:nth-child(even) td { background: #f8fafc; }

  /* ── Badges ── */
  .badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 9pt;
    font-weight: 600;
  }
  .badge-green { background: #d1fae5; color: #065f46; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-red { background: #fee2e2; color: #991b1b; }
  .badge-blue { background: #dbeafe; color: #1e40af; }

  /* ── Stats cards ── */
  .stats {
    display: flex;
    gap: 12px;
    margin: 16px 0;
  }
  .stat-card {
    flex: 1;
    background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
    border: 1px solid #bbf7d0;
    border-radius: 12px;
    padding: 14px;
    text-align: center;
  }
  .stat-card .number {
    font-family: 'Syne', sans-serif;
    font-size: 22pt;
    font-weight: 800;
    color: var(--emerald-dark);
  }
  .stat-card .label {
    font-size: 9pt;
    color: var(--slate-500);
    margin-top: 2px;
  }

  /* ── Checklist ── */
  .check { color: var(--emerald); font-weight: 700; }
  .pending { color: var(--amber-500); font-weight: 700; }
  .blocked { color: var(--red-500); font-weight: 700; }

  ul { margin: 6px 0 6px 20px; }
  li { margin: 3px 0; }

  /* ── Footer ── */
  .footer {
    margin-top: 35px;
    padding-top: 15px;
    border-top: 2px solid var(--slate-200);
    text-align: center;
    font-size: 9pt;
    color: var(--slate-500);
  }

  /* ── Callout ── */
  .callout {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border-left: 4px solid var(--blue-500);
    padding: 14px 18px;
    border-radius: 0 10px 10px 0;
    margin: 16px 0;
    font-size: 10.5pt;
  }
  .callout strong { color: var(--blue-500); }

  .callout-amber {
    background: linear-gradient(135deg, #fffbeb, #fef3c7);
    border-left: 4px solid var(--amber-500);
  }
  .callout-amber strong { color: #b45309; }

  p { margin: 6px 0; }

  @page {
    size: A4;
    margin: 15mm 15mm 20mm 15mm;
    @bottom-center {
      content: "Matheux — Notice Fondateur — Page " counter(page) " / " counter(pages);
      font-size: 8pt;
      color: #94a3b8;
    }
  }
</style>
</head>
<body>

<!-- ═══════════════════════ HEADER ═══════════════════════ -->
<div class="header">
  <h1>matheux<span>.fr</span></h1>
  <div class="subtitle">Notice Fondateur — État du projet</div>
  <div class="date">Lundi 16 mars 2026 — Lancement J-2</div>
</div>

<!-- ═══════════════════════ CHIFFRES CLÉS ═══════════════════════ -->
<div class="stats">
  <div class="stat-card">
    <div class="number">1 872</div>
    <div class="label">exercices (score qualité ~98%)</div>
  </div>
  <div class="stat-card">
    <div class="number">54</div>
    <div class="label">chapitres (6e→3e + 1re Spé)</div>
  </div>
  <div class="stat-card">
    <div class="number">74/74</div>
    <div class="label">tests automatisés PASS</div>
  </div>
  <div class="stat-card">
    <div class="number">19,99€</div>
    <div class="label">/mois — Stripe PROD actif</div>
  </div>
</div>

<!-- ═══════════════════════ PROJET ═══════════════════════ -->
<h2>1. Le projet en bref</h2>
<p><strong>Matheux</strong> est un outil de soutien scolaire en maths adaptatif, de la 6e à la 3e + 1re Spé Maths. L'app détecte les lacunes de l'élève via un diagnostic, puis prépare des exercices personnalisés chaque jour.</p>
<p><strong>Fondateur :</strong> Nicolas Follezou, prof de maths — ancien chef de projet Aérospatiale.<br>
<strong>Positionnement :</strong> "Un prof de maths derrière, pas juste un algorithme." — 19,99€/mois, 25× moins cher qu'un cours particulier.<br>
<strong>Objectif lancement :</strong> 50 clients payants = ~1 000€ MRR.</p>

<!-- ═══════════════════════ STACK ═══════════════════════ -->
<h2>2. Architecture technique</h2>
<table>
  <tr><th>Composant</th><th>Techno</th><th>Détail</th></tr>
  <tr><td>Frontend</td><td>HTML + CSS + JS vanilla</td><td>SPA ~9 900 lignes — GitHub Pages (matheux.fr)</td></tr>
  <tr><td>Backend</td><td>Google Apps Script (V8)</td><td>~5 300 lignes — 30 actions API via doPost</td></tr>
  <tr><td>Base de données</td><td>Google Sheets</td><td>13 onglets — ~20 users simultanés max</td></tr>
  <tr><td>Paiement</td><td>Stripe PROD</td><td>19,99€/mois — webhook + premium guard déployés</td></tr>
  <tr><td>Emails</td><td>GmailApp + Ionos SMTP</td><td>no-reply@, contact@, nicolas@matheux.fr</td></tr>
  <tr><td>Analytics</td><td>GA4</td><td>RGPD-compliant, consentement explicite</td></tr>
</table>

<!-- ═══════════════════════ CONTENU PÉDA ═══════════════════════ -->
<h2>3. Contenu pédagogique</h2>
<table>
  <tr><th>Type</th><th>Volume</th><th>Détail</th></tr>
  <tr><td>Curriculum</td><td>1 080 exercices</td><td>54 chapitres × 20 — programme officiel ~100%</td></tr>
  <tr><td>Diagnostic</td><td>108 exercices</td><td>54 chapitres × 2 — détection lacunes</td></tr>
  <tr><td>Boost quotidien</td><td>540 exercices</td><td>54 chapitres × 10 — entraînement ciblé</td></tr>
  <tr><td>Brevet blanc</td><td>144 exercices</td><td>15 chapitres 3e — format épreuve</td></tr>
</table>
<p><strong>Niveaux couverts :</strong> 6e, 5e, 4e, 3e (collège complet) + 1re Spé Maths (10 chapitres expérimentaux).<br>
<strong>Audit qualité :</strong> 1 872 exercices audités le 15 mars — score ~98%. Notation française, indices progressifs, doublons corrigés.</p>

<!-- ═══════════════════════ FONCTIONNALITÉS ═══════════════════════ -->
<h2>4. Fonctionnalités clés</h2>

<h3>Côté élève</h3>
<ul>
  <li><strong>Boost du jour</strong> — 5 exercices ciblés, ~10 min/jour</li>
  <li><strong>Chapitres libres</strong> — accessibles en permanence après le boost</li>
  <li><strong>Brevet blanc</strong> (3e) — quiz sans indices, résultats détaillés, mentions</li>
  <li><strong>Mode révision</strong> — chapitres d'une autre année assignés par l'admin</li>
  <li><strong>Figures géo SVG</strong> — 18 types auto-détectés depuis l'énoncé</li>
  <li><strong>Brouillon + Calculette</strong> — contextuel par chapitre/niveau</li>
  <li><strong>Gamification</strong> — XP, streak, confettis, mastery ring, mode nuit</li>
  <li><strong>Bouton "j'ai pas compris"</strong> — profil cognitif dans la fiche admin</li>
  <li><strong>Types d'exercices</strong> — QCM, Vrai/Faux, trous à compléter</li>
</ul>

<h3>Côté admin (Nicolas)</h3>
<ul>
  <li><strong>Cockpit 3 onglets</strong> — À FAIRE / FAIT / TEST — cartes élèves triées par urgence</li>
  <li><strong>Publish 1-clic</strong> — boost, chapitre, brevet blanc depuis la fiche élève</li>
  <li><strong>Emails marketing</strong> — J+0 auto, J+3/J+5/J+7 manuels (templates éditables)</li>
  <li><strong>Rapport parent hebdo</strong> — stats réelles, mot adapté au score</li>
  <li><strong>Feedbacks élève</strong> — signalements, ressenti, incompréhensions</li>
  <li><strong>Checklist quotidienne</strong> — items auto-cochés à chaque action</li>
</ul>

<h3>Côté parent</h3>
<ul>
  <li><strong>Email J+0</strong> — bienvenue automatique, ton prof humain</li>
  <li><strong>7 jours gratuits</strong> — accès complet sans carte bancaire</li>
  <li><strong>Formulaire contact</strong> — accessible depuis le footer</li>
</ul>

<!-- ═══════════════════════ SÉCURITÉ & JURIDIQUE ═══════════════════════ -->
<h2>5. Sécurité & Juridique</h2>
<table>
  <tr><th>Élément</th><th>État</th></tr>
  <tr><td>RGPD renforcé mineurs</td><td><span class="badge badge-green">✅ Complet</span></td></tr>
  <tr><td>Consentement parental obligatoire</td><td><span class="badge badge-green">✅ Formulaire</span></td></tr>
  <tr><td>5 pages légales (mentions, CGU, CGV, confidentialité, cookies)</td><td><span class="badge badge-green">✅ En ligne</span></td></tr>
  <tr><td>TVA art. 293 B CGI (exonéré)</td><td><span class="badge badge-green">✅ CGV</span></td></tr>
  <tr><td>Hash MDP client SHA-256 (salted)</td><td><span class="badge badge-green">✅ Actif</span></td></tr>
  <tr><td>Rate limiting GAS (60/min global, 15/min sensibles)</td><td><span class="badge badge-green">✅ Actif</span></td></tr>
  <tr><td>Stripe webhook MAXIMAL PARANOID + Premium Guard</td><td><span class="badge badge-green">✅ Déployé @85</span></td></tr>
  <tr><td>GA4 conditionné au consentement cookies</td><td><span class="badge badge-green">✅ Actif</span></td></tr>
</table>

<!-- ═══════════════════════ BILAN 16 MARS ═══════════════════════ -->
<h2>6. Bilan lundi 16 mars — 12 actions terminées</h2>

<table>
  <tr><th>#</th><th>Action</th><th>Statut</th></tr>
  <tr><td>1</td><td>Stripe TEST → PROD (19,99€/mois, limite 50)</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>2</td><td>3 boîtes mail Ionos (contact@, no-reply@, nicolas@)</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>3</td><td>Alias Gmail no-reply@ (SMTP Ionos port 465 SSL)</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>4</td><td>Sécurité Stripe déployée — webhook + premium guard</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>5</td><td>TVA art. 293 B CGI dans CGV</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>6</td><td>Formulaire contact (3 footers + toast)</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>7</td><td>Merge sécurité freelance → main + GitHub Pages</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>8</td><td>Tests emails (J+0, reset MDP, contact) tous OK</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>9</td><td>Stripe config (CGV + confidentialité + TVA off + limite 50)</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>10</td><td>Bandeau rappel limite Stripe admin</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>11</td><td>Nettoyage base (SIM01-SIM12 supprimés)</td><td><span class="badge badge-green">✅</span></td></tr>
  <tr><td>12</td><td>Test élève 6e ✅ / 5e ✅ / 4e ✅ — 15 frictions notées</td><td><span class="badge badge-green">✅</span></td></tr>
</table>

<!-- ═══════════════════════ MARDI 17 ═══════════════════════ -->
<h2>7. Mardi 17 mars matin — Plan d'action</h2>

<div class="callout-amber callout">
  <strong>Priorité absolue :</strong> Finir test 3e + fixer les 15 frictions élève avant le lancement.
</div>

<table>
  <tr><th>#</th><th>Action</th><th>Statut</th></tr>
  <tr><td>1</td><td><strong>Test élève 3EME</strong> — dernier niveau à tester</td><td><span class="badge badge-amber">⏳ Mardi matin</span></td></tr>
  <tr><td>2</td><td><strong>Fix 15 frictions</strong> — mode nuit, LaTeX×3, messages×3, boost×2, chapitre×4, scroll, bouton "j'ai pas compris" + frictions 3e</td><td><span class="badge badge-amber">⏳ Mardi</span></td></tr>
  <tr><td>3</td><td>Test admin workflow en conditions réelles</td><td><span class="badge badge-amber">⏳ Mardi</span></td></tr>
  <tr><td>4</td><td>Test parent parcours complet</td><td><span class="badge badge-amber">⏳ Mardi</span></td></tr>
  <tr><td>5</td><td>Landing page — relecture parent, wording final</td><td><span class="badge badge-amber">⏳ Mardi</span></td></tr>
</table>

<!-- ═══════════════════════ AVANT/APRÈS LANCEMENT ═══════════════════════ -->
<h2>8. Avant / après lancement</h2>
<table>
  <tr><th>Action</th><th>Deadline</th><th>Priorité</th></tr>
  <tr><td>Endpoint webhook Stripe (URL GAS + whsec_)</td><td>Avant J+7</td><td><span class="badge badge-red">⛔ Critique</span></td></tr>
  <tr><td>Vrai paiement CB test (19,99€ → Premium=1)</td><td>Avant J+7</td><td><span class="badge badge-red">⛔ Critique</span></td></tr>
  <tr><td>Triggers Apps Script (emails auto J+3/J+5/J+7)</td><td>Dès 10 clients</td><td><span class="badge badge-amber">🟡 Plus tard</span></td></tr>
  <tr><td>Centraliser 3 mails matheux.fr</td><td>Jeudi 19 mars</td><td><span class="badge badge-blue">🔵 Confort</span></td></tr>
</table>

<!-- ═══════════════════════ MERCREDI LANCEMENT ═══════════════════════ -->
<h2>9. Mercredi 18 mars — Jour J</h2>
<div class="callout">
  <strong>Lancement confirmé : mercredi 18 mars 2026 à 9h.</strong><br>
  La page teasing bascule automatiquement vers la vraie landing à 9h (heure de Paris).
</div>
<ul>
  <li>Vérifier DNS + HTTPS sur matheux.fr</li>
  <li>GA4 reçoit des events (mode debug Chrome)</li>
  <li>Admin HMD493 accessible (triple-clic logo)</li>
  <li>Publier un boost test → visible élève</li>
  <li>Annonce sur les réseaux</li>
</ul>

<!-- ═══════════════════════ EMAILS ═══════════════════════ -->
<h2>10. Architecture emails</h2>
<table>
  <tr><th>Email</th><th>Mode</th><th>Expéditeur</th></tr>
  <tr><td>J+0 bienvenue</td><td><span class="badge badge-green">✅ Auto</span></td><td>no-reply@matheux.fr</td></tr>
  <tr><td>Reset mot de passe</td><td><span class="badge badge-green">✅ Auto</span></td><td>no-reply@matheux.fr</td></tr>
  <tr><td>Formulaire contact</td><td><span class="badge badge-green">✅ Auto</span></td><td>no-reply@matheux.fr</td></tr>
  <tr><td>J+3 / J+5 / J+7 marketing</td><td><span class="badge badge-amber">Manuel admin</span></td><td>—</td></tr>
  <tr><td>Rapport parent hebdo</td><td><span class="badge badge-amber">Manuel admin</span></td><td>—</td></tr>
</table>

<!-- ═══════════════════════ SCALE ═══════════════════════ -->
<h2>11. Roadmap après lancement</h2>
<table>
  <tr><th>Seuil</th><th>Action</th></tr>
  <tr><td>10 clients</td><td>Activer triggers emails auto (J+3/J+5/J+7)</td></tr>
  <tr><td>15 clients</td><td>Analyser colonne Objectif → décider offres différenciées</td></tr>
  <tr><td>20 clients</td><td>Automatiser rapport parent hebdo</td></tr>
  <tr><td>30 clients</td><td>Automatiser boosts nuit + rapport matin</td></tr>
  <tr><td>50 clients</td><td>~1 000€ MRR — objectif atteint</td></tr>
  <tr><td>80-100 clients</td><td>Migration Google Sheets → Supabase (PostgreSQL)</td></tr>
</table>

<!-- ═══════════════════════ FOOTER ═══════════════════════ -->
<div class="footer">
  <strong>matheux.fr</strong> — Nicolas Follezou — SIRET 837 763 713 00059<br>
  Document généré le """ + datetime.now().strftime("%d/%m/%Y à %Hh%M") + """ — Usage interne
</div>

</body>
</html>"""


def generate_pdf():
    """Génère le PDF."""
    HTML(string=HTML_CONTENT).write_pdf(PDF_PATH)
    print(f"✅ PDF généré : {PDF_PATH}")
    return PDF_PATH


def send_email(smtp_password: str, to_email: str = "seopourvous@gmail.com"):
    """Envoie le PDF par email via SMTP Ionos."""
    FROM = "no-reply@matheux.fr"
    SMTP_HOST = "smtp.ionos.fr"
    SMTP_PORT = 465

    msg = MIMEMultipart()
    msg["From"] = f"Matheux <{FROM}>"
    msg["To"] = to_email
    msg["Subject"] = "Matheux — Notice Fondateur · Lancement J-2"

    body = """Salut Nicolas,

Voici ta Notice Fondateur Matheux à jour — bilan complet du projet au 16 mars 2026.

12 actions terminées aujourd'hui, lancement confirmé mercredi 18 mars à 9h.

Demain matin : test 3EME + fix 15 frictions.

Bonne soirée !

—
Matheux · matheux.fr
"""
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with open(PDF_PATH, "rb") as f:
        part = MIMEBase("application", "pdf")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename="Matheux_Notice_Fondateur_16mars2026.pdf")
        msg.attach(part)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(FROM, smtp_password)
        server.send_message(msg)
    print(f"✅ Email envoyé à {to_email}")


if __name__ == "__main__":
    generate_pdf()
    if len(sys.argv) > 1:
        send_email(sys.argv[1])
    else:
        print("💡 Pour envoyer : python3 notice_fondateur.py <mot_de_passe_smtp_ionos>")
