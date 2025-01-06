from asyncio import sleep

from .message import Message, fetch_msg
from .matcher import Matcher
from .handler import handler


async def run():
    """轮询获取最新消息并进行处理"""
    while True:
        # 获取并初始化最新的消息
        msg: Message = await fetch_msg()
        # 实例化一个matcher，匹配消息内容
        matcher = Matcher(msg)
        if matcher.is_new_msg:
            # 如果是新消息则尝试触发所有的handler
            await handler.handle_all(matcher)
        await sleep(2)
