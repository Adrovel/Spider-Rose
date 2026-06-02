# Spider Rose

Terminal-first agent creation and execution for developers.

Spider Rose lets users create Markdown agents visually, create agents from the terminal, run the default agent from the terminal, and arrange agent cards on a visual canvas.

The next product requirements are persistent terminal history and connector edges between agent cards. Workflow execution is archived for a later phase.

## Install

Linux/macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/Adrovel/Spider-Rose/main/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/Adrovel/Spider-Rose/main/install.ps1 | iex
```

Then run:

```bash
spiderrose
```

One-time run without installing:

```bash
pipx run git+https://github.com/Adrovel/Spider-Rose.git
```

## Install For Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
npm install
```

## CLI

```bash
spiderrose
```

Inside Spider Rose:

```text
/visualise
/new agent researcher
/run Search Nathan's LinkedIn
/clear
/exit
```

## Project Files Created Automatically

```text
agents/
memory/
spider-rose.toml
```

## Documentation

Canonical developer docs live in [`docs/developer-docs/`](./docs/developer-docs/README.md), grouped by product, implementation, planning, and team.
Research notes live in [`docs/research-docs/`](./docs/research-docs/README.md).

## Storybook

Component stories live under `stories/`.

```bash
npm run storybook
npm run build-storybook
```

## Status

The MVP is intentionally local-first and terminal-first. The runtime currently executes one default Markdown-defined agent deterministically. The terminal shell now renders a project header, default-agent context, command panels, and run output panels. Persistent history and visual flow edges are required next; logs, validation, LangGraph execution, workflow execution, and multi-agent handoffs are future features.
