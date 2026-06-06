# Google Careers Teaching Scratch

Version: 0.1.0  
Status: Unapproved teaching scratch  
Last updated: 2026-06-05

Purpose: preserve earlier Google Careers scraper scaffold as learning material for Joel and Mukthar.

## Boundary

These files are not approved implementation.

They were moved out of `src/` and `tests/` so they do not define Spider Rose runtime behavior or test coverage.

Use them only to discuss:

- what a Web Scraper block might need internally
- why block messages should use JSON
- why stored records should use JSONL
- what should be simplified before implementation

## Files

- `google_careers.py` — early parser/scraper sketch
- `tool_runner.py` — early sketch of wiring a tool from an agent definition
- `test_google_careers.py` — early parser test sketch

## Current Product Direction

The approved teaching workflow is:

```text
[Web Scraper: Google Careers]
  -> [Store: Job Results]
```

Visible Web Scraper fields:

- `site`
- `scrape_description`

Implementation still requires atomic-plan approval from Joel and Mukthar.
