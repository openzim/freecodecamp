import argparse
import functools
import os
from datetime import datetime

from zimscraperlib.constants import (
    MAXIMUM_DESCRIPTION_METADATA_LENGTH as MAX_DESC_LENGTH,
)
from zimscraperlib.constants import (
    MAXIMUM_LONG_DESCRIPTION_METADATA_LENGTH as MAX_LONG_DESC_LENGTH,
)

from fcc2zim.constants import FCC_LANG_MAP, VERSION, Global, set_debug
from fcc2zim.scraper import Scraper


def log_and_sys_exit(func):
    @functools.wraps(func)
    def wrapper():
        try:
            func()
        except SystemExit:  # SystemExit has been asked for at lower level, simply do it
            raise
        except Exception as exc:
            Global.logger.error(f"A fatal error occurred: {exc}")
            Global.logger.exception(exc)
            raise SystemExit(1) from exc

    return wrapper


@log_and_sys_exit
def main():
    parser = argparse.ArgumentParser(
        prog="fcc2zim",
        description="Scraper to create ZIM files from freeCodeCamp courses",
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
        choices=FCC_LANG_MAP.keys(),
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
        # TODO: once Zimscraperlib > 3.1.1 is released, use constant from library
        # instead of '30' magic number
        help="Title of zim file (less than 30 chars)",
        required=True,
    )
    parser.add_argument(
        "--description",
        type=str,
        help=f"Description of ZIM file (less than {MAX_DESC_LENGTH} chars)",
        required=True,
    )
    parser.add_argument(
        "--long-description",
        type=str,
        help=f"Long description of ZIM file (less than {MAX_LONG_DESC_LENGTH} chars)",
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
        "--output-dir",
        type=str,
        help="Output directory where zim file will be built",
        default="/output",
    )
    parser.add_argument(
        "--build-dir",
        type=str,
        help="The build directory to hold temporary files during scraper operation",
        default=os.getenv("TMPDIR"),
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

    scraper = Scraper(
        do_fetch=args.fetch,
        do_prebuild=args.prebuild,
        do_build=args.build,
        zimui_dist_dir=args.zimui_dist_dir,
        output_dir=args.output_dir,
        build_dir=args.build_dir,
        language=args.language,
        name=args.name,
        title=args.title,
        description=args.description,
        long_description=args.long_description,
        content_creator=args.creator,
        publisher=args.publisher,
        zim_file=args.zim_file,
        force=args.force,
        course_csv=args.course,
        zip_path=args.zip_path,
        start_time=datetime.now(),  # noqa: DTZ005
    )

    scraper.run()

    Global.logger.info("Scraper completed")
