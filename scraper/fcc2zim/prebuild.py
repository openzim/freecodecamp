import json
import shutil
from pathlib import Path
from typing import List

from fcc2zim.challenge import Challenge
from fcc2zim.constants import Global


def get_challenges_for_lang(tmp_path, language="english"):
    return Path(tmp_path, language).rglob("*.md")


def update_index(path: Path, superblock: str, slug: str, language="english"):
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


def write_locales_to_path(source_dir: Path, curriculumdir: Path, language="english"):
    shutil.copytree(source_dir, curriculumdir / "locales" / language)


def write_course_to_path(
    challenge_list: List[Challenge],
    superblock: str,
    course_slug: str,
    curriculumdir: Path,
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


def prebuild_command(
    course_csv: str,
    language_full: str,
    curriculum_raw_dir: Path,
    curriculum_dist_dir: Path,
):
    """Transform raw data in curriculum_raw_dir into pre-built data in
    curriculum_dist_dir

    E.g. if lang in english:
    - curriculum_dist_dir/index.json
        => { 'english': {'superblock': ['basic-javascript'] } }
    - curriculum_dist_dir/english/<superblock>/<course_slug>/_meta.json
        => { challenges: [{slug, title}] }
    - curriculum_dist_dir/english/<superblock>/<course_slug>/{slug}.md
    """
    Global.logger.info("Scraper: prebuild phase starting")

    curriculum_dist_dir.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(curriculum_dist_dir)

    challenges_dir = curriculum_raw_dir.joinpath(
        "freeCodeCamp-main", "curriculum", "challenges"
    )
    locales_dir = curriculum_raw_dir.joinpath(
        "freeCodeCamp-main", "client", "i18n", "locales", language_full
    )

    # eg. ['basic-javascript', 'debugging']
    for course in course_csv.split(","):
        Global.logger.debug(f"Prebuilding {course}")
        meta = json.loads(
            challenges_dir.joinpath("_meta", course, "meta.json").read_text()
        )
        # Get the order that the challenges should be completed in for <course>
        ids = [
            item[0] if isinstance(item, list) else item["id"]
            for item in meta["challengeOrder"]
        ]
        superblock = meta["superBlock"]

        challenge_list: List[Challenge] = []
        for file in get_challenges_for_lang(challenges_dir, language_full):
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
            curriculum_dist_dir.joinpath("curriculum", language_full),
        )

    # Copy all the locales for this language
    write_locales_to_path(locales_dir, curriculum_dist_dir, language_full)
    Global.logger.info(f"Prebuilt curriculum into {curriculum_dist_dir}")
    Global.logger.info("Scraper: prebuild phase finished")
