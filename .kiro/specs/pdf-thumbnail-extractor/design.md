# Design Document

## Overview

The PDF Thumbnail Extractor is a Python script that processes PDF files in batch, extracting the first page of each document as a JPEG image. The solution uses the PyMuPDF (fitz) library for efficient PDF rendering and PIL/Pillow for image processing.

## Architecture

### High-Level Architecture

```
[P064 Directory] → [PDF Extractor Script] → [public/images/p064/ Directory]
                           ↓                         ↓
                    [Progress Logger]         [Image Cropper]
                    [Error Handler]                  ↓
                                            [public/address-images/p064/ Directory]
```

### Technology Stack

- **Python 3.7+**: Core runtime
- **PyMuPDF (fitz)**: PDF rendering and page extraction
- **Pillow (PIL)**: Image format conversion and optimization
- **pathlib**: Cross-platform path handling
- **os**: Directory operations

## Components and Interfaces

### 1. Main Extractor Module (`extract_pdf_thumbnails.py`)

**Purpose**: Orchestrates the entire extraction process

**Key Functions**:

```python
def extract_first_page(pdf_path: Path, output_path: Path, dpi: int = 150) -> bool
    """
    Extracts the first page from a PDF and saves as JPEG.
    
    Args:
        pdf_path: Path to source PDF file
        output_path: Path where JPEG should be saved
        dpi: Resolution for rendering (default 150)
    
    Returns:
        bool: True if successful, False otherwise
    """

def crop_image(image_path: Path, output_path: Path, left: int, top: int, width: int, height: int) -> tuple
    """
    Crops an image to specified coordinates and saves the result.
    
    Args:
        image_path: Path to source image file
        output_path: Path where cropped image should be saved
        left: Left coordinate of crop region
        top: Top coordinate of crop region
        width: Width of crop region
        height: Height of crop region
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """

def process_pdf_directory(source_dir: str, output_dir: str, dpi: int = 150) -> dict
    """
    Processes all PDFs in a directory.
    
    Args:
        source_dir: Path to directory containing PDFs
        output_dir: Path to output directory for images
        dpi: Resolution for rendering
    
    Returns:
        dict: Summary with 'success', 'failed', and 'errors' keys
    """

def ensure_output_directory(output_path: Path) -> None
    """
    Creates output directory structure if it doesn't exist.
    
    Args:
        output_path: Path to output directory
    """
```

### 2. PDF Processing Component

**Responsibilities**:
- Open PDF files using PyMuPDF
- Extract first page (index 0)
- Render page to pixmap at specified DPI
- Convert pixmap to PIL Image
- Handle PDF-specific errors (corrupted files, empty PDFs)

**Implementation Details**:
- Use `fitz.open()` to load PDF
- Use `page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))` for rendering
- Calculate zoom factor: `zoom = dpi / 72` (72 is default PDF DPI)
- Convert to RGB mode to ensure JPEG compatibility

### 3. Image Processing Component

**Responsibilities**:
- Convert rendered pixmap to PIL Image
- Ensure RGB color mode (no alpha channel)
- Save as JPEG with quality setting
- Handle transparency by adding white background

**Implementation Details**:
- Use `Image.frombytes()` to create PIL Image from pixmap
- Convert RGBA to RGB if necessary: `image.convert('RGB')`
- Save with `image.save(output_path, 'JPEG', quality=85, optimize=True)`

### 5. Image Cropping Component

**Responsibilities**:
- Load extracted JPEG images
- Crop images to specified coordinates (left: 133, top: 425, width: 1058, height: 393)
- Save cropped images to address-images directory
- Validate crop region is within image boundaries

**Implementation Details**:
- Use `Image.open()` to load the extracted JPEG
- Calculate crop box: `(left, top, left + width, top + height)`
- Use `image.crop(box)` to extract the region
- Validate coordinates: ensure `left + width <= image.width` and `top + height <= image.height`
- Save cropped image with same quality settings
- Handle errors if crop region is invalid

### 4. Progress and Logging Component

**Responsibilities**:
- Display current progress (file X of Y)
- Show filename being processed
- Log errors with details
- Display summary statistics

**Implementation Details**:
- Use simple print statements for progress
- Track success/failure counts
- Store error messages in list for final report
- Display elapsed time using `time.time()`

## Data Models

### ProcessingResult

```python
{
    'success': int,           # Count of successfully processed files
    'failed': int,            # Count of failed files
    'errors': [               # List of error details
        {
            'filename': str,
            'error': str
        }
    ],
    'elapsed_time': float     # Total processing time in seconds
}
```

### Configuration

```python
{
    'source_directory': 'P064',
    'output_directory': 'public/images/p064',
    'address_output_directory': 'public/address-images/p064',
    'dpi': 150,
    'jpeg_quality': 85,
    'crop_coordinates': {
        'left': 133,
        'top': 425,
        'width': 1058,
        'height': 393
    }
}
```

## Error Handling

### Error Categories

1. **File Access Errors**
   - PDF file not found or not readable
   - Output directory not writable
   - Action: Log error, skip file, continue processing

2. **PDF Processing Errors**
   - Corrupted PDF file
   - Empty PDF (no pages)
   - Encrypted/password-protected PDF
   - Action: Log error with filename, skip file, continue processing

3. **Image Conversion Errors**
   - Memory issues with large PDFs
   - Invalid pixmap data
   - Action: Log error, skip file, continue processing

4. **Image Cropping Errors**
   - Crop region exceeds image boundaries
   - Invalid crop coordinates
   - Source image not found or corrupted
   - Action: Log error with details, skip file, continue processing

4. **System Errors**
   - Insufficient disk space
   - Permission denied
   - Action: Log error, attempt to continue or fail gracefully

### Error Handling Strategy

```python
try:
    # Process PDF
except fitz.FileDataError:
    # Handle corrupted PDF
except fitz.EmptyFileError:
    # Handle empty PDF
except Exception as e:
    # Catch-all for unexpected errors
finally:
    # Ensure resources are cleaned up
```

## Testing Strategy

### Unit Testing

1. **Test PDF extraction with valid file**
   - Verify JPEG is created
   - Verify correct filename
   - Verify image dimensions are reasonable

2. **Test error handling with corrupted PDF**
   - Verify error is logged
   - Verify processing continues

3. **Test directory creation**
   - Verify output directory is created if missing
   - Verify nested directories are created

4. **Test batch processing**
   - Verify all files are processed
   - Verify summary statistics are accurate

### Integration Testing

1. **Test with actual P064 directory**
   - Process subset of files (e.g., first 10)
   - Verify images are created correctly
   - Verify progress output

2. **Test with mixed file types**
   - Include valid and corrupted PDFs
   - Verify graceful handling

### Manual Testing

1. **Visual inspection of generated thumbnails**
   - Check image quality
   - Verify correct page is extracted
   - Check for rendering artifacts

2. **Performance testing**
   - Measure time to process all 601 PDFs
   - Monitor memory usage

## Implementation Notes

### Performance Considerations

- PyMuPDF is significantly faster than alternatives (pdf2image, PyPDF2)
- Processing 601 PDFs should take approximately 2-5 minutes depending on hardware
- Memory usage should remain reasonable as files are processed sequentially

### File Naming Convention

- Input: `P064/P0640001.pdf`
- Full page output: `public/images/p064/P0640001.jpg`
- Cropped address output: `public/address-images/p064/P0640001.jpg`
- Preserve original filename, change extension only

### DPI Selection

- 150 DPI provides good balance between quality and file size
- Can be adjusted via parameter if needed
- Higher DPI (200-300) for better quality but larger files
- Lower DPI (100) for smaller files but reduced quality

### Dependencies Installation

```bash
pip install PyMuPDF Pillow
```

Or using requirements.txt:
```
PyMuPDF>=1.23.0
Pillow>=10.0.0
```
