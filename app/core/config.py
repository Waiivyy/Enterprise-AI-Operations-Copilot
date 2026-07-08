from functools import lru_cache
import os
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Enterprise AI Operations Copilot"
    llm_provider: str = "mock"
    openai_compatible_base_url: str | None = None
    openai_compatible_model: str | None = None
    reports_dir: Path = Path("reports")
    sqlite_path: Path = Path("app/data/demo.sqlite")
    simulation_mode: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings(
        llm_provider=os.getenv("LLM_PROVIDER", "mock"),
        openai_compatible_base_url=os.getenv("OPENAI_COMPATIBLE_BASE_URL") or None,
        openai_compatible_model=os.getenv("OPENAI_COMPATIBLE_MODEL") or None,
        reports_dir=Path(os.getenv("REPORTS_DIR", "reports")),
        sqlite_path=Path(os.getenv("SQLITE_PATH", "app/data/demo.sqlite")),
        simulation_mode=os.getenv("SIMULATION_MODE", "true").lower() == "true",
    )
