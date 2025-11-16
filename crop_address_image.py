#!/usr/bin/env python3
"""
Crop a specific image with custom coordinates and save to public-taluko folder.
"""

from extract_pdf_thumbnails import crop_image
from pathlib import Path

def crop_all_images():
    """Crop all images in p064 folder with specified coordinates."""
    
    # Source directory
    source_dir = "public/address-images/p064"
    
    # Output directory
    output_dir = "public-gaam"
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Crop coordinates
    left = 800
    top = 50
    width = 226
    height = 71
    
    # Get all jpg files from source directory
    source_path = Path(source_dir)
    image_files = sorted(source_path.glob("*.jpg"))
    
    total_files = len(image_files)
    success_count = 0
    failed_count = 0
    
    print(f"Cropping {total_files} images from {source_dir}...")
    print(f"Output directory: {output_dir}")
    print(f"Crop region: left={left}, top={top}, width={width}, height={height}")
    print("-" * 60)
    
    # Crop each image
    for index, image_file in enumerate(image_files, start=1):
        original_filename = image_file.name
        output_file = Path(output_dir) / original_filename
        
        print(f"[{index}/{total_files}] Cropping: {original_filename}")
        
        # Perform the crop
        success, error_message = crop_image(
            image_file,
            output_file,
            left=left,
            top=top,
            width=width,
            height=height
        )
        
        if success:
            success_count += 1
        else:
            failed_count += 1
            print(f"  ✗ Error: {error_message}")
    
    print("-" * 60)
    print(f"✓ Successfully cropped: {success_count}")
    print(f"✗ Failed: {failed_count}")
    
    return success_count, failed_count

if __name__ == "__main__":
    crop_all_images()
