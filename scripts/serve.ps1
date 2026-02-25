# Start Jekyll development server with LiveReload
# Run from project root: .\scripts\serve.ps1

Write-Host "Starting Jekyll development server..." -ForegroundColor Cyan

# Function to find and add Ruby to PATH
function Add-RubyToPath {
    # Common Ruby installation paths
    $rubyPaths = @(
        "C:\Ruby33-x64\bin",
        "C:\Ruby32-x64\bin",
        "C:\Ruby31-x64\bin",
        "C:\Ruby30-x64\bin",
        "$env:USERPROFILE\.rbenv\shims",
        "$env:ProgramFiles\Ruby\Ruby33-x64\bin",
        "$env:ProgramFiles\Ruby\Ruby32-x64\bin"
    )
    
    foreach ($path in $rubyPaths) {
        if (Test-Path $path) {
            Write-Host "Found Ruby at: $path" -ForegroundColor Green
            $env:Path = "$path;$env:Path"
            return $true
        }
    }
    return $false
}

# Check if bundle is available
if (-not (Get-Command bundle -ErrorAction SilentlyContinue)) {
    Write-Host "Bundler not in PATH, searching for Ruby installation..." -ForegroundColor Yellow
    
    if (Add-RubyToPath) {
        # Check again after adding to PATH
        if (-not (Get-Command bundle -ErrorAction SilentlyContinue)) {
            Write-Host "Ruby found but Bundler not installed. Installing Bundler..." -ForegroundColor Yellow
            gem install bundler
        }
    } else {
        Write-Host "ERROR: Ruby not found!" -ForegroundColor Red
        Write-Host "Please install Ruby and Bundler first:" -ForegroundColor Yellow
        Write-Host "  winget install RubyInstallerTeam.RubyWithDevKit.3.3" -ForegroundColor Yellow
        exit 1
    }
}

# Verify bundle is now available
if (-not (Get-Command bundle -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Still cannot find Bundler!" -ForegroundColor Red
    exit 1
}

Write-Host "Ruby environment configured!" -ForegroundColor Green
Write-Host "Starting server at http://localhost:4000 with LiveReload..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

# Run Jekyll server
bundle exec jekyll serve --livereload

# If server stops, show message
Write-Host "`nJekyll server stopped." -ForegroundColor Yellow
