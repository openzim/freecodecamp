import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from fcc2zim.scraper import Scraper

DEFAULT_START_DATE = datetime.date.fromisoformat("2023-08-23")
WORKING_DIR = TemporaryDirectory(prefix="fcc2zim_tests_")
WORKING_DIR_PATH = Path(WORKING_DIR.name)
ZIMUI_DIST_PATH = WORKING_DIR_PATH.joinpath("zimui/dist")
ZIMUI_DIST_PATH.mkdir(parents=True, exist_ok=True)
BUILD_PATH = WORKING_DIR_PATH.joinpath("build")
OUTPUT_PATH = WORKING_DIR_PATH.joinpath("output")

LONG_TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua. At erat pellentesque adipiscing "
    "commodo elit at imperdiet. Rutrum tellus pellentesque eu tincidunt tortor aliquam"
    " nulla facilisi. Eget lorem dolor sed viverra ipsum nunc. Ipsum nunc aliquet "
    "bibendum enim facilisis gravida neque convallis. Aliquam malesuada bibendum arcu "
    "vitae elementum curabitur. Platea dictumst quisque sagittis purus sit amet "
    "volutpat. Blandit libero volutpat sed cras ornare. In eu mi bibendum neque "
    "egestas. Egestas dui id ornare arcu odio. Pulvinar neque laoreet suspendisse "
    "interdum. Fames ac turpis egestas integer eget aliquet nibh praesent tristique. Et"
    " egestas quis ipsum suspendisse ultrices gravida dictum fusce. Malesuada fames ac "
    "turpis egestas. Tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada "
    "proin libero. In arcu cursus euismod quis viverra. Faucibus in ornare quam viverra"
    ". Curabitur vitae nunc sed velit dignissim sodales ut eu sem. Velit scelerisque in"
    " dictum non consectetur a erat nam. Proin fermentum leo vel orci porta non. Fames"
    " ac turpis egestas sed tempus. Vitae justo eget magna fermentum iaculis eu non. "
    "Imperdiet massa tincidunt nunc pulvinar sapien et ligula. Laoreet sit amet cursus "
    "sit amet dictum sit amet. Quis hendrerit dolor magna eget. Orci ac auctor augue "
    "mauris augue. Consequat interdum varius sit amet mattis. At ultrices mi tempus "
    "imperdiet nulla malesuada pellentesque elit. Volutpat est velit egestas dui. "
    "Potenti nullam ac tortor vitae. At tempor commodo ullamcorper a lacus vestibulum "
    "sed arcu non. Duis ut diam quam nulla. Vestibulum mattis ullamcorper velit sed "
    "ullamcorper. Sit amet commodo nulla facilisi nullam vehicula. Faucibus purus in "
    "massa tempor nec feugiat. Sem fringilla ut morbi tincidunt augue interdum velit. "
    "Etiam dignissim diam quis enim lobortis scelerisque fermentum dui. Nunc vel risus "
    "commodo viverra maecenas accumsan. Aenean sed adipiscing diam donec adipiscing "
    "tristique. Maecenas accumsan lacus vel facilisis volutpat est velit egestas. Nulla"
    " aliquet porttitor lacus luctus accumsan tortor posuere ac. Habitant morbi "
    "tristique senectus et netus et. Eget mi proin sed libero enim sed faucibus turpis "
    "in. Vulputate enim nulla aliquet porttitor lacus. Dui ut ornare lectus sit amet "
    "est. Quam lacus suspendisse faucibus interdum posuere. Sagittis orci a scelerisque"
    " purus semper eget duis at tellus. Tellus molestie nunc non blandit massa. Feugiat"
    " vivamus at augue eget arcu dictum varius duis at. Varius morbi enim nunc faucibus"
    " a pellentesque sit. Id aliquet lectus proin nibh nisl condimentum id venenatis a."
    " Tortor dignissim convallis aenean et tortor at risus viverra adipiscing. Aliquam "
    "malesuada bibendum arcu vitae elementum curabitur vitae nunc sed. Habitasse platea"
    " dictumst quisque sagittis purus sit amet volutpat. Vitae auctor eu augue ut "
    "lectus. At varius vel pharetra vel turpis nunc eget. Dictum at tempor  commodo "
    "ullamcorper a lacus vestibulum sed arcu. Pellentesque massa placerat duis "
    "ultricies. Enim nunc faucibus a pellentesque sit amet porttitor eget dolor. "
    "Volutpat blandit aliquam etiam erat velit scelerisque in. Amet mattis vulputate "
    "enim nulla aliquet porttitor. Egestas maecenas pharetra convallis posuere morbi "
    "leo urna molestie. Duis ut diam quam nulla porttitor massa id. In fermentum "
    "posuere urna nec tincidunt praesent. Turpis egestas sed tempus urna et pharetra "
    "pharetra massa. Tellus molestie nunc non blandit massa. Diam phasellus vestibulum "
    "lorem sed risus ultricies. Egestas erat imperdiet sed euismod nisi porta lorem. "
    "Quam viverra orci sagittis eu volutpat odio facilisis mauris sit. Ornare aenean "
    "euismod elementum nisi quis. Laoreet non curabitur gravida arcu ac tortor "
    "dignissim convallis aenean. Sagittis aliquam malesuada bibendum arcu vitae "
    "elementum. Sed blandit libero volutpat sed cras ornare. Sagittis eu volutpat odio "
    "facilisis mauris. Facilisis volutpat est velit egestas dui id ornare arcu odio. "
    "Eu feugiat pretium  nibh."
)


class TestScraper:
    def create_scraper(
        self,
        *,
        do_fetch: bool = True,
        do_prebuild: bool = True,
        do_build: bool = True,
        zimui_dist: str = str(ZIMUI_DIST_PATH),
        output: str = str(OUTPUT_PATH),
        build: str = str(BUILD_PATH),
        language: str = "eng",
        name="fcc_en_javascript",
        title="freeCodeCamp Javascript",
        description="FCC Javascript Courses",
        long_description: str | None = None,
        content_creator: str = "freeCodeCamp",
        publisher="openZIM",
        zim_file: str | None = None,
        force: bool = False,
        course_csv="regular-expressions,basic-javascript",
        zip_path: str | None = None,
        start_date: datetime.date = DEFAULT_START_DATE,
    ):
        return Scraper(
            do_fetch=do_fetch,
            do_prebuild=do_prebuild,
            do_build=do_build,
            zimui_dist=zimui_dist,
            output=output,
            build=build,
            language=language,
            name=name,
            title=title,
            description=description,
            long_description=long_description,
            content_creator=content_creator,
            publisher=publisher,
            zim_file=zim_file,
            force=force,
            course_csv=course_csv,
            zip_path=zip_path,
            start_date=start_date,
        )

    def test_init_ok(self):
        assert not OUTPUT_PATH.exists()
        assert not BUILD_PATH.exists()
        self.create_scraper()
        assert OUTPUT_PATH.exists()
        assert BUILD_PATH.exists()

    @pytest.mark.parametrize(
        "do_fetch, do_prebuild, do_build, expected_do_fetch, expected_do_prebuild,"
        "expected_do_build",
        [
            pytest.param(False, False, False, True, True, True, id="FFF"),
            pytest.param(True, False, False, True, False, False, id="TFF"),
            pytest.param(False, True, False, False, True, False, id="FTF"),
            pytest.param(True, True, False, True, True, False, id="TTF"),
            pytest.param(False, False, True, False, False, True, id="FFT"),
            pytest.param(True, False, True, True, False, True, id="TFT"),
            pytest.param(False, True, True, False, True, True, id="FTT"),
            pytest.param(True, True, True, True, True, True, id="TTT"),
        ],
    )
    def test_do_phases_ok(
        self,
        *,
        do_fetch: bool,
        do_prebuild: bool,
        do_build: bool,
        expected_do_fetch: bool,
        expected_do_prebuild: bool,
        expected_do_build: bool,
    ):
        scraper = self.create_scraper(
            do_fetch=do_fetch, do_prebuild=do_prebuild, do_build=do_build
        )
        assert scraper.do_fetch == expected_do_fetch
        assert scraper.do_prebuild == expected_do_prebuild
        assert scraper.do_build == expected_do_build

    def test_zimui_dist_ko(self):
        with pytest.raises(ValueError):
            self.create_scraper(zimui_dist="whatever")

    @pytest.mark.parametrize(
        "language, expected_fcc_lang",
        [
            pytest.param("eng", "english", id="english"),
            pytest.param("eng", "english", id="english"),
            pytest.param("ara", "arabic", id="arabic"),
            pytest.param("cmn", "chinese", id="chinese"),
            pytest.param("lzh", "chinese-traditional", id="chinese-traditional"),
            pytest.param("eng", "english", id="english"),
            pytest.param("spa", "espanol", id="espanol"),
            pytest.param("deu", "german", id="german"),
            pytest.param("ita", "italian", id="italian"),
            pytest.param("jpn", "japanese", id="japanese"),
            pytest.param("por", "portuguese", id="portuguese"),
            pytest.param("ukr", "ukranian", id="ukranian"),
        ],
    )
    def test_fcc_lang_ok(self, language: str, expected_fcc_lang: str):
        scraper = self.create_scraper(language=language)
        assert scraper.language == language
        assert scraper.fcc_lang == expected_fcc_lang

    def test_language_ko(self):
        with pytest.raises(ValueError):
            self.create_scraper(language="whatever")

    def test_description_ko(self):
        with pytest.raises(ValueError):
            self.create_scraper(description=LONG_TEXT[:81])

    def test_long_description_ko(self):
        with pytest.raises(ValueError):
            self.create_scraper(long_description=LONG_TEXT[:4001])

    def test_title_ko(self):
        with pytest.raises(ValueError):
            self.create_scraper(title=LONG_TEXT[:31])

    def test_zip_path_ok(self):
        with NamedTemporaryFile(dir=WORKING_DIR_PATH) as tmp:
            zip_path = tmp.name
            self.create_scraper(zip_path=zip_path)

    def test_zip_path_ko(self):
        with pytest.raises(ValueError):
            self.create_scraper(zip_path="whatever")

    @pytest.mark.parametrize(
        "name, start_date",
        [
            pytest.param("something", "2023-08-23", id="case1"),
            pytest.param("name2", "2023-08-24", id="case2"),
        ],
    )
    def test_zim_file_default(self, name, start_date):
        scraper = self.create_scraper(
            name=name, start_date=datetime.date.fromisoformat(start_date)
        )
        assert scraper.zim_path == OUTPUT_PATH.joinpath(f"{name}_{start_date[:7]}.zim")

    def test_zim_file_is_path_ko(self):
        with pytest.raises(ValueError):
            self.create_scraper(zim_file=str(OUTPUT_PATH.joinpath("whatever.zim")))

    def test_zim_file_ok(self):
        self.create_scraper(zim_file="whatever.zim")

    def test_zim_file_exists_ko(self):
        with NamedTemporaryFile(dir=OUTPUT_PATH, suffix=".zim") as tmp:
            zim_file = Path(tmp.name).name
            with pytest.raises(ValueError):
                self.create_scraper(zim_file=zim_file)

    def test_zim_file_exists_force(self):
        with NamedTemporaryFile(dir=OUTPUT_PATH, suffix=".zim", delete=False) as tmp:
            zim_file = Path(tmp.name).name
            self.create_scraper(zim_file=zim_file, force=True)
            assert not Path(tmp.name).exists()
