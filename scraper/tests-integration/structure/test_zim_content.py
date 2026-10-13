import json
from pathlib import Path

from zimscraperlib.zim import Archive

SUPERBLOCK = "javascript-algorithms-and-data-structures"
COURSE = "debugging"
SAMPLE_CHALLENGE_ID = "587d7b83367417b2b2512b33"
SAMPLE_CHALLENGE_TITLE = "Use the JavaScript Console to Check the Value of a Variable"
EXPECTED_CHALLENGE_COUNT = 12

# This course is also scraped alongside `debugging` (see the "Run scraper" step in the
# GitHub workflows) because it contains math-heavy challenges, used by the MathJax
# rendering tests in ../rendering. See https://github.com/openzim/freecodecamp/issues/57
EULER_SUPERBLOCK = "project-euler"
EULER_COURSE = "project-euler-problems-101-to-200"
EULER_SAMPLE_CHALLENGE_ID = "5900f3d21000cf542c50fee4"
EULER_SAMPLE_CHALLENGE_TITLE = "Problem 101: Optimum polynomial"


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
    assert zim_fh.get_text_metadata("Title") == "FCC Integration Test"
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


def test_zim_content_curriculum_index_math_course(zim_fh: Archive):
    """Ensure the math-heavy course used for MathJax tests is present too"""

    index_item = zim_fh.get_item("content/curriculum/index.json")
    index = json.loads(bytes(index_item.content))

    challenges = index[EULER_SUPERBLOCK][EULER_COURSE]
    assert {
        "title": EULER_SAMPLE_CHALLENGE_TITLE,
        "slug": EULER_SAMPLE_CHALLENGE_ID,
    } in challenges


def test_zim_content_challenge_markdown_mathjax(zim_fh: Archive):
    """Ensure the math-heavy challenge markdown still contains its LaTeX source

    Regression test for https://github.com/openzim/freecodecamp/issues/57: this
    challenge mixes inline math, a LaTeX array environment and the \\color
    extension. Actual MathJax rendering is checked in ../rendering.
    """

    challenge_item = zim_fh.get_item(
        f"content/curriculum/{EULER_SUPERBLOCK}/{EULER_COURSE}/"
        f"{EULER_SAMPLE_CHALLENGE_ID}.md"
    )
    content = bytes(challenge_item.content).decode()
    assert EULER_SAMPLE_CHALLENGE_TITLE in content
    assert "\\begin{array}" in content
    assert "\\color{red}" in content


def test_zim_content_locales(zim_fh: Archive):
    """Ensure client locales have been included"""

    locale_item = zim_fh.get_item("content/locales/translations.json")
    assert locale_item.mimetype == "application/json"
    locale = json.loads(bytes(locale_item.content))
    assert len(locale) > 0
