#!/usr/bin/env python3
"""
PDF Combiner Tool

This script combines all PDF files from the source-pdfs folder into a single PDF file.
The output file will be saved in the same directory as this script.
"""

import os
import glob
from pathlib import Path
from datetime import datetime
import argparse
import sys

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("Error: PyPDF2 is required but not installed.")
    print("Please install it using: pip install PyPDF2")
    sys.exit(1)


def get_pdf_files(source_folder):
    """
    Get all PDF files from the source folder.
    
    Args:
        source_folder (str): Path to the folder containing source PDFs
        
    Returns:
        list: List of PDF file paths sorted alphabetically
    """
    pdf_pattern = os.path.join(source_folder, "*.pdf")
    pdf_files = glob.glob(pdf_pattern)
    return sorted(pdf_files)


def combine_pdfs(source_folder, output_filename=None):
    """
    Combine all PDF files from the source folder into a single PDF.
    
    Args:
        source_folder (str): Path to the folder containing source PDFs
        output_filename (str, optional): Name of the output file. If None, 
                                       generates a timestamped filename.
        
    Returns:
        str: Path to the created combined PDF file
    """
    # Get all PDF files
    pdf_files = get_pdf_files(source_folder)
    
    if not pdf_files:
        raise ValueError(f"No PDF files found in {source_folder}")
    
    print(f"Found {len(pdf_files)} PDF files to combine:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"  {i}. {os.path.basename(pdf_file)}")
    
    # Create output filename if not provided
    if output_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"combined_pdfs_{timestamp}.pdf"
    
    # Ensure output filename has .pdf extension
    if not output_filename.lower().endswith('.pdf'):
        output_filename += '.pdf'
    
    # Create the output path in the src directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_filename)
    
    # Create PDF writer object
    pdf_writer = PdfWriter()
    
    # Add pages from each PDF file
    for pdf_file in pdf_files:
        try:
            print(f"Processing: {os.path.basename(pdf_file)}")
            pdf_reader = PdfReader(pdf_file)
            
            # Add all pages from the current PDF
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
                
        except Exception as e:
            print(f"Warning: Could not process {pdf_file}: {str(e)}")
            continue
    
    # Write the combined PDF
    try:
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)
        
        print(f"\nSuccess! Combined PDF created: {output_path}")
        print(f"Total pages in combined PDF: {len(pdf_writer.pages)}")
        return output_path
        
    except Exception as e:
        raise Exception(f"Failed to write combined PDF: {str(e)}")


def main():
    """Main function to handle command line arguments and execute PDF combination."""
    parser = argparse.ArgumentParser(
        description="Combine multiple PDF files into a single PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python combine_pdfs.py                    # Use default source folder and filename
  python combine_pdfs.py -o my_combined.pdf # Specify output filename
  python combine_pdfs.py -s /path/to/pdfs   # Specify source folder
        """
    )
    
    parser.add_argument(
        '-s', '--source',
        default='source-pdfs',
        help='Source folder containing PDF files (default: source-pdfs)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output filename for the combined PDF (default: auto-generated with timestamp)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Get the absolute path of the source folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if os.path.isabs(args.source):
        source_folder = args.source
    else:
        source_folder = os.path.join(script_dir, args.source)
    
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(source_folder):
        print(f"Error: '{source_folder}' is not a directory.")
        sys.exit(1)
    
    try:
        if args.verbose:
            print(f"Source folder: {source_folder}")
            print(f"Output filename: {args.output or 'auto-generated'}")
        
        output_path = combine_pdfs(source_folder, args.output)
        
        if args.verbose:
            file_size = os.path.getsize(output_path)
            print(f"Output file size: {file_size:,} bytes")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
