@echo off
REM Quick Start Script for Student Dropout Prediction & Counselling System
REM Run this script to start the Flask application

echo ============================================================
echo STUDENT DROPOUT PREDICTION & COUNSELLING SYSTEM
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install/upgrade dependencies
echo Checking dependencies...
pip install -r requirements.txt --quiet
echo.

REM Check if database exists
if not exist "database.db" (
    echo Initializing database...
    python init_db.py
    echo.
) else (
    echo Database already initialized.
    echo.
)

REM Get local IP address
echo Finding local IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set LOCAL_IP=%%b
        goto :found
    )
)
:found

echo ============================================================
echo Starting Flask Application...
echo ============================================================
echo.
echo Access the application at:
echo   Local:  http://localhost:5000
echo   Network: http:%LOCAL_IP%:5000
echo.
echo Default Login Credentials:
echo   Admin:   username = admin,    password = admin123
echo   Staff:   username = staff,    password = staff123
echo   Student: username = REG-2023-001, password = student123
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Start Flask app
python app.py
