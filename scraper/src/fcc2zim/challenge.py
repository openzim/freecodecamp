import pathlib

import yaml


# Each markdown challenge contains 'frontmatter' which is a header
# consisting of yaml formatted data enclosed inside of '---\n' lines
# '---' lines in YAML denote multiple documents, so this can be read
# directly with python's yaml library pulling in the first document
# with 'next' and immediately returning
def read_yaml_frontmatter(filename: pathlib.Path):
    with open(filename) as f:
        return next(yaml.load_all(f, Loader=yaml.FullLoader))


class Challenge:
    def __init__(self, fpath: str | pathlib.Path) -> None:
        self.path = pathlib.Path(fpath)
        self.course_slug = self.path.parent.stem
        self.course_superblock = "-".join(self.path.parent.parent.stem.split("-")[1:])
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
