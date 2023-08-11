from .qr_scan import login_by_qrcode
from ..utils import server
from ..utils.cookies import Cookies
from ..utils.logger import Logger


async def login() -> None:
    """
    通用bilibili登录
    :return:
    """
    cookies = Cookies()
    while True:
        check = cookies.check()
        if check:
            cookies.load()
            try:
                server.run()
            except Exception as e:
                Logger.error(f'发生问题：{e}')
                break
        else:
            token = await login_by_qrcode()
            cookies.save(token)
