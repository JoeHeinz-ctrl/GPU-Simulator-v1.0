@echo off
REM GPU Simulator - Automated Setup and Run Script for Windows
REM This script will install dependencies and start the application

echo ========================================
echo GPU Simulator - Setup and Run
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/3] Python found:
python --version
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo [2/3] Installing required packages...
echo This may take a few minutes on first run...
echo.

REM Install dependencies
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo [SUCCESS] All packages installed successfully!
echo.

echo [3/3] Starting GPU Simulator...
echo.
echo ========================================
echo Server will start at: http://localhost:8000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python run_server.py

pause
