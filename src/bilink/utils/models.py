from typing import Dict

HOST = "https://api.vc.bilibili.com"
LOGIN = "http://passport.bilibili.com/x/passport-login"


class Api:
    """可调用api的全局变量"""

    GET_SESSIONS: str = f"{HOST}/session_svr/v1/session_svr/get_sessions?session_type=1"
    FETCH_SESSION_MSGS: str = f"{HOST}/svr_sync/v1/svr_sync/fetch_session_msgs"
    SEND_MSG: str = f"{HOST}/web_im/v1/web_im/send_msg"
    NEW_SESSIONS: str = f"{HOST}/session_svr/v1/session_svr/new_sessions"
    "?begin_ts=1668417681186054&build=0&mobi_app=web"

    QRCODE_GENERATE: str = f"{LOGIN}/web/qrcode/generate"
    QRCODE_POLL: str = f"{LOGIN}/web/qrcode/poll"


class Authorization:
    """身份验证model"""

    Cookie: Dict[str, str]

    SelfUid: int
    SelfUsername: str
    Token: str
