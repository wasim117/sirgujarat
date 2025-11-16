#!/usr/bin/env python3
"""
Test script for Tesseract OCR integration functions.

Tests the following functions:
- extract_text_from_image()
- get_confidence_score()
- validate_gujarati_text()

Generates HTML output with extracted text for browser viewing.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gujarati_text_extractor import (
    load_image,
    preprocess_image,
    extract_text_from_image,
    get_confidence_score,
    validate_gujarati_text
)


def test_extract_text_from_image():
    """Test extract_text_from_image function."""
    print("\n" + "="*70)
    print("TEST 1: extract_text_from_image()")
    print("="*70)
    
    # Use first available image
    image_path = "public/address-images/p064/P0640400.jpg"
    
    if not os.path.exists(image_path):
        print(f"SKIP: Image not found at {image_path}")
        return False
    
    try:
        # Load and preprocess image
        image = load_image(image_path)
        preprocessed = preprocess_image(image)
        
        # Extract text
        text = extract_text_from_image(preprocessed, language='guj')
        
        print(f"✓ Successfully extracted text from {os.path.basename(image_path)}")
        print(f"  Text length: {len(text)} characters")
        print(f"  First 100 chars: {text[:100]}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_get_confidence_score():
    """Test get_confidence_score function."""
    print("\n" + "="*70)
    print("TEST 2: get_confidence_score()")
    print("="*70)
    
    image_path = "public/images/p064/P0640001.jpg"
    
    if not os.path.exists(image_path):
        print(f"SKIP: Image not found at {image_path}")
        return False
    
    try:
        # Load and preprocess image
        image = load_image(image_path)
        preprocessed = preprocess_image(image)
        
        # Get confidence score
        confidence = get_confidence_score(preprocessed, language='guj')
        
        print(f"✓ Successfully extracted confidence score")
        print(f"  Confidence: {confidence:.2f}%")
        
        # Verify confidence is in valid range
        if 0 <= confidence <= 100:
            print(f"  ✓ Confidence is in valid range [0-100]")
            return True
        else:
            print(f"  ✗ Confidence is out of valid range: {confidence}")
            return False
            
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_validate_gujarati_text():
    """Test validate_gujarati_text function."""
    print("\n" + "="*70)
    print("TEST 3: validate_gujarati_text()")
    print("="*70)
    
    # Test with Gujarati text
    gujarati_text = "આ એક ગુજરાતી ટેક્સ્ટ છે"
    
    try:
        result = validate_gujarati_text(gujarati_text)
        print(f"✓ Gujarati text validation: {result}")
        
        if result:
            print(f"  ✓ Correctly identified Gujarati text")
        else:
            print(f"  ✗ Failed to identify Gujarati text")
            return False
        
        # Test with non-Gujarati text
        english_text = "This is English text"
        result = validate_gujarati_text(english_text)
        print(f"✓ English text validation: {result}")
        
        if not result:
            print(f"  ✓ Correctly rejected non-Gujarati text")
            return True
        else:
            print(f"  ✗ Incorrectly identified English as Gujarati")
            return False
            
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_error_handling():
    """Test error handling for missing Tesseract or language data."""
    print("\n" + "="*70)
    print("TEST 4: Error Handling")
    print("="*70)
    
    image_path = "public/images/p064/P0640001.jpg"
    
    if not os.path.exists(image_path):
        print(f"SKIP: Image not found at {image_path}")
        return False
    
    try:
        image = load_image(image_path)
        preprocessed = preprocess_image(image)
        
        # Try to extract with invalid language code
        try:
            text = extract_text_from_image(preprocessed, language='invalid_lang')
            print(f"✗ Should have raised error for invalid language")
            return False
        except Exception as e:
            error_msg = str(e)
            if 'language' in error_msg.lower() or 'data' in error_msg.lower():
                print(f"✓ Correctly raised error for invalid language")
                print(f"  Error message: {error_msg[:100]}...")
                return True
            else:
                print(f"✗ Error message doesn't mention language/data issue")
                print(f"  Error: {error_msg}")
                return False
                
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def generate_html_report(test_results):
    """
    Generate HTML report with extracted text and test results.
    
    Args:
        test_results: Dictionary with test data including extracted text and confidence scores
    """
    html_content = """<!DOCTYPE html>
<html lang="gu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gujarati Text Extraction - OCR Test Results</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .test-section {
            margin-bottom: 40px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            background: #f9f9f9;
        }
        
        .test-section h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.5em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .test-result {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin-right: 15px;
            min-width: 80px;
            text-align: center;
        }
        
        .status-pass {
            background: #4caf50;
            color: white;
        }
        
        .status-fail {
            background: #f44336;
            color: white;
        }
        
        .extracted-text {
            background: white;
            border: 2px solid #667eea;
            border-radius: 5px;
            padding: 20px;
            margin-top: 15px;
            font-size: 1.2em;
            line-height: 1.8;
            color: #333;
            word-wrap: break-word;
            font-family: 'Noto Sans Gujarati', 'Segoe UI', sans-serif;
        }
        
        .metadata {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .metadata-item {
            background: white;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }
        
        .metadata-label {
            font-weight: bold;
            color: #667eea;
            font-size: 0.9em;
            text-transform: uppercase;
        }
        
        .metadata-value {
            font-size: 1.2em;
            color: #333;
            margin-top: 5px;
        }
        
        .summary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            margin-top: 40px;
        }
        
        .summary h3 {
            font-size: 1.8em;
            margin-bottom: 15px;
        }
        
        .summary-stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
        }
        
        .stat-label {
            font-size: 1em;
            opacity: 0.9;
            margin-top: 5px;
        }
        
        .footer {
            background: #f0f0f0;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        
        .error-message {
            background: #ffebee;
            border-left: 4px solid #f44336;
            padding: 15px;
            border-radius: 5px;
            color: #c62828;
            margin-top: 10px;
        }
        
        .success-message {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 15px;
            border-radius: 5px;
            color: #2e7d32;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔤 Gujarati Text Extraction</h1>
            <p>Tesseract OCR Integration Test Results</p>
        </div>
        
        <div class="content">
"""
    
    # Add test results
    if 'extract_text' in test_results:
        result = test_results['extract_text']
        status_class = 'status-pass' if result['success'] else 'status-fail'
        status_text = 'PASS' if result['success'] else 'FAIL'
        
        html_content += f"""
            <div class="test-section">
                <h2>📝 Text Extraction Test</h2>
                <div class="test-result">
                    <span class="status-badge {status_class}">{status_text}</span>
                    <span>extract_text_from_image()</span>
                </div>
"""
        
        if result['success']:
            # Escape HTML special characters in text
            escaped_text = (result['text']
                          .replace('&', '&amp;')
                          .replace('<', '&lt;')
                          .replace('>', '&gt;')
                          .replace('"', '&quot;')
                          .replace("'", '&#39;'))
            display_text = escaped_text[:500] + ('...' if len(escaped_text) > 500 else '')
            
            html_content += f"""
                <div class="success-message">
                    ✓ Successfully extracted text from {result['filename']}
                </div>
                <div class="metadata">
                    <div class="metadata-item">
                        <div class="metadata-label">Text Length</div>
                        <div class="metadata-value">{result['text_length']} characters</div>
                    </div>
                    <div class="metadata-item">
                        <div class="metadata-label">Image File</div>
                        <div class="metadata-value">{result['filename']}</div>
                    </div>
                </div>
                <div class="extracted-text">
                    {display_text}
                </div>
"""
        else:
            html_content += f"""
                <div class="error-message">
                    ✗ Error: {result['error']}
                </div>
"""
        
        html_content += """
            </div>
"""
    
    # Add confidence score results
    if 'confidence' in test_results:
        result = test_results['confidence']
        status_class = 'status-pass' if result['success'] else 'status-fail'
        status_text = 'PASS' if result['success'] else 'FAIL'
        
        html_content += f"""
            <div class="test-section">
                <h2>📊 Confidence Score Test</h2>
                <div class="test-result">
                    <span class="status-badge {status_class}">{status_text}</span>
                    <span>get_confidence_score()</span>
                </div>
"""
        
        if result['success']:
            html_content += f"""
                <div class="success-message">
                    ✓ Successfully extracted confidence score
                </div>
                <div class="metadata">
                    <div class="metadata-item">
                        <div class="metadata-label">Confidence Score</div>
                        <div class="metadata-value">{result['confidence']:.2f}%</div>
                    </div>
                    <div class="metadata-item">
                        <div class="metadata-label">Score Range</div>
                        <div class="metadata-value">0-100 ✓</div>
                    </div>
                </div>
"""
        else:
            html_content += f"""
                <div class="error-message">
                    ✗ Error: {result['error']}
                </div>
"""
        
        html_content += """
            </div>
"""
    
    # Add validation results
    if 'validation' in test_results:
        result = test_results['validation']
        status_class = 'status-pass' if result['success'] else 'status-fail'
        status_text = 'PASS' if result['success'] else 'FAIL'
        
        html_content += f"""
            <div class="test-section">
                <h2>✅ Gujarati Text Validation Test</h2>
                <div class="test-result">
                    <span class="status-badge {status_class}">{status_text}</span>
                    <span>validate_gujarati_text()</span>
                </div>
"""
        
        if result['success']:
            html_content += f"""
                <div class="success-message">
                    ✓ Gujarati text validation working correctly
                </div>
                <div class="metadata">
                    <div class="metadata-item">
                        <div class="metadata-label">Gujarati Text Detected</div>
                        <div class="metadata-value">{result['gujarati_detected']}</div>
                    </div>
                    <div class="metadata-item">
                        <div class="metadata-label">Non-Gujarati Rejected</div>
                        <div class="metadata-value">{result['english_rejected']}</div>
                    </div>
                </div>
"""
        else:
            html_content += f"""
                <div class="error-message">
                    ✗ Error: {result['error']}
                </div>
"""
        
        html_content += """
            </div>
"""
    
    # Add summary
    if 'summary' in test_results:
        summary = test_results['summary']
        html_content += f"""
            <div class="summary">
                <h3>Test Summary</h3>
                <div class="summary-stats">
                    <div class="stat">
                        <div class="stat-number">{summary['passed']}</div>
                        <div class="stat-label">Tests Passed</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{summary['total']}</div>
                        <div class="stat-label">Total Tests</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{summary['success_rate']:.1f}%</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                </div>
            </div>
"""
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>Generated on """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p>Gujarati Text Extraction - Tesseract OCR Integration Test</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content


def save_html_report(html_content, output_file='ocr_test_results.html'):
    """
    Save HTML report to file with UTF-8 encoding.
    
    Args:
        html_content: HTML content string
        output_file: Output file path
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"\n✓ HTML report saved to: {output_file}")
        return True
    except Exception as e:
        print(f"\n✗ Failed to save HTML report: {str(e)}")
        return False


def main():
    """Run all tests and generate HTML report."""
    print("\n" + "="*70)
    print("TESSERACT OCR INTEGRATION TESTS")
    print("="*70)
    
    test_results = {}
    
    # Use the specific image path provided
    image_path = "public/address-images/p064/P0640400.jpg"
    
    # Test 1: Extract text
    print("\nRunning: extract_text_from_image()...")
    if os.path.exists(image_path):
        try:
            image = load_image(image_path)
            preprocessed = preprocess_image(image)
            text = extract_text_from_image(preprocessed, language='guj')
            test_results['extract_text'] = {
                'success': True,
                'filename': os.path.basename(image_path),
                'text': text,
                'text_length': len(text)
            }
            print(f"  ✓ PASS - Extracted {len(text)} characters")
        except Exception as e:
            test_results['extract_text'] = {
                'success': False,
                'error': str(e)
            }
            print(f"  ✗ FAIL - {str(e)}")
    else:
        test_results['extract_text'] = {
            'success': False,
            'error': f"Image not found: {image_path}"
        }
        print(f"  ✗ SKIP - Image not found")
    
    # Test 2: Confidence score
    print("Running: get_confidence_score()...")
    if os.path.exists(image_path):
        try:
            image = load_image(image_path)
            preprocessed = preprocess_image(image)
            confidence = get_confidence_score(preprocessed, language='guj')
            test_results['confidence'] = {
                'success': True,
                'confidence': confidence
            }
            print(f"  ✓ PASS - Confidence: {confidence:.2f}%")
        except Exception as e:
            test_results['confidence'] = {
                'success': False,
                'error': str(e)
            }
            print(f"  ✗ FAIL - {str(e)}")
    else:
        test_results['confidence'] = {
            'success': False,
            'error': f"Image not found: {image_path}"
        }
        print(f"  ✗ SKIP - Image not found")
    
    # Test 3: Gujarati validation
    print("Running: validate_gujarati_text()...")
    try:
        gujarati_text = "આ એક ગુજરાતી ટેક્સ્ટ છે"
        gujarati_result = validate_gujarati_text(gujarati_text)
        english_text = "This is English text"
        english_result = validate_gujarati_text(english_text)
        
        if gujarati_result and not english_result:
            test_results['validation'] = {
                'success': True,
                'gujarati_detected': 'Yes ✓',
                'english_rejected': 'Yes ✓'
            }
            print(f"  ✓ PASS - Gujarati detected, English rejected")
        else:
            test_results['validation'] = {
                'success': False,
                'error': 'Validation logic failed'
            }
            print(f"  ✗ FAIL - Validation logic failed")
    except Exception as e:
        test_results['validation'] = {
            'success': False,
            'error': str(e)
        }
        print(f"  ✗ FAIL - {str(e)}")
    
    # Calculate summary
    passed = sum(1 for key in ['extract_text', 'confidence', 'validation'] 
                 if key in test_results and test_results[key]['success'])
    total = len([key for key in ['extract_text', 'confidence', 'validation'] 
                 if key in test_results])
    
    test_results['summary'] = {
        'passed': passed,
        'total': total,
        'success_rate': (passed / total * 100) if total > 0 else 0
    }
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {test_results['summary']['success_rate']:.1f}%")
    print("="*70)
    
    # Generate and save HTML report
    print("\nGenerating HTML report...")
    html_content = generate_html_report(test_results)
    save_html_report(html_content)
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
