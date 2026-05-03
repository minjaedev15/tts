#!/usr/bin/env bash
set -euo pipefail

# Parse arguments
CLEAN=false
VERSION=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --clean)
      CLEAN=true
      shift
      ;;
    --version)
      VERSION=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--clean] [--version]"
      exit 1
      ;;
  esac
done

if [[ "$VERSION" == true ]]; then
  echo "TTS Build Script v1.0.0"
  exit 0
fi

# Build artifacts directory
BUILD_DIR="build"

# Nuitka output directory inside BUILD_DIR
NUITKA_OUT_DIR="${BUILD_DIR}/dist"

# Final zip name
ZIP_PATH="${BUILD_DIR}/build_output.zip"

# Environment safety: avoid network/audio during builds
export TTS_DISABLE_TTS="${TTS_DISABLE_TTS:-1}"
export TTS_DISABLE_AUDIO="${TTS_DISABLE_AUDIO:-1}"

# Set PYTHONPATH for src/ imports
export PYTHONPATH="${PYTHONPATH}:."

# Cleanup
if [[ "$CLEAN" == true ]]; then
  echo "Cleaning build directory..."
  rm -rf "${BUILD_DIR}"
fi
mkdir -p "${NUITKA_OUT_DIR}" "${BUILD_DIR}"

# Build (host build; CI does dockerized builds)
if [[ "$(uname -s)" == "Darwin" ]]; then
  # PyObjC/`Foundation` requires --mode=app on macOS
  python3 -m nuitka --standalone --mode=app --output-dir="${NUITKA_OUT_DIR}" src/app.py
else
  python3 -m nuitka --standalone --output-dir="${NUITKA_OUT_DIR}" src/app.py
fi

# Zip the Nuitka output
rm -f "${ZIP_PATH}"
(
  cd "${NUITKA_OUT_DIR}"
  # Include the directory contents of dist/ in the zip
  zip -r "${ZIP_PATH}" .
)

# Optional DMG on macOS if you have hdiutil available
if [[ "$(uname -s)" == "Darwin" ]]; then
  DMG_PATH="${BUILD_DIR}/build_output.dmg"
  rm -f "${DMG_PATH}"
  mkdir -p "${BUILD_DIR}/dmg_contents"
  cp "${ZIP_PATH}" "${BUILD_DIR}/dmg_contents/"
  hdiutil create -volname "TTS-Build" -srcfolder "${BUILD_DIR}/dmg_contents" -ov -format UDZO "${DMG_PATH}" || true
fi

echo "Build complete:"
echo " - ${ZIP_PATH}"
if [[ "$(uname -s)" == "Darwin" ]]; then
  echo " - ${BUILD_DIR}/build_output.dmg"
fi
