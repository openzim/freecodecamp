import os
import re
from fcctozim.relative_path_swap import RelPathProvider
from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint
import magic

mime = magic.Magic(mime=True)

class MyItem(Item):
    def __init__(self, title, rel_path, fpath):
        super().__init__()
        self.rel_path = rel_path
        self.title = title
        self.fpath = fpath

    def get_path(self):
        return os.path.relpath(self.fpath, self.rel_path)

    def get_title(self):
        if self.title:
            return self.title
        return self.get_path().title()

    def get_mimetype(self):
        # magic seems to think .js is text/plain
        if (re.search(r'js$', self.fpath)):
            return 'application/javascript'
        if (re.search(r'css$', self.fpath)):
            return 'text/css'
        return mime.from_file(self.fpath)

    def get_contentprovider(self):
        # ext = os.path.splitext(self.fpath)
        # if ext[1] in ['.css', '.html', '.js']:
        #     result = RelPathProvider(self.get_path(), self.fpath, '/__KIWIX_ROOT__').get_relative_content()
        #     return result
        return FileProvider(self.fpath)
       
    def get_hints(self):
        return {Hint.FRONT_ARTICLE: True}


def build_zimfile(source_dir, course_slug):
    rootPath = os.path.join(source_dir, 'index.html')
    fileList = []
    for (root, dirs, files) in os.walk(source_dir):
        for name in files:
            fileList.append(os.path.join(root, name))

    fileList = [file for file in fileList if os.path.splitext(file)[1] != '.map']
    # def matches_course_slug(full_path):
        # paths = full_path.split(os.sep)
        # if (len(paths) > 3 and paths[1] == 'learn'):
            # return paths[2] == course_slug
        # if (len(paths) > 3 and paths[1] == 'page-data' and paths[2] == 'learn'):
            # return paths[3] == course_slug
        # return True
# 
    # fileList = filter(matches_course_slug, fileList)
# 
    root_item = MyItem("Home", source_dir, rootPath)

    items = []

    for file in fileList:
        items.append(MyItem(None, source_dir, file))
        ext = os.path.splitext(file)

    with Creator("test.zim").config_indexing(True, "eng") as creator:
        creator.set_mainpath(root_item.get_path())
        creator.add_item(root_item)
        for item in items:
            print("Adding ", item.get_path() , item.get_mimetype())
            if (item.fpath != rootPath):
                creator.add_item(item)
        print("Done adding all pages")
        for name, value in {
            "creator": "python-libzim",
            "description": "Created in python",
            "name": "my-zim",
            "publisher": "You",
            "title": "Test ZIM",
        }.items():

            print("adding metadata: ", name.title(), value)
            creator.add_metadata(name.title(), value)