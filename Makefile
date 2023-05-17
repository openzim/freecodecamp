SHELL=/bin/bash

COURSES = 	regular-expressions \
	    	basic-javascript \
			basic-data-structures \
			debugging \
			functional-programming \
			object-oriented-programming \
			basic-algorithm-scripting \
			intermediate-algorithm-scripting \
			javascript-algorithms-and-data-structures-projects

COURSE_CSV=$(shell sed -r 's/\s/,/g' <<< "${COURSES}")

LANG=english
DISTDIR=./client/dist
TMPDIR=./tmp
OUTPATH=./${LANG}.zim

.PHONY: all setup clean

clean:
	rm -rf client/src/assets/curriculum
	rm -rf client/dist
	rm -rf ${TMPDIR}

setup:
	cd openzim && \
    	pip install -r requirements.txt
	cd client && \
    	yarn install --frozen-lockfile

fetch:
	python3 openzim/fcc2zim fetch --filter=02-javascript --tmp_dir=${TMPDIR}

prebuild:
	python3 openzim/fcc2zim prebuild --course=${COURSE_CSV} --outdir=./client/src/assets/curriculum --lang ${LANG} --tmp_dir=${TMPDIR}

build:
	cd client && yarn build
	python3 openzim/fcc2zim zim --distdir ${DISTDIR} --outpath ${OUTPATH}

all: fetch prebuild build
