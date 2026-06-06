# Spider Rose UI Plan Layer

Version: 0.1.0  
Status: Active UI direction  
Last updated: 2026-06-04

Purpose: define the visual and interaction layers without overbuilding the product.

## Layer 1 - Terminal Home

The terminal remains the main entry point.

```bash
spiderrose
```

Users should be able to type naturally, while slash commands remain reserved for app actions.

Current commands:

- `/run <task>`
- `/new agent <name>`
- `/visualise`
- `/help`
- `/exit`

Planned terminal direction:

- persistent terminal screen layout
- visible message history
- stable input area
- current project and default agent context
- plain text becomes a task for the current/default agent
- slash commands control the app

## Layer 2 - Agent Editor

Route:

```text
/
```

Purpose:

- show agents
- create agents
- edit agent Markdown
- save agent files
- show where each agent is stored
- set the default agent

Design:

- black theme
- quiet layout
- dense enough for work
- no marketing content
- no decorative panels

## Layer 3 - Visual Workflow Grid

Route:

```text
/workflow
```

Product purpose:

- reusable workflow blocks on a grid
- directional connector edges between blocks
- active execution surface after approved implementation
- clear Lego-style composition without hiding how data moves

Current behavior:

- cards can be clicked
- cards can be duplicated visually without duplicating the underlying Markdown file
- cards can be dragged
- positions are saved locally
- agents come from `agents/*.md`
- each card shows the agent name and a short description
- each card opens a detail popup with Markdown, LangGraph, and Tools views
- canvas layout is stored in `workflow-layout.json`

Required next behavior:

- define the first fundamental block library
- connect one block to another
- render directional edges
- save edges with the canvas layout
- edit or remove edges
- show whether a connector carries data, a trigger, or both
- support the Google Careers learning workflow as the first education scenario

Fundamental block candidates:

- Input
- Website Source
- Web Scraper
- Extractor
- Store/RAG
- Scheduler
- Formatter
- WhatsApp Sender
- Agent

Not included until approved:

- execution order
- run logs
- workflow validation
- LangGraph graph execution

## Layer 4 - Future Workflow Builder

Only add this after the canvas is useful.

Future behavior after atomic-plan approval:

- mark start agent
- save workflow definitions
- run a workflow from the visual grid
- inspect each agent output

## UI Rule

Every UI layer should answer one question:

```text
What can I create, edit, move, or run right now?
```

If a screen does not answer that question, it probably does not belong in Spider Rose yet.

## Component Review Layer

Storybook covers the visible UI pieces:

- sidebar tabs
- agent editor
- floating add control
- agent picker
- agent details popup

Run:

```bash
npm run storybook
```
