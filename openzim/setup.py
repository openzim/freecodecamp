#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

""" freeCodeCamp ZIM creator for Offline Use """

import pathlib
import shutil

from setuptools import setup

root_dir = pathlib.Path(__file__).parent


def copyParentData():
    sourcePaths = [
        pathlib.Path.joinpath(root_dir.parent, "LICENSE"),
        pathlib.Path.joinpath(root_dir.parent, "README.md"),
    ]
    for sourcePath in sourcePaths:
        dest = pathlib.Path.joinpath(root_dir, sourcePath.name)
        shutil.copy2(sourcePath, dest)


copyParentData()


def read(*names, **kwargs):
    with open(root_dir.joinpath(*names), "r") as fh:
        return fh.read()


setup(
    name="fcc2zim",
    version=read("fcc2zim", "VERSION").strip(),
    description=__doc__,
    author="Kiwix",
    author_email="reg@kiwix.org",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="http://github.com/openzim/fcc",
    keywords="fcc freecodecamp zim kiwix openzim offline",
    license="GPL-3.0",
    packages=["fcc2zim"],
    zip_safe=False,
    platforms="any",
    include_package_data=True,
    data_files=["LICENSE", "README.md", "requirements.pip"],
    # package_data={"": [f for f in copy_client()]},
    # package_dir={"": "openzim"},
    install_requires=[
        line.strip()
        for line in read("requirements.pip").splitlines()
        if not line.strip().startswith("#")
    ],
    entry_points={
        "console_scripts": [
            "fcc2zim=fcc2zim.__main__:main",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
)
