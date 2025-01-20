import pathlib

from fcc2zim.__about__ import __version__

NAME = "fcc2zim"
VERSION = __version__
ROOT_DIR = pathlib.Path(__file__).parent

# key is the language passed at CLI (and used as ZIM Language metadata)
# value is the name of folders used in FCC source code
FCC_LANG_MAP = {
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
    "swa": "swahili",
}
