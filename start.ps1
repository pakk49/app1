Write-Host "Starting Medical Analysis System..." -ForegroundColor Green

# Set environment variables
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"

# Install dependencies
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run the application
Write-Host "Starting the server..." -ForegroundColor Green
Write-Host "Please open your browser to http://localhost:8080" -ForegroundColor Cyan
python app.py