# freeCodeCamp scraper

This scraper downloads selected [freeCodeCamp](https://www.freecodecamp.org/) courses and puts it in a
[ZIM](https://openzim.org) file, a clean and user friendly format for storing content for offline usage.

[![CodeFactor](https://www.codefactor.io/repository/github/openzim/freecodecamp/badge)](https://www.codefactor.io/repository/github/openzim/freecodecamp)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![codecov](https://codecov.io/gh/openzim/freecodecamp/branch/main/graph/badge.svg)](https://codecov.io/gh/openzim/freecodecamp)
[![PyPI version shields.io](https://img.shields.io/pypi/v/fcc2zim.svg)](https://pypi.org/project/fcc2zim/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fcc2zim.svg)](https://pypi.org/project/fcc2zim/)
[![Docker](https://ghcr-badge.deta.dev/openzim/freecodecamp/latest_tag?label=docker)](https://ghcr.io/openzim/freecodecamp)
## Architecture
This project consists of two major components:

- `zimui` - A Vue.JS application specially crafted to:
    - be embeded inside the ZIM and serve as main entry point (through compilation for offline usage with Vite)
    - present FCC curriculum, including solving exercices
    - be compatible with most ZIM readers
- `scraper` - The Python tool that build FCC ZIM. It is responsible to:
    - fetch FCC curriculum and package it into a proper format
    - embed client can read, as well as our zim builder

## Dependencies

Aside Node.JS and Python dependencies which are managed, other binary dependencies comes from Python [zimscraperlib](https://github.com/openzim/python-scraperlib/)


## Development

See [CONTRIBUTING.md](CONTRIBUTING.md).

### Prerequisites

- Node 20.x
- Python 3.11

### Running scraper locally

You have to:
- build the `zimui` frontend which will be embededed inside the ZIM (and redo it every time you make modifications to the `zimui`)
- run the `scraper` to retrieve FCC curriculum and build the ZIM

Sample commands:
```
cd zimui
yarn install
yarn build
cd ../scraper
hatch run fcc2zim --language eng --course "regular-expressions,basic-javascript,basic-data-structures,debugging,functional-programming,object-oriented-programming,basic-algorithm-scripting,intermediate-algorithm-scripting,javascript-algorithms-and-data-structures-projects" --name "fcc_en_javascript" --title "freeCodeCamp Javascript" --description "FCC Javascript Courses"
```

### Running scraper with Docker

Run from official version (published on GHCR.io) ; ZIM will be available in the `output` sub-folder of current working directory.

```
docker run --rm -it -v $(pwd)/output:/output ghcr.io/openzim/freecodecamp:latest fcc2zim --language eng --course "regular-expressions,basic-javascript,basic-data-structures,debugging,functional-programming,object-oriented-programming,basic-algorithm-scripting,intermediate-algorithm-scripting,javascript-algorithms-and-data-structures-projects" --name "fcc_en_javascript" --title "freeCodeCamp Javascript" --description "FCC Javascript Courses"
```

## Course Options and Limitations

Currently this scraper only supports Javascript challenges. A list of courses is passed to the scraper as a comma seperated list of 'course slugs'.

You can find a list of course slugs in the [freeCodeCamp curriculum folder](https://github.com/freeCodeCamp/freeCodeCamp/tree/main/curriculum/challenges/english/02-javascript-algorithms-and-data-structures)

In docker example above, see the `--course` argument : `regular-expressions,basic-javascript,basic-data-structures,debugging,functional-programming,object-oriented-programming,basic-algorithm-scripting,intermediate-algorithm-scripting,javascript-algorithms-and-data-structures-projects`
