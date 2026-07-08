from app.copilot.planner import CopilotPlanner
from app.models.workflow import ChatRequest


def test_planner_builds_onboarding_plan_with_safe_actions(tmp_path):
    planner = CopilotPlanner(report_dir=tmp_path)
    request = ChatRequest(
        scenario="onboarding",
        message="Plan onboarding for Sara, full-time employee in Europe, joining Engineering next Monday.",
    )

    response = planner.handle_chat(request)

    assert response.scenario == "onboarding"
    assert response.summary.startswith("Simulation-only onboarding plan")
    assert any(action.target == "assign-license" for action in response.planned_actions)
    assert any(action.target == "add-group:group-engineering" for action in response.planned_actions)
    assert all(action.simulation_only for action in response.planned_actions)
