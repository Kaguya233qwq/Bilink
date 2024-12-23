import json
from pathlib import Path

from .logger import Logger
from .exception import CookieCacheNotFoundError
from ..models import Authorization


class Cookie:
    """cookie类"""

    cache_path = Path("bilink_cache")
    cookie_file = cache_path / ".userdata"

    @staticmethod
    def save(cookie: dict) -> None:
        """
        保存cookie
        """

        if not Cookie.cache_path.exists():
            Path(Cookie.cache_path).mkdir()
        with open(Cookie.cookie_file, "w") as f:
            cookie_ = json.dumps(cookie)
            f.write(cookie_)

    @staticmethod
    def load() -> None:
        """
        读取cookie
        """
        if not Cookie.cookie_file.exists():
            raise CookieCacheNotFoundError("cookie文件不存在！")
        with open(Cookie.cookie_file, "r") as f:
            cookie_str = f.read()
            cookie: dict = json.loads(cookie_str)
            Authorization.Cookie = cookie
            Authorization.Token = cookie.get("bili_jct")
            Authorization.SelfUid = int(cookie.get("DedeUserID"))

    @staticmethod
    def check() -> bool:
        """
        检查cookie
        """
        if Cookie.cookie_file.exists():
            return True
        else:
            return False

    @staticmethod
    def clear() -> None:
        """
        清除cookie
        """
        if Path(Cookie.cookie_file).exists():
            Path(Cookie.cookie_file).unlink()
            Logger.success("Cookie cleared successfully")
