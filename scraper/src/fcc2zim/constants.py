import logging

from zimscraperlib.logging import getLogger

from fcc2zim.__about__ import __version__

FCC_LANG_MAP = {
    "ara": "arabic",
    "cmn": "chinese",
    "lzh": "chinese-traditional",
    "eng": "english",
    "spa": "espanol",
    "deu": "german",
    "ita": "italian",
    "jpn": "japanese",
    "por": "portuguese",
    "ukr": "ukranian",
}

VERSION = __version__


class Global:
    debug = False
    logger: logging.Logger = getLogger("fcc2zim", level=logging.INFO)


def set_debug(*, debug: bool):
    Global.debug = debug
    Global.logger = getLogger(  # refresh logger to update log level
        "fcc2zim", level=logging.DEBUG if Global.debug else logging.INFO
    )
