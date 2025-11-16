# Design Document

## Overview

The PDF Gallery Viewer is a static web application that displays extracted address images in a responsive grid layout with search functionality and PDF linking. Built with vanilla HTML, CSS, and JavaScript, it requires no backend server and deploys directly to Vercel as a static site.

## Architecture

### High-Level Architecture

```
[Vercel Static Hosting]
        ↓
[index.html] → [styles.css] → [script.js]
        ↓              ↓              ↓
   [Structure]   [Responsive]   [Interactivity]
                      ↓
        [/public/address-images/p064/] (Images)
        [/P064/] (PDF Files)
```

### Technology Stack

- **HTML5**: Semantic markup and structure
- **CSS3**: Responsive design with Flexbox/Grid, animations
- **JavaScript (Vanilla)**: DOM manipulation, search filtering, lazy loading
- **Vercel**: Static site hosting and deployment
- **No Backend**: Pure client-side application

## Components and Interfaces

### 1. HTML Structure (`index.html`)

**Purpose**: Provides semantic markup and page structure

**Key Sections**:

```html
<header>
  - Logo/Title
  - Collection description
  - Statistics (total documents, last updated)
</header>

<nav>
  - Search input field
  - Filter controls
  - Sort options
</nav>

<main>
  - Gallery grid container
  - Individual image cards with:
    - Image thumbnail
    - Filename/document number
    - File size and dimensions
    - Hover overlay with PDF link
</main>

<footer>
  - Copyright/attribution
  - Deployment info
  - Links to source
</footer>
```

**Key Features**:
- Semantic HTML5 elements (header, nav, main, footer, article)
- Data attributes for image metadata (`data-filename`, `data-size`, `data-dimensions`)
- Accessible markup with ARIA labels
- Meta tags for SEO and responsive design

### 2. CSS Styling (`styles.css`)

**Purpose**: Responsive design and visual presentation

**Key Components**:

```css
/* Responsive Grid */
.gallery-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
}

/* Mobile: 2 columns */
@media (max-width: 768px) {
  .gallery-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Tablet: 3 columns */
@media (min-width: 769px) and (max-width: 1024px) {
  .gallery-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Desktop: 4 columns */
@media (min-width: 1025px) {
  .gallery-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Image Card */
.image-card {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.image-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}

/* Hover Overlay */
.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-card:hover .image-overlay {
  opacity: 1;
}

/* Search Input */
.search-container {
  margin: 2rem 0;
  display: flex;
  gap: 1rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.search-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0,123,255,0.25);
}

/* No Results Message */
.no-results {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.1rem;
}

/* Loading State */
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

**Responsive Breakpoints**:
- Mobile: < 768px (2 columns)
- Tablet: 768px - 1024px (3 columns)
- Desktop: > 1024px (4 columns)

### 3. JavaScript Functionality (`script.js`)

**Purpose**: Dynamic image loading, search filtering, and interactivity

**Key Functions**:

```javascript
// Initialize gallery on page load
async function initializeGallery() {
  // Fetch image list from /public/address-images/p064/
  // Generate image cards
  // Set up event listeners
  // Implement lazy loading
}

// Fetch list of images from directory
async function fetchImageList() {
  // Read directory contents
  // Return array of image filenames
  // Handle errors gracefully
}

// Generate image cards dynamically
function generateImageCards(images) {
  // Create card elements for each image
  // Add data attributes with metadata
  // Append to gallery grid
  // Set up click handlers
}

// Search/filter functionality
function filterImages(searchTerm) {
  // Filter images by filename or number
  // Update display in real-time
  // Show/hide cards based on match
  // Update result count
}

// Lazy loading implementation
function setupLazyLoading() {
  // Use Intersection Observer API
  // Load images only when visible
  // Improve initial page load time
}

// PDF link handler
function handleImageClick(filename) {
  // Map image filename to PDF file
  // Open PDF in new tab
  // Handle missing PDFs gracefully
}

// Get image metadata
function getImageMetadata(filename) {
  // Extract file size
  // Get image dimensions
  // Return metadata object
}

// Update statistics
function updateStatistics() {
  // Count total images
  // Display in header
  // Show last updated date
}
```

**Key Features**:
- Lazy loading using Intersection Observer API
- Real-time search filtering
- Dynamic image card generation
- Error handling for missing images/PDFs
- Browser caching for performance
- Responsive event handling

### 4. Data Flow

```
Page Load
  ↓
Fetch image list from /public/address-images/p064/
  ↓
Generate image cards with metadata
  ↓
Set up lazy loading observers
  ↓
Render initial visible images
  ↓
User Interaction (Search/Click)
  ↓
Filter or navigate to PDF
```

### 5. File Structure

```
project-root/
├── index.html                    # Main gallery page
├── styles.css                    # Responsive styling
├── script.js                     # Gallery functionality
├── vercel.json                   # Vercel configuration
├── public/
│   ├── address-images/
│   │   └── p064/                 # Extracted address images
│   │       ├── P0640001.jpg
│   │       ├── P0640002.jpg
│   │       └── ... (up to P0640601.jpg)
│   └── favicon.ico               # Site icon
├── P064/                         # Original PDF files
│   ├── P0640001.pdf
│   ├── P0640002.pdf
│   └── ... (up to P0640601.pdf)
└── README.md                     # Documentation
```

## Data Models

### Image Card Object

```javascript
{
  filename: "P0640001.jpg",
  documentNumber: "P064-0001",
  pdfPath: "P064/P0640001.pdf",
  imagePath: "public/address-images/p064/P0640001.jpg",
  fileSize: "245 KB",
  dimensions: "1058x393",
  lastModified: "2024-01-15"
}
```

### Gallery Configuration

```javascript
{
  imageDirectory: "public/address-images/p064/",
  pdfDirectory: "P064/",
  imagesPerPage: 20,
  lazyLoadThreshold: 200,
  searchDebounceDelay: 300,
  gridColumns: {
    mobile: 2,
    tablet: 3,
    desktop: 4
  }
}
```

## Error Handling

### Error Scenarios

1. **Missing Image Directory**
   - Display: "Image gallery not available"
   - Action: Show placeholder or error message

2. **Missing PDF File**
   - Display: Disable PDF link on hover
   - Action: Show tooltip "PDF not available"

3. **Image Load Failure**
   - Display: Placeholder with broken image icon
   - Action: Log error, continue loading other images

4. **Network Issues**
   - Display: Retry button or offline message
   - Action: Implement retry logic with exponential backoff

### Error Handling Strategy

```javascript
try {
  // Fetch and render images
} catch (error) {
  console.error('Gallery initialization failed:', error);
  displayErrorMessage('Unable to load gallery');
}

// Image load error handler
image.onerror = function() {
  this.src = 'placeholder-image.png';
  console.warn(`Failed to load image: ${filename}`);
};
```

## Testing Strategy

### Unit Testing

1. **Search Filtering**
   - Test partial matching
   - Test case-insensitive search
   - Test empty search results

2. **Image Metadata Extraction**
   - Verify filename parsing
   - Verify PDF path mapping
   - Verify metadata display

3. **Responsive Layout**
   - Test grid columns at different breakpoints
   - Verify spacing and alignment

### Integration Testing

1. **Gallery Initialization**
   - Verify all images load
   - Verify metadata displays correctly
   - Verify search functionality works

2. **PDF Linking**
   - Verify correct PDF opens for each image
   - Verify new tab opens
   - Verify error handling for missing PDFs

3. **Performance**
   - Verify lazy loading works
   - Measure initial load time
   - Verify smooth scrolling

### Manual Testing

1. **Visual Inspection**
   - Check responsive layout on different devices
   - Verify hover effects work
   - Check image quality

2. **User Interaction**
   - Test search functionality
   - Test PDF links
   - Test on different browsers

## Deployment Configuration

### Vercel Configuration (`vercel.json`)

```json
{
  "buildCommand": "echo 'Static site - no build needed'",
  "outputDirectory": ".",
  "public": true,
  "env": {
    "NODE_ENV": "production"
  },
  "headers": [
    {
      "source": "/public/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### Performance Optimization

- **Image Optimization**: Serve images at appropriate sizes
- **Caching**: Set long cache headers for static assets
- **Lazy Loading**: Load images only when visible
- **Minification**: Minify CSS and JavaScript
- **CDN**: Vercel's global CDN for fast delivery

## Implementation Notes

### Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Intersection Observer API support required for lazy loading
- Fallback for older browsers without Intersection Observer

### Accessibility

- Semantic HTML structure
- ARIA labels for images
- Keyboard navigation support
- High contrast colors for readability
- Alt text for all images

### SEO Considerations

- Meta tags for title and description
- Open Graph tags for social sharing
- Structured data (Schema.org) for images
- Sitemap for search engines

