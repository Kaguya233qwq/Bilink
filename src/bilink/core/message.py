import json
import time

import httpx

from ..utils.models import Authorization, Api
from ..utils.logger import Logger
from ..utils.tools import create_headers


class Message:
    """消息体对象"""

    def __init__(
        self,
        sender_uid: int = 0,
        send_to_uid: str = "",
        content: str = "",
        timestamp: int = 0,
    ):
        self.SenderUID: int = sender_uid
        """发送人的uid"""

        self.SendToUID: str = send_to_uid
        """发送目标用户的uid"""

        self.Content: str = content
        """消息内容"""

        self.Timestamp: int = timestamp
        """时间戳"""

    def is_new_msg(self) -> bool:
        """
        判断是否为新消息且不是bot自己的消息
        """
        check = (
            message_manager.get_latest_msg().Timestamp != self.Timestamp
            and Authorization.SelfUid != self.SenderUID
        )
        if check:
            # 如果判断为最新一条消息则需要更新最新消息
            message_manager.update_latest_msg(self)
        return check


class MessageManager:
    """消息管理器"""

    def __init__(self):
        self.latest_msg: Message = Message()

    def is_empty(self):
        return self.latest_msg.Timestamp == 0 and self.latest_msg.SenderUID == 0

    def update_latest_msg(self, message: Message) -> None:
        """更新最新消息"""
        self.latest_msg = message

    def get_latest_msg(self) -> Message:
        """获取最新的消息"""
        return self.latest_msg


message_manager = MessageManager()


# async def auto_reply(keywords: str, msg: str) -> None:
#     """
#     根据关键词自动回复一条消息
#     """
#     matcher = Matcher(latest_msg)
#     if matcher.is_new_msg() and matcher.starts_with(keywords):
#         Logger.info(f"用户[{Message.SenderUID}]:{Message.Content}")
#         await send_text_msg(msg, Message.SenderUID)


async def send_text_msg(msg: str, receiver_id: int) -> None:
    """
    发送文本消息
    """
    data = {
        "msg[sender_uid]": Authorization.SelfUid,
        "msg[receiver_id]": receiver_id,
        "msg[receiver_type]": 1,
        "msg[msg_type]": 1,
        "msg[msg_status]": 0,
        "msg[dev_id]": "00000000-0000-0000-0000-000000000000",
        "msg[timestamp]": int(time.time()),
        "csrf": Authorization.Token,
        "csrf_token": Authorization.Token,
        "msg[content]": json.dumps({"content": msg}),
        "msg[new_face_version]": 0,
        "from_firework": 0,
        "build": 0,
        "mobi_app": "web",
    }
    try:
        async with httpx.AsyncClient() as client:
            client: httpx.AsyncClient
            res: httpx.Response = await client.post(
                url=Api.SEND_MSG,
                cookies=Authorization.Cookie,
                headers=create_headers(),
                data=data,
            )
            if res.status_code == 200:
                if res.json().get("code") == 0:
                    Logger.info(f"me :{msg}")
                else:
                    Logger.error(str(res.json()))
            else:
                Logger.error("Error: Sending message failed")
    except Exception as e:
        Logger.error(f"发送消息失败:{e}")


async def fetch_msg() -> Message:
    """
    获取最新的消息对象
    """

    async with httpx.AsyncClient() as client:
        client: httpx.AsyncClient
        res: httpx.Response = await client.get(
            url=Api.GET_SESSIONS,
            cookies=Authorization.Cookie,
            headers=create_headers(),
            timeout=None,
        )
        string = res.json()
        session_list = string["data"]["session_list"]
        last_talker = session_list[0]
        last_msg = last_talker["last_msg"]
        msg_json = json.loads(last_msg["content"].replace("'", '"'))
        message = Message(
            sender_uid=last_msg.get("sender_uid", 0),
            send_to_uid=last_talker.get("talker_id", ""),
            content=msg_json.get("content", ""),
            timestamp=last_msg.get("timestamp", 0),
        )
        if message_manager.is_empty():
            message_manager.update_latest_msg(message)
        return message
