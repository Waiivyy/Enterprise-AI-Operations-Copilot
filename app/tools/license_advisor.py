import json
from functools import lru_cache
from pathlib import Path

from app.models.user import UserProfile
from app.models.workflow import LicenseRecommendation

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "license_map.json"


@lru_cache
def _license_map() -> dict:
    return json.loads(DATA_PATH.read_text())


def recommend_license(user: UserProfile) -> LicenseRecommendation:
    license_map = _license_map()
    department = user.department_key
    selected = license_map["departments"].get(department, license_map["default"])
    reason = selected["reason"]
    if user.region_key == "europe":
        reason = f"{reason}; Europe data-residency and collaboration baseline"
    return LicenseRecommendation(
        sku_id=selected["sku_id"],
        name=selected["name"],
        reason=reason,
        confidence=selected.get("confidence", 0.82),
    )
