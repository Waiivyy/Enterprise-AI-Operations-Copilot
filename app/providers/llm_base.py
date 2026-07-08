from abc import ABC, abstractmethod

from app.models.workflow import ChatRequest


class LLMProvider(ABC):
    @abstractmethod
    def build_tool_plan(self, request: ChatRequest) -> list[str]:
        """Return deterministic tool names the planner should execute."""
