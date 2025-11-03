import pathlib
import re

import yaml

FRONTMATTER_BOUNDARY = re.compile(r"^-{3,}\s*$", re.MULTILINE)


# Each markdown challenge contains 'frontmatter' which is a header
# consisting of yaml formatted data enclosed inside of '---\n' lines
# We load into YAML only the frontmatter
def read_yaml_frontmatter(filename: pathlib.Path) -> dict[str, str]:
    _, fm, _ = FRONTMATTER_BOUNDARY.split(filename.read_text("UTF8"), 2)
    return yaml.load(  # pyright: ignore[reportReturnType, reportUnknownVariableType, reportUnknownMemberType]
        fm, Loader=yaml.SafeLoader
    )


class Challenge:
    def __init__(self, course_superblock: str, fpath: str | pathlib.Path) -> None:
        self.path = pathlib.Path(fpath)
        self.course_slug = self.path.parent.stem
        self.course_superblock = course_superblock
        self.language = self.path.parent.parent.parent.stem
        self._frontmatter = None

    def identifier(self):
        return str(self.frontmatter()["id"])

    def title(self):
        return str(self.frontmatter()["title"])

    def frontmatter(self):
        if not self._frontmatter:
            self._frontmatter = read_yaml_frontmatter(self.path)
        return self._frontmatter
