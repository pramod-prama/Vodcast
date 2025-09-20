@echo off
echo Setting up SadTalker Frontend Demo...
echo.

echo Installing dependencies...
call npm install

if %ERRORLEVEL% neq 0 (
    echo Error installing dependencies!
    pause
    exit /b 1
)

echo.
echo Setup complete!
echo.
echo To start the frontend demo:
echo 1. Make sure the SadTalker API server is running (python simple_api_server.py)
echo 2. Run: npm start
echo 3. Open http://localhost:3000 in your browser
echo.
pause
