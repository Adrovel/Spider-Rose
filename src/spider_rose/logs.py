from __future__ import annotations

from pathlib import Path
import json


def list_runs(root: Path, limit: int = 10) -> list[dict]:
    runs_dir = root / "runs"
    if not runs_dir.exists():
        return []
    paths = sorted(runs_dir.glob("run_*.json"), reverse=True)[:limit]
    runs: list[dict] = []
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_path"] = str(path)
        runs.append(data)
    return runs

