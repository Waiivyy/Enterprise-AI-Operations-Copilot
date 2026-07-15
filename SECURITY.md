# Security Policy

## Supported Versions

This repository is a simulation-first engineering demo. Security fixes are applied to the latest code on `main` and the current `0.1.x` release line.

| Version | Supported |
| --- | --- |
| `main` | Yes |
| `0.1.x` | Yes |
| Earlier versions | No |

## Reporting a Vulnerability

Use GitHub private vulnerability reporting for this repository when it is available. Include:

- The affected file, endpoint, or workflow.
- Reproduction steps using only fake data and `example.invalid` identities.
- The expected impact within this simulation-first application.
- A suggested mitigation, if known.

Do not include real credentials, tenant identifiers, access tokens, employee data, or support-ticket content. If private reporting is unavailable, open a public issue that requests a private contact channel without disclosing sensitive details.

## Security Boundary

The project does not execute Microsoft Graph or SaaS tenant changes. Reports and planned actions are demo artifacts, not evidence that a real operation occurred. A change that introduces live credentials, production endpoints, or write-capable integrations requires a separate threat model and security review before it can be accepted.
