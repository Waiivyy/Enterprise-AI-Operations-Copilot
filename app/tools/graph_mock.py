import json
from functools import lru_cache
from pathlib import Path

from app.models.workflow import AccessFinding, PlannedAction

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "mock_tenant_state.json"


@lru_cache
def _tenant_state() -> dict:
    return json.loads(DATA_PATH.read_text())


def get_user_state(email: str) -> dict | None:
    return _tenant_state()["users"].get(email.lower())


def troubleshoot_access(email: str, app_name: str = "Teams") -> AccessFinding:
    state = _tenant_state()
    user = state["users"].get(email.lower())
    app_key = app_name.lower()
    requirements = state["app_requirements"].get(app_key, {})
    evidence: list[str] = []
    recommended: list[str] = []
    checks = [
        f"GET /users/{email}",
        f"GET /users/{email}/licenseDetails",
        f"GET /users/{email}/memberOf",
        "Evaluate mock conditional access and device compliance placeholders",
    ]

    if not user:
        return AccessFinding(
            likely_cause="User not found in mock tenant state",
            evidence=[f"No mock state exists for {email}"],
            recommended_actions=["Confirm the demo user email or add the user to mock_tenant_state.json"],
            graph_style_checks=checks,
            confidence=0.7,
        )

    if not user["account_enabled"]:
        evidence.append("Account is disabled in mock tenant state.")
        recommended.append("Review sign-in status before license or group changes.")
        cause = "Account disabled"
        confidence = 0.92
    elif requirements.get("required_license") not in user["assigned_licenses"]:
        evidence.append(
            f"User has {', '.join(user['assigned_licenses'])}, but {app_name} requires {requirements.get('required_license')} in sample policy."
        )
        recommended.append("Review license assignment and approval path.")
        cause = f"{app_name} license missing"
        confidence = 0.88
    elif requirements.get("required_group") not in user["groups"]:
        evidence.append(f"User is not a member of {requirements.get('required_group')}.")
        recommended.append("Review group membership and app assignment policy.")
        cause = f"{app_name} group membership missing"
        confidence = 0.84
    elif not user["device_compliant"]:
        evidence.append("Device compliance placeholder is false.")
        recommended.append("Route to endpoint compliance review.")
        cause = "Device compliance placeholder issue"
        confidence = 0.68
    else:
        evidence.append("License, group membership, sign-in, and placeholders match sample policy.")
        recommended.append("Collect client-side error timestamp and retry after token refresh.")
        cause = "No tenant-side issue found in mock data"
        confidence = 0.55

    return AccessFinding(
        likely_cause=cause,
        evidence=evidence,
        recommended_actions=recommended,
        graph_style_checks=checks,
        confidence=confidence,
    )


def plan_graph_actions(kind: str, user_email: str, targets: list[str]) -> list[PlannedAction]:
    return [
        PlannedAction(
            target=target,
            description=f"Plan {kind} Graph-style action for {user_email}: {target}",
            tool="graph_mock",
        )
        for target in targets
    ]
