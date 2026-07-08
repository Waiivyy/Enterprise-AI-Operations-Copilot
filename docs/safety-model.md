# Safety Model

The lab is public-safe by default.

Rules:

- No real tenant actions.
- No live Microsoft Graph calls.
- No real SaaS API calls.
- No secrets in source control.
- No production domains.
- Demo identities must use `example.invalid`.
- Group IDs and license SKUs must be fake readable identifiers.
- Execution requests are rewritten as plan-only actions.
- Reports must avoid sensitive data and must state that no changes were executed.

The safety guardrails live in `app/copilot/safety_guardrails.py`. They are intentionally simple so the behavior is easy to audit and extend.
