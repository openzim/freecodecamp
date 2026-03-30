"""Checks that the ZIM UI only uses translation keys that are listed in ui_keys.yaml."""

import re
import sys
from typing import cast

import yaml

from fcc2zim.constants import ROOT_DIR

UI_KEYS_PATH = ROOT_DIR / "ui_keys.yaml"
ZIMUI_SRC = ROOT_DIR.parent.parent.parent / "zimui" / "src"

T_CALL_RE = re.compile(r"main\.t\('([^']+)'")


def flatten_keys(
    data: dict[str, object], prefix: tuple[str, ...] = ()
) -> set[tuple[str, ...]]:
    result: set[tuple[str, ...]] = set()
    for key, value in data.items():
        path = (*prefix, key)
        if value is None:
            result.add(path)
        elif isinstance(value, dict):
            dict_value = cast(dict[str, object], value)
            if set(dict_value.keys()) == {"placeholders"}:
                result.add(path)
            else:
                result.update(flatten_keys(dict_value, path))
    return result


def main() -> None:
    spec: dict[str, object] = yaml.safe_load(UI_KEYS_PATH.read_text())
    allowed = flatten_keys(spec)

    errors: list[str] = []
    for file in list(ZIMUI_SRC.rglob("*.vue")) + list(ZIMUI_SRC.rglob("*.ts")):
        content = file.read_text()

        for match in T_CALL_RE.finditer(content):
            key_path = tuple(match.group(1).split("."))
            if key_path not in allowed:
                errors.append(f"{file.name}: unknown key {match.group(1)}")

    if errors:
        for err in errors:
            print(err, file=sys.stderr)  # noqa: T201
        sys.exit(1)

    print("All UI translation keys are in ui_keys.yaml")  # noqa: T201


if __name__ == "__main__":
    main()
