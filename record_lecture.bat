@echo off
cd /d "%~dp0"
python backend\lecture_recorder.py %*
pause
