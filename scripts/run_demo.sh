#!/usr/bin/env bash
# Lance le portail de démonstration IF29 Groupe 3
set -e
cd "$(dirname "$0")/.."

if [ -d "venv_if29" ]; then
  source venv_if29/bin/activate
fi

pip install -q streamlit 2>/dev/null || true

echo "Portail IF29 Groupe 3 — http://localhost:8501"
streamlit run demo/app.py --server.headless true
