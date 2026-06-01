# Spider Rose Agents

Version: 0.1.0  
Status: Phase 1 scope locked  
Last updated: 2026-06-01

Phase 1 agents are Markdown files under `agents/`.

## Format

```md
# Researcher Agent

Goal:
Find accurate information.

Instructions:
- Search reliable sources.
- Summarize findings.

Tools:
- web_search

Output:
research_summary
```

## Naming

Agent names are converted into lowercase slugs:

| Input | File |
|---|---|
| `Researcher` | `agents/researcher.md` |
| `LinkedIn Search` | `agents/linkedin-search.md` |
| `identify_person` | `agents/identify-person.md` |

## Phase 1 Execution

`spiderrose run "<task>"` sends the task to the default agent.

If the first agent is created with:

```bash
spiderrose new agent researcher
```

then `researcher` becomes the default agent automatically.

## Limits

Phase 1 agents do not yet execute live tools, call LinkedIn, browse the web, or hand off to other agents. They define the local file format and execution surface first.

Those capabilities are documented in `Future-Features.md`.
