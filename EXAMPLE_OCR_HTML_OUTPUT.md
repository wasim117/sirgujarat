# Example OCR HTML Output

## What the Generated HTML Report Looks Like

When you run `python run_ocr_html_test.py`, you'll get an HTML file that looks like this:

### Visual Layout

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    🔤 Gujarati Text Extraction                            ║
║              Tesseract OCR Integration Test Results                        ║
║                                                                            ║
║                    [Purple Gradient Background]                           ║
╚════════════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────────────────┐
│ 📝 Text Extraction Test                                                    │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [✓ PASS] extract_text_from_image()                                       │
│                                                                            │
│  ✓ Successfully extracted text from P0640400.jpg                          │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │ Text Length: 1234 characters                                         │ │
│  │ Image File: P0640400.jpg                                             │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │ આ એક ગુજરાતી ટેક્સ્ટ છે                                              │ │
│  │ આ ગુજરાતી ભાષાનો નમૂનો છે                                            │ │
│  │ આ ટેક્સ્ટ OCR દ્વારા નિષ્કર્ષણ કરવામાં આવ્યો છે                      │ │
│  │ ...                                                                  │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│ 📊 Confidence Score Test                                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [✓ PASS] get_confidence_score()                                          │
│                                                                            │
│  ✓ Successfully extracted confidence score                                │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │ Confidence Score: 85.50%                                             │ │
│  │ Score Range: 0-100 ✓                                                 │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│ ✅ Gujarati Text Validation Test                                           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [✓ PASS] validate_gujarati_text()                                        │
│                                                                            │
│  ✓ Gujarati text validation working correctly                             │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │ Gujarati Text Detected: Yes ✓                                        │ │
│  │ Non-Gujarati Rejected: Yes ✓                                         │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                          Test Summary                                      ║
║                                                                            ║
║                    3 Tests Passed                                          ║
║                    3 Total Tests                                           ║
║                    100.0% Success Rate                                     ║
║                                                                            ║
║                    [Purple Gradient Background]                           ║
╚════════════════════════════════════════════════════════════════════════════╝

Generated on 2024-01-15 14:30:45
Gujarati Text Extraction - Tesseract OCR Integration Test
```

## HTML Features

### 1. Proper UTF-8 Encoding
```html
<meta charset="UTF-8">
```
Ensures Gujarati characters display correctly in all browsers.

### 2. Responsive Design
- Desktop: Full-width with multiple columns
- Tablet: Adjusted spacing
- Mobile: Single column layout

### 3. Color Scheme
- **Primary Gradient**: #667eea → #764ba2 (Purple)
- **Success**: #4caf50 (Green)
- **Error**: #f44336 (Red)
- **Background**: #f9f9f9 (Light Gray)

### 4. Typography
- **Headers**: Bold, large, easy to read
- **Body**: Clean sans-serif (Segoe UI, Tahoma, Geneva)
- **Gujarati**: Noto Sans Gujarati font

### 5. Status Badges
```
[✓ PASS]  - Green badge for successful tests
[✗ FAIL]  - Red badge for failed tests
```

## Sample Gujarati Text Output

The HTML will display actual extracted Gujarati text like:

```
આ એક ગુજરાતી ટેક્સ્ટ છે
આ ગુજરાતી ભાષાનો નમૂનો છે
આ ટેક્સ્ટ OCR દ્વારા નિષ્કર્ષણ કરવામાં આવ્યો છે
આ પરીક્ષણ સફળ રહ્યું છે
```

## Metadata Display

Each test section shows:

### Text Extraction
- ✓ Image filename
- ✓ Text length in characters
- ✓ First 500 characters of extracted text

### Confidence Score
- ✓ Confidence percentage (0-100)
- ✓ Valid range verification

### Gujarati Validation
- ✓ Gujarati text detection result
- ✓ Non-Gujarati text rejection result

## File Information

**File Name**: `ocr_test_results.html`
**Encoding**: UTF-8
**Size**: ~50-100 KB
**Format**: HTML5
**Compatibility**: All modern browsers

## Browser Rendering

The HTML uses:
- ✓ CSS Grid for responsive layout
- ✓ Flexbox for alignment
- ✓ CSS Gradients for styling
- ✓ CSS Media Queries for responsiveness
- ✓ HTML5 semantic elements

## Accessibility Features

- ✓ Semantic HTML structure
- ✓ Proper heading hierarchy
- ✓ Color contrast compliance
- ✓ Clear visual indicators
- ✓ Readable font sizes

## Performance

- **Load Time**: Instant (static HTML)
- **File Size**: ~50-100 KB
- **Rendering**: <1 second
- **Browser Support**: 100% of modern browsers

## Customization

To modify the HTML output, edit the `generate_html_report()` function in `test_ocr_integration.py`:

```python
def generate_html_report(test_results):
    """Generate HTML report with extracted text and test results."""
    html_content = """<!DOCTYPE html>
    ...
    """
    return html_content
```

You can customize:
- Colors and gradients
- Fonts and typography
- Layout and spacing
- Icons and badges
- Content and sections

## Example CSS Customization

```css
/* Change primary color */
.header {
    background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
}

/* Change font */
body {
    font-family: 'Your Font', sans-serif;
}

/* Change badge colors */
.status-pass {
    background: #YOUR_SUCCESS_COLOR;
}
```

## Next Steps

1. Run: `python run_ocr_html_test.py`
2. Open the generated `ocr_test_results.html` in your browser
3. View the extracted Gujarati text
4. Check the confidence scores
5. Verify all tests pass

---

**Note**: The actual HTML output will contain real extracted Gujarati text from the image, not the sample text shown here.
