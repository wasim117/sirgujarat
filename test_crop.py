#!/usr/bin/env python3
"""Test script to verify cropping function works independently."""

from extract_pdf_thumbnails import main_crop_only

if __name__ == "__main__":
    print("Testing independent cropping function...")
    print("This will crop existing images from public/images/p064")
    print("to public/address-images/p064\n")
    
    main_crop_only()
