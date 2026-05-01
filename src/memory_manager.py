from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class MemoryPaths:
    root: Path
    profile: Path
    backlog: Path
    tracker: Path
    schedule_dir: Path
    log_file: Path


class MemoryManager:
    def __init__(self, project_root: str | Path) -> None:
        root = Path(project_root).resolve()
        self.paths = MemoryPaths(
            root=root,
            profile=root / "memory" / "profile.json",
            backlog=root / "memory" / "backlog.json",
            tracker=root / "memory" / "tracker" / "daily_logs.json",
            schedule_dir=root / "memory" / "schedule",
            log_file=root / "logs" / "agent_action.log",
        )

    def _read_json(self, path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, path: Path, data: dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")

    def _append_log(self, action: str, target: Path, entity_id: str, summary: str) -> None:
        now = datetime.now().isoformat(timespec="seconds")
        line = f"[{now}] {action} | {target.as_posix()} | {entity_id} | {summary}\n"
        with self.paths.log_file.open("a", encoding="utf-8") as f:
            f.write(line)

    def load_profile(self) -> dict[str, Any]:
        return self._read_json(self.paths.profile)

    def load_backlog(self) -> dict[str, Any]:
        return self._read_json(self.paths.backlog)

    def save_backlog(self, backlog: dict[str, Any], summary: str = "Backlog updated") -> None:
        self._write_json(self.paths.backlog, backlog)
        self._append_log("UPDATE", self.paths.backlog, "BACKLOG", summary)

    def load_schedule_month(self, month_id: str) -> dict[str, Any]:
        return self._read_json(self.paths.schedule_dir / f"{month_id}.json")

    def save_schedule_month(self, month_id: str, data: dict[str, Any], summary: str = "") -> None:
        target = self.paths.schedule_dir / f"{month_id}.json"
        self._write_json(target, data)
        self._append_log("UPDATE", target, month_id, summary or "Schedule month updated")

    def add_backlog_task(self, task: dict[str, Any]) -> None:
        backlog = self.load_backlog()
        tasks = backlog.get("homework_and_tasks")
        if tasks is None:
            tasks = backlog.setdefault("tasks", [])
        tasks.append(task)
        self.save_backlog(backlog, summary=f"Task added: {task.get('id', 'UNKNOWN')}")
        self._append_log("CREATE", self.paths.backlog, task.get("id", "UNKNOWN"), "Created task")

    def mark_backlog_item_status(self, item_id: str, status: str) -> bool:
        backlog = self.load_backlog()
        found = False
        for group_key in ("homework_and_tasks", "tasks", "learning_materials"):
            for item in backlog.get(group_key, []):
                if item.get("id") == item_id:
                    item["status"] = status
                    found = True
                    break
            if found:
                break
        if found:
            self.save_backlog(backlog, summary=f"Status update: {item_id} -> {status}")
        return found
