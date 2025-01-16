import tempfile
from pathlib import Path

from fcc2zim.challenge import read_yaml_frontmatter


def test_good_front_matter():
    with tempfile.TemporaryDirectory() as tmp_dir:
        md_file = Path(tmp_dir) / "file.md"
        # dd:ee\ndd: is bad YAML which is intentionaly here, because outside
        # the front matter and should hence be properly ignored
        md_file.write_text("----\ntitle: foo\nsubject: bar\n---\ndd:ee\ndd:")
        front = read_yaml_frontmatter(md_file)
        assert front["title"] == "foo"
        assert front["subject"] == "bar"
