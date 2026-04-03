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

// ── Cache en mémoire (persiste tant que l'instance Edge Function est chaude) ──
const _cache: Record<string, { data: unknown; ts: number }> = {};
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

function cacheGet(key: string): unknown | null {
  const entry = _cache[key];
  if (!entry) return null;
  if (Date.now() - entry.ts > CACHE_TTL) { delete _cache[key]; return null; }
  return entry.data;
}

function cacheSet(key: string, data: unknown): void {
  _cache[key] = { data, ts: Date.now() };
}

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
  const password = String(p.raw_password || p.password || "").trim();
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

  // Limite bêta supprimée — Supabase tient la charge (migration 02/04/2026)

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
    free_chapter: null,
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
    trial: { isPremium: false, freeChapter: null },
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

  // ── Curriculum officiel (cached 5 min — identique pour tous les élèves d'un même niveau) ──
  const cacheKey = `curriculum_${level}`;
  let curriculumOfficiel = cacheGet(cacheKey) as Record<string, unknown>[] | null;

  if (!curriculumOfficiel) {
    const { data: curriculum } = await adminClient.from("curriculum")
      .select("categorie, titre, icone, exos_json, timer, ordered")
      .eq("niveau", level);

    curriculumOfficiel = (curriculum || []).map((r: Record<string, unknown>) => {
      const co: Record<string, unknown> = {
        categorie: r.categorie, titre: r.titre, icone: r.icone,
        exos: typeof r.exos_json === "string" ? JSON.parse(r.exos_json) : (r.exos_json || []),
      };
      if (r.timer) co.timer = r.timer;
      if (r.ordered) co.ordered = true;
      return co;
    });
    cacheSet(cacheKey, curriculumOfficiel);
  }

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

  // ── History (scores hors CALIBRAGE — 60 derniers jours, champs allégés) ──
  const histCutoff = new Date();
  histCutoff.setDate(histCutoff.getDate() - 60);
  const histCutoffStr = histCutoff.toISOString().split("T")[0];

  const { data: scoreRows } = await adminClient.from("scores")
    .select("code, niveau, chapitre, num_exo, resultat, temps_sec, nb_indices, formule_vue, date, source")
    .eq("code", code).neq("chapitre", "CALIBRAGE")
    .gte("date", histCutoffStr);

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

    const todayStr = new Date().toISOString().slice(0, 10);
    coursRows.forEach((row: Record<string, unknown>) => {
      const cat = String(row.categorie || "");
      if (!cat) return;
      const nbExos = chapNbExos[cat] || 0;
      const unlocked: unknown[] = [];
      const locked: unknown[] = [];
      const teasingCours: unknown[] = [];
      milestones.forEach((m) => {
        const contenu = String((row as Record<string, string>)[m.key] || "").trim();
        if (!contenu) return;
        // Gate J+1 : publish_XX doit être <= aujourd'hui
        const publishKey = m.key === "section_10" ? "publish_10" : "publish_20";
        const publishDate = String(row[publishKey] || "");
        const isPublished = publishDate && publishDate <= todayStr;
        if (nbExos >= m.at && isPublished) unlocked.push({ unlock_at: m.at, titre: m.titre, contenu });
        else if (nbExos >= m.at && !isPublished) teasingCours.push({ unlock_at: m.at, titre: m.titre });
        else locked.push({ unlock_at: m.at, titre: m.titre });
      });
      if (unlocked.length + locked.length + teasingCours.length > 0) {
        coursData[cat] = { unlocked, locked, teasingCours, nbExos, nextMilestone: locked.length > 0 ? (locked[0] as { unlock_at: number }).unlock_at : null };
      }
    });
  }

  // ── Freemium status ──
  // premium_end = date d'expiration premium (ex: 2026-06-30 pour Brevet 2026)
  let isPremium = premium;
  if (isPremium && user.premium_end) {
    const endDate = String(user.premium_end).substring(0, 10);
    if (endDate && endDate < todayStr) isPremium = false; // premium expiré
  }
  const freeChapter = user.free_chapter ? String(user.free_chapter) : null;

  return {
    status: "success",
    profile: { code, name, level, isAdmin, premium: isPremium, trialStart, objectif },
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
    trial: { isPremium, freeChapter },
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
    .select("email, premium, premium_end, free_chapter").eq("code", code).maybeSingle();
  if (!profile) return { status: "error", message: "Élève introuvable." };
  if (p.email && String(p.email).toLowerCase() !== profile.email)
    return { status: "error", message: "Identité non vérifiée." };

  // Freemium guard : si !premium, autoriser seulement CALIBRAGE, BOOST, et le chapitre gratuit
  const source = String(p.source || "");
  const categorie = String(p.categorie || "");
  let _isPremium = !!profile.premium;
  if (_isPremium && profile.premium_end) {
    const endDate = String(profile.premium_end).substring(0, 10);
    if (endDate && endDate < todayParis()) _isPremium = false;
  }
  if (!_isPremium && source !== "CALIBRAGE" && source !== "BOOST") {
    if (!profile.free_chapter || categorie !== profile.free_chapter) {
      return { status: "error", message: "Chapitre verrouillé — débloque l'accès complet pour continuer." };
    }
  }

  const dedupDate = p.answeredAt && /^\d{4}-\d{2}-\d{2}$/.test(String(p.answeredAt))
    ? String(p.answeredAt) : todayParis();

  // Insert with ON CONFLICT dedup (idx_scores_dedup: code+chapitre+num_exo+date)
  const { error: insertErr } = await adminClient.from("scores").upsert({
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
  }, { onConflict: "code,chapitre,num_exo,date", ignoreDuplicates: true });

  // Update confidence score (Progress) — hors BOOST et CALIBRAGE
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
  code: string, level: string, categorie: string, resultat: string, _exerciceIdx: number
) {
  // Use RPC or read-then-write (UPSERT can't do nb_exos+1 atomically with supabase-js)
  const { data: existing } = await adminClient.from("progress")
    .select("id, nb_exos, nb_easy").eq("code", code).eq("categorie", categorie).maybeSingle();

  const nbExos = (existing?.nb_exos || 0) + 1;
  const nbEasy = (existing?.nb_easy || 0) + (resultat === "EASY" ? 1 : 0);
  const score = nbExos > 0 ? Math.round((nbEasy / nbExos) * 100) : 0;
  const todayStr = todayParis();

  if (existing) {
    await adminClient.from("progress").update({
      nb_exos: nbExos, nb_easy: nbEasy, score, derniere_pratique: todayStr,
    }).eq("id", existing.id);
  } else {
    await adminClient.from("progress").upsert({
      code, niveau: level, categorie, nb_exos: nbExos, nb_easy: nbEasy, score, derniere_pratique: todayStr,
    }, { onConflict: "code,chapitre" }).catch(() => {
      // Race condition fallback — another request created it
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

  // Identifier le chapitre le plus faible et le set comme free_chapter
  // (seulement si l'élève n'est pas premium et n'a pas encore de free_chapter)
  let freeChapter: string | null = null;
  const { data: prof } = await adminClient.from("profiles")
    .select("premium, free_chapter").eq("code", code).maybeSingle();

  if (prof && !prof.premium && !prof.free_chapter) {
    const chapErrors: Record<string, { total: number; wrong: number }> = {};
    for (const s of (p.scores as Record<string, unknown>[])) {
      // originalChapter contient le vrai chapitre (categorie = "CALIBRAGE" pour tous)
      const cat = String(s.originalChapter || s.categorie || "");
      if (!cat || cat === "CALIBRAGE") continue;
      if (!chapErrors[cat]) chapErrors[cat] = { total: 0, wrong: 0 };
      chapErrors[cat].total++;
      if (String(s.resultat || "") !== "EASY") chapErrors[cat].wrong++;
    }
    let weakest = "";
    let worstRatio = -1;
    for (const [cat, stats] of Object.entries(chapErrors)) {
      const ratio = stats.total > 0 ? stats.wrong / stats.total : 0;
      if (ratio > worstRatio) { worstRatio = ratio; weakest = cat; }
    }
    if (weakest) {
      await adminClient.from("profiles").update({ free_chapter: weakest }).eq("code", code);
      freeChapter = weakest;
    }
  } else if (prof) {
    freeChapter = prof.free_chapter || null;
  }

  return { status: "success", saved: rows.length, freeChapter };
}

// ── SAVE_SCORES_BATCH (generic — for boost/chapter flush) ───

async function saveScoresBatch(p: Record<string, unknown>) {
  if (!p.code || !p.scores || !Array.isArray(p.scores) || p.scores.length === 0)
    return { status: "error", message: "code et scores[] requis." };
  if ((p.scores as unknown[]).length > 25)
    return { status: "error", message: "Max 25 scores par batch." };

  const code = String(p.code);
  if (code.length !== 6) return { status: "error", message: "Code élève invalide." };

  // Single identity check for the whole batch
  const { data: profile } = await adminClient.from("profiles")
    .select("email, premium, premium_end, free_chapter").eq("code", code).maybeSingle();
  if (!profile) return { status: "error", message: "Élève introuvable." };

  // Freemium guard batch
  let _batchPremium = !!profile.premium;
  if (_batchPremium && profile.premium_end) {
    const endDate = String(profile.premium_end).substring(0, 10);
    if (endDate && endDate < todayParis()) _batchPremium = false;
  }
  if (!_batchPremium) {
    for (const s of (p.scores as Record<string, unknown>[])) {
      const src = String(s.source || "");
      const cat = String(s.categorie || "");
      if (src === "CALIBRAGE" || src === "BOOST") continue;
      if (!profile.free_chapter || cat !== profile.free_chapter) {
        return { status: "error", message: "Chapitre verrouillé — débloque l'accès complet." };
      }
    }
  }

  const todayStr = todayParis();
  const name = String(p.name || "");
  const level = String(p.level || "");

  // Build rows
  const rows = (p.scores as Record<string, unknown>[]).map((s) => ({
    code, prenom: name, niveau: level,
    chapitre: String(s.categorie || ""),
    num_exo: Number(s.exercice_idx || 0),
    enonce: String(s.q || "").substring(0, 500),
    resultat: String(s.resultat || "HARD"),
    temps_sec: parseInt(String(s.time || s.temps || "0")),
    nb_indices: parseInt(String(s.indices || s.nbIndices || "0")),
    formule_vue: !!(s.formule),
    mauvaise_option: String(s.wrongOpt || ""),
    draft: String(s.draft || ""),
    date: (s.answeredAt && /^\d{4}-\d{2}-\d{2}$/.test(String(s.answeredAt)))
      ? String(s.answeredAt) : todayStr,
    source: String(s.source || ""),
  }));

  // Batch insert with dedup (ON CONFLICT ignore)
  await adminClient.from("scores").upsert(rows, {
    onConflict: "code,chapitre,num_exo,date", ignoreDuplicates: true
  });

  // Batch progress updates — group by chapitre, only for non-BOOST non-CALIBRAGE
  const chapScores: Record<string, string[]> = {};
  let boostCount = 0;
  for (const s of (p.scores as Record<string, unknown>[])) {
    const src = String(s.source || "");
    if (src === "BOOST") { boostCount++; continue; }
    if (src === "CALIBRAGE") continue;
    const cat = String(s.categorie || "");
    if (!chapScores[cat]) chapScores[cat] = [];
    chapScores[cat].push(String(s.resultat || "HARD"));
  }

  // Update progress per chapter
  for (const [cat, results] of Object.entries(chapScores)) {
    const { data: existing } = await adminClient.from("progress")
      .select("id, nb_exos, nb_easy").eq("code", code).eq("categorie", cat).maybeSingle();

    const nbExos = (existing?.nb_exos || 0) + results.length;
    const nbEasy = (existing?.nb_easy || 0) + results.filter(r => r === "EASY").length;
    const score = nbExos > 0 ? Math.round((nbEasy / nbExos) * 100) : 0;

    if (existing) {
      await adminClient.from("progress").update({
        nb_exos: nbExos, nb_easy: nbEasy, score, derniere_pratique: todayStr,
      }).eq("id", existing.id);
    } else {
      await adminClient.from("progress").insert({
        code, niveau: level, categorie: cat, nb_exos: nbExos, nb_easy: nbEasy, score, derniere_pratique: todayStr,
      });
    }
  }

  // Update ExosDone in DailyBoosts if any BOOST scores
  if (boostCount > 0) {
    const { data: boostRow } = await adminClient.from("daily_boosts")
      .select("id, exos_done").eq("code", code)
      .or(`date.eq.${todayStr},exos_done.lt.5`)
      .order("date", { ascending: false }).limit(1).maybeSingle();
    if (boostRow) {
      await adminClient.from("daily_boosts")
        .update({ exos_done: Math.min((boostRow.exos_done || 0) + boostCount, 5) }).eq("id", boostRow.id);
    }
  }

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
      // Filtrer les fill côté backend (diagnostic = QCM/VF uniquement)
      const qcmVf = parsed.filter((e: Record<string, unknown>) => {
        if (e.type === "fill") return false;
        const opts = (e.options || e.opts || []) as unknown[];
        if (!opts.length && e.a) return false; // fill implicite
        return true;
      });
      const pool = qcmVf.length > 0 ? qcmVf : parsed; // fallback si tout est fill
      const pick = pool[Math.floor(Math.random() * pool.length)];
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
    .select("premium, premium_end, free_chapter").eq("code", code).maybeSingle();
  if (!profile) return { status: "error", message: "Utilisateur introuvable." };

  let isPremium = !!profile.premium;
  if (isPremium && profile.premium_end) {
    const endDate = String(profile.premium_end).substring(0, 10);
    const todayStr = todayParis();
    if (endDate && endDate < todayStr) isPremium = false;
  }
  const freeChapter = profile.free_chapter ? String(profile.free_chapter) : null;
  return { status: "success", isPremium, freeChapter };
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
    premium_end: String(p.premium_end || "2026-06-30"),
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

  const upsertData: Record<string, unknown> = {
    niveau, categorie, date_maj: todayParis(),
  };
  if (p.section10 !== undefined) {
    upsertData.section_10 = String(p.section10 || "");
    upsertData.publish_10 = String(p.publish10 || todayParis());
  }
  if (p.section20 !== undefined) {
    upsertData.section_20 = String(p.section20 || "");
    upsertData.publish_20 = String(p.publish20 || todayParis());
  }
  await adminClient.from("cours").upsert(upsertData, { onConflict: "niveau,categorie" });

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
  save_scores_batch: saveScoresBatch,
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
