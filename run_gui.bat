@echo off
REM FT-897 Memory Manager - Windows Launcher
REM ==========================================

echo ======================================================
echo FT-897 Memory Manager - Tkinter GUI
echo ======================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or newer from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

echo Starting GUI application...
echo.

REM Run the Tkinter GUI (no dependencies needed!)
python ft897_gui_tkinter.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start
    echo.
    pause
)
