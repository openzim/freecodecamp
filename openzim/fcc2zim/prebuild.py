#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
import json
import pathlib
import shutil
from typing import List

from fcc2zim import FCC_LANG_MAP
from fcc2zim.challenge import Challenge


def get_challenges_for_lang(tmp_path, language="english"):
    return pathlib.Path(tmp_path, language).rglob("*.md")


def update_index(path: pathlib.Path, superblock: str, slug: str, language="english"):
    index_path = path.joinpath("index.json")
    if not index_path.exists():
        index_path.write_bytes(json.dumps({}).encode("utf-8"))

    index = json.loads(index_path.read_text())
    if language not in index:
        index[language] = {}
    if superblock not in index[language]:
        index[language][superblock] = []
    if slug not in index[language][superblock]:
        index[language][superblock].append(slug)

    with open(index_path, "w") as outfile:
        json.dump(index, outfile, indent=4)


"""
Simply copies over the locales to the client locales path
"""


def write_locales_to_path(
    source_dir: pathlib.Path, curriculumdir: pathlib.Path, language="english"
):
    shutil.copytree(source_dir, curriculumdir / "locales" / language)


def write_course_to_path(
    challenge_list: List[Challenge],
    superblock: str,
    course_slug: str,
    curriculumdir: pathlib.Path,
):
    """Writes the course to the chosen path.

    Each individual Markdown challenge is written along
    with the meta data for the course.

    Finally, we udpate the root index.json file with the course, which allows
    us to render a page listing all available courses
    """
    curriculumdir.mkdir(parents=True, exist_ok=True)
    meta = {"challenges": []}

    for challenge in challenge_list:
        challenge_dest_path = curriculumdir.joinpath(
            challenge.course_superblock, challenge.course_slug
        )
        challenge_dest_path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(challenge.path, challenge_dest_path.joinpath(challenge.path.name))
        meta["challenges"].append(
            {"title": challenge.title(), "slug": challenge.path.stem}
        )

    meta_path = curriculumdir.joinpath(superblock, course_slug, "_meta.json")
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    with open(meta_path, "w") as outfile:
        json.dump(meta, outfile, indent=4)

    # Create an index with a list of the courses
    update_index(curriculumdir, superblock, course_slug, challenge_list[0].language)


def prebuild_command(arguments):
    """Writes out a structure of challenges to output dir:

    /output_dir/index.json => { 'english': {'superblock': ['basic-javascript'] } }
    /output_dir/english/<superblock>/<course_slug>/_meta.json
        => { challenges: [{slug, title}] }
    /output_dir/english/<superblock>/<course_slug>/{slug}.md
    """
    course_list_str = str(arguments.course)
    curriculumdir = pathlib.Path(arguments.curriculumdir)
    lang = FCC_LANG_MAP[arguments.language]
    tmpdir = arguments.tmpdir or "./tmp"
    curriculum_dir = pathlib.Path(
        tmpdir, "curriculum", "freeCodeCamp-main", "curriculum", "challenges"
    )
    locales_dir = pathlib.Path(
        tmpdir, "curriculum", "freeCodeCamp-main", "client", "i18n", "locales", lang
    )

    # eg. ['basic-javascript', 'debugging']
    for course in course_list_str.split(","):
        print(f"Prebuilding {course}")
        meta = json.loads(
            curriculum_dir.joinpath("_meta", course, "meta.json").read_text()
        )
        # Get the order that the challenges should be completed in for <course>
        ids = [
            item[0] if isinstance(item, list) else item["id"]
            for item in meta["challengeOrder"]
        ]
        superblock = meta["superBlock"]

        challenge_list: List[Challenge] = []
        for file in get_challenges_for_lang(curriculum_dir, lang):
            challenge = Challenge(file)
            if challenge.course_superblock != superblock:
                continue
            # ID is a UUID the Challenge, the only add it to the challenge list if it's
            # a part of the course.
            if challenge.id() in ids:
                challenge_list.append(challenge)

        write_course_to_path(
            sorted(challenge_list, key=lambda x: ids.index(x.id())),
            superblock,
            course,
            curriculumdir.joinpath("curriculum", lang),
        )
        print(f"Prebuilt {course}")

    # Copy all the locales for this language
    write_locales_to_path(locales_dir, curriculumdir, lang)
    print(f"Prebuilt curriculum into {curriculumdir}")
