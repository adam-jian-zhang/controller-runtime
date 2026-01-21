# Controller-Runtime Documentation Site

This is a Hugo-based static site for the controller-runtime documentation.

## Features

- ✅ **Light/Dark Mode Toggle**: Switch between light and dark themes
- ✅ **Collapsible Menu**: Collapse sidebar to icon bar with tooltips
- ✅ **Resizable Panels**: Drag the divider to adjust sidebar width
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **Mermaid Diagrams**: Converted to SVG for fast loading
- ✅ **Code Syntax Highlighting**: Beautiful code blocks
- ✅ **Copy Code Button**: Easy code copying
- ✅ **Table of Contents**: Auto-generated for long pages
- ✅ **Smooth Navigation**: Smooth scrolling and transitions

## Quick Start

### Prerequisites

- Hugo (v0.120.0+)
- Python 3
- mmdc (Mermaid CLI) - optional, for diagram conversion

### Build and Serve

```bash
# Process documentation and build site
make build

# Serve locally on port 9005
make serve

# Or use Hugo directly
hugo server -s . -p 9005
```

### Docker

```bash
# Build Docker image
make docker-build

# Run container
make docker-run

# Stop container
make docker-stop
```

The site will be available at http://localhost:9005

## Directory Structure

```
site/
├── content/          # Processed markdown content
├── static/           # Static assets (CSS, JS, images)
├── themes/           # Hugo theme
│   └── controller-runtime-docs/
│       ├── layouts/  # HTML templates
│       └── static/   # Theme assets
├── scripts/          # Processing scripts
├── public/           # Generated site (after build)
├── Makefile          # Build automation
├── Dockerfile        # Container image
└── hugo.toml         # Hugo configuration
```

## Makefile Targets

- `make help` - Show available targets
- `make process` - Process markdown files
- `make build` - Build the Hugo site
- `make serve` - Serve site locally
- `make clean` - Clean generated files
- `make docker-build` - Build Docker image
- `make docker-run` - Run Docker container
- `make docker-stop` - Stop Docker container
- `make all` - Clean and build everything

## Theme Features

### Light/Dark Mode

Click the moon/sun icon in the sidebar header to toggle between light and dark modes. The preference is saved in localStorage.

### Collapsible Menu

Click the hamburger menu icon to collapse the sidebar to an icon bar. On mobile, the menu slides in from the left.

### Resizable Sidebar

Drag the vertical divider between the sidebar and content to adjust the sidebar width. The width is saved in localStorage.

### Code Blocks

Code blocks have syntax highlighting and a "Copy" button that appears on hover.

### Mermaid Diagrams

Mermaid diagrams are converted to SVG files for fast loading. The SVG filename is based on a hash of the diagram content.

## Customization

### Colors

Edit `themes/controller-runtime-docs/static/css/style.css` and modify the CSS variables in `:root` and `[data-theme="dark"]`.

### Layout

Edit templates in `themes/controller-runtime-docs/layouts/`.

### Navigation

Edit `hugo.toml` to modify the main navigation menu.

## Processing Documentation

The `scripts/process.py` script:
1. Reads markdown files from `../docs/`
2. Extracts titles and creates Hugo front matter
3. Converts mermaid diagrams to SVG (optional)
4. Outputs to `content/docs/`

## Troubleshooting

### Site not building

- Check Hugo version: `hugo version`
- Ensure content directory exists
- Check for syntax errors in markdown

### Diagrams not showing

- Ensure mmdc is installed: `npm install -g @mermaid-js/mermaid-cli`
- Check `static/images/diagrams/` for SVG files
- Verify mermaid syntax in markdown

### Styles not loading

- Run `hugo` to regenerate the site
- Check browser console for errors
- Clear browser cache

## License

Apache License 2.0 - Same as controller-runtime project
