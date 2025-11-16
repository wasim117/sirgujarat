# Design Document

## Overview

The Gujarati Text Extraction system is a Python-based OCR solution that processes image files and extracts Gujarati language text. The system uses Tesseract OCR with Gujarati language support as the core recognition engine, combined with image preprocessing to improve accuracy. The design prioritizes local processing without external dependencies, batch processing capabilities, and graceful error handling.

## Architecture

```
[Source Images] 
    ↓
[Image Loader] → [Image Preprocessing] → [Tesseract OCR Engine] → [Text Output]
    ↓                                              ↓
[Error Handler] ←─────────────────────────────────┘
    ↓
[Progress Logger]
    ↓
[Summary Report]
```

### Key Components

1. **Image Loader**: Reads image files from source directory, validates format
2. **Image Preprocessing**: Applies image enhancement techniques to improve OCR accuracy
3. **Tesseract OCR Engine**: Performs optical character recognition with Gujarati language support
4. **Text Output Handler**: Saves extracted text to output files
5. **Error Handler**: Catches and logs processing errors
6. **Progress Logger**: Displays real-time processing status
7. **Summary Report Generator**: Creates final processing summary

## Components and Interfaces

### 1. Image Processing Module

**Purpose**: Load and preprocess images for optimal OCR performance

**Key Functions**:
- `load_image(image_path)`: Load image file using PIL/OpenCV
- `preprocess_image(image)`: Apply preprocessing techniques (grayscale conversion, contrast enhancement, noise reduction)
- `validate_image_format(image_path)`: Verify image is in supported format (JPEG, PNG, BMP)

**Input**: Image file path
**Output**: Preprocessed PIL Image object

### 2. OCR Engine Module

**Purpose**: Extract Gujarati text from preprocessed images

**Key Functions**:
- `extract_text_from_image(image, language='guj')`: Use Tesseract to extract text
- `get_confidence_score(ocr_result)`: Extract confidence metrics from OCR result
- `validate_gujarati_text(text)`: Verify extracted text contains Gujarati characters

**Input**: PIL Image object, language code
**Output**: Extracted text string, confidence score

### 3. File I/O Module

**Purpose**: Handle reading and writing of image and text files

**Key Functions**:
- `get_image_files(source_dir)`: Retrieve list of image files from directory
- `save_extracted_text(text, output_path)`: Write extracted text to file
- `ensure_output_directory(output_path)`: Create output directory structure

**Input**: Directory paths, text content
**Output**: File paths, success/failure status

### 4. Batch Processing Module

**Purpose**: Orchestrate processing of multiple images

**Key Functions**:
- `process_single_image(image_path, output_path)`: Extract text from one image
- `process_image_directory(source_dir, output_dir)`: Batch process all images
- `process_image_for_testing(image_path)`: Single image processing with console output

**Input**: Image file paths, output directory
**Output**: Processing results, error logs

### 5. Reporting Module

**Purpose**: Track progress and generate summary reports

**Key Functions**:
- `log_progress(current, total, filename)`: Display processing progress
- `log_error(filename, error_message)`: Record processing errors
- `generate_summary_report(results)`: Create final processing summary

**Input**: Processing metrics, error information
**Output**: Console output, summary statistics

## Data Models

### ProcessingResult

```python
{
    'success': int,              # Number of successfully processed images
    'failed': int,               # Number of failed images
    'errors': [                  # List of error details
        {
            'filename': str,     # Image filename
            'error': str         # Error message
        }
    ],
    'elapsed_time': float,       # Processing time in seconds
    'output_dir': str,           # Output directory path
    'total_files': int           # Total files processed
}
```

### ExtractionResult

```python
{
    'text': str,                 # Extracted Gujarati text
    'confidence': float,         # OCR confidence score (0-100)
    'language': str,             # Detected language code
    'success': bool,             # Whether extraction succeeded
    'error': str or None         # Error message if failed
}
```

## Error Handling

### Error Categories

1. **File System Errors**
   - File not found
   - Permission denied
   - Invalid file format
   - Disk space issues

2. **Image Processing Errors**
   - Corrupted image file
   - Unsupported image format
   - Image too small or too large
   - Image loading failure

3. **OCR Errors**
   - Tesseract not installed
   - Gujarati language data not available
   - OCR processing timeout
   - Invalid image for OCR

4. **Output Errors**
   - Cannot create output directory
   - Cannot write to output file
   - Insufficient permissions

### Error Handling Strategy

- **Graceful Degradation**: Continue processing remaining files if one fails
- **Detailed Logging**: Record specific error messages for each failure
- **User Notification**: Display errors in console and summary report
- **Recovery**: Attempt to create missing directories automatically

## Testing Strategy

### Unit Testing

1. **Image Loading Tests**
   - Test loading valid image formats (JPEG, PNG, BMP)
   - Test handling of corrupted images
   - Test handling of missing files

2. **Image Preprocessing Tests**
   - Test grayscale conversion
   - Test contrast enhancement
   - Test noise reduction

3. **OCR Tests**
   - Test Gujarati text extraction from sample images
   - Test confidence score extraction
   - Test handling of images with no text

4. **File I/O Tests**
   - Test directory creation
   - Test file writing
   - Test file naming conventions

### Integration Testing

1. **Single Image Processing**
   - Test end-to-end processing of one image
   - Verify text output file creation
   - Verify console output

2. **Batch Processing**
   - Test processing multiple images
   - Test error handling during batch processing
   - Test progress reporting

3. **Error Scenarios**
   - Test processing with missing source directory
   - Test processing with corrupted images
   - Test processing with insufficient permissions

### Manual Testing

1. **Test with First Image**: Process `/public/address-image/p064/P0640001.pdf` (or first image in directory)
2. **Verify Output**: Check extracted text is valid Gujarati
3. **Check Confidence**: Verify confidence scores are reasonable
4. **Validate File Creation**: Confirm output text file is created

## Technology Stack

### Core Libraries

1. **Tesseract OCR** (pytesseract)
   - Local OCR engine with Gujarati language support
   - No internet required
   - Supports multiple languages
   - Installation: `pip install pytesseract`
   - Requires: Tesseract binary installation

2. **Pillow (PIL)**
   - Image loading and preprocessing
   - Format conversion
   - Installation: `pip install Pillow`

3. **OpenCV (optional)**
   - Advanced image preprocessing
   - Contrast enhancement
   - Noise reduction
   - Installation: `pip install opencv-python`

### System Requirements

- Python 3.7+
- Tesseract OCR binary (system-level installation)
- Gujarati language data for Tesseract
- 2GB+ RAM for batch processing
- 500MB+ disk space for Tesseract and language data

## Implementation Approach

### Phase 1: Setup and Single Image Testing
- Install and configure Tesseract OCR
- Install Gujarati language support
- Create image loading and preprocessing functions
- Test with single image from `/public/address-image/p064/`
- Verify text extraction works

### Phase 2: Core OCR Integration
- Implement Tesseract integration
- Extract confidence scores
- Handle OCR errors
- Validate Gujarati text output

### Phase 3: Batch Processing
- Implement directory scanning
- Create batch processing orchestration
- Add progress logging
- Implement error tracking

### Phase 4: Output and Reporting
- Implement text file output
- Create summary reports
- Add detailed error logging
- Test end-to-end workflow

## Dependencies and Installation

### Tesseract Installation

**Windows**:
```
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
Run: tesseract-ocr-w64-setup-v5.x.x.exe
Note installation path (default: C:\Program Files\Tesseract-OCR)
```

**macOS**:
```
brew install tesseract
```

**Linux**:
```
sudo apt-get install tesseract-ocr
```

### Gujarati Language Data

Tesseract includes Gujarati support in standard installation. Verify with:
```
tesseract --list-langs | grep guj
```

### Python Dependencies

```
pytesseract>=0.3.10
Pillow>=10.0.0
opencv-python>=4.8.0 (optional, for advanced preprocessing)
```

## Performance Considerations

- **Image Size**: Optimal 300-400 DPI for OCR accuracy
- **Batch Processing**: Process images sequentially to manage memory
- **Preprocessing**: Balance between accuracy and processing speed
- **Confidence Threshold**: Consider filtering low-confidence results

## Security Considerations

- Validate file paths to prevent directory traversal
- Check file permissions before processing
- Limit file size to prevent memory exhaustion
- Sanitize output filenames

