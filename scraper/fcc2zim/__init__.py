import threading

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
