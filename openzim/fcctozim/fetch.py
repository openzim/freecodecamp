import os
import pathlib
import shutil
import zipfile

import requests


def fetch_command(arguments):
    filter = arguments.filter
    force = arguments.force or False
    tmp_dir = arguments.tmp_dir or "./tmp"
    url = "https://github.com/freeCodeCamp/freeCodeCamp/archive/refs/heads/main.zip"
    zip_path = f"{tmp_dir}/main.zip"
    curriculum_path = f"{tmp_dir}/curriculum"

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
                # TODO: We'll eventually need a better way to filter curriculum
                if filter:
                    if (
                        zip_info.filename.find(filter) >= 0
                        or zip_info.filename.find("_meta") >= 0
                    ):
                        zip_ref.extract(zip_info, curriculum_path)
                        file_count = file_count + 1
                else:
                    zip_ref.extract(zip_info, curriculum_path)
                    file_count = file_count + 1
            elif zip_info.filename.find("freeCodeCamp-main/client/i18n/locales") >= 0:
                zip_ref.extract(zip_info, curriculum_path)
                file_count = file_count + 1
        print(f"Extracted {file_count} files")
