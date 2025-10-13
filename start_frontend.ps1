# PowerShell script to run the frontend
# Usage: .\start_frontend.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Multi-Modal AI Chatbot Frontend" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "✓ Activating virtual environment..." -ForegroundColor Green
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "! Virtual environment not found" -ForegroundColor Yellow
    Write-Host "  Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Check if requirements are installed
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Cyan
$requirementsCheck = pip list | Select-String "gradio"
if (-not $requirementsCheck) {
    Write-Host "! Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✓ Requirements installed" -ForegroundColor Green
} else {
    Write-Host "✓ Dependencies already installed" -ForegroundColor Green
}

# Check if API URL is configured
$apiUrlCheck = Select-String -Path ".\frontend_app.py" -Pattern "YOUR_NGROK_URL_HERE"
if ($apiUrlCheck) {
    Write-Host ""
    Write-Host "⚠️  WARNING: API_URL not configured!" -ForegroundColor Red
    Write-Host "   Please update API_URL in frontend_app.py with your ngrok URL" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to continue anyway or Ctrl+C to exit"
}

# Start the frontend
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Starting Frontend Application..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The app will open at: http://localhost:7860" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python frontend_app.py
