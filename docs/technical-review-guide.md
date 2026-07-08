# Technical Review Guide

Review focus areas:

- Confirm all default data uses fake identities and `example.invalid`.
- Confirm no route performs real tenant or SaaS writes.
- Confirm `execute` inputs are converted into `plan` actions.
- Confirm report outputs state simulation-only behavior.
- Confirm optional provider code is disabled by default.
- Confirm tests cover advisors, guardrails, planner behavior, ticket analysis, and report output.
- Confirm route tests cover `/health` and `/chat`.
- Confirm mock tenant state includes license, group, and device/compliance access cases.
- Confirm README diagrams render on GitHub and screenshot guidance exists.

Useful commands:

```bash
pytest
uvicorn app.main:app --reload
curl -s http://127.0.0.1:8000/health
```

Suggested review prompts:

- `Plan onboarding for Sara, full-time employee in Europe, joining Engineering next Monday.`
- `Create an offboarding checklist for Priya leaving on Friday.`
- `Maria cannot access Teams.`
- `Analyze this ticket: Noah has the Teams license but access is blocked after a device compliance prompt.`
