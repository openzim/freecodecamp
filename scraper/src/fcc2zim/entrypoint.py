import argparse
import datetime
from pathlib import Path

from zimscraperlib.constants import (
    MAXIMUM_DESCRIPTION_METADATA_LENGTH as MAX_DESC_LENGTH,
)
from zimscraperlib.constants import (
    MAXIMUM_LONG_DESCRIPTION_METADATA_LENGTH as MAX_LONG_DESC_LENGTH,
)
from zimscraperlib.constants import RECOMMENDED_MAX_TITLE_LENGTH

from fcc2zim.constants import FCC_LANG_MAP, NAME, VERSION
from fcc2zim.context import Context


def prepare_context(raw_args: list[str]) -> None:
    """Initialize scraper context from command line arguments"""

    parser = argparse.ArgumentParser(
        prog=NAME,
        description="Scraper to create ZIM files from freeCodeCamp courses",
    )

    parser.add_argument(
        "--course",
        help="Course or course list (separated by commas)",
        type=lambda x: [course.strip() for course in x.split(",")],
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
        help=f"Title of ZIM file (less than {RECOMMENDED_MAX_TITLE_LENGTH} graphemes)",
        required=True,
    )

    parser.add_argument(
        "--description",
        type=str,
        help=f"Description of ZIM file (less than {MAX_DESC_LENGTH} graphemes)",
        required=True,
    )

    parser.add_argument(
        "--long-description",
        type=str,
        help=f"Long description of ZIM file (less than {MAX_LONG_DESC_LENGTH} "
        "graphemes)",
    )

    parser.add_argument(
        "--creator",
        type=str,
        help=f"Name of freeCodeCamp courses creator. Default: {Context.creator!s}",
    )

    parser.add_argument(
        "--publisher",
        type=str,
        help=f"Publisher of the zim file. Default: {Context.publisher!s}",
    )

    parser.add_argument(
        "--force",
        help="Force a full reprocessing, not benefiting from any cached file",
        action="store_true",
    )

    parser.add_argument(
        "--debug",
        help="Enable verbose output",
        action="store_true",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory where zim file will be built",
        dest="output_folder",
    )

    parser.add_argument(
        "--build",
        type=Path,
        help="The build directory to hold temporary files during scraper operation",
        dest="build_folder",
    )

    parser.add_argument(
        "--zimui-dist",
        type=Path,
        help=(
            "Dev option to customize directory containing Vite build output from the "
            "ZIM UI Vue.JS application"
        ),
    )

    parser.add_argument(
        "--zim-file",
        type=str,
        help="ZIM file name (based on --name if not provided), could contain {period}"
        " placeholder which will be replaced by <year>_<month>",
    )

    parser.add_argument(
        "--zip-path",
        help="Path to main zip file containing FCC courses",
        type=str,
        dest="main_zip_path",
    )

    parser.add_argument(
        "--i18n-zip-path",
        help="Path to i18n zip file containing translations of FCC courses",
        type=str,
    )

    parser.add_argument(
        "--version",
        help="Display scraper version and exit",
        action="version",
        version=f"fcc2zim {VERSION}",
    )

    parser.add_argument(
        "--overwrite",
        help="Do not fail if ZIM already exists, overwrite it",
        action="store_true",
        dest="overwrite_existing_zim",
    )

    parser.add_argument(
        "--illustration",
        help="Path or URL to ZIM illustration. Bitmap and SVG formats are supported.",
    )

    args = parser.parse_args(raw_args)

    # Ignore unset values so they do not override the default specified in Context
    args_dict = {key: value for key, value in args._get_kwargs() if value}

    args_dict["start_date"] = datetime.date.today()

    Context.setup(**args_dict)
