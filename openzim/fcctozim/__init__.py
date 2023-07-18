#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import logging
import threading

logger = logging.getLogger(__name__)

VERSION = "1.0.0"

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

lock = threading.Lock()

creator = None
