#!/usr/bin/env python3
"""
Test script for ImageDiscovery class
"""

import os
import tempfile
from gujarati_ocr_json_extractor import ImageDiscovery, ErrorLogger


def test_discover_images():
    """Test image discovery functionality."""
    discovery = ImageDiscovery()
    
    # Test with existing directory (public-taluko)
    if os.path.exists('public-taluko'):
        images = discovery.discover_images('public-taluko')
        print(f"Found {len(images)} images in public-taluko/")
        if images:
            print(f"First image: {images[0]}")
    
    # Test with existing directory (public-gaam)
    if os.path.exists('public-gaam'):
        images = discovery.discover_images('public-gaam')
        print(f"Found {len(images)} images in public-gaam/")
        if images:
            print(f"First image: {images[0]}")
    
    # Test with non-existent directory
    images = discovery.discover_images('non-existent-directory')
    assert len(images) == 0, "Should return empty list for non-existent directory"
    print("✓ Non-existent directory handled correctly")
    
    # Test with P064 directory
    if os.path.exists('P064'):
        images = discovery.discover_images('P064')
        print(f"Found {len(images)} images in P064/")
        if images:
            print(f"First few images: {images[:3]}")


def test_error_handling():
    """Test error handling with ErrorLogger."""
    error_logger = ErrorLogger()
    discovery = ImageDiscovery(error_logger)
    
    print("\nTesting error handling:")
    
    # Test with non-existent directory
    images = discovery.discover_images('non-existent-directory-test')
    assert len(images) == 0, "Should return empty list for non-existent directory"
    assert error_logger.failure_count == 1, "Should log one error"
    print("✓ Non-existent directory error logged")
    
    # Test with file instead of directory
    if os.path.exists('README.md'):
        images = discovery.discover_images('README.md')
        assert len(images) == 0, "Should return empty list for file path"
        assert error_logger.failure_count == 2, "Should log second error"
        print("✓ File path (not directory) error logged")
    
    # Display error summary
    summary = error_logger.get_summary()
    print(f"\nError Summary:")
    print(f"  Total errors: {summary['failed']}")
    print(f"  Errors logged: {len(summary['errors'])}")
    for error in summary['errors']:
        print(f"    - [{error['error_type']}] {error['message']}")


def test_get_image_name():
    """Test filename extraction."""
    discovery = ImageDiscovery()
    
    # Test various path formats
    test_cases = [
        ('P064/P0640001.pdf', 'P0640001'),
        ('/full/path/to/P0640001.png', 'P0640001'),
        ('image.jpg', 'image'),
        ('path/to/file.jpeg', 'file'),
    ]
    
    for file_path, expected_name in test_cases:
        result = discovery.get_image_name(file_path)
        assert result == expected_name, f"Expected {expected_name}, got {result}"
        print(f"✓ {file_path} -> {result}")


if __name__ == "__main__":
    print("Testing ImageDiscovery class")
    print("=" * 50)
    
    print("\n1. Testing discover_images():")
    test_discover_images()
    
    print("\n2. Testing get_image_name():")
    test_get_image_name()
    
    print("\n3. Testing error handling:")
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("All tests passed!")
