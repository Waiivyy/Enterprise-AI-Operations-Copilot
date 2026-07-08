import json

from app.models.report import ReportRequest
from app.tools.report_writer import create_report


def test_report_writer_creates_markdown_and_json(tmp_path):
    request = ReportRequest(
        report_type="onboarding",
        subject="Sara Holm",
        summary="Simulation-only onboarding plan.",
        findings=["Business Premium recommended"],
        planned_actions=[{"operation": "plan", "target": "assign-license"}],
        safety_notes=["No tenant changes executed."],
    )

    result = create_report(request, output_dir=tmp_path)

    assert result.markdown_path.exists()
    assert result.json_path.exists()
    assert "Simulation-only onboarding plan" in result.markdown_path.read_text()
    payload = json.loads(result.json_path.read_text())
    assert payload["subject"] == "Sara Holm"
    assert payload["simulation_only"] is True
