#!/usr/bin/env python3
"""
Quick runner for OCR integration tests with HTML output generation.

Usage:
    python run_ocr_test.py
    
This will:
1. Run all OCR integration tests
2. Generate ocr_test_results.html with extracted text
3. Display results in console
"""

import subprocess
import sys
import os

def main():
    print("Starting OCR Integration Tests...")
    print("=" * 70)
    
    # Run the test script
    result = subprocess.run(
        [sys.executable, 'test_ocr_integration.py'],
        capture_output=False
    )
    
    # Check if HTML was generated
    if os.path.exists('ocr_test_results.html'):
        print("\n" + "=" * 70)
        print("✓ HTML report generated successfully!")
        print("=" * 70)
        print("\nTo view the results:")
        print("  1. Open 'ocr_test_results.html' in your web browser")
        print("  2. Or use: python -m http.server 8000")
        print("     Then visit: http://localhost:8000/ocr_test_results.html")
        print("\n" + "=" * 70)
    
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())
