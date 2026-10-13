import os

import pytest
from playwright.sync_api import Browser, sync_playwright


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL of a plain static file server exposing the dumped ZIM content

    (e.g. `zimdump dump --dir=<dir> <zim>` served with `python -m http.server`).
    The zimui app only ever uses relative URLs, so serving the dumped ZIM
    content like this is equivalent (for our purposes) to serving it from an
    actual ZIM through kiwix-serve.
    """
    return os.environ.get("RENDERING_TEST_BASE_URL", "http://localhost:8080")


@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()
