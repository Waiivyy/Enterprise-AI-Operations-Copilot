from app.models.workflow import ChatRequest
from app.providers.llm_base import LLMProvider


class MockLLMProvider(LLMProvider):
    def build_tool_plan(self, request: ChatRequest) -> list[str]:
        if request.scenario == "onboarding":
            return ["recommend_license", "recommend_groups", "generate_saas_payloads", "plan_graph_actions", "create_report"]
        if request.scenario == "offboarding":
            return ["get_user_state", "generate_saas_payloads", "plan_graph_actions", "create_report"]
        if request.scenario == "access_troubleshooting":
            return ["get_user_state", "troubleshoot_access", "create_report"]
        if request.scenario == "ticket_analysis":
            return ["analyze_ticket", "create_report"]
        return ["create_report"]
