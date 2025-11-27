#!/bin/bash
# Shell script to combine PDFs
# This script runs the PDF combiner from the src directory

echo "======================================"
echo "PDF Combiner Tool"
echo "======================================"
echo

# Check if we're in the right directory
if [ ! -f "combine_pdfs.py" ]; then
    echo "Error: combine_pdfs.py not found in current directory."
    echo "Please run this script from the src folder."
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH."
    echo "Please install Python 3.6 or higher."
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Determine which Python command to use
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # Check if python points to Python 3
    PYTHON_VERSION=$(python -c "import sys; print(sys.version_info.major)")
    if [ "$PYTHON_VERSION" = "3" ]; then
        PYTHON_CMD="python"
    else
        echo "Error: Python 3 is required, but 'python' points to Python 2."
        echo "Please install Python 3 or use 'python3' command."
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "Using Python command: $PYTHON_CMD"

# Check Python version
PYTHON_VERSION_FULL=$($PYTHON_CMD --version 2>&1)
echo "Python version: $PYTHON_VERSION_FULL"

# Check if PyPDF2 is installed
if ! $PYTHON_CMD -c "import PyPDF2" &> /dev/null; then
    echo "PyPDF2 is not installed. Installing now..."
    if ! $PYTHON_CMD -m pip install PyPDF2; then
        echo "Error: Failed to install PyPDF2."
        echo "Please install it manually: $PYTHON_CMD -m pip install PyPDF2"
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo "PyPDF2 installed successfully."
else
    echo "PyPDF2 is already installed."
fi

# Ask user about watermark removal
echo
read -p "Remove watermarks (CamScanner logos)? (y/n): " watermark
read -p "Use advanced OpenCV method? (y/n, default=n): " method

# Run the PDF combiner
echo
echo "Running PDF combiner..."

if [[ "$watermark" =~ ^[Yy]$ ]]; then
    if [[ "$method" =~ ^[Yy]$ ]]; then
        echo "Using advanced OpenCV watermark removal..."
        $PYTHON_CMD combine_pdfs.py --remove-watermarks --watermark-method opencv "$@"
    else
        echo "Using basic watermark removal..."
        $PYTHON_CMD combine_pdfs.py --remove-watermarks "$@"
    fi
else
    echo "Combining PDFs without watermark removal..."
    $PYTHON_CMD combine_pdfs.py "$@"
fi

echo
echo "Done! Check the src directory for your combined PDF file."
echo
read -p "Press Enter to exit..."
