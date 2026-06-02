from __future__ import annotations

import json

from typer.testing import CliRunner

from spider_rose.cli import app
from spider_rose.server import _read_workflow_layout, create_app


runner = CliRunner()


def test_terminal_mvp_flow(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SPIDER_ROSE_PROJECT_ROOT", str(tmp_path))

    result = runner.invoke(app, input="/run Search Nathan's LinkedIn\n/exit\n")
    assert result.exit_code == 0
    assert "Spider Rose" in result.output
    assert "local agent workspace" in result.output
    assert "Project" in result.output
    assert "Default" in result.output
    assert "INPUT" in result.output
    assert "Terminal input" in result.output
    assert "Spider Rose memory" in result.output
    assert "Type a slash command" in result.output
    assert "🕷" in result.output
    assert "spiderrose >" not in result.output
    assert "Run" in result.output
    assert "Researcher Agent" in result.output
    assert "Search Nathan's LinkedIn" in result.output
    assert "Recent" not in result.output
    assert "Closed Spider Rose." in result.output
    assert (tmp_path / "agents" / "researcher.md").exists()
    assert (tmp_path / "agents" / "hello.md").exists()


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
    assert "INPUT" in result.output
    assert "Terminal input" in result.output
    assert "Spider Rose memory" in result.output
    assert "Type a slash command" in result.output
    assert "🕷" in result.output
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
    assert "/tools" in routes
    assert "/api/agents" in routes
    assert "/api/workflow-layout" in routes


def test_workflow_layout_supports_duplicate_agent_cards(tmp_path):
    (tmp_path / "workflow-layout.json").write_text(
        json.dumps(
            {
                "cards": [
                    {"id": "researcher-1", "agent": "researcher", "x": 10, "y": 20},
                    {"id": "researcher-2", "agent": "researcher", "x": 40, "y": 60},
                ]
            }
        ),
        encoding="utf-8",
    )

    layout = _read_workflow_layout(tmp_path)

    assert len(layout["cards"]) == 2
    assert layout["cards"][1]["id"] == "researcher-2"
