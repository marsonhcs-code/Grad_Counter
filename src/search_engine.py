from __future__ import annotations

from typing import Any


def suggest_queries(profile: dict[str, Any]) -> list[str]:
    learning = profile.get("learning_profile") or profile.get("learning_interests") or {}
    return list(learning.get("search_keywords", []))


def search_materials(_queries: list[str], _settings: dict[str, Any]) -> list[dict[str, Any]]:
    return []

