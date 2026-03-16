// ══════════════════════════════════════════════════════════════
  // Double-check que le statut Premium n'est pas falsifié côté client.
  // Vérifie périodiquement auprès du backend que le statut est toujours valide.

  /**
   * Vérification Premium périodique (toutes les 5 min)
   * Empêche un utilisateur de falsifier S.trial.isPremium en localStorage/mémoire
   */
  var _premiumCheckInterval = null;

  function startPremiumGuard() {
    // Ne pas vérifier pour les admins
    if (S.prof && S.prof.isAdmin) return;

    // Check immédiat au login
    _verifyPremiumStatus();

    // Check toutes les 5 minutes
    if (_premiumCheckInterval) clearInterval(_premiumCheckInterval);
    _premiumCheckInterval = setInterval(_verifyPremiumStatus, 5 * 60 * 1000);
  }

  async function _verifyPremiumStatus() {
    if (!S.prof || !S.prof.code) return;
    try {
      var r = await fetch(SU, {
        method: 'POST',
        body: JSON.stringify({ action: 'check_trial_status', code: S.prof.code })
      });
      var d = await r.json();
      if (d.status === 'success') {
        var serverPremium = !!d.isPremium;
        var serverTrialActive = !!d.trialActive;

        // ── Détection de falsification ──
        // Si le client dit Premium mais le serveur dit non → forcer la synchro
        if (S.trial && S.trial.isPremium && !serverPremium) {
          S.trial.isPremium = false;
          S.trial.trialActive = serverTrialActive;
          S.trial.daysLeft = d.daysLeft || 0;
          renderTrialBadge();
          if (!serverTrialActive) {
            showTrialExpired();
          }
        }

        // ── Activation détectée (webhook Stripe a activé Premium) ──
        if (S.trial && !S.trial.isPremium && serverPremium) {
          S.trial.isPremium = true;
          S.prof.premium = true;
          renderTrialBadge(); // cache le badge
          // Retirer l'overlay trial expiré si présent
          var ov = document.getElementById('trial-expired-overlay');
          if (ov) ov.remove();
          showT('Abonnement activé ! Accès illimité.', 4000, '🎉');
        }

        // ── Synchro daysLeft ──
        if (S.trial) {
          S.trial.daysLeft = d.daysLeft || S.trial.daysLeft;
          S.trial.trialActive = serverTrialActive;
        }
      }
    } catch (e) {
      // Silencieux — pas de blocage si le réseau coupe
    }
  }

  /**
   * Vérification anti-tampering au moment critique (accès aux exercices)
   * Appelé avant chaque save_score pour s'assurer que l'utilisateur a le droit de jouer
   */
  function isPremiumOrTrialValid() {
    if (!S.trial) return false;
    if (S.prof && S.prof.isAdmin) return true;
    if (S.trial.isPremium) return true;
    if (S.trial.trialActive && S.trial.daysLeft > 0) return true;
    return false;
  }