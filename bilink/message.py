import json
import sys
import time
from typing import Pattern, AnyStr

import httpx
import re

from bilink.models import Authorization, Api, Message
from bilink.utils.logger import Logger
from bilink.utils.tools import create_headers


class __BaseMatcher:
    ...


class Matcher(__BaseMatcher):
    """
    消息匹配规则
    """

    @classmethod
    def starts_with(cls, msg: str) -> bool:
        if Message.MsgContent.startswith(msg):
            return True
        else:
            return False

    @classmethod
    def ends_with(cls, msg: str) -> bool:
        if Message.MsgContent.endswith(msg):
            return True
        else:
            return False

    @classmethod
    def contains(cls, msg: str) -> bool:
        if msg in Message.MsgContent:
            return True
        else:
            return False

    @classmethod
    def regex(cls, pattern: Pattern[AnyStr], msg: str) -> bool:
        matched = re.findall(pattern, msg)
        if matched:
            return True
        else:
            return False


def is_new_msg():
    """
    判断是否有新的消息（且不是自己的消息
    """
    if Message.Timestamp != Message.LastTimestamp and Message.SenderUid != Authorization.SelfUid:
        Logger.message(f"用户[{Message.SenderUid}]:{Message.MsgContent}")
        return True
    else:
        return False


async def auto_reply(keywords: str, msg: str) -> None:
    """
    根据关键词自动回复一条消息
    """
    if is_new_msg() and Matcher.starts_with(keywords):
        await send_text_msg(
            msg,
            Message.SenderUid
        )


async def send_text_msg(msg: str, receiver_id: int) -> None:
    """
    发送文本消息
    """
    data = {
        'msg[sender_uid]': Authorization.SelfUid,
        'msg[receiver_id]': receiver_id,
        'msg[receiver_type]': 1,
        'msg[msg_type]': 1,
        'msg[msg_status]': 0,
        'msg[dev_id]': '00000000-0000-0000-0000-000000000000',
        'msg[timestamp]': int(time.time()),
        'csrf': Authorization.Token,
        'csrf_token': Authorization.Token,
        'msg[content]': '{"content": "%s"}' % msg,
        'msg[new_face_version]': 0,
        'from_firework': 0,
        'build': 0,
        'mobi_app': 'web'
    }
    try:
        async with httpx.AsyncClient() as client:
            client: httpx.AsyncClient
            res: httpx.Response = await client.post(
                url=Api.SEND_MSG,
                cookies=Authorization.Cookie,
                headers=create_headers(),
                data=data
            )
            if res.status_code == 200:
                if res.json().get('code') == 0:
                    Logger.message(f'me :{msg}')
                else:
                    Logger.error(res.json().__str__())
            else:
                Logger.error('Error: Sending message failed')
    except Exception as e:
        Logger.error(f"发生错误:{e}")
        sys.exit(-1)


async def fetch_msgs() -> None:
    """
    获取最新一条消息记录
    """
    try:
        async with httpx.AsyncClient() as client:
            client: httpx.AsyncClient
            res: httpx.Response = await client.get(
                url=Api.GET_SESSIONS,
                cookies=Authorization.Cookie,
                headers=create_headers(),
                timeout=None
            )
            string = res.json()
            session_list = string['data']['session_list']
            last_talker = session_list[0]
            last_msg = last_talker['last_msg']
            msg_json = json.loads(
                last_msg['content'].replace('\'', '\"')
            )
            Message.TalkerId = last_talker['talker_id']
            if msg_json.get('content'):
                Message.MsgContent = msg_json['content']
            elif msg_json.get('reply_content'):
                Message.MsgContent = msg_json['reply_content']
            else:
                Message.MsgContent = ''
            Message.Timestamp = last_msg['timestamp']
            Message.SenderUid = last_msg['sender_uid']
    except (httpx.HTTPError, httpx.ConnectError):
        Logger.error(f"网络错误，请关闭代理")
        sys.exit(-1)
    except Exception as e:
        Logger.error(f"发生错误:{e}")
        sys.exit(-1)
