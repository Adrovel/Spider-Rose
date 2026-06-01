# Spider Rose Architecture

Version: 0.1.0  
Status: Working architecture  
Last updated: 2026-06-01

Spider Rose is a local-first, terminal-native agent workspace with a visual agent editor and workflow planning canvas.

## System Summary

```text
CLI
  -> Terminal UI
  -> Project File Manager
  -> Agent Registry
  -> Single-Agent Runtime
  -> Local Visualization Server
  -> Canvas Layout Store
  -> Markdown Agent Files
```

## MVP Boundaries

Spider Rose Phase 1 supports one definition mode:

| Mode | File | Purpose |
|---|---|---|
| Markdown Agent | `agents/*.md` | beginner-friendly agent definition |

LangGraph Python and workflow definitions are archived for later phases. No third definition format should be introduced.

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
9. The canvas should store visual connector edges that show planned flow between cards.

The visual server should run once per port. If `spiderrose visualise` sees an existing server on the target host/port, it opens that URL instead of starting a second server.

## Canvas Data Model

The canvas stores visual cards now, and should also store visual flow edges:

```json
{
  "cards": [
    { "id": "researcher-1", "agent": "researcher", "x": 70, "y": 72 }
  ],
  "edges": [
    { "id": "edge-1", "from": "researcher-1", "to": "hello-1" }
  ]
}
```

Cards reference Markdown agents. Duplicating a card creates another visual reference to the same agent file; it does not duplicate `agents/*.md`.
Edges reference canvas card IDs. They show intended flow only until workflow execution is implemented.

## Production Readiness Rules

- Every CLI command must fail with a clear user-facing error.
- File writes must be deterministic and easy to diff.
- Terminal workflows must work without a browser.
- Visual creation/editing must work without workflow concepts.
