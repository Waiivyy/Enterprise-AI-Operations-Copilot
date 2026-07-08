from app.copilot.safety_guardrails import validate_public_safe_email


def assert_public_safe_email(email: str) -> None:
    if not validate_public_safe_email(email):
        raise ValueError("Only example.invalid addresses are allowed in the demo.")
