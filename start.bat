@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Starting server...
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1
python -m flask run --host=0.0.0.0 --port=8080
pause