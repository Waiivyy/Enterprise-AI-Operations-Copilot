import json
import re
from datetime import datetime, timezone
from pathlib import Path

from app.models.report import ReportRequest, ReportResult


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "report"


def create_report(request: ReportRequest, output_dir: Path | str = Path("reports")) -> ReportResult:
    report_dir = Path(output_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_id = f"{timestamp}-{_slug(request.report_type)}-{_slug(request.subject)}"
    markdown_path = report_dir / f"{report_id}.md"
    json_path = report_dir / f"{report_id}.json"

    markdown = [
        f"# {request.report_type.title()} Report: {request.subject}",
        "",
        request.summary,
        "",
        "## Findings",
        *[f"- {finding}" for finding in request.findings],
        "",
        "## Planned Actions",
        *[
            f"- `{action.get('operation', 'plan')}` {action.get('target', 'unknown')}: {action.get('description', 'No description')}"
            for action in request.planned_actions
        ],
        "",
        "## Safety Notes",
        *[f"- {note}" for note in request.safety_notes],
        "",
        "_Simulation-only report. No tenant changes were executed._",
        "",
    ]
    markdown_path.write_text("\n".join(markdown), encoding="utf-8")
    json_path.write_text(json.dumps(request.model_dump(), indent=2), encoding="utf-8")
    return ReportResult(report_id=report_id, markdown_path=markdown_path, json_path=json_path)
