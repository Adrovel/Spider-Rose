# Spider Rose Agents

Version: 0.1.0  
Status: Phase 1 scope locked  
Last updated: 2026-06-01

Phase 1 agents are Markdown files under `agents/`.

## Storage

Agents are stored in the active Spider Rose project directory:

```text
agents/<agent-slug>.md
```

For example:

```text
agents/researcher.md
agents/linkedin-search.md
```

The project directory is whichever folder the user runs `spiderrose` from. If `spider-rose.toml` is not found, Spider Rose initializes that folder by creating:

```text
agents/
memory/
spider-rose.toml
```

The visual app and terminal shell edit the same Markdown files.

Workflow canvas positions are stored separately:

```text
workflow-layout.json
```

Moving an agent card on the canvas does not change the agent Markdown file.

The canvas stores visual cards, not duplicate agents. This means one Markdown agent can appear multiple times on the canvas as separate visual blocks:

```json
{
  "cards": [
    { "id": "researcher-1", "agent": "researcher", "x": 70, "y": 72 },
    { "id": "researcher-2", "agent": "researcher", "x": 180, "y": 160 }
  ]
}
```

Clicking a card opens a popup with:

- Markdown view
- LangGraph view
- Tools view

In Phase 1, Markdown is editable in the sidebar and LangGraph/Tools are inspection placeholders.

## Preloaded Agents

Every new Spider Rose project starts with:

```text
agents/researcher.md
```

`researcher` is the default agent in Phase 1. It is responsible for turning a user task into a clear, structured starting point.

Initial researcher template:

```md
# Researcher Agent

Goal:
Find accurate information and turn a user task into a clear starting point.

Instructions:
- Identify what the user is asking for.
- Pull out names, entities, platforms, and constraints.
- Say what information is known and what is still missing.
- Return concise, structured output.

Tools:
- web_search

Output:
research_summary
```

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

`/run <task>` sends the task to the default agent inside the `spiderrose` shell.

New custom agents can be created with `/new agent <name>`. The first preloaded default remains `researcher` unless the visual editor sets another default.

## Limits

Phase 1 agents do not yet execute live tools, call LinkedIn, browse the web, or hand off to other agents. They define the local file format and execution surface first.

Those capabilities are documented in `Future-Features.md`.
