import json
import time
import asyncio
from typing import Dict, Optional, List
import httpx
import qrcode  # type: ignore

from ..utils.models import Api, Authorization
from ..utils.logger import Logger
from ..utils.tools import create_headers, enc_wbi
from ..utils.exception import GetLoginQrcodeFailedError
from ..events.message import MessageEvent
from ..events.segment import MessageSegment
from ..core.session import MessageManager
from .client import BilibiliClient


class BilibiliApi:
    """Bilibili API封装"""

    def __init__(self, client_wrapper: BilibiliClient):
        self.client_wrapper = client_wrapper

    @property
    def client(self) -> httpx.AsyncClient:
        return self.client_wrapper.get_client()

    async def get_qrcode(self) -> Optional[Dict[str, str]]:
        """获取二维码"""
        resp = await self.client.get(
            url=Api.QRCODE_GENERATE,
            headers=create_headers(),
            follow_redirects=True,  # type: ignore
        )
        if resp.status_code == 200:
            qrcode_obj = resp.json()
            qrcode_url = str(qrcode_obj["data"]["url"])
            qrcode_key = str(qrcode_obj["data"]["qrcode_key"])
            return {"url": qrcode_url, "key": qrcode_key}
        else:
            raise GetLoginQrcodeFailedError()

    async def save_qrcode(self, url_qrcode: str) -> None:
        """保存二维码到本地并在终端输出"""
        qr_code = qrcode.QRCode(error_correction=1, box_size=1, border=2)
        qr_code.add_data(url_qrcode)
        qr_code.print_ascii(invert=True)
        img = qr_code.make_image()
        with open("qrCode.png", "wb") as f:
            img.save(f)  # type: ignore

    async def polling(self, qrcode_key: str) -> Optional[Dict[str, str]]:
        """轮询扫码状态"""
        while True:
            params = {"qrcode_key": qrcode_key}
            resp: httpx.Response = await self.client.get(
                url=Api.QRCODE_POLL,
                headers=create_headers(),  # type: ignore
                params=params,
                follow_redirects=True,
            )
            poll = json.loads(resp.text)
            state_code = poll["data"]["code"]
            message = poll["data"]["message"]
            if state_code == 0:
                Logger.success("登录成功！")
                sess_data = resp.cookies.get("SESSDATA")
                user_id = resp.cookies.get("DedeUserID")
                ck_md5 = resp.cookies.get("DedeUserID__ckMd5")
                bili_jct = resp.cookies.get("bili_jct")
                sid = resp.cookies.get("sid")
                cookies = {
                    "SESSDATA": str(sess_data),
                    "DedeUserID": str(user_id),
                    "bili_jct": str(bili_jct),
                    "DedeUserID__ckMd5": str(ck_md5),
                    "sid": str(sid),
                }
                return cookies
            elif state_code == 86038:
                Logger.warning(message)
                return None
            elif state_code == 86101:
                await asyncio.sleep(2)
            elif state_code == 86090:
                Logger.success("已扫码，请在手机上确认")
                await asyncio.sleep(2)
            else:
                Logger.error(message)
                return None

    async def login_by_qrcode(self) -> Optional[Dict[str, str]]:
        """通用bilibili扫码登录"""
        qr = await self.get_qrcode()
        if qr is None:
            return None
        await self.save_qrcode(qr.get("url", ""))
        Logger.success("二维码生成成功，请使用bilibili客户端扫描确认")
        return await self.polling(qr.get("key", ""))

    async def check_login_status(self) -> bool:
        """检查当前登录状态是否有效"""
        try:
            res = await self.client.get(
                url=Api.NAV,
                cookies=Authorization.Cookie,  # type: ignore
                headers=create_headers(),  # type: ignore
            )
            data = res.json()
            if data.get("code") == 0 and data.get("data", {}).get("isLogin"):
                return True
        except Exception as e:
            Logger.error(f"检查登录状态异常: {e}")
        return False

    async def check_unread_msgs(self) -> bool:
        """检查是否有未读消息"""
        try:
            params = {"unread_type": 0, "show_unfollow_list": 1}
            res = await self.client.get(
                url=Api.SINGLE_UNREAD,
                cookies=Authorization.Cookie,  # type: ignore
                headers=create_headers(),  # type: ignore
                params=params,
            )
            data = res.json()
            if data.get("code") == 0:
                unread_data = data.get("data", {})
                follow_unread = unread_data.get("follow_unread", 0)
                unfollow_unread = unread_data.get("unfollow_unread", 0)
                return (follow_unread + unfollow_unread) > 0
        except Exception as e:
            Logger.error(f"检查未读消息数异常: {e}")
        return True  # 异常时默认返回True放行拉取逻辑

    async def _send_raw_msg(
        self, receiver_id: int, msg_type: int, content: str
    ) -> None:
        """底层发送私信实现"""
        data = {
            "msg[sender_uid]": Authorization.SelfUid,
            "msg[receiver_id]": receiver_id,
            "msg[receiver_type]": 1,
            "msg[msg_type]": msg_type,
            "msg[msg_status]": 0,
            "msg[dev_id]": "00000000-0000-0000-0000-000000000000",
            "msg[timestamp]": int(time.time()),
            "csrf": Authorization.Token,
            "csrf_token": Authorization.Token,
            "msg[content]": content,
            "msg[new_face_version]": 0,
            "from_firework": 0,
            "build": 0,
            "mobi_app": "web",
        }
        try:
            res = await self.client.post(
                url=Api.SEND_MSG,
                cookies=Authorization.Cookie,  # type: ignore
                headers=create_headers(),  # type: ignore
                data=data,
            )
            if res.status_code == 200:
                if res.json().get("code") != 0:
                    Logger.error(str(res.json()))
            else:
                Logger.error("Error: Sending message failed")
        except Exception as e:
            Logger.error(f"发送消息失败:{e}")

    async def send_msg(self, msg: MessageSegment | str, receiver_id: int) -> None:
        """统一发送混合消息类型"""
        if isinstance(msg, str):
            msg = MessageSegment.text(msg)

        await self._send_raw_msg(receiver_id, msg.msg_type, msg.content_str)

        if msg.msg_type == 1:
            Logger.info(f"me :{msg.data.get('content')}")
        elif msg.msg_type == 2:
            Logger.info(f"me [图片]: {msg.data.get('url')}")
        elif msg.msg_type == 7:
            Logger.info(
                f"me [分享卡片]: {msg.data.get('title')}({msg.data.get('bvid')})"
            )
        else:
            Logger.info(f"me [MsgType={msg.msg_type}]:发送成功")

    async def fetch_msgs(self, manager: MessageManager) -> List[MessageEvent]:
        """获取最新的消息对象列表"""
        new_messages: List[MessageEvent] = []
        try:
            res = await self.client.get(
                url=Api.GET_SESSIONS,
                cookies=Authorization.Cookie,  # type: ignore
                headers=create_headers(),  # type: ignore
            )
            res_data = res.json()
            # print("Fetch res:", res_data)  # DEBUG
            if res_data.get("code") != 0:
                Logger.warning(f"获取消息响应异常: {res_data}")

            data_dict = res_data.get("data")
            if not data_dict:
                return new_messages

            session_list = data_dict.get("session_list", [])

            for session in session_list:
                if session.get("system_msg_type") != 0:
                    continue
                last_msg = session.get("last_msg")
                if not last_msg:
                    continue

                sender_uid = last_msg.get("sender_uid", 0)
                timestamp = last_msg.get("timestamp", 0)

                # 忽略来自自己的消息
                if sender_uid == Authorization.SelfUid:
                    continue

                if manager.check_is_new(sender_uid, timestamp):
                    msg_content = last_msg.get("content", "{}")
                    msg_json = json.loads(msg_content.replace("'", '"'))
                    message = MessageEvent(
                        sender_uid=sender_uid,
                        send_to_uid=session.get("talker_id", ""),
                        content=msg_json.get("content", ""),
                        timestamp=timestamp,
                    )
                    new_messages.append(message)
                    Logger.info(f"用户[{sender_uid}]: {message.Content}")

                manager.update_latest(sender_uid, timestamp)
        except Exception as e:
            Logger.error(f"获取消息失败: {e}")

        return new_messages

    async def get_user_info(self, mid: int) -> dict:
        """获取某个用户的信息"""
        try:
            params = {"mid": mid}
            res = await self.client.get(
                url=Api.USER_CARD,
                cookies=Authorization.Cookie,  # type: ignore
                headers=create_headers(),  # type: ignore
                params=params,
            )
            return res.json().get("data", {})
        except Exception as e:
            Logger.error(f"获取UID[{mid}]信息异常: {e}")
            return {}

    async def get_fans(self, vmid: int, pn: int = 1, ps: int = 50) -> dict:
        """获取目标用户的粉丝列表"""
        try:
            params = {"vmid": vmid, "pn": pn, "ps": ps}
            res = await self.client.get(
                url=Api.RELATION_FANS,
                cookies=Authorization.Cookie,  # type: ignore
                headers=create_headers(),  # type: ignore
                params=params,
            )
            # data.list 为粉丝列表
            return res.json().get("data", {})
        except Exception as e:
            Logger.error(f"获取粉丝列表异常: {e}")
            return {}

    async def get_fav_folders(self, up_mid: int) -> dict:
        """获取自己或指定用户所有的收藏夹列表"""
        try:
            params = {"up_mid": up_mid}
            res = await self.client.get(
                url=Api.FAV_FOLDERS,
                cookies=Authorization.Cookie,  # type: ignore
                headers=create_headers(),  # type: ignore
                params=params,
            )
            # data.list 为收藏夹对象数组
            return res.json().get("data", {})
        except Exception as e:
            Logger.error(f"获取收藏夹列表异常: {e}")
            return {}

    async def get_fav_folder_videos(
        self, media_id: int, pn: int = 1, ps: int = 20
    ) -> dict:
        """获取指定的收藏夹下视频列表"""
        try:
            params = {"media_id": media_id, "pn": pn, "ps": ps}
            res = await self.client.get(
                url=Api.FAV_RESOURCES,
                cookies=Authorization.Cookie,  # type: ignore
                headers=create_headers(),  # type: ignore
                params=params,
            )
            # data.medias 为视频稿件列表
            return res.json().get("data", {})
        except Exception as e:
            Logger.error(f"获取收藏夹视频列表异常: {e}")
            return {}

    async def get_video_download_url(self, bvid: str, cid: int, qn: int = 64) -> dict:
        """获取视频的真实流地址/下载地址(MP4/flv)"""
        try:
            params = {
                "bvid": bvid,
                "cid": cid,
                "qn": qn,  # 画质，默认64: 720P
                "fnval": 1,  # 1表示MP4格式，16为DASH
                "fnver": 0,
                "fourk": 0,
            }
            res = await self.client.get(
                url=Api.PLAY_URL,
                cookies=Authorization.Cookie,  # type: ignore
                headers=create_headers(),  # type: ignore
                params=params,
            )
            # data.durl[0].url 为下载链接
            return res.json().get("data", {})
        except Exception as e:
            Logger.error(f"获取视频下载流异常: {e}")
            return {}

    async def get_up_recent_videos(self, mid: int, pn: int = 1, ps: int = 10) -> list:
        """获取UP主最近的视频列表（通过 WBI 签名）"""
        try:
            # 获取 wbi 密钥
            nav_res = await self.client.get(
                url=Api.NAV,
                cookies=Authorization.Cookie,  # type: ignore
                headers=create_headers(),  # type: ignore
            )
            nav_data = nav_res.json()
            if nav_data.get("code") != 0:
                Logger.error(f"获取 nav 失败: {nav_data.get('message')}")
                return []

            wbi_img = nav_data.get("data", {}).get("wbi_img", {})
            img_url = wbi_img.get("img_url", "")
            sub_url = wbi_img.get("sub_url", "")
            if not img_url or not sub_url:
                Logger.error("未能找到 wbi_img 数据")
                return []

            img_key = img_url.split("/")[-1].split(".")[0]
            sub_key = sub_url.split("/")[-1].split(".")[0]

            # 构造并签名参数
            params = {"mid": mid, "pn": pn, "ps": ps}
            signed_params = enc_wbi(params, img_key, sub_key)

            # 发送带签名的请求
            headers = create_headers()
            headers["Referer"] = f"https://space.bilibili.com/{mid}/video"

            search_api = "https://api.bilibili.com/x/space/wbi/arc/search"
            res = await self.client.get(
                url=search_api,
                cookies=Authorization.Cookie,  # type: ignore
                headers=headers,  # type: ignore
                params=signed_params,
            )

            data = res.json()
            if data.get("code") == 0:
                vlist = data.get("data", {}).get("list", {}).get("vlist", [])
                return vlist
            else:
                Logger.error(
                    f"获取UP主视频失败: {data.get('message')} - {data.get('code')}"
                )
                return []
        except Exception as e:
            Logger.error(f"获取UP主视频列表异常: {e}")
            return []
