# Access Troubleshooting Report: maria.novak@example.invalid

Likely cause: Teams license missing.

## Evidence

- User has `sku-m365-business-basic`.
- Sample Teams policy requires `sku-m365-business-premium`.
- User is still enabled and has baseline group membership.

## Planned Actions

- `plan` review-license-assignment: Review license assignment against the mock Teams policy.
- `plan` review-group-membership: Confirm required group membership.
- `plan` collect-client-error: Capture client-side timestamp if the license review does not explain the issue.

## Safety Notes

- This is a mock diagnosis from sample tenant state.
- No Graph checks are executed against a live tenant.
