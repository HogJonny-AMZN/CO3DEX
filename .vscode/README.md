# VSCode Workspace Configuration

This folder contains VSCode-specific settings for the CO3DEX Jekyll site.

## Quick Start

### First Time Setup
1. **Install Ruby**: 
   ```powershell
   winget install RubyInstallerTeam.RubyWithDevKit.3.3
   ```
   (Restart your terminal after installation)

2. **Install Dependencies**: 
   - Press `Ctrl+Shift+P`
   - Type "Tasks: Run Task"
   - Select "Jekyll: Install Dependencies"
   
   Or run directly:
   ```powershell
   .\scripts\install.ps1
   ```

### Daily Development

**Start Dev Server**:
- Press `Ctrl+Shift+P` → "Tasks: Run Task" → "Jekyll: Serve (Dev Server)"
- Or: `.\scripts\serve.ps1`
- Visit: http://localhost:4000

**Build for Production**:
- Press `Ctrl+Shift+B` (default build task)
- Or: `.\scripts\build.ps1`

## Available Tasks

Access via `Ctrl+Shift+P` → "Tasks: Run Task":

- **Jekyll: Install Dependencies** - Install/update Ruby gems
- **Jekyll: Serve (Dev Server)** - Start local server with LiveReload
- **Jekyll: Build** - Build production site (also `Ctrl+Shift+B`)
- **Jekyll: Clean** - Remove build artifacts

## Recommended Extensions

Install these for the best experience (VSCode will prompt you):

- **Markdown All in One** - Enhanced markdown editing
- **Shopify Liquid** - Syntax highlighting for Jekyll templates
- **YAML** - Config file support
- **Front Matter CMS** - Visual CMS for managing content
- **GitLens** - Git integration

## Keyboard Shortcuts

- `Ctrl+Shift+B` - Build site
- `Ctrl+Shift+P` - Command palette (access tasks)
- `Ctrl+K Ctrl+O` - Open folder
- `Ctrl+` ` - Toggle terminal

## File Structure

```
.vscode/
├── tasks.json       - Build & serve tasks
├── settings.json    - Workspace settings
├── extensions.json  - Recommended extensions
└── launch.json      - Debug configurations
```

## Troubleshooting

**"Ruby not found" error**:
1. Install Ruby via winget (see above)
2. Restart VSCode
3. Run install task again

**"bundle not found"**:
```powershell
gem install bundler
```

**Port 4000 already in use**:
Kill the existing Jekyll process or use a different port:
```powershell
bundle exec jekyll serve --port 4001
```

## Additional Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Project README](../README.md)
- [Installation Guide](../install.md)
