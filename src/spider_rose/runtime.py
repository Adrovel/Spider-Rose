from __future__ import annotations

from pathlib import Path

from spider_rose.agents import parse_markdown_agent
from spider_rose.project import get_default_agent


def run_default_agent(root: Path, task: str) -> str:
    agent_name = get_default_agent(root)
    agent = parse_markdown_agent(root / "agents" / f"{agent_name}.md")
    instruction_text = "\n".join(f"- {item}" for item in agent.instructions) or "- No extra instructions."
    tools_text = ", ".join(agent.tools) if agent.tools else "none"
    return f"""Agent: {agent.title}

Task:
{task}

Goal:
{agent.goal}

Instructions Applied:
{instruction_text}

Tools Declared:
{tools_text}

Output ({agent.output}):
Phase 1 local execution prepared this task for `{agent.name}`. Live tool execution and multi-agent workflows are archived for the next phases.
"""
