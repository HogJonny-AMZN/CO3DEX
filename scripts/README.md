# CO3DEX Development Scripts

Quick commands to manage the Jekyll site.

## Usage

### PowerShell (Recommended for Windows)

```powershell
# Install dependencies
.\scripts\install.ps1

# Start development server with LiveReload
.\scripts\serve.ps1

# Build for production
.\scripts\build.ps1

# Clean build artifacts
.\scripts\clean.ps1
```

### Batch Files (Windows CMD)

```cmd
REM Start development server
scripts\serve.cmd
```

### Makefile (Linux/macOS/Windows with Make)

```bash
# Show available commands
make help

# Install dependencies
make install

# Start development server
make serve

# Build for production
make build

# Clean build artifacts
make clean
```

## Prerequisites

- Ruby 3.3+ with DevKit
- Bundler gem

Install with:
```powershell
winget install RubyInstallerTeam.RubyWithDevKit.3.3
gem install bundler
```

## Development Workflow

1. **First time setup:**
   ```powershell
   .\scripts\install.ps1
   ```

2. **Start local server:**
   ```powershell
   .\scripts\serve.ps1
   ```
   Visit http://localhost:4000

3. **Build for deployment:**
   ```powershell
   .\scripts\build.ps1
   ```
   Output in `_site/` folder

## Notes

- Config changes (`_config.yml`) require server restart
- LiveReload auto-refreshes browser on file changes
- Server runs on http://localhost:4000 by default
