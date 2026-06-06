# Spider Rose Team

Version: 0.1.0  
Status: Active team plan  
Last updated: 2026-06-05

## Capacity

Planning capacity:

| Person | Weekly capacity | Daily rhythm | Planning rule |
|---|---:|---:|---|
| Joel | 20 hours/week | about 2-3 hours/day | product, architecture, review, release quality |
| Mukthar | 20 hours/week | about 2-3 hours/day | implementation, tests, UI polish, docs updates |

Combined planning capacity is 40 hours/week. Plans should assume small, independently shippable tasks because both contributors work limited daily blocks.

## Joel

Joel owns product direction, architecture shape, CLI ergonomics, and final project quality.

Joel is the final product decision owner. Mukthar can review, challenge, and propose product ideas, but Mukthar's product decisions may need Joel approval. If Joel and Mukthar disagree on product direction, Joel usually overrides.

Best tasks:

- define command surface
- approve workflow and runtime boundaries
- write design decisions
- review terminal UX
- decide when LangGraph support is MVP-ready

Non-blocking work:

- write or update product docs while Mukthar implements
- review CLI and UI behavior after small task branches land
- define feature boundaries before implementation starts
- prepare public positioning once completion reaches 40%

## Mukthar

Mukthar owns scoped implementation work, test coverage, documentation upkeep, and visualisation support.

Mukthar owns implementation quality within approved product boundaries. For product direction, Mukthar should raise concerns and alternatives, then defer to Joel's final decision.

Best tasks:

- master terminal UI fundamentals, reference strong CLI/TUI products, and teach the concepts from `Mukthar-TUI-Working-Start.md`
- implement small CLI commands
- add tests for parser and runtime behavior
- improve docs after implementation
- implement React Flow screens once API contracts are stable
- validate terminal examples on a clean machine

Non-blocking work:

- implement terminal UI tasks from documented acceptance criteria
- add focused tests without waiting for visual design polish
- update docs after code behavior changes
- prepare screenshots/demo artifacts once publicisation starts

## Shared Rules

- Principle No. 1: before you optise a requirement or complete a task, question whether the task needs to be done.
- Requirement No. 2: understand the fundamentals of the task, even if you think you know it.
- Requirement No. 3: if you don't know the fundamentals, learn it before implementing the task.
- Keep terminal use working before workflow features.
- Update developer docs when changing architecture or command behavior.
- Do not add a third definition format.
- Do not introduce cloud assumptions into the MVP.
- Keep Joel and Mukthar unblocked by splitting work into independent tasks.
- Publicise the app when the plan reaches 40% completion.
