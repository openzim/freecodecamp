import os
import re
import json

from zimscraperlib.zim import Archive, Creator, StaticItem, URLItem
from frontmatter import Frontmatter

logo_path = os.path.join(os.path.dirname(__file__), '..', 'fcc_48.png')

def build_curriculum_redirects(client_dir, language):
    index_json_path = os.path.join(client_dir, 'src/assets/curriculum/index.json')
    with open(index_json_path) as course_index_str:
        course_list = json.load(course_index_str)[language]
    redirects = []
    for course in course_list:
        meta_json_path = os.path.join(client_dir, 'src/assets/curriculum/', language, course, '_meta.json')
        with open(meta_json_path) as meta_json_str:
            challenges = json.load(meta_json_str)['challenges']
        for challenge in challenges:
            redirects.append([ f'index.html#{language}/{course}/{challenge["slug"]}', challenge['title'] ])
            
    return redirects


def build_zimfile(client_dir, outpath, language):
    source_dir = os.path.join(client_dir, 'dist')
    rootPath = os.path.join(source_dir, 'index.html')
    fileList = []
    for (root, dirs, files) in os.walk(source_dir):
        for name in files:
            fileList.append(os.path.join(root, name))

    fileList = [file for file in fileList if os.path.splitext(file)[1] != '.map']

    main_path = os.path.relpath(rootPath, source_dir)
    tags = ";".join(["FCC", "freeCodeCamp"])
    with open(logo_path, "rb") as fh:
        png_data = fh.read()
    with Creator(outpath, main_path).config_dev_metadata(
        Tags=tags, Illustration_48x48_at_1=png_data
    ) as creator:
        for file in fileList:
            print(file)
            path = os.path.relpath(file, source_dir)
            creator.add_item_for(path, fpath=file)
        

        for course_page in build_curriculum_redirects(client_dir, language):
            print(course_page[0], course_page[1])
            creator.add_redirect(course_page[0], course_page[0], course_page[1], is_front=True)
            # chrome-extension://donaljnlmapmngakoipdmehbfcioahhk/english.zim/C/index.html#/english/regular-expressions/extract-matches
