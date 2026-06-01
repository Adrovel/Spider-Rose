# Spider Rose Product Principles

Version: 0.1.0  
Status: Active product guardrails  
Last updated: 2026-06-01

Purpose: keep Spider Rose from becoming overbuilt before users prove what matters.

## Core Principles

### 1. Simple To Use

Spider Rose should be understandable from one command:

```bash
spiderrose
```

The user should not need to understand orchestration theory, LangGraph internals, workflow engines, or config files before creating and running an agent.

Default behavior should be useful:

- new projects preload a `researcher` agent
- users can type natural tasks
- slash commands are reserved for app actions
- generated files are visible and editable
- errors should say what to do next

### 2. Simple UI

The UI should stay quiet, black-themed, and functional.

Phase 1 UI rules:

- show agents
- create agents
- edit agent Markdown
- show where the agent is stored
- avoid workflow canvas complexity until workflows are actually needed
- avoid dashboards, charts, marketing panels, and decorative layouts

Simple does not mean unfinished. It means the user can immediately see what exists, edit it, and keep moving.

## Production Guardrail

Until Spider Rose has more than 10 real users, push changes to production/main by default after they pass local verification.

This keeps iteration fast while the product is still searching for its shape.

Default flow:

1. Make the scoped change.
2. Run the relevant local check.
3. Commit.
4. Push to `main`.
5. Verify the public install path still works when install behavior changes.

## Complexity Gate

Do not add major abstractions before there is user pressure.

Examples of gated complexity:

- workflow canvas
- authentication
- cloud accounts
- billing
- marketplace
- team permissions
- distributed runtime
- heavy local databases

The question before adding complexity:

```text
Would this help the next 10 users, or is it architecture vanity?
```

If the answer is unclear, document it in `Future-Features.md` instead of building it.
