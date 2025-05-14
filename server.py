import os
import sys
from waitress import serve

# เพิ่ม path ของโปรเจค
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app

if __name__ == '__main__':
    print("Starting server on http://localhost:8080")
    serve(app, host='0.0.0.0', port=8080)
