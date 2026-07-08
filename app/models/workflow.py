from typing import Literal

from pydantic import BaseModel, Field

from app.models.ticket import Ticket, TicketAnalysis
from app.models.user import UserProfile


Scenario = Literal["onboarding", "offboarding", "access_troubleshooting", "ticket_analysis"]


class PlannedAction(BaseModel):
    operation: str = "plan"
    target: str
    description: str
    tool: str | None = None
    simulation_only: bool = True
    safety_note: str = "Simulation only. No tenant changes were executed."


class LicenseRecommendation(BaseModel):
    sku_id: str
    name: str
    reason: str
    confidence: float = Field(default=0.8, ge=0, le=1)


class GroupRecommendation(BaseModel):
    group_id: str
    display_name: str
    reason: str


class SaaSPayload(BaseModel):
    app: str
    operation: str
    payload: dict
    simulation_only: bool = True


class AccessTroubleshootingRequest(BaseModel):
    user_email: str
    app_name: str = "Teams"
    issue: str = "access problem"


class AccessFinding(BaseModel):
    likely_cause: str
    evidence: list[str]
    recommended_actions: list[str]
    graph_style_checks: list[str]
    confidence: float = Field(ge=0, le=1)


class ChatRequest(BaseModel):
    scenario: Scenario
    message: str = Field(..., min_length=3)


class ChatResponse(BaseModel):
    scenario: Scenario
    summary: str
    tool_plan: list[str]
    planned_actions: list[PlannedAction]
    safety_notes: list[str]
    evidence: list[str] = Field(default_factory=list)
    report_id: str | None = None
    report_markdown: str | None = None
    report_json: str | None = None


class OnboardingRequest(BaseModel):
    user: UserProfile


class OnboardingPlan(BaseModel):
    user: UserProfile
    license: LicenseRecommendation
    groups: list[GroupRecommendation]
    saas_payloads: list[SaaSPayload]
    planned_actions: list[PlannedAction]
    safety_notes: list[str]
    report_id: str | None = None


class OffboardingRequest(BaseModel):
    user: UserProfile
    preserve_mailbox_access_for: str | None = None


class OffboardingPlan(BaseModel):
    user: UserProfile
    planned_actions: list[PlannedAction]
    saas_payloads: list[SaaSPayload]
    manager_handoff: list[str]
    safety_notes: list[str]
    report_id: str | None = None


class TicketAnalysisRequest(BaseModel):
    ticket: Ticket


class TicketAnalysisResponse(BaseModel):
    analysis: TicketAnalysis
    planned_actions: list[PlannedAction]
    safety_notes: list[str]
