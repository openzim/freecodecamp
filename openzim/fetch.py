#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

"""fetch.py

Usage:
  fetch.py
  fetch.py --filter=<filter_str>
  fetch.py (-h | --help)

Options:
  -h --help     Show this screen.
  --force       Force redownload curriculum zip
  --filter=<filter_str>  Filter zip file for matching course. eg. '02-javascript'
"""

import os
import pathlib
import shutil
import zipfile

from path import Path as path
from docopt import docopt
import requests

def main(arguments):
    FILTER = arguments.get("--filter", "")
    FORCE = arguments.get("--force")
    url = "https://github.com/freeCodeCamp/freeCodeCamp/archive/refs/heads/main.zip"
    tmp_dir = './tmp'
    zip_path = f'{tmp_dir}/main.zip'
    curriculum_path = f'{tmp_dir}/curriculum'

    pathlib.Path(curriculum_path).mkdir(parents=True, exist_ok=True)

    # Don't redownload the file if we already have it (it's a large file)
    if FORCE or not os.path.exists(zip_path):
        r = requests.get(url, allow_redirects=True)
        with open(zip_path, 'wb') as f:
            f.write(r.content)

    shutil.rmtree(curriculum_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_count = 0
        for zip_info in zip_ref.infolist():
            if not zip_info.filename.find("freeCodeCamp-main/curriculum/") == 0:
                continue
            # TODO: We'll eventually need a better way to filter curriculum
            if FILTER:
                if zip_info.filename.find(FILTER) >= 0 or zip_info.filename.find("_meta") >= 0:
                    zip_ref.extract(zip_info, curriculum_path)
                    file_count = file_count + 1
            else:
                zip_ref.extract(zip_info, curriculum_path)
                file_count = file_count + 1
        print(f'Extracted {file_count} files')

if __name__ == "__main__":
    main(docopt(__doc__))
