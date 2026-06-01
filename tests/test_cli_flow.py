from __future__ import annotations

from typer.testing import CliRunner

from spider_rose.cli import app


runner = CliRunner()


def test_terminal_mvp_flow(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["new", "agent", "researcher"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["run", "Search Nathan's LinkedIn"])
    assert result.exit_code == 0
    assert "Researcher Agent" in result.output
    assert "Search Nathan's LinkedIn" in result.output
