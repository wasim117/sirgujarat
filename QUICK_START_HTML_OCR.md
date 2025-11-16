# Quick Start - OCR HTML Test

## One-Line Start

```bash
python run_ocr_html_test.py
```

That's it! The script will:
1. ✓ Run OCR tests on `public/address-images/p064/P0640400.jpg`
2. ✓ Generate `ocr_test_results.html` with proper UTF-8 encoding
3. ✓ Open the report in your browser automatically

## What You'll See

A beautiful HTML report showing:

| Test | Function | Result |
|------|----------|--------|
| Text Extraction | `extract_text_from_image()` | ✓ PASS |
| Confidence Score | `get_confidence_score()` | ✓ PASS |
| Gujarati Validation | `validate_gujarati_text()` | ✓ PASS |

Plus the actual **Gujarati text extracted from the image** displayed with proper encoding.

## Manual Steps

If you prefer to run manually:

```bash
# Step 1: Run the test
python test_ocr_integration.py

# Step 2: Open the HTML file
# Windows: start ocr_test_results.html
# Mac: open ocr_test_results.html
# Linux: xdg-open ocr_test_results.html
```

## Key Features

✓ **UTF-8 Encoding** - Gujarati text displays perfectly
✓ **Responsive Design** - Works on all devices
✓ **Beautiful UI** - Modern purple gradient theme
✓ **Test Results** - Clear pass/fail indicators
✓ **Extracted Text** - See the actual OCR output
✓ **Confidence Metrics** - OCR accuracy scores

## Image Used

```
public/address-images/p064/P0640400.jpg
```

## Output File

```
ocr_test_results.html
```

Open this file in any web browser to view the results.

## Requirements

- Python 3.7+
- pytesseract
- Pillow
- Tesseract OCR installed
- Gujarati language data for Tesseract

## Troubleshooting

**Q: Gujarati text shows as boxes?**
A: Install Noto Sans Gujarati font or try Chrome browser

**Q: HTML file not generated?**
A: Check console output for errors, verify image path exists

**Q: Tests show SKIP?**
A: Verify Tesseract is installed and Gujarati data is available

## Next Steps

1. Run: `python run_ocr_html_test.py`
2. View the HTML report
3. Check extracted Gujarati text
4. Review confidence scores
5. Verify all tests pass

---

**Time to run**: ~5-10 seconds
**Output size**: ~50-100 KB HTML file
**Browser support**: All modern browsers
