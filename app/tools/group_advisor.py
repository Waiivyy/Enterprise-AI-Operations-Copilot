import json
from functools import lru_cache
from pathlib import Path

from app.models.user import UserProfile
from app.models.workflow import GroupRecommendation

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "group_map.json"


@lru_cache
def _group_map() -> dict:
    return json.loads(DATA_PATH.read_text())


def _group_from_record(record: dict, reason: str) -> GroupRecommendation:
    return GroupRecommendation(
        group_id=record["group_id"],
        display_name=record["display_name"],
        reason=reason,
    )


def recommend_groups(user: UserProfile) -> list[GroupRecommendation]:
    mapping = _group_map()
    groups = [
        _group_from_record(mapping["baseline"]["employees"], "Baseline employee access"),
    ]
    if department := mapping["departments"].get(user.department_key):
        groups.append(_group_from_record(department, f"{user.department} department access"))
    if region := mapping["regions"].get(user.region_key):
        groups.append(_group_from_record(region, f"{user.region} regional access"))
    return groups
