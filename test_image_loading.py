#!/usr/bin/env python3
"""
Test script to verify image loading and validation functions.
Tests the functions required for task 2.
"""

import os
import sys
from pathlib import Path
from PIL import Image
import tempfile

# Import the functions to test
from gujarati_text_extractor import (
    load_image,
    validate_image_format,
    get_image_files,
    preprocess_image,
    convert_to_grayscale,
    enhance_contrast,
    enhance_brightness,
    enhance_sharpness,
    reduce_noise_opencv
)


def test_validate_image_format():
    """Test validate_image_format function."""
    print("Testing validate_image_format()...")
    
    # Test supported formats
    assert validate_image_format("test.jpg") == True, "JPG should be supported"
    assert validate_image_format("test.jpeg") == True, "JPEG should be supported"
    assert validate_image_format("test.png") == True, "PNG should be supported"
    assert validate_image_format("test.bmp") == True, "BMP should be supported"
    assert validate_image_format("test.pdf") == True, "PDF should be supported"
    
    # Test unsupported formats
    assert validate_image_format("test.txt") == False, "TXT should not be supported"
    assert validate_image_format("test.doc") == False, "DOC should not be supported"
    
    # Test case insensitivity
    assert validate_image_format("test.JPG") == True, "JPG uppercase should be supported"
    assert validate_image_format("test.PNG") == True, "PNG uppercase should be supported"
    
    print("✓ validate_image_format() tests passed")


def test_load_image():
    """Test load_image function."""
    print("Testing load_image()...")
    
    # Create a temporary test image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        tmp_path = tmp.name
        # Create a simple test image
        test_img = Image.new('RGB', (100, 100), color='red')
        test_img.save(tmp_path)
    
    try:
        # Test loading valid image
        img = load_image(tmp_path)
        assert img is not None, "Should load valid image"
        assert isinstance(img, Image.Image), "Should return PIL Image object"
        print("✓ Successfully loaded test image")
        
        # Test loading non-existent file
        try:
            load_image("non_existent_file.png")
            assert False, "Should raise Exception for missing file"
        except Exception as e:
            assert "not found" in str(e).lower(), "Error should mention file not found"
            print("✓ Correctly raised Exception for missing file")
        
        print("✓ load_image() tests passed")
    finally:
        # Clean up - close the image first to release file handle
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except:
            pass  # Ignore cleanup errors on Windows


def test_get_image_files():
    """Test get_image_files function."""
    print("Testing get_image_files()...")
    
    # Create temporary directory with test images
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test image files
        for i in range(3):
            img = Image.new('RGB', (100, 100), color='blue')
            img.save(os.path.join(tmpdir, f"test_{i}.png"))
        
        # Create a non-image file
        with open(os.path.join(tmpdir, "readme.txt"), 'w') as f:
            f.write("test")
        
        # Test getting image files
        image_files = get_image_files(tmpdir)
        assert len(image_files) == 3, f"Should find 3 image files, found {len(image_files)}"
        assert all(f.endswith('.png') for f in image_files), "All files should be PNG"
        print(f"✓ Found {len(image_files)} image files in test directory")
        
        # Test with non-existent directory
        try:
            get_image_files("non_existent_directory")
            assert False, "Should raise FileNotFoundError for missing directory"
        except FileNotFoundError:
            print("✓ Correctly raised FileNotFoundError for missing directory")
        
        print("✓ get_image_files() tests passed")


def test_convert_to_grayscale():
    """Test convert_to_grayscale helper function."""
    print("Testing convert_to_grayscale()...")
    
    # Create a test image in RGB mode
    test_img = Image.new('RGB', (100, 100), color='red')
    assert test_img.mode == 'RGB', "Test image should start in RGB mode"
    
    # Convert to grayscale
    grayscale = convert_to_grayscale(test_img)
    assert grayscale is not None, "Should return grayscale image"
    assert isinstance(grayscale, Image.Image), "Should return PIL Image object"
    assert grayscale.mode == 'L', "Should convert to grayscale (mode L)"
    print("✓ Successfully converted image to grayscale")
    
    # Test with already grayscale image
    grayscale_again = convert_to_grayscale(grayscale)
    assert grayscale_again.mode == 'L', "Should remain grayscale"
    print("✓ convert_to_grayscale() tests passed")


def test_enhance_contrast():
    """Test enhance_contrast helper function."""
    print("Testing enhance_contrast()...")
    
    # Create a test image
    test_img = Image.new('L', (100, 100), color=128)
    
    # Enhance contrast
    enhanced = enhance_contrast(test_img, factor=1.5)
    assert enhanced is not None, "Should return enhanced image"
    assert isinstance(enhanced, Image.Image), "Should return PIL Image object"
    print("✓ Successfully enhanced contrast")
    print("✓ enhance_contrast() tests passed")


def test_enhance_brightness():
    """Test enhance_brightness helper function."""
    print("Testing enhance_brightness()...")
    
    # Create a test image
    test_img = Image.new('L', (100, 100), color=100)
    
    # Enhance brightness
    enhanced = enhance_brightness(test_img, factor=1.2)
    assert enhanced is not None, "Should return enhanced image"
    assert isinstance(enhanced, Image.Image), "Should return PIL Image object"
    print("✓ Successfully enhanced brightness")
    print("✓ enhance_brightness() tests passed")


def test_enhance_sharpness():
    """Test enhance_sharpness helper function."""
    print("Testing enhance_sharpness()...")
    
    # Create a test image
    test_img = Image.new('L', (100, 100), color=150)
    
    # Enhance sharpness
    enhanced = enhance_sharpness(test_img, factor=1.2)
    assert enhanced is not None, "Should return enhanced image"
    assert isinstance(enhanced, Image.Image), "Should return PIL Image object"
    print("✓ Successfully enhanced sharpness")
    print("✓ enhance_sharpness() tests passed")


def test_reduce_noise_opencv():
    """Test reduce_noise_opencv helper function."""
    print("Testing reduce_noise_opencv()...")
    
    # Create a test image
    test_img = Image.new('L', (100, 100), color=128)
    
    # Reduce noise
    denoised = reduce_noise_opencv(test_img)
    assert denoised is not None, "Should return denoised image"
    assert isinstance(denoised, Image.Image), "Should return PIL Image object"
    print("✓ Successfully reduced noise")
    print("✓ reduce_noise_opencv() tests passed")


def test_preprocess_image():
    """Test preprocess_image function."""
    print("Testing preprocess_image()...")
    
    # Create a test image
    test_img = Image.new('RGB', (100, 100), color='green')
    
    # Test preprocessing
    preprocessed = preprocess_image(test_img)
    assert preprocessed is not None, "Should return preprocessed image"
    assert isinstance(preprocessed, Image.Image), "Should return PIL Image object"
    assert preprocessed.mode == 'L', "Should convert to grayscale (mode L)"
    print("✓ Successfully preprocessed test image")
    print("✓ preprocess_image() tests passed")


def test_with_real_pdf_directory():
    """Test with real P064 directory if available."""
    print("\nTesting with real P064 directory...")
    
    if os.path.exists('P064'):
        try:
            image_files = get_image_files('P064')
            print(f"✓ Found {len(image_files)} PDF files in P064 directory")
            
            if image_files:
                first_file = image_files[0]
                print(f"✓ First file: {os.path.basename(first_file)}")
                print(f"✓ File format validation: {validate_image_format(first_file)}")
        except Exception as e:
            print(f"✗ Error testing with P064: {e}")
    else:
        print("⊘ P064 directory not found, skipping real directory test")


if __name__ == '__main__':
    print("="*70)
    print("IMAGE LOADING AND VALIDATION TESTS")
    print("="*70 + "\n")
    
    try:
        test_validate_image_format()
        print()
        test_load_image()
        print()
        test_get_image_files()
        print()
        test_convert_to_grayscale()
        print()
        test_enhance_contrast()
        print()
        test_enhance_brightness()
        print()
        test_enhance_sharpness()
        print()
        test_reduce_noise_opencv()
        print()
        test_preprocess_image()
        print()
        test_with_real_pdf_directory()
        
        print("\n" + "="*70)
        print("ALL TESTS PASSED ✓")
        print("="*70)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
