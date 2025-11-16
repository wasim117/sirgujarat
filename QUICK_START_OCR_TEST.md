# Quick Start: OCR Integration Test with HTML Output

## 30-Second Setup

### Step 1: Run the Test
```bash
python test_ocr_integration.py
```

### Step 2: Open the HTML Report
- Look for `ocr_test_results.html` in your current directory
- Double-click to open in your default browser
- Or use: `python -m http.server 8000` and visit `http://localhost:8000/ocr_test_results.html`

### Step 3: View Results
The HTML report shows:
- ✓ Extracted Gujarati text from images
- ✓ OCR confidence scores
- ✓ Text validation results
- ✓ Test summary statistics

## What You'll See

### In the Browser
A professional HTML report with:
- **Extracted Text** - Gujarati text extracted from images using Tesseract OCR
- **Confidence Scores** - How confident the OCR engine is (0-100%)
- **Validation Results** - Whether Gujarati characters were properly detected
- **Test Summary** - Overall pass/fail statistics

### In the Console
```
TESSERACT OCR INTEGRATION TESTS
======================================================================
Running: extract_text_from_image()...
  ✓ PASS - Extracted 1234 characters

Running: get_confidence_score()...
  ✓ PASS - Confidence: 87.45%

Running: validate_gujarati_text()...
  ✓ PASS - Gujarati detected, English rejected

======================================================================
TEST SUMMARY
======================================================================
Passed: 3/3
Success Rate: 100.0%
======================================================================

✓ HTML report saved to: ocr_test_results.html
```

## File Encoding

The HTML file uses **UTF-8 encoding** for proper Gujarati character display:
```html
<meta charset="UTF-8">
```

This ensures Gujarati text displays correctly in all modern browsers.

## Troubleshooting

### "Image not found" Error
- Ensure images exist in `public/images/p064/`
- Run from the project root directory

### Gujarati Text Not Displaying
- Try a different browser (Chrome, Firefox, Safari)
- Check that your browser supports UTF-8 encoding
- Verify the HTML file has UTF-8 encoding

### Tests Failing
- Ensure Tesseract OCR is installed: `tesseract --version`
- Verify Gujarati language data: `tesseract --list-langs | grep guj`
- See `GUJARATI_TEXT_EXTRACTION_USAGE.md` for installation help

## Files Generated

After running the test:
- `ocr_test_results.html` - Beautiful HTML report with test results and extracted text

## Next Steps

1. **Review the HTML Report** - Open in browser to see extracted Gujarati text
2. **Check Confidence Scores** - Verify OCR accuracy
3. **Validate Results** - Ensure text extraction is working correctly
4. **Explore the Code** - See `test_ocr_integration.py` for implementation details

## Advanced Usage

### Custom Image Testing
Edit `test_ocr_integration.py` and change:
```python
image_path = "public/images/p064/P0640001.jpg"
```

To any other image path.

### Modify HTML Styling
Edit the `<style>` section in `generate_html_report()` function to customize:
- Colors (change `#667eea` and `#764ba2`)
- Fonts (modify `font-family`)
- Layout (adjust grid and spacing)

### Batch Testing
Create a loop to test multiple images:
```python
for i in range(1, 11):
    image_path = f"public/images/p064/P064000{i:02d}.jpg"
    # Run tests...
```

## Support

For more information:
- See `OCR_TEST_README.md` for detailed documentation
- Check `GUJARATI_TEXT_EXTRACTION_USAGE.md` for setup instructions
- Review `gujarati_text_extractor.py` for implementation details
