from plistlib import Dict

HOST = 'https://api.vc.bilibili.com'
LOGIN = 'http://passport.bilibili.com/x/passport-login'


class Api:
    GET_SESSIONS = f'{HOST}/session_svr/v1/session_svr/get_sessions'
    '?session_type=1'
    FETCH_SESSION_MSGS = f'{HOST}/svr_sync/v1/svr_sync/fetch_session_msgs'
    SEND_MSG = f'{HOST}/web_im/v1/web_im/send_msg'
    NEW_SESSIONS = f'{HOST}/session_svr/v1/session_svr/new_sessions'
    '?begin_ts=1668417681186054&build=0&mobi_app=web'

    QRCODE_GENERATE = f'{LOGIN}/web/qrcode/generate'
    QRCODE_POLL = f'{LOGIN}/web/qrcode/poll'


class Authorization:
    Cookie: Dict[str, str]

    SelfUid: int
    SelfUsername: str
    Token: str


class Message:
    TalkerId: str
    MsgContent: str
    Timestamp: int
    SenderUid: str
