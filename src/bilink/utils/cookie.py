import json
from pathlib import Path
from typing import Dict

from .logger import Logger
from .exception import CookieCacheNotFoundError
from .models import Authorization
from ..config import config


class Cookie:
    """cookie类"""

    cache_path = Path(config.cache_dir)
    cookie_file = cache_path / ".userdata"

    @staticmethod
    def save(cookie: Dict[str, str]) -> None:
        """
        保存cookie
        """

        if not Cookie.cache_path.exists():
            Cookie.cache_path.mkdir(parents=True, exist_ok=True)
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
            cookie: Dict[str, str] = json.loads(cookie_str)
            Authorization.Cookie = cookie
            Authorization.Token = cookie.get("bili_jct", "")
            Authorization.SelfUid = int(cookie.get("DedeUserID", 0))

    @staticmethod
    def check() -> bool:
        """
        检查cookie
        """
        return Cookie.cookie_file.exists()

    @staticmethod
    def clear() -> None:
        """
        清除cookie
        """
        if Cookie.cookie_file.exists():
            Cookie.cookie_file.unlink()
            Logger.success("Cookie cleared successfully")
