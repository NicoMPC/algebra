#!/bin/bash
# AlgèbreBoost — deploy backend.js via clasp
# Usage : ./deploy.sh
# --force : écrase le manifest sans demander confirmation

cd "$(dirname "$0")"
echo "⬆️  clasp push..."
clasp push --force
echo "✅ Push terminé — pense à redéployer dans Apps Script UI (Déployer → Nouvelle version)"
