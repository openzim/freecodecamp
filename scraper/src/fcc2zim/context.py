import dataclasses
import datetime
import logging
import os
from pathlib import Path
from typing import Any

from zimscraperlib.logging import DEFAULT_FORMAT_WITH_THREADS, getLogger

from fcc2zim.constants import (
    NAME,
)


@dataclasses.dataclass(kw_only=True)
class Context:
    """Class holding every contextual / configuration bits which can be moved

    Used to easily pass information around in the scraper. One singleton instance is
    always available.
    """

    # singleton instance
    _instance: Context | None = None

    # list of courses to include
    course: list[str]

    # ZIM language, also used to fetch proper FCC content
    language: str

    # ZIM name (also used for filename if zim_file is not set) and filename
    name: str
    zim_file: str | None = None

    # Other ZIM metadata
    title: str
    description: str
    long_description: str | None = None
    creator: str = "freeCodeCamp"
    publisher: str = "openZIM"

    # force flag
    force: bool = False

    # debug flag
    debug: bool = False

    # do flags (to control which steps will be done)
    do_fetch: bool = os.getenv("DO_FETCH", "False").lower() == "true"
    do_prebuild: bool = os.getenv("DO_PREBUILD", "False").lower() == "true"
    do_build: bool = os.getenv("DO_BUILD", "False").lower() == "true"

    # folder where the ZIM will be written
    output_folder: Path = Path(os.getenv("FCC_OUTPUT", "../output"))

    # folder where temporary files will be stored
    build_folder: Path = Path(os.getenv("FCC_BUILD", "../build"))

    # folder where Vue.JS UI has been built
    zimui_dist: Path = Path(os.getenv("FCC_ZIMUI_DIST", "../zimui/dist"))

    # ZIP of FCC content
    main_zip_path: Path | None = None
    i18n_zip_path: Path | None = None

    # Do not fail if ZIM already exists, overwrite it
    overwrite_existing_zim: bool = False

    # Date when the crawl started
    start_date: datetime.date

    # Path or URL to use as ZIM illustration
    illustration: str | None = None

    # logger to use everywhere (do not mind about mutability, we want to reuse same
    # logger everywhere)
    logger: logging.Logger = getLogger(  # noqa: RUF009
        NAME, level=logging.DEBUG, log_format=DEFAULT_FORMAT_WITH_THREADS
    )

    @classmethod
    def setup(cls, **kwargs: Any):
        new_instance = cls(**kwargs)
        if cls._instance:
            # replace values 'in-place' so that we do not change the Context object
            # which might be already imported in some modules
            for field in dataclasses.fields(new_instance):
                cls._instance.__setattr__(
                    field.name, new_instance.__getattribute__(field.name)
                )
        else:
            cls._instance = new_instance

    @classmethod
    def get(cls) -> Context:
        if not cls._instance:
            raise OSError("Uninitialized context")  # pragma: no cover
        return cls._instance
