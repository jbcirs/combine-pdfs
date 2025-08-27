#!/usr/bin/env python3
"""
Setup script for PDF Combiner Tool

This script helps set up the environment and install dependencies.
"""

import subprocess
import sys
import os

def install_package(package_name):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package_name}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(f"Error: Python 3.6 or higher is required. You have Python {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import PyPDF2
        print("✓ PyPDF2 is already installed")
        return True
    except ImportError:
        print("✗ PyPDF2 is not installed")
        return False

def setup_directories():
    """Ensure required directories exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(script_dir, "source-pdfs")
    
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
        print(f"✓ Created source directory: {source_dir}")
    else:
        print(f"✓ Source directory exists: {source_dir}")
    
    return True

def main():
    """Run the setup process."""
    print("=== PDF Combiner Tool Setup ===\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    dependencies_ok = check_dependencies()
    
    if not dependencies_ok:
        print("\nInstalling required dependencies...")
        if install_package("PyPDF2"):
            print("✓ PyPDF2 installed successfully")
        else:
            print("✗ Failed to install PyPDF2")
            print("Please try installing manually: pip install PyPDF2")
            sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    print("\n=== Setup Complete ===")
    print("The PDF Combiner Tool is ready to use!")
    print("\nNext steps:")
    print("1. Add PDF files to the 'source-pdfs' folder")
    print("2. Run: python combine_pdfs.py")
    print("3. Check the output in this directory")
    print("\nFor help, run: python combine_pdfs.py --help")

if __name__ == "__main__":
    main()
