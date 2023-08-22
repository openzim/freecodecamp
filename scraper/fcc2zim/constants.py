import logging

from zimscraperlib.logging import getLogger


class Global:
    debug = False
    logger: logging.Logger = getLogger("fcc2zim", level=logging.INFO)


def set_debug(debug: bool):
    Global.debug = debug
    Global.logger = getLogger(  # refresh logger to update log level
        "fcc2zim", level=logging.DEBUG if Global.debug else logging.INFO
    )
