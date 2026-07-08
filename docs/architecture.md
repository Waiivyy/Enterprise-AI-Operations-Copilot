# Architecture

The app is a FastAPI service with a static UI, Pydantic request and response schemas, deterministic planning logic, and mock tools.

Core flow:

1. A user submits a scenario and natural-language request.
2. `CopilotPlanner` asks the mock LLM provider for a structured tool plan.
3. The planner routes only to approved local mock tools.
4. Guardrails convert any execution-oriented action into a plan-only action.
5. The report writer creates Markdown and JSON planning reports under `reports/`.

The tool boundary is intentionally explicit. Adding a real provider later should not bypass the planner, guardrails, or report model.
