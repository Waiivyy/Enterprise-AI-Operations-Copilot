from app.models.ticket import Ticket
from app.tools.ticket_analyzer import analyze_ticket


def test_ticket_analyzer_classifies_teams_access_issue():
    ticket = Ticket(
        ticket_id="TCK-1001",
        requester="Maria Novak",
        requester_email="maria.novak@example.invalid",
        title="Cannot access Teams",
        description="Maria can sign in but Teams says the license is missing.",
    )

    result = analyze_ticket(ticket)

    assert result.category == "access_troubleshooting"
    assert result.urgency == "medium"
    assert result.likely_system == "Microsoft Teams"
    assert result.automation_candidate is True
    assert result.risk_level == "medium"
    assert "Check license assignment" in result.suggested_next_steps


def test_ticket_analyzer_classifies_device_compliance_issue():
    ticket = Ticket(
        ticket_id="TCK-1004",
        requester="Noah Reed",
        requester_email="noah.reed@example.invalid",
        title="Device compliance blocks Teams",
        description="Noah has the Teams license but access is blocked after a device compliance prompt.",
    )

    result = analyze_ticket(ticket)

    assert result.category == "device_compliance"
    assert result.likely_system == "Endpoint compliance"
    assert result.automation_candidate is False
    assert result.risk_level == "medium"
