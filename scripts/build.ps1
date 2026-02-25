# Build Jekyll site for production
# Run from project root: .\scripts\build.ps1

Write-Host "Building Jekyll site for production..." -ForegroundColor Cyan

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
        Write-Host "ERROR: Ruby not found!" -ForegroundColor Red
        Write-Host "Please install Ruby first:" -ForegroundColor Yellow
        Write-Host "  winget install RubyInstallerTeam.RubyWithDevKit.3.3" -ForegroundColor Yellow
        exit 1
    }
}

# Build site
bundle exec jekyll build

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSite built successfully in _site/" -ForegroundColor Green
} else {
    Write-Host "`nBuild failed" -ForegroundColor Red
    exit 1
}
