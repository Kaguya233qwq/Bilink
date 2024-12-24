import json
import sys
import time
from typing import Pattern, AnyStr

import httpx
import re

from .models import Authorization, Api, Message
from .utils.logger import Logger
from .utils.tools import create_headers

latest_msg = Message()


class Matcher:
    """
    消息匹配器
    """

    def __init__(self, message: Message):
        self.message = message

    def starts_with(self, content: str) -> bool:
        """如果消息以指定内容开头时"""
        if self.message.Content.startswith(content):
            return True
        else:
            return False

    def ends_with(self, content: str) -> bool:
        """如果消息以指定内容结尾时"""
        if self.message.Content.endswith(content):
            return True
        else:
            return False

    def contains(self, content: str) -> bool:
        """如果消息内容中包含指定内容时"""
        if content in self.message.Content:
            return True
        else:
            return False

    def send_by_user(self, user_id: str) -> bool:
        """如果发送人为指定用户时"""
        if self.message.SenderUID == user_id:
            return True
        else:
            return False

    def regex(self, pattern: Pattern[AnyStr]) -> bool:
        """如果消息匹配指定正则表达式"""
        matched = re.findall(pattern, self.message.Content)
        if matched:
            return True
        else:
            return False

    def is_new_msg(self) -> bool:
        """
        判断如果为新消息且不是bot自己的消息
        """
        if (
            latest_msg.Timestamp != self.message.Timestamp
            and latest_msg.SenderUID != self.message.SenderUID
            and Authorization.SelfUid != self.message.SenderUID
        ):
            return True
        else:
            return False


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
        "msg[content]": '{"content": "%s"}' % msg,
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
        return Message(
            sender_uid=last_msg.get("sender_uid", 0),
            send_to_uid=last_talker.get("talker_id", ""),
            content=msg_json.get("content", ""),
            timestamp=last_msg.get("timestamp", 0),
        )
