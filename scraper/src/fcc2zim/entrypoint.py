import argparse
from pathlib import Path

from fcc2zim.build import build_command
from fcc2zim.constants import FCC_LANG_MAP, VERSION, Global, set_debug
from fcc2zim.fetch import fetch_command
from fcc2zim.prebuild import prebuild_command
from fcc2zim.zimscraperlib import compute_descriptions


def log_and_sys_exit(func):
    def wrapper():
        try:
            func()
        except Exception as exc:
            Global.logger.error(f"FAILED. An error occurred: {exc}")
            Global.logger.exception(exc)
            raise SystemExit(1) from exc

    return wrapper


@log_and_sys_exit
def main():
    parser = argparse.ArgumentParser(
        prog="fcc2zim",
        description="Scraper to create ZIM files from Freecodedcamp courses",
    )

    parser.add_argument(
        "--course",
        type=str,
        help="Course or course list (separated by commas)",
        required=True,
    )
    parser.add_argument(
        "--language",
        type=str,
        help="Curriculum language",
        required=True,
    )
    parser.add_argument(
        "--name",
        type=str,
        help="ZIM name. Used as identifier and filename (date will be appended)",
        required=True,
    )
    parser.add_argument(
        "--title",
        type=str,
        help="Title of zim file",
        required=True,
    )
    parser.add_argument(
        "--description", type=str, help="Description of ZIM file", required=True
    )
    parser.add_argument(
        "--long-description",
        type=str,
        help="Long description of ZIM file",
    )
    parser.add_argument(
        "--creator",
        type=str,
        help="Name of freeCodeCamp courses creator",
        default="freeCodeCamp",
    )
    parser.add_argument(
        "--publisher", type=str, help="Publisher of the zim file", default="OpenZIM"
    )
    parser.add_argument(
        "--fetch",
        help="Run fetch scraper phase",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--prebuild",
        help="Run pre-build scraper phase",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--build",
        help="Run build scraper phase",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--force",
        help="Force a full reprocessing, not benefiting from any cached file",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--debug",
        help="Enable verbose output",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        help="Output directory where zim file will be built",
        default="/output",
    )
    parser.add_argument(
        "--tmp-dir",
        type=str,
        help="The temporary directory to hold temporary files during scraper operation",
        default="/tmp",  # noqa: S108
    )
    parser.add_argument(
        "--zimui-dist-dir",
        type=str,
        help=(
            "Directory containing Vite build output from the Zim UI Vue.JS application"
        ),
        default="/src/zimui",
    )
    parser.add_argument(
        "--zim-file",
        type=str,
        help="ZIM file name (based on --name if not provided), could contain {period}"
        " placeholder which will be replaced by <year>_<month>",
    )
    parser.add_argument(
        "--zip-path",
        help="Path to zip file containing FCC courses",
        type=str,
    )
    parser.add_argument(
        "--version",
        help="Display scraper version and exit",
        action="version",
        version=f"fcc2zim {VERSION}",
    )

    args = parser.parse_args()

    Global.logger.info(f"Starting scraper {VERSION}")

    set_debug(debug=args.debug)

    do_fetch = args.fetch
    do_prebuid = args.prebuild
    do_build = args.build

    if not (do_fetch + do_prebuid + do_build):
        do_fetch = do_prebuid = do_build = True

    zimui_dist_dir = Path(args.zimui_dist_dir)
    if not zimui_dist_dir.exists():
        raise ValueError("zimui_dist_dir {zimui_dist_dir} does not exists")

    out_dir = Path(args.out_dir)
    tmp_dir = Path(args.tmp_dir)
    curriculum_raw_dir = tmp_dir.joinpath("curriculum-raw")
    curriculum_dist_dir = tmp_dir.joinpath("curriculum-dist")

    # Make sure the output directory exists
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    language = args.language
    if language not in FCC_LANG_MAP:
        raise ValueError(f"Unsupported language {language}")
    language_full = FCC_LANG_MAP[language]

    name = args.name
    title = args.title

    description = args.description
    long_description = args.long_description
    (description, long_description) = compute_descriptions(
        description, description, long_description
    )

    creator = args.creator
    publisher = args.publisher
    zim_file = args.zim_file
    force = args.force
    course_csv = args.course
    zip_path = args.zip_path
    if not zip_path:
        zip_path = tmp_dir.joinpath("main.zip")
    else:
        zip_path = Path(zip_path)
        if not zip_path:
            raise ValueError(f"Zip file not found in {zip_path}")

    if do_fetch:
        fetch_command(
            force=force, curriculum_raw_dir=curriculum_raw_dir, zip_path=zip_path
        )
    if do_prebuid:
        prebuild_command(
            language_full=language_full,
            course_csv=course_csv,
            curriculum_raw_dir=curriculum_raw_dir,
            curriculum_dist_dir=curriculum_dist_dir,
        )
    if do_build:
        build_command(
            language=language,
            name=name,
            title=title,
            description=description,
            long_description=long_description,
            creator=creator,
            publisher=publisher,
            out_dir=out_dir,
            zimui_dist_dir=zimui_dist_dir,
            curriculum_dist_dir=curriculum_dist_dir,
            zim_file=zim_file,
            force=force,
        )

    Global.logger.info("Scraper completed")
