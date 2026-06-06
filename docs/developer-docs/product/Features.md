# Spider Rose Features

Version: 0.1.0  
Status: Working feature map  
Last updated: 2026-06-05

## Implemented Features

| Feature | Command | Status |
|---|---|---|
| Launch terminal shell | `spiderrose` | implemented |
| Launch visual agent editor | `/visualise` | implemented |
| Preload Google Careers scraper agent | automatic on first run | implemented |
| Create Markdown agent | `/new agent google-careers-scraper` | implemented |
| Run default agent | `/run Search Nathan's LinkedIn` | implemented |
| Click agent canvas blocks | visual app | implemented |
| Duplicate visual agent blocks | visual app | implemented |
| Inspect Markdown/LangGraph per block | visual app | implemented |
| Component stories | `npm run storybook` | implemented |

## Required Next Features

Spider Rose stays local-first. The clarified product priority is a visual execution grid made from reusable fundamental blocks. Implementation remains atomic-plan gated and requires Joel and Mukthar approval.

| Feature | Surface | Status |
|---|---|---|
| Persistent terminal history | `spiderrose` shell | required next |
| Fundamental block library definition | product/education docs | required next |
| Typed connector model | `/workflow` canvas | required next |
| Connector edges between workflow blocks | `/workflow` canvas | required next |
| Google Careers learning workflow | education + atomic plan | required next |
| Custom agent library | terminal and visual app | planned after core editor |

## Terminal UI Requirement

The terminal should feel like a real app surface, not only a prompt loop.

Implemented behavior:

- project header
- default-agent context
- three-row input composer with spider-only indicator
- clear command responses
- panel-rendered run output
- background in-session history for task context
- `/recent` command for showing terminal history
- `/menu` command for showing the shared slash command menu
- slash command typeahead sourced from the shared command registry
- slash command support
- `/clear` command

Deferred behavior:

- streaming responses
- multiline composer
- selectable agent context
- run history browser
- persistent message history

## Fundamental Block Requirement

Spider Rose should not create a new block type for every website or scenario.

First block candidates:

- Input
- Website Source
- Web Scraper
- Extractor
- Store/RAG
- Scheduler
- Formatter
- WhatsApp Sender
- Agent

Example:

`Web Scraper` is fundamental. `Google Careers` is an input or configuration.

## Connector Edge Requirement

The workflow canvas should visually show active flow between blocks.

Required behavior:

- connect one workflow block to another
- render directional connector edges
- persist card positions and edge relationships
- define whether each connector carries data, a trigger, or both
- keep existing agent cards as references to `agents/*.md`
- use connectors as the execution model after approval

Deferred behavior:

- conditional routing
- workflow validation
- terminal workflow execution
- LangGraph compilation

## Learning Workflow Requirement

The first product-clarity workflow is:

```text
Input
  -> Website Source: Google Careers
  -> Web Scraper
  -> Extractor
  -> Store/RAG
  -> Formatter
  -> WhatsApp Sender
```

The purpose is to educate Joel and Mukthar, then approve an implementation plan. It is not permission to add scraper code directly.

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
/library add google-careers-scraper
/new agent review-bot --from-library reviewer
```

Suggested local shape:

```text
agent-library/
  google-careers-scraper.md
  planner.md
  reviewer.md
```

The library is not a marketplace. It should not require accounts, publishing, ratings, or remote sync in the current plan.

## Not Active Now

These are useful later, but not part of the current implementation plan:

- run logs and run artifacts
- validation command
- canvas sticky notes
- canvas inspector panel
- MCP execution

## User Promise

A user should be able to stay entirely in the terminal:

```bash
spiderrose
```

Inside Spider Rose:

```text
/visualise
/new agent google-careers-scraper
/run Search Nathan's LinkedIn
```

## Definition Formats

Only one definition format is active in Phase 1:

- Markdown agents in `agents/*.md`

Workflow execution formats are paused until approved. Visual connector edges and fundamental workflow blocks are now part of the required product direction.

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
