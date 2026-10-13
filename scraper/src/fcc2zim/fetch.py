import shutil
import zipfile
from pathlib import Path

import requests

from fcc2zim.context import Context

logger = Context.logger


def fetch_command(
    zip_main_path: Path,
    zip_i18n_path: Path,
    curriculum_raw: Path,
    fcc_lang: str,
    *,
    force: bool,
):
    logger.info("Scraper: fetch phase starting")
    main_url = (
        "https://github.com/freeCodeCamp/freeCodeCamp/archive/refs/heads/main.zip"
    )
    i18n_url = (
        "https://github.com/freeCodeCamp/i18n-curriculum/archive/refs/heads/main.zip"
    )

    # Don't redownload the file if we already have it (it's a large file)
    for zip_path in [zip_main_path, zip_i18n_path]:
        if force or not zip_path.exists():
            logger.debug(f"Download zip file to {zip_path}")
            resp = requests.get(
                main_url if zip_path == zip_main_path else i18n_url,
                allow_redirects=True,
                timeout=5,
            )
            zip_path.write_bytes(resp.content)
        else:
            logger.debug(f"Using existing zip file {zip_path}")

    curriculum_raw.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(curriculum_raw)

    logger.debug("Extracting files")
    for zip_path in [zip_main_path, zip_i18n_path]:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            count = 0
            fcc_main_client_prefix = (
                f"freeCodeCamp-main/client/i18n/locales/{fcc_lang}/"
            )
            i18n_client_prefix = f"i18n-curriculum-main/client/{fcc_lang}/"
            for member in zip_ref.namelist():
                if member.endswith("/"):
                    continue
                if member.startswith("freeCodeCamp-main/curriculum/structure") or (
                    member.startswith(
                        f"freeCodeCamp-main/curriculum/challenges/{fcc_lang}"
                    )
                    or member.startswith(
                        f"freeCodeCamp-main/curriculum/dictionaries/{fcc_lang}"
                    )
                    or member.startswith(
                        f"i18n-curriculum-main/curriculum/challenges/{fcc_lang}"
                    )
                    or member.startswith(
                        f"i18n-curriculum-main/curriculum/dictionaries/{fcc_lang}"
                    )
                ):
                    # compute path to merge freeCodeCamp and i18n-curriculum content
                    target_path = (
                        curriculum_raw
                        / "extracted"
                        / member[18 if member.startswith("freeCodeCamp-main") else 21 :]
                    )
                elif member.startswith(fcc_main_client_prefix):
                    # English client UI translation files are still published in the
                    # freeCodeCamp main repo
                    target_path = (
                        curriculum_raw
                        / "extracted"
                        / "client"
                        / fcc_lang
                        / member.removeprefix(fcc_main_client_prefix)
                    )
                elif member.startswith(i18n_client_prefix):
                    # non-English client UI translation files were moved out of the
                    # freeCodeCamp main repo and into i18n-curriculum
                    # (see freeCodeCamp/freeCodeCamp#68425)
                    target_path = (
                        curriculum_raw
                        / "extracted"
                        / "client"
                        / fcc_lang
                        / member.removeprefix(i18n_client_prefix)
                    )
                else:
                    continue
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_bytes(zip_ref.read(member))
                count += 1
            logger.info(f"Extracted {count} files from {zip_path}")
    logger.info(f"Fetched curriculum into {curriculum_raw}")
    logger.info("Scraper: fetch phase finished")
