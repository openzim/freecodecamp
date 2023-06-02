import os
import pathlib
import shutil
import zipfile

import requests


def fetch_command(arguments):
    force = arguments.force or False
    tmpdir = arguments.tmpdir or "./tmp"
    url = "https://github.com/freeCodeCamp/freeCodeCamp/archive/refs/heads/main.zip"
    zip_path = f"{tmpdir}/main.zip"
    curriculum_path = f"{tmpdir}/curriculum"

    pathlib.Path(curriculum_path).mkdir(parents=True, exist_ok=True)

    # Don't redownload the file if we already have it (it's a large file)
    if force or not os.path.exists(zip_path):
        r = requests.get(url, allow_redirects=True)
        with open(zip_path, "wb") as f:
            f.write(r.content)

    shutil.rmtree(curriculum_path)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        file_count = 0
        for zip_info in zip_ref.infolist():
            if zip_info.filename.find("freeCodeCamp-main/curriculum/") >= 0:
                zip_ref.extract(zip_info, curriculum_path)
                file_count = file_count + 1
            elif zip_info.filename.find("freeCodeCamp-main/client/i18n/locales") >= 0:
                zip_ref.extract(zip_info, curriculum_path)
                file_count = file_count + 1
        print(f"Extracted {file_count} files")
