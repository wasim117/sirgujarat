#!/usr/bin/env python3
"""
PDF Thumbnail Extractor

Extracts the first page from PDF files as JPEG images.
Processes all PDFs in a source directory and saves thumbnails to an output directory.

Usage:
    # Run both extraction and cropping (default)
    python extract_pdf_thumbnails.py
    
    # Or import and run specific functions:
    from extract_pdf_thumbnails import main_extract_only, main_crop_only, main_extract_and_crop
    
    main_extract_only()        # Extract PDFs to images only
    main_crop_only()           # Crop existing images only
    main_extract_and_crop()    # Extract and crop in one workflow
"""

import fitz  # PyMuPDF
from PIL import Image
from pathlib import Path
import time


def extract_first_page(pdf_path: Path, output_path: Path, dpi: int = 150) -> tuple:
    """
    Extracts the first page from a PDF and saves as JPEG.
    
    Args:
        pdf_path: Path to source PDF file
        output_path: Path where JPEG should be saved
        dpi: Resolution for rendering (default 150)
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    pdf_document = None
    
    try:
        # Open the PDF file using PyMuPDF
        pdf_document = fitz.open(pdf_path)
        
        # Check if PDF has pages (handle empty PDFs)
        if pdf_document.page_count == 0:
            error_msg = "PDF file is empty (no pages)"
            return False, error_msg
        
        # Get the first page (index 0)
        first_page = pdf_document[0]
        
        # Calculate zoom factor for desired DPI (72 is default PDF DPI)
        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)
        
        # Render page to pixmap at specified DPI
        pixmap = first_page.get_pixmap(matrix=matrix)
        
        # Convert pixmap to PIL Image
        # PyMuPDF pixmap provides image data in RGB or RGBA format
        img_data = pixmap.samples
        img_mode = "RGBA" if pixmap.alpha else "RGB"
        img_size = (pixmap.width, pixmap.height)
        
        # Create PIL Image from pixmap data
        pil_image = Image.frombytes(img_mode, img_size, img_data)
        
        # Handle transparency by converting to RGB with white background
        if pil_image.mode == "RGBA":
            # Create white background
            white_background = Image.new("RGB", pil_image.size, (255, 255, 255))
            # Paste image onto white background using alpha channel as mask
            white_background.paste(pil_image, mask=pil_image.split()[3])
            pil_image = white_background
        elif pil_image.mode != "RGB":
            # Ensure RGB mode for JPEG compatibility
            pil_image = pil_image.convert("RGB")
        
        # Save as JPEG with quality setting of 85 and optimization enabled
        pil_image.save(output_path, "JPEG", quality=85, optimize=True)
        
        return True, None
    
    except fitz.FileDataError as e:
        # Handle corrupted PDF files
        error_msg = f"Corrupted or invalid PDF file - {str(e)}"
        return False, error_msg
    
    except fitz.EmptyFileError as e:
        # Handle empty PDF files
        error_msg = f"Empty PDF file - {str(e)}"
        return False, error_msg
    
    except IndexError as e:
        # Handle PDFs with no accessible pages
        error_msg = f"Cannot access first page - {str(e)}"
        return False, error_msg
    
    except PermissionError as e:
        # Handle file permission issues
        error_msg = f"Permission denied - {str(e)}"
        return False, error_msg
    
    except OSError as e:
        # Handle file system errors (file not found, disk full, etc.)
        error_msg = f"File system error - {str(e)}"
        return False, error_msg
    
    except Exception as e:
        # Catch-all for any unexpected errors
        error_msg = f"Unexpected error - {str(e)}"
        return False, error_msg
    
    finally:
        # Ensure PDF document is closed to free resources
        if pdf_document is not None:
            try:
                pdf_document.close()
            except Exception:
                # Silently ignore errors during cleanup
                pass


def crop_image(image_path: Path, output_path: Path, left: int, top: int, width: int, height: int) -> tuple:
    """
    Crops an image to specified coordinates and saves the result.
    
    Args:
        image_path: Path to source image file
        output_path: Path where cropped image should be saved
        left: Left coordinate of crop region
        top: Top coordinate of crop region
        width: Width of crop region
        height: Height of crop region
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    try:
        # Load the image using PIL
        image = Image.open(image_path)
        
        # Calculate crop box coordinates (left, top, right, bottom)
        right = left + width
        bottom = top + height
        crop_box = (left, top, right, bottom)
        
        # Validate that crop region is within image boundaries before cropping
        if left < 0 or top < 0:
            error_msg = f"Crop coordinates cannot be negative (left={left}, top={top})"
            return False, error_msg
        
        if right > image.width or bottom > image.height:
            error_msg = f"Crop region exceeds image boundaries (image: {image.width}x{image.height}, crop: {right}x{bottom})"
            return False, error_msg
        
        if width <= 0 or height <= 0:
            error_msg = f"Crop dimensions must be positive (width={width}, height={height})"
            return False, error_msg
        
        # Use image.crop() method to extract the specified region
        cropped_image = image.crop(crop_box)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save cropped image as JPEG with quality setting of 85
        cropped_image.save(output_path, "JPEG", quality=85, optimize=True)
        
        return True, None
    
    except FileNotFoundError as e:
        error_msg = f"Source image not found - {str(e)}"
        return False, error_msg
    
    except PermissionError as e:
        error_msg = f"Permission denied - {str(e)}"
        return False, error_msg
    
    except OSError as e:
        error_msg = f"File system error - {str(e)}"
        return False, error_msg
    
    except Exception as e:
        error_msg = f"Unexpected error during cropping - {str(e)}"
        return False, error_msg


def ensure_output_directory(output_path: Path) -> None:
    """
    Creates output directory structure if it doesn't exist.
    
    Args:
        output_path: Path to output directory
    """
    output_path.mkdir(parents=True, exist_ok=True)


def get_pdf_files(source_dir: Path) -> list:
    """
    Gets list of all PDF files from source directory.
    
    Args:
        source_dir: Path to directory containing PDFs
    
    Returns:
        list: List of Path objects for PDF files
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")
    
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_dir}")
    
    return sorted(source_dir.glob('*.pdf'))


def process_image_cropping(source_dir: str, output_dir: str, left: int = 133, top: int = 425, width: int = 1058, height: int = 393) -> dict:
    """
    Crops all images in a directory to specified coordinates.
    
    Args:
        source_dir: Path to directory containing source images
        output_dir: Path to output directory for cropped images
        left: Left coordinate of crop region (default 133)
        top: Top coordinate of crop region (default 425)
        width: Width of crop region (default 1058)
        height: Height of crop region (default 393)
    
    Returns:
        dict: Summary with 'success', 'failed', 'errors', 'elapsed_time', and 'output_dir' keys
    """
    # Convert string paths to Path objects
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    # Ensure output directory exists
    ensure_output_directory(output_path)
    
    # Get list of all image files (jpg, jpeg, png)
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
        image_files.extend(source_path.glob(ext))
    image_files = sorted(image_files)
    
    total_files = len(image_files)
    
    # Initialize counters and error tracking
    success_count = 0
    failed_count = 0
    errors = []
    
    # Start timing
    start_time = time.time()
    
    print(f"Cropping {total_files} images from {source_dir}...")
    print(f"Output directory: {output_dir}")
    print(f"Crop region: left={left}, top={top}, width={width}, height={height}")
    print("-" * 50)
    
    # Iterate through all images
    for index, image_file in enumerate(image_files, start=1):
        # Display progress information
        print(f"[{index}/{total_files}] Cropping: {image_file.name}")
        
        # Generate output filename (same name)
        output_file_path = output_path / image_file.name
        
        # Crop the image
        success, error_message = crop_image(
            image_file,
            output_file_path,
            left=left,
            top=top,
            width=width,
            height=height
        )
        
        # Track success and failure counts
        if success:
            success_count += 1
        else:
            failed_count += 1
            # Collect error details
            errors.append({
                'filename': image_file.name,
                'error': error_message if error_message else 'Unknown error'
            })
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Return summary
    return {
        'success': success_count,
        'failed': failed_count,
        'errors': errors,
        'elapsed_time': elapsed_time,
        'output_dir': output_dir
    }


def process_pdf_directory(source_dir: str, output_dir: str, address_output_dir: str = None, dpi: int = 150) -> dict:
    """
    Processes all PDFs in a directory.
    
    Args:
        source_dir: Path to directory containing PDFs
        output_dir: Path to output directory for images
        address_output_dir: Path to output directory for cropped address images (optional)
        dpi: Resolution for rendering
    
    Returns:
        dict: Summary with 'success', 'failed', 'errors', 'elapsed_time', 'output_dir', 
              'crop_success', 'crop_failed', and 'address_output_dir' keys
    """
    # Convert string paths to Path objects
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    # Ensure output directory exists
    ensure_output_directory(output_path)
    
    # Create address-images output directory if specified
    address_output_path = None
    if address_output_dir:
        address_output_path = Path(address_output_dir)
        ensure_output_directory(address_output_path)
    
    # Get list of all PDF files
    pdf_files = get_pdf_files(source_path)
    total_files = len(pdf_files)
    
    # Initialize counters and error tracking
    success_count = 0
    failed_count = 0
    crop_success_count = 0
    crop_failed_count = 0
    errors = []
    
    # Start timing - track elapsed time using time module
    start_time = time.time()
    
    print(f"Processing {total_files} PDF files from {source_dir}...")
    print(f"Output directory: {output_dir}")
    if address_output_dir:
        print(f"Address output directory: {address_output_dir}")
    print("-" * 50)
    
    # Iterate through all PDFs in source directory
    for index, pdf_file in enumerate(pdf_files, start=1):
        # Display progress information during processing (file X of Y)
        print(f"[{index}/{total_files}] Processing: {pdf_file.name}")
        
        # Generate output filename (same name but .jpg extension)
        output_filename = pdf_file.stem + ".jpg"
        output_file_path = output_path / output_filename
        
        # Process the PDF file
        success, error_message = extract_first_page(pdf_file, output_file_path, dpi)
        
        # Track success and failure counts during processing
        if success:
            success_count += 1
            
            # After each successful PDF extraction, call crop_image() with coordinates
            if address_output_path:
                address_output_file_path = address_output_path / output_filename
                crop_success, crop_error = crop_image(
                    output_file_path, 
                    address_output_file_path,
                    left=133,
                    top=425,
                    width=1058,
                    height=393
                )
                
                # Track cropping success and failure counts separately
                if crop_success:
                    crop_success_count += 1
                else:
                    crop_failed_count += 1
                    # Add cropping errors to the error report
                    errors.append({
                        'filename': pdf_file.name,
                        'error': f"Cropping failed - {crop_error if crop_error else 'Unknown error'}"
                    })
        else:
            failed_count += 1
            # Collect error details in a list for final reporting
            errors.append({
                'filename': pdf_file.name,
                'error': error_message if error_message else 'Unknown error'
            })
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Return summary with success, failed, errors, elapsed_time, output_dir, and cropping stats
    result = {
        'success': success_count,
        'failed': failed_count,
        'errors': errors,
        'elapsed_time': elapsed_time,
        'output_dir': output_dir
    }
    
    # Add cropping statistics if address output directory was specified
    if address_output_dir:
        result['crop_success'] = crop_success_count
        result['crop_failed'] = crop_failed_count
        result['address_output_dir'] = address_output_dir
    
    return result


def main_extract_only():
    """Extract PDF thumbnails only (without cropping)."""
    # Configuration
    source_dir = 'P064'
    output_dir = 'public/images/p064'
    dpi = 150
    
    # Process PDFs without cropping
    result = process_pdf_directory(source_dir, output_dir, address_output_dir=None, dpi=dpi)
    
    # Create summary report
    print("\n" + "="*60)
    print("PDF EXTRACTION SUMMARY")
    print("="*60)
    print(f"Total files processed:  {result['success'] + result['failed']}")
    print(f"Successfully processed: {result['success']}")
    print(f"Failed:                 {result['failed']}")
    print(f"Total time:             {result['elapsed_time']:.2f} seconds")
    print(f"Output directory:       {result['output_dir']}")
    print("="*60)
    
    # Print detailed error list if any failures occurred
    if result['errors']:
        print("\nDETAILED ERROR LIST:")
        print("-" * 60)
        for idx, error in enumerate(result['errors'], start=1):
            print(f"{idx}. {error['filename']}")
            print(f"   Error: {error['error']}")
        print("-" * 60)


def main_crop_only():
    """Crop existing images to address region only."""
    # Configuration
    source_dir = 'public/images/p064'
    output_dir = 'public/address-images/p064'
    
    # Process image cropping
    result = process_image_cropping(
        source_dir,
        output_dir,
        left=133,
        top=425,
        width=1058,
        height=393
    )
    
    # Create summary report
    print("\n" + "="*60)
    print("IMAGE CROPPING SUMMARY")
    print("="*60)
    print(f"Total files processed:  {result['success'] + result['failed']}")
    print(f"Successfully cropped:   {result['success']}")
    print(f"Failed:                 {result['failed']}")
    print(f"Total time:             {result['elapsed_time']:.2f} seconds")
    print(f"Output directory:       {result['output_dir']}")
    print("="*60)
    
    # Print detailed error list if any failures occurred
    if result['errors']:
        print("\nDETAILED ERROR LIST:")
        print("-" * 60)
        for idx, error in enumerate(result['errors'], start=1):
            print(f"{idx}. {error['filename']}")
            print(f"   Error: {error['error']}")
        print("-" * 60)


def main_extract_and_crop():
    """Extract PDF thumbnails and crop to address region (combined workflow)."""
    # Configuration
    source_dir = 'P064'
    output_dir = 'public/images/p064'
    address_output_dir = 'public/address-images/p064'
    dpi = 150
    
    # Process PDFs with cropping
    result = process_pdf_directory(source_dir, output_dir, address_output_dir, dpi)
    
    # Create summary report
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    print(f"Total files processed:  {result['success'] + result['failed']}")
    print(f"Successfully processed: {result['success']}")
    print(f"Failed:                 {result['failed']}")
    
    # Include cropped image count in summary report if cropping was enabled
    if 'crop_success' in result:
        print(f"Cropped successfully:   {result['crop_success']}")
        print(f"Cropping failed:        {result['crop_failed']}")
    
    print(f"Total time:             {result['elapsed_time']:.2f} seconds")
    print(f"Output directory:       {result['output_dir']}")
    
    # Show address-images output directory path in summary
    if 'address_output_dir' in result:
        print(f"Address output dir:     {result['address_output_dir']}")
    
    print("="*60)
    
    # Print detailed error list if any failures occurred
    if result['errors']:
        print("\nDETAILED ERROR LIST:")
        print("-" * 60)
        for idx, error in enumerate(result['errors'], start=1):
            print(f"{idx}. {error['filename']}")
            print(f"   Error: {error['error']}")
        print("-" * 60)


def main():
    """Main execution function - runs combined extract and crop workflow."""
    main_extract_and_crop()


if __name__ == "__main__":
    main()
