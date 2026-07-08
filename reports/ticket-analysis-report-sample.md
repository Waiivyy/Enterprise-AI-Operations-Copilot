# Ticket Analysis Report: TCK-1001

Ticket classified as access troubleshooting with medium urgency and medium risk.

## Ticket

- Requester: Maria Novak (`maria.novak@example.invalid`)
- Title: Cannot access Teams
- Description: Maria can sign in but Teams says the license is missing.

## Findings

- Category: access troubleshooting.
- Likely system: Microsoft Teams.
- Automation candidate: yes, because the first checks are read-only and policy-based.
- Required approval: service owner review if license assignment changes are needed.

## Suggested Next Steps

- Check license assignment.
- Review group membership.
- Confirm account sign-in is enabled.
- Inspect conditional access placeholders in mock policy.

## Safety Notes

- Ticket analysis is advisory and should be reviewed by the service desk.
- No live tenant data is read.
