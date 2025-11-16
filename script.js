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
    filterState: {
        selectedTaluko: null,
        selectedGaam: null,
        availableTalukos: [],
        availableGaams: [],
        locationData: {}
    }
};

// ============================================
// Filter State Management Functions
// ============================================

/**
 * Update taluko filter selection
 * @param {string|null} taluko - The selected taluko value, or null to clear
 */
function setTalukoFilter(taluko) {
    const previousValue = galleryState.filterState.selectedTaluko;
    galleryState.filterState.selectedTaluko = taluko;
    console.log(`[Filter State] Taluko filter changed: "${previousValue || 'none'}" → "${taluko || 'none'}"`);
}

/**
 * Update gaam filter selection
 * @param {string|null} gaam - The selected gaam value, or null to clear
 */
function setGaamFilter(gaam) {
    const previousValue = galleryState.filterState.selectedGaam;
    galleryState.filterState.selectedGaam = gaam;
    console.log(`[Filter State] Gaam filter changed: "${previousValue || 'none'}" → "${gaam || 'none'}"`);
}

/**
 * Reset all filter selections
 */
function clearFilters() {
    const hadFilters = galleryState.filterState.selectedTaluko || galleryState.filterState.selectedGaam;
    galleryState.filterState.selectedTaluko = null;
    galleryState.filterState.selectedGaam = null;
    console.log(`[Filter State] All location filters cleared${hadFilters ? ' (filters were active)' : ' (no filters were active)'}`);
}

/**
 * Get list of document IDs that match current filter selections
 * @returns {string[]} Array of document IDs matching the current filters
 */
function getFilteredDocuments() {
    const { selectedTaluko, selectedGaam, locationData } = galleryState.filterState;
    
    console.log('[Filter State] Getting filtered documents with filters:', {
        taluko: selectedTaluko || 'none',
        gaam: selectedGaam || 'none',
        totalDocuments: Object.keys(locationData).length
    });
    
    // If no filters are active, return all document IDs
    if (!selectedTaluko && !selectedGaam) {
        const allDocIds = Object.keys(locationData);
        console.log(`[Filter State] No filters active, returning all ${allDocIds.length} documents`);
        return allDocIds;
    }
    
    // Filter documents based on active filters
    const filteredDocIds = [];
    
    Object.entries(locationData).forEach(([docId, location]) => {
        let matches = true;
        
        // Check taluko filter if active
        if (selectedTaluko && location.taluko !== selectedTaluko) {
            matches = false;
        }
        
        // Check gaam filter if active
        if (selectedGaam && location.gaam !== selectedGaam) {
            matches = false;
        }
        
        if (matches) {
            filteredDocIds.push(docId);
        }
    });
    
    console.log(`[Filter State] Filtered documents: ${filteredDocIds.length} matches out of ${Object.keys(locationData).length} total`);
    return filteredDocIds;
}

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
        console.log('[Init] Starting gallery initialization...');
        showLoading(true);
        
        // Fetch image list from directory
        console.log('[Init] Step 1: Fetching image list...');
        await fetchImageList();
        console.log('[Init] Step 1 complete: Image list loaded');
        
        // Load location data for filtering
        console.log('[Init] Step 2: Loading location data...');
        const locationDataLoaded = await loadLocationData();
        
        if (locationDataLoaded) {
            console.log('[Init] Step 2 complete: Location data loaded successfully');
            
            // Populate filter dropdowns only if location data loaded successfully
            console.log('[Init] Step 3: Populating filter dropdowns...');
            populateTalukoDropdown();
            populateGaamDropdown();
            console.log('[Init] Step 3 complete: Filter dropdowns populated');
        } else {
            console.warn('[Init] Step 2 warning: Location data failed to load, filters disabled');
            console.log('[Init] Step 3: Skipping filter dropdown population');
        }
        
        // Generate image cards
        console.log('[Init] Step 4: Generating image cards...');
        generateImageCards(galleryState.allImages);
        console.log('[Init] Step 4 complete: Image cards generated');
        
        // Set up event listeners
        console.log('[Init] Step 5: Setting up event listeners...');
        setupEventListeners();
        console.log('[Init] Step 5 complete: Event listeners set up');
        
        // Update statistics
        console.log('[Init] Step 6: Updating statistics...');
        updateStatistics();
        console.log('[Init] Step 6 complete: Statistics updated');
        
        showLoading(false);
        console.log('[Init] Gallery initialization complete!');
    } catch (error) {
        console.error('[Init] Gallery initialization failed:', error);
        console.error('[Init] Error details:', {
            message: error.message,
            stack: error.stack
        });
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
 * Load and parse location data from extracted_data.json
 */
async function loadLocationData() {
    try {
        console.log('[Location Data] Loading from extracted_data.json...');
        
        // Fetch the JSON file
        const response = await fetch('extracted_data.json');
        
        // Check if fetch was successful
        if (!response.ok) {
            throw new Error(`Failed to fetch location data: ${response.status} ${response.statusText}`);
        }
        
        // Parse JSON
        const locationData = await response.json();
        
        // Validate that we got an object
        if (!locationData || typeof locationData !== 'object') {
            throw new Error('Invalid location data format: expected an object');
        }
        
        // Store location data in state
        galleryState.filterState.locationData = locationData;
        
        // Extract and cache unique taluko and gaam values
        const talukos = new Set();
        const gaams = new Set();
        let documentsWithoutLocation = 0;
        
        Object.entries(locationData).forEach(([docId, entry]) => {
            // Track documents without complete location data
            if (!entry || !entry.taluko || !entry.gaam) {
                documentsWithoutLocation++;
                console.warn(`[Location Data] Document ${docId} has incomplete location data:`, entry);
            }
            
            if (entry && entry.taluko) {
                talukos.add(entry.taluko);
            }
            if (entry && entry.gaam) {
                gaams.add(entry.gaam);
            }
        });
        
        // Sort alphabetically and store in state
        galleryState.filterState.availableTalukos = Array.from(talukos).sort();
        galleryState.filterState.availableGaams = Array.from(gaams).sort();
        
        console.log('[Location Data] Loaded successfully:');
        console.log(`  - ${Object.keys(locationData).length} documents with location data`);
        console.log(`  - ${galleryState.filterState.availableTalukos.length} unique talukos`);
        console.log(`  - ${galleryState.filterState.availableGaams.length} unique gaams`);
        if (documentsWithoutLocation > 0) {
            console.warn(`  - ${documentsWithoutLocation} documents have incomplete location data`);
        }
        
        return true;
    } catch (error) {
        console.error('[Location Data] Failed to load:', error);
        console.error('[Location Data] Error details:', {
            message: error.message,
            stack: error.stack
        });
        
        // Display user-friendly error message
        displayLocationDataError(error);
        
        // Return false to indicate failure, but don't throw
        // This allows the gallery to continue functioning without filters
        return false;
    }
}

/**
 * Display error message when location data fails to load
 * @param {Error} error - The error that occurred during loading
 */
function displayLocationDataError(error) {
    console.warn('[Location Data] Location filters will be unavailable');
    
    // Disable filter dropdowns and show error state
    const talukoDropdown = document.getElementById('taluko-filter');
    const gaamDropdown = document.getElementById('gaam-filter');
    const clearFiltersButton = document.getElementById('clear-filters');
    const filterContainer = document.querySelector('.filter-container');
    
    if (talukoDropdown) {
        talukoDropdown.disabled = true;
        talukoDropdown.innerHTML = '<option value="">Location data unavailable</option>';
        talukoDropdown.classList.add('filter-disabled');
    }
    
    if (gaamDropdown) {
        gaamDropdown.disabled = true;
        gaamDropdown.innerHTML = '<option value="">Location data unavailable</option>';
        gaamDropdown.classList.add('filter-disabled');
    }
    
    if (clearFiltersButton) {
        clearFiltersButton.disabled = true;
        clearFiltersButton.classList.add('filter-disabled');
    }
    
    if (filterContainer) {
        filterContainer.classList.add('filter-error');
        
        // Add error message to filter container
        const errorMessage = document.createElement('div');
        errorMessage.className = 'filter-error-message';
        errorMessage.innerHTML = `
            <span class="error-icon">⚠️</span>
            <span class="error-text">Location filters unavailable. Gallery search still works.</span>
        `;
        filterContainer.appendChild(errorMessage);
    }
    
    console.log('[Location Data] Filter UI disabled due to loading failure');
}

/**
 * Populate taluko dropdown with unique values from location data
 */
function populateTalukoDropdown() {
    const talukoDropdown = document.getElementById('taluko-filter');
    
    if (!talukoDropdown) {
        console.error('[Dropdown] Taluko dropdown element not found');
        return;
    }
    
    // Clear existing options except the default one
    talukoDropdown.innerHTML = '<option value="">Select Taluko</option>';
    
    // Get unique taluko values from state (already sorted alphabetically)
    const talukos = galleryState.filterState.availableTalukos;
    
    console.log(`[Dropdown] Populating taluko dropdown with ${talukos.length} options`);
    
    // Create and append option elements for each taluko
    talukos.forEach((taluko) => {
        const option = document.createElement('option');
        option.value = taluko;
        option.textContent = taluko;
        talukoDropdown.appendChild(option);
    });
    
    console.log(`[Dropdown] Taluko dropdown populated successfully`);
}

/**
 * Populate gaam dropdown with values filtered by selected taluko
 * @param {string|null} selectedTaluko - The currently selected taluko, or null for all gaams
 */
function populateGaamDropdown(selectedTaluko = null) {
    const gaamDropdown = document.getElementById('gaam-filter');
    
    if (!gaamDropdown) {
        console.error('[Dropdown] Gaam dropdown element not found');
        return;
    }
    
    console.log(`[Dropdown] Populating gaam dropdown${selectedTaluko ? ` (filtered by taluko: "${selectedTaluko}")` : ' (all gaams)'}`);
    
    // Clear existing options except the default one
    gaamDropdown.innerHTML = '<option value="">Select Gaam</option>';
    
    let gaamsToDisplay = [];
    
    // If a taluko is selected, filter gaams by that taluko
    if (selectedTaluko) {
        const locationData = galleryState.filterState.locationData;
        const gaamSet = new Set();
        
        // Iterate through location data to find gaams in the selected taluko
        Object.values(locationData).forEach((entry) => {
            if (entry && entry.taluko === selectedTaluko && entry.gaam) {
                gaamSet.add(entry.gaam);
            }
        });
        
        // Convert to array and sort alphabetically
        gaamsToDisplay = Array.from(gaamSet).sort();
        console.log(`[Dropdown] Found ${gaamsToDisplay.length} gaams in taluko "${selectedTaluko}"`);
    } else {
        // No taluko selected, show all unique gaams (already sorted in state)
        gaamsToDisplay = galleryState.filterState.availableGaams;
        console.log(`[Dropdown] Showing all ${gaamsToDisplay.length} gaams`);
    }
    
    // Create and append option elements for each gaam
    gaamsToDisplay.forEach((gaam) => {
        const option = document.createElement('option');
        option.value = gaam;
        option.textContent = gaam;
        gaamDropdown.appendChild(option);
    });
    
    console.log(`[Dropdown] Gaam dropdown populated successfully with ${gaamsToDisplay.length} options`);
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
        </div>
        <div class="card-metadata">
            <div class="card-filename">${metadata.documentNumber}</div>
            <div class="card-info">
                <div class="card-info-item">
                    <span class="card-info-value">${filename}</span>
                </div>
            </div>
            <button class="pdf-link-button" data-pdf="${pdfPath}" aria-label="Open PDF for ${metadata.documentNumber}">
                📄 Open PDF
            </button>
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
    const documentNumber = `P064.zip/P064/P064${number}`;
    
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
    
    // Taluko dropdown change event - cascading behavior
    const talukoDropdown = document.getElementById('taluko-filter');
    if (talukoDropdown) {
        talukoDropdown.addEventListener('change', (e) => {
            const selectedTaluko = e.target.value || null;
            
            // Update taluko filter state
            setTalukoFilter(selectedTaluko);
            
            // Repopulate gaam dropdown based on selected taluko
            populateGaamDropdown(selectedTaluko);
            
            // Reset gaam selection
            const gaamDropdown = document.getElementById('gaam-filter');
            if (gaamDropdown) {
                gaamDropdown.value = '';
                setGaamFilter(null);
            }
            
            // Trigger filter application
            applyLocationFilters();
        });
    }
    
    // Gaam dropdown change event
    const gaamDropdown = document.getElementById('gaam-filter');
    if (gaamDropdown) {
        gaamDropdown.addEventListener('change', (e) => {
            const selectedGaam = e.target.value || null;
            
            // Update gaam filter state
            setGaamFilter(selectedGaam);
            
            // Trigger filter application
            applyLocationFilters();
        });
    }
    
    // Clear filters button click event
    const clearFiltersButton = document.getElementById('clear-filters');
    if (clearFiltersButton) {
        clearFiltersButton.addEventListener('click', () => {
            // Reset taluko dropdown to default option
            if (talukoDropdown) {
                talukoDropdown.value = '';
            }
            
            // Reset gaam dropdown to default option
            if (gaamDropdown) {
                gaamDropdown.value = '';
            }
            
            // Clear filter state
            clearFilters();
            
            // Repopulate gaam dropdown to show all gaams (no taluko filter)
            populateGaamDropdown(null);
            
            // Trigger gallery display update
            applyLocationFilters();
        });
    }
}

/**
 * Apply location filters (taluko and gaam) to the gallery
 * This function is called when location filter dropdowns change
 */
function applyLocationFilters() {
    // Reuse the combined filter logic
    filterImages(galleryState.searchTerm);
}

/**
 * Filter images based on search term and location filters
 * This function implements combined filter application logic
 * @param {string} searchTerm - The search term to filter by
 */
function filterImages(searchTerm) {
    console.log('[Filter] Starting filter operation...');
    
    // Update search term in state
    galleryState.searchTerm = searchTerm.toLowerCase();
    
    // Start with all images
    let filtered = [...galleryState.allImages];
    let documentsWithoutLocationData = 0;
    
    // Get current location filter state
    const { selectedTaluko, selectedGaam, locationData } = galleryState.filterState;
    
    console.log('[Filter] Active filters:', {
        taluko: selectedTaluko || 'none',
        gaam: selectedGaam || 'none',
        searchTerm: galleryState.searchTerm || 'none'
    });
    
    // Step 1: Apply location filters (taluko and/or gaam) if any are active
    if (selectedTaluko || selectedGaam) {
        filtered = filtered.filter((filename) => {
            // Map image filename to document ID for location data lookup
            // Extract document ID from filename (e.g., P0640001.jpg -> P0640001)
            const docId = filename.replace('.jpg', '');
            
            // Get location data for this document
            const location = locationData[docId];
            
            // If document has no location data, exclude it when filters are active
            // This treats documents without location data as not matching any location filter
            if (!location) {
                documentsWithoutLocationData++;
                console.debug(`[Filter] Document ${docId} has no location data, excluding from filtered results`);
                return false;
            }
            
            // Apply taluko filter if selected
            if (selectedTaluko && location.taluko !== selectedTaluko) {
                return false;
            }
            
            // Apply gaam filter if selected
            if (selectedGaam && location.gaam !== selectedGaam) {
                return false;
            }
            
            // Document matches all active location filters
            return true;
        });
        
        console.log(`[Filter] Location filters applied: ${filtered.length} images match` +
                    (selectedTaluko ? ` taluko="${selectedTaluko}"` : '') +
                    (selectedGaam ? ` gaam="${selectedGaam}"` : ''));
        
        if (documentsWithoutLocationData > 0) {
            console.log(`[Filter] ${documentsWithoutLocationData} documents excluded due to missing location data`);
        }
    }
    
    // Step 2: Combine with existing search term filter
    if (galleryState.searchTerm) {
        const beforeSearchCount = filtered.length;
        filtered = filtered.filter((filename) => {
            const metadata = galleryState.imageMetadata[filename];
            const searchMatch = (
                filename.toLowerCase().includes(galleryState.searchTerm) ||
                metadata.documentNumber.toLowerCase().includes(galleryState.searchTerm)
            );
            return searchMatch;
        });
        
        console.log(`[Filter] Search filter applied: ${filtered.length} of ${beforeSearchCount} images match term="${galleryState.searchTerm}"`);
    }
    
    // Step 3: Update filteredImages array with results matching all active filters
    galleryState.filteredImages = filtered;
    
    console.log(`[Filter] Final result: ${filtered.length} of ${galleryState.allImages.length} images displayed`);
    
    // Update display
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
    
    // Show/hide no results message with appropriate context
    const visibleCards = Array.from(cards).filter((card) => !card.classList.contains('hidden'));
    const hasActiveFilters = galleryState.filterState.selectedTaluko || 
                            galleryState.filterState.selectedGaam || 
                            galleryState.searchTerm !== '';
    
    if (visibleCards.length === 0 && hasActiveFilters) {
        // Display appropriate message based on which filters are active
        displayNoResultsMessage();
        elements.noResultsContainer.style.display = 'block';
    } else {
        elements.noResultsContainer.style.display = 'none';
    }
    
    console.log(`[Display] Gallery updated: ${visibleCards.length} cards visible`);
}

/**
 * Display appropriate "no results" message based on active filters
 */
function displayNoResultsMessage() {
    const { selectedTaluko, selectedGaam } = galleryState.filterState;
    const hasSearch = galleryState.searchTerm !== '';
    
    let message = '<p><strong>No results found</strong></p>';
    
    // Build detailed message based on active filters
    const activeFilters = [];
    if (selectedTaluko) {
        activeFilters.push(`Taluko: <em>${selectedTaluko}</em>`);
    }
    if (selectedGaam) {
        activeFilters.push(`Gaam: <em>${selectedGaam}</em>`);
    }
    if (hasSearch) {
        activeFilters.push(`Search: <em>"${galleryState.searchTerm}"</em>`);
    }
    
    if (activeFilters.length > 0) {
        message += '<p>No documents match the following filters:</p>';
        message += '<ul class="filter-list">';
        activeFilters.forEach(filter => {
            message += `<li>${filter}</li>`;
        });
        message += '</ul>';
        message += '<p>Try adjusting your filters or <button id="clear-all-filters-inline" class="inline-clear-button">clear all filters</button> to see more results.</p>';
    }
    
    elements.noResultsContainer.innerHTML = message;
    
    // Add event listener to inline clear button if it exists
    const inlineClearButton = document.getElementById('clear-all-filters-inline');
    if (inlineClearButton) {
        inlineClearButton.addEventListener('click', () => {
            // Clear all filters including search
            elements.searchInput.value = '';
            const talukoDropdown = document.getElementById('taluko-filter');
            const gaamDropdown = document.getElementById('gaam-filter');
            
            if (talukoDropdown) talukoDropdown.value = '';
            if (gaamDropdown) gaamDropdown.value = '';
            
            clearFilters();
            populateGaamDropdown(null);
            filterImages('');
            
            console.log('[Display] All filters cleared via inline button');
        });
    }
    
    console.log('[Display] No results message displayed with active filters:', activeFilters);
}

/**
 * Update result count display
 * This function reflects combined filter results from location filters and search
 */
function updateResultCount() {
    const count = galleryState.filteredImages.length;
    const total = galleryState.allImages.length;
    
    // Build result text with filter state information
    let text = count === 1 ? '1 result' : `${count} results`;
    
    // Add filter state information if filters are active
    const filterInfo = getActiveFilterInfo();
    if (filterInfo) {
        text += ` ${filterInfo}`;
        // Add visual class to highlight result count when filters are active
        elements.resultCount.classList.add('has-filters');
    } else {
        // Remove visual class when no filters are active
        elements.resultCount.classList.remove('has-filters');
    }
    
    elements.resultCount.textContent = text;
    
    // Update visual indication of active filters
    updateFilterVisualState();
}

/**
 * Get information about currently active filters
 * @returns {string} Description of active filters, or empty string if none
 */
function getActiveFilterInfo() {
    const { selectedTaluko, selectedGaam } = galleryState.filterState;
    const hasSearch = galleryState.searchTerm !== '';
    
    const filterParts = [];
    
    if (selectedTaluko) {
        filterParts.push(`taluko: ${selectedTaluko}`);
    }
    
    if (selectedGaam) {
        filterParts.push(`gaam: ${selectedGaam}`);
    }
    
    if (hasSearch) {
        filterParts.push(`search: "${galleryState.searchTerm}"`);
    }
    
    if (filterParts.length === 0) {
        return '';
    }
    
    return `(filtered by ${filterParts.join(', ')})`;
}

/**
 * Update visual indication of active filters in the UI
 * Adds/removes CSS classes to show when filters are applied
 */
function updateFilterVisualState() {
    const { selectedTaluko, selectedGaam } = galleryState.filterState;
    
    // Get filter elements
    const talukoDropdown = document.getElementById('taluko-filter');
    const gaamDropdown = document.getElementById('gaam-filter');
    const filterContainer = document.querySelector('.filter-container');
    
    // Add 'active' class to dropdowns when they have a selection
    if (talukoDropdown) {
        if (selectedTaluko) {
            talukoDropdown.classList.add('filter-active');
        } else {
            talukoDropdown.classList.remove('filter-active');
        }
    }
    
    if (gaamDropdown) {
        if (selectedGaam) {
            gaamDropdown.classList.add('filter-active');
        } else {
            gaamDropdown.classList.remove('filter-active');
        }
    }
    
    // Add 'has-active-filters' class to container when any filter is active
    if (filterContainer) {
        if (selectedTaluko || selectedGaam) {
            filterContainer.classList.add('has-active-filters');
        } else {
            filterContainer.classList.remove('has-active-filters');
        }
    }
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
    
    // Update filter availability statistics
    const { availableTalukos, availableGaams, locationData } = galleryState.filterState;
    const hasLocationData = Object.keys(locationData).length > 0;
    
    if (hasLocationData) {
        console.log('[Statistics] Filter availability:', {
            totalDocuments: galleryState.allImages.length,
            documentsWithLocation: Object.keys(locationData).length,
            availableTalukos: availableTalukos.length,
            availableGaams: availableGaams.length
        });
        
        // Add filter statistics to the UI if there's a stats container
        const statsContainer = document.querySelector('.stats-container');
        if (statsContainer) {
            // Check if filter stats already exist
            let filterStats = document.getElementById('filter-stats');
            if (!filterStats) {
                filterStats = document.createElement('div');
                filterStats.id = 'filter-stats';
                filterStats.className = 'stat-item';
                statsContainer.appendChild(filterStats);
            }
            
            filterStats.innerHTML = `
                <span class="stat-label">Filters:</span>
                <span class="stat-value">${availableTalukos.length} talukos, ${availableGaams.length} gaams</span>
            `;
        }
    } else {
        console.log('[Statistics] Location filters unavailable - no location data loaded');
        
        // Remove filter stats if they exist
        const filterStats = document.getElementById('filter-stats');
        if (filterStats) {
            filterStats.remove();
        }
    }
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
