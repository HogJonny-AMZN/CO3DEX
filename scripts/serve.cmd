@echo off
REM Start Jekyll development server with LiveReload
REM Run from project root: scripts\serve.cmd

echo Starting Jekyll development server...
bundle exec jekyll serve --livereload

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start Jekyll server
    echo Make sure Ruby and Bundler are installed
    pause
)
