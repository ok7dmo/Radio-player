@echo off
REM FT-897 Image Dump Tool - Windows Launcher
REM This tool analyzes your CHIRP image file to diagnose detection issues

echo ========================================
echo FT-897 Image Dump Tool
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if image file is provided
if "%~1"=="" (
    echo Usage: dump_image.bat ^<path-to-image.dat^>
    echo.
    echo Example: dump_image.bat C:\Users\YourName\Documents\ft897.dat
    echo.
    echo Or drag and drop your image file onto this .bat file
    echo.
    pause
    exit /b 1
)

echo Analyzing image file: %~1
echo.

REM Run the dump tool and save output to a text file
set OUTPUT_FILE=%~n1_dump.txt
python ft897_dump_channels.py "%~1" > "%OUTPUT_FILE%"

echo.
echo ========================================
echo Analysis complete!
echo.
echo Output saved to: %OUTPUT_FILE%
echo.
echo Please send this file to help diagnose the issue.
echo ========================================
echo.

REM Open the output file
notepad "%OUTPUT_FILE%"

pause
