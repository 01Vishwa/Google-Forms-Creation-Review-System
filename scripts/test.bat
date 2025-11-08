@echo off
REM ====================================
REM Google Forms System - Run All Tests
REM ====================================

echo.
echo ========================================
echo   Running Backend Unit Tests
echo ========================================
echo.

cd backend

REM Check if pytest is installed
pip show pytest >nul 2>&1
if errorlevel 1 (
    echo [WARNING] pytest not found, installing...
    pip install pytest pytest-asyncio requests
    echo.
)

echo Running test suite...
echo.

pytest test_surveys.py -v --tb=short --color=yes

if errorlevel 1 (
    echo.
    echo ========================================
    echo   Tests Failed! ❌
    echo ========================================
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo   All Tests Passed! ✅
    echo ========================================
    echo.
)

cd ..

echo.
echo Test execution complete.
echo.
pause
