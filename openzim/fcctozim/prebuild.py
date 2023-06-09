import json
import os
import pathlib
import shutil
from typing import List

import yaml
from fcctozim import FCCLangMap

default_tmp_path = "./tmp"


def readFrontmatter(filename: str):
    with open(filename) as f:
        front_matter = next(yaml.load_all(f, Loader=yaml.FullLoader))
        return front_matter


def get_challenges_for_lang(tmp_path, language="english"):
    return pathlib.Path(f"{tmp_path}/{language}").rglob("*.md")


def update_index(path: str, slug: str, language="english"):
    index_path = f"{path}/index.json"
    if not os.path.exists(index_path):
        with open(index_path, "w") as index_json:
            index_json.write(json.dumps({}))

    f = open(index_path, "r")
    index = json.load(f)
    if not index.get(language):
        index[language] = []
    if slug not in index[language]:
        index[language].append(slug)

    with open(index_path, "w") as outfile:
        json.dump(index, outfile, indent=4)


def write_locales_to_path(source_dir: str, outdir: str, language="english"):
    locales_dir = f"{outdir}/locales/{language}"
    print(source_dir, locales_dir)
    shutil.copytree(source_dir, locales_dir)


def write_course_to_path(
    course_list, course_slug: str, outdir: str, language="english"
):
    course_dir = f"{outdir}/curriculum/{language}/{course_slug}"
    pathlib.Path(course_dir).mkdir(parents=True, exist_ok=True)
    meta = {"challenges": []}

    for course_item in course_list:
        filename = os.path.basename(course_item[1])
        shutil.copy2(course_item[1], f"{course_dir}/{filename}")
        meta["challenges"].append(
            {"title": course_item[2], "slug": os.path.splitext(filename)[0]}
        )

    with open(f"{course_dir}/_meta.json", "w") as outfile:
        json.dump(meta, outfile, indent=4)
    update_index(outdir, course_slug, language)


"""
Should write out the following structure of challenges to output dir:

/output_dir/index.json => { 'english': ['basic-javascript'] }
/output_dir/english/basic-javascript/_meta.json => { challenges: [{slug, title}] }
/output_dir/english/basic-javascript/<slug>.md

"""


def prebuild_command(arguments):
    course_list = arguments.course
    outdir = arguments.outdir
    lang = FCCLangMap[arguments.language]
    tmpdir = arguments.tmpdir or default_tmp_path
    curriculum_dir = os.path.join(
        tmpdir, "curriculum/freeCodeCamp-main/curriculum/challenges"
    )
    locales_dir = os.path.join(
        tmpdir, f"curriculum/freeCodeCamp-main/client/i18n/locales/{lang}"
    )
    print(tmpdir, curriculum_dir)

    for COURSE in course_list.split(","):
        # Opening JSON file
        f = open(
            f"{curriculum_dir}/_meta/{COURSE}/meta.json",
        )

        # returns JSON object as
        # a dictionary
        meta = json.load(f)
        ids = list(map(lambda item: item[0], meta["challengeOrder"]))

        course_list: List[str, str, str] = []
        # List[id, path, title]
        for file in get_challenges_for_lang(curriculum_dir, lang):
            info = readFrontmatter(file)
            id = info["id"]
            title = info["title"]
            try:
                if ids.index(id) > -1:
                    course_list.append([id, str(file), title])
            except ValueError:
                continue
        write_course_to_path(
            sorted(course_list, key=lambda x: ids.index(x[0])), COURSE, outdir, lang
        )

    # Copy all the locales for this language
    write_locales_to_path(locales_dir, outdir, lang)
