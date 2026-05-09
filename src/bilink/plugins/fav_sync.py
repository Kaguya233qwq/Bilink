import json
from pathlib import Path
import httpx

from ..core.handler import handler
from ..core.matcher import MatchType
from ..utils.logger import Logger
from ..utils.models import Authorization

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Bot

# 使用持久化文件保存下载记录
CACHE_FILE = Path("bilink_cache/download_history.json")


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

# 在这里配置你的目标收藏夹名称
TARGET_FOLDER_NAME = "密藏之物品2"
# 配置接收推送通知的目标用户 UID 
# 如果不想接收私信通知，请保持为 0
NOTIFY_USER_UID = 32001059


@handler.register(MatchType.CRON, "* * * * *")
async def auto_sync_fav_job(bot: "Bot"):
    """
    改为 CRON 定时任务触发，每分钟自动执行一次。
    后台接管同步，不需要再发送任何指令。
    """
    uid = Authorization.SelfUid
    api = bot.api  # type: ignore

    try:
        folders_res = await api.get_fav_folders(uid)
        folder_list = folders_res.get("list", [])

        if not folder_list:
            return

        target_media_id = None
        target_folder_name = TARGET_FOLDER_NAME

        if target_folder_name:
            for folder in folder_list:
                if folder.get("title") == target_folder_name:
                    target_media_id = folder.get("id")
                    break
        else:
            # 默认取第一个
            target_media_id = folder_list[0].get("id")
            target_folder_name = folder_list[0].get("title")

        if not target_media_id:
            Logger.warning(f"CRON任务: 未找到名为【{target_folder_name}】的收藏夹！")
            return

        safe_folder_name = "".join(
            [c for c in target_folder_name if c not in r'\/:*?"<>|']
        )
        save_dir = Path(f"Download/{uid}/{safe_folder_name}")
        save_dir.mkdir(parents=True, exist_ok=True)

        fav_res = await api.get_fav_folder_videos(media_id=target_media_id, pn=1, ps=10)
        medias = fav_res.get("medias", [])

        for media in medias:
            bvid = media.get("bvid")
            title = media.get("title", "未知标题")

            if not bvid or bvid in _downloaded_cache:
                continue  # 已经下载过了或者无效视频

            # 避免系统不允许的非法文件名符号
            safe_title = "".join([c for c in title if c not in r'\/:*?"<>|'])

            Logger.info(f"CRON任务监测到新收藏视频，准备下载: {title} ({bvid})")

            view_res = await api.client.get(
                f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            view_data = view_res.json()

            if view_data.get("code") != 0:
                Logger.warning(f"获取视频详情失败: {bvid}")
                continue

            cid = view_data["data"]["cid"]

            # 获取 MP4 高清真实流下载地址
            play_data = await api.get_video_download_url(bvid=bvid, cid=cid)
            durl = play_data.get("durl", [])

            if not durl:
                Logger.warning(f"无法获取视频流下载地址，可能需要大会员或风控: {bvid}")
                continue

            video_download_url = durl[0]["url"]

            file_path = save_dir / f"{safe_title}_{bvid}.mp4"
            Logger.info(f"开始写入文件: {file_path}")

            async with httpx.AsyncClient(
                http2=True, follow_redirects=True
            ) as dl_client:
                dl_res = await dl_client.get(
                    video_download_url,
                    headers={
                        "Referer": "https://www.bilibili.com",
                        "User-Agent": "Mozilla/5.0",
                    },
                    timeout=300.0,  # MP4体积大，5分钟超时
                )

                if dl_res.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(dl_res.content)

                    msg_text = f"[自动任务] 收藏夹视频【{safe_title}】已下载入库！"
                    Logger.success(msg_text)
                    try:
                        if NOTIFY_USER_UID:
                            await api.send_msg(msg_text, receiver_id=NOTIFY_USER_UID)
                    except Exception as e:
                        Logger.error(f"消息推送失败: {e}")
                    # 加入缓存内存字典并持久化保存
                    _downloaded_cache.add(bvid)
                    save_download_cache(_downloaded_cache)
                else:
                    Logger.error(f"下载文件失败: HTTP {dl_res.status_code}")

    except Exception as e:
        Logger.error(f"收藏夹增量同步任务发生异常: {e}")
