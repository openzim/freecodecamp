This folder contains integration tests, testing how the scraper behaves end-to-end,
building a ZIM out of a couple of small freeCodeCamp courses (`debugging` and
`project-euler-problems-101-to-200`).

- `structure/` checks the resulting ZIM directly (metadata, entries, content), with
  `zimscraperlib`. It is run from the scraper Docker image, from GitHub workflow(s).
- `rendering/` checks that content actually renders as expected in a browser, fully
  offline (no CDN/network request), using Playwright against a plain HTTP server
  serving the ZIM content dumped with `zimdump`. This covers MathJax typesetting
  math-heavy challenges and running challenge tests (the worker-based test-runner),
  but more rendering checks can be added here. It needs a browser (installed with
  `playwright install --with-deps chromium`) and
  is run directly on the GitHub runner, from GitHub workflow(s), against a dump of
  the ZIM built by the `run-integration-tests` job.
