from __future__ import annotations

from typer.testing import CliRunner

from spider_rose.cli import app


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
