# Spider Rose

Spider Rose is a developer-first, local visual workflow workspace for composing executable blocks and agents.

## Identity

| Field | Value |
|---|---|
| Product | Spider Rose |
| CLI | `spiderrose` |
| Purpose | Compose reusable workflow blocks, connect them visually, and run local agent-powered workflows |
| Primary users | AI engineers, software engineers, LangGraph users, open-source agent builders |
| Owners | Joel and Mukthar |
| Status | MVP scaffold, product discovery and atomic-plan gated implementation |

## Direction

Spider Rose starts as files, terminal commands, and a local visual grid:

- Markdown agents under `agents/`
- local project config in `spider-rose.toml`
- canvas layout in `workflow-layout.json`
- future workflow blocks such as Input, Website Source, Web Scraper, Extractor, Store/RAG, Scheduler, Formatter, WhatsApp Sender, and Agent

Visualization is the intended active execution surface. Blocks should connect like Lego pieces on a grid, with connectors carrying output/control flow from one block to the next.

Implementation remains gated: no code changes or feature additions should happen until the work is captured in the atomic plan and approved by Joel and Mukthar.

## Non-Goals

- cloud platform
- authentication
- billing
- marketplace
- vector database
- Kubernetes
- distributed execution
- enterprise permissions
- run history/log browsing
