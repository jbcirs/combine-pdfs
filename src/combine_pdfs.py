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
    import pdfplumber
    from PIL import Image, ImageDraw
    import cv2
    import numpy as np
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import io
except ImportError as e:
    print(f"Error: Required packages are not installed.")
    print(f"Missing: {e.name}")
    print("Please install all requirements using: pip install -r requirements.txt")
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


def remove_watermark_region(pdf_path, output_path, bottom_height_percent=15):
    """
    Remove watermark from bottom region of PDF pages.
    
    Args:
        pdf_path (str): Path to input PDF
        output_path (str): Path for output PDF
        bottom_height_percent (int): Percentage of page height to crop from bottom
    
    Returns:
        str: Path to the processed PDF
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pdf_writer = PdfWriter()
            
            for page_num, page in enumerate(pdf.pages):
                # Convert page to image
                img = page.to_image(resolution=200)
                
                # Get the actual PIL image from PageImage object
                pil_img = img.original
                
                # Crop bottom portion
                img_width, img_height = pil_img.size
                crop_bottom = int(img_height * (bottom_height_percent / 100))
                
                # Crop the image (remove bottom portion)
                cropped_img = pil_img.crop((0, 0, img_width, img_height - crop_bottom))
                
                # Save cropped image to bytes
                img_bytes = io.BytesIO()
                cropped_img.save(img_bytes, format='PDF')
                img_bytes.seek(0)
                
                # Read the cropped image as PDF and add to writer
                cropped_pdf = PdfReader(img_bytes)
                if len(cropped_pdf.pages) > 0:
                    pdf_writer.add_page(cropped_pdf.pages[0])
            
            # Write the processed PDF
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return output_path
            
    except Exception as e:
        print(f"Warning: Could not remove watermark from {pdf_path}: {str(e)}")
        # If watermark removal fails, copy original file
        import shutil
        shutil.copy2(pdf_path, output_path)
        return output_path


def remove_watermark_opencv(pdf_path, output_path):
    """
    Advanced watermark removal using OpenCV for image processing.
    
    Args:
        pdf_path (str): Path to input PDF
        output_path (str): Path for output PDF
    
    Returns:
        str: Path to the processed PDF
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pdf_writer = PdfWriter()
            
            for page_num, page in enumerate(pdf.pages):
                # Convert page to image with high resolution
                img = page.to_image(resolution=300)
                
                # Get the actual PIL image from PageImage object
                pil_img = img.original
                
                # Convert PIL image to OpenCV format
                opencv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                
                # Remove bottom 15% of the image (common watermark location)
                height, width = opencv_img.shape[:2]
                crop_height = int(height * 0.85)  # Keep top 85%
                cropped_img = opencv_img[0:crop_height, 0:width]
                
                # Optional: Apply additional filtering to remove text-like watermarks
                # This is aggressive and might remove legitimate content
                # Uncomment if needed:
                # gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                # _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
                # cropped_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
                
                # Convert back to PIL Image
                processed_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
                
                # Convert to PDF page
                img_bytes = io.BytesIO()
                processed_img.save(img_bytes, format='PDF')
                img_bytes.seek(0)
                
                # Add to PDF writer
                processed_pdf = PdfReader(img_bytes)
                if len(processed_pdf.pages) > 0:
                    pdf_writer.add_page(processed_pdf.pages[0])
            
            # Write the processed PDF
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return output_path
            
    except Exception as e:
        print(f"Warning: Could not process {pdf_path} with OpenCV: {str(e)}")
        # Fallback to simple crop method
        return remove_watermark_region(pdf_path, output_path)


def combine_pdfs(source_folder, output_filename=None, remove_watermarks=False, watermark_method='crop'):
    """
    Combine all PDF files from the source folder into a single PDF.
    
    Args:
        source_folder (str): Path to the folder containing source PDFs
        output_filename (str, optional): Name of the output file. If None, 
                                       generates a timestamped filename.
        remove_watermarks (bool): Whether to attempt watermark removal
        watermark_method (str): Method to use ('crop' or 'opencv')
        
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
            
            # Process file for watermark removal if requested
            if remove_watermarks:
                temp_file = os.path.join(script_dir, f"temp_{os.path.basename(pdf_file)}")
                
                if watermark_method == 'opencv':
                    processed_file = remove_watermark_opencv(pdf_file, temp_file)
                else:
                    processed_file = remove_watermark_region(pdf_file, temp_file)
                
                pdf_reader = PdfReader(processed_file)
                
                # Clean up temporary file
                try:
                    os.remove(temp_file)
                except:
                    pass
            else:
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
  python combine_pdfs.py --remove-watermarks # Remove watermarks using crop method
  python combine_pdfs.py --remove-watermarks --watermark-method opencv # Advanced removal
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
    
    parser.add_argument(
        '--remove-watermarks',
        action='store_true',
        help='Attempt to remove watermarks (e.g., CamScanner logos) from PDFs'
    )
    
    parser.add_argument(
        '--watermark-method',
        choices=['crop', 'opencv'],
        default='crop',
        help='Method for watermark removal: crop (simple) or opencv (advanced)'
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
        
        if args.remove_watermarks:
            print(f"Watermark removal enabled using method: {args.watermark_method}")
        
        output_path = combine_pdfs(
            source_folder, 
            args.output, 
            remove_watermarks=args.remove_watermarks,
            watermark_method=args.watermark_method
        )
        
        if args.verbose:
            file_size = os.path.getsize(output_path)
            print(f"Output file size: {file_size:,} bytes")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
