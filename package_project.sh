#!/usr/bin/env bash
# Package the TAPIS DIGITECH project into a distributable ZIP.
set -euo pipefail
NAME="TAPIS-DIGITECH"
OUT="${NAME}.zip"
cd "$(dirname "$0")"
rm -f "../${OUT}"
zip -rq "../${OUT}" . -x "*.zip" -x "*.DS_Store" -x "node_modules/*"
echo "Created ../${OUT}"
