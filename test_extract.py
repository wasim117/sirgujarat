#!/usr/bin/env python3
"""Test script to verify extraction function works independently."""

from extract_pdf_thumbnails import main_extract_only

if __name__ == "__main__":
    print("Testing independent extraction function...")
    print("This will extract PDFs from P064 to public/images/p064")
    print("WITHOUT cropping\n")
    
    main_extract_only()
