# Source PDFs Folder

This folder is where you should place all the PDF files that you want to combine into a single document.

## Instructions

1. **Add your PDF files**: Copy or move all the PDF files you want to combine into this folder.

2. **File naming**: For best results, name your files with prefixes to control the order:
   - `01_introduction.pdf`
   - `02_chapter1.pdf`
   - `03_chapter2.pdf`
   - `04_conclusion.pdf`

3. **Run the script**: From the parent `src/` directory, run:

   ```bash
   python combine_pdfs.py
   ```

## File Organization Tips

- **Use numbered prefixes** (01, 02, 03, etc.) to ensure proper ordering
- **Keep file names descriptive** to easily identify content
- **Avoid special characters** in filenames that might cause issues
- **Check file integrity** - ensure all PDFs can be opened before combining

## Example Structure

```text
source-pdfs/
├── 01_cover_page.pdf
├── 02_table_of_contents.pdf
├── 03_introduction.pdf
├── 04_methodology.pdf
├── 05_results.pdf
├── 06_discussion.pdf
├── 07_conclusion.pdf
└── 08_references.pdf
```

## Processing Order

Files are processed in **alphabetical order** by filename. This means:

- `document1.pdf` comes before `document2.pdf`
- `a_file.pdf` comes before `b_file.pdf`
- Numbers are sorted as strings: `10_file.pdf` comes before `2_file.pdf`
  - To avoid this, use zero-padding: `02_file.pdf`, `10_file.pdf`

## Supported File Types

- Only `.pdf` files are processed
- All other file types in this folder will be ignored
- Both single-page and multi-page PDFs are supported

## Output Location

The combined PDF will be created in the parent `src/` directory with a filename like:

- `combined_pdfs_YYYYMMDD_HHMMSS.pdf` (default)
- Or your custom filename if specified with the `-o` option

## Troubleshooting

If you encounter issues:

1. **Check file permissions**: Ensure you can read the PDF files
2. **Verify PDF integrity**: Try opening each PDF individually
3. **Check filename encoding**: Avoid special characters or non-ASCII names
4. **File size considerations**: Very large PDFs may take longer to process

## Need Help?

Refer to the main README.md file in the project root for complete usage instructions and troubleshooting guide.
