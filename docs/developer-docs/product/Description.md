# Spider Rose Description

Version: 0.1.0  
Status: Living product description  
Last updated: 2026-06-05

Spider Rose is a local-first visual workflow workspace for developers. It starts from local files and terminal commands, but the product direction is a visual execution grid where reusable blocks connect like Lego pieces.

The current app is not yet the full workflow engine. It is the first usable loop for creating agents, editing them visually, running the default agent, and arranging cards. The clarified product direction is that visual blocks become the active execution model after the work is approved through the atomic plan.

## Working Description

Spider Rose should let a developer:

- start a local project with `spiderrose`
- create Markdown agents from the terminal
- run the configured default agent from the terminal
- open a local visual app with `/visualise`
- edit agent Markdown in the browser
- inspect Markdown and LangGraph placeholder views for an agent card
- open a visual workflow grid with `/workflow`
- move, click, and duplicate visual blocks without duplicating the underlying definition
- connect workflow blocks so output/control flows from one block to the next
- build workflows from reusable fundamental blocks instead of creating a new block for every site
- reuse custom agents from a local agent library once the core editor is stable

Agents are plain files under `agents/`. The generated project also includes `memory/`, `spider-rose.toml`, and a `workflow-layout.json` file once canvas positions are saved.

## Current Mental Model

```text
Terminal shell
  -> creates agents
  -> runs the default agent
  -> opens the visual app

Visual app
  -> edits Markdown agent files
  -> shows agent detail popups
  -> stores canvas block positions and workflow connectors
  -> becomes the active execution surface after approved implementation

Fundamental blocks
  -> Input
  -> Website Source
  -> Web Scraper
  -> Extractor
  -> Store/RAG
  -> Scheduler
  -> Formatter
  -> WhatsApp Sender
  -> Agent

Local project files
  -> agents/google-careers-scraper.md
  -> agents/<custom-agent>.md
  -> agent-library/
  -> memory/
  -> spider-rose.toml
  -> workflow-layout.json
```

Canvas cards currently reference Markdown agents. The product direction is broader: the canvas should support workflow blocks. Duplicating an agent card creates another visual block that points to the same agent file; it does not create another `agents/*.md` file.

## Product Clarity Scenario

The first education workflow is:

```text
Input: "software engineer in India"
  -> Website Source: Google Careers
  -> Web Scraper
  -> Extractor
  -> Store/RAG
  -> Formatter
  -> WhatsApp Sender
```

This should teach Joel and Mukthar how fundamental blocks compose into a useful workflow. Google Careers is an input/configuration for a Web Scraper workflow, not automatically a permanent one-off block.

## What Exists Now

- installable `spiderrose` CLI
- interactive terminal shell with slash commands
- terminal header with project and default-agent context
- panel-rendered help and run output
- automatic local project initialization
- preloaded `google-careers-scraper` demo agent
- Markdown agent creation
- deterministic default-agent run path
- local visual editor
- editable agent Markdown
- workflow planning canvas
- fixed demo canvas with clickable workflow blocks
- Storybook component review
- education docs for fundamental blocks and the Google Careers learning workflow

## Required Next

- persistent terminal history
- fundamental block library definition
- typed connector model for visual execution flow
- directional connector edges between workflow blocks
- persisted edge data alongside canvas block positions
- Google Careers learning workflow design before implementation
- custom agent library for reusable Markdown agents

## What Is Deliberately Later

- multi-agent handoffs
- live tool execution
- run logs and log browsing
- validation commands
- LangGraph runtime compilation
- cloud accounts or hosted workspaces

This file should change whenever the app surface changes enough that a new contributor would otherwise misunderstand what Spider Rose currently is.
