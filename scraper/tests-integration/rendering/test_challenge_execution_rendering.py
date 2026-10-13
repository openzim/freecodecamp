"""Ensure challenge execution works fully offline, against a real challenge.

Regression test for https://github.com/openzim/freecodecamp/issues/157: zimui used to
run challenge test code by eval()-ing it directly in the main thread, with chai and
curriculum-helpers' JS helpers exposed as globals. It now delegates to
@freecodecamp/curriculum-helpers' worker-based test-runner, which runs the test code
in a Web Worker (javascript-test-evaluator.js) loaded from a local, vendored copy.
This drives a real "debugging" course challenge end-to-end (typing a solution,
checking it, and waiting for the hint to pass) to make sure the worker loads and
replies correctly, and never reaches out to the network while doing so.
"""

from playwright.sync_api import Browser

SUPERBLOCK = "javascript-algorithms-and-data-structures"
COURSE = "debugging"
# "Use the JavaScript Console to Check the Value of a Variable"
CHALLENGE_ID = "587d7b83367417b2b2512b33"
SOLUTION = "var a = 5; console.log(a);"


def test_challenge_passes_and_runs_fully_offline(browser: Browser, base_url: str):
    page = browser.new_page()
    requests: list[str] = []
    page.on("request", lambda request: requests.append(request.url))

    page.goto(f"{base_url}/index.html#{SUPERBLOCK}/{COURSE}/{CHALLENGE_ID}")
    page.wait_for_selector(".cm-content", timeout=15_000)
    # Wait for the automatic check-on-load (against the unsolved seed code) to settle
    # before interacting, so it does not race with typing the solution below.
    page.wait_for_selector(".hint", timeout=15_000)

    # Replace the seed code with a known-good solution.
    page.click(".cm-content")
    page.keyboard.press("ControlOrMeta+a")
    page.keyboard.press("Delete")
    page.keyboard.type(SOLUTION)

    page.get_by_text("Check Your Code", exact=True).click()

    # The worker-based test-runner replies asynchronously (postMessage round trip),
    # unlike the old eval()-based implementation which updated the hint synchronously.
    # test_passed.svg embeds a data-playwright-test-label marker, but it is only ever
    # rendered as a data: URI (never parsed into the DOM), so it has to be matched as
    # a plain substring of the <img>'s src attribute rather than as a real attribute.
    page.wait_for_selector('.hint img[src*="test-pass-icon"]', timeout=10_000)

    page.close()

    external_requests = [
        url
        for url in requests
        if not url.startswith(base_url) and not url.startswith("blob:")
    ]
    assert external_requests == [], (
        "Challenge execution must never reach out to a CDN or any other external "
        f"host when used offline, but it requested: {external_requests}"
    )
