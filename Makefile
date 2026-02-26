# CO3DEX Makefile
# Quick commands for development

.PHONY: help install serve build clean

help:
	@echo "CO3DEX Development Commands"
	@echo "=========================="
	@echo "make install  - Install Ruby dependencies"
	@echo "make serve    - Start Jekyll development server with LiveReload"
	@echo "make build    - Build the site for production"
	@echo "make clean    - Clean build artifacts"
	@echo ""
	@echo "Or use PowerShell scripts in ./scripts/"

install:
	bundle install

serve:
	bundle exec jekyll serve --livereload

build:
	bundle exec jekyll build

clean:
	bundle exec jekyll clean
	rm -rf _site .jekyll-cache .jekyll-metadata
