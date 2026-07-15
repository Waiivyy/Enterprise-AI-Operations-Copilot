import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen

import pytest

playwright_sync = pytest.importorskip(
    "playwright.sync_api",
    reason="Install the e2e dependency group to run browser tests.",
)
expect = playwright_sync.expect
sync_playwright = playwright_sync.sync_playwright

pytestmark = pytest.mark.e2e


def _available_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


def _wait_for_server(url: str, process: subprocess.Popen, timeout: float = 15.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Demo server exited before becoming ready.")
        try:
            with urlopen(f"{url}/health", timeout=1) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.1)
    raise TimeoutError(f"Demo server did not become ready at {url}.")


@pytest.fixture(scope="module")
def live_server(tmp_path_factory: pytest.TempPathFactory):
    repo_root = Path(__file__).resolve().parents[2]
    runtime_dir = tmp_path_factory.mktemp("ui-smoke")
    port = _available_port()
    url = f"http://127.0.0.1:{port}"
    env = os.environ.copy()
    env["REPORTS_DIR"] = str(runtime_dir / "reports")
    env["SQLITE_PATH"] = str(runtime_dir / "demo.sqlite")
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=repo_root,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_server(url, process)
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def test_user_can_generate_access_troubleshooting_plan(live_server: str):
    with sync_playwright() as playwright:
        executable_path = os.getenv("PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH")
        launch_options = {"headless": True}
        if executable_path:
            launch_options["executable_path"] = executable_path
        browser = playwright.chromium.launch(**launch_options)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})

        page.goto(live_server)
        expect(page.get_by_role("heading", name="Enterprise AI Operations Copilot")).to_be_visible()
        expect(page.get_by_text("Simulation mode", exact=True)).to_be_visible()

        page.get_by_role("button", name="Teams license issue").click()
        expect(page.locator("#scenario")).to_have_value("access_troubleshooting")
        expect(page.locator("#message")).to_have_value("Maria cannot access Teams.")

        with page.expect_response(
            lambda response: response.url.endswith("/chat") and response.request.method == "POST"
        ) as response_info:
            page.get_by_role("button", name="Generate plan").click()

        assert response_info.value.status == 200
        expect(page.locator("#summary")).to_contain_text('"scenario": "access_troubleshooting"')
        expect(page.locator("#summary")).to_contain_text("Teams license missing")
        expect(page.locator("#actions li").first).to_be_visible()
        expect(page.locator("#evidence li").first).to_be_visible()
        expect(page.locator("#safety li").first).to_contain_text("Simulation only")

        browser.close()
