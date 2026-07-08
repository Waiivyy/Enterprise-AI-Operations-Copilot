# Technical Review Guide

Review focus areas:

- Confirm all default data uses fake identities and `example.invalid`.
- Confirm no route performs real tenant or SaaS writes.
- Confirm `execute` inputs are converted into `plan` actions.
- Confirm report outputs state simulation-only behavior.
- Confirm optional provider code is disabled by default.
- Confirm tests cover advisors, guardrails, planner behavior, ticket analysis, and report output.

Useful commands:

```bash
pytest
uvicorn app.main:app --reload
curl -s http://127.0.0.1:8000/health
```
