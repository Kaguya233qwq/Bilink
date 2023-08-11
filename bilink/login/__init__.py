from .qr_scan import login_by_qrcode
from ..utils import listening
from ..utils.cookies import Cookies
from ..utils.logger import Logger


async def login() -> None:
    """
    通用bilibili登录
    :return:
    """
    cookies = Cookies()
    check = await cookies.check()
    if check:
        cookies_ = await cookies.load()
        try:
            listening.run(cookies_)
        except Exception as e:
            Logger.error('发生问题：%s' % e)
            await cookies.clear()
    else:
        await login_by_qrcode()
