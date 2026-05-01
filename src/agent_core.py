from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from memory_manager import MemoryManager
from scheduler import plan_day


@dataclass
class AgentDecision:
    target_date: date
    action: str
    payload: dict[str, Any]


class AgentCore:
    def __init__(self, memory: MemoryManager) -> None:
        self.memory = memory

    def daily_schedule(self, target_date: date) -> AgentDecision:
        profile = self.memory.load_profile()
        backlog = self.memory.load_backlog()
        plan = plan_day(target_date=target_date, profile=profile, backlog=backlog)
        return AgentDecision(target_date=target_date, action="schedule_day", payload=plan)

