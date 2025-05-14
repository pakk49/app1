import os
import sys

# เพิ่ม path ของโฟลเดอร์ src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
