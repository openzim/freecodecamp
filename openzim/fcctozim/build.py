import json
import os
from collections import OrderedDict

from fcctozim import VERSION, FCCLangMap, logger
from zimscraperlib.zim import Creator

logo_path = os.path.join(os.path.dirname(__file__), "..", "fcc_48.png")


def build_curriculum_redirects(clientdir, language):
    fcc_lang = FCCLangMap[language]
    index_json_path = os.path.join(clientdir, "fcc/index.json")
    with open(index_json_path) as course_index_str:
        course_list = json.load(course_index_str)[fcc_lang]

    redirects = []
    for course in course_list:
        meta_json_path = os.path.join(
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

    logger.info(
        f"Building {clientdir} for {language} => {outpath} - Version: {VERSION}"
    )

    source_dir = os.path.join(clientdir)
    rootPath = os.path.join(source_dir, "index.html")
    fileList = []

    # Walk the ree and get a list of files we care about
    for root, dirs, files in os.walk(source_dir):
        for name in files:
            file = os.path.join(root, name)
            if os.path.splitext(file)[1] == ".map":
                continue
            fileList.append(file)

    main_path = os.path.relpath(rootPath, source_dir)

    # Make sure the outpath directory exists
    outpathExists = os.path.exists(os.path.dirname(outpath))
    if not outpathExists:
        os.makedirs(os.path.dirname(outpath))

    tags = ";".join(["FCC", "freeCodeCamp"])

    with open(logo_path, "rb") as fh:
        png_data = fh.read()

    with Creator(outpath, main_path).config_dev_metadata(
        Name=name,
        Title=title,
        Description=description,
        Language=language,
        Tags=tags,
        Scraper=f"fcc2zim V{VERSION}",
        Illustration_48x48_at_1=png_data,
    ) as creator:
        for file in fileList:
            print(file)
            path = os.path.relpath(file, source_dir)
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
                content=content,
                title=course_page[1],
                mimetype="text/html",
                is_front=True,
            )
            # Example index.html#/english/regular-expressions/extract-matches
