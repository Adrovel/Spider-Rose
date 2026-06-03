# Mukthar TUI Working Start

Version: 0.1.0  
Status: Active learning start  
Last updated: 2026-06-03

Purpose: Mukthar should learn terminal user interfaces in a nuanced and fundamental manner. He should be able to explain the concepts, use the jargon correctly, make implementation decisions, and teach the same ideas to another developer.

## Outcome

Mukthar is not ready when he can only change colors, add commands, or copy examples. He is ready when he can explain why a terminal interaction works, what constraints the terminal creates, what libraries are responsible for each layer, and how Spider Rose should behave when the terminal is interactive, non-interactive, narrow, slow, or misused.

## Fundamentals To Learn First

1. Terminal model
   - What stdin, stdout, and stderr are.
   - Difference between a command-line interface and an interactive shell.
   - Difference between a normal terminal, redirected input, and a non-interactive script.
   - Why terminal width, wrapping, cursor position, and line editing matter.

2. CLI command model
   - How top-level commands differ from in-shell slash commands.
   - How arguments, raw text, quoting, escaping, and punctuation behave.
   - Why `/run Search Nathan's LinkedIn` should treat everything after `/run ` as task text.
   - Why command parsing must be predictable before it is clever.

3. TUI interaction model
   - Prompt, composer, panel, menu, history, completion, and error states.
   - Keyboard behavior: Enter, multiline entry, cancellation, completion, and escape paths.
   - How users recover when they type the wrong command.
   - Why a terminal app must remain usable without visual decoration.

4. Rendering model
   - What Rich renders and what it does not own.
   - What prompt-toolkit owns: prompt session, line editing, key bindings, completion, continuation prompt.
   - Why layout must survive different terminal widths and fonts.
   - Why color should communicate state but not carry meaning alone.

5. Product model
   - Spider Rose opens as a product when `spiderrose` runs.
   - Slash commands are the reliable app-control layer.
   - Plain text is not app control until the shell intentionally supports it.
   - Terminal behavior should stay stable before workflow complexity is added.

## Spider Rose Code Map

- `src/spider_rose/cli.py` owns the terminal entry point, top-level Typer commands, interactive shell loop, slash command handling, Rich panels, prompt-toolkit composer, completion, and recent history rendering.
- `docs/developer-docs/implementation/Terminal-UX-Plan.md` defines the intended terminal behavior.
- `tests/test_cli_flow.py` protects CLI smoke behavior and command handling.
- `pyproject.toml` exposes the installed command as `spiderrose`.

## First Working Path

Mukthar should work through these in order:

1. Run `spiderrose` locally and use `/help`, `/menu`, `/new agent test`, `/run explain this app`, `/recent`, `/clear`, and `/exit`.
2. Explain out loud what happens from typing `spiderrose` to seeing the first shell prompt.
3. Read only the CLI path in `src/spider_rose/cli.py`: app callback, `shell()`, `handle_slash_command()`, `_read_composer_input()`, and `_render_command_menu()`.
4. Trace one command end to end: `/run hello`. Explain input parsing, history update, runtime call, and panel rendering.
5. Break one command intentionally and document the error behavior: empty `/run`, unknown command, plain text without slash, narrow terminal width.
6. Add or modify one low-risk command only after explaining where it belongs in the command registry and how it should appear in `/help`, `/menu`, and typeahead.
7. Teach the flow back to Joel or another developer in 10 minutes without reading the code.

## Vocabulary He Should Be Able To Teach

- CLI
- TUI
- interactive shell
- top-level command
- slash command
- command registry
- raw task text
- parser
- prompt session
- composer
- continuation prompt
- key binding
- completion
- panel
- terminal width
- stdout and stderr
- non-interactive fallback
- in-session history

## Teaching Checkpoint

Mukthar should be able to answer these without guessing:

- Why does Spider Rose use `spiderrose` first and slash commands inside the app?
- What is the difference between `spiderrose run "task"` and `/run task` inside the shell?
- Why should `/run Search Nathan's LinkedIn` not rely on shell-style quoting inside the interactive shell?
- What does prompt-toolkit handle that Rich does not handle?
- What does Rich handle that prompt-toolkit does not handle?
- What should happen when a terminal is too narrow?
- What should happen when input is non-interactive?
- Where does a new command need to be registered so `/help`, `/menu`, and typeahead stay consistent?

## Definition Of Ready

Mukthar is ready to own deeper TUI work when he can:

- implement a small terminal behavior without breaking the current command model
- explain the user-facing behavior before explaining the code
- write or update a test for the behavior
- update terminal docs when behavior changes
- teach the same concept to someone else using Spider Rose examples
