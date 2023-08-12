import sys
from asyncio import sleep
from .logger import Logger
from .tools import create_banner
from .. import message
from ..models import Message


async def run():
    await message.fetch_msgs()
    Message.LastTimestamp = Message.Timestamp
    create_banner()
    Logger.info("bilibili消息助手正在运行...")
    try:
        while True:
            await message.fetch_msgs()
            await message.auto_reply('你好', '(*´▽｀)ノノ你好鸭~~')
            Message.LastTimestamp = Message.Timestamp
            await sleep(2)
    except KeyboardInterrupt:
        Logger.info('进程被用户手动终止')
        sys.exit()
