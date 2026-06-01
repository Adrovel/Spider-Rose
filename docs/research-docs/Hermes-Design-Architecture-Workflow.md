# Hermes Design, Architecture, Workflow

## Scope Note

"Hermes" can refer to several projects. For Spider Rose, this note refers to the Hermes Agent CLI installed locally in this workspace and the existing local `insta_clip_agent` prototype that uses Hermes as a multi-agent runner.

## What It Is

Hermes Agent is a terminal-native AI assistant with tool-calling capabilities. The local CLI exposes chat, TUI, gateway, dashboard, skills, plugins, MCP, sessions, logs, profiles, and toolset management.

## Core Product Shape

- CLI-first interaction.
- Optional TUI/dashboard surfaces.
- Toolsets, skills, plugins, and MCP expand the agent's capabilities.
- Sessions are first-class and can be resumed.
- Gateway mode connects agent behavior to messaging or external surfaces.

## Workflow Model

The local `insta_clip_agent` project shows a useful pattern:

1. A Python orchestrator receives one user prompt.
2. Each creative stage runs as a separate Hermes CLI invocation.
3. Each stage has a different system prompt and output contract.
4. Artifacts are passed forward between stages.
5. A review stage can trigger revision.
6. Final artifacts are written to disk.

This is close to the Spider Rose idea: a small terminal command coordinates specialized agents without forcing users into a large platform.

## Architecture Notes

- Hermes treats terminal execution, skills, tools, sessions, profiles, and gateways as separate capabilities.
- A workflow can be built outside Hermes by calling the CLI repeatedly with different prompts/contracts.
- This keeps orchestration understandable, but requires strict output contracts and error handling.

## Lessons For Spider Rose

- Keep the terminal as the primary product surface.
- Make output contracts explicit in agent Markdown.
- Store run artifacts locally in predictable folders.
- Later, allow Spider Rose to execute agents through external runners such as Hermes, LangGraph, or direct provider calls, but do not introduce that complexity in Phase 1.
- A popup with Markdown, LangGraph, and Tools tabs matches the Hermes lesson: users need both simple operation and deeper capability inspection.

## What To Avoid

- Hiding multi-agent behavior behind a single opaque chat session.
- Depending on a specific external agent runner for MVP.
- Adding a dashboard before the terminal workflow is dependable.

## Sources

- Local command reference captured with `hermes --help` on 2026-06-01.
- Local prototype: `/home/moneydrome/2026-Projects/2026-Active-Projects/insta_clip_agent/README.md`
- Local prototype identity: `/home/moneydrome/2026-Projects/2026-Active-Projects/insta_clip_agent/PROJECT.md`
- Hermes Agent docs hub: https://hermes-agent.app/en/docs
- Hermes Agent CLI page: https://hermes-agent.ai/tools/hermes-agent-cli
