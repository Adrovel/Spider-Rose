# Spider Rose Stacks and Tools

Version: 0.1.0  
Status: Phase 1 scope locked  
Last updated: 2026-06-01

## Stack Summary

| Layer | Tool | Why |
|---|---|---|
| CLI | Typer | clean Python CLI with nested commands |
| Terminal UI | Rich | readable tables and status output |
| Runtime | Python single-agent runner | smallest useful terminal MVP |
| Agent format | Markdown | editable, git-friendly, readable |
| Local app server | FastAPI | simple local server for the visual agent editor |
| Visual UI | Built-in HTML/CSS/JS | no frontend build step for Phase 1 |
| Storage | local Markdown and TOML files | MVP stays transparent and file-native |
| Testing | pytest | fast CLI and parser tests |

## CLI Names

- Canonical command: `spiderrose`

## Packaging

The project is packaged with `pyproject.toml` and exposes console scripts. Users should eventually install it with:

```bash
pipx install spider-rose
```

For local development:

```bash
pip install -e ".[dev]"
```

## Deferred Tools

- LangGraph runtime execution
- React Flow UI implementation
- SQLite run database
- MCP support
- tool marketplace
- cloud deployment
