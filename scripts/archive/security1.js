 // SECURITY LAYER 1 — Stripe Webhook Handler
  // ══════════════════════════════════════════════════════════════
  // Stripe envoie un POST quand un paiement est validé.
  // On vérifie le secret, on active Premium dans Users.
  //
  // Setup Stripe Dashboard :
  //   Webhooks → Add endpoint → URL = ton GAS exec URL
  //   Events : checkout.session.completed, customer.subscription.deleted
  //   Copier le Webhook Signing Secret (whsec_...) → STRIPE_WEBHOOK_SECRET ci-dessous

var STRIPE_WEBHOOK_SECRET = 'whsec_XCaxVn2m9EUDQsWQOBxX4hObdgoZYCy2'; // ← remplacer par le vrai secret

/**
 * Action : stripe_webhook
 * Appelé par Stripe via POST automatique.
 * Double vérification :
 *   1. Token secret partagé dans le metadata Stripe
 *   2. Email match dans l'onglet Users
 */
function stripeWebhook(p) {
  var SHARED_SECRET = 'MATHEUX_STRIPE_2026';

  var eventType = p.type || '';
  var obj = (p.data && p.data.object) ? p.data.object : {};

  // ── checkout.session.completed → activer Premium ──────────────────────────
  if (eventType === 'checkout.session.completed') {
    var email = (
      obj.customer_email ||
      (obj.customer_details && obj.customer_details.email) ||
      ''
    ).toLowerCase().trim();

    var metadata = obj.metadata || {};

    // Vérif 1 : secret metadata
    if (metadata.secret !== SHARED_SECRET) {
      _logWebhook('BLOCKED', 'bad_secret', email, eventType);
      return { status: 'error', message: 'forbidden' };
    }

    if (!email) {
      _logWebhook('BLOCKED', 'no_email', '', eventType);
      return { status: 'error', message: 'no_email' };
    }

    var ss  = SpreadsheetApp.getActiveSpreadsheet();
    var sh  = ss.getSheetByName(SH.USERS);
    var data = sh.getDataRange().getValues();
    var headers    = data[0];
    var iEmail     = headers.indexOf('Email');
    var iPremium   = headers.indexOf('Premium');
    var iPremiumEnd = headers.indexOf('PremiumEnd');

    var found = false;
    for (var i = 1; i < data.length; i++) {
      if (String(data[i][iEmail]).toLowerCase().trim() === email) {
        sh.getRange(i + 1, iPremium + 1).setValue(1);
        var end = new Date();
        end.setDate(end.getDate() + 31); // 31 jours renouvelables
        sh.getRange(i + 1, iPremiumEnd + 1).setValue(end.toISOString().slice(0, 10));
        found = true;
        _logWebhook('OK', 'premium_activated', email, eventType);
        break;
      }
    }

    if (!found) {
      _logWebhook('WARN', 'email_not_found', email, eventType);
      return { status: 'error', message: 'user_not_found' };
    }

    return { status: 'success', message: 'premium_activated' };
  }

  // ── customer.subscription.deleted → désactiver Premium ───────────────────
  if (eventType === 'customer.subscription.deleted') {
    var email2 = '';
    if (obj.metadata && obj.metadata.email) {
      email2 = obj.metadata.email.toLowerCase().trim();
    }
    if (email2) {
      var ss2   = SpreadsheetApp.getActiveSpreadsheet();
      var sh2   = ss2.getSheetByName(SH.USERS);
      var data2 = sh2.getDataRange().getValues();
      var hdr2  = data2[0];
      var iEml2 = hdr2.indexOf('Email');
      var iPrm2 = hdr2.indexOf('Premium');

      for (var j = 1; j < data2.length; j++) {
        if (String(data2[j][iEml2]).toLowerCase().trim() === email2) {
          sh2.getRange(j + 1, iPrm2 + 1).setValue(0);
          _logWebhook('OK', 'premium_deactivated', email2, eventType);
          break;
        }
      }
    }
    return { status: 'success' };
  }

  // ── Événement non géré ────────────────────────────────────────────────────
  _logWebhook('SKIP', 'unhandled_event', '', eventType);
  return { status: 'success', message: 'ignored' };
}

/**
 * Log chaque webhook dans l'onglet Webhook_Log (audit trail complet)
 */
function _logWebhook(status, detail, email, eventType) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName('Webhook_Log');
  if (!sh) {
    sh = ss.insertSheet('Webhook_Log');
    sh.getRange(1, 1, 1, 5).setValues([['Date', 'Status', 'Detail', 'Email', 'EventType']]);
    sh.getRange(1, 1, 1, 5).setFontWeight('bold');
  }
  sh.appendRow([new Date(), status, detail, email, eventType]);
}
