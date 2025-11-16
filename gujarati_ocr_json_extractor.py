#!/usr/bin/env python3
"""
Gujarati OCR JSON Extractor

This script extracts Gujarati text from images in two directories (taluko and gaam)
and consolidates the results into a structured JSON file.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from PIL import Image
import pytesseract


class ImageDiscovery:
    """Discovers and enumerates image files from source directories."""
    
    # Supported image formats
    SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
    
    def __init__(self, error_logger: Optional['ErrorLogger'] = None):
        """
        Initialize ImageDiscovery with optional error logger.
        
        Args:
            error_logger: ErrorLogger instance for logging errors
        """
        self.error_logger = error_logger
    
    def discover_images(self, directory_path: str) -> List[str]:
        """
        Discover all image files in a given directory.
        
        Args:
            directory_path: Path to the directory to scan
            
        Returns:
            List of full paths to image files
        """
        image_files = []
        
        # Check if directory exists
        if not os.path.exists(directory_path):
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'file_system',
                    f"Directory does not exist: {directory_path}"
                )
            return image_files
        
        if not os.path.isdir(directory_path):
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'file_system',
                    f"Path is not a directory: {directory_path}"
                )
            return image_files
        
        # Scan directory for image files
        try:
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                
                # Check if it's a file (not a directory)
                if os.path.isfile(file_path):
                    # Check if file has a supported image extension
                    _, ext = os.path.splitext(filename)
                    if ext.lower() in self.SUPPORTED_FORMATS:
                        image_files.append(file_path)
        except PermissionError as e:
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'file_system',
                    f"Permission denied accessing directory: {directory_path}"
                )
            return []
        except OSError as e:
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'file_system',
                    f"OS error reading directory {directory_path}: {str(e)}"
                )
            return []
        except Exception as e:
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'file_system',
                    f"Unexpected error reading directory {directory_path}: {str(e)}"
                )
            return []
        
        return sorted(image_files)
    
    def get_image_name(self, file_path: str) -> str:
        """
        Extract base filename without extension.
        
        Args:
            file_path: Full path to the image file
            
        Returns:
            Base filename without extension (e.g., "P0640001")
        """
        filename = os.path.basename(file_path)
        name_without_ext, _ = os.path.splitext(filename)
        return name_without_ext


class OCRProcessor:
    """Extracts Gujarati text from images using OCR."""
    
    def __init__(self, language: str = 'guj', error_logger: Optional['ErrorLogger'] = None):
        """
        Initialize OCRProcessor with language configuration.
        
        Args:
            language: Tesseract language code (default: 'guj' for Gujarati)
            error_logger: ErrorLogger instance for logging errors
        """
        self.language = language
        self.error_logger = error_logger
    
    def extract_text(self, image_path: str) -> Optional[str]:
        """
        Extract text from image using pytesseract.
        
        Args:
            image_path: Full path to the image file
            
        Returns:
            Extracted text as string, or None if extraction fails
        """
        try:
            # Load image using Pillow
            image = Image.open(image_path)
            
            # Configure Tesseract for Gujarati language
            custom_config = f'--oem 3 --psm 6 -l {self.language}'
            
            # Perform OCR extraction
            extracted_text = pytesseract.image_to_string(image, config=custom_config)
            
            # Strip whitespace and return
            return extracted_text.strip()
            
        except FileNotFoundError:
            if self.error_logger:
                image_name = os.path.basename(image_path)
                self.error_logger.log_error(
                    image_name,
                    'ocr',
                    f"Image file not found: {image_path}"
                )
            return None
            
        except Image.UnidentifiedImageError:
            if self.error_logger:
                image_name = os.path.basename(image_path)
                self.error_logger.log_error(
                    image_name,
                    'ocr',
                    f"Cannot identify image file (corrupted or unsupported format): {image_path}"
                )
            return None
            
        except pytesseract.TesseractNotFoundError:
            if self.error_logger:
                image_name = os.path.basename(image_path)
                self.error_logger.log_error(
                    image_name,
                    'ocr',
                    "Tesseract OCR is not installed or not in PATH"
                )
            return None
            
        except Exception as e:
            if self.error_logger:
                image_name = os.path.basename(image_path)
                self.error_logger.log_error(
                    image_name,
                    'ocr',
                    f"Unexpected error during OCR extraction: {str(e)}"
                )
            return None
    
    def validate_gujarati_text(self, text: str) -> bool:
        """
        Validate that extracted text contains Gujarati characters.
        
        Args:
            text: Text to validate
            
        Returns:
            True if text contains Gujarati characters, False otherwise
        """
        if not text or len(text.strip()) == 0:
            return False
        
        # Gujarati Unicode range: U+0A80 to U+0AFF
        gujarati_range = range(0x0A80, 0x0B00)
        
        # Check if any character in the text is in Gujarati range
        for char in text:
            if ord(char) in gujarati_range:
                return True
        
        return False


class DataAggregator:
    """Maps and combines taluko and gaam data by image name."""
    
    def __init__(self):
        """Initialize the data aggregator with an empty data structure."""
        self._data = {}
    
    def add_taluko_entry(self, image_name: str, text: str) -> None:
        """
        Store taluko data for a given image name.
        
        Args:
            image_name: Base filename without extension (e.g., "P0640001")
            text: Extracted Gujarati text from taluko image
        """
        if image_name not in self._data:
            self._data[image_name] = {'taluko': None, 'gaam': None}
        
        self._data[image_name]['taluko'] = text
    
    def add_gaam_entry(self, image_name: str, text: str) -> None:
        """
        Store gaam data for a given image name.
        
        Args:
            image_name: Base filename without extension (e.g., "P0640001")
            text: Extracted Gujarati text from gaam image
        """
        if image_name not in self._data:
            self._data[image_name] = {'taluko': None, 'gaam': None}
        
        self._data[image_name]['gaam'] = text
    
    def get_aggregated_data(self) -> Dict:
        """
        Return the combined data structure.
        
        Returns:
            Dictionary mapping image names to their taluko and gaam data
            Format: {image_name: {taluko: "text", gaam: "text"}}
        """
        return self._data


class JSONOutputWriter:
    """Generates and writes JSON output file."""
    
    def __init__(self, error_logger: Optional['ErrorLogger'] = None):
        """
        Initialize JSONOutputWriter with optional error logger.
        
        Args:
            error_logger: ErrorLogger instance for logging errors
        """
        self.error_logger = error_logger
    
    def write_json(self, data: Dict, output_path: str) -> bool:
        """
        Write aggregated data to JSON file.
        
        Args:
            data: Dictionary mapping image names to their taluko and gaam data
                  Format: {image_name: {taluko: "text", gaam: "text"}}
            output_path: Full path to the output JSON file
            
        Returns:
            True if file was written successfully, False otherwise
        """
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not self.validate_output_directory(output_dir):
                return False
            
            # Write JSON file with proper formatting
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except PermissionError:
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'output',
                    f"Permission denied writing to file: {output_path}"
                )
            return False
            
        except OSError as e:
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'output',
                    f"OS error writing file {output_path}: {str(e)}"
                )
            return False
            
        except Exception as e:
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'output',
                    f"Unexpected error writing JSON file: {str(e)}"
                )
            return False
    
    def validate_output_directory(self, path: str) -> bool:
        """
        Ensure output directory exists, create if missing.
        
        Args:
            path: Path to the output directory
            
        Returns:
            True if directory exists or was created successfully, False otherwise
        """
        # If path is empty, assume current directory
        if not path:
            return True
        
        # Check if directory already exists
        if os.path.exists(path):
            if os.path.isdir(path):
                return True
            else:
                if self.error_logger:
                    self.error_logger.log_error(
                        'N/A',
                        'output',
                        f"Output path exists but is not a directory: {path}"
                    )
                return False
        
        # Try to create the directory
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except PermissionError:
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'output',
                    f"Permission denied creating directory: {path}"
                )
            return False
        except OSError as e:
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'output',
                    f"OS error creating directory {path}: {str(e)}"
                )
            return False
        except Exception as e:
            if self.error_logger:
                self.error_logger.log_error(
                    'N/A',
                    'output',
                    f"Unexpected error creating directory: {str(e)}"
                )
            return False


class ErrorLogger:
    """Captures and reports processing errors."""
    
    def __init__(self):
        """Initialize the error logger."""
        self.errors = []
        self.success_count = 0
        self.failure_count = 0
    
    def log_error(self, image_name: str, error_type: str, message: str) -> None:
        """
        Record an error with context.
        
        Args:
            image_name: Name of the image being processed (or "N/A" for system errors)
            error_type: Category of error (e.g., "file_system", "ocr", "output")
            message: Detailed error message
        """
        error_entry = {
            'image_name': image_name,
            'error_type': error_type,
            'message': message
        }
        self.errors.append(error_entry)
        self.failure_count += 1
        
        # Print error to console for immediate visibility
        print(f"ERROR [{error_type}] {image_name}: {message}")
    
    def log_success(self) -> None:
        """Increment the success counter."""
        self.success_count += 1
    
    def get_summary(self) -> Dict:
        """
        Return processing summary with success/failure counts.
        
        Returns:
            Dictionary containing summary statistics
        """
        return {
            'total_processed': self.success_count + self.failure_count,
            'successful': self.success_count,
            'failed': self.failure_count,
            'errors': self.errors
        }


def main():
    """Main execution flow for the OCR extraction system."""
    print("Gujarati OCR JSON Extractor")
    print("=" * 50)
    
    # Initialize error logger
    error_logger = ErrorLogger()
    
    # Initialize components
    image_discovery = ImageDiscovery(error_logger=error_logger)
    ocr_processor = OCRProcessor(language='guj', error_logger=error_logger)
    data_aggregator = DataAggregator()
    json_writer = JSONOutputWriter(error_logger=error_logger)
    
    # Define input directories and output file
    taluko_dir = 'public-taluko'
    gaam_dir = 'public-gaam'
    output_file = 'extracted_data.json'
    
    print(f"\nDiscovering images in {taluko_dir}/...")
    taluko_images = image_discovery.discover_images(taluko_dir)
    print(f"Found {len(taluko_images)} taluko images")
    
    print(f"\nDiscovering images in {gaam_dir}/...")
    gaam_images = image_discovery.discover_images(gaam_dir)
    print(f"Found {len(gaam_images)} gaam images")
    
    # Process taluko images
    print(f"\nProcessing taluko images...")
    for image_path in taluko_images:
        image_name = image_discovery.get_image_name(image_path)
        print(f"  Processing {image_name}...", end=' ')
        
        extracted_text = ocr_processor.extract_text(image_path)
        
        if extracted_text is not None:
            data_aggregator.add_taluko_entry(image_name, extracted_text)
            error_logger.log_success()
            print("[OK]")
        else:
            print("[FAIL]")
    
    # Process gaam images
    print(f"\nProcessing gaam images...")
    for image_path in gaam_images:
        image_name = image_discovery.get_image_name(image_path)
        print(f"  Processing {image_name}...", end=' ')
        
        extracted_text = ocr_processor.extract_text(image_path)
        
        if extracted_text is not None:
            data_aggregator.add_gaam_entry(image_name, extracted_text)
            error_logger.log_success()
            print("[OK]")
        else:
            print("[FAIL]")
    
    # Get aggregated data
    aggregated_data = data_aggregator.get_aggregated_data()
    
    print(f"\n" + "=" * 50)
    print(f"Processing complete!")
    print(f"Total entries aggregated: {len(aggregated_data)}")
    
    # Generate final JSON output file
    print(f"\nGenerating JSON output file: {output_file}...")
    write_success = json_writer.write_json(aggregated_data, output_file)
    
    if write_success:
        print(f"[SUCCESS] JSON file successfully created: {output_file}")
    else:
        print(f"[ERROR] Failed to create JSON file: {output_file}")
    
    # Display processing summary
    summary = error_logger.get_summary()
    print(f"\n" + "=" * 50)
    print(f"Processing Summary:")
    print(f"  Total images processed: {summary['total_processed']}")
    print(f"  Successful extractions: {summary['successful']}")
    print(f"  Failed extractions: {summary['failed']}")
    print(f"  Data entries created: {len(aggregated_data)}")
    
    if summary['failed'] > 0:
        print(f"\n[WARNING] Errors encountered: {summary['failed']}")
        print("Review the error messages above for details.")
    
    if write_success and len(aggregated_data) > 0:
        print(f"\n[SUCCESS] Extraction complete! Check {output_file} for results.")
    elif len(aggregated_data) == 0:
        print(f"\n[WARNING] No data was extracted. Check input directories and error messages.")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
