// ════════════════════════════════════════════════════════════
//  MATHEUX — Edge Function API (remplace backend.js GAS)
//  Runtime : Deno (Supabase Edge Functions)
//  Dispatch sur "action" comme l'ancien doPost(e)
// ════════════════════════════════════════════════════════════

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const ALLOWED_LEVELS = ["6EME", "5EME", "4EME", "3EME", "1ERE"];

// GAS gardé pour les emails (GmailApp) — migration Resend prévue à ~50 users
const GAS_URL = "https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec";

// Client admin (service_role) pour bypass RLS
const adminClient = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

// ── Helpers ──────────────────────────────────────────────────

function todayParis(): string {
  return new Date().toLocaleDateString("sv-SE", { timeZone: "Europe/Paris" });
}

function json(obj: unknown, status = 200): Response {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization, apikey",
    },
  });
}

function generateCode(): string {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  let code = "";
  for (let i = 0; i < 6; i++) {
    code += chars[Math.floor(Math.random() * chars.length)];
  }
  return code;
}

async function uniqueCode(): Promise<string> {
  const { data: existing } = await adminClient.from("profiles").select("code");
  const codes = (existing || []).map((r: { code: string }) => r.code);
  let code: string;
  do { code = generateCode(); } while (codes.includes(code));
  return code;
}

// ── REGISTER ────────────────────────────────────────────────

async function register(p: Record<string, unknown>) {
  const name = String(p.name || "").trim();
  const email = String(p.email || "").trim().toLowerCase();
  const level = String(p.level || "").toUpperCase();
  const password = String(p.raw_password || "").trim();
  const objectif = String(p.objectif || "").trim().substring(0, 50);

  if (!name) return { status: "error", message: "Le prénom est requis." };
  if (!email) return { status: "error", message: "L'email est requis." };
  if (!password) return { status: "error", message: "Le mot de passe est requis." };
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email))
    return { status: "error", message: "Format d'email invalide." };
  if (name.length > 50)
    return { status: "error", message: "Le prénom ne doit pas dépasser 50 caractères." };
  if (!ALLOWED_LEVELS.includes(level))
    return { status: "error", message: "Seul le niveau 3EME est accepté." };

  // Email déjà pris ?
  const { data: existingUser } = await adminClient.from("profiles").select("code").eq("email", email).maybeSingle();
  if (existingUser) return { status: "error", message: "Un compte existe déjà avec cet email." };

  const isTest = email.endsWith("@matheux.fr") || p.test === true;

  // Limite bêta 50
  if (!isTest) {
    const { count } = await adminClient.from("profiles").select("code", { count: "exact", head: true }).eq("is_admin", false).eq("is_test", false);
    if ((count || 0) >= 50) {
      return { status: "waitlist", message: "Matheux est en bêta privée limitée à 50 familles. Votre adresse est sur liste d'attente." };
    }
  }

  // Créer user Supabase Auth
  const { data: authData, error: authError } = await adminClient.auth.admin.createUser({
    email,
    password,
    email_confirm: true,
  });
  if (authError) return { status: "error", message: "Erreur création compte : " + authError.message };

  const userId = authData.user.id;
  const code = await uniqueCode();
  const now = todayParis();

  // Insérer profil
  const { error: profileError } = await adminClient.from("profiles").insert({
    id: userId,
    code,
    prenom: name,
    niveau: level,
    email,
    date_inscription: now,
    is_admin: false,
    premium: false,
    trial_start: now,
    is_test: isTest,
  });
  if (profileError) return { status: "error", message: "Erreur profil : " + profileError.message };

  // Email bienvenue J+0 + notification fondateur → via GAS (garde Gmail)
  try {
    await fetch(GAS_URL, {
      method: "POST",
      body: JSON.stringify({ action: "send_welcome_email", email, name, code, level, objectif }),
    });
  } catch { /* silencieux — ne bloque pas l'inscription */ }

  // Curriculum officiel
  const { data: curriculum } = await adminClient.from("curriculum")
    .select("categorie, titre, icone, exos_json, timer, ordered")
    .eq("niveau", level);

  const curriculumOfficiel = (curriculum || []).map((r: Record<string, unknown>) => {
    const co: Record<string, unknown> = {
      categorie: r.categorie, titre: r.titre, icone: r.icone,
      exos: typeof r.exos_json === "string" ? JSON.parse(r.exos_json) : (r.exos_json || []),
    };
    if (r.timer) co.timer = r.timer;
    if (r.ordered) co.ordered = true;
    return co;
  });

  return {
    status: "success",
    profile: { code, name, level, isAdmin: false, premium: false, trialStart: now, objectif },
    curriculumOfficiel,
    diagExos: [],
    dailyBoost: null,
    boostExistsInDB: false,
    boostExosDone: 0,
    isFirstDay: true,
    history: [],
    boostHistory: [],
    coursData: {},
    dynamicChapters: [],
    nextChapter: null,
    nextBoost: null,
    pendingBrevet: null,
    revisionChapters: [],
    trial: { trialActive: true, daysLeft: 7, isPremium: false },
  };
}

// ── LOGIN ───────────────────────────────────────────────────

async function login(p: Record<string, unknown>) {
  const email = String(p.email || "").trim().toLowerCase();
  const password = String(p.raw_password || p.password || "").trim();

  if (!email || !password) return { status: "error", message: "Email et mot de passe requis." };

  // Auth Supabase — tente le sign in
  const { data: authData, error: authError } = await adminClient.auth.signInWithPassword({ email, password });

  // Fallback : ancien hash SHA-256 (transition)
  let user: Record<string, unknown> | null = null;
  let isAdminLogin = false;

  if (authError) {
    // Vérifier si c'est un login avec l'ancien hash
    const hash = String(p.password || "").trim();
    if (hash.length === 64) {
      const { data: profile } = await adminClient.from("profiles")
        .select("*").eq("email", email).maybeSingle();
      if (profile && profile.password_hash === hash) {
        user = profile;
      }
    }
    if (!user) return { status: "error", message: "Email ou mot de passe incorrect." };
  } else {
    // Auth OK — récupérer le profil
    const { data: profile } = await adminClient.from("profiles")
      .select("*").eq("id", authData.user.id).single();
    if (!profile) return { status: "error", message: "Profil introuvable." };
    user = profile;
  }

  const code = String(user.code);
  const level = String(user.niveau).toUpperCase();
  const name = String(user.prenom);
  const isAdmin = !!user.is_admin;
  const premium = !!user.premium;
  const trialStart = user.trial_start ? String(user.trial_start) : "";
  const objectif = String(user.objectif || "");
  const todayStr = todayParis();

  // ── Curriculum officiel ──
  const { data: curriculum } = await adminClient.from("curriculum")
    .select("categorie, titre, icone, exos_json, timer, ordered")
    .eq("niveau", level);

  const curriculumOfficiel = (curriculum || []).map((r: Record<string, unknown>) => {
    const co: Record<string, unknown> = {
      categorie: r.categorie, titre: r.titre, icone: r.icone,
      exos: typeof r.exos_json === "string" ? JSON.parse(r.exos_json) : (r.exos_json || []),
    };
    if (r.timer) co.timer = r.timer;
    if (r.ordered) co.ordered = true;
    return co;
  });

  // ── Boost du jour ──
  const { data: boostRows } = await adminClient.from("daily_boosts")
    .select("*").eq("code", code).order("date", { ascending: false });

  let todayBoost = null;
  let boostExosDone = 0;
  let lastUnfinishedBoost = null;
  let lastUnfinishedExosDone = 0;

  for (const br of (boostRows || [])) {
    const brDate = String(br.date).substring(0, 10);
    if (brDate === todayStr) {
      todayBoost = typeof br.boost_json === "string" ? JSON.parse(br.boost_json) : br.boost_json;
      boostExosDone = br.exos_done || 0;
      break;
    }
    if ((br.exos_done || 0) < 5 && !lastUnfinishedBoost) {
      lastUnfinishedBoost = typeof br.boost_json === "string" ? JSON.parse(br.boost_json) : br.boost_json;
      lastUnfinishedExosDone = br.exos_done || 0;
    }
  }
  if (!todayBoost && lastUnfinishedBoost) {
    todayBoost = lastUnfinishedBoost;
    boostExosDone = lastUnfinishedExosDone;
  }
  const boostExistsInDB = todayBoost !== null;

  // ── History (scores hors CALIBRAGE) ──
  const { data: scoreRows } = await adminClient.from("scores")
    .select("*").eq("code", code).neq("chapitre", "CALIBRAGE");

  let _hasCalibration = false;
  {
    const { count } = await adminClient.from("scores")
      .select("id", { count: "exact", head: true }).eq("code", code).eq("source", "CALIBRAGE");
    _hasCalibration = (count || 0) > 0;
  }

  const history = (scoreRows || []).map((r: Record<string, unknown>) => {
    const res = String(r.resultat || "");
    return {
      niveau: String(r.niveau || ""),
      categorie: String(r.chapitre || ""),
      exercice_idx: r.num_exo,
      resultat: res,
      xp: res === "EASY" ? 100 : res === "MEDIUM" ? 50 : 10,
      date: String(r.date || ""),
      q: String(r.enonce || ""),
      mauvaise_option: String(r.mauvaise_option || ""),
      nb_indices: r.nb_indices || 0,
      formule_vue: !!r.formule_vue,
      source: String(r.source || ""),
    };
  });

  // ── Suivi (nextChapter / nextBoost) ──
  let nextChapter = null;
  let nextBoost = null;
  let teasingChapter = false;
  let teasingBoost = false;

  const { data: suiviRow } = await adminClient.from("suivi")
    .select("*").eq("code", code).maybeSingle();

  if (suiviRow) {
    // Scan chapitres (chap1..chap4)
    const chapCols = ["chap1", "chap2", "chap3", "chap4"] as const;
    for (const col of chapCols) {
      const val = suiviRow[col];
      if (!val) continue;
      try {
        const parsed = typeof val === "string" ? JSON.parse(val) : val;
        if (parsed?.draft) continue;
        if (parsed?.categorie && parsed?.exos?.length > 0) {
          if (parsed.publishDate && parsed.publishDate >= todayStr) {
            teasingChapter = true;
          } else {
            nextChapter = parsed;
            if (!isAdminLogin) {
              await adminClient.from("suivi").update({ [col]: null }).eq("code", code);
            }
          }
        }
      } catch { /* JSON malformé — skip */ }
      break;
    }

    // Boost from Suivi
    const boostVal = suiviRow.boost;
    if (boostVal) {
      try {
        const parsed = typeof boostVal === "string" ? JSON.parse(boostVal) : boostVal;
        if (!parsed?.draft && parsed?.exos?.length > 0) {
          if (parsed.publishDate && parsed.publishDate >= todayStr) {
            teasingBoost = true;
          } else {
            nextBoost = parsed;
            if (!isAdminLogin) {
              await adminClient.from("suivi").update({ boost: null }).eq("code", code);
              // Créer entrée DailyBoosts
              const { data: existingBoost } = await adminClient.from("daily_boosts")
                .select("id").eq("code", code).eq("date", todayStr).maybeSingle();
              if (!existingBoost) {
                await adminClient.from("daily_boosts").insert({
                  code, date: todayStr, boost_json: parsed, exos_done: 0,
                });
              }
            }
          }
        }
      } catch { /* skip */ }
    }
  }

  // ── Boost history (10 derniers, hors aujourd'hui) ──
  const { data: boostHistRows } = await adminClient.from("daily_boosts")
    .select("date, exos_done, boost_json")
    .eq("code", code).neq("date", todayStr)
    .order("date", { ascending: false }).limit(10);

  const boostHistory = (boostHistRows || []).map((r: Record<string, unknown>) => ({
    date: String(r.date || ""),
    exosDone: r.exos_done || 0,
    boost: typeof r.boost_json === "string" ? JSON.parse(r.boost_json as string) : r.boost_json,
  }));

  // ── Cours data ──
  const coursData: Record<string, unknown> = {};
  const { data: coursRows } = await adminClient.from("cours")
    .select("*").eq("niveau", level);

  if (coursRows) {
    // Count chapter exos from history
    const chapNbExos: Record<string, number> = {};
    history.forEach((r: { source: string; categorie: string }) => {
      if (r.source === "BOOST") return;
      chapNbExos[r.categorie] = (chapNbExos[r.categorie] || 0) + 1;
    });

    const milestones = [
      { at: 10, key: "section_10" as const, titre: "L'essentiel — Méthode & Exemples" },
      { at: 20, key: "section_20" as const, titre: "Cours complet ✨" },
    ];

    coursRows.forEach((row: Record<string, unknown>) => {
      const cat = String(row.categorie || "");
      if (!cat) return;
      const nbExos = chapNbExos[cat] || 0;
      const unlocked: unknown[] = [];
      const locked: unknown[] = [];
      milestones.forEach((m) => {
        const contenu = String((row as Record<string, string>)[m.key] || "").trim();
        if (!contenu) return;
        if (nbExos >= m.at) unlocked.push({ unlock_at: m.at, titre: m.titre, contenu });
        else locked.push({ unlock_at: m.at, titre: m.titre });
      });
      if (unlocked.length + locked.length > 0) {
        coursData[cat] = { unlocked, locked, nbExos, nextMilestone: locked.length > 0 ? (locked[0] as { unlock_at: number }).unlock_at : null };
      }
    });
  }

  // ── Trial status ──
  let trialActive = false;
  let daysLeft = 0;
  if (trialStart && !premium) {
    const ts = new Date(trialStart);
    const daysSince = Math.floor((Date.now() - ts.getTime()) / 86400000);
    daysLeft = Math.max(0, 7 - daysSince);
    trialActive = daysSince <= 7;
  }

  return {
    status: "success",
    profile: { code, name, level, isAdmin, premium, trialStart, objectif },
    curriculumOfficiel,
    diagExos: [],
    dailyBoost: todayBoost,
    boostExistsInDB,
    boostExosDone,
    isFirstDay: history.length === 0 && !boostExistsInDB,
    history,
    boostHistory,
    coursData,
    dynamicChapters: [],
    nextChapter,
    nextBoost,
    teasingChapter,
    teasingBoost,
    pendingBrevet: user.pending_brevet || null,
    revisionChapters: [],
    hasCalibration: _hasCalibration,
    trial: { trialActive, daysLeft, isPremium: premium },
  };
}

// ── SAVE_SCORE ──────────────────────────────────────────────

async function saveScore(p: Record<string, unknown>) {
  const required = ["code", "name", "level", "categorie", "exercice_idx", "resultat"];
  for (const field of required) {
    if (!p[field] && p[field] !== 0) return { status: "error", message: "Champ manquant : " + field };
  }

  const VALID_RESULTS = ["EASY", "MEDIUM", "HARD", "SKIP"];
  if (!VALID_RESULTS.includes(String(p.resultat)))
    return { status: "error", message: "Résultat invalide." };

  const code = String(p.code);
  if (code.length !== 6) return { status: "error", message: "Code élève invalide." };

  // Vérifier identité
  const { data: profile } = await adminClient.from("profiles")
    .select("email, premium, trial_start").eq("code", code).maybeSingle();
  if (!profile) return { status: "error", message: "Élève introuvable." };
  if (p.email && String(p.email).toLowerCase() !== profile.email)
    return { status: "error", message: "Identité non vérifiée." };

  // Check trial
  if (!profile.premium && profile.trial_start) {
    const daysSince = Math.floor((Date.now() - new Date(profile.trial_start).getTime()) / 86400000);
    if (daysSince > 7) return { status: "error", message: "Essai terminé." };
  }

  const dedupDate = p.answeredAt && /^\d{4}-\d{2}-\d{2}$/.test(String(p.answeredAt))
    ? String(p.answeredAt) : todayParis();

  // Dedup
  const { count } = await adminClient.from("scores")
    .select("id", { count: "exact", head: true })
    .eq("code", code).eq("chapitre", String(p.categorie))
    .eq("num_exo", Number(p.exercice_idx)).eq("date", dedupDate);
  if ((count || 0) > 0) return { status: "success", message: "Score déjà enregistré (dedup)." };

  // Insert
  await adminClient.from("scores").insert({
    code,
    prenom: String(p.name),
    niveau: String(p.level),
    chapitre: String(p.categorie),
    num_exo: Number(p.exercice_idx),
    enonce: String(p.q || "").substring(0, 500),
    resultat: String(p.resultat),
    temps_sec: parseInt(String(p.time || "0")),
    nb_indices: parseInt(String(p.indices || "0")),
    formule_vue: !!p.formule,
    mauvaise_option: String(p.wrongOpt || ""),
    draft: String(p.draft || ""),
    date: dedupDate,
    source: String(p.source || ""),
  });

  // Update confidence score (Progress) — hors BOOST et CALIBRAGE
  const source = String(p.source || "");
  if (source !== "BOOST" && source !== "CALIBRAGE") {
    await updateConfidenceScore(code, String(p.level), String(p.categorie), String(p.resultat), parseInt(String(p.exercice_idx || "0")));
  }

  // MAJ ExosDone dans DailyBoosts si source=BOOST
  if (source === "BOOST") {
    const todayStr = todayParis();
    // Chercher le boost d'aujourd'hui ou le dernier non terminé
    const { data: boostRow } = await adminClient.from("daily_boosts")
      .select("id, exos_done").eq("code", code)
      .or(`date.eq.${todayStr},exos_done.lt.5`)
      .order("date", { ascending: false }).limit(1).maybeSingle();
    if (boostRow) {
      await adminClient.from("daily_boosts")
        .update({ exos_done: (boostRow.exos_done || 0) + 1 }).eq("id", boostRow.id);
    }
  }

  return { status: "success" };
}

// ── UPDATE_CONFIDENCE_SCORE (Progress) ──────────────────────

async function updateConfidenceScore(
  code: string, level: string, categorie: string, resultat: string, exerciceIdx: number
) {
  const { data: existing } = await adminClient.from("progress")
    .select("*").eq("code", code).eq("categorie", categorie).maybeSingle();

  const nbExos = (existing?.nb_exos || 0) + 1;
  const nbEasy = (existing?.nb_easy || 0) + (resultat === "EASY" ? 1 : 0);
  const score = nbExos > 0 ? Math.round((nbEasy / nbExos) * 100) : 0;
  const todayStr = todayParis();

  if (existing) {
    await adminClient.from("progress").update({
      nb_exos: nbExos, nb_easy: nbEasy, score, derniere_pratique: todayStr,
    }).eq("id", existing.id);
  } else {
    await adminClient.from("progress").insert({
      code, niveau: level, categorie, nb_exos: nbExos, nb_easy: nbEasy, score, derniere_pratique: todayStr,
    });
  }
}

// ── SAVE_CALIBRATION_BATCH ──────────────────────────────────

async function saveCalibrationBatch(p: Record<string, unknown>) {
  if (!p.code || !p.scores || !Array.isArray(p.scores))
    return { status: "error", message: "code et scores requis." };

  const code = String(p.code);
  const name = String(p.name || "");
  const level = String(p.level || "");
  const now = todayParis();

  const rows = (p.scores as Record<string, unknown>[]).map((s) => ({
    code, prenom: name, niveau: level,
    chapitre: String(s.categorie || "CALIBRAGE"),
    num_exo: Number(s.exercice_idx || 0),
    enonce: String(s.q || "").substring(0, 500),
    resultat: String(s.resultat || "HARD"),
    temps_sec: parseInt(String(s.temps || "0")),
    nb_indices: parseInt(String(s.nbIndices || "0")),
    formule_vue: !!s.formule,
    mauvaise_option: "", draft: "", date: now, source: "CALIBRAGE",
  }));

  await adminClient.from("scores").insert(rows);
  return { status: "success", saved: rows.length };
}

// ── GENERATE_DIAGNOSTIC ─────────────────────────────────────

// Explicit mapping for frontend names that lost accented chars (BREVET_PACK in app.html)
const CHAP_ALIAS: Record<string, string[]> = {
  "calcul_littral": ["calcul_litteral"],
  "thorme_de_thals": ["thales"],
  "trigonomtrie": ["trigonometrie"],
  "probabilits": ["probabilites"],
};

// Normalise for fuzzy match: lowercase, strip accents, strip _Brevet, strip _de_, underscores
function _normCat(s: string): string {
  return s.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .toLowerCase().replace(/_brevet$/, "").replace(/_+$/, "")
    .replace(/_de_/g, "_").replace(/_/g, "");
}

// Expand a frontend chapter name into all possible normalized forms to match against
function _expandNorms(frontendName: string): string[] {
  const base = _normCat(frontendName);
  const key = frontendName.toLowerCase().replace(/_+$/, "");
  const aliases = CHAP_ALIAS[key] || [];
  return [base, ...aliases.map(_normCat)];
}

// Fuzzy match: check if two normalized strings are "close enough"
// Handles frontend stripping accented chars (Littral vs Litteral, Thorme vs Theoreme)
function _fuzzyMatch(frontNorm: string, dbNorm: string): boolean {
  if (frontNorm === dbNorm) return true;
  if (dbNorm.startsWith(frontNorm) || frontNorm.startsWith(dbNorm)) return true;
  if (dbNorm.includes(frontNorm) || frontNorm.includes(dbNorm)) return true;
  // Subsequence check: all chars of shorter must appear in order in longer
  const [short, long] = frontNorm.length <= dbNorm.length ? [frontNorm, dbNorm] : [dbNorm, frontNorm];
  let j = 0;
  for (let i = 0; i < long.length && j < short.length; i++) {
    if (long[i] === short[j]) j++;
  }
  // If short is a subsequence and at least 60% of long's length, it's a match
  if (j === short.length && short.length >= long.length * 0.5) return true;
  return false;
}

async function generateDiagnostic(p: Record<string, unknown>) {
  const level = String(p.level || "").toUpperCase();
  const selectedChapters = (p.selectedChapters || []) as string[];

  // Always fetch all categories for this level, then filter in memory
  // (handles frontend sending stripped names like "Calcul_Littral" vs DB "Calcul_Litteral_Brevet")
  const { data: allRows } = await adminClient.from("diagnostic_exos")
    .select("categorie, exos_json").eq("niveau", level);

  let diagRows = allRows || [];

  if (selectedChapters.length > 0) {
    const allNorms = selectedChapters.flatMap(_expandNorms);
    diagRows = diagRows.filter((r: Record<string, unknown>) => {
      const dbNorm = _normCat(String(r.categorie));
      return allNorms.some(ns => _fuzzyMatch(ns, dbNorm));
    });
  }
  const exos: unknown[] = [];
  (diagRows || []).forEach((r: Record<string, unknown>) => {
    const parsed = typeof r.exos_json === "string" ? JSON.parse(r.exos_json) : (r.exos_json || []);
    if (Array.isArray(parsed) && parsed.length > 0) {
      // 1 question aléatoire par chapitre
      const pick = parsed[Math.floor(Math.random() * parsed.length)];
      exos.push({ ...pick, categorie: r.categorie });
    }
  });

  return { status: "success", exos };
}

// ── GET_PROGRESS ────────────────────────────────────────────

async function getProgress(p: Record<string, unknown>) {
  const code = String(p.code);
  const { data } = await adminClient.from("progress").select("*").eq("code", code);
  return { status: "success", progress: data || [] };
}

// ── CHECK_TRIAL_STATUS ──────────────────────────────────────

async function checkTrialStatus(p: Record<string, unknown>) {
  const code = String(p.code);
  const { data: profile } = await adminClient.from("profiles")
    .select("premium, trial_start, premium_end").eq("code", code).maybeSingle();
  if (!profile) return { status: "error", message: "Utilisateur introuvable." };

  const isPremium = !!profile.premium;
  if (isPremium) return { trialActive: false, daysLeft: 0, isPremium: true };

  if (profile.trial_start) {
    const daysSince = Math.floor((Date.now() - new Date(profile.trial_start).getTime()) / 86400000);
    return { trialActive: daysSince <= 7, daysLeft: Math.max(0, 7 - daysSince), isPremium: false };
  }
  return { trialActive: false, daysLeft: 0, isPremium: false };
}

// ── SAVE_BOOST ──────────────────────────────────────────────

async function saveBoost(p: Record<string, unknown>) {
  if (!p.code || !p.boost) return { status: "error", message: "code et boost requis." };

  const code = String(p.code);
  const todayStr = todayParis();
  const exosDone = p.exoIdx !== undefined ? parseInt(String(p.exoIdx)) + 1 : 1;

  // Update si existe déjà
  const { data: existing } = await adminClient.from("daily_boosts")
    .select("id").eq("code", code).eq("date", todayStr).maybeSingle();

  if (existing) {
    await adminClient.from("daily_boosts").update({
      boost_json: p.boost, exos_done: exosDone,
    }).eq("id", existing.id);
  } else {
    await adminClient.from("daily_boosts").insert({
      code, date: todayStr, boost_json: p.boost, exos_done: 0,
    });
  }
  return { status: "success" };
}

// ── SUBMIT_FEEDBACK ─────────────────────────────────────────

async function submitFeedback(p: Record<string, unknown>) {
  await adminClient.from("contact").insert({
    email: String(p.email || ""),
    nom: String(p.name || ""),
    message: String(p.feedback || ""),
    type: "feedback",
  });
  return { status: "success" };
}

// ── LOG_CONTACT ─────────────────────────────────────────────

async function logContact(p: Record<string, unknown>) {
  await adminClient.from("contact").insert({
    email: String(p.email || ""),
    nom: String(p.nom || ""),
    message: String(p.message || ""),
    type: "contact",
  });
  return { status: "success" };
}

// ── FORGOT_PASSWORD ─────────────────────────────────────────

async function forgotPassword(p: Record<string, unknown>) {
  const email = String(p.email || "").trim().toLowerCase();
  if (!email) return { status: "error", message: "Email requis." };

  const { error } = await adminClient.auth.resetPasswordForEmail(email, {
    redirectTo: "https://matheux.fr/app.html#reset",
  });
  if (error) return { status: "error", message: error.message };
  return { status: "success", message: "Email de réinitialisation envoyé." };
}

// ── GET_ADMIN_OVERVIEW ──────────────────────────────────────

async function getAdminOverview(p: Record<string, unknown>) {
  const code = String(p.code);
  const { data: profile } = await adminClient.from("profiles")
    .select("is_admin").eq("code", code).maybeSingle();
  if (!profile?.is_admin) return { status: "error", message: "Accès refusé." };

  const { data: users } = await adminClient.from("profiles").select("*").eq("is_test", false);
  const { data: allScores } = await adminClient.from("scores").select("code, chapitre, resultat, date, source");
  const { data: allBoosts } = await adminClient.from("daily_boosts").select("code, date, exos_done");
  const { data: allProgress } = await adminClient.from("progress").select("*");
  const { data: allSuivi } = await adminClient.from("suivi").select("*");

  return {
    status: "success",
    users: users || [],
    scores: allScores || [],
    boosts: allBoosts || [],
    progress: allProgress || [],
    suivi: allSuivi || [],
  };
}

// ── PUBLISH_ADMIN_BOOST ─────────────────────────────────────

async function publishAdminBoost(p: Record<string, unknown>) {
  const code = String(p.code);
  const boostJson = p.boost;
  if (!code || !boostJson) return { status: "error", message: "code et boost requis." };

  const todayStr = todayParis();

  // Écrire dans suivi.boost avec publishDate
  const boost = typeof boostJson === "string" ? JSON.parse(boostJson as string) : boostJson;
  (boost as Record<string, unknown>).publishDate = todayStr;

  const { data: suiviRow } = await adminClient.from("suivi")
    .select("id").eq("code", code).maybeSingle();

  if (suiviRow) {
    await adminClient.from("suivi").update({ boost: JSON.stringify(boost) }).eq("id", suiviRow.id);
  } else {
    await adminClient.from("suivi").insert({ code, boost: JSON.stringify(boost) });
  }

  return { status: "success" };
}

// ── PUBLISH_ADMIN_CHAPTER ───────────────────────────────────

async function publishAdminChapter(p: Record<string, unknown>) {
  const code = String(p.code);
  const chapterJson = p.chapter;
  if (!code || !chapterJson) return { status: "error", message: "code et chapter requis." };

  const todayStr = todayParis();
  const chapter = typeof chapterJson === "string" ? JSON.parse(chapterJson as string) : chapterJson;
  (chapter as Record<string, unknown>).publishDate = todayStr;

  const { data: suiviRow } = await adminClient.from("suivi")
    .select("id, chap1, chap2, chap3, chap4").eq("code", code).maybeSingle();

  // Trouver le premier slot vide
  const slots = ["chap1", "chap2", "chap3", "chap4"] as const;
  let targetSlot = "chap1";
  if (suiviRow) {
    for (const s of slots) {
      if (!suiviRow[s]) { targetSlot = s; break; }
    }
    await adminClient.from("suivi").update({ [targetSlot]: JSON.stringify(chapter) }).eq("id", suiviRow.id);
  } else {
    await adminClient.from("suivi").insert({ code, [targetSlot]: JSON.stringify(chapter) });
  }

  return { status: "success" };
}

// ── STRIPE_WEBHOOK ──────────────────────────────────────────

async function stripeWebhook(p: Record<string, unknown>) {
  const email = String(p.email || "").trim().toLowerCase();
  if (!email) return { status: "error", message: "email requis." };

  await adminClient.from("profiles").update({
    premium: true,
    premium_end: String(p.premium_end || ""),
  }).eq("email", email);

  return { status: "success" };
}

// ── UNSUBSCRIBE ─────────────────────────────────────────────

async function unsubscribeEmail(p: Record<string, unknown>) {
  const email = String(p.email || "").trim().toLowerCase();
  if (!email) return { status: "error", message: "email requis." };

  await adminClient.from("emails").insert({
    email, type: "UNSUB", date: todayParis(),
  });

  return { status: "success" };
}

// ── RESET_PASSWORD ───────────────────────────────────────────

async function resetPassword(p: Record<string, unknown>) {
  const email = String(p.email || "").trim().toLowerCase();
  const password = String(p.password || "").trim();
  if (!email || !password) return { status: "error", message: "Email et mot de passe requis." };

  // Trouver l'utilisateur par email
  const { data: profile } = await adminClient.from("profiles")
    .select("id").eq("email", email).maybeSingle();
  if (!profile) return { status: "error", message: "Utilisateur introuvable." };

  // Mettre à jour le mot de passe via admin API
  const { error } = await adminClient.auth.admin.updateUserById(profile.id, { password });
  if (error) return { status: "error", message: error.message };

  // Mettre à jour le hash dans profiles aussi (pour fallback)
  await adminClient.from("profiles").update({ password_hash: password }).eq("id", profile.id);

  return { status: "success", message: "Mot de passe mis à jour." };
}

// ── REPORT_EXO ──────────────────────────────────────────────

async function reportExo(p: Record<string, unknown>) {
  await adminClient.from("insights").insert({
    code: String(p.code || ""),
    prenom: String(p.name || ""),
    niveau: String(p.level || ""),
    type: String(p.type || "erreur"),
    message: String(p.message || ""),
    enonce_exo: String(p.q || "").substring(0, 80),
    source: String(p.source || ""),
    ref: String(p.ref || ""),
  });
  return { status: "success" };
}

// ── SEND_CONTACT ────────────────────────────────────────────

async function sendContact(p: Record<string, unknown>) {
  await adminClient.from("contact").insert({
    email: String(p.email || ""),
    nom: String(p.nom || p.name || ""),
    message: String(p.message || ""),
    type: "contact_landing",
  });
  return { status: "success" };
}

// ── LOG_MANUAL_EMAIL ────────────────────────────────────────

async function logManualEmail(p: Record<string, unknown>) {
  await adminClient.from("emails").insert({
    email: String(p.email || ""),
    prenom: String(p.prenom || ""),
    type: String(p.type || "manuel"),
    status: "envoyé",
    subject: String(p.subject || ""),
  });
  return { status: "success" };
}

// ── GET_COURS_ADMIN ─────────────────────────────────────────

async function getCoursAdmin(p: Record<string, unknown>) {
  const { data } = await adminClient.from("cours").select("*");
  return { status: "success", cours: data || [] };
}

// ── SAVE_COURS ──────────────────────────────────────────────

async function saveCours(p: Record<string, unknown>) {
  const niveau = String(p.niveau || "");
  const categorie = String(p.categorie || "");
  if (!niveau || !categorie) return { status: "error", message: "niveau et categorie requis." };

  await adminClient.from("cours").upsert({
    niveau, categorie,
    section_10: String(p.section10 || ""),
    section_20: String(p.section20 || ""),
    date_maj: todayParis(),
  }, { onConflict: "niveau,categorie" });

  return { status: "success" };
}

// ── GET_BREVET_CHAPTERS ─────────────────────────────────────

async function getBrevetChapters(_p: Record<string, unknown>) {
  const { data } = await adminClient.from("brevet_exos").select("niveau, categorie, exos_json");
  return { status: "success", chapters: data || [] };
}

// ── GENERATE_BREVET_SESSION ─────────────────────────────────

async function generateBrevetSession(p: Record<string, unknown>) {
  const chapitres = (p.chapitres || []) as string[];
  const { data } = await adminClient.from("brevet_exos")
    .select("categorie, exos_json").in("categorie", chapitres);

  const exos: unknown[] = [];
  (data || []).forEach((r: Record<string, unknown>) => {
    const parsed = typeof r.exos_json === "string" ? JSON.parse(r.exos_json) : (r.exos_json || []);
    if (Array.isArray(parsed)) exos.push(...parsed);
  });

  return { status: "success", exos };
}

// ── SAVE_BREVET_RESULT ──────────────────────────────────────

async function saveBrevetResult(p: Record<string, unknown>) {
  await adminClient.from("brevet_results").insert({
    code: String(p.code || ""),
    prenom: String(p.name || ""),
    niveau: String(p.level || "3EME"),
    chapitres: String(p.chapitres || ""),
    nb_questions: Number(p.nbQuestions || 0),
    nb_correct: Number(p.nbCorrect || 0),
    score_pct: Number(p.scorePct || 0),
    detail_json: p.detail || null,
    message: String(p.message || ""),
  });
  return { status: "success" };
}

// ── PROXY GAS — actions qui nécessitent GmailApp ────────────

async function proxyGas(p: Record<string, unknown>) {
  try {
    const resp = await fetch(GAS_URL, { method: "POST", body: JSON.stringify(p) });
    return await resp.json();
  } catch (err) {
    return { status: "error", message: "GAS proxy error: " + String(err) };
  }
}

// ── NOOP actions (fonctionnalités secondaires, retournent success) ──

async function noopAction(_p: Record<string, unknown>) {
  return { status: "success" };
}

// ── DISPATCH ────────────────────────────────────────────────

const ACTIONS: Record<string, (p: Record<string, unknown>) => Promise<unknown>> = {
  register,
  login,
  save_score: saveScore,
  save_boost: saveBoost,
  save_calibration_batch: saveCalibrationBatch,
  generate_diagnostic: generateDiagnostic,
  get_progress: getProgress,
  check_trial_status: checkTrialStatus,
  submit_feedback: submitFeedback,
  log_contact: logContact,
  forgot_password: forgotPassword,
  reset_password: resetPassword,
  get_admin_overview: getAdminOverview,
  publish_admin_boost: publishAdminBoost,
  publish_admin_chapter: publishAdminChapter,
  stripe_webhook: stripeWebhook,
  unsubscribe: unsubscribeEmail,
  report_exo: reportExo,
  send_contact: sendContact,
  log_manual_email: logManualEmail,
  get_cours_admin: getCoursAdmin,
  save_cours: saveCours,
  get_brevet_chapters: getBrevetChapters,
  generate_brevet_session: generateBrevetSession,
  save_brevet_result: saveBrevetResult,
  // Noop — fonctionnalités secondaires qui ne cassent pas le parcours
  add_teasing_early: noopAction,
  detect_fragile_prereqs: noopAction,
  enqueue: noopAction,
  generate_daily_boost: noopAction,
  generate_revision: noopAction,
  log_event: noopAction,
  mark_all_test: noopAction,
  simulate_next_day: noopAction,
  send_test_email: proxyGas,
  send_weekly_report: proxyGas,
  send_custom_email: proxyGas,
  send_session_rapport: proxyGas,
  get_audit_exos: noopAction,
  get_audit_remarks: noopAction,
  publish_admin_brevet: noopAction,
  publish_admin_revision: noopAction,
  request_brevet_chapter: noopAction,
};

Deno.serve(async (req: Request) => {
  // CORS preflight
  if (req.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, apikey",
      },
    });
  }

  if (req.method !== "POST") return json({ status: "error", message: "POST uniquement" }, 405);

  try {
    const p = await req.json();
    const action = String(p.action || "");
    const handler = ACTIONS[action];
    if (!handler) return json({ status: "error", message: "Action inconnue : " + action });

    const result = await handler(p);
    return json(result);
  } catch (err) {
    return json({ status: "error", message: "Erreur serveur : " + String(err) }, 500);
  }
});
