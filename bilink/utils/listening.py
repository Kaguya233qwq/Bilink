import httpx
import json
import time
from bilink.utils.logger import Logger

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
                resp = httpx.get(url=url, cookies=cookies_, headers=headers)
                json_str = json.loads(resp.text)
                session_list = json_str['data']['session_list']
                last_talker = session_list[0]
                last_msg = last_talker['last_msg']
                msg_json = json.loads(last_msg['content'].replace('\'', '\"'))

                self.talker_id = last_talker['talker_id']
                self.msg_content = msg_json['content']
                self.timestamp = last_msg['timestamp']
                self.sender_uid = last_msg['sender_uid']
            except Exception as e:
                Logger.error(e)

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
    while True:
        bili = BiliMsg()
        if bili.get_timestamp() != current_msg and bili.get_sender_uid() != bili.SelfUid:
            Logger.message(bili.get_msg_content())
            if '你好' in bili.get_msg_content():
                content = '(*´▽｀)ノノ你好鸭~~'
                data = {
                    'msg[sender_uid]': str(bili.SelfUid),
                    'msg[receiver_id]': bili.get_talker_id(),
                    'msg[receiver_type]': 1,
                    'msg[msg_type]': 1,
                    'msg[msg_status]': 0,
                    'msg[dev_id]': '00000000-0000-0000-0000-000000000000',
                    'msg[timestamp]': int(time.time()),
                    'csrf': cookies_.get('bili_jct'),
                    'csrf_token': cookies_.get('bili_jct'),
                    'msg[content]': '{"content": "%s"}' % content,
                    'msg[new_face_version]': 0,
                    'from_firework': 0,
                    'build': 0,
                    'mobi_app': 'web'
                }
                response = httpx.post(
                    url=send,
                    cookies=cookies_,
                    headers=headers,
                    data=data
                )
                if response.status_code == 200:
                    Logger.auto(content)
        current_msg = bili.get_timestamp()
        time.sleep(2)
