// ════════════════════════════════════════════════════════════
//  MATHEUX — BACKEND GOOGLE APPS SCRIPT
//  Version collège : 6EME / 5EME / 4EME / 3EME uniquement
//  BUILD: 2026-03-10
//
//  Actions gérées :
//    register · login · save_score · save_boost
//    generate_diagnostic · generate_daily_boost · generate_remediation
//    get_progress · get_prerequisites · detect_fragile_prereqs
//    enqueue · process_queue · generate_exam_prep · debug_progress
//    get_admin_overview · publish_admin_boost · publish_admin_chapter
//
//  Onglets Google Sheet requis :
//    Users · Scores · Curriculum_Officiel · DailyBoosts
//    DiagnosticExos · RemediationChapters · Progress
//    👁 Suivi · 📋 Historique
//
//  Déploiement :
//    clasp push → Apps Script → Déployer → Nouvelle version
//    Accès : Tout le monde (anonyme)
// ════════════════════════════════════════════════════════════

// ── Niveaux autorisés ────────────────────────────────────────
var ALLOWED_LEVELS = ['6EME', '5EME', '4EME', '3EME'];

// ── Noms exacts des onglets ──────────────────────────────────
var SH = {
  USERS:       'Users',
  SCORES:      'Scores',
  CURRICULUM:  'Curriculum_Officiel',
  BOOSTS:      'DailyBoosts',
  DIAG:        'DiagnosticExos',
  REMEDIATION: 'RemediationChapters',
  PROGRESS:    'Progress',
  PREREQS:     'Prerequisites',
  QUEUE:       'Queue',
  RAPPORTS:    'Rapports',
  PENDING:     'Pending_Exos',
  SUIVI:       '👁 Suivi',
  HISTORIQUE:  '📋 Historique'
};

// ════════════════════════════════════════════════════════════
//  POINT D'ENTRÉE
// ════════════════════════════════════════════════════════════

function doGet() {
  return json({ status: 'ok', version: 'matheux_backend_v1' });
}

function doPost(e) {
  try {
    var p = JSON.parse(e.postData.contents);
    var res;

    // Rate limiting : max 15 req/min par email sur les actions sensibles
    if (p.action === 'register' || p.action === 'login') {
      var rlKey   = 'rl_' + (p.email || '').toLowerCase().replace(/[^a-z0-9@._-]/g, '');
      var cache   = CacheService.getScriptCache();
      var count   = parseInt(cache.get(rlKey) || '0');
      if (count >= 15) {
        return json({ status: 'error', message: 'Trop de tentatives. Réessaie dans 1 minute.' });
      }
      cache.put(rlKey, String(count + 1), 60);
    }

    switch (p.action) {
      case 'register':             res = register(p);            break;
      case 'login':                res = login(p);               break;
      case 'save_score':           res = saveScore(p);           break;
      case 'save_boost':           res = saveBoost(p);           break;
      case 'generate_diagnostic':  res = generateDiagnostic(p);  break;
      case 'generate_daily_boost': res = generateDailyBoost(p);  break;
      case 'generate_remediation':       res = generateRemediation(p);      break;
      case 'get_progress':               res = getProgress(p);              break;
      case 'get_prerequisites':          res = getPrerequisites();          break;
      case 'detect_fragile_prereqs':     res = detectFragilePrerequisites(p); break;
      case 'enqueue':                    res = enqueueTask(p);              break;
      case 'process_queue':              res = processQueue();              break;
      case 'generate_exam_prep':         res = generateExamPrep(p);        break;
      case 'debug_progress':             res = debugProgress(p);           break;
      case 'get_admin_overview':         res = getAdminOverview(p);        break;
      case 'publish_admin_boost':        res = publishAdminBoost(p);       break;
      case 'publish_admin_chapter':      res = publishAdminChapter(p);     break;
      case 'check_trial_status':         res = checkTrialStatus(p);        break;
      default:
        res = { status: 'error', message: 'Action inconnue : ' + p.action };
    }
  } catch (err) {
    res = { status: 'error', message: 'Erreur serveur : ' + err.toString() };
  }
  return json(res);
}

// ════════════════════════════════════════════════════════════
//  HELPERS GÉNÉRAUX
// ════════════════════════════════════════════════════════════

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// Retourne l'onglet (lance une erreur propre si absent)
function getSheet(name) {
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name);
  if (!sh) throw new Error('Onglet introuvable : ' + name);
  return sh;
}

// Retourne toutes les lignes d'un onglet comme tableau d'objets { header: valeur }
function getRows(name) {
  var sh   = getSheet(name);
  var data = sh.getDataRange().getValues();
  if (data.length <= 1) return [];
  var headers = data[0];
  return data.slice(1).map(function(row) {
    var obj = {};
    headers.forEach(function(h, i) { obj[h] = row[i]; });
    return obj;
  });
}

// Vérifie si un onglet existe sans lever d'erreur
function sheetExists(name) {
  return SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name) !== null;
}

function appendRow(name, values) {
  getSheet(name).appendRow(values);
}

// Met à jour une cellule précise (ligne 1-indexée, colonne 1-indexée)
function updateCell(name, row, col, value) {
  getSheet(name).getRange(row, col).setValue(value);
}

function today() {
  return Utilities.formatDate(new Date(), 'Europe/Paris', 'yyyy-MM-dd');
}

function formatDateFR(dateStr) {
  if (!dateStr) return '';
  try {
    var d = new Date(dateStr);
    if (isNaN(d.getTime())) return String(dateStr);
    return Utilities.formatDate(d, 'Europe/Paris', 'dd/MM/yyyy HH:mm');
  } catch (e) { return String(dateStr); }
}

function isValidLevel(level) {
  return ALLOWED_LEVELS.indexOf((level || '').toUpperCase()) !== -1;
}

function parseJSON(str) {
  try { return JSON.parse(str || '[]'); } catch (e) { return []; }
}

function shuffle(arr) {
  var a = arr.slice();
  for (var i = a.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = a[i]; a[i] = a[j]; a[j] = tmp;
  }
  return a;
}

// Génère un code élève unique (6 caractères sans ambigüité visuelle)
function generateCode() {
  var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  var code  = '';
  for (var i = 0; i < 6; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return code;
}

function uniqueCode() {
  var existing = getRows(SH.USERS).map(function(r) { return String(r['Code']); });
  var code;
  do { code = generateCode(); } while (existing.indexOf(code) !== -1);
  return code;
}

// ════════════════════════════════════════════════════════════
//  1. REGISTER
//  Payload : { name, email, level, password (hash SHA-256) }
//  Réponse : { status, profile }
// ════════════════════════════════════════════════════════════

function register(p) {
  ensureUsersCols();
  var name  = (p.name  || '').trim();
  var email = (p.email || '').trim().toLowerCase();
  var level = (p.level || '').toUpperCase();
  var hash  = (p.password || '').trim();

  // Validation
  if (!name)  return { status: 'error', message: 'Le prénom est requis.' };
  if (!email) return { status: 'error', message: 'L\'email est requis.' };
  if (!hash)  return { status: 'error', message: 'Le mot de passe est requis.' };
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    return { status: 'error', message: 'Format d\'email invalide.' };
  }
  if (name.length > 50) {
    return { status: 'error', message: 'Le prénom ne doit pas dépasser 50 caractères.' };
  }
  if (hash.length !== 64) {
    return { status: 'error', message: 'Mot de passe invalide (hash attendu).' };
  }
  if (!isValidLevel(level)) {
    return { status: 'error', message: 'Niveau invalide. Valeurs acceptées : ' + ALLOWED_LEVELS.join(', ') };
  }

  // Email déjà enregistré ?
  var users = getRows(SH.USERS);
  var taken = users.some(function(u) {
    return u['Email'] && u['Email'].toString().toLowerCase() === email;
  });
  if (taken) {
    return { status: 'error', message: 'Un compte existe déjà avec cet email.' };
  }

  var code = uniqueCode();
  var now  = today();

  // Users : Code | Prénom | Niveau | Email | PasswordHash | DateInscription | IsAdmin | Premium | TrialStart
  appendRow(SH.USERS, [code, name, level, email, hash, now, 0, 0, now]);

  return {
    status:  'success',
    profile: { code: code, name: name, level: level, isAdmin: false, premium: false }
  };
}

// ════════════════════════════════════════════════════════════
//  2. LOGIN
//  Payload : { email, password (hash) }
//  Réponse : { status, profile, curriculumOfficiel, diagExos,
//              dailyBoost, boostExistsInDB, history,
//              dynamicChapters }
// ════════════════════════════════════════════════════════════

function login(p) {
  var email = (p.email || '').trim().toLowerCase();
  var hash  = (p.password || '').trim();

  if (!email || !hash) {
    return { status: 'error', message: 'Email et mot de passe requis.' };
  }

  // Authentification
  var users = getRows(SH.USERS);
  var user  = null;
  for (var i = 0; i < users.length; i++) {
    var u = users[i];
    if (u['Email'] && u['Email'].toString().toLowerCase() === email &&
        u['PasswordHash'] && u['PasswordHash'].toString() === hash) {
      user = u;
      break;
    }
  }
  if (!user) {
    return { status: 'error', message: 'Email ou mot de passe incorrect.' };
  }

  var code       = String(user['Code']);
  var level      = String(user['Niveau']).toUpperCase();
  var name       = String(user['Prénom']);
  var isAdmin    = parseInt(user['IsAdmin']  || 0) === 1;
  var premium    = parseInt(user['Premium']  || 0) === 1;
  var trialStart = user['TrialStart'] ? String(user['TrialStart']) : '';

  // ── Curriculum officiel (chapitres du niveau) ─────────────
  var curriculumOfficiel = [];
  getRows(SH.CURRICULUM)
    .filter(function(r) {
      return r['Niveau'] && r['Niveau'].toString().toUpperCase() === level;
    })
    .forEach(function(r) {
      curriculumOfficiel.push({
        categorie: String(r['Categorie']),
        titre:     String(r['Titre']),
        icone:     String(r['Icone']),
        exos:      parseJSON(r['ExosJSON'])
      });
    });

  // ── diagExos : généré à la demande via generate_diagnostic ──
  //  (le login ne pré-charge plus rien — la colonne Categorie est
  //   maintenant la clé de filtrage dans DiagnosticExos)
  var diagExos = [];

  // ── Boost du jour ─────────────────────────────────────────
  var todayStr    = today();
  var boostRows   = getRows(SH.BOOSTS);
  var todayBoost  = null;
  var boostExosDone = 0;
  for (var b = 0; b < boostRows.length; b++) {
    var br = boostRows[b];
    if (!br['Code'] || String(br['Code']) !== code) continue;
    // La colonne Date peut être un objet Date (Sheets auto-converti) ou une string
    var brDate = br['Date'];
    var brDateStr = (brDate instanceof Date)
      ? Utilities.formatDate(brDate, 'Europe/Paris', 'yyyy-MM-dd')
      : String(brDate || '').substring(0, 10);
    if (brDateStr === todayStr) {
      todayBoost = parseJSON(br['BoostJSON']);
      boostExosDone = parseInt(br['ExosDone'] || 0);
      break;
    }
  }
  var boostExistsInDB = todayBoost !== null;

  // ── Historique des scores ─────────────────────────────────
  var history = getRows(SH.SCORES)
    .filter(function(r) { return r['Code'] && String(r['Code']) === code; })
    .map(function(r) {
      var res = String(r['Résultat'] || '');
      return {
        niveau:       String(r['Niveau']   || ''),
        categorie:    String(r['Chapitre'] || ''),
        exercice_idx: r['NumExo'],
        resultat:     res,
        xp:           res === 'EASY' ? 100 : res === 'MEDIUM' ? 50 : 10,
        date:         String(r['Date']     || '')
      };
    });

  // ── Injection des colonnes Nicolas depuis 👁 Suivi ────────
  // Structure avec ACTION en col A (21 cols) :
  // Col U = index 20 (Code masquée)
  // →Nouveau ChN : G=6, J=9, M=12, P=15 (0-based)
  // →Nouveau Boost : S=18 (0-based)
  var nextChapter = null;
  var nextBoost   = null;
  if (sheetExists(SH.SUIVI)) {
    var suiviSh   = getSheet(SH.SUIVI);
    var suiviData = suiviSh.getDataRange().getValues();
    for (var si = 1; si < suiviData.length; si++) {
      if (String(suiviData[si][20]) === code) {
        // Colonnes →Nouveau ChN (0-based: 6,9,12,15 → 1-based: 7,10,13,16)
        var chapIndices = [6, 9, 12, 15];
        for (var sk = 0; sk < chapIndices.length; sk++) {
          var val = String(suiviData[si][chapIndices[sk]] || '').trim();
          if (!val) continue;
          try {
            var parsed = JSON.parse(val);
            if (parsed && parsed.categorie && parsed.exos && parsed.exos.length > 0) {
              nextChapter = parsed;
              suiviSh.getRange(si + 1, chapIndices[sk] + 1).setValue('');
            } else if (parsed && parsed.categorie) {
              // JSON valide mais exos vide → PENDING_MANUAL, vider la cellule
              nextChapter = { categorie: 'PENDING_MANUAL', exos: [],
                insight: 'Ton prof prépare ton prochain chapitre personnalisé… reviens dans quelques heures !' };
              suiviSh.getRange(si + 1, chapIndices[sk] + 1).setValue('');
            } else {
              // JSON sans categorie valide → laisser la cellule intacte
              Logger.log('login injection KO (pas de categorie) pour ' + code + ' : ' + val.substring(0, 100));
            }
          } catch (e) {
            // JSON malformé → PENDING_MANUAL, laisser la cellule intacte pour re-essai
            Logger.log('login injection KO (JSON malformé) pour ' + code + ' : ' + val.substring(0, 100));
            nextChapter = { categorie: 'PENDING_MANUAL', exos: [],
              insight: 'Ton prof prépare ton prochain chapitre personnalisé… reviens dans quelques heures !' };
          }
          break;
        }
        // Colonne →Nouveau Boost (0-based: 18 → 1-based: 19)
        var boostVal = String(suiviData[si][18] || '').trim();
        if (boostVal) {
          try {
            var boostParsed = JSON.parse(boostVal);
            if (boostParsed && boostParsed.exos && boostParsed.exos.length > 0) {
              nextBoost = boostParsed;
              suiviSh.getRange(si + 1, 19).setValue('');
            } else {
              Logger.log('login boost injection KO pour ' + code);
            }
          } catch (e) {
            Logger.log('login boost injection JSON KO pour ' + code);
          }
        }
        break;
      }
    }
  }
  // Rebuildsuivi si injection faite (met à jour les couleurs)
  if (nextChapter || nextBoost) {
    try { rebuildSuivi(code); } catch (e) {}
  }

  return {
    status:             'success',
    profile:            { code: code, name: name, level: level, isAdmin: isAdmin, premium: premium, trialStart: trialStart },
    curriculumOfficiel: curriculumOfficiel,
    diagExos:           diagExos,
    dailyBoost:         todayBoost,
    boostExistsInDB:    boostExistsInDB,
    boostExosDone:      boostExosDone,
    isFirstDay:         history.length === 0 && !boostExistsInDB,
    history:            history,
    dynamicChapters:    [],
    nextChapter:        nextChapter,
    nextBoost:          nextBoost,
    trial:              checkTrialStatus({ code: code })
  };
}

// ════════════════════════════════════════════════════════════
//  3. SAVE_SCORE
//  Payload : { code, name, level, categorie, exercice_idx,
//              resultat, q, time, indices, formule, wrongOpt, draft }
//  Réponse : { status }
// ════════════════════════════════════════════════════════════

function saveScore(p) {
  var required = ['code', 'name', 'level', 'categorie', 'exercice_idx', 'resultat'];
  for (var i = 0; i < required.length; i++) {
    if (!p[required[i]] && p[required[i]] !== 0) {
      return { status: 'error', message: 'Champ manquant : ' + required[i] };
    }
  }

  // Scores : Code | Prénom | Niveau | Chapitre | NumExo | Énoncé |
  //          Résultat | Temps(sec) | NbIndices | FormuleVue | MauvaiseOption | Draft | Date
  appendRow(SH.SCORES, [
    String(p.code),
    String(p.name),
    String(p.level),
    String(p.categorie),
    p.exercice_idx,
    String(p.q        || ''),
    String(p.resultat),
    parseInt(p.time   || 0),
    parseInt(p.indices || 0),
    p.formule ? 1 : 0,
    String(p.wrongOpt || ''),
    String(p.draft    || ''),
    today()
  ]);

  // Mise à jour score de confiance + streak (best-effort, ne bloque pas la réponse)
  // Exclure BOOST et CALIBRAGE : leurs exos sont remappés vers la catégorie d'origine
  // côté client, ce qui fausserait le compteur nbExos du chapitre dans Progress.
  var streakAlert = false;
  var source = String(p.source || p.categorie || '');
  if (source !== 'BOOST' && source !== 'CALIBRAGE') {
    try {
      var updateResult = updateConfidenceScore(
        String(p.code),
        String(p.level),
        String(p.categorie),
        String(p.resultat),
        parseInt(p.indices || 0),
        parseInt(p.exercice_idx || 0)
      );
      streakAlert = updateResult.streakAlert || false;
    } catch (e) {
      // Silencieux — le score de confiance est non-bloquant
    }
  }

  try { rebuildSuivi(String(p.code)); } catch (e) {}
  try { writeToHistorique(p); } catch (e) {}

  return { status: 'success', streakAlert: streakAlert };
}

// ════════════════════════════════════════════════════════════
//  4. SAVE_BOOST
//  Payload : { code, boost }
//  Réponse : { status }
// ════════════════════════════════════════════════════════════

function saveBoost(p) {
  if (!p.code || !p.boost) {
    return { status: 'error', message: 'code et boost requis.' };
  }

  var code     = String(p.code);
  var todayStr = today();
  var sh       = getSheet(SH.BOOSTS);
  var data     = sh.getDataRange().getValues();

  // Auto-ajout header ExosDone en col D si absent
  if (data.length > 0 && data[0].length < 4) {
    sh.getRange(1, 4).setValue('ExosDone');
    data = sh.getDataRange().getValues();
  }

  // ExosDone = exoIdx + 1 (exoIdx est 0-based, envoyé par le frontend)
  var exosDone = (p.exoIdx !== undefined && p.exoIdx !== null)
    ? (parseInt(p.exoIdx) + 1)
    : 1;

  // Mise à jour si une ligne existe déjà pour (code, date)
  for (var i = 1; i < data.length; i++) {
    var sbDate = data[i][1];
    var sbDateStr = (sbDate instanceof Date)
      ? Utilities.formatDate(sbDate, 'Europe/Paris', 'yyyy-MM-dd')
      : String(sbDate || '').substring(0, 10);
    if (String(data[i][0]) === code && sbDateStr === todayStr) {
      sh.getRange(i + 1, 3).setValue(JSON.stringify(p.boost));
      sh.getRange(i + 1, 4).setValue(exosDone);  // col D ExosDone
      return { status: 'success' };
    }
  }

  // DailyBoosts : Code | Date | BoostJSON | ExosDone
  appendRow(SH.BOOSTS, [code, todayStr, JSON.stringify(p.boost), exosDone]);
  try { rebuildSuivi(code); } catch (e) {}
  return { status: 'success' };
}

// ════════════════════════════════════════════════════════════
//  5. GENERATE_DIAGNOSTIC
//  Payload : { code, level, selectedChapters[] }
//  Réponse : { status, exos[] }
//
//  Structure DiagnosticExos : Niveau | Categorie | ExosJSON
//  Une ligne par (niveau, chapitre). La colonne Categorie doit
//  correspondre EXACTEMENT aux valeurs data-chap générées par
//  le frontend (voir CHAPS_BY_LEVEL dans index.html).
//
//  Clés attendues par niveau :
//  6EME : Nombres_entiers, Fractions, Proportionnalité,
//          Géométrie, PérimètresAires, Angles
//  5EME : Fractions, Nombres_relatifs, Proportionnalité,
//          Puissances, Pythagore, Calcul_Littéral
//  4EME : Fractions, Puissances, Calcul_Littéral,
//          Équations, Pythagore, Proportionnalité
//  3EME : Calcul_Littéral, Équations, Fonctions,
//          Théorème_de_Thalès, Trigonométrie, Statistiques
//
//  ExosJSON par ligne :
//  [ { "q":"...", "a":"...", "options":[...],
//      "steps":[...], "f":"...", "lvl":1 }, ... ]
// ════════════════════════════════════════════════════════════

function generateDiagnostic(p) {
  var level    = (p.level || '').toUpperCase();
  var selected = p.selectedChapters || [];

  if (!isValidLevel(level)) {
    return { status: 'error', message: 'Niveau invalide : ' + level };
  }

  // Toutes les lignes DiagnosticExos du niveau
  var diagRows = getRows(SH.DIAG).filter(function(r) {
    return r['Niveau'] && r['Niveau'].toString().toUpperCase() === level;
  });

  if (diagRows.length === 0) {
    return { status: 'error', message: 'Aucun exo de diagnostic pour le niveau ' + level + '. Remplis l\'onglet DiagnosticExos (une ligne par chapitre).' };
  }

  // Filtre par chapitres sélectionnés (colonne Categorie)
  var filtered = diagRows;
  if (selected.length > 0) {
    var byChap = diagRows.filter(function(r) {
      return selected.indexOf(String(r['Categorie'] || '')) !== -1;
    });
    // Fallback : si aucun chapitre ne matche, on prend tout le niveau
    if (byChap.length > 0) filtered = byChap;
  }

  // Garantit 1 exo lvl1 + 1 exo lvl2 par chapitre sélectionné
  var exos = [];
  filtered.forEach(function(r) {
    var chapExos = parseJSON(r['ExosJSON']);
    var l1 = shuffle(chapExos.filter(function(e){ return (e.lvl || 1) === 1; }));
    var l2 = shuffle(chapExos.filter(function(e){ return (e.lvl || 1) === 2; }));
    if (l1.length > 0) exos.push(l1[0]);
    if (l2.length > 0) {
      exos.push(l2[0]);
    } else if (l1.length > 1) {
      // Fallback : pas de champ lvl → on prend un 2e exo lvl1 comme substitute
      exos.push(l1[1]);
    }
    // Fallback total : aucun exo dans aucun bucket
    if (l1.length === 0 && l2.length === 0) {
      chapExos.slice(0, 2).forEach(function(e){ exos.push(e); });
    }
  });

  if (exos.length === 0) {
    return { status: 'error', message: 'DiagnosticExos vide pour le niveau ' + level + '.' };
  }

  return { status: 'success', exos: shuffle(exos) };
}

// ════════════════════════════════════════════════════════════
//  6. GENERATE_DAILY_BOOST
//  Payload : { code, level, errors[] (optionnel, depuis diagnostic) }
//  Réponse : { status, boost: { insight, exos[] } }
//
//  Logique :
//  - Si appelé après le diagnostic (errors fournis) → tirage
//    dans tout le curriculum (les scores CALIBRAGE ne sont pas
//    encore catégorisés par chapitre)
//  - Si appelé manuellement → cible les chapitres avec HARD
//    du jour, complète si besoin
// ════════════════════════════════════════════════════════════

// ── Retourne les IDs (chapitre_numExo) déjà vus par un élève ─
//  Utilisé pour l'anti-redondance dans boost et remédiation.
function getSeenExoKeys(code) {
  var seen = {};
  getRows(SH.SCORES).filter(function(r) {
    return r['Code'] && String(r['Code']) === code;
  }).forEach(function(r) {
    var cat = String(r['Chapitre'] || '');
    var num = String(r['NumExo']   || '');
    if (cat && num) seen[cat + '_' + num] = true;
  });
  return seen;
}

// ── Retourne les chapitres du niveau triés par score Progress ─
//  Score absent = 0. Permet de prioriser les chapitres faibles.
function getChaptersByWeakness(code, level) {
  if (!sheetExists(SH.PROGRESS)) return null;
  var progressRows = getRows(SH.PROGRESS).filter(function(r) {
    return r['Code']  && String(r['Code'])  === code &&
           r['Niveau'] && String(r['Niveau']).toUpperCase() === level;
  });
  // Map chapitre → score
  var scoreMap = {};
  progressRows.forEach(function(r) {
    scoreMap[String(r['Chapitre'])] = parseFloat(r['Score'] || 0);
  });
  return scoreMap;
}

// ── Filtre un pool d'exos en excluant ceux déjà vus ──────────
function filterSeen(pool, cat, seenKeys) {
  return pool.filter(function(ex, idx) {
    // Les exos du curriculum sont indexés 1-based par position dans l'array de la catégorie
    var key = cat + '_' + (idx + 1);
    return !seenKeys[key];
  });
}

function generateDailyBoost(p) {
  var code     = String(p.code  || '');
  var level    = (p.level || '').toUpperCase();
  var fromDiag = Array.isArray(p.errors) && p.errors.length > 0;

  if (!code || !isValidLevel(level)) {
    return { status: 'error', message: 'code et level (6EME/5EME/4EME/3EME) requis.' };
  }

  // Récupère tout le curriculum du niveau
  var curriculum = getRows(SH.CURRICULUM).filter(function(r) {
    return r['Niveau'] && r['Niveau'].toString().toUpperCase() === level;
  });

  if (curriculum.length === 0) {
    return { status: 'error', message: 'Curriculum_Officiel vide pour le niveau ' + level + '.' };
  }

  // ── P5 : Filtrer strictement sur les chapitres diagnostiqués de l'élève ──
  var diagnosedChaps = [];
  getRows(SH.SCORES).filter(function(r) {
    return r['Code'] && String(r['Code']) === code;
  }).forEach(function(r) {
    var cat = String(r['Chapitre'] || '');
    if (cat && cat !== 'CALIBRAGE' && diagnosedChaps.indexOf(cat) === -1) {
      diagnosedChaps.push(cat);
    }
  });
  if (diagnosedChaps.length > 0) {
    var filtered = curriculum.filter(function(r) {
      return diagnosedChaps.indexOf(String(r['Categorie'])) !== -1;
    });
    // Fallback : si aucun chapitre diagostiqué n'existe dans le curriculum, utiliser tout le curriculum
    if (filtered.length > 0) curriculum = filtered;
  }

  // ── P3 : Anti-redondance — exos déjà vus par l'élève ────────
  var seenKeys = getSeenExoKeys(code);

  // ── P3 : Scores par chapitre pour priorisation ───────────────
  var weaknessMap = getChaptersByWeakness(code, level) || {};

  var pool    = [];
  var insight = '';

  if (fromDiag) {
    // ── Boost post-diagnostic : tirage varié priorité chapitres faibles
    // Trier le curriculum par score croissant (chapitres faibles d'abord)
    var sortedCurriculum = curriculum.slice().sort(function(a, b) {
      var sA = weaknessMap[String(a['Categorie'])] || 0;
      var sB = weaknessMap[String(b['Categorie'])] || 0;
      return sA - sB;
    });
    sortedCurriculum.forEach(function(r) {
      var cat   = String(r['Categorie']);
      var exos  = parseJSON(r['ExosJSON']);
      var fresh = filterSeen(exos, cat, seenKeys);
      // Si tous vus, prendre quand même (fallback)
      var source = fresh.length >= 2 ? fresh : exos;
      source.forEach(function(ex) {
        pool.push(Object.assign({}, ex, { _cat: cat }));
      });
    });
    insight = 'Programme personnalisé basé sur ton diagnostic. Ces 5 exercices couvrent tes points clés du niveau ' + level.replace('EME', 'ème') + '.';

  } else {
    // ── Boost quotidien : cible les chapitres avec erreurs du jour
    var todayStr  = today();
    var todayHard = getRows(SH.SCORES).filter(function(r) {
      return r['Code']     && String(r['Code'])     === code     &&
             r['Date']     && String(r['Date'])     === todayStr &&
             r['Résultat'] && String(r['Résultat']) === 'HARD';
    });

    // Compte les erreurs par chapitre, tri décroissant
    var errBycat = {};
    todayHard.forEach(function(r) {
      var cat = String(r['Chapitre'] || '');
      if (cat && cat !== 'CALIBRAGE') errBycat[cat] = (errBycat[cat] || 0) + 1;
    });
    var targetCats = Object.keys(errBycat).sort(function(a, b) {
      return errBycat[b] - errBycat[a];
    });

    // ── P3 : Si pas d'erreurs du jour, utiliser chapitres faibles (score < 50%)
    if (targetCats.length === 0) {
      var weakCats = Object.keys(weaknessMap)
        .filter(function(c) { return weaknessMap[c] < 50; })
        .sort(function(a, b) { return weaknessMap[a] - weaknessMap[b]; });
      if (weakCats.length > 0) targetCats = weakCats.slice(0, 3);
    }

    if (targetCats.length > 0) {
      // Pioche en priorité dans les chapitres ciblés, exercices non vus
      targetCats.slice(0, 3).forEach(function(cat) {
        var row = curriculum.filter(function(r) { return String(r['Categorie']) === cat; })[0];
        if (!row) return;
        var exos  = parseJSON(row['ExosJSON']);
        var fresh = filterSeen(exos, cat, seenKeys);
        // Fallback chapitre connexe via Prerequisites si tous vus
        if (fresh.length === 0 && sheetExists(SH.PREREQS)) {
          var prereqRows = getRows(SH.PREREQS).filter(function(r) {
            return r['Niveau']   && String(r['Niveau']).toUpperCase() === level &&
                   r['Chapitre'] && String(r['Chapitre']) === cat;
          });
          for (var pi = 0; pi < prereqRows.length; pi++) {
            var relCat = String(prereqRows[pi]['PrerequisChapitre'] || '');
            var relRow = curriculum.filter(function(r) { return String(r['Categorie']) === relCat; })[0];
            if (relRow) {
              var relExos  = parseJSON(relRow['ExosJSON']);
              var relFresh = filterSeen(relExos, relCat, seenKeys);
              if (relFresh.length > 0) {
                relFresh.forEach(function(ex) { pool.push(Object.assign({}, ex, { _cat: relCat })); });
                break;
              }
            }
          }
        } else {
          var source = fresh.length >= 2 ? fresh : exos;
          source.forEach(function(ex) { pool.push(Object.assign({}, ex, { _cat: cat })); });
        }
      });

      // Complète si pool trop petit
      if (pool.length < 10) {
        curriculum.forEach(function(r) {
          var cat = String(r['Categorie']);
          if (targetCats.indexOf(cat) !== -1) return; // déjà traité
          var exos  = parseJSON(r['ExosJSON']);
          var fresh = filterSeen(exos, cat, seenKeys);
          var source = fresh.length >= 2 ? fresh : exos;
          source.forEach(function(ex) { pool.push(Object.assign({}, ex, { _cat: cat })); });
        });
      }

      // Génère l'insight
      var catLabels = targetCats.slice(0, 2).map(function(c) {
        return c.toLowerCase().replace(/_/g, ' ');
      });
      var isWeaknessBoost = errBycat[targetCats[0]] === undefined;
      if (isWeaknessBoost) {
        insight = catLabels.length === 1
          ? 'Ton point faible "' + catLabels[0] + '" mérite encore du travail. Ces 5 exercices ciblés vont renforcer ça.'
          : 'Tes points faibles "' + catLabels.join('" et "') + '" ont besoin d\'être consolidés. On s\'y attaque.';
      } else {
        insight = catLabels.length === 1
          ? 'Tu as buté sur "' + catLabels[0] + '" aujourd\'hui. Ces 5 exercices te permettront de consolider ce point.'
          : 'Aujourd\'hui tu as eu du mal sur "' + catLabels.join('" et "') + '". On repart là-dessus.';
      }

    } else {
      // Aucune erreur, aucun point faible → tirage varié, priorité exos non vus
      curriculum.forEach(function(r) {
        var cat   = String(r['Categorie']);
        var exos  = parseJSON(r['ExosJSON']);
        var fresh = filterSeen(exos, cat, seenKeys);
        var source = fresh.length >= 1 ? fresh : exos;
        source.forEach(function(ex) { pool.push(Object.assign({}, ex, { _cat: cat })); });
      });
      insight = 'Super journée ! Voici un entraînement varié avec des exercices que tu n\'as pas encore faits.';
    }
  }

  if (pool.length === 0) {
    return { status: 'error', message: 'Aucun exercice disponible dans Curriculum_Officiel.' };
  }

  var selected = shuffle(pool).slice(0, 5);
  var boost    = { insight: insight, exos: selected };

  // Sauvegarde (ou mise à jour) dans DailyBoosts
  var todayStr2 = today();
  var sh        = getSheet(SH.BOOSTS);
  var data      = sh.getDataRange().getValues();
  var saved     = false;
  for (var i = 1; i < data.length; i++) {
    var rowDate = data[i][1];
    var rowDateStr = (rowDate instanceof Date)
      ? Utilities.formatDate(rowDate, 'Europe/Paris', 'yyyy-MM-dd')
      : String(rowDate || '').substring(0, 10);
    if (String(data[i][0]) === code && rowDateStr === todayStr2) {
      sh.getRange(i + 1, 3).setValue(JSON.stringify(boost));
      saved = true;
      break;
    }
  }
  if (!saved) appendRow(SH.BOOSTS, [code, todayStr2, JSON.stringify(boost)]);

  return { status: 'success', boost: boost };
}

// ════════════════════════════════════════════════════════════
//  7. GENERATE_REMEDIATION
//  Payload : { code, category, level, errors[] }
//  Réponse : { status }
//
//  Crée un chapitre de remédiation ciblé sur les erreurs.
//  Sauvegarde dans RemediationChapters (visible au prochain login
//  via dynamicChapters).
//  Maximum V3 (3 remédiation par chapitre).
// ════════════════════════════════════════════════════════════

function generateRemediation(p) {
  // Désactivé — contenu prêt demain (rebranchera quand vrais élèves)
  return { status: 'success' };
  /* ── DÉSACTIVÉ ──
  var code     = String(p.code     || '');
  var category = String(p.category || '');
  var level    = (p.level || '').toUpperCase();
  var errors   = p.errors || [];

  if (!code || !category || !isValidLevel(level)) {
    return { status: 'error', message: 'code, category et level requis.' };
  }

  if (!sheetExists(SH.REMEDIATION)) {
    return { status: 'error', message: 'L\'onglet RemediationChapters n\'existe pas. Crée-le dans le Google Sheet.' };
  }

  // Récupère les exos du chapitre dans le curriculum
  var chapRows = getRows(SH.CURRICULUM).filter(function(r) {
    return r['Niveau']    && r['Niveau'].toString().toUpperCase() === level &&
           r['Categorie'] && r['Categorie'].toString() === category;
  });

  if (chapRows.length === 0) {
    return { status: 'error', message: 'Chapitre "' + category + '" introuvable dans Curriculum_Officiel pour le niveau ' + level + '.' };
  }

  var chapRow = chapRows[0];
  var allExos = parseJSON(chapRow['ExosJSON']);
  var titre   = String(chapRow['Titre'] || category);

  if (allExos.length === 0) {
    return { status: 'error', message: 'Aucun exercice dans le chapitre "' + category + '".' };
  }

  // ── P3 : Anti-redondance — exos déjà vus (EASY ou HARD) sur ce chapitre
  var allSeenIdxs = getRows(SH.SCORES)
    .filter(function(r) {
      return r['Code']     && String(r['Code'])     === code     &&
             r['Chapitre'] && String(r['Chapitre']) === category;
    })
    .map(function(r) { return parseInt(r['NumExo']); });

  var easyIdxs = getRows(SH.SCORES)
    .filter(function(r) {
      return r['Code']     && String(r['Code'])     === code     &&
             r['Chapitre'] && String(r['Chapitre']) === category &&
             r['Résultat'] && String(r['Résultat']) === 'EASY';
    })
    .map(function(r) { return parseInt(r['NumExo']); });

  var hardIdxs = getRows(SH.SCORES)
    .filter(function(r) {
      return r['Code']     && String(r['Code'])     === code     &&
             r['Chapitre'] && String(r['Chapitre']) === category &&
             r['Résultat'] && String(r['Résultat']) === 'HARD';
    })
    .map(function(r) { return parseInt(r['NumExo']); });

  // Priorité 1 : exos difficiles (HARD) → à retravailler en priorité
  // Priorité 2 : exos jamais vus
  // Priorité 3 : exos EASY (fallback si nécessaire)
  var hardExos  = allExos.filter(function(ex, i) { return hardIdxs.indexOf(i + 1) !== -1; });
  var freshExos = allExos.filter(function(ex, i) { return allSeenIdxs.indexOf(i + 1) === -1; });
  var easyExos  = allExos.filter(function(ex, i) { return easyIdxs.indexOf(i + 1) !== -1; });

  var candidates = shuffle(hardExos).concat(shuffle(freshExos));
  if (candidates.length < 3) candidates = candidates.concat(shuffle(easyExos));
  if (candidates.length < 3) candidates = allExos; // fallback total

  // ── P3 : Si tous les exos du chapitre vus + niveau faible → chercher un chapitre prérequis connexe
  if (freshExos.length === 0 && hardExos.length === 0 && sheetExists(SH.PREREQS)) {
    var prereqChap = null;
    var prereqRows2 = getRows(SH.PREREQS).filter(function(r) {
      return r['Niveau']   && String(r['Niveau']).toUpperCase() === level &&
             r['Chapitre'] && String(r['Chapitre']) === category;
    });
    for (var pi2 = 0; pi2 < prereqRows2.length; pi2++) {
      var relCat2 = String(prereqRows2[pi2]['PrerequisChapitre'] || '');
      var relRows2 = getRows(SH.CURRICULUM).filter(function(r) {
        return r['Niveau']    && r['Niveau'].toString().toUpperCase() === level &&
               r['Categorie'] && r['Categorie'].toString() === relCat2;
      });
      if (relRows2.length > 0) {
        var relExos2   = parseJSON(relRows2[0]['ExosJSON']);
        var seenK      = getSeenExoKeys(code);
        var freshRel   = filterSeen(relExos2, relCat2, seenK);
        if (freshRel.length >= 3) {
          candidates = shuffle(freshRel);
          prereqChap = relCat2;
          break;
        }
      }
    }
    if (prereqChap) {
      insight = 'Tu as travaillé tous les exercices de "' + titre + '". ' +
        'Voici des exercices sur le prérequis "' + prereqChap.toLowerCase().replace(/_/g, ' ') +
        '" pour consolider les bases.';
    }
  }

  var remExos = candidates.slice(0, 8);

  // Détermine la version (cap à 3)
  var existingRem = getRows(SH.REMEDIATION).filter(function(r) {
    return r['Code']      && String(r['Code'])      === code &&
           r['Categorie'] && String(r['Categorie']) === category;
  });
  var version = Math.min(existingRem.length + 1, 3);

  var insight = 'Remédiation "' + titre + '" · Version ' + version + '. ' +
    (errors.length > 0
      ? 'Exercices sélectionnés d\'après tes erreurs spécifiques.'
      : 'Nouveau set pour consolider le chapitre.');

  // RemediationChapters : Code | Categorie | Version | ExosJSON | Insight | Date
  appendRow(SH.REMEDIATION, [
    code,
    category,
    version,
    JSON.stringify(remExos),
    insight,
    today()
  ]);

  return { status: 'success' };
  ── FIN DÉSACTIVÉ ── */
}

// ════════════════════════════════════════════════════════════
//  8. UPDATE_CONFIDENCE_SCORE  (interne — appelé par saveScore)
//
//  Logique de score 0–100 par (élève, chapitre) :
//    EASY lvl1 sans indice  : +5
//    EASY lvl1 avec indice  : +2
//    EASY lvl2 sans indice  : +10
//    EASY lvl2 avec indice  : +5
//    MEDIUM (tout)          : +1
//    HARD  lvl1             : -3
//    HARD  lvl2             : -5
//  Score clampé 0–100.
//
//  Statut "maitrise" : score > 80 ET 2 derniers exos lvl2
//    consécutifs EASY sans indice.
//
//  Décroissance inactivité : si DernierePratique > 14 jours,
//    on soustrait floor((jours − 14) × 0.5) au prochain accès.
//
//  Streak global (jours consécutifs) :
//    - Si DernierePratique = hier → Streak + 1
//    - Si DernierePratique = aujourd'hui → inchangé
//    - Sinon → Streak = 1 (reset)
//    - streakAlert = true si streak en cours ET on n'a pas
//      encore joué aujourd'hui (danger de rupture ce soir)
//
//  Progress : Code | Niveau | Chapitre | Score | NbExos |
//             NbErreurs | DernierePratique | Statut | Streak
// ════════════════════════════════════════════════════════════

function updateConfidenceScore(code, level, categorie, resultat, indicesVus, exoIdx) {
  if (!sheetExists(SH.PROGRESS)) return { streakAlert: false };

  var sh       = getSheet(SH.PROGRESS);
  var data     = sh.getDataRange().getValues();
  var headers  = data[0];
  var todayStr = today();

  // Colonnes (0-indexées dans le tableau, 1-indexées pour setValues)
  var COL = {};
  headers.forEach(function(h, i) { COL[h] = i; });

  // Cherche la ligne existante pour (code, chapitre)
  var rowIndex = -1;
  for (var i = 1; i < data.length; i++) {
    if (String(data[i][COL['Code']]) === code &&
        String(data[i][COL['Chapitre']]) === categorie) {
      rowIndex = i;
      break;
    }
  }

  // Valeurs actuelles ou défauts
  var score        = rowIndex >= 0 ? (parseFloat(data[rowIndex][COL['Score']])        || 0) : 0;
  var nbExos       = rowIndex >= 0 ? (parseInt(data[rowIndex][COL['NbExos']])         || 0) : 0;
  var nbErreurs    = rowIndex >= 0 ? (parseInt(data[rowIndex][COL['NbErreurs']])      || 0) : 0;
  var lastPractice = rowIndex >= 0 ? String(data[rowIndex][COL['DernierePratique']] || '') : '';
  var streak       = rowIndex >= 0 ? (parseInt(data[rowIndex][COL['Streak']])         || 0) : 0;
  var statut       = rowIndex >= 0 ? String(data[rowIndex][COL['Statut']] || 'non_commence') : 'non_commence';

  // ── Décroissance inactivité ───────────────────────────────
  if (lastPractice && lastPractice !== todayStr) {
    var msPerDay  = 24 * 60 * 60 * 1000;
    var lastDate  = new Date(lastPractice);
    var todayDate = new Date(todayStr);
    var daysDiff  = Math.floor((todayDate - lastDate) / msPerDay);
    if (daysDiff > 14) {
      score = Math.max(0, score - Math.floor((daysDiff - 14) * 0.5));
    }
  }

  // ── Streak ───────────────────────────────────────────────
  var streakAlert = false;
  if (!lastPractice) {
    streak = 1;
  } else if (lastPractice === todayStr) {
    // Déjà joué aujourd'hui — streak inchangé, pas d'alerte
  } else {
    var msPerDay2  = 24 * 60 * 60 * 1000;
    var lastDate2  = new Date(lastPractice);
    var todayDate2 = new Date(todayStr);
    var diff2      = Math.floor((todayDate2 - lastDate2) / msPerDay2);
    if (diff2 === 1) {
      streak++;
    } else {
      streak = 1; // reset
    }
  }

  // ── Delta de score ────────────────────────────────────────
  // lvl déterminé par position : idx 1-10 = lvl1, 11-20 = lvl2
  var exoLvl = (exoIdx && exoIdx >= 11) ? 2 : 1;
  var delta  = 0;

  if (resultat === 'EASY') {
    if (exoLvl === 1) delta = indicesVus > 0 ? 2 : 5;
    else              delta = indicesVus > 0 ? 5 : 10;
  } else if (resultat === 'MEDIUM') {
    delta = 1;
  } else if (resultat === 'HARD') {
    delta = exoLvl === 1 ? -3 : -5;
    nbErreurs++;
  }

  score = Math.min(100, Math.max(0, score + delta));
  nbExos++;

  // ── Statut "maitrise" ─────────────────────────────────────
  if (score > 80 && exoLvl === 2 && resultat === 'EASY' && indicesVus === 0) {
    var recentLvl2 = getRows(SH.SCORES).filter(function(r) {
      return r['Code']       && String(r['Code'])       === code      &&
             r['Chapitre']   && String(r['Chapitre'])   === categorie &&
             r['NumExo']     && parseInt(r['NumExo'])   >= 11         &&
             r['Résultat']   && String(r['Résultat'])   === 'EASY'    &&
             r['NbIndices'] !== undefined && parseInt(r['NbIndices']) === 0;
    });
    if (recentLvl2.length >= 2) {
      statut = 'maitrise';
    }
  } else if (statut !== 'maitrise') {
    statut = nbExos > 0 ? 'en_cours' : 'non_commence';
  }

  var newRow = [code, level, categorie, score, nbExos, nbErreurs, todayStr, statut, streak];

  if (rowIndex >= 0) {
    sh.getRange(rowIndex + 1, 1, 1, newRow.length).setValues([newRow]);
  } else {
    appendRow(SH.PROGRESS, newRow);
  }

  return { streakAlert: streakAlert, streak: streak, score: score };
}

// ════════════════════════════════════════════════════════════
//  HELPER — Construit le résumé JSON d'un chapitre (pour DeepSeek)
// ════════════════════════════════════════════════════════════
function buildChapterSummary(code, cat, niveau, catScores) {
  if (!catScores || catScores.length === 0) return '';
  var total = catScores.length;
  var easy  = catScores.filter(function(r) { return String(r['Résultat']) === 'EASY'; });
  var hard  = catScores.filter(function(r) { return String(r['Résultat']) === 'HARD'; });
  var taux  = Math.round((easy.length / total) * 100);

  var erreurs = hard.slice(-5).map(function(r) {
    return {
      enonce:           String(r['Énoncé']        || '').substring(0, 80),
      mauvaise_reponse: String(r['MauvaiseOption'] || ''),
      indices_vus:      parseInt(r['NbIndices']    || 0),
      formule_vue:      r['FormuleVue'] == 1 || r['FormuleVue'] === 'oui'
    };
  }).filter(function(e) { return e.enonce; });

  var reussiteSet = {}, reussites = [];
  easy.forEach(function(r) {
    var q = String(r['Énoncé'] || '').substring(0, 60);
    if (q && !reussiteSet[q]) { reussiteSet[q] = true; reussites.push(q); }
  });

  try {
    return JSON.stringify({
      chapitre:       cat,
      niveau:         niveau,
      exos_faits:     total,
      taux_reussite:  taux + '%',
      erreurs:        erreurs,
      reussites:      reussites.slice(0, 3)
    });
  } catch (e) { return ''; }
}

// ════════════════════════════════════════════════════════════
//  HELPER — Construit le résumé JSON du boost (pour DeepSeek)
// ════════════════════════════════════════════════════════════
function buildBoostSummary(boostScores) {
  if (!boostScores || boostScores.length === 0) return '';
  var total = boostScores.length;
  var easy  = boostScores.filter(function(r) { return String(r['Résultat']) === 'EASY'; });
  var hard  = boostScores.filter(function(r) { return String(r['Résultat']) === 'HARD'; });

  var erreurs = hard.slice(-5).map(function(r) {
    return {
      enonce:           String(r['Énoncé']        || '').substring(0, 80),
      mauvaise_reponse: String(r['MauvaiseOption'] || ''),
      indices_vus:      parseInt(r['NbIndices']    || 0)
    };
  }).filter(function(e) { return e.enonce; });

  try {
    return JSON.stringify({
      boost_date:    today(),
      exos_faits:    total,
      taux_reussite: total > 0 ? Math.round((easy.length / total) * 100) + '%' : '—',
      erreurs:       erreurs,
      reussites:     easy.slice(0, 3).map(function(r) {
        return String(r['Énoncé'] || '').substring(0, 60);
      }).filter(Boolean)
    });
  } catch (e) { return ''; }
}

// ════════════════════════════════════════════════════════════
//  SUIVI — Upsert une ligne dans "👁 Suivi" pour l'élève <code>
//  Structure avec ACTION (21 cols) :
//  A=⚡ACTION  B=Prénom  C=Niveau  D=Dernière connexion
//  E=Ch1  F=Résumé Ch1  G=→Nouveau Ch1   (Nicolas colle JSON ici)
//  H=Ch2  I=Résumé Ch2  J=→Nouveau Ch2
//  K=Ch3  L=Résumé Ch3  M=→Nouveau Ch3
//  N=Ch4  O=Résumé Ch4  P=→Nouveau Ch4
//  Q=Boost actuel  R=Résumé Boost  S=→Nouveau Boost  (Nicolas colle JSON ici)
//  T=📧 Rapport envoyé  U=Code masqué
//
//  4 règles ACTION (ordre strict) :
//  1. 🔴 DIAGNOSTIC FAIT → préparer boost 1 : scores > 0 ET jamais de boost
//  2. 🆕 BOOST TERMINÉ → préparer boost suivant : lastBoost < today ET boost consommé
//  3. ✅ CHAPITRE TERMINÉ → assigner suite : ≥20 exos ET col →Nouveau vide
//  4. 👍 RAS
// ════════════════════════════════════════════════════════════
function rebuildSuivi(code) {
  if (!sheetExists(SH.SUIVI)) return;

  // ── Utilisateur ──────────────────────────────────────────
  var users = getRows(SH.USERS);
  var user  = null;
  for (var i = 0; i < users.length; i++) {
    if (String(users[i]['Code']) === code) { user = users[i]; break; }
  }
  if (!user) return;

  var prenom = String(user['Prénom'] || '');
  var niveau = String(user['Niveau'] || '');

  // ── Scores ────────────────────────────────────────────────
  var allScores = getRows(SH.SCORES).filter(function(r) {
    return r['Code'] && String(r['Code']) === code;
  });

  var todayStr = today();
  var dates    = allScores.map(function(r) { return String(r['Date'] || ''); }).filter(Boolean).sort();
  var lastDate = dates.length ? formatDateFR(dates[dates.length - 1]) : '';

  // Chapitres dans l'ordre de première apparition (sans CALIBRAGE ni BOOST)
  var chapOrder = [], chapCount = {}, chapFirstDate = {}, chapScores = {};
  allScores.forEach(function(r) {
    var cat = String(r['Chapitre'] || '');
    var d   = String(r['Date']     || '');
    if (!cat || cat === 'CALIBRAGE' || cat === 'BOOST') return;
    chapCount[cat] = (chapCount[cat] || 0) + 1;
    if (!chapScores[cat]) chapScores[cat] = [];
    chapScores[cat].push(r);
    if (!chapFirstDate[cat] || d < chapFirstDate[cat]) chapFirstDate[cat] = d;
    if (chapOrder.indexOf(cat) === -1) chapOrder.push(cat);
  });
  chapOrder.sort(function(a, b) {
    return (chapFirstDate[a] || '') < (chapFirstDate[b] || '') ? -1 : 1;
  });

  // ── Boost ─────────────────────────────────────────────────
  var boostTodayScores = allScores.filter(function(r) {
    return String(r['Chapitre'] || '') === 'BOOST' && String(r['Date'] || '') === todayStr;
  });
  var boostTodayDone = boostTodayScores.length;
  var boostConsumed  = boostTodayDone >= 5;

  // ── Lire ligne existante — préserver colonnes Nicolas ─────
  // 0-based: Code=20, →Ch1=6, →Ch2=9, →Ch3=12, →Ch4=15, →Boost=18, Rapport=19
  var suiviSh   = getSheet(SH.SUIVI);
  var suiviData = suiviSh.getDataRange().getValues();
  var rowIdx    = -1;
  var newCh1 = '', newCh2 = '', newCh3 = '', newCh4 = '';
  var newBoost = '', rapportEnvoye = '';
  for (var j = 1; j < suiviData.length; j++) {
    if (String(suiviData[j][20]) === code) {
      rowIdx        = j;
      newCh1        = String(suiviData[j][6]  || '');
      newCh2        = String(suiviData[j][9]  || '');
      newCh3        = String(suiviData[j][12] || '');
      newCh4        = String(suiviData[j][15] || '');
      newBoost      = String(suiviData[j][18] || '');
      rapportEnvoye = String(suiviData[j][19] || '');
      break;
    }
  }

  // Chapitres 5+ dans col S si Nicolas n'a rien écrit
  var extraChaps = chapOrder.length > 4
    ? chapOrder.slice(4).map(function(c) { return c + '(' + (chapCount[c] || 0) + ')'; }).join(', ')
    : '';
  if (extraChaps && !rapportEnvoye) rapportEnvoye = 'Chap+: ' + extraChaps;

  // ── Calcul ACTION (4 règles revues) ──────────────────────
  var allUserBoosts = getRows(SH.BOOSTS).filter(function(r) { return String(r['Code']||'') === code; });
  var lastBoostDate = allUserBoosts.length
    ? allUserBoosts.map(function(r){ return String(r['Date']||''); }).sort().pop()
    : '';

  // Dernier boost : ExosDone (col D, index 3)
  var lastBoostExosDone = 0;
  if (allUserBoosts.length > 0) {
    var sortedBoosts = allUserBoosts.slice().sort(function(a, b) {
      var da = String(a['Date']||''), db = String(b['Date']||'');
      return da < db ? 1 : da > db ? -1 : 0;
    });
    lastBoostExosDone = parseInt(sortedBoosts[0]['ExosDone'] || 0) || 0;
  }

  // Inactivité > 7j
  var inactif7j = false;
  if (lastDate) {
    try {
      var daysInact7 = Math.floor((new Date(todayStr) - new Date(lastDate.substring(0,10))) / 86400000);
      if (daysInact7 > 7) inactif7j = true;
    } catch(e) {}
  } else {
    inactif7j = true; // jamais connecté
  }

  // Score < 40 sur tous chapitres
  var allChapLow = chapOrder.length > 0 && chapOrder.every(function(cat) {
    var exos = chapScores[cat] || [];
    if (!exos.length) return true;
    var easy = exos.filter(function(r){ return String(r['Résultat']||'') === 'EASY'; }).length;
    return Math.round(easy * 100 / exos.length) < 40;
  });

  var chapTermine = chapOrder.slice(0, 4).some(function(cat) {
    return cat && (chapCount[cat]||0) >= 20 && !newCh1 && !newCh2 && !newCh3 && !newCh4;
  });

  var action;
  // Règle 1 : BLOQUÉ — inactif > 7j ET score < 40 partout
  if (inactif7j && allChapLow && chapOrder.length > 0) {
    action = '🔴 BLOQUÉ';
  // Règle 2 : Boost terminé (ExosDone==5) ET le dernier boost n'est pas d'aujourd'hui
  } else if (allUserBoosts.length >= 1 && lastBoostExosDone >= 5 && lastBoostDate < todayStr && !newBoost) {
    action = '⚡ BOOST TERMINÉ → préparer le suivant';
  // Règle 3 : Chapitre terminé (≥20 exos) ET col Nicolas vide
  } else if (chapTermine) {
    action = '✅ CHAPITRE TERMINÉ → assigner la suite';
  // Règle 4 : RAS
  } else {
    action = '👍 RAS';
  }

  // ── Construire la ligne ───────────────────────────────────
  var chaps   = chapOrder.slice(0, 4);
  var newCols = [newCh1, newCh2, newCh3, newCh4];
  while (chaps.length < 4) chaps.push('');

  function chapStatut(cat) {
    if (!cat) return '';
    var n = chapCount[cat] || 0;
    return n >= 20 ? '✅ Terminé (' + n + ')' : ('En cours ' + n + '/20');
  }

  var resumes = chaps.map(function(cat) {
    if (!cat) return '';
    return buildChapterSummary(code, cat, niveau, chapScores[cat] || []);
  });

  var resumeBoost = boostTodayScores.length > 0 ? buildBoostSummary(boostTodayScores) : '';

  var boostActuel = boostConsumed
    ? ('Consommé ✅ (' + boostTodayDone + '/5)')
    : (boostTodayDone > 0 ? 'En cours (' + boostTodayDone + '/5)' : '—');

  var newRow = [
    action,                                        // A ⚡ ACTION
    prenom,                                        // B Prénom
    niveau,                                        // C Niveau
    lastDate,                                      // D Dernière connexion
    chaps[0], resumes[0], newCols[0],              // E F G Ch1 | Résumé | →Nouveau
    chaps[1], resumes[1], newCols[1],              // H I J Ch2 | Résumé | →Nouveau
    chaps[2], resumes[2], newCols[2],              // K L M Ch3 | Résumé | →Nouveau
    chaps[3], resumes[3], newCols[3],              // N O P Ch4 | Résumé | →Nouveau
    boostActuel,                                   // Q Boost actuel
    resumeBoost,                                   // R Résumé Boost
    newBoost,                                      // S →Nouveau Boost (préservé)
    rapportEnvoye,                                 // T 📧 Rapport envoyé
    code                                           // U Code masqué
  ];

  if (rowIdx >= 0) {
    suiviSh.getRange(rowIdx + 1, 1, 1, newRow.length).setValues([newRow]);
  } else {
    suiviSh.appendRow(newRow);
    rowIdx = suiviSh.getLastRow() - 1;
  }

  // ── Couleurs ──────────────────────────────────────────────
  var targetRow = rowIdx + 1;  // 1-based
  var GREEN = '#d9ead3', RED = '#f4cccc', GRAY = '#efefef', WHITE = '#ffffff';
  var YELLOW = '#fff2cc';

  // Colonne A : ACTION — fond jaune pâle si ≠ RAS, gris si > 3j inactif
  var acColor = action === '👍 RAS' ? WHITE : YELLOW;
  if (lastDate) {
    try {
      var daysInact = Math.floor((new Date(todayStr) - new Date(lastDate.substring(0,10))) / 86400000);
      if (daysInact > 3) acColor = GRAY;
    } catch (e) {}
  }
  suiviSh.getRange(targetRow, 1).setBackground(acColor);

  // Paires [col chapitre (1-based), col →Nouveau (1-based)] — décalées +1 vs ancienne structure
  var colPairs = [[5, 7], [8, 10], [11, 13], [14, 16]];
  for (var ci = 0; ci < 4; ci++) {
    var cat3 = chaps[ci];
    if (!cat3) continue;
    var done3 = (chapCount[cat3] || 0) >= 20;
    suiviSh.getRange(targetRow, colPairs[ci][0]).setBackground(done3 ? GREEN : WHITE);
    var newVal = newCols[ci] || '';
    suiviSh.getRange(targetRow, colPairs[ci][1]).setBackground(done3 && !newVal ? RED : WHITE);
  }
  // Boost : Q=17, S=19 (1-based)
  suiviSh.getRange(targetRow, 17).setBackground(boostConsumed ? GRAY : WHITE);
  suiviSh.getRange(targetRow, 19).setBackground(boostConsumed && !newBoost ? RED : WHITE);
}

// ════════════════════════════════════════════════════════════
//  HELPER — Récupère le texte d'un énoncé depuis Curriculum_Officiel
//  Retourne les 60 premiers caractères, ou '' si introuvable.
// ════════════════════════════════════════════════════════════

function getEnonceFromCurriculum(level, categorie, exoIdx) {
  var levelUpper = (level || '').toUpperCase();
  var rows = getRows(SH.CURRICULUM);
  for (var i = 0; i < rows.length; i++) {
    var r = rows[i];
    if (String(r['Niveau'] || '').toUpperCase() === levelUpper &&
        String(r['Categorie'] || '') === categorie) {
      try {
        var exos = JSON.parse(r['ExosJSON'] || '[]');
        var idx  = parseInt(exoIdx) - 1;  // exoIdx est 1-indexé
        if (idx >= 0 && idx < exos.length) {
          return String(exos[idx].q || '').substring(0, 60);
        }
      } catch (e) {}
    }
  }
  return '';
}

// ════════════════════════════════════════════════════════════
//  HELPER — Écrit une ligne dans 📋 Historique (récent en haut)
//  10 colonnes : Date | Prénom | Niveau | Chapitre | Énoncé |
//                Résultat | Temps | Indices | Formule | MauvaiseOption
// ════════════════════════════════════════════════════════════

function writeToHistorique(p) {
  if (!sheetExists(SH.HISTORIQUE)) return;

  var enonce = '';
  try {
    enonce = getEnonceFromCurriculum(String(p.level), String(p.categorie), p.exercice_idx);
  } catch (e) {}

  // insertRowAfter(1) : décale vers le bas → récents en haut
  var sh = getSheet(SH.HISTORIQUE);
  sh.insertRowAfter(1);
  sh.getRange(2, 1, 1, 10).setValues([[
    today(),
    String(p.name      || ''),
    String(p.level     || ''),
    String(p.categorie || ''),
    enonce,
    String(p.resultat  || ''),
    parseInt(p.time    || 0),
    parseInt(p.indices || 0),
    p.formule ? 'oui' : 'non',
    String(p.wrongOpt  || '')
  ]]);
}

// ════════════════════════════════════════════════════════════
//  9. GET_PROGRESS
//  Payload : { code }
//  Réponse : { status, progress: [ {chapitre, niveau, score,
//               nbExos, nbErreurs, dernierePratique,
//               statut, streak}, ... ] }
// ════════════════════════════════════════════════════════════

// ════════════════════════════════════════════════════════════
//  GET_PREREQUISITES
//  Payload : (aucun)
//  Réponse : { status, prerequisites: [{niveau, chapitre,
//               prerequisNiveau, prerequisChapitre}] }
// ════════════════════════════════════════════════════════════

function getPrerequisites() {
  if (!sheetExists(SH.PREREQS)) return { status: 'success', prerequisites: [] };
  var rows = getRows(SH.PREREQS).map(function(r) {
    return {
      niveau:             String(r['Niveau']              || ''),
      chapitre:           String(r['Chapitre']            || ''),
      prerequisNiveau:    String(r['PrerequisNiveau']     || ''),
      prerequisChapitre:  String(r['PrerequisChapitre']   || '')
    };
  }).filter(function(r) { return r.niveau && r.chapitre; });
  return { status: 'success', prerequisites: rows };
}

function getProgress(p) {
  var code = String(p.code || '');
  if (!code) return { status: 'error', message: 'code requis.' };

  if (!sheetExists(SH.PROGRESS)) {
    return { status: 'success', progress: [] };
  }

  var rows = getRows(SH.PROGRESS).filter(function(r) {
    return r['Code'] && String(r['Code']) === code;
  });

  var progress = rows.map(function(r) {
    return {
      chapitre:         String(r['Chapitre']          || ''),
      niveau:           String(r['Niveau']            || ''),
      score:            parseFloat(r['Score']         || 0),
      nbExos:           parseInt(r['NbExos']          || 0),
      nbErreurs:        parseInt(r['NbErreurs']       || 0),
      dernierePratique: (r['DernierePratique'] instanceof Date)
        ? Utilities.formatDate(r['DernierePratique'], 'Europe/Paris', 'yyyy-MM-dd')
        : String(r['DernierePratique'] || ''),
      statut:           String(r['Statut']            || 'non_commence'),
      streak:           parseInt(r['Streak']          || 0)
    };
  });

  return { status: 'success', progress: progress };
}

// ════════════════════════════════════════════════════════════
//  10. DETECT_FRAGILE_PREREQUISITES  (A4)
//  Payload : { code, chapitre, niveau }
//  Réponse : { status, fragile: bool, prereq?: { chapitre, niveau } }
//
//  Logique :
//  - Calcule le taux d'erreur sur les 10 derniers exos lvl1
//    du chapitre courant dans Scores.
//  - Si taux > 60% → remonte dans Prerequisites.
//  - Vérifie le score du prérequis dans Progress.
//  - Si score prérequis < 50 → fragile = true.
// ════════════════════════════════════════════════════════════

function detectFragilePrerequisites(p) {
  var code     = String(p.code     || '');
  var chapitre = String(p.chapitre || '');
  var niveau   = String(p.niveau   || '').toUpperCase();

  if (!code || !chapitre || !niveau) {
    return { status: 'error', message: 'code, chapitre et niveau requis.' };
  }

  // Récupère les 10 derniers exos lvl1 du chapitre
  var allScores = getRows(SH.SCORES).filter(function(r) {
    return r['Code']     && String(r['Code'])     === code     &&
           r['Chapitre'] && String(r['Chapitre']) === chapitre &&
           r['NumExo']   && parseInt(r['NumExo']) <= 10;
  });

  var recent = allScores.slice(-10);

  if (recent.length < 3) {
    return { status: 'success', fragile: false };
  }

  var hardCount = recent.filter(function(r) {
    return String(r['Résultat']) === 'HARD';
  }).length;

  if (hardCount / recent.length <= 0.6) {
    return { status: 'success', fragile: false };
  }

  if (!sheetExists(SH.PREREQS)) {
    return { status: 'success', fragile: false };
  }

  var prereqs = getRows(SH.PREREQS).filter(function(r) {
    return r['Niveau']   && String(r['Niveau'])   === niveau   &&
           r['Chapitre'] && String(r['Chapitre']) === chapitre;
  });

  if (prereqs.length === 0) {
    return { status: 'success', fragile: false };
  }

  var progressRows = sheetExists(SH.PROGRESS) ? getRows(SH.PROGRESS) : [];

  for (var i = 0; i < prereqs.length; i++) {
    var preqNiveau   = String(prereqs[i]['PrerequisNiveau']   || '');
    var preqChapitre = String(prereqs[i]['PrerequisChapitre'] || '');

    var preqProgress = null;
    for (var j = 0; j < progressRows.length; j++) {
      if (String(progressRows[j]['Code'])     === code        &&
          String(progressRows[j]['Chapitre']) === preqChapitre) {
        preqProgress = progressRows[j];
        break;
      }
    }

    var preqScore = preqProgress ? parseFloat(preqProgress['Score'] || 0) : 0;

    if (preqScore < 50) {
      return {
        status:  'success',
        fragile: true,
        prereq:  { chapitre: preqChapitre, niveau: preqNiveau, score: preqScore }
      };
    }
  }

  return { status: 'success', fragile: false };
}

// ════════════════════════════════════════════════════════════
//  DEBUG — debug_progress : diagnostique updateConfidenceScore
// ════════════════════════════════════════════════════════════
function debugProgress(p) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ssId = ss ? ss.getId() : 'null';
  var progExists = sheetExists(SH.PROGRESS);
  var progRows = 0;
  var progHeaders = [];
  var writeError = '';
  if (progExists) {
    var sh = getSheet(SH.PROGRESS);
    var data = sh.getDataRange().getValues();
    progRows = data.length;
    progHeaders = data.length > 0 ? data[0] : [];
    // Tente un vrai appel updateConfidenceScore
    try {
      var r = updateConfidenceScore(
        String(p.code || 'DEBUG'),
        String(p.level || '4EME'),
        String(p.categorie || 'Fractions'),
        'EASY', 0, 1
      );
      writeError = 'ok:' + JSON.stringify(r);
    } catch(e) {
      writeError = 'EXCEPTION: ' + e.toString();
    }
  }
  return {
    status: 'success',
    spreadsheetId: ssId,
    progressSheetExists: progExists,
    progressRowCount: progRows,
    progressHeaders: progHeaders,
    updateResult: writeError
  };
}

// ════════════════════════════════════════════════════════════
//  11. QUEUE — ENQUEUE + PROCESS  (A5)
//
//  enqueueTask  : { code, type ('diagnostic'|'boost'|'remediation') }
//  processQueue : aucun payload — traite toutes les lignes pending
//
//  Queue : Code | TypeTache | Date | Statut
// ════════════════════════════════════════════════════════════

function enqueueTask(p) {
  var code = String(p.code || '');
  var type = String(p.type || '');
  if (!code || !type) return { status: 'error', message: 'code et type requis.' };

  if (!sheetExists(SH.QUEUE)) return { status: 'error', message: 'Onglet Queue introuvable.' };

  appendRow(SH.QUEUE, [code, type, today(), 'pending']);
  return { status: 'success' };
}

function processQueue() {
  if (!sheetExists(SH.QUEUE)) return { status: 'error', message: 'Onglet Queue introuvable.' };

  var sh   = getSheet(SH.QUEUE);
  var data = sh.getDataRange().getValues();
  if (data.length <= 1) return { status: 'success', processed: 0 };

  var headers = data[0];
  var COL     = {};
  headers.forEach(function(h, i) { COL[h] = i; });

  var processed = 0;
  var errors    = 0;

  for (var i = 1; i < data.length; i++) {
    var row    = data[i];
    var statut = String(row[COL['Statut']] || '');
    if (statut !== 'pending') continue;

    var code = String(row[COL['Code']]      || '');
    var type = String(row[COL['TypeTache']] || '');

    try {
      if (type === 'boost') {
        var userRows = getRows(SH.USERS).filter(function(u) {
          return u['Code'] && String(u['Code']) === code;
        });
        if (userRows.length > 0) {
          generateDailyBoost({ code: code, level: String(userRows[0]['Niveau']) });
        }
      }
      // 'diagnostic' et 'remediation' sont générés à la demande → rien à pré-générer
      sh.getRange(i + 1, COL['Statut'] + 1).setValue('done');
      processed++;
    } catch (e) {
      sh.getRange(i + 1, COL['Statut'] + 1).setValue('error');
      errors++;
    }
  }

  return { status: 'success', processed: processed, errors: errors };
}

// Placeholder pour le trigger "On edit" (configuré manuellement dans Apps Script)
function onSheetEdit(e) {
  // Le trigger Sheets surveille les modifications directes dans le Sheet.
  // La mise en queue principale se fait via saveScore (côté doPost).
}

// ════════════════════════════════════════════════════════════
//  12. GENERATE_EXAM_PREP  (A7 — Mode "Contrôle demain")
//  Payload : { code, chapitre, niveau }
//  Réponse : { status, exos[], insight }
//
//  Pioche 10 exos ciblés : priorité lvl2 non-acquis, puis lvl1.
// ════════════════════════════════════════════════════════════

function generateExamPrep(p) {
  var code     = String(p.code     || '');
  var chapitre = String(p.chapitre || '');
  var niveau   = (p.niveau || '').toUpperCase();

  if (!code || !chapitre || !isValidLevel(niveau)) {
    return { status: 'error', message: 'code, chapitre et niveau requis.' };
  }

  var chapRows = getRows(SH.CURRICULUM).filter(function(r) {
    return r['Niveau']    && r['Niveau'].toString().toUpperCase() === niveau &&
           r['Categorie'] && r['Categorie'].toString() === chapitre;
  });

  if (chapRows.length === 0) {
    return { status: 'error', message: 'Chapitre "' + chapitre + '" introuvable pour ' + niveau + '.' };
  }

  var allExos = parseJSON(chapRows[0]['ExosJSON']);
  var titre   = String(chapRows[0]['Titre'] || chapitre);

  if (allExos.length === 0) {
    return { status: 'error', message: 'Aucun exercice dans ce chapitre.' };
  }

  var easyIdxs = getRows(SH.SCORES)
    .filter(function(r) {
      return r['Code']     && String(r['Code'])     === code     &&
             r['Chapitre'] && String(r['Chapitre']) === chapitre &&
             r['Résultat'] && String(r['Résultat']) === 'EASY';
    })
    .map(function(r) { return parseInt(r['NumExo']); });

  var lvl2NotAcquired = allExos.filter(function(ex, idx) {
    return ex.lvl === 2 && easyIdxs.indexOf(idx + 1) === -1;
  });
  var lvl1NotAcquired = allExos.filter(function(ex, idx) {
    return ex.lvl === 1 && easyIdxs.indexOf(idx + 1) === -1;
  });
  var allLvl2 = allExos.filter(function(ex) { return ex.lvl === 2; });

  // 7 exos lvl2 (non-acquis en priorité) + 3 lvl1 non-acquis
  var pool = shuffle(lvl2NotAcquired).slice(0, 7);
  if (pool.length < 7) {
    pool = pool.concat(shuffle(allLvl2).slice(0, 7 - pool.length));
  }
  pool = pool.concat(shuffle(lvl1NotAcquired).slice(0, 10 - pool.length));
  if (pool.length === 0) pool = shuffle(allExos).slice(0, 10);

  var insight = 'Révision express "' + titre + '" avant ton contrôle ! ' +
    'Ces 10 questions couvrent les points essentiels. ' +
    'Concentre-toi sur les exercices de niveau 2 — ce sont ceux qui tombent en contrôle.';

  return { status: 'success', exos: pool.slice(0, 10), insight: insight };
}

// ════════════════════════════════════════════════════════════
//  13. GENERATE_MORNING_REPORT  (trigger quotidien 7h)
//
//  Configure dans Apps Script :
//    Déclencheurs → + Ajouter → generateMorningReport
//    → Heure → Chaque jour → 7h–8h
//
//  Analyse les 21 derniers jours par élève × chapitre.
//  Classe chaque notion : ACQUISE / EN_PROGRESSION / FRAGILE / BLOQUEE.
//  Envoie un email actionnable pour prompter DeepSeek.
//  Écrit dans l'onglet Rapports.
//
//  Règles de classification :
//    ACQUISE      : score > 80 ET statut='maitrise' ET 0 HARD depuis 14j ET ≥3 sessions
//    BLOQUEE      : score < 40 ET trend stable ou dégradée sur 2 semaines
//    FRAGILE      : score < 40 OU ≥3 HARD sur 7 derniers jours (mais pas bloquée)
//    EN_PROGRESSION : amélioration semaine sur semaine (taux erreur S-1 > S-2)
// ════════════════════════════════════════════════════════════

var FOUNDER_EMAIL = 'seopourvous@gmail.com';

// Retourne une date ISO (yyyy-MM-dd) décalée de N jours depuis aujourd'hui
function dateOffset(n) {
  var d = new Date();
  d.setDate(d.getDate() + n);
  return Utilities.formatDate(d, 'Europe/Paris', 'yyyy-MM-dd');
}

// Classe une chaîne date ISO dans une semaine relative (0=cette sem, 1=S-1, 2=S-2)
function weekBucket(dateStr, todayStr) {
  if (!dateStr) return -1;
  var d = dateStr.substring(0, 10);
  var diffMs   = new Date(todayStr) - new Date(d);
  var diffDays = Math.floor(diffMs / 86400000);
  if (diffDays < 0)  return -1;
  if (diffDays < 7)  return 0;
  if (diffDays < 14) return 1;
  if (diffDays < 21) return 2;
  return -1; // plus vieux, ignoré
}

function generateMorningReport() {
  var todayStr = today();
  var cutoff   = dateOffset(-21); // on regarde 21 jours en arrière

  // ── 1. Charger les données ─────────────────────────────────
  var allScores  = getRows(SH.SCORES).filter(function(r) {
    var d = String(r['Date'] || '').substring(0, 10);
    return d >= cutoff && d <= todayStr;
  });
  var allProgress = sheetExists(SH.PROGRESS) ? getRows(SH.PROGRESS) : [];

  if (allScores.length === 0) {
    GmailApp.sendEmail(
      FOUNDER_EMAIL,
      '[Matheux] Rapport ' + todayStr + ' — aucune activité',
      'Aucun exercice réalisé ces 21 derniers jours.'
    );
    return;
  }

  // ── 2. Construire profil par élève ─────────────────────────
  var students = {};
  allScores.forEach(function(r) {
    var code = String(r['Code'] || '');
    var name = String(r['Prénom'] || code);
    var lv   = String(r['Niveau'] || '');
    var chap = String(r['Chapitre'] || '');
    var res  = String(r['Résultat'] || '');
    var date = String(r['Date'] || '').substring(0, 10);
    var idx  = parseInt(r['NumExo'] || 0);
    if (!code || !chap) return;

    if (!students[code]) students[code] = { name: name, level: lv, chapters: {}, sessions: {} };
    var s = students[code];

    // Sessions distinctes (par jour)
    s.sessions[date] = true;

    // Stats par chapitre
    if (!s.chapters[chap]) {
      s.chapters[chap] = {
        total: 0, hard: 0, easy: 0, medium: 0,
        hardDates: [],
        byWeek: [
          { total:0, hard:0 },  // S0 = cette semaine
          { total:0, hard:0 },  // S1 = semaine passée
          { total:0, hard:0 }   // S2 = il y a 2 semaines
        ],
        sessionsOnChap: {}
      };
    }
    var c = s.chapters[chap];
    c.total++;
    if (res === 'HARD')   { c.hard++; c.hardDates.push(date); }
    if (res === 'EASY')     c.easy++;
    if (res === 'MEDIUM')   c.medium++;
    c.sessionsOnChap[date] = true;
    var w = weekBucket(date, todayStr);
    if (w >= 0 && w <= 2) { c.byWeek[w].total++; if (res === 'HARD') c.byWeek[w].hard++; }
  });

  // ── 3. Enrichir avec Progress (score de confiance, statut) ─
  allProgress.forEach(function(p) {
    var code = String(p['Code'] || '');
    var chap = String(p['Chapitre'] || '');
    if (!students[code] || !students[code].chapters[chap]) return;
    students[code].chapters[chap].score  = parseFloat(p['Score'] || 0);
    students[code].chapters[chap].statut = String(p['Statut'] || '');
    students[code].chapters[chap].streak = parseInt(p['Streak'] || 0);
  });

  // ── 4. Classifier chaque notion ───────────────────────────
  function classifyChap(c, todayStr) {
    var score  = c.score  || 0;
    var statut = c.statut || '';
    var nbSess = Object.keys(c.sessionsOnChap).length;

    // HARD récents
    var cutoff7  = dateOffset(-7);
    var hardLast7 = c.hardDates.filter(function(d){ return d >= cutoff7; }).length;
    var hardLast14 = c.hardDates.filter(function(d){ return d >= dateOffset(-14); }).length;

    // Taux d'erreur par semaine
    var errS0 = c.byWeek[0].total > 0 ? c.byWeek[0].hard / c.byWeek[0].total : null;
    var errS1 = c.byWeek[1].total > 0 ? c.byWeek[1].hard / c.byWeek[1].total : null;

    if (score > 80 && statut === 'maitrise' && hardLast14 === 0 && nbSess >= 3) {
      return 'ACQUISE';
    }
    // Bloquée : score bas ET pas d'amélioration sur 2 semaines
    if (score < 40 && errS0 !== null && errS1 !== null && errS0 >= errS1 - 0.05 && nbSess >= 4) {
      return 'BLOQUEE';
    }
    if (score < 40 || hardLast7 >= 3) {
      return 'FRAGILE';
    }
    // Progression : taux erreur en baisse semaine sur semaine
    if (errS0 !== null && errS1 !== null && errS0 < errS1 - 0.1) {
      return 'EN_PROGRESSION';
    }
    return 'EN_COURS';
  }

  // ── 5. Construire email + données Rapports ─────────────────
  var todayActifs = dateOffset(-1); // actifs depuis hier
  var lines  = [];
  var rapportRows = [];
  var actionsDeepSeek = [];

  lines.push('📊 RAPPORT MATHEUX — ' + todayStr);
  lines.push('══════════════════════════════════');
  lines.push('');

  var totalStudents = Object.keys(students).length;
  var totalExos = allScores.filter(function(r){
    return String(r['Date']||'').substring(0,10) >= dateOffset(-7);
  }).length;
  lines.push(totalStudents + ' élèves | ' + totalExos + ' exos (7 derniers jours)');
  lines.push('');

  // Section actions DeepSeek en tête
  var actionLines = [];

  Object.keys(students).sort().forEach(function(code) {
    var s = students[code];
    var nbSessions = Object.keys(s.sessions).length;
    var chapKeys   = Object.keys(s.chapters);

    // Stats hebdo
    var exosS0 = allScores.filter(function(r){
      return String(r['Code']||'') === code && weekBucket(String(r['Date']||'').substring(0,10), todayStr) === 0;
    }).length;

    lines.push('──────────────────────────────────');
    lines.push('👤 ' + s.name + ' (' + s.level + ') — ' + nbSessions + ' sessions | ' + exosS0 + ' exos cette semaine');
    lines.push('');

    var chapAcquis = [], chapFragiles = [], chapEnCours = [];

    chapKeys.forEach(function(chap) {
      var c    = s.chapters[chap];
      var cls  = classifyChap(c, todayStr);
      var score = Math.round(c.score || 0);
      var errRate = c.total > 0 ? Math.round(c.hard / c.total * 100) : 0;
      var nbSess = Object.keys(c.sessionsOnChap).length;

      if (cls === 'ACQUISE') {
        chapAcquis.push('  ✅ ACQUISE — ' + chap + ' (score:' + score + ', ' + nbSess + ' sessions)');

      } else if (cls === 'BLOQUEE') {
        var hardRecents = c.hardDates.filter(function(d){ return d >= dateOffset(-7); }).length;
        chapFragiles.push('  🔴 BLOQUEE — ' + chap + ' (score:' + score + ', ' + errRate + '% erreurs, ' + nbSess + ' sessions)');
        actionLines.push('[URGENT] ' + s.name + ' — ' + chap + ' (' + s.level + ')');
        actionLines.push('  Score: ' + score + '/100 | ' + errRate + '% erreurs | bloqué depuis ' + nbSess + ' sessions');
        actionLines.push('  → Prompt DeepSeek : "Génère 5 exos de remédiation sur ' + chap + ' niveau ' + s.level + ', steps très détaillés, contexte concret, niveau lvl1 uniquement"');
        actionLines.push('');

      } else if (cls === 'FRAGILE') {
        var hardLast7 = c.hardDates.filter(function(d){ return d >= dateOffset(-7); }).length;
        chapFragiles.push('  🟡 FRAGILE — ' + chap + ' (score:' + score + ', ' + hardLast7 + ' HARD cette semaine)');
        actionLines.push('[À TRAITER] ' + s.name + ' — ' + chap + ' (' + s.level + ')');
        actionLines.push('  Score: ' + score + '/100 | ' + hardLast7 + ' erreurs cette semaine');
        actionLines.push('  → Prompt DeepSeek : "Génère 3 exos de renforcement sur ' + chap + ' niveau ' + s.level + ', avec indices progressifs et formule rappelée"');
        actionLines.push('');

      } else if (cls === 'EN_PROGRESSION') {
        var errS0 = c.byWeek[0].total > 0 ? Math.round(c.byWeek[0].hard/c.byWeek[0].total*100) : 0;
        var errS1 = c.byWeek[1].total > 0 ? Math.round(c.byWeek[1].hard/c.byWeek[1].total*100) : 0;
        chapEnCours.push('  📈 PROGRESSION — ' + chap + ' (score:' + score + ', S-1:' + errS1 + '% → cette sem:' + errS0 + '% erreurs)');

      } else {
        chapEnCours.push('  📘 EN_COURS — ' + chap + ' (score:' + score + ', ' + errRate + '% erreurs)');
      }
    });

    if (chapAcquis.length)   { lines.push('Notions acquises :');   chapAcquis.forEach(function(l){ lines.push(l); });  lines.push(''); }
    if (chapFragiles.length) { lines.push('Notions à travailler :'); chapFragiles.forEach(function(l){ lines.push(l); }); lines.push(''); }
    if (chapEnCours.length)  { lines.push('En cours :');           chapEnCours.forEach(function(l){ lines.push(l); });  lines.push(''); }

    // ── Écriture dans Rapports ─────────────────────────────
    var acqNames    = chapKeys.filter(function(k){ return classifyChap(s.chapters[k], todayStr) === 'ACQUISE'; }).join(', ');
    var fragilNames = chapKeys.filter(function(k){
      var cls = classifyChap(s.chapters[k], todayStr);
      return cls === 'FRAGILE' || cls === 'BLOQUEE';
    }).join(', ');
    var scoresMoy = chapKeys.map(function(k){ return s.chapters[k].score || 0; });
    var moyScore  = scoresMoy.length > 0 ? Math.round(scoresMoy.reduce(function(a,b){return a+b;},0) / scoresMoy.length) : 0;
    var maxStreak = Math.max.apply(null, chapKeys.map(function(k){ return s.chapters[k].streak || 0; }).concat([0]));
    var nbErr7    = allScores.filter(function(r){
      return String(r['Code']||'') === code &&
             String(r['Résultat']||'') === 'HARD' &&
             weekBucket(String(r['Date']||'').substring(0,10), todayStr) === 0;
    }).length;

    var msgAuto = '';
    if (actionLines.length > 0) {
      msgAuto = 'Actions DeepSeek requises sur : ' + fragilNames;
    } else if (acqNames) {
      msgAuto = 'Bonnes nouvelles ! Notions acquises : ' + acqNames;
    } else {
      msgAuto = 'En progression — continuer le travail régulier.';
    }

    rapportRows.push([
      code, s.name, s.level,
      dateOffset(-6),       // SemaineDebut
      exosS0,               // NbExos cette semaine
      nbErr7,               // NbErreurs cette semaine
      fragilNames || '-',   // ChapitresActifs (fragiles = priorité)
      acqNames    || '-',   // ChapitresMaitrises
      moyScore,             // ScoreMoyen
      maxStreak,            // Streak max
      msgAuto               // MessageAuto
    ]);
  });

  // ── 6. Section actions DeepSeek en tête de l'email ─────────
  if (actionLines.length > 0) {
    var emailLines = [
      '📊 RAPPORT MATHEUX — ' + todayStr,
      '══════════════════════════════════',
      '',
      '⚡ CE QUE TU DOIS PROMPTER À DEEPSEEK CE MATIN :',
      '──────────────────────────────────'
    ].concat(actionLines).concat([
      '══════════════════════════════════',
      '── DÉTAIL PAR ÉLÈVE ──',
      ''
    ]).concat(lines.slice(4)); // skip le header déjà mis
    lines = emailLines;
  }

  // ── 7. Écrire dans Rapports sheet ─────────────────────────
  if (sheetExists(SH.RAPPORTS) && rapportRows.length > 0) {
    var rapSh = getSheet(SH.RAPPORTS);
    rapportRows.forEach(function(row) { rapSh.appendRow(row); });
  }

  // ── 8. Génération IA désactivée (rebranchera avec vrais élèves) ────

  // ── 9. Envoyer l'email ────────────────────────────────────
  var subject = '[Matheux] Rapport ' + todayStr + ' — ' + totalStudents + ' élèves';
  if (actionLines.length > 0) {
    subject = '[Matheux ⚡ ACTION] Rapport ' + todayStr + ' — notions à traiter';
  }
  GmailApp.sendEmail(FOUNDER_EMAIL, subject, lines.join('\n'));
}

// Alias pour rétrocompatibilité avec l'ancien trigger
function analyzeToday() { generateMorningReport(); }

// ════════════════════════════════════════════════════════════
//  14. GÉNÉRATION D'EXERCICES IA — Claude API
//
//  Flux :
//    1. generateMorningReport() appelle generatePendingExos(students)
//    2. Pour chaque élève FRAGILE/BLOQUEE → callClaude(prompt) → Pending_Exos
//    3. À chaque login → processPendingAtLogin(code) :
//         - trouve les lignes Pending_Exos où Validé = YES
//         - les pousse dans RemediationChapters (chapitres) ou DailyBoosts (boost)
//         - les retourne dans dynamicChapters / dailyBoost
//
//  Setup requis :
//    Apps Script → Paramètres → Propriétés de script
//    Clé : CLAUDE_API_KEY  |  Valeur : sk-ant-...
//
//  Sheet Pending_Exos (à créer) :
//    Code | Prénom | Niveau | Chapitre | Type | ExosJSON |
//    DateGeneree | Validé | DateValidation
// ════════════════════════════════════════════════════════════

// ── Appel Claude API ──────────────────────────────────────────
function callClaude(prompt) {
  var apiKey = PropertiesService.getScriptProperties().getProperty('CLAUDE_API_KEY');
  if (!apiKey) throw new Error('CLAUDE_API_KEY manquante dans les propriétés du script.');

  var payload = {
    model:      'claude-sonnet-4-6',
    max_tokens: 8000,
    messages:   [{ role: 'user', content: prompt }]
  };

  var response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', {
    method:           'POST',
    headers: {
      'Content-Type':      'application/json',
      'x-api-key':         apiKey,
      'anthropic-version': '2023-06-01'
    },
    payload:           JSON.stringify(payload),
    muteHttpExceptions: true
  });

  var data = JSON.parse(response.getContentText());
  if (data.error) throw new Error('Claude API error : ' + data.error.message);
  return data.content[0].text;
}

// ── Validation du format d'un exercice généré ─────────────────
function validateExo(ex) {
  if (typeof ex !== 'object' || ex === null) return false;
  if (typeof ex.q !== 'string' || ex.q.trim().length < 5) return false;
  if (typeof ex.a !== 'string' || ex.a.trim().length === 0) return false;
  if (!Array.isArray(ex.options) || ex.options.length !== 3) return false;
  if (ex.options.indexOf(ex.a) === -1) return false; // la bonne réponse doit être dans les options
  if (!Array.isArray(ex.steps) || ex.steps.length < 2 || ex.steps.length > 5) return false;
  if (typeof ex.f !== 'string' || ex.f.trim().length === 0) return false;
  if (ex.lvl !== 1 && ex.lvl !== 2) return false;
  return true;
}

// ── Normalise et valide un array d'exos brut (retour Claude) ──
//  Retourne l'array filtré, ou lève une erreur si trop d'exos invalides.
function parseAndValidateExos(raw, expectedCount) {
  var start = raw.indexOf('[');
  var end   = raw.lastIndexOf(']');
  if (start === -1 || end === -1) throw new Error('Pas de JSON array dans la réponse Claude.');
  var arr = JSON.parse(raw.substring(start, end + 1));
  if (!Array.isArray(arr)) throw new Error('La réponse n\'est pas un array JSON.');

  var valid = arr.filter(validateExo);
  var minRequired = Math.ceil(expectedCount * 0.8); // tolère 20% d'invalides
  if (valid.length < minRequired) {
    throw new Error('Seulement ' + valid.length + '/' + arr.length + ' exos valides (minimum requis : ' + minRequired + ').');
  }
  return valid;
}

// ── Prompt de génération d'exercices ─────────────────────────
//  type : 'boost' (5 exos ciblés) | 'chapter' (20 exos complets)
function buildExoPrompt(prenom, niveau, chapitre, type, hardQuestions, score, statut) {
  var n = type === 'boost' ? 5 : 20;

  // Description du profil adaptatif
  var profileDesc;
  if (score < 20) {
    profileDesc = 'PROFIL TRÈS FAIBLE (score ' + score + '/100). Partir des bases absolues. Chaque question doit être décomposable étape par étape. Utiliser des contextes très concrets et familiers (argent, distances, nourriture). Ne jamais supposer que l\'élève connaît une notion non explicitée.';
  } else if (score < 40) {
    profileDesc = 'PROFIL FRAGILE (score ' + score + '/100). Les fondamentaux sont instables. Chaque step doit expliquer le POURQUOI avant le COMMENT. Varier légèrement les présentations pour que l\'élève reconnaisse la notion dans des contextes différents.';
  } else if (score < 60) {
    profileDesc = 'PROFIL EN PROGRESSION (score ' + score + '/100). Les bases existent mais les transferts sont difficiles. Partir d\'un exemple concret puis généraliser. Les exos lvl2 doivent introduire une légère complexité supplémentaire (données manquantes, reformulation).';
  } else if (score < 80) {
    profileDesc = 'PROFIL CORRECT (score ' + score + '/100). Consolider les acquis et introduire des variantes pour ancrer la généralisation. Les exos lvl2 peuvent inclure des pièges calculatoires ou des reformulations inhabituelles.';
  } else {
    profileDesc = 'PROFIL FORT (score ' + score + '/100). Proposer des exercices challengeants. Les exos lvl2 peuvent mêler plusieurs notions ou demander un raisonnement en plusieurs étapes non guidées.';
  }

  // Section erreurs récentes
  var errorsSection;
  if (hardQuestions.length > 0) {
    errorsSection = [
      'ERREURS RÉCENTES DE L\'ÉLÈVE (questions où il/elle a échoué — à cibler en priorité) :',
      hardQuestions.slice(0, 6).map(function(q, i) { return (i + 1) + '. ' + q; }).join('\n'),
      '→ Construire au moins ' + Math.min(hardQuestions.length, 3) + ' exercice(s) testant exactement ces lacunes (même notion, formulation différente).'
    ].join('\n');
  } else {
    errorsSection = 'Aucune erreur spécifique récente — générer une progression équilibrée couvrant les points essentiels du chapitre.';
  }

  // Répartition niveaux
  var lvlInstructions;
  if (type === 'boost') {
    lvlInstructions = [
      'RÉPARTITION NIVEAUX pour ce boost de 5 exos :',
      '- 2 exos lvl:1 (accessible, fondamental, guidé)',
      '- 3 exos lvl:2 (application, légèrement plus complexe)',
      '→ Si l\'élève est très faible (score < 30), inverser : 3 lvl:1 + 2 lvl:2'
    ].join('\n');
  } else {
    lvlInstructions = [
      'RÉPARTITION NIVEAUX pour ce chapitre de 20 exos :',
      '- Exos 1–10 : lvl:1 — fondamentaux, contextes concrets, très bien guidé',
      '- Exos 11–20 : lvl:2 — application, autonomie, légèrement plus complexe',
      '→ Progression croissante de difficulté au sein de chaque groupe'
    ].join('\n');
  }

  // Exemple d'exercice conforme (ancre le format)
  var exampleExo = JSON.stringify({
    lvl: 1,
    q: "Une pizza coûte $12{,}50$ €. Sarah a $8$ €. Combien lui manque-t-il ?",
    a: "4,50 €",
    options: ["4,50 €", "3,50 €", "20,50 €"],
    steps: [
      "Indice 1 : Cherche ce qui manque = ce qu'il faut ajouter à ce qu'on a pour atteindre le prix.",
      "Indice 2 : Pose la soustraction : $12{,}50 - 8 = ?$",
      "Indice 3 : $12{,}50 - 8 = 4{,}50$ €. Vérifie : $8 + 4{,}50 = 12{,}50$ ✓"
    ],
    f: "Manquant = Prix total $-$ Argent disponible"
  }, null, 2);

  return [
    'Tu es un professeur de maths expérimenté créant des exercices pédagogiques pour collégiens français (niveaux 6ème–3ème).',
    '',
    '══════ CONTEXTE ÉLÈVE ══════',
    'Prénom : ' + prenom + ' | Niveau : ' + niveau + ' | Chapitre : ' + chapitre,
    'Score de confiance : ' + score + '/100 | Statut : ' + statut,
    '',
    profileDesc,
    '',
    '══════ ERREURS À CIBLER ══════',
    errorsSection,
    '',
    '══════ OBJECTIF ══════',
    'Générer EXACTEMENT ' + n + ' exercices pour le chapitre "' + chapitre + '".',
    lvlInstructions,
    '',
    '══════ RÈGLES IMPÉRATIVES ══════',
    '1. STEPS — 3 étapes obligatoires, progression vague→méthode→quasi-solution :',
    '   • Step 1 : indice vague sur la stratégie ("De quoi as-tu besoin ?", "Quelle opération…")',
    '   • Step 2 : méthode concrète avec formule ou calcul intermédiaire',
    '   • Step 3 : quasi-solution (calcul final ou vérification guidée)',
    '2. OPTIONS — 3 valeurs exactes dont la bonne réponse + 2 distracteurs ciblant des erreurs fréquentes :',
    '   • Ex pour fractions : si a = "3/4", distracteurs = "1/4" (soustraction au lieu d\'addition) et "4/3" (inversion)',
    '   • "a" doit apparaître mot pour mot dans "options"',
    '3. FORMULE — "f" = règle clé en 1 ligne max, en LaTeX si math (ex: "$a^2 + b^2 = c^2$")',
    '4. LATEX — utiliser $ $ pour tout symbole maths : $\\frac{3}{4}$, $\\times$, $\\div$, $\\sqrt{25}$, $x^2$',
    '5. CONTEXTES — exos lvl:1 dans des contextes concrets du quotidien (sport, cuisine, argent, transports)',
    '6. LVL — doit être exactement 1 (fondamental) ou 2 (application)',
    '7. "a" — réponse avec unité si nécessaire (ex: "4,50 €", "12 cm", "3/4")',
    '',
    '══════ EXEMPLE D\'EXERCICE CONFORME ══════',
    exampleExo,
    '',
    '══════ FORMAT DE RÉPONSE ══════',
    'Retourne UNIQUEMENT un JSON array de ' + n + ' objets, sans texte avant ni après, sans balise markdown.',
    'Chaque objet DOIT avoir exactement ces 6 champs : lvl, q, a, options, steps, f',
    '',
    '['
  ].join('\n');
}

// ── Génère les exos en attente pour tous les élèves fragiles ─
function generatePendingExos(students) {
  if (!sheetExists(SH.PENDING)) return; // sheet pas encore créé → skip silencieux
  var todayStr = today();

  // Éviter de regénérer si déjà fait aujourd'hui pour cet élève+chapitre
  var existingPending = getRows(SH.PENDING);
  var alreadyDone = {};
  existingPending.forEach(function(r) {
    alreadyDone[String(r['Code']) + '_' + String(r['Chapitre']) + '_' + String(r['Type'])] = true;
  });

  var pendingSh = getSheet(SH.PENDING);

  Object.keys(students).forEach(function(code) {
    var s = students[code];

    // Récupérer les erreurs récentes par chapitre (7 derniers jours)
    var cutoff7 = dateOffset(-7);
    var recentHard = {};
    getRows(SH.SCORES).filter(function(r) {
      return String(r['Code'] || '') === code &&
             String(r['Résultat'] || '') === 'HARD' &&
             String(r['Date'] || '').substring(0, 10) >= cutoff7;
    }).forEach(function(r) {
      var chap = String(r['Chapitre'] || '');
      if (!recentHard[chap]) recentHard[chap] = [];
      if (r['Énoncé']) recentHard[chap].push(String(r['Énoncé']));
    });

    Object.keys(s.chapters).forEach(function(chap) {
      var c   = s.chapters[chap];
      var cls = classifyChap(c, todayStr);
      if (cls !== 'FRAGILE' && cls !== 'BLOQUEE') return; // skip les autres

      var score  = Math.round(c.score || 0);
      var hardQs = (recentHard[chap] || []).slice(0, 5); // max 5 erreurs comme contexte

      // ── Boost (5 exos) ───────────────────────────────────
      var boostKey = code + '_' + chap + '_boost';
      if (!alreadyDone[boostKey]) {
        try {
          var bPrompt = buildExoPrompt(s.name, s.level, chap, 'boost', hardQs, score, cls);
          var bRaw    = callClaude(bPrompt);
          var bExos   = parseAndValidateExos(bRaw, 5);
          pendingSh.appendRow([code, s.name, s.level, chap, 'boost', JSON.stringify(bExos), todayStr, '', '']);
          alreadyDone[boostKey] = true;
        } catch(e) {
          Logger.log('Erreur génération boost ' + code + '/' + chap + ' : ' + e.toString());
        }
      }

      // ── Nouveau chapitre (20 exos) — seulement si BLOQUEE ─
      if (cls === 'BLOQUEE') {
        var chapKey = code + '_' + chap + '_chapter';
        if (!alreadyDone[chapKey]) {
          try {
            var cPrompt = buildExoPrompt(s.name, s.level, chap, 'chapter', hardQs, score, cls);
            var cRaw    = callClaude(cPrompt);
            var cExos   = parseAndValidateExos(cRaw, 20);
            pendingSh.appendRow([code, s.name, s.level, chap, 'chapter', JSON.stringify(cExos), todayStr, '', '']);
            alreadyDone[chapKey] = true;
          } catch(e) {
            Logger.log('Erreur génération chapitre ' + code + '/' + chap + ' : ' + e.toString());
          }
        }
      }
    });
  });
}

// ── Traitement des exos validés au login ──────────────────────
//  Retourne { newDynamicChapters: [...], newBoost: obj|null }
function processPendingAtLogin(code) {
  if (!sheetExists(SH.PENDING)) return { newDynamicChapters: [], newBoost: null };

  var sh2     = getSheet(SH.PENDING);
  var data    = sh2.getDataRange().getValues();
  var headers = data[0];
  var COL     = {};
  headers.forEach(function(h, i) { COL[h] = i; });

  var todayStr         = today();
  var newDynamic       = [];
  var newBoost         = null;

  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var rCode    = String(row[COL['Code']]          || '');
    var rType    = String(row[COL['Type']]          || '');
    var rValide  = String(row[COL['Validé']]        || '').toUpperCase().trim();
    var rDateVal = String(row[COL['DateValidation']]|| '');

    if (rCode !== code || rValide !== 'YES' || rDateVal !== '') continue; // pas pour cet élève ou déjà traité

    var rChap  = String(row[COL['Chapitre']] || '');
    var rExos  = parseJSON(row[COL['ExosJSON']] || '[]');
    var rPrenom= String(row[COL['Prénom']]   || '');
    var rNiv   = String(row[COL['Niveau']]   || '');

    if (rType === 'boost') {
      // Écrire dans DailyBoosts pour demain
      var insight = 'Boost personnalisé sur ' + rChap + ' — généré par IA sur tes erreurs récentes.';
      appendRow(SH.BOOSTS, [code, todayStr, JSON.stringify({ insight: insight, exos: rExos })]);
      newBoost = { insight: insight, exos: rExos };

    } else if (rType === 'chapter') {
      // Écrire dans RemediationChapters (version auto)
      var existingVersions = getRows(SH.REMEDIATION)
        .filter(function(r) { return String(r['Code']) === code && String(r['Categorie']) === rChap; })
        .map(function(r) { return parseInt(r['Version'] || 0); });
      var nextVersion = existingVersions.length > 0 ? Math.max.apply(null, existingVersions) + 1 : 1;
      if (nextVersion <= 3) { // cap V3
        appendRow(SH.REMEDIATION, [
          code, rChap, nextVersion,
          JSON.stringify(rExos),
          'Chapitre IA généré sur tes lacunes — version ' + nextVersion,
          todayStr
        ]);
        newDynamic.push({
          originalCat: rChap,
          version:     nextVersion,
          exos:        rExos,
          insight:     'Nouveau contenu ciblé sur tes erreurs en ' + rChap
        });
      }
    }

    // Marquer comme traité
    sh2.getRange(i + 1, COL['DateValidation'] + 1).setValue(todayStr);
  }

  return { newDynamicChapters: newDynamic, newBoost: newBoost };
}

// ════════════════════════════════════════════════════════════
//  ADMIN — verifyAdmin
//  Vérifie qu'un code correspond bien à un utilisateur IsAdmin=1.
// ════════════════════════════════════════════════════════════

function verifyAdmin(adminCode) {
  if (!adminCode) return false;
  var users = getRows(SH.USERS);
  for (var i = 0; i < users.length; i++) {
    if (String(users[i]['Code']) === adminCode) {
      return parseInt(users[i]['IsAdmin'] || 0) === 1;
    }
  }
  return false;
}

// ════════════════════════════════════════════════════════════
//  ADMIN — get_admin_overview
//  Payload : { adminCode }
//  Réponse : { status, students: [ { code, prenom, niveau,
//    lastConnection, action, chapitres, boostActuel,
//    boostNew, chapNewCount, chapitresDetail } ] }
//
//  chapitresDetail : par chapitre (30 derniers jours) :
//    { cat, totalExos, hardCount, rateSuccess, avgTime,
//      avgIndices, pctFormula, exosList (12 max, récents) }
//
//  Lit 👁 Suivi (index-based) + Scores (tous résultats).
//  Trie : non-RAS en tête, puis par lastConnection desc.
// ════════════════════════════════════════════════════════════

function getAdminOverview(p) {
  if (!verifyAdmin(String(p.adminCode || ''))) {
    return { status: 'error', message: 'Accès refusé.' };
  }

  var users = getRows(SH.USERS);

  // ── Lecture raw du Suivi ─────────────────────────────────
  var suiviByCode = {};
  if (sheetExists(SH.SUIVI)) {
    var suiviSh  = getSheet(SH.SUIVI);
    var suiviRaw = suiviSh.getDataRange().getValues();
    for (var si = 1; si < suiviRaw.length; si++) {
      var rowCode = String(suiviRaw[si][20] || '');
      if (rowCode) suiviByCode[rowCode] = suiviRaw[si];
    }
  }

  // ── Scores (30 derniers jours, TOUS résultats) ───────────
  var cutoff30 = dateOffset(-30);
  var scoresByCode = {};  // code → { cat → { exos:[] } }
  getRows(SH.SCORES).forEach(function(r) {
    var code = String(r['Code']     || '');
    var cat  = String(r['Chapitre'] || '');
    var res  = String(r['Résultat'] || '');
    var date = String(r['Date']     || '').substring(0, 10);
    if (!code || !cat || cat === 'CALIBRAGE' || cat === 'BOOST') return;
    if (date < cutoff30) return;
    if (!scoresByCode[code])      scoresByCode[code]      = {};
    if (!scoresByCode[code][cat]) scoresByCode[code][cat] = { exos: [] };
    var enonce = String(r['Énoncé'] || '');
    // Détection source : on utilise la longueur NumExo pour les diagnostics (1-2 exos)
    // Les diagnostics ont typiquement NumExo 1 ou 2, et les questions sont réelles
    // On détecte via le num d'exo et la présence de patterns: anciens labels ou petits NumExo
    var numExoRaw = parseInt(r['NumExo'] || 0) || 0;
    var scoreSource = 'chapter';
    // Note: les scores de diagnostic ont NumExo 1-2 (2 exos par chapitre en diag)
    // Les boosts ont NumExo 1-5 et sont dans un contexte "boost" (date J+1 du diag)
    // En pratique on ne peut pas toujours distinguer, on utilise une heuristique:
    // On expose la source telle quelle pour l'admin
    scoresByCode[code][cat].exos.push({
      res:     res,
      enonce:  enonce,
      wrongOpt:String(r['MauvaiseOption']  || ''),
      indices: parseInt(r['NbIndices']     || 0) || 0,
      formula: String(r['FormuleVue']      || '').toLowerCase() === 'true' || String(r['FormuleVue'] || '') === '1',
      temps:   parseInt(r['Temps(sec)']    || 0) || 0,
      date:    date,
      num:     numExoRaw,
      source:  scoreSource
    });
  });

  // ── DailyBoosts (tous) ───────────────────────────────────
  var todayStrAdmin = today();
  var boostsByCode = {};  // code → [ { date, exosDone, boostJSON } ]
  getRows(SH.BOOSTS).forEach(function(r) {
    var code = String(r['Code'] || '');
    if (!code) return;
    var bDate = r['Date'];
    var bDateStr = (bDate instanceof Date)
      ? Utilities.formatDate(bDate, 'Europe/Paris', 'yyyy-MM-dd')
      : String(bDate || '').substring(0, 10);
    var exosDone = parseInt(r['ExosDone'] || 0) || 0;
    var boostJSON = String(r['BoostJSON'] || '');
    var boostObj = null;
    try { boostObj = JSON.parse(boostJSON); } catch (e) {}
    if (!boostsByCode[code]) boostsByCode[code] = [];
    boostsByCode[code].push({ date: bDateStr, exosDone: exosDone, boost: boostObj });
  });

  // ── Progress (pour currentChapExosDone) ─────────────────
  var progressByCode = {};  // code → [ { chapitre, nbExos, score, statut } ]
  getRows(SH.PROGRESS).forEach(function(r) {
    var code = String(r['Code'] || '');
    if (!code) return;
    if (!progressByCode[code]) progressByCode[code] = [];
    progressByCode[code].push({
      chapitre: String(r['Chapitre'] || ''),
      nbExos:   parseInt(r['NbExos'] || 0) || 0,
      score:    parseFloat(r['Score'] || 0) || 0,
      statut:   String(r['Statut'] || '')
    });
  });

  // ── Construction de la liste élèves ─────────────────────
  var CHAP_NEW_IDX  = [6, 9, 12, 15];
  var BOOST_NEW_IDX = 18;

  var students = users
    .filter(function(u) { return parseInt(u['IsAdmin'] || 0) !== 1; })
    .map(function(u) {
      var code   = String(u['Code']   || '');
      var prenom = String(u['Prénom'] || '');
      var niveau = String(u['Niveau'] || '');

      var row            = suiviByCode[code] || null;
      var action         = row ? String(row[0] || '👍 RAS') : '👍 RAS';
      var lastConnection = row ? String(row[3] || '')       : '';

      // Chapitres Suivi (slots 1-4)
      var chapSlots = [
        { catIdx: 4,  statIdx: 5,  newIdx: 6  },
        { catIdx: 7,  statIdx: 8,  newIdx: 9  },
        { catIdx: 10, statIdx: 11, newIdx: 12 },
        { catIdx: 13, statIdx: 14, newIdx: 15 }
      ];
      var chapitres = [];
      chapSlots.forEach(function(sl) {
        var cat = row ? String(row[sl.catIdx] || '') : '';
        if (!cat) return;
        chapitres.push({
          cat:        cat,
          statut:     row ? String(row[sl.statIdx] || '') : '',
          pendingNew: row ? (String(row[sl.newIdx] || '').trim() !== '') : false
        });
      });

      var chapNewCount = row
        ? CHAP_NEW_IDX.filter(function(ci) { return String(row[ci] || '').trim() !== ''; }).length
        : 0;

      var boostActuel = row ? String(row[16] || '—') : '—';
      var boostNew    = row ? (String(row[BOOST_NEW_IDX] || '').trim() !== '') : false;

      // Détail par chapitre (depuis Scores 30j) — TOUS les exos, pas de cap
      var chapData = scoresByCode[code] || {};
      var chapitresDetail = Object.keys(chapData).map(function(cat) {
        var exos      = chapData[cat].exos;
        var total     = exos.length;
        var hardExos  = exos.filter(function(e) { return e.res === 'HARD'; });
        var easyCount = exos.filter(function(e) { return e.res === 'EASY'; }).length;
        var totalTime = exos.reduce(function(s, e) { return s + e.temps;   }, 0);
        var totalIdx  = exos.reduce(function(s, e) { return s + e.indices; }, 0);
        var fCount    = exos.filter(function(e) { return e.formula; }).length;
        // Tri par num décroissant → du plus récent au plus ancien
        var sorted    = exos.slice().sort(function(a, b) { return b.num - a.num; });
        return {
          cat:        cat,
          totalExos:  total,
          hardCount:  hardExos.length,
          rateSuccess:total ? Math.round(easyCount * 100 / total) : 0,
          avgTime:    total ? Math.round(totalTime  / total)      : 0,
          avgIndices: total ? Math.round(totalIdx   / total * 10) / 10 : 0,
          pctFormula: total ? Math.round(fCount     * 100 / total)     : 0,
          exosList:   sorted  // tous les exos, sans cap
        };
      }).sort(function(a, b) { return b.hardCount - a.hardCount; }); // plus fragile en 1er

      // ── boostHistory ───────────────────────────────────────
      var userBoosts = (boostsByCode[code] || []).slice().sort(function(a, b) {
        return b.date > a.date ? 1 : b.date < a.date ? -1 : 0;
      });
      var boostHistory = userBoosts.map(function(b) {
        var status = b.exosDone === 0 ? 'pending'
          : b.exosDone >= 5 ? 'done'
          : 'in_progress';
        return {
          date:      b.date,
          exosDone:  b.exosDone,
          insight:   b.boost ? (b.boost.insight || '') : '',
          exos:      b.boost ? (b.boost.exos || []) : [],
          status:    status,
          isPending: b.exosDone === 0
        };
      });

      // boost du jour ou dernier boost non terminé
      var currentBoostExosDone = 0;
      if (userBoosts.length > 0) {
        var todayBoost = userBoosts.find(function(b) { return b.date === todayStrAdmin; });
        if (todayBoost) {
          currentBoostExosDone = todayBoost.exosDone;
        } else {
          // dernier boost non encore terminé
          var lastUnfinished = userBoosts.find(function(b) { return b.exosDone < 5; });
          if (lastUnfinished) currentBoostExosDone = lastUnfinished.exosDone;
        }
      }

      // ── currentChapExosDone ────────────────────────────────
      var userProgress = progressByCode[code] || [];
      // Chapitre en cours = le premier non maîtrisé avec des exos
      var currentChapExosDone = 0;
      var activeChapProgress = userProgress
        .filter(function(pr) { return pr.nbExos > 0 && pr.nbExos < 20; })
        .sort(function(a, b) { return b.nbExos - a.nbExos; });
      if (activeChapProgress.length > 0) {
        currentChapExosDone = activeChapProgress[0].nbExos;
      }

      return {
        code:                 code,
        prenom:               prenom,
        niveau:               niveau,
        lastConnection:       lastConnection,
        action:               action,
        chapitres:            chapitres,
        chapNewCount:         chapNewCount,
        boostActuel:          boostActuel,
        boostNew:             boostNew,
        chapitresDetail:      chapitresDetail,
        boostHistory:         boostHistory,
        currentBoostExosDone: currentBoostExosDone,
        currentChapExosDone:  currentChapExosDone
      };
    })
    .sort(function(a, b) {
      var aRas = a.action.indexOf('RAS') !== -1;
      var bRas = b.action.indexOf('RAS') !== -1;
      if (aRas !== bRas) return aRas ? 1 : -1;
      if (b.lastConnection > a.lastConnection) return 1;
      if (b.lastConnection < a.lastConnection) return -1;
      return 0;
    });

  return { status: 'success', students: students };
}

// ════════════════════════════════════════════════════════════
//  ADMIN — publish_admin_boost
//  Payload : { adminCode, targetCode, exos (array), insight }
//
//  Écrit dans la colonne S (→Nouveau Boost) du 👁 Suivi.
//  L'élève recevra le boost au prochain login via login().
//  Valide le format minimum de chaque exo avant écriture.
// ════════════════════════════════════════════════════════════

function publishAdminBoost(p) {
  if (!verifyAdmin(String(p.adminCode || ''))) {
    return { status: 'error', message: 'Accès refusé.' };
  }

  var targetCode = String(p.targetCode || '');
  var insight    = String(p.insight    || 'Boost personnalisé de ton prof.');
  if (!targetCode) return { status: 'error', message: 'targetCode requis.' };

  // ── Validation des exos ──────────────────────────────────
  var exos;
  try {
    exos = (typeof p.exos === 'string') ? JSON.parse(p.exos) : p.exos;
    if (!Array.isArray(exos) || exos.length === 0) {
      return { status: 'error', message: 'exos doit être un tableau non vide.' };
    }
    for (var i = 0; i < exos.length; i++) {
      var ex = exos[i];
      if (!ex || typeof ex.q !== 'string' || !ex.q.trim()) {
        return { status: 'error', message: 'Exo ' + (i + 1) + ' invalide : champ "q" manquant.' };
      }
      if (typeof ex.a !== 'string' || !ex.a.trim()) {
        return { status: 'error', message: 'Exo ' + (i + 1) + ' invalide : champ "a" manquant.' };
      }
      if (!Array.isArray(ex.options) || ex.options.length === 0) {
        return { status: 'error', message: 'Exo ' + (i + 1) + ' invalide : options[] manquant.' };
      }
      if (ex.options.indexOf(ex.a) === -1) {
        return { status: 'error', message: 'Exo ' + (i + 1) + ' invalide : "a" absent des options.' };
      }
    }
  } catch (e) {
    return { status: 'error', message: 'JSON invalide : ' + e.toString() };
  }

  if (!sheetExists(SH.SUIVI)) {
    return { status: 'error', message: 'Onglet 👁 Suivi introuvable.' };
  }

  var motProf   = String(p.motProf || '').trim();
  var boostObj  = { insight: insight, exos: exos };
  if (motProf) boostObj.motProf = motProf;
  var boostJSON = JSON.stringify(boostObj);

  var suiviSh   = getSheet(SH.SUIVI);
  var suiviData = suiviSh.getDataRange().getValues();
  var found     = false;

  for (var si = 1; si < suiviData.length; si++) {
    if (String(suiviData[si][20]) === targetCode) {
      suiviSh.getRange(si + 1, 19).setValue(boostJSON); // col S = 0-based 18 → 1-based 19
      found = true;
      break;
    }
  }

  if (!found) {
    // Première fois : construire le Suivi pour cet élève, puis réécrire
    try { rebuildSuivi(targetCode); } catch (e) {}
    suiviData = suiviSh.getDataRange().getValues();
    for (var si2 = 1; si2 < suiviData.length; si2++) {
      if (String(suiviData[si2][20]) === targetCode) {
        suiviSh.getRange(si2 + 1, 19).setValue(boostJSON);
        found = true;
        break;
      }
    }
  }

  if (!found) return { status: 'error', message: 'Élève introuvable dans le Suivi.' };

  try { rebuildSuivi(targetCode); } catch (e) {}

  return { status: 'success', message: 'Boost publié. L\'élève le recevra à son prochain login.' };
}

// ════════════════════════════════════════════════════════════
//  ADMIN — publish_admin_chapter
//  Payload : { adminCode, targetCode, categorie, exos (array), insight }
//
//  Écrit dans la première colonne →Nouveau Ch libre (G/J/M/P).
//  Si les 4 slots sont pleins, écrase le slot G (le plus ancien).
//  L'élève recevra le chapitre au prochain login via login().
// ════════════════════════════════════════════════════════════

function publishAdminChapter(p) {
  if (!verifyAdmin(String(p.adminCode || ''))) {
    return { status: 'error', message: 'Accès refusé.' };
  }

  var targetCode = String(p.targetCode || '');
  var categorie  = String(p.categorie  || '');
  var insight    = String(p.insight    || 'Nouveau chapitre personnalisé de ton prof.');
  if (!targetCode || !categorie) {
    return { status: 'error', message: 'targetCode et categorie requis.' };
  }

  // ── Validation des exos ──────────────────────────────────
  var exos;
  try {
    exos = (typeof p.exos === 'string') ? JSON.parse(p.exos) : p.exos;
    if (!Array.isArray(exos) || exos.length === 0) {
      return { status: 'error', message: 'exos doit être un tableau non vide.' };
    }
    for (var i = 0; i < exos.length; i++) {
      var ex = exos[i];
      if (!ex || typeof ex.q !== 'string' || !ex.q.trim()) {
        return { status: 'error', message: 'Exo ' + (i + 1) + ' invalide : "q" manquant.' };
      }
      if (typeof ex.a !== 'string' || !ex.a.trim()) {
        return { status: 'error', message: 'Exo ' + (i + 1) + ' invalide : "a" manquant.' };
      }
      if (!Array.isArray(ex.options) || ex.options.length === 0) {
        return { status: 'error', message: 'Exo ' + (i + 1) + ' invalide : options[] manquant.' };
      }
      if (ex.options.indexOf(ex.a) === -1) {
        return { status: 'error', message: 'Exo ' + (i + 1) + ' : "a" absent des options.' };
      }
    }
  } catch (e) {
    return { status: 'error', message: 'JSON invalide : ' + e.toString() };
  }

  if (!sheetExists(SH.SUIVI)) {
    return { status: 'error', message: 'Onglet 👁 Suivi introuvable.' };
  }

  var motProf  = String(p.motProf || '').trim();
  var chapObj  = { categorie: categorie, insight: insight, exos: exos };
  if (motProf) chapObj.motProf = motProf;
  var chapJSON = JSON.stringify(chapObj);

  // Slots →Nouveau Ch : 0-based indices 6, 9, 12, 15 → 1-based 7, 10, 13, 16
  var SLOTS_0 = [6, 9, 12, 15];
  var SLOTS_1 = [7, 10, 13, 16];

  var suiviSh   = getSheet(SH.SUIVI);
  var suiviData = suiviSh.getDataRange().getValues();
  var found     = false;

  for (var si = 1; si < suiviData.length; si++) {
    if (String(suiviData[si][20]) !== targetCode) continue;

    // Trouver le premier slot libre
    var written = false;
    for (var ci = 0; ci < SLOTS_0.length; ci++) {
      if (!String(suiviData[si][SLOTS_0[ci]] || '').trim()) {
        suiviSh.getRange(si + 1, SLOTS_1[ci]).setValue(chapJSON);
        written = true;
        break;
      }
    }
    if (!written) {
      // Tous les slots pleins → écrase le slot G (premier, le plus ancien)
      suiviSh.getRange(si + 1, SLOTS_1[0]).setValue(chapJSON);
    }
    found = true;
    break;
  }

  if (!found) {
    try { rebuildSuivi(targetCode); } catch (e) {}
    suiviData = suiviSh.getDataRange().getValues();
    for (var si2 = 1; si2 < suiviData.length; si2++) {
      if (String(suiviData[si2][20]) === targetCode) {
        suiviSh.getRange(si2 + 1, SLOTS_1[0]).setValue(chapJSON);
        found = true;
        break;
      }
    }
  }

  if (!found) return { status: 'error', message: 'Élève introuvable dans le Suivi.' };

  try { rebuildSuivi(targetCode); } catch (e) {}

  return { status: 'success', message: 'Chapitre "' + categorie + '" publié. L\'élève le recevra à son prochain login.' };
}

// ════════════════════════════════════════════════════════════
//  TRIAL & MARKETING — ensureUsersCols / sendMarketingSequence
//  triggerDailyMarketing / checkTrialStatus
// ════════════════════════════════════════════════════════════

/**
 * Migration douce : ajoute TrialStart (col 9) et PremiumEnd (col 10)
 * au header de l'onglet Users si absentes.
 * NE JAMAIS écraser les données existantes.
 */
function ensureUsersCols() {
  var sh      = getSheet(SH.USERS);
  var header  = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
  var changed = false;

  if (header.indexOf('TrialStart') === -1) {
    var colIdx = header.length + 1; // 1-indexed
    sh.getRange(1, colIdx).setValue('TrialStart');
    header.push('TrialStart');
    changed = true;
  }

  if (header.indexOf('PremiumEnd') === -1) {
    var colIdx2 = header.length + 1;
    sh.getRange(1, colIdx2).setValue('PremiumEnd');
    changed = true;
  }

  return changed;
}

/**
 * Envoie l'email marketing du jour `day` (0, 3 ou 7) à l'utilisateur.
 * Retourne { status: 'success' } ou { status: 'error', message: ... }
 */
function sendMarketingSequence(email, prenom, day) {
  try {
    var subject, htmlBody;
    var unsubLink = 'https://matheux.fr/unsubscribe?email=' + encodeURIComponent(email);
    var footer = '<p style="margin-top:32px;font-size:12px;color:#9ca3af;text-align:center;">' +
      'Matheux · 100 % pédagogique, 0 % pression · ' +
      '<a href="' + unsubLink + '" style="color:#9ca3af;">Se désinscrire</a>' +
      '</p>';

    if (day === 0) {
      subject  = 'Bienvenue sur Matheux, ' + prenom + ' ! 🎯';
      htmlBody =
        '<div style="max-width:500px;margin:0 auto;font-family:sans-serif;background:#ffffff;padding:32px 24px;border-radius:12px;">' +
        '<h1 style="color:#4338ca;font-size:24px;margin-bottom:8px;">Bienvenue, ' + prenom + ' !</h1>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">On est vraiment contents de vous accueillir sur Matheux.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">L\'objectif est simple : avancer à votre rythme, sans pression, en comprenant vraiment les notions — pas en les apprenant par cœur.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">Cette semaine, ' + prenom + ' va passer un petit diagnostic (8 questions), et l\'application va adapter les exercices à son niveau exact. Aucun jugement, aucune mauvaise réponse définitive.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;"><strong>Pour commencer :</strong> connectez-vous sur <a href="https://matheux.fr" style="color:#4338ca;">matheux.fr</a> et suivez le guide.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">Si vous avez la moindre question, répondez simplement à cet email.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">À très vite,<br><strong>Nicolas</strong><br><span style="color:#6b7280;font-size:14px;">Prof de maths & fondateur de Matheux</span></p>' +
        footer + '</div>';

    } else if (day === 3) {
      subject  = 'Comment ça se passe pour ' + prenom + ' ? 💪';
      htmlBody =
        '<div style="max-width:500px;margin:0 auto;font-family:sans-serif;background:#ffffff;padding:32px 24px;border-radius:12px;">' +
        '<h1 style="color:#4338ca;font-size:24px;margin-bottom:8px;">3 jours déjà !</h1>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">Bonjour,</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">Cela fait 3 jours que ' + prenom + ' a rejoint Matheux. On espère que les premiers exercices se passent bien.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">Pas d\'inquiétude si certaines notions semblent difficiles — c\'est normal, c\'est même l\'objectif : identifier ce qui accroche pour mieux le travailler.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;"><strong>Petit rappel :</strong> le boost quotidien (5 exercices, ~10 minutes) est la clé. Régulier vaut mieux qu\'intense.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">N\'hésitez pas à me faire un retour — un simple "ça va bien" ou "on galère sur les fractions" suffit. Je lis tous les messages.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">Bon courage,<br><strong>Nicolas</strong></p>' +
        footer + '</div>';

    } else if (day === 7) {
      subject  = 'Bilan de la semaine de ' + prenom + ' ⭐';
      htmlBody =
        '<div style="max-width:500px;margin:0 auto;font-family:sans-serif;background:#ffffff;padding:32px 24px;border-radius:12px;">' +
        '<h1 style="color:#4338ca;font-size:24px;margin-bottom:8px;">Une semaine avec Matheux !</h1>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">Bonjour,</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">La première semaine de ' + prenom + ' sur Matheux touche à sa fin. C\'est déjà beaucoup — le simple fait de commencer, c\'est 90 % du travail.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">En une semaine, ' + prenom + ' a :</p>' +
        '<ul style="color:#374151;font-size:16px;line-height:1.8;padding-left:20px;">' +
        '<li>Identifié ses points forts et ses points à renforcer</li>' +
        '<li>Travaillé avec des exercices adaptés à son niveau</li>' +
        '<li>Posé des bases solides pour la suite</li>' +
        '</ul>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">Pour continuer sur cette lancée, vous pouvez <a href="https://matheux.fr" style="color:#4338ca;font-weight:bold;">activer l\'abonnement</a> — 9,99 €/mois, sans engagement, résiliable à tout moment.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">Si vous avez des questions avant de décider, répondez à cet email — je suis là.</p>' +
        '<p style="color:#374151;font-size:16px;line-height:1.6;">Merci pour votre confiance,<br><strong>Nicolas</strong></p>' +
        footer + '</div>';

    } else {
      return { status: 'error', message: 'Jour invalide : ' + day + '. Valeurs acceptées : 0, 3, 7.' };
    }

    MailApp.sendEmail({ to: email, subject: subject, htmlBody: htmlBody });
    return { status: 'success' };

  } catch (err) {
    return { status: 'error', message: err.toString() };
  }
}

/**
 * Trigger Apps Script — à appeler chaque jour à 9h-10h.
 * Configuration : Apps Script UI → Déclencheurs → triggerDailyMarketing → Chaque jour → 9h-10h
 *
 * Pour chaque utilisateur avec TrialStart rempli et Premium != true,
 * envoie l'email marketing du bon jour (0, 3 ou 7).
 */
function triggerDailyMarketing() {
  var sh      = getSheet(SH.USERS);
  var data    = sh.getDataRange().getValues();
  if (data.length <= 1) return;

  var headers    = data[0];
  var iCode      = headers.indexOf('Code');
  var iPrenom    = headers.indexOf('Prénom');
  var iEmail     = headers.indexOf('Email');
  var iPremium   = headers.indexOf('Premium');
  var iTrialStart = headers.indexOf('TrialStart');

  if (iTrialStart === -1) return; // colonne absente → rien à faire

  var today_    = new Date();
  today_.setHours(0, 0, 0, 0);

  for (var i = 1; i < data.length; i++) {
    var row        = data[i];
    var email      = String(row[iEmail] || '').trim();
    var prenom     = String(row[iPrenom] || '').trim();
    var premium    = row[iPremium];
    var trialStart = row[iTrialStart];

    if (!email || !trialStart) continue;
    if (premium === true || premium === 1 || premium === 'TRUE' || premium === 'true') continue;

    var startDate = new Date(trialStart);
    startDate.setHours(0, 0, 0, 0);
    if (isNaN(startDate.getTime())) continue;

    var diffMs   = today_ - startDate;
    var diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0 || diffDays === 3 || diffDays === 7) {
      try {
        sendMarketingSequence(email, prenom, diffDays);
      } catch (e) {
        Logger.log('triggerDailyMarketing error for ' + email + ' : ' + e.toString());
      }
    }
  }
}

/**
 * Action GAS — check_trial_status
 * Payload : { code }
 * Réponse : { status:'success', trialActive: bool, daysLeft: number, isPremium: bool }
 */
function checkTrialStatus(p) {
  var code = (p.code || '').trim();
  if (!code) return { status: 'error', message: 'Code requis.' };

  var sh     = getSheet(SH.USERS);
  var data   = sh.getDataRange().getValues();
  if (data.length <= 1) return { status: 'error', message: 'Utilisateur introuvable.' };

  var headers     = data[0];
  var iCode       = headers.indexOf('Code');
  var iPremium    = headers.indexOf('Premium');
  var iTrialStart = headers.indexOf('TrialStart');

  var userRow = null;
  for (var i = 1; i < data.length; i++) {
    if (String(data[i][iCode]) === code) { userRow = data[i]; break; }
  }
  if (!userRow) return { status: 'error', message: 'Utilisateur introuvable.' };

  var premium    = userRow[iPremium];
  var isPremium  = (premium === true || premium === 1 || premium === 'TRUE' || premium === 'true');

  var trialActive = false;
  var daysLeft    = 0;

  if (iTrialStart !== -1) {
    var trialStart = userRow[iTrialStart];
    if (trialStart) {
      var startDate = new Date(trialStart);
      startDate.setHours(0, 0, 0, 0);
      var now_ = new Date();
      now_.setHours(0, 0, 0, 0);
      var diffDays = Math.round((now_ - startDate) / (1000 * 60 * 60 * 24));
      trialActive  = diffDays < 8;
      daysLeft     = Math.max(0, 7 - diffDays);
    }
  }

  return { status: 'success', trialActive: trialActive, daysLeft: daysLeft, isPremium: isPremium };
}
