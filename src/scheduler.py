from __future__ import annotations

from datetime import date
from typing import Any


def plan_day(target_date: date, profile: dict[str, Any], backlog: dict[str, Any]) -> dict[str, Any]:
    daily_focus = "Complete highest-priority pending items"
    events: list[dict[str, Any]] = []

    candidates = backlog.get("homework_and_tasks") or backlog.get("tasks") or []
    if candidates:
        top = candidates[0]
        events.append(
            {
                "time": "09:00-10:30",
                "title": top.get("title", "Planned Task"),
                "type": "dynamic",
                "linked_id": top.get("id", "UNKNOWN"),
                "is_completed": False,
                "agent_note": "Auto-planned by scheduler.",
            }
        )

    return {target_date.isoformat(): {"daily_focus": daily_focus, "events": events}}

