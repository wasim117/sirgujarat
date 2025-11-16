# Usage Examples

## Quick Start

### Run Default (Extract + Crop)
```bash
python extract_pdf_thumbnails.py
```

## Independent Workflows

### 1. Extract PDFs Only (No Cropping)

Create `run_extract.py`:
```python
from extract_pdf_thumbnails import main_extract_only

if __name__ == "__main__":
    main_extract_only()
```

Run:
```bash
python run_extract.py
```

### 2. Crop Images Only (No PDF Extraction)

Create `run_crop.py`:
```python
from extract_pdf_thumbnails import main_crop_only

if __name__ == "__main__":
    main_crop_only()
```

Run:
```bash
python run_crop.py
```

### 3. Extract and Crop Together

Create `run_both.py`:
```python
from extract_pdf_thumbnails import main_extract_and_crop

if __name__ == "__main__":
    main_extract_and_crop()
```

Run:
```bash
python run_both.py
```

## Custom Configurations

### Custom PDF Extraction

```python
from extract_pdf_thumbnails import process_pdf_directory

# Extract without cropping
result = process_pdf_directory(
    source_dir='my_pdfs',
    output_dir='my_output',
    address_output_dir=None,  # No cropping
    dpi=200  # Higher quality
)

print(f"Processed {result['success']} files")
```

### Custom Image Cropping

```python
from extract_pdf_thumbnails import process_image_cropping

# Crop with custom coordinates
result = process_image_cropping(
    source_dir='public/images/p064',
    output_dir='public/custom-crop',
    left=100,
    top=200,
    width=800,
    height=400
)

print(f"Cropped {result['success']} images")
```

### Extract and Crop with Custom Settings

```python
from extract_pdf_thumbnails import process_pdf_directory

# Extract and crop in one go
result = process_pdf_directory(
    source_dir='P064',
    output_dir='public/images/p064',
    address_output_dir='public/address-images/p064',  # Enable cropping
    dpi=150
)

print(f"Extracted: {result['success']}")
print(f"Cropped: {result['crop_success']}")
```

## Workflow Recommendations

### Scenario 1: First Time Setup
1. Run extraction only to verify PDFs process correctly
2. Check output images
3. Run cropping separately to test crop coordinates
4. Once satisfied, use combined workflow

### Scenario 2: Re-crop Existing Images
- Use `main_crop_only()` to re-process images with different coordinates
- No need to re-extract PDFs

### Scenario 3: Add New PDFs
- Use `main_extract_and_crop()` to process new PDFs
- Existing images won't be affected

### Scenario 4: Different Crop Regions
- Extract once with `main_extract_only()`
- Crop multiple times with different coordinates using `process_image_cropping()`
