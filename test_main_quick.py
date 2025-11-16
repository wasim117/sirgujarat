#!/usr/bin/env python3
"""
Quick test of the main script with limited images.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gujarati_ocr_json_extractor import (
    ImageDiscovery,
    OCRProcessor,
    DataAggregator,
    JSONOutputWriter,
    ErrorLogger
)


def main():
    """Quick test with 2 images."""
    print("Quick Main Script Test")
    print("=" * 50)
    
    # Initialize error logger
    error_logger = ErrorLogger()
    
    # Initialize components
    image_discovery = ImageDiscovery(error_logger=error_logger)
    ocr_processor = OCRProcessor(language='guj', error_logger=error_logger)
    data_aggregator = DataAggregator()
    json_writer = JSONOutputWriter(error_logger=error_logger)
    
    # Define input directories and output file
    taluko_dir = 'public-taluko'
    gaam_dir = 'public-gaam'
    output_file = 'test_output.json'
    
    print(f"\nDiscovering images in {taluko_dir}/...")
    taluko_images = image_discovery.discover_images(taluko_dir)[:2]
    print(f"Found {len(taluko_images)} taluko images")
    
    print(f"\nDiscovering images in {gaam_dir}/...")
    gaam_images = image_discovery.discover_images(gaam_dir)[:2]
    print(f"Found {len(gaam_images)} gaam images")
    
    # Process taluko images
    print(f"\nProcessing taluko images...")
    for image_path in taluko_images:
        image_name = image_discovery.get_image_name(image_path)
        print(f"  Processing {image_name}...", end=' ')
        
        extracted_text = ocr_processor.extract_text(image_path)
        
        if extracted_text is not None:
            data_aggregator.add_taluko_entry(image_name, extracted_text)
            error_logger.log_success()
            print("[OK]")
        else:
            print("[FAIL]")
    
    # Process gaam images
    print(f"\nProcessing gaam images...")
    for image_path in gaam_images:
        image_name = image_discovery.get_image_name(image_path)
        print(f"  Processing {image_name}...", end=' ')
        
        extracted_text = ocr_processor.extract_text(image_path)
        
        if extracted_text is not None:
            data_aggregator.add_gaam_entry(image_name, extracted_text)
            error_logger.log_success()
            print("[OK]")
        else:
            print("[FAIL]")
    
    # Get aggregated data
    aggregated_data = data_aggregator.get_aggregated_data()
    
    print(f"\n" + "=" * 50)
    print(f"Processing complete!")
    print(f"Total entries aggregated: {len(aggregated_data)}")
    
    # Generate final JSON output file
    print(f"\nGenerating JSON output file: {output_file}...")
    write_success = json_writer.write_json(aggregated_data, output_file)
    
    if write_success:
        print(f"[SUCCESS] JSON file successfully created: {output_file}")
        
        # Verify the file
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"[VERIFIED] JSON file contains {len(data)} entries")
            
            # Show sample entry
            if len(data) > 0:
                sample_key = list(data.keys())[0]
                print(f"\nSample entry ({sample_key}):")
                print(f"  taluko: {data[sample_key]['taluko'][:50] if data[sample_key]['taluko'] else 'None'}...")
                print(f"  gaam: {data[sample_key]['gaam'][:50] if data[sample_key]['gaam'] else 'None'}...")
    else:
        print(f"[ERROR] Failed to create JSON file: {output_file}")
    
    # Display processing summary
    summary = error_logger.get_summary()
    print(f"\n" + "=" * 50)
    print(f"Processing Summary:")
    print(f"  Total images processed: {summary['total_processed']}")
    print(f"  Successful extractions: {summary['successful']}")
    print(f"  Failed extractions: {summary['failed']}")
    print(f"  Data entries created: {len(aggregated_data)}")
    
    if summary['failed'] > 0:
        print(f"\n[WARNING] Errors encountered: {summary['failed']}")
        print("Review the error messages above for details.")
    
    if write_success and len(aggregated_data) > 0:
        print(f"\n[SUCCESS] Extraction complete! Check {output_file} for results.")
    elif len(aggregated_data) == 0:
        print(f"\n[WARNING] No data was extracted. Check input directories and error messages.")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
