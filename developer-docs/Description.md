# Spider Rose Description

Version: 0.1.0  
Status: Living product description  
Last updated: 2026-06-01

Spider Rose is a simple local app for creating and running small AI agents from your computer.

An agent is a reusable worker with a name, a goal, instructions, tools it may use later, and an expected output. In Spider Rose, agents are stored as plain Markdown files, so they are easy to read, edit, copy, share, and version control.

The first version keeps the product intentionally small:

- open Spider Rose from the terminal with `spiderrose`
- use the built-in `researcher` agent immediately
- create more agents when needed
- edit agents in a simple black-themed browser UI
- see exactly where each agent is stored on disk
- move agents around on a workflow canvas as a planning surface

Spider Rose is not trying to be a large no-code automation platform. It is meant for developers, AI builders, and semi-technical users who want agent workflows that start as files and remain understandable.

## Current Mental Model

```text
Terminal
  -> opens Spider Rose
  -> runs or creates agents

Visual app
  -> edits agent files
  -> shows a simple workflow canvas

Local files
  -> agents/researcher.md
  -> agents/<custom-agent>.md
  -> workflow-layout.json
```

## What Exists Now

- local terminal shell
- slash commands
- preloaded `researcher` agent
- visual agent editor
- editable Markdown agent files
- simple movable workflow canvas

## What Comes Later

- connected workflows
- multi-agent handoffs
- live tools
- logs
- validation
- LangGraph execution
- richer terminal interface

This file should be updated whenever the app meaningfully changes so that a new person can quickly understand what Spider Rose is becoming.
