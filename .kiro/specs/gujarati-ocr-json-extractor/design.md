# Design Document: Gujarati OCR JSON Extractor

## Overview

The Gujarati OCR JSON Extractor is a Python-based system that processes images containing Gujarati text from two separate directories (taluko and gaam), extracts the text using OCR technology, and consolidates the results into a structured JSON file. The system is designed to be robust, handling errors gracefully while providing visibility into the processing pipeline.

## Architecture

The system follows a modular, pipeline-based architecture with clear separation of concerns:

```
Input Layer (Image Discovery)
    ↓
Processing Layer (OCR Extraction)
    ↓
Aggregation Layer (Data Mapping)
    ↓
Output Layer (JSON Generation)
```

### Key Components

1. **Image Discovery Module**: Scans designated directories and identifies image files
2. **OCR Processing Module**: Performs optical character recognition on images
3. **Data Aggregation Module**: Maps and combines taluko and gaam data by image name
4. **JSON Output Module**: Generates and writes the final JSON file
5. **Error Handling Module**: Captures and logs errors throughout the pipeline

## Components and Interfaces

### 1. ImageDiscovery Class

**Purpose**: Locate and enumerate image files from source directories

**Methods**:
- `discover_images(directory_path: str) -> List[str]`: Returns list of image file paths
- `get_image_name(file_path: str) -> str`: Extracts base filename without extension

**Supported Formats**: PNG, JPG, JPEG, BMP, TIFF

### 2. OCRProcessor Class

**Purpose**: Extract Gujarati text from images using OCR

**Methods**:
- `extract_text(image_path: str) -> str`: Performs OCR and returns extracted text
- `validate_gujarati_text(text: str) -> bool`: Verifies extracted text contains Gujarati characters

**OCR Engine**: Tesseract with Gujarati language support (tessdata_best-guj)

### 3. DataAggregator Class

**Purpose**: Map and combine taluko and gaam data by image name

**Methods**:
- `add_taluko_entry(image_name: str, text: str) -> None`: Store taluko data
- `add_gaam_entry(image_name: str, text: str) -> None`: Store gaam data
- `get_aggregated_data() -> Dict`: Return combined data structure

**Data Structure**:
```python
{
    "image_name": {
        "taluko": "extracted_gujarati_text",
        "gaam": "extracted_gujarati_text"
    }
}
```

### 4. JSONOutputWriter Class

**Purpose**: Generate and write JSON output file

**Methods**:
- `write_json(data: Dict, output_path: str) -> bool`: Write data to JSON file
- `validate_output_directory(path: str) -> bool`: Ensure output directory exists

### 5. ErrorLogger Class

**Purpose**: Capture and report processing errors

**Methods**:
- `log_error(image_name: str, error_type: str, message: str) -> None`: Record error
- `get_summary() -> Dict`: Return processing summary with success/failure counts

## Data Models

### Input Data Model

```python
class ImageData:
    image_name: str          # e.g., "P0640001"
    file_path: str           # Full path to image file
    directory_type: str      # "taluko" or "gaam"
    extracted_text: str      # OCR result
    processing_status: str   # "success" or "failed"
    error_message: str       # Error details if failed
```

### Output Data Model

```python
class ExtractedEntry:
    image_name: str
    taluko: Optional[str]    # Extracted taluko text or None
    gaam: Optional[str]      # Extracted gaam text or None
```

### JSON Output Structure

```json
{
    "P0640001": {
        "taluko": "તાલુકો નામ",
        "gaam": "ગામ નામ"
    },
    "P0640002": {
        "taluko": "તાલુકો નામ",
        "gaam": null
    }
}
```

## Error Handling

### Error Categories

1. **File System Errors**: Missing directories, unreadable files
2. **Image Processing Errors**: Corrupted images, unsupported formats
3. **OCR Errors**: OCR engine failures, text extraction issues
4. **Output Errors**: Write failures, permission issues

### Error Handling Strategy

- **Graceful Degradation**: Continue processing remaining images if one fails
- **Detailed Logging**: Record error type, image name, and context
- **Partial Results**: Include successfully processed images in output
- **Summary Report**: Provide count of successes and failures

### Error Recovery

- Automatically create output directory if missing
- Skip corrupted images and log the issue
- Retry OCR with alternative parameters if initial attempt fails
- Validate JSON before writing to disk

## Testing Strategy

### Unit Tests

1. **ImageDiscovery Tests**:
   - Verify correct image file discovery
   - Test handling of empty directories
   - Validate filename extraction

2. **OCRProcessor Tests**:
   - Test OCR extraction with sample Gujarati images
   - Verify Gujarati text validation
   - Test error handling for corrupted images

3. **DataAggregator Tests**:
   - Test data mapping by image name
   - Verify handling of missing taluko or gaam data
   - Test data structure correctness

4. **JSONOutputWriter Tests**:
   - Verify JSON file creation
   - Test JSON structure and formatting
   - Validate directory creation

5. **ErrorLogger Tests**:
   - Test error logging functionality
   - Verify summary generation

### Integration Tests

1. End-to-end processing: Images → OCR → JSON output
2. Error scenarios: Missing directories, corrupted images
3. Partial data: Only taluko or only gaam images present

### Test Data

- Sample Gujarati images in `/public-taluko/` and `/public-gaam/`
- Test images with various formats and quality levels
- Corrupted image files for error testing

## Implementation Approach

### Phase 1: Core Infrastructure
- Set up project structure
- Implement ImageDiscovery and basic file handling
- Create error logging framework

### Phase 2: OCR Integration
- Integrate Tesseract OCR with Gujarati support
- Implement OCRProcessor with text extraction
- Add Gujarati text validation

### Phase 3: Data Processing
- Implement DataAggregator for mapping and combining data
- Create JSON output writer
- Integrate all components into main pipeline

### Phase 4: Testing and Refinement
- Write comprehensive tests
- Handle edge cases
- Optimize performance

## Dependencies

- **pytesseract**: Python wrapper for Tesseract OCR
- **Tesseract OCR**: Core OCR engine with Gujarati language data
- **Pillow (PIL)**: Image processing library
- **Python 3.8+**: Runtime environment

## Configuration

- Input directories: `/public-taluko/`, `/public-gaam/`
- Output file: `extracted_data.json` (configurable)
- Supported image formats: PNG, JPG, JPEG, BMP, TIFF
- OCR language: Gujarati (guj)
