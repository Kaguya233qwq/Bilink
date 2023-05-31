import asyncio
from typing import Union

from .qr_scan import Login
from ..utils.logger import Logger


def login() -> Union[None, dict[str:str]]:
    """

    通用bilibili扫码登录

    """
    qrcode = asyncio.run(Login.get_qrcode())
    if qrcode:
        url = qrcode.get('url')
        key = qrcode.get('key')
        await Login.save_qrcode(url)  # 保存二维码图片并输出至终端
        Logger.success('二维码生成成功，请使用bilibili客户端扫描确认')
        cookies: dict = await Login.polling(key)
        if cookies:
            return cookies
        else:
            Logger.error('未能返回正确数据，登陆失败')
            return None
    else:
        return None
