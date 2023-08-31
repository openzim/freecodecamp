import argparse
import datetime
import functools
import os

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
        # once Zimscraperlib > 3.1.1 is released, use constant from library
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
        "--output",
        type=str,
        help="Output directory where zim file will be built",
        default=os.getenv("FCC_OUTPUT", "../output"),
    )
    parser.add_argument(
        "--build",
        type=str,
        help="The build directory to hold temporary files during scraper operation",
        default=os.getenv("FCC_BUILD", "../build"),
    )
    parser.add_argument(
        "--zimui-dist",
        type=str,
        help=(
            "Directory containing Vite build output from the Zim UI Vue.JS application"
        ),
        default=os.getenv("FCC_ZIMUI_DIST", "../zimui/dist"),
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

    Global.logger.info(f"Starting fcc2zim {VERSION}")

    set_debug(debug=args.debug)

    scraper = Scraper(
        do_fetch=os.getenv("DO_FETCH", "False").lower() == "true",
        do_prebuild=os.getenv("DO_PREBUILD", "False").lower() == "true",
        do_build=os.getenv("DO_BUILD", "False").lower() == "true",
        zimui_dist=args.zimui_dist,
        output=args.output,
        build=args.build,
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
        start_date=datetime.date.today(),
    )

    scraper.run()

    Global.logger.info("Scraper completed")
