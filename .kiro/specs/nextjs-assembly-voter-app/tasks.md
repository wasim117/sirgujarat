# Implementation Plan

- [ ] 1. Initialize Next.js project with TypeScript and Tailwind CSS
  - Create new Next.js 14+ project with App Router
  - Configure TypeScript with strict mode
  - Set up Tailwind CSS with custom configuration
  - Install required dependencies (react-pdf, fast-check, vitest)
  - Configure project structure (app/, components/, lib/ directories)
  - _Requirements: All_

- [ ] 2. Set up data layer and type definitions
  - [ ] 2.1 Create TypeScript type definitions
    - Define Assembly, PDFFile, LocationData interfaces in lib/types.ts
    - Export all types for use across the application
    - _Requirements: 1.1, 2.2, 8.1_

  - [ ] 2.2 Implement assembly data loading utilities
    - Create lib/assemblyData.ts with folder scanning logic
    - Implement function to read assembly folders from public directory
    - Implement function to count PDFs in each assembly folder
    - Implement function to load assembly metadata
    - _Requirements: 1.1, 1.5, 7.1_

  - [ ]* 2.3 Write property test for folder discovery
    - **Property 2: Folder discovery**
    - **Validates: Requirements 1.5, 7.1**

  - [ ] 2.4 Implement folder name parsing
    - Create parser function to extract assembly code from folder names
    - Handle patterns like "P064" and "P070Shahpur"
    - _Requirements: 7.3_

  - [ ]* 2.5 Write property test for folder name parsing
    - **Property 7: Folder name parsing**
    - **Validates: Requirements 7.3**

  - [ ] 2.6 Create location data utilities
    - Implement function to load Taluko/Gaam data from JSON
    - Create mapping functions for PDF location metadata
    - _Requirements: 8.1, 8.2, 8.3_

- [ ] 3. Build core UI components
  - [ ] 3.1 Create AssemblyCard component
    - Implement card component with code, name, and document count
    - Add hover effects and click handling
    - Style with Tailwind CSS
    - _Requirements: 1.2, 1.3_

  - [ ]* 3.2 Write property test for assembly display completeness
    - **Property 1: Assembly display completeness**
    - **Validates: Requirements 1.2**

  - [ ] 3.3 Create SearchBar component
    - Implement controlled input with real-time filtering
    - Add clear button functionality
    - Style with Tailwind CSS
    - _Requirements: 4.1, 4.4_

  - [ ] 3.4 Create AssemblyGrid component
    - Implement responsive grid layout
    - Integrate search filtering logic
    - Handle empty states
    - _Requirements: 1.4, 4.3_

  - [ ]* 3.5 Write property tests for search functionality
    - **Property 5: Search filtering correctness**
    - **Property 6: Search clear restoration**
    - **Validates: Requirements 4.1, 4.4**

  - [ ] 3.6 Create Navigation component
    - Implement header with site title and navigation links
    - Add breadcrumb navigation for assembly pages
    - Style with Tailwind CSS
    - _Requirements: 2.5_

- [ ] 4. Implement home page
  - [ ] 4.1 Create app/page.tsx
    - Fetch assembly data at build time
    - Render AssemblyGrid with SearchBar
    - Add page metadata for SEO
    - _Requirements: 1.1, 1.2, 9.1_

  - [ ]* 4.2 Write property test for meta tag presence
    - **Property 12: Meta tag presence**
    - **Validates: Requirements 9.1**

  - [ ] 4.3 Create app/layout.tsx
    - Set up root layout with Navigation
    - Configure global metadata and Open Graph tags
    - Add font optimization
    - _Requirements: 9.1, 9.4_

  - [ ]* 4.4 Write property test for Open Graph tags
    - **Property 13: Open Graph tag presence**
    - **Validates: Requirements 9.4**

- [ ] 5. Build PDF thumbnail and viewer components
  - [ ] 5.1 Create PDFThumbnail component
    - Implement thumbnail display with lazy loading
    - Add click handler to open viewer
    - Show PDF filename and metadata
    - _Requirements: 2.3_

  - [ ]* 5.2 Write property test for thumbnail generation
    - **Property 4: Thumbnail generation**
    - **Validates: Requirements 2.3**

  - [ ] 5.3 Create PDFViewer modal component
    - Implement modal with react-pdf integration
    - Add page navigation controls
    - Add zoom controls
    - Add close button and error handling
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ]* 5.4 Write unit tests for PDF viewer interactions
    - Test modal open/close state
    - Test error state display
    - Test download fallback option
    - _Requirements: 3.1, 3.4, 3.5_

- [ ] 6. Implement location filtering
  - [ ] 6.1 Create FilterPanel component
    - Implement Taluko dropdown with options
    - Implement Gaam dropdown with cascading options
    - Add clear filters button
    - Style with Tailwind CSS
    - _Requirements: 8.1, 8.2, 8.3, 8.5_

  - [ ] 6.2 Implement filter logic functions
    - Create Taluko filtering function
    - Create Gaam filtering function
    - Create filter count calculation function
    - Create filter clear function
    - _Requirements: 8.2, 8.3, 8.4, 8.5_

  - [ ]* 6.3 Write property tests for filtering
    - **Property 8: Taluko filtering correctness**
    - **Property 9: Gaam filtering correctness**
    - **Property 10: Filter count accuracy**
    - **Property 11: Filter clear restoration**
    - **Validates: Requirements 8.2, 8.3, 8.4, 8.5**

- [ ] 7. Create assembly detail pages
  - [ ] 7.1 Implement app/assembly/[code]/page.tsx
    - Create dynamic route with generateStaticParams
    - Fetch PDF list for assembly
    - Load location data for filters
    - Render FilterPanel and PDF grid
    - Add page metadata with assembly name
    - _Requirements: 2.1, 2.2, 8.1_

  - [ ]* 7.2 Write property test for PDF listing completeness
    - **Property 3: PDF listing completeness**
    - **Validates: Requirements 2.2**

  - [ ] 7.3 Create app/assembly/[code]/loading.tsx
    - Implement loading skeleton for assembly page
    - _Requirements: 6.5_

  - [ ] 7.4 Handle empty assembly state
    - Display message when assembly has no PDFs
    - _Requirements: 2.4_

  - [ ] 7.5 Implement 404 page for invalid assemblies
    - Create app/not-found.tsx
    - Add link back to home page
    - _Requirements: Error Handling_

- [ ] 8. Add PDF thumbnail generation
  - [ ] 8.1 Create thumbnail generation script
    - Use pdf.js to extract first page of each PDF
    - Generate thumbnail images at build time
    - Save thumbnails to public/thumbnails directory
    - _Requirements: 2.3_

  - [ ] 8.2 Integrate thumbnail generation into build process
    - Add script to package.json
    - Run before Next.js build
    - _Requirements: 2.3_

- [ ] 9. Implement SEO and metadata
  - [ ] 9.1 Create sitemap generation
    - Implement app/sitemap.ts
    - Include all assembly pages
    - _Requirements: 9.3_

  - [ ] 9.2 Add robots.txt
    - Create public/robots.txt
    - Allow all crawlers
    - _Requirements: 9.1_

  - [ ] 9.3 Configure metadata for all pages
    - Add dynamic metadata to assembly pages
    - Include Open Graph images
    - _Requirements: 9.1, 9.4_

- [ ] 10. Optimize performance
  - [ ] 10.1 Implement image optimization
    - Use Next.js Image component for thumbnails
    - Configure image loader for PDFs
    - _Requirements: 6.2_

  - [ ] 10.2 Add lazy loading for PDF thumbnails
    - Implement intersection observer for thumbnails
    - Load thumbnails as they enter viewport
    - _Requirements: 6.2_

  - [ ] 10.3 Optimize PDF viewer loading
    - Lazy load PDFViewer component with dynamic import
    - Implement progressive PDF page loading
    - _Requirements: 6.4_

- [ ] 11. Add error boundaries and error handling
  - [ ] 11.1 Create error boundary component
    - Implement app/error.tsx
    - Add retry functionality
    - _Requirements: Error Handling_

  - [ ] 11.2 Add error states to components
    - Handle PDF loading errors in PDFViewer
    - Handle data loading errors in pages
    - _Requirements: 3.5, Error Handling_

- [ ] 12. Create assembly metadata file
  - [ ] 12.1 Create data/assemblies.json
    - Add metadata for P064 (Sarkhej)
    - Add metadata for P070 (Shahpur)
    - Document schema for adding new assemblies
    - _Requirements: 1.1, 7.2_

  - [ ] 12.2 Create data/location-data.json
    - Add Taluko and Gaam mappings
    - Structure data for cascading dropdowns
    - _Requirements: 8.1_

- [ ] 13. Configure deployment
  - [ ] 13.1 Create next.config.js
    - Configure static export if needed
    - Set up image optimization
    - Configure base path if deploying to subdirectory
    - _Requirements: Deployment_

  - [ ] 13.2 Create deployment documentation
    - Document build process
    - Document environment variables
    - Add deployment instructions for Vercel/Netlify
    - _Requirements: Deployment_

- [ ] 14. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
