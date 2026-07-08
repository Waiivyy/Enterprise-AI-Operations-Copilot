# Tool Calling Design

The mock LLM provider returns deterministic tool names instead of free-form actions. `ToolRouter` exposes the only tools the planner can call:

- `get_user_state`
- `recommend_license`
- `recommend_groups`
- `generate_saas_payloads`
- `analyze_ticket`
- `create_report`
- `plan_graph_actions`
- `troubleshoot_access`

This keeps the default demo predictable and safe. A future real provider should produce the same structured plan shape and pass through the same router and guardrails.
