from pathlib import Path

from pydantic import BaseModel, Field


class ReportRequest(BaseModel):
    report_type: str
    subject: str
    summary: str
    findings: list[str] = Field(default_factory=list)
    planned_actions: list[dict] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)
    simulation_only: bool = True


class ReportResult(BaseModel):
    report_id: str
    markdown_path: Path
    json_path: Path
    simulation_only: bool = True
