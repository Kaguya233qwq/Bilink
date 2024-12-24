from . import server
from .login import login_by_qrcode
from ..utils.cookie import Cookie


async def run_forever() -> None:
    """
    启动服务
    """
    cookies = Cookie()
    while True:
        check = cookies.check()
        if check:
            cookies.load()
            await server.run()
        else:
            token = await login_by_qrcode()
            if token:
                cookies.save(token)
