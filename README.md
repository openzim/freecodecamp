# FCC on Zim

This project consists of two major components:

- `scraper` - The Python tool that build FCC ZIM. It is responsible to:
    - fetch FCC curriculum and package it into a proper format
    - embed client can read, as well as our zim builder
- `zimui` - A vite app specially crafted to:
    - be embeded inside the ZIM and serve as main entry point
    - present FCC curriculum, including solving exercices
    - be compatible with most ZIM readers

## freeCodeCamp Zim build process

This process can be broken down into 5 parts

1. Build the Vite client
1. Fetch the latest curriculum from freeCodeCamp by downloading the latest release source archive
1. "Prebuild" the curriculum for a selected langauge and set of courses. Copy to the client directory
1. Build a Zim file of the resulting Vite application.

## Development

#### Prerequsites

- Node 20.x
- Python 3

This project comes with .devcontainer to help onboard new developers, with Node 20 and Python3 installed

See: [`Makefile`](Makefile) for a full build process

## Building with Docker

- `docker build -t openzim/fcc2zim .`
- `docker run --rm -it -v /workspaces/openzim-freecodecamp/tmp:/tmp/fcc2zim openzim/fcc2zim all \
    --clientdir ./client/dist --curriculumdir=./client/dist/fcc --outpath ./build/eng.zim \
    --language eng --tmpdir=/tmp/fcc2zim \
    --course=regular-expressions,basic-javascript,basic-data-structures,debugging,functional-programming,object-oriented-programming,basic-algorithm-scripting,intermediate-algorithm-scripting,javascript-algorithms-and-data-structures-projects \
    --name "fcc_en_javascript" --title "freeCodeCamp Javascript" --description "FCC Javascript Courses"
`

## Course Options and Limitations

Currently this scraper only supports Javascript challenges. A list of courses is passed to the `prebuild` step as a comma seperated list of 'course slugs'.

You can find a list of course slugs in the [freeCodeCamp curriculum folder](https://github.com/freeCodeCamp/freeCodeCamp/tree/main/curriculum/challenges/english/02-javascript-algorithms-and-data-structures)

Example:

```
python3 openzim/fcc2zim prebuild --course=regular-expressions,basic-javascript,basic-data-structures,debugging,functional-programming,object-oriented-programming,basic-algorithm-scripting,intermediate-algorithm-scripting,javascript-algorithms-and-data-structures-projects --curriculumdir=./client/dist/fcc --language eng --tmpdir=./tmp
```

# License

This repository is licensed under GPLv3, with the exception of the freeCodeCamp curriculum which is licensed under BSD 3 Clause (see LICENSE.fcc.md).
