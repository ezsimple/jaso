#!/bin/bash

# ------------------------------
# 준비
# ------------------------------
# 버전: python3.11.0
# ------------------------------
pyenv local 3.11.0
pip install setuptools
pip install py2app
pip install poetry
pip install rumps
pip install watchdog
pip install python-dotenv

# ------------------------------
# 빌드하기
# ------------------------------
rm -rf build/ dist/
python setup.py py2app

# ------------------------------
# 디버깅하기
# ------------------------------
# open "dist/자소.app"
