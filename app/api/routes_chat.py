from fastapi import APIRouter

from app.copilot.planner import CopilotPlanner
from app.core.config import get_settings
from app.models.workflow import ChatRequest, ChatResponse

router = APIRouter()
planner = CopilotPlanner(report_dir=get_settings().reports_dir)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return planner.handle_chat(request)
