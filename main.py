import asyncio

from src.bilink.core import run_forever
from src.bilink.utils.logger import Logger

if __name__ == "__main__":
    try:
        asyncio.run(run_forever())
    except KeyboardInterrupt:
        Logger.info("server shutdown")
