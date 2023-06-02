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

TITLE="freeCodeCamp Javascript"
NAME="fcc_en_javascript"
DESCRIPTION="FCC Javascript Courses"
LANG=eng
CLIENTDIR=./client/dist
TMPDIR=./tmp
OUTPATH=./${LANG}.zim

.PHONY: all setup clean client

clean_curriculum:
	rm -rf client/dist/fcc

clean:
	rm -rf client/dist
	rm -rf ${TMPDIR}

setup:
	cd openzim && \
    	pip install -r requirements.txt

client:
	cd client && rm -rf dist && yarn install --frozen-lockfile && yarn build

fetch:
	python3 openzim/fcc2zim fetch --tmpdir=${TMPDIR}

prebuild:
	python3 openzim/fcc2zim prebuild --course=${COURSE_CSV} --outdir=./client/dist/fcc --language ${LANG} --tmpdir=${TMPDIR}

build_zim:
	python3 openzim/fcc2zim all --clientdir ${CLIENTDIR} --outzim ${OUTPATH} \
	--language ${LANG} --name ${NAME} --title ${TITLE} --description ${DESCRIPTION}

all:
	python3 openzim/fcc2zim all --clientdir ${CLIENTDIR} --outdir=./client/dist/fcc --outzim ${OUTPATH} \
	--language ${LANG} --tmpdir=${TMPDIR} --course=${COURSE_CSV} \
	--name ${NAME} --title ${TITLE} --description ${DESCRIPTION}
