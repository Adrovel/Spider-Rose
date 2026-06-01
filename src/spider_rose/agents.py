from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SECTION_NAMES = {"goal", "instructions", "tools", "output"}


@dataclass(frozen=True)
class AgentDefinition:
    name: str
    title: str
    goal: str
    instructions: list[str]
    tools: list[str]
    output: str
    path: Path


def slugify_agent_name(name: str) -> str:
    slug = name.strip().lower().replace(" ", "-").replace("_", "-")
    slug = "".join(char for char in slug if char.isalnum() or char == "-")
    slug = "-".join(part for part in slug.split("-") if part)
    if not slug:
        raise ValueError("Agent name must contain at least one letter or number.")
    return slug


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def default_agent_markdown(name: str) -> str:
    slug = slugify_agent_name(name)
    title = title_from_slug(slug)
    if slug == "researcher":
        return """# Researcher Agent

Goal:
Find accurate information and turn a user task into a clear starting point.

Instructions:
- Identify what the user is asking for.
- Pull out names, entities, platforms, and constraints.
- Say what information is known and what is still missing.
- Return concise, structured output.

Tools:
- web_search

Output:
research_summary
"""
    if slug == "hello":
        return """# Hello Agent

Goal:
Greet the user, explain Spider Rose briefly, and help them take their first action.

Instructions:
- Keep the response short and friendly.
- Mention that agents are stored as Markdown files.
- Suggest creating or editing an agent when the user is ready.
- Avoid technical jargon unless the user asks for it.

Tools:
- none

Output:
hello_message
"""

    return f"""# {title} Agent

Goal:
Describe what this agent is responsible for.

Instructions:
- Keep work focused.
- Return clear, structured output.

Tools:
- none

Output:
{slug}_output
"""


def parse_markdown_agent(path: Path) -> AgentDefinition:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = path.stem
    sections: dict[str, list[str]] = {name: [] for name in SECTION_NAMES}
    current: str | None = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and title == path.stem:
            title = stripped[2:].strip()
            continue
        key = stripped[:-1].lower() if stripped.endswith(":") else ""
        if key in SECTION_NAMES:
            current = key
            continue
        if current:
            sections[current].append(line)

    instructions = _parse_bullets(sections["instructions"])
    tools = _parse_bullets(sections["tools"])
    goal = _parse_block(sections["goal"])
    output = _parse_block(sections["output"])

    if not goal:
        raise ValueError(f"{path} is missing a Goal section.")
    if not output:
        raise ValueError(f"{path} is missing an Output section.")

    return AgentDefinition(
        name=path.stem,
        title=title,
        goal=goal,
        instructions=instructions,
        tools=tools,
        output=output,
        path=path,
    )


def _parse_bullets(lines: list[str]) -> list[str]:
    values: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            values.append(stripped[2:].strip())
        else:
            values.append(stripped)
    return values


def _parse_block(lines: list[str]) -> str:
    return "\n".join(line.strip() for line in lines).strip()
