# Fundamental Blocks Primer

Version: 0.1.0  
Status: Product learning note  
Last updated: 2026-06-04

Purpose: explain the reusable block idea so Joel and Mukthar do not design every workflow as a new custom agent.

## Core Idea

Spider Rose should feel like Lego for workflows.

A workflow is made from reusable fundamental blocks. Each block has a clear responsibility, inputs, outputs, and connectors.

## Fundamental Blocks

| Block | Responsibility | Example input | Example output |
|---|---|---|---|
| Input | Accept user-provided text, URL, handle, image, or file | `software engineer in India` | normalized input |
| Website Source | Represents a target website or page | Google Careers URL | source config |
| Web Scraper | Fetch and extract data from configured websites | source config + query | raw or structured records |
| Extractor | Convert raw content into clean fields | raw page text | title, location, date |
| Store/RAG | Save output for search or later use | structured records | stored collection |
| Scheduler | Decide when a workflow runs | daily at 9 AM | run trigger |
| Formatter | Turn records into readable messages | stored records | message text |
| WhatsApp Sender | Send output to Joel over WhatsApp | message text | delivery result |
| Agent | Reason, summarize, decide, or transform | records + task | summary or decision |

## Product Rule

Specific sites should usually be inputs or configuration, not separate block types.

Example:

- Good: `Web Scraper` block with `site = Google Careers`
- Avoid by default: one permanent `Google Careers Scraper` block unless the site needs special handling that cannot fit the generic scraper

## Data Format Rule

Use different formats for different jobs:

| Use | Format | Reason |
|---|---|---|
| Human-authored agent/block definition | Markdown | readable, editable, good for instructions |
| Project config | TOML | already used by `spider-rose.toml` |
| Block-to-block message | JSON | native to Python and JavaScript, easy to validate, good for connectors |
| Stored workflow records | JSONL | append-only, inspectable, easy to deduplicate |
| Human report | Markdown | readable final output |

Do not use Markdown for block-to-block data. Markdown is too loose for reliable parsing, deduplication, and validation.

Do not use YAML for runtime messages in v0. YAML is useful for human-authored config, but JSON is safer for live block communication because it is native in Python/JavaScript and has fewer parsing surprises.

## Why This Matters

This keeps Spider Rose small and composable.

The same Web Scraper block can support:

- Google Careers job search
- public Instagram profile details
- product pages
- company career pages

The workflow changes by changing inputs, extractors, and connectors instead of inventing a new block every time.
