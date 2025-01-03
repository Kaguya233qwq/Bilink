from . import server
from .login import login_by_qrcode
from ..utils.cookie import Cookie


async def run_forever() -> None:
    """
    启动服务
    """
    # 检查cookie
    check = Cookie.check()
    if not check:
        token = await login_by_qrcode()
        if token:
            Cookie.save(token)
    # 加载cookie
    Cookie.load()
    # 启动服务
    await server.run()
