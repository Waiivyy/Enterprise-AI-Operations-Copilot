from pydantic import BaseModel, Field, field_validator


class Ticket(BaseModel):
    ticket_id: str = Field(..., pattern=r"^TCK-[0-9]{4}$")
    requester: str
    requester_email: str
    title: str
    description: str

    @field_validator("requester_email")
    @classmethod
    def email_must_use_example_invalid(cls, value: str) -> str:
        if not value.endswith("@example.invalid"):
            raise ValueError("demo tickets must use example.invalid emails")
        return value


class TicketAnalysis(BaseModel):
    ticket_id: str
    category: str
    urgency: str
    likely_system: str
    suggested_next_steps: list[str]
    required_approvals: list[str]
    automation_candidate: bool
    risk_level: str
