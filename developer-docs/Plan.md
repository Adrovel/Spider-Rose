# Spider Rose Plan

Version: 0.1.0  
Status: Phase 1 scope locked  
Last updated: 2026-06-01

## Phase 0 - Product Spine

Goal: make the smallest terminal and visual app loop work end-to-end.

Exit criteria:

- `spiderrose` launches the terminal shell.
- `/visualise` launches a local visual agent editor.
- `/new agent <name>` creates Markdown agents.
- `/run <task>` runs the default agent.
- A friend can use one copyable command after the GitHub repo is pushed.

## Phase 1 - Production CLI Hardening

Goal: make terminal usage reliable enough for outside users.

Work:

- improve error messages
- add more parser tests
- add packaging smoke test
- add release checklist

## Phase 2 - Workflow Creation

Goal: introduce workflow creation after the agent editor is useful.

Work:

- visual workflow creation
- workflow connections
- default workflow selection
- terminal workflow execution

Current bridge:

- `/workflow` now exists as a movable planning canvas.
- Cards can be positioned before workflow edges/execution are introduced.

## Phase 3 - LangGraph Runtime

Goal: execute workflows through LangGraph while keeping Markdown agents simple.

Work:

- compile YAML workflow into LangGraph `StateGraph`
- support LangGraph Python workflow discovery
- preserve JSON run logs
- document how LangGraph users opt in

## Phase 4 - Advanced Visualisation

Goal: add canvas-based workflow editing once workflows exist.

Work:

- FastAPI project endpoints
- React Flow canvas
- tabs for Canvas, Agents, Tools, Runs, Logs, Settings
- Markdown agent editing
- save changes back to files

## Phase 5 - Local Persistence

Goal: add SQLite only where JSON logs become limiting.

Work:

- SQLite schema for runs and events
- migration path from JSON logs
- local-only memory store
