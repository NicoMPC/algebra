#!/bin/bash
# AlgèbreBoost — push + deploy backend.js via clasp
# Usage : ./deploy.sh "description"

cd "$(dirname "$0")"
DESC="${1:-deploy}"
echo "⬆️  clasp push..."
clasp push --force
echo "🚀 clasp deploy..."
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "$DESC"
echo "✅ Deploy terminé"
