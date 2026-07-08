from fastapi import APIRouter

from app.copilot.planner import CopilotPlanner
from app.models.workflow import ChatRequest, ChatResponse

router = APIRouter()
planner = CopilotPlanner()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return planner.handle_chat(request)
