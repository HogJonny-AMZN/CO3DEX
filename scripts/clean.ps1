# Clean Jekyll build artifacts
# Run from project root: .\scripts\clean.ps1

Write-Host "Cleaning Jekyll build artifacts..." -ForegroundColor Cyan

# Function to find and add Ruby to PATH
function Add-RubyToPath {
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
    
    if (-not (Add-RubyToPath)) {
        Write-Host "WARNING: Ruby not found, cleaning manually..." -ForegroundColor Yellow
    }
}

# Try Jekyll clean if available, otherwise manual cleanup
if (Get-Command bundle -ErrorAction SilentlyContinue) {
    bundle exec jekyll clean
    Write-Host "Jekyll clean completed" -ForegroundColor Green
} else {
    # Manual cleanup
    if (Test-Path "_site") {
        Remove-Item -Recurse -Force "_site"
        Write-Host "Removed _site/" -ForegroundColor Green
    }
    if (Test-Path ".jekyll-cache") {
        Remove-Item -Recurse -Force ".jekyll-cache"
        Write-Host "Removed .jekyll-cache/" -ForegroundColor Green
    }
    if (Test-Path ".jekyll-metadata") {
        Remove-Item -Force ".jekyll-metadata"
        Write-Host "Removed .jekyll-metadata" -ForegroundColor Green
    }
}

Write-Host "`nCleanup complete!" -ForegroundColor Green
