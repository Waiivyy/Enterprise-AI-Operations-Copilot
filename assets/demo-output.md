# Demo Output

## Onboarding Prompt

Prompt:

```text
Plan onboarding for Sara, full-time employee in Europe, joining Engineering next Monday.
```

Expected response shape:

```json
{
  "scenario": "onboarding",
  "summary": "Simulation-only onboarding plan for Sara Holm. Recommended Microsoft 365 Business Premium.",
  "tool_plan": [
    "recommend_license",
    "recommend_groups",
    "generate_saas_payloads",
    "plan_graph_actions",
    "create_report"
  ],
  "planned_actions": [
    {
      "operation": "plan",
      "target": "assign-license",
      "description": "Assign Microsoft 365 Business Premium",
      "simulation_only": true
    },
    {
      "operation": "plan",
      "target": "add-group:group-engineering",
      "description": "Add to Engineering",
      "simulation_only": true
    }
  ],
  "safety_notes": [
    "Simulation only: no Microsoft Graph, SaaS, or tenant write calls are made."
  ]
}
```

## Access Troubleshooting Prompt

Prompt:

```text
Maria cannot access Teams.
```

Expected finding:

- Likely cause: Teams license missing.
- Evidence: Maria has `sku-m365-business-basic`, while the sample Teams policy requires `sku-m365-business-premium`.
- Recommended action: review license assignment and group membership.
- Confidence: high enough for triage, not a production diagnosis.

## Missing Group Prompt

Prompt:

```text
lena.ortiz@example.invalid cannot access Teams.
```

Expected finding:

- Likely cause: Teams group membership missing.
- Evidence: user has the Teams license but lacks `group-employees`.
- Recommended action: review group membership and app assignment policy.

## Ticket Classification Prompt

Prompt:

```text
Analyze this ticket: Noah has the Teams license but access is blocked after a device compliance prompt.
```

Expected finding:

- Category: device compliance.
- Likely system: endpoint compliance.
- Automation candidate: no, because the workflow needs endpoint review.
