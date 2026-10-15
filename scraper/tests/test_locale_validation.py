import json
import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import pytest

from fcc2zim.locale_validation import logger, validate_locales

JsonDict = dict[str, Any]


class ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.messages: list[str] = []

    def emit(self, record: logging.LogRecord):
        self.messages.append(record.getMessage())


VALID_TRANSLATIONS: JsonDict = {
    "buttons": {
        "check-code": "Check Your Code",
        "reset-lesson": "Reset Lesson",
        "run": "Run",
        "go-to-next": "Go to Next Challenge",
    },
    "learn": {
        "heading": "Learn",
        "reset": "Reset",
        "reset-warn": "Are you sure you want to reset '{{title}}'?",
        "reset-warn-2": "This cannot be undone.",
    },
}

VALID_INTRO: JsonDict = {
    "misc-text": {
        "courses": "Courses",
        "expand": "Expand",
        "collapse": "Collapse",
    },
}

VALID_MOTIVATION: JsonDict = {
    "compliments": ["Nice job!"],
    "motivationalQuotes": [{"quote": "Keep going.", "author": "Someone"}],
}


def write_locales(
    path: Path,
    *,
    translations: JsonDict | None = VALID_TRANSLATIONS,
    intro: JsonDict | None = VALID_INTRO,
    motivation: JsonDict | None = VALID_MOTIVATION,
    skip_motivation: bool = False,
):
    path.mkdir(parents=True, exist_ok=True)
    path.joinpath("translations.json").write_text(json.dumps(translations))
    path.joinpath("intro.json").write_text(json.dumps(intro))
    if not skip_motivation:
        path.joinpath("motivation.json").write_text(json.dumps(motivation))


class TestLocaleValidation:
    def setup_method(self):
        self.tmp_dir = TemporaryDirectory(prefix="fcc2zim_locale_tests_")
        self.locales_path = Path(self.tmp_dir.name)

    def teardown_method(self):
        self.tmp_dir.cleanup()

    def test_valid_locales_ok(self):
        write_locales(self.locales_path)
        validate_locales(self.locales_path, {})

    def test_motivation_file_missing_ko(self):
        write_locales(self.locales_path, skip_motivation=True)
        with pytest.raises(FileNotFoundError):
            validate_locales(self.locales_path, {})

    @pytest.mark.parametrize(
        "motivation, match",
        [
            pytest.param({}, "missing or empty 'compliments'", id="no_keys"),
            pytest.param(
                {
                    "compliments": [],
                    "motivationalQuotes": [{"quote": "q", "author": "a"}],
                },
                "missing or empty 'compliments'",
                id="empty_compliments",
            ),
            pytest.param(
                {
                    "compliments": ["", "Nice!"],
                    "motivationalQuotes": [{"quote": "q", "author": "a"}],
                },
                "'compliments' must be a list of non-empty strings",
                id="blank_compliment",
            ),
            pytest.param(
                {"compliments": ["Nice!"], "motivationalQuotes": []},
                "missing or empty 'motivationalQuotes'",
                id="empty_quotes",
            ),
            pytest.param(
                {"compliments": ["Nice!"], "motivationalQuotes": [{"quote": "q"}]},
                "'motivationalQuotes' must be a list of objects",
                id="quote_missing_author",
            ),
        ],
    )
    def test_motivation_content_ko(self, motivation: JsonDict, match: str):
        write_locales(self.locales_path, motivation=motivation)
        handler = ListHandler()
        logger.addHandler(handler)
        try:
            with pytest.raises(ValueError, match="Locale validation failed"):
                validate_locales(self.locales_path, {})
        finally:
            logger.removeHandler(handler)
        assert any(match in message for message in handler.messages)
