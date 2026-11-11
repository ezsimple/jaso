#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

# ------------------------------
# 준비
# ------------------------------
# 버전: python3.11.0
# ------------------------------
if command -v pyenv >/dev/null 2>&1; then
  if ! pyenv prefix 3.11.0 >/dev/null 2>&1; then
    echo "pyenv에 3.11.0이 없습니다. 설치합니다..."
    pyenv install 3.11.0
  fi
  pyenv local 3.11.0
else
  echo "[경고] pyenv가 없습니다. 현재 python3로 빌드합니다."
fi

PYBIN="$(command -v python3)"
"$PYBIN" -m pip install -U setuptools
"$PYBIN" -m pip install -U py2app
"$PYBIN" -m pip install -U poetry
"$PYBIN" -m pip install -U rumps
"$PYBIN" -m pip install -U watchdog
"$PYBIN" -m pip install -U python-dotenv

# ------------------------------
# 빌드하기
# ------------------------------
rm -rf build/ dist/
"$PYBIN" setup.py py2app

if [ -d "dist/자소.app" ]; then
  echo "빌드 성공: dist/자소.app"
else
  echo "빌드 실패: dist/자소.app이 없습니다." >&2
  exit 1
fi

# ------------------------------
# 디버깅하기
# ------------------------------
# open "dist/자소.app"
