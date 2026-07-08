from app.models.workflow import ChatRequest
from app.providers.llm_base import LLMProvider


class OpenAICompatibleProvider(LLMProvider):
    """Optional provider seam. Disabled by default and intentionally not wired to secrets."""

    def __init__(self, base_url: str | None = None, model: str | None = None) -> None:
        self.base_url = base_url
        self.model = model

    def build_tool_plan(self, request: ChatRequest) -> list[str]:
        raise RuntimeError(
            "OpenAI-compatible provider is optional and disabled in the public-safe demo. "
            "Use the mock provider unless you intentionally add credentials outside the repo."
        )
