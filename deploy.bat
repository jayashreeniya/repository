@echo off
REM Niya Sales Agent - Windows Deployment Script
REM This script automates the setup and deployment process on Windows

echo 🚀 Niya Sales Agent - Deployment Script
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✅ pip found:
pip --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo ✅ Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ✅ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo ✅ Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo Please create .env file with your credentials
    pause
    exit /b 1
) else (
    echo ✅ Environment file found
)

REM Check if Gmail service account file exists
if not exist "gmail-service.json" (
    echo ⚠️  gmail-service.json not found
    echo ⚠️  Please download your Gmail service account JSON file and place it in the project directory
)

REM Run setup test
echo 🧪 Running setup test...
python test_setup.py

REM Check if Docker is available
docker --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Docker found. You can also deploy using Docker:
    echo   docker-compose up -d
) else (
    echo ⚠️  Docker not found. You can install Docker for containerized deployment.
)

echo.
echo 🤖 Starting Niya Sales Agent...
echo Press Ctrl+C to stop the agent
echo.

python niya_agent.py

echo.
echo 🎉 Deployment completed!
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Add your gmail-service.json file
echo 3. Run: python niya_agent.py
echo.
echo For testing: python test_setup.py
echo For help: python niya_agent.py --help
echo.
pause 