# Contributing

Contributions should preserve the project's simulation-first safety boundary and keep the demo deterministic, public-safe, and easy to run locally.

## Development Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

For the browser smoke test:

```bash
python -m pip install -e ".[dev,e2e]"
python -m playwright install chromium
pytest -m e2e
```

On a managed workstation where the Playwright browser download is blocked, set `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` to an installed Chromium-based browser before running the test. CI always installs and uses Playwright's managed Chromium build.

## Pull Requests

- Keep changes focused and explain the workflow or safety behavior they affect.
- Add or update tests for changed behavior.
- Use fake identities under `example.invalid` and readable mock IDs.
- Update documentation and sample output when an API contract or visible UI changes.
- Confirm that unit tests and the browser smoke test pass before requesting review.

## Safety Requirements

Contributions must not add real tenant data, credentials, access tokens, production domains, or write-capable external calls. Requests that imply execution must continue to be converted into simulation-only plans. Optional provider integrations must be disabled by default and require explicit local configuration.

## Reports and Generated Files

Runtime reports and SQLite databases are ignored. Commit only deliberately reviewed sample reports whose filenames match the existing `*-sample.md` and `*-sample.json` convention.
