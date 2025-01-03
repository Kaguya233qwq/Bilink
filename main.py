import asyncio

from src.bilink.core import run_forever
from src.bilink.utils.logger import Logger
from src.bilink.utils.tools import print_banner

if __name__ == "__main__":
    try:
        print_banner()
        Logger.info("start bilink server...")
        asyncio.run(run_forever())
    except KeyboardInterrupt:
        Logger.info("server shutdown")
