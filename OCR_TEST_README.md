# OCR Integration Test - HTML Output Guide

## Overview

The updated `test_ocr_integration.py` script now generates a beautiful HTML report with extracted Gujarati text that you can view in any web browser.

## Features

✓ **UTF-8 Encoding** - Proper support for Gujarati Unicode characters  
✓ **Responsive Design** - Works on desktop and mobile browsers  
✓ **Visual Test Results** - Color-coded pass/fail indicators  
✓ **Extracted Text Display** - Shows extracted Gujarati text with proper formatting  
✓ **Confidence Metrics** - Displays OCR confidence scores  
✓ **Test Summary** - Overall statistics and success rates  

## Running the Tests

### Option 1: Direct Python Execution
```bash
python test_ocr_integration.py
```

This will:
1. Run all OCR integration tests
2. Generate `ocr_test_results.html` in the current directory
3. Display test results in the console

### Option 2: Using the Runner Script
```bash
python run_ocr_test.py
```

This provides a convenient wrapper with additional guidance.

## Viewing the HTML Report

### Method 1: Direct File Opening
Simply open `ocr_test_results.html` in your web browser:
- Windows: Double-click the file
- Mac: Double-click or right-click → Open With → Browser
- Linux: Right-click → Open With → Browser

### Method 2: Local Web Server (Recommended)
For better compatibility and to avoid CORS issues:

```bash
# Python 3
python -m http.server 8000

# Then visit in your browser:
# http://localhost:8000/ocr_test_results.html
```

### Method 3: Using Python's Built-in Server
```bash
python -m http.server 8000 --directory .
```

## HTML Report Contents

### Header Section
- Title and description
- Test execution timestamp

### Test Results Sections

#### 1. Text Extraction Test
- Status indicator (Pass/Fail)
- Extracted text preview (first 500 characters)
- Text length statistics
- Source image filename

#### 2. Confidence Score Test
- Status indicator
- Confidence percentage (0-100%)
- Validation that score is in valid range

#### 3. Gujarati Text Validation Test
- Status indicator
- Gujarati character detection result
- Non-Gujarati text rejection result

### Summary Section
- Number of tests passed
- Total tests run
- Success rate percentage

### Footer
- Generation timestamp
- Test information

## HTML Features

### Styling
- Modern gradient background
- Color-coded status badges (green for pass, red for fail)
- Responsive grid layout
- Professional typography
- Proper spacing and visual hierarchy

### Gujarati Text Support
- UTF-8 encoding declaration in HTML head
- Noto Sans Gujarati font support
- Proper line-height for Gujarati script
- Word-wrap for long text

### Accessibility
- Semantic HTML structure
- Proper heading hierarchy
- Color contrast compliance
- Responsive design for all screen sizes

## Example Output

The HTML report displays:

```
🔤 Gujarati Text Extraction
Tesseract OCR Integration Test Results

📝 Text Extraction Test
✓ PASS - extract_text_from_image()
  Successfully extracted text from P0640001.jpg
  Text Length: 1,234 characters
  
  [Extracted Gujarati text displayed here...]

📊 Confidence Score Test
✓ PASS - get_confidence_score()
  Confidence Score: 87.45%
  Score Range: 0-100 ✓

✅ Gujarati Text Validation Test
✓ PASS - validate_gujarati_text()
  Gujarati Text Detected: Yes ✓
  Non-Gujarati Rejected: Yes ✓

Test Summary
  3 Tests Passed
  3 Total Tests
  100.0% Success Rate
```

## Troubleshooting

### HTML File Not Generated
- Ensure `test_ocr_integration.py` runs without errors
- Check console output for error messages
- Verify write permissions in the current directory

### Gujarati Text Not Displaying Correctly
- Ensure your browser supports UTF-8 encoding
- Try a different browser (Chrome, Firefox, Safari all support UTF-8)
- Check that the HTML file has UTF-8 encoding (view source)

### Tests Failing
- Ensure Tesseract OCR is installed: `tesseract --version`
- Verify Gujarati language data is installed
- Check that image files exist in `public/images/p064/`
- See GUJARATI_TEXT_EXTRACTION_USAGE.md for setup instructions

## File Encoding

The HTML file is saved with **UTF-8 encoding** to ensure proper display of Gujarati characters:

```html
<meta charset="UTF-8">
```

This is automatically handled by the `save_html_report()` function:

```python
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)
```

## Browser Compatibility

Tested and working on:
- ✓ Chrome/Chromium (latest)
- ✓ Firefox (latest)
- ✓ Safari (latest)
- ✓ Edge (latest)
- ✓ Mobile browsers (iOS Safari, Chrome Mobile)

## Customization

To modify the HTML report styling, edit the `<style>` section in the `generate_html_report()` function in `test_ocr_integration.py`.

Common customizations:
- Change colors: Modify `#667eea` and `#764ba2` hex codes
- Adjust fonts: Edit `font-family` properties
- Modify layout: Change `grid-template-columns` values
- Update spacing: Adjust `padding` and `margin` values

## Next Steps

After viewing the HTML report:

1. **Verify Results** - Check that extracted text is correct
2. **Review Confidence** - Ensure confidence scores are acceptable
3. **Validate Text** - Confirm Gujarati characters are properly detected
4. **Troubleshoot** - If tests fail, check installation and configuration

For more information, see:
- `GUJARATI_TEXT_EXTRACTION_USAGE.md` - Setup and installation guide
- `gujarati_text_extractor.py` - Main extraction module
- `.kiro/specs/gujarati-text-extraction/` - Feature specifications
