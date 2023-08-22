=============
fcc2zim
=============

A scraper that downloads selected course material from `freeCodeCamp <http://freecodecamp.org>`_
and puts it into a `ZIM file <http://www.openzim.org>`_,
a clean and user friendly format for storing content for offline usage.

------------
Dependencies
------------

Aside Python dependencies which are managed, other binary dependencies comes from `zimscraperlib <https://github.com/openzim/python-scraperlib/>`_

------
Usage
------

.. code-block:: sh

	fcc2zim [-h] --course COURSE --language LANGUAGE --name NAME --title TITLE --description
				DESCRIPTION [--long-description LONG_DESCRIPTION] [--creator CREATOR]
				[--publisher PUBLISHER] [--fetch] [--prebuild] [--build] [--force] [--debug]
				[--out-dir OUT_DIR] [--tmp-dir TMP_DIR] [--zimui-dist-dir ZIMUI_DIST_DIR]
				[--zim-file ZIM_FILE] [--zip-path ZIP_PATH] [--version]

	options:
	-h, --help            show this help message and exit
	--course COURSE       Course or course list (separated by commas)
	--language LANGUAGE   Curriculum language
	--name NAME           ZIM name. Used as identifier and filename (date will be appended)
	--title TITLE         Title of zim file
	--description DESCRIPTION
							Description of ZIM file
	--long-description LONG_DESCRIPTION
							Long description of ZIM file
	--creator CREATOR     Name of freeCodeCamp courses creator
	--publisher PUBLISHER
							Publisher of the zim file
	--fetch               Run fetch scraper phase
	--prebuild            Run pre-build scraper phase
	--build               Run build scraper phase
	--force               Force a full reprocessing, not benefiting from any cached file
	--debug               Enable verbose output
	--out-dir OUT_DIR     Output directory where zim file will be built
	--tmp-dir TMP_DIR     The temporary directory to hold temporary files during scraper operation
	--zimui-dist-dir ZIMUI_DIST_DIR
							Directory containing Vite build output from the Zim UI Vue.JS application
	--zim-file ZIM_FILE   ZIM file name (based on --name if not provided), could contain {period}
							placeholder which will be replaced by <year>_<month>
	--zip-path ZIP_PATH   Path to zip file containing FCC courses
	--version             Display scraper version and exit
