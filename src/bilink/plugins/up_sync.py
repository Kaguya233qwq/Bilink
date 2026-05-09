import json
from pathlib import Path
import httpx

from ..core.handler import handler
from ..core.matcher import MatchType
from ..utils.logger import Logger

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Bot

# 使用独立的持久化文件保存 UP 主视频下载记录
CACHE_FILE = Path("bilink_cache/up_download_history.json")


def load_download_cache() -> set[str]:
    if CACHE_FILE.exists():
        try:
            return set(json.loads(CACHE_FILE.read_text("utf-8")))
        except Exception:
            pass
    return set()


def save_download_cache(cache: set[str]):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(list(cache), ensure_ascii=False), "utf-8")


_downloaded_cache: set[str] = load_download_cache()

# 配置要订阅监听的 UP主 UID 列表
TARGET_UP_MIDS = []
# 通知目标
NOTIFY_USER_UID = 32001059


@handler.register(MatchType.CRON, "* * * * *")
async def auto_sync_up_job(bot: "Bot"):
    """
    定时监听配置列表中的 UP主 的最近投稿视频
    如探测到新投稿视频，尝试解析并将其同步下载到本地，避免视频被删。
    """
    api = bot.api  # pyright: ignore[reportUndefinedVariable]
    if not TARGET_UP_MIDS:
        return

    try:
        for mid in TARGET_UP_MIDS:
            # 尝试获取 UP 主近期的视频内容
            vlist = await api.get_up_recent_videos(mid=mid, pn=1, ps=5)

            if not vlist:
                continue

            for video in vlist:
                bvid = video.get("bvid", "")
                title = video.get("title", "未知投稿")
                author = video.get("author", f"USER_{mid}")

                if not bvid or bvid in _downloaded_cache:
                    continue  # 已经下载过了

                safe_title = "".join([c for c in title if c not in r'\/:*?"<>|'])
                safe_author = "".join([c for c in author if c not in r'\/:*?"<>|'])

                Logger.info(
                    f"CRON任务: 侦测到 UP【{author}】发布新视频，准备下载: {title} ({bvid})"
                )

                save_dir = Path(f"Download/UP_{safe_author}_{mid}")
                save_dir.mkdir(parents=True, exist_ok=True)

                # 2. 我们需要在底层强行补个获取cid的请求
                view_res = await api.client.get(
                    f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                view_data = view_res.json()

                if view_data.get("code") != 0:
                    Logger.warning(f"获取视频详情失败: {bvid}")
                    continue

                cid = view_data["data"]["cid"]

                play_data = await api.get_video_download_url(bvid=bvid, cid=cid)
                durl = play_data.get("durl", [])

                if not durl:
                    Logger.warning(
                        f"无法获取下载地址，可能需要大会员或严重风控: {bvid}"
                    )
                    continue

                video_download_url = durl[0]["url"]
                file_path = save_dir / f"{safe_title}_{bvid}.mp4"

                async with httpx.AsyncClient(
                    http2=True, follow_redirects=True
                ) as dl_client:
                    dl_res = await dl_client.get(
                        video_download_url,
                        headers={
                            "Referer": "https://www.bilibili.com",
                            "User-Agent": "Mozilla/5.0",
                        },
                        timeout=300.0,
                    )

                    if dl_res.status_code == 200:
                        with open(file_path, "wb") as f:
                            f.write(dl_res.content)

                        msg_text = f"[自动任务] 成功为您下载 UP【{author}】的新视频:【{safe_title}】"
                        Logger.success(msg_text)
                        try:
                            if NOTIFY_USER_UID:
                                await api.send_msg(
                                    msg_text, receiver_id=NOTIFY_USER_UID
                                )
                        except Exception as e:
                            Logger.error(f"消息推送失败: {e}")

                        # 加入缓存并保存持久化
                        _downloaded_cache.add(bvid)
                        save_download_cache(_downloaded_cache)
                    else:
                        Logger.error(f"下载文件失败: HTTP {dl_res.status_code}")

    except Exception as e:
        Logger.error(f"UP主更新监听同步任务发生异常: {e}")
