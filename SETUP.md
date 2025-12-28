# Setup Instructions

## Environment Requirements
- macOS with Apple Silicon (M1/M2/M3)
- Homebrew Ruby (arm64)
- Bundler 2+

## First-Time Setup

### 1. Install Homebrew Ruby
System Ruby (2.6) is incompatible with modern Jekyll on Apple Silicon.

```bash
brew install ruby
```

### 2. Configure Shell PATH
Add Homebrew Ruby to your PATH before system Ruby.

**For zsh (default on macOS):**
```bash
echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

### 3. Verify Ruby Installation
```bash
ruby -v
# Should show: ruby 3.x.x (NOT 2.6.x)

which ruby
# Should show: /opt/homebrew/opt/ruby/bin/ruby
```

### 4. Install Bundler
```bash
gem install bundler
```

Verify Bundler version:
```bash
bundle -v
# Should show: Bundler version 2.x or higher
```

### 5. Install Project Dependencies
```bash
cd /Users/vebjornhegrand/Desktop/ProjectPortfolio
bundle install
```

This installs Jekyll and all dependencies with correct arm64 architecture.

### 6. Run Jekyll
```bash
bundle exec jekyll serve
```

Visit http://localhost:4000

## Common Issues

### Issue: "wrong architecture" or "LoadError"
**Cause:** Gems installed for wrong Ruby version or architecture.

**Solution:**
```bash
# Remove existing gems
rm -rf vendor/bundle
bundle clean --force

# Reinstall with correct Ruby
bundle install
```

### Issue: "Jekyll command not found"
**Cause:** Using system Ruby instead of Homebrew Ruby.

**Solution:**
```bash
# Verify Ruby path
which ruby
# If shows /usr/bin/ruby, PATH is incorrect

# Re-add Homebrew Ruby to PATH
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
```

### Issue: Old Bundler version (1.17)
**Solution:**
```bash
gem update --system
gem install bundler
```

## Daily Workflow

Always use `bundle exec` to ensure correct gem versions:

```bash
# Start development server
bundle exec jekyll serve

# Build site
bundle exec jekyll build
```

## Notes
- Never run `jekyll serve` directly without `bundle exec`
- Never use system Ruby (/usr/bin/ruby) on Apple Silicon
- Gemfile.lock is gitignored to avoid architecture conflicts

