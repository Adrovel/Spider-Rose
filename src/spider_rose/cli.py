from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shlex
import socket
import webbrowser

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from spider_rose.project import ProjectError, create_agent, find_or_init_project_root, get_default_agent
from spider_rose.runtime import run_default_agent


app = typer.Typer(help="Spider Rose: terminal-first agent creation and execution.")
console = Console()
INPUT_PROMPT = "[bold black on white] INPUT [/bold black on white] [bold white]🕷[/bold white] [bold green]›[/bold green] "
HISTORY_LIMIT = 6


@dataclass(frozen=True)
class ShellMessage:
    role: str
    title: str
    body: str


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Open Spider Rose when no subcommand is provided."""
    if ctx.invoked_subcommand is None:
        interactive_shell()


@app.command("new")
def new(kind: str, name: str, force: bool = False) -> None:
    """Create a new agent, for example `spiderrose new agent researcher`."""
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
            raw_command = console.input(INPUT_PROMPT).strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            return

        if not raw_command:
            continue
        if not raw_command.startswith("/"):
            history.append(ShellMessage("User", "Input", raw_command))
            message = "Use slash commands. Try /help."
            console.print(_message_panel(message, "Command needed", "yellow"))
            history.append(ShellMessage("System", "Command needed", message))
            _render_history(history)
            continue
        if raw_command in {"/exit", "/quit"}:
            console.print("[dim]Closed Spider Rose.[/dim]")
            return
        history.append(ShellMessage("User", "Command", raw_command))
        response = handle_slash_command(raw_command)
        if response:
            history.append(response)
        _render_history(history)


def handle_slash_command(raw_command: str) -> ShellMessage | None:
    """Execute one slash command inside the interactive shell."""
    if raw_command.startswith("/run "):
        task = raw_command[len("/run ") :].strip()
        if not task:
            message = "Usage: /run <task>"
            console.print(_message_panel(message, "Usage", "red"))
            return ShellMessage("System", "Usage", message)
        root = _root()
        result = run_default_agent(root, task)
        console.print(_response_panel(result, "Run"))
        return ShellMessage("Run", "Default agent", task)

    try:
        parts = shlex.split(raw_command[1:])
    except ValueError as exc:
        message = str(exc)
        console.print(_message_panel(message, "Parse error", "red"))
        return ShellMessage("System", "Parse error", message)

    if not parts:
        return None

    command = parts[0]
    args = parts[1:]

    if command == "help":
        _render_help()
        return ShellMessage("System", "Help", "Showed command list.")

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
            console.print(_message_panel(message, "Usage", "red"))
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
            console.print(_message_panel(message, "Usage", "red"))
            return ShellMessage("System", "Usage", message)
        task = " ".join(args)
        root = _root()
        result = run_default_agent(root, task)
        console.print(_response_panel(result, "Run"))
        return ShellMessage("Run", "Default agent", task)

    message = f"Unknown command: /{command}\nRun /help to see available commands."
    console.print(_message_panel(message, "Unknown command", "red"))
    return ShellMessage("System", "Unknown command", f"/{command}")


def _render_shell_header(root: Path) -> None:
    default_agent = _default_agent_label(root)
    title = Text("Spider Rose", style="bold white")
    title.append("  local agent workspace", style="dim")
    body = Table.grid(padding=(0, 2))
    body.add_column(style="dim", no_wrap=True)
    body.add_column(style="white")
    body.add_row("Project", str(root))
    body.add_row("Default", default_agent)
    body.add_row("Try", "/run <task>  /new agent <name>  /visualise  /help")
    console.print(Panel(body, title=title, border_style="white", padding=(1, 2)))


def _render_help() -> None:
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Command", style="bold white", no_wrap=True)
    table.add_column("Description", style="dim")
    table.add_row("/run <task>", "Run the default Markdown agent.")
    table.add_row("/new agent <name>", "Create a local Markdown agent.")
    table.add_row("/visualise", "Open the local visual editor.")
    table.add_row("/clear", "Clear the terminal and redraw the shell header.")
    table.add_row("/exit", "Close Spider Rose.")
    console.print(Panel(table, title="Commands", border_style="white", padding=(1, 2)))


def _render_history(history: list[ShellMessage]) -> None:
    if not history:
        return
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Role", style="bold white", no_wrap=True)
    table.add_column("Title", style="green", no_wrap=True)
    table.add_column("Body", style="dim")
    for message in history[-HISTORY_LIMIT:]:
        table.add_row(message.role, message.title, _compact_history_body(message.body))
    console.print(Panel(table, title="Recent", border_style="cyan", padding=(1, 2)))


def _compact_history_body(body: str, limit: int = 88) -> str:
    compact = " ".join(body.split())
    if len(compact) <= limit:
        return compact
    return f"{compact[: limit - 3]}..."


def _response_panel(message: str, title: str) -> Panel:
    return Panel(message.strip(), title=title, border_style="green", padding=(1, 2))


def _message_panel(message: str, title: str, border_style: str) -> Panel:
    return Panel(message, title=title, border_style=border_style, padding=(1, 2))


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
