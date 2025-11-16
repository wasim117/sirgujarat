# PDF Thumbnail Extractor

A Python script that automatically extracts the first page from PDF files and saves them as JPEG thumbnail images. Perfect for generating preview images for PDF documents in web applications or file management systems.

## Features

- 📄 Batch processing of multiple PDF files
- 🖼️ High-quality JPEG output with configurable DPI
- ✂️ Image cropping to extract specific regions (e.g., address sections)
- 🎯 Automatic handling of transparency (white background)
- 📊 Progress tracking and detailed reporting
- 🛡️ Robust error handling (continues processing even if some files fail)
- 📁 Automatic output directory creation
- 🔄 Independent or combined workflows (extract, crop, or both)

## Requirements

### System Requirements

- Python 3.7 or higher
- Sufficient disk space for output images

### Python Dependencies

- **PyMuPDF** (fitz) >= 1.23.0 - For PDF rendering and page extraction
- **Pillow** (PIL) >= 10.0.0 - For image processing and JPEG conversion

## Installation

### Step 1: Clone or Download the Script

Download `extract_pdf_thumbnails.py` to your project directory.

### Step 2: Install Dependencies

#### Option A: Using pip directly

```bash
pip install PyMuPDF Pillow
```

#### Option B: Using requirements.txt

1. Ensure `requirements.txt` exists with the following content:
```
PyMuPDF>=1.23.0
Pillow>=10.0.0
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

#### Option C: Using a virtual environment (recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

The script provides three independent workflows:

#### 1. Extract and Crop (Default - Combined Workflow)

Process PDFs and automatically crop to address region:

```bash
python extract_pdf_thumbnails.py
```

This runs `main_extract_and_crop()` which:
- Extracts first page from PDFs in `P064` → `public/images/p064`
- Crops extracted images to address region → `public/address-images/p064`

#### 2. Extract Only (Without Cropping)

Extract PDF thumbnails without cropping:

```python
from extract_pdf_thumbnails import main_extract_only

main_extract_only()
```

Or create a script:
```python
# extract_only.py
from extract_pdf_thumbnails import main_extract_only

if __name__ == "__main__":
    main_extract_only()
```

#### 3. Crop Only (Process Existing Images)

Crop existing images independently:

```python
from extract_pdf_thumbnails import main_crop_only

main_crop_only()
```

Or create a script:
```python
# crop_only.py
from extract_pdf_thumbnails import main_crop_only

if __name__ == "__main__":
    main_crop_only()
```

### Custom Configuration

#### Customize PDF Extraction

Modify `main_extract_only()` or `main_extract_and_crop()`:

```python
def main_extract_only():
    source_dir = 'P064'                    # Change source directory
    output_dir = 'public/images/p064'      # Change output directory
    dpi = 150                              # Change resolution (72-300)
    
    result = process_pdf_directory(source_dir, output_dir, address_output_dir=None, dpi=dpi)
```

#### Customize Image Cropping

Modify `main_crop_only()` or use `process_image_cropping()` directly:

```python
from extract_pdf_thumbnails import process_image_cropping

# Custom crop coordinates
result = process_image_cropping(
    source_dir='public/images/p064',
    output_dir='public/custom-crop',
    left=100,      # Left coordinate
    top=200,       # Top coordinate
    width=800,     # Width of crop region
    height=400     # Height of crop region
)
```

### DPI Settings

- **72 DPI**: Low quality, smallest file size
- **150 DPI**: Good balance (default, recommended)
- **200 DPI**: High quality, larger files
- **300 DPI**: Print quality, very large files

## Output

### File Naming Convention

The script preserves the original PDF filename and changes the extension:

- Input: `P064/P0640001.pdf`
- Full page output: `public/images/p064/P0640001.jpg`
- Cropped address output: `public/address-images/p064/P0640001.jpg`

### Image Format

- **Format**: JPEG
- **Quality**: 85% (optimized)
- **Color Mode**: RGB
- **Background**: White (for PDFs with transparency)

### Crop Coordinates (Default)

The default cropping extracts the address region:
- **Left**: 133 pixels
- **Top**: 425 pixels
- **Width**: 1058 pixels
- **Height**: 393 pixels

### Processing Summary

#### Extract and Crop (Combined)

```
==========================================================
PROCESSING SUMMARY
==========================================================
Total files processed:  601
Successfully processed: 598
Failed:                 3
Cropped successfully:   598
Cropping failed:        0
Total time:             45.23 seconds
Output directory:       public/images/p064
Address output dir:     public/address-images/p064
==========================================================
```

#### Extract Only

```
==========================================================
PDF EXTRACTION SUMMARY
==========================================================
Total files processed:  601
Successfully processed: 598
Failed:                 3
Total time:             42.15 seconds
Output directory:       public/images/p064
==========================================================
```

#### Crop Only

```
==========================================================
IMAGE CROPPING SUMMARY
==========================================================
Total files processed:  601
Successfully cropped:   598
Failed:                 3
Total time:             38.54 seconds
Output directory:       public/address-images/p064
==========================================================
```

If any files fail, detailed error information is displayed:

```
DETAILED ERROR LIST:
------------------------------------------------------------
1. P0640123.pdf
   Error: Corrupted or invalid PDF file
2. P0640456.pdf
   Error: PDF file is empty (no pages)
------------------------------------------------------------
```

## Troubleshooting

### Common Issues and Solutions

#### 1. ModuleNotFoundError: No module named 'fitz'

**Problem**: PyMuPDF is not installed.

**Solution**:
```bash
pip install PyMuPDF
```

#### 2. ModuleNotFoundError: No module named 'PIL'

**Problem**: Pillow is not installed.

**Solution**:
```bash
pip install Pillow
```

#### 3. FileNotFoundError: Source directory does not exist

**Problem**: The source directory path is incorrect or doesn't exist.

**Solution**:
- Verify the source directory exists
- Check the path in the `main()` function
- Use absolute paths if relative paths aren't working:
```python
source_dir = r'C:\Users\YourName\Documents\P064'  # Windows
source_dir = '/home/username/documents/P064'       # Linux/macOS
```

#### 4. PermissionError: Permission denied

**Problem**: The script doesn't have permission to read PDFs or write to the output directory.

**Solution**:
- Check file and directory permissions
- Run the script with appropriate permissions
- On Windows, try running as administrator
- On Linux/macOS, check file ownership and permissions:
```bash
chmod 755 P064
chmod 644 P064/*.pdf
```

#### 5. Corrupted or invalid PDF file

**Problem**: Some PDF files are corrupted or not valid PDF format.

**Solution**:
- The script will skip corrupted files and continue processing
- Check the error list in the summary to identify problematic files
- Try opening the PDF in a PDF reader to verify it's valid
- Re-download or obtain a new copy of the corrupted file

#### 6. PDF file is empty (no pages)

**Problem**: The PDF file contains no pages.

**Solution**:
- The script will skip empty PDFs and continue processing
- Verify the PDF file is not corrupted
- Check if the PDF was created correctly

#### 7. Memory errors with large PDFs

**Problem**: Processing very large PDFs causes memory issues.

**Solution**:
- Reduce the DPI setting (e.g., from 150 to 100)
- Process files in smaller batches
- Close other applications to free up memory

#### 8. Output images are too large or too small

**Problem**: Image file size or dimensions are not suitable.

**Solution**:
- Adjust the DPI setting:
  - Lower DPI = smaller files, lower quality
  - Higher DPI = larger files, higher quality
- Modify the JPEG quality setting in `extract_first_page()`:
```python
pil_image.save(output_path, "JPEG", quality=70, optimize=True)  # Lower quality
```

#### 9. Images have black background instead of white

**Problem**: Transparency handling issue.

**Solution**:
- This should be handled automatically by the script
- If the issue persists, check the PDF file for unusual color profiles
- The script converts RGBA to RGB with a white background

#### 10. Script runs but no images are created

**Problem**: Output directory permissions or path issues.

**Solution**:
- Check that the output directory is created (script does this automatically)
- Verify write permissions for the output directory
- Check the console output for error messages
- Ensure there's sufficient disk space

### Getting Help

If you encounter issues not covered here:

1. Check the console output for specific error messages
2. Verify all dependencies are installed correctly:
```bash
pip list | grep -E "PyMuPDF|Pillow"
```
3. Test with a single PDF file first to isolate the issue
4. Check Python version:
```bash
python --version
```

## Performance

### Expected Processing Times

Processing time depends on:
- Number of PDF files
- PDF file sizes and complexity
- DPI setting
- System hardware (CPU, disk speed)

**Typical performance** (150 DPI, modern hardware):
- ~0.1-0.3 seconds per PDF
- 601 PDFs: approximately 2-5 minutes

### Optimization Tips

1. **Lower DPI for faster processing**: Use 100 DPI instead of 150 DPI
2. **SSD vs HDD**: Processing is faster on SSD drives
3. **Batch size**: The script processes all files sequentially to manage memory efficiently

## Technical Details

### How It Works

1. **Directory Scanning**: Finds all `.pdf` files in the source directory
2. **PDF Rendering**: Opens each PDF with PyMuPDF and renders the first page
3. **Image Conversion**: Converts the rendered page to a PIL Image
4. **Format Optimization**: Handles transparency, converts to RGB, and saves as JPEG
5. **Error Handling**: Catches and logs errors, continues processing remaining files
6. **Reporting**: Displays progress and generates a summary report

### Architecture

```
[Source Directory] → [PDF Extractor] → [Output Directory]
                           ↓
                    [Progress Logger]
                    [Error Handler]
```

### Key Functions

- `extract_first_page()`: Extracts and converts a single PDF page
- `crop_image()`: Crops an image to specified coordinates
- `process_pdf_directory()`: Batch processes all PDFs in a directory (with optional cropping)
- `process_image_cropping()`: Batch crops all images in a directory
- `main_extract_only()`: Extract PDFs without cropping
- `main_crop_only()`: Crop existing images independently
- `main_extract_and_crop()`: Combined workflow (extract and crop)
- `ensure_output_directory()`: Creates output directory structure
- `get_pdf_files()`: Retrieves list of PDF files from source directory

## License

This script is provided as-is for use in your projects.

## Contributing

Feel free to modify and enhance the script for your specific needs.

## Changelog

### Version 1.0.0
- Initial release
- Batch PDF processing
- JPEG thumbnail generation
- Error handling and reporting
- Progress tracking
