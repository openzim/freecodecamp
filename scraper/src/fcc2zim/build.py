import json
from collections import OrderedDict
from pathlib import Path

from zimscraperlib.zim import Creator

from fcc2zim.constants import Global


def build_curriculum_redirects(curriculum_dist: Path, fcc_lang: str):
    """
    Build the list of redirects from challenge URL to Vite hash URL

    The Vite app uses its own router to navigate. We have a single HTML file, but we
    need an URL for each challenge for the zim search to work.
    This builds the list of redirect needed fron the challenge URL to Vite hash URL.
    """
    index_json_path = curriculum_dist.joinpath("curriculum", fcc_lang, "index.json")
    with open(index_json_path) as course_index_str:
        superblock_dict = json.load(course_index_str)[fcc_lang]

    redirects = []
    for superblock in superblock_dict:
        course_list = superblock_dict[superblock]
        for course in course_list:
            meta_json_path = Path(
                curriculum_dist,
                "curriculum",
                fcc_lang,
                superblock,
                course,
                "_meta.json",
            )
            challenges = json.loads(meta_json_path.read_text())["challenges"]
            for challenge in challenges:
                title = challenge["title"]
                redirects.append(
                    (f'{fcc_lang}/{superblock}/{course}/{challenge["slug"]}', title)
                )

    return OrderedDict(redirects).items()


def build_command(
    zimui_dist: Path,
    fcc_lang: str,
    creator: Creator,
    curriculum_dist: Path,
):
    Global.logger.info("Scraper: build phase starting")

    # Add zimui files
    for file in zimui_dist.rglob("*"):
        if file.is_dir():
            continue
        path = str(Path(file).relative_to(zimui_dist))
        Global.logger.debug(f"Adding {path} to ZIM")
        creator.add_item_for(path, fpath=file)

    # Add prebuild generated curriculum file
    for file in curriculum_dist.rglob("*"):
        if file.is_dir():
            continue
        path = str(Path("fcc").joinpath(Path(file).relative_to(curriculum_dist)))
        Global.logger.debug(f"Adding {path} to ZIM")
        creator.add_item_for(path, fpath=file)

    for redir_slug, redir_title in build_curriculum_redirects(
        curriculum_dist=curriculum_dist, fcc_lang=fcc_lang
    ):
        redirect_path = f"{redir_slug}"
        redirect_url = redir_slug.count("/") * "../" + f"index.html#{redir_slug}"
        content = (
            f"<html><head><title>{redir_title}</title>"
            f'<meta http-equiv="refresh" content="0;URL=\'{redirect_url}\'" />'
            f"</head><body></body></html>"
        )
        Global.logger.debug(
            f"Redirecting {redirect_path} to {redirect_url} for slug {redir_slug}"
            f"and title {redir_title}",
        )
        creator.add_item_for(
            redirect_path,
            content=bytes(content, "utf-8"),
            title=redir_title,
            mimetype="text/html",
            is_front=True,
        )
        # Example index.html#/english/regular-expressions/extract-matches

    Global.logger.info("Scraper: build phase finished")
