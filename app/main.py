from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import routes_chat, routes_health, routes_tickets, routes_workflows
from app.core.config import get_settings
from app.core.database import seed_demo_database
from app.core.logging import configure_logging

configure_logging()
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Simulation-first AI operations copilot for enterprise IT teams.",
    version="0.1.0",
)

app.include_router(routes_health.router)
app.include_router(routes_chat.router)
app.include_router(routes_tickets.router)
app.include_router(routes_workflows.router)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def startup() -> None:
    seed_demo_database()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
