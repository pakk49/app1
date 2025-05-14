@echo off
@echo off
cls
echo ================================================
echo            ระบบวิเคราะห์อาการเจ็บป่วย
echo ================================================
echo.
echo [1/4] กำลังตรวจสอบสภาพแวดล้อม...

REM สร้าง virtual environment ถ้ายังไม่มี
if not exist "venv" (
    echo สร้าง Virtual Environment...
    python -m venv venv
)

REM เปิดใช้งาน virtual environment
call venv\Scripts\activate.bat

echo [2/4] กำลังติดตั้งแพ็คเกจที่จำเป็น...
pip install -r requirements.txt

echo [3/4] กำลังตั้งค่าระบบ...

REM ตั้งค่า environment variables
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1

echo [4/4] กำลังเริ่มต้นเซิร์ฟเวอร์...
echo.
echo ================================================
echo  เปิดเบราว์เซอร์ไปที่ http://localhost:8080
echo  เพื่อเริ่มใช้งานระบบวิเคราะห์อาการเจ็บป่วย
echo ================================================
echo.
echo * กด Ctrl+C เพื่อปิดเซิร์ฟเวอร์
echo.

REM รันแอปพลิเคชัน
python app.py
pause