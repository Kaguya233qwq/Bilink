from . import server, plugin
from .login import login_by_qrcode
from ..utils.cookie import Cookie


async def start_server() -> None:
    """
    启动服务
    """
    while True:
        # 检查cookie
        check = Cookie.check()
        if not check:
            token = await login_by_qrcode()
            if not token:
                continue
            Cookie.save(token)
        else:
            # 加载cookie
            Cookie.load()
            # 加载所有插件
            plugin.load_all()
            # 启动服务
            await server.run()
