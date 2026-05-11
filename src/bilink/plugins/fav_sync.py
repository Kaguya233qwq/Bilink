from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

from ..core.handler import handler
from ..core.matcher import MatchType
from ..utils.logger import Logger
from ..utils.models import Authorization

if TYPE_CHECKING:
    from ..bot import Bot
    from ..connection.api import BilibiliApi

CACHE_FILE = Path("bilink_cache/download_history.json")
TARGET_FOLDER_NAME = "密藏之物品2"
NOTIFY_USER_UID = 32001059


def load_cache() -> set[str]:
    if not CACHE_FILE.exists():
        return set()
    try:
        return set(json.loads(CACHE_FILE.read_text("utf-8")))
    except Exception:
        return set()


def save_cache(cache: set[str]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(list(cache), ensure_ascii=False), "utf-8")


_cached_bvids: set[str] = load_cache()


def sanitize_filename(name: str) -> str:
    return "".join(c for c in name if c not in r'/:*?`"<>|')


async def get_folder_meta(
    api: BilibiliApi, uid: int, target_name: str
) -> tuple[int, str] | None:
    resp = await api.get_fav_folders(uid)
    folders = resp.get("list", [])
    if not folders:
        return None

    if target_name:
        for folder in folders:
            if folder.get("title") == target_name:
                return folder.get("id"), target_name

    return folders[0].get("id"), folders[0].get("title")


async def get_video_cid(client: httpx.AsyncClient, bvid: str) -> int | None:
    resp = await client.get(
        f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    if resp.status_code != 200:
        return None

    data = resp.json()
    if data.get("code") != 0:
        return None

    return data["data"]["cid"]


async def fetch_video_url(api: BilibiliApi, bvid: str) -> str | None:
    cid = await get_video_cid(api.client, bvid)
    if not cid:
        return None

    play_data = await api.get_video_download_url(bvid=bvid, cid=cid)
    durls = play_data.get("durl", [])
    if not durls:
        return None

    return durls[0]["url"]


async def download_video(url: str, output_path: Path) -> bool:
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as client:
        resp = await client.get(
            url,
            headers={
                "Referer": "https://www.bilibili.com",
                "User-Agent": "Mozilla/5.0",
            },
            timeout=300.0,
        )
        if resp.status_code != 200:
            return False

        output_path.write_bytes(resp.content)
        return True


@handler.register(MatchType.CRON, "* * * * *")
async def sync_favorites(bot: "Bot") -> None:
    uid = Authorization.SelfUid
    api = bot.api  # type: ignore

    try:
        meta = await get_folder_meta(api, uid, TARGET_FOLDER_NAME)
        if not meta:
            return

        target_media_id, resolved_folder_name = meta

        safe_folder_name = sanitize_filename(resolved_folder_name)
        save_dir = Path("Download") / str(uid) / safe_folder_name
        save_dir.mkdir(parents=True, exist_ok=True)

        fav_resp = await api.get_fav_folder_videos(
            media_id=target_media_id, pn=1, ps=10
        )
        medias = fav_resp.get("medias", [])

        for media in medias:
            bvid = media.get("bvid")
            title = media.get("title", "Unknown")

            if not bvid or bvid in _cached_bvids:
                continue

            Logger.info(f"Targeting: {title} ({bvid})")

            url = await fetch_video_url(api, bvid)
            if not url:
                Logger.warning(f"Failed resolving URL: {bvid}")
                continue

            safe_title = sanitize_filename(title)
            file_path = save_dir / f"{safe_title}_{bvid}.mp4"

            if await download_video(url, file_path):
                Logger.success(f"Downloaded: {safe_title}")
                if NOTIFY_USER_UID:
                    try:
                        await api.send_msg(
                            f"Downloaded: {safe_title}", receiver_id=NOTIFY_USER_UID
                        )
                    except Exception as e:
                        Logger.error(f"Notify failed: {e}")

                _cached_bvids.add(bvid)
                save_cache(_cached_bvids)
            else:
                Logger.error(f"Download failed HTTP: {bvid}")

    except Exception as e:
        Logger.error(f"Sync task error: {e}")
