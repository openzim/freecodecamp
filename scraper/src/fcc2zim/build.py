import json
from dataclasses import dataclass
from pathlib import Path

from zimscraperlib.zim import Creator

from fcc2zim.context import Context

logger = Context.logger


@dataclass
class CurriculumRedirect:
    path: str
    title: str


def build_curriculum_redirects(curriculum_dist: Path):
    """
    Build the list of redirects from challenge URL to Vite hash URL

    The Vite app uses its own router to navigate. We have a single HTML file, but we
    need an URL for each challenge for the zim search to work.
    This builds the list of redirect needed fron the challenge URL to Vite hash URL.
    """
    index_json_path = curriculum_dist.joinpath("curriculum", "index.json")
    with open(index_json_path) as course_index_str:
        superblock_dict = json.load(course_index_str)

    redirects: list[CurriculumRedirect] = []
    for superblock, course_data in superblock_dict.items():
        for course, challenges in course_data.items():
            for challenge in challenges:
                title = challenge["title"]
                redirects.append(
                    CurriculumRedirect(
                        path=f'{superblock}/{course}/{challenge["slug"]}', title=title
                    )
                )

    return redirects


def build_command(
    zimui_dist: Path,
    creator: Creator,
    curriculum_dist: Path,
):
    logger.info("Scraper: build phase starting")

    # Add Mathjax files
    mathjax = (Path(__file__) / "../mathjax").resolve()
    count_mathjax_files = len(list(mathjax.rglob("*")))
    logger.info(f"Adding {count_mathjax_files} MathJax files in {mathjax}")
    for file in mathjax.rglob("*"):
        if not file.is_file():
            continue
        path = str(Path(file).relative_to(mathjax.parent))
        logger.debug(f"Adding {path} to ZIM")
        creator.add_item_for(
            path=path,
            fpath=file,
            is_front=False,
        )

    # Add fonts files
    fonts = (Path(__file__) / "../fonts").resolve()
    count_fonts_files = len(list(fonts.rglob("*")))
    logger.info(f"Adding {count_fonts_files} fonts files in {fonts}")
    for file in fonts.rglob("*"):
        if not file.is_file():
            continue
        path = Path("content") / Path(file).relative_to(fonts.parent)
        logger.debug(f"Adding {path} to ZIM")
        creator.add_item_for(
            path=str(path),
            fpath=file,
            is_front=False,
        )

    # Add zimui files
    for file in zimui_dist.rglob("*"):
        if file.is_dir():
            continue
        path = str(Path(file).relative_to(zimui_dist))
        logger.debug(f"Adding {path} to ZIM")
        creator.add_item_for(path, fpath=file)

    # Add prebuild generated curriculum file
    for file in curriculum_dist.rglob("*"):
        if file.is_dir():
            continue
        path = str(Path("content").joinpath(Path(file).relative_to(curriculum_dist)))
        logger.debug(f"Adding {path} to ZIM")
        creator.add_item_for(path, fpath=file)

    for redirection in build_curriculum_redirects(curriculum_dist=curriculum_dist):
        redirect_path = f"index/{redirection.path}.html"
        redirect_url = (
            redirection.path.count("/") + 1
        ) * "../" + f"index.html#{redirection.path}"
        content = (
            f"<html><head><title>{redirection.title}</title>"
            f'<meta http-equiv="refresh" content="0;URL=\'{redirect_url}\'" />'
            f"</head><body></body></html>"
        )
        logger.debug(
            f"Redirecting {redirect_path} to {redirect_url} for slug {redirection.path}"
            f"and title {redirection.title}",
        )
        creator.add_item_for(
            redirect_path,
            content=bytes(content, "utf-8"),
            title=redirection.title,
            mimetype="text/html",
            is_front=True,
        )
        # Example index.html#/regular-expressions/extract-matches

    logger.info("Scraper: build phase finished")
