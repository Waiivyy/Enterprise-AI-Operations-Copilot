# Changelog

## v0.1.0 - 2026-07-08

Initial simulation-first prototype.

- Added FastAPI backend with health, chat, ticket, onboarding, offboarding, and access troubleshooting endpoints.
- Added deterministic mock LLM provider and explicit mock tool router.
- Added mock Microsoft Graph-style tenant state, license advisor, group advisor, SaaS payload generator, and ticket analyzer.
- Added safety guardrails that convert destructive actions into simulation-only planned actions.
- Added Markdown and JSON report generation with public-safe sample reports.
- Added static UI for scenario-based demo prompts and structured response review.
- Added documentation for architecture, safety model, tool calling design, technical review, screenshots, and roadmap.
- Added Docker, Docker Compose, GitHub Actions CI, and pytest coverage.
