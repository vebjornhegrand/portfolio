"""Portfolio project generator - creates Markdown files and organizes images."""

import os
import re
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


def slugify(text):
    """Convert title to URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


def validate_project_data(data):
    """Validate required fields."""
    required = ['title', 'description', 'category', 'date', 'overview', 'takeaways']
    missing = [f for f in required if not data.get(f)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    
    if not data.get('visuals'):
        raise ValueError("At least one visual with caption is required")
    
    # Validate date format
    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        raise ValueError("Date must be YYYY-MM-DD format")


def generate_front_matter(data, slug):
    """Generate YAML front matter."""
    tools_str = ', '.join([f'"{t}"' for t in data['tools']]) if data.get('tools') else ''
    
    return f"""---
layout: project
title: "{data['title']}"
description: "{data['description']}"
hero_image: /assets/images/projects/{slug}/hero.png
tools: [{tools_str}]
category: "{data['category']}"
date: {data['date']}
---"""


def generate_visuals_section(visuals, slug):
    """Generate Key Visuals section with <figure> blocks.
    
    Note: First visual (index 0) is the hero image and is NOT included here.
    Only visuals starting from index 1 are included in Key Visuals section.
    """
    figures = []
    # Skip first visual (it's the hero, which appears separately at top of page)
    for i, visual in enumerate(visuals[1:], start=1):
        filename = f"visual-{i}.png"
        caption = visual['caption']
        role = visual['role']
        
        figures.append(f'''<figure class="project-visual">
  <img src="/assets/images/projects/{slug}/{filename}" alt="{caption}">
  <figcaption><strong>{role}:</strong> {caption}</figcaption>
</figure>''')
    
    return '\n\n'.join(figures)


def generate_takeaways_section(takeaways):
    """Generate Key Takeaways list with proper class."""
    items = [f"  <li>{t.strip()}</li>" for t in takeaways if t.strip()]
    return '<ul class="project-takeaways">\n' + '\n'.join(items) + '\n</ul>'


def generate_markdown(data, slug):
    """Generate complete Markdown file content."""
    front_matter = generate_front_matter(data, slug)
    visuals = generate_visuals_section(data['visuals'], slug)
    takeaways = generate_takeaways_section(data['takeaways'])
    
    return f"""{front_matter}

## Overview
{data['overview'].strip()}

## Key Visuals

{visuals}

## Key Takeaways
{takeaways}
"""


def save_project(data, images, project_root):
    """
    Create project files and folders.
    
    Args:
        data: Project metadata and content
        images: List of (file_storage, index) tuples
        project_root: Path to ProjectPortfolio root
    
    Returns:
        dict with status and created files
    """
    # Validate
    validate_project_data(data)
    
    slug = slugify(data['title'])
    
    # Create paths
    project_root = Path(project_root)
    markdown_file = project_root / '_projects' / f'{slug}.md'
    image_dir = project_root / 'assets' / 'images' / 'projects' / slug
    
    # Check if project exists
    if markdown_file.exists():
        raise ValueError(f"Project '{slug}' already exists")
    
    # Create image directory
    image_dir.mkdir(parents=True, exist_ok=True)
    
    # Save images (first is hero.png, rest are visual-N.png)
    saved_images = []
    for idx, (file_storage, original_idx) in enumerate(images):
        if idx == 0:
            # First image is hero.png
            filename = 'hero.png'
        else:
            # Rest are visual-{idx}.png (visual-1, visual-2, etc.)
            filename = f'visual-{idx}.png'
        
        filepath = image_dir / filename
        file_storage.save(str(filepath))
        saved_images.append(str(filepath))
    
    # Generate and save markdown
    markdown_content = generate_markdown(data, slug)
    markdown_file.write_text(markdown_content)
    
    return {
        'slug': slug,
        'markdown_file': str(markdown_file),
        'images': saved_images,
        'url': f'/projects/{slug}/'
    }


def list_projects(project_root):
    """List all existing projects."""
    project_root = Path(project_root)
    projects_dir = project_root / '_projects'
    
    projects = []
    for md_file in projects_dir.glob('*.md'):
        try:
            content = md_file.read_text()
            # Extract front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    front_matter = parts[1]
                    title = re.search(r'title:\s*"([^"]+)"', front_matter)
                    date = re.search(r'date:\s*(\S+)', front_matter)
                    category = re.search(r'category:\s*"([^"]+)"', front_matter)
                    
                    projects.append({
                        'slug': md_file.stem,
                        'title': title.group(1) if title else md_file.stem,
                        'date': date.group(1) if date else '',
                        'category': category.group(1) if category else ''
                    })
        except Exception:
            continue
    
    # Sort by date, newest first
    projects.sort(key=lambda x: x['date'], reverse=True)
    return projects


def load_project(slug, project_root):
    """Load existing project data."""
    project_root = Path(project_root)
    markdown_file = project_root / '_projects' / f'{slug}.md'
    image_dir = project_root / 'assets' / 'images' / 'projects' / slug
    
    if not markdown_file.exists():
        raise ValueError(f"Project '{slug}' not found")
    
    content = markdown_file.read_text()
    
    # Parse front matter
    if not content.startswith('---'):
        raise ValueError("Invalid project file format")
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        raise ValueError("Invalid project file format")
    
    front_matter = parts[1]
    body = parts[2].strip()
    
    # Extract fields
    title = re.search(r'title:\s*"([^"]+)"', front_matter)
    description = re.search(r'description:\s*"([^"]+)"', front_matter)
    category = re.search(r'category:\s*"([^"]+)"', front_matter)
    date = re.search(r'date:\s*(\S+)', front_matter)
    tools_match = re.search(r'tools:\s*\[([^\]]*)\]', front_matter)
    
    tools = []
    if tools_match:
        tools_str = tools_match.group(1)
        tools = [t.strip().strip('"') for t in tools_str.split(',') if t.strip()]
    
    # Parse body sections
    overview = ''
    takeaways = []
    visuals = []
    
    # Extract Overview
    overview_match = re.search(r'## Overview\s*\n(.*?)(?=##|\Z)', body, re.DOTALL)
    if overview_match:
        overview = overview_match.group(1).strip()
    
    # Extract Key Takeaways
    takeaways_match = re.search(r'## Key Takeaways\s*\n(.*?)(?=##|\Z)', body, re.DOTALL)
    if takeaways_match:
        takeaways_text = takeaways_match.group(1).strip()
        # Try HTML format first
        li_items = re.findall(r'<li>(.*?)</li>', takeaways_text, re.DOTALL)
        if li_items:
            takeaways = [item.strip() for item in li_items]
        else:
            # Fallback to markdown format
            takeaways = [line.lstrip('- ').strip() for line in takeaways_text.split('\n') if line.strip().startswith('-')]
    
    # Extract visuals from Key Visuals section
    visuals_section = re.search(r'## Key Visuals\s*\n(.*?)(?=##|\Z)', body, re.DOTALL)
    if visuals_section:
        # Try with <strong> tags first
        figures = re.findall(r'<figure class="project-visual">\s*<img src="([^"]+)" alt="([^"]*)">\s*<figcaption><strong>([^:]+):</strong>\s*([^<]+)</figcaption>', visuals_section.group(1), re.DOTALL)
        if not figures:
            # Fallback to without <strong> tags
            figures = re.findall(r'<figure class="project-visual">\s*<img src="([^"]+)" alt="([^"]*)">\s*<figcaption>([^:]+):\s*([^<]+)</figcaption>', visuals_section.group(1), re.DOTALL)
        
        for img_src, alt, role, caption in figures:
            filename = Path(img_src).name
            visuals.append({
                'filename': filename,
                'role': role.strip(),
                'caption': caption.strip()
            })
    
    # Build complete visuals list: hero + visual-N.png images
    synced_visuals = []
    existing_images = []
    
    # First, add hero image (position 0)
    hero_path = image_dir / 'hero.png'
    if hero_path.exists():
        synced_visuals.append({
            'filename': 'hero.png',
            'role': 'Result',
            'caption': title.group(1) if title else 'Hero image'
        })
        existing_images.append('hero.png')
    
    # Then add visual-N.png images from Key Visuals section
    if image_dir.exists():
        visual_files = sorted(image_dir.glob('visual-*.png'))
        for img_path in visual_files:
            img_name = img_path.name
            existing_images.append(img_name)
            # Try to find matching visual by filename from Key Visuals section
            matching_visual = None
            for visual in visuals:
                if visual['filename'] == img_name:
                    matching_visual = visual
                    break
            
            if matching_visual:
                synced_visuals.append(matching_visual)
            else:
                # Image exists but no caption found, create placeholder
                synced_visuals.append({
                    'filename': img_name,
                    'role': 'Result',
                    'caption': 'Image description'
                })
    
    return {
        'slug': slug,
        'title': title.group(1) if title else '',
        'description': description.group(1) if description else '',
        'category': category.group(1) if category else '',
        'date': date.group(1) if date else '',
        'tools': tools,
        'overview': overview,
        'takeaways': takeaways,
        'visuals': synced_visuals,
        'existing_images': existing_images
    }


def delete_project(slug, project_root):
    """Delete project and its images."""
    project_root = Path(project_root)
    markdown_file = project_root / '_projects' / f'{slug}.md'
    image_dir = project_root / 'assets' / 'images' / 'projects' / slug
    
    if not markdown_file.exists():
        raise ValueError(f"Project '{slug}' not found")
    
    # Delete markdown file
    markdown_file.unlink()
    
    # Delete image directory
    if image_dir.exists():
        shutil.rmtree(image_dir)
    
    return {'slug': slug, 'deleted': True}


def update_project(data, images, old_slug, project_root, keep_existing_images=None):
    """Update existing project.
    
    Args:
        data: Project metadata and content
        images: List of (file_storage, index) tuples for new images
        old_slug: Current project slug
        project_root: Path to project root
        keep_existing_images: List of existing image filenames to preserve
    """
    project_root = Path(project_root)
    old_markdown_file = project_root / '_projects' / f'{old_slug}.md'
    old_image_dir = project_root / 'assets' / 'images' / 'projects' / old_slug
    
    if not old_markdown_file.exists():
        raise ValueError(f"Project '{old_slug}' not found")
    
    # Validate
    validate_project_data(data)
    
    new_slug = slugify(data['title'])
    
    # If slug changed, check new slug doesn't exist
    if new_slug != old_slug:
        new_markdown_file = project_root / '_projects' / f'{new_slug}.md'
        if new_markdown_file.exists():
            raise ValueError(f"Cannot rename: project '{new_slug}' already exists")
    
    # Create new image directory
    new_image_dir = project_root / 'assets' / 'images' / 'projects' / new_slug
    new_image_dir.mkdir(parents=True, exist_ok=True)
    
    # Process images: save new ones OR copy existing ones
    saved_images = []
    uploaded_indices = {original_idx for _, original_idx in images}
    
    for idx in range(len(data['visuals'])):
        if idx == 0:
            # First image is hero.png
            filename = 'hero.png'
        else:
            # Rest are visual-{idx}.png (visual-1, visual-2, etc.)
            filename = f'visual-{idx}.png'
        
        filepath = new_image_dir / filename
        
        # Check if user uploaded a new image for this position
        if idx in uploaded_indices:
            # Find the uploaded file for this index
            for file_storage, original_idx in images:
                if original_idx == idx:
                    file_storage.save(str(filepath))
                    saved_images.append(str(filepath))
                    break
        else:
            # No new upload, try to keep existing image
            old_image_path = old_image_dir / filename
            if old_image_path.exists():
                # Only copy if source and destination are different
                if old_image_path != filepath:
                    shutil.copy2(old_image_path, filepath)
                saved_images.append(str(filepath))
    
    # Delete old files
    old_markdown_file.unlink()
    if old_image_dir.exists() and old_image_dir != new_image_dir:
        shutil.rmtree(old_image_dir)
    
    # Generate and save markdown
    markdown_content = generate_markdown(data, new_slug)
    new_markdown_file = project_root / '_projects' / f'{new_slug}.md'
    new_markdown_file.write_text(markdown_content)
    
    return {
        'slug': new_slug,
        'old_slug': old_slug,
        'slug_changed': new_slug != old_slug,
        'markdown_file': str(new_markdown_file),
        'images': saved_images
    }


def git_push(project_root, message):
    """Commit and push changes to GitHub.
    
    Args:
        project_root: Path to project root directory
        message: Commit message
    
    Returns:
        dict with success status and message
    """
    try:
        project_root = Path(project_root)
        
        # Add all changes
        subprocess.run(['git', 'add', '-A'], cwd=project_root, check=True, capture_output=True)
        
        # Commit
        result = subprocess.run(
            ['git', 'commit', '-m', message], 
            cwd=project_root, 
            check=True, 
            capture_output=True,
            text=True
        )
        
        # Push
        subprocess.run(['git', 'push'], cwd=project_root, check=True, capture_output=True)
        
        return {
            'success': True,
            'message': 'Changes committed and pushed to GitHub'
        }
    except subprocess.CalledProcessError as e:
        # If commit fails because there are no changes, that's okay
        if 'nothing to commit' in str(e.stderr):
            return {
                'success': True,
                'message': 'No changes to commit'
            }
        return {
            'success': False,
            'message': f'Git error: {e.stderr}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to push: {str(e)}'
        }

