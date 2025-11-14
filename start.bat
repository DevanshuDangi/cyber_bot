@echo off
REM Start script for Windows - 1930 Cyber Crime Helpline WhatsApp Chatbot

echo.
echo ==========================================
echo   Starting 1930 Cyber Crime Helpline
echo   WhatsApp Chatbot Servers
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found. Please run setup first.
    echo Run: python setup.py
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo [ERROR] .env file not found. Please run setup first.
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo [INFO] Starting backend server (FastAPI) on http://localhost:8000...
start "Backend Server" cmd /k "uvicorn backend.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo [INFO] Starting frontend server (React) on http://localhost:5173...
cd admin-ui
start "Frontend Server" cmd /k "npm run dev"
cd ..

echo.
echo ==========================================
echo   Servers Running Successfully!
echo ==========================================
echo.
echo [SUCCESS] Backend API: http://localhost:8000
echo [SUCCESS] Frontend UI: http://localhost:5173
echo [SUCCESS] API Docs: http://localhost:8000/docs
echo.
echo [INFO] Servers are running in separate windows
echo [INFO] Close the windows to stop the servers
echo.
pause

