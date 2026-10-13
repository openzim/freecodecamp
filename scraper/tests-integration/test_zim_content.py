import json
from pathlib import Path

from zimscraperlib.zim import Archive

SUPERBLOCK = "javascript-algorithms-and-data-structures"
COURSE = "debugging"
SAMPLE_CHALLENGE_ID = "587d7b83367417b2b2512b33"
SAMPLE_CHALLENGE_TITLE = "Use the JavaScript Console to Check the Value of a Variable"
EXPECTED_CHALLENGE_COUNT = 12


def test_is_file(zim_file_path: Path):
    """Ensure ZIM file exists"""
    assert zim_file_path.exists()
    assert zim_file_path.is_file()


def test_zim_main_page(zim_fh: Archive):
    """Ensure main page is a redirect to index.html"""

    main_entry = zim_fh.main_entry
    assert main_entry.is_redirect
    assert main_entry.get_redirect_entry().path == "index.html"


def test_zim_metadata(zim_fh: Archive):
    """Ensure scraper and zim metadata are present and correct"""

    assert "fcc2zim v" in zim_fh.get_text_metadata("Scraper")
    assert zim_fh.get_text_metadata("Title") == "FCC Debugging Test"
    assert zim_fh.get_text_metadata("Description") == "Test ZIM for integration tests"
    assert zim_fh.get_text_metadata("Language") == "eng"
    assert zim_fh.get_text_metadata("Publisher") == "openZIM"
    assert zim_fh.get_text_metadata("Creator") == "freeCodeCamp"


def test_zim_tags(zim_fh: Archive):
    """Ensure expected tags are present"""

    tags = zim_fh.get_metadata("Tags").decode()
    for expected_tag in ["FCC", "freeCodeCamp"]:
        assert expected_tag in tags


def test_zim_content_zimui_index(zim_fh: Archive):
    """Ensure the ZIM UI entrypoint is present"""

    index_item = zim_fh.get_item("index.html")
    assert index_item.mimetype == "text/html"
    assert len(index_item.content) > 0


def test_zim_content_curriculum_index(zim_fh: Archive):
    """Ensure curriculum index lists the expected course and challenges"""

    index_item = zim_fh.get_item("content/curriculum/index.json")
    assert index_item.mimetype == "application/json"
    index = json.loads(bytes(index_item.content))

    challenges = index[SUPERBLOCK][COURSE]
    assert len(challenges) == EXPECTED_CHALLENGE_COUNT
    assert {"title": SAMPLE_CHALLENGE_TITLE, "slug": SAMPLE_CHALLENGE_ID} in challenges


def test_zim_content_challenge_markdown(zim_fh: Archive):
    """Ensure a sample challenge markdown file is present and readable"""

    challenge_item = zim_fh.get_item(
        f"content/curriculum/{SUPERBLOCK}/{COURSE}/{SAMPLE_CHALLENGE_ID}.md"
    )
    assert challenge_item.mimetype.startswith("text/")
    content = bytes(challenge_item.content).decode()
    assert SAMPLE_CHALLENGE_TITLE in content
    assert "console.log" in content


def test_zim_content_challenge_redirect(zim_fh: Archive):
    """Ensure a sample challenge has its index redirect page"""

    redirect_item = zim_fh.get_item(
        f"index/{SUPERBLOCK}/{COURSE}/{SAMPLE_CHALLENGE_ID}.html"
    )
    assert redirect_item.mimetype == "text/html"
    content = bytes(redirect_item.content).decode()
    assert SAMPLE_CHALLENGE_TITLE in content
    assert f"../../../index.html#{SUPERBLOCK}/{COURSE}/{SAMPLE_CHALLENGE_ID}" in content


def test_zim_content_locales(zim_fh: Archive):
    """Ensure client locales have been included"""

    locale_item = zim_fh.get_item("content/locales/translations.json")
    assert locale_item.mimetype == "application/json"
    locale = json.loads(bytes(locale_item.content))
    assert len(locale) > 0
