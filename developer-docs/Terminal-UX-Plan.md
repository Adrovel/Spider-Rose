# Spider Rose Terminal UX Plan

Version: 0.1.0  
Status: Draft for Phase 1 hardening  
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
/exit
```

## First-Run Behavior

When the user runs `spiderrose` in a new folder:

1. Create `agents/`.
2. Create `memory/`.
3. Create `agents/researcher.md`.
4. Create `spider-rose.toml` with `default_agent = "researcher"`.
5. Print the project path.
6. Show the slash-command prompt.

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

## Visual Flow

Input:

```text
/visualise
```

Behavior:

- start the local server
- open the browser when possible
- show only agent creation/editing in Phase 1
- show where each agent file is stored

## Future Terminal Ideas

Archive these until workflows exist:

- Codex/Claude-style chat terminal where plain text is treated as a task
- slash commands remain reserved for app actions
- multiline input composer
- streaming output panels
- keyboard shortcuts for cancel, clear, history, and agent switching
- visible current agent/default project state
- `/new workflow <name>`
- `/connect <from> <to>`
- `/run workflow <name> <task>`
- `/logs`
- `/validate`
- `/doctor`
- command history
- tab completion
- project switcher
