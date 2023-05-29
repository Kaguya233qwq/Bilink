from .login.qr_scan import Login as Login

from .login.qr_scan import Login as Login
from .utils import listening
from .utils.cookies import Cookies
from .utils.logger import Logger


async def running():
    """自动判断登录方式"""
    cookies = Cookies()
    check = await cookies.check()
    if check:
        cookies_ = await cookies.load_cookie()
        try:
            listening.run(cookies_)
        except Exception as e:
            Logger.error('发生问题：%s' % e)
            await cookies.delete()
    else:
        while True:
            cookies_ = await cookies.get_cookie()
            if cookies_:
                await cookies.save_cookie(cookies_)
                listening.run(cookies_)
            else:
                Logger.error('获取二维码失败！请联系开发者反馈问题')
                break
