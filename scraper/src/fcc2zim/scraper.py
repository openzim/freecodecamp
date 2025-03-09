import io
import logging
from pathlib import Path

from zimscraperlib.image.conversion import convert_image, convert_svg2png
from zimscraperlib.image.probing import format_for
from zimscraperlib.image.transformation import resize_image
from zimscraperlib.inputs import compute_descriptions, handle_user_provided_file
from zimscraperlib.zim import Creator, metadata

from fcc2zim.build import build_command
from fcc2zim.constants import FCC_LANG_MAP, VERSION
from fcc2zim.context import Context
from fcc2zim.fetch import fetch_command
from fcc2zim.prebuild import prebuild_command

logger = Context.logger
context = Context.get()


class Scraper:
    def __init__(self):
        logger.setLevel(level=logging.DEBUG if context.debug else logging.INFO)

        if not (context.do_fetch + context.do_prebuild + context.do_build):
            context.do_fetch = context.do_prebuild = context.do_build = True

        if not context.zimui_dist.exists():
            raise ValueError(
                f"zimui_dist directory {context.zimui_dist} does not exists"
            )

        self.curriculum_raw = context.build_folder / "curriculum-raw"
        self.curriculum_dist = context.build_folder / "curriculum-dist"

        # Make sure the output directory exists
        context.output_folder.mkdir(parents=True, exist_ok=True)
        context.build_folder.mkdir(parents=True, exist_ok=True)

        if context.language not in FCC_LANG_MAP:
            raise ValueError(f"Unsupported language {context.language}")
        self.fcc_lang = FCC_LANG_MAP[context.language]

        context.description, context.long_description = compute_descriptions(
            context.description, context.description, context.long_description
        )

        if context.main_zip_path and not context.main_zip_path.exists():
            raise ValueError(f"main zip file not found in {context.main_zip_path}")
        self.main_zip_path = (
            context.main_zip_path
            if context.main_zip_path
            else context.build_folder / "main.zip"
        )

        if context.i18n_zip_path and not context.i18n_zip_path.exists():
            raise ValueError(f"i18n zip file not found in {context.i18n_zip_path}")
        self.i18n_zip_path = (
            context.i18n_zip_path
            if context.i18n_zip_path
            else context.build_folder / "i18n.zip"
        )

        # if we do not build the ZIM, we can stop here
        if not context.do_build:
            return

        period = context.start_date.strftime("%Y-%m")
        if context.zim_file:
            self.zim_path = Path(context.zim_file.format(period=period))
            # make sure we were given a filename and not a path
            if Path(self.zim_path.name) != self.zim_path:
                raise ValueError(f"zim_name is not a filename: {context.zim_file}")
        else:
            self.zim_path = Path(f"{context.name}_{period}.zim")

        # build full path
        self.zim_path = context.output_folder / self.zim_path

        if self.zim_path.exists():
            if not (context.force or context.overwrite_existing_zim):
                raise ValueError(f"ZIM file {self.zim_path} already exist.")
            logger.info(f"Removing existing ZIM file {self.zim_path}")
            self.zim_path.unlink()
        else:
            logger.info(f"ZIM path: {self.zim_path}")

        if context.illustration:
            logo_path = handle_user_provided_file(context.illustration)
            if not logo_path:
                raise ValueError(f"Logo not found at {context.illustration}")
        else:
            logo_path = Path(__file__).parent.joinpath("assets", "fcc_48.png")
        if not logo_path.exists():
            raise ValueError(f"Logo not found at {logo_path}")

        illustration = io.BytesIO()
        illustration_format = format_for(logo_path, from_suffix=False)
        if illustration_format == "SVG":
            convert_svg2png(
                logo_path,
                illustration,
                metadata.DefaultIllustrationMetadata.illustration_size,
                metadata.DefaultIllustrationMetadata.illustration_size,
            )
        else:
            if illustration_format != "PNG":
                convert_image(logo_path, illustration, fmt="PNG")
            else:
                illustration = io.BytesIO(logo_path.read_bytes())
            resize_image(
                illustration,
                width=metadata.DefaultIllustrationMetadata.illustration_size,
                height=metadata.DefaultIllustrationMetadata.illustration_size,
                method="cover",
            )

        self.creator = Creator(self.zim_path, "index.html").config_metadata(
            std_metadata=metadata.StandardMetadataList(
                Name=metadata.NameMetadata(context.name),
                Language=metadata.LanguageMetadata(context.language),
                Title=metadata.TitleMetadata(context.title),
                Creator=metadata.CreatorMetadata(context.creator),
                Publisher=metadata.PublisherMetadata(context.publisher),
                Date=metadata.DateMetadata(context.start_date),
                Illustration_48x48_at_1=metadata.DefaultIllustrationMetadata(
                    illustration
                ),
                Description=metadata.DescriptionMetadata(context.description),
                LongDescription=(
                    metadata.LongDescriptionMetadata(context.long_description)
                    if context.long_description
                    else None
                ),
                Tags=metadata.TagsMetadata(["FCC", "freeCodeCamp"]),
                Scraper=metadata.ScraperMetadata(f"fcc2zim v{VERSION}"),
            )
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
                logger.error("KeyboardInterrupt, exiting.")
                raise SystemExit(3) from exc
            else:
                logger.error(f"Interrupting process due to error: {exc}")
                logger.exception(exc)
                raise SystemExit(2) from exc
        else:
            if self.creator:
                self.creator.finish()
                logger.info(f"Finished creating ZIM at {self.zim_path}")

    def run_commands(self):
        if context.do_fetch:
            fetch_command(
                force=context.force,
                curriculum_raw=self.curriculum_raw,
                zip_main_path=self.main_zip_path,
                zip_i18n_path=self.i18n_zip_path,
                fcc_lang=self.fcc_lang,
            )
        if context.do_prebuild:
            prebuild_command(
                fcc_lang=self.fcc_lang,
                course_list=context.course,
                curriculum_raw=self.curriculum_raw,
                curriculum_dist=self.curriculum_dist,
            )
        if context.do_build:
            build_command(
                creator=self.creator,
                zimui_dist=context.zimui_dist,
                curriculum_dist=self.curriculum_dist,
            )
