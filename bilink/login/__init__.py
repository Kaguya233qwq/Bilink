from .qr_scan import login_by_qrcode
from ..utils import server
from ..utils.cookies import Cookies


async def login() -> None:
    """
    通用bilibili登录
    :return:
    """
    cookies = Cookies()
    while True:
        try:
            check = cookies.check()
            if check:
                cookies.load()
                await server.run()
            else:
                token = await login_by_qrcode()
                cookies.save(token)
        except KeyboardInterrupt:
            print('用户退出')
