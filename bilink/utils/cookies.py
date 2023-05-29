import os
import json
from pathlib import Path

from ..login.qr_scan import Login
from .logger import Logger


class Cookies:
    """定义cookie类"""

    def __init__(self):
        self.cache_path = r'BilinkCache'
        self.cookie_file = self.cache_path + r'\cookie.bc'

    @staticmethod
    async def get_cookie():
        qrcode = await Login.get_qrcode()
        if qrcode:
            url = qrcode.get('url')
            key = qrcode.get('key')
            await Login.save_qrcode(url)
            cookies = await Login.polling(key)
            return cookies
        else:
            return None

    async def save_cookie(self, cookie):
        try:
            if not os.path.exists(self.cache_path):
                os.makedirs(self.cache_path)
                with open(self.cookie_file, 'a') as f:
                    f.close()
                Logger.success('缓存文件初始化成功')
            with open(self.cookie_file, 'w') as f:
                cookie_ = json.dumps(cookie)
                f.write(cookie_)
                f.close()
            Logger.success('cookie文件保存成功')
        except Exception as e:
            Logger.error('cookie保存失败！%s' % e)

    async def load_cookie(self):
        try:
            with open(self.cookie_file, 'r') as f:
                cookie_str = f.read()
                cookie = json.loads(cookie_str)
                f.close()
                Logger.success('cookie文件读取成功')
                return cookie
        except Exception as e:
            Logger.error('cookie读取失败！%s' % e)

    async def check(self):
        if Path(self.cookie_file).is_file():
            return True
        else:
            return False

    async def delete(self):
        if Path(self.cookie_file).is_file():
            Path(self.cookie_file).unlink()
            Logger.success('cookie清除成功')
        else:
            Logger.info('cookie文件不存在，无需删除')
