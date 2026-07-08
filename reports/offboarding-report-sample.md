# Offboarding Report: Priya Shah

Simulation-only offboarding plan for Priya Shah.

## Findings

- Departure workflow requires HR confirmation and manager timing approval.
- Mailbox handoff should be reviewed with Elena Cruz before access removal.
- SaaS deprovisioning payloads are prepared but not executed.

## Planned Actions

- `plan` disable-sign-in: Disable sign-in after approved departure time.
- `plan` revoke-sessions: Revoke active sessions.
- `plan` remove-licenses: Remove assigned licenses.
- `plan` remove-groups: Remove group memberships.
- `plan` deprovision-saas: Prepare Slack, Box, Notion, Zoom, and ExpenseCloud deprovisioning payloads.

## Safety Notes

- Offboarding actions are destructive in real systems, so this lab converts them to plan-only actions.
- No live tenant, Graph, or SaaS calls are made.
