@echo off

title Download bot

echo Starting download bot...
call .venv\Scripts\activate
python bot\download.py
pause

