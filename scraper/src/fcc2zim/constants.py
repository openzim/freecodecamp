import pathlib

from fcc2zim.__about__ import __version__

NAME = "fcc2zim"
VERSION = __version__
ROOT_DIR = pathlib.Path(__file__).parent

# key is the language passed at CLI
# value is the name of folders used in FCC source code
FCC_LANG_MAP = {
    "zh-hans": "chinese",
    "zh-hant": "chinese-traditional",
    "eng": "english",
    "spa": "espanol",
    "deu": "german",
    "ita": "italian",
    "jpn": "japanese",
    "por": "portuguese",
    "ukr": "ukrainian",
    "swa": "swahili",
}

ZIM_LANG_MAP = {
    "zh-hans": "zho",
    "zh-hant": "zho",
    "eng": "eng",
    "spa": "spa",
    "deu": "deu",
    "ita": "ita",
    "jpn": "jpn",
    "por": "por",
    "ukr": "ukr",
    "swa": "swa",
}
