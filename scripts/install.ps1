# Install Ruby dependencies
# Run from project root: .\scripts\install.ps1

Write-Host "Installing Ruby dependencies..." -ForegroundColor Cyan

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
    
    if (Add-RubyToPath) {
        if (-not (Get-Command bundle -ErrorAction SilentlyContinue)) {
            Write-Host "Ruby found but Bundler not installed. Installing Bundler..." -ForegroundColor Yellow
            gem install bundler
        }
    } else {
        Write-Host "ERROR: Ruby not found!" -ForegroundColor Red
        Write-Host "Please install Ruby first:" -ForegroundColor Yellow
        Write-Host "  winget install RubyInstallerTeam.RubyWithDevKit.3.3" -ForegroundColor Yellow
        exit 1
    }
}

# Install dependencies
bundle install

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nDependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "`nFailed to install dependencies" -ForegroundColor Red
    exit 1
}
