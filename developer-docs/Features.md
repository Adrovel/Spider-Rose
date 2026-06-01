# Spider Rose Features

Version: 0.1.0  
Status: Phase 1 scope locked  
Last updated: 2026-06-01

## MVP Features

| Feature | Command | Status |
|---|---|---|
| Launch visual agent editor | `spiderrose visualise` | implemented |
| Create Markdown agent | `spiderrose new agent researcher` | implemented |
| Run default agent | `spiderrose run "Search Nathan's LinkedIn"` | implemented |

## User Promise

A user should be able to stay entirely in the terminal:

```bash
spiderrose visualise
spiderrose new agent researcher
spiderrose run "Search Nathan's LinkedIn"
```

## Definition Formats

Only one definition format is active in Phase 1:

- Markdown agents in `agents/*.md`

Workflow formats are paused.

## Non-Goals

- cloud platform
- user authentication
- billing
- marketplace
- vector database
- Kubernetes
- distributed execution
- enterprise permissions
- workflow creation
- workflow validation
- run log browsing
