# Design Document

## Overview

The location filter feature extends the existing PDF Gallery Viewer by adding dropdown-based filtering for taluko (district) and gaam (village). The design integrates seamlessly with the current search functionality and maintains the existing architecture patterns. The solution uses the extracted_data.json file as the data source and implements cascading dropdown behavior where gaam options are filtered based on the selected taluko.

## Architecture

### Component Structure

```
Gallery System
├── Data Layer
│   ├── Location Data Loader (new)
│   └── Image List Manager (existing)
├── UI Layer
│   ├── Filter Component (new)
│   │   ├── Taluko Dropdown
│   │   ├── Gaam Dropdown
│   │   └── Clear Filters Button
│   ├── Search Component (existing)
│   └── Gallery Grid (existing)
└── State Management
    ├── Filter State (new)
    └── Gallery State (existing)
```

### Data Flow

1. **Initialization**: Load extracted_data.json → Parse location data → Populate dropdowns
2. **User Interaction**: User selects filter → Update filter state → Apply filters → Update display
3. **Combined Filtering**: Merge location filters with search filters → Filter image list → Update gallery

## Components and Interfaces

### 1. Location Data Loader

**Purpose**: Load and parse the extracted_data.json file

**Interface**:
```javascript
async function loadLocationData()
  Returns: Promise<LocationDataMap>
  
LocationDataMap = {
  [documentId: string]: {
    taluko: string,
    gaam: string
  }
}
```

**Implementation Details**:
- Fetch extracted_data.json from the root directory
- Parse JSON and validate structure
- Handle errors gracefully with fallback to empty data
- Cache parsed data in galleryState

### 2. Filter State Manager

**Purpose**: Manage filter selections and state

**State Structure**:
```javascript
filterState = {
  selectedTaluko: string | null,
  selectedGaam: string | null,
  availableTalukos: string[],
  availableGaams: string[],
  locationData: LocationDataMap
}
```

**Methods**:
- `setTalukoFilter(taluko: string | null)`: Update taluko selection
- `setGaamFilter(gaam: string | null)`: Update gaam selection
- `clearFilters()`: Reset all filters
- `getFilteredDocuments()`: Return list of document IDs matching current filters

### 3. Filter UI Component

**HTML Structure**:
```html
<div class="filter-container">
  <div class="filter-group">
    <label for="taluko-filter">Taluko (District):</label>
    <select id="taluko-filter" class="filter-dropdown">
      <option value="">Select Taluko</option>
      <!-- Options populated dynamically -->
    </select>
  </div>
  
  <div class="filter-group">
    <label for="gaam-filter">Gaam (Village):</label>
    <select id="gaam-filter" class="filter-dropdown">
      <option value="">Select Gaam</option>
      <!-- Options populated dynamically -->
    </select>
  </div>
  
  <button id="clear-filters" class="clear-filters-button">
    Clear Filters
  </button>
</div>
```

**Placement**: Insert filter container in the navigation section, between the search container and search results

**Styling**:
- Use existing CSS variables and design patterns
- Responsive layout: horizontal on desktop, stacked on mobile
- Consistent with existing button and input styles
- Visual feedback for active filters (e.g., highlighted border)

### 4. Dropdown Population Logic

**Taluko Dropdown**:
```javascript
function populateTalukoDropdown(locationData)
  1. Extract all unique taluko values
  2. Sort alphabetically
  3. Create option elements
  4. Append to dropdown
```

**Gaam Dropdown**:
```javascript
function populateGaamDropdown(locationData, selectedTaluko)
  1. If taluko selected: filter gaams by taluko
  2. Else: show all unique gaams
  3. Sort alphabetically
  4. Create option elements
  5. Append to dropdown
```

### 5. Filter Application Logic

**Combined Filter Function**:
```javascript
function applyFilters()
  1. Get current filter state (taluko, gaam, searchTerm)
  2. Start with all images
  3. If taluko selected: filter by taluko
  4. If gaam selected: filter by gaam
  5. If search term: filter by filename/document number
  6. Update filteredImages array
  7. Update gallery display
  8. Update result count
```

**Document ID Mapping**:
- Image filename format: `P0640001.jpg`
- Location data key format: `P0640001`
- Mapping: Extract document ID from filename by removing extension

## Data Models

### Location Data Structure

**Source File**: `extracted_data.json`

**Format**:
```json
{
  "P0640001": {
    "taluko": "ગાંધીનગર",
    "gaam": "ઉવારસદ"
  },
  "P0640002": {
    "taluko": "ગાંધીનગર",
    "gaam": "ઉવારસદ"
  }
}
```

### Filter State Model

```javascript
{
  selectedTaluko: "ગાંધીનગર" | null,
  selectedGaam: "ઉવારસદ" | null,
  availableTalukos: ["ગાંધીનગર", "દસક્રોઈ", "સીટી"],
  availableGaams: ["ઉવારસદ", "સરગાસણ", "શેરથા"],
  locationData: {
    "P0640001": { taluko: "ગાંધીનગર", gaam: "ઉવારસદ" }
  }
}
```

## Error Handling

### Scenarios and Responses

1. **Location Data Load Failure**
   - Log error to console
   - Display user-friendly message: "Location filters unavailable"
   - Disable filter dropdowns
   - Allow gallery to function with search only

2. **Malformed JSON Data**
   - Parse with try-catch
   - Skip invalid entries
   - Log warnings for debugging
   - Continue with valid data

3. **Missing Document Mapping**
   - If document ID not in location data, treat as "no location"
   - Don't filter out these documents when no filters are active
   - Hide these documents when location filters are active

4. **Empty Filter Results**
   - Display "No results found" message
   - Show current filter selections
   - Provide clear filters button

## Testing Strategy

### Unit Tests

1. **Location Data Loader**
   - Test successful JSON loading
   - Test error handling for network failures
   - Test parsing of malformed JSON

2. **Filter State Manager**
   - Test filter selection updates
   - Test cascading dropdown logic
   - Test clear filters functionality

3. **Filter Application**
   - Test single filter (taluko only)
   - Test single filter (gaam only)
   - Test combined filters (taluko + gaam)
   - Test combined with search
   - Test edge cases (no matches, all matches)

### Integration Tests

1. **UI Interaction**
   - Test dropdown population on load
   - Test cascading behavior (taluko → gaam)
   - Test filter application on selection
   - Test clear filters button

2. **Combined Functionality**
   - Test filters + search together
   - Test filter persistence during search
   - Test result count updates

### Manual Testing

1. **Visual Testing**
   - Verify dropdown styling matches existing design
   - Test responsive layout on mobile/tablet/desktop
   - Verify Gujarati text renders correctly

2. **User Experience**
   - Test filter selection flow
   - Verify performance with all 601 images
   - Test accessibility (keyboard navigation, screen readers)

## Performance Considerations

1. **Data Loading**
   - Load extracted_data.json once during initialization
   - Cache parsed data in memory
   - Estimated file size: ~30-50KB (acceptable for client-side loading)

2. **Filter Application**
   - Use efficient array filtering methods
   - Avoid DOM manipulation during filtering (use CSS classes)
   - Debounce not needed for dropdown changes (instant feedback expected)

3. **Dropdown Population**
   - Pre-compute unique values during initialization
   - Cache sorted arrays
   - Only rebuild gaam dropdown when taluko changes

## Accessibility

1. **Semantic HTML**
   - Use `<label>` elements associated with dropdowns
   - Use `<select>` elements for native dropdown behavior

2. **ARIA Attributes**
   - Add `aria-label` to clear filters button
   - Use `aria-live` region for result count updates

3. **Keyboard Navigation**
   - Ensure all dropdowns are keyboard accessible
   - Tab order: search → taluko → gaam → clear filters

## Future Enhancements

1. **URL Parameters**: Persist filter state in URL for sharing
2. **Multi-select**: Allow selecting multiple talukos or gaams
3. **Filter Presets**: Save common filter combinations
4. **Analytics**: Track popular filter combinations
