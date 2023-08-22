import json
import pathlib
from collections import OrderedDict
from datetime import datetime

from zimscraperlib.zim import Creator

from fcc2zim.constants import FCC_LANG_MAP, VERSION, Global

logo_path = pathlib.Path(__file__).parent.joinpath("assets", "fcc_48.png")


def build_curriculum_redirects(curriculum_dist_dir: pathlib.Path, language):
    fcc_lang = FCC_LANG_MAP[language]
    index_json_path = curriculum_dist_dir.joinpath("curriculum", fcc_lang, "index.json")
    with open(index_json_path) as course_index_str:
        superblock_dict = json.load(course_index_str)[fcc_lang]

    redirects = []
    for superblock in superblock_dict:
        course_list = superblock_dict[superblock]
        for course in course_list:
            meta_json_path = pathlib.Path(
                curriculum_dist_dir,
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
    zimui_dist_dir: pathlib.Path,
    out_dir: pathlib.Path,
    language: str,
    name: str,
    title: str,
    description: str,
    long_description: str | None,
    creator: str,
    publisher: str,
    curriculum_dist_dir: pathlib.Path,
    zim_file: str | None,
    *,
    force: bool,
):
    Global.logger.info("Scraper: build phase starting")

    period = datetime.today().strftime("%Y-%m")  # noqa: DTZ002
    if zim_file:
        zim_path = pathlib.Path(zim_file.format(period=period))
        # make sure we were given a filename and not a path
        if pathlib.Path(zim_path.name) != zim_path:
            raise ValueError(f"zim_name is not a filename: {zim_file}")
    else:
        zim_path = pathlib.Path(f"{name}_{period}.zim")

    # build full path
    zim_path = out_dir.joinpath(zim_path)

    if zim_path.exists():
        if not force:
            raise ValueError(f"ZIM file {zim_path} already exist.")
        Global.logger.info(f"Removing existing ZIM file {zim_path}")
        zim_path.unlink()
    else:
        Global.logger.info(f"ZIM path: {zim_path}")

    with Creator(zim_path, "index.html").config_metadata(
        Name=name,
        Title=title,
        Publisher=publisher,
        Date=datetime.now(),  # noqa: DTZ005
        Creator=creator,
        Description=description,
        LongDescription=long_description,
        Language=language,
        Tags=";".join(["FCC", "freeCodeCamp"]),
        Scraper=f"fcc2zim v{VERSION}",
        Illustration_48x48_at_1=logo_path.read_bytes(),
    ) as creator:
        # Add zimui files
        for file in zimui_dist_dir.rglob("*"):
            if file.is_dir():
                continue
            if file.suffix == ".map":
                Global.logger.debug(f"IGNORING: {file}")
                continue
            path = str(pathlib.Path(file).relative_to(zimui_dist_dir))
            Global.logger.debug(f"Adding {path} to ZIM")
            creator.add_item_for(path, fpath=file)

        for file in curriculum_dist_dir.rglob("*"):
            if file.is_dir():
                continue
            if file.suffix == ".map":
                Global.logger.debug(f"IGNORING: {file}")
                continue
            path = str(
                pathlib.Path("fcc").joinpath(
                    pathlib.Path(file).relative_to(curriculum_dist_dir)
                )
            )
            Global.logger.debug(f"Adding {path} to ZIM")
            creator.add_item_for(path, fpath=file)

        for redir_slug, redir_title in build_curriculum_redirects(
            curriculum_dist_dir, language
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
