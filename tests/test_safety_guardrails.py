from app.copilot.safety_guardrails import enforce_simulation_mode, validate_public_safe_email


def test_execute_actions_are_converted_to_plan_only():
    actions = [
        {"operation": "execute", "target": "disable-sign-in", "description": "Disable account"},
        {"operation": "plan", "target": "notify-manager", "description": "Prepare handoff"},
    ]

    guarded = enforce_simulation_mode(actions)

    assert guarded[0]["operation"] == "plan"
    assert guarded[0]["simulation_only"] is True
    assert "converted from execute" in guarded[0]["safety_note"]
    assert all(action["simulation_only"] for action in guarded)


def test_only_example_invalid_email_is_public_safe():
    assert validate_public_safe_email("alex.chen@example.invalid") is True
    assert validate_public_safe_email("alex@example.com") is False
