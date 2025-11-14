# How to View Technical Documentation

The technical documentation includes Mermaid diagrams that need to be rendered to be visible.

## Option 1: View HTML Version (Recommended)

1. Open `TECHNICAL_DOCUMENTATION.html` in any web browser
2. The Mermaid diagrams will be automatically rendered
3. You can print to PDF from the browser (File → Print → Save as PDF)

## Option 2: View Markdown with Mermaid Support

### Online Viewers:
- **GitHub**: Push to GitHub and view - GitHub renders Mermaid diagrams
- **GitLab**: Similar to GitHub, renders Mermaid
- **Markdown Preview Enhanced** (VS Code extension)
- **Obsidian**: Markdown editor with Mermaid support

### VS Code:
1. Install "Markdown Preview Enhanced" extension
2. Open `TECHNICAL_DOCUMENTATION.md`
3. Right-click → "Markdown Preview Enhanced: Open Preview"
4. Diagrams will be rendered

## Option 3: Convert to PDF with Diagrams

### Using Mermaid CLI:
```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Convert to PDF (requires additional setup)
mmdc -i TECHNICAL_DOCUMENTATION.md -o TECHNICAL_DOCUMENTATION.pdf
```

### Using Pandoc + Mermaid Filter:
```bash
# Install pandoc and mermaid-filter
pandoc TECHNICAL_DOCUMENTATION.md -o TECHNICAL_DOCUMENTATION.pdf \
  --filter mermaid-filter
```

### Using Online Tools:
1. Go to https://mermaid.live/
2. Copy Mermaid code blocks from the markdown
3. Export as PNG/SVG
4. Insert into PDF

## Option 4: Use Documentation Generators

### MkDocs with Mermaid Plugin:
```bash
pip install mkdocs mkdocs-material
pip install mkdocs-mermaid2-plugin
# Configure mkdocs.yml and build
mkdocs build
```

### Docusaurus:
- Supports Mermaid out of the box
- Great for technical documentation websites

## Quick Reference

**File Locations:**
- `TECHNICAL_DOCUMENTATION.md` - Markdown source with Mermaid diagrams
- `TECHNICAL_DOCUMENTATION.html` - HTML version (open in browser)

**Diagram Types Included:**
- System Architecture Diagrams
- Workflow Diagrams
- Data Flow Diagrams
- Database Schema (ERD)
- Sequence Diagrams
- Component Diagrams
- Security Architecture

**Total Diagrams:** 15+ Mermaid diagrams covering all aspects of the system

