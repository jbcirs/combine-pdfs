# PDF Combiner Tool

A Python utility to combine multiple PDF files into a single PDF document.

## Features

- Combines all PDF files from a source folder into one PDF
- **Watermark removal** for CamScanner and other logos (optional)
- Maintains the order of files (alphabetical by filename)
- Preserves all pages from each PDF
- Generates timestamped output filenames by default
- Command-line interface with flexible options
- Two watermark removal methods: simple crop and advanced OpenCV
- Error handling for corrupted or problematic PDF files

## Requirements

- Python 3.6 or higher
- PyPDF2 library (required)
- Additional libraries for watermark removal (optional):
  - pdfplumber
  - Pillow (PIL)
  - reportlab
  - opencv-python
  - numpy

## Installation

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd combine-pdfs
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Or use the setup script:

   ```bash
   python setup.py
   ```

   For basic PDF combining only (no watermark removal):

   ```bash
   pip install PyPDF2
   ```

## Usage

### Basic Usage

1. Place your PDF files in the `pdfs/source/` folder
2. Run the script from the `scripts/` directory:

   ```bash
   cd scripts
   python combine_pdfs.py
   ```

This will create a combined PDF with an auto-generated filename like `combined_pdfs_20250827_143052.pdf`.

### Command Line Options

```bash
python combine_pdfs.py [options]
```

**Options:**

- `-s, --source FOLDER`: Specify the source folder containing PDF files (default: `source-pdfs`)
- `-o, --output FILENAME`: Specify the output filename (default: auto-generated with timestamp)
- `-v, --verbose`: Enable verbose output for detailed processing information
- `--remove-watermarks`: Attempt to remove watermarks (e.g., CamScanner logos) from PDFs
- `--watermark-method {crop,opencv}`: Method for watermark removal: crop (simple/fast) or opencv (advanced)
- `-h, --help`: Show help message and exit

### Examples

```bash
# Use default settings
python combine_pdfs.py

# Specify custom output filename
python combine_pdfs.py -o my_combined_document.pdf

# Remove watermarks (simple method)
python combine_pdfs.py --remove-watermarks

# Remove watermarks (advanced OpenCV method)
python combine_pdfs.py --remove-watermarks --watermark-method opencv

# Use a different source folder
python combine_pdfs.py -s /path/to/my/pdfs

# Enable verbose output
python combine_pdfs.py -v

# Combine all options
python combine_pdfs.py -s custom_folder -o final_document.pdf --remove-watermarks -v
```

### Using the Batch/Shell Scripts

For easier use, especially on Windows:

```bash
# Windows (from scripts directory)
cd scripts
.\combine_pdfs.bat

# Unix/Linux/macOS (from scripts directory)
cd scripts
./combine_pdfs.sh
```

The scripts will interactively ask about watermark removal options.

## File Organization

```text
combine-pdfs/
├── README.md
├── requirements.txt
├── setup.py                 # Setup script for dependencies
├── WATERMARK_REMOVAL.md     # Detailed watermark removal guide
├── LICENSE
├── scripts/                 # All executable scripts
│   ├── combine_pdfs.py      # Main Python script
│   ├── combine_pdfs.bat     # Windows batch script
│   ├── combine_pdfs.sh      # Unix/Linux/macOS shell script
│   ├── create_test_pdfs.py  # Test PDF generator
│   └── example_usage.py     # Usage examples
└── pdfs/
    ├── source/              # Place your PDF files here
    │   ├── document1.pdf    # Example PDF files
    │   ├── document2.pdf
    │   └── document3.pdf
    └── output/              # Combined PDFs will be saved here
```

## How It Works

1. **File Discovery**: The script scans the `pdfs/source/` folder for all `.pdf` files
2. **Sorting**: Files are processed in alphabetical order by filename
3. **Processing**: Each PDF is opened and all pages are extracted
4. **Combining**: All pages are added to a new PDF document in order
5. **Output**: The combined PDF is saved in the `pdfs/output/` directory

## Error Handling

- The script will display a warning if individual PDF files cannot be processed
- Processing continues with remaining files even if some files fail
- Clear error messages are provided for common issues (missing folder, no PDF files, etc.)

## Tips

- **File Naming**: Use numbered prefixes (e.g., `01_intro.pdf`, `02_chapter1.pdf`) to control the order of combination
- **File Organization**: Keep your source PDFs organized in the `source-pdfs` folder
- **Large Files**: The tool can handle large PDF files, but processing time will increase with file size and number of files

## Troubleshooting

**"No PDF files found"**:

- Ensure your PDF files are in the correct source folder
- Check that files have the `.pdf` extension
- Verify folder permissions

**"PyPDF2 is required but not installed"**:

- Install the dependency: `pip install PyPDF2`

**"Required packages are not installed"** (for watermark removal):

- Install all dependencies: `pip install -r requirements.txt`
- Or run the setup script: `python setup.py`

**Permission errors**:

- Ensure you have write permissions in the output directory
- Close any PDF files that might be open in other applications

**Watermark removal not working**:

- Try the alternative method: `--watermark-method opencv` or `--watermark-method crop`
- Check the WATERMARK_REMOVAL.md guide for detailed troubleshooting
- Ensure all required packages are installed

## Watermark Removal

The tool includes powerful watermark removal features designed specifically for scanned documents with CamScanner or similar watermarks.

### Quick Start

```bash
# Remove watermarks with default (crop) method
python combine_pdfs.py --remove-watermarks

# Use advanced OpenCV method
python combine_pdfs.py --remove-watermarks --watermark-method opencv
```

### Methods

- **Crop Method** (default): Fast, removes bottom 15% of each page where watermarks typically appear
- **OpenCV Method**: Advanced computer vision processing, better for complex watermarks

### Requirements

Watermark removal requires additional packages:
```bash
pip install pdfplumber Pillow reportlab opencv-python numpy
```

For detailed information, see [WATERMARK_REMOVAL.md](WATERMARK_REMOVAL.md)

## License

This project is licensed under the terms specified in the LICENSE file.
