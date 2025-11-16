# Gujarati Text Extraction - Installation and Usage Guide

## Overview

The Gujarati Text Extraction module uses Tesseract OCR to extract Gujarati language text from images. This guide provides step-by-step instructions for installation and usage.

## System Requirements

- Python 3.7 or higher
- 2GB+ RAM for batch processing
- 500MB+ disk space for Tesseract and language data
- Supported operating systems: Windows, macOS, Linux

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements_gujarati.txt
```

This installs:
- **pytesseract** (>=0.3.10): Python wrapper for Tesseract OCR
- **Pillow** (>=10.0.0): Image processing library
- **opencv-python** (>=4.8.0): Advanced image processing (optional but recommended)
- **numpy** (>=1.21.0): Numerical computing library

### Step 2: Install Tesseract OCR Binary

Tesseract OCR must be installed separately on your system. Follow the instructions for your operating system:

#### Windows

1. Download the Tesseract installer from:
   https://github.com/UB-Mannheim/tesseract/wiki

2. Run the installer (e.g., `tesseract-ocr-w64-setup-v5.x.x.exe`)

3. During installation, note the installation path (default: `C:\Program Files\Tesseract-OCR`)

4. After installation, configure pytesseract to find Tesseract:
   ```python
   import pytesseract
   pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

5. Verify installation:
   ```bash
   tesseract --version
   tesseract --list-langs
   ```

#### macOS

```bash
# Install using Homebrew
brew install tesseract

# Verify installation
tesseract --version
tesseract --list-langs
```

#### Linux (Ubuntu/Debian)

```bash
# Install Tesseract
sudo apt-get update
sudo apt-get install tesseract-ocr

# Verify installation
tesseract --version
tesseract --list-langs
```

#### Linux (Fedora/RHEL)

```bash
# Install Tesseract
sudo dnf install tesseract

# Verify installation
tesseract --version
tesseract --list-langs
```

### Step 3: Verify Gujarati Language Support

Tesseract includes Gujarati language support by default. Verify it's available:

```bash
tesseract --list-langs | grep guj
```

You should see `guj` in the output. If not, the Gujarati language data may need to be installed separately.

**Note**: Standard Tesseract installations include Gujarati support. If you need to install it manually:

- Download from: https://github.com/tesseract-ocr/tessdata
- Place `guj.traineddata` in Tesseract's `tessdata` directory
  - Windows: `C:\Program Files\Tesseract-OCR\tessdata`
  - macOS: `/usr/local/share/tessdata`
  - Linux: `/usr/share/tesseract-ocr/4.00/tessdata`

## Usage

### Basic Usage

#### Test with Single Image

Test the OCR functionality with a single image:

```bash
python gujarati_text_extractor.py --test
```

This processes the first image found in the `P064` directory and displays:
- Extracted Gujarati text
- Confidence score
- Output file location

#### Batch Process Directory

Process all images in a directory:

```bash
python gujarati_text_extractor.py
```

This processes all images in the `P064` directory and saves extracted text to the `output` directory.

### Advanced Usage

#### Custom Source Directory

```bash
python gujarati_text_extractor.py --source /path/to/images
```

#### Custom Output Directory

```bash
python gujarati_text_extractor.py --output /path/to/output
```

#### Test Specific Image

```bash
python gujarati_text_extractor.py --test --image /path/to/image.jpg
```

#### Combine Options

```bash
python gujarati_text_extractor.py --source /path/to/images --output /path/to/output
```

### Python API Usage

You can also use the module directly in Python:

```python
from gujarati_text_extractor import (
    process_single_image,
    process_image_directory,
    process_image_for_testing
)

# Test with single image
result = process_image_for_testing('path/to/image.jpg', 'output')

# Process single image
result = process_single_image('path/to/image.jpg', 'output/image.txt')
if result['success']:
    print(f"Extracted text: {result['text']}")
    print(f"Confidence: {result['confidence']:.2f}%")

# Batch process directory
results = process_image_directory('P064', 'output')
print(f"Processed: {results['success']} successful, {results['failed']} failed")
```

## Output

### Output Files

Extracted text is saved to `.txt` files in the output directory:
- Input: `P064/P0640001.pdf` → Output: `output/P0640001.txt`
- Input: `P064/image.jpg` → Output: `output/image.txt`

### Console Output

#### Single Image Processing

```
======================================================================
SINGLE IMAGE PROCESSING RESULT
======================================================================
Image: P0640001.pdf
Status: SUCCESS
Confidence Score: 85.42%
Output File: output/P0640001.txt

Extracted Text:
----------------------------------------------------------------------
[Gujarati text content...]
======================================================================
```

#### Batch Processing

```
[1/100] (1.0%) Processing: P0640001.pdf
[2/100] (2.0%) Processing: P0640002.pdf
...
======================================================================
PROCESSING SUMMARY REPORT
======================================================================
Total Files Processed: 100
Successful: 98
Failed: 2
Execution Time: 245.32 seconds
Output Directory: output

Errors:
----------------------------------------------------------------------
  • P0640050.pdf: Failed to load image P064/P0640050.pdf: [error details]
  • P0640075.pdf: OCR extraction failed: [error details]
======================================================================
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- PDF (.pdf)

## Image Quality Recommendations

For best OCR accuracy:

1. **Resolution**: 300-400 DPI (dots per inch)
2. **Contrast**: High contrast between text and background
3. **Orientation**: Text should be upright (0 degrees)
4. **Clarity**: Text should be clear and not blurry
5. **Size**: Text should be at least 10 pixels high

## Troubleshooting

### Issue: "pytesseract.TesseractNotFoundError"

**Solution**: Tesseract is not installed or pytesseract cannot find it.

- Windows: Ensure Tesseract is installed and update the path in the code
- macOS/Linux: Verify `tesseract --version` works in terminal

### Issue: "Gujarati language data not found"

**Solution**: Gujarati language support is not installed.

```bash
# Verify Gujarati is available
tesseract --list-langs | grep guj

# If not found, install manually (see Step 3 above)
```

### Issue: "No image files found"

**Solution**: Check that:
- Source directory path is correct
- Directory contains supported image formats
- Files are readable and not corrupted

### Issue: "Permission denied" when creating output directory

**Solution**: Ensure you have write permissions to the output directory location.

### Issue: Low confidence scores or poor text extraction

**Solution**: 
- Improve image quality (higher resolution, better contrast)
- Check that text is in Gujarati script
- Verify Tesseract is properly installed
- Try preprocessing options in the code

## Performance Considerations

- **Batch Processing**: Processing speed depends on image size and system resources
- **Memory Usage**: Large images may consume significant memory
- **Disk Space**: Ensure sufficient space for output files
- **Typical Speed**: ~2-5 seconds per image on modern systems

## Configuration

### Adjusting Preprocessing

Edit `gujarati_text_extractor.py` to modify preprocessing:

```python
def preprocess_image(image: Image.Image) -> Image.Image:
    # Adjust contrast enhancement factor (1.5 = 50% increase)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)  # Change this value
    
    # Adjust brightness enhancement factor
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.1)  # Change this value
    
    return image
```

### Adjusting OCR Language

To extract text in a different language:

```python
# In your code, change the language parameter
text = extract_text_from_image(image, language='eng')  # For English
text = extract_text_from_image(image, language='hin')  # For Hindi
```

## Supported Languages

Tesseract supports many languages. Common language codes:
- `guj` - Gujarati
- `eng` - English
- `hin` - Hindi
- `mar` - Marathi
- `tam` - Tamil
- `tel` - Telugu

## Additional Resources

- Tesseract Documentation: https://github.com/tesseract-ocr/tesseract
- pytesseract Documentation: https://github.com/madmaze/pytesseract
- Tesseract Language Data: https://github.com/tesseract-ocr/tessdata

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review Tesseract documentation
3. Check pytesseract GitHub issues
4. Verify system requirements are met

## License

This module uses Tesseract OCR, which is licensed under the Apache License 2.0.
See: https://github.com/tesseract-ocr/tesseract/blob/master/LICENSE
