@echo off
echo Running LitReview Setup for Windows...
echo.

REM Check if Python is available
py --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python first.
    echo Download from: https://python.org/downloads
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

REM Run the setup script
py "%~dp0setup.py"

echo.
echo Press any key to exit...
pause >nul