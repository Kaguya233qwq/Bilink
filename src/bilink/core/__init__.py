from ..login.qr_scan import login_by_qrcode
from ..utils import server
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
            cookies.save(token)
