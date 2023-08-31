import shutil
import zipfile
from pathlib import Path

import requests

from fcc2zim.constants import Global


def fetch_command(zip_path: Path, curriculum_raw: Path, *, force: bool):
    Global.logger.info("Scraper: fetch phase starting")
    url = "https://github.com/freeCodeCamp/freeCodeCamp/archive/refs/heads/main.zip"

    # Don't redownload the file if we already have it (it's a large file)
    if force or not zip_path.exists():
        Global.logger.debug(f"Download zip file to {zip_path}")
        resp = requests.get(url, allow_redirects=True, timeout=5)
        zip_path.write_bytes(resp.content)
    else:
        Global.logger.debug(f"Using existing zip file {zip_path}")

    curriculum_raw.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(curriculum_raw)

    Global.logger.debug("Extracting files")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        members = [
            member
            for member in zip_ref.namelist()
            if member.startswith("freeCodeCamp-main/curriculum/")
            or member.startswith("freeCodeCamp-main/client/i18n/locales")
        ]
        zip_ref.extractall(members=members, path=curriculum_raw)
        Global.logger.info(f"Extracted {len(members)} files")
    Global.logger.info(f"Fetched curriculum into {curriculum_raw}")
    Global.logger.info("Scraper: fetch phase finished")
