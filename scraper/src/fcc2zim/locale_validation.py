import json
import re
from pathlib import Path
from typing import cast

import yaml

from fcc2zim.constants import ROOT_DIR
from fcc2zim.context import Context

logger = Context.logger
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")


def validate_locales(locales_path: Path, included_superblocks: dict[str, list[str]]):
    """Checks locale files against ui_keys.yaml and fails it if anything seems off."""

    spec = yaml.safe_load((ROOT_DIR / "ui_keys.yaml").read_text())
    translations = json.loads(
        (locales_path / "translations.json").read_text(encoding="utf-8")
    )
    intro = json.loads((locales_path / "intro.json").read_text(encoding="utf-8"))
    errors: list[str] = []

    # checks static keys from translations.json and intro.json
    for file_key, data in [("translations", translations), ("intro", intro)]:
        if file_key not in spec:
            continue
        for section, keys in spec[file_key].items():
            if section not in data:
                errors.append(f"{file_key}.json: missing section '{section}'")
                continue
            for key, opts in keys.items():
                if key not in data[section]:
                    errors.append(f"{file_key}.json: missing key '{section}.{key}'")
                    continue

                value = data[section][key]
                if not isinstance(value, str):
                    continue

                actual: set[str] = set(PLACEHOLDER_RE.findall(value))
                expected: set[str] = (
                    set(opts.get("placeholders", [])) if opts else set()
                )

                for name in expected - actual:
                    errors.append(
                        f"{file_key}.json: '{section}.{key}'"
                        f" missing placeholder {{{{{name}}}}}"
                    )
                for name in actual - expected:
                    errors.append(
                        f"{file_key}.json: '{section}.{key}'"
                        f" has unexpected placeholder {{{{{name}}}}}"
                    )

    # checks intro.json has entries for every included superblock/course
    for superblock, courses in included_superblocks.items():
        if superblock not in intro:
            errors.append(f"intro.json: missing superblock '{superblock}'")
            continue

        sb = intro[superblock]
        for field in ("title", "intro", "blocks"):
            if field not in sb:
                errors.append(f"intro.json: superblock '{superblock}' has no '{field}'")

        # checks superblock intro has no unexpected placeholders
        if "title" in sb and isinstance(sb["title"], str):
            for ph in PLACEHOLDER_RE.findall(sb["title"]):
                errors.append(
                    f"intro.json: '{superblock}.title'"
                    f" has unexpected placeholder {{{{{ph}}}}}"
                )
        if "intro" in sb and isinstance(sb["intro"], list):
            for para in sb["intro"]:
                if isinstance(para, str):
                    for ph in PLACEHOLDER_RE.findall(para):
                        errors.append(
                            f"intro.json: '{superblock}.intro'"
                            f" has unexpected placeholder {{{{{ph}}}}}"
                        )

        blocks = sb.get("blocks", {})
        for course in courses:
            if course not in blocks:
                errors.append(
                    f"intro.json: can't find block '{course}' in '{superblock}'"
                )
                continue
            for field in ("title", "intro"):
                if field not in blocks[course]:
                    errors.append(f"intro.json: block '{course}' has no '{field}'")
                    continue
                val = blocks[course][field]
                if isinstance(val, str):
                    texts: list[str] = [val]
                elif isinstance(val, list):
                    texts = cast(list[str], val)
                else:
                    texts = []
                for text in texts:
                    for ph in PLACEHOLDER_RE.findall(text):
                        errors.append(
                            f"intro.json: '{superblock}.blocks.{course}.{field}'"
                            f" has unexpected placeholder {{{{{ph}}}}}"
                        )

    if errors:
        for err in errors:
            logger.error(err)
        raise ValueError(f"Locale validation failed with {len(errors)} error(s)")
    logger.info("Locale files validated")
