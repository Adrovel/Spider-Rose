# Spider Rose Agents

Version: 0.1.0  
Status: Phase 1 scope locked  
Last updated: 2026-06-05

Phase 1 agents are Markdown files under `agents/`.

## Storage

Agents are stored in the active Spider Rose project directory:

```text
agents/<agent-slug>.md
```

For example:

```text
agents/google-careers-scraper.md
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
    { "id": "google-careers-scraper-1", "agent": "google-careers-scraper", "x": 70, "y": 72 }
  ]
}
```

Clicking a card opens a popup with:

- Markdown view
- LangGraph view
- LangGraph view

In Phase 1, Markdown is editable in the sidebar and LangGraph is an inspection placeholder.

## Preloaded Agents

Every new Spider Rose project starts with:

```text
agents/google-careers-scraper.md
```

`google-careers-scraper` is the current default while the two-block Google Careers demo is the immediate priority.

Initial Google Careers scraper template:

```md
# Google Careers Scraper Agent

Goal:
Scrape Google Careers search results and return a small, readable list of matching jobs.

Instructions:
- Use the user's task as the search query.
- Treat text after "in" as the location when the user writes a task like "software engineer in India".
- Return job title, location, level, and minimum qualifications.
- Do not invent jobs when the Careers page cannot be fetched or parsed.

Tools:
- google_careers_scraper

Output:
google_careers_jobs
```

## Format

```md
# Google Careers Scraper Agent

Goal:
Scrape Google Careers search results and return matching jobs.

Instructions:
- Use the user's task as the search query.
- Return clear, structured output.

Tools:
- google_careers_scraper

Output:
google_careers_jobs
```

## Naming

Agent names are converted into lowercase slugs:

| Input | File |
|---|---|
| `Google Careers Scraper` | `agents/google-careers-scraper.md` |
| `LinkedIn Search` | `agents/linkedin-search.md` |
| `identify_person` | `agents/identify-person.md` |

## Phase 1 Execution

`/run <task>` sends the task to the default agent inside the `spiderrose` shell.

New custom agents can be created with `/new agent <name>`. The first preloaded default is currently `google-careers-scraper` while the demo is being made workable.

## Limits

Phase 1 agents do not yet execute live tools, call LinkedIn, browse the web, or hand off to other agents. They define the local file format and execution surface first.

Those capabilities are documented in `Future-Features.md`.
