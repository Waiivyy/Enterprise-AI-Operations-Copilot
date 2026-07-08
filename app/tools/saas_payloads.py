from app.models.user import UserProfile
from app.models.workflow import SaaSPayload


DEPARTMENT_APPS = {
    "engineering": ["Slack", "Box", "Notion", "Zoom", "GitHub Enterprise"],
    "finance": ["Slack", "Box", "Notion", "Zoom", "ExpenseCloud"],
    "sales": ["Slack", "Box", "Notion", "Zoom", "CRM Sandbox"],
}


def generate_saas_payloads(user: UserProfile, operation: str = "provision") -> list[SaaSPayload]:
    apps = DEPARTMENT_APPS.get(user.department_key, ["Slack", "Box", "Notion", "Zoom"])
    return [
        SaaSPayload(
            app=app,
            operation=operation,
            payload={
                "user": user.email,
                "display_name": user.display_name,
                "department": user.department,
                "region": user.region,
                "mode": "simulation",
            },
        )
        for app in apps
    ]
