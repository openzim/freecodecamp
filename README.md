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

- `scraper` - The Python tool that build FCC ZIM. It is responsible to:
    - fetch FCC curriculum and package it into a proper format
    - embed client can read, as well as our zim builder
- `zimui` - A Vue.JS application specially crafted to:
    - be embeded inside the ZIM and serve as main entry point (through compilation for offline usage with Vite)
    - present FCC curriculum, including solving exercices
    - be compatible with most ZIM readers

## Scraper operation

The scraper assumes that `zimui` is already built and ready to be embedded into the ZIM in the `<zimui_dir>`.

The scraper operation is divided into three phases:
1. `fetch`: retrieve curriculum source code from Github and extracts it into `<tmp_dir>/curriculum` folder
2. `prebuild`: transform curriculum data into files ready to be consumed by the Vite UI
3. `build`: create the final ZIM with `zimui` and curriculum data

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md).

### Prerequisites

- Node 20.x
- Python 3.11

This project comes with .devcontainer to help onboard new developers, with Node 20 and Python3 installed

See: [`Makefile`](Makefile) for a full build process

### Running scraper with Docker

Run from official version (published on GHCR.io) ; ZIM will be available in the `output` sub-folder of current working directory.

```
docker run --rm -it -v $(pwd)/output:/output ghcr.io/openzim/freecodecamp:latest --language eng --course "regular-expressions,basic-javascript,basic-data-structures,debugging,functional-programming,object-oriented-programming,basic-algorithm-scripting,intermediate-algorithm-scripting,javascript-algorithms-and-data-structures-projects" --name "fcc_en_javascript" --title "freeCodeCamp Javascript" --description "FCC Javascript Courses"
```

You might add `-v $(pwd)/tmp:/tmp` parameter to also mount temporary directory and keep temporary artificats.

You might use the `dev` Docker image tag instead of `latest` to use current development version (based on Github `main` branch).

You might build your own local Docker image and then use it with `openzim/freecodecamp` instead of `ghcr.io/openzim/freecodecamp:latest`:
```
docker build -t openzim/freecodecamp .
```

## Course Options and Limitations

Currently this scraper only supports Javascript challenges. A list of courses is passed to the scraper as a comma seperated list of 'course slugs'.

You can find a list of course slugs in the [freeCodeCamp curriculum folder](https://github.com/freeCodeCamp/freeCodeCamp/tree/main/curriculum/challenges/english/02-javascript-algorithms-and-data-structures)

In docker example above, see the `--course` argument : `regular-expressions,basic-javascript,basic-data-structures,debugging,functional-programming,object-oriented-programming,basic-algorithm-scripting,intermediate-algorithm-scripting,javascript-algorithms-and-data-structures-projects`

## License

This repository is licensed under GPLv3, with the exception of the freeCodeCamp curriculum which is licensed under BSD 3 Clause (see LICENSE.fcc.md).
