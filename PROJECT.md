# Spider Rose

Spider Rose is a developer-first, local agent workspace for creating, editing, arranging, and running Markdown agents.

## Identity

| Field | Value |
|---|---|
| Product | Spider Rose |
| CLI | `spiderrose` |
| Purpose | Create, edit, arrange, and run local Markdown agents from the terminal and visual app |
| Primary users | AI engineers, software engineers, LangGraph users, open-source agent builders |
| Owners | Joel and Mukthar |
| Status | MVP scaffold, CLI-first |

## Direction

Spider Rose starts as files, terminal commands, and a local visual editor:

- Markdown agents under `agents/`
- local project config in `spider-rose.toml`
- canvas layout in `workflow-layout.json`

Visualization is the Phase 1 app surface for creating, editing, inspecting, and arranging agent cards.
Visual connector edges are required next so the canvas can show intended flow. Workflow execution is intentionally paused until a later phase.

## Non-Goals

- cloud platform
- authentication
- billing
- marketplace
- vector database
- Kubernetes
- distributed execution
- enterprise permissions
- workflow execution
- run history/log browsing
