@echo off
REM Windows batch script to combine PDFs
REM This script runs the PDF combiner from the src directory

echo ======================================
echo PDF Combiner Tool
echo ======================================
echo.

REM Check if we're in the right directory
if not exist "combine_pdfs.py" (
    echo Error: combine_pdfs.py not found in current directory.
    echo Please run this script from the src folder.
    echo.
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.6 or higher.
    echo.
    pause
    exit /b 1
)

REM Check if PyPDF2 is installed
python -c "import PyPDF2" >nul 2>&1
if %errorlevel% neq 0 (
    echo PyPDF2 is not installed. Installing now...
    pip install PyPDF2
    REM Check again if PyPDF2 was actually installed
    python -c "import PyPDF2" >nul 2>&1
    if %errorlevel% neq 0 (
        echo Error: Failed to install PyPDF2.
        echo Please install it manually: pip install PyPDF2
        echo.
        pause
        exit /b 1
    ) else (
        echo PyPDF2 installed successfully!
    )
)

REM Ask user about watermark removal
echo.
set /p watermark="Remove watermarks (CamScanner logos)? (y/n): "
set /p method="Use advanced OpenCV method? (y/n, default=n): "

REM Run the PDF combiner
echo.
echo Running PDF combiner...

if /i "%watermark%"=="y" (
    if /i "%method%"=="y" (
        echo Using advanced OpenCV watermark removal...
        python combine_pdfs.py --remove-watermarks --watermark-method opencv %*
    ) else (
        echo Using basic watermark removal...
        python combine_pdfs.py --remove-watermarks %*
    )
) else (
    echo Combining PDFs without watermark removal...
    python combine_pdfs.py %*
)

echo.
echo Done! Check the src directory for your combined PDF file.
echo.
pause
