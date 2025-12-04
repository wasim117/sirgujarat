# Design Document

## Overview

This document outlines the design for a Next.js-based frontend application that displays Assembly-wise Voter Lists from 2002 electoral data. The application will use Next.js 14+ with the App Router, TypeScript for type safety, and Tailwind CSS for styling. The architecture emphasizes static generation for performance, with dynamic routes for scalability as new assemblies are added.

## Architecture

### Technology Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **PDF Handling**: react-pdf or pdf.js
- **State Management**: React Context API (for filters and UI state)
- **Image Optimization**: Next.js Image component
- **Deployment**: Vercel or Netlify (static export compatible)

### Application Structure

```
voter-list-app/
├── app/
│   ├── layout.tsx                 # Root layout with metadata
│   ├── page.tsx                   # Home page (assembly listing)
│   ├── assembly/
│   │   └── [code]/
│   │       ├── page.tsx           # Assembly detail page
│   │       └── loading.tsx        # Loading state
│   └── api/
│       └── assemblies/
│           └── route.ts           # API route for assembly data
├── components/
│   ├── AssemblyCard.tsx           # Assembly card component
│   ├── AssemblyGrid.tsx           # Grid layout for assemblies
│   ├── PDFViewer.tsx              # PDF viewer modal
│   ├── PDFThumbnail.tsx           # PDF thumbnail component
│   ├── SearchBar.tsx              # Search input component
│   ├── FilterPanel.tsx            # Taluko/Gaam filter component
│   └── Navigation.tsx             # Navigation header
├── lib/
│   ├── assemblyData.ts            # Assembly data fetching logic
│   ├── pdfUtils.ts                # PDF processing utilities
│   └── types.ts                   # TypeScript type definitions
├── public/
│   ├── P064/                      # Assembly PDF folders
│   ├── P070/
│   └── thumbnails/                # Generated thumbnails
└── data/
    ├── assemblies.json            # Assembly metadata
    └── location-data.json         # Taluko/Gaam mapping
```

## Components and Interfaces

### Core Components

#### 1. AssemblyCard Component
Displays a single assembly with code, name, and document count.

```typescript
interface AssemblyCardProps {
  code: string;
  name: string;
  documentCount: number;
  onClick: () => void;
}
```

#### 2. AssemblyGrid Component
Renders a responsive grid of assembly cards with search functionality.

```typescript
interface AssemblyGridProps {
  assemblies: Assembly[];
  searchQuery: string;
}
```

#### 3. PDFViewer Component
Modal component for viewing PDFs with navigation controls.

```typescript
interface PDFViewerProps {
  pdfUrl: string;
  isOpen: boolean;
  onClose: () => void;
  fileName: string;
}
```

#### 4. FilterPanel Component
Provides Taluko and Gaam dropdown filters.

```typescript
interface FilterPanelProps {
  talukos: string[];
  gaams: string[];
  selectedTaluko: string | null;
  selectedGaam: string | null;
  onTalukoChange: (taluko: string | null) => void;
  onGaamChange: (gaam: string | null) => void;
}
```

## Data Models

### Assembly Type

```typescript
interface Assembly {
  code: string;              // e.g., "P064"
  name: string;              // e.g., "Sarkhej"
  documentCount: number;
  pdfFiles: PDFFile[];
}
```

### PDFFile Type

```typescript
interface PDFFile {
  fileName: string;          // e.g., "P0640001.pdf"
  filePath: string;          // Relative path to PDF
  thumbnailPath: string;     // Path to thumbnail image
  taluko?: string;           // Optional location data
  gaam?: string;
  pageCount?: number;
}
```

### LocationData Type

```typescript
interface LocationData {
  talukos: Taluko[];
}

interface Taluko {
  name: string;
  gaams: string[];
}
```

## Data Flow

### 1. Assembly Listing (Home Page)

1. Server-side: Read assembly folders from `public/` directory
2. Server-side: Count PDF files in each folder
3. Server-side: Load assembly metadata from `data/assemblies.json`
4. Client-side: Render AssemblyGrid with data
5. Client-side: Filter assemblies based on search input

### 2. Assembly Detail Page

1. Server-side: Generate static params for all assemblies
2. Server-side: Read PDF files from assembly folder
3. Server-side: Load location data for filters
4. Client-side: Render PDF thumbnails with lazy loading
5. Client-side: Apply Taluko/Gaam filters
6. Client-side: Open PDFViewer modal on thumbnail click

### 3. PDF Viewing

1. User clicks PDF thumbnail
2. PDFViewer modal opens with PDF URL
3. react-pdf loads and renders PDF
4. User navigates pages or closes viewer

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After reviewing the prework, several properties can be consolidated:
- Properties 1.5 and 7.1 both test folder discovery - combine into one
- Properties 8.4 and 8.5 both relate to filter state management - keep separate as they test different aspects
- Properties 2.2 and 2.3 both relate to PDF display - keep separate as they test different data aspects

### Properties

Property 1: Assembly display completeness
*For any* assembly object, when rendered as a card, the output should contain the assembly code, name, and document count
**Validates: Requirements 1.2**

Property 2: Folder discovery
*For any* valid assembly folder added to the data directory, the data loading function should detect and include it in the assemblies list
**Validates: Requirements 1.5, 7.1**

Property 3: PDF listing completeness
*For any* assembly, the assembly page data should include all PDF files present in that assembly's folder
**Validates: Requirements 2.2**

Property 4: Thumbnail generation
*For any* PDF file in an assembly, a thumbnail path should be generated or referenced
**Validates: Requirements 2.3**

Property 5: Search filtering correctness
*For any* search query and assembly list, the filtered results should only include assemblies whose code or name contains the search query (case-insensitive)
**Validates: Requirements 4.1**

Property 6: Search clear restoration
*For any* assembly list, applying a search filter and then clearing it should restore the original full list
**Validates: Requirements 4.4**

Property 7: Folder name parsing
*For any* folder name following the pattern "P###" or "P###Name", the parser should correctly extract the assembly code
**Validates: Requirements 7.3**

Property 8: Taluko filtering correctness
*For any* selected Taluko and PDF list with location data, the filtered results should only include PDFs from that Taluko
**Validates: Requirements 8.2**

Property 9: Gaam filtering correctness
*For any* selected Gaam and PDF list with location data, the filtered results should only include PDFs from that Gaam
**Validates: Requirements 8.3**

Property 10: Filter count accuracy
*For any* applied filters and PDF list, the displayed count should equal the number of PDFs in the filtered results
**Validates: Requirements 8.4**

Property 11: Filter clear restoration
*For any* PDF list, applying filters and then clearing them should restore the original full list
**Validates: Requirements 8.5**

Property 12: Meta tag presence
*For any* page in the application, the rendered HTML should include title and description meta tags
**Validates: Requirements 9.1**

Property 13: Open Graph tag presence
*For any* page in the application, the rendered HTML should include Open Graph tags for social sharing
**Validates: Requirements 9.4**

## Error Handling

### PDF Loading Errors

- **Scenario**: PDF file is corrupted or missing
- **Handling**: Display error message in PDFViewer with download fallback link
- **User Action**: Option to download PDF directly or return to assembly page

### Assembly Data Loading Errors

- **Scenario**: Assembly folder exists but contains no valid PDFs
- **Handling**: Display empty state message on assembly page
- **User Action**: Show message "No voter lists available for this assembly"

### Search No Results

- **Scenario**: Search query matches no assemblies
- **Handling**: Display "No assemblies found" message with suggestion to clear search
- **User Action**: Clear search button to restore full list

### Network Errors

- **Scenario**: Static assets fail to load
- **Handling**: Show error boundary with retry option
- **User Action**: Reload page or navigate back to home

### Invalid Assembly Route

- **Scenario**: User navigates to non-existent assembly code
- **Handling**: Show 404 page with link back to home
- **User Action**: Return to assembly listing

## Testing Strategy

### Unit Testing

The application will use **Vitest** for unit testing React components and utility functions.

**Unit test coverage:**

- Assembly data loading functions (folder discovery, PDF enumeration)
- Folder name parsing logic
- Search filtering logic
- Location filter logic (Taluko/Gaam)
- Component rendering with specific props
- Error state handling

**Example unit tests:**

- Test that `parseAssemblyCode("P064")` returns `"P064"`
- Test that `parseAssemblyCode("P070Shahpur")` returns `"P070"`
- Test that AssemblyCard renders with correct props
- Test that empty assembly shows appropriate message
- Test that invalid PDF triggers error state

### Property-Based Testing

The application will use **fast-check** for property-based testing to verify universal properties across random inputs.

**Configuration:**
- Each property test will run a minimum of 100 iterations
- Tests will use custom generators for assembly data, PDF files, and search queries

**Property test tagging:**
- Each property-based test will include a comment: `// Feature: nextjs-assembly-voter-app, Property X: [property description]`

**Property test coverage:**

- Property 1: Assembly display completeness
- Property 2: Folder discovery
- Property 3: PDF listing completeness
- Property 4: Thumbnail generation
- Property 5: Search filtering correctness
- Property 6: Search clear restoration
- Property 7: Folder name parsing
- Property 8: Taluko filtering correctness
- Property 9: Gaam filtering correctness
- Property 10: Filter count accuracy
- Property 11: Filter clear restoration
- Property 12: Meta tag presence
- Property 13: Open Graph tag presence

### Integration Testing

- Test full user flows: home → assembly → PDF viewer
- Test filter interactions: Taluko selection → Gaam selection → clear
- Test search → filter combinations
- Test navigation and routing

### End-to-End Testing

While not part of the core implementation tasks, E2E tests using Playwright could verify:
- Full page loads and navigation
- PDF viewer functionality
- Responsive behavior across viewports

## Performance Considerations

### Static Generation

- Use Next.js `generateStaticParams` to pre-render all assembly pages at build time
- Generate static HTML for SEO and fast initial loads
- Leverage ISR (Incremental Static Regeneration) if data updates frequently

### Image Optimization

- Use Next.js Image component for automatic optimization
- Generate thumbnail images at build time using pdf.js
- Implement lazy loading for PDF thumbnails
- Use WebP format for thumbnails where supported

### Code Splitting

- Lazy load PDFViewer component (only load when needed)
- Split location data by assembly (load only relevant data per page)
- Use dynamic imports for heavy PDF processing libraries

### Caching Strategy

- Cache assembly metadata in memory during build
- Use browser caching for static assets (PDFs, thumbnails)
- Implement service worker for offline access (optional enhancement)

## Accessibility

- Semantic HTML structure (nav, main, article elements)
- ARIA labels for interactive elements
- Keyboard navigation support for all interactive components
- Focus management in PDF viewer modal
- Alt text for thumbnail images
- Color contrast meeting WCAG AA standards
- Screen reader announcements for filter changes

## Deployment

### Build Process

1. Run `npm run build` to generate static site
2. Next.js will:
   - Scan assembly folders
   - Generate static pages for each assembly
   - Optimize images and assets
   - Create sitemap

### Environment Variables

```
NEXT_PUBLIC_SITE_URL=https://voterlist.example.com
NEXT_PUBLIC_ASSEMBLIES_PATH=/public
```

### Hosting Options

- **Vercel**: Native Next.js support, automatic deployments
- **Netlify**: Static export with form handling
- **GitHub Pages**: Static export for simple hosting

### CI/CD Pipeline

1. Push to main branch
2. Run tests (unit + property tests)
3. Build static site
4. Deploy to hosting platform
5. Verify deployment with smoke tests

## Future Enhancements

- **Search within PDFs**: OCR integration for full-text search
- **Bookmarking**: Save favorite assemblies or PDFs
- **Comparison View**: View multiple PDFs side-by-side
- **Print Optimization**: Better print layouts for voter lists
- **Offline Mode**: Progressive Web App with offline access
- **Analytics**: Track popular assemblies and search terms
- **Multi-language**: Support for Gujarati interface
- **Export**: Download filtered results as ZIP
