from asyncio import sleep

from .message import Message, fetch_msg
from .matcher import Matcher


async def run():
    """轮询获取最新消息并进行比对"""
    while True:
        # 获取并初始化最新的消息
        msg: Message = await fetch_msg()
        # 实例化一个matcher，匹配消息内容
        matcher = Matcher(msg)
        # # 注册钩子函数
        # matcher.add_hook()
        
        # # 注册处理函数
        # matcher.add_handler()
        await sleep(2)
