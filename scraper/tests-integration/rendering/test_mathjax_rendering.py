"""Ensure MathJax renders math-heavy challenges fully offline.

Regression test for https://github.com/openzim/freecodecamp/issues/57: the
"Problem 101: Optimum polynomial" Project Euler challenge mixes inline math, a
LaTeX array environment and the `\\color` extension, and used to fail to
render with the vendored MathJax. It is also a good exercise of the MathJax 4
upgrade, since some of its glyphs are only available in a font chunk loaded
dynamically, which must come from the vendored, local copy and never from a
CDN since the ZIM is meant to be used fully offline.
"""

from playwright.sync_api import Browser

SUPERBLOCK = "project-euler"
COURSE = "project-euler-problems-101-to-200"
CHALLENGE_ID = "5900f3d21000cf542c50fee4"  # "Problem 101: Optimum polynomial"


def test_mathjax_renders_without_any_external_request(browser: Browser, base_url: str):
    page = browser.new_page()
    requests: list[str] = []
    page.on("request", lambda request: requests.append(request.url))

    page.goto(f"{base_url}/index.html#{SUPERBLOCK}/{COURSE}/{CHALLENGE_ID}")
    # MathJax replaces the raw LaTeX source with <mjx-container> elements containing
    # a rendered <svg>, once it is done typesetting the page.
    page.wait_for_selector("mjx-container svg", timeout=15_000)

    svg_count = page.locator("mjx-container svg").count()
    assert (
        svg_count >= 10
    ), f"expected many equations to be typeset as SVG, got {svg_count}"

    # The \color{red} extension used by this challenge should have produced some
    # red-colored glyphs: if MathJax failed to parse/typeset the equation (the
    # original issue), none of this would be present.
    red_glyphs = page.locator('[fill="red"], [stroke="red"]').count()
    assert red_glyphs > 0, "expected the \\color{red} extension to have been applied"

    page.close()

    external_requests = [
        url
        for url in requests
        if not url.startswith(base_url) and not url.startswith("blob:")
    ]
    assert external_requests == [], (
        "MathJax must never reach out to a CDN or any other external host when "
        f"used offline, but it requested: {external_requests}"
    )
