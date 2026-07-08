from fastapi import APIRouter

from app.copilot.planner import CopilotPlanner
from app.models.workflow import (
    AccessTroubleshootingRequest,
    ChatResponse,
    OffboardingPlan,
    OffboardingRequest,
    OnboardingPlan,
    OnboardingRequest,
)

router = APIRouter()
planner = CopilotPlanner()


@router.post("/workflows/onboarding", response_model=OnboardingPlan)
def onboarding(request: OnboardingRequest) -> OnboardingPlan:
    return planner.plan_onboarding(request)


@router.post("/workflows/offboarding", response_model=OffboardingPlan)
def offboarding(request: OffboardingRequest) -> OffboardingPlan:
    return planner.plan_offboarding(request)


@router.post("/workflows/troubleshoot-access", response_model=ChatResponse)
def troubleshoot_access(request: AccessTroubleshootingRequest) -> ChatResponse:
    return planner.troubleshoot_access(request)
