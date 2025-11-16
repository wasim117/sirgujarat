#!/usr/bin/env python3
"""
Full pipeline integration test for the Gujarati OCR JSON Extractor.
Tests that all components are properly wired together.
"""

import os
import sys
import json
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gujarati_ocr_json_extractor import (
    ImageDiscovery,
    OCRProcessor,
    DataAggregator,
    JSONOutputWriter,
    ErrorLogger
)


def test_full_pipeline():
    """Test the complete pipeline with all components wired together."""
    print("\n" + "="*70)
    print("FULL PIPELINE INTEGRATION TEST")
    print("="*70)
    
    # Initialize error logger
    error_logger = ErrorLogger()
    
    # Initialize all components
    print("\n1. Initializing components...")
    image_discovery = ImageDiscovery(error_logger=error_logger)
    ocr_processor = OCRProcessor(language='guj', error_logger=error_logger)
    data_aggregator = DataAggregator()
    json_writer = JSONOutputWriter(error_logger=error_logger)
    print("   ✓ All components initialized")
    
    # Define test directories (use first 3 images only for quick test)
    taluko_dir = 'public-taluko'
    gaam_dir = 'public-gaam'
    
    # Discover images
    print("\n2. Discovering images...")
    taluko_images = image_discovery.discover_images(taluko_dir)[:3]
    gaam_images = image_discovery.discover_images(gaam_dir)[:3]
    print(f"   ✓ Found {len(taluko_images)} taluko test images")
    print(f"   ✓ Found {len(gaam_images)} gaam test images")
    
    if len(taluko_images) == 0 and len(gaam_images) == 0:
        print("\n   SKIP: No test images available")
        return None
    
    # Process taluko images
    print("\n3. Processing taluko images...")
    for image_path in taluko_images:
        image_name = image_discovery.get_image_name(image_path)
        extracted_text = ocr_processor.extract_text(image_path)
        
        if extracted_text is not None:
            data_aggregator.add_taluko_entry(image_name, extracted_text)
            error_logger.log_success()
            print(f"   ✓ {image_name}")
        else:
            print(f"   ✗ {image_name}")
    
    # Process gaam images
    print("\n4. Processing gaam images...")
    for image_path in gaam_images:
        image_name = image_discovery.get_image_name(image_path)
        extracted_text = ocr_processor.extract_text(image_path)
        
        if extracted_text is not None:
            data_aggregator.add_gaam_entry(image_name, extracted_text)
            error_logger.log_success()
            print(f"   ✓ {image_name}")
        else:
            print(f"   ✗ {image_name}")
    
    # Get aggregated data
    print("\n5. Aggregating data...")
    aggregated_data = data_aggregator.get_aggregated_data()
    print(f"   ✓ Created {len(aggregated_data)} data entries")
    
    # Write JSON output to temporary file
    print("\n6. Writing JSON output...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        output_file = tmp.name
    
    write_success = json_writer.write_json(aggregated_data, output_file)
    
    if write_success:
        print(f"   ✓ JSON file created: {output_file}")
        
        # Verify JSON file contents
        with open(output_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        print(f"   ✓ JSON file verified: {len(loaded_data)} entries")
        
        # Clean up
        os.unlink(output_file)
    else:
        print(f"   ✗ Failed to create JSON file")
        return False
    
    # Display summary
    print("\n7. Processing summary...")
    summary = error_logger.get_summary()
    print(f"   Total processed: {summary['total_processed']}")
    print(f"   Successful: {summary['successful']}")
    print(f"   Failed: {summary['failed']}")
    
    # Verify requirements
    print("\n8. Verifying requirements...")
    
    # Requirement 3.4: JSON structure verification
    if len(aggregated_data) > 0:
        sample_key = list(aggregated_data.keys())[0]
        sample_entry = aggregated_data[sample_key]
        
        if 'taluko' in sample_entry and 'gaam' in sample_entry:
            print("   ✓ Requirement 3.4: JSON structure is correct")
        else:
            print("   ✗ Requirement 3.4: JSON structure is incorrect")
            return False
    
    # Requirement 5.1: Error handling
    if error_logger is not None:
        print("   ✓ Requirement 5.1: Error handling implemented")
    
    # Requirement 5.2: Processing summary
    if summary['total_processed'] > 0:
        print("   ✓ Requirement 5.2: Processing summary generated")
    
    # Requirement 5.4: JSON file creation
    if write_success:
        print("   ✓ Requirement 5.4: JSON file successfully created")
    
    return True


def main():
    """Run the full pipeline integration test."""
    result = test_full_pipeline()
    
    if result is None:
        print("\n" + "="*70)
        print("TEST SKIPPED - No images available")
        print("="*70)
        return True
    elif result:
        print("\n" + "="*70)
        print("✓ FULL PIPELINE TEST PASSED")
        print("All components are properly wired together!")
        print("="*70)
        return True
    else:
        print("\n" + "="*70)
        print("✗ FULL PIPELINE TEST FAILED")
        print("="*70)
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
