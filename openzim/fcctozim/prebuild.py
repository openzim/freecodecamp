import json
import pathlib
import shutil
from typing import List

import yaml
from fcctozim import FCC_LANG_MAP


# Each markdown challenge contains 'frontmatter' which is a header
# consisting of yaml formatted data enclosed inside of '---\n' lines
# '---' lines in YAML denote multiple documents, so this can be read
# directly with python's yaml library pulling in the first document
# with 'next' and immediately returning
def read_yaml_frontmatter(filename: pathlib.Path):
    with open(filename) as f:
        front_matter = next(yaml.load_all(f, Loader=yaml.FullLoader))
        return front_matter


def get_challenges_for_lang(tmp_path, language="english"):
    return pathlib.Path(tmp_path, language).rglob("*.md")


def update_index(path: str, slug: str, language="english"):
    index_path = pathlib.Path(path, "index.json")
    if not index_path.exists():
        index_path.write_bytes(bytes(json.dumps({}), "utf-8"))

    index = json.loads(index_path.read_text())
    if not index.get(language):
        index[language] = []
    if slug not in index[language]:
        index[language].append(slug)

    with open(index_path, "w") as outfile:
        json.dump(index, outfile, indent=4)


def write_locales_to_path(source_dir: pathlib.Path, outdir: str, language="english"):
    locales_dir = pathlib.Path(outdir, "locales", language)
    shutil.copytree(source_dir, locales_dir)


def write_course_to_path(
    course_list, course_slug: str, outdir: str, language="english"
):
    course_dir = pathlib.Path(outdir, "curriculum", language, course_slug)
    pathlib.Path(course_dir).mkdir(parents=True, exist_ok=True)
    meta = {"challenges": []}

    for course_item in course_list:
        filename = pathlib.Path(course_item[1]).name
        shutil.copy2(course_item[1], course_dir.joinpath(filename))
        meta["challenges"].append(
            {"title": course_item[2], "slug": pathlib.Path(filename).suffix}
        )

    with open(course_dir.joinpath("meta.json"), "w") as outfile:
        json.dump(meta, outfile, indent=4)
    update_index(outdir, course_slug, language)


"""
Should write out the following structure of challenges to output dir:

/output_dir/index.json => { 'english': ['basic-javascript'] }
/output_dir/english/basic-javascript/_meta.json => { challenges: [{slug, title}] }
/output_dir/english/basic-javascript/<slug>.md

"""


def prebuild_command(arguments):
    course_list_str = str(arguments.course)
    outdir = str(arguments.outdir)
    lang = FCC_LANG_MAP[arguments.language]
    tmpdir = arguments.tmpdir or "./tmp"
    curriculum_dir = pathlib.Path(
        tmpdir, "curriculum", "freeCodeCamp-main", "curriculum", "challenges"
    )
    locales_dir = pathlib.Path(
        tmpdir, "curriculum", "freeCodeCamp-main", "client", "i18n", "locales", lang
    )

    for course in course_list_str.split(","):
        meta = json.loads(
            curriculum_dir.joinpath("_meta", course, "meta.json").read_text()
        )

        ids = [item[0] for item in meta["challengeOrder"]]

        course_list: List[List[str]] = []
        # List[[id, path, title]]
        for file in get_challenges_for_lang(curriculum_dir, lang):
            info = read_yaml_frontmatter(file)
            id = str(info["id"])
            try:
                if ids.index(id) > -1:
                    course_list.append([id, str(file.as_posix()), str(info["title"])])
            except ValueError:
                continue
        write_course_to_path(
            sorted(course_list, key=lambda x: ids.index(x[0])),
            course,
            outdir,
            lang,
        )

    # Copy all the locales for this language
    write_locales_to_path(locales_dir, outdir, lang)
    print(f"Prebuilt curriculum into {outdir}")
