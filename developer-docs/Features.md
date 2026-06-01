# Spider Rose Features

Version: 0.1.0  
Status: Phase 1 scope locked  
Last updated: 2026-06-01

## MVP Features

| Feature | Command | Status |
|---|---|---|
| Launch terminal shell | `spiderrose` | implemented |
| Launch visual agent editor | `/visualise` | implemented |
| Preload researcher agent | automatic on first run | implemented |
| Create Markdown agent | `/new agent researcher` | implemented |
| Run default agent | `/run Search Nathan's LinkedIn` | implemented |
| Move agents on workflow canvas | `/workflow` in the visual app | implemented |

## User Promise

A user should be able to stay entirely in the terminal:

```bash
spiderrose
```

Inside Spider Rose:

```text
/visualise
/new agent researcher
/run Search Nathan's LinkedIn
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
