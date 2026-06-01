from __future__ import annotations

import json

from typer.testing import CliRunner

from spider_rose.cli import app
from spider_rose.server import _read_workflow_layout, create_app


runner = CliRunner()


def test_terminal_mvp_flow(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, input="/run Search Nathan's LinkedIn\n/exit\n")
    assert result.exit_code == 0
    assert "Spider Rose" in result.output
    assert "Researcher Agent" in result.output
    assert "Search Nathan's LinkedIn" in result.output
    assert (tmp_path / "agents" / "researcher.md").exists()


def test_help_shows_interactive_slash_commands(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, input="/help\n/exit\n")
    assert result.exit_code == 0
    assert "/visualise" in result.output
    assert "/new agent <name>" in result.output
    assert "/run <task>" in result.output


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
