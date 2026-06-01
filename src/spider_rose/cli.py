from __future__ import annotations

from pathlib import Path
import webbrowser

import typer
from rich.console import Console

from spider_rose.project import ProjectError, create_agent, find_or_init_project_root
from spider_rose.runtime import run_default_agent


app = typer.Typer(help="Spider Rose: terminal-first agent creation and execution.")
console = Console()


@app.callback()
def main() -> None:
    """Create agents visually or run the default agent from the terminal."""


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
    console.print(f"[green]Starting Spider Rose[/green] {url}")
    webbrowser.open(url)
    uvicorn.run("spider_rose.server:create_app", host=host, port=port, factory=True)


def _root() -> Path:
    try:
        return find_or_init_project_root()
    except ProjectError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


def _entrypoint() -> None:
    try:
        app()
    except ProjectError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


if __name__ == "__main__":
    _entrypoint()
