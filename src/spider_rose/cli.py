from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
import shlex
import socket
import sys
import webbrowser

import typer
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from spider_rose.project import ProjectError, create_agent, find_or_init_project_root, get_default_agent
from spider_rose.runtime import run_default_agent


app = typer.Typer(help="Spider Rose: terminal-first agent creation and execution.")
console = Console()
ROSE = "#d9829b"
ROSE_BLOOM = "#f0b8c8"
SPIDER_ROSE = ROSE_BLOOM
COMMAND_ROSE = "#c76180"
ROSE_SHADOW = "#7a334a"
PETAL = "#f2d7df"
COBWEB = "#b9aab1"
THORN = "#7da08b"
VINE = "#8fab9a"
NIGHT_ROSE = "#241920"
COMPOSER_WIDTH = 78
COMPOSER_MIN_HEIGHT = 3
COMPOSER_MAX_HEIGHT = 12
COMPOSER_INPUT_MAX_HEIGHT = COMPOSER_MAX_HEIGHT - 2
COMPOSER_BLANK_LINE = " " * COMPOSER_WIDTH
INPUT_PROMPT = "\n".join(
    [
        COMPOSER_BLANK_LINE,
        COMPOSER_BLANK_LINE,
        f"[bold {SPIDER_ROSE}]  🕷  [/bold {SPIDER_ROSE}]",
    ]
)
HISTORY_LIMIT = 6


@dataclass(frozen=True)
class ShellMessage:
    role: str
    title: str
    body: str


@dataclass(frozen=True)
class SlashCommand:
    usage: str
    description: str
    featured: bool = False


SLASH_COMMANDS: tuple[SlashCommand, ...] = (
    SlashCommand("/run <task>", "Run the default Markdown agent.", featured=True),
    SlashCommand("/recent", "Show the current terminal session history.", featured=True),
    SlashCommand("/menu", "Open the slash command menu.", featured=True),
    SlashCommand("/new agent <name>", "Create a local Markdown agent."),
    SlashCommand("/visualise", "Open the local visual editor."),
    SlashCommand("/clear", "Clear the terminal and redraw the shell header."),
    SlashCommand("/help", "Show command help."),
    SlashCommand("/exit", "Close Spider Rose."),
)


class SlashCommandCompleter(Completer):
    """Suggest registered slash commands while the user types the command token."""

    def get_completions(self, document: Document, complete_event) -> Iterator[Completion]:
        token = document.text_before_cursor
        if not token.startswith("/") or any(character.isspace() for character in token):
            return

        for command in SLASH_COMMANDS:
            command_name = _command_name(command.usage)
            if command_name.startswith(token):
                yield Completion(
                    _completion_text(command.usage),
                    start_position=-len(token),
                    display=command.usage,
                    display_meta=command.description,
                )


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Open Spider Rose when no subcommand is provided."""
    if ctx.invoked_subcommand is None:
        interactive_shell()


@app.command("new")
def new(kind: str, name: str, force: bool = False) -> None:
    """Create a new agent, for example `spiderrose new agent google-careers-scraper`."""
    if kind != "agent":
        raise typer.BadParameter("Phase 1 only supports `spiderrose new agent <name>`.")
    root = _root()
    path = create_agent(root, name, force=force)
    console.print(f"[green]Created agent[/green] {path.relative_to(root)}")


@app.command()
def run(task: str = typer.Argument(..., help="Task to send to the default agent.")) -> None:
    """Run the default agent against a terminal task."""
    root = _root()
    console.print(_response_panel(run_default_agent(root, task), "Run"))


@app.command()
def visualise(host: str = "127.0.0.1", port: int = 3000) -> None:
    """Start the local visual agent editor."""
    root = _root()
    import uvicorn

    url = f"http://{host}:{port}"
    if _server_is_running(host, port):
        console.print(f"[yellow]Spider Rose is already running[/yellow] {url}")
        webbrowser.open(url)
        return
    console.print(f"[green]Starting Spider Rose[/green] {url}")
    webbrowser.open(url)
    uvicorn.run("spider_rose.server:create_app", host=host, port=port, factory=True)


def interactive_shell() -> None:
    """Run the slash-command terminal shell."""
    root = _root()
    history: list[ShellMessage] = []
    _render_shell_header(root)
    while True:
        try:
            raw_command = _read_composer_input().strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            return

        if not raw_command:
            continue
        if not raw_command.startswith("/"):
            history.append(ShellMessage("User", "Input", raw_command))
            message = "Use slash commands. Try /help."
            console.print(_themed_error_panel(message, "Thorn path"))
            history.append(ShellMessage("System", "Command needed", message))
            continue
        if raw_command in {"/exit", "/quit"}:
            console.print("[dim]Closed Spider Rose.[/dim]")
            return
        history.append(ShellMessage("User", "Command", raw_command))
        response = handle_slash_command(raw_command, history)
        if response:
            history.append(response)


def handle_slash_command(raw_command: str, history: list[ShellMessage] | None = None) -> ShellMessage | None:
    """Execute one slash command inside the interactive shell."""
    if raw_command.startswith("/run "):
        task = raw_command[len("/run ") :].strip()
        if not task:
            message = "Usage: /run <task>"
            console.print(_themed_error_panel(message, "Petal missing"))
            return ShellMessage("System", "Usage", message)
        root = _root()
        result = _run_with_session_context(root, task, _history_before_current_command(history, raw_command))
        console.print(_response_panel(result, "Run"))
        return ShellMessage("Run", "Default agent", task)

    try:
        parts = shlex.split(raw_command[1:])
    except ValueError as exc:
        message = str(exc)
        console.print(_themed_error_panel(message, "Vine snag"))
        return ShellMessage("System", "Parse error", message)

    if not parts:
        return None

    command = parts[0]
    args = parts[1:]

    if command == "help":
        _render_command_menu("Commands")
        return ShellMessage("System", "Help", "Showed command list.")

    if command == "menu":
        _render_command_menu("Slash Command Menu")
        return ShellMessage("System", "Menu", "Showed slash command menu.")

    if command == "recent":
        _render_history(_history_before_current_command(history, raw_command))
        return ShellMessage("System", "Recent", "Showed terminal history.")

    if command == "clear":
        console.clear()
        _render_shell_header(_root())
        return ShellMessage("System", "Clear", "Redrew the terminal shell.")

    if command == "visualise":
        visualise()
        return ShellMessage("System", "Visualise", "Opened the local visual editor.")

    if command == "new":
        if len(args) < 2 or args[0] != "agent":
            message = "Usage: /new agent <name>"
            console.print(_themed_error_panel(message, "Petal missing"))
            return ShellMessage("System", "Usage", message)
        name = " ".join(args[1:])
        root = _root()
        path = create_agent(root, name)
        relative_path = path.relative_to(root)
        console.print(f"[green]Created agent[/green] {relative_path}")
        return ShellMessage("System", "Created agent", str(relative_path))

    if command == "run":
        if not args:
            message = "Usage: /run <task>"
            console.print(_themed_error_panel(message, "Petal missing"))
            return ShellMessage("System", "Usage", message)
        task = " ".join(args)
        root = _root()
        result = _run_with_session_context(root, task, _history_before_current_command(history, raw_command))
        console.print(_response_panel(result, "Run"))
        return ShellMessage("Run", "Default agent", task)

    message = f"Unknown command: /{command}\nRun /help to see available commands."
    console.print(_themed_error_panel(message, "Thorned command"))
    return ShellMessage("System", "Unknown command", f"/{command}")


def _render_shell_header(root: Path) -> None:
    default_agent = _default_agent_label(root)
    title = Text("🕷 Spider Rose", style=f"bold {ROSE_BLOOM}")
    title.append("  🕸 local agent web", style="dim")
    body = Table.grid(padding=(0, 2))
    body.add_column(style="dim", no_wrap=True)
    body.add_column(style="white")
    body.add_row("Project", str(root))
    body.add_row("Default", default_agent)
    body.add_row("Theme", "rose web shell")
    body.add_row("Try", _featured_command_text())
    console.print(Panel(body, title=title, border_style=ROSE, padding=(1, 2)))


def _render_command_menu(title: str) -> None:
    table = Table(show_header=False, box=None, padding=(0, 2), expand=False)
    table.add_column("Petal", style=THORN, no_wrap=True)
    table.add_column("Command", no_wrap=True)
    table.add_column("Description", style=COBWEB)
    for command in SLASH_COMMANDS:
        table.add_row("❧", _command_usage_text(command.usage), command.description)

    panel_title = Text("🕷 ", style=f"bold {ROSE_BLOOM}")
    panel_title.append(title, style=f"bold {PETAL}")
    panel_title.append("  🕸 rose web", style=COBWEB)
    console.print(Panel(table, title=panel_title, border_style=ROSE_SHADOW, padding=(1, 2)))


def _command_usage_text(usage: str) -> Text:
    command, _, args = usage.partition(" ")
    text = Text(command, style=f"bold {COMMAND_ROSE}")
    if args:
        text.append(f" {args}", style=COBWEB)
    return text


def _command_name(usage: str) -> str:
    return usage.split()[0]


def _completion_text(usage: str) -> str:
    if usage.startswith("/new agent "):
        return "/new agent "
    return _command_name(usage)


def _read_composer_input() -> str:
    if not sys.stdin.isatty():
        return console.input(INPUT_PROMPT)
    try:
        return _read_prompt_toolkit_input()
    except ImportError:
        return console.input(INPUT_PROMPT)


def _read_prompt_toolkit_input() -> str:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.shortcuts import CompleteStyle
    from prompt_toolkit.shortcuts import print_formatted_text
    from prompt_toolkit.styles import Style

    bindings = KeyBindings()

    @bindings.add("enter")
    def _(event) -> None:
        event.app.exit(result=event.app.current_buffer.text)

    @bindings.add("escape", "enter")
    def _(event) -> None:
        event.app.current_buffer.insert_text("\n")

    @bindings.add("c-c")
    def _(event) -> None:
        event.app.exit(exception=KeyboardInterrupt)

    @bindings.add("/")
    def _(event) -> None:
        event.app.current_buffer.insert_text("/")
        event.app.current_buffer.start_completion(select_first=False)

    style = Style.from_dict(
        {
            "completion-menu.completion": f"bg:{NIGHT_ROSE} {PETAL}",
            "completion-menu.completion.current": f"bg:{ROSE_SHADOW} #ffffff bold",
            "completion-menu.meta.completion": f"bg:{NIGHT_ROSE} {COBWEB}",
            "completion-menu.meta.completion.current": f"bg:{ROSE_SHADOW} {PETAL}",
            "composer-icon": f"{SPIDER_ROSE} bold",
            "composer-input": "#f5f5f5",
            "scrollbar.background": f"bg:{NIGHT_ROSE}",
            "scrollbar.button": f"bg:{ROSE_SHADOW}",
        }
    )
    blank_line = HTML(" ")
    print_formatted_text(blank_line, style=style)
    session = PromptSession(
        multiline=True,
        wrap_lines=True,
        key_bindings=bindings,
        style=style,
        completer=SlashCommandCompleter(),
        complete_while_typing=True,
        complete_style=CompleteStyle.COLUMN,
    )
    result = session.prompt(
        HTML('<composer-icon>  🕷  </composer-icon><composer-input> </composer-input>'),
        prompt_continuation=HTML("<composer-input>       </composer-input>"),
    )
    print_formatted_text(blank_line, style=style)
    return result


def _featured_command_text() -> str:
    return "  ".join(command.usage for command in SLASH_COMMANDS if command.featured)


def _render_history(history: list[ShellMessage]) -> None:
    if not history:
        console.print(_message_panel("No terminal history yet.", "Recent", "cyan"))
        return
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Role", style="bold white", no_wrap=True)
    table.add_column("Title", style="green", no_wrap=True)
    table.add_column("Body", style="dim")
    for message in history[-HISTORY_LIMIT:]:
        table.add_row(message.role, message.title, _compact_history_body(message.body))
    console.print(Panel(table, title="Recent", border_style="cyan", padding=(1, 2)))


def _run_with_session_context(root: Path, task: str, history: list[ShellMessage] | None) -> str:
    result = run_default_agent(root, task)
    context = _session_context_text(history or [])
    if not context:
        return result
    return f"""{result}
Session Context:
{context}
"""


def _session_context_text(history: list[ShellMessage]) -> str:
    useful_history = [
        message
        for message in history
        if message.role in {"User", "Run", "System"} and message.title not in {"Recent", "Help", "Clear"}
    ]
    if not useful_history:
        return ""
    return "\n".join(
        f"- {message.role} {message.title}: {_compact_history_body(message.body, limit=96)}"
        for message in useful_history[-HISTORY_LIMIT:]
    )


def _history_before_current_command(history: list[ShellMessage] | None, raw_command: str) -> list[ShellMessage]:
    if not history:
        return []
    if history[-1].role == "User" and history[-1].body == raw_command:
        return history[:-1]
    return history


def _compact_history_body(body: str, limit: int = 88) -> str:
    compact = " ".join(body.split())
    if len(compact) <= limit:
        return compact
    return f"{compact[: limit - 3]}..."


def _response_panel(message: str, title: str) -> Panel:
    return Panel(message.strip(), title=f"🌹 {title}", border_style=ROSE, padding=(1, 2))


def _message_panel(message: str, title: str, border_style: str) -> Panel:
    return Panel(message, title=title, border_style=border_style, padding=(1, 2))


def _themed_error_panel(message: str, title: str) -> Panel:
    body = Text("❧ ", style=f"bold {THORN}")
    body.append(message, style=PETAL)
    return Panel(body, title=f"🌿 {title}", border_style=VINE, padding=(1, 2))


def _default_agent_label(root: Path) -> str:
    try:
        return get_default_agent(root)
    except ProjectError:
        return "not set"


def _root() -> Path:
    try:
        return find_or_init_project_root()
    except ProjectError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


def _server_is_running(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.25):
            return True
    except OSError:
        return False


def _entrypoint() -> None:
    try:
        app()
    except ProjectError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


if __name__ == "__main__":
    _entrypoint()
