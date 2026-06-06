# Spider Rose

Local visual workflow blocks for developer agents and automation.

Spider Rose lets users compose reusable workflow blocks on a visual grid, connect those blocks, and keep the underlying project local and inspectable.

The current MVP still includes a terminal shell, Markdown agents, and a local visual app. The clarified product direction is a Lego-style visual execution surface with fundamental blocks such as Input, Website Source, Web Scraper, Extractor, Store/RAG, Scheduler, Formatter, WhatsApp Sender, and Agent.

No feature implementation should happen until the work is captured in the atomic plan and approved by Joel and Mukthar.

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
/new agent google-careers-scraper
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

Core product questions live in [`idea.md`](./idea.md).
Canonical developer docs live in [`docs/developer-docs/`](./docs/developer-docs/README.md), grouped by product, implementation, planning, and team.
Education docs live in [`docs/developer-docs/education/`](./docs/developer-docs/education/README.md), including the Google Careers workflow learning scenario.
Research notes live in [`docs/research-docs/`](./docs/research-docs/README.md).

## Storybook

Component stories live under `stories/`.

```bash
npm run storybook
npm run build-storybook
```

## Status

The MVP is local-first. The runtime currently executes one default Markdown-defined agent deterministically, and the visual app edits and arranges agent cards. Product work is now focused on fundamental block definitions, typed visual connectors, and the Google Careers learning workflow before runtime implementation.
