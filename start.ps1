Clear-Host
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "            ระบบวิเคราะห์อาการเจ็บป่วย            " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] กำลังตรวจสอบสภาพแวดล้อม..." -ForegroundColor Yellow

# Set environment variables
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"

# Install dependencies
Write-Host "[2/4] กำลังติดตั้งแพ็คเกจที่จำเป็น..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "[3/4] กำลังตั้งค่าระบบ..." -ForegroundColor Yellow

# Run the application
Write-Host "[4/4] กำลังเริ่มต้นเซิร์ฟเวอร์..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  เปิดเบราว์เซอร์ไปที่ http://localhost:8080" -ForegroundColor White
Write-Host "  เพื่อเริ่มใช้งานระบบวิเคราะห์อาการเจ็บป่วย" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "* กด Ctrl+C เพื่อปิดเซิร์ฟเวอร์" -ForegroundColor Red
Write-Host ""

python app.py