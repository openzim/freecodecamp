#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
import argparse

from fcc2zim.build import build
from fcc2zim.fetch import fetch_command
from fcc2zim.prebuild import prebuild_command

arg_flags = {
    "tmpdir": {
        "flags": "--tmpdir",
        "type": str,
        "help": "the temporary directory to hold the curriculum",
    },
    "force": {
        "flags": "--force",
        "type": bool,
        "help": "force a re-download of the curriculum zip",
    },
    "language": {"flags": "--language", "type": str, "help": "Curriculum language"},
    "course": {
        "flags": "--course",
        "type": str,
        "help": "Course or course list (separated by commas)",
        "required": True,
    },
    "curriculumdir": {
        "flags": "--curriculumdir",
        "type": str,
        "help": "the directory to place the processed curriculum",
        "required": True,
    },
    "clientdir": {
        "flags": "--clientdir",
        "type": str,
        "help": "the directory containing our Vite application",
        "required": True,
    },
    "outpath": {
        "flags": "--outpath",
        "type": str,
        "help": "output path",
        "required": True,
    },
    "title": {
        "flags": "--title",
        "type": str,
        "help": "Title of zim file",
        "required": True,
    },
    "name": {
        "flags": "--name",
        "type": str,
        "help": "Name of zim file",
        "required": True,
    },
    "description": {
        "flags": "--description",
        "type": str,
        "help": "Description of zim file",
        "required": True,
    },
    "long_description": {
        "flags": "--long_description",
        "type": str,
        "help": "Long description of zim file",
        "required": False,
    },
    "creator": {
        "flags": "--creator",
        "type": str,
        "help": "Creator of the zim files content",
    },
    "publisher": {
        "flags": "--publisher",
        "type": str,
        "help": "Publisher of the zim file",
    },
}


def main():
    parser = argparse.ArgumentParser(prog="fcc2zim")

    # create sub-parser
    sub_parsers = parser.add_subparsers(help="sub-command help", dest="command")

    fetch_cmd = sub_parsers.add_parser("fetch", help="fetch the latest curriculum")
    add_arguments(fetch_cmd, [arg_flags["tmpdir"], arg_flags["force"]])

    prebuild_cmd = sub_parsers.add_parser(
        "prebuild", help="prebuild curriculum for Vite frontend"
    )
    add_arguments(
        prebuild_cmd,
        [
            arg_flags["language"],
            arg_flags["course"],
            arg_flags["curriculumdir"],
            arg_flags["tmpdir"],
        ],
    )

    zim_cmd = sub_parsers.add_parser("zim", help="package up the zim file")
    add_arguments(
        zim_cmd,
        [
            arg_flags["clientdir"],
            arg_flags["outpath"],
            arg_flags["language"],
            arg_flags["title"],
            arg_flags["name"],
            arg_flags["description"],
            arg_flags["long_description"],
            arg_flags["creator"],
            arg_flags["publisher"],
        ],
    )

    all_cmd = sub_parsers.add_parser(
        "all", help="fetch, build and package up a zim file"
    )
    add_arguments(all_cmd, [arg_flags[key] for key in arg_flags])

    args = parser.parse_args()
    if args.command:
        command = args.command

        if command == "fetch":
            fetch_command(args)
        elif command == "prebuild":
            prebuild_command(args)
        elif command == "zim":
            build(args)
        elif command == "all":
            fetch_command(args)
            prebuild_command(args)
            build(args)
    else:
        parser.print_usage()


def add_arguments(parser, args):
    for arg in args:
        parser.add_argument(
            arg["flags"],
            type=arg.get("type", str),
            help=arg["help"],
            required=arg.get("required", False),
        )
