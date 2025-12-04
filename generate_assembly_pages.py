#!/usr/bin/env python3
"""
Assembly Constituency Page Generator

This script generates 182 HTML pages (one per assembly constituency) from a template.
Each page has unique SEO meta tags, titles, and H1 tags while maintaining the same structure.

Usage:
    python generate_assembly_pages.py

To regenerate pages:
    1. Update anand.html (template) if needed
    2. Update assembly_constituencies.json if needed
    3. Run: python generate_assembly_pages.py
"""

import json
import re
import os
from pathlib import Path


def load_template(template_path='anand.html'):
    """Load the HTML template file."""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading template: {e}")
        return None


def load_assemblies(json_path='assembly_constituencies.json'):
    """Load assembly constituency data from JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Assembly data file '{json_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def generate_title(assembly_name):
    """Generate page title for assembly."""
    # Remove parentheses content for title (e.g., "Abdasa" not "Abdasa (SC)")
    clean_name = re.sub(r'\s*\([^)]+\)', '', assembly_name)
    return f"Search SIR 2002 voter list {clean_name.lower()} gujarat"


def generate_description(assembly_name):
    """Generate meta description for assembly (placeholder - user will customize later)."""
    clean_name = re.sub(r'\s*\([^)]+\)', '', assembly_name)
    return f"Search 2002 voter list {clean_name.lower()} gujarat electoral records. Browse and find voter records by taluko and gaam for {clean_name} assembly constituency."


def generate_h1(assembly_name):
    """Generate H1 heading for assembly."""
    # Keep parentheses for H1 (e.g., "Abdasa (SC)")
    return f"{assembly_name} - 2002 Voter List Gujarat"


def replace_meta_tag(html, tag_name, attribute, new_value):
    """Replace a meta tag value in HTML."""
    # Pattern for meta tags: <meta name="..." content="..."> or <meta property="..." content="...">
    pattern = rf'<meta\s+(?:name|property)="{re.escape(tag_name)}"\s+content="[^"]*"'
    replacement = f'<meta {attribute}="{tag_name}" content="{new_value}"'
    return re.sub(pattern, replacement, html)


def replace_title(html, new_title):
    """Replace the <title> tag content."""
    pattern = r'<title>.*?</title>'
    replacement = f'<title>{new_title}</title>'
    return re.sub(pattern, replacement, html, flags=re.DOTALL)


def replace_canonical(html, url):
    """Replace the canonical URL."""
    pattern = r'<link\s+rel="canonical"\s+href="[^"]*"'
    replacement = f'<link rel="canonical" href="{url}"'
    return re.sub(pattern, replacement, html)


def replace_h1(html, new_h1):
    """Replace the H1 tag content."""
    # Find the H1 in the header section
    pattern = r'(<h1>).*?(</h1>)'
    replacement = f'\\1{new_h1}\\2'
    return re.sub(pattern, replacement, html, count=1)


def replace_json_ld(html, assembly_name, description, base_url):
    """Replace JSON-LD structured data."""
    # Find the JSON-LD script tag and update name and description
    # Pattern matches: "name": "content"
    pattern = r'"name":\s*"[^"]*"'
    replacement = f'"name": "2002 Voter List Gujarat - {assembly_name}"'
    html = re.sub(pattern, replacement, html, count=1)
    
    # Pattern matches: "description": "content"
    pattern = r'"description":\s*"[^"]*"'
    replacement = f'"description": "{description}"'
    html = re.sub(pattern, replacement, html, count=1)
    
    # Update URL in JSON-LD
    pattern = r'"url":\s*"[^"]*"'
    replacement = f'"url": "{base_url}"'
    html = re.sub(pattern, replacement, html, count=1)
    
    return html


def replace_og_image(html, base_url):
    """Replace Open Graph and Twitter image URLs."""
    # Replace og:image
    pattern = r'<meta\s+property="og:image"\s+content="[^"]*"'
    replacement = f'<meta property="og:image" content="{base_url}og-image.jpg"'
    html = re.sub(pattern, replacement, html)
    
    # Replace twitter:image
    pattern = r'<meta\s+name="twitter:image"\s+content="[^"]*"'
    replacement = f'<meta name="twitter:image" content="{base_url}og-image.jpg"'
    html = re.sub(pattern, replacement, html)
    
    return html


def generate_assembly_links_html(assemblies, current_slug, base_url):
    """Generate HTML for assembly links section."""
    links_html = '''    <!-- Other Assembly Constituencies Links -->
    <section class="assembly-links-section" style="padding: 40px 20px; background: #ffffff; margin: 40px 0; border-top: 2px solid #e9ecef;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <h2 style="text-align: center; color: #007bff; margin-bottom: 20px; font-size: 24px;">Other Assembly Constituencies</h2>
            <p style="text-align: center; color: #666; margin-bottom: 30px;">Browse 2002 voter list for other assembly constituencies:</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; margin-top: 20px;">'''
    
    for assembly in assemblies:
        if assembly['slug'] != current_slug:  # Don't link to current page
            links_html += f'''
                <a href="{assembly['slug']}.html" style="display: block; padding: 10px 12px; background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; text-decoration: none; color: #333; transition: all 0.3s ease; text-align: center; font-size: 14px;" onmouseover="this.style.background='#007bff'; this.style.color='#fff'; this.style.borderColor='#007bff';" onmouseout="this.style.background='#f8f9fa'; this.style.color='#333'; this.style.borderColor='#dee2e6';">
                    {assembly['full_name']}
                </a>'''
    
    links_html += '''
            </div>
        </div>
    </section>'''
    
    return links_html


def insert_assembly_links(html, assemblies, current_slug, base_url):
    """Insert assembly links section before the CTA section."""
    links_html = generate_assembly_links_html(assemblies, current_slug, base_url)
    
    # Find the CTA section and insert before it
    pattern = r'(\s+<!-- CTA Section for Fillable Form -->)'
    replacement = f'{links_html}\\n\\1'
    html = re.sub(pattern, replacement, html)
    
    return html


def generate_page(html_template, assembly, assemblies_list, base_url='https://sir-2002.gujrera.com/'):
    """Generate a single assembly page from template."""
    html = html_template
    
    # Generate values
    title = generate_title(assembly['name'])
    description = generate_description(assembly['name'])
    h1 = generate_h1(assembly['name'])
    page_url = f"{base_url}{assembly['slug']}.html"
    
    # Replace title
    html = replace_title(html, title)
    
    # Replace meta description
    html = replace_meta_tag(html, 'description', 'name', description)
    
    # Replace Open Graph tags
    html = replace_meta_tag(html, 'og:title', 'property', title)
    html = replace_meta_tag(html, 'og:description', 'property', description)
    html = replace_meta_tag(html, 'og:url', 'property', page_url)
    
    # Replace Twitter Card tags
    html = replace_meta_tag(html, 'twitter:title', 'name', title)
    html = replace_meta_tag(html, 'twitter:description', 'name', description)
    
    # Replace canonical URL
    html = replace_canonical(html, page_url)
    
    # Replace H1
    html = replace_h1(html, h1)
    
    # Replace JSON-LD structured data
    html = replace_json_ld(html, assembly['name'], description, base_url)
    
    # Replace OG image URLs
    html = replace_og_image(html, base_url)
    
    # Insert assembly links section
    html = insert_assembly_links(html, assemblies_list, assembly['slug'], base_url)
    
    return html


def main():
    """Main function to generate all assembly pages."""
    print("=" * 60)
    print("Assembly Constituency Page Generator")
    print("=" * 60)
    
    # Load template
    print("\n[1/4] Loading template...")
    template = load_template()
    if not template:
        return
    print("✓ Template loaded successfully")
    
    # Load assembly data
    print("\n[2/4] Loading assembly data...")
    assemblies = load_assemblies()
    if not assemblies:
        return
    print(f"✓ Loaded {len(assemblies)} assemblies")
    
    # Generate pages
    print("\n[3/4] Generating pages...")
    generated_count = 0
    failed_count = 0
    base_url = 'https://sir-2002.gujrera.com/'
    
    for assembly in assemblies:
        try:
            # Generate page content
            page_content = generate_page(template, assembly, assemblies, base_url)
            
            # Write to file
            output_file = f"{assembly['slug']}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(page_content)
            
            generated_count += 1
            if generated_count % 20 == 0:
                print(f"  Generated {generated_count} pages...")
                
        except Exception as e:
            print(f"  ✗ Error generating {assembly['slug']}.html: {e}")
            failed_count += 1
    
    # Summary
    print("\n[4/4] Generation complete!")
    print("=" * 60)
    print(f"Total assemblies: {len(assemblies)}")
    print(f"Successfully generated: {generated_count}")
    if failed_count > 0:
        print(f"Failed: {failed_count}")
    print("=" * 60)
    print("\nTo regenerate pages with updates:")
    print("  1. Update anand.html (template) if needed")
    print("  2. Update assembly_constituencies.json if needed")
    print("  3. Run: python generate_assembly_pages.py")


if __name__ == '__main__':
    main()

