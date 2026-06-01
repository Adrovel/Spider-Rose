# Spider Rose Architecture

Version: 0.1.0  
Status: Phase 1 scope locked  
Last updated: 2026-06-01

Spider Rose is a local-first, terminal-native agent runner with a visual agent editor.

## System Summary

```text
CLI
  -> Project File Manager
  -> Agent Registry
  -> Single-Agent Runtime
  -> Local Visualization Server
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

## Production Readiness Rules

- Every CLI command must fail with a clear user-facing error.
- File writes must be deterministic and easy to diff.
- Terminal workflows must work without a browser.
- Visual creation/editing must work without workflow concepts.
