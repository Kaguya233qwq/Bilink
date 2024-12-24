from . import server
from .login import login_by_qrcode
from ..utils.cookie import Cookie


async def run_forever() -> None:
    """
    启动服务
    """
    while True:
        check = Cookie.check()
        if check:
            Cookie.load()
            await server.run()
        else:
            token = await login_by_qrcode()
            if token:
                Cookie.save(token)
