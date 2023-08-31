import datetime
from pathlib import Path

from zimscraperlib.zim import Creator

from fcc2zim.build import build_command
from fcc2zim.constants import FCC_LANG_MAP, VERSION, Global
from fcc2zim.fetch import fetch_command
from fcc2zim.prebuild import prebuild_command
from fcc2zim.zimscraperlib_fork import compute_descriptions


class Scraper:
    def __init__(
        self,
        *,
        do_fetch: bool,
        do_prebuild: bool,
        do_build: bool,
        zimui_dist: str,
        output: str,
        build: str,
        language: str,
        name: str,
        title: str,
        description: str,
        long_description: str | None,
        content_creator: str,
        publisher: str,
        zim_file: str | None,
        force: bool,
        course_csv: str,
        zip_path: str | None,
        start_date: datetime.date,
    ):
        self.creator = None

        self.do_fetch = do_fetch
        self.do_prebuild = do_prebuild
        self.do_build = do_build

        if not (self.do_fetch + self.do_prebuild + self.do_build):
            self.do_fetch = self.do_prebuild = self.do_build = True

        self.zimui_dist = Path(zimui_dist)
        if not self.zimui_dist.exists():
            raise ValueError(f"zimui_dist directory {self.zimui_dist} does not exists")

        self.output = Path(output)
        self.build = Path(build)
        self.curriculum_raw = self.build.joinpath("curriculum-raw")
        self.curriculum_dist = self.build.joinpath("curriculum-dist")

        # Make sure the output directory exists
        self.output.mkdir(parents=True, exist_ok=True)
        self.build.mkdir(parents=True, exist_ok=True)

        self.language = language
        if self.language not in FCC_LANG_MAP:
            raise ValueError(f"Unsupported language {self.language}")
        self.fcc_lang = FCC_LANG_MAP[language]

        self.name = name
        self.title = title

        self.description = description
        self.long_description = long_description
        self.description, self.long_description = compute_descriptions(
            self.description, self.description, self.long_description
        )

        self.content_creator = content_creator
        self.publisher = publisher
        self.force = force
        self.course_csv = course_csv
        if not zip_path:
            self.zip_path = self.build.joinpath("main.zip")
        else:
            self.zip_path = Path(zip_path)
            if not self.zip_path.exists():
                raise ValueError(f"Zip file not found in {self.zip_path}")

        # if we do not build the ZIM, we can stop here
        if not self.do_build:
            return

        period = start_date.strftime("%Y-%m")
        if zim_file:
            self.zim_path = Path(zim_file.format(period=period))
            # make sure we were given a filename and not a path
            if Path(self.zim_path.name) != self.zim_path:
                raise ValueError(f"zim_name is not a filename: {zim_file}")
        else:
            self.zim_path = Path(f"{name}_{period}.zim")

        # build full path
        self.zim_path = self.output.joinpath(self.zim_path)

        if self.zim_path.exists():
            if not self.force:
                raise ValueError(f"ZIM file {self.zim_path} already exist.")
            Global.logger.info(f"Removing existing ZIM file {self.zim_path}")
            self.zim_path.unlink()
        else:
            Global.logger.info(f"ZIM path: {self.zim_path}")

        logo_path = Path(__file__).parent.joinpath("assets", "fcc_48.png")
        if not logo_path.exists():
            raise ValueError(f"Logo not found at {logo_path}")

        self.creator = Creator(self.zim_path, "index.html").config_metadata(
            Name=self.name,
            Title=self.title,
            Publisher=self.publisher,
            Date=start_date,
            Creator=self.content_creator,
            Description=self.description,
            LongDescription=self.long_description,
            Language=self.language,
            Tags=";".join(["FCC", "freeCodeCamp"]),
            Scraper=f"fcc2zim v{VERSION}",
            Illustration_48x48_at_1=logo_path.read_bytes(),
        )

        # start creator early to detect any problem early as well
        self.creator.start()

    def run(self):
        try:
            self.run_commands()
        except Exception as exc:
            if self.creator:
                self.creator.can_finish = False
            if isinstance(exc, KeyboardInterrupt):
                Global.logger.error("KeyboardInterrupt, exiting.")
                raise SystemExit(3) from exc
            else:
                Global.logger.error(f"Interrupting process due to error: {exc}")
                Global.logger.exception(exc)
                raise SystemExit(2) from exc
        else:
            if self.creator:
                self.creator.finish()
                Global.logger.info(f"Finished creating Zim at {self.zim_path}")

    def run_commands(self):
        if self.do_fetch:
            fetch_command(
                force=self.force,
                curriculum_raw=self.curriculum_raw,
                zip_path=self.zip_path,
            )
        if self.do_prebuild:
            prebuild_command(
                fcc_lang=self.fcc_lang,
                course_csv=self.course_csv,
                curriculum_raw=self.curriculum_raw,
                curriculum_dist=self.curriculum_dist,
            )
        if self.do_build:
            build_command(
                fcc_lang=self.fcc_lang,
                creator=self.creator,
                zimui_dist=self.zimui_dist,
                curriculum_dist=self.curriculum_dist,
            )
