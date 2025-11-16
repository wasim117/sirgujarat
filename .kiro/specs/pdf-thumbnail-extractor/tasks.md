# Implementation Plan

- [x] 1. Set up project structure and dependencies





  - Create requirements.txt file with PyMuPDF and Pillow dependencies
  - Create main script file extract_pdf_thumbnails.py
  - _Requirements: 1.1, 1.2_

- [x] 2. Implement directory and path utilities





  - Write function to ensure output directory exists and create nested directories if needed
  - Write function to get list of all PDF files from source directory
  - Implement path validation to verify source directory exists
  - _Requirements: 1.5_

- [x] 3. Implement core PDF extraction function






  - Write extract_first_page() function that opens a PDF file using PyMuPDF
  - Implement page rendering logic with configurable DPI (default 150)
  - Add pixmap to PIL Image conversion with RGB color mode handling
  - Implement JPEG saving with quality setting of 85 and optimization enabled
  - Add white background handling for PDFs with transparency
  - _Requirements: 1.2, 1.3, 1.4, 4.1, 4.2, 4.3_

- [x] 4. Implement error handling for PDF processing





  - Add try-except blocks to catch PyMuPDF file errors (corrupted, empty PDFs)
  - Implement error logging that captures filename and error message
  - Ensure function returns boolean success indicator
  - Add resource cleanup in finally block to close PDF documents
  - _Requirements: 2.1, 2.2, 2.4_

- [x] 5. Implement batch processing function





  - Write process_pdf_directory() function that iterates through all PDFs in source directory
  - Implement progress counter showing current file number and total count
  - Add filename display for each file being processed
  - Track success and failure counts during processing
  - Collect error details in a list for final reporting
  - _Requirements: 1.1, 2.3, 3.1, 3.2_

- [x] 6. Implement progress reporting and summary





  - Add elapsed time tracking using time module
  - Display progress information during processing (file X of Y)
  - Create summary report showing success count, failure count, and total time
  - Display output directory path in summary
  - Print detailed error list if any failures occurred
  - _Requirements: 2.3, 3.1, 3.2, 3.3, 3.4_

- [x] 7. Create main execution block






  - Write main() function or if __name__ == "__main__" block
  - Set configuration values (source_dir='P064', output_dir='public/images/p064', dpi=150)
  - Call process_pdf_directory() with configuration
  - Display final summary results
  - _Requirements: 1.1, 1.4_

- [ ]* 8. Add command-line argument support
  - Implement argparse to accept source directory, output directory, and DPI as optional arguments
  - Add help text for each argument
  - Set default values matching the requirements
  - _Requirements: 1.1, 4.1_

- [ ]* 9. Create test script for validation
  - Write test script that processes a small subset of PDFs (first 5 files)
  - Add assertions to verify output files exist
  - Check that image files are valid JPEG format
  - Verify image dimensions are reasonable
  - _Requirements: 1.2, 1.3, 4.4_

- [x] 10. Add documentation






  - Write README.md with usage instructions
  - Document required dependencies and installation steps
  - Add example commands for running the script
  - Include troubleshooting section for common errors
  - _Requirements: All_

- [x] 11. Implement image cropping function






  - Write crop_image() function that loads an image using PIL
  - Calculate crop box coordinates from left, top, width, and height parameters
  - Validate that crop region is within image boundaries before cropping
  - Use image.crop() method to extract the specified region
  - Save cropped image as JPEG with quality setting of 85
  - Return success status and error message if validation fails
  - _Requirements: 5.1, 5.4, 5.5_

- [x] 12. Integrate cropping into batch processing







  - Update process_pdf_directory() to create address-images output directory
  - After each successful PDF extraction, call crop_image() with coordinates left=133, top=425, width=1058, height=393
  - Save cropped images to public/address-images/p064 directory with same filename
  - Track cropping success and failure counts separately
  - Add cropping errors to the error report
  - _Requirements: 5.1, 5.2, 5.3_

- [ ] 13. Update progress reporting for cropping
  - Display cropping progress alongside extraction progress
  - Include cropped image count in summary report
  - Show address-images output directory path in summary
  - Add cropping errors to detailed error list
  - _Requirements: 5.2, 5.3_
