from pydantic import BaseModel, Field

HOST = "https://api.vc.bilibili.com"
LOGIN = "http://passport.bilibili.com/x/passport-login"


class ApiConfig:
    """可调用api的全局变量"""

    GET_SESSIONS: str = f"{HOST}/session_svr/v1/session_svr/get_sessions?session_type=1"
    SINGLE_UNREAD: str = f"{HOST}/session_svr/v1/session_svr/single_unread"
    FETCH_SESSION_MSGS: str = f"{HOST}/svr_sync/v1/svr_sync/fetch_session_msgs"
    SEND_MSG: str = f"{HOST}/web_im/v1/web_im/send_msg"
    NEW_SESSIONS: str = f"{HOST}/session_svr/v1/session_svr/new_sessions?begin_ts=1668417681186054&build=0&mobi_app=web"

    QRCODE_GENERATE: str = f"{LOGIN}/web/qrcode/generate"
    QRCODE_POLL: str = f"{LOGIN}/web/qrcode/poll"
    NAV: str = "https://api.bilibili.com/x/web-interface/nav"

    USER_CARD: str = "https://api.bilibili.com/x/web-interface/card"
    RELATION_FANS: str = "https://api.bilibili.com/x/relation/fans"
    FAV_FOLDERS: str = "https://api.bilibili.com/x/v3/fav/folder/created/list-all"
    FAV_RESOURCES: str = "https://api.bilibili.com/x/v3/fav/resource/list"
    PLAY_URL: str = "https://api.bilibili.com/x/player/playurl"


Api = ApiConfig()


class _Authorization(BaseModel):
    """身份验证model"""

    Cookie: dict[str, str] = Field(default_factory=dict)
    SelfUid: int = Field(default=0)
    SelfUsername: str = Field(default="")
    Token: str = Field(default="")


Authorization = _Authorization()
