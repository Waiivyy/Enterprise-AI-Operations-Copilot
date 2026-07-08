# Architecture

The app is a FastAPI service with a static UI, Pydantic request and response schemas, deterministic planning logic, and mock tools.

The default mode uses a deterministic mock LLM provider. That makes the project runnable without paid APIs or secrets while still demonstrating where a model provider would produce a structured tool plan.

Core flow:

1. A user submits a scenario and natural-language request.
2. `CopilotPlanner` asks the mock LLM provider for a structured tool plan.
3. The planner routes only to approved local mock tools.
4. Guardrails convert any execution-oriented action into a plan-only action.
5. The report writer creates Markdown and JSON planning reports under `reports/`.

The tool boundary is intentionally explicit. Adding a real provider later should not bypass the planner, guardrails, or report model.

Simulation boundary:

- The tool router exposes only local mock tools.
- The mock Graph client reads `app/data/mock_tenant_state.json`.
- SaaS payload generation creates local planning payloads only.
- Report generation writes Markdown and JSON files locally.
- No route performs a live tenant or SaaS action.
