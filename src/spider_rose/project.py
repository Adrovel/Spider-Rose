from __future__ import annotations

import os
from pathlib import Path
import tomllib

from spider_rose.agents import default_agent_markdown, slugify_agent_name


CONFIG_FILE = "spider-rose.toml"


class ProjectError(RuntimeError):
    """Raised when the current directory is not a valid Spider Rose project."""


def find_project_root(start: Path | None = None) -> Path:
    override = os.environ.get("SPIDER_ROSE_PROJECT_ROOT", "").strip()
    if override:
        root = Path(override).expanduser().resolve()
        if (root / CONFIG_FILE).exists():
            return root
        raise ProjectError(f"Missing {CONFIG_FILE} at SPIDER_ROSE_PROJECT_ROOT: {root}")

    current = (start or Path.cwd()).resolve()
    for path in (current, *current.parents):
        if (path / CONFIG_FILE).exists():
            return path
    raise ProjectError("No spider-rose.toml found.")


def find_or_init_project_root(start: Path | None = None) -> Path:
    override = os.environ.get("SPIDER_ROSE_PROJECT_ROOT", "").strip()
    if override:
        root = Path(override).expanduser().resolve()
        if not (root / CONFIG_FILE).exists():
            init_project(root)
        return root

    try:
        return find_project_root(start)
    except ProjectError:
        root = (start or Path.cwd()).resolve()
        init_project(root)
        return root


def init_project(path: Path, force: bool = False) -> list[Path]:
    root = path.resolve()
    created: list[Path] = []
    for directory in ["agents", "memory"]:
        target = root / directory
        target.mkdir(parents=True, exist_ok=True)
        created.append(target)

    for preloaded_agent in ["researcher", "hello"]:
        agent_path = root / "agents" / f"{preloaded_agent}.md"
        if force or not agent_path.exists():
            agent_path.write_text(default_agent_markdown(preloaded_agent), encoding="utf-8")
            created.append(agent_path)

    config = root / CONFIG_FILE
    if force or not config.exists():
        config.write_text(
            """[project]
name = "Spider Rose Workflow"
default_agent = "researcher"

[runtime]
mode = "local"
""",
            encoding="utf-8",
        )
        created.append(config)

    return created


def create_agent(root: Path, name: str, force: bool = False) -> Path:
    slug = slugify_agent_name(name)
    path = root / "agents" / f"{slug}.md"
    if path.exists() and not force:
        raise ProjectError(f"Agent already exists: {path}")
    path.write_text(default_agent_markdown(slug), encoding="utf-8")
    config = read_config(root)
    if not config.get("project", {}).get("default_agent"):
        set_default_agent(root, slug)
    return path


def read_config(root: Path) -> dict:
    config_path = root / CONFIG_FILE
    if not config_path.exists():
        raise ProjectError("Missing spider-rose.toml.")
    return tomllib.loads(config_path.read_text(encoding="utf-8"))


def get_default_agent(root: Path) -> str:
    config = read_config(root)
    default_agent = config.get("project", {}).get("default_agent", "").strip()
    if not default_agent:
        agents = sorted((root / "agents").glob("*.md"))
        if len(agents) == 1:
            return agents[0].stem
        raise ProjectError("No default agent set. Create one with `spiderrose new agent researcher`.")
    _require_agent(root, default_agent)
    return default_agent


def set_default_agent(root: Path, agent: str) -> Path:
    slug = slugify_agent_name(agent)
    _require_agent(root, slug)
    config_path = root / CONFIG_FILE
    config_path.write_text(
        f"""[project]
name = "Spider Rose Workflow"
default_agent = "{slug}"

[runtime]
mode = "local"
""",
        encoding="utf-8",
    )
    return config_path


def _require_agent(root: Path, slug: str) -> None:
    path = root / "agents" / f"{slug}.md"
    if not path.exists():
        raise ProjectError(f"Missing agent `{slug}`. Create it with `spiderrose new agent {slug}`.")
