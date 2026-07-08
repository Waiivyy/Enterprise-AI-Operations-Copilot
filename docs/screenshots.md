# Screenshots

Use this guide to capture visual proof for the README or GitHub repository page.

## Start the App

```bash
cd enterprise-ai-operations-copilot
source .venv/bin/activate
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Recommended Captures

1. UI homepage
   - Capture the page before submitting a prompt.
   - Show the title, scenario selector, example prompt buttons, and request box.

2. Onboarding response
   - Click `Onboard Sara`.
   - Click `Generate plan`.
   - Capture the structured response, planned actions, evidence, and safety notes.

3. Access troubleshooting response
   - Click `Teams license issue`.
   - Click `Generate plan`.
   - Capture the likely cause, evidence, and planned review actions.

4. Generated report output
   - Open one of the sample reports in `reports/`, or use a report generated during the demo run.
   - Capture the report title, findings, planned actions, and safety notes.

## Suggested Filenames

- `assets/screenshot-homepage.png`
- `assets/screenshot-onboarding-response.png`
- `assets/screenshot-access-troubleshooting.png`
- `assets/screenshot-ticket-analysis.png`
- `assets/screenshot-report-output.png` if you also capture a rendered report file later

Do not include real tenant data, production domains, real employee names, or real support tickets in screenshots.
