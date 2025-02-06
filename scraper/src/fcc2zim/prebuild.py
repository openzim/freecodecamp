import json
import shutil
from pathlib import Path

from fcc2zim.challenge import Challenge
from fcc2zim.context import Context

logger = Context.logger


def get_challenges_for_lang(tmp_path: Path, language: str):
    return Path(tmp_path, language).rglob("*.md")


def update_index(
    path: Path, superblock: str, slug: str, challenges: list[dict[str, str]]
):
    index_path = path.joinpath("index.json")
    if not index_path.exists():
        index_path.write_bytes(json.dumps({}).encode("utf-8"))

    index = json.loads(index_path.read_text())
    if superblock not in index:
        index[superblock] = {}
    if slug not in index[superblock]:
        index[superblock][slug] = challenges

    with open(index_path, "w") as outfile:
        json.dump(index, outfile, indent=4)


"""
Simply copies over the locales to the client locales path
"""


def write_locales_to_path(source: Path, curriculumdir: Path):
    shutil.copytree(source, curriculumdir / "locales")


def write_course_to_path(
    challenge_list: list[Challenge],
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
    challenges: list[dict[str, str]] = []
    # meta: dict[str, list[dict[str, str]]] = {"challenges": []}

    for challenge in challenge_list:
        challenge_dest_path = curriculumdir.joinpath(
            challenge.course_superblock, challenge.course_slug
        )
        challenge_dest_path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(challenge.path, challenge_dest_path.joinpath(challenge.path.name))
        challenges.append({"title": challenge.title(), "slug": challenge.path.stem})

    # Create an index with a list of the courses
    update_index(curriculumdir, superblock, course_slug, challenges)


def prebuild_command(
    course_list: list[str],
    fcc_lang: str,
    curriculum_raw: Path,
    curriculum_dist: Path,
):
    """Transform raw data in curriculum_raw directory into pre-built data in
    curriculum_dist directory

    This gives following files:
    - <curriculum_dist>/index.json
        => { 'superblock': {'course_slug': [ {challenge_slug, challenge_title} ] } }
    - <curriculum_dist>/<superblock>/<course_slug>/{slug}.md
    """
    logger.info("Scraper: prebuild phase starting")

    curriculum_dist.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(curriculum_dist)

    challenges = curriculum_raw.joinpath("extracted", "curriculum", "challenges")
    locales = curriculum_raw.joinpath(
        "extracted", "client", "i18n", "locales", fcc_lang
    )

    # eg. ['basic-javascript', 'debugging']
    for course in course_list:
        logger.debug(f"Prebuilding {course}")
        meta = json.loads(challenges.joinpath("_meta", course, "meta.json").read_text())
        # Get the order that the challenges should be completed in for <course>
        ids: list[str] = [
            item[0] if isinstance(item, list) else item["id"]
            for item in meta["challengeOrder"]
        ]
        superblock = meta["superBlock"]

        challenge_list: list[Challenge] = []
        for file in get_challenges_for_lang(challenges, fcc_lang):
            challenge = Challenge(file)
            if challenge.course_superblock != superblock:
                continue
            # ID is a UUID the Challenge, the only add it to the challenge list if it's
            # a part of the course.
            if challenge.identifier() in ids:
                challenge_list.append(challenge)

        write_course_to_path(
            sorted(challenge_list, key=lambda x: ids.index(x.identifier())),
            superblock,
            course,
            curriculum_dist.joinpath("curriculum"),
        )

    # Copy all the locales for this language
    write_locales_to_path(locales, curriculum_dist)
    logger.info(f"Prebuilt curriculum into {curriculum_dist}")
    logger.info("Scraper: prebuild phase finished")
