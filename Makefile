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
OUTPATH=./build/${LANG}.zim
MAX_LINE_LENGTH = 88

.PHONY: all setup clean client build

clean:
	rm -rf client/dist/fcc
	rm -rf client/public/fcc
	rm -rf ${TMPDIR}/curriculum
	rm -rf build

setup:
	cd openzim && \
    	pip install -r requirements.txt \
    	pip install -r lint_requirements.txt

lint:
	cd openzim
	black .
	flake8 . --count --max-line-length=${MAX_LINE_LENGTH} --statistics
	isort --profile black .

fetch:
	python3 openzim/fcctozim fetch --tmpdir=${TMPDIR}

prebuild:
	python3 openzim/fcctozim prebuild --course=${COURSE_CSV} --curriculumdir=./client/dist/fcc --language ${LANG} --tmpdir=${TMPDIR}

zim:
	python3 openzim/fcctozim zim --clientdir ${CLIENTDIR} --outpath ${OUTPATH} \
	--language ${LANG} --name ${NAME} --title ${TITLE} --description ${DESCRIPTION}

all: clean fetch prebuild zim

build:
	python3 openzim/fcctozim all --clientdir ${CLIENTDIR} --curriculumdir=./client/dist/fcc --outpath ${OUTPATH} \
	--language ${LANG} --tmpdir=${TMPDIR} --course=${COURSE_CSV} \
	--name ${NAME} --title ${TITLE} --description ${DESCRIPTION}

docker_build:
	docker build . -t openzim/fcctozim

docker_run:
	docker run --rm -it -v $(PWD)/tmp:/tmp/fcctozim openzim/fcctozim all --clientdir ${CLIENTDIR} --curriculumdir=./client/dist/fcc --outpath ${OUTPATH} \
	--language ${LANG} --tmpdir=/tmp/fcctozim --course=${COURSE_CSV} \
	--name ${NAME} --title ${TITLE} --description ${DESCRIPTION}

docker_debug:
	docker run --rm -it --entrypoint=/bin/bash openzim/fcctozim