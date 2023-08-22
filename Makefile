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
TMPDIR=./tmp
OUTDIR=./output
ZIMUI_DIST_DIR=./zimui/dist
MAX_LINE_LENGTH = 88

.PHONY: all clean

clean:
	rm -rf ${TMPDIR}
	rm -rf ${OUTDIR}
	rm -rf ${ZIMUI_DIST_DIR}
	
scraper_setup:
	cd scraper && \
		pip install -U pip && \
		pip install -r requirements.txt && \
		pip install -r lint_requirements.txt

scraper_lint:
	black scraper
	flake8 scraper/fcc2zim --count --max-line-length=${MAX_LINE_LENGTH} --statistics
	isort --profile black -p fcc2zim scraper/fcc2zim

zimui_build:
	cd zimui && \
		yarn install --frozen-lockfile  && \
		yarn build

scraper_fetch:
	python3 scraper/fcc2zim --fetch \
	--language ${LANG} --course=${COURSE_CSV} \
	--name ${NAME} --title ${TITLE} --description ${DESCRIPTION} \
	--out-dir ${OUTDIR} --tmp-dir ${TMPDIR} \
	--zimui-dist-dir ${ZIMUI_DIST_DIR}

scraper_prebuild:
	python3 scraper/fcc2zim --prebuild \
	--language ${LANG} --course=${COURSE_CSV} \
	--name ${NAME} --title ${TITLE} --description ${DESCRIPTION} \
	--out-dir ${OUTDIR} --tmp-dir ${TMPDIR} \
	--zimui-dist-dir ${ZIMUI_DIST_DIR}

scraper_build:
	python3 scraper/fcc2zim --build \
	--language ${LANG} --course=${COURSE_CSV} \
	--name ${NAME} --title ${TITLE} --description ${DESCRIPTION} \
	--out-dir ${OUTDIR} --tmp-dir ${TMPDIR} \
	--zimui-dist-dir ${ZIMUI_DIST_DIR}

all: clean zimui_build scraper_all

scraper_all:
	python3 scraper/fcc2zim \
	--language ${LANG} --course=${COURSE_CSV} \
	--name ${NAME} --title ${TITLE} --description ${DESCRIPTION} \
	--out-dir ${OUTDIR} --tmp-dir ${TMPDIR} \
	--zimui-dist-dir ${ZIMUI_DIST_DIR}

docker_build:
	docker build . -t openzim/freecodecamp

docker_run:
	docker run --rm -it -v $(PWD)/tmp:/tmp/fcc2zim openzim/freecodecamp \
	--language ${LANG} --course=${COURSE_CSV} \
	--name ${NAME} --title ${TITLE} --description ${DESCRIPTION} \
	--out-dir ${OUTDIR} --tmp-dir ${TMPDIR} 

docker_debug:
	docker run --rm -it --entrypoint=/bin/bash openzim/freecodecamp