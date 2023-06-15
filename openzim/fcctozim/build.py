from datetime import datetime
import json
import pathlib
from collections import OrderedDict

from fcctozim import FCC_LANG_MAP, VERSION, logger
from zimscraperlib.zim import Creator

logo_path = pathlib.Path(__file__).parent.parent.joinpath("fcc_48.png")


def build_curriculum_redirects(clientdir, language):
    fcc_lang = FCC_LANG_MAP[language]
    index_json_path = pathlib.Path(clientdir, "fcc/index.json")
    with open(index_json_path) as course_index_str:
        course_list = json.load(course_index_str)[fcc_lang]

    redirects = []
    for course in course_list:
        meta_json_path = pathlib.Path(
            clientdir, "fcc/curriculum/", fcc_lang, course, "_meta.json"
        )
        with open(meta_json_path) as meta_json_str:
            challenges = json.load(meta_json_str)["challenges"]
        for challenge in challenges:
            title = challenge["title"]
            redirects.append((f'{fcc_lang}/{course}/{challenge["slug"]}', title))

    return OrderedDict(redirects).items()


def build(arguments):
    clientdir = arguments.clientdir
    outpath = arguments.outzim
    language = arguments.language
    name = arguments.name
    title = arguments.title
    description = arguments.description
    creator = arguments.creator

    logger.info(
        f"Building {clientdir} for {language} => {outpath} - Version: {VERSION}"
    )

    source_dir = pathlib.Path(clientdir)
    root_path = source_dir / "index.html"
    fileList = []

    # Walk the tree and get a list of files we care about
    for file in pathlib.Path(source_dir).glob("**/*"):
        if file.is_dir():
            continue
        if file.suffix == ".map":
            continue
        fileList.append(file)

    main_path = root_path.relative_to(source_dir)

    # Make sure the outpath directory exists

    pathlib.Path(outpath).mkdir(parents=True, exist_ok=True)

    with Creator(outpath, main_path.as_posix()).config_metadata(
        Name=name,
        Title=title,
        Publisher="Kiwix",
        Date=datetime.now(),
        Creator=creator,
        Description=description,
        Language=language,
        Tags=";".join(["FCC", "freeCodeCamp"]),
        Scraper=f"fcc2zim V{VERSION}",
        Illustration_48x48_at_1=logo_path.read_bytes(),
    ) as creator:
        for file in fileList:
            print(file)
            path = pathlib.Path(file).relative_to(source_dir).as_posix()
            creator.add_item_for(path, fpath=file)

        for course_page in build_curriculum_redirects(clientdir, language):
            print(course_page[0], course_page[1])
            redirect_path = f"redirect/{course_page[0]}"
            redirect_url = (
                len(redirect_path.split("/")) - 1
            ) * "../" + f"index.html#{course_page[0]}"
            content = f'<html><head><title>{title}</title><meta http-equiv="refresh" content="0;URL=\'{redirect_url}\'" /></head><body></body></html>'  # noqa: E501
            creator.add_item_for(
                redirect_path,
                content=bytes(content, 'utf-8'),
                title=course_page[1],
                mimetype="text/html",
                is_front=True,
            )
            # Example index.html#/english/regular-expressions/extract-matches
