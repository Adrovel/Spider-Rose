# Spider Rose Atomic Plan

Version: 0.1.0  
Status: Working task plan  
Last updated: 2026-06-05

Every task must produce a working artifact, test, or decision record.

## Implementation Gate

No actual code changes should happen without the work going through this atomic-plan phase. Joel is the final product approval owner. Mukthar review is important for implementation quality, technical concerns, and TUI work, but Mukthar product decisions may need Joel approval and Joel usually overrides product direction.

Scenario walkthroughs are product discovery. They should clarify blocks, connectors, inputs, and workflows before implementation starts.

## Current Joel Priority

Joel's immediate priority has shifted to making the current two-block Google Careers demoable.

The current demo should take what is already done, then improve functionality first. After that, improve the UI component by component: progress chips, blocks, connectors, and the right sidebar.

Before any feature is implemented, Joel should see the resource-use cost of that feature. Resource use is a planning and approval input for Joel, not a layman-facing product feature.

Current source of truth:

- clarified decisions: `docs/developer-docs/product-decisions/Product-Decisions.md`
- ambiguous queue: `docs/developer-docs/product-decisions/Ambiguous-Questions.md`
- demo/outreach plan: `docs/developer-docs/planning/Demo-and-Outreach-Plan.md`

Joel's immediate work:

- [x] Decide first real users: Joel and Mukthar, then developers.
- [x] Decide first painful jobs: creating agents, arranging agents, and understanding flows.
- [x] Decide first-run feeling: simplicity.
- [x] Decide product feel: local workflow builder and agent IDE.
- [x] Decide agent creation interaction: chat-style wizard, not a form.
- [x] Define the chat-style wizard questions for creating the first useful agent.
- [x] Decide which fields a non-developer must understand to create a useful agent.
- [x] Define exact terminal wizard command behavior for `/new agent`.
- [x] Clarify that the visual canvas is the active execution model.
- [ ] Define exact visual wizard entry point and review screen.
- [ ] Resolve terminal versus visual boundary from the ambiguous queue.
- [x] Clarify what connector edges mean before implementation: active execution/data flow between blocks.
- [x] Clarify the first teaching workflow: Web Scraper: Google Careers -> Store: Job Results.
- [x] Decide implementation gate: code changes require atomic-plan approval; Joel is final product owner and Mukthar reviews implementation/technical quality.
- [x] Clarify reusable fundamental blocks: Web Scraper can accept sites as inputs instead of each site becoming a new block.
- [x] Decide v0 data formats: Markdown for definitions, JSON for block messages, JSONL for stored records, TOML for project config, Markdown for human reports.
- [x] Decide Store block v0 output includes `sample_records` so users can preview saved job links without opening the JSONL file.
- [x] Decide first visual proof: selecting the Store block opens a right-side inspector panel with saved path, counts, dedupe rule, and sample job links.
- [x] Decide v0 block run states: Idle, Running, Success, Failed.
- [x] Decide first connector contract: internal `data` connector carries `job_results` from Web Scraper to Store.
- [ ] Decide non-technical user-facing words for block and connector labels; avoid exposing internal terms like `payload_type` and `job_results` in normal UI.
- [ ] Decide what information appears inside workflow blocks on the grid; this is separate from the right-side inspector panel.
- [ ] Decide v0 workflow storage path: `artifacts/google-careers/job-results.jsonl` is the current working proposal, but the artifact method is still debatable.
- [ ] Todo: add a "grill me" teaching/review skill inspired by Antigravity-style scrutiny, so Joel and Mukthar can challenge product assumptions before implementation.
- [x] Define first implementation slice: visual-only Google Careers flow with approved mock data for this demo, two blocks, one connector, four run states, and Store right-side inspector.
- [ ] Get Mukthar technical review when available for the first implementation slice; Joel product approval is already sufficient to proceed.
- [ ] Walk through more real scenarios to identify the first fundamental block library.
- [ ] Walk through the Google Careers two-block workflow with Joel and Mukthar before defining Block Library v0 or Connector Model v0.

## Approved Immediate Shift 002 - Demoable Two-Block Web

Status: Joel approved after showing the demo to Fahim with clear positive feedback.

Product language direction:

- agents may be called `spiders`
- workflows may be called `webs`
- the first demo is a small web made from two blocks/spiders

Immediate scope:

- make the existing Google Careers two-block web demoable
- keep the demo focused on the two current blocks
- improve functionality before visual polish
- after functionality works, refine progress chips, blocks, connectors, and the right sidebar
- keep every feature cheap enough for a developer installing the Spider Rose SDK/CLI in a Linux terminal
- show Joel resource-use cost before implementing each feature
- remove the top-level Tools feature surface for now
- remove unrelated visible block clutter from the demo experience
- keep queued UI notes separate unless Joel explicitly approves each item for atomic-plan work
- create a specific GitHub, LinkedIn, and content creator outreach plan

Immediate code tasks:

- [x] Hide unrelated agent cards from the Workflow demo view.
- [x] Remove the top-level Tools tab, Tools panel, and `/tools` visual route for now.
- [x] Remove the agent detail Tools tab from the current demo UI for now.
- [x] Update tests so Tools is no longer treated as an active visual route.
- [x] Restart the local demo server after the UI change.
- [x] Remove the `hello` and `researcher` default agents from the current demo.
- [x] Make `google-careers-scraper` the only preloaded/default demo agent.
- [x] Remove zoom controls and zoom scaling from the canvas.
- [x] Clear stale `hello` and `researcher` cards from `workflow-layout.json`.
- [ ] Replace mock job results with a real Google Careers scrape path.
- [ ] Show a clear scrape failure state when Google Careers cannot be reached or parsed.
- [ ] Store the real scraped job records in the proposed JSONL path or a revised approved storage path.
- [ ] After real scrape works, refine progress chips.
- [ ] After real scrape works, refine the two blocks.
- [ ] After real scrape works, refine the connector.
- [ ] After real scrape works, refine the right sidebar.

Immediate planning tasks:

- [x] Add queued UI notes for movable blocks, delete behavior, refined links, data transfer, and floating inspector.
- [x] Create separate queued UI note file for workflow blocks.
- [x] Add demo/outreach plan covering GitHub, LinkedIn, and content creator outreach.
- [ ] Define demoable acceptance criteria for the two-block web.
- [ ] Draft the demo feedback questions for Fahim and the next audience group.
- [ ] Decide the minimum real scrape fields needed for demo: title, location, job link, level, and qualifications.
- [ ] Define the pre-implementation resource-use review format for Joel: network requests, runtime duration, disk writes, stored file size, dependency cost, retry behavior, and expected limits.
- [x] Add a resource-use note before approving the real Google Careers scrape implementation.

Demo audience:

- Fahim
- Alfeen
- Don
- Christie
- Prithvi
- Mubaris
- Pranav
- Joel Sam
- Gowri
- Athul
- Mevit
- Varsha
- Reshma
- Nithin Noushad
- Joel
- others

## Approved Implementation Slice 001 - Google Careers Visual Demo

Status: Joel approved for product direction; Mukthar technical review useful when available, but not a product blocker.

Scope:

- show two visual blocks: `Web Scraper: Google Careers` and `Store: Job Results`
- connect Web Scraper to Store
- use internal connector contract: `kind = data`, `payload_type = job_results`
- use non-technical connector wording in normal UI
- use four block states: Idle, Running, Success, Failed
- use mock job data only for this demo
- clicking Store opens a right-side inspector with saved path, counts, dedupe rule, and sample job links

Out of scope:

- real Google Careers scraping
- scheduler
- WhatsApp
- final storage decision
- deciding what information appears inside each grid block

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
- [x] Create product decision Q&A and ambiguous-question queue.
- [x] Capture first product direction decisions.
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

- [ ] Define terminal UI layout acceptance criteria after the terminal-versus-visual boundary is clearer.
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

Target: add visual connector edges as the first active workflow execution surface. Estimate: 35-55h.

Joel:

- [ ] Define supported edge labels for v1.
- [ ] Decide edge direction rules.
- [ ] Decide whether duplicate cards can connect to each other.
- [ ] Review canvas edge UX.

Mukthar:

- [ ] Add connector edges between workflow canvas blocks.
- [ ] Render directional arrows.
- [ ] Support edge labels.
- [ ] Persist edges in `workflow-layout.json`.
- [ ] Add edge edit/delete interactions.
- [ ] Make the first connector model executable for the Google Careers workflow path.
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
