# Spider Rose Atomic Plan

Version: 0.1.0  
Status: Working task plan  
Last updated: 2026-06-01

Every task must produce a working artifact, test, or decision record.

## Capacity and Working Rules

| Person | Capacity | Work style |
|---|---:|---|
| Joel | 20 hours/week | product, architecture, UX review, release quality |
| Mukthar | 20 hours/week | implementation, tests, docs, visual support |

Tasks should be small enough to finish in one or two short work sessions. Joel and Mukthar should always have non-blocking work available.

## Completion Rule

Publicise the app at 40% completion.

Marketing checklist for the 40% point:

- [ ] Write one-sentence positioning for Spider Rose.
- [ ] Update README with current screenshots or GIF.
- [ ] Record a short terminal UI demo.
- [ ] Record or capture the visual canvas flow.
- [ ] Share with a small developer audience.
- [ ] Track feedback in a local planning doc or issue list.

## Phase 0 Tasks

Target: finish the existing MVP spine. Estimate: 8-12h remaining.

Joel:

- [x] Create active project folder.
- [x] Add `PROJECT.md`.
- [x] Add `README.md`.
- [x] Add canonical developer docs.
- [x] Create GitHub repository under Adrovel.
- [ ] Review current README pitch.
- [ ] Approve first public repo positioning.
- [ ] Decide whether current install copy is enough for private testers.

Mukthar:

- [x] Create active project folder.
- [x] Add `PROJECT.md`.
- [x] Add `README.md`.
- [x] Add canonical developer docs.
- [x] Add installable Python package scaffold.
- [x] Add `spiderrose new agent`.
- [x] Add `spiderrose run`.
- [x] Add `spiderrose visualise`.
- [x] Add plain `spiderrose` interactive shell with slash commands.
- [x] Archive workflow/log/validate features for later.
- [x] Add basic CLI flow test.
- [ ] Run tests in a clean virtual environment.
- [ ] Fix any clean-install failures.
- [ ] Push initial repository to GitHub after Joel approves push.

## Phase 1 Tasks

Target: make `spiderrose` feel like a real terminal app. Estimate: 40-55h.

Joel:

- [ ] Define terminal UI layout acceptance criteria.
- [ ] Decide exact header fields: project, default agent, mode.
- [ ] Decide slash command menu contents.
- [ ] Review terminal copy for `/help`, `/run`, `/new agent`, `/visualise`, `/exit`.
- [ ] Review final terminal UI behavior before Phase 1 close.

Mukthar:

- [ ] Build terminal UI layout for the `spiderrose` shell.
- [ ] Show terminal message history.
- [ ] Show current project and default agent context in the terminal UI.
- [ ] Add fixed input bar.
- [ ] Add slash command menu.
- [ ] Render clean output blocks for agent runs.
- [ ] Keep existing slash commands working.
- [ ] Add malformed Markdown agent tests.
- [ ] Add package install smoke test.
- [ ] Add release checklist.
- [ ] Add terminal demo GIF or asciinema script.

## Phase 2 Tasks

Target: add visual connector edges without workflow execution. Estimate: 30-45h.

Joel:

- [ ] Define supported edge labels for v1.
- [ ] Decide edge direction rules.
- [ ] Decide whether duplicate cards can connect to each other.
- [ ] Review canvas edge UX.

Mukthar:

- [ ] Add connector edges between workflow canvas cards.
- [ ] Render directional arrows.
- [ ] Support edge labels.
- [ ] Persist edges in `workflow-layout.json`.
- [ ] Add edge edit/delete interactions.
- [ ] Keep edge behavior visual-only until runtime support exists.
- [ ] Add tests or fixtures for edge persistence.

## Phase 3 Tasks

Target: complete agent editing and default-agent control. Estimate: 25-35h.

Joel:

- [ ] Finalize Markdown agent fields: name, role, goal, instructions, tools, expected output.
- [ ] Define default-agent selector behavior.
- [ ] Review whether agent fields stay readable in raw Markdown.

Mukthar:

- [ ] Add agent detail sidebar.
- [ ] Edit agent name from sidebar.
- [ ] Edit role, goal, instructions, tools, and expected output from sidebar.
- [ ] Save sidebar edits directly to `agents/*.md`.
- [ ] Add visual default-agent selector.
- [ ] Add `/default <agent>` command.
- [ ] Update `spider-rose.toml` when default changes.
- [ ] Add focused tests for default-agent behavior.

## Phase 4 Tasks

Target: make reusable agent creation useful across projects. Estimate: 35-50h.

Joel:

- [ ] Define custom agent library scope.
- [ ] Decide whether library storage is project-local, user-global, or both.
- [ ] Decide library naming rules.
- [ ] Decide first library categories.
- [ ] Write built-in template content for Researcher.
- [ ] Write built-in template content for Planner.
- [ ] Write built-in template content for Coder.
- [ ] Write built-in template content for Reviewer.
- [ ] Write built-in template content for Summarizer.
- [ ] Write built-in template content for Debugger.
- [ ] Review custom agent library UX.
- [ ] Trigger 40% marketing checklist if not already started.

Mukthar:

- [ ] Add local `agent-library/` storage.
- [ ] Add command to list library agents.
- [ ] Add command to save an existing agent into the library.
- [ ] Add `/new agent <name> --from-library <library-agent>`.
- [ ] Add visual library browser.
- [ ] Add create-from-library flow in the visual app.
- [ ] Add template registry.
- [ ] Add `/new agent <name> --template <template>`.
- [ ] Keep library entries as Markdown files.
- [ ] Add tests for library agent creation.
- [ ] Add tests for template agent creation.

## Phase 5 Tasks

Target: defer heavier runtime work until the app is useful. Estimate: 50-80h.

Joel:

- [ ] Decide when real workflow execution is worth adding.
- [ ] Decide whether LangGraph is still the right runtime target.
- [ ] Decide MCP boundary after core app stabilizes.
- [ ] Decide local RAG boundary after file/runs model stabilizes.

Mukthar:

- [ ] Add LangGraph dependency gate only after approval.
- [ ] Compile workflow model into LangGraph graph only after visual model stabilizes.
- [ ] Add runtime tests only after execution semantics are approved.
- [ ] Keep RAG, MCP, logs, validation, and canvas notes out of active scope until reopened.
