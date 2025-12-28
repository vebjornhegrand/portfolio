# Portfolio Admin Tool

Local-only web UI for generating portfolio projects.

## Setup

```bash
cd tools/admin
pip3 install -r requirements.txt
```

## Usage

```bash
python3 app.py
```

Open http://127.0.0.1:5000

## Workflow

1. Fill in project metadata (title, description, category, date, tools)
2. Write overview and takeaways
3. Add visuals:
   - First image becomes `hero.png`
   - Upload image, select role (Result/Design/Analysis/Process), add caption
   - Add more visuals as needed
4. Click "Generate Project"
5. Files are created:
   - `_projects/<slug>.md`
   - `assets/images/projects/<slug>/`
6. Run `bundle exec jekyll serve` to view

## Output

Generates standard portfolio project files with:
- Correct front matter
- Semantic `<figure>` blocks
- Proper image paths
- Role-prefixed captions

## Notes

- Private tool, not deployed to GitHub Pages
- Writes directly to Jekyll structure
- Validates required fields and formats
- Auto-generates slug from title

