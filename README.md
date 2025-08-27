# PDF Combiner Tool

A Python utility to combine multiple PDF files into a single PDF document.

## Features

- Combines all PDF files from a source folder into one PDF
- Maintains the order of files (alphabetical by filename)
- Preserves all pages from each PDF
- Generates timestamped output filenames by default
- Command-line interface with flexible options
- Error handling for corrupted or problematic PDF files

## Requirements

- Python 3.6 or higher
- PyPDF2 library

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

   Or install PyPDF2 directly:

   ```bash
   pip install PyPDF2
   ```

## Usage

### Basic Usage

1. Place your PDF files in the `src/source-pdfs/` folder
2. Run the script from the `src/` directory:

   ```bash
   cd src
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
- `-h, --help`: Show help message and exit

### Examples

```bash
# Use default settings
python combine_pdfs.py

# Specify custom output filename
python combine_pdfs.py -o my_combined_document.pdf

# Use a different source folder
python combine_pdfs.py -s /path/to/my/pdfs

# Enable verbose output
python combine_pdfs.py -v

# Combine all options
python combine_pdfs.py -s custom_folder -o final_document.pdf -v
```

## File Organization

```text
combine-pdfs/
├── README.md
├── requirements.txt
├── LICENSE
└── src/
    ├── combine_pdfs.py      # Main Python script
    └── source-pdfs/         # Place your PDF files here
        ├── document1.pdf    # Example PDF files
        ├── document2.pdf
        └── document3.pdf
```

## How It Works

1. **File Discovery**: The script scans the source folder for all `.pdf` files
2. **Sorting**: Files are processed in alphabetical order by filename
3. **Processing**: Each PDF is opened and all pages are extracted
4. **Combining**: All pages are added to a new PDF document in order
5. **Output**: The combined PDF is saved in the `src/` directory

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

**Permission errors**:

- Ensure you have write permissions in the output directory
- Close any PDF files that might be open in other applications

## License

This project is licensed under the terms specified in the LICENSE file.
