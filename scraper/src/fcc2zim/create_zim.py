from pathlib import Path
from urllib.parse import quote, urlsplit

from jinja2 import Environment, PackageLoader
from zimscraperlib.rewriting.css import CssRewriter
from zimscraperlib.rewriting.html import HtmlRewriter
from zimscraperlib.rewriting.js import JsRewriter
from zimscraperlib.rewriting.url_rewriting import ArticleUrlRewriter, HttpUrl, ZimPath
from zimscraperlib.zim import Creator

from fcc2zim.constants import Global

logger = Global.logger

ZIM_NAME = "tests_eng_fcc-from-src"
ZIM_PATH = Path(
    f"/home/benoit/Repos/openzim/freecodecamp/scraper/output/{ZIM_NAME}.zim"
)

DIST_DIR = Path("/home/benoit/Repos/freeCodeCamp/freeCodeCamp/dist")


def process_html_file(creator: Creator, file: Path, rel_path: str):
    orig_url = f"https://{rel_path}"
    zim_path = ArticleUrlRewriter.normalize(HttpUrl(orig_url))


def main():
    if ZIM_PATH.exists():
        logger.info("Removing existing ZIM")
        ZIM_PATH.unlink()

    expected_zim_items: set[ZimPath] = set()

    js_modules: set[ZimPath] = set()

    def notify_js_modules(zim_path: ZimPath):
        logger.info(f"JS Module found: {zim_path.value}")
        js_modules.add(zim_path)

    for file in DIST_DIR.rglob("*"):
        if not file.is_file():
            continue

        rel_path = str(file.relative_to(DIST_DIR))
        rel_path = (
            rel_path[:-11]
            if rel_path.startswith("www.freecodecamp.org") and file.name == "index.html"
            else rel_path
        )

        item_url = HttpUrl(f"https://{rel_path}")
        expected_zim_items.add(ArticleUrlRewriter.normalize(item_url))

    logger.info(f"{len(expected_zim_items)} entries expected")

    # autoescape=False to allow injecting html entities from translated text
    env = Environment(
        loader=PackageLoader("fcc2zim", "templates"),
        autoescape=False,  # noqa: S701
    )

    env.filters["urlsplit"] = urlsplit
    env.filters["tobool"] = lambda val: "true" if val else "false"

    pre_head_template = env.get_template("head_insert.html")

    with Creator(ZIM_PATH, "www.freecodecamp.org").config_dev_metadata() as creator:
        creator.add_item_for(
            path="localhost/user/get-session-user",
            content="{}",
            mimetype="application/json",
        )

        for file in DIST_DIR.rglob("*"):
            if not file.is_file():
                continue

            rel_path = str(file.relative_to(DIST_DIR))
            rel_path = (
                rel_path[:-11]
                if rel_path.startswith("www.freecodecamp.org")
                and file.name == "index.html"
                else rel_path
            )

            # add _zim_static files as-is
            if rel_path.startswith("_zim_static"):
                creator.add_item_for(
                    fpath=file,
                    path=rel_path,
                )
                continue

            # we are now processing only www.freecodecamp.org files
            # if file.suffix != ".html":
            #     continue

            # ignore courses for now, we want index to work first
            if rel_path.startswith("www.freecodecamp.org/learn") and not rel_path in [
                "www.freecodecamp.org/learn",
                "www.freecodecamp.org/learn/data-visualization",
                "www.freecodecamp.org/learn/data-visualization/data-visualization-with-d3",
                "www.freecodecamp.org/learn/data-visualization/data-visualization-with-d3/work-with-data-in-d3",
            ]:
                continue

            item_url = HttpUrl(f"https://{rel_path}")
            item_path = ArticleUrlRewriter.normalize(item_url)
            url_rewriter = ArticleUrlRewriter(
                article_url=item_url,
                article_path=item_path,
                existing_zim_paths=expected_zim_items,
            )

            if file.suffix == ".html":
                orig_url = urlsplit(item_url.value)
                rel_static_prefix = url_rewriter.get_document_uri(
                    ZimPath("_zim_static/"), ""
                )

                html_rewriter = HtmlRewriter(
                    url_rewriter=url_rewriter,
                    pre_head_insert=pre_head_template.render(
                        path=quote(item_path.value),
                        static_prefix=rel_static_prefix,
                        orig_url=item_url.value,
                        orig_scheme=orig_url.scheme,
                        orig_host=orig_url.netloc,
                    ),
                    post_head_insert=None,
                    notify_js_module=notify_js_modules,
                )

                creator.add_item_for(
                    content=html_rewriter.rewrite(file.read_text()).content,
                    path=rel_path,
                    mimetype="text/html",
                )

            elif file.suffix == ".css":
                css_rewriter = CssRewriter(url_rewriter=url_rewriter, base_href=None)
                creator.add_item_for(
                    content=css_rewriter.rewrite(file.read_text()),
                    path=rel_path,
                    mimetype="text/css",
                )

            elif file.suffix == ".js":
                js_rewriter = JsRewriter(
                    url_rewriter=url_rewriter,
                    base_href=None,
                    notify_js_module=notify_js_modules,
                )
                creator.add_item_for(
                    content=js_rewriter.rewrite(file.read_text(encoding="utf-8"))
                    .replace('____wb_rewrite_import__("", ...)', "import(...)")
                    .replace('____wb_rewrite_import__("", )', "import()")
                    .replace("_____WB$wombat$check$this$function_____(this)", "this"),
                    path=rel_path,
                    mimetype="application/javascript; charset=utf-8",
                )

            else:
                creator.add_item_for(
                    fpath=file,
                    path=rel_path,
                )
