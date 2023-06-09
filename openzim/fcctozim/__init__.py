#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import logging
import threading
from pathlib import Path as path

logger = logging.getLogger(__name__)

TMP_FOLDER = "tmp"
TMP_FOLDER_PATH = path(TMP_FOLDER)

VERSION = "1.0.0"


FCCLangMap = {
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

lock = threading.Lock()

creator = None
