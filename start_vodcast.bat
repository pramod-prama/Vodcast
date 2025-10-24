@echo off
echo ========================================
echo    🎭 Prama Vodcast - Auto Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

:: Check if we're in the right directory
if not exist "real_api_server.py" (
    echo ❌ Please run this file from the Vodcast project directory
    echo    Current directory: %CD%
    pause
    exit /b 1
)

echo ✅ Project directory found
echo.

:: Install/Update dependencies
echo 📦 Installing/Updating dependencies...
echo.

:: Install YouTube dependencies
echo Installing YouTube API dependencies...
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib --quiet

:: Install other dependencies
echo Installing other dependencies...
pip install flask flask-cors werkzeug requests --quiet
pip install google-cloud-storage google-cloud-texttospeech --quiet
pip install imageio imageio-ffmpeg librosa scipy scikit-image --quiet
pip install opencv-python pillow tqdm pyyaml joblib --quiet

:: Fix NumPy compatibility
echo Fixing NumPy compatibility...
echo Installing compatible versions for Python 3.13...
pip install numpy==1.24.4 --only-binary=all --quiet
pip install opencv-python-headless==4.8.1.78 --quiet
pip install numba==0.58.1 --quiet

echo ✅ Dependencies installed
echo.

:: Check for YouTube credentials
if not exist "youtube_client_secrets.json" (
    echo ⚠️  YouTube credentials not found!
    echo    Please follow YOUTUBE_SETUP_GUIDE.md to setup YouTube integration
    echo    Or run without YouTube upload for now
    echo.
)

:: Check for Google Cloud credentials
if not exist "revoiz-ai-dd6bb5e7b3ee.json" (
    echo ⚠️  Google Cloud credentials not found!
    echo    TTS and GCS features may not work
    echo.
)

:: Create necessary directories
if not exist "uploads" mkdir uploads
if not exist "results" mkdir results

echo ✅ Directories created
echo.

:: Start the API server
echo 🚀 Starting SadTalker API Server...
echo    Server will be available at: http://localhost:7860
echo    Frontend (demo.html) will auto-open now
echo.
echo 📝 Available endpoints:
echo    - GET  /api/health - Health check
echo    - POST /api/text-to-speech - Convert text to speech
echo    - POST /api/jobs - Create a new job
echo    - GET  /api/jobs - List all jobs
echo    - GET  /api/jobs/^<job_id^> - Get job status
echo    - GET  /api/youtube/auth - Initialize YouTube OAuth
echo    - POST /api/youtube/auth/callback - Complete YouTube OAuth
echo.
echo 🎥 YouTube Integration:
echo    - Set upload_to_youtube=true in job creation
echo    - Provide youtube_title, youtube_description, youtube_tags, youtube_privacy
echo    - Videos will be uploaded to your YouTube channel after generation
echo.
echo ⚠️  Press Ctrl+C to stop the server
echo ========================================
echo.

:: Auto-open frontend (demo.html)
if exist "sadtalker-frontend-demo\demo.html" (
    echo 🌐 Opening frontend: sadtalker-frontend-demo\demo.html
    start "" "%CD%\sadtalker-frontend-demo\demo.html"
) else (
    echo ⚠️  demo.html not found at sadtalker-frontend-demo\demo.html
)

:: Start the server
python real_api_server.py

:: If server stops, show message
echo.
echo ========================================
echo 🛑 Server stopped
echo ========================================
pause
