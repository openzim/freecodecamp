import json
import pathlib
from collections import OrderedDict
from datetime import datetime

from fcctozim import FCC_LANG_MAP, VERSION, logger
from zimscraperlib.zim import Creator

logo_path = pathlib.Path(__file__).parent.parent.joinpath("fcc_48.png")


def build_curriculum_redirects(clientdir, language):
    fcc_lang = FCC_LANG_MAP[language]
    index_json_path = pathlib.Path(
        clientdir, "fcc", "curriculum", fcc_lang, "index.json"
    )
    with open(index_json_path) as course_index_str:
        superblock_dict = json.load(course_index_str)[fcc_lang]

    redirects = []
    for superblock in superblock_dict:
        course_list = superblock_dict[superblock]
        for course in course_list:
            meta_json_path = pathlib.Path(
                clientdir, "fcc/curriculum/", fcc_lang, superblock, course, "_meta.json"
            )
            challenges = json.loads(meta_json_path.read_text())["challenges"]
            for challenge in challenges:
                title = challenge["title"]
                redirects.append(
                    (f'{fcc_lang}/{superblock}/{course}/{challenge["slug"]}', title)
                )

    return OrderedDict(redirects).items()


def build(arguments):
    clientdir = pathlib.Path(arguments.clientdir)
    outpath = pathlib.Path(arguments.outpath)
    language = arguments.language
    name = arguments.name
    title = arguments.title
    description = arguments.description
    long_description = arguments.long_description
    creator = arguments.creator or "freeCodeCamp"
    publisher = arguments.publisher or "openZIM"

    logger.info(
        f"Building {clientdir} for {language} => {outpath} - Version: {VERSION}"
    )

    fileList = []

    # Walk the tree and get a list of files we care about
    for file in clientdir.rglob("*"):
        if file.is_dir():
            continue
        if file.suffix == ".map":
            continue
        fileList.append(file)

    main_path = clientdir.joinpath("index.html").relative_to(clientdir)

    # Make sure the output directory exists

    outpath.parent.mkdir(parents=True, exist_ok=True)

    with Creator(outpath, main_path.as_posix()).config_metadata(
        Name=name,
        Title=title,
        Publisher=publisher,
        Date=datetime.now(),
        Creator=creator,
        Description=description,
        LongDescription=long_description,
        Language=language,
        Tags=";".join(["FCC", "freeCodeCamp"]),
        Scraper=f"fcctozim V{VERSION}",
        Illustration_48x48_at_1=logo_path.read_bytes(),
    ) as creator:
        for file in fileList:
            print(file)
            path = pathlib.Path(file).relative_to(clientdir).as_posix()
            creator.add_item_for(path, fpath=file)

        for redir_slug, redir_title in build_curriculum_redirects(clientdir, language):
            print("Redirect", redir_slug)
            redirect_path = f"{redir_slug}"
            redirect_url = redir_slug.count("/") * "../" + f"index.html#{redir_slug}"
            content = (
                f"<html><head><title>{redir_title}</title>"
                f'<meta http-equiv="refresh" content="0;URL=\'{redirect_url}\'" />'
                f"</head><body></body></html>"
            )
            creator.add_item_for(
                redirect_path,
                content=bytes(content, "utf-8"),
                title=redir_title,
                mimetype="text/html",
                is_front=True,
            )
            # Example index.html#/english/regular-expressions/extract-matches
