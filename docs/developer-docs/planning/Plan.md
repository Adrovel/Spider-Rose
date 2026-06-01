# Spider Rose Plan

Version: 0.1.0  
Status: Working implementation plan  
Last updated: 2026-06-01

## Planning Assumptions

Spider Rose is local-first and terminal-first.

Team capacity:

| Person | Capacity | Main lane |
|---|---:|---|
| Joel | 20 hours/week | product direction, architecture, terminal UX review, release quality |
| Mukthar | 20 hours/week | implementation, tests, visual polish, docs support |

Combined capacity is 40 hours/week. Each phase is estimated in focused engineering hours, not calendar hours. Calendar estimates assume both contributors can work without blocking each other.

Features not active now:

- run logs and run artifacts
- validation command
- canvas sticky notes and inspector
- RAG
- MCP execution

## Publicity Trigger

Publicise Spider Rose when the plan reaches 40% completion.

At 40%, the app should have:

- local project initialization
- terminal-first shell
- usable terminal UI
- Markdown agent creation
- default-agent run path
- local visual editor
- workflow canvas with basic visual flow

Marketing reminder at 40%:

- prepare a short demo video or GIF
- write a concise README pitch
- publish screenshots of terminal UI and visual canvas
- share the repo with a small developer audience first
- collect feedback before broader launch

## Phase Summary

| Phase | Focus | Estimate | Calendar at 40h/week | Completion weight |
|---|---|---:|---:|---:|
| 0 | Product spine and existing MVP scaffold | 8-12h remaining | 2-3 days | 15% |
| 1 | Terminal UI | 40-55h | 1-1.5 weeks | 25% |
| 2 | Visual flow edges | 30-45h | 1 week | 20% |
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

## Phase 2 - Visual Flow Edges

Goal: show intended flow between agents on the visual canvas.

Work:

- connector edges between agent cards
- directional edge rendering
- edge persistence in the canvas layout model
- edge edit/delete interactions
- default workflow selection

Current bridge:

- `/workflow` now exists as a movable planning canvas.
- Cards can be positioned before execution is introduced.
- Edges should show planned flow only; they should not execute workflows yet.

Estimate: 30-45h.

Joel lane:

- decide edge labels and flow semantics
- review canvas behavior

Mukthar lane:

- implement card-to-card connections
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
