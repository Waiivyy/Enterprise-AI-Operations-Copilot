import re
from pathlib import Path

from app.copilot.response_builder import build_chat_response
from app.copilot.safety_guardrails import enforce_simulation_mode, safety_notes
from app.copilot.tool_router import ToolRouter
from app.models.report import ReportRequest
from app.models.ticket import Ticket
from app.models.user import UserProfile
from app.models.workflow import (
    AccessTroubleshootingRequest,
    ChatRequest,
    ChatResponse,
    OffboardingPlan,
    OffboardingRequest,
    OnboardingPlan,
    OnboardingRequest,
    PlannedAction,
    TicketAnalysisResponse,
)
from app.providers.mock_llm import MockLLMProvider
from app.tools.report_writer import create_report


class CopilotPlanner:
    def __init__(self, report_dir: Path | str = Path("reports")) -> None:
        self.report_dir = Path(report_dir)
        self.llm = MockLLMProvider()
        self.tools = ToolRouter()

    def handle_chat(self, request: ChatRequest) -> ChatResponse:
        if request.scenario == "onboarding":
            return self._chat_from_onboarding(request)
        if request.scenario == "offboarding":
            return self._chat_from_offboarding(request)
        if request.scenario == "access_troubleshooting":
            return self._chat_from_troubleshooting(request)
        return self._chat_from_ticket(request)

    def plan_onboarding(self, request: OnboardingRequest) -> OnboardingPlan:
        user = request.user
        license_rec = self.tools.recommend_license(user)
        groups = self.tools.recommend_groups(user)
        saas_payloads = self.tools.generate_saas_payloads(user, operation="provision")
        raw_actions = [
            {"operation": "execute", "target": "assign-license", "description": f"Assign {license_rec.name}", "tool": "graph_mock"},
            *[
                {
                    "operation": "execute",
                    "target": f"add-group:{group.group_id}",
                    "description": f"Add to {group.display_name}",
                    "tool": "graph_mock",
                }
                for group in groups
            ],
            *[
                {
                    "operation": "execute",
                    "target": f"provision-saas:{payload.app.lower().replace(' ', '-')}",
                    "description": f"Provision {payload.app}",
                    "tool": "saas_payloads",
                }
                for payload in saas_payloads
            ],
        ]
        planned_actions = [PlannedAction(**action) for action in enforce_simulation_mode(raw_actions)]
        notes = safety_notes(["Required approvals: manager approval and application owner approval for privileged tools."])
        report = create_report(
            ReportRequest(
                report_type="onboarding",
                subject=user.display_name,
                summary=f"Simulation-only onboarding plan for {user.display_name}.",
                findings=[
                    f"Recommended license: {license_rec.name}",
                    f"Recommended groups: {', '.join(group.group_id for group in groups)}",
                ],
                planned_actions=[action.model_dump() for action in planned_actions],
                safety_notes=notes,
            ),
            self.report_dir,
        )
        return OnboardingPlan(
            user=user,
            license=license_rec,
            groups=groups,
            saas_payloads=saas_payloads,
            planned_actions=planned_actions,
            safety_notes=notes,
            report_id=report.report_id,
        )

    def plan_offboarding(self, request: OffboardingRequest) -> OffboardingPlan:
        user = request.user
        saas_payloads = self.tools.generate_saas_payloads(user, operation="deprovision")
        raw_actions = [
            {"operation": "execute", "target": "disable-sign-in", "description": "Disable sign-in after approved departure time", "tool": "graph_mock"},
            {"operation": "execute", "target": "revoke-sessions", "description": "Revoke active sessions", "tool": "graph_mock"},
            {"operation": "execute", "target": "remove-licenses", "description": "Remove assigned licenses", "tool": "graph_mock"},
            {"operation": "execute", "target": "remove-groups", "description": "Remove group memberships", "tool": "graph_mock"},
            *[
                {
                    "operation": "execute",
                    "target": f"deprovision-saas:{payload.app.lower().replace(' ', '-')}",
                    "description": f"Prepare {payload.app} deprovisioning payload",
                    "tool": "saas_payloads",
                }
                for payload in saas_payloads
            ],
        ]
        if request.preserve_mailbox_access_for:
            raw_actions.append(
                {
                    "operation": "plan",
                    "target": "preserve-mailbox-access",
                    "description": f"Plan mailbox handoff for {request.preserve_mailbox_access_for}",
                    "tool": "graph_mock",
                }
            )
        planned_actions = [PlannedAction(**action) for action in enforce_simulation_mode(raw_actions)]
        handoff = [
            "Confirm final working date with HR and manager.",
            "Identify files, mailboxes, and shared resources requiring handoff.",
            "Prepare access removal window and rollback contact.",
        ]
        notes = safety_notes(["Offboarding plans require HR confirmation before any real-world execution outside this demo."])
        report = create_report(
            ReportRequest(
                report_type="offboarding",
                subject=user.display_name,
                summary=f"Simulation-only offboarding plan for {user.display_name}.",
                findings=handoff,
                planned_actions=[action.model_dump() for action in planned_actions],
                safety_notes=notes,
            ),
            self.report_dir,
        )
        return OffboardingPlan(
            user=user,
            planned_actions=planned_actions,
            saas_payloads=saas_payloads,
            manager_handoff=handoff,
            safety_notes=notes,
            report_id=report.report_id,
        )

    def troubleshoot_access(self, request: AccessTroubleshootingRequest) -> ChatResponse:
        tool_plan = ["get_user_state", "troubleshoot_access", "create_report"]
        finding = self.tools.troubleshoot_access(request.user_email, request.app_name)
        raw_actions = [
            {
                "operation": "plan",
                "target": "review-license-assignment",
                "description": "Review the license recommendation against mock app policy.",
                "tool": "graph_mock",
            },
            {
                "operation": "plan",
                "target": "review-group-membership",
                "description": "Review group membership required by the mock app policy.",
                "tool": "graph_mock",
            },
        ]
        planned_actions = [PlannedAction(**action) for action in enforce_simulation_mode(raw_actions)]
        notes = safety_notes()
        report = create_report(
            ReportRequest(
                report_type="access-troubleshooting",
                subject=request.user_email,
                summary=f"Likely cause: {finding.likely_cause}.",
                findings=[*finding.evidence, *finding.recommended_actions],
                planned_actions=[action.model_dump() for action in planned_actions],
                safety_notes=notes,
            ),
            self.report_dir,
        )
        return build_chat_response(
            scenario="access_troubleshooting",
            summary=f"Likely cause: {finding.likely_cause}. Confidence {finding.confidence:.0%}.",
            tool_plan=tool_plan,
            planned_actions=planned_actions,
            safety_notes=notes,
            evidence=[*finding.evidence, *finding.graph_style_checks],
            report=report,
        )

    def analyze_ticket(self, ticket: Ticket) -> TicketAnalysisResponse:
        analysis = self.tools.analyze_ticket(ticket)
        raw_actions = [
            {
                "operation": "plan",
                "target": f"classify-ticket:{ticket.ticket_id}",
                "description": f"Classify as {analysis.category} with {analysis.risk_level} risk.",
                "tool": "ticket_analyzer",
            }
        ]
        planned_actions = [PlannedAction(**action) for action in enforce_simulation_mode(raw_actions)]
        notes = safety_notes(["Ticket analysis is advisory and should be reviewed by the service desk."])
        create_report(
            ReportRequest(
                report_type="ticket-analysis",
                subject=ticket.ticket_id,
                summary=f"Ticket classified as {analysis.category}.",
                findings=[*analysis.suggested_next_steps, *analysis.required_approvals],
                planned_actions=[action.model_dump() for action in planned_actions],
                safety_notes=notes,
            ),
            self.report_dir,
        )
        return TicketAnalysisResponse(analysis=analysis, planned_actions=planned_actions, safety_notes=notes)

    def _chat_from_onboarding(self, request: ChatRequest) -> ChatResponse:
        user = _user_from_message(request.message, default_name="Sara Holm", default_email="sara.holm@example.invalid")
        plan = self.plan_onboarding(OnboardingRequest(user=user))
        tool_plan = self.llm.build_tool_plan(request)
        return build_chat_response(
            scenario="onboarding",
            summary=f"Simulation-only onboarding plan for {user.display_name}. Recommended {plan.license.name}.",
            tool_plan=tool_plan,
            planned_actions=plan.planned_actions,
            safety_notes=plan.safety_notes,
            evidence=[plan.license.reason, *[group.reason for group in plan.groups]],
            report_id=plan.report_id,
        )

    def _chat_from_offboarding(self, request: ChatRequest) -> ChatResponse:
        user = _user_from_message(request.message, default_name="Priya Shah", default_email="priya.shah@example.invalid")
        plan = self.plan_offboarding(OffboardingRequest(user=user, preserve_mailbox_access_for=user.manager))
        return build_chat_response(
            scenario="offboarding",
            summary=f"Simulation-only offboarding plan for {user.display_name}.",
            tool_plan=self.llm.build_tool_plan(request),
            planned_actions=plan.planned_actions,
            safety_notes=plan.safety_notes,
            evidence=plan.manager_handoff,
            report_id=plan.report_id,
        )

    def _chat_from_troubleshooting(self, request: ChatRequest) -> ChatResponse:
        email = _email_from_message(request.message) or "maria.novak@example.invalid"
        app_name = "Teams" if "teams" in request.message.lower() else "Box"
        return self.troubleshoot_access(AccessTroubleshootingRequest(user_email=email, app_name=app_name, issue=request.message))

    def _chat_from_ticket(self, request: ChatRequest) -> ChatResponse:
        ticket = Ticket(
            ticket_id="TCK-9001",
            requester="Demo Requester",
            requester_email="demo.requester@example.invalid",
            title=request.message[:80],
            description=request.message,
        )
        analysis_response = self.analyze_ticket(ticket)
        return build_chat_response(
            scenario="ticket_analysis",
            summary=f"Ticket classified as {analysis_response.analysis.category} with {analysis_response.analysis.risk_level} risk.",
            tool_plan=self.llm.build_tool_plan(request),
            planned_actions=analysis_response.planned_actions,
            safety_notes=analysis_response.safety_notes,
            evidence=analysis_response.analysis.suggested_next_steps,
        )


def _email_from_message(message: str) -> str | None:
    match = re.search(r"[\w.+-]+@example\.invalid", message.lower())
    return match.group(0) if match else None


def _user_from_message(message: str, default_name: str, default_email: str) -> UserProfile:
    lower = message.lower()
    name = default_name
    email = _email_from_message(message) or default_email
    for candidate in ["Sara", "Priya", "Alex", "Maria"]:
        if candidate.lower() in lower:
            name = {
                "Sara": "Sara Holm",
                "Priya": "Priya Shah",
                "Alex": "Alex Chen",
                "Maria": "Maria Novak",
            }[candidate]
            email = f"{name.lower().replace(' ', '.')}@example.invalid"
            break
    department = "Engineering" if "engineering" in lower else "Finance" if "finance" in lower else "Sales" if "sales" in lower else "General"
    region = "Europe" if "europe" in lower else "North America" if "north america" in lower else "Global"
    employment_type = "contractor" if "contractor" in lower else "full-time"
    return UserProfile(
        display_name=name,
        email=email,
        department=department,
        region=region,
        employment_type=employment_type,
        manager="Nina Patel",
    )
