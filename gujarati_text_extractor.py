"""
Gujarati Text Extraction Module

This module provides functionality to extract Gujarati text from images using
Tesseract OCR. It supports batch processing of images with error handling,
progress logging, and summary reporting.

Requirements:
- pytesseract >= 0.3.10
- Pillow >= 10.0.0
- opencv-python >= 4.8.0 (optional, for advanced preprocessing)
- Tesseract OCR binary installed on system
- Gujarati language data for Tesseract

Installation:
    pip install -r requirements.txt
    
    For Tesseract OCR installation, see GUJARATI_TEXT_EXTRACTION_USAGE.md
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import numpy as np

try:
    import pytesseract
    from PIL import Image, ImageEnhance
    import cv2
except ImportError as e:
    print(f"Error: Required package not installed. {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


# ============================================================================
# Image Processing Module
# ============================================================================

def load_image(image_path: str) -> Optional[Image.Image]:
    """
    Load an image file using PIL.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        PIL Image object if successful, None otherwise
        
    Raises:
        FileNotFoundError: If image file does not exist
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        image = Image.open(image_path)
        return image
    except Exception as e:
        raise Exception(f"Failed to load image {image_path}: {str(e)}")


def validate_image_format(image_path: str) -> bool:
    """
    Validate that image is in a supported format (JPEG, PNG, BMP).
    
    Args:
        image_path: Path to the image file
        
    Returns:
        True if format is supported, False otherwise
    """
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.pdf'}
    file_ext = Path(image_path).suffix.lower()
    return file_ext in supported_formats


def convert_to_grayscale(image: Image.Image) -> Image.Image:
    """
    Convert image to grayscale for improved OCR processing.
    
    Args:
        image: PIL Image object
        
    Returns:
        Grayscale PIL Image object (mode 'L')
    """
    try:
        if image.mode != 'L':
            image = image.convert('L')
        return image
    except Exception as e:
        raise Exception(f"Failed to convert image to grayscale: {str(e)}")


def enhance_contrast(image: Image.Image, factor: float = 1.5) -> Image.Image:
    """
    Enhance image contrast to improve text visibility.
    
    Args:
        image: PIL Image object (should be grayscale)
        factor: Contrast enhancement factor (1.0 = no change, >1.0 = more contrast)
        
    Returns:
        Contrast-enhanced PIL Image object
    """
    try:
        enhancer = ImageEnhance.Contrast(image)
        enhanced = enhancer.enhance(factor)
        return enhanced
    except Exception as e:
        raise Exception(f"Failed to enhance contrast: {str(e)}")


def enhance_brightness(image: Image.Image, factor: float = 1.1) -> Image.Image:
    """
    Enhance image brightness for better OCR accuracy.
    
    Args:
        image: PIL Image object
        factor: Brightness enhancement factor (1.0 = no change, >1.0 = brighter)
        
    Returns:
        Brightness-enhanced PIL Image object
    """
    try:
        enhancer = ImageEnhance.Brightness(image)
        enhanced = enhancer.enhance(factor)
        return enhanced
    except Exception as e:
        raise Exception(f"Failed to enhance brightness: {str(e)}")


def enhance_sharpness(image: Image.Image, factor: float = 1.2) -> Image.Image:
    """
    Enhance image sharpness to improve text clarity.
    
    Args:
        image: PIL Image object
        factor: Sharpness enhancement factor (1.0 = no change, >1.0 = sharper)
        
    Returns:
        Sharpness-enhanced PIL Image object
    """
    try:
        enhancer = ImageEnhance.Sharpness(image)
        enhanced = enhancer.enhance(factor)
        return enhanced
    except Exception as e:
        raise Exception(f"Failed to enhance sharpness: {str(e)}")


def reduce_noise_opencv(image: Image.Image) -> Image.Image:
    """
    Apply noise reduction using OpenCV bilateral filtering.
    
    This function is optional and recommended for noisy images.
    Converts PIL Image to OpenCV format, applies bilateral filter, and converts back.
    
    Args:
        image: PIL Image object (should be grayscale)
        
    Returns:
        Noise-reduced PIL Image object
    """
    try:
        # Convert PIL Image to numpy array
        image_array = np.array(image)
        
        # Apply bilateral filter for noise reduction
        # Parameters: image, diameter, sigma_color, sigma_space
        denoised = cv2.bilateralFilter(image_array, 9, 75, 75)
        
        # Convert back to PIL Image
        result_image = Image.fromarray(denoised)
        return result_image
    except Exception as e:
        raise Exception(f"Failed to reduce noise: {str(e)}")


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Apply preprocessing techniques to improve OCR accuracy.
    
    Preprocessing includes:
    - Conversion to grayscale
    - Contrast enhancement
    - Brightness enhancement
    - Sharpness enhancement
    
    Args:
        image: PIL Image object
        
    Returns:
        Preprocessed PIL Image object
    """
    try:
        # Convert to grayscale
        image = convert_to_grayscale(image)
        
        # Enhance contrast
        image = enhance_contrast(image, factor=1.5)
        
        # Enhance brightness
        image = enhance_brightness(image, factor=1.1)
        
        # Enhance sharpness
        image = enhance_sharpness(image, factor=1.2)
        
        return image
    except Exception as e:
        raise Exception(f"Failed to preprocess image: {str(e)}")


def get_image_files(source_dir: str) -> List[str]:
    """
    Retrieve list of image files from directory.
    
    Args:
        source_dir: Path to source directory
        
    Returns:
        List of image file paths
        
    Raises:
        FileNotFoundError: If source directory does not exist
    """
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    
    if not os.path.isdir(source_dir):
        raise NotADirectoryError(f"Path is not a directory: {source_dir}")
    
    image_files = []
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.pdf'}
    
    for file in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file)
        if os.path.isfile(file_path):
            file_ext = Path(file_path).suffix.lower()
            if file_ext in supported_formats:
                image_files.append(file_path)
    
    return sorted(image_files)


# ============================================================================
# OCR Engine Module
# ============================================================================

def extract_text_from_image(image: Image.Image, language: str = 'guj') -> str:
    """
    Extract Gujarati text from image using Tesseract OCR.
    
    Args:
        image: PIL Image object
        language: Language code for OCR (default: 'guj' for Gujarati)
        
    Returns:
        Extracted text string
        
    Raises:
        Exception: If OCR processing fails (Tesseract not installed, language data missing, etc.)
    """
    try:
        text = pytesseract.image_to_string(image, lang=language)
        return text
    except pytesseract.TesseractNotFoundError:
        raise Exception(
            "Tesseract OCR is not installed or not found in system PATH. "
            "Please install Tesseract OCR. See GUJARATI_TEXT_EXTRACTION_USAGE.md for instructions."
        )
    except pytesseract.TesseractFileNotFoundError:
        raise Exception(
            "Tesseract executable not found. "
            "Please ensure Tesseract OCR is properly installed and in system PATH."
        )
    except Exception as e:
        error_msg = str(e).lower()
        if 'language' in error_msg or 'guj' in error_msg or 'data' in error_msg:
            raise Exception(
                f"Gujarati language data not found or not installed. "
                f"Please ensure Tesseract Gujarati language support is installed. "
                f"Original error: {str(e)}"
            )
        else:
            raise Exception(f"OCR extraction failed: {str(e)}")


def get_confidence_score(image: Image.Image, language: str = 'guj') -> float:
    """
    Extract confidence score from OCR result.
    
    Args:
        image: PIL Image object
        language: Language code for OCR
        
    Returns:
        Confidence score (0-100). Returns 0.0 if no text detected or confidence cannot be determined.
    """
    try:
        data = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT)
        confidences = [int(conf) for conf in data['confidence'] if int(conf) > 0]
        
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            return avg_confidence
        return 0.0
    except pytesseract.TesseractNotFoundError:
        raise Exception(
            "Tesseract OCR is not installed or not found in system PATH. "
            "Please install Tesseract OCR. See GUJARATI_TEXT_EXTRACTION_USAGE.md for instructions."
        )
    except pytesseract.TesseractFileNotFoundError:
        raise Exception(
            "Tesseract executable not found. "
            "Please ensure Tesseract OCR is properly installed and in system PATH."
        )
    except Exception as e:
        error_msg = str(e).lower()
        if 'language' in error_msg or 'guj' in error_msg or 'data' in error_msg:
            raise Exception(
                f"Gujarati language data not found or not installed. "
                f"Please ensure Tesseract Gujarati language support is installed. "
                f"Original error: {str(e)}"
            )
        else:
            raise Exception(f"Failed to extract confidence score: {str(e)}")


def validate_gujarati_text(text: str) -> bool:
    """
    Verify that extracted text contains Gujarati characters.
    
    Gujarati Unicode range: U+0A80 to U+0AFF
    
    Args:
        text: Extracted text string
        
    Returns:
        True if text contains Gujarati characters, False otherwise
    """
    gujarati_range = range(0x0A80, 0x0B00)
    for char in text:
        if ord(char) in gujarati_range:
            return True
    return False


# ============================================================================
# File I/O Module
# ============================================================================

def ensure_output_directory(output_path: str) -> None:
    """
    Create output directory structure if it doesn't exist.
    
    Args:
        output_path: Path to output directory
        
    Raises:
        Exception: If directory creation fails
    """
    try:
        os.makedirs(output_path, exist_ok=True)
    except Exception as e:
        raise Exception(f"Failed to create output directory {output_path}: {str(e)}")


def save_extracted_text(text: str, output_path: str) -> None:
    """
    Write extracted text to output file.
    
    Args:
        text: Extracted text content
        output_path: Path to output file
        
    Raises:
        Exception: If file writing fails
    """
    try:
        # Ensure parent directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            ensure_output_directory(output_dir)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        raise Exception(f"Failed to save text to {output_path}: {str(e)}")


# ============================================================================
# Batch Processing Module
# ============================================================================

def process_single_image(image_path: str, output_path: str) -> Dict:
    """
    Extract text from a single image and save to output file.
    
    Args:
        image_path: Path to input image
        output_path: Path to output text file
        
    Returns:
        Dictionary with processing result
    """
    result = {
        'success': False,
        'text': '',
        'confidence': 0.0,
        'error': None,
        'filename': os.path.basename(image_path)
    }
    
    try:
        # Validate image format
        if not validate_image_format(image_path):
            raise ValueError(f"Unsupported image format: {image_path}")
        
        # Load image
        image = load_image(image_path)
        
        # Preprocess image
        preprocessed_image = preprocess_image(image)
        
        # Extract text
        text = extract_text_from_image(preprocessed_image)
        
        # Get confidence score
        confidence = get_confidence_score(preprocessed_image)
        
        # Save extracted text
        save_extracted_text(text, output_path)
        
        result['success'] = True
        result['text'] = text
        result['confidence'] = confidence
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


def process_image_for_testing(image_path: str, output_dir: str = 'output') -> Dict:
    """
    Process single image for testing with console output.
    
    Args:
        image_path: Path to input image
        output_dir: Directory for output files
        
    Returns:
        Dictionary with processing result
    """
    # Ensure output directory exists
    ensure_output_directory(output_dir)
    
    # Generate output filename
    base_name = Path(image_path).stem
    output_path = os.path.join(output_dir, f"{base_name}.txt")
    
    # Process image
    result = process_single_image(image_path, output_path)
    
    # Display results to console
    print("\n" + "="*70)
    print("SINGLE IMAGE PROCESSING RESULT")
    print("="*70)
    print(f"Image: {os.path.basename(image_path)}")
    print(f"Status: {'SUCCESS' if result['success'] else 'FAILED'}")
    
    if result['success']:
        print(f"Confidence Score: {result['confidence']:.2f}%")
        print(f"Output File: {output_path}")
        print("\nExtracted Text:")
        print("-"*70)
        print(result['text'][:500] if len(result['text']) > 500 else result['text'])
        if len(result['text']) > 500:
            print(f"... (truncated, total length: {len(result['text'])} characters)")
    else:
        print(f"Error: {result['error']}")
    
    print("="*70 + "\n")
    
    return result


def process_image_directory(source_dir: str, output_dir: str = 'output') -> Dict:
    """
    Batch process all images in source directory.
    
    Args:
        source_dir: Path to source directory containing images
        output_dir: Path to output directory for text files
        
    Returns:
        Dictionary with processing summary
    """
    results = {
        'success': 0,
        'failed': 0,
        'errors': [],
        'elapsed_time': 0.0,
        'output_dir': output_dir,
        'total_files': 0
    }
    
    start_time = time.time()
    
    try:
        # Get list of image files
        image_files = get_image_files(source_dir)
        results['total_files'] = len(image_files)
        
        if not image_files:
            print(f"No image files found in {source_dir}")
            return results
        
        # Ensure output directory exists
        ensure_output_directory(output_dir)
        
        # Process each image
        for idx, image_path in enumerate(image_files, 1):
            # Log progress
            log_progress(idx, len(image_files), os.path.basename(image_path))
            
            # Generate output filename
            base_name = Path(image_path).stem
            output_path = os.path.join(output_dir, f"{base_name}.txt")
            
            # Process image
            result = process_single_image(image_path, output_path)
            
            if result['success']:
                results['success'] += 1
            else:
                results['failed'] += 1
                error_info = {
                    'filename': result['filename'],
                    'error': result['error']
                }
                results['errors'].append(error_info)
                log_error(result['filename'], result['error'])
    
    except Exception as e:
        log_error("batch_processing", str(e))
        results['errors'].append({
            'filename': 'batch_processing',
            'error': str(e)
        })
    
    finally:
        results['elapsed_time'] = time.time() - start_time
    
    return results


# ============================================================================
# Reporting Module
# ============================================================================

def log_progress(current: int, total: int, filename: str) -> None:
    """
    Display processing progress to console.
    
    Args:
        current: Current file number
        total: Total number of files
        filename: Name of file being processed
    """
    percentage = (current / total) * 100
    print(f"[{current}/{total}] ({percentage:.1f}%) Processing: {filename}")


def log_error(filename: str, error_message: str) -> None:
    """
    Record processing error to console.
    
    Args:
        filename: Name of file that failed
        error_message: Error message
    """
    print(f"  ✗ ERROR in {filename}: {error_message}")


def generate_summary_report(results: Dict) -> None:
    """
    Display final processing summary report.
    
    Args:
        results: Dictionary with processing results
    """
    print("\n" + "="*70)
    print("PROCESSING SUMMARY REPORT")
    print("="*70)
    print(f"Total Files Processed: {results['total_files']}")
    print(f"Successful: {results['success']}")
    print(f"Failed: {results['failed']}")
    print(f"Execution Time: {results['elapsed_time']:.2f} seconds")
    print(f"Output Directory: {results['output_dir']}")
    
    if results['errors']:
        print("\nErrors:")
        print("-"*70)
        for error in results['errors']:
            print(f"  • {error['filename']}: {error['error']}")
    
    print("="*70 + "\n")


# ============================================================================
# Main Execution Functions
# ============================================================================

def main_test_single_image(image_path: Optional[str] = None, output_dir: str = 'output') -> None:
    """
    Test text extraction with first image in directory.
    
    Args:
        image_path: Path to specific image (if None, uses first image from P064 directory)
        output_dir: Directory for output files
    """
    try:
        if image_path is None:
            # Try to find first image in P064 directory
            p064_dir = 'P064'
            if os.path.exists(p064_dir):
                image_files = get_image_files(p064_dir)
                if image_files:
                    image_path = image_files[0]
                else:
                    print(f"No image files found in {p064_dir}")
                    return
            else:
                print(f"Directory {p064_dir} not found")
                return
        
        print(f"Testing with image: {image_path}")
        process_image_for_testing(image_path, output_dir)
        
    except Exception as e:
        print(f"Error during single image testing: {str(e)}")


def main_process_directory(source_dir: str = 'P064', output_dir: str = 'output') -> None:
    """
    Batch process all images in directory.
    
    Args:
        source_dir: Source directory containing images
        output_dir: Output directory for text files
    """
    try:
        print(f"Starting batch processing from: {source_dir}")
        print(f"Output directory: {output_dir}\n")
        
        results = process_image_directory(source_dir, output_dir)
        generate_summary_report(results)
        
    except Exception as e:
        print(f"Error during batch processing: {str(e)}")


def main() -> None:
    """
    Main entry point for the Gujarati Text Extraction module.
    
    Supports command-line arguments:
        python gujarati_text_extractor.py [--test] [--source SOURCE_DIR] [--output OUTPUT_DIR]
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Gujarati Text Extraction from Images using Tesseract OCR'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test with single image instead of batch processing'
    )
    parser.add_argument(
        '--source',
        default='P064',
        help='Source directory containing images (default: P064)'
    )
    parser.add_argument(
        '--output',
        default='output',
        help='Output directory for extracted text files (default: output)'
    )
    parser.add_argument(
        '--image',
        help='Specific image file to process (for testing)'
    )
    
    args = parser.parse_args()
    
    if args.test:
        main_test_single_image(args.image, args.output)
    else:
        main_process_directory(args.source, args.output)


if __name__ == '__main__':
    main()
