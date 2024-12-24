from asyncio import sleep

from ..utils.logger import Logger
from ..utils.tools import print_banner
from .. import message
from ..message import Matcher
from ..models import Message


async def run():
    """轮询获取最新消息并进行比对"""
    print_banner()
    Logger.info("bilibili消息助手正在运行...")
    while True:
        msg: Message = await message.fetch_msg()
        # # 判断是否加载最新的消息体对象
        if not message.latest_msg.Timestamp:
            # 如果没有初始化则初始化最新消息变量
            message.latest_msg = msg
        else:
            # 实例化一个matcher，继续匹配命令或要发送的内容
            matcher = Matcher(msg)
            if matcher.is_new_msg():
                # 如果是新消息，触发所有注册的发送hook
                pass
            await sleep(2)
