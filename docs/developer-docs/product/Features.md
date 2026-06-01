# Spider Rose Features

Version: 0.1.0  
Status: Working feature map  
Last updated: 2026-06-01

## Implemented Features

| Feature | Command | Status |
|---|---|---|
| Launch terminal shell | `spiderrose` | implemented |
| Launch visual agent editor | `/visualise` | implemented |
| Preload hello agent | automatic on first run | implemented |
| Preload researcher agent | automatic on first run | implemented |
| Create Markdown agent | `/new agent researcher` | implemented |
| Run default agent | `/run Search Nathan's LinkedIn` | implemented |
| Move agents on workflow canvas | `/workflow` in the visual app | implemented |
| Click agent canvas blocks | visual app | implemented |
| Duplicate visual agent blocks | visual app | implemented |
| Inspect Markdown/LangGraph/Tools per block | visual app | implemented |
| Component stories | `npm run storybook` | implemented |

## Required Next Features

Spider Rose stays local-first and terminal-first. The current priority is making the terminal shell feel like a real app, then making the visual canvas show simple flow between agents.

| Feature | Surface | Status |
|---|---|---|
| Terminal UI | `spiderrose` shell | required next |
| Connector edges between agent cards | `/workflow` canvas | required next |
| Custom agent library | terminal and visual app | planned after core editor |

## Terminal UI Requirement

The terminal should feel like a real app surface, not only a prompt loop.

Required behavior:

- persistent terminal screen layout
- visible message history
- command input area
- clear command responses
- obvious current project and default agent context
- slash command support

Deferred behavior:

- streaming responses
- multiline composer
- selectable agent context
- run history browser

## Connector Edge Requirement

The workflow canvas should visually show flow between agents.

Required behavior:

- connect one agent card to another
- render directional connector edges
- persist card positions and edge relationships
- keep cards as references to `agents/*.md`
- avoid executing the workflow until runtime support exists

Deferred behavior:

- conditional routing
- workflow validation
- terminal workflow execution
- LangGraph compilation

## Custom Agent Library Requirement

The agent library should be a local-first collection of reusable Markdown agents.

Required behavior:

- save a current agent into the library
- create a project agent from a library entry
- browse library agents from the visual app
- list library agents from the terminal
- keep library entries as readable Markdown files
- support user-created library entries, not only built-in templates

Possible commands:

```text
/library
/library add researcher
/new agent review-bot --from-library reviewer
```

Suggested local shape:

```text
agent-library/
  researcher.md
  planner.md
  reviewer.md
```

Stored custom agent ideas live in [Custom Agents](./Custom-Agents.md).

The library is not a marketplace. It should not require accounts, publishing, ratings, or remote sync in the current plan.

## Not Active Now

These are useful later, but not part of the current implementation plan:

- run logs and run artifacts
- validation command
- canvas sticky notes
- canvas inspector panel
- RAG
- MCP execution

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

Workflow execution formats are paused. Visual connector edges are now part of the required canvas experience.

## Non-Goals

- cloud platform
- user authentication
- billing
- marketplace
- vector database
- Kubernetes
- distributed execution
- enterprise permissions
- workflow validation
- run log browsing
