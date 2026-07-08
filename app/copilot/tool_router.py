from app.models.ticket import Ticket
from app.models.user import UserProfile
from app.tools.graph_mock import get_user_state, plan_graph_actions, troubleshoot_access
from app.tools.group_advisor import recommend_groups
from app.tools.license_advisor import recommend_license
from app.tools.saas_payloads import generate_saas_payloads
from app.tools.ticket_analyzer import analyze_ticket


class ToolRouter:
    """Small explicit router for mock tools that are safe to execute locally."""

    allowed_tools = {
        "get_user_state",
        "recommend_license",
        "recommend_groups",
        "generate_saas_payloads",
        "analyze_ticket",
        "create_report",
        "plan_graph_actions",
        "troubleshoot_access",
    }

    def recommend_license(self, user: UserProfile):
        return recommend_license(user)

    def recommend_groups(self, user: UserProfile):
        return recommend_groups(user)

    def generate_saas_payloads(self, user: UserProfile, operation: str = "provision"):
        return generate_saas_payloads(user, operation=operation)

    def analyze_ticket(self, ticket: Ticket):
        return analyze_ticket(ticket)

    def get_user_state(self, email: str):
        return get_user_state(email)

    def troubleshoot_access(self, email: str, app_name: str = "Teams"):
        return troubleshoot_access(email, app_name=app_name)

    def plan_graph_actions(self, kind: str, user_email: str, targets: list[str]):
        return plan_graph_actions(kind, user_email, targets)
