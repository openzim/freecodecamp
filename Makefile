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

COURSE_CSV=$(shell sed -r 's/[[:space:]]/,/g' <<< "${COURSES}")

LANG=english
CLIENTDIR=./client
TMPDIR=./tmp
OUTPATH=./${LANG}.zim

.PHONY: all setup clean

clean:
	rm -rf client/src/assets/fcc
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
	python3 openzim/fcc2zim prebuild --course=${COURSE_CSV} --outdir=./client/public/fcc --lang ${LANG} --tmp_dir=${TMPDIR}

build_client:
	cd client && yarn build

build_zim:
	python3 openzim/fcc2zim zim --clientdir ${CLIENTDIR} --outpath ${OUTPATH} --lang ${LANG}

build: build_client build_zim

all: fetch prebuild build
