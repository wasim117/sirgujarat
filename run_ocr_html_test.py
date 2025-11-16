#!/usr/bin/env python3
"""
Simple runner script for OCR integration tests with HTML output.

This script runs the OCR tests and generates an HTML report that can be
viewed in a web browser with proper Gujarati text encoding.

Usage:
    python run_ocr_html_test.py

Output:
    - Console output with test results
    - ocr_test_results.html - HTML report with extracted text
"""

import subprocess
import sys
import os
import webbrowser
from pathlib import Path


def run_tests():
    """Run the OCR integration tests."""
    print("Starting OCR Integration Tests with HTML Output...")
    print("=" * 70)
    
    try:
        # Run the test script
        result = subprocess.run(
            [sys.executable, 'test_ocr_integration.py'],
            capture_output=False,
            text=True
        )
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        return False


def open_html_report():
    """Open the generated HTML report in default browser."""
    html_file = 'ocr_test_results.html'
    
    if os.path.exists(html_file):
        print("\n" + "=" * 70)
        print("HTML Report Generated Successfully!")
        print("=" * 70)
        print(f"\nReport saved to: {os.path.abspath(html_file)}")
        
        try:
            # Try to open in default browser
            webbrowser.open(f'file://{os.path.abspath(html_file)}')
            print("Opening report in default browser...")
        except Exception as e:
            print(f"Could not open browser automatically: {str(e)}")
            print(f"Please open the file manually: {html_file}")
    else:
        print(f"\nWarning: HTML report not found at {html_file}")


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("OCR Integration Test Runner")
    print("=" * 70)
    print("\nConfiguration:")
    print("  - Image: public/address-images/p064/P0640400.jpg")
    print("  - Language: Gujarati (guj)")
    print("  - Output: ocr_test_results.html")
    print("\n" + "=" * 70 + "\n")
    
    # Run tests
    success = run_tests()
    
    # Open HTML report
    if success:
        open_html_report()
    
    print("\n" + "=" * 70)
    print("Test execution completed!")
    print("=" * 70 + "\n")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
