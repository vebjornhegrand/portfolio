# Engineering Portfolio

Visual-first engineering portfolio built with Jekyll for GitHub Pages.

## How to Run Locally

### Initial Setup (Apple Silicon / M1 Macs)
This project requires Homebrew Ruby (arm64), not system Ruby.

```bash
# 1. Install Homebrew Ruby
brew install ruby

# 2. Add Homebrew Ruby to PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"

# 3. Reload shell or source your profile
source ~/.zshrc

# 4. Verify Ruby version (should be 3.x from Homebrew)
ruby -v

# 5. Install Bundler 2+
gem install bundler

# 6. Install dependencies
cd /Users/vebjornhegrand/Desktop/ProjectPortfolio
bundle install

# 7. Serve the site (always use bundle exec)
bundle exec jekyll serve

# Visit http://localhost:4000
```

### Running After Initial Setup
```bash
bundle exec jekyll serve
```

**Important**: Always use `bundle exec jekyll serve`, never `jekyll serve` directly.

## Adding a Project
1. Create a new Markdown file in `_projects/` (e.g., `my-project.md`)
2. Add front matter with required fields:
   ```yaml
   ---
   layout: project
   title: "Project Title"
   description: "One-sentence declaration of what this solves"
   hero_image: /assets/images/projects/my-project/hero.png
   tools: ["Tool1", "Tool2"]
   category: "python"  # or "cad"
   date: 2024-12-24
   ---
   ```
3. Write content following the standard structure:
   - Overview (what, why, context)
   - Key Visuals (use `<figure>` with captions)
   - Key Takeaways (3 bullets)
4. Add images to `/assets/images/projects/my-project/`

**Visual Format:**
```html
<figure class="project-visual">
  <img src="/assets/images/projects/my-project/result.png" alt="Description">
  <figcaption><strong>Result:</strong> What this image shows</figcaption>
</figure>
```

**Takeaways Format:**
```html
<ul class="project-takeaways">
  <li>First major outcome or engineering insight</li>
  <li>Second key result or technical decision made</li>
</ul>
```

Caption prefixes: `Result:`, `Design:`, `Analysis:`, `Process:`

## Project Structure
- `_config.yml`: Site configuration
- `_layouts/`: HTML templates
- `_projects/`: Project Markdown files
- `assets/`: CSS and images
- `index.html`: Homepage

## Deployment
Push to GitHub. Enable GitHub Pages in repository settings (source: main branch, root).

