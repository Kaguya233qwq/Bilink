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
    while True:
        await message.fetch_msgs()
        await message.auto_reply('你好', '(*´▽｀)ノノ你好鸭~~')
        Message.LastTimestamp = Message.Timestamp
        await sleep(2)
