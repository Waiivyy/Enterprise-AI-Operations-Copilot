SAFE_DOMAIN = "example.invalid"


SAFETY_NOTES = [
    "Simulation only: no Microsoft Graph, SaaS, or tenant write calls are made.",
    "All identities, groups, licenses, and domains are fake demo values.",
    "Requests to execute changes are converted into plan-only actions.",
]


def validate_public_safe_email(email: str) -> bool:
    return email.lower().endswith(f"@{SAFE_DOMAIN}")


def enforce_simulation_mode(actions: list[dict]) -> list[dict]:
    guarded: list[dict] = []
    for action in actions:
        next_action = dict(action)
        original_operation = str(next_action.get("operation", "plan")).lower()
        if original_operation == "execute":
            next_action["operation"] = "plan"
            next_action["safety_note"] = "Action converted from execute to plan-only."
        else:
            next_action["operation"] = "plan"
            next_action.setdefault("safety_note", "Simulation only. No tenant changes were executed.")
        next_action["simulation_only"] = True
        guarded.append(next_action)
    return guarded


def safety_notes(extra: list[str] | None = None) -> list[str]:
    return [*SAFETY_NOTES, *(extra or [])]
