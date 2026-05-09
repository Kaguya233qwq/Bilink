import asyncio

from .config import config, Config
from .connection.client import BilibiliClient
from .connection.api import BilibiliApi
from .core.session import MessageManager
from .utils.cookie import Cookie
from .utils.logger import Logger
from .core.plugin import load_all


class Bot:
    """Bilink 核心机器人实例"""

    def __init__(self) -> None:
        self.config: Config = config
        self.client: BilibiliClient = BilibiliClient(timeout=self.config.timeout)
        self.api: BilibiliApi = BilibiliApi(self.client)
        self.session_manager: MessageManager = MessageManager()

    async def _loop(self):
        """主轮询逻辑"""
        from .core.matcher import Matcher
        from .core.handler import handler

        while True:
            try:
                # 预检：如果根本没有任何未读消息，直接抛弃本次笨重的拉取，节省极大带宽和风控概率
                has_unread = await self.api.check_unread_msgs()
                if not has_unread:
                    await asyncio.sleep(self.config.poll_interval)
                    continue

                msgs = await self.api.fetch_msgs(self.session_manager)
                if not msgs:
                    await asyncio.sleep(self.config.poll_interval)
                    continue

                for msg in msgs:
                    Logger.debug(f"Process raw message: {msg}")
                    matcher = Matcher(bot=self, message=msg)
                    _ = asyncio.create_task(handler.handle_all(matcher))

                await asyncio.sleep(self.config.poll_interval)
            except Exception as e:
                Logger.error(f"消息轮询发生严重异常：{e}")
                await asyncio.sleep(5)

    async def start(self) -> None:
        """启动服务"""
        while True:
            # 检查cookie
            check = Cookie.check()
            if check:
                Cookie.load()
                # 验证cookie是否在有效期内
                if not await self.api.check_login_status():
                    Logger.warning("Cookie已过期或失效，需要重新扫码登录")
                    check = False
                    # 删除失效的Cookie缓存
                    Cookie.cookie_file.unlink(missing_ok=True)

            if not check:
                from .connection.login import login_by_qrcode

                token = await login_by_qrcode(self.client)
                if not token:
                    continue
                Cookie.save(token)
                Cookie.load()

            # 加载所有插件
            load_all()

            # 开启所有定时任务
            from .core.handler import handler

            handler.start_cron_jobs(self)

            break

        await self._loop()

    def run(self):
        """阻塞运行服务"""
        try:
            from .utils.tools import print_banner

            print_banner()
            Logger.info("start bilink server...")
            asyncio.run(self.start())
        except KeyboardInterrupt:
            Logger.info("server shutdown")
