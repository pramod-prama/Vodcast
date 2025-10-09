@echo off
echo 🚀 Starting SadTalker API Server...
echo.
echo 📋 Prerequisites Check:
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python 3.8+ and try again
    pause
    exit /b 1
)
echo ✅ Python is installed

REM Check if requirements are installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Flask not found. Installing requirements...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
)
echo ✅ Dependencies are installed

REM Check if credentials file exists
if not exist "revoiz-ai-dd6bb5e7b3ee.json" (
    echo ❌ Google Cloud credentials file not found
    echo    Please ensure revoiz-ai-dd6bb5e7b3ee.json is in the project directory
    pause
    exit /b 1
)
echo ✅ Google Cloud credentials found

REM Check if gcs_credentials.json exists, if not copy from revoiz file
if not exist "gcs_credentials.json" (
    echo 📋 Creating gcs_credentials.json...
    copy "revoiz-ai-dd6bb5e7b3ee.json" "gcs_credentials.json"
    echo ✅ gcs_credentials.json created
)

echo.
echo 🎯 Starting API Server...
echo    Server will be available at: http://localhost:7860
echo    Frontend demo: sadtalker-frontend-demo/demo.html
echo.
echo 💡 Press Ctrl+C to stop the server
echo.

REM Start the server
python real_api_server.py

echo.
echo 👋 Server stopped. Press any key to exit...
pause >nul
