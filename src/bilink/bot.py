from __future__ import annotations

import asyncio

from .config import Config, config
from .connection.api import BilibiliApi
from .connection.client import BilibiliClient
from .core.plugin import load_all
from .core.session import MessageManager
from .utils.cookie import Cookie
from .utils.logger import Logger


class Bot:
    """Bilink 核心机器人实例"""

    def __init__(self) -> None:
        self.config: Config = config
        self.client: BilibiliClient = BilibiliClient(timeout=self.config.timeout)
        self.api: BilibiliApi = BilibiliApi(self.client)
        self.session_manager: MessageManager = MessageManager()

    async def _ensure_login(self) -> None:
        while True:
            if Cookie.check():
                Cookie.load()
                if await self.api.check_login_status():
                    return

                Logger.warning("Cookie Expired. Need to re-login via QR Code.")
                Cookie.cookie_file.unlink(missing_ok=True)

            from .connection.login import login_by_qrcode

            token = await login_by_qrcode(self.client)
            if not token:
                continue

            Cookie.save(token)
            Cookie.load()
            return

    async def _loop(self) -> None:
        from .core.handler import handler
        from .core.matcher import Matcher

        while True:
            try:
                if not await self.api.check_unread_msgs():
                    await asyncio.sleep(self.config.poll_interval)
                    continue

                msgs = await self.api.fetch_msgs(self.session_manager)
                if not msgs:
                    await asyncio.sleep(self.config.poll_interval)
                    continue

                for msg in msgs:
                    Logger.debug(f"Process raw message: {msg}")
                    matcher = Matcher(bot=self, message=msg)
                    asyncio.create_task(handler.handle_all(matcher))

                await asyncio.sleep(self.config.poll_interval)
            except Exception as e:
                Logger.error(f"Polling critical error: {e}")
                await asyncio.sleep(5)

    async def start(self) -> None:
        await self._ensure_login()
        load_all()

        from .core.handler import handler

        handler.start_cron_jobs(self)

        await self._loop()

    def run(self) -> None:
        from .utils.tools import print_banner

        try:
            print_banner()
            Logger.info("start bilink server...")
            asyncio.run(self.start())
        except KeyboardInterrupt:
            Logger.info("server shutdown")
