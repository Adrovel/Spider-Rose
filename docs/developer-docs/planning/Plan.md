# Spider Rose Plan

Version: 0.1.0  
Status: Working implementation plan  
Last updated: 2026-06-05

## Planning Assumptions

Spider Rose is local-first with a terminal entry point and a visual workflow grid as the intended active execution surface.

Implementation is atomic-plan gated. No feature code should be added until Joel and Mukthar approve the relevant atomic-plan item.

Team capacity:

| Person | Capacity | Main lane |
|---|---:|---|
| Joel | 20 hours/week | product direction, architecture, terminal UX review, release quality |
| Mukthar | 20 hours/week | implementation, tests, visual polish, docs support |

Combined capacity is 40 hours/week. Each phase is estimated in focused engineering hours, not calendar hours. Calendar estimates assume both contributors can work without blocking each other.

Immediate phase shift:

- Make the current two-block Google Careers workflow demoable.
- Use the current two blocks as the first small web.
- Treat agents as possible **spiders** and workflows as possible **webs** in product language.
- Improve functionality first, especially real Google Careers scraping.
- After functionality works, refine UI component by component: progress chips, blocks, connectors, and the right sidebar.
- Demo to Fahim first, then Alfeen, Don, Christie, Prithvi, Mubaris, Pranav, Joel Sam, Gowri, Athul, Mevit, Varsha, Reshma, Nithin Noushad, Joel, and others.
- Keep GitHub, LinkedIn, and content creator outreach focused on the demo story.

Features not active now:

- run logs and run artifacts
- validation command
- canvas sticky notes and inspector
- MCP execution
- top-level Tools surface

## Publicity Trigger

Publicise Spider Rose when the plan reaches 40% completion.

At 40%, the app should have:

- local project initialization
- terminal entry shell
- usable terminal UI
- Markdown agent creation
- default-agent run path
- local visual editor
- visual workflow grid with fundamental block and connector direction

Marketing reminder at 40%:

- prepare a short demo video or GIF
- write a concise README pitch
- publish screenshots of terminal UI and visual canvas
- share the repo with a small developer audience first
- collect feedback before broader launch

Current demo/outreach plan: [Demo And Outreach Plan](./Demo-and-Outreach-Plan.md)

## Phase Summary

| Phase | Focus | Estimate | Calendar at 40h/week | Completion weight |
|---|---|---:|---:|---:|
| 0 | Product spine and existing MVP scaffold | 8-12h remaining | 2-3 days | 15% |
| 1A | Demoable two-block web | 8-16h | 1-2 days | immediate |
| 1 | Terminal UI | 40-55h | 1-1.5 weeks | 25% |
| 2 | Visual workflow blocks and typed connector edges | 35-55h | 1-1.5 weeks | 20% |
| 3 | Agent editing and defaults | 25-35h | 1 week | 15% |
| 4 | Custom agent library and templates | 35-50h | 1-1.5 weeks | 15% |
| 5 | Later runtime path | 50-80h | 1.5-2 weeks | 10% |

40% completion lands after Phase 1 is complete and Phase 2 has started or after Phase 2 is partially complete.

## Phase 0 - Product Spine

Goal: make the smallest terminal and visual app loop work end-to-end.

Exit criteria:

- `spiderrose` launches the terminal shell.
- `/visualise` launches a local visual agent editor.
- `/new agent <name>` creates Markdown agents.
- `/run <task>` runs the default agent.
- A friend can use one copyable command after the GitHub repo is pushed.

Remaining estimate: 8-12h.

Joel lane:

- confirm public repo/readme direction
- review install and first-run story

Mukthar lane:

- verify clean install
- fix packaging or first-run bugs

## Phase 1 - Terminal UI

Goal: make `spiderrose` feel like a usable terminal app, not only a raw prompt loop.

Work:

- persistent terminal screen layout
- visible message history
- stable command input area
- current project and default agent context
- clear responses for slash commands
- improve error messages
- add more parser tests
- add packaging smoke test
- add release checklist

Estimate: 40-55h.

Joel lane:

- define terminal UI acceptance criteria
- review copy, command behavior, and UX fit

Mukthar lane:

- implement terminal layout
- wire message history and input behavior
- add parser and display tests

## Phase 1A - Demoable Two-Block Web

Goal: make the current Google Careers two-block web demoable before expanding the product.

Work:

- keep the demo focused on the two existing blocks
- replace mock results with real Google Careers scraping
- handle scrape failure visibly and honestly
- keep the feature cheap for a developer installing the SDK/CLI in a Linux terminal
- show Joel the resource-use cost before implementation approval
- remove the top-level Tools feature surface for now
- keep unrelated agent cards out of the demo view
- after real scraping works, improve progress chips
- after real scraping works, improve the two blocks
- after real scraping works, improve the connector
- after real scraping works, improve the right sidebar
- prepare GitHub, LinkedIn, and content creator demo material

Estimate: 8-16h.

Joel lane:

- review the demo story
- decide user-facing words for spiders and webs
- approve what counts as demoable
- prepare demo audience feedback questions

Mukthar lane:

- keep the UI focused on the two-block web
- polish block/link/inspector behavior after approval
- keep tests updated

## Phase 2 - Visual Workflow Blocks And Edges

Goal: define and begin the active visual workflow model with reusable fundamental blocks and typed connector edges.

Work:

- first fundamental block library: Input, Website Source, Web Scraper, Extractor, Store/RAG, Scheduler, Formatter, WhatsApp Sender, Agent
- typed connector semantics: data, trigger, or both
- connector edges between workflow blocks
- directional edge rendering
- edge persistence in the canvas layout model
- edge edit/delete interactions
- Google Careers learning workflow as the first approved education scenario

Current bridge:

- `/workflow` now exists as a movable canvas.
- Cards can be positioned before executable workflow runtime is introduced.
- Edges should be shaped for active execution semantics, but runtime implementation still needs atomic-plan approval.

Estimate: 35-55h.

Joel lane:

- decide first fundamental blocks and connector semantics
- review canvas behavior

Mukthar lane:

- implement approved block-to-block connections
- persist edges in `workflow-layout.json`
- add edit/delete behavior for edges

## Phase 3 - Agent Editing and Defaults

Goal: make agent editing and default-agent control complete enough for daily use.

Work:

- agent detail sidebar
- edit name, role, goal, instructions, tools, and expected output
- save changes to Markdown agent files
- visual default-agent selector
- `/default <agent>` command
- update `spider-rose.toml`

Estimate: 25-35h.

Joel lane:

- define final Markdown agent fields
- review default-agent UX

Mukthar lane:

- implement sidebar form and save flow
- implement default command and selector
- add focused tests

## Phase 4 - Custom Agent Library and Templates

Goal: make agents reusable across projects before real workflow execution exists.

Work:

- local custom agent library
- save project agents into the library
- create project agents from library entries
- browse library entries in the visual app
- list library entries in the terminal
- built-in templates for Researcher, Planner, Coder, Reviewer, Summarizer, Debugger
- `/new agent <name> --template <template>` command
- `/new agent <name> --from-library <library-agent>` command

Estimate: 35-50h.

Joel lane:

- define library boundaries and naming rules
- define template content
- review library UX and demo story

Mukthar lane:

- implement local library storage
- implement library list/create/import commands
- implement visual library browser
- implement templates and command parsing

## Phase 5 - Later Runtime Path

Goal: execute workflows through LangGraph while keeping Markdown agents simple.

Work:

- real workflow execution
- compile YAML workflow into LangGraph `StateGraph`
- support LangGraph Python workflow discovery
- document how LangGraph users opt in
- consider MCP tool execution after the base app is stable
- consider local RAG after runs and file access are mature

Estimate: 50-80h.
