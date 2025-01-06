import asyncio

from .core import start_server
from .utils.logger import Logger
from .utils.tools import print_banner


def run_forever():
    try:
        print_banner()
        Logger.info("start bilink server...")
        asyncio.run(start_server())
    except KeyboardInterrupt:
        Logger.info("server shutdown")
