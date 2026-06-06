from __future__ import annotations

from pathlib import Path

from spider_rose.agents import parse_markdown_agent
from spider_rose.google_careers import format_google_careers_jobs, scrape_google_careers_jobs


def run_agent_from_visual(root: Path, agent_name: str, task: str) -> str:
    agent = parse_markdown_agent(root / "agents" / f"{agent_name}.md")
    if "google_careers_scraper" not in agent.tools:
        return f"Agent `{agent.name}` has no executable visual tool yet."

    query, location = _parse_google_task(task)
    jobs = scrape_google_careers_jobs(query=query, location=location, limit=5)
    return (
        f"Agent: {agent.title}\n"
        f"Tool: google_careers_scraper\n"
        f"Query: {query or 'all jobs'}\n"
        f"Location: {location or 'all locations'}\n\n"
        f"{format_google_careers_jobs(jobs)}"
    )


def _parse_google_task(task: str) -> tuple[str, str]:
    query = task.strip()
    location = ""
    marker = " in "
    if marker in query.lower():
        parts = query.rsplit(marker, 1)
        query = parts[0].strip()
        location = parts[1].strip()
    return query, location
