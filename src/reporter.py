from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


def render_weekly_report(week_id: str, logs: dict[str, Any]) -> str:
    entries = logs.get("logs", [])
    planned = 0
    completed = 0
    for row in entries:
        metrics = row.get("metrics", {})
        planned += int(metrics.get("tasks_planned", 0))
        completed += int(metrics.get("tasks_completed", 0))
    rate = (completed / planned) if planned else 0.0

    return (
        f"# Weekly Report {week_id}\n\n"
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}\n"
        f"- tasks_planned: {planned}\n"
        f"- tasks_completed: {completed}\n"
        f"- completion_rate: {rate:.2f}\n"
    )


def save_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

