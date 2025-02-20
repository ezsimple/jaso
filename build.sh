#!/bin/bash
# pip install rumps
# pip install watchdog

# 빌드, python3.11.0
# pyenv local 3.11.0
python setup.py py2app

# 디버깅하기
# (cd dist/자소.app/Contents/MacOS; open 자소)
