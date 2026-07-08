from app.copilot.planner import CopilotPlanner
from app.models.user import UserProfile
from app.models.workflow import ChatRequest, OffboardingRequest, OnboardingRequest


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


def test_onboarding_plan_creates_license_group_saas_and_report_actions(tmp_path):
    planner = CopilotPlanner(report_dir=tmp_path)
    user = UserProfile(
        display_name="Sara Holm",
        email="sara.holm@example.invalid",
        department="Engineering",
        region="Europe",
        employment_type="full-time",
    )

    plan = planner.plan_onboarding(OnboardingRequest(user=user))
    targets = {action.target for action in plan.planned_actions}

    assert plan.license.sku_id == "sku-m365-business-premium"
    assert {"group-engineering", "group-europe", "group-employees"} <= {group.group_id for group in plan.groups}
    assert {"Slack", "Box", "Notion", "Zoom", "GitHub Enterprise"} <= {payload.app for payload in plan.saas_payloads}
    assert {"assign-license", "add-group:group-engineering", "provision-saas:slack"} <= targets
    assert plan.report_id is not None


def test_offboarding_plan_converts_destructive_actions_to_simulation_only(tmp_path):
    planner = CopilotPlanner(report_dir=tmp_path)
    user = UserProfile(
        display_name="Priya Shah",
        email="priya.shah@example.invalid",
        department="Finance",
        region="North America",
        employment_type="full-time",
    )

    plan = planner.plan_offboarding(OffboardingRequest(user=user, preserve_mailbox_access_for="Elena Cruz"))

    assert {"disable-sign-in", "revoke-sessions", "remove-licenses", "remove-groups"} <= {
        action.target for action in plan.planned_actions
    }
    assert all(action.operation == "plan" for action in plan.planned_actions)
    assert all(action.simulation_only for action in plan.planned_actions)
    assert any("converted from execute" in action.safety_note for action in plan.planned_actions)
