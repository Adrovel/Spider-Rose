from __future__ import annotations

import json

from typer.testing import CliRunner

from prompt_toolkit.document import Document

from spider_rose.cli import (
    COMPOSER_INPUT_MAX_HEIGHT,
    COMPOSER_MAX_HEIGHT,
    COMPOSER_MIN_HEIGHT,
    SlashCommandCompleter,
    app,
)
from spider_rose.server import APP_HTML, _read_workflow_layout, create_app
from spider_rose.google_careers import parse_google_careers_jobs, store_google_careers_jobs


runner = CliRunner()


GOOGLE_CAREERS_HTML = """
<main>
<h2>Jobs search results</h2>
<a href="/about/careers/applications/jobs/results/123-software-engineer">
<h3>Software Engineer III, AI Infrastructure</h3>
</a>
<span>Mid</span>
<div>Google | Bengaluru, Karnataka, India</div>
<h4>Minimum qualifications</h4>
<p>Bachelor's degree or equivalent practical experience.</p>
<p>2 years of experience with software development.</p>
<a href="/about/careers/applications/jobs/results/456-product-manager">
<h3>Product Manager II, Google Cloud</h3>
</a>
<span>Mid</span>
<div>Google | Sunnyvale, CA, USA</div>
<h4>Minimum qualifications</h4>
<p>Bachelor's degree or equivalent practical experience.</p>
</main>
"""


def test_composer_height_is_bounded():
    assert COMPOSER_MIN_HEIGHT == 3
    assert COMPOSER_MAX_HEIGHT == 12
    assert COMPOSER_INPUT_MAX_HEIGHT == 10


def test_slash_command_typeahead_uses_registered_commands():
    completer = SlashCommandCompleter()

    def completions(text: str) -> list[str]:
        document = Document(text=text, cursor_position=len(text))
        return [completion.text for completion in completer.get_completions(document, None)]

    assert "/run" in completions("/")
    assert "/recent" in completions("/r")
    assert "/menu" in completions("/m")
    assert "/new agent " in completions("/n")
    assert completions("hello") == []
    assert completions("/run ") == []


def test_terminal_mvp_flow(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SPIDER_ROSE_PROJECT_ROOT", str(tmp_path))

    result = runner.invoke(app, input="/run Search Nathan's LinkedIn\n/exit\n")
    assert result.exit_code == 0
    assert "Spider Rose" in result.output
    assert "local agent web" in result.output
    assert "rose web shell" in result.output
    assert "Project" in result.output
    assert "Default" in result.output
    assert "🕷" in result.output
    assert "INPUT" not in result.output
    assert "Terminal input" not in result.output
    assert "Spider Rose memory" not in result.output
    assert "Type a slash command" not in result.output
    assert "spiderrose >" not in result.output
    assert "Run" in result.output
    assert "Google Careers Scraper Agent" in result.output
    assert "Search Nathan's LinkedIn" in result.output
    assert "Recent" not in result.output
    assert "Closed Spider Rose." in result.output
    assert (tmp_path / "agents" / "google-careers-scraper.md").exists()
    assert not (tmp_path / "agents" / "researcher.md").exists()
    assert not (tmp_path / "agents" / "hello.md").exists()


def test_help_shows_interactive_slash_commands(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SPIDER_ROSE_PROJECT_ROOT", str(tmp_path))

    result = runner.invoke(app, input="/help\n/exit\n")
    assert result.exit_code == 0
    assert "Commands" in result.output
    assert "/visualise" in result.output
    assert "/new agent <name>" in result.output
    assert "/run <task>" in result.output
    assert "/recent" in result.output
    assert "/menu" in result.output
    assert "/clear" in result.output
    assert "🕷" in result.output
    assert "INPUT" not in result.output
    assert "Terminal input" not in result.output
    assert "Spider Rose memory" not in result.output
    assert "Type a slash command" not in result.output
    assert "spiderrose >" not in result.output
    assert "Recent" not in result.output
    assert "Showed command list." not in result.output
    assert "Use /visualise, /new agent <name>, /run <task>, /help, or /exit." not in result.output


def test_menu_shows_registered_slash_commands(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SPIDER_ROSE_PROJECT_ROOT", str(tmp_path))

    result = runner.invoke(app, input="/menu\n/exit\n")

    assert result.exit_code == 0
    assert "Slash Command Menu" in result.output
    assert "/run <task>" in result.output
    assert "/recent" in result.output
    assert "/menu" in result.output
    assert "/new agent <name>" in result.output
    assert "/visualise" in result.output
    assert "/clear" in result.output
    assert "/help" in result.output
    assert "/exit" in result.output


def test_terminal_history_tracks_current_session(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SPIDER_ROSE_PROJECT_ROOT", str(tmp_path))

    result = runner.invoke(app, input="hello\n/help\n/run Plan tomorrow\n/clear\n/recent\n/exit\n")

    assert result.exit_code == 0
    assert "Recent" in result.output
    assert "Input" in result.output
    assert "hello" in result.output
    assert "Command needed" in result.output
    assert "/help" in result.output
    assert "Showed command list." in result.output
    assert "/run Plan tomorrow" in result.output
    assert "Plan tomorrow" in result.output
    assert "Redrew the terminal shell." in result.output
    assert "Showed terminal history." not in result.output


def test_run_uses_background_history_context_without_showing_recent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SPIDER_ROSE_PROJECT_ROOT", str(tmp_path))

    result = runner.invoke(app, input="client prefers concise output\n/run Draft status update\n/exit\n")

    assert result.exit_code == 0
    assert "Session Context:" in result.output
    assert "client prefers concise output" in result.output
    assert "Recent" not in result.output


def test_visual_routes_exist(tmp_path):
    routes = {route.path for route in create_app(tmp_path).routes}

    assert "/" in routes
    assert "/workflow" in routes
    assert "/tools" not in routes
    assert "/api/agents" in routes
    assert "/api/workflow-layout" in routes
    assert "/api/demo/google-careers/run" in routes


def test_google_careers_visual_demo_is_rendered():
    assert "Web Scraper: Google Careers" in APP_HTML
    assert "Store: Job Results" in APP_HTML
    assert "Jobs found" in APP_HTML
    assert "Run demo" in APP_HTML
    assert "Scraping Google Careers..." in APP_HTML
    assert "/api/demo/google-careers/run" in APP_HTML
    assert "Results are scraped from Google Careers when the demo runs." in APP_HTML
    assert "canvasLayer.innerHTML = activeTab === 'workflow' ? ''" in APP_HTML
    assert 'data-tab="tools"' not in APP_HTML
    assert 'id="panelTools"' not in APP_HTML
    assert 'data-detail="tools"' not in APP_HTML
    assert 'id="zoomInBtn"' not in APP_HTML
    assert 'id="zoomOutBtn"' not in APP_HTML


def test_google_careers_parser_extracts_jobs_with_links():
    jobs = parse_google_careers_jobs(GOOGLE_CAREERS_HTML)

    assert len(jobs) == 2
    assert jobs[0].title == "Software Engineer III, AI Infrastructure"
    assert jobs[0].location == "Bengaluru, Karnataka, India"
    assert jobs[0].level == "Mid"
    assert jobs[0].url == "https://www.google.com/about/careers/applications/jobs/results/123-software-engineer"
    assert jobs[0].minimum_qualifications[0] == "Bachelor's degree or equivalent practical experience."


def test_google_careers_store_dedupes_by_url(tmp_path):
    jobs = parse_google_careers_jobs(GOOGLE_CAREERS_HTML)

    first = store_google_careers_jobs(tmp_path, jobs)
    second = store_google_careers_jobs(tmp_path, jobs)

    assert first.new_count == 2
    assert first.duplicate_count == 0
    assert second.new_count == 0
    assert second.duplicate_count == 2
    assert (tmp_path / "artifacts" / "google-careers" / "job-results.jsonl").exists()


def test_workflow_layout_supports_duplicate_agent_cards(tmp_path):
    (tmp_path / "workflow-layout.json").write_text(
        json.dumps(
            {
                "cards": [
                    {"id": "google-careers-scraper-1", "agent": "google-careers-scraper", "x": 10, "y": 20},
                    {"id": "google-careers-scraper-2", "agent": "google-careers-scraper", "x": 40, "y": 60},
                ]
            }
        ),
        encoding="utf-8",
    )

    layout = _read_workflow_layout(tmp_path)

    assert len(layout["cards"]) == 2
    assert layout["cards"][1]["id"] == "google-careers-scraper-2"
