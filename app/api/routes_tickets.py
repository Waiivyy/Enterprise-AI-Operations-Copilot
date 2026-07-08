import json
from pathlib import Path

from fastapi import APIRouter

from app.copilot.planner import CopilotPlanner
from app.models.ticket import Ticket
from app.models.workflow import TicketAnalysisRequest, TicketAnalysisResponse

router = APIRouter()
planner = CopilotPlanner()
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_tickets.json"


@router.get("/tickets", response_model=list[Ticket])
def list_tickets() -> list[Ticket]:
    return [Ticket(**item) for item in json.loads(DATA_PATH.read_text())]


@router.post("/tickets/analyze", response_model=TicketAnalysisResponse)
def analyze_ticket(request: TicketAnalysisRequest) -> TicketAnalysisResponse:
    return planner.analyze_ticket(request.ticket)
