from __future__ import annotations

from datetime import date
from pathlib import Path

from agent_core import AgentCore
from memory_manager import MemoryManager


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    memory = MemoryManager(root)
    agent = AgentCore(memory)

    today = date.today()
    decision = agent.daily_schedule(today)
    month_id = today.strftime("%Y-%m")

    month_data = memory.load_schedule_month(month_id)
    month_data.update(decision.payload)
    memory.save_schedule_month(month_id, month_data, summary=f"Scheduled {today.isoformat()}")

    print(f"Scheduled day: {today.isoformat()}")


if __name__ == "__main__":
    main()

