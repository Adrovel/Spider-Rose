# Spider Rose Architecture

Version: 0.1.0  
Status: Working architecture  
Last updated: 2026-06-04

Spider Rose is a local-first workflow workspace with a terminal entry point and a visual execution grid.

## System Summary

```text
CLI
  -> Terminal UI
  -> Project File Manager
  -> Agent Registry
  -> Single-Agent Runtime
  -> Local Visualization Server
  -> Visual Workflow Grid
  -> Canvas Layout And Connector Store
  -> Markdown Agent Files
```

Planned visual workflow model:

```text
Input
  -> Website Source
  -> Web Scraper
  -> Extractor
  -> Store/RAG
  -> Formatter
  -> WhatsApp Sender
```

## MVP Boundaries

Spider Rose Phase 1 supports one definition mode:

| Mode | File | Purpose |
|---|---|---|
| Markdown Agent | `agents/*.md` | beginner-friendly agent definition |

Implementation is atomic-plan gated. LangGraph Python and heavy workflow definitions are not active until Joel and Mukthar approve the relevant plan.

## Data Format Contract

Spider Rose should use format boundaries intentionally:

| Surface | Format | Purpose |
|---|---|---|
| Agent/block definitions | Markdown | human-authored instructions and readable definitions |
| Project config | TOML | local project settings |
| Block messages | JSON | data passed across workflow connectors |
| Stored records/artifacts | JSONL | append-only workflow outputs such as scraped jobs |
| Human reports | Markdown | readable summaries after data is processed |

Runtime block communication should not use Markdown. Markdown remains for human-authored definitions and reports.

YAML is not the v0 runtime-message format. It can be revisited for config-like use cases, but JSON is the default for block-to-block communication.

## Local Project Layout

```text
project/
├── agents/
├── memory/
├── workflow-layout.json
└── spider-rose.toml
```

## Phase 1 Runtime Path

1. `spiderrose` opens the terminal shell.
2. CLI locates `spider-rose.toml`.
3. If the config does not exist, CLI creates a local Spider Rose project.
4. `/run <task>` loads the default Markdown agent from `agents/`.
5. Runtime applies the terminal task to that agent.
6. Result is printed to the terminal.
7. `/visualise` serves an agent editor over the same local files.
8. `/workflow` serves a movable canvas backed by `workflow-layout.json`.
9. The canvas should store visual connector edges that represent workflow data/control flow between blocks.

The visual server should run once per port. If `spiderrose visualise` sees an existing server on the target host/port, it opens that URL instead of starting a second server.

## Canvas Data Model

The canvas stores visual cards now, and should evolve toward workflow blocks and typed flow edges:

```json
{
  "cards": [
    { "id": "input-1", "type": "input", "x": 70, "y": 72 },
    { "id": "scraper-1", "type": "web-scraper", "x": 320, "y": 72 }
  ],
  "edges": [
    { "id": "edge-1", "from": "input-1", "to": "scraper-1", "kind": "data" }
  ]
}
```

Agent cards reference Markdown agents. Fundamental blocks such as Web Scraper, Store/RAG, Scheduler, and WhatsApp Sender should be reusable block types with site-specific details supplied as inputs/configuration.
Edges reference canvas block IDs and should be shaped for execution semantics, not only visual explanation.

## Production Readiness Rules

- Every CLI command must fail with a clear user-facing error.
- File writes must be deterministic and easy to diff.
- Terminal workflows must work without a browser.
- Visual creation/editing must work without workflow concepts.
- New executable workflow features must pass through the atomic plan and Joel/Mukthar review before code changes.
