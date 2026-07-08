# Onboarding Report: Sara Holm

Simulation-only onboarding plan for Sara Holm, a full-time Engineering employee in Europe.

## Findings

- Recommended license: Microsoft 365 Business Premium (`sku-m365-business-premium`).
- Recommended groups: `group-employees`, `group-engineering`, `group-europe`.
- SaaS payloads prepared for Slack, Box, Notion, Zoom, and GitHub Enterprise.
- Required approvals: manager approval and application owner approval for privileged tools.

## Planned Actions

- `plan` assign-license: Assign Microsoft 365 Business Premium.
- `plan` add-group:group-engineering: Add user to Engineering group.
- `plan` add-group:group-europe: Add user to Europe group.
- `plan` provision-saas: Prepare SaaS provisioning payloads.

## Safety Notes

- Simulation only: no Microsoft Graph, SaaS, or tenant write calls are made.
- All identities, groups, licenses, and domains are fake demo values.
- No tenant changes were executed.
