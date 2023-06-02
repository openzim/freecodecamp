import os
import re
import json

from zimscraperlib.zim import Archive, Creator, StaticItem, URLItem
from fcctozim import logger

logo_path = os.path.join(os.path.dirname(__file__), '..', 'fcc_48.png')

def build_curriculum_redirects(clientdir, language):
    index_json_path = os.path.join(clientdir, 'src/assets/fcc/index.json')
    with open(index_json_path) as course_index_str:
        course_list = json.load(course_index_str)[language]

    redirects = []
    for course in course_list:
        meta_json_path = os.path.join(clientdir, 'src/assets/fcc/curriculum/', language, course, '_meta.json')
        with open(meta_json_path) as meta_json_str:
            challenges = json.load(meta_json_str)['challenges']
        for challenge in challenges:
            redirects.append([ f'index.html#{language}/{course}/{challenge["slug"]}', challenge['title'] ])
            
    return redirects


def build_zimfile(clientdir, outpath, language):
    source_dir = os.path.join(clientdir, 'dist')
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
        

        for course_page in build_curriculum_redirects(clientdir, language):
            print(course_page[0], course_page[1])
            creator.add_redirect(course_page[0], course_page[0], course_page[1], is_front=True)
            #Example index.html#/english/regular-expressions/extract-matches


def build(arguments):
    clientdir = arguments.clientdir
    outpath = arguments.outpath
    language = arguments.language
    logger.info(f'Building {clientdir} for {language} => {outpath}')

    build_zimfile(
        clientdir=clientdir,
        outpath=outpath,
        language=language
    )