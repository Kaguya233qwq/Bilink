import sys
import httpx
import json
import time
from .logger import Logger
from ..api import message

url = 'https://api.vc.bilibili.com/session_svr/v1/session_svr/get_sessions?session_type=1'
urls = 'https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs'
send = 'https://api.vc.bilibili.com/web_im/v1/web_im/send_msg'
new = 'https://api.vc.bilibili.com/session_svr/v1/session_svr/new_sessions?begin_ts=1668417681186054&build=0&mobi_app=web'
headers = {
    'authority': 'api.vc.bilibili.com',
    'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://message.bilibili.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://message.bilibili.com/',
    'accept-language': 'zh-CN,zh;q=0.9'
}


def run(cookies_: json):
    class BiliMsg:
        talker_id = ''
        msg_content = ''
        timestamp = ''
        sender_uid = ''
        SelfUid = int(cookies_.get('DedeUserID'))

        def get(self):
            try:
                resp = httpx.get(
                    url=url,
                    cookies=cookies_,
                    headers=headers,
                    timeout=None
                )
                json_str = json.loads(resp.text)
                session_list = json_str['data']['session_list']
                last_talker = session_list[0]
                last_msg = last_talker['last_msg']
                msg_json = json.loads(last_msg['content'].replace('\'', '\"'))

                self.talker_id = last_talker['talker_id']
                if msg_json.get('content'):
                    self.msg_content = msg_json['content']
                elif msg_json.get('reply_content'):
                    self.msg_content = msg_json['reply_content']
                else:
                    self.msg_content = ''
                self.timestamp = last_msg['timestamp']
                self.sender_uid = last_msg['sender_uid']
            except Exception as e:
                Logger.error(f"cookie已失效，请重新登录:{e}")

        def get_talker_id(self):
            self.get()
            return self.talker_id

        def get_msg_content(self):
            self.get()
            return self.msg_content

        def get_timestamp(self):
            self.get()
            return self.timestamp

        def get_sender_uid(self):
            self.get()
            return self.sender_uid

    current_msg = BiliMsg().get_timestamp()
    Logger.info("bilibili消息助手正在运行...\033[0m")
    try:
        while True:
            bili = BiliMsg()
            if bili.get_timestamp() != current_msg and bili.get_sender_uid() != bili.SelfUid:
                msg = bili.get_msg_content()
                sender = bili.get_sender_uid()
                Logger.message(f"用户[{sender}]:{msg}")
                if '你好' in msg:
                    message.send_text('(*´▽｀)ノノ你好鸭~~')
            current_msg = bili.get_timestamp()
            time.sleep(2)
    except KeyboardInterrupt:
        Logger.info('进程终止')
        sys.exit()
