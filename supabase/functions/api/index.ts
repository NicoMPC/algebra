// ════════════════════════════════════════════════════════════
//  MATHEUX — Edge Function API (remplace backend.js GAS)
//  Runtime : Deno (Supabase Edge Functions)
//  Dispatch sur "action" comme l'ancien doPost(e)
// ════════════════════════════════════════════════════════════

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const ALLOWED_LEVELS = ["6EME", "5EME", "4EME", "3EME", "1ERE"];

// GAS gardé en legacy (plus d'envoi email — Resend depuis 07/04/2026)
const GAS_URL = "https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec";
const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY")!;
// Stripe webhook signing secret (set via `supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_...`)
// REQUIRED en prod — si absent, les webhooks Stripe sont rejetés (fail-closed).
const STRIPE_WEBHOOK_SECRET = Deno.env.get("STRIPE_WEBHOOK_SECRET") || "";

// Client admin (service_role) pour bypass RLS
const adminClient = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);
// Client dédié au login (signInWithPassword) : sur adminClient, la session de l'élève connecté
// remplaçait la clé service_role dans toutes les requêtes suivantes de l'instance (RLS appliquée
// → « Profil introuvable » / « Élève introuvable » pour les autres élèves). Bug trouvé en dev local 24/09.
const authClient = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY, {
  auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false },
});

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

// ── Stripe signature verification (manual HMAC SHA-256, pas de dépendance) ──
function _hexOfBuf(buf: ArrayBuffer): string {
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, "0")).join("");
}

function _timingSafeEqualHex(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

async function verifyStripeSignature(rawBody: string, signatureHeader: string, secret: string, toleranceSec = 300): Promise<boolean> {
  if (!signatureHeader || !secret) return false;
  const parts = signatureHeader.split(",").map(s => s.trim());
  const tsPart = parts.find(p => p.startsWith("t="));
  const sigHexes = parts.filter(p => p.startsWith("v1=")).map(p => p.slice(3));
  if (!tsPart || sigHexes.length === 0) return false;
  const ts = tsPart.slice(2);
  const tsNum = parseInt(ts);
  if (!Number.isFinite(tsNum)) return false;
  // Replay protection : rejeter les timestamps trop anciens (> 5 min par défaut)
  const nowSec = Math.floor(Date.now() / 1000);
  if (Math.abs(nowSec - tsNum) > toleranceSec) return false;
  const signedPayload = `${ts}.${rawBody}`;
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sigBuf = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(signedPayload));
  const expected = _hexOfBuf(sigBuf);
  return sigHexes.some(h => _timingSafeEqualHex(h, expected));
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
  // Audit 2026-04-11 P0 (porté de la prod le 25/09) : whitelist chars pour bloquer XSS stored dans le dashboard admin.
  if (!/^[\p{L}\p{M}\s'\-]{1,50}$/u.test(name))
    return { status: "error", message: "Prénom invalide — uniquement lettres, espaces, tirets et apostrophes." };
  if (!ALLOWED_LEVELS.includes(level))
    return { status: "error", message: "Niveau non accepté." };

  // Email déjà pris ? Check profiles ET Supabase Auth
  const { data: existingProfile } = await adminClient.from("profiles").select("code").eq("email", email).maybeSingle();
  if (existingProfile) return { status: "error", message: "Un compte existe déjà avec cet email." };

  // Check Supabase Auth aussi (cas : auth existe mais profil supprimé/orphelin)
  const { data: authLookup } = await adminClient.auth.admin.listUsers({ perPage: 1000, page: 1 });
  const authExists = (authLookup?.users || []).some((u: { email?: string }) => u.email?.toLowerCase() === email);
  if (authExists) return { status: "error", message: "Un compte existe déjà avec cet email." };

  const isTest = email.endsWith("@matheux.fr") || p.test === true;

  // Limite bêta supprimée — Supabase tient la charge (migration 02/04/2026)

  // Créer user Supabase Auth
  const { data: authData, error: authError } = await adminClient.auth.admin.createUser({
    email,
    password,
    email_confirm: true,
  });
  if (authError) {
    const msg = authError.message || "";
    // Supabase Auth renvoie "already been registered" si email existe déjà
    if (msg.toLowerCase().includes("already") || msg.toLowerCase().includes("exist") || msg.toLowerCase().includes("duplicate")) {
      return { status: "error", message: "Un compte existe déjà avec cet email." };
    }
    return { status: "error", message: "Erreur création compte : " + msg };
  }

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

  // Session tout de suite (Besoin API n°8/9) : l'app enchaîne les actions élève avec access_token.
  const { data: sess } = await authClient.auth.signInWithPassword({ email, password });
  const session = sess?.session || null;

  // Diagnostic express fait en invité avant le compte (Besoin API n°1) : rattachement + rejeu.
  let rattache: Awaited<ReturnType<typeof mxRattacherInvite>> = null;
  if (p.diagnostic_id && p.guest_token) {
    try { rattache = await mxRattacherInvite(p, { code, prenom: name, niveau: level, email, free_chapter: null }); }
    catch (e) { console.error("[register] rattachement invité", e); }
  }
  // Ancien templateJ0 remplacé par P-X0 (bilan express au parent, Besoin API n°7) : il part dès que la
  // carte express existe (ici si le diag invité est terminé, sinon à la fin du diagnostic).
  if (rattache?.termine && rattache.carte) {
    await mxEmailBilanExpress({ code, prenom: name, email }, rattache.diagnostic_id, rattache.carte, rattache.ref);
  }

  // Notification fondateur
  try {
    const isTest = email.endsWith("@matheux.fr");
    if (!isTest) {
      await resendSend("seopourvous@gmail.com",
        "[Matheux] Nouvelle inscription : " + name + " (" + level + ")",
        "<p>" + name + " (" + level + ") vient de s'inscrire.</p><p>Email parent : " + email + "<br>Code : " + code + "<br>Objectif : " + (objectif || "—") + "</p>"
      );
    }
  } catch { /* silencieux */ }

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
    profile: { code, name, level, isAdmin: false, premium: false, trialStart: now, objectif, mode: null },
    access_token: session?.access_token || null,
    refresh_token: session?.refresh_token || null,
    expires_at: session?.expires_at || null,
    diagnostic_id: rattache?.diagnostic_id || null,
    diagnostic_rattache: !!rattache,
    ...(p.diagnostic_id && p.guest_token && !rattache ? { rattachement_erreur: "Session invitée expirée ou déjà utilisée : refais le diagnostic express." } : {}),
    carte: rattache?.carte ? mxMasquerCarte(rattache.carte, "free", rattache.ref) : null,
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
  const { data: authData, error: authError } = await authClient.auth.signInWithPassword({ email, password });

  // Fallback : ancien hash SHA-256 (transition)
  let user: Record<string, unknown> | null = null;

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
  // Besoin API n°12 : diagnostic express fait en invité par quelqu'un qui a DÉJÀ un compte → rattaché au login
  // (même logique que register). Seulement avec une vraie session (pas le fallback hash legacy).
  let rattache: Awaited<ReturnType<typeof mxRattacherInvite>> = null;
  if (authData?.session && p.diagnostic_id && p.guest_token && !user!.is_admin) {
    try { rattache = await mxRattacherInvite(p, user!); } catch (e) { console.error("[login] rattachement invité", e); }
    if (rattache?.termine && rattache.carte) await mxEmailBilanExpress(user!, rattache.diagnostic_id, rattache.carte, rattache.ref);
  }
  const rep = await mxReponseSession(user!, authData?.session || null);
  if (p.diagnostic_id && p.guest_token) {
    Object.assign(rep, { diagnostic_id: rattache?.diagnostic_id || null, diagnostic_rattache: !!rattache,
      ...(rattache ? {} : { rattachement_erreur: "Session invitée expirée ou déjà utilisée." }) });
  }
  return rep;
}

// Réponse de connexion (login, login_token) : profil + état de l'app + jetons de session.
// `session` = jetons à renvoyer (access_token pour chaque appel élève, refresh_token pour le renouveler).
async function mxReponseSession(user: Record<string, unknown>,
  session: { access_token: string; refresh_token?: string | null; expires_at?: number | null } | null) {
  let isAdminLogin = false;
  const code = String(user.code);
  const level = String(user.niveau).toUpperCase();
  const name = String(user.prenom);
  const isAdmin = !!user.is_admin;
  // A6 : admin read-only — ne pas consommer nextBoost/nextChapter depuis suivi
  isAdminLogin = isAdmin;
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
  // premium_end = null par défaut (accès one-shot non expirant). Réservé à un usage
  // futur (ex: offre limitée dans le temps) — si renseigné, coupe l'accès après la date.
  let isPremium = premium;
  if (isPremium && user.premium_end) {
    const endDate = String(user.premium_end).substring(0, 10);
    if (endDate && endDate < todayStr) isPremium = false; // premium expiré
  }
  const freeChapter = user.free_chapter ? String(user.free_chapter) : null;

  return {
    status: "success",
    profile: { code, name, level, isAdmin, premium: isPremium, trialStart, objectif, mode: user.mode || null },
    access_token: session?.access_token || null,
    refresh_token: session?.refresh_token || null,
    expires_at: session?.expires_at || null,
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

// ── LOGIN_TOKEN {access_token, refresh_token?} / REFRESH_SESSION {refresh_token} (Besoin API n°9) ──
// Auto-login sans garder le hash du mot de passe côté app : on garde access_token + refresh_token.
// access_token valide → même réponse que login. Expiré mais refresh_token fourni → session renouvelée
// (nouveaux jetons dans la réponse, à re-stocker : le refresh_token est à usage unique chez Supabase).
async function mxRafraichir(refresh: string) {
  if (!refresh) return null;
  const { data, error } = await authClient.auth.refreshSession({ refresh_token: refresh });
  if (error || !data?.session || !data.user) return null;
  return { uid: data.user.id, session: data.session };
}

async function loginToken(p: Record<string, unknown>) {
  const access = String(p.access_token || ""), refresh = String(p.refresh_token || "");
  let uid: string | null = null;
  let session: { access_token: string; refresh_token?: string | null; expires_at?: number | null } | null = null;
  if (access) {
    const { data, error } = await adminClient.auth.getUser(access);
    if (!error && data?.user) { uid = data.user.id; session = { access_token: access, refresh_token: refresh || null, expires_at: null }; }
  }
  if (!uid && refresh) {
    const r = await mxRafraichir(refresh);
    if (r) { uid = r.uid; session = r.session; }
  }
  if (!uid || !session) return MX_AUTH_REFUS;
  const { data: profile } = await adminClient.from("profiles").select("*").eq("id", uid).maybeSingle();
  if (!profile) return { status: "error", message: "Profil introuvable." };
  return await mxReponseSession(profile as Record<string, unknown>, session);
}

async function refreshSession(p: Record<string, unknown>) {
  const r = await mxRafraichir(String(p.refresh_token || ""));
  if (!r) return MX_AUTH_REFUS;
  const { data: profile } = await adminClient.from("profiles").select("code").eq("id", r.uid).maybeSingle();
  return { status: "success", access_token: r.session.access_token, refresh_token: r.session.refresh_token,
    expires_at: r.session.expires_at || null, code: profile?.code || null };
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
  if (!(await mxAuth(p))) return MX_AUTH_REFUS; // Besoin API n°8 : jeton de session obligatoire

  // Vérifier identité — SELECT avec `mode` (fix P1 #4 mode lite Leo)
  const { data: profile } = await adminClient.from("profiles")
    .select("email, mode, premium, premium_end, free_chapter").eq("code", code).maybeSingle();
  if (!profile) return { status: "error", message: "Élève introuvable." };
  if (p.email && String(p.email).toLowerCase() !== profile.email)
    return { status: "error", message: "Identité non vérifiée." };

  const source = String(p.source || "");
  const categorie = String(p.categorie || "");

  // Hardening (P1 #7) : CALIBRAGE ne doit pas passer par saveScore — seulement par save_calibration_batch
  if (source === "CALIBRAGE") {
    return { status: "error", message: "CALIBRAGE doit passer par save_calibration_batch." };
  }

  // Hardening (P1 #7) : source=BOOST nécessite un boost actif en DB.
  // On remonte la lookup du boost ici pour le réutiliser plus bas (évite un 2ème round-trip).
  let activeBoostRow: { id: number; exos_done: number } | null = null;
  if (source === "BOOST") {
    const todayStr = todayParis();
    const { data: boostRow } = await adminClient.from("daily_boosts")
      .select("id, exos_done").eq("code", code)
      .or(`date.eq.${todayStr},exos_done.lt.5`)
      .order("date", { ascending: false }).limit(1).maybeSingle();
    if (!boostRow) {
      return { status: "error", message: "Aucun boost actif — source BOOST refusée." };
    }
    activeBoostRow = boostRow as { id: number; exos_done: number };
  }

  // Freemium guard : mode lite OU premium OU BOOST actif OU free_chapter
  const isLite = (profile as Record<string, unknown>).mode === "lite";
  let _isPremium = !!profile.premium;
  if (_isPremium && profile.premium_end) {
    const endDate = String(profile.premium_end).substring(0, 10);
    if (endDate && endDate < todayParis()) _isPremium = false;
  }
  // LIBRE = entraînement libre du Programme Brevet (get_training {comp}) : réservé au programme.
  if (source === "LIBRE" && !_isPremium) {
    return { status: "error", message: "Entraînement libre réservé au Programme Brevet.", paywall: "programme_brevet" };
  }
  if (!isLite && !_isPremium && source !== "BOOST") {
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
  }, { onConflict: "code,chapitre,num_exo,date,source", ignoreDuplicates: true }); // = idx_scores_dedup (schema.sql)
  // Audit 2026-04-11 P0 (porté 25/09) : ne plus échouer en silence (scores perdus 9 jours en avril).
  if (insertErr) {
    console.error("saveScore upsert error:", insertErr);
    return { status: "error", message: "Erreur enregistrement score : " + insertErr.message };
  }

  // Update confidence score (Progress) — hors BOOST, LIBRE et CALIBRAGE
  if (source !== "BOOST" && source !== "LIBRE" && source !== "CALIBRAGE") {
    await updateConfidenceScore(code, String(p.level), String(p.categorie), String(p.resultat), parseInt(String(p.exercice_idx || "0")));
  }

  // Moteur 3e : maîtrise par compétence — additif, ignoré si l'exo ne porte ni item_id ni comp.
  if (p.item_id || p.comp) {
    try { await mxMajDepuisScore(code, p, source === "BOOST" || source === "LIBRE" ? "train" : "legacy"); }
    catch (e) { console.error("[moteur] maj maîtrise save_score", e); }
  }

  // MAJ ExosDone dans DailyBoosts si source=BOOST — réutilise activeBoostRow chargé plus haut
  if (source === "BOOST" && activeBoostRow) {
    await adminClient.from("daily_boosts")
      .update({ exos_done: Math.min((activeBoostRow.exos_done || 0) + 1, 5) }).eq("id", activeBoostRow.id);
  }

  return { status: "success" };
}

// ── UPDATE_CONFIDENCE_SCORE (Progress) ──────────────────────

async function updateConfidenceScore(
  code: string, level: string, categorie: string, _resultat: string, _exerciceIdx: number
) {
  // Audit 2026-04-11 P0 (porté de la prod le 25/09) : on recompte depuis `scores` (source de vérité)
  // au lieu d'incrémenter progress.nb_easy (colonne absente en prod avant la migration
  // 20260924_progress_nb_easy → PGRST204, progress jamais écrite). Ne dépend plus de l'ordre de déploiement.
  const { data: scoreRows, error: selErr } = await adminClient.from("scores")
    .select("resultat, source")
    .eq("code", code).eq("chapitre", categorie);
  if (selErr) {
    console.error("updateConfidenceScore select error:", selErr);
    return;
  }
  const relevant = (scoreRows || []).filter((s: Record<string, unknown>) => {
    const src = String(s.source || "");
    return src !== "BOOST" && src !== "CALIBRAGE" && src !== "LIBRE";
  });
  const nbExos = relevant.length;
  const nbEasy = relevant.filter((s: Record<string, unknown>) => String(s.resultat) === "EASY").length;
  const nbErreurs = nbExos - nbEasy;
  const score = nbExos > 0 ? Math.round((nbEasy / nbExos) * 100) : 0;
  const todayStr = todayParis();

  // Schéma progress : unique(code, categorie). onConflict doit matcher cet index.
  const { error: upErr } = await adminClient.from("progress").upsert({
    code, niveau: level, categorie,
    nb_exos: nbExos, nb_erreurs: nbErreurs, score,
    derniere_pratique: todayStr,
  }, { onConflict: "code,categorie" });
  if (upErr) console.error("updateConfidenceScore upsert error:", upErr);
}

// ── SAVE_CALIBRATION_BATCH ──────────────────────────────────

async function saveCalibrationBatch(p: Record<string, unknown>) {
  if (!p.code || !p.scores || !Array.isArray(p.scores))
    return { status: "error", message: "code et scores requis." };
  if (!(await mxAuth(p))) return MX_AUTH_REFUS; // Besoin API n°8

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

  // ── Choix du chapitre offert (free_chapter) ─────────────────
  // Refonte 10/04/2026 (audit 2026-04-11, porté de la prod le 25/09) : scoring pondéré par importance Brevet + tie-break explicite
  // + fallback Fonctions Affines pour élève fort (0 erreur).
  // Seulement si l'élève n'est pas premium et n'a pas encore de free_chapter.
  let freeChapter: string | null = null;
  const { data: prof } = await adminClient.from("profiles")
    .select("premium, free_chapter").eq("code", code).maybeSingle();

  if (prof && !prof.premium && !prof.free_chapter) {
    // Poids stratégiques Brevet (plus élevé = plus prioritaire si raté)
    const CALIB_WEIGHTS: Record<string, number> = {
      "fonctions_affines": 2.0,  // LE chapitre décisif Brevet
      "pythagore":         1.6,
      "thales":            1.6,
      "calcul_litteral":   1.5,
      "fractions":         1.4,
      "proportionnalite":  1.0,
      "puissances":        0.9,
    };
    // Ordre de priorité pour tie-break (1er gagne si scores égaux)
    const CALIB_PRIORITY = [
      "fonctions_affines", "thales", "pythagore", "calcul_litteral",
      "fractions", "proportionnalite", "puissances",
    ];
    // Normaliser un nom de chapitre pour matcher avec les clés de poids
    const normCalib = (s: string): string => {
      const n = s.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .toLowerCase().replace(/_brevet$/, "").replace(/_+$/, "")
        .replace(/_de_/g, "_").replace(/\s+/g, "_");
      for (const k of Object.keys(CALIB_WEIGHTS)) {
        if (n === k || n.includes(k) || k.includes(n)) return k;
      }
      return n;
    };

    const chapErrors: Record<string, { total: number; wrong: number; raw: string }> = {};
    for (const s of (p.scores as Record<string, unknown>[])) {
      // originalChapter contient le vrai chapitre (categorie = "CALIBRAGE" pour tous)
      const rawCat = String(s.originalChapter || s.categorie || "");
      if (!rawCat || rawCat === "CALIBRAGE") continue;
      const cat = normCalib(rawCat);
      if (!chapErrors[cat]) chapErrors[cat] = { total: 0, wrong: 0, raw: rawCat };
      chapErrors[cat].total++;
      if (String(s.resultat || "") !== "EASY") chapErrors[cat].wrong++;
    }

    // Score pondéré = wrong × poids (wrong = 0/1 avec 1 question par chapitre)
    let bestScore = -1;
    const tied: string[] = [];
    for (const [cat, stats] of Object.entries(chapErrors)) {
      const wrong = stats.wrong > 0 ? 1 : 0;
      const weight = CALIB_WEIGHTS[cat] ?? 1.0;
      const score = wrong * weight;
      if (score > bestScore) { bestScore = score; tied.length = 0; tied.push(cat); }
      else if (score === bestScore) { tied.push(cat); }
    }

    let weakestKey = "";
    if (bestScore > 0 && tied.length > 0) {
      // Tie-break par ordre de priorité explicite
      for (const pKey of CALIB_PRIORITY) {
        if (tied.includes(pKey)) { weakestKey = pKey; break; }
      }
      if (!weakestKey) weakestKey = tied[0];
    } else {
      // Fallback élève fort (0 erreur) → Fonctions Affines
      weakestKey = "fonctions_affines";
    }

    // Récupérer le nom brut original (ex: "Fonctions_Affines_Brevet") pour cohérence DB.
    // Si l'élève fort n'a pas vu cette catégorie, on fallback sur le nom canonique *_Brevet.
    const weakest = chapErrors[weakestKey]?.raw || "Fonctions_Affines_Brevet";
    await adminClient.from("profiles").update({ free_chapter: weakest }).eq("code", code);
    freeChapter = weakest;
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
  if (!(await mxAuth(p))) return MX_AUTH_REFUS; // Besoin API n°8

  // Single identity check for the whole batch — SELECT avec `mode`
  const { data: profile } = await adminClient.from("profiles")
    .select("email, mode, premium, premium_end, free_chapter").eq("code", code).maybeSingle();
  if (!profile) return { status: "error", message: "Élève introuvable." };

  // Hardening (P1 #7) : analyser les sources avant la gate freemium
  let _batchHasBoost = false;
  for (const s of (p.scores as Record<string, unknown>[])) {
    const src = String(s.source || "");
    if (src === "CALIBRAGE") {
      return { status: "error", message: "CALIBRAGE doit passer par save_calibration_batch." };
    }
    if (src === "BOOST") _batchHasBoost = true;
  }
  if (_batchHasBoost) {
    const todayStrBatch = todayParis();
    const { data: boostRow } = await adminClient.from("daily_boosts")
      .select("id").eq("code", code)
      .or(`date.eq.${todayStrBatch},exos_done.lt.5`)
      .order("date", { ascending: false }).limit(1).maybeSingle();
    if (!boostRow) {
      return { status: "error", message: "Aucun boost actif — source BOOST refusée." };
    }
  }

  // Freemium guard batch : mode lite OU premium OU BOOST (validé) OU free_chapter
  const _batchIsLite = (profile as Record<string, unknown>).mode === "lite";
  let _batchPremium = !!profile.premium;
  if (_batchPremium && profile.premium_end) {
    const endDate = String(profile.premium_end).substring(0, 10);
    if (endDate && endDate < todayParis()) _batchPremium = false;
  }
  if (!_batchIsLite && !_batchPremium) {
    for (const s of (p.scores as Record<string, unknown>[])) {
      const src = String(s.source || "");
      const cat = String(s.categorie || "");
      if (src === "BOOST") continue; // déjà gated par la vérif boost actif
      if (src === "LIBRE") return { status: "error", message: "Entraînement libre réservé au Programme Brevet.", paywall: "programme_brevet" };
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
  // FIX 2026-04-11 P0 (porté de la prod le 25/09) : onConflict doit matcher l'index unique (5 cols, pas 4).
  const { error: batchErr } = await adminClient.from("scores").upsert(rows, {
    onConflict: "code,chapitre,num_exo,date,source", ignoreDuplicates: true, // = idx_scores_dedup (schema.sql)
  });
  if (batchErr) {
    console.error("save_scores_batch upsert error:", batchErr);
    return { status: "error", message: "Erreur batch scores : " + batchErr.message };
  }

  // Moteur 3e : maîtrise par compétence — additif, seulement pour les exos portant item_id ou comp.
  for (const s of (p.scores as Record<string, unknown>[])) {
    if (!s.item_id && !s.comp) continue;
    try { await mxMajDepuisScore(code, s, ["BOOST", "LIBRE"].includes(String(s.source || "")) ? "train" : "legacy"); }
    catch (e) { console.error("[moteur] maj maîtrise save_scores_batch", e); }
  }

  // Batch progress updates — group by chapitre, only for non-BOOST non-CALIBRAGE non-LIBRE
  const chapCats = new Set<string>();
  let boostCount = 0;
  for (const s of (p.scores as Record<string, unknown>[])) {
    const src = String(s.source || "");
    if (src === "BOOST") { boostCount++; continue; }
    if (src === "CALIBRAGE" || src === "LIBRE") continue;
    const cat = String(s.categorie || "");
    if (cat) chapCats.add(cat);
  }

  // Update progress per chapter — recompute from scores table (source de vérité)
  // FIX 2026-04-11 P0 (porté de la prod le 25/09) : ne plus utiliser `progress.nb_easy` (colonne inexistante).
  for (const cat of chapCats) {
    const { data: scoreRows, error: selErr } = await adminClient.from("scores")
      .select("resultat, source")
      .eq("code", code).eq("chapitre", cat);
    if (selErr) { console.error("batch progress select error:", selErr); continue; }
    const rel = (scoreRows || []).filter((s: Record<string, unknown>) => {
      const src = String(s.source || "");
      return src !== "BOOST" && src !== "CALIBRAGE" && src !== "LIBRE";
    });
    const nbExos = rel.length;
    const nbEasy = rel.filter((s: Record<string, unknown>) => String(s.resultat) === "EASY").length;
    const nbErreurs = nbExos - nbEasy;
    const score = nbExos > 0 ? Math.round((nbEasy / nbExos) * 100) : 0;
    const { error: upErr } = await adminClient.from("progress").upsert({
      code, niveau: level, categorie: cat,
      nb_exos: nbExos, nb_erreurs: nbErreurs, score,
      derniere_pratique: todayStr,
    }, { onConflict: "code,categorie" });
    if (upErr) console.error("batch progress upsert error:", upErr);
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
  if (!(await mxAuth(p, { lectureAdmin: true }))) return MX_AUTH_REFUS; // Besoin API n°8
  const code = String(p.code);
  const { data } = await adminClient.from("progress").select("*").eq("code", code);
  return { status: "success", progress: data || [] };
}

// ── CHECK_TRIAL_STATUS ──────────────────────────────────────

async function checkTrialStatus(p: Record<string, unknown>) {
  if (!(await mxAuth(p, { lectureAdmin: true }))) return MX_AUTH_REFUS; // Besoin API n°8
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
  if (!(await mxAuth(p))) return MX_AUTH_REFUS; // Besoin API n°8

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

// ── GENERATE_ADAPTIVE_BOOST ──────────────────────────────────
// Moteur de sélection algorithmique du boost quotidien (5 exos), en remplacement
// de la génération LLM par élève (admin-auto). Pioche dans la banque statique
// `curriculum` en pondérant par lacune (progress.score) + exclut les exos déjà
// vus (par texte d'énoncé, cf. scores.enonce). Aucun appel LLM.
//
// Respecte G16 (J+1 non négociable) : écrit toujours dans daily_boosts avec
// date = demain. Additif — n'écrase pas le workflow admin/admin-auto existant,
// à tester en parallèle avant bascule (cf. CLAUDE.md "Moteur adaptatif").

type ExoQuestion = { num: number; q: string; a: unknown; type?: string; options?: unknown[]; steps?: unknown[]; f?: string; f_disabled?: boolean; lvl?: number };
type ExoParapluie = { id?: string; title?: string; context?: string; figure?: string; figure_desc?: string; questions: ExoQuestion[] };

function tomorrowParis(): string {
  const d = new Date(new Date().toLocaleString("en-US", { timeZone: "Europe/Paris" }));
  d.setDate(d.getDate() + 1);
  return d.toISOString().slice(0, 10);
}

function shuffleArr<T>(arr: T[]): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

async function generateAdaptiveBoost(p: Record<string, unknown>) {
  const code = String(p.code || "");
  if (code.length !== 6) return { status: "error", message: "code élève invalide." };
  if (!(await mxAuth(p, { lectureAdmin: true }))) return MX_AUTH_REFUS; // Besoin API n°8 (écrit daily_boosts : élève ou admin)

  const { data: profile } = await adminClient.from("profiles")
    .select("niveau").eq("code", code).maybeSingle();
  if (!profile) return { status: "error", message: "Élève introuvable." };
  const niveau = String(profile.niveau || "");

  // 1. Lacunes — chapitres du niveau triés par progress.score croissant (plus faible = prioritaire).
  //    Un chapitre jamais pratiqué (pas de ligne progress) reçoit un score neutre (50) : ni prioritaire
  //    ni ignoré, pour laisser une vraie lacune remonter avant un chapitre juste jamais commencé.
  const { data: curriculumRows } = await adminClient.from("curriculum")
    .select("categorie, exos_json").eq("niveau", niveau);
  if (!curriculumRows || curriculumRows.length === 0) {
    return { status: "error", message: "Aucun chapitre en banque pour ce niveau." };
  }

  const { data: progressRows } = await adminClient.from("progress")
    .select("categorie, score").eq("code", code);
  const scoreByChap: Record<string, number> = {};
  (progressRows || []).forEach((r: Record<string, unknown>) => { scoreByChap[String(r.categorie)] = Number(r.score) || 0; });

  const chapitresTries = curriculumRows
    .map((r: Record<string, unknown>) => ({ categorie: String(r.categorie), score: scoreByChap[String(r.categorie)] ?? 50 }))
    .sort((a, b) => a.score - b.score);

  // 2. Anti-doublon — tous les énoncés déjà servis à cet élève (curriculum + boost confondus).
  const { data: seenRows } = await adminClient.from("scores")
    .select("enonce").eq("code", code).not("enonce", "is", null);
  const seenEnonces = new Set((seenRows || []).map((r: Record<string, unknown>) => String(r.enonce || "").trim()).filter(Boolean));

  // 3. Pool pondéré — les 3 chapitres les plus faibles fournissent le gros du pool,
  //    avec un poids décroissant (le plus faible d'abord), le reste du niveau complète si besoin.
  const curByChap: Record<string, ExoParapluie[]> = {};
  curriculumRows.forEach((r: Record<string, unknown>) => {
    const exos = typeof r.exos_json === "string" ? JSON.parse(r.exos_json as string) : (r.exos_json || []);
    curByChap[String(r.categorie)] = exos as ExoParapluie[];
  });

  type Candidate = { categorie: string; q: ExoQuestion };
  const weighted: Candidate[] = [];
  const weights = [3, 2, 1]; // top-3 chapitres faibles sur-représentés dans le pool
  chapitresTries.forEach((c, idx) => {
    const parapluies = curByChap[c.categorie] || [];
    const questions: ExoQuestion[] = [];
    parapluies.forEach((par) => (par.questions || []).forEach((q) => questions.push(q)));
    const notSeen = questions.filter((q) => !seenEnonces.has(String(q.q || "").trim()));
    const repeat = idx < weights.length ? weights[idx] : 1;
    for (let i = 0; i < repeat; i++) notSeen.forEach((q) => weighted.push({ categorie: c.categorie, q }));
  });

  if (weighted.length === 0) {
    return { status: "error", message: "Banque épuisée pour cet élève sur ce niveau — réassort nécessaire." };
  }

  // 4. Tirage — 5 exos, en évitant les doublons du même exercice dans le même boost.
  const picked: Candidate[] = [];
  const usedQ = new Set<string>();
  for (const cand of shuffleArr(weighted)) {
    const key = cand.categorie + "|" + cand.q.num + "|" + cand.q.q;
    if (usedQ.has(key)) continue;
    usedQ.add(key);
    picked.push(cand);
    if (picked.length >= 5) break;
  }

  const boostJson = {
    generatedBy: "algo_v1",
    exos: picked.map((c, i) => ({ ...c.q, categorie: c.categorie, boostIdx: i })),
  };

  const tomorrow = tomorrowParis();
  const { data: existing } = await adminClient.from("daily_boosts")
    .select("id").eq("code", code).eq("date", tomorrow).maybeSingle();
  if (existing) {
    await adminClient.from("daily_boosts").update({ boost_json: boostJson, exos_done: 0 }).eq("id", existing.id);
  } else {
    await adminClient.from("daily_boosts").insert({ code, date: tomorrow, boost_json: boostJson, exos_done: 0 });
  }

  return { status: "success", niveau, chapitresCibles: chapitresTries.slice(0, 3).map((c) => c.categorie), nbExosPool: weighted.length, boost: boostJson };
}

// ════════════════════════════════════════════════════════════
// MOTEUR_PUR_DEBUT — Moteur « Diagnostic 3e » : diagnostic adaptatif,
// maîtrise par compétence, carte, entraînement, droits d'accès.
// Spec : docs/specs/20-moteur.md · Contrat : docs/specs/00-contrat-commun.md §3-5
//
// LOGIQUE PURE : aucune I/O ici (ni adminClient, ni Deno, ni fetch, ni Math.random,
// ni new Date() sans argument). Tout est déterministe à entrées égales.
// Ce bloc est extrait tel quel et testé par supabase/tests/moteur_test.ts :
// ne rien y référencer qui soit défini hors du bloc.
// ════════════════════════════════════════════════════════════

type MxErreurRef = { id: string; libelle: string; libelle_parent?: string; remediation?: string };
type MxComp = {
  id: string; domaine: string; theme?: string; titre: string; titre_eleve?: string;
  niveau_origine: string; prerequis: string[]; poids_brevet: number;
  chapitres_legacy?: string[]; erreurs?: MxErreurRef[];
  diag_autorise?: boolean; hors_programme?: boolean; diag?: boolean; // diag: false = jamais en diagnostic (contrat §9)
};
type MxItem = {
  id: string; comp: string; q: string; a: string; type?: string; options?: string[];
  alt?: string[]; err?: Record<string, string>; steps?: string[]; f?: string;
  lvl?: number; usage?: string[]; contexte?: boolean; [k: string]: unknown;
};
type MxObs = {
  item_id: string; comp: string; ok: boolean; w: number;
  reponse?: string; err?: string | null; temps?: number | null; date?: string; graine?: boolean;
  imputee?: boolean; // erreur d'un prérequis direct imputée à ce prérequis (contrat §9)
};
type MxMaitrise = {
  comp: string; alpha: number; beta: number; maitrise: number; n_obs: number; n_succes: number;
  derniere_obs: string | null; erreurs_vues: Record<string, number>;
  boite: number; prochaine_revision: string | null;
};
type MxStatut = "lacune" | "fragile" | "acquis" | "non_evalue";
type MxRef = {
  comps: Record<string, MxComp>;
  ordre: string[];
  enfants: Record<string, string[]>;
  ancetres: Record<string, string[]>;     // tous les prérequis (fermeture transitive)
  descendants: Record<string, string[]>;  // tout ce qui en dépend (fermeture transitive)
  anc2: Record<string, string[]>;         // prérequis à distance 1 ou 2
  desc2: Record<string, string[]>;        // dépendants à distance 1 ou 2
  items: Record<string, MxItem>;
  itemsParComp: Record<string, MxItem[]>;
};
type MxModule = { domaines: string[]; cibles: string[]; bonus: string[]; budget: number; poses: number; termine: boolean };
type MxEtatDiag = {
  version: 1; type: string; code: string;
  module: number; modules: MxModule[];
  obs: MxObs[];
  pile: string[]; differes: string[];
  ouverte: string | null; en_attente: string | null;
  fermees: Record<string, MxStatut>;
  profondeur: Record<string, number>;
  phase: "balayage" | "descente";
  termine: boolean;
};
type MxDiagCfg = {
  modules: { domaines: string[]; budget: number }[];
  maxObsCible: number; // nb max de questions sur une cible 3e (profondeur 0)
  maxObs: number;      // nb max de questions sur un prérequis exploré en descente
  minObsLacune: number; // nb min d'observations pour conclure « lacune » (robustesse aux étourderies)
  profondeurMax: number; descenteImmediate: boolean;
  seuilDescente: number; // une clôture « fragile » avec maîtrise < seuil déclenche aussi la descente
};

const MX_DOMAINES: [string, string][] = [
  ["NC", "Nombres et calculs"],
  ["DF", "Organisation et gestion de données, fonctions"],
  ["GM", "Grandeurs et mesures"],
  ["EG", "Espace et géométrie"],
  ["AP", "Algorithmique et programmation"],
];
const MX_TOUS_DOMAINES = MX_DOMAINES.map((d) => d[0]);
// Compétences hors programme (contrat §8) : entraînement seulement, JAMAIS en diagnostic,
// même si un item est marqué `diag`. Complété par competences.diag_autorise = false en base.
const MX_HORS_DIAG = ["NC.RAC.03", "NC.RAC.04", "EG.REP.02"];

const MX = {
  SEUIL_LACUNE: 0.4,          // contrat §4
  SEUIL_ACQUIS: 0.7,          // contrat §4
  OBS_MIN: 2,                 // jamais de conclusion sur 1 seule réponse
  PRIOR: 1,                   // Beta(1,1) : maîtrise initiale 0.5, sans avis
  OUBLI: 0.9,                 // maîtrise globale : chaque nouvelle obs « vieillit » les précédentes (×0.9)
  REVISION_JOURS: [2, 4, 8, 16, 32], // répétition espacée (boîtes de Leitner)
  REDIAG_JOURS: 30,           // re-diagnostic mensuel
  TEMPS_SUSPECT_SEC: 4,       // réponse plus rapide = probablement au hasard
  EXOS_PAR_JOUR: 5,
  DIAG: {
    express: {
      modules: [{ domaines: MX_TOUS_DOMAINES, budget: 15 }],
      maxObsCible: 2, maxObs: 3, minObsLacune: 2, profondeurMax: 2, descenteImmediate: false, seuilDescente: 0.5,
    },
    complet: {
      modules: [
        { domaines: ["NC"], budget: 24 },
        { domaines: ["DF", "AP"], budget: 20 },
        { domaines: ["EG", "GM"], budget: 20 },
      ],
      maxObsCible: 3, maxObs: 4, minObsLacune: 3, profondeurMax: 2, descenteImmediate: true, seuilDescente: 0.6,
    },
    mensuel: {
      modules: [{ domaines: MX_TOUS_DOMAINES, budget: 20 }],
      maxObsCible: 2, maxObs: 3, minObsLacune: 2, profondeurMax: 2, descenteImmediate: true, seuilDescente: 0.5,
    },
  } as Record<string, MxDiagCfg>,
};

// Prix : SEUL endroit où ils sont codés (contrat « Hypothèses de prix »). Les montants
// réellement encaissés sont ceux des Payment Links Stripe — garder les deux alignés.
const MX_PRODUITS: Record<string, { libelle: string; prix_cents: number; deduction?: { si: string; cents: number } }> = {
  diagnostic_complet: { libelle: "Diagnostic complet", prix_cents: 1900 },
  programme_brevet: { libelle: "Programme Brevet", prix_cents: 4900, deduction: { si: "diagnostic_complet", cents: 1900 } },
};

// ── Utilitaires ─────────────────────────────────────────────

function mxHash(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

function mxR(x: number, d = 4): number { const k = Math.pow(10, d); return Math.round(x * k) / k; }

function mxAjoutJours(date: string, n: number): string {
  const d = new Date(date.slice(0, 10) + "T00:00:00Z");
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

function mxJoursEntre(a: string, b: string): number {
  const da = Date.parse(a.slice(0, 10) + "T00:00:00Z"), db = Date.parse(b.slice(0, 10) + "T00:00:00Z");
  return Math.round((db - da) / 86400000);
}

function mxNiveauLabel(n: string): string {
  return ({ "6EME": "6e", "5EME": "5e", "4EME": "4e", "3EME": "3e" } as Record<string, string>)[n] || n;
}

// Normalisation des réponses — portage fidèle de _normFill/_toNum/_matchFill (app.html)
function mxNorm(s: unknown): string {
  let v = String(s ?? "").replace(/\$/g, "").replace(/\{,\}/g, ",").replace(/\\,/g, "").replace(/\s+/g, "")
    .replace(/,/g, ".").toLowerCase().trim();
  // moins Unicode (clavier iOS, copier-coller) → « - » ; préfixe « x= » / « a= » retiré (aligné app.html)
  v = v.replace(/[\u2212\u2013]/g, "-").replace(/^[a-z]=/, "");
  v = v.replace(/\\d?frac\{([^}]*)\}\{([^}]*)\}/g, "$1/$2");
  v = v.replace(/\\times/g, "×").replace(/\\cdot/g, "·").replace(/\\div/g, "÷");
  v = v.replace(/\\text\{([^}]*)\}/g, "$1").replace(/\\(left|right|displaystyle|,|;|!|quad)/g, "");
  v = v.replace(/\^\{([^}]*)\}/g, "^$1").replace(/\^\(([^)]*)\)/g, "^$1");
  v = v.replace(/\\sqrt\{([^}]*)\}/g, "sqrt($1)").replace(/(\d)sqrt/g, "$1*sqrt");
  v = v.replace(/\*/g, "×").replace(/(\d)x(?=[\d(s])/g, "$1×");
  return v;
}

// Valeur numérique STRICTE (même règle que _toNum d'app.html depuis le correctif « 4x+3 ») :
// jamais de parseFloat sur une entrée libre, seulement sur une chaîne entièrement numérique.
const MX_NOMBRE = "-?(?:\\d+\\.?\\d*|\\.\\d+)";
function mxNum(s: unknown): number | null {
  const v = mxNorm(s);
  const pct = v.match(new RegExp("^(" + MX_NOMBRE + ")%$"));
  if (pct) return parseFloat(pct[1]) / 100;
  const frac = v.match(new RegExp("^(" + MX_NOMBRE + ")/(" + MX_NOMBRE + ")$"));
  if (frac) return parseFloat(frac[2]) !== 0 ? parseFloat(frac[1]) / parseFloat(frac[2]) : null;
  const sansUnite = v.replace(/(mm|cm|dm|km|m|g|kg|l|cl|ml|s|min|h|€|°)(²|³|\^2|\^3)?$/, "");
  return new RegExp("^" + MX_NOMBRE + "$").test(sansUnite) ? parseFloat(sansUnite) : null;
}

function mxEgal(u: unknown, c: unknown, alt?: string[]): boolean {
  const nu = mxNorm(u), nc = mxNorm(c);
  if (!nu) return false;
  if (nu === nc) return true;
  const vf: Record<string, string> = { oui: "vrai", non: "faux", yes: "vrai", no: "faux", v: "vrai", f: "faux" };
  if (vf[nu] === nc || nu === vf[nc]) return true;
  const a = mxNum(u), b = mxNum(c);
  if (a !== null && b !== null && Math.abs(a - b) < 1e-9) return true;
  return !!alt && alt.some((x) => mxEgal(u, x));
}

function mxTypeItem(it: { type?: string; options?: unknown[] }): "qcm" | "vf" | "fill" {
  if (it.type === "vf" || it.type === "fill" || it.type === "qcm") return it.type;
  return (it.options || []).length ? "qcm" : "fill";
}

// Poids d'un SUCCÈS : un QCM à k options se réussit par hasard 1 fois sur k → ne vaut
// que 1 - 1/k d'une réussite « pleine ». Un échec vaut toujours 1 (contrat §4 / P8).
function mxPoidsSucces(it: { type?: string; options?: unknown[] }): number {
  const t = mxTypeItem(it);
  if (t === "fill") return 1;
  if (t === "vf") return 0.5;
  const k = (it.options || []).length;
  return k >= 2 ? Math.max(0.5, 1 - 1 / k) : 1;
}

function mxErreurType(it: MxItem, reponse: string): string | null {
  for (const [k, v] of Object.entries(it.err || {})) if (mxEgal(reponse, k)) return v;
  return null;
}

// Réponse vide / null = « je ne sais pas » = échec sans erreur type.
function mxCorriger(it: MxItem, reponse: unknown): { ok: boolean; err: string | null } {
  const r = reponse == null ? "" : String(reponse).trim();
  if (!r) return { ok: false, err: null };
  if (mxEgal(r, it.a, it.alt)) return { ok: true, err: null };
  return { ok: false, err: mxErreurType(it, r) };
}

// Observations à appliquer pour UNE réponse : la compétence de l'item, et — si l'erreur type
// appartient à un prérequis DIRECT de cette compétence — un échec imputé à ce prérequis (contrat §9).
function mxImputer(ref: MxRef | null, it: MxItem, ok: boolean, err: string | null) {
  const out: { comp: string; ok: boolean; err: string | null; imputee: boolean }[] = [];
  const compErr = err ? err.split("#")[0] : null;
  const versPrerequis = !!(compErr && compErr !== it.comp && ref && ref.comps[it.comp]?.prerequis.includes(compErr));
  out.push({ comp: it.comp, ok, err: versPrerequis ? null : err, imputee: false });
  if (versPrerequis) out.push({ comp: compErr!, ok: false, err, imputee: true });
  return out;
}

// ── Référentiel ─────────────────────────────────────────────

function mxIndexer(comps: MxComp[], items: MxItem[]): MxRef {
  const map: Record<string, MxComp> = {};
  for (const c of comps) map[c.id] = { ...c, prerequis: (c.prerequis || []).filter((p) => p && p !== c.id) };
  const ordre = Object.keys(map).sort();
  const enfants: Record<string, string[]> = {};
  ordre.forEach((id) => (enfants[id] = []));
  for (const id of ordre) for (const p of map[id].prerequis) if (map[p]) enfants[p].push(id);
  // Fermeture transitive tolérante aux cycles (un cycle ne boucle pas, il est juste ignoré)
  const fermeture = (start: string, suiv: (x: string) => string[]): string[] => {
    const vus = new Set<string>();
    const pile = [...suiv(start)];
    while (pile.length) {
      const x = pile.pop()!;
      if (x === start || vus.has(x) || !map[x]) continue;
      vus.add(x);
      pile.push(...suiv(x));
    }
    return [...vus].sort();
  };
  const ancetres: Record<string, string[]> = {}, descendants: Record<string, string[]> = {};
  const anc2: Record<string, string[]> = {}, desc2: Record<string, string[]> = {};
  const deuxNiveaux = (id: string, suiv: (x: string) => string[]) =>
    [...new Set([...suiv(id), ...suiv(id).flatMap(suiv)])].filter((x) => x !== id && map[x]).sort();
  for (const id of ordre) {
    ancetres[id] = fermeture(id, (x) => map[x]?.prerequis || []);
    descendants[id] = fermeture(id, (x) => enfants[x] || []);
    anc2[id] = deuxNiveaux(id, (x) => (map[x]?.prerequis || []).filter((p) => map[p]));
    desc2[id] = deuxNiveaux(id, (x) => enfants[x] || []);
  }
  const itemsMap: Record<string, MxItem> = {};
  const itemsParComp: Record<string, MxItem[]> = {};
  ordre.forEach((id) => (itemsParComp[id] = []));
  for (const it of items) {
    if (!it || !it.id || !map[it.comp]) continue;
    itemsMap[it.id] = it;
    // Une sous-question qui dépend de la précédente n'a de sens que dans son problème complet :
    // jamais servie seule (ni en diagnostic, ni en entraînement quotidien).
    if (it.depend_question_precedente) continue;
    itemsParComp[it.comp].push(it);
  }
  for (const id of ordre) itemsParComp[id].sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  return { comps: map, ordre, enfants, ancetres, descendants, anc2, desc2, items: itemsMap, itemsParComp };
}

// Détecte un cycle dans les prérequis (le contrat exige un graphe acyclique).
function mxCycles(ref: MxRef): string[] {
  return ref.ordre.filter((id) => ref.ancetres[id].some((a) => ref.ancetres[a].includes(id)) ||
    ref.comps[id].prerequis.some((p) => ref.ancetres[p]?.includes(id)));
}

// ── Maîtrise (contrat §4) ───────────────────────────────────

function mxMaitriseVide(comp: string): MxMaitrise {
  return { comp, alpha: MX.PRIOR, beta: MX.PRIOR, maitrise: 0.5, n_obs: 0, n_succes: 0,
    derniere_obs: null, erreurs_vues: {}, boite: 0, prochaine_revision: null };
}

function mxStatut(m?: { maitrise: number; n_obs: number } | null): MxStatut {
  if (!m || m.n_obs < MX.OBS_MIN) return "non_evalue";
  if (m.maitrise < MX.SEUIL_LACUNE) return "lacune";
  if (m.maitrise <= MX.SEUIL_ACQUIS) return "fragile";
  return "acquis";
}

// Mise à jour après UNE réponse (diagnostic comme entraînement).
// Modèle : Beta(alpha, beta) avec oubli exponentiel ; maîtrise = alpha / (alpha + beta).
function mxMajMaitrise(m0: MxMaitrise | undefined | null, comp: string, ok: boolean, w: number,
  err: string | null, date: string, oubli: number = MX.OUBLI): MxMaitrise {
  const m: MxMaitrise = m0 ? { ...m0, erreurs_vues: { ...(m0.erreurs_vues || {}) } } : mxMaitriseVide(comp);
  const P = MX.PRIOR;
  m.alpha = mxR(P + (m.alpha - P) * oubli + (ok ? w : 0));
  m.beta = mxR(P + (m.beta - P) * oubli + (ok ? 0 : 1));
  m.maitrise = mxR(m.alpha / (m.alpha + m.beta));
  m.n_obs += 1;
  if (ok) m.n_succes += 1;
  if (err) m.erreurs_vues[err] = (m.erreurs_vues[err] || 0) + 1;
  m.derniere_obs = date;
  const acquis = mxStatut(m) === "acquis";
  if (!ok) {
    m.boite = 0;
    m.prochaine_revision = acquis ? mxAjoutJours(date, 1) : null;
  } else if (acquis) {
    const b = Math.min(m.boite, MX.REVISION_JOURS.length - 1);
    m.prochaine_revision = mxAjoutJours(date, MX.REVISION_JOURS[b]);
    m.boite = Math.min(m.boite + 1, MX.REVISION_JOURS.length - 1);
  } else {
    m.prochaine_revision = null;
  }
  return m;
}

// ── Diagnostic adaptatif ────────────────────────────────────

function mxTriCibles(ref: MxRef, ids: string[]): string[] {
  return ids.slice().sort((a, b) => {
    const ca = ref.comps[a], cb = ref.comps[b];
    return (cb.poids_brevet - ca.poids_brevet) ||
      (ref.ancetres[b].length - ref.ancetres[a].length) || (a < b ? -1 : a > b ? 1 : 0);
  });
}

function mxDiagAutorise(ref: MxRef, c: string): boolean {
  const comp = ref.comps[c];
  return !!comp && comp.diag_autorise !== false && comp.diag !== false && !comp.hors_programme && !MX_HORS_DIAG.includes(c);
}

// Cibles d'un ensemble de domaines : les compétences de 3e (avec items). Un domaine sans compétence
// de 3e (ex. AP dans le référentiel réel) prend ses compétences du plus haut niveau disponible.
function mxCibles3e(ref: MxRef, domaines: string[]): string[] {
  const rangNiv: Record<string, number> = { "3EME": 3, "4EME": 2, "5EME": 1, "6EME": 0 };
  const out: string[] = [];
  for (const d of domaines) {
    const ids = ref.ordre.filter((id) => ref.comps[id].domaine === d && (ref.itemsParComp[id] || []).length > 0 &&
      mxDiagAutorise(ref, id));
    const top = Math.max(-1, ...ids.map((id) => rangNiv[ref.comps[id].niveau_origine] ?? 0));
    out.push(...ids.filter((id) => (rangNiv[ref.comps[id].niveau_origine] ?? 0) === top));
  }
  return mxTriCibles(ref, out);
}

function mxEvalSession(etat: MxEtatDiag, comp: string): { m: number; n: number } {
  let a = MX.PRIOR, b = MX.PRIOR, n = 0;
  for (const o of etat.obs) if (o.comp === comp) { n++; if (o.ok) a += o.w; else b += 1; }
  return { m: a / (a + b), n };
}

// null = continuer à interroger ; sinon statut de clôture. maxObs = 0 → clôture forcée.
function mxDecider(m: number, n: number, maxObs: number, minObsLacune: number = MX.OBS_MIN): MxStatut | null {
  if (n < MX.OBS_MIN) return maxObs === 0 ? "non_evalue" : null;
  if (m > MX.SEUIL_ACQUIS) return "acquis";
  if (m < MX.SEUIL_LACUNE && (n >= minObsLacune || maxObs === 0 || n >= maxObs)) return "lacune";
  if (m < MX.SEUIL_LACUNE) return null;
  if (maxObs === 0 || n >= maxObs) return "fragile";
  return null;
}

// Seuils d'arrêt pour une compétence. Si un de ses dépendants directs vient d'être jugé acquis,
// une lacune serait incohérente (probable étourderie) : on exige une observation de plus.
function mxSeuils(etat: MxEtatDiag, ref: MxRef, c: string): { maxObs: number; minLac: number } {
  const cfg = MX.DIAG[etat.type];
  const base = (etat.profondeur[c] || 0) === 0 ? cfg.maxObsCible : cfg.maxObs;
  const contredit = (ref.enfants[c] || []).some((e) => etat.fermees[e] === "acquis");
  const minLac = cfg.minObsLacune + (contredit ? 1 : 0);
  return { maxObs: Math.max(base, minLac), minLac };
}

function mxPousserPrerequis(etat: MxEtatDiag, ref: MxRef, c: string) {
  const cfg = MX.DIAG[etat.type];
  const prof = (etat.profondeur[c] || 0) + 1;
  if (prof > cfg.profondeurMax) return;
  const aTester = (ref.comps[c]?.prerequis || []).filter((p) => ref.comps[p] && !(p in etat.fermees) &&
    (ref.itemsParComp[p] || []).length > 0 && mxDiagAutorise(ref, p));
  // Le plus « structurant » (poids + nb de dépendants) sera dépilé en premier.
  aTester.sort((a, b) =>
    (ref.comps[a].poids_brevet + ref.desc2[a].length) - (ref.comps[b].poids_brevet + ref.desc2[b].length) ||
    (a < b ? 1 : a > b ? -1 : 0));
  for (const p of aTester) {
    etat.pile = etat.pile.filter((x) => x !== p);
    etat.pile.push(p);
    etat.profondeur[p] = Math.min(etat.profondeur[p] ?? 99, prof);
  }
}

function mxFermer(etat: MxEtatDiag, ref: MxRef, c: string, force: boolean) {
  const cfg = MX.DIAG[etat.type];
  const { m, n } = mxEvalSession(etat, c);
  const se = mxSeuils(etat, ref, c);
  const d = mxDecider(m, n, force ? 0 : se.maxObs, se.minLac) || "fragile";
  etat.fermees[c] = d;
  if (etat.ouverte === c) etat.ouverte = null;
  // On ne descend dans les prérequis qu'à partir d'un échec sur une compétence de 3e
  // (ou en poursuivant une descente déjà commencée depuis une compétence de 3e).
  const depuis3e = ref.comps[c].niveau_origine === "3EME" || (etat.profondeur[c] || 0) > 0;
  const descendre = depuis3e && (d === "lacune" || (d === "fragile" && m < cfg.seuilDescente));
  if (!descendre) return;
  if (cfg.descenteImmediate || etat.phase === "descente") mxPousserPrerequis(etat, ref, c);
  else etat.differes.push(c);
}

function mxDemarrerDiag(ref: MxRef, type: string, code: string,
  opts: { graines?: MxObs[]; maitrise?: Record<string, MxMaitrise>; date?: string } = {}): MxEtatDiag {
  const cfg = MX.DIAG[type];
  if (!cfg) throw new Error("type de diagnostic inconnu : " + type);
  const modules: MxModule[] = cfg.modules.map((m) => ({ domaines: m.domaines, cibles: [], bonus: [], budget: m.budget, poses: 0, termine: false }));
  if (type === "express") {
    // 1 cible par domaine (la plus lourde au Brevet), domaines ordonnés par leur meilleure cible ;
    // les autres cibles 3e ne servent que s'il reste du budget après la descente.
    const parDomaine = MX_TOUS_DOMAINES.map((d) => mxCibles3e(ref, [d])).filter((l) => l.length > 0);
    const premieres = mxTriCibles(ref, parDomaine.map((l) => l[0]));
    modules[0].cibles = premieres;
    modules[0].bonus = mxTriCibles(ref, parDomaine.flatMap((l) => l.slice(1)));
  } else if (type === "mensuel" && opts.maitrise) {
    const mt = opts.maitrise;
    const prios = mxPriorites(ref, mt).filter((id) => mxDiagAutorise(ref, id)).slice(0, 8);
    const acquis = ref.ordre.filter((id) => mxStatut(mt[id]) === "acquis" && (ref.itemsParComp[id] || []).length && mxDiagAutorise(ref, id))
      .sort((a, b) => (String(mt[a].derniere_obs) < String(mt[b].derniere_obs) ? -1 : 1)).slice(0, 4);
    const neufs = mxCibles3e(ref, MX_TOUS_DOMAINES).filter((id) => mxStatut(mt[id]) === "non_evalue").slice(0, 4);
    modules[0].cibles = [...new Set([...prios, ...acquis, ...neufs])];
  } else {
    for (const mod of modules) mod.cibles = mxCibles3e(ref, mod.domaines);
  }
  const etat: MxEtatDiag = {
    version: 1, type, code, module: 0, modules, obs: [], pile: [], differes: [],
    ouverte: null, en_attente: null, fermees: {}, profondeur: {},
    phase: cfg.descenteImmediate ? "descente" : "balayage", termine: false,
  };
  for (const mod of modules) for (const c of mod.cibles) etat.profondeur[c] = 0;
  // Graines (express → complet) : observations déjà faites, hors budget.
  if (opts.graines && opts.graines.length) {
    etat.obs = opts.graines.filter((o) => ref.comps[o.comp]).map((o) => ({ ...o, graine: true }));
    const compsVus = [...new Set(etat.obs.map((o) => o.comp))].sort();
    const lacunes: string[] = [];
    for (const c of compsVus) {
      const { m, n } = mxEvalSession(etat, c);
      // un prérequis (non 3e) reste ouvert jusqu'à maxObs : la descente pourra le re-questionner
      const d = mxDecider(m, n, ref.comps[c].niveau_origine === "3EME" ? cfg.maxObsCible : cfg.maxObs, cfg.minObsLacune);
      const depuis3e = ref.comps[c].niveau_origine === "3EME" || (etat.profondeur[c] || 0) > 0;
      if (d) { etat.fermees[c] = d; if (depuis3e && (d === "lacune" || (d === "fragile" && m < cfg.seuilDescente))) lacunes.push(c); }
    }
    // On reprend la descente là où l'express l'a laissée (lacunes les plus lourdes en haut de pile).
    lacunes.sort((a, b) => ref.comps[a].poids_brevet - ref.comps[b].poids_brevet || (a < b ? 1 : -1));
    for (const c of lacunes) mxPousserPrerequis(etat, ref, c);
  }
  return etat;
}

function mxChoisirItemDiag(etat: MxEtatDiag, ref: MxRef, c: string, dejaVus: string[]): MxItem | null {
  if (!mxDiagAutorise(ref, c)) return null;
  const poses = new Set(etat.obs.map((o) => o.item_id));
  let cands = (ref.itemsParComp[c] || []).filter((it) => !poses.has(it.id));
  const pourDiag = cands.filter((it) => !it.usage || it.usage.includes("diag"));
  if (pourDiag.length) cands = pourDiag;
  if (!cands.length) return null;
  const obsC = etat.obs.filter((o) => o.comp === c);
  const derniere = obsC[obsC.length - 1];
  const veutFill = !!derniere && derniere.ok && derniere.w < 1; // confirmer un succès QCM par une réponse ouverte
  const lvlPref = ref.comps[c].niveau_origine === "3EME" ? 2 : 1;
  const vus = new Set(dejaVus);
  const score = (it: MxItem) => (vus.has(it.id) ? 100 : 0) + Math.abs((it.lvl || 1) - lvlPref) * 3 +
    (veutFill && mxTypeItem(it) !== "fill" ? 5 : 0) + (mxTypeItem(it) !== "fill" ? 1 : 0) + (it.contexte ? 1 : 0);
  cands.sort((a, b) => score(a) - score(b) || mxHash(etat.code + "|" + a.id) - mxHash(etat.code + "|" + b.id));
  return cands[0];
}

function mxTacheSuivante(etat: MxEtatDiag, ref: MxRef, mod: MxModule): string | null {
  const libre = (c: string) => !!ref.comps[c] && !(c in etat.fermees);
  if (etat.phase === "descente") {
    while (etat.pile.length) { const c = etat.pile.pop()!; if (libre(c)) return c; }
  }
  for (const c of mod.cibles) if (libre(c)) return c;
  if (etat.phase === "balayage") {
    // Express : balayage des domaines terminé → on creuse la lacune la plus lourde d'abord.
    etat.phase = "descente";
    const prio = (c: string) => ref.comps[c].poids_brevet * (1 - mxEvalSession(etat, c).m);
    const lac = etat.differes.slice().sort((a, b) => prio(a) - prio(b) || (a < b ? 1 : -1));
    etat.differes = [];
    for (const c of lac) mxPousserPrerequis(etat, ref, c);
    return mxTacheSuivante(etat, ref, mod);
  }
  for (const c of mod.bonus) if (libre(c)) { etat.profondeur[c] = 0; return c; }
  return null;
}

type MxQuestion = { item: MxItem } | { fin_module: number } | { fin: true };

function mxProchaineQuestion(etat: MxEtatDiag, ref: MxRef, dejaVus: string[] = []): MxQuestion {
  if (etat.termine) return { fin: true };
  if (etat.en_attente) {
    const it = ref.items[etat.en_attente];
    if (it) return { item: it };
    etat.en_attente = null;
  }
  for (let garde = 0; garde < 10000; garde++) {
    const mod = etat.modules[etat.module];
    if (!mod) { etat.termine = true; return { fin: true }; }
    if (mod.termine || mod.poses >= mod.budget) {
      mod.termine = true;
      if (etat.ouverte) mxFermer(etat, ref, etat.ouverte, true);
      etat.module++;
      if (etat.module >= etat.modules.length) { etat.termine = true; return { fin: true }; }
      return { fin_module: etat.module }; // index (0-based) du module suivant — reprenable plus tard
    }
    let c = etat.ouverte;
    if (!c) c = mxTacheSuivante(etat, ref, mod);
    if (!c) { mod.termine = true; continue; }
    etat.ouverte = c;
    const it = mxChoisirItemDiag(etat, ref, c, dejaVus);
    if (!it) { mxFermer(etat, ref, c, true); continue; }
    etat.en_attente = it.id;
    return { item: it };
  }
  etat.termine = true;
  return { fin: true };
}

function mxEnregistrerReponse(etat: MxEtatDiag, ref: MxRef, itemId: string, reponse: unknown,
  temps: number | null, date: string): { error: string } | { obs: MxObs; item: MxItem; imputations: MxObs[] } {
  if (!etat.en_attente || etat.en_attente !== itemId) return { error: "Question inattendue (déjà répondue ou non posée)." };
  const it = ref.items[itemId];
  if (!it) return { error: "Item introuvable." };
  const { ok, err } = mxCorriger(it, reponse);
  const obs: MxObs = { item_id: it.id, comp: it.comp, ok, w: mxPoidsSucces(it),
    reponse: String(reponse ?? "").slice(0, 100), err, temps, date };
  const imputations = mxImputer(ref, it, ok, err);
  if (imputations.length > 1) obs.err = null; // l'erreur est portée par l'observation imputée
  etat.obs.push(obs);
  for (const im of imputations.slice(1)) {
    etat.obs.push({ item_id: it.id, comp: im.comp, ok: false, w: 1, reponse: obs.reponse, err: im.err, temps, date, imputee: true });
  }
  etat.en_attente = null;
  etat.modules[etat.module].poses++;
  const { m, n } = mxEvalSession(etat, it.comp);
  const se = mxSeuils(etat, ref, it.comp);
  if (mxDecider(m, n, se.maxObs, se.minLac)) mxFermer(etat, ref, it.comp, false);
  return { obs, item: it, imputations: etat.obs.slice(etat.obs.length - imputations.length) };
}

function mxProgression(etat: MxEtatDiag) {
  const mod = etat.modules[Math.min(etat.module, etat.modules.length - 1)];
  return {
    module: Math.min(etat.module, etat.modules.length - 1) + 1, n_modules: etat.modules.length,
    poses_module: mod.poses, budget_module: mod.budget,
    poses_total: etat.modules.reduce((s, m) => s + m.poses, 0),
    budget_total: etat.modules.reduce((s, m) => s + m.budget, 0),
    termine: etat.termine,
  };
}

// ── Carte (contrat §5) ──────────────────────────────────────

function mxAnalyse(ref: MxRef, mt: Record<string, MxMaitrise>) {
  const st: Record<string, MxStatut> = {};
  for (const id of ref.ordre) st[id] = mxStatut(mt[id]);
  const lac = new Set(ref.ordre.filter((id) => st[id] === "lacune"));
  // Recommandation didacticien : le graphe complet est trop large (NC.ENT.02 atteint 66 compétences),
  // on ne raisonne que sur les voisins à distance 1 ou 2.
  const causeRacine = (id: string) => lac.has(id) && ref.desc2[id].some((d) => lac.has(d));
  const racineProfonde = (id: string) => lac.has(id) && !ref.anc2[id].some((a) => lac.has(a));
  const bloque = (id: string) => ref.desc2[id].filter((d) => st[d] === "lacune" || st[d] === "fragile")
    .sort((a, b) => ref.comps[b].poids_brevet - ref.comps[a].poids_brevet || (a < b ? -1 : 1));
  return { st, causeRacine, racineProfonde, bloque };
}

// Ordre = cause racine × poids Brevet × lacune, puis tri topologique : un prérequis EN LACUNE
// (distance ≤ 2) passe toujours avant ce qu'il débloque (un prérequis seulement fragile ne bloque pas).
function mxPriorites(ref: MxRef, mt: Record<string, MxMaitrise>): string[] {
  const A = mxAnalyse(ref, mt);
  const cands = ref.ordre.filter((id) => A.st[id] === "lacune" || A.st[id] === "fragile");
  const score: Record<string, number> = {};
  for (const c of cands) {
    const facteur = A.causeRacine(c) ? (A.racineProfonde(c) ? 2 : 1.5) : 1;
    // le bonus « ce qu'elle débloque » ne compte que pour une cause racine confirmée (lacune qui bloque des lacunes)
    const impact = ref.comps[c].poids_brevet +
      (A.causeRacine(c) ? A.bloque(c).reduce((s, d) => s + ref.comps[d].poids_brevet, 0) : 0);
    score[c] = (1 - mt[c].maitrise) * facteur * impact;
  }
  let restant = cands.sort((a, b) => score[b] - score[a] || (a < b ? -1 : 1));
  const res: string[] = [];
  while (restant.length) {
    const c = restant.find((x) => !ref.anc2[x].some((a) => A.st[a] === "lacune" && restant.includes(a))) || restant[0];
    res.push(c);
    restant = restant.filter((x) => x !== c);
  }
  return res;
}

function mxPlan4Semaines(ref: MxRef, mt: Record<string, MxMaitrise>, prios: string[]) {
  const A = mxAnalyse(ref, mt);
  const titre = (id: string) => ref.comps[id].titre_eleve || ref.comps[id].titre;
  const plan: { semaine: number; focus: string[]; objectif: string }[] = [];
  let i = 0;
  for (let s = 1; s <= 4; s++) {
    const focus: string[] = [];
    let charge = 0;
    while (i < prios.length && charge < 2) {
      focus.push(prios[i]);
      charge += A.st[prios[i]] === "lacune" ? 1 : 0.5;
      i++;
    }
    let objectif: string;
    if (!focus.length) objectif = "Entretenir les acquis (révisions espacées) et s'entraîner sur des sujets type Brevet";
    else if (A.causeRacine(focus[0])) objectif = "Reconstruire la base : " + focus.map(titre).join(" ; ");
    else objectif = "Travailler : " + focus.map(titre).join(" ; ");
    plan.push({ semaine: s, focus, objectif });
  }
  return plan;
}

function mxFiabilite(ref: MxRef, st: Record<string, MxStatut>, obs: MxObs[]) {
  const reelles = obs.filter((o) => !o.graine && !o.imputee);
  const avecTemps = reelles.filter((o) => typeof o.temps === "number");
  const rapides = avecTemps.length ? avecTemps.filter((o) => (o.temps as number) < MX.TEMPS_SUSPECT_SEC).length / avecTemps.length : 0;
  let aretes = 0, inversions = 0;
  for (const c of ref.ordre) for (const p of ref.comps[c].prerequis) {
    if (!ref.comps[p] || st[p] === "non_evalue" || st[c] === "non_evalue") continue;
    aretes++;
    if (st[c] === "acquis" && st[p] === "lacune") inversions++;
  }
  const inv = aretes ? inversions / aretes : 0;
  const niveau = rapides >= 0.4 || (aretes >= 3 && inv > 0.34) ? "faible" : rapides >= 0.2 || inv > 0.2 ? "moyenne" : "bonne";
  return { niveau, reponses_rapides: mxR(rapides, 2), inversions: mxR(inv, 2) };
}

function mxCalculerCarte(ref: MxRef, mt: Record<string, MxMaitrise>, opts: {
  type: string; eleve: { prenom: string; niveau: string }; date: string;
  duree_min?: number; n_questions?: number; obs?: MxObs[];
}) {
  const A = mxAnalyse(ref, mt);
  const obs = opts.obs || [];
  const titre = (id: string) => ref.comps[id].titre_eleve || ref.comps[id].titre;
  const evalues = ref.ordre.filter((id) => (mt[id]?.n_obs || 0) > 0);
  const prios = mxPriorites(ref, mt);
  const competences = evalues.map((id) => {
    const c = ref.comps[id], m = mt[id];
    const erreurs = Object.entries(m.erreurs_vues || {}).sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1)).map(([eid, n]) => {
      const def = (c.erreurs || []).find((e) => e.id === eid);
      const ex = obs.slice().reverse().find((o) => o.err === eid);
      const it = ex ? ref.items[ex.item_id] : null;
      return { id: eid, libelle: def?.libelle || eid, libelle_parent: def?.libelle_parent || null,
        remediation: def?.remediation || null, n,
        exemple: it ? { q: it.q, reponse_eleve: ex!.reponse || "", a: it.a } : null };
    });
    return { id, titre: c.titre, titre_eleve: titre(id), domaine: c.domaine, niveau_origine: c.niveau_origine,
      statut: A.st[id], maitrise: mxR(m.maitrise, 2), n_obs: m.n_obs,
      cause_racine: A.causeRacine(id), racine_profonde: A.racineProfonde(id),
      bloque: A.st[id] === "lacune" || A.st[id] === "fragile" ? A.bloque(id) : [], erreurs };
  });
  // Taux d'un ensemble de compétences : acquis = 1, fragile = 0.5, lacune = 0, pondéré par le poids
  // Brevet. (La moyenne brute des maîtrises serait plafonnée ~0.75 après 2 questions à cause du prior :
  // un élève parfait n'afficherait jamais 100 %.)
  const valeur: Record<string, number> = { acquis: 1, fragile: 0.5, lacune: 0 };
  const taux = (ids: string[]) => {
    const pds = ids.reduce((s, id) => s + ref.comps[id].poids_brevet, 0);
    return pds ? ids.reduce((s, id) => s + ref.comps[id].poids_brevet * valeur[A.st[id]], 0) / pds : 0;
  };
  const domaines = MX_DOMAINES.map(([code, libelle]) => {
    const ids = ref.ordre.filter((id) => ref.comps[id].domaine === code);
    const ev = ids.filter((id) => A.st[id] !== "non_evalue");
    const m = taux(ev);
    const statut: MxStatut = !ev.length ? "non_evalue" : m < MX.SEUIL_LACUNE ? "lacune" : m <= MX.SEUIL_ACQUIS ? "fragile" : "acquis";
    return { code, libelle, maitrise: mxR(m, 2), statut, n_comp: ids.length, n_evalues: ev.length,
      n_lacunes: ids.filter((id) => A.st[id] === "lacune").length };
  }).filter((d) => d.n_comp > 0);
  const ev3 = ref.ordre.filter((id) => A.st[id] !== "non_evalue" && ref.comps[id].niveau_origine === "3EME");
  const base = ev3.length ? ev3 : ref.ordre.filter((id) => A.st[id] !== "non_evalue");
  const score_global = Math.round(100 * taux(base));
  const points_forts = ref.ordre.filter((id) => A.st[id] === "acquis").sort((a, b) =>
    (ref.comps[a].niveau_origine === "3EME" ? 0 : 1) - (ref.comps[b].niveau_origine === "3EME" ? 0 : 1) ||
    ref.comps[b].poids_brevet - ref.comps[a].poids_brevet || mt[b].maitrise - mt[a].maitrise || (a < b ? -1 : 1)).slice(0, 5);
  const fiabilite = mxFiabilite(ref, A.st, obs);
  // Point faible révélé = la 1re priorité qui est une lacune confirmée (cause racine de préférence).
  const pf = prios.find((id) => A.causeRacine(id)) || prios.find((id) => A.st[id] === "lacune") || prios[0] || null;
  // Zone d'entraînement gratuite : ses prérequis non acquis (évalués) + lui + ce qu'il bloque.
  const zone_gratuite = pf ? [...new Set([
    ...ref.anc2[pf].filter((a) => A.st[a] === "lacune" || A.st[a] === "fragile"), pf, ...A.bloque(pf)])] : [];
  const prenom = opts.eleve.prenom || "Votre enfant";
  let message_parent = prenom + (points_forts.length
    ? " est à l'aise sur : " + points_forts.slice(0, 2).map(titre).join(" ; ") + ". "
    : " a encore des bases à consolider. ");
  if (pf) {
    const nb = A.bloque(pf).length;
    message_parent += "Priorité n°1 : " + titre(pf) +
      (A.causeRacine(pf) ? " — une notion de " + mxNiveauLabel(ref.comps[pf].niveau_origine) +
        " qui freine " + nb + " autre" + (nb > 1 ? "s" : "") + " compétence" + (nb > 1 ? "s" : "") + " du programme." : ".") +
      " Le plan : 5 exercices ciblés par jour, environ 10 minutes.";
  } else {
    message_parent += "Aucune lacune détectée sur les compétences évaluées : on entretient les acquis.";
  }
  // « L'essentiel » en 1 phrase (couverture du PDF, haut de la carte), dérivée de la cause racine principale.
  let phrase_cle: string;
  if (pf && A.causeRacine(pf)) {
    const nb = A.bloque(pf).length;
    phrase_cle = "Le blocage principal vient d'une notion de " + mxNiveauLabel(ref.comps[pf].niveau_origine) + " : « " +
      titre(pf) + " ». Elle freine " + nb + " autre" + (nb > 1 ? "s" : "") + " compétence" + (nb > 1 ? "s" : "") + " : c'est par là qu'on commence.";
  } else if (pf) {
    phrase_cle = "Priorité n°1 : « " + titre(pf) + " ». Le reste de la carte est plus solide.";
  } else {
    phrase_cle = "Aucune lacune sur ce qui a été évalué : l'objectif est d'entretenir les acquis et de viser les exercices type Brevet.";
  }
  const carte: Record<string, unknown> = {
    eleve: { prenom: opts.eleve.prenom, niveau: opts.eleve.niveau },
    type: opts.type, date: opts.date,
    duree_min: opts.duree_min ?? null,
    n_questions: opts.n_questions ?? obs.filter((o) => !o.graine && !o.imputee).length,
    score_global, phrase_cle, domaines, competences,
    priorites: prios, point_faible: pf,
    plan_4_semaines: mxPlan4Semaines(ref, mt, prios),
    points_forts, message_parent, fiabilite, zone_gratuite,
  };
  if (fiabilite.niveau === "faible") {
    carte.alerte = "Beaucoup de réponses très rapides ou incohérentes : la carte est peut-être faussée. " +
      "Conseil : refaire le diagnostic au calme.";
  }
  return carte;
}

// Zone d'entraînement gratuite = prérequis fragiles du point faible + point faible + ce qu'il bloque.
function mxZoneGratuite(carte: Record<string, unknown> | null): string[] | null {
  if (!carte || !carte.point_faible) return null;
  if (Array.isArray(carte.zone_gratuite) && carte.zone_gratuite.length) return carte.zone_gratuite as string[];
  const pf = String(carte.point_faible);
  const c = ((carte.competences || []) as { id: string; bloque?: string[] }[]).find((x) => x.id === pf);
  return [pf, ...((c && c.bloque) || [])];
}

function mxComparerCartes(ancienne: Record<string, unknown> | null, nouvelle: Record<string, unknown>) {
  if (!ancienne) return null;
  const av: Record<string, string> = {};
  for (const c of (ancienne.competences || []) as { id: string; statut: string }[]) av[c.id] = c.statut;
  const changements = ((nouvelle.competences || []) as { id: string; statut: string }[])
    .filter((c) => av[c.id] && av[c.id] !== c.statut).map((c) => ({ id: c.id, avant: av[c.id], apres: c.statut }));
  return { score_avant: ancienne.score_global ?? null, score_apres: nouvelle.score_global, changements };
}

// ── Entraînement quotidien ──────────────────────────────────

type MxHist = { item_id: string; date: string; ok: boolean; contexte?: string };
type MxExoChoisi = { item: MxItem; role: "reussite" | "travail" | "revision" | "entretien" };

function mxChoisirItemTrain(ref: MxRef, comp: string, lvlCible: number, dernier: Record<string, MxHist>,
  date: string, code: string, pris: Set<string>, strict = true): MxItem | null {
  // strict : jamais un item vu il y a moins de 3 jours (banque peu profonde → on complète ailleurs d'abord)
  let cands = (ref.itemsParComp[comp] || []).filter((it) => !pris.has(it.id) &&
    (!strict || !dernier[it.id] || mxJoursEntre(dernier[it.id].date, date) >= 3));
  const pourTrain = cands.filter((it) => !it.usage || it.usage.includes("train"));
  if (pourTrain.length) cands = pourTrain;
  if (!cands.length) return null;
  const score = (it: MxItem) => {
    const h = dernier[it.id];
    let s = Math.abs((it.lvl || 1) - lvlCible) * 4;
    if (h) {
      const j = mxJoursEntre(h.date, date);
      // déjà vu : plus c'est ancien, mieux c'est ; réussi récemment = inutile ; < 3 jours = dernier recours
      s += 50 - Math.min(j, 45) + (h.ok && j < 14 ? 40 : 0);
    }
    return s;
  };
  cands.sort((a, b) => score(a) - score(b) || mxHash(code + "|" + date + "|" + a.id) - mxHash(code + "|" + date + "|" + b.id));
  return cands[0];
}

function mxLvlCible(m?: MxMaitrise): number {
  if (!m || m.n_obs < MX.OBS_MIN) return 1;
  if (m.maitrise < MX.SEUIL_LACUNE) return 1;
  if (m.maitrise <= MX.SEUIL_ACQUIS) return 2;
  return m.maitrise > 0.85 ? 3 : 2;
}

// 5 exos/jour : 1 réussite (échauffement) + 3 travail (priorités « prêtes ») + 1 révision espacée.
// zone = null → toute la carte (Programme Brevet) ; sinon restreint à la zone (gratuit).
function mxChoisirEntrainement(ref: MxRef, mt: Record<string, MxMaitrise>, opts: {
  code: string; date: string; zone: string[] | null; historique: MxHist[];
}) {
  const dans = (id: string) => !opts.zone || opts.zone.includes(id);
  const st = (id: string) => mxStatut(mt[id]);
  const aItems = (id: string) => (ref.itemsParComp[id] || []).length > 0;
  const dernier: Record<string, MxHist> = {};
  for (const h of opts.historique.slice().sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0))) dernier[h.item_id] = h;

  const prios = mxPriorites(ref, mt).filter((c) => dans(c) && aItems(c));
  // Maîtrise d'abord : une compétence n'est « prête » que si aucun de ses prérequis proches (distance ≤ 2,
  // dans le périmètre) n'est en lacune ou fragile. Repli : seulement « pas de prérequis en lacune »
  // (jamais de blocage total si un prérequis plafonne).
  const enChantier = new Set(prios);
  const preteStricte = (c: string) => !ref.anc2[c].some((a) => enChantier.has(a));
  const preteSouple = (c: string) => !ref.anc2[c].some((a) => st(a) === "lacune");
  const prete = prios.some(preteStricte) ? preteStricte : preteSouple;
  // Maîtrise d'abord : une compétence travaillée ces 3 derniers jours reste au focus jusqu'à « acquis »
  // (sinon elle sortirait du focus dès qu'elle quitte « lacune » et resterait fragile pour toujours).
  const recentes = new Set(opts.historique
    .filter((h) => (h.contexte || "train") === "train" && mxJoursEntre(h.date, opts.date) <= 3)
    .map((h) => ref.items[h.item_id]?.comp).filter(Boolean) as string[]);
  // Une priorité bloquée « remonte » le prérequis qui la bloque (le plus prioritaire d'entre eux).
  const rang = (c: string) => prios.indexOf(c);
  const pretes: string[] = [];
  for (const c of prios) {
    const cible = prete(c) ? c
      : ref.anc2[c].filter((a) => enChantier.has(a) && prete(a)).sort((a, b) => rang(a) - rang(b))[0];
    if (cible && !pretes.includes(cible)) pretes.push(cible);
  }
  let focus = [...pretes.filter((c) => recentes.has(c)), ...pretes.filter((c) => !recentes.has(c))].slice(0, 2);
  if (!focus.length && !opts.zone) {
    // Tout est acquis ou non évalué : on explore (diagnostic continu) les compétences 3e non évaluées.
    focus = mxCibles3e(ref, MX_TOUS_DOMAINES).filter((id) => st(id) === "non_evalue" && prete(id)).slice(0, 2);
  }
  const acquis = ref.ordre.filter((id) => dans(id) && aItems(id) && st(id) === "acquis");
  const dues = acquis.filter((id) => mt[id].prochaine_revision && String(mt[id].prochaine_revision) <= opts.date)
    .sort((a, b) => (String(mt[a].prochaine_revision) < String(mt[b].prochaine_revision) ? -1 : 1) || (a < b ? -1 : 1));
  // Échauffement : un acquis solide, en tournant (le moins récemment vu d'abord).
  const facile = acquis.filter((id) => id !== dues[0])
    .sort((a, b) => (String(mt[a].derniere_obs) < String(mt[b].derniere_obs) ? -1 : String(mt[a].derniere_obs) > String(mt[b].derniere_obs) ? 1 : 0) ||
      mxHash(opts.code + opts.date + a) - mxHash(opts.code + opts.date + b))[0];

  type Voeu = { comp: string; role: MxExoChoisi["role"]; lvl: number };
  const voeux: Voeu[] = [];
  const reussite: Voeu | null = facile ? { comp: facile, role: "reussite", lvl: 1 }
    : focus[0] ? { comp: focus[0], role: "reussite", lvl: 1 } : null;
  const revision: Voeu | null = dues[0] ? { comp: dues[0], role: "revision", lvl: mxLvlCible(mt[dues[0]]) } : null;
  const nTravail = MX.EXOS_PAR_JOUR - (reussite ? 1 : 0) - (revision ? 1 : 0);
  const motif = [0, 0, 1, 0, 1];
  const travail: Voeu[] = [];
  for (let k = 0; k < nTravail && focus.length; k++) {
    const c = focus[motif[k] % focus.length];
    travail.push({ comp: c, role: "travail", lvl: mxLvlCible(mt[c]) });
  }
  if (reussite) voeux.push(reussite);
  voeux.push(...travail.slice(0, 2));
  if (revision) voeux.push(revision);
  voeux.push(...travail.slice(2));

  const pris = new Set<string>();
  const exos: MxExoChoisi[] = [];
  for (const v of voeux) {
    const it = mxChoisirItemTrain(ref, v.comp, v.lvl, dernier, opts.date, opts.code, pris);
    if (it) { pris.add(it.id); exos.push({ item: it, role: v.role }); }
  }
  // Compléments si la banque manque ou si rien n'est à travailler : révisions dues, puis entretien des acquis
  // (les plus anciens d'abord), puis la zone elle-même.
  // (jamais une compétence non acquise dont un prérequis proche est encore en lacune)
  const secours = [...new Set([...focus, ...dues.slice(1),
    ...acquis.slice().sort((a, b) => (String(mt[a].derniere_obs) < String(mt[b].derniere_obs) ? -1 : 1)),
    ...pretes, ...(opts.zone || []).filter(aItems)])]
    .filter((c) => st(c) === "acquis" || preteSouple(c));
  for (let tour = 0; tour < 3 && exos.length < MX.EXOS_PAR_JOUR; tour++) {
    for (const c of secours) {
      if (exos.length >= MX.EXOS_PAR_JOUR) break;
      const it = mxChoisirItemTrain(ref, c, mxLvlCible(mt[c]), dernier, opts.date, opts.code, pris);
      if (it) { pris.add(it.id); exos.push({ item: it, role: st(c) === "acquis" ? "entretien" : "travail" }); }
    }
  }
  const zone_maitrisee = !!opts.zone && opts.zone.length > 0 && opts.zone.every((c) => st(c) === "acquis");
  // Banque trop peu profonde pour 5 items distincts sans reprise < 3 jours : on n'invente rien, on signale
  // (à remonter au concepteur d'items — viser ≥ 15 items « train » par compétence).
  const banque_insuffisante = exos.length < MX.EXOS_PAR_JOUR;
  if (banque_insuffisante) {
    // Derniers recours (jamais 0 exo) : entretien des points forts hors zone, puis reprise d'items de la zone.
    const horsZone = ref.ordre.filter((id) => !dans(id) && aItems(id) && st(id) === "acquis");
    const recours: [string, boolean][] = [...horsZone.map((c) => [c, true] as [string, boolean]),
      ...secours.map((c) => [c, false] as [string, boolean])];
    for (const [c, strict] of recours) {
      if (exos.length >= MX.EXOS_PAR_JOUR) break;
      const it = mxChoisirItemTrain(ref, c, mxLvlCible(mt[c]), dernier, opts.date, opts.code, pris, strict);
      if (it) { pris.add(it.id); exos.push({ item: it, role: st(c) === "acquis" ? "entretien" : "travail" }); }
    }
  }
  return { exos: exos.slice(0, MX.EXOS_PAR_JOUR), focus, zone_maitrisee, banque_insuffisante };
}

// ── Droits d'accès ──────────────────────────────────────────
// free < diagnostic_complet < programme_brevet. Compatibilité : profiles.premium (legacy,
// paiement 29,99 € par niveau) = accès complet → programme_brevet.
function mxDroits(profile: { premium?: boolean | null; premium_end?: string | null },
  achats: { produit: string }[], today: string) {
  const premiumActif = !!profile.premium && !(profile.premium_end && String(profile.premium_end).slice(0, 10) < today);
  const p = new Set(achats.map((a) => a.produit));
  const acces = p.has("programme_brevet") || premiumActif ? "programme_brevet"
    : p.has("diagnostic_complet") ? "diagnostic_complet" : "free";
  const prog = MX_PRODUITS.programme_brevet;
  const prixProgramme = prog.prix_cents - (prog.deduction && p.has(prog.deduction.si) ? prog.deduction.cents : 0);
  return {
    acces,
    diagnostic_complet: acces !== "free",
    pdf: acces !== "free",
    entrainement_complet: acces === "programme_brevet",
    rediagnostic_mensuel: acces === "programme_brevet",
    brevets_blancs: acces === "programme_brevet",
    prix_cents: {
      diagnostic_complet: acces === "free" ? MX_PRODUITS.diagnostic_complet.prix_cents : 0,
      programme_brevet: acces === "programme_brevet" ? 0 : prixProgramme,
    },
  };
}

// Streak calculé côté serveur (depuis les dates de réponses) : ne dépend plus du localStorage.
// Règle G3 : 1 jour de gel toléré par fenêtre de 7 jours si les 2 jours précédant le trou sont actifs.
// Aujourd'hui pas encore actif = le streak d'hier est conservé (il n'est pas encore perdu).
function mxStreak(dates: string[], today: string) {
  const S = new Set(dates.map((d) => String(d).slice(0, 10)).filter((d) => d <= today));
  const prev = (d: string) => mxAjoutJours(d, -1);
  let d = S.has(today) ? today : prev(today);
  let streak = 0, i = 0, dernierGel = -99, gel_utilise = false;
  for (let garde = 0; garde < 3660; garde++) {
    if (S.has(d)) { streak++; d = prev(d); i++; continue; }
    const p = prev(d);
    if (S.has(p) && S.has(prev(p)) && i - dernierGel >= 7) { dernierGel = i; gel_utilise = true; d = p; i++; continue; }
    break;
  }
  return { streak, actif_aujourdhui: S.has(today), gel_utilise };
}

function mxRediagDu(dernierDiagDate: string | null, today: string, acces: string): boolean {
  return acces === "programme_brevet" && !!dernierDiagDate && mxJoursEntre(dernierDiagDate, today) >= MX.REDIAG_JOURS;
}

// Item envoyé au client pendant le DIAGNOSTIC : sans réponse, sans erreurs types, sans indices
// (la correction est faite serveur). Options mélangées de façon déterministe.
function mxItemPublic(it: MxItem, code: string) {
  const { a: _a, alt: _alt, err: _err, steps: _s, f: _f, ...reste } = it;
  const out: Record<string, unknown> = { ...reste, type: mxTypeItem(it) };
  if (Array.isArray(it.options)) {
    out.options = it.options.slice().sort((x, y) => mxHash(code + "|" + it.id + "|" + x) - mxHash(code + "|" + it.id + "|" + y));
  }
  return out;
}

// Libellés des erreurs types d'un item d'entraînement ({err_id: libelle}) pour le feedback
// « Erreur classique : … ». L'id peut désigner une erreur d'un prérequis direct (contrat §9) :
// on la cherche dans la compétence que porte l'id, pas forcément celle de l'item.
function mxErrLibelles(ref: MxRef, it: { err?: Record<string, string> }): Record<string, string> {
  const out: Record<string, string> = {};
  for (const eid of Object.values(it.err || {})) {
    const def = (ref.comps[String(eid).split("#")[0]]?.erreurs || []).find((e) => e.id === eid);
    if (def) out[eid] = def.libelle;
  }
  return out;
}

// Maîtrise reconstruite depuis les observations d'une session (diagnostic invité : pas encore de
// compte, donc pas de lignes `maitrise`). Même mise à jour, dans le même ordre, que la couche I/O
// (mxAppliquerReponse) : une fois le compte créé, le rejeu donne exactement la même carte.
function mxMaitriseDepuisObs(obs: MxObs[], date: string, base: Record<string, MxMaitrise> = {}): Record<string, MxMaitrise> {
  const mt: Record<string, MxMaitrise> = { ...base };
  for (const o of obs) {
    if (o.graine) continue;
    mt[o.comp] = mxMajMaitrise(mt[o.comp], o.comp, o.ok, o.w, o.err || null, o.date || date);
  }
  return mt;
}

function mxFocusTitres(ref: MxRef, focus: string[]) {
  return focus.filter((id) => ref.comps[id]).map((id) => ({ id, titre_eleve: ref.comps[id].titre_eleve || ref.comps[id].titre,
    niveau_origine: ref.comps[id].niveau_origine, domaine: ref.comps[id].domaine }));
}

// « Pourquoi cette séance » (carte « Ta séance du jour ») : 1 phrase déterministe, tutoiement.
// Ordre des raisons : cause racine > erreur type déjà vue > statut (à reprendre / fragile / découverte),
// + la révision espacée s'il y en a une. Jamais de « ton prof » : c'est l'algorithme qui choisit.
function mxPourquoi(ref: MxRef, mt: Record<string, MxMaitrise>, focus: string[],
  exos: { comp: string; role: string }[], zone_maitrisee = false): string {
  const titre = (id: string) => ref.comps[id]?.titre_eleve || ref.comps[id]?.titre || id;
  const autres = (n: number) => n > 1 ? n + " autres points" : n + " autre point";
  const rev = exos.find((e) => e.role === "revision");
  const finRev = rev ? " Et 1 révision de « " + titre(rev.comp) + " » pour ne pas l'oublier." : "";
  const f = focus.find((id) => ref.comps[id]);
  if (!f) {
    return (zone_maitrisee ? "Ta zone de travail est acquise : " : "Rien de fragile à reprendre aujourd'hui : ") +
      "séance d'entretien pour garder le rythme." + finRev;
  }
  const A = mxAnalyse(ref, mt);
  const c = ref.comps[f];
  let s: string;
  if (A.causeRacine(f)) {
    s = "On attaque « " + titre(f) + " » : c'est une notion de " + mxNiveauLabel(c.niveau_origine) +
      " qui te freine sur " + autres(A.bloque(f).length) + " du programme.";
  } else {
    const vues = Object.entries(mt[f]?.erreurs_vues || {}).sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1));
    const def = vues.length ? (ref.comps[vues[0][0].split("#")[0]]?.erreurs || []).find((e) => e.id === vues[0][0]) : null;
    if (def) s = "On travaille « " + titre(f) + " » : tu as fait l'erreur classique « " + def.libelle + " ».";
    else if (A.st[f] === "non_evalue") s = "On découvre « " + titre(f) + " », pas encore mesuré par ton diagnostic.";
    else if (A.st[f] === "lacune") s = "On reprend « " + titre(f) + " » : c'est encore à construire.";
    else if (A.st[f] === "fragile") s = "On consolide « " + titre(f) + " » : c'est presque acquis, encore fragile.";
    else s = "On consolide « " + titre(f) + " ».";
  }
  const f2 = focus.find((id) => id !== f && ref.comps[id]);
  if (f2) s += " Puis « " + titre(f2) + " ».";
  return s + finRev;
}

// MOTEUR_PUR_FIN
// ════════════════════════════════════════════════════════════

// ════════════════════════════════════════════════════════════
// MOTEUR 3E — couche I/O (Supabase). Actions : start_diagnostic, answer_diagnostic,
// get_carte, get_training, get_acces (+ maj maîtrise branchée dans save_score /
// save_scores_batch quand l'exo porte item_id ou comp). Spec : docs/specs/20-moteur.md
// ════════════════════════════════════════════════════════════

async function mxChargerRef(): Promise<MxRef> {
  const cached = cacheGet("mx_ref") as MxRef | null;
  if (cached) return cached;
  const { data: comps } = await adminClient.from("competences").select("*").eq("actif", true);
  const items: MxItem[] = [];
  for (let from = 0; ; from += 1000) {
    const { data: rows } = await adminClient.from("items").select("id, comp, item_json")
      .eq("actif", true).order("id").range(from, from + 999);
    for (const r of (rows || []) as Record<string, unknown>[]) {
      const j = (typeof r.item_json === "string" ? JSON.parse(r.item_json as string) : r.item_json) as MxItem;
      items.push({ ...j, id: String(r.id), comp: String(r.comp) });
    }
    if (!rows || rows.length < 1000) break;
  }
  const ref = mxIndexer((comps || []).map((c: Record<string, unknown>) => ({
    id: String(c.id), domaine: String(c.domaine), theme: String(c.theme || ""), titre: String(c.titre),
    titre_eleve: c.titre_eleve ? String(c.titre_eleve) : undefined, niveau_origine: String(c.niveau_origine),
    prerequis: (c.prerequis || []) as string[], poids_brevet: Number(c.poids_brevet) || 1,
    chapitres_legacy: (c.chapitres_legacy || []) as string[], erreurs: (c.erreurs || []) as MxErreurRef[],
    diag_autorise: c.diag_autorise !== false,
  })), items);
  if (ref.ordre.length) cacheSet("mx_ref", ref);
  return ref;
}

function mxDepuisLigne(r: Record<string, unknown>): MxMaitrise {
  return {
    comp: String(r.comp), alpha: Number(r.alpha), beta: Number(r.beta), maitrise: Number(r.maitrise),
    n_obs: Number(r.n_obs) || 0, n_succes: Number(r.n_succes) || 0,
    derniere_obs: r.derniere_obs ? String(r.derniere_obs).slice(0, 10) : null,
    erreurs_vues: (r.erreurs_vues || {}) as Record<string, number>, boite: Number(r.boite) || 0,
    prochaine_revision: r.prochaine_revision ? String(r.prochaine_revision).slice(0, 10) : null,
  };
}

async function mxChargerMaitrise(code: string): Promise<Record<string, MxMaitrise>> {
  const { data } = await adminClient.from("maitrise").select("*").eq("code", code);
  const out: Record<string, MxMaitrise> = {};
  for (const r of (data || []) as Record<string, unknown>[]) out[String(r.comp)] = mxDepuisLigne(r);
  return out;
}

async function mxSauverMaitrise(code: string, m: MxMaitrise) {
  await adminClient.from("maitrise").upsert({ code, ...m }, { onConflict: "code,comp" });
}

// Applique UNE réponse à la maîtrise globale + journalise dans reponses_items.
async function mxAppliquerReponse(code: string, comp: string, itemId: string, ok: boolean, w: number,
  err: string | null, extra: { contexte: string; diagnostic_id?: string | null; resultat?: string; reponse?: string; temps?: number | null; imputee?: boolean; date?: string }) {
  const date = extra.date || todayParis();
  const { data: row } = await adminClient.from("maitrise").select("*").eq("code", code).eq("comp", comp).maybeSingle();
  const m = mxMajMaitrise(row ? mxDepuisLigne(row as Record<string, unknown>) : null, comp, ok, w, err, date);
  await mxSauverMaitrise(code, m);
  if (extra.imputee) return; // observation imputée à un prérequis : maîtrise seulement, pas de ligne de journal
  await adminClient.from("reponses_items").insert({
    code, item_id: itemId, comp, contexte: extra.contexte, diagnostic_id: extra.diagnostic_id || null,
    ok, resultat: extra.resultat || (ok ? "EASY" : "HARD"), reponse: (extra.reponse || "").slice(0, 200),
    err_id: err, temps_sec: extra.temps ?? null, date,
  });
}

// Branché dans save_score / save_scores_batch : n'agit que si l'exo porte item_id ou comp.
async function mxMajDepuisScore(code: string, s: Record<string, unknown>, contexte: string) {
  const ref = await mxChargerRef();
  const it = s.item_id ? ref.items[String(s.item_id)] : undefined;
  const comp = it?.comp || String(s.comp || "");
  if (!ref.comps[comp]) return;
  const ok = String(s.resultat) === "EASY";
  const nOpt = Number(s.nbOptions || s.nb_options || 0);
  const w = it ? mxPoidsSucces(it) : mxPoidsSucces({ type: String(s.type || ""), options: new Array(nOpt).fill("") });
  const rep = String(s.reponse ?? s.wrongOpt ?? "");
  const err = !ok ? (it && rep ? mxErreurType(it, rep) : (s.err_id ? String(s.err_id) : null)) : null;
  const imps = mxImputer(ref, it || { id: "", comp, q: "", a: "" }, ok, err);
  for (const im of imps) {
    await mxAppliquerReponse(code, im.comp, it?.id || String(s.item_id || ""), im.ok, im.imputee ? 1 : w, im.err, {
      contexte, resultat: String(s.resultat || ""), reponse: rep, imputee: im.imputee,
      temps: parseInt(String(s.time ?? s.temps ?? "")) || null,
    });
  }
}

// ── Sécurité des actions élève (Besoin API n°8, 25/09) ──────────────────────
// Le code élève (6 caractères) IDENTIFIE, il n'AUTHENTIFIE pas : il circule (liens, écrans, comptes de
// test dans le dépôt public) et se devine. Toute action qui lit ou écrit les données d'un élève exige
// `access_token` (jeton de session renvoyé par login / register / login_token / refresh_session),
// vérifié par auth.getUser et rattaché au profil du `code`. `lectureAdmin` : un admin authentifié
// peut LIRE la fiche d'un autre élève (monitoring), jamais écrire à sa place (A6).
const MX_AUTH_REFUS = { status: "error", message: "Session expirée ou invalide : reconnecte-toi.", auth_requise: true };
// Helper UNIQUE de vérification du jeton de session (élève comme admin) : id Supabase Auth ou null.
async function mxSessionUid(p: Record<string, unknown>): Promise<string | null> {
  const token = String(p.access_token || "");
  if (!token) return null;
  const { data, error } = await adminClient.auth.getUser(token);
  return error || !data?.user ? null : data.user.id;
}
async function mxAuth(p: Record<string, unknown>, opts: { lectureAdmin?: boolean } = {}):
  Promise<{ profile: Record<string, unknown>; parAdmin: boolean } | null> {
  const code = String(p.code || "").trim().toUpperCase();
  if (!/^[A-Z0-9]{6}$/.test(code)) return null;
  const uid = await mxSessionUid(p);
  if (!uid) return null;
  const { data: profile } = await adminClient.from("profiles").select("*").eq("code", code).maybeSingle();
  if (!profile) return null;
  if (profile.id === uid) return { profile: profile as Record<string, unknown>, parAdmin: false };
  if (!opts.lectureAdmin) return null;
  const { data: moi } = await adminClient.from("profiles").select("is_admin").eq("id", uid).maybeSingle();
  return moi?.is_admin ? { profile: profile as Record<string, unknown>, parAdmin: true } : null;
}

async function mxProfil(p: Record<string, unknown>, opts: { lectureAdmin?: boolean } = {}) {
  const auth = await mxAuth(p, opts);
  if (!auth) return { error: MX_AUTH_REFUS.message, auth_requise: true };
  const profile = auth.profile as { code: string; email: string; premium?: boolean | null; premium_end?: string | null; [k: string]: unknown };
  const code = String(profile.code);
  if (p.email && String(p.email).toLowerCase() !== profile.email) return { error: "Identité non vérifiée.", auth_requise: false };
  const { data: achats } = await adminClient.from("achats").select("produit")
    .or(`code.eq.${code},email.eq."${profile.email}"`);
  const droits = mxDroits(profile, (achats || []) as { produit: string }[], todayParis());
  return { profile: profile as Record<string, unknown>, droits };
}

async function mxDejaVus(code: string): Promise<string[]> {
  const { data } = await adminClient.from("reponses_items").select("item_id").eq("code", code);
  return [...new Set((data || []).map((r: Record<string, unknown>) => String(r.item_id)))];
}

async function mxDernierDiag(code: string, types?: string[]) {
  let q = adminClient.from("diagnostics").select("*").eq("code", code).eq("statut", "termine");
  if (types) q = q.in("type", types);
  const { data } = await q.order("finished_at", { ascending: false }).limit(1).maybeSingle();
  return data as Record<string, unknown> | null;
}

// Carte masquée selon les droits : en gratuit, seul le point faible est détaillé (reste « flouté »).
// Les titres (titre_eleve, niveau_origine) restent visibles partout (Besoin API n°3) : ce ne sont pas
// des résultats (50 §2.2 « titres lisibles ») ; il en faut pour bloque[] et « pas encore mesuré ».
// Avec `ref` : `non_mesurees` = compétences de 3e diagnostiquables pas encore conclues (≥ 2 obs).
function mxMasquerCarte(carte: Record<string, unknown> | null, acces: string, ref: MxRef | null = null) {
  if (!carte) return carte;
  const pf = carte.point_faible;
  const out: Record<string, unknown> = acces !== "free" ? { ...carte } : {
    ...carte,
    competences: ((carte.competences || []) as Record<string, unknown>[]).map((c) => c.id === pf ? c
      : { id: c.id, domaine: c.domaine, statut: c.statut, titre_eleve: c.titre_eleve, niveau_origine: c.niveau_origine, masque: true }),
    priorites: pf ? [pf] : [],
    plan_4_semaines: ((carte.plan_4_semaines || []) as unknown[]).slice(0, 1),
    masque: true,
  };
  if (ref) {
    const mesurees = new Set(((carte.competences || []) as { id: string; statut: string }[])
      .filter((c) => c.statut !== "non_evalue").map((c) => c.id));
    out.non_mesurees = ref.ordre.filter((id) => ref.comps[id].niveau_origine === "3EME" && mxDiagAutorise(ref, id) && !mesurees.has(id))
      .map((id) => ({ id, titre_eleve: ref.comps[id].titre_eleve || ref.comps[id].titre, domaine: ref.comps[id].domaine,
        niveau_origine: ref.comps[id].niveau_origine }));
  }
  return out;
}

async function mxFinaliserDiagnostic(diag: Record<string, unknown>, etat: MxEtatDiag, ref: MxRef,
  profile: Record<string, unknown>) {
  const code = String(profile.code);
  const mt = await mxChargerMaitrise(code);
  const debut = Date.parse(String(diag.started_at || new Date().toISOString()));
  const carte = mxCalculerCarte(ref, mt, {
    type: etat.type, eleve: { prenom: String(profile.prenom || ""), niveau: String(profile.niveau || "3EME") },
    date: todayParis(), duree_min: Math.max(1, Math.round((Date.now() - debut) / 60000)),
    n_questions: etat.obs.filter((o) => !o.graine && !o.imputee).length, obs: etat.obs,
  });
  if (etat.type === "mensuel") {
    const prec = await mxDernierDiag(code, ["complet", "mensuel"]);
    carte.evolution = mxComparerCartes((prec?.carte_json || null) as Record<string, unknown> | null, carte);
  }
  // Compat legacy : le chapitre gratuit de l'app actuelle suit le point faible révélé.
  const pf = carte.point_faible ? ref.comps[String(carte.point_faible)] : null;
  if (pf && !profile.free_chapter && (pf.chapitres_legacy || []).length) {
    await adminClient.from("profiles").update({ free_chapter: pf.chapitres_legacy![0] }).eq("code", code);
  }
  return carte;
}

// Question envoyée au client + domaine et niveau d'origine de la compétence (Besoin API n°11 :
// étiquettes « Données, fonctions » / « Niveau 5e » de la maquette 01). Jamais la réponse.
function mxQuestionPublique(it: MxItem, code: string, ref: MxRef) {
  const c = ref.comps[it.comp];
  return { ...mxItemPublic(it, code), domaine: c?.domaine || it.comp.split(".")[0], niveau_origine: c?.niveau_origine || null };
}

// ── START_DIAGNOSTIC {code, email?, type: express|complet|mensuel} ──
async function startDiagnostic(p: Record<string, unknown>) {
  const type = String(p.type || "express");
  if (!MX.DIAG[type]) return { status: "error", message: "Type de diagnostic inconnu." };
  // Sans compte (ni code ni jeton de session) : diagnostic express invité (Besoin API n°1).
  if (!p.code && !p.access_token) return await startDiagnosticInvite(p);
  const pr = await mxProfil(p);
  if ("error" in pr) return { status: "error", message: pr.error, auth_requise: pr.auth_requise };
  const { profile, droits } = pr;
  if (type === "complet" && !droits.diagnostic_complet)
    return { status: "error", message: "Diagnostic complet non débloqué.", paywall: "diagnostic_complet", droits };
  if (type === "mensuel" && !droits.rediagnostic_mensuel)
    return { status: "error", message: "Re-diagnostic réservé au Programme Brevet.", paywall: "programme_brevet", droits };
  const ref = await mxChargerRef();
  if (!ref.ordre.length) return { status: "error", message: "Référentiel non importé." };
  const code = String(profile.code);

  const { data: enCours } = await adminClient.from("diagnostics").select("*")
    .eq("code", code).eq("type", type).eq("statut", "en_cours")
    .order("started_at", { ascending: false }).limit(1).maybeSingle();
  let diag = enCours as Record<string, unknown> | null;
  let etat: MxEtatDiag;
  if (diag) {
    etat = diag.etat_json as MxEtatDiag;
  } else {
    let graines: MxObs[] | undefined;
    if (type === "complet") {
      const exp = await mxDernierDiag(code, ["express"]);
      graines = exp ? ((exp.etat_json as MxEtatDiag).obs || []).filter((o) => !o.graine) : undefined;
    }
    const maitrise = type === "mensuel" ? await mxChargerMaitrise(code) : undefined;
    etat = mxDemarrerDiag(ref, type, code, { graines, maitrise });
    const { data: ins, error } = await adminClient.from("diagnostics")
      .insert({ code, type, statut: "en_cours", etat_json: etat, n_questions: 0 }).select("*").single();
    if (error || !ins) return { status: "error", message: "Création diagnostic impossible : " + (error?.message || "") };
    diag = ins as Record<string, unknown>;
    await mxLogEvent(code, type === "express" ? "diag_express_start" : type === "complet" ? "diag_complet_start" : "rediag_start", {});
  }
  const dejaVus = await mxDejaVus(code);
  let q = mxProchaineQuestion(etat, ref, dejaVus);
  if ("fin_module" in q) q = mxProchaineQuestion(etat, ref, dejaVus); // reprise = on enchaîne le module suivant
  let carte: Record<string, unknown> | null = null;
  if ("fin" in q) carte = await mxFinaliserDiagnostic(diag, etat, ref, profile);
  await adminClient.from("diagnostics").update({
    etat_json: etat, ...(carte ? { statut: "termine", carte_json: carte, finished_at: new Date().toISOString() } : {}),
  }).eq("id", diag.id);
  if (carte && etat.type === "express") await mxEmailBilanExpress(profile, String(diag.id), carte, ref);
  return {
    status: "success", diagnostic_id: diag.id, type, repris: !!enCours,
    question: "item" in q ? mxQuestionPublique(q.item, etat.code || code, ref) : null,
    progression: mxProgression(etat), termine: !!carte,
    carte: mxMasquerCarte(carte, droits.acces, ref), droits,
  };
}

// ── ANSWER_DIAGNOSTIC {code, email?, diagnostic_id, item_id, reponse, temps?} ──
// reponse vide/null = « je ne sais pas ».
async function answerDiagnostic(p: Record<string, unknown>) {
  if (!p.code && p.guest_token) return await answerDiagnosticInvite(p); // diagnostic invité (Besoin API n°1)
  const pr = await mxProfil(p);
  if ("error" in pr) return { status: "error", message: pr.error, auth_requise: pr.auth_requise };
  const { profile, droits } = pr;
  const code = String(profile.code);
  const { data: diag } = await adminClient.from("diagnostics").select("*")
    .eq("id", String(p.diagnostic_id || "")).eq("code", code).maybeSingle();
  if (!diag) return { status: "error", message: "Diagnostic introuvable." };
  if (diag.statut !== "en_cours") return { status: "error", message: "Diagnostic déjà terminé." };
  const ref = await mxChargerRef();
  const etat = diag.etat_json as MxEtatDiag;
  const temps = p.temps !== undefined && p.temps !== null ? Number(p.temps) : null;
  const res = mxEnregistrerReponse(etat, ref, String(p.item_id || ""), p.reponse, temps, todayParis());
  if ("error" in res) return { status: "error", message: res.error };
  const { item } = res;
  for (const o of res.imputations) {
    await mxAppliquerReponse(code, o.comp, o.item_id, o.ok, o.w, o.err || null, {
      contexte: "diag", diagnostic_id: String(diag.id), reponse: o.reponse, temps, imputee: !!o.imputee,
    });
  }
  const dejaVus = await mxDejaVus(code);
  const q = mxProchaineQuestion(etat, ref, dejaVus);
  let carte: Record<string, unknown> | null = null;
  if ("fin" in q) carte = await mxFinaliserDiagnostic(diag as Record<string, unknown>, etat, ref, profile);
  await adminClient.from("diagnostics").update({
    etat_json: etat, n_questions: etat.obs.filter((o) => !o.graine && !o.imputee).length,
    ...(carte ? { statut: "termine", carte_json: carte, finished_at: new Date().toISOString() } : {}),
  }).eq("id", diag.id);
  void item;
  if ("fin_module" in q) await mxLogEvent(code, "module_done", { type: etat.type, module: q.fin_module });
  if (carte) await mxLogEvent(code, etat.type === "express" ? "diag_express_done" : etat.type === "complet" ? "diag_complet_done" : "rediag_done",
    { score: carte.score_global, n_questions: carte.n_questions });
  // Bilan express au parent (P-X0, Besoin API n°7) : dès que la carte express existe ET que le compte existe.
  if (carte && etat.type === "express") await mxEmailBilanExpress(profile, String(diag.id), carte, ref);
  // Pas de correction pendant le diagnostic (ni juste/faux, ni bonne réponse) : récapitulatif à la fin.
  return {
    status: "success",
    question: "item" in q ? mxQuestionPublique(q.item, etat.code || code, ref) : null,
    fin_module: "fin_module" in q ? q.fin_module + 1 : null, // n° (1-based) du module suivant
    progression: mxProgression(etat), termine: !!carte,
    carte: mxMasquerCarte(carte, droits.acces, ref),
    corrections: carte ? mxRecapCorrections(etat, ref) : null,
  };
}

// Récapitulatif montré à la FIN du diagnostic (pendant : aucune correction).
function mxRecapCorrections(etat: MxEtatDiag, ref: MxRef) {
  return etat.obs.filter((o) => !o.graine && !o.imputee).map((o) => {
    const it = ref.items[o.item_id];
    const def = o.err ? (ref.comps[o.comp]?.erreurs || []).find((e) => e.id === o.err) : null;
    return { item_id: o.item_id, comp: o.comp, q: it?.q || "", reponse_eleve: o.reponse || "", ok: o.ok,
      a: it?.a || "", steps: it?.steps || [], f: it?.f || "",
      erreur: def ? { id: def.id, libelle: def.libelle, remediation: def.remediation || null } : null };
  });
}

// ── Diagnostic express INVITÉ (Besoin API n°1) ─────────────────────────────
// La carte partielle s'affiche AVANT la création du compte (contrat §7). Sans compte, pas de ligne
// `profiles` : la session vit dans `diagnostics_invites` (état du moteur + carte), protégée par un
// `guest_token` (192 bits, seul son SHA-256 est stocké) qui expire au bout de MX_INVITE_JOURS.
// Rien n'est écrit dans maitrise / reponses_items tant que le compte n'existe pas : register
// {diagnostic_id, guest_token} rattache la session et REJOUE les observations (mêmes calculs).
const MX_INVITE_JOURS = 2;

async function mxSha256(s: string): Promise<string> {
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(h)).map((x) => x.toString(16).padStart(2, "0")).join("");
}

// Session invitée valide = id + jeton qui correspondent, non expirée, non rattachée. Sinon null
// (même réponse dans tous les cas : on ne dit pas si l'id existe).
async function mxInvite(p: Record<string, unknown>): Promise<Record<string, unknown> | null> {
  const id = String(p.diagnostic_id || ""), tok = String(p.guest_token || "");
  if (!/^[0-9a-f-]{36}$/i.test(id) || !/^[0-9a-f]{48}$/.test(tok)) return null;
  const { data } = await adminClient.from("diagnostics_invites").select("*").eq("id", id).maybeSingle();
  if (!data || data.statut === "rattache" || data.guest_token_hash !== await mxSha256(tok)) return null;
  if (Date.parse(String(data.expires_at)) < Date.now()) return null;
  return data as Record<string, unknown>;
}

function mxCarteInvite(inv: Record<string, unknown>, etat: MxEtatDiag, ref: MxRef) {
  const today = todayParis();
  const debut = Date.parse(String(inv.started_at || new Date().toISOString()));
  return mxCalculerCarte(ref, mxMaitriseDepuisObs(etat.obs, today), {
    type: "express", eleve: { prenom: String(inv.prenom || ""), niveau: "3EME" }, date: today,
    duree_min: Math.max(1, Math.round((Date.now() - debut) / 60000)),
    n_questions: etat.obs.filter((o) => !o.graine && !o.imputee).length, obs: etat.obs,
  });
}

// START_DIAGNOSTIC {type:'express', prenom?} sans code → {diagnostic_id, guest_token, question…}
// START_DIAGNOSTIC {diagnostic_id, guest_token} sans code → reprise (question en attente).
async function startDiagnosticInvite(p: Record<string, unknown>) {
  const type = String(p.type || "express");
  if (type !== "express") return { ...MX_AUTH_REFUS, message: "Connecte-toi pour faire ce diagnostic." };
  const ref = await mxChargerRef();
  if (!ref.ordre.length) return { status: "error", message: "Référentiel non importé." };
  let inv: Record<string, unknown> | null = null;
  let guest_token: string | null = null;
  if (p.guest_token || p.diagnostic_id) {
    inv = await mxInvite(p);
    if (!inv) return { status: "error", invite_expire: true, message: "Session invitée expirée ou inconnue : recommence le diagnostic." };
  } else {
    guest_token = mxJeton();
    const hash = await mxSha256(guest_token);
    // pseudo-code élève : graine du tirage déterministe des items (hash code|item), jamais un vrai code
    const etat0 = mxDemarrerDiag(ref, "express", "G" + hash.slice(0, 8), {});
    const { data: ins, error } = await adminClient.from("diagnostics_invites").insert({
      guest_token_hash: hash, type: "express", statut: "en_cours", etat_json: etat0,
      // même whitelist que register (audit 2026-04-11 : XSS stockée) ; sinon pas de prénom
      prenom: /^[\p{L}\p{M}\s'\-]{1,50}$/u.test(String(p.prenom || "").trim()) ? String(p.prenom).trim() : null,
      expires_at: new Date(Date.now() + MX_INVITE_JOURS * 86400000).toISOString(),
    }).select("*").single();
    if (error || !ins) return { status: "error", message: "Création diagnostic impossible : " + (error?.message || "") };
    inv = ins as Record<string, unknown>;
    await mxLogEvent(null, "diag_express_start", { invite: true });
  }
  const etat = inv.etat_json as MxEtatDiag;
  let carte = (inv.carte_json || null) as Record<string, unknown> | null;
  const q = mxProchaineQuestion(etat, ref, []);
  if ("fin" in q && !carte) {
    carte = mxCarteInvite(inv, etat, ref);
    await adminClient.from("diagnostics_invites").update({ etat_json: etat, statut: "termine", carte_json: carte,
      finished_at: new Date().toISOString() }).eq("id", inv.id);
  } else if (!("fin" in q)) {
    await adminClient.from("diagnostics_invites").update({ etat_json: etat }).eq("id", inv.id);
  }
  return {
    status: "success", invite: true, diagnostic_id: inv.id, ...(guest_token ? { guest_token } : {}),
    expires_at: inv.expires_at, type: "express", repris: !guest_token,
    question: "item" in q ? mxQuestionPublique(q.item, etat.code, ref) : null,
    progression: mxProgression(etat), termine: !!carte,
    carte: mxMasquerCarte(carte, "free", ref), droits: mxDroits({}, [], todayParis()),
  };
}

// ANSWER_DIAGNOSTIC {diagnostic_id, guest_token, item_id, reponse, temps?} sans code.
async function answerDiagnosticInvite(p: Record<string, unknown>) {
  const inv = await mxInvite(p);
  if (!inv) return { status: "error", invite_expire: true, message: "Session invitée expirée ou inconnue : recommence le diagnostic." };
  if (inv.statut !== "en_cours") return { status: "error", message: "Diagnostic déjà terminé." };
  const ref = await mxChargerRef();
  const etat = inv.etat_json as MxEtatDiag;
  const temps = p.temps !== undefined && p.temps !== null ? Number(p.temps) : null;
  const res = mxEnregistrerReponse(etat, ref, String(p.item_id || ""), p.reponse, temps, todayParis());
  if ("error" in res) return { status: "error", message: res.error };
  const q = mxProchaineQuestion(etat, ref, []);
  const carte = "fin" in q ? mxCarteInvite(inv, etat, ref) : null;
  const n = etat.obs.filter((o) => !o.graine && !o.imputee).length;
  await adminClient.from("diagnostics_invites").update({
    etat_json: etat, n_questions: n,
    ...(carte ? { statut: "termine", carte_json: carte, finished_at: new Date().toISOString(),
      // le compte se crée après la carte : on laisse encore MX_INVITE_JOURS pour s'inscrire
      expires_at: new Date(Date.now() + MX_INVITE_JOURS * 86400000).toISOString() } : {}),
  }).eq("id", inv.id);
  if (carte) await mxLogEvent(null, "diag_express_done", { invite: true, score: carte.score_global, n_questions: n });
  return {
    status: "success", invite: true,
    question: "item" in q ? mxQuestionPublique(q.item, etat.code, ref) : null,
    fin_module: null, progression: mxProgression(etat), termine: !!carte,
    carte: mxMasquerCarte(carte, "free", ref),
    corrections: carte ? mxRecapCorrections(etat, ref) : null,
  };
}

// Appelé par register : rattache la session invitée au nouveau compte et rejoue ses observations
// dans maitrise / reponses_items (contexte diag), puis recalcule la carte avec le vrai prénom.
async function mxRattacherInvite(p: Record<string, unknown>, profile: Record<string, unknown>) {
  const inv = await mxInvite(p);
  if (!inv) return null;
  const code = String(profile.code);
  const ref = await mxChargerRef();
  const etat = inv.etat_json as MxEtatDiag;
  const termine = inv.statut === "termine";
  const { data: diag, error } = await adminClient.from("diagnostics").insert({
    code, type: "express", statut: "en_cours", etat_json: etat,
    n_questions: etat.obs.filter((o) => !o.graine && !o.imputee).length, started_at: inv.started_at,
  }).select("*").single();
  if (error || !diag) { console.error("[invite] rattachement", error); return null; }
  // Verrou tout de suite (un 2e register avec le même jeton ne rattache rien)
  await adminClient.from("diagnostics_invites").update({ statut: "rattache", code, diagnostic_id: diag.id,
    rattache_at: new Date().toISOString() }).eq("id", inv.id);
  for (const o of etat.obs) {
    if (o.graine) continue;
    await mxAppliquerReponse(code, o.comp, o.item_id, o.ok, o.w, o.err || null, {
      contexte: "diag", diagnostic_id: String(diag.id), reponse: o.reponse, temps: o.temps ?? null,
      imputee: !!o.imputee, date: o.date,
    });
  }
  let carte: Record<string, unknown> | null = null;
  if (termine) {
    carte = await mxFinaliserDiagnostic(diag as Record<string, unknown>, etat, ref, profile);
    const avant = inv.carte_json as Record<string, unknown> | null;
    if (avant?.duree_min) carte.duree_min = avant.duree_min; // durée du diagnostic, pas jusqu'à l'inscription
    await adminClient.from("diagnostics").update({ statut: "termine", carte_json: carte,
      finished_at: inv.finished_at || new Date().toISOString() }).eq("id", diag.id);
  }
  // Minimisation (RGPD) : les réponses vivent désormais dans le compte, on vide la copie invitée.
  await adminClient.from("diagnostics_invites").update({ etat_json: null, carte_json: null, prenom: null }).eq("id", inv.id);
  await mxLogEvent(code, "diag_invite_rattache", { termine });
  return { diagnostic_id: String(diag.id), termine, carte, etat, ref };
}

// ── Email P-X0 « bilan express » au parent (Besoin API n°7, spec 51 §2) ─────────
// Remplace templateJ0 pour le parent. Déclenché quand la carte express existe ET que le compte existe
// (fin du diag avec compte, ou register qui rattache un diag invité terminé). Une seule fois par adresse
// (dédup email_logs type D3:P-X0), jamais si l'adresse est désinscrite (UNSUB). Le lien « voir le bilan »
// est un partage dédié (canal email_parent) ; le même jeton sert à la confirmation parentale.
function mxEsc(s: unknown): string {
  return String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function templateBilanExpressParent(prenomBrut: string, email: string, carte: Record<string, unknown>, ref: MxRef,
  lienBilan: string, lienConfirm: string): { subject: string; html: string } {
  const prenom = mxEsc(prenomBrut || "votre enfant");
  const comps = (carte.competences || []) as Record<string, unknown>[];
  const doms = (carte.domaines || []) as { statut: string }[];
  const nb = (st: string) => doms.filter((d) => d.statut === st).length;
  const morceaux: string[] = [];
  if (nb("acquis")) morceaux.push(nb("acquis") + " domaine" + (nb("acquis") > 1 ? "s" : "") + " solide" + (nb("acquis") > 1 ? "s" : ""));
  if (nb("fragile")) morceaux.push(nb("fragile") + " fragile" + (nb("fragile") > 1 ? "s" : ""));
  if (nb("lacune")) morceaux.push(nb("lacune") + " à travailler");
  const resume = morceaux.length ? morceaux.join(", ") : "pas encore assez de réponses pour conclure";
  const nMes = comps.filter((c) => c.statut !== "non_evalue" && c.niveau_origine === "3EME").length;
  const nTot = ref.ordre.filter((id) => ref.comps[id].niveau_origine === "3EME").length;
  const pf = comps.find((c) => c.id === carte.point_faible) || null;
  const P = (t: string) => '<p style="color:#374151;font-size:16px;line-height:1.7;margin:0 0 14px;">' + t + "</p>";
  const H = (t: string) => '<p style="color:#1e293b;font-size:17px;font-weight:800;line-height:1.5;margin:22px 0 10px;">' + t + "</p>";
  let blocPf = "";
  if (pf) {
    const err = ((pf.erreurs || []) as { libelle_parent?: string | null }[]).find((e) => e.libelle_parent);
    blocPf += P("Le point le plus fragile : <strong>" + mxEsc(pf.titre || pf.titre_eleve) + "</strong>." + (err ? " " + mxEsc(err.libelle_parent) + "." : ""));
    const bl = (pf.bloque || []) as string[];
    if (pf.cause_racine && bl.length) {
      const b1 = ref.comps[bl[0]];
      blocPf += P("C'est une notion dont dépend" + (bl.length > 1 ? "ent " + bl.length + " autres points" : " 1 autre point") +
        " du programme" + (b1 ? ", dont « " + mxEsc(b1.titre) + " »" : "") + ".");
    }
  } else {
    blocPf = P("Rien d'inquiétant sur cet échantillon, ce qui est une bonne nouvelle.");
  }
  return {
    subject: "Le bilan maths de " + (prenomBrut || "votre enfant") + " (et une confirmation à faire)",
    html: emailWrap(email, mxEsc(resume.charAt(0).toUpperCase() + resume.slice(1)) + ". 1 clic pour confirmer l'inscription.",
      P("Bonjour,") +
      P(prenom + " vient de passer le diagnostic express de maths sur Matheux et a créé son espace avec votre adresse email.") +
      H("1. Merci de confirmer l'inscription") +
      P(prenom + " est mineur(e) : j'ai besoin de votre accord de parent pour conserver son espace et ses résultats.") +
      emailCTA(lienConfirm, "Je confirme l'inscription de " + prenom) +
      '<p style="color:#6b7280;font-size:13px;line-height:1.6;margin:0 0 14px;">Sur la page de confirmation, vous pourrez aussi choisir de recevoir mes conseils et offres (facultatif). Si ce n\'est pas vous, ou si vous n\'êtes pas d\'accord, ignorez ce message.</p>' +
      H("2. Ce que montre le diagnostic express") +
      P("En quelques minutes, il a mesuré " + nMes + " compétence" + (nMes > 1 ? "s" : "") + " de 3e sur " + nTot + ". Résultat : " + mxEsc(resume) + ".") +
      blocPf +
      H("3. Et maintenant ?") +
      P("Dès aujourd'hui, " + prenom + " a accès gratuitement à 5 exercices par jour sur ce point. 10 minutes suffisent. Aucune carte bancaire n'est demandée.") +
      emailCTA(lienBilan, "Voir le bilan de " + prenom) +
      P("Une question ? Répondez à cet email, c'est moi qui lis."),
    ),
  };
}

async function mxEmailBilanExpress(profile: Record<string, unknown>, diagId: string, carte: Record<string, unknown>, ref: MxRef) {
  try {
    const email = String(profile.email || "").trim().toLowerCase();
    const code = String(profile.code || "");
    if (!email || !code) return;
    const type = "D3:P-X0";
    const { data: unsub } = await adminClient.from("email_logs").select("id").eq("email", email).eq("type", "UNSUB").limit(1);
    if (unsub && unsub.length) return;
    const { data: deja } = await adminClient.from("email_logs").select("id").eq("email", email).eq("type", type).eq("statut", "envoyé").limit(1);
    if (deja && deja.length) return;
    const token = mxJeton();
    const { error: shErr } = await adminClient.from("bilan_partages").insert({
      token, code, diagnostic_id: diagId, type_carte: "express", canal: "email_parent",
      expires_at: new Date(Date.now() + 30 * 86400000).toISOString(),
    });
    if (shErr) { console.error("[P-X0] partage", shErr); return; }
    const lien = "https://matheux.fr/b/" + token;
    const tpl = templateBilanExpressParent(String(profile.prenom || ""), email, carte, ref, lien + "?src=email_px0", lien + "?confirmer=1");
    const r = await resendSend(email, tpl.subject, tpl.html);
    await adminClient.from("email_logs").insert({
      email, prenom: String(profile.prenom || ""), type, statut: r.ok ? "envoyé" : "erreur", details: r.error || null,
      categorie: "T", code, created_at: new Date().toISOString(),
    });
    await mxLogEvent(code, "email_bilan_parent", { ok: r.ok });
  } catch (e) { console.error("[P-X0]", e); /* jamais bloquant */ }
}

// Partage valide (page parent) : jeton hex 48, non révoqué, non expiré.
async function mxPartageValide(token: string): Promise<Record<string, unknown> | null> {
  if (!/^[0-9a-f]{48}$/.test(token)) return null;
  const { data: sh } = await adminClient.from("bilan_partages").select("*").eq("token", token).maybeSingle();
  if (!sh || sh.revoked_at || Date.parse(String(sh.expires_at)) < Date.now()) return null;
  return sh as Record<string, unknown>;
}

// ── CONFIRM_PARENT {token, optin_marketing?, texte_version?, texte_hash?} — PUBLIC, page parent ──
// Confirmation parentale depuis le lien du mail P-X0 (partage canal email_parent : seul le parent l'a reçu).
async function confirmParent(p: Record<string, unknown>) {
  const sh = await mxPartageValide(String(p.token || ""));
  if (!sh || sh.canal !== "email_parent") return { status: "error", expire: true, message: "Lien de confirmation invalide ou expiré." };
  const code = String(sh.code);
  const now = new Date().toISOString();
  const { data: prof } = await adminClient.from("profiles").select("consentement_parent_at").eq("code", code).maybeSingle();
  const maj: Record<string, unknown> = {};
  if (!prof?.consentement_parent_at) maj.consentement_parent_at = now;
  if (p.optin_marketing !== undefined) { maj.optin_marketing = !!p.optin_marketing; maj.optin_marketing_at = p.optin_marketing ? now : null; }
  if (Object.keys(maj).length) await adminClient.from("profiles").update(maj).eq("code", code);
  await adminClient.from("consentements").insert({
    code, produit: "compte", texte_version: String(p.texte_version || "P-X0-confirmation").slice(0, 40),
    texte_hash: String(p.texte_hash || "").slice(0, 128), cases: p.optin_marketing ? ["optin_marketing"] : [],
  });
  await mxLogEvent(code, "parent_confirm", { optin: !!p.optin_marketing });
  return { status: "success", confirme: true, optin_marketing: !!p.optin_marketing };
}

// Journal minimal du funnel (50-offre-conversion §8) : pas d'IP, pas d'email, pas d'user-agent.
async function mxLogEvent(code: string | null, event: string, meta: Record<string, unknown>) {
  try { await adminClient.from("funnel_events").insert({ code, event, meta }); } catch { /* jamais bloquant */ }
}

// Streak serveur : jours avec au moins une réponse (réponses items + scores legacy), 400 derniers jours.
async function mxStreakEleve(code: string) {
  const today = todayParis();
  const depuis = mxAjoutJours(today, -400);
  const { data: a } = await adminClient.from("reponses_items").select("date").eq("code", code).gte("date", depuis);
  const { data: b } = await adminClient.from("scores").select("date").eq("code", code).gte("date", depuis);
  const dates = [...(a || []), ...(b || [])].map((r: Record<string, unknown>) => String(r.date).slice(0, 10));
  return mxStreak(dates, today);
}

// ── LOG_FUNNEL_EVENT {code?, event, meta?} — événements côté client (liste fermée) ──
const MX_EVENTS_CLIENT = ["paywall_view", "checkout_click", "pdf_open", "share_opened_app"];
async function logFunnelEvent(p: Record<string, unknown>) {
  const event = String(p.event || "");
  if (!MX_EVENTS_CLIENT.includes(event)) return { status: "error", message: "Événement non autorisé." };
  // Le code n'est retenu que s'il est prouvé (jeton de session, ou lien de partage parent) :
  // sinon n'importe qui pourrait écrire des événements au nom d'un élève.
  let code: string | null = null;
  if (p.access_token && p.code) { const a = await mxAuth(p, { lectureAdmin: true }); code = a ? String(a.profile.code) : null; }
  else if (p.token) { const sh = await mxPartageValide(String(p.token)); code = sh ? String(sh.code) : null; }
  const meta = (p.meta && typeof p.meta === "object" && JSON.stringify(p.meta).length <= 500) ? p.meta as Record<string, unknown> : {};
  await mxLogEvent(code, event, meta);
  return { status: "success" };
}

// ── SET_PREFERENCES {code, email, email_eleve?, optin_marketing?, date_brevet_blanc?, consentement_parent?} ──
async function setPreferences(p: Record<string, unknown>) {
  if (!p.email) return { status: "error", message: "Email du compte requis." };
  const pr = await mxProfil(p);
  if ("error" in pr) return { status: "error", message: pr.error, auth_requise: pr.auth_requise };
  const maj: Record<string, unknown> = {};
  if (p.email_eleve !== undefined) {
    const e = String(p.email_eleve || "").trim().toLowerCase();
    if (e && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e)) return { status: "error", message: "Email élève invalide." };
    maj.email_eleve = e || null;
  }
  if (p.optin_marketing !== undefined) { maj.optin_marketing = !!p.optin_marketing; maj.optin_marketing_at = p.optin_marketing ? new Date().toISOString() : null; }
  if (p.date_brevet_blanc !== undefined) {
    const d = String(p.date_brevet_blanc || "");
    if (d && !/^\d{4}-\d{2}-\d{2}$/.test(d)) return { status: "error", message: "Date invalide (AAAA-MM-JJ)." };
    maj.date_brevet_blanc = d || null;
  }
  if (p.consentement_parent === true) maj.consentement_parent_at = new Date().toISOString();
  if (!Object.keys(maj).length) return { status: "error", message: "Rien à mettre à jour." };
  await adminClient.from("profiles").update(maj).eq("code", String(pr.profile.code));
  return { status: "success" };
}

// ── LOG_CONSENT {code, email?, produit, texte_version, texte_hash, cases[]} — avant redirection Stripe ──
// Appelable par l'élève connecté (access_token) OU par la page parent avec le jeton du lien de partage
// (le parent n'a pas de session : c'est lui qui paie depuis /b/<token>).
async function logConsent(p: Record<string, unknown>) {
  let codeEleve: string;
  if (!p.access_token && p.token) {
    const sh = await mxPartageValide(String(p.token));
    if (!sh) return { status: "error", expire: true, message: "Lien expiré." };
    codeEleve = String(sh.code);
  } else {
    const pr = await mxProfil(p);
    if ("error" in pr) return { status: "error", message: pr.error, auth_requise: pr.auth_requise };
    codeEleve = String(pr.profile.code);
  }
  const produit = String(p.produit || "");
  if (!["diag_complet", "programme_brevet", "programme_upgrade", "compte"].includes(produit))
    return { status: "error", message: "Produit inconnu." };
  if (!p.texte_version || !p.texte_hash) return { status: "error", message: "texte_version et texte_hash requis." };
  await adminClient.from("consentements").insert({
    code: codeEleve, produit, texte_version: String(p.texte_version).slice(0, 40),
    texte_hash: String(p.texte_hash).slice(0, 128),
    cases: Array.isArray(p.cases) ? (p.cases as unknown[]).map(String).slice(0, 10) : [],
  });
  return { status: "success" };
}

// ── Partage de la carte au parent (lien /b/<token>) ──
function mxJeton(): string {
  const b = new Uint8Array(24); // 192 bits
  crypto.getRandomValues(b);
  return Array.from(b).map((x) => x.toString(16).padStart(2, "0")).join("");
}

// Carte réduite pour la page parent : pas de réponses brutes, pas d'email, pas d'exemples.
function mxCartePartage(carte: Record<string, unknown>) {
  const comps = (carte.competences || []) as Record<string, unknown>[];
  const titre = (id: unknown) => String(comps.find((c) => c.id === id)?.titre_eleve || id);
  const pf = comps.find((c) => c.id === carte.point_faible);
  return {
    eleve: { prenom: (carte.eleve as Record<string, unknown>)?.prenom || "" }, type: carte.type, date: carte.date,
    n_questions: carte.n_questions, duree_min: carte.duree_min,
    score_global: carte.score_global, phrase_cle: carte.phrase_cle, domaines: carte.domaines,
    point_faible: pf ? { id: pf.id, titre_eleve: pf.titre_eleve, niveau_origine: pf.niveau_origine, statut: pf.statut,
      cause_racine: pf.cause_racine, n_bloque: ((pf.bloque || []) as unknown[]).length } : null,
    priorites: ((carte.priorites || []) as string[]).slice(0, 3).map((id) => ({ id, titre_eleve: titre(id) })),
    points_forts: ((carte.points_forts || []) as string[]).slice(0, 3).map((id) => ({ id, titre_eleve: titre(id) })),
    message_parent: carte.message_parent, fiabilite: carte.fiabilite, alerte: carte.alerte || null,
  };
}

// ── CREATE_SHARE {code, email?, canal?} → {token, url, expires_at} ──
async function createShare(p: Record<string, unknown>) {
  const pr = await mxProfil(p);
  if ("error" in pr) return { status: "error", message: pr.error, auth_requise: pr.auth_requise };
  const code = String(pr.profile.code);
  const diag = await mxDernierDiag(code);
  if (!diag) return { status: "error", message: "Aucun diagnostic terminé à partager." };
  const token = mxJeton();
  const expires_at = new Date(Date.now() + 30 * 86400000).toISOString();
  const { error } = await adminClient.from("bilan_partages").insert({
    token, code, diagnostic_id: diag.id, type_carte: diag.type, expires_at,
    // « email_parent » est réservé au lien du mail P-X0 (il vaut confirmation parentale) : jamais depuis l'app
    canal: (String(p.canal || "").slice(0, 20) || null)?.replace(/^email_parent$/, "app") || null,
  });
  if (error) return { status: "error", message: "Partage impossible : " + error.message };
  await mxLogEvent(code, "share_created", { canal: String(p.canal || "").slice(0, 20) });
  return { status: "success", token, url: "https://matheux.fr/b/" + token, expires_at };
}

// ── REVOKE_SHARE {code, email?, token? } — sans token : révoque tous les liens actifs de l'élève ──
async function revokeShare(p: Record<string, unknown>) {
  const pr = await mxProfil(p);
  if ("error" in pr) return { status: "error", message: pr.error, auth_requise: pr.auth_requise };
  let q = adminClient.from("bilan_partages").update({ revoked_at: new Date().toISOString() })
    .eq("code", String(pr.profile.code)).is("revoked_at", null);
  if (p.token) q = q.eq("token", String(p.token));
  await q;
  return { status: "success" };
}

// ── GET_BILAN_PARTAGE {token} — PUBLIC (page bilan.html, /b/<token>) ──
async function getBilanPartage(p: Record<string, unknown>) {
  const token = String(p.token || "");
  const expire = { status: "error", expire: true, message: "Ce lien a expiré. Demandez à votre enfant de vous en renvoyer un." };
  if (!/^[0-9a-f]{48}$/.test(token)) return expire;
  const { data: sh } = await adminClient.from("bilan_partages").select("*").eq("token", token).maybeSingle();
  if (!sh || sh.revoked_at || String(sh.expires_at) < new Date().toISOString()) return expire;
  const { data: diag } = await adminClient.from("diagnostics").select("carte_json").eq("id", sh.diagnostic_id).maybeSingle();
  if (!diag?.carte_json) return expire;
  const { data: prof } = await adminClient.from("profiles").select("code, premium, premium_end, email").eq("code", sh.code).maybeSingle();
  const { data: achats } = prof ? await adminClient.from("achats").select("produit").eq("code", prof.code) : { data: [] };
  const droits = prof ? mxDroits(prof, (achats || []) as { produit: string }[], todayParis()) : null;
  await adminClient.from("bilan_partages").update({ vues: (Number(sh.vues) || 0) + 1, dernier_vu_at: new Date().toISOString() }).eq("token", token);
  if (!sh.vues) await mxLogEvent(String(sh.code), "share_viewed", {});
  const carte = mxCartePartage(diag.carte_json as Record<string, unknown>);
  const prenom = String(carte.eleve.prenom || "votre enfant");
  return {
    status: "success", carte, code: sh.code, // le code sert de client_reference_id pour le paiement depuis la page parent
    acces: droits?.acces || "free", prix_cents: droits?.prix_cents || null, expires_at: sh.expires_at,
    og: {
      title: "Le bilan maths de " + prenom + " (3e)",
      description: String(carte.phrase_cle || "").slice(0, 190),
    },
  };
}

// ── GET_CARTE {code, email?, diagnostic_id?} ──
async function getCarte(p: Record<string, unknown>) {
  const pr = await mxProfil(p, { lectureAdmin: true });
  if ("error" in pr) return { status: "error", message: pr.error, auth_requise: pr.auth_requise };
  const { profile, droits } = pr;
  const code = String(profile.code);
  let diag: Record<string, unknown> | null;
  if (p.diagnostic_id) {
    const { data } = await adminClient.from("diagnostics").select("*").eq("id", String(p.diagnostic_id))
      .eq("code", code).eq("statut", "termine").maybeSingle();
    diag = data as Record<string, unknown> | null;
  } else diag = await mxDernierDiag(code);
  const { data: enCours } = await adminClient.from("diagnostics").select("id, type, etat_json")
    .eq("code", code).eq("statut", "en_cours");
  // Besoin API n°14 : liens de partage actifs (bandeau « pas encore vue par tes parents »)
  const { data: parts } = await adminClient.from("bilan_partages").select("token, created_at, expires_at, vues, dernier_vu_at, canal, revoked_at")
    .eq("code", code).is("revoked_at", null).order("created_at", { ascending: false });
  const partages = ((parts || []) as Record<string, unknown>[]).filter((x) => Date.parse(String(x.expires_at)) >= Date.now())
    .map((x) => ({ token: x.token, created_at: x.created_at, expires_at: x.expires_at, vues: Number(x.vues) || 0,
      dernier_vu_at: x.dernier_vu_at || null, canal: x.canal || null }));
  return {
    status: "success", droits, streak: await mxStreakEleve(code), partages,
    carte: mxMasquerCarte((diag?.carte_json || null) as Record<string, unknown> | null, droits.acces, await mxChargerRef()),
    diagnostic_id: diag?.id || null,
    en_cours: (enCours || []).map((d: Record<string, unknown>) => ({
      diagnostic_id: d.id, type: d.type, progression: mxProgression(d.etat_json as MxEtatDiag) })),
  };
}

// ── GET_ACCES {code, email?} ──
// produits : prix catalogue en centimes (source unique MX_PRODUITS), avec `offre` = metadata.produit du
// Payment Link correspondant. programme_upgrade = programme − diagnostic déduit (19 / 49 / 30 €).
// Ce que CET élève paierait : droits.prix_cents. Les URL des Payment Links restent dans app.html (OFFRE).
function mxCatalogue() {
  const prog = MX_PRODUITS.programme_brevet;
  return {
    diagnostic_complet: { ...MX_PRODUITS.diagnostic_complet, offre: "diag_complet" },
    programme_brevet: { ...prog, offre: "programme_brevet" },
    programme_upgrade: { libelle: prog.libelle + " (diagnostic complet déduit)", offre: "programme_upgrade",
      prix_cents: prog.prix_cents - (prog.deduction?.cents || 0), si: prog.deduction?.si || "diagnostic_complet" },
  };
}

async function getAcces(p: Record<string, unknown>) {
  const pr = await mxProfil(p, { lectureAdmin: true });
  if ("error" in pr) return { status: "error", message: pr.error, auth_requise: pr.auth_requise };
  return { status: "success", droits: pr.droits, produits: mxCatalogue() };
}

// ── GET_TRAINING {code, email?} — 5 exos du jour, idempotent (1 ligne daily_boosts / jour) ──
// Écrit dans daily_boosts (date = aujourd'hui) : l'app sait déjà rendre un boost et save_score
// source=BOOST incrémente exos_done. Chaque exo porte item_id + comp → maîtrise mise à jour.
async function getTraining(p: Record<string, unknown>) {
  const pr = await mxProfil(p);
  if ("error" in pr) return { status: "error", message: pr.error, auth_requise: pr.auth_requise };
  const { profile, droits } = pr;
  const code = String(profile.code);
  const today = todayParis();
  const dernier = await mxDernierDiag(code);
  const dernierComplet = await mxDernierDiag(code, ["complet", "mensuel"]);
  const rediagnostic_du = mxRediagDu(dernierComplet ? String(dernierComplet.finished_at || "").slice(0, 10) : null, today, droits.acces);

  const { data: existant } = await adminClient.from("daily_boosts").select("boost_json, exos_done")
    .eq("code", code).eq("date", today).maybeSingle();
  const streak = await mxStreakEleve(code);
  if (p.comp) return await mxEntrainementLibre(p, code, droits, today, existant as Record<string, unknown> | null, streak);
  if (existant) {
    const b = existant.boost_json as Record<string, unknown>;
    // séances créées avant les Besoins API n°2/4 : on complète à la lecture (sans réécrire la séance)
    if (b && !b.pourquoi && Array.isArray(b.exos)) mxEnrichirBoost(b, await mxChargerRef(), await mxChargerMaitrise(code));
    return { status: "success", boost: b, exos_done: existant.exos_done || 0, deja: true, rediagnostic_du, streak, droits };
  }
  if (!dernier) return { status: "error", message: "Fais d'abord le diagnostic express.", diagnostic_requis: true };

  const ref = await mxChargerRef();
  const mt = await mxChargerMaitrise(code);
  const { data: hist } = await adminClient.from("reponses_items").select("item_id, date, ok, contexte")
    .eq("code", code).gte("date", mxAjoutJours(today, -90));
  const zone = droits.entrainement_complet ? null : mxZoneGratuite(dernier.carte_json as Record<string, unknown>);
  const sel = mxChoisirEntrainement(ref, mt, {
    code, date: today, zone,
    historique: ((hist || []) as Record<string, unknown>[]).map((h) => ({ item_id: String(h.item_id), date: String(h.date), ok: !!h.ok, contexte: String(h.contexte || "") })),
  });
  if (!sel.exos.length) return { status: "error", message: "Banque vide pour cette zone — réassort nécessaire." };
  const boost = {
    generatedBy: "moteur_v2", date: today, focus: sel.focus, zone, zone_maitrisee: sel.zone_maitrisee,
    banque_insuffisante: sel.banque_insuffisante,
    exos: sel.exos.map((e, i) => ({
      ...e.item, item_id: e.item.id, comp: e.item.comp, role: e.role, boostIdx: i, num: i + 1,
      type: mxTypeItem(e.item), categorie: (ref.comps[e.item.comp].chapitres_legacy || [])[0] || e.item.comp,
    })),
  };
  mxEnrichirBoost(boost, ref, mt);
  await adminClient.from("daily_boosts").upsert({ code, date: today, boost_json: boost, exos_done: 0 },
    { onConflict: "code,date", ignoreDuplicates: true });
  const { data: final } = await adminClient.from("daily_boosts").select("boost_json, exos_done")
    .eq("code", code).eq("date", today).maybeSingle();
  return { status: "success", boost: final?.boost_json || boost, exos_done: final?.exos_done || 0, deja: false,
    rediagnostic_du, zone_maitrisee: sel.zone_maitrisee, streak, droits };
}

// Besoins API n°2 et 4 : err_libelles par exo, focus_titres, pourquoi (phrase déterministe).
function mxEnrichirBoost(boost: Record<string, unknown>, ref: MxRef, mt: Record<string, MxMaitrise>) {
  const exos = (boost.exos || []) as Record<string, unknown>[];
  for (const e of exos) if (!e.err_libelles) e.err_libelles = mxErrLibelles(ref, e as { err?: Record<string, string> });
  const focus = ((boost.focus || []) as string[]);
  boost.focus_titres = mxFocusTitres(ref, focus);
  if (!boost.pourquoi) {
    boost.pourquoi = mxPourquoi(ref, mt, focus, exos.map((e) => ({ comp: String(e.comp || ""), role: String(e.role || "") })),
      !!boost.zone_maitrisee);
  }
  return boost;
}

// ── GET_TRAINING {code, access_token, comp} : entraînement libre (Besoin API n°5) ──
// Programme Brevet uniquement. 5 items sur UNE compétence, hors quota : n'écrit PAS daily_boosts,
// autant de séries que voulu (un item vu il y a < 3 jours n'est resservi qu'en dernier recours ; les
// items de la séance du jour sont exclus). L'app envoie ensuite save_score avec source « LIBRE ».
async function mxEntrainementLibre(p: Record<string, unknown>, code: string, droits: ReturnType<typeof mxDroits>,
  today: string, existant: Record<string, unknown> | null, streak: unknown) {
  if (!droits.entrainement_complet) {
    return { status: "error", message: "L'entraînement libre fait partie du Programme Brevet.", paywall: "programme_brevet", droits };
  }
  const ref = await mxChargerRef();
  const comp = String(p.comp || "");
  if (!ref.comps[comp] || !(ref.itemsParComp[comp] || []).length) return { status: "error", message: "Compétence inconnue ou sans exercice." };
  const mt = await mxChargerMaitrise(code);
  // Plusieurs séries le même jour : « dernière réponse » = la plus récente à la seconde près (created_at), pas au jour.
  const { data: hist } = await adminClient.from("reponses_items").select("item_id, date, ok, contexte, created_at")
    .eq("code", code).gte("date", mxAjoutJours(today, -90)).order("created_at", { ascending: true });
  const rows = ((hist || []) as Record<string, unknown>[]).map((h) => ({ item_id: String(h.item_id), date: String(h.date), ok: !!h.ok, contexte: String(h.contexte || "") }));
  const dernier: Record<string, MxHist> = {};
  for (const h of rows) dernier[h.item_id] = h;
  const pris = new Set<string>((((existant?.boost_json as Record<string, unknown>)?.exos || []) as { item_id?: string }[])
    .map((e) => String(e.item_id || "")).filter(Boolean));
  const lvl = mxLvlCible(mt[comp]);
  const items: MxItem[] = [];
  for (const strict of [true, false]) {
    while (items.length < MX.EXOS_PAR_JOUR) {
      const it = mxChoisirItemTrain(ref, comp, lvl, dernier, today, code, pris, strict);
      if (!it) break;
      pris.add(it.id); items.push(it);
    }
  }
  if (!items.length) return { status: "error", message: "Plus d'exercice disponible sur cette compétence pour l'instant." };
  // num unique dans la journée (dédup scores code+chapitre+num_exo+date+source) : 100 + réponses du jour
  const base = 100 + rows.filter((h) => h.date === today && h.contexte === "train").length;
  const titre = ref.comps[comp].titre_eleve || ref.comps[comp].titre;
  const boost: Record<string, unknown> = {
    generatedBy: "libre", libre: true, date: today, comp, focus: [comp], zone: null,
    banque_insuffisante: items.length < MX.EXOS_PAR_JOUR,
    pourquoi: "Entraînement libre sur « " + titre + " » : enchaîne autant de séries que tu veux.",
    exos: items.map((it, i) => ({
      ...it, item_id: it.id, comp: it.comp, role: "libre", boostIdx: i, num: base + i + 1,
      type: mxTypeItem(it), categorie: (ref.comps[it.comp].chapitres_legacy || [])[0] || it.comp,
    })),
  };
  mxEnrichirBoost(boost, ref, mt);
  return { status: "success", libre: true, boost, exos_done: 0, source_score: "LIBRE", streak, droits };
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

// Vérifie que l'appel vient d'un admin authentifié (jeton de session Supabase), pas d'un
// simple `code` : le code admin est public (dépôt GitHub). Faille corrigée le 24/09.
// Même vérification de jeton que les actions élève (mxSessionUid), + is_admin.
async function requireAdmin(p: Record<string, unknown>): Promise<Record<string, unknown> | null> {
  const uid = await mxSessionUid(p);
  if (!uid) return { status: "error", message: "Accès refusé.", auth_requise: true };
  const { data: prof } = await adminClient.from("profiles")
    .select("is_admin").eq("id", uid).maybeSingle();
  return prof?.is_admin ? null : { status: "error", message: "Accès refusé." };
}

async function getAdminOverview(p: Record<string, unknown>) {
  const denied = await requireAdmin(p);
  if (denied) return denied;

  const { data: users } = await adminClient.from("profiles").select("*").eq("is_test", false);
  const { data: allScores } = await adminClient.from("scores").select("code, chapitre, resultat, date, source");
  const { data: allBoosts } = await adminClient.from("daily_boosts").select("code, date, exos_done");
  const { data: allProgress } = await adminClient.from("progress").select("*");
  const { data: allSuivi } = await adminClient.from("suivi").select("*");

  // Monitoring du nouveau parcours (Besoin API n°10) : diagnostics, invités, achats, funnel agrégé.
  const { data: diags } = await adminClient.from("diagnostics")
    .select("id, code, type, statut, n_questions, started_at, finished_at, carte_json");
  const diagnostics = ((diags || []) as Record<string, unknown>[]).map((d) => {
    const c = (d.carte_json || null) as Record<string, unknown> | null;
    return { id: d.id, code: d.code, type: d.type, statut: d.statut, n_questions: d.n_questions,
      started_at: d.started_at, finished_at: d.finished_at,
      score_global: c?.score_global ?? null, point_faible: c?.point_faible ?? null,
      fiabilite: (c?.fiabilite as Record<string, unknown> | undefined)?.niveau ?? null };
  });
  const diagnostics_stats: Record<string, Record<string, number>> = {};
  for (const d of diagnostics) {
    const k = String(d.type), st = String(d.statut);
    diagnostics_stats[k] ||= { en_cours: 0, termine: 0, abandonne: 0 };
    diagnostics_stats[k][st] = (diagnostics_stats[k][st] || 0) + 1;
  }
  const { data: invs } = await adminClient.from("diagnostics_invites").select("statut, expires_at");
  const invites: Record<string, number> = { en_cours: 0, termine: 0, rattache: 0, expires: 0 };
  for (const i of (invs || []) as Record<string, unknown>[]) {
    if (i.statut !== "rattache" && Date.parse(String(i.expires_at)) < Date.now()) invites.expires++;
    else invites[String(i.statut)] = (invites[String(i.statut)] || 0) + 1;
  }
  const { data: achats } = await adminClient.from("achats").select("*").order("created_at", { ascending: false });
  const ca_cents = ((achats || []) as Record<string, unknown>[]).filter((a) => !a.rembourse_at)
    .reduce((t, a) => t + (Number(a.montant_cents) || 0), 0);
  const { data: evs } = await adminClient.from("funnel_events").select("event, created_at");
  const j7 = Date.now() - 7 * 86400000, j30 = Date.now() - 30 * 86400000;
  const funnel: Record<string, { total: number; j7: number; j30: number }> = {};
  for (const e of (evs || []) as Record<string, unknown>[]) {
    const f = funnel[String(e.event)] ||= { total: 0, j7: 0, j30: 0 };
    const t = Date.parse(String(e.created_at));
    f.total++; if (t >= j7) f.j7++; if (t >= j30) f.j30++;
  }

  return {
    status: "success",
    users: users || [],
    scores: allScores || [],
    boosts: allBoosts || [],
    progress: allProgress || [],
    suivi: allSuivi || [],
    diagnostics, diagnostics_stats, invites,
    achats: achats || [], ca_cents,
    funnel,
  };
}

// ── PUBLISH_ADMIN_BOOST ─────────────────────────────────────

async function publishAdminBoost(p: Record<string, unknown>) {
  const denied = await requireAdmin(p);
  if (denied) return denied;
  // Audit 2026-04-11 (porté) : l'élève visé peut arriver en targetCode (le front admin envoie adminCode + targetCode)
  const code = String(p.targetCode || p.code);
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
  const denied = await requireAdmin(p);
  if (denied) return denied;
  const code = String(p.targetCode || p.code);
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

  // Accès one-shot non expirant : premium_end reste null (les checks isPremium
  // partout dans ce fichier ne testent la date que si premium_end est renseigné).
  // niveau = provient des metadata du Payment Link Stripe (6EME/5EME/4EME/3EME),
  // conservé pour reporting admin — l'accès lui-même n'est pas restreint par niveau
  // côté serveur (un profil = un niveau, cf. profiles.level).
  const niveau = String(p.niveau || "").trim().toUpperCase();

  // Refonte diagnostic 3e (docs/specs/50-offre-conversion.md §4) : metadata.produit ∈ {diag_complet,
  // programme_brevet, programme_upgrade}, client_reference_id = code élève (clé fiable : le parent paie
  // souvent avec une autre adresse). Achat tracé dans `achats` ; droits calculés par mxDroits.
  // diag_complet ne donne PAS premium (premium = accès complet legacy). Sans metadata.produit : legacy.
  const codeRef = String(p.code || "").trim().toUpperCase();
  let prof: { code: string } | null = null;
  if (/^[A-Z0-9]{6}$/.test(codeRef)) {
    const { data } = await adminClient.from("profiles").select("code").eq("code", codeRef).maybeSingle();
    prof = data as { code: string } | null;
  }
  if (!prof) {
    const { data } = await adminClient.from("profiles").select("code").eq("email", email).maybeSingle();
    prof = data as { code: string } | null;
  }
  const offre = String(p.produit || "").trim();
  const produit = ({ diag_complet: "diagnostic_complet", diagnostic_complet: "diagnostic_complet",
    programme_brevet: "programme_brevet", programme_upgrade: "programme_brevet" } as Record<string, string>)[offre] || "";
  if (produit) {
    const achat = {
      code: prof?.code || null, email, produit, offre, offre_version: p.offre_version ? String(p.offre_version) : null,
      niveau: niveau || null,
      montant_cents: Number.isFinite(Number(p.montant_cents)) ? Number(p.montant_cents) : null,
      stripe_session_id: p.session_id ? String(p.session_id) : null,
    };
    if (achat.stripe_session_id) {
      await adminClient.from("achats").upsert(achat, { onConflict: "stripe_session_id", ignoreDuplicates: true });
    } else {
      await adminClient.from("achats").insert(achat);
    }
    await mxLogEvent(prof?.code || null, "purchase", { produit: offre, montant: achat.montant_cents });
    if (produit === "diagnostic_complet") return { status: "success", produit };
  }

  const update: Record<string, unknown> = { premium: true, premium_end: null };
  if (niveau) update.premium_niveau = niveau;

  if (prof) await adminClient.from("profiles").update(update).eq("code", prof.code);
  else await adminClient.from("profiles").update(update).eq("email", email);

  return { status: "success" };
}

// ── UNSUBSCRIBE ─────────────────────────────────────────────

async function unsubscribeEmail(p: Record<string, unknown>) {
  const email = String(p.email || "").trim().toLowerCase();
  if (!email) return { status: "error", message: "email requis." };

  // Log dans emails (legacy) + email_logs (nouveau — check par sendMarketingEmail)
  await adminClient.from("emails").insert({
    email, type: "UNSUB", date: todayParis(),
  });
  await adminClient.from("email_logs").insert({
    email, prenom: "", type: "UNSUB", statut: "unsub",
    created_at: new Date().toISOString(),
  });

  return { status: "success" };
}

// ── RESET_PASSWORD ───────────────────────────────────────────

async function resetPassword(p: Record<string, unknown>) {
  const email = String(p.email || "").trim().toLowerCase();
  const password = String(p.password || "").trim();
  if (!email || !password) return { status: "error", message: "Email et mot de passe requis." };

  // Jeton de récupération obligatoire (access_token du lien envoyé par forgot_password).
  // Avant le 24/09 : aucun contrôle → n'importe qui changeait le mot de passe d'un compte avec son email.
  const token = String(p.access_token || "");
  if (!token) return { status: "error", message: "Lien de réinitialisation invalide ou expiré." };
  const { data: tokData, error: tokErr } = await adminClient.auth.getUser(token);
  if (tokErr || !tokData?.user || String(tokData.user.email || "").toLowerCase() !== email) {
    return { status: "error", message: "Lien de réinitialisation invalide ou expiré." };
  }
  const profile = { id: tokData.user.id };

  // Mettre à jour le mot de passe via admin API (Supabase Auth gère le hash)
  const { error } = await adminClient.auth.admin.updateUserById(profile.id, { password });
  if (error) return { status: "error", message: error.message };

  // Nullifier le fallback legacy password_hash pour éviter tout stockage résiduel
  await adminClient.from("profiles").update({ password_hash: null }).eq("id", profile.id);

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
  if (!(await mxAuth(p))) return MX_AUTH_REFUS; // Besoin API n°8
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

// ── PROXY GAS (legacy, plus d'emails) ────────────

async function proxyGas(p: Record<string, unknown>) {
  try {
    const resp = await fetch(GAS_URL, { method: "POST", body: JSON.stringify(p) });
    return await resp.json();
  } catch (err) {
    return { status: "error", message: "GAS proxy error: " + String(err) };
  }
}

// ── RESEND — envoi d'emails ────────────────────────────────

async function resendSend(to: string, subject: string, html: string, replyTo = "contact@matheux.fr"): Promise<{ ok: boolean; error?: string }> {
  try {
    const resp = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: "Matheux <no-reply@matheux.fr>",
        to, subject, html, reply_to: replyTo,
      }),
    });
    if (!resp.ok) {
      const err = await resp.text();
      return { ok: false, error: err };
    }
    return { ok: true };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}

// ── Templates emails ────────────────────────────────────────
// Layout unifié : table Outlook-safe, ligne bleue top, preheader, signature cohérente

const FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif";

function emailWrap(email: string, preheader: string, body: string): string {
  const unsubLink = "https://matheux.fr/unsubscribe?email=" + encodeURIComponent(email);
  return (
    // Preheader invisible (preview Gmail/Outlook)
    '<span style="display:none;font-size:0;color:transparent;max-height:0;overflow:hidden;">' + preheader + '\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0</span>' +
    // Wrapper centré (Outlook-safe)
    '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#f9fafb;"><tr><td align="center" style="padding:24px 0;">' +
    '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="520" style="max-width:520px;width:100%;font-family:' + FONT + ';">' +
    // Ligne bleue top
    '<tr><td style="background:#1E40AF;height:4px;font-size:0;line-height:0;">&nbsp;</td></tr>' +
    // Logo
    '<tr><td style="padding:24px 28px 0;background:#ffffff;"><p style="font-size:13px;font-weight:800;color:#1E40AF;letter-spacing:2px;text-transform:uppercase;margin:0;">MATHEUX</p></td></tr>' +
    // Body
    '<tr><td style="background:#ffffff;padding:24px 28px 32px;">' + body + '</td></tr>' +
    // Signature
    '<tr><td style="background:#ffffff;padding:0 28px 24px;border-top:1px solid #e5e7eb;">' +
    '<p style="color:#1e293b;font-size:15px;font-weight:700;margin:16px 0 2px;">Nicolas</p>' +
    '<p style="color:#6b7280;font-size:13px;margin:0;">Fondateur de Matheux</p>' +
    '</td></tr>' +
    // Footer désinscription
    '<tr><td style="padding:16px 28px;text-align:center;background:#f9fafb;">' +
    '<p style="font-size:11px;color:#9ca3af;margin:0;">Matheux · 100 % pédagogique, 0 % pression · <a href="' + unsubLink + '" style="color:#9ca3af;text-decoration:underline;">Se désinscrire</a></p>' +
    '</td></tr>' +
    '</table></td></tr></table>'
  );
}

function emailCTA(href: string, label: string, gradient = false): string {
  const bg = gradient ? 'background:linear-gradient(135deg,#4338ca,#6366f1);' : 'background:#1E40AF;';
  return (
    '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td align="center" style="padding:24px 0;">' +
    '<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>' +
    '<td style="' + bg + 'border-radius:8px;text-align:center;">' +
    '<a href="' + href + '" style="display:inline-block;padding:14px 32px;color:#ffffff;font-size:15px;font-weight:700;text-decoration:none;letter-spacing:-.2px;">' + label + '</a>' +
    '</td></tr></table></td></tr></table>'
  );
}

// Un Payment Link Stripe par niveau (29,99€, accès non expirant) — cf. metadata.niveau
// configuré sur chaque lien, lu par le webhook (stripeWebhook ci-dessous).
const STRIPE_LINKS_PAR_NIVEAU: Record<string, string> = {
  "6EME": "https://buy.stripe.com/14A8wRgky4rHf0Q3yvb3q03",
  "5EME": "https://buy.stripe.com/00waEZ0lA6zP1a0glhb3q04",
  "4EME": "https://buy.stripe.com/6oU4gBgkybU9g4Uglhb3q05",
  "3EME": "https://buy.stripe.com/3cI9AVd8maQ51a05GDb3q06",
};
function stripeUrlForNiveau(niveau: string): string {
  return STRIPE_LINKS_PAR_NIVEAU[niveau] || STRIPE_LINKS_PAR_NIVEAU["3EME"];
}
function niveauLabel(niveau: string): string {
  const labels: Record<string, string> = { "6EME": "6ème", "5EME": "5ème", "4EME": "4ème", "3EME": "3ème", "1ERE": "1ère" };
  return labels[niveau] || "sa classe";
}

function emailHighlight(text: string): string {
  return (
    '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:20px 0;"><tr>' +
    '<td style="background:#eef2ff;border:1px solid #c7d2fe;border-radius:8px;padding:16px 20px;text-align:center;">' +
    '<p style="color:#1E40AF;font-size:15px;font-weight:800;margin:0;">' + text + '</p>' +
    '</td></tr></table>'
  );
}

// ── J+0 : Welcome ──────────────────────────────────────────

function templateJ0(prenom: string, email: string): { subject: string; html: string } {
  return {
    subject: prenom + " est inscrit — ses premiers exos arrivent demain",
    html: emailWrap(email, "5 exercices sur mesure, 10 minutes, adaptés à son niveau.",
      '<p style="color:#1e293b;font-size:20px;font-weight:800;line-height:1.4;margin:0 0 20px;">' + prenom + ' est inscrit. Demain matin, 5\u00a0exercices sur mesure l\u2019attendent.</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.8;margin:0 0 24px;">Bonjour,</p>' +
      '<p style="color:#1e293b;font-size:16px;line-height:1.8;font-weight:700;margin:0 0 12px;">Concrètement, voilà comment ça fonctionne :</p>' +
      '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 24px;"><tr><td style="padding:12px 16px;background:#f8fafc;border-left:3px solid #1E40AF;border-radius:0 6px 6px 0;">' +
      '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">' +
      '<tr><td style="padding:4px 0;color:#374151;font-size:15px;line-height:1.8;"><strong style="color:#1E40AF;">1.</strong> Chaque jour, <strong>5 exercices ciblés</strong> sur ses lacunes</td></tr>' +
      '<tr><td style="padding:4px 0;color:#374151;font-size:15px;line-height:1.8;"><strong style="color:#1E40AF;">2.</strong> <strong>10 minutes</strong> suffisent — pas de surcharge</td></tr>' +
      '<tr><td style="padding:4px 0;color:#374151;font-size:15px;line-height:1.8;"><strong style="color:#1E40AF;">3.</strong> Le parcours <strong>s\u2019adapte</strong> automatiquement à ses réponses</td></tr>' +
      '</table></td></tr></table>' +
      '<p style="color:#1e293b;font-size:16px;line-height:1.8;font-weight:700;margin:0 0 12px;">Ce que vous allez observer :</p>' +
      '<p style="color:#374151;font-size:15px;line-height:1.8;margin:0 0 6px;">✔️ Il sait mieux par où commencer</p>' +
      '<p style="color:#374151;font-size:15px;line-height:1.8;margin:0 0 6px;">✔️ Il travaille régulièrement, sans qu\u2019on le pousse</p>' +
      '<p style="color:#374151;font-size:15px;line-height:1.8;margin:0 0 24px;">✔️ Et surtout… <strong>il reprend confiance</strong></p>' +
      emailHighlight("Dès demain matin, son premier boost sur mesure l\u2019attend.") +
      '<p style="color:#374151;font-size:15px;line-height:1.7;margin:0 0 8px;">Chaque semaine, vous recevrez un <strong>bilan clair</strong> : ce qui est acquis, ce qui bloque, et ce qui progresse.</p>' +
      emailCTA("https://matheux.fr/app.html", "Ouvrir Matheux →") +
      '<p style="color:#374151;font-size:14px;line-height:1.8;margin:0 0 10px;">J\u2019ai créé Matheux après des années à donner des cours de maths. Le même constat revenait : les élèves comprennent en cours, mais ne s\u2019entraînent pas assez entre les séances.</p>' +
      '<p style="color:#374151;font-size:14px;line-height:1.8;margin:0 0 10px;">Le problème n\u2019est presque jamais la compréhension. <strong>C\u2019est la pratique.</strong></p>' +
      '<p style="color:#374151;font-size:14px;line-height:1.8;margin:0;">Une question ? <strong>Répondez à cet email</strong>, je lis tout personnellement.</p>'
    ),
  };
}

// ── J+1 : "Son boost est prêt" ─────────────────────────────

function templateJ1(prenom: string, email: string): { subject: string; html: string } {
  return {
    subject: "Le premier boost de " + prenom + " est prêt 🎯",
    html: emailWrap(email, "5 exercices ciblés, 10 minutes — c'est parti.",
      '<p style="color:#1e293b;font-size:20px;font-weight:800;line-height:1.4;margin:0 0 20px;">Le premier boost de ' + prenom + ' est prêt.</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.8;margin:0 0 16px;">Bonjour,</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.8;margin:0 0 16px;">5 exercices ciblés sur les résultats de son diagnostic l\'attendent. C\'est court (10 minutes), adapté à son niveau, et ça commence à combler ses lacunes dès aujourd\'hui.</p>' +
      emailHighlight("🎯 5 exercices · 10 minutes · adapté à " + prenom) +
      emailCTA("https://matheux.fr/app.html", "Commencer le boost →") +
      '<p style="color:#6b7280;font-size:14px;line-height:1.6;margin:0;">Un petit rituel quotidien vaut mieux qu\'une grosse session de temps en temps. 😉</p>'
    ),
  };
}

// ── J+3 : Check-in engagement ───────────────────────────────

function templateJ3(prenom: string, email: string, objectif: string): { subject: string; html: string } {
  const variants: Record<string, string> = {
    lacunes: "Les premiers exercices permettent de cibler précisément ce qui bloque " + prenom + " — pas les difficultés supposées, les vraies. C'est là que le diagnostic devient utile.",
    chapitre_jour: "La régularité, c'est la clé. Un chapitre par jour, 10 minutes — si " + prenom + " tient ce rythme cette semaine, les résultats suivront.",
    brevet: "Le brevet, ça se prépare dans la durée. Ces premiers jours posent les bases — les exercices style brevet arrivent au fur et à mesure de la progression.",
    toutes_matieres: prenom + " a accès à l'intégralité du programme. L'important à ce stade : trouver un rythme et rester régulier, même 10 minutes par jour.",
  };
  return {
    subject: "Comment ça se passe pour " + prenom + " ? 💪",
    html: emailWrap(email, "3 jours déjà — un petit point sur la progression.",
      '<h1 style="color:#1e293b;font-size:22px;font-weight:800;margin:0 0 20px;">3 jours déjà !</h1>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 12px;">Bonjour,</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 12px;">Cela fait 3 jours que ' + prenom + ' a rejoint Matheux.</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 12px;">' + (variants[objectif] || variants.lacunes) + '</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 0;"><strong>Petit rappel :</strong> le boost quotidien (5 exercices, ~10 minutes) est la clé. Régulier vaut mieux qu\'intense.</p>' +
      emailCTA("https://matheux.fr/app.html", "Voir sa progression →") +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 12px;">N\'hésitez pas à me faire un retour — un simple "ça va bien" ou "on galère sur les fractions" suffit. Je lis tous les messages.</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0;">Bon courage,</p>'
    ),
  };
}

// ── J+7 : Bilan semaine 1 + soft conversion ─────────────────

function templateJ7(prenom: string, email: string, objectif: string, niveau: string): { subject: string; html: string } {
  const variants: Record<string, string> = {
    lacunes: '<li>Identifié ses lacunes précises — pas celles de sa classe, les siennes</li><li>Travaillé sur des exercices vraiment ciblés</li><li>Posé les bases d\'un rattrapage durable</li>',
    chapitre_jour: '<li>Établi une routine quotidienne de travail</li><li>Progressé chapitre par chapitre à son rythme</li><li>Prouvé qu\'il pouvait tenir sur la durée</li>',
    brevet: '<li>Fait ses premiers exercices style brevet</li><li>Identifié les chapitres à travailler en priorité</li><li>Posé des bases solides pour la préparation</li>',
    toutes_matieres: '<li>Exploré plusieurs chapitres du programme</li><li>Repéré ses points forts et ses axes de travail</li><li>Pris ses premières marques sur Matheux</li>',
  };
  return {
    subject: "Bilan de la semaine de " + prenom + " ⭐",
    html: emailWrap(email, "Une semaine avec Matheux — voici le bilan.",
      '<h1 style="color:#1e293b;font-size:22px;font-weight:800;margin:0 0 20px;">Une semaine avec Matheux !</h1>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 12px;">Bonjour,</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 12px;">La première semaine de ' + prenom + ' sur Matheux touche à sa fin. Le simple fait de commencer, c\'est déjà 90 % du travail.</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 8px;">En une semaine, ' + prenom + ' a :</p>' +
      '<ul style="color:#374151;font-size:16px;line-height:1.8;padding-left:20px;margin:0 0 16px;">' +
      (variants[objectif] || variants.lacunes) + '</ul>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 0;">' + prenom + ' a accès à <strong>1 chapitre complet gratuit</strong> + ses boosts quotidiens. Pour débloquer tout le programme de ' + niveauLabel(niveau) + ', c\'est <strong>29,99 € en une fois</strong> — pas d\'abonnement, accès non expirant.</p>' +
      emailCTA(stripeUrlForNiveau(niveau), "Débloquer tous les chapitres →", true) +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 12px;">Si vous avez des questions avant de décider, répondez à cet email — je suis là.</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0;">Merci pour votre confiance,</p>'
    ),
  };
}

// ── J+14 : Conversion nudge (freemium → premium) ───────────

function templateJ14(prenom: string, email: string, niveau: string): { subject: string; html: string } {
  return {
    subject: prenom + " progresse — et si on passait à la vitesse supérieure ?",
    html: emailWrap(email, "2 semaines déjà — il est temps de passer aux choses sérieuses.",
      '<h1 style="color:#1e293b;font-size:22px;font-weight:800;margin:0 0 20px;">2 semaines déjà 🎉</h1>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 12px;">Bonjour,</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 12px;">' + prenom + ' utilise Matheux depuis 2 semaines. Peu d\'élèves tiennent aussi longtemps — c\'est un vrai signal de motivation.</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 16px;">Aujourd\'hui, ' + prenom + ' travaille sur <strong>1 chapitre gratuit</strong>. Mais le programme de ' + niveauLabel(niveau) + ' en compte plus d\'une dizaine.</p>' +
      '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 20px;"><tr><td style="background:#f8fafc;border-left:3px solid #1E40AF;border-radius:0 6px 6px 0;padding:16px 20px;">' +
      '<p style="color:#1e293b;font-size:15px;line-height:1.8;margin:0 0 6px;"><strong>Avec l\'accès complet :</strong></p>' +
      '<p style="color:#374151;font-size:15px;line-height:1.8;margin:0 0 4px;">✅ Tous les chapitres du programme</p>' +
      (niveau === "3EME"
        ? '<p style="color:#374151;font-size:15px;line-height:1.8;margin:0 0 4px;">✅ Exercices style Brevet</p>'
        : '<p style="color:#374151;font-size:15px;line-height:1.8;margin:0 0 4px;">✅ Exercices ciblés sur ses erreurs</p>') +
      '<p style="color:#374151;font-size:15px;line-height:1.8;margin:0 0 4px;">✅ Parcours adapté à ses lacunes</p>' +
      '<p style="color:#374151;font-size:15px;line-height:1.8;margin:0;">✅ Accès non expirant</p>' +
      '</td></tr></table>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 0;"><strong>29,99 € en une fois</strong> — pas d\'abonnement, pas de renouvellement, pas de surprise.</p>' +
      emailCTA(stripeUrlForNiveau(niveau), "Débloquer tout le programme →", true) +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0 0 12px;">Pas de pression — ' + prenom + ' garde son chapitre gratuit et ses boosts dans tous les cas. Mais plus tôt ' + prenom + ' comble ses lacunes, plus vite ça devient un réflexe.</p>' +
      '<p style="color:#374151;font-size:16px;line-height:1.6;margin:0;">Une question ? Répondez directement à cet email.</p>'
    ),
  };
}

// ── Action send_email — envoi via Resend ────────────────────

async function sendMarketingEmail(p: Record<string, unknown>) {
  const email = String(p.email || "").trim().toLowerCase();
  const prenom = String(p.name || p.prenom || "").trim();
  const day = Number(p.day ?? 0);
  const objectif = String(p.objectif || "lacunes").trim();
  const niveau = String(p.niveau || p.level || "3EME").trim().toUpperCase();

  if (!email || !prenom) return { status: "error", message: "email et name requis." };

  // Check désinscription
  const { data: unsub } = await adminClient.from("email_logs")
    .select("id").eq("email", email).eq("type", "UNSUB").limit(1);
  if (unsub && unsub.length > 0) return { status: "success", message: "Utilisateur désinscrit." };

  // Dédup
  const { data: already } = await adminClient.from("email_logs")
    .select("id").eq("email", email).eq("type", "J+" + day).eq("statut", "envoyé").limit(1);
  if (already && already.length > 0) return { status: "success", message: "J+" + day + " déjà envoyé." };

  // Template
  let tpl: { subject: string; html: string };
  if (day === 0) tpl = templateJ0(prenom, email);
  else if (day === 1) tpl = templateJ1(prenom, email);
  else if (day === 3) tpl = templateJ3(prenom, email, objectif);
  else if (day === 7) tpl = templateJ7(prenom, email, objectif, niveau);
  else if (day === 14) tpl = templateJ14(prenom, email, niveau);
  else return { status: "error", message: "Jour invalide : " + day + ". Valeurs acceptées : 0, 1, 3, 7, 14." };

  const result = await resendSend(email, tpl.subject, tpl.html);

  // Log
  await adminClient.from("email_logs").insert({
    email, prenom, type: "J+" + day,
    statut: result.ok ? "envoyé" : "erreur",
    details: result.error || null,
    created_at: new Date().toISOString(),
  });

  if (!result.ok) return { status: "error", message: "Resend: " + result.error };
  return { status: "success" };
}

// ── Action cron_send_emails — à appeler 1×/jour (9h) ────────
// Scanne tous les élèves, calcule J+N depuis inscription, envoie si pas déjà fait

async function cronSendEmails(_p: Record<string, unknown>) {
  const today = todayParis();
  const todayDate = new Date(today + "T00:00:00Z");

  // Tous les profils non-admin, non-test
  const { data: profiles } = await adminClient.from("profiles")
    .select("code, prenom, email, date_inscription, objectif, premium, niveau")
    .eq("is_admin", false)
    .eq("is_test", false);

  if (!profiles || profiles.length === 0) return { status: "success", sent: 0 };

  const SEQUENCE = [1, 3, 7, 14]; // jours après inscription
  let sent = 0;
  const errors: string[] = [];

  for (const p of profiles) {
    if (!p.email || !p.date_inscription) continue;

    const inscDate = new Date(p.date_inscription + "T00:00:00Z");
    const diffDays = Math.floor((todayDate.getTime() - inscDate.getTime()) / (1000 * 60 * 60 * 24));

    for (const day of SEQUENCE) {
      // Catch-up safe : si le cron saute un jour, on rattrape.
      // La dédup est assurée côté sendMarketingEmail via email_logs.
      if (diffDays < day) continue;

      // Skip conversion emails (J+7, J+14) si déjà premium
      if ((day === 7 || day === 14) && p.premium) continue;

      const result = await sendMarketingEmail({
        email: p.email,
        name: p.prenom,
        day,
        objectif: p.objectif || "lacunes",
        niveau: p.niveau,
      });

      if (result && (result as Record<string, unknown>).status === "success") {
        sent++;
      } else {
        errors.push(p.code + "/J+" + day + ": " + JSON.stringify(result));
      }
    }
  }

  return { status: "success", sent, errors: errors.length > 0 ? errors : undefined };
}

// ── Action send_test_email — test admin ─────────────────────

async function sendTestEmailResend(p: Record<string, unknown>) {
  const email = String(p.targetEmail || "").trim();
  const prenom = String(p.targetPrenom || "Nicolas").trim();
  const day = Number(p.day ?? 0);
  const niveau = String(p.niveau || p.level || "3EME").trim().toUpperCase();
  if (!email) return { status: "error", message: "targetEmail requis." };

  // Bypass dédup pour tests : on envoie directement
  let tpl: { subject: string; html: string };
  if (day === 0) tpl = templateJ0(prenom, email);
  else if (day === 1) tpl = templateJ1(prenom, email);
  else if (day === 3) tpl = templateJ3(prenom, email, "lacunes");
  else if (day === 7) tpl = templateJ7(prenom, email, "lacunes", niveau);
  else if (day === 14) tpl = templateJ14(prenom, email, niveau);
  else return { status: "error", message: "Jour invalide : " + day };

  const result = await resendSend(email, tpl.subject, tpl.html);
  if (!result.ok) return { status: "error", message: "Resend: " + result.error };
  return { status: "success", sent_to: email };
}

// ── send_admin_email — envoi custom Resend (audit 2026-04-11, porté de la prod le 25/09) ──
// Mails one-shot personnalisés (premier contact, suivi). Garde : ADMIN_ONLY (jeton de session admin),
// et non plus adminCode (le code admin est public).
async function sendAdminEmail(p: Record<string, unknown>) {
  const to = String(p.to || "").trim().toLowerCase();
  const subject = String(p.subject || "").trim();
  const html = String(p.html || "").trim();
  const replyTo = String(p.replyTo || "contact@matheux.fr").trim();
  if (!to || !subject || !html) return { status: "error", message: "to, subject, html requis." };
  const result = await resendSend(to, subject, html, replyTo);
  // Log dans email_logs (type ADMIN pour distinguer des marketing J+N)
  await adminClient.from("email_logs").insert({
    email: to, prenom: "", type: "ADMIN",
    statut: result.ok ? "envoyé" : "erreur",
    details: result.error || subject,
    created_at: new Date().toISOString(),
  });
  if (!result.ok) return { status: "error", message: "Resend: " + result.error };
  return { status: "success", sent_to: to };
}

// ── NOOP actions (fonctionnalités secondaires, retournent success) ──

async function noopAction(_p: Record<string, unknown>) {
  return { status: "success" };
}

// ── DISPATCH ────────────────────────────────────────────────

// ── Actions réservées à l'admin : jeton de session admin obligatoire (hotfix prod 4fc6123, 25/09) ──
// Garde centrale dans le dispatch (même liste que la prod) : le code admin est public (dépôt GitHub) et
// les actions d'envoi d'email seraient sinon un relais de spam depuis no-reply@matheux.fr.
const ADMIN_ONLY = new Set([
  "get_admin_overview", "publish_admin_boost", "publish_admin_chapter", "get_cours_admin", "save_cours",
  "send_admin_email", "send_test_email", "send_marketing_email", "log_manual_email",
  "send_weekly_report", "send_custom_email", "send_session_rapport",
]);
// cron_send_emails : pg_cron (secret CRON_SECRET, cf. migration 20260925) ou admin. Fail-closed.
const CRON_SECRET = Deno.env.get("CRON_SECRET") || "";
async function cronGarde(p: Record<string, unknown>) {
  const s = String(p.cron_secret || "");
  if (CRON_SECRET && s && _timingSafeEqualHex(s, CRON_SECRET)) return await cronSendEmails(p);
  return (await requireAdmin(p)) || await cronSendEmails(p);
}

const ACTIONS: Record<string, (p: Record<string, unknown>) => Promise<unknown>> = {
  register,
  login,
  login_token: loginToken,
  refresh_session: refreshSession,
  confirm_parent: confirmParent,
  save_score: saveScore,
  save_scores_batch: saveScoresBatch,
  save_boost: saveBoost,
  generate_adaptive_boost: generateAdaptiveBoost,
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
  // stripe_webhook retiré du dispatch (24/09) : accordait le premium sans signature.
  // Seul le chemin signé (checkout.session.completed, plus bas) appelle stripeWebhook.
  unsubscribe: unsubscribeEmail,
  report_exo: reportExo,
  send_contact: sendContact,
  log_manual_email: logManualEmail,
  get_cours_admin: getCoursAdmin,
  save_cours: saveCours,
  get_brevet_chapters: getBrevetChapters,
  generate_brevet_session: generateBrevetSession,
  save_brevet_result: saveBrevetResult,
  // Moteur diagnostic 3e (docs/specs/20-moteur.md)
  start_diagnostic: startDiagnostic,
  answer_diagnostic: answerDiagnostic,
  get_carte: getCarte,
  get_training: getTraining,
  get_acces: getAcces,
  set_preferences: setPreferences,
  log_consent: logConsent,
  log_funnel_event: logFunnelEvent,
  create_share: createShare,
  revoke_share: revokeShare,
  get_bilan_partage: getBilanPartage,
  // Noop — fonctionnalités secondaires qui ne cassent pas le parcours
  add_teasing_early: noopAction,
  detect_fragile_prereqs: noopAction,
  enqueue: noopAction,
  generate_daily_boost: noopAction,
  generate_revision: noopAction,
  log_event: noopAction,
  mark_all_test: noopAction,
  simulate_next_day: noopAction,
  send_test_email: sendTestEmailResend,
  send_admin_email: sendAdminEmail,
  send_marketing_email: sendMarketingEmail,
  cron_send_emails: cronGarde,
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
    const raw = await req.text();
    const p = JSON.parse(raw);

    // ── Stripe native webhook (checkout.session.completed) ──
    // FAIL-CLOSED : on exige Stripe-Signature valide.
    // Si STRIPE_WEBHOOK_SECRET manquant → on rejette (évite exploit "n'importe qui grante premium").
    if (p.type === "checkout.session.completed" && p.data?.object) {
      const sigHeader = req.headers.get("stripe-signature") || req.headers.get("Stripe-Signature") || "";
      if (!STRIPE_WEBHOOK_SECRET) {
        console.error("[stripe] STRIPE_WEBHOOK_SECRET non configuré — webhook rejeté");
        return json({ status: "error", message: "Stripe webhook: secret not configured" }, 500);
      }
      const valid = await verifyStripeSignature(raw, sigHeader, STRIPE_WEBHOOK_SECRET);
      if (!valid) {
        console.error("[stripe] Signature invalide — webhook rejeté");
        return json({ status: "error", message: "Stripe webhook: invalid signature" }, 400);
      }
      const session = p.data.object;
      const email = String(session.customer_details?.email || session.customer_email || "").trim().toLowerCase();
      if (!email) return json({ status: "error", message: "Stripe webhook: no email found" });
      // niveau du Payment Link acheté : metadata.niveau uniquement. client_reference_id porte
      // désormais le code élève (refonte diagnostic 3e) : il ne doit plus finir dans premium_niveau.
      const niveau = String(session.metadata?.niveau || "");
      const result = await stripeWebhook({
        email, niveau,
        produit: String(session.metadata?.produit || ""), // refonte diagnostic 3e (vide = lien legacy)
        offre_version: String(session.metadata?.offre_version || ""),
        code: String(session.client_reference_id || ""), // code élève
        session_id: session.id, montant_cents: session.amount_total,
      });
      return json(result);
    }

    const action = String(p.action || "");
    const handler = ACTIONS[action];
    if (!handler) return json({ status: "error", message: "Action inconnue : " + action });
    if (ADMIN_ONLY.has(action)) {
      const denied = await requireAdmin(p);
      if (denied) return json(denied);
    }

    const result = await handler(p);
    return json(result);
  } catch (err) {
    return json({ status: "error", message: "Erreur serveur : " + String(err) }, 500);
  }
});
