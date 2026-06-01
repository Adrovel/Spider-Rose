from __future__ import annotations

from pathlib import Path
import shlex
import socket
import webbrowser

import typer
from rich.console import Console

from spider_rose.project import ProjectError, create_agent, find_or_init_project_root
from spider_rose.runtime import run_default_agent


app = typer.Typer(help="Spider Rose: terminal-first agent creation and execution.")
console = Console()


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
    console.print(run_default_agent(root, task))


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
    _root()
    console.print("[bold]Spider Rose[/bold]")
    console.print("Use /visualise, /new agent <name>, /run <task>, /help, or /exit.")
    while True:
        try:
            raw_command = input("spiderrose> ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            return

        if not raw_command:
            continue
        if not raw_command.startswith("/"):
            console.print("[yellow]Use slash commands. Try /help.[/yellow]")
            continue
        if raw_command in {"/exit", "/quit"}:
            return
        handle_slash_command(raw_command)


def handle_slash_command(raw_command: str) -> None:
    """Execute one slash command inside the interactive shell."""
    if raw_command.startswith("/run "):
        task = raw_command[len("/run ") :].strip()
        if not task:
            console.print("[red]Usage: /run <task>[/red]")
            return
        run(task)
        return

    try:
        parts = shlex.split(raw_command[1:])
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return

    if not parts:
        return

    command = parts[0]
    args = parts[1:]

    if command == "help":
        console.print("Commands:")
        console.print("  /visualise")
        console.print("  /new agent <name>")
        console.print("  /run <task>")
        console.print("  /exit")
        return

    if command == "visualise":
        visualise()
        return

    if command == "new":
        if len(args) < 2 or args[0] != "agent":
            console.print("[red]Usage: /new agent <name>[/red]")
            return
        new("agent", " ".join(args[1:]))
        return

    if command == "run":
        if not args:
            console.print("[red]Usage: /run <task>[/red]")
            return
        run(" ".join(args))
        return

    console.print(f"[red]Unknown command: /{command}[/red]")


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
