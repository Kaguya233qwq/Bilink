import time

from bilink.utils.cookies import Cookies


def send_text(msg: str) -> None:
    cookies_ = Cookies()
    content = msg
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
