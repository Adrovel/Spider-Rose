# Spider Rose Description

Version: 0.1.0  
Status: Living product description  
Last updated: 2026-06-01

Spider Rose is a local-first agent workspace for developers. It starts in the terminal, stores agents as Markdown files, and gives those same files a browser-based editor and planning canvas.

The current app is not a full workflow engine. It is the first usable loop for creating agents, editing them visually, running the default agent, and arranging agent cards. The next required product step is to make the terminal feel like a proper app UI and add connector edges that show flow between agent cards.

## Working Description

Spider Rose lets a developer:

- start a local project with `spiderrose`
- create Markdown agents from the terminal
- run the configured default agent from the terminal
- open a local visual app with `/visualise`
- edit agent Markdown in the browser
- inspect Markdown, LangGraph, and Tools placeholder views for an agent card
- open a workflow planning canvas with `/workflow`
- move, click, and duplicate visual cards without duplicating the underlying agent file
- connect agent cards visually so a user can see intended flow before execution exists

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
  -> stores canvas card positions and visual flow edges

Local project files
  -> agents/hello.md
  -> agents/researcher.md
  -> agents/<custom-agent>.md
  -> memory/
  -> spider-rose.toml
  -> workflow-layout.json
```

Canvas cards are visual references to Markdown agents. Duplicating a card creates another visual block that points to the same agent file; it does not create another `agents/*.md` file.

## What Exists Now

- installable `spiderrose` CLI
- interactive terminal shell with slash commands
- automatic local project initialization
- preloaded `hello` and `researcher` agents
- Markdown agent creation
- deterministic default-agent run path
- local visual editor
- editable agent Markdown
- workflow planning canvas
- movable, clickable, duplicable agent cards
- Storybook component review

## Required Next

- terminal UI with history, context, and a stable input area
- directional connector edges between agent cards
- persisted edge data alongside canvas card positions

## What Is Deliberately Later

- workflow execution
- multi-agent handoffs
- live tool execution
- run logs and log browsing
- validation commands
- LangGraph runtime compilation
- cloud accounts or hosted workspaces

This file should change whenever the app surface changes enough that a new contributor would otherwise misunderstand what Spider Rose currently is.
