from app.models.report import ReportResult
from app.models.workflow import ChatResponse, PlannedAction, Scenario


def build_chat_response(
    *,
    scenario: Scenario,
    summary: str,
    tool_plan: list[str],
    planned_actions: list[PlannedAction],
    safety_notes: list[str],
    evidence: list[str] | None = None,
    report: ReportResult | None = None,
    report_id: str | None = None,
) -> ChatResponse:
    return ChatResponse(
        scenario=scenario,
        summary=summary,
        tool_plan=tool_plan,
        planned_actions=planned_actions,
        safety_notes=safety_notes,
        evidence=evidence or [],
        report_id=report.report_id if report else report_id,
        report_markdown=str(report.markdown_path) if report else None,
        report_json=str(report.json_path) if report else None,
    )
