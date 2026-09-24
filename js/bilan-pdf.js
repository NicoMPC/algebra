/**
 * Matheux — générateur du PDF « Bilan de compétences maths 3e » (destiné au parent).
 *
 *   window.MatheuxBilanPDF.render(carte, opts) → Promise<{ blob, url, fileName, pageCount }>
 *
 * `carte` = objet Carte du contrat commun (docs/specs/00-contrat-commun.md §5).
 * Contrat détaillé, options et limites : docs/specs/30-pdf.md.
 *
 * Vanilla JS, pas d'import ES, pas de bundler. jsPDF (UMD) est chargé depuis jsdelivr
 * s'il n'est pas déjà présent (window.jspdf). Architecture portée du moteur HUMANA :
 * dessin bloc par bloc dans un état { y }, saut de page via ensureSpace, chrome
 * (en-tête / pied de page) redessiné par page, polices TTF injectées dans le VFS jsPDF.
 *
 * Polices : Syne Bold + DM Sans (Regular / SemiBold / Bold), instances statiques
 * sous-ensemblées (latin + symboles maths) dans js/bilan-pdf-assets/. Si elles ne
 * peuvent pas être chargées (file://, réseau), fallback Helvetica avec translittération
 * des caractères hors WinAnsi (−, ≤, →…) : les accents français restent corrects.
 */
(function (global) {
  'use strict';

  var VERSION = '1.0.0';
  var JSPDF_URL = 'https://cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js';

  // Dossier du script (pour trouver bilan-pdf-assets/ quel que soit l'emplacement de la page)
  var SCRIPT_BASE = (function () {
    try {
      var s = global.document && global.document.currentScript && global.document.currentScript.src;
      return s ? s.replace(/[^/]*$/, '') : '';
    } catch (e) { return ''; }
  })();

  /* ───────────────────────── Charte ───────────────────────── */

  var C = {
    navy: '#0F172A', ink: '#1E293B', ink2: '#334155', mut: '#64748B', mut2: '#94A3B8',
    brd: '#E2E8F0', bg: '#F8FAFC', p: '#1E40AF', pl: '#EEF2FF', pm: '#C7D2FE', white: '#FFFFFF',
  };
  var STATUS = {
    lacune: { c: '#DC2626', l: '#FEE2E2', d: '#991B1B', label: 'Lacune', plural: 'lacunes' },
    fragile: { c: '#F59E0B', l: '#FEF3C7', d: '#92400E', label: 'Fragile', plural: 'fragiles' },
    acquis: { c: '#059669', l: '#D1FAE5', d: '#065F46', label: 'Acquis', plural: 'acquises' },
    non_evalue: { c: '#94A3B8', l: '#F1F5F9', d: '#475569', label: 'Non évalué', plural: 'non évaluées' },
  };
  var STATUS_ORDER = { lacune: 0, fragile: 1, acquis: 2, non_evalue: 3 };
  var DOMAINES = {
    NC: 'Nombres et calculs',
    DF: 'Données, statistiques et fonctions',
    GM: 'Grandeurs et mesures',
    EG: 'Espace et géométrie',
    AP: 'Algorithmique et programmation',
  };
  var DOMAINE_ORDER = ['NC', 'DF', 'GM', 'EG', 'AP'];
  var NIVEAUX = { '6EME': '6e', '5EME': '5e', '4EME': '4e', '3EME': '3e' };
  var MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août',
    'septembre', 'octobre', 'novembre', 'décembre'];

  var PAGE = { w: 210, h: 297 };
  var M = { x0: 18, x1: 192 };
  var CW = M.x1 - M.x0; // 174
  var CONTENT_TOP = 30;
  var BOTTOM = 277;
  var PT = 0.352778; // mm par point typographique

  /* ───────────────────────── Chargement ───────────────────────── */

  var jspdfPromise = null;
  function loadJsPDF(url) {
    if (global.jspdf && global.jspdf.jsPDF) return Promise.resolve(global.jspdf.jsPDF);
    if (!jspdfPromise) {
      jspdfPromise = new Promise(function (resolve, reject) {
        var s = global.document.createElement('script');
        s.src = url || JSPDF_URL;
        s.onload = function () {
          if (global.jspdf && global.jspdf.jsPDF) resolve(global.jspdf.jsPDF);
          else reject(new Error('jsPDF chargé mais introuvable'));
        };
        s.onerror = function () { jspdfPromise = null; reject(new Error('Impossible de charger jsPDF')); };
        global.document.head.appendChild(s);
      });
    }
    return jspdfPromise;
  }

  function bufToBase64(buffer) {
    var bytes = new Uint8Array(buffer), bin = '', chunk = 0x8000;
    for (var i = 0; i < bytes.length; i += chunk) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
    return global.btoa(bin);
  }
  function fetchBase64(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error(url + ' (' + r.status + ')');
      return r.arrayBuffer();
    }).then(bufToBase64);
  }

  var FONT_FILES = [
    { file: 'Syne-Bold.ttf', family: 'Syne', style: 'bold' },
    { file: 'DMSans-Regular.ttf', family: 'DMSans', style: 'normal' },
    { file: 'DMSans-SemiBold.ttf', family: 'DMSans', style: 'semibold' },
    { file: 'DMSans-Bold.ttf', family: 'DMSans', style: 'bold' },
  ];
  var assetCache = {};
  function loadAssets(opts) {
    var base = opts.assetBase || (SCRIPT_BASE + 'bilan-pdf-assets/');
    if (assetCache[base]) return assetCache[base];
    var load = opts.loadAsset || function (f) { return fetchBase64(base + f); };
    var fonts = Promise.all(FONT_FILES.map(function (f) {
      return load(f.file).then(function (b64) { return { file: f.file, family: f.family, style: f.style, b64: b64 }; });
    })).catch(function (e) {
      if (global.console) console.warn('[MatheuxBilanPDF] polices indisponibles, fallback Helvetica :', e.message);
      return null;
    });
    var img = function (f) { return load(f).then(function (b) { return 'data:image/png;base64,' + b; }).catch(function () { return null; }); };
    var p = Promise.all([fonts, img('logo.png'), img('logo-m.png')]).then(function (r) {
      return { fonts: r[0], logo: r[1], logoM: r[2] };
    });
    assetCache[base] = p;
    p.then(function (a) { if (!a.fonts) delete assetCache[base]; }); // retente au prochain rendu
    return p;
  }

  /* ───────────────────────── Helpers de dessin ───────────────────────── */

  function rgb(hex) {
    var h = hex.replace('#', '');
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  }
  function fill(doc, hex) { var c = rgb(hex); doc.setFillColor(c[0], c[1], c[2]); }
  function stroke(doc, hex) { var c = rgb(hex); doc.setDrawColor(c[0], c[1], c[2]); }
  function color(doc, hex) { var c = rgb(hex); doc.setTextColor(c[0], c[1], c[2]); }

  // Fallback Helvetica (WinAnsi) : on translittère ce qui n'existe pas dans l'encodage.
  var ASCII_MAP = {
    '−': '-', '≤': '<=', '≥': '>=', '≠': '=/=', '≈': '~', 'π': 'pi', '→': '->', '←': '<-',
    '′': "'", '″': '"', '√': 'racine',
  };
  // Typo française : espace insécable (U+00A0, présente dans les deux jeux de polices)
  // à l'intérieur des guillemets et avant : ; ! ? % — évite un « » ou un : orphelin en fin de ligne.
  function clean(ctx, s) {
    s = String(s == null ? '' : s).replace(/\u202F/g, '\u00A0')
      .replace(/« /g, '«\u00A0').replace(/ »/g, '\u00A0»').replace(/ ([:;!?%])/g, '\u00A0$1');
    if (ctx.hasFonts) return s;
    return s.replace(/[−≤≥≠≈π→←′″√]/g, function (ch) { return ASCII_MAP[ch]; });
  }

  // Rôles typographiques : title (Syne), body / semi / bold (DM Sans)
  function font(ctx, role, size) {
    var d = ctx.doc;
    if (ctx.hasFonts) {
      if (role === 'title') d.setFont('Syne', 'bold');
      else d.setFont('DMSans', role === 'semi' ? 'semibold' : role === 'bold' ? 'bold' : 'normal');
    } else {
      d.setFont('helvetica', role === 'body' ? 'normal' : 'bold');
    }
    d.setFontSize(size);
  }
  function tw(ctx, s) { return ctx.doc.getTextWidth(clean(ctx, s)); }
  function txt(ctx, s, x, y, o) { ctx.doc.text(clean(ctx, s), x, y, o || {}); }
  function wrap(ctx, s, w) { return ctx.doc.splitTextToSize(clean(ctx, s), w); }

  /** Paragraphe simple (sans maths). Renvoie le y sous la dernière ligne. */
  function para(ctx, s, x, y, w, o) {
    o = o || {};
    var size = o.size || 9.5;
    font(ctx, o.role || 'body', size);
    color(ctx.doc, o.color || C.ink2);
    var lh = o.lh || size * PT * 1.45;
    var lines = wrap(ctx, s, w);
    if (o.max && lines.length > o.max) { lines = lines.slice(0, o.max); lines[o.max - 1] = lines[o.max - 1].replace(/\s*\S*$/, '') + '…'; }
    lines.forEach(function (l, i) {
      txt(ctx, l, o.align === 'center' ? x + w / 2 : o.align === 'right' ? x + w : x, y + size * PT * 0.78 + i * lh, { align: o.align || 'left' });
    });
    return y + lines.length * lh;
  }
  function paraH(ctx, s, w, o) {
    o = o || {};
    var size = o.size || 9.5;
    font(ctx, o.role || 'body', size);
    var n = wrap(ctx, s, w).length;
    if (o.max) n = Math.min(n, o.max);
    return n * (o.lh || size * PT * 1.45);
  }

  function spaced(ctx, s, x, y, sp, align) {
    var d = ctx.doc, str = clean(ctx, s);
    d.setCharSpace(sp);
    var w = d.getTextWidth(str) + sp * Math.max(0, str.length - 1);
    var dx = align === 'right' ? x - w : align === 'center' ? x - w / 2 : x;
    d.text(str, dx, y);
    d.setCharSpace(0);
    return w;
  }
  function eyebrow(ctx, s, x, y, col, size) {
    font(ctx, 'bold', size || 7.4);
    color(ctx.doc, col || C.p);
    return spaced(ctx, s.toUpperCase(), x, y, 0.45);
  }

  function statusKey(s) {
    s = String(s || '').toLowerCase().replace(/[éè]/g, 'e').replace(/[\s-]/g, '_');
    if (s.indexOf('lacun') === 0) return 'lacune';
    if (s.indexOf('fragil') === 0) return 'fragile';
    if (s.indexOf('acqui') === 0) return 'acquis';
    return 'non_evalue';
  }
  function statusFromMaitrise(m) {
    if (m == null || isNaN(m)) return 'non_evalue';
    return m < 0.4 ? 'lacune' : m <= 0.7 ? 'fragile' : 'acquis';
  }

  /** Pastille de statut (remplace les emoji 🔴🟠🟢⚪). */
  function pastille(ctx, st, x, y, r) {
    var d = ctx.doc, S = STATUS[st] || STATUS.non_evalue;
    r = r || 1.5;
    if (st === 'non_evalue') {
      fill(d, C.white); stroke(d, S.c); d.setLineWidth(0.45);
      d.circle(x, y, r - 0.2, 'FD');
    } else {
      fill(d, S.c); d.circle(x, y, r, 'F');
    }
  }
  /** Petite étiquette pleine (ex. « CAUSE RACINE »). Renvoie sa largeur. */
  function tag(ctx, label, x, y, bgHex, fgHex, o) {
    o = o || {};
    var d = ctx.doc, size = o.size || 6, s = label.toUpperCase();
    font(ctx, 'bold', size);
    var w = tw(ctx, s) + 0.3 * (s.length - 1) + 3.2, h = size * PT + 2;
    var x0 = o.align === 'right' ? x - w : x;
    fill(d, bgHex);
    if (o.outline) { stroke(d, o.outline); d.setLineWidth(0.3); d.roundedRect(x0, y - h / 2, w, h, h / 2, h / 2, 'FD'); } else d.roundedRect(x0, y - h / 2, w, h, h / 2, h / 2, 'F');
    color(d, fgHex);
    spaced(ctx, s, x0 + 1.6, y + size * PT * 0.36, 0.3);
    return w;
  }
  function check(ctx, x, y, r, hex) { // rond + coche
    var d = ctx.doc; fill(d, hex); d.circle(x, y, r, 'F');
    stroke(d, C.white); d.setLineWidth(r * 0.28); d.setLineCap('round'); d.setLineJoin('round');
    d.lines([[r * 0.35, r * 0.35], [r * 0.7, -r * 0.8]], x - r * 0.5, y + r * 0.02, [1, 1], 'S', false);
    d.setLineCap('butt');
  }
  function cross(ctx, x, y, r, hex) {
    var d = ctx.doc; fill(d, hex); d.circle(x, y, r, 'F');
    stroke(d, C.white); d.setLineWidth(r * 0.28); d.setLineCap('round');
    var k = r * 0.42;
    d.line(x - k, y - k, x + k, y + k); d.line(x - k, y + k, x + k, y - k);
    d.setLineCap('butt');
  }
  function bar(ctx, x, y, w, h, ratio, hex, track) {
    var d = ctx.doc;
    fill(d, track || C.brd); d.roundedRect(x, y, w, h, h / 2, h / 2, 'F');
    if (ratio > 0) { fill(d, hex); d.roundedRect(x, y, Math.max(h, w * Math.min(1, ratio)), h, h / 2, h / 2, 'F'); }
  }
  function arc(ctx, cx, cy, r, a0, a1, lw, hex) { // angles en radians, 0 = haut, sens horaire
    var d = ctx.doc, n = Math.max(8, Math.ceil(Math.abs(a1 - a0) / 0.05));
    var pts = [], i, px = cx + r * Math.sin(a0), py = cy - r * Math.cos(a0);
    for (i = 1; i <= n; i++) {
      var a = a0 + (a1 - a0) * i / n, nx = cx + r * Math.sin(a), ny = cy - r * Math.cos(a);
      pts.push([nx - px, ny - py]); px = nx; py = ny;
    }
    stroke(d, hex); d.setLineWidth(lw); d.setLineCap('round');
    d.lines(pts, cx + r * Math.sin(a0), cy - r * Math.cos(a0), [1, 1], 'S', false);
    d.setLineCap('butt');
  }

  /* ───────────────────────── Mini-moteur maths (sans KaTeX) ─────────────────────────
   * Sous-ensemble LaTeX : \frac \dfrac \sqrt ^ _ \times \div \cdot \le \ge \neq \approx \pi
   * \text \widehat \overline \vec \left \right \, \; \quad … Les fractions sont empilées,
   * les racines et chapeaux dessinés au trait, les puissances en exposant. */

  var SYM = {
    times: '×', div: '÷', cdot: '·', le: '≤', leq: '≤', leqslant: '≤', ge: '≥', geq: '≥', geqslant: '≥',
    neq: '≠', ne: '≠', approx: '≈', pi: 'π', pm: '±', degree: '°', circ: '°', ldots: '…', dots: '…',
    cdots: '…', rightarrow: '→', Rightarrow: '→', to: '→', '%': '%', '{': '{', '}': '}', '$': '$',
    '&': '&', '#': '#', '_': '_', lbrace: '{', rbrace: '}', lt: '<', gt: '>', prime: '′',
  };
  var SPACES = { ',': 0.17, ';': 0.28, ':': 0.22, ' ': 0.25, quad: 1, qquad: 2, '!': 0 };
  var OPS = '+−×÷=≤≥≈≠<>±→';
  var TEXTCMD = { text: 1, mathrm: 1, textbf: 1, mbox: 1, operatorname: 1, textit: 1, mathbf: 1, mathit: 1, textrm: 1 };
  var ACCENTS = { widehat: 1, hat: 1, overline: 1, vec: 1, overrightarrow: 1, bar: 1 };

  function parseTex(src) {
    var i = 0;
    function ws() { while (i < src.length && /\s/.test(src[i])) i++; }
    function name() {
      var s = i;
      if (/[a-zA-Z]/.test(src[i] || '')) { while (i < src.length && /[a-zA-Z]/.test(src[i])) i++; } else i++;
      return src.slice(s, i);
    }
    function raw() {
      ws();
      if (src[i] !== '{') return src[i++] || '';
      var depth = 1, s = ++i;
      while (i < src.length && depth) { if (src[i] === '{') depth++; else if (src[i] === '}') depth--; i++; }
      return src.slice(s, i - 1);
    }
    function atom() {
      ws();
      if (src[i] === '{') { i++; return seq('}'); }
      if (src[i] === '\\') { var o = []; cmd(o); return o; }
      if (i >= src.length) return [];
      return [chr(src[i++])];
    }
    function chr(c) {
      if (c === '-') c = '−';
      if (c === '*') c = '×';
      return OPS.indexOf(c) >= 0 ? { t: 'op', s: c } : { t: 'txt', s: c };
    }
    function cmd(out) {
      i++;
      var n = name();
      if (n === 'frac' || n === 'dfrac' || n === 'tfrac') { var a = atom(); out.push({ t: 'frac', n: a, d: atom() }); return; }
      if (n === 'sqrt') { ws(); if (src[i] === '[') { while (i < src.length && src[i] !== ']') i++; i++; } out.push({ t: 'sqrt', b: atom() }); return; }
      if (TEXTCMD[n]) { out.push({ t: 'txt', s: raw().replace(/\\/g, ''), keep: true }); return; }
      if (ACCENTS[n]) { out.push({ t: 'acc', k: n, b: atom() }); return; }
      if (n === 'left' || n === 'right') {
        ws();
        var dl = src[i];
        if (dl === '\\') { i++; dl = name(); dl = dl === '{' || dl === 'lbrace' ? '{' : dl === '}' || dl === 'rbrace' ? '}' : dl === '|' ? '|' : ''; } else i++;
        if (dl && dl !== '.') out.push({ t: 'txt', s: dl });
        return;
      }
      if (SPACES[n] != null) { out.push({ t: 'sp', w: SPACES[n] }); return; }
      if (SYM[n]) { var s = SYM[n]; out.push(OPS.indexOf(s) >= 0 ? { t: 'op', s: s } : { t: 'txt', s: s }); return; }
      if (n === '\\') { out.push({ t: 'sp', w: 0.4 }); return; }
      out.push({ t: 'txt', s: n, fn: true }); // cos, sin, tan, ln… en romain
    }
    function seq(end) {
      var out = [];
      while (i < src.length) {
        var c = src[i];
        if (end && c === end) { i++; return out; }
        if (/\s/.test(c)) { i++; continue; }
        if (c === '{') { i++; out.push({ t: 'grp', b: seq('}') }); continue; }
        if (c === '}') { i++; continue; }
        if (c === '^' || c === '_') {
          i++;
          var b = atom();
          if (c === '^' && b.length === 1 && b[0].s === '°') out.push({ t: 'txt', s: '°' });
          else out.push({ t: c === '^' ? 'sup' : 'sub', b: b });
          continue;
        }
        if (c === '\\') { cmd(out); continue; }
        i++;
        out.push(chr(c));
      }
      return out;
    }
    return seq(null);
  }

  function hbox(boxes) {
    var w = 0, a = 0, d = 0;
    boxes.forEach(function (b) { w += b.w; a = Math.max(a, b.a); d = Math.max(d, b.d); });
    return {
      w: w, a: a, d: d, boxes: boxes,
      draw: function (ctx, x, y, col) { boxes.forEach(function (b) { b.draw(ctx, x, y, col); x += b.w; }); },
    };
  }

  function layMath(ctx, nodes, size) {
    var E = size * PT, boxes = [], list = [];
    nodes.forEach(function (n) {
      var last = list[list.length - 1];
      if (n.t === 'txt' && last && last.t === 'txt' && !n.fn && !last.fn) list[list.length - 1] = { t: 'txt', s: last.s + n.s, keep: last.keep || n.keep };
      else list.push(n);
    });
    list.forEach(function (n, k) {
      var prev = boxes[boxes.length - 1];
      if (n.t === 'txt') {
        var s = n.s;
        if (n.fn && list[k + 1] && list[k + 1].t !== 'op' && list[k + 1].t !== 'sup') s += ' '; // « cos x »
        boxes.push(textBox(ctx, s, size));
      } else if (n.t === 'op') {
        var unary = (n.s === '−' || n.s === '+' || n.s === '±') && (!prev || prev.isOp || prev.open);
        var pad = unary ? 0.02 * E : (n.s === '=' || n.s === '≤' || n.s === '≥' || n.s === '≈' || n.s === '≠' || n.s === '→' ? 0.28 : 0.22) * E;
        var ob = textBox(ctx, n.s, size);
        var w0 = ob.w;
        boxes.push({
          w: w0 + 2 * pad, a: ob.a, d: ob.d, isOp: !unary,
          draw: function (c, x, y, col) { ob.draw(c, x + pad, y, col); },
        });
      } else if (n.t === 'sp') {
        boxes.push({ w: n.w * E, a: 0, d: 0, draw: function () {} });
      } else if (n.t === 'grp') {
        boxes.push(layMath(ctx, n.b, size));
      } else if (n.t === 'frac') {
        boxes.push(fracBox(ctx, n, size));
      } else if (n.t === 'sqrt') {
        boxes.push(sqrtBox(ctx, n, size));
      } else if (n.t === 'sup' || n.t === 'sub') {
        var sb = layMath(ctx, n.b, Math.max(5.5, size * 0.68));
        if (n.t === 'sup') {
          var shift = Math.max(0.4 * E, (prev ? prev.a : 0.72 * E) - sb.a * 0.55);
          boxes.push({ w: sb.w + 0.05 * E, a: shift + sb.a, d: Math.max(0, sb.d - shift),
            draw: function (c, x, y, col) { sb.draw(c, x + 0.03 * E, y - shift, col); } });
        } else {
          var sh = 0.2 * E;
          boxes.push({ w: sb.w + 0.05 * E, a: Math.max(0, sb.a - sh), d: sh + sb.d,
            draw: function (c, x, y, col) { sb.draw(c, x + 0.03 * E, y + sh, col); } });
        }
      } else if (n.t === 'acc') {
        boxes.push(accBox(ctx, n, size));
      }
    });
    return hbox(boxes);
  }

  function textBox(ctx, s, size) {
    var E = size * PT;
    font(ctx, 'body', size);
    var str = clean(ctx, s), w = ctx.doc.getTextWidth(str);
    return {
      w: w, a: 0.72 * E, d: 0.22 * E, open: /[([]$/.test(s),
      draw: function (c, x, y, col) { font(c, 'body', size); color(c.doc, col); c.doc.text(str, x, y); },
    };
  }
  function fracBox(ctx, n, size) {
    var E = size * PT, cs = Math.max(6.5, size * 0.84);
    var nb = layMath(ctx, n.n, cs), db = layMath(ctx, n.d, cs);
    var axis = 0.29 * E, gap = 0.16 * E, th = Math.max(0.2, 0.055 * E), side = 0.12 * E;
    var inner = Math.max(nb.w, db.w) + 0.14 * E, w = inner + 2 * side;
    return {
      w: w, a: axis + gap + nb.d + nb.a, d: gap + db.a + db.d - axis,
      draw: function (c, x, y, col) {
        var d = c.doc;
        nb.draw(c, x + side + (inner - nb.w) / 2, y - axis - gap - nb.d, col);
        db.draw(c, x + side + (inner - db.w) / 2, y - axis + gap + db.a, col);
        stroke(d, col); d.setLineWidth(th);
        d.line(x + side, y - axis, x + side + inner, y - axis);
      },
    };
  }
  function sqrtBox(ctx, n, size) {
    var E = size * PT, bb = layMath(ctx, n.b, size);
    var a = bb.a + 0.16 * E, rw = 0.55 * E, w = rw + bb.w + 0.12 * E;
    return {
      w: w, a: a, d: Math.max(bb.d, 0.1 * E),
      draw: function (c, x, y, col) {
        var d = c.doc;
        stroke(d, col); d.setLineWidth(Math.max(0.2, 0.055 * E)); d.setLineJoin('round');
        var top = y - a + 0.03 * E;
        // trait d'attaque, descente jusqu'à la ligne de base, remontée, barre horizontale
        d.lines([[0.12 * E, -0.06 * E], [0.15 * E, 0.44 * E], [0.24 * E, top - (y + 0.04 * E)], [w - 0.53 * E, 0]],
          x + 0.02 * E, y - 0.34 * E, [1, 1], 'S', false);
        bb.draw(c, x + rw, y, col);
      },
    };
  }
  function accBox(ctx, n, size) {
    var E = size * PT, bb = layMath(ctx, n.b, size), up = 0.26 * E;
    return {
      w: bb.w + 0.06 * E, a: bb.a + up, d: bb.d,
      draw: function (c, x, y, col) {
        var d = c.doc, top = y - bb.a - 0.06 * E;
        bb.draw(c, x + 0.03 * E, y, col);
        stroke(d, col); d.setLineWidth(Math.max(0.18, 0.05 * E)); d.setLineJoin('round');
        if (n.k === 'widehat' || n.k === 'hat') {
          d.lines([[bb.w / 2, -up + 0.06 * E], [bb.w / 2, up - 0.06 * E]], x + 0.03 * E, top, [1, 1], 'S', false);
        } else {
          d.line(x + 0.03 * E, top - 0.08 * E, x + bb.w + 0.03 * E, top - 0.08 * E);
          if (n.k === 'vec' || n.k === 'overrightarrow') {
            var ex = x + bb.w + 0.03 * E, ey = top - 0.08 * E;
            d.line(ex, ey, ex - 0.14 * E, ey - 0.09 * E); d.line(ex, ey, ex - 0.14 * E, ey + 0.09 * E);
          }
        }
      },
    };
  }

  /** Texte « élève » brut → texte riche : 7/12 → $\frac{7}{12}$, x^2, sqrt(25)… */
  function plainToRich(s) {
    s = String(s == null ? '' : s).trim();
    if (!s || s.indexOf('$') >= 0) return s;
    var looksMath = /^[\s\d.,+\-−×*÷/^()=<>≤≥√πa-zA-Z]*$/.test(s) && !/[a-zA-ZÀ-ÿ]{3,}/.test(s.replace(/sqrt/g, ''));
    var t = s
      .replace(/sqrt\s*\(([^)]*)\)/g, '\\sqrt{$1}')
      .replace(/√\s*\(([^)]*)\)/g, '\\sqrt{$1}')
      .replace(/√\s*(\d+)/g, '\\sqrt{$1}')
      .replace(/\(([^()]+)\)\s*\/\s*\(([^()]+)\)/g, '\\frac{$1}{$2}')
      .replace(/(\d+(?:[.,]\d+)?)\s*\/\s*(\d+(?:[.,]\d+)?)/g, '\\frac{$1}{$2}')
      .replace(/\^\s*\(([^)]*)\)/g, '^{$1}')
      .replace(/\^\s*(−?-?\d+)/g, '^{$1}');
    if (looksMath) return '$' + t.replace(/(\d)\s*(cm|mm|dm|km|m|kg|g|mL|cL|L|min|h|s)(²|³)?$/, '$1\\,\\text{$2$3}') + '$';
    // texte courant : on n'isole que les fragments mathématiques
    return t.replace(/(\S*\\(?:frac|sqrt)\{[^$]*?\}(?:\{[^}]*\})?\S*|\S+\^\{[^}]*\}\S*)/g, function (m) {
      var trail = /[.,;:!?)]$/.test(m) ? m.slice(-1) : '';
      return '$' + (trail ? m.slice(0, -1) : m) + '$' + trail;
    });
  }

  /** Mise en page d'un paragraphe mêlant texte et maths ($…$). */
  function richLayout(ctx, str, width, o) {
    o = o || {};
    var size = o.size || 9.5, role = o.role || 'body', E = size * PT;
    var LH = o.lh || size * PT * 1.45;
    var parts = String(str == null ? '' : str).split(/(\$[^$]*\$)/);
    var items = [], pendingSpace = false;
    font(ctx, role, size);
    var spaceW = tw(ctx, ' ');
    parts.forEach(function (p) {
      if (!p) return;
      if (p[0] === '$' && p[p.length - 1] === '$' && p.length > 1) {
        var box = layMath(ctx, parseTex(p.slice(1, -1)), size);
        items.push({ m: box, w: box.w, sp: pendingSpace });
        pendingSpace = false;
      } else {
        font(ctx, role, size);
        clean(ctx, p).split(/([ \t\n]+)/).forEach(function (wd) {
          if (!wd) return;
          if (/^[ \t\n]+$/.test(wd)) { pendingSpace = true; return; }
          font(ctx, role, size);
          items.push({ s: wd, w: tw(ctx, wd), sp: pendingSpace });
          pendingSpace = false;
        });
      }
    });
    var lines = [], cur = null;
    items.forEach(function (it) {
      var add = (cur && cur.items.length && it.sp ? spaceW : 0) + it.w;
      if (!cur || (cur.items.length && cur.w + add > width)) { cur = { items: [], w: 0 }; lines.push(cur); add = it.w; }
      cur.items.push(it); cur.w += add;
    });
    var h = 0;
    lines.forEach(function (l) {
      l.a = 0.74 * E; l.d = 0.24 * E;
      l.items.forEach(function (it) { if (it.m) { l.a = Math.max(l.a, it.m.a); l.d = Math.max(l.d, it.m.d); } });
      l.h = Math.max(LH, l.a + l.d + 0.36 * E);
      h += l.h;
    });
    return { lines: lines, h: h, w: lines.reduce(function (m, l) { return Math.max(m, l.w); }, 0), size: size, role: role, spaceW: spaceW, width: width };
  }
  function richDraw(ctx, L, x, y, o) {
    o = o || {};
    var col = o.color || C.ink2;
    L.lines.forEach(function (l) {
      var base = y + (l.h - (l.a + l.d)) / 2 + l.a;
      var cx = o.align === 'center' ? x + (L.width - l.w) / 2 : x;
      l.items.forEach(function (it, k) {
        if (k && it.sp) cx += L.spaceW;
        if (it.m) it.m.draw(ctx, cx, base, col);
        else { font(ctx, L.role, L.size); color(ctx.doc, col); txt(ctx, it.s, cx, base); }
        cx += it.w;
      });
      y += l.h;
    });
    return y;
  }

  /* ───────────────────────── Données dérivées ───────────────────────── */

  function prepare(carte, opts) {
    var comps = (carte.competences || []).map(function (c) {
      var st = c.statut ? statusKey(c.statut) : statusFromMaitrise(c.maitrise);
      return Object.assign({}, c, { st: st, dom: c.domaine || String(c.id || '').split('.')[0] });
    });
    var byId = {};
    comps.forEach(function (c) { byId[c.id] = c; });
    var count = { lacune: 0, fragile: 0, acquis: 0, non_evalue: 0 };
    comps.forEach(function (c) { count[c.st]++; });
    var roots = comps.filter(function (c) { return c.cause_racine && (c.bloque || []).length; })
      .sort(function (a, b) { return (b.bloque.length - a.bloque.length) || ((a.maitrise || 0) - (b.maitrise || 0)); });
    var prenom = (carte.eleve && carte.eleve.prenom) || 'votre enfant';
    var nq = carte.n_questions || 0;
    return {
      carte: carte, comps: comps, byId: byId, count: count, roots: roots, prenom: prenom,
      niveau: NIVEAUX[(carte.eleve && carte.eleve.niveau) || '3EME'] || '3e',
      dateLong: dateLong(carte.date), nq: nq,
    };
  }
  function title(c) { return (c && (c.titre || c.titre_eleve)) || (c && c.id) || ''; }
  function compOrStub(D, id) {
    return D.byId[id] || { id: id, titre: id, st: 'non_evalue', dom: String(id).split('.')[0] };
  }
  function dateLong(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || '');
    if (!m) return iso || '';
    return (+m[3] === 1 ? '1er' : String(+m[3])) + ' ' + MOIS[+m[2] - 1] + ' ' + m[1];
  }
  function pl(n, one, many) { return n + ' ' + (n > 1 ? many : one); }
  function pct(m) { return m == null || isNaN(m) ? '—' : Math.round(m * 100) + ' %'; }
  function slug(s) {
    return String(s || 'eleve').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Za-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'eleve';
  }
  function niveauOrigine(c) {
    var n = NIVEAUX[c.niveau_origine];
    return n ? 'notion de ' + n : '';
  }

  function phraseCle(D) {
    var c = D.carte;
    if (c.phrase_cle) return c.phrase_cle;
    var r = D.roots[0];
    if (r) return 'La priorité : « ' + lowerFirst(title(r)) + ' ». Cette base fragile fait trébucher ' + D.prenom + ' sur ' + pl(r.bloque.length, 'autre notion', 'autres notions') + ' du programme.';
    if (D.count.lacune) return pl(D.count.lacune, 'notion est', 'notions sont') + ' à reprendre, sans base manquante en amont : un entraînement ciblé suffit.';
    if (D.count.fragile) return 'Un bon niveau d\'ensemble. ' + pl(D.count.fragile, 'point reste', 'points restent') + ' à consolider pour aborder le Brevet sereinement.';
    return 'Un très bon niveau : toutes les notions évaluées sont acquises.';
  }
  function lowerFirst(s) { return s ? s.charAt(0).toLowerCase() + s.slice(1) : s; }

  /* ───────────────────────── Chrome de page ───────────────────────── */

  function pageHeader(ctx) {
    var d = ctx.doc, D = ctx.D;
    if (ctx.assets.logoM) d.addImage(ctx.assets.logoM, 'PNG', M.x0, 11, 8.6, 7, 'logoM', 'FAST');
    font(ctx, 'title', 9.5); color(d, C.navy);
    txt(ctx, 'Matheux', M.x0 + (ctx.assets.logoM ? 11 : 0), 16.6);
    font(ctx, 'body', 8); color(d, C.mut);
    var right = 'Bilan de ' + D.prenom + ' · Maths ' + D.niveau;
    txt(ctx, right, M.x1, 16.4, { align: 'right' });
    if (ctx.apercu) {
      tag(ctx, 'Aperçu', M.x1 - tw(ctx, right) - 3, 15.3, C.pl, C.p, { align: 'right', size: 6 });
    }
    stroke(d, C.brd); d.setLineWidth(0.3); d.line(M.x0, 21.5, M.x1, 21.5);
  }
  function newPage(ctx) {
    ctx.doc.addPage();
    pageHeader(ctx);
    ctx.y = CONTENT_TOP;
  }
  function ensure(ctx, h, onBreak) {
    if (ctx.y + h > BOTTOM) { newPage(ctx); if (onBreak) onBreak(); return true; }
    return false;
  }
  function footer(ctx, p, total) {
    var d = ctx.doc, D = ctx.D, y = 289;
    stroke(d, C.brd); d.setLineWidth(0.3); d.line(M.x0, 283, M.x1, 283);
    font(ctx, 'bold', 8); color(d, C.p); txt(ctx, 'matheux.fr', M.x0, y);
    font(ctx, 'body', 7.3); color(d, C.mut);
    var mid = 'Bilan du ' + D.dateLong + ' · généré à partir de ' + pl(D.nq, 'réponse', 'réponses');
    if (ctx.apercu) mid += ' · aperçu';
    txt(ctx, mid, PAGE.w / 2, y, { align: 'center' });
    font(ctx, 'semi', 7.5); color(d, C.mut);
    txt(ctx, p + ' / ' + total, M.x1, y, { align: 'right' });
  }
  function sectionTitle(ctx, num, eyebrowTxt, titleTxt, lead) {
    var d = ctx.doc, y = ctx.y + 4;
    eyebrow(ctx, num + '  ·  ' + eyebrowTxt, M.x0, y);
    font(ctx, 'title', 20); color(d, C.navy);
    txt(ctx, titleTxt, M.x0, y + 9.6);
    ctx.y = y + 13;
    if (lead) ctx.y = para(ctx, lead, M.x0, ctx.y, CW * 0.9, { size: 9.3, color: C.mut, lh: 4.5 }) + 2;
    ctx.y += 3;
  }
  function subTitle(ctx, s, y) {
    font(ctx, 'bold', 10.5); color(ctx.doc, C.navy);
    txt(ctx, s, M.x0, y + 3.8);
    return y + 7.5;
  }

  /* ───────────────────────── Page 1 : couverture ───────────────────────── */

  function drawCover(ctx) {
    var d = ctx.doc, D = ctx.D, c = D.carte;
    if (ctx.assets.logo) d.addImage(ctx.assets.logo, 'PNG', M.x0, 16, 30, 30 * 361 / 600, 'logo', 'FAST');
    else { font(ctx, 'title', 18); color(d, C.navy); txt(ctx, 'Matheux', M.x0, 26); }
    font(ctx, 'semi', 8.5); color(d, C.mut);
    txt(ctx, c.type === 'express' ? 'Diagnostic express' : 'Diagnostic complet', M.x1, 22, { align: 'right' });
    txt(ctx, D.dateLong, M.x1, 26.5, { align: 'right' });
    if (ctx.apercu) tag(ctx, 'Aperçu gratuit', M.x1, 32, C.pl, C.p, { align: 'right', size: 6.4 });

    var y = 58;
    eyebrow(ctx, 'Bilan de compétences · maths ' + D.niveau, M.x0, y, C.p, 8.4);
    var nameSize = 38;
    font(ctx, 'title', nameSize);
    while (nameSize > 20 && tw(ctx, D.prenom) > CW) { nameSize -= 2; font(ctx, 'title', nameSize); }
    color(d, C.navy);
    txt(ctx, D.prenom, M.x0, y + 16);
    fill(d, C.p); d.rect(M.x0, y + 21.5, 14, 1.3, 'F');
    var meta = ['Diagnostic réalisé le ' + D.dateLong];
    if (c.duree_min) meta.push(c.duree_min + ' min');
    meta.push(pl(D.nq, 'réponse analysée', 'réponses analysées'));
    para(ctx, meta.join('  ·  '), M.x0, y + 25, CW, { size: 9.5, color: C.mut });

    // Panneau score + phrase-clé
    y = 97;
    var phrase = phraseCle(D);
    var tx = M.x0 + 68, tWidth = M.x1 - 8 - tx;
    var ph = paraH(ctx, phrase, tWidth, { role: 'title', size: 14, lh: 6.6 });
    var H = Math.max(60, ph + 28);
    fill(d, C.bg); stroke(d, C.brd); d.setLineWidth(0.3);
    d.roundedRect(M.x0, y, CW, H, 4, 4, 'FD');
    var score = Math.max(0, Math.min(100, Math.round(c.score_global || 0)));
    var sst = statusFromMaitrise(score / 100);
    var cx = M.x0 + 33, cy = y + H / 2, r = 20;
    arc(ctx, cx, cy, r, 0, Math.PI * 2 - 0.001, 5.2, C.brd);
    if (score > 0) arc(ctx, cx, cy, r, 0, Math.PI * 2 * score / 100, 5.2, STATUS[sst].c);
    font(ctx, 'title', 25); color(d, C.navy);
    var sw = tw(ctx, String(score));
    font(ctx, 'title', 12);
    var pw = tw(ctx, '%');
    font(ctx, 'title', 25);
    txt(ctx, String(score), cx - (sw + pw + 0.8) / 2, cy + 2.6);
    font(ctx, 'title', 12); txt(ctx, '%', cx - (sw + pw + 0.8) / 2 + sw + 0.8, cy + 2.6);
    font(ctx, 'semi', 7); color(d, C.mut);
    txt(ctx, 'SCORE GLOBAL', cx, cy + 8.2, { align: 'center' });
    stroke(d, C.brd); d.setLineWidth(0.3); d.line(tx - 6, y + 10, tx - 6, y + H - 10);
    var ty = y + (H - (ph + 19)) / 2;
    eyebrow(ctx, 'L\'essentiel', tx, ty + 3);
    ty = para(ctx, phrase, tx, ty + 6.5, tWidth, { role: 'title', size: 14, lh: 6.6, color: C.navy });
    para(ctx, 'Score global = part des questions réussies du premier coup, sans indice.', tx, ty + 3, tWidth, { size: 7.8, color: C.mut });

    // En un coup d'œil
    y = y + H + 8;
    y = subTitle(ctx, 'En un coup d\'œil', y);
    var keys = ['acquis', 'fragile', 'lacune', 'non_evalue'];
    var gap = 4, w = (CW - gap * 3) / 4, h = 23;
    keys.forEach(function (k, i) {
      var S = STATUS[k], x = M.x0 + i * (w + gap);
      fill(d, S.l); d.roundedRect(x, y, w, h, 3, 3, 'F');
      pastille(ctx, k, x + 6, y + 7, 1.8);
      font(ctx, 'semi', 7.8); color(d, S.d);
      txt(ctx, S.label, x + 9.5, y + 8.2);
      font(ctx, 'title', 20); color(d, S.d);
      txt(ctx, String(D.count[k]), x + 4.5, y + 18);
      font(ctx, 'body', 7.4); color(d, S.d);
      var n = D.count[k];
      var sub = k === 'lacune' && D.roots.length ? 'dont ' + pl(D.roots.length, 'cause racine', 'causes racines') : (n > 1 ? 'compétences' : 'compétence');
      font(ctx, 'title', 20);
      var nw = tw(ctx, String(n));
      font(ctx, 'body', 7.4);
      txt(ctx, sub, x + 4.5 + nw + 2, y + 18);
    });
    y += h + 8;

    // Priorités / points forts
    var colW = (CW - 10) / 2, xl = M.x0, xr = M.x0 + colW + 10;
    var yl = subTitle(ctx, 'Par où commencer', y);
    var prios = (c.priorites || []).slice(0, 3).map(function (id) { return compOrStub(D, id); });
    if (!prios.length) prios = D.comps.filter(function (x) { return x.st === 'lacune' || x.st === 'fragile'; }).slice(0, 3);
    prios.forEach(function (p, i) {
      fill(d, C.navy); d.circle(xl + 2.6, yl + 2.6, 2.6, 'F');
      font(ctx, 'bold', 7.5); color(d, C.white); txt(ctx, String(i + 1), xl + 2.6, yl + 3.7, { align: 'center' });
      var yy = para(ctx, title(p), xl + 8, yl, colW - 8, { role: 'semi', size: 9, color: C.ink, lh: 4.2, max: 2 });
      font(ctx, 'body', 7.4); color(d, STATUS[p.st].d);
      var extra = STATUS[p.st].label + (p.maitrise != null ? ' · ' + pct(p.maitrise) : '') + (p.cause_racine ? ' · cause racine' : '');
      txt(ctx, extra, xl + 8, yy + 2.4);
      yl = yy + 5.6;
    });
    if (!prios.length) para(ctx, 'Aucune priorité : tout est acquis.', xl, yl, colW, { size: 9 });
    var yr = y;
    font(ctx, 'bold', 10.5); color(d, C.navy); txt(ctx, 'Points forts', xr, yr + 3.8);
    yr += 7.5;
    var forts = (c.points_forts || []).map(function (id) { return compOrStub(D, id); });
    if (!forts.length) forts = D.comps.filter(function (x) { return x.st === 'acquis'; }).sort(function (a, b) { return (b.maitrise || 0) - (a.maitrise || 0); }).slice(0, 3);
    forts.slice(0, 3).forEach(function (f) {
      check(ctx, xr + 2.6, yr + 2.6, 2.6, STATUS.acquis.c);
      yr = para(ctx, title(f), xr + 8, yr, colW - 8, { role: 'semi', size: 9, color: C.ink, lh: 4.2, max: 2 }) + 3.4;
    });
    if (!forts.length) para(ctx, 'Pas encore de point fort net : c\'est normal en début d\'année.', xr, yr, colW, { size: 9 });

    // Légende
    var ly = Math.max(Math.max(yl, yr) + 3, BOTTOM - 25);
    drawLegend(ctx, ly);
  }

  function drawLegend(ctx, y) {
    var d = ctx.doc, h = 25;
    stroke(d, C.brd); d.setLineWidth(0.3); fill(d, C.white);
    d.roundedRect(M.x0, y, CW, h, 3, 3, 'FD');
    eyebrow(ctx, 'Comment lire ce bilan', M.x0 + 5, y + 6, C.mut, 6.8);
    var items = [
      ['acquis', 'Acquis', 'maîtrise > 70 %'],
      ['fragile', 'Fragile', 'maîtrise 40 à 70 %'],
      ['lacune', 'Lacune', 'maîtrise < 40 %'],
      ['non_evalue', 'Non évalué', 'moins de 2 réponses'],
    ];
    var w = (CW - 10) / 4;
    items.forEach(function (it, i) {
      var x = M.x0 + 5 + i * w;
      pastille(ctx, it[0], x + 1.6, y + 10.8, 1.6);
      font(ctx, 'semi', 8); color(d, C.ink); txt(ctx, it[1], x + 5, y + 11.8);
      font(ctx, 'body', 7.2); color(d, C.mut); txt(ctx, it[2], x + 5, y + 15.2);
    });
    var tgw = tag(ctx, 'Cause racine', M.x0 + 5, y + 20.3, STATUS.lacune.c, C.white, { size: 5.8 });
    font(ctx, 'body', 7.4); color(d, C.ink2);
    txt(ctx, 'une lacune de base qui en entraîne d\'autres : c\'est elle qu\'il faut traiter en premier.', M.x0 + 5 + tgw + 2.5, y + 21.4);
  }

  /* ───────────────────────── Page 2 : la carte ───────────────────────── */

  function drawCarte(ctx) {
    var d = ctx.doc, D = ctx.D, c = D.carte;
    newPage(ctx);
    sectionTitle(ctx, '01', 'La carte', 'La carte des compétences',
      'Les 5 domaines du programme, puis le détail compétence par compétence. Une compétence n\'est jugée qu\'à partir de 2 questions au moins.');

    var doms = (c.domaines || []).slice().sort(function (a, b) { return DOMAINE_ORDER.indexOf(a.code) - DOMAINE_ORDER.indexOf(b.code); });
    if (!doms.length) doms = DOMAINE_ORDER.map(function (k) { return { code: k }; });
    var y = ctx.y;
    doms.forEach(function (dm) {
      var st = dm.statut ? statusKey(dm.statut) : statusFromMaitrise(dm.maitrise);
      if (!dm.n_comp && dm.maitrise == null) st = 'non_evalue';
      var S = STATUS[st];
      font(ctx, 'semi', 10); color(d, C.ink);
      txt(ctx, dm.libelle || DOMAINES[dm.code] || dm.code, M.x0, y + 3.6);
      var right = st === 'non_evalue' ? 'Non évalué' : pct(dm.maitrise);
      font(ctx, 'bold', 10); color(d, S.d);
      var rw = tw(ctx, right);
      txt(ctx, right, M.x1, y + 3.6, { align: 'right' });
      if (st !== 'non_evalue') tag(ctx, S.label, M.x1 - rw - 2.5, y + 2.4, S.l, S.d, { align: 'right', size: 5.8 });
      bar(ctx, M.x0, y + 5.4, CW, 3, st === 'non_evalue' ? 0 : dm.maitrise, S.c);
      // repères 40 % / 70 %
      stroke(d, C.white); d.setLineWidth(0.5);
      d.line(M.x0 + CW * 0.4, y + 5.4, M.x0 + CW * 0.4, y + 8.4);
      d.line(M.x0 + CW * 0.7, y + 5.4, M.x0 + CW * 0.7, y + 8.4);
      font(ctx, 'body', 7.4); color(d, C.mut);
      var info = [];
      if (dm.n_comp != null) info.push(pl(dm.n_comp, 'compétence évaluée', 'compétences évaluées'));
      if (dm.n_lacunes) info.push(pl(dm.n_lacunes, 'lacune', 'lacunes'));
      else if (dm.n_comp) info.push('aucune lacune');
      txt(ctx, info.join(' · '), M.x0, y + 11.9);
      y += 14.6;
    });
    font(ctx, 'body', 6.8); color(d, C.mut2);
    txt(ctx, 'Repères sur les jauges : 40 % (seuil lacune) et 70 % (seuil acquis).', M.x1, y - 2.7, { align: 'right' });
    ctx.y = y + 2;

    // Détail en deux colonnes, coulé colonne par colonne
    ctx.y = subTitle(ctx, 'Détail par compétence', ctx.y);
    var colW = (CW - 8) / 2, cols = [M.x0, M.x0 + colW + 8];
    var flow = { col: 0, top: ctx.y, y: ctx.y };
    function place(h) {
      var moved = false;
      if (flow.y + h > BOTTOM) {
        moved = true;
        if (flow.col === 0) { flow.col = 1; flow.y = flow.top; }
        else { newPage(ctx); flow.col = 0; flow.top = ctx.y + 2; flow.y = flow.top; }
      }
      return { x: cols[flow.col], y: flow.y, moved: moved };
    }
    function groupHeader(label, x, y) {
      font(ctx, 'bold', 7); color(d, C.mut);
      spaced(ctx, label.toUpperCase(), x, y + 4, 0.35);
      stroke(d, C.brd); d.setLineWidth(0.3); d.line(x, y + 5.8, x + colW, y + 5.8);
    }
    var groups = DOMAINE_ORDER.concat(Object.keys(groupBy(D.comps, 'dom')).filter(function (k) { return DOMAINE_ORDER.indexOf(k) < 0; }));
    var byDom = groupBy(D.comps, 'dom');
    groups.forEach(function (code) {
      var list = (byDom[code] || []).slice().sort(function (a, b) {
        return (STATUS_ORDER[a.st] - STATUS_ORDER[b.st]) || ((a.maitrise || 0) - (b.maitrise || 0));
      });
      if (!list.length) return;
      var rows = list.map(function (cp) { return measureRow(ctx, cp, colW); });
      var p = place(7.5 + rows[0].h);
      var dl = (doms.filter(function (x) { return x.code === code; })[0] || {}).libelle || DOMAINES[code] || code;
      groupHeader(dl, p.x, p.y);
      flow.y = p.y + 7.2;
      rows.forEach(function (r) {
        var q = place(r.h);
        if (q.moved) { groupHeader(dl + ' (suite)', q.x, q.y); flow.y = q.y + 7.2; q = place(r.h); }
        drawRow(ctx, r, q.x, q.y, colW);
        flow.y = q.y + r.h;
      });
      flow.y += 2;
    });
    ctx.y = flow.col === 0 ? flow.y : BOTTOM;
  }
  function groupBy(arr, k) {
    var o = {};
    arr.forEach(function (x) { (o[x[k]] = o[x[k]] || []).push(x); });
    return o;
  }
  function measureRow(ctx, cp, colW) {
    var tW = colW - 5 - 11;
    font(ctx, cp.st === 'lacune' ? 'semi' : 'body', 8.2);
    var lines = wrap(ctx, title(cp), tW).slice(0, 3);
    var h = lines.length * 3.5 + (cp.cause_racine ? 3.8 : 0) + 2.1;
    return { cp: cp, lines: lines, h: Math.max(5.6, h) };
  }
  function drawRow(ctx, r, x, y, colW) {
    var d = ctx.doc, cp = r.cp, S = STATUS[cp.st];
    pastille(ctx, cp.st, x + 1.5, y + 2.7, 1.3);
    font(ctx, cp.st === 'lacune' ? 'semi' : 'body', 8.2); color(d, cp.st === 'non_evalue' ? C.mut : C.ink);
    r.lines.forEach(function (l, i) { txt(ctx, l, x + 5, y + 3.7 + i * 3.5); });
    if (cp.cause_racine) tag(ctx, 'Cause racine', x + 5, y + 3.7 + r.lines.length * 3.5 + 0.4, STATUS.lacune.c, C.white, { size: 5.2 });
    font(ctx, 'semi', 8); color(d, cp.st === 'non_evalue' ? C.mut2 : S.d);
    txt(ctx, cp.st === 'non_evalue' ? '—' : pct(cp.maitrise), x + colW, y + 3.7, { align: 'right' });
    stroke(d, C.bg); d.setLineWidth(0.25);
    d.line(x + 5, y + r.h - 0.4, x + colW, y + r.h - 0.4);
  }

  /* ───────────────────────── Page 3 : causes racines ───────────────────────── */

  function drawCauses(ctx) {
    var d = ctx.doc, D = ctx.D;
    newPage(ctx);
    sectionTitle(ctx, '02', 'Les causes', 'Ce qui bloque vraiment',
      D.roots.length
        ? 'En maths, chaque notion s\'appuie sur les précédentes. Quand une base n\'est pas solide, tout ce qui est construit dessus devient difficile. Réparer la base débloque le reste.'
        : 'En maths, chaque notion s\'appuie sur les précédentes. Nous avons vérifié si les difficultés de ' + D.prenom + ' venaient d\'une base manquante.');

    if (!D.roots.length) {
      var h = 30;
      fill(d, STATUS.acquis.l); d.roundedRect(M.x0, ctx.y, CW, h, 3, 3, 'F');
      check(ctx, M.x0 + 10, ctx.y + h / 2, 4, STATUS.acquis.c);
      font(ctx, 'title', 13); color(d, STATUS.acquis.d);
      txt(ctx, 'Aucune cause racine', M.x0 + 19, ctx.y + 11.5);
      para(ctx, 'Les points à travailler de ' + D.prenom + ' sont isolés : ils ne viennent pas d\'une base manquante des années précédentes. Un entraînement ciblé sur chacun suffit.',
        M.x0 + 19, ctx.y + 14.5, CW - 26, { size: 9, color: STATUS.acquis.d, lh: 4.3 });
      ctx.y += h + 8;
    }

    D.roots.forEach(function (root) { drawRootGraph(ctx, root); });

    // Points isolés : à travailler mais sans lien avec une cause racine
    var linked = {};
    D.roots.forEach(function (r) { linked[r.id] = 1; r.bloque.forEach(function (b) { linked[b] = 1; }); });
    var iso = D.comps.filter(function (c) { return (c.st === 'lacune' || c.st === 'fragile') && !linked[c.id]; })
      .sort(function (a, b) { return (STATUS_ORDER[a.st] - STATUS_ORDER[b.st]) || ((a.maitrise || 0) - (b.maitrise || 0)); });
    if (iso.length) {
      ensure(ctx, 24);
      ctx.y = subTitle(ctx, D.roots.length ? 'Les autres points à travailler' : 'Les points à consolider', ctx.y + 1);
      font(ctx, 'bold', 10.5);
      var stw = tw(ctx, D.roots.length ? 'Les autres points à travailler' : 'Les points à consolider');
      font(ctx, 'body', 8.2); color(d, C.mut);
      txt(ctx, D.roots.length ? '· indépendants des causes racines, ils se travaillent directement' : '· chacun se travaille directement, sans revenir sur les années précédentes', M.x0 + stw + 2, ctx.y - 3.7);
      ctx.y += 0.5;
      var icw = (CW - 4) / 2, rowTop = null;
      iso.forEach(function (cp, k) {
        var S = STATUS[cp.st], col = k % 2;
        font(ctx, 'semi', 8.4);
        var lines = wrap(ctx, title(cp), icw - 10).slice(0, 2);
        var h = lines.length * 3.6 + 6.8;
        if (col === 0) {
          var nxt = iso[k + 1];
          var h2 = nxt ? (font(ctx, 'semi', 8.4), Math.min(2, wrap(ctx, title(nxt), icw - 10).length) * 3.6 + 6.8) : 0;
          ensure(ctx, Math.max(h, h2) + 2);
          rowTop = { y: ctx.y, h: Math.max(h, h2) };
        }
        var x = M.x0 + col * (icw + 4), y = rowTop.y, hh = rowTop.h;
        fill(d, S.l); d.roundedRect(x, y, icw, hh, 2, 2, 'F');
        pastille(ctx, cp.st, x + 4, y + 4.2, 1.35);
        font(ctx, 'semi', 8.4); color(d, C.ink);
        lines.forEach(function (l, i) { txt(ctx, l, x + 7.5, y + 5.2 + i * 3.6); });
        font(ctx, 'body', 7); color(d, S.d);
        var o = niveauOrigine(cp);
        txt(ctx, S.label + ' · ' + pct(cp.maitrise) + (o && cp.niveau_origine !== '3EME' ? ' · ' + o : ''), x + 7.5, y + 5.2 + lines.length * 3.6 + 0.4);
        if (col === 1 || k === iso.length - 1) ctx.y = rowTop.y + rowTop.h + 2;
      });
    }
  }

  function drawRootGraph(ctx, root) {
    var d = ctx.doc, D = ctx.D;
    var pad = 5, lw = 62, rwid = 74;
    var lx = M.x0 + pad, rx = M.x1 - pad - rwid;
    // mesures
    font(ctx, 'bold', 10);
    var lLines = wrap(ctx, title(root), lw - 10);
    var lh = 8 + lLines.length * 4.4 + 8;
    var right = root.bloque.map(function (id) {
      var cp = compOrStub(D, id);
      font(ctx, 'semi', 8.6);
      var ls = wrap(ctx, title(cp), rwid - 11).slice(0, 3);
      return { cp: cp, lines: ls, h: ls.length * 3.7 + 6.6 };
    });
    var rgap = 2.2, rh = right.reduce(function (s, r) { return s + r.h; }, 0) + rgap * (right.length - 1);
    var gh = Math.max(lh, rh);
    var sentence = 'Tant que « ' + lowerFirst(title(root)) + ' » n\'est pas solide, ' + D.prenom + ' bute aussi sur ' +
      (right.length > 1 ? 'ces ' + right.length + ' notions' : 'cette notion') + '. C\'est par là qu\'il faut commencer.';
    var sh = paraH(ctx, sentence, CW - 2 * pad, { size: 9, lh: 4.4 });
    var H = pad + 5 + gh + 4.5 + sh + pad - 1;
    ensure(ctx, H + 6);
    var y0 = ctx.y;
    stroke(d, C.brd); d.setLineWidth(0.3); fill(d, C.white);
    d.roundedRect(M.x0, y0, CW, H, 3, 3, 'FD');
    font(ctx, 'bold', 6.6); color(d, C.mut);
    spaced(ctx, 'LA CAUSE', lx, y0 + pad + 1.5, 0.4);
    spaced(ctx, 'CE QU\'ELLE BLOQUE', rx, y0 + pad + 1.5, 0.4);
    var gy = y0 + pad + 5;
    // nœud gauche
    var ly = gy + (gh - lh) / 2;
    fill(d, STATUS.lacune.l); d.roundedRect(lx, ly, lw, lh, 2.5, 2.5, 'F');
    fill(d, STATUS.lacune.c); d.rect(lx, ly + 1, 1.4, lh - 2, 'F');
    tag(ctx, 'Cause racine', lx + 5, ly + 5.2, STATUS.lacune.c, C.white, { size: 5.6 });
    font(ctx, 'bold', 10); color(d, C.navy);
    lLines.forEach(function (l, i) { txt(ctx, l, lx + 5, ly + 12.8 + i * 4.4); });
    font(ctx, 'body', 7.6); color(d, STATUS.lacune.d);
    var o = niveauOrigine(root);
    txt(ctx, (o ? o.charAt(0).toUpperCase() + o.slice(1) + ' · ' : '') + 'maîtrise ' + pct(root.maitrise), lx + 5, ly + lh - 3.6);
    // nœuds droits + liens
    var ry = gy + (gh - rh) / 2;
    var sx = lx + lw, sy = ly + lh / 2;
    right.forEach(function (r) {
      var S = STATUS[r.cp.st], cyN = ry + r.h / 2;
      // lien (courbe de Bézier) + flèche
      var ex = rx - 1.6, mx = (sx + ex) / 2;
      stroke(d, STATUS.lacune.c); d.setLineWidth(0.45);
      d.lines([[mx - sx, 0, mx - sx, cyN - sy, ex - sx, cyN - sy]], sx, sy, [1, 1], 'S', false);
      fill(d, STATUS.lacune.c);
      d.triangle(rx, cyN, rx - 2.4, cyN - 1.3, rx - 2.4, cyN + 1.3, 'F');
      fill(d, S.l); d.roundedRect(rx, ry, rwid, r.h, 2, 2, 'F');
      pastille(ctx, r.cp.st, rx + 4.2, ry + 4.4, 1.35);
      font(ctx, 'semi', 8.6); color(d, C.ink);
      r.lines.forEach(function (l, i) { txt(ctx, l, rx + 7.8, ry + 5.4 + i * 3.8); });
      font(ctx, 'body', 7); color(d, S.d);
      txt(ctx, S.label + (r.cp.maitrise != null ? ' · ' + pct(r.cp.maitrise) : ''), rx + 7.8, ry + r.h - 2);
      ry += r.h + rgap;
    });
    fill(d, STATUS.lacune.c); d.circle(sx, sy, 1, 'F');
    para(ctx, sentence, M.x0 + pad, gy + gh + 4.5, CW - 2 * pad, { size: 9, lh: 4.4, color: C.ink2 });
    ctx.y = y0 + H + 5;
  }

  /* ───────────────────────── Page 4 : erreurs types ───────────────────────── */

  function collectErreurs(D, max) {
    var prio = {};
    (D.carte.priorites || []).forEach(function (id, i) { prio[id] = i; });
    var out = [];
    D.comps.forEach(function (cp) {
      (cp.erreurs || []).forEach(function (e) { if (e && e.exemple) out.push({ cp: cp, e: e }); });
    });
    out.sort(function (a, b) {
      var pa = prio[a.cp.id] != null ? prio[a.cp.id] : 99, pb = prio[b.cp.id] != null ? prio[b.cp.id] : 99;
      return (pa - pb) || (STATUS_ORDER[a.cp.st] - STATUS_ORDER[b.cp.st]) || ((b.cp.cause_racine ? 1 : 0) - (a.cp.cause_racine ? 1 : 0));
    });
    var seen = {};
    return out.filter(function (x) { if (seen[x.cp.id]) return false; seen[x.cp.id] = 1; return true; }).slice(0, max);
  }

  function drawErreurs(ctx) {
    var d = ctx.doc, D = ctx.D;
    var list = collectErreurs(D, ctx.opts.maxErreurs || 3);
    newPage(ctx);
    sectionTitle(ctx, '03', 'Les erreurs types', 'Les erreurs qui reviennent',
      'Une erreur qui se répète n\'est pas de l\'étourderie : c\'est une règle mal comprise, qu\'il faut remplacer. Voici celles repérées chez ' + D.prenom + ', avec une vraie question du diagnostic.');
    if (!list.length) {
      para(ctx, 'Aucune erreur récurrente n\'a été repérée : les erreurs de ' + D.prenom + ' sont ponctuelles.', M.x0, ctx.y, CW, { size: 9.5 });
      return;
    }
    list.forEach(function (x) { drawErreurCard(ctx, x.cp, x.e); });
  }

  function drawErreurCard(ctx, cp, e) {
    var d = ctx.doc, D = ctx.D, S = STATUS[cp.st], pad = 5.5;
    var ex = e.exemple || {};
    var inW = CW - 2 * pad;
    font(ctx, 'bold', 10.5);
    var tLines = wrap(ctx, title(cp), inW - 28).slice(0, 2);
    var main = e.libelle_parent || e.libelle || '';
    var detail = e.libelle_parent && e.libelle ? e.libelle : '';
    var remed = e.remediation || '';
    var Lmain = richLayout(ctx, plainToRich(main), inW, { role: 'semi', size: 9.4, lh: 4.5 });
    // encadré : question à gauche (~52 %), réponse élève / bonne réponse à droite
    var qW = Math.round((inW - 8) * 0.52), aW = (inW - 8 - qW - 5 - 3) / 2;
    var Lq = richLayout(ctx, plainToRich(ex.q), qW, { size: 9.4, lh: 4.5 });
    var half = aW;
    var La = richLayout(ctx, plainToRich(ex.reponse_eleve), half - 8, { role: 'semi', size: 10.5, lh: 5 });
    var Lb = richLayout(ctx, plainToRich(ex.a), half - 8, { role: 'semi', size: 10.5, lh: 5 });
    var Ld = detail ? richLayout(ctx, 'En détail : ' + plainToRich(detail), inW, { size: 8.4, lh: 4 }) : null;
    var Lr = remed ? richLayout(ctx, plainToRich(remed), inW - 22, { size: 8.6, lh: 4.2 }) : null;
    var ansH = Math.max(La.h, Lb.h) + 5.2;
    var boxH = Math.max(3.5 + Lq.h + 1, ansH) + 7;
    var H = pad + tLines.length * 4.6 + 3 + 3.5 + Lmain.h + (Ld ? Ld.h + 1 : 0) + 3 + boxH + (Lr ? 3 + Lr.h : 0) + pad;
    ensure(ctx, H + 5);
    var y0 = ctx.y, y = y0 + pad;
    stroke(d, C.brd); d.setLineWidth(0.3); fill(d, C.white);
    d.roundedRect(M.x0, y0, CW, H, 3, 3, 'FD');
    fill(d, S.c); d.rect(M.x0, y0 + 3, 1.2, H - 6, 'F');
    var x = M.x0 + pad;
    font(ctx, 'bold', 10.5); color(d, C.navy);
    tLines.forEach(function (l, i) { txt(ctx, l, x, y + 3.8 + i * 4.6); });
    var tagW = tag(ctx, S.label, M.x1 - pad, y + 2.6, S.l, S.d, { align: 'right', size: 5.8 });
    if (cp.cause_racine) tag(ctx, 'Cause racine', M.x1 - pad - tagW - 1.5, y + 2.6, STATUS.lacune.c, C.white, { align: 'right', size: 5.8 });
    y += tLines.length * 4.6 + 3;
    eyebrow(ctx, 'Erreur repérée', x, y + 2, STATUS.lacune.c, 6.6);
    y += 3.5;
    y = richDraw(ctx, Lmain, x, y, { color: C.ink });
    if (Ld) y = richDraw(ctx, Ld, x, y + 0.5, { color: C.mut }) + 0.5;
    y += 3;
    // encadré exemple
    fill(d, C.bg); d.roundedRect(x, y, inW, boxH, 2.5, 2.5, 'F');
    var bx = x + 4, by = y + 3.5;
    eyebrow(ctx, 'La question posée', bx, by + 1.5, C.mut, 6.4);
    richDraw(ctx, Lq, bx, by + 2.5, { color: C.ink });
    var ax = bx + qW + 5, bx2 = ax + half + 3;
    font(ctx, 'semi', 6.4);
    var who = tw(ctx, ('Réponse de ' + D.prenom).toUpperCase()) <= half - 10 ? 'Réponse de ' + D.prenom : 'Sa réponse';
    by = y + (boxH - ansH) / 2;
    [[ax, who, La, STATUS.lacune], [bx2, 'Bonne réponse', Lb, STATUS.acquis]].forEach(function (col, k) {
      fill(d, C.white); stroke(d, C.brd); d.setLineWidth(0.25);
      d.roundedRect(col[0], by, half, ansH, 2, 2, 'FD');
      if (k === 0) cross(ctx, col[0] + 4.2, by + ansH / 2, 2.2, col[3].c);
      else check(ctx, col[0] + 4.2, by + ansH / 2, 2.2, col[3].c);
      font(ctx, 'semi', 6.4); color(d, C.mut);
      txt(ctx, col[1].toUpperCase(), col[0] + 8.4, by + 3.6);
      richDraw(ctx, col[2], col[0] + 8.4, by + 3.9, { color: col[3].d });
    });
    y += boxH;
    if (Lr) {
      y += 3;
      font(ctx, 'bold', 7.8); color(d, C.p);
      txt(ctx, 'Ce qui aide', x, y + 3.2);
      richDraw(ctx, Lr, x + 22, y, { color: C.ink2 });
    }
    ctx.y = y0 + H + 4;
  }

  /* ───────────────────────── Page 5 : plan 4 semaines ───────────────────────── */

  function drawPlan(ctx) {
    var d = ctx.doc, D = ctx.D, c = D.carte;
    var plan = (c.plan_4_semaines || []).slice(0, 6);
    newPage(ctx);
    sectionTitle(ctx, '04', 'Le plan', 'Le plan sur 4 semaines',
      'Un objectif par semaine, dans l\'ordre qui compte : d\'abord les bases qui bloquent, ensuite les notions qui en dépendent. Les exercices du jour sont choisis automatiquement sur l\'objectif de la semaine.');

    // bandeau rythme
    var bh = 16;
    fill(d, C.pl); d.roundedRect(M.x0, ctx.y, CW, bh, 3, 3, 'F');
    var stats = [['15 min', 'par jour'], ['5 jours', 'sur 7'], ['5 exercices', 'par séance']];
    var w3 = CW / 3;
    stats.forEach(function (s, i) {
      var x = M.x0 + i * w3 + 7;
      font(ctx, 'title', 13); color(d, C.p); txt(ctx, s[0], x, ctx.y + 9.5);
      var sw = tw(ctx, s[0]);
      font(ctx, 'body', 8.4); color(d, C.ink2); txt(ctx, s[1], x + sw + 2, ctx.y + 9.5);
      if (i) { stroke(d, C.pm); d.setLineWidth(0.3); d.line(M.x0 + i * w3, ctx.y + 4, M.x0 + i * w3, ctx.y + bh - 4); }
    });
    ctx.y += bh + 8;

    if (!plan.length) { para(ctx, 'Plan à venir.', M.x0, ctx.y, CW); return; }
    var lineX = M.x0 + 6;
    plan.forEach(function (sem, i) {
      var foc = (sem.focus || []).map(function (id) { return compOrStub(D, id); });
      var obj = sem.objectif || '';
      var cx = M.x0 + 18, cw = CW - 18;
      var oh = obj ? paraH(ctx, obj, cw, { size: 9.2, lh: 4.4 }) : 0;
      var fl = foc.map(function (f) { font(ctx, 'semi', 8.8); return wrap(ctx, title(f), cw - 34).slice(0, 2); });
      var fh = fl.reduce(function (s, l) { return s + l.length * 4 + 2.6; }, 0);
      var H = 7 + 3 + oh + 3 + fh + 4;
      ensure(ctx, H);
      var y = ctx.y;
      // frise
      if (i < plan.length - 1) { stroke(d, C.pm); d.setLineWidth(0.6); d.line(lineX, y + 6, lineX, y + H + 1); }
      fill(d, C.p); d.circle(lineX, y + 4, 4.2, 'F');
      font(ctx, 'title', 10.5); color(d, C.white); txt(ctx, String(sem.semaine || i + 1), lineX, y + 5.6, { align: 'center' });
      font(ctx, 'title', 12.5); color(d, C.navy);
      txt(ctx, 'Semaine ' + (sem.semaine || i + 1), cx, y + 5.4);
      var yy = y + 10;
      if (obj) yy = para(ctx, obj, cx, yy - 0.5, cw, { size: 9.2, lh: 4.4, color: C.ink2 }) + 3;
      foc.forEach(function (f, k) {
        var S = STATUS[f.st], lh = fl[k].length * 4 + 1.2;
        fill(d, S.l); d.roundedRect(cx, yy - 0.6, cw, lh + 1.2, 1.8, 1.8, 'F');
        pastille(ctx, f.st, cx + 3.6, yy + 2.5, 1.25);
        font(ctx, 'semi', 8.8); color(d, C.ink);
        fl[k].forEach(function (l, j) { txt(ctx, l, cx + 7, yy + 3.4 + j * 4); });
        font(ctx, 'body', 7.4); color(d, S.d);
        txt(ctx, S.label + (f.maitrise != null ? ' · ' + pct(f.maitrise) : ''), cx + cw - 3, yy + 3.3, { align: 'right' });
        yy += lh + 1.4;
      });
      ctx.y = y + H;
    });

    // après le plan
    var nh = 18.5;
    ensure(ctx, nh + 4);
    ctx.y += 2;
    stroke(d, C.brd); d.setLineWidth(0.3); fill(d, C.white);
    d.roundedRect(M.x0, ctx.y, CW, nh, 3, 3, 'FD');
    font(ctx, 'bold', 9.5); color(d, C.navy);
    txt(ctx, 'Et au bout de 4 semaines ?', M.x0 + 5, ctx.y + 6.5);
    para(ctx, 'On refait le point avec un nouveau diagnostic : les progrès se mesurent sur les mêmes compétences, pas à l\'impression.', M.x0 + 5, ctx.y + 9, CW - 10, { size: 8.6, color: C.ink2, lh: 4 });
    ctx.y += nh + 4;
  }

  /* ───────────────────────── Page 6 : pour les parents ───────────────────────── */

  function drawParents(ctx) {
    var d = ctx.doc, D = ctx.D, c = D.carte, P = D.prenom;
    newPage(ctx);
    sectionTitle(ctx, '05', 'Pour les parents', 'Accompagner sans faire à sa place',
      'Votre rôle n\'est pas d\'être prof de maths. Il est d\'installer une routine et de valoriser l\'effort. C\'est ce qui fait la différence sur une année.');

    var cards = [
      ['Combien de temps ?', '15 minutes par jour, 5 jours sur 7. Court et régulier vaut mieux que 2 heures le dimanche : la mémoire se construit par répétition.'],
      ['Quand ?', 'Toujours au même moment (après le goûter, avant l\'écran du soir). Une habitude fixe évite la négociation quotidienne.'],
      ['Votre place', 'À côté, pas à la place. Vous n\'avez pas besoin de connaître la réponse : demandez à ' + P + ' d\'expliquer sa démarche.'],
    ];
    var gap = 4, w = (CW - 2 * gap) / 3;
    var hh = Math.max.apply(null, cards.map(function (k) { return paraH(ctx, k[1], w - 10, { size: 8.6, lh: 4.2 }); })) + 16;
    cards.forEach(function (k, i) {
      var x = M.x0 + i * (w + gap);
      fill(d, C.bg); d.roundedRect(x, ctx.y, w, hh, 3, 3, 'F');
      font(ctx, 'title', 11); color(d, C.p); txt(ctx, k[0], x + 5, ctx.y + 8);
      para(ctx, k[1], x + 5, ctx.y + 11, w - 10, { size: 8.6, lh: 4.2, color: C.ink2 });
    });
    ctx.y += hh + 9;

    // À dire / à éviter
    var dire = ['« Montre-moi comment tu as fait. »', '« Qu\'est-ce qui était plus facile qu\'hier ? »', '« Une erreur ? C\'est justement là qu\'on apprend. »', '« Tu as tenu tes séances toute la semaine, bravo. »'];
    var eviter = ['« Moi non plus, je n\'étais pas bon en maths. »', '« Mais c\'est facile pourtant ! »', '« Donne, je vais te montrer. »', 'Comparer avec un frère, une sœur ou des camarades.'];
    var cw = (CW - 6) / 2;
    var listH = function (arr) { return arr.reduce(function (s, t) { return s + paraH(ctx, t, cw - 16, { size: 8.8, lh: 4.2 }) + 2.4; }, 0); };
    var H = Math.max(listH(dire), listH(eviter)) + 15;
    [[M.x0, 'Ce qu\'on peut dire', dire, STATUS.acquis, true], [M.x0 + cw + 6, 'Ce qu\'on évite', eviter, STATUS.lacune, false]].forEach(function (col) {
      var x = col[0], S = col[3];
      fill(d, S.l); d.roundedRect(x, ctx.y, cw, H, 3, 3, 'F');
      if (col[4]) check(ctx, x + 7, ctx.y + 7.3, 2.6, S.c); else cross(ctx, x + 7, ctx.y + 7.3, 2.6, S.c);
      font(ctx, 'bold', 10); color(d, S.d); txt(ctx, col[1], x + 12, ctx.y + 8.6);
      var yy = ctx.y + 13.5;
      col[2].forEach(function (t) {
        fill(d, S.c); d.circle(x + 8.5, yy + 1.55, 0.7, 'F');
        yy = para(ctx, t, x + 12, yy, cw - 16, { size: 8.8, lh: 4.2, color: C.ink }) + 2.4;
      });
    });
    ctx.y += H + 9;

    // Sans faire à sa place
    ctx.y = subTitle(ctx, 'Quand ' + P + ' bloque sur un exercice', ctx.y);
    var tips = [
      ['Laisser chercher 3 minutes', 'avant d\'intervenir. Chercher, même sans trouver, c\'est déjà travailler.'],
      ['Poser une question plutôt que donner la méthode', ': « Qu\'est-ce que l\'énoncé demande ? », « Tu as déjà vu un exercice qui ressemble ? »'],
      ['Utiliser les indices de Matheux', 'plutôt que la réponse : ils guident étape par étape sans tout dévoiler.'],
      ['S\'arrêter à l\'heure', ', même au milieu d\'un exercice. Mieux vaut finir sur une réussite que sur une dispute.'],
    ];
    tips.forEach(function (t, i) {
      var s = t[0] + (t[1][0] === ',' || t[1][0] === ':' ? '' : ' ') + t[1];
      var h = paraH(ctx, s, CW - 10, { size: 9, lh: 4.4 });
      ensure(ctx, h + 3);
      fill(d, C.p); d.circle(M.x0 + 2.4, ctx.y + 2.4, 2.4, 'F');
      font(ctx, 'bold', 7.2); color(d, C.white); txt(ctx, String(i + 1), M.x0 + 2.4, ctx.y + 3.4, { align: 'center' });
      // début en gras, suite en normal (sur la 1re ligne seulement si ça tient)
      font(ctx, 'bold', 9);
      var bw = tw(ctx, t[0]);
      font(ctx, 'body', 9);
      var restLines = wrap(ctx, (t[1][0] === ',' || t[1][0] === ':' ? '' : ' ') + t[1], CW - 8 - bw);
      if (restLines.length === 1) {
        font(ctx, 'bold', 9); color(d, C.ink); txt(ctx, t[0], M.x0 + 8, ctx.y + 3.2);
        font(ctx, 'body', 9); color(d, C.ink2); txt(ctx, restLines[0], M.x0 + 8 + bw, ctx.y + 3.2);
        ctx.y += 4.4 + 2.6;
      } else {
        font(ctx, 'bold', 9); color(d, C.ink); txt(ctx, t[0], M.x0 + 8, ctx.y + 3.2);
        ctx.y = para(ctx, t[1].replace(/^[,:]\s*/, ''), M.x0 + 8, ctx.y + 4.4, CW - 8, { size: 9, lh: 4.4, color: C.ink2 }) + 2.6;
      }
    });

    if (c.message_parent) {
      var mh = paraH(ctx, c.message_parent, CW - 16, { size: 9.4, lh: 4.6 }) + 16;
      ensure(ctx, mh + 6);
      ctx.y += 4;
      fill(d, C.navy); d.roundedRect(M.x0, ctx.y, CW, mh, 3, 3, 'F');
      font(ctx, 'title', 10.5); color(d, C.white);
      txt(ctx, 'Notre regard sur ' + P, M.x0 + 8, ctx.y + 8.5);
      para(ctx, c.message_parent, M.x0 + 8, ctx.y + 11.5, CW - 16, { size: 9.4, lh: 4.6, color: '#E2E8F0' });
      ctx.y += mh;
    }
  }

  /* ───────────────────────── Aperçu : page verrouillée ───────────────────────── */

  function drawLocked(ctx) {
    var d = ctx.doc, D = ctx.D, c = D.carte, o = ctx.opts.cta || {};
    newPage(ctx);
    sectionTitle(ctx, '02 → 05', 'La suite du bilan', 'Ce que contient le bilan complet', null);
    var nErr = collectErreurs(D, ctx.opts.maxErreurs || 3).length;
    var teasers = [
      ['02', 'Ce qui bloque vraiment', D.roots.length ? pl(D.roots.length, 'cause racine identifiée', 'causes racines identifiées') + ', et les notions qu\'elles bloquent' : 'L\'analyse des bases des années précédentes'],
      ['03', 'Les erreurs qui reviennent', nErr ? pl(nErr, 'erreur type repérée', 'erreurs types repérées') + ', avec une vraie question du diagnostic' : 'Les erreurs types, avec exemples'],
      ['04', 'Le plan sur 4 semaines', 'Un objectif par semaine, dans l\'ordre qui débloque le reste'],
      ['05', 'Pour les parents', 'Comment accompagner ' + D.prenom + ' sans faire à sa place'],
    ];
    var seed = 7;
    function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
    teasers.forEach(function (t) {
      var y = ctx.y, h = 40;
      stroke(d, C.brd); d.setLineWidth(0.3); fill(d, C.white);
      d.roundedRect(M.x0, y, CW, h, 3, 3, 'FD');
      eyebrow(ctx, t[0], M.x0 + 6, y + 8, C.mut2, 7);
      font(ctx, 'title', 12.5); color(d, C.navy); txt(ctx, t[1], M.x0 + 16, y + 8.6);
      font(ctx, 'semi', 8.6); color(d, C.p); txt(ctx, t[2], M.x0 + 16, y + 14);
      // texte « flouté » : barres grises (aucun contenu réel n'est dessiné)
      for (var r = 0; r < 3; r++) {
        var bx = M.x0 + 16, by = y + 20 + r * 5.6;
        while (bx < M.x1 - 30) {
          var bw = 8 + rnd() * 22;
          fill(d, r === 0 ? '#E7EBF1' : '#EEF1F5'); d.roundedRect(bx, by, Math.min(bw, M.x1 - 12 - bx), 2.6, 1.3, 1.3, 'F');
          bx += bw + 2.2;
        }
      }
      // cadenas
      var lx = M.x1 - 12, ly = y + 8;
      stroke(d, C.mut2); d.setLineWidth(0.6);
      d.lines([[0, -1.6], [0.6, -1.7, 3.4, -1.7, 4, 0], [0, 1.6]], lx - 2, ly - 0.2, [1, 1], 'S', false);
      fill(d, C.mut2); d.roundedRect(lx - 3, ly - 0.4, 6, 4.4, 0.8, 0.8, 'F');
      ctx.y += h + 4;
    });

    // Appel à l'action
    var y = ctx.y + 2, H = 44;
    if (y + H > BOTTOM) y = BOTTOM - H;
    fill(d, C.navy); d.roundedRect(M.x0, y, CW, H, 4, 4, 'F');
    font(ctx, 'title', 15); color(d, C.white);
    txt(ctx, 'Débloquez le bilan complet de ' + D.prenom, M.x0 + 8, y + 12);
    para(ctx, o.texte || 'Les causes des difficultés, les erreurs expliquées, un plan semaine par semaine et un guide pour vous : tout pour savoir exactement quoi travailler.', M.x0 + 8, y + 15, CW - 70, { size: 8.8, lh: 4.3, color: '#CBD5E1' });
    var label = (o.label || 'Débloquer le bilan') + (o.prix ? '  ·  ' + o.prix : '');
    font(ctx, 'bold', 9.5);
    var bw2 = tw(ctx, label) + 12, bh = 11, bx2 = M.x1 - 8 - bw2, by2 = y + H - 8 - bh;
    fill(d, '#10B981'); d.roundedRect(bx2, by2, bw2, bh, bh / 2, bh / 2, 'F');
    color(d, C.white); txt(ctx, label, bx2 + bw2 / 2, by2 + 7.1, { align: 'center' });
    if (o.url) d.link(bx2, by2, bw2, bh, { url: o.url });
    if (o.url) {
      font(ctx, 'body', 7.4); color(d, '#94A3B8');
      txt(ctx, o.url.replace(/^https?:\/\//, ''), M.x0 + 8, y + H - 7);
    }
  }

  /* ───────────────────────── API ───────────────────────── */

  function render(carte, opts) {
    opts = opts || {};
    if (!carte || typeof carte !== 'object') return Promise.reject(new Error('MatheuxBilanPDF.render : carte requise'));
    return Promise.all([loadJsPDF(opts.jsPDFUrl), loadAssets(opts)]).then(function (r) {
      var JsPDF = r[0], assets = r[1];
      var doc = new JsPDF({ unit: 'mm', format: 'a4', orientation: 'portrait', compress: true });
      var hasFonts = !!assets.fonts;
      if (hasFonts) {
        try {
          assets.fonts.forEach(function (f) { doc.addFileToVFS(f.file, f.b64); doc.addFont(f.file, f.family, f.style); });
        } catch (e) { hasFonts = false; }
      }
      var D = prepare(carte, opts);
      var ctx = { doc: doc, D: D, opts: opts, assets: assets, hasFonts: hasFonts, apercu: !!opts.apercu, y: 0 };
      doc.setProperties({
        title: 'Bilan de compétences maths ' + D.niveau + ' — ' + D.prenom,
        subject: 'Diagnostic Matheux du ' + D.dateLong, author: 'Matheux', creator: 'matheux.fr',
      });
      doc.setLineHeightFactor(1.2);

      drawCover(ctx);
      drawCarte(ctx);
      if (ctx.apercu) {
        drawLocked(ctx);
      } else {
        drawCauses(ctx);
        drawErreurs(ctx);
        drawPlan(ctx);
        drawParents(ctx);
      }
      var total = doc.internal.getNumberOfPages();
      for (var p = 1; p <= total; p++) { doc.setPage(p); footer(ctx, p, total); }

      var blob = doc.output('blob');
      var fileName = 'Bilan-maths-' + D.niveau + '_' + slug(D.prenom) + '_' + (carte.date || 'bilan') + (ctx.apercu ? '_apercu' : '') + '.pdf';
      return {
        blob: blob,
        url: global.URL && global.URL.createObjectURL ? global.URL.createObjectURL(blob) : null,
        fileName: fileName,
        pageCount: total,
        fontsEmbedded: hasFonts,
      };
    });
  }

  global.MatheuxBilanPDF = {
    version: VERSION,
    render: render,
    // exposés pour tests / réutilisation (ex. aperçu HTML)
    _plainToRich: plainToRich,
    _parseTex: parseTex,
  };
})(typeof window !== 'undefined' ? window : globalThis);
