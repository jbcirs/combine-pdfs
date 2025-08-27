#!/usr/bin/env python3
"""
Example usage script for the PDF combiner tool.

This script demonstrates different ways to use the combine_pdfs.py module.
"""

import os
import sys
from combine_pdfs import combine_pdfs, get_pdf_files

def main():
    """Demonstrate different usage patterns of the PDF combiner."""
    
    print("=== PDF Combiner Example ===\n")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_folder = os.path.join(script_dir, "source-pdfs")
    
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist.")
        print("Please create the folder and add some PDF files to test.")
        return
    
    # Check for PDF files
    pdf_files = get_pdf_files(source_folder)
    
    if not pdf_files:
        print(f"No PDF files found in '{source_folder}'.")
        print("Please add some PDF files to test the combiner.")
        print("\nExample files you could add:")
        print("- 01_document.pdf")
        print("- 02_document.pdf")
        print("- 03_document.pdf")
        return
    
    print(f"Found {len(pdf_files)} PDF files in the source folder:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"  {i}. {os.path.basename(pdf_file)}")
    
    print("\n" + "="*50)
    print("EXAMPLE 1: Basic combination with default filename")
    print("="*50)
    
    try:
        output_path = combine_pdfs(source_folder)
        print(f"✓ Success! Combined PDF created at: {output_path}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*50)
    print("EXAMPLE 2: Combination with custom filename")
    print("="*50)
    
    try:
        custom_filename = "my_custom_combined_document.pdf"
        output_path = combine_pdfs(source_folder, custom_filename)
        print(f"✓ Success! Custom named PDF created at: {output_path}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*50)
    print("EXAMPLE 3: File information")
    print("="*50)
    
    # Show file sizes and information
    for pdf_file in pdf_files:
        try:
            file_size = os.path.getsize(pdf_file)
            print(f"File: {os.path.basename(pdf_file)}")
            print(f"  Size: {file_size:,} bytes")
            print(f"  Path: {pdf_file}")
        except Exception as e:
            print(f"  Error reading file info: {e}")
    
    print("\nExample completed! Check the output files in the src directory.")

if __name__ == "__main__":
    main()
