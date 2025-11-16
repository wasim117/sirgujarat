#!/usr/bin/env python3
"""
Test script for OCRProcessor class.
"""

import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gujarati_ocr_json_extractor import OCRProcessor, ErrorLogger


def test_ocr_processor_initialization():
    """Test OCRProcessor initialization."""
    print("\n" + "="*70)
    print("TEST 1: OCRProcessor Initialization")
    print("="*70)
    
    try:
        # Test with default language
        processor = OCRProcessor()
        print(f"✓ OCRProcessor created with default language: {processor.language}")
        
        # Test with custom language
        processor_custom = OCRProcessor(language='eng')
        print(f"✓ OCRProcessor created with custom language: {processor_custom.language}")
        
        # Test with error logger
        logger = ErrorLogger()
        processor_with_logger = OCRProcessor(error_logger=logger)
        print(f"✓ OCRProcessor created with error logger")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_extract_text_basic():
    """Test basic text extraction."""
    print("\n" + "="*70)
    print("TEST 2: Basic Text Extraction")
    print("="*70)
    
    # Try to find a test image
    test_paths = [
        "public/address-images/p064/P0640400.jpg",
        "public-taluko/P0640001.png",
        "public-gaam/P0640001.png",
        "P064/P0640001.pdf"
    ]
    
    image_path = None
    for path in test_paths:
        if os.path.exists(path):
            image_path = path
            break
    
    if not image_path:
        print(f"SKIP: No test images found in expected locations")
        return None
    
    try:
        logger = ErrorLogger()
        processor = OCRProcessor(language='guj', error_logger=logger)
        
        # Extract text
        text = processor.extract_text(image_path)
        
        if text is not None:
            print(f"✓ Successfully extracted text from {os.path.basename(image_path)}")
            print(f"  Text length: {len(text)} characters")
            if len(text) > 0:
                print(f"  First 100 chars: {text[:100]}")
            return True
        else:
            print(f"✗ Text extraction returned None")
            return False
            
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_gujarati_validation():
    """Test Gujarati text validation."""
    print("\n" + "="*70)
    print("TEST 3: Gujarati Text Validation")
    print("="*70)
    
    try:
        processor = OCRProcessor()
        
        # Test with Gujarati text
        gujarati_text = "આ એક ગુજરાતી ટેક્સ્ટ છે"
        result = processor.validate_gujarati_text(gujarati_text)
        
        if result:
            print(f"✓ Correctly identified Gujarati text")
        else:
            print(f"✗ Failed to identify Gujarati text")
            return False
        
        # Test with English text
        english_text = "This is English text"
        result = processor.validate_gujarati_text(english_text)
        
        if not result:
            print(f"✓ Correctly rejected non-Gujarati text")
        else:
            print(f"✗ Incorrectly identified English as Gujarati")
            return False
        
        # Test with empty text
        empty_text = ""
        result = processor.validate_gujarati_text(empty_text)
        
        if not result:
            print(f"✓ Correctly rejected empty text")
        else:
            print(f"✗ Incorrectly validated empty text")
            return False
        
        # Test with mixed text (should return True if contains any Gujarati)
        mixed_text = "Hello આ છે test"
        result = processor.validate_gujarati_text(mixed_text)
        
        if result:
            print(f"✓ Correctly identified mixed text with Gujarati")
            return True
        else:
            print(f"✗ Failed to identify mixed text with Gujarati")
            return False
            
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_error_handling():
    """Test error handling for missing files."""
    print("\n" + "="*70)
    print("TEST 4: Error Handling")
    print("="*70)
    
    try:
        logger = ErrorLogger()
        processor = OCRProcessor(error_logger=logger)
        
        # Try to extract from non-existent file
        text = processor.extract_text("nonexistent_file.png")
        
        if text is None:
            print(f"✓ Correctly returned None for missing file")
            
            # Check if error was logged
            if logger.failure_count > 0:
                print(f"✓ Error was logged: {logger.errors[0]['message'][:80]}...")
                return True
            else:
                print(f"✗ Error was not logged")
                return False
        else:
            print(f"✗ Should have returned None for missing file")
            return False
            
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("OCRProcessor CLASS TESTS")
    print("="*70)
    
    results = []
    
    # Run tests
    results.append(test_ocr_processor_initialization())
    results.append(test_extract_text_basic())
    results.append(test_gujarati_validation())
    results.append(test_error_handling())
    
    # Filter out None results (skipped tests)
    actual_results = [r for r in results if r is not None]
    
    # Print summary
    passed = sum(1 for r in actual_results if r)
    total = len(actual_results)
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Passed: {passed}/{total}")
    if total > 0:
        print(f"Success Rate: {passed/total*100:.1f}%")
    print("="*70)
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
