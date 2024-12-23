import os
import json
from pathlib import Path

from .logger import Logger
from ..models import Authorization


class Cookies:
    """定义cookie类"""

    cache_path = r'BilinkCache'
    cookie_file = cache_path + r'\cookie'

    @classmethod
    def save(cls, cookie) -> None:
        """
        保存cookie
        """
        try:
            if not os.path.exists(cls.cache_path):
                os.makedirs(cls.cache_path)
                with open(cls.cookie_file, 'a') as f:
                    f.close()
                Logger.success('Initializing cookie file..')
            with open(cls.cookie_file, 'w') as f:
                cookie_ = json.dumps(cookie)
                f.write(cookie_)
                f.close()
        except Exception as e:
            Logger.error(f'Cookie saving failed: {e}')

    @classmethod
    def load(cls) -> None:
        """
        读取cookie
        """
        try:
            with open(cls.cookie_file, 'r') as f:
                cookie_str = f.read()
                cookie: dict = json.loads(cookie_str)
                Authorization.Cookie = cookie
                Authorization.Token = cookie.get('bili_jct')
                Authorization.SelfUid = int(cookie.get('DedeUserID'))
        except Exception as e:
            Logger.error(f'Cookie loading failed: {e}')

    @classmethod
    def check(cls) -> bool:
        """
        检查cookie
        """
        if Path(cls.cookie_file).is_file():
            return True
        else:
            return False

    @classmethod
    def clear(cls) -> None:
        """
        清除cookie
        """
        if Path(cls.cookie_file).is_file():
            Path(cls.cookie_file).unlink()
            Logger.success('Cookie cleared successful')
