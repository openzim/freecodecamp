import pathlib
import shutil
import zipfile

import requests


def fetch_command(arguments):
    force = arguments.force or False
    tmpdir = pathlib.Path(arguments.tmpdir or "./tmp")
    url = "https://github.com/freeCodeCamp/freeCodeCamp/archive/refs/heads/main.zip"
    zip_path = pathlib.Path(tmpdir, "main.zip")
    curriculum_path = pathlib.Path(tmpdir, "curriculum")

    curriculum_path.mkdir(parents=True, exist_ok=True)

    # Don't redownload the file if we already have it (it's a large file)
    if force or not zip_path.exists():
        resp = requests.get(url, allow_redirects=True)
        zip_path.write_bytes(resp.content)

    shutil.rmtree(curriculum_path)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        members = [
            member
            for member in zip_ref.namelist()
            if member.startswith("freeCodeCamp-main/curriculum/")
            or member.startswith("freeCodeCamp-main/client/i18n/locales")
        ]
        zip_ref.extractall(members=members, path=curriculum_path)
        print(f"Extracted {len(members)} files")
