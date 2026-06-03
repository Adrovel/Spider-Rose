# Spider Rose Terminal UX Plan

Version: 0.1.0  
Status: Active terminal UI plan  
Last updated: 2026-06-01

Purpose: define how `spiderrose` should feel in the terminal before adding workflow complexity.

## Terminal Principle

Running `spiderrose` should open the product, not show a command manual.

The shell uses slash commands because they are easy to remember, easy to copy, and do not require users to learn many top-level CLI commands.

## Phase 1 Commands

```text
spiderrose
```

Inside the shell:

```text
/visualise
/new agent <name>
/run <task>
/help
/recent
/menu
/clear
/exit
```

## Required Terminal UI

The terminal has the first stable app shape:

- header with current project path
- default agent indicator
- command response area
- three-row grey composer with only a terminal-native spider glyph as the input indicator
- rose-colored spider indicator and rose/web panel accents
- interactive multiline input that grows as content wraps or new lines are inserted
- background in-session history
- `/recent` command for showing terminal history on demand
- `/menu` slash command menu rendered from one shared command registry
- compact help text when `/help` is used

Composer behavior:

- no placeholder text is shown
- typing starts on the middle input row next to the spider indicator
- the grey composer area uses consistent spacing around the icon and text
- empty composer height is fixed at three rows and does not scale with terminal height
- the composer grows only with content, capped at twelve rows before scrolling
- Enter submits the current command; Esc+Enter inserts a new line in interactive terminals
- interactive terminals use prompt-toolkit for multiline input; non-interactive scripts use a compatible fallback prompt

Still required:

- persistent history saved after the shell exits
- richer input behavior after the basic shell is stable

In-session history means Spider Rose remembers commands, inputs, and compact responses while the current shell is open. It is stored quietly in memory, fetched as context when `/run` prepares a task, and shown to the user only when `/recent` is used. It is not written to disk yet.

Plain text can become a task for the default agent after the shell has a clear UI. Slash commands remain the reliable app-control layer.

## First-Run Behavior

When the user runs `spiderrose` in a new folder:

1. Create `agents/`.
2. Create `memory/`.
3. Create `agents/hello.md`.
4. Create `agents/researcher.md`.
5. Create `spider-rose.toml` with `default_agent = "researcher"`.
5. Print the project path.
6. Show the project header and slash-command prompt.

The user should not need a separate `init` command in Phase 1.

## Agent Creation Flow

Input:

```text
/new agent researcher
```

Output:

```text
Created agent agents/researcher.md
```

Storage:

```text
agents/researcher.md
```

New projects already include `researcher`, so user-created agents do not replace the default automatically unless the user changes the default in the visual editor.

New projects also include `hello` as a lightweight onboarding agent.

## Run Flow

Input:

```text
/run Search Nathan's LinkedIn
```

Rules:

- Treat everything after `/run ` as raw task text.
- Do not require shell-style quoting.
- Apostrophes and punctuation must work naturally.
- If no default agent exists, tell the user to create one.
- Render run output in a clear terminal panel.

## Visual Flow

Input:

```text
/visualise
```

Behavior:

- start the local server
- open the browser when possible
- show agent creation and editing
- show the workflow canvas
- support visual connector edges between agent cards
- show where each agent file is stored

## Future Terminal Ideas

Archive these until workflows exist:

- multiline input composer
- streaming output panels
- keyboard shortcuts for cancel, clear, history, and agent switching
- `/new workflow <name>`
- `/connect <from> <to>`
- `/run workflow <name> <task>`
- `/logs`
- `/validate`
- `/doctor`
- command history
- tab completion
- project switcher
