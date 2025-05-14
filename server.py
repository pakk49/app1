from waitress import serve
from app import app

if __name__ == '__main__':
    print("เริ่มต้นเซิร์ฟเวอร์ที่ http://localhost:8080")
    serve(app, host='127.0.0.1', port=8080, threads=6)
