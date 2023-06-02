import os
import json
from pathlib import Path

from .logger import Logger


class Cookies:
    """定义cookie类"""

    cache_path = r'BilinkCache'
    cookie_file = cache_path + r'\cookie.bc'

    @classmethod
    async def save(cls, cookie):
        try:
            if not os.path.exists(cls.cache_path):
                os.makedirs(cls.cache_path)
                with open(cls.cookie_file, 'a') as f:
                    f.close()
                Logger.success('缓存文件初始化成功')
            with open(cls.cookie_file, 'w') as f:
                cookie_ = json.dumps(cookie)
                f.write(cookie_)
                f.close()
            Logger.success('cookie文件保存成功')
        except Exception as e:
            Logger.error('cookie保存失败！%s' % e)

    @classmethod
    async def load(cls):
        try:
            with open(cls.cookie_file, 'r') as f:
                cookie_str = f.read()
                cookie = json.loads(cookie_str)
                f.close()
                Logger.success('cookie文件读取成功')
                return cookie
        except Exception as e:
            Logger.error('cookie读取失败！%s' % e)

    @classmethod
    async def check(cls):
        if Path(cls.cookie_file).is_file():
            return True
        else:
            return False

    @classmethod
    async def clear(cls):
        if Path(cls.cookie_file).is_file():
            Path(cls.cookie_file).unlink()
            Logger.success('cookie清除成功')
