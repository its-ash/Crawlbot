@echo off
echo Starting CrawlBot...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed. Please install Node.js 18 or higher.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo No .env file found. Copying from .env.example...
    copy .env.example .env
    echo Created .env file. Please configure it if needed.
)

REM Create virtual environment
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Install Python dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Install Playwright browsers
echo Installing Playwright browsers...
playwright install chromium

REM Install Node dependencies
echo Installing Node.js dependencies...
cd frontend
if not exist node_modules (
    npm install
)
cd ..

REM Start backend
echo Starting backend server...
start cmd /k "venv\Scripts\activate.bat && uvicorn backend.main:app --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting frontend server...
cd frontend
start cmd /k "npm run dev"
cd ..

echo.
echo CrawlBot is running!
echo.
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers.
pause
