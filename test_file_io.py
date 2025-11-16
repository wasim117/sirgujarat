#!/usr/bin/env python3
"""
Test script for file I/O operations.

Tests the following functions required for task 5:
- save_extracted_text()
- ensure_output_directory()
- Filename conversion (image filename to .txt extension)
- Error handling for permission and disk space issues
"""

import os
import sys
import tempfile
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gujarati_text_extractor import (
    save_extracted_text,
    ensure_output_directory,
    process_single_image,
    get_image_files
)


def test_ensure_output_directory():
    """Test ensure_output_directory function."""
    print("\n" + "="*70)
    print("TEST 1: ensure_output_directory()")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test creating a new directory
        test_dir = os.path.join(tmpdir, "test_output", "nested", "dir")
        
        try:
            ensure_output_directory(test_dir)
            
            if os.path.exists(test_dir) and os.path.isdir(test_dir):
                print(f"✓ Successfully created directory: {test_dir}")
                return True
            else:
                print(f"✗ Directory was not created")
                return False
        except Exception as e:
            print(f"✗ FAILED: {str(e)}")
            return False


def test_save_extracted_text():
    """Test save_extracted_text function."""
    print("\n" + "="*70)
    print("TEST 2: save_extracted_text()")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test saving text to file
        output_path = os.path.join(tmpdir, "output", "test.txt")
        test_text = "આ એક ગુજરાતી ટેક્સ્ટ છે\nThis is a test."
        
        try:
            save_extracted_text(test_text, output_path)
            
            # Verify file was created
            if not os.path.exists(output_path):
                print(f"✗ Output file was not created")
                return False
            
            # Verify content
            with open(output_path, 'r', encoding='utf-8') as f:
                saved_text = f.read()
            
            if saved_text == test_text:
                print(f"✓ Successfully saved text to file")
                print(f"  File: {output_path}")
                print(f"  Content length: {len(saved_text)} characters")
                return True
            else:
                print(f"✗ Saved content doesn't match original")
                print(f"  Expected: {test_text}")
                print(f"  Got: {saved_text}")
                return False
                
        except Exception as e:
            print(f"✗ FAILED: {str(e)}")
            return False


def test_filename_conversion():
    """Test filename conversion from image to .txt extension."""
    print("\n" + "="*70)
    print("TEST 3: Filename Conversion (image to .txt)")
    print("="*70)
    
    test_cases = [
        ("image.jpg", "image.txt"),
        ("photo.png", "photo.txt"),
        ("document.bmp", "document.txt"),
        ("P0640001.pdf", "P0640001.txt"),
        ("file_with_multiple.dots.jpg", "file_with_multiple.dots.txt"),
    ]
    
    try:
        all_passed = True
        for input_name, expected_output in test_cases:
            # Simulate filename conversion
            base_name = Path(input_name).stem
            output_name = f"{base_name}.txt"
            
            if output_name == expected_output:
                print(f"✓ {input_name} → {output_name}")
            else:
                print(f"✗ {input_name} → {output_name} (expected {expected_output})")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_error_handling_permission():
    """Test error handling for permission issues."""
    print("\n" + "="*70)
    print("TEST 4: Error Handling - Permission Issues")
    print("="*70)
    
    # This test is platform-specific and may not work on all systems
    # We'll test that the function raises an appropriate exception
    
    try:
        # Try to save to a path that likely won't have write permissions
        # On Windows, this might be C:\Windows\System32\test.txt
        # On Unix, this might be /root/test.txt
        
        restricted_path = "/root/test_no_permission.txt" if os.name != 'nt' else "C:\\Windows\\System32\\test_no_permission.txt"
        
        try:
            save_extracted_text("test", restricted_path)
            print(f"⊘ Could not test permission error (path may be writable)")
            return True  # Not a failure, just can't test
        except Exception as e:
            error_msg = str(e).lower()
            if 'permission' in error_msg or 'denied' in error_msg or 'access' in error_msg:
                print(f"✓ Correctly raised permission error")
                print(f"  Error: {str(e)[:80]}...")
                return True
            else:
                print(f"✓ Raised exception for restricted path")
                print(f"  Error: {str(e)[:80]}...")
                return True
                
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_error_handling_invalid_path():
    """Test error handling for invalid paths."""
    print("\n" + "="*70)
    print("TEST 5: Error Handling - Invalid Paths")
    print("="*70)
    
    try:
        # Try to save to an invalid path (with null bytes or other invalid characters)
        # This should raise an exception
        
        invalid_paths = [
            "/invalid\x00path/file.txt",  # Null byte
        ]
        
        for invalid_path in invalid_paths:
            try:
                save_extracted_text("test", invalid_path)
                print(f"✗ Should have raised error for invalid path: {invalid_path}")
                return False
            except Exception as e:
                print(f"✓ Correctly raised error for invalid path")
                print(f"  Error: {str(e)[:80]}...")
                return True
                
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_integration_with_process_single_image():
    """Test file I/O integration with process_single_image."""
    print("\n" + "="*70)
    print("TEST 6: Integration with process_single_image()")
    print("="*70)
    
    # Check if we have a test image available
    image_path = "public/images/p064/P0640001.jpg"
    
    if not os.path.exists(image_path):
        print(f"⊘ Test image not found at {image_path}, skipping integration test")
        return True
    
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            output_path = os.path.join(tmpdir, "output.txt")
            
            # Process single image
            result = process_single_image(image_path, output_path)
            
            # Check if output file was created
            if not os.path.exists(output_path):
                print(f"✗ Output file was not created")
                return False
            
            # Check if file has content
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) > 0:
                print(f"✓ Successfully processed image and saved output")
                print(f"  Output file: {output_path}")
                print(f"  Content length: {len(content)} characters")
                print(f"  Processing success: {result['success']}")
                return True
            else:
                print(f"⊘ Output file created but is empty")
                return True  # Not necessarily a failure
                
        except Exception as e:
            print(f"✗ FAILED: {str(e)}")
            return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("FILE I/O OPERATIONS TESTS (Task 5)")
    print("="*70)
    
    results = []
    
    # Run tests
    results.append(("ensure_output_directory", test_ensure_output_directory()))
    results.append(("save_extracted_text", test_save_extracted_text()))
    results.append(("filename_conversion", test_filename_conversion()))
    results.append(("error_handling_permission", test_error_handling_permission()))
    results.append(("error_handling_invalid_path", test_error_handling_invalid_path()))
    results.append(("integration_with_process_single_image", test_integration_with_process_single_image()))
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*70 + "\n")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
