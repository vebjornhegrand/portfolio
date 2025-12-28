# Architecture

## System Overview
Static Jekyll site for visual-first engineering portfolio. Projects are Markdown files in a collection, rendered using two layouts. Homepage displays project cards in a grid. Single CSS file enforces visual consistency.

## Dataflow
```
_projects/*.md → Jekyll collection → index.html (grid) or project.html (page)
                     ↓
                 default.html (base template)
                     ↓
                 main.css (styling)
```

## Module Map
- `_config.yml`: Jekyll configuration, collection setup
- `_layouts/default.html`: Base HTML structure (header, footer, CSS)
- `_layouts/project.html`: Project page template (hero, content, tools)
- `index.html`: Homepage with project card grid loop
- `assets/css/main.css`: All styles, CSS variables for consistency
- `_projects/`: One Markdown file per project (front matter + content)
- `assets/images/projects/`: Per-project image folders

## Key Invariants
- Every project has: title, description, hero_image, tools, category, date
- All project pages render with identical structure (hero → overview → visuals → takeaways → tools)
- Visual hierarchy enforced by typography scale and spacing system (see UI_SYSTEM.md)
- Images must use `<figure class="project-visual">` with semantic captions
- Section headings are uppercase + tracked (structural markers)
- Description uses primary color with accent bottom border (contract emphasis)
- Grid layout responsive (3 columns → 1 on mobile)
- No source code displayed in UI
- Images organized: `/assets/images/projects/{project-slug}/`

## Main Entrypoints
- `index.html`: Loops through `site.projects`, sorted by date (desc), renders cards
- `_layouts/project.html`: Renders front matter + Markdown content into standard sections
- Adding a project: drop `.md` file into `_projects/`, add images to `assets/images/projects/`

## Scaling
Add project = add one Markdown file. No manual updates to homepage or config needed.

