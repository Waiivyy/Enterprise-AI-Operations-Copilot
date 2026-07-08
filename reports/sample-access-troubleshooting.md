# Access Troubleshooting Report: maria.novak@example.invalid

Likely cause: Teams license missing.

## Findings

- User has `sku-m365-business-basic`.
- Sample Teams policy requires `sku-m365-business-premium`.
- Recommended action: review license assignment and group membership.

## Planned Actions

- `plan` review-license-assignment: Review the license recommendation against mock app policy.
- `plan` review-group-membership: Review group membership required by the mock app policy.

## Safety Notes

- Simulation only: no Microsoft Graph, SaaS, or tenant write calls are made.
- No tenant changes were executed.
