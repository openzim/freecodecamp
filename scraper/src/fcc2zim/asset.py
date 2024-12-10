# from typing import NamedTuple

# from zimscraperlib.rewriting.url_rewriting import HttpUrl, ZimPath

# from fcc2zim.constants import Global

# logger = Global.logger


# class AssetDetails(NamedTuple):
#     asset_urls: set[HttpUrl]
#     used_by: set[str]
#     always_fetch_online: bool
#     kind: str | None

#     @property
#     def get_usage_repr(self) -> str:
#         """Returns a representation of asset usage, typically for logs"""
#         if len(self.used_by) == 0:
#             return ""
#         return f' used by {", ".join(self.used_by)}'


# class AssetManager:
#     """Class responsible to manage a list of assets to download"""

#     def __init__(self) -> None:
#         self.assets: dict[ZimPath, AssetDetails] = {}

#     def add_asset(
#         self,
#         asset_path: ZimPath,
#         asset_url: HttpUrl,
#         used_by: str,
#         kind: str | None,
#         *,
#         always_fetch_online: bool,
#     ):
#         """Add a new asset to download

#         asset_path: target path inside the ZIM
#         asset_url: URL where the asset can be downloaded
#         used_by: string explaining (mostly for debug purposes) where the asset is used
#           (typically on which page)
#         kind: kind of asset if we know it ; for instance "img" is used to not rely only
#           on returned mime type to decide if we should optimize it or not
#         always_fetch_online: if False, the asset may be cached on S3 ; if True, it is
#           always fetch online
#         """
#         if asset_path not in self.assets:
#             self.assets[asset_path] = AssetDetails(
#                 asset_urls={asset_url},
#                 used_by={used_by},
#                 kind=kind,
#                 always_fetch_online=always_fetch_online,
#             )
#             return
#         current_asset = self.assets[asset_path]
#         if current_asset.kind != kind:
#             logger.warning(
#                 f"Conflicting kind found for asset at {asset_path} already used by "
#                 f"{current_asset.get_usage_repr}; current kind is "
#                 f"'{current_asset.kind}';new kind '{kind}' from {asset_url} used by "
#                 f"{used_by} will be ignored"
#             )
#         if current_asset.always_fetch_online != always_fetch_online:
#             logger.warning(
#                 f"Conflicting always_fetch_online found for asset at {asset_path} "
#                 f"already used by {current_asset.get_usage_repr}; current "
#                 f"always_fetch_online is '{current_asset.always_fetch_online}';"
#                 f"new always_fetch_online '{always_fetch_online}' from {asset_url} used"
#                 f" by {used_by} will be ignored"
#             )
#         current_asset.used_by.add(used_by)
#         current_asset.asset_urls.add(asset_url)
