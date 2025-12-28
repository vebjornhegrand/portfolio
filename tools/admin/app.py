"""Portfolio Admin Tool - Local-only project generator."""

from flask import Flask, render_template, request, jsonify
from pathlib import Path
import sys

# Add parent directory to path to access generator
sys.path.insert(0, str(Path(__file__).parent))
from generator import save_project, list_projects, load_project, delete_project, update_project, git_push

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Project root (two levels up from tools/admin/)
PROJECT_ROOT = Path(__file__).parent.parent.parent


@app.route('/')
def index():
    """Admin UI."""
    return render_template('index.html')


@app.route('/projects', methods=['GET'])
def get_projects():
    """List all projects."""
    try:
        projects = list_projects(PROJECT_ROOT)
        return jsonify({'success': True, 'projects': projects})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/project/<slug>', methods=['GET'])
def get_project(slug):
    """Load project data."""
    try:
        project = load_project(slug, PROJECT_ROOT)
        return jsonify({'success': True, 'project': project})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/project/<slug>', methods=['DELETE'])
def delete_project_route(slug):
    """Delete project."""
    try:
        result = delete_project(slug, PROJECT_ROOT)
        
        # Automatically commit and push to GitHub
        git_result = git_push(PROJECT_ROOT, f'Delete project: {slug}')
        
        return jsonify({
            'success': True, 
            'message': f'Project deleted: {slug}',
            'git': git_result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/project/<slug>', methods=['PUT'])
def update_project_route(slug):
    """Update existing project."""
    try:
        # Extract form data
        data = {
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'category': request.form.get('category', '').strip(),
            'date': request.form.get('date', '').strip(),
            'tools': [t.strip() for t in request.form.get('tools', '').split(',') if t.strip()],
            'overview': request.form.get('overview', '').strip(),
            'takeaways': [t.strip() for t in request.form.get('takeaways', '').split('\n') if t.strip()],
            'visuals': []
        }
        
        # Extract visuals data
        visual_count = int(request.form.get('visual_count', 0))
        for i in range(visual_count):
            caption = request.form.get(f'caption_{i}', '').strip()
            role = request.form.get(f'role_{i}', '').strip()
            if caption and role:
                data['visuals'].append({'caption': caption, 'role': role})
        
        # Extract images (only those that were uploaded)
        images = []
        for i in range(visual_count):
            file_key = f'image_{i}'
            if file_key in request.files:
                file = request.files[file_key]
                if file and file.filename:
                    images.append((file, i))
        
        # For updates, images are optional (keep existing if not uploaded)
        # No validation needed - we'll keep existing images for missing uploads
        
        # Update project
        result = update_project(data, images, slug, PROJECT_ROOT)
        
        # Automatically commit and push to GitHub
        git_result = git_push(PROJECT_ROOT, f'Update project: {data["title"]}')
        
        return jsonify({
            'success': True,
            'message': f'Project updated: {result["slug"]}',
            'slug_changed': result['slug_changed'],
            'new_slug': result['slug'],
            'git': git_result
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@app.route('/generate', methods=['POST'])
def generate():
    """Generate project files from form data."""
    try:
        # Extract form data
        data = {
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'category': request.form.get('category', '').strip(),
            'date': request.form.get('date', '').strip(),
            'tools': [t.strip() for t in request.form.get('tools', '').split(',') if t.strip()],
            'overview': request.form.get('overview', '').strip(),
            'takeaways': [t.strip() for t in request.form.get('takeaways', '').split('\n') if t.strip()],
            'visuals': []
        }
        
        # Extract visuals data (captions + roles)
        visual_count = int(request.form.get('visual_count', 0))
        for i in range(visual_count):
            caption = request.form.get(f'caption_{i}', '').strip()
            role = request.form.get(f'role_{i}', '').strip()
            if caption and role:
                data['visuals'].append({'caption': caption, 'role': role})
        
        # Extract images
        images = []
        for i in range(visual_count):
            file_key = f'image_{i}'
            if file_key in request.files:
                file = request.files[file_key]
                if file and file.filename:
                    images.append((file, i))
        
        # Validate image count matches visual count
        if len(images) != len(data['visuals']):
            return jsonify({
                'success': False,
                'error': f'Image count mismatch: {len(images)} images, {len(data["visuals"])} captions'
            }), 400
        
        # Generate project
        result = save_project(data, images, PROJECT_ROOT)
        
        # Automatically commit and push to GitHub
        git_result = git_push(PROJECT_ROOT, f'Add project: {data["title"]}')
        
        return jsonify({
            'success': True,
            'message': f'Project created: {result["slug"]}',
            'files': {
                'markdown': result['markdown_file'],
                'images': result['images']
            },
            'url': result['url'],
            'git': git_result
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Portfolio Admin Tool")
    print("="*60)
    print(f"Project root: {PROJECT_ROOT}")
    print("Open: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)

