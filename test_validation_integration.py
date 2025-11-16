#!/usr/bin/env python3
"""
Integration test for OCR extraction with Gujarati validation.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gujarati_ocr_json_extractor import OCRProcessor, ErrorLogger


def test_ocr_with_validation():
    """Test OCR extraction followed by validation."""
    print("\n" + "="*70)
    print("INTEGRATION TEST: OCR Extraction + Validation")
    print("="*70)
    
    # Find a test image
    test_paths = [
        "public/address-images/p064/P0640400.jpg",
        "public-taluko/P0640001.png",
        "public-gaam/P0640001.png"
    ]
    
    image_path = None
    for path in test_paths:
        if os.path.exists(path):
            image_path = path
            break
    
    if not image_path:
        print("SKIP: No test images found")
        return None
    
    try:
        logger = ErrorLogger()
        processor = OCRProcessor(language='guj', error_logger=logger)
        
        # Extract text
        print(f"\nExtracting text from: {os.path.basename(image_path)}")
        extracted_text = processor.extract_text(image_path)
        
        if extracted_text is None:
            print("✗ Text extraction failed")
            return False
        
        print(f"✓ Extracted {len(extracted_text)} characters")
        print(f"  First 100 chars: {extracted_text[:100]}")
        
        # Validate the extracted text
        is_gujarati = processor.validate_gujarati_text(extracted_text)
        
        if is_gujarati:
            print(f"✓ Validation confirmed: Text contains Gujarati characters")
            return True
        else:
            print(f"✗ Validation failed: No Gujarati characters detected")
            print(f"  This might indicate an OCR configuration issue")
            return False
            
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def main():
    """Run integration test."""
    print("\n" + "="*70)
    print("OCR + VALIDATION INTEGRATION TEST")
    print("="*70)
    
    result = test_ocr_with_validation()
    
    if result is None:
        print("\nTest skipped - no images available")
        return True
    elif result:
        print("\n" + "="*70)
        print("✓ INTEGRATION TEST PASSED")
        print("="*70)
        return True
    else:
        print("\n" + "="*70)
        print("✗ INTEGRATION TEST FAILED")
        print("="*70)
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
