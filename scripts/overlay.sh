#!/usr/bin/env bash
# overlay.sh — copy Stage 4 output onto nexacro-fullstack-starter scaffold
set -euo pipefail

OUT_DIR="${1:?usage: overlay.sh <stage4-out-dir> <project-root>}"
PROJECT_ROOT="${2:?usage: overlay.sh <stage4-out-dir> <project-root>}"

# Forms + datasets
mkdir -p "${PROJECT_ROOT}/nxui/_form_" "${PROJECT_ROOT}/nxui/_datasets_"
cp -f "${OUT_DIR}/nxui/_form_/"*.xfdl              "${PROJECT_ROOT}/nxui/_form_/"
cp -f "${OUT_DIR}/nxui/_datasets_/dsMenu.seed.xml" "${PROJECT_ROOT}/nxui/_datasets_/"

# Patches — typedefinition append (manual review recommended)
echo "[overlay] typedefinition.patch.xml ready at ${OUT_DIR}/patches/ — merge into ${PROJECT_ROOT}/nxui/typedefinition.xml manually or via typedefinition.merge.py"

# Docs
mkdir -p "${PROJECT_ROOT}/docs"
cp -f "${OUT_DIR}/docs/"*.md "${PROJECT_ROOT}/docs/" 2>/dev/null || true

echo "[overlay] done"
