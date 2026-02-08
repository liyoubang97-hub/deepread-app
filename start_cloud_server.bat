@echo off
REM DeepRead Cloud Sync Server Startup Script
echo ====================================
echo DeepRead Cloud Sync Server
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing FastAPI and dependencies...
    pip install fastapi uvicorn[standard] requests pydantic
)

REM Start the server
echo.
echo Starting Cloud Sync Server...
echo Server will run at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python cloud_sync_server.py

pause
