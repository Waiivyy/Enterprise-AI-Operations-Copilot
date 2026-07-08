from app.models.ticket import Ticket, TicketAnalysis


def analyze_ticket(ticket: Ticket) -> TicketAnalysis:
    text = f"{ticket.title} {ticket.description}".lower()
    if "teams" in text or "license" in text:
        return TicketAnalysis(
            ticket_id=ticket.ticket_id,
            category="access_troubleshooting",
            urgency="medium",
            likely_system="Microsoft Teams",
            suggested_next_steps=[
                "Check license assignment",
                "Review group membership",
                "Confirm account sign-in is enabled",
                "Inspect conditional access placeholders in mock policy",
            ],
            required_approvals=["Service owner review if license change is needed"],
            automation_candidate=True,
            risk_level="medium",
        )
    if "offboard" in text or "leaving" in text:
        return TicketAnalysis(
            ticket_id=ticket.ticket_id,
            category="offboarding",
            urgency="high",
            likely_system="Identity lifecycle",
            suggested_next_steps=[
                "Confirm departure date",
                "Prepare sign-in disablement plan",
                "Generate SaaS deprovisioning checklist",
            ],
            required_approvals=["Manager approval", "HR confirmation"],
            automation_candidate=True,
            risk_level="high",
        )
    return TicketAnalysis(
        ticket_id=ticket.ticket_id,
        category="general_support",
        urgency="low",
        likely_system="IT service desk",
        suggested_next_steps=["Collect affected user, system, and timestamp details"],
        required_approvals=[],
        automation_candidate=False,
        risk_level="low",
    )
