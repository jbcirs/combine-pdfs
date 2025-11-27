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
    required_packages = [
        ('PyPDF2', 'PyPDF2'),
        ('pdfplumber', 'pdfplumber'), 
        ('Pillow', 'PIL'),
        ('reportlab', 'reportlab'),
        ('opencv-python', 'cv2'),
        ('numpy', 'numpy')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name} is already installed")
        except ImportError:
            print(f"✗ {package_name} is not installed")
            missing_packages.append(package_name)
    
    return len(missing_packages) == 0, missing_packages

def setup_directories():
    """Ensure required directories exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(script_dir, "pdfs", "source")
    output_dir = os.path.join(script_dir, "pdfs", "output")
    
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
        print(f"✓ Created source directory: {source_dir}")
    else:
        print(f"✓ Source directory exists: {source_dir}")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✓ Created output directory: {output_dir}")
    else:
        print(f"✓ Output directory exists: {output_dir}")
    
    return True

def main():
    """Run the setup process."""
    print("=== PDF Combiner Tool Setup ===\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    dependencies_ok, missing_packages = check_dependencies()
    
    if not dependencies_ok:
        print("\nInstalling missing dependencies...")
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✓ {package} installed successfully")
            else:
                print(f"✗ Failed to install {package}")
                print("Please try installing manually: pip install -r requirements.txt")
                sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    print("\n=== Setup Complete ===")
    print("The PDF Combiner Tool is ready to use!")
    print("\nNext steps:")
    print("1. Add PDF files to the 'pdfs/source' folder")
    print("2. Navigate to scripts: cd scripts")
    print("3. Run: python combine_pdfs.py")
    print("   Or with watermark removal: python combine_pdfs.py --remove-watermarks")
    print("4. Check the output in the 'pdfs/output' directory")
    print("\nFor help, run: python combine_pdfs.py --help")
    print("For watermark removal details, see WATERMARK_REMOVAL.md")

if __name__ == "__main__":
    main()
