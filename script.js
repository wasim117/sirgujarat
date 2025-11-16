/**
 * PDF Gallery Viewer - Main Application Script
 * Handles image loading, search filtering, lazy loading, and PDF linking
 */

// ============================================
// Configuration
// ============================================

const CONFIG = {
    imageDirectory: 'public/address-images/p064/',
    pdfDirectory: 'P064/',
    lazyLoadThreshold: 200,
    searchDebounceDelay: 300,
};

// ============================================
// State Management
// ============================================

let galleryState = {
    allImages: [],
    filteredImages: [],
    imageMetadata: {},
    searchTerm: '',
    lazyLoadObserver: null,
};

// ============================================
// DOM Elements
// ============================================

const elements = {
    galleryGrid: document.getElementById('gallery-grid'),
    searchInput: document.getElementById('search-input'),
    clearButton: document.getElementById('clear-search'),
    loadingContainer: document.getElementById('loading'),
    noResultsContainer: document.getElementById('no-results'),
    totalDocuments: document.getElementById('total-documents'),
    lastUpdated: document.getElementById('last-updated'),
    resultCount: document.getElementById('result-count'),
};

// ============================================
// Initialization
// ============================================

/**
 * Initialize the gallery on page load
 */
async function initializeGallery() {
    try {
        showLoading(true);
        
        // Fetch image list from directory
        await fetchImageList();
        
        // Generate image cards
        generateImageCards(galleryState.allImages);
        
        // Set up event listeners
        setupEventListeners();
        

        
        // Update statistics
        updateStatistics();
        
        showLoading(false);
    } catch (error) {
        console.error('Gallery initialization failed:', error);
        showLoading(false);
        displayErrorMessage('Unable to load gallery. Please refresh the page.');
    }
}

/**
 * Fetch list of images from the directory
 */
async function fetchImageList() {
    try {
        // Generate list of images from P0640001 to P0640601
        const imageCount = 601;
        const images = [];
        
        for (let i = 1; i <= imageCount; i++) {
            const paddedNumber = String(i).padStart(4, '0');
            const filename = `P064${paddedNumber}.jpg`;
            images.push(filename);
        }
        
        galleryState.allImages = images;
        galleryState.filteredImages = [...images];
        
        console.log(`Loaded ${images.length} images`);
    } catch (error) {
        console.error('Failed to fetch image list:', error);
        throw error;
    }
}

/**
 * Generate image card elements dynamically
 */
function generateImageCards(images) {
    elements.galleryGrid.innerHTML = '';
    
    images.forEach((filename) => {
        const card = createImageCard(filename);
        elements.galleryGrid.appendChild(card);
    });
}

/**
 * Create a single image card element
 */
function createImageCard(filename) {
    const card = document.createElement('article');
    card.className = 'image-card';
    card.setAttribute('data-filename', filename);
    
    const imagePath = `/public/address-images/p064/${filename}`;
    const pdfPath = `${CONFIG.pdfDirectory}${filename.replace('.jpg', '.pdf')}`;
    
    // Extract metadata
    const metadata = extractImageMetadata(filename);
    galleryState.imageMetadata[filename] = metadata;
    
    // Create card HTML
    card.innerHTML = `
        <div class="image-wrapper">
            <img 
                src="${imagePath}" 
                alt="${metadata.documentNumber}"
            >
            <div class="image-overlay">
                <button class="pdf-link-button" data-pdf="${pdfPath}" aria-label="Open PDF for ${metadata.documentNumber}">
                    Open PDF
                </button>
            </div>
        </div>
        <div class="card-metadata">
            <div class="card-filename">${metadata.documentNumber}</div>
            <div class="card-info">
                <div class="card-info-item">
                    <span class="card-info-label">File:</span>
                    <span class="card-info-value">${filename}</span>
                </div>
                <div class="card-info-item">
                    <span class="card-info-label">Size:</span>
                    <span class="card-info-value">--</span>
                </div>
                <div class="card-info-item">
                    <span class="card-info-label">Dimensions:</span>
                    <span class="card-info-value">--</span>
                </div>
            </div>
        </div>
    `;
    
    // Add click handler for PDF link
    const pdfButton = card.querySelector('.pdf-link-button');
    pdfButton.addEventListener('click', (e) => {
        e.stopPropagation();
        handleImageClick(filename, pdfPath);
    });
    
    return card;
}

/**
 * Extract metadata from image filename
 */
function extractImageMetadata(filename) {
    // Extract document number from filename (e.g., P0640001.jpg -> P064-0001)
    const match = filename.match(/P064(\d+)/);
    const number = match ? match[1] : '0001';
    const documentNumber = `P064-${number}`;
    
    return {
        filename: filename,
        documentNumber: documentNumber,
        fileSize: 'Unknown',
        dimensions: 'Unknown',
    };
}

/**
 * Set up event listeners for search and interactions
 */
function setupEventListeners() {
    // Search input with debounce
    let searchTimeout;
    elements.searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            filterImages(e.target.value);
        }, CONFIG.searchDebounceDelay);
    });
    
    // Clear search button
    elements.clearButton.addEventListener('click', () => {
        elements.searchInput.value = '';
        filterImages('');
    });
}

/**
 * Filter images based on search term
 */
function filterImages(searchTerm) {
    galleryState.searchTerm = searchTerm.toLowerCase();
    
    if (galleryState.searchTerm === '') {
        galleryState.filteredImages = [...galleryState.allImages];
    } else {
        galleryState.filteredImages = galleryState.allImages.filter((filename) => {
            const metadata = galleryState.imageMetadata[filename];
            return (
                filename.toLowerCase().includes(galleryState.searchTerm) ||
                metadata.documentNumber.toLowerCase().includes(galleryState.searchTerm)
            );
        });
    }
    
    updateGalleryDisplay();
    updateResultCount();
}

/**
 * Update gallery display based on filtered images
 */
function updateGalleryDisplay() {
    const cards = elements.galleryGrid.querySelectorAll('.image-card');
    
    cards.forEach((card) => {
        const filename = card.getAttribute('data-filename');
        if (galleryState.filteredImages.includes(filename)) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
    
    // Show/hide no results message
    const visibleCards = Array.from(cards).filter((card) => !card.classList.contains('hidden'));
    if (visibleCards.length === 0 && galleryState.searchTerm !== '') {
        elements.noResultsContainer.style.display = 'block';
    } else {
        elements.noResultsContainer.style.display = 'none';
    }
}

/**
 * Update result count display
 */
function updateResultCount() {
    const count = galleryState.filteredImages.length;
    const text = count === 1 ? '1 result' : `${count} results`;
    elements.resultCount.textContent = text;
}



/**
 * Handle image click to open PDF
 */
function handleImageClick(filename, pdfPath) {
    // Map image filename to PDF file and open in new tab
    try {
        window.open(pdfPath, '_blank', 'noopener,noreferrer');
    } catch (error) {
        console.error(`Failed to open PDF: ${pdfPath}`, error);
        alert('Unable to open PDF. The file may not exist.');
    }
}

/**
 * Update statistics display
 */
function updateStatistics() {
    // Update total documents count
    elements.totalDocuments.textContent = galleryState.allImages.length;
    
    // Update last updated date
    const now = new Date();
    const dateString = now.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
    elements.lastUpdated.textContent = dateString;
}

/**
 * Show or hide loading indicator
 */
function showLoading(show) {
    if (show) {
        elements.loadingContainer.style.display = 'flex';
    } else {
        elements.loadingContainer.style.display = 'none';
    }
}

/**
 * Display error message
 */
function displayErrorMessage(message) {
    elements.noResultsContainer.textContent = message;
    elements.noResultsContainer.style.display = 'block';
}

// ============================================
// Event Listeners
// ============================================

/**
 * Initialize gallery when DOM is ready
 */
document.addEventListener('DOMContentLoaded', initializeGallery);

/**
 * Handle visibility change to pause/resume lazy loading
 */
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, could pause operations
    } else {
        // Page is visible, resume operations
    }
});
