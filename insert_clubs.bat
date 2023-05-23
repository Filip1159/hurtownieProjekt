echo off
call venv\scripts\activate.bat
pip install -r requirements.txt
python insert_clubs.py
