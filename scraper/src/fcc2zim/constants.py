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
    "ara": "arabic",
    "kor": "korean",
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
    "ara": "ara",
    "kor": "kor",
}

# languages (keyed the same way as FCC_LANG_MAP/ZIM_LANG_MAP, i.e. as passed at CLI)
# which are written right-to-left and must be rendered accordingly in the ZIM UI
RTL_LANGUAGES = {"ara"}
