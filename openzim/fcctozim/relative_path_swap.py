from itertools import repeat
import os

from libzim.writer import StringProvider


# Request for
# /PREFIX/static/foo.css
# from 
# ./my/long/path/index.html should become
# ../../../static/foo.css
class RelPathProvider:
    def __init__(self, rel_path: str, fpath: str, prefix: str):
        super().__init__()
        self.filepath = fpath
        self.path = rel_path
        self.prefix = prefix
        self.size = os.path.getsize(self.filepath)

    def get_replacement_path(self):
        parts = self.path.split(os.sep)
        depth = len(parts)
        # Is at root level eg. '/index.html' => './'
        if (depth == 2):
            return './'
        else:
        # Is at root level eg. '/static/foo/index.html' => ''
          return os.sep.join(list(repeat('..', depth - 1)))


    def get_relative_content(self):
        # Reading the content of the file
        # using the read() function and storing
        # them in a new variable
        with open(self.filepath, 'r') as file:
            data = file.read()
            return StringProvider(data.replace(self.prefix, self.get_replacement_path()))


