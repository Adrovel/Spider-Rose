# Spider Rose

Terminal-first agent creation and execution for developers.

Spider Rose lets users create Markdown agents visually, create agents from the terminal, and run the default agent from the terminal.

Phase 1 intentionally does not include workflow creation. That is archived for a later phase.

## Copyable Launch Command

After the GitHub repo is pushed, friends should be able to try the app with:

```bash
pipx run git+https://github.com/Adrovel/Spider-Rose.git visualise
```

## Install For Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## CLI

```bash
spiderrose visualise
spiderrose new agent researcher
spiderrose run "Search Nathan's LinkedIn"
```

The legacy handover command name is also supported:

```bash
agentforge visualise
```

## Project Files Created Automatically

```text
agents/
memory/
spider-rose.toml
```

## Documentation

Canonical developer docs live in [`developer-docs/`](./developer-docs/README.md).

## Status

The MVP is intentionally local-first and terminal-first. The runtime currently executes one default Markdown-defined agent deterministically. Workflows, logs, validation, LangGraph execution, and multi-agent handoffs are future features.
