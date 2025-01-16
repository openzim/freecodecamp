import logging

from zimscraperlib.logging import getLogger

from fcc2zim.__about__ import __version__

# key is the language passed at CLI (and used as ZIM Language metadata)
# value is the name of folders used in FCC source code
FCC_LANG_MAP = {
    "ara": "arabic",
    # removed until we settle on these two codes
    # "cmn": "chinese",
    # "lzh": "chinese-traditional",
    "eng": "english",
    "spa": "espanol",
    "deu": "german",
    "ita": "italian",
    "jpn": "japanese",
    "por": "portuguese",
    "ukr": "ukrainian",
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
