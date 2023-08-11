import json
import sys
import time
import httpx

from bilink.models import Authorization, Api, Message
from bilink.utils.logger import Logger
from bilink.utils.tools import headers


async def send_text_msg(msg: str, receiver_id: str) -> None:
    """
    发送文本消息
    """
    data = {
        'msg[sender_uid]': str(Authorization.SelfUid),
        'msg[receiver_id]': receiver_id,
        'msg[receiver_type]': 1,
        'msg[msg_type]': 1,
        'msg[msg_status]': 0,
        'msg[dev_id]': '00000000-0000-0000-0000-000000000000',
        'msg[timestamp]': time.time(),
        'csrf': Authorization.Token,
        'csrf_token': Authorization.Token,
        'msg[content]': '{"content": "%s"}' % msg,
        'msg[new_face_version]': 0,
        'from_firework': 0,
        'build': 0,
        'mobi_app': 'web'
    }
    async with httpx.AsyncClient as client:
        client: httpx.AsyncClient
        response: httpx.Response = await client.post(
            url=Api.SEND_MSG,
            cookies=Authorization.Cookie,
            headers=headers,
            data=data
        )
        if response.status_code == 200:
            Logger.message(f'me :{msg}')
        else:
            Logger.error('Error: Sending message failed')


async def fetch_msgs() -> None:
    """
    获取最新一条消息记录
    """
    try:
        async with httpx.AsyncClient as client:
            client: httpx.AsyncClient
            res: httpx.Response = await client.post(
                url=Api.GET_SESSIONS,
                cookies=Authorization.Cookie,
                headers=headers,
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
    except Exception as e:
        Logger.error(f"cookie已失效，请重新登录:{e}")
        sys.exit(-1)
