#!/usr/bin/env bash
# Regenera la suite CRECE+ y la publica en GitHub Pages en un solo paso.
# Uso:  ./deploy.sh ["mensaje de commit opcional"]
set -euo pipefail

# Trabaja siempre en la carpeta de este script
cd "$(dirname "$0")"

MSG="${1:-Actualiza suite CRECE+}"

echo "▶ Regenerando la suite (build_suite.py)…"
python3 build_suite.py

echo "▶ Copiando la suite a index.html (lo que sirve GitHub Pages)…"
cp crece-suite.html index.html

echo "▶ Preparando commit…"
git add -A
if git diff --cached --quiet; then
  echo "✔ No hay cambios que subir. Nada que hacer."
  exit 0
fi

git commit -m "$MSG"

echo "▶ Subiendo a GitHub (git push)…"
git push

echo ""
echo "✅ Listo. En 1–3 min recarga (Cmd+Shift+R):"
echo "   https://juniorsep.github.io/pos-cotizador/"
