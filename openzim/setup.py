#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

""" Project Gutemberg ZIM creator for Offline Use """

from codecs import open

from fcc2zim import VERSION
from setuptools import find_packages, setup

with open("requirements.pip", "r") as f:
    requirements = [line.strip() for line in f.readlines() if len(line.strip())]
with open("pypi-readme.rst", "r", "utf-8") as f:
    readme = f.read()

setup(
    name="fcc2zim",
    version=VERSION,
    description=__doc__,
    author="Kiwix",
    author_email="reg@kiwix.org",
    long_description=readme,
    url="http://github.com/openzim/fcc",
    keywords="fcc zim kiwix openzim offline",
    license="GPL-3.0",
    packages=find_packages("."),
    zip_safe=False,
    platforms="any",
    include_package_data=True,
    data_files=["pypi-readme.rst", "LICENSE", "requirements.pip"],
    package_dir={"fcc": "fcc"},
    install_requires=requirements,
    scripts=["fcc2zim"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
)
