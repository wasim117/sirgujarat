# Requirements Document: Gujarati OCR JSON Extractor

## Introduction

This feature enables automated extraction of Gujarati text from images organized in two categories (taluko and gaam) and consolidates the extracted data into a structured JSON file. The system reads images from designated directories, performs OCR to extract Gujarati text, and creates a mapping file that associates image names with their extracted content.

## Glossary

- **OCR (Optical Character Recognition)**: Technology that converts images containing text into machine-readable text
- **Gujarati Text**: Text written in the Gujarati script, an Indic script used for the Gujarati language
- **Taluko**: Administrative subdivision; in this context, refers to images containing taluko (administrative region) names in Gujarati
- **Gaam**: Village; in this context, refers to images containing village names in Gujarati
- **JSON File**: Structured data format storing key-value pairs for easy programmatic access
- **Image Name**: The filename of the source image (e.g., P0640001.png)
- **Extraction**: The process of reading and converting image content to text

## Requirements

### Requirement 1: Taluko Image Processing

**User Story:** As a data processor, I want to extract Gujarati taluko names from images in the `/public-taluko/` directory, so that I can capture administrative region information programmatically.

#### Acceptance Criteria

1. WHEN the system processes images from `/public-taluko/`, THE system SHALL read all image files from that directory
2. WHEN an image is read from the taluko directory, THE system SHALL perform OCR to extract Gujarati text
3. WHEN OCR extraction completes for a taluko image, THE system SHALL store the extracted text with the image name as the identifier
4. IF an image file cannot be read or processed, THEN THE system SHALL log the error and continue processing remaining images

### Requirement 2: Gaam Image Processing

**User Story:** As a data processor, I want to extract Gujarati gaam (village) names from images in the `/public-gaam/` directory, so that I can capture village information programmatically.

#### Acceptance Criteria

1. WHEN the system processes images from `/public-gaam/`, THE system SHALL read all image files from that directory
2. WHEN an image is read from the gaam directory, THE system SHALL perform OCR to extract Gujarati text
3. WHEN OCR extraction completes for a gaam image, THE system SHALL store the extracted text with the image name as the identifier
4. IF an image file cannot be read or processed, THEN THE system SHALL log the error and continue processing remaining images

### Requirement 3: JSON Output Generation

**User Story:** As a data consumer, I want the extracted taluko and gaam data consolidated into a single JSON file, so that I can easily access and process the information programmatically.

#### Acceptance Criteria

1. WHEN all images have been processed, THE system SHALL create a JSON file with a structured format
2. THE JSON file SHALL contain entries mapping image names to extracted taluko and gaam text
3. THE JSON structure SHALL follow the format: `{image_name: {taluko: "extracted_gujarati_text", gaam: "extracted_gujarati_text"}}`
4. WHEN the JSON file is created, THE system SHALL write it to a specified output location with proper formatting

### Requirement 4: Data Mapping and Association

**User Story:** As a data analyst, I want taluko and gaam data to be associated by image name, so that I can correlate administrative and village information for the same location.

#### Acceptance Criteria

1. WHEN processing images, THE system SHALL match taluko and gaam images by their base filename (e.g., P0640001)
2. WHEN both taluko and gaam data exist for the same image name, THE system SHALL combine them into a single JSON entry
3. WHERE taluko or gaam data is missing for an image name, THE system SHALL include the available data with null or empty string for missing fields
4. THE system SHALL preserve the original image name as the key in the JSON output

### Requirement 5: Error Handling and Logging

**User Story:** As a system operator, I want visibility into processing errors and warnings, so that I can identify and resolve issues with image processing or OCR extraction.

#### Acceptance Criteria

1. WHEN an error occurs during image reading or OCR processing, THE system SHALL capture and log the error with context
2. WHEN processing completes, THE system SHALL provide a summary of successfully processed images and any failures
3. IF the output directory does not exist, THEN THE system SHALL create it automatically
4. WHEN the JSON file is written, THE system SHALL verify the file was created successfully
