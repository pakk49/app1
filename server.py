import os
import sys

# เพิ่ม path ของโฟลเดอร์ src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from waitress import serve
from app import app
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"เริ่มต้นเซิร์ฟเวอร์ที่ http://localhost:{port}")
    serve(app, host='0.0.0.0', port=port)
