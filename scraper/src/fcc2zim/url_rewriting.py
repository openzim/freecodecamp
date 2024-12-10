# from zimscraperlib.rewriting.url_rewriting import (
#     ArticleUrlRewriter,
#     HttpUrl,
#     RewriteResult,
#     ZimPath,
# )

# from fcc2zim.asset import AssetManager


# class FccUrlsRewriter(ArticleUrlRewriter):
#     """A rewriter for HTML processing

#     This rewriter does not store items to download on-the-fly but has containers and
#     metadata so that HTML rewriting rules can decide what needs to be downloaded
#     """

#     def __init__(
#         self,
#         article_url: HttpUrl,
#         article_path: ZimPath,
#         existing_zim_paths: set[ZimPath],
#         asset_manager: AssetManager,
#     ):
#         super().__init__(
#             article_url=article_url,
#             article_path=article_path,
#             existing_zim_paths=existing_zim_paths,
#         )
#         self.asset_manager = asset_manager

#     def __call__(
#         self, item_url: str, base_href: str | None, *, rewrite_all_url: bool = True
#     ) -> RewriteResult:
#         result = super().__call__(item_url, base_href, rewrite_all_url=rewrite_all_url)
#         return result

#     def add_item_to_download(self, rewrite_result: RewriteResult, kind: str | None):
#         """Add item to download based on rewrite result"""
#         if rewrite_result.zim_path is None:
#             return
#         # if item is expected to be inside the ZIM, store asset information so that
#         # we can download it afterwards
#         self.asset_manager.add_asset(
#             asset_path=rewrite_result.zim_path,
#             asset_url=HttpUrl(rewrite_result.absolute_url),
#             used_by="foo",
#             kind=kind,
#             always_fetch_online=False,
#         )
